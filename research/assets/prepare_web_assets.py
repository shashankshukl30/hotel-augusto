from pathlib import Path
import json, hashlib
from PIL import Image, ImageOps

ROOT=Path(__file__).resolve().parent
PUBLIC=ROOT.parents[1]/'public'/'images'
selected=[
('1687586875','deluxe-room','rooms','A double room at Hotel Augusto with a cushioned headboard, white bedding and wood detailing.'),
('1687586846','twin-room','rooms','Two separate single beds with green runners in a Hotel Augusto twin room.'),
('1687586850','family-room','rooms','Two double beds and a seating area in a Hotel Augusto family room.'),
('1687586877','hotel-lobby','hotel','The entrance lounge and reception at Hotel Augusto, with sofas and warm ceiling lights.'),
('1687586880','hotel-lounge','hotel','Sofa seating beside the entrance hallway at Hotel Augusto.'),
('1687586879','hotel-reception','hotel','Hotel Augusto reception desk with wood panelling and patterned wall details.'),
('1687586892','hotel-exterior','hotel','Hotel Augusto illuminated entrance and street facade in Godowlia at night.'),
('1687586848','hotel-exterior-day','hotel','Hotel Augusto street facade and entrance in daylight.'),
('1687586868','dining-room','dining','The Hotel Augusto dining room with tables, upholstered chairs and a serving counter.'),
('1687586884','dining-room-wide','dining','A view along the tables and chairs of the Hotel Augusto dining room.'),
('1687586828','room-tea','details','An electric kettle, glasses and cups on the room tea tray at Hotel Augusto.'),
('1687586860','deluxe-room-blue','rooms','Hotel Augusto double room with a blue upholstered headboard and sofa.'),
('1687586838','family-room-alternate','rooms','A Hotel Augusto room with two double beds and brown upholstered headboards.'),
('1687586855','room-bathroom','details','A tiled private bathroom with a shower at Hotel Augusto.')
]
manifest=json.loads((ROOT/'asset-manifest.json').read_text(encoding='utf-8'))
index={r['id']:r for r in manifest['assets']}
for id,name,category,alt in selected:
    im=ImageOps.exif_transpose(Image.open(ROOT/'originals'/(id+'.jpg'))).convert('RGB')
    im.thumbnail((1600,1600),Image.Resampling.LANCZOS)
    target=PUBLIC/(name+'.webp')
    im.save(target,quality=86,method=6)
    index[id].update(public_path='/images/'+target.name,public_width=im.width,public_height=im.height,public_bytes=target.stat().st_size,category=category,alt=alt,verified='Visually checked contact sheets against Hotel Augusto listing; no removed watermarks, no substituted hotel.')
(ROOT/'asset-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('\n'.join('/images/'+s[1]+'.webp' for s in selected))
