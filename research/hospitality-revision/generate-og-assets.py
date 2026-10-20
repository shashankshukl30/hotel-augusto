"""Create tracked, reproducible OG dependencies from existing property and OFL assets."""
import hashlib
import json
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image, ImageFont

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "research" / "hospitality-revision"
FONTS = ROOT / "public" / "fonts"
FONTS.mkdir(exist_ok=True)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def oklch_hex(lightness, chroma, hue):
    a = chroma * math.cos(math.radians(hue))
    b = chroma * math.sin(math.radians(hue))
    l = (lightness + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (lightness - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (lightness - 0.0894841775 * a - 1.2914855480 * b) ** 3
    linear = [4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
              -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
              -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s]
    srgb = [12.92 * c if c <= .0031308 else 1.055 * c ** (1 / 2.4) - .055 for c in linear]
    return "#" + "".join(f"{round(max(0, min(1, c)) * 255):02x}" for c in srgb)


palette = {
    "paper": oklch_hex(.965, .014, 80),
    "ink": oklch_hex(.25, .026, 250),
    "bronze": oklch_hex(.47, .065, 65),
    "muted": oklch_hex(.48, .023, 70),
}
manifest = {
    "generated": datetime.now(timezone.utc).isoformat(),
    "purpose": "Hotel Augusto Open Graph image and favicon in the hospitality visual system",
    "generator": "research/hospitality-revision/generate-og-assets.py",
    "palette": palette,
    "paletteNote": "sRGB equivalents of shared OKLCH theme tokens for ImageResponse/SVG compatibility.",
    "photo": {},
    "fonts": [],
}

photo_source = ROOT / "public" / "images" / "deluxe-room-blue.webp"
photo_output = ROOT / "public" / "images" / "augusto-og-room-v1.jpg"
with Image.open(photo_source) as original:
    image = original.convert("RGB")
    image.thumbnail((1200, 675), Image.Resampling.LANCZOS)
    image.save(photo_output, "JPEG", quality=87, optimize=True)
    dimensions = image.size
manifest["photo"] = {
    "source": str(photo_source.relative_to(ROOT)).replace("\\", "/"),
    "sourceSha256": digest(photo_source),
    "output": str(photo_output.relative_to(ROOT)).replace("\\", "/"),
    "outputSha256": digest(photo_output),
    "dimensions": dimensions,
    "bytes": photo_output.stat().st_size,
    "changes": "Downsampled from tracked 1600x900 WebP to 1200x675 JPEG for ImageResponse. No visual content added, removed or retouched. OG composition applies a responsive crop.",
    "sourcePage": "https://www.varanasihotels.org/augusto-varanasi.en.html",
    "originalSourceUrl": "https://www.varanasihotels.org/data/Photos/1920x1080/16875/1687586/1687586860.JPEG",
    "sourceLedger": "research/assets/asset-manifest.json",
    "rights": "Genuine Hotel Augusto public listing photograph. Client reuse rights remain subject to hotel confirmation.",
}

for package, weight, filename, family in [
    ("bodoni-moda", 400, "augusto-og-bodoni-400-v1.ttf", "Augusto OG Display"),
    ("manrope", 500, "augusto-og-manrope-500-v1.ttf", "Augusto OG Body"),
]:
    folder = ROOT / "node_modules" / "@fontsource-variable" / package
    source = folder / "files" / f"{package}-latin-wght-normal.woff2"
    font = instantiateVariableFont(TTFont(source), {"wght": weight}, inplace=False)
    font.flavor = None
    font.recalcTimestamp = False
    for entry in font["name"].names:
        replacements = {1: family, 2: "Regular", 4: family + " Regular",
                        6: family.replace(" ", "") + "-Regular", 16: family, 17: "Regular"}
        if entry.nameID in replacements:
            entry.string = replacements[entry.nameID].encode(entry.getEncoding(), errors="replace")
    output = FONTS / filename
    font.save(output)
    license_output = FONTS / f"{package}-OFL.txt"
    shutil.copyfile(folder / "LICENSE", license_output)
    manifest["fonts"].append({
        "sourcePackage": f"@fontsource-variable/{package}",
        "source": str(source.relative_to(ROOT)).replace("\\", "/"),
        "sourceSha256": digest(source),
        "output": str(output.relative_to(ROOT)).replace("\\", "/"),
        "outputSha256": digest(output),
        "bytes": output.stat().st_size,
        "weight": weight,
        "internalFamily": family,
        "changes": "Static weight instantiation, WOFF2 to TTF conversion, renamed internal font family for this derived asset. All copyright/license name records retained.",
        "license": "SIL Open Font License 1.1",
        "licenseFile": str(license_output.relative_to(ROOT)).replace("\\", "/"),
        "licenseSha256": digest(license_output),
    })

display = TTFont(FONTS / "augusto-og-bodoni-400-v1.ttf")
glyphs = display.getGlyphSet()
glyph_name = display.getBestCmap()[ord("A")]
bounds = BoundsPen(glyphs)
glyphs[glyph_name].draw(bounds)
x0, y0, x1, y1 = bounds.bounds
scale = 43 / (y1 - y0)
offset_x = 32 - (x0 + x1) * scale / 2
offset_y = 10.5 + y1 * scale
pen = SVGPathPen(glyphs)
glyphs[glyph_name].draw(TransformPen(pen, (scale, 0, 0, -scale, offset_x, offset_y)))
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="6" fill="{palette["bronze"]}"/><rect x="4.5" y="4.5" width="55" height="55" rx="3" fill="none" stroke="{palette["paper"]}" stroke-opacity=".5"/><path d="{pen.getCommands()}" fill="{palette["paper"]}" stroke="{palette["paper"]}" stroke-width=".25"/></svg>\n'
(ROOT / "app" / "icon.svg").write_text(svg, encoding="utf-8")
manifest["favicon"] = {"file": "app/icon.svg", "sha256": digest(ROOT / "app" / "icon.svg"),
                       "glyphSource": "Static OFL Bodoni Moda-derived A outline", "viewBox": [0, 0, 64, 64]}
font = ImageFont.truetype(str(FONTS / "augusto-og-bodoni-400-v1.ttf"), 86)
manifest["headlineWidthCheck"] = {text: font.getlength(text) for text in ["Your place", "in Kashi."]}
manifest["totalRuntimeDependencyBytes"] = photo_output.stat().st_size + sum(f["bytes"] for f in manifest["fonts"])
(HERE / "og-assets-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"palette": palette, "bytes": manifest["totalRuntimeDependencyBytes"],
                  "headlineWidths": manifest["headlineWidthCheck"]}))
