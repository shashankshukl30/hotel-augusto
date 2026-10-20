"""Create responsive WebP copies without changing or upscaling source artwork."""

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, __version__ as pillow_version

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "public/images"
OUTPUT = SOURCE / "responsive"
WIDTHS = (96, 192, 480, 960, 1600)
QUALITY = 85
EVIDENCE = ROOT / "research/apple-dominant-revision/responsive-images.json"
RUNTIME_MANIFEST = ROOT / "content/responsive-images.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def provenance():
    result = {}
    ledgers = [
        ("research/assets/asset-manifest.json", "assets"),
        ("research/ota-revision/asset-candidates.json", "assets"),
        ("research/awwwards-revision/hero-asset.json", None),
    ]
    for name, key in ledgers:
        document = json.loads((ROOT / name).read_text(encoding="utf8"))
        entries = document.get(key, []) if key else [document]
        for asset in entries:
            if asset.get("public_path"):
                result[asset["public_path"]] = {
                    "ledger": name,
                    "sourcePage": asset.get("source_page", asset.get("sourcePage")),
                    "rights": asset.get("rights", asset.get("license")),
                    "licenseUrl": asset.get("license_url"),
                }
    return result


def main():
    before = {drive: shutil.disk_usage(drive + ":/").free for drive in ("C", "D")}
    OUTPUT.mkdir(parents=True, exist_ok=True)
    ledgers = provenance()
    manifest = {}
    assets = []
    for source in sorted(SOURCE.glob("*.webp")):
        public_path = "/" + source.relative_to(ROOT / "public").as_posix()
        if public_path not in ledgers:
            raise ValueError(f"Missing source provenance: {public_path}")
        source_hash = sha(source)
        with Image.open(source) as original:
            original.load()
            width, height = original.size
            variants = []
            for target in WIDTHS:
                if target >= width:
                    # Reuse an existing native-size source rather than re-encode it.
                    variants.append({
                        "width": width, "height": height, "src": public_path,
                        "bytes": source.stat().st_size, "sha256": source_hash,
                        "retainedOriginal": True,
                    })
                    break
                target_height = max(1, round(height * target / width))
                output = OUTPUT / f"{source.stem}-{target}w.webp"
                resized = original.resize((target, target_height), Image.Resampling.LANCZOS)
                options = {"format": "WEBP", "quality": QUALITY, "method": 6}
                if original.info.get("icc_profile"):
                    options["icc_profile"] = original.info["icc_profile"]
                resized.save(output, **options)
                with Image.open(output) as reopened:
                    reopened.load()
                    assert reopened.size == (target, target_height)
                variants.append({
                    "width": target, "height": target_height,
                    "src": "/" + output.relative_to(ROOT / "public").as_posix(),
                    "bytes": output.stat().st_size, "sha256": sha(output),
                    "retainedOriginal": False,
                })
        assert sha(source) == source_hash, f"Source changed: {source}"
        manifest[public_path] = [{"width": v["width"], "src": v["src"]} for v in variants]
        assets.append({
            "source": public_path, "sourceDimensions": [width, height],
            "sourceBytes": source.stat().st_size, "sourceSha256": source_hash,
            "provenance": ledgers[public_path], "variants": variants,
        })

    RUNTIME_MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf8")
    generated = [variant for asset in assets for variant in asset["variants"]
                 if not variant["retainedOriginal"]]
    original_bytes = sum(asset["sourceBytes"] for asset in assets)
    totals = {}
    for width in (480, 960, 1600):
        total = sum(next((v for v in a["variants"] if v["width"] >= width),
                         a["variants"][-1])["bytes"] for a in assets)
        totals[str(width)] = {
            "bytesAcrossAllImages": total,
            "reductionFromOriginalPercent": round((1 - total / original_bytes) * 100, 2),
        }
    report = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "generator": "scripts/generate-responsive-images.py",
        "pillowVersion": pillow_version,
        "method": {
            "widths": WIDTHS, "quality": QUALITY, "encoder": "WebP method6",
            "resize": "Lanczos, original aspect ratio, nearest whole-pixel height",
            "maxWidth": 1600, "upscale": False, "crop": False,
            "retouch": False, "syntheticContent": False,
            "nativeSize": "Reuse the existing source when its width is 1600px or smaller.",
        },
        "delivery": {
            "staticExport": "Next custom loader selects pre-generated local WebP variants.",
            "normalNext": "Default Next optimizer remains enabled, with AVIF/WebP negotiation.",
            "quality": "Static preview uses one quality85 profile; normal Next keeps quality75/85.",
            "untouched": "Brand assets, metadata JPEG, source photos and original rights ledgers.",
        },
        "summary": {
            "sources": len(assets), "originalBytes": original_bytes,
            "generatedFiles": len(generated),
            "generatedBytes": sum(v["bytes"] for v in generated),
            "responsiveTotals": totals,
        },
        "assets": assets,
        "cleanup": {
            "removed": [], "beforeFreeBytes": before,
            "afterFreeBytes": {d: shutil.disk_usage(d + ":/").free for d in ("C", "D")},
            "retained": "All originals, responsive runtime files, provenance and generator.",
        },
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(report, indent=2) + "\n", encoding="utf8")
    print(json.dumps(report["summary"], indent=2))


if __name__ == "__main__":
    main()
