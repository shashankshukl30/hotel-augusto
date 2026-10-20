"""Create the static OFL Inter derivative; preserve supplied logo and photograph."""
import hashlib
import json
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import ImageFont

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def color(lightness, chroma, hue):
    a, b = chroma * math.cos(math.radians(hue)), chroma * math.sin(math.radians(hue))
    l = (lightness + .3963377774 * a + .2158037573 * b) ** 3
    m = (lightness - .1055613458 * a - .0638541728 * b) ** 3
    s = (lightness - .0894841775 * a - 1.291485548 * b) ** 3
    linear = [4.0767416621*l - 3.3077115913*m + .2309699292*s,
              -1.2684380046*l + 2.6097574011*m - .3413193965*s,
              -.0041960863*l - .7034186147*m + 1.707614701*s]
    values = [12.92*c if c <= .0031308 else 1.055*c**(1/2.4)-.055 for c in linear]
    return "#" + "".join(f"{round(max(0,min(1,c))*255):02x}" for c in values)


palette = {"paper": color(.991,.001,260), "ink": color(.225,.006,260),
           "muted": color(.49,.009,260), "accent": color(.515,.19,255)}
source = ROOT / "node_modules/@fontsource-variable/inter/files/inter-latin-wght-normal.woff2"
destination = ROOT / "public/fonts/augusto-og-inter-600-v1.ttf"
license_source = ROOT / "node_modules/@fontsource-variable/inter/LICENSE"
license_destination = ROOT / "public/fonts/inter-OFL.txt"
font = instantiateVariableFont(TTFont(source), {"wght": 600}, inplace=False)
font.flavor = None
font.recalcTimestamp = False
names = {1: "Augusto OG Sans", 2: "Semibold", 4: "Augusto OG Sans Semibold",
         6: "AugustoOGSans-Semibold", 16: "Augusto OG Sans", 17: "Semibold"}
for entry in font["name"].names:
    if entry.nameID in names:
        entry.string = names[entry.nameID].encode(entry.getEncoding(), errors="replace")
font.save(destination)
shutil.copyfile(license_source, license_destination)

logo_source = ROOT / "logo.jpeg"
logo = ROOT / "public/brand/logo.jpeg"
logo_sha = "849f6b9670939eb5b2cd9285b912a998a96863d97338b8119cf2c98d3488cef2"
assert sha(logo_source) == sha(logo) == logo_sha, "Supplied brand artwork changed"
photo = ROOT / "public/images/augusto-og-room-v1.jpg"
previous = json.loads((ROOT / "research/hospitality-revision/og-assets-manifest.json").read_text())
assert sha(photo) == previous["photo"]["outputSha256"], "Existing property photograph changed"
headline = ImageFont.truetype(str(destination), 82)
manifest = {
    "generated": datetime.now(timezone.utc).isoformat(),
    "generator": "research/apple-dominant-revision/generate-og-assets.py",
    "palette": palette,
    "paletteNote": "sRGB equivalents of the current shared OKLCH tokens.",
    "font": {
        "source": source.relative_to(ROOT).as_posix(), "sourceSha256": sha(source),
        "output": destination.relative_to(ROOT).as_posix(), "outputSha256": sha(destination),
        "bytes": destination.stat().st_size, "weight": 600, "family": "Augusto OG Sans",
        "changes": "Static weight600 instantiation, WOFF2 to TTF conversion and renamed family. Copyright and license records preserved.",
        "license": "SIL Open Font License 1.1", "licenseFile": license_destination.relative_to(ROOT).as_posix(),
        "licenseSha256": sha(license_destination),
    },
    "photo": {**previous["photo"], "reusedWithoutModification": True},
    "brand": {
        "source": "logo.jpeg", "output": "public/brand/logo.jpeg",
        "sourceSha256": logo_sha, "outputSha256": logo_sha,
        "dimensions": [1254, 1254], "bytes": logo.stat().st_size,
        "provenance": "Hotel Augusto logo supplied by the user in the project folder.",
        "changes": "None. Public JPEG is byte-identical to the supplied source.",
        "presentation": "The website and OG composition crop surrounding whitespace in their layout. Source pixels are unchanged.",
    },
    "favicon": {
        "file": "public/brand/logo.jpeg", "sha256": logo_sha,
        "dimensions": [1254, 1254], "format": "JPEG",
        "routes": ["metadata.icons.icon", "metadata.icons.apple"],
        "replaces": "The invented app/icon.svg was removed by the parent and is no longer used.",
    },
    "headlineWidthsAt82px": {text: headline.getlength(text) for text in ["Your place", "in Kashi."]},
    "runtimeDependencyBytes": photo.stat().st_size + destination.stat().st_size + logo.stat().st_size,
}
path = ROOT / "research/apple-dominant-revision/og-assets-manifest.json"
path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf8")
print(json.dumps({"palette": palette, "headlineWidths": manifest["headlineWidthsAt82px"],
                  "runtimeDependencyBytes": manifest["runtimeDependencyBytes"]}))
