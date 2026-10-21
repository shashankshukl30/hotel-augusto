"""Arrange QA screenshot slices for read-only alignment inspection."""
from math import ceil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 16)
for source in sorted(root.glob('alignment-chromium-*-full-page.png')):
    image = Image.open(source).convert('RGB')
    width, height = image.size
    if width not in (390, 1440):
        continue
    target = root / ('review-' + source.name.removeprefix('alignment-chromium-'))
    if target.exists() and target.stat().st_mtime >= source.stat().st_mtime:
        continue
    strip_height = 960 if width == 390 else 1100
    column_width = 280 if width == 390 else 720
    columns = 4 if width == 390 else 2
    count = ceil(height / strip_height)
    slice_height = round(strip_height * column_width / width)
    cell_height = slice_height + 28
    sheet = Image.new('RGB', (columns * (column_width + 12), ceil(count / columns) * cell_height), '#d8d8d8')
    draw = ImageDraw.Draw(sheet)
    for index in range(count):
        y = index * strip_height
        section = image.crop((0, y, width, min(y + strip_height, height)))
        section = section.resize((column_width, round(section.height * column_width / width)))
        x, top = (index % columns) * (column_width + 12), (index // columns) * cell_height
        draw.text((x + 3, top + 3), f'{index + 1}: y={y}', fill='#222222', font=font)
        sheet.paste(section, (x, top + 26))
    sheet.save(target)
    print(target.name, sheet.size)
