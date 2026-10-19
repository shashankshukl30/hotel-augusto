from pathlib import Path
import json, shutil, hashlib
from PIL import Image

ROOT=Path(__file__).resolve().parent
PUBLIC=ROOT.parents[1]/'public'/'images'
manifest=json.loads((ROOT/'asset-manifest.json').read_text(encoding='utf-8'))
checks=[]
for entry in manifest['assets']:
    original=ROOT/entry['original']
    assert original.is_file(),str(original)
    assert hashlib.sha256(original.read_bytes()).hexdigest()==entry['sha256'],str(original)
    with Image.open(original) as im: im.verify()
    if 'public_path' in entry:
        public=PUBLIC/Path(entry['public_path']).name
        with Image.open(public) as im: im.verify()
        checks.append({'path':str(public),'bytes':public.stat().st_size})
before={drive:shutil.disk_usage(drive+':/').free for drive in ['C','D']}
removed=[]
for name in ['booking-page.md','makemytrip-page.md','hotels-page.md','goibibo-page.md']:
    path=ROOT/name
    if not path.exists(): continue
    assert path.resolve().parent==ROOT
    assert not path.is_symlink() and not path.is_junction()
    assert not any(p.is_symlink() or p.is_junction() for p in path.parents)
    removed.append({'path':str(path),'bytes':path.stat().st_size,'reason':'Disposable failed page extraction: irrelevant search results, 200-OK placeholder, or bot verification page; source URLs and access limitations are retained in asset research notes.'})
    path.unlink()
after={drive:shutil.disk_usage(drive+':/').free for drive in ['C','D']}
report={'date':'2026-10-19','start_of_asset_task_free_bytes':{'C':30069055488,'D':69505159168},'cleanup_before_free_bytes':before,'cleanup_after_free_bytes':after,'removed':removed,'removed_bytes':sum(x['bytes'] for x in removed),'original_hashes_verified':len(manifest['assets']),'public_images_opened':checks,'note':'Parallel website work may change drive free space during asset collection. All 77 downloaded original assets and editable asset scripts are retained; no dependencies, user files, or sibling projects were removed.'}
(ROOT/'asset-validation-cleanup.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'verified_originals':len(manifest['assets']),'verified_web_assets':len(checks),'removed_bytes':report['removed_bytes'],'free_bytes_after':after},indent=2))
