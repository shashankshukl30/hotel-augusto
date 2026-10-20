param(
  [Parameter(Mandatory=$true)][ValidatePattern('^\d+$')][string]$StoppedSession,
  [string]$ReportPath = 'evidence\dev-output-cleanup.json'
)
$ErrorActionPreference = 'Stop'
$taskRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$expectedRoot = 'D:\Digiocular\Websites\Hotel Augusto'
if ($taskRoot -ne $expectedRoot) { throw 'Unexpected project root' }
$taskReportPath = [IO.Path]::GetFullPath((Join-Path $taskRoot $ReportPath))
if (-not $taskReportPath.StartsWith("$expectedRoot\evidence\", [StringComparison]::OrdinalIgnoreCase)) { throw 'Report escapes evidence scope' }
if ([IO.Path]::GetExtension($taskReportPath) -ne '.json') { throw 'JSON report required' }
$taskReportParent = Split-Path -Parent $taskReportPath
if (-not (Test-Path -LiteralPath $taskReportParent -PathType Container)) { throw 'Report folder must already exist' }
for ($taskParent = Get-Item -LiteralPath $taskReportParent; $taskParent.FullName -ne $taskRoot; $taskParent = $taskParent.Parent) {
  if ($taskParent.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Report reparse point refused' }
}
$taskTarget = [IO.Path]::GetFullPath((Join-Path $taskRoot '.next\dev'))
if ($taskTarget -ne "$expectedRoot\.next\dev") { throw 'Unexpected cleanup target' }
if (-not (Test-Path -LiteralPath "$taskRoot\.next\BUILD_ID")) { throw 'Production build missing' }
if (-not (Test-Path -LiteralPath $taskTarget)) { Write-Output 'No inactive development output remains'; exit 0 }
foreach ($taskCheck in @($taskRoot, "$taskRoot\.next", $taskTarget)) {
  if ((Get-Item -LiteralPath $taskCheck -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse point refused' }
}
$taskEntries = @(Get-ChildItem -LiteralPath $taskTarget -Recurse -Force)
foreach ($taskEntry in $taskEntries) {
  if ($taskEntry.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Reparse point refused: $($taskEntry.FullName)" }
  if (-not $taskEntry.FullName.StartsWith($taskTarget + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Entry escapes scope' }
}
$taskFiles = @($taskEntries | Where-Object { -not $_.PSIsContainer })
$taskBefore = @{ C = (Get-PSDrive C).Free; D = (Get-PSDrive D).Free }
$taskProductionId = Get-Content -LiteralPath "$taskRoot\.next\BUILD_ID" -Raw
$taskReport = @{
  scope = $taskTarget
  reason = "Stopped task-owned next dev session $StoppedSession. Production preview uses .next/server and .next/static; .next/dev is generated, inactive, fully rebuildable development output."
  removed = @($taskFiles | ForEach-Object { @{ path = $_.FullName; bytes = $_.Length } })
  removedBytes = ($taskFiles | Measure-Object -Property Length -Sum).Sum
  freeBeforeBytes = $taskBefore
}
Remove-Item -LiteralPath $taskTarget -Recurse -Force
if ((Get-Content -LiteralPath "$taskRoot\.next\BUILD_ID" -Raw) -ne $taskProductionId) { throw 'Production identity changed' }
$taskResponse = Invoke-WebRequest -Uri 'http://127.0.0.1:3080' -UseBasicParsing
if ($taskResponse.StatusCode -ne 200 -or $taskResponse.Content -notmatch 'Your place') { throw 'Production preview verification failed' }
$taskReport.freeAfterBytes = @{ C = (Get-PSDrive C).Free; D = (Get-PSDrive D).Free }
$taskReport.productionVerifiedAfter = $true
$taskReport.completed = (Get-Date).ToUniversalTime().ToString('o')
$taskReport | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $taskReportPath -Encoding UTF8
@{ removedFiles = $taskFiles.Count; removedBytes = $taskReport.removedBytes; freeAfterBytes = $taskReport.freeAfterBytes; productionVerifiedAfter = $true } | ConvertTo-Json
