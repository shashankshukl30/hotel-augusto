from pathlib import Path
import json, hashlib
from PIL import Image,ImageOps

ROOT=Path(__file__).resolve().parent
PUBLIC=ROOT.parents[1]/'public'/'images'
manifest=json.loads((ROOT/'asset-manifest.json').read_text(encoding='utf-8'))
new=[
{'id':'kashi-vishwanath-2025','source_page':'https://commons.wikimedia.org/wiki/File:Kashi_Vishwanath_Temple_in_2025.jpg','url':'https://upload.wikimedia.org/wikipedia/commons/3/38/Kashi_Vishwanath_Temple_in_2025.jpg','author':'Pradum Shukla','rights':'CC BY 4.0','license_url':'https://creativecommons.org/licenses/by/4.0/','category':'destination','public_path':'/images/kashi-vishwanath.webp','alt':'The golden spire and courtyard of Shri Kashi Vishwanath Temple in Varanasi.','changes':'WebP conversion; may be cropped responsively in page layout. No photographic content altered.'},
{'id':'kashi-vishwanath','source_page':'https://commons.wikimedia.org/wiki/File:Shri_Kashi_Vishwanath_Temple.jpg','url':'https://upload.wikimedia.org/wikipedia/commons/f/ff/Shri_Kashi_Vishwanath_Temple.jpg','author':'Gannu03','rights':'CC BY-SA 4.0','license_url':'https://creativecommons.org/licenses/by-sa/4.0/','category':'destination','selection_status':'Research only. Side-lane spire view; not used on website.'},
{'id':'kashi-vishwanath-main','source_page':'https://commons.wikimedia.org/wiki/File:Shree_Kashi_Vishwanath_temple.jpg','url':'https://upload.wikimedia.org/wikipedia/commons/d/dd/Shree_Kashi_Vishwanath_temple.jpg','author':'Thenerdatul','rights':'CC BY 4.0','license_url':'https://creativecommons.org/licenses/by/4.0/','category':'destination','selection_status':'Research only. Entrance arch view; not used on website.'}
]
for entry in new:
    file=ROOT/'originals'/(entry['id']+'.jpg')
    im=ImageOps.exif_transpose(Image.open(file)).convert('RGB')
    entry.update(kind='destination',original=str(file.relative_to(ROOT)),width=im.width,height=im.height,bytes=file.stat().st_size,sha256=hashlib.sha256(file.read_bytes()).hexdigest())
    if 'public_path' in entry:
        target=PUBLIC/Path(entry['public_path']).name
        im.save(target,quality=88,method=6)
        entry.update(public_width=im.width,public_height=im.height,public_bytes=target.stat().st_size)
    manifest['assets']=[a for a in manifest['assets'] if a['id']!=entry['id']]+[entry]
for entry in manifest['assets']:
    if entry['id'] in ['varanasi-ghats','ganges-dawn','ganges-boats']:
        target=PUBLIC/(entry['id']+'.webp')
        entry.update(public_path='/images/'+target.name,public_width=entry['width'],public_height=entry['height'],public_bytes=target.stat().st_size,changes='WebP conversion; no photographic content altered.')
    if entry['id']=='ganges-boats':
        entry['description_note']='Photographer description states Boating at Ganga at Sunrise, varanasi; automated Unsplash slug says sunset. Use warm-light wording if desired.'
manifest.update(photography_policy='Only genuine hotel listing photography and licensed destination photography. No generative hotel images, removed watermarks, or unrelated hotel stand-ins.',logo_status='No usable first-party logo file retrieved. Official site is a Booking.com redirect. Use an original typographic hotel wordmark without claiming it is a recovered client logo.')
(ROOT/'asset-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('Finalized',len(manifest['assets']),'source records and',len(list(PUBLIC.glob('*.webp'))),'public web images.')
