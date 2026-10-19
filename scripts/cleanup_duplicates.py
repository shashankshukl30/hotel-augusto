"""Remove only named, byte-identical task screenshot copies; retain all unique evidence."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PAIRS = [
    ('evidence/qa-problem-varanasi-390.png', 'evidence/independent-review/varanasi-390-top.png'),
    *[(f'evidence/independent-review/{route}-{width}-{kind}.png', f'evidence/contact-review/{route}-{width}-{kind}.png')
      for route in ['contact', 'privacy'] for width in [1440, 390] for kind in ['full', 'top']],
    ('research/design-qa/varanasi-390.png', 'evidence/independent-review/varanasi-390-full.png'),
]

def safe_path(relative):
    path = ROOT / relative
    assert path.resolve().is_relative_to(ROOT), path
    for part in [path, *path.parents]:
        assert not part.is_symlink(), part
        assert not (hasattr(part, 'is_junction') and part.is_junction()), part
        if part == ROOT:
            break
    return path

report_path = ROOT / 'evidence/storage-cleanup.json'
report = json.loads(report_path.read_text(encoding='utf-8')) if report_path.exists() else {
    'scope': str(ROOT), 'started': datetime.now(timezone.utc).isoformat(),
    'freeBeforeBytes': {d: shutil.disk_usage(d+':/').free for d in ['C','D']}, 'removed': []}
for duplicate, survivor in PAIRS:
    candidate, retained = safe_path(duplicate), safe_path(survivor)
    if not candidate.exists():
        continue
    assert candidate.is_file() and retained.is_file()
    digest = hashlib.sha256(candidate.read_bytes()).hexdigest()
    assert candidate.stat().st_size == retained.stat().st_size
    assert digest == hashlib.sha256(retained.read_bytes()).hexdigest()
    with Image.open(retained) as photo:
        photo.load()
    entry = {'path': str(candidate), 'bytes': candidate.stat().st_size,
             'reason': 'Task-generated screenshot duplicate; identical original evidence retained and decoded.',
             'retainedCopy': str(retained), 'sha256': digest}
    candidate.unlink()
    assert retained.is_file() and hashlib.sha256(retained.read_bytes()).hexdigest() == digest
    report['removed'].append(entry)
report['removedBytes'] = sum(item['bytes'] for item in report['removed'])
report['freeAfterBytes'] = {d: shutil.disk_usage(d+':/').free for d in ['C','D']}
report['completed'] = datetime.now(timezone.utc).isoformat()
report['preserved'] = ['All source and dependencies', 'All original and optimized hotel/destination assets',
                       'All unique research and verification evidence', 'Active production build', 'Editable handoff files']
report_path.write_text(json.dumps(report, indent=2),encoding='utf-8')
print(json.dumps({'removedFiles':len(report['removed']),'removedBytes':report['removedBytes'],
                  'freeBeforeBytes':report['freeBeforeBytes'],'freeAfterBytes':report['freeAfterBytes']}))
