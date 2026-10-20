"""Read-only checks for the Sites export; hosting behavior needs a live check."""
import argparse
import json
import posixpath
import re
import shutil
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

from fontTools.ttLib import TTFont
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--output", default="evidence/hospitality-revision/static-export-audit.json")
args = parser.parse_args()
OUT = ROOT / "out"
BASE = "https://hotel-augusto.candy-okapi-4696.chatgpt.site"
ROUTES = [
    "/", "/hotel", "/rooms", "/rooms/compare", "/rooms/deluxe-room",
    "/rooms/deluxe-twin-room", "/rooms/family-room", "/dining", "/varanasi",
    "/gallery", "/guides", "/guides/arriving-in-godowlia",
    "/guides/choosing-your-room", "/guides/first-visit-to-kashi", "/group-stays", "/contact", "/privacy",
]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.assets, self.links, self.canonicals, self.forms, self.actions = [], [], [], [], []
        self.metadata, self.h1s, self.title, self.in_title = {}, 0, "", False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.h1s += 1
        if tag == "meta":
            self.metadata[a.get("name") or a.get("property", "")] = a.get("content", "")
        if tag == "form":
            self.forms.append(a)
        if tag == "input" and a.get("name", "").startswith("$ACTION"):
            self.actions.append(a)
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
        if tag == "link":
            if a.get("rel") == "canonical":
                self.canonicals.append(a.get("href", ""))
            elif a.get("rel") in ["stylesheet", "preload", "icon", "apple-touch-icon"]:
                self.assets.append((a.get("href", ""), "link:" + a["rel"]))
        if tag in ["img", "script", "source", "video", "audio"]:
            for attribute in ["src", "poster"]:
                if a.get(attribute):
                    self.assets.append((a[attribute], tag))
            for src in a.get("srcset", "").split(","):
                if src.strip():
                    self.assets.append((src.strip().split()[0], tag + ":srcset"))

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def local_path(url, source):
    parsed = urlparse(url)
    if parsed.scheme and (parsed.scheme not in ["http", "https"] or parsed.netloc != urlparse(BASE).netloc):
        return None
    if parsed.netloc and parsed.netloc != urlparse(BASE).netloc:
        return None
    raw = unquote(parsed.path)
    if not raw:
        return None
    relative = raw.lstrip("/") if raw.startswith("/") else posixpath.normpath(
        posixpath.join(source.parent.relative_to(OUT).as_posix(), raw))
    result = OUT / relative
    if not result.resolve().is_relative_to(OUT.resolve()):
        raise ValueError("Reference escapes export: " + url)
    return result


def main():
    report_path = ROOT / args.output
    previous = json.loads(report_path.read_text()) if report_path.exists() else None
    before = {d: shutil.disk_usage(d + ":/").free for d in ["C", "D"]}
    checks, pages, dependencies, missing_links, metadata_issues, forms, actions = [], [], {}, [], [], [], []

    def check(name, passed, detail=None):
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    def dependency(url, source, kind):
        target = local_path(url, source)
        if target is not None:
            entry = dependencies.setdefault(target, {"file": target.relative_to(ROOT).as_posix(), "types": set(), "references": 0})
            entry["types"].add(kind)
            entry["references"] += 1

    for route in ROUTES + ["/404"]:
        path = OUT / ("index.html" if route == "/" else route.lstrip("/") + ".html")
        check("Export exists: " + route, path.is_file())
        if not path.exists():
            continue
        page = Page()
        page.feed(path.read_text(encoding="utf8"))
        pages.append({"route": route, "title": page.title, "h1Count": page.h1s,
                      "canonical": page.canonicals, "ogImage": page.metadata.get("og:image"),
                      "ogUrl": page.metadata.get("og:url"), "robots": page.metadata.get("robots")})
        if route != "/404":
            check("One H1: " + route, page.h1s == 1)
            check("Private noindex: " + route, "noindex" in page.metadata.get("robots", ""))
            if not page.metadata.get("og:image", "").startswith(BASE + "/opengraph-image"):
                metadata_issues.append({"route": route, "key": "og:image"})
        for url in page.canonicals:
            if urlparse(url).netloc != urlparse(BASE).netloc or urlparse(url).path.rstrip("/") != route.rstrip("/"):
                metadata_issues.append({"route": route, "key": "canonical", "value": url})
        if page.metadata.get("og:url") and not page.metadata["og:url"].startswith(BASE + "/"):
            metadata_issues.append({"route": route, "key": "og:url"})
        for url, kind in page.assets:
            dependency(url, path, kind)
        for url in page.links:
            target = local_path(url, path)
            if target is not None and not (target.is_file() or target.with_suffix(".html").is_file() or (target / "index.html").is_file()):
                missing_links.append({"route": route, "href": url})
        forms += [{"route": route, "attributes": form} for form in page.forms]
        actions += page.actions
    for css in OUT.rglob("*.css"):
        for match in re.finditer(r"""url\(\s*['"]?([^'"\)]+)""", css.read_text(encoding="utf8")):
            dependency(match.group(1), css, "css:url")
    for js in OUT.rglob("*.js"):
        for match in re.finditer(r"""['"]((?:/_next/)?static/(?:chunks|media)/[^'"\s]+\.(?:js|css|woff2|svg))['"]""", js.read_text(encoding="utf8")):
            url = match.group(1)
            dependency(url if url.startswith("/") else "/_next/" + url, js, "js:static-dependency")
    missing = [item["file"] for path, item in dependencies.items() if not path.is_file()]
    check("Referenced image/font/script/stylesheet files resolve", not missing, missing)
    check("Local navigation targets have corresponding artifacts", not missing_links, missing_links)
    check("All canonical and OG URLs use expected private preview base", not metadata_issues, metadata_issues)
    payload_aliases = []
    for source in OUT.rglob("*.txt"):
        parts = source.relative_to(OUT).parts
        segment_index = next((index for index, part in enumerate(parts)
                              if part.startswith("__next.")), None)
        if segment_index is None or segment_index == len(parts) - 1:
            continue
        destination = OUT.joinpath(*parts[:segment_index], ".".join(parts[segment_index:]))
        payload_aliases.append({
            "source": source.relative_to(OUT).as_posix(),
            "destination": destination.relative_to(OUT).as_posix(),
            "matches": destination.is_file() and destination.read_bytes() == source.read_bytes(),
        })
    check("Windows RSC segment aliases match browser URLs and original bytes",
          all(item["matches"] for item in payload_aliases), payload_aliases)

    images = []
    for path in list((OUT / "images").glob("*")) + [OUT / "opengraph-image"]:
        if path.suffix.lower() not in [".webp", ".jpg", ".jpeg", ".png", ".avif"] and path.name != "opengraph-image":
            continue
        with Image.open(path) as image:
            image.load()
            images.append({"file": path.relative_to(ROOT).as_posix(), "format": image.format, "size": list(image.size), "valid": True})
    check("Every exported property/destination photo and OG image decodes", all(item["valid"] for item in images), len(images))
    check("Exported OG is PNG1200x630", any(item["file"] == "out/opengraph-image" and item["format"] == "PNG" and item["size"] == [1200, 630] for item in images))
    fonts = []
    for path in list(OUT.rglob("*.woff2")) + list(OUT.rglob("*.ttf")):
        font = TTFont(path)
        fonts.append({"file": path.relative_to(ROOT).as_posix(), "valid": True, "glyphs": len(font.getBestCmap())})
        font.close()
    check("All exported fonts parse", all(item["valid"] for item in fonts), len(fonts))
    source_hits = []
    for directory in ["app", "components", "lib"]:
        for path in (ROOT / directory).rglob("*"):
            if path.suffix not in [".ts", ".tsx"]:
                continue
            text = path.read_text(encoding="utf8")
            if re.search(r"""^\s*['"]use server['"]""", text, re.M) or re.search(r"""fetch\s*\(\s*['"](?:/api/|https?://)""", text):
                source_hits.append(path.relative_to(ROOT).as_posix())
    api_routes = [path.relative_to(ROOT).as_posix() for path in (ROOT / "app").rglob("route.*")]
    active_forms = [form for form in forms if form["attributes"].get("action") or form["attributes"].get("method", "get").lower() == "post"]
    check("No active exported form server actions", not active_forms and not actions, active_forms + actions)
    check("No application API/server-action dependency", not source_hits and not api_routes, source_hits + api_routes)
    for relative, required in [
        ("components/booking-form.tsx", ["event.preventDefault()", "buildWhatsAppUrl", "setDraft"]),
        ("components/stay-bar.tsx", ["preventDefault()", "stayQuery", "/contact"]),
    ]:
        text = (ROOT / relative).read_text(encoding="utf8")
        check("Client form handoff: " + relative, all(token in text for token in required))
    robots = (OUT / "robots.txt").read_text(encoding="utf8")
    check("Preview robots blocks indexing", "Disallow: /" in robots and "Sitemap:" not in robots)
    failed = [item for item in checks if not item["passed"]]
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "scope": "Read-only static artifact audit including Windows RSC navigation payloads; no browser or network requests.",
        "expectedBaseUrl": BASE, "status": "fail" if failed else "pass",
        "previousAudit": {"timestamp": previous["timestamp"], "summary": previous["summary"]} if previous else None,
        "summary": {"contentRoutes": len(ROUTES), "notFoundArtifact": (OUT / "404.html").is_file(),
                    "checks": len(checks), "passed": len(checks) - len(failed), "failed": len(failed),
                    "localDependencies": len(dependencies), "dependencyReferences": sum(v["references"] for v in dependencies.values()),
                    "imagesDecoded": len(images), "fontsParsed": len(fonts), "formsInspected": len(forms)},
        "checks": checks, "pages": pages, "images": images, "fonts": fonts, "forms": forms,
        "rscPayloadAliases": payload_aliases,
        "dependencies": [dict(item, types=sorted(item["types"])) for item in dependencies.values()],
        "hostingBehavior": previous.get("hostingBehavior") if previous else {
            "notEstablished": ["Installed Sites helper does not specify clean-URL .html resolution. Deployed route and OG content-type checks remain necessary."]},
        "cleanup": {"beforeFreeBytes": before, "afterFreeBytes": {d: shutil.disk_usage(d + ":/").free for d in ["C", "D"]},
                    "removed": [], "reason": "Only required reproducible audit source and report created; no disposable files."},
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf8")
    print(json.dumps({"summary": report["summary"], "failures": failed, "report": str(report_path)}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
