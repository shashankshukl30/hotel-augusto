$ErrorActionPreference = 'Stop'
$taskRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$expectedRoot = 'D:\Digiocular\Websites\Hotel Augusto'
if ($taskRoot -ne $expectedRoot) { throw 'Unexpected project root' }
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
  reason = 'Stopped task-owned next dev session 94264. Production preview uses .next/server and .next/static; .next/dev is generated, inactive, fully rebuildable development output.'
  removed = @($taskFiles | ForEach-Object { @{ path = $_.FullName; bytes = $_.Length } })
  removedBytes = ($taskFiles | Measure-Object -Property Length -Sum).Sum
  freeBeforeBytes = $taskBefore
}
Remove-Item -LiteralPath $taskTarget -Recurse -Force
if ((Get-Content -LiteralPath "$taskRoot\.next\BUILD_ID" -Raw) -ne $taskProductionId) { throw 'Production identity changed' }
$taskResponse = Invoke-WebRequest -Uri 'http://127.0.0.1:3080' -UseBasicParsing
if ($taskResponse.StatusCode -ne 200 -or $taskResponse.Content -notmatch 'Varanasi, up close') { throw 'Production preview verification failed' }
$taskReport.freeAfterBytes = @{ C = (Get-PSDrive C).Free; D = (Get-PSDrive D).Free }
$taskReport.productionVerifiedAfter = $true
$taskReport.completed = (Get-Date).ToUniversalTime().ToString('o')
$taskReport | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath "$taskRoot\evidence\dev-output-cleanup.json" -Encoding UTF8
@{ removedFiles = $taskFiles.Count; removedBytes = $taskReport.removedBytes; freeAfterBytes = $taskReport.freeAfterBytes; productionVerifiedAfter = $true } | ConvertTo-Json
