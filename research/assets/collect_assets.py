from pathlib import Path
import re, json, hashlib, shutil, subprocess
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import requests
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT.parents[1] / 'public' / 'images'
ORIGINALS = ROOT / 'originals'
ORIGINALS.mkdir(exist_ok=True)
PUBLIC.mkdir(exist_ok=True, parents=True)
page = (ROOT / 'varanasihotels-page.html').read_text(encoding='utf-8')
paths = list(dict.fromkeys(re.findall(r'/data/Photos/1920x1080/[^\s"<>]+', page)))
items = [{'id': Path(p).stem, 'url': 'https://www.varanasihotels.org' + p,
          'source_page': 'https://www.varanasihotels.org/augusto-varanasi.en.html',
          'kind': 'hotel', 'rights': 'Hotel listing photography; ownership and client reuse rights require confirmation.'} for p in paths]
items += [
    {'id':'varanasi-ghats','url':'https://images.unsplash.com/photo-1771313018650-254f6b5f2c91?auto=format&fit=max&fm=jpg&q=90&w=2400',
     'source_page':'https://unsplash.com/photos/boats-on-a-river-with-city-buildings-in-background-_IdOI0J_doY','kind':'destination','author':'Rudra Gupta','rights':'Unsplash License','license_url':'https://unsplash.com/license'},
    {'id':'ganges-dawn','url':'https://images.unsplash.com/photo-1768844335653-7593a132c203?auto=format&fit=max&fm=jpg&q=90&w=2400',
     'source_page':'https://unsplash.com/photos/two-boats-on-a-wide-river-at-sunrise-Sj6zqvbuykY','kind':'destination','author':'Subhra Jyoti Paul','rights':'Unsplash License','license_url':'https://unsplash.com/license'},
    {'id':'ganges-boats','url':'https://images.unsplash.com/photo-1677047759978-8782844a3d3a?auto=format&fit=max&fm=jpg&q=90&w=2400',
     'source_page':'https://unsplash.com/photos/two-people-in-a-small-boat-on-the-water-at-sunset-y4oZkoD6RYY','kind':'destination','author':'ARTO SURAJ','rights':'Unsplash License','license_url':'https://unsplash.com/license'}
]

def fetch(item):
    target = ORIGINALS / (item['id'] + '.jpg')
    try:
        if not target.exists():
            response = subprocess.run(['curl.exe','-f','-L','--max-time','30','-s',item['url']],capture_output=True,check=True)
            im = Image.open(BytesIO(response.stdout))
            im.verify()
            target.write_bytes(response.stdout)
        im = Image.open(target)
        item.update(width=im.width,height=im.height,bytes=target.stat().st_size,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),original=str(target.relative_to(ROOT)))
        return item
    except Exception as e:
        item['error'] = str(e)
        return item

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(fetch,items))
(ROOT/'asset-manifest.json').write_text(json.dumps({'retrieved':'2026-10-19','assets':results},indent=2),encoding='utf-8')
good = [r for r in results if 'error' not in r]
for offset in range(0,len(good),24):
    batch=good[offset:offset+24]
    sheet=Image.new('RGB',(1200,((len(batch)+3)//4)*225),'#e8e3da')
    draw=ImageDraw.Draw(sheet)
    for i,item in enumerate(batch):
        im=Image.open(ORIGINALS/(item['id']+'.jpg')).convert('RGB')
        thumb=ImageOps.contain(im,(290,190))
        x=(i%4)*300+(300-thumb.width)//2
        y=(i//4)*225
        sheet.paste(thumb,(x,y))
        draw.text(((i%4)*300+8,y+194),item['id']+' '+str(item['width'])+'x'+str(item['height']),fill='#282b23')
    sheet.save(ROOT/('contact-sheet-'+str(offset//24+1)+'.jpg'),quality=90)
for item in good:
    if item['kind']=='destination':
        im=Image.open(ORIGINALS/(item['id']+'.jpg')).convert('RGB')
        im.save(PUBLIC/(item['id']+'.webp'),quality=85,method=6)
print(json.dumps({'downloaded':len(good),'failed':[r['id'] for r in results if 'error' in r], 'total_bytes':sum(r['bytes'] for r in good)},indent=2))
