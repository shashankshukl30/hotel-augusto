"""Check client access in a fresh browser, with no Vercel bypass credentials."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ROUTES = [
    "/", "/hotel", "/rooms", "/rooms/compare", "/rooms/deluxe-room",
    "/rooms/deluxe-twin-room", "/rooms/family-room", "/dining", "/varanasi",
    "/gallery", "/guides", "/guides/first-visit-to-kashi",
    "/guides/arriving-in-godowlia", "/guides/choosing-your-room",
    "/group-stays", "/contact", "/privacy",
]
parser = argparse.ArgumentParser()
parser.add_argument("--base-url", required=True)
parser.add_argument("--output", required=True)
parser.add_argument("--expect-public", action="store_true")
args = parser.parse_args()
base = args.base_url.rstrip("/")
origin = urlsplit(base).netloc
out = ROOT / args.output
out.parent.mkdir(parents=True, exist_ok=True)
report = {
    "date": datetime.now(timezone.utc).isoformat(), "base_url": base,
    "bypass_credentials_used": False, "custom_request_headers": False,
    "checks": [], "runtime_errors": [], "external_messages_sent": 0,
}


def check(name, passed, detail=None):
    report["checks"].append({"name": name, "passed": bool(passed), "detail": detail})


with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    context = browser.new_context(
        viewport={"width": 390, "height": 844}, device_scale_factor=1,
    )
    report["initial_cookie_count"] = len(context.cookies())
    page = context.new_page()
    page.on("pageerror", lambda error: report["runtime_errors"].append(str(error)))
    try:
        response = page.goto(base, wait_until="networkidle", timeout=60000)
        report["initial_page"] = {
            "http": response.status, "landed_url": page.url,
            "title": page.title(), "headings": page.locator("h1").all_text_contents(),
        }
        page.screenshot(path=str(out.with_suffix(".png")))
        if args.expect_public:
            for route in ROUTES:
                response = page.goto(base + route, wait_until="networkidle", timeout=60000)
                check("Anonymous route " + route,
                      response.status == 200 and urlsplit(page.url).netloc == origin
                      and page.locator("main h1").count() == 1,
                      {"status": response.status, "url": page.url,
                       "heading": page.locator("main h1").all_text_contents()})
                check("Mobile layout " + route, page.evaluate(
                    "document.body.scrollWidth===document.documentElement.clientWidth"))
                check("Preview stays noindex " + route,
                      "noindex" in (page.locator('meta[name="robots"]').get_attribute("content") or ""))
                print("Checked anonymous route " + route, flush=True)
            page.goto(base + "/rooms", wait_until="networkidle")
            page.locator('main a[href="/rooms/deluxe-room"]').first.click()
            page.wait_for_url("**/rooms/deluxe-room")
            check("Room navigation works without login",
                  page.locator("main h1").count() == 1 and urlsplit(page.url).netloc == origin)
            for asset in ["/brand/logo.jpeg", "/downloads/hotel-augusto-dining-guide.pdf"]:
                response = context.request.get(base + asset)
                expected = (ROOT / "public" / asset.lstrip("/")).read_bytes()
                check("Anonymous asset " + asset, response.status == 200
                      and hashlib.sha256(response.body()).digest() == hashlib.sha256(expected).digest())
            robots = context.request.get(base + "/robots.txt")
            check("Robots blocks indexing", robots.status == 200 and "Disallow: /" in robots.text())
            page.set_viewport_size({"width": 1440, "height": 900})
            page.goto(base, wait_until="networkidle")
            page.wait_for_timeout(500)
            check("Desktop hero loads without login",
                  page.locator(".hero-photo img").evaluate_all(
                      "imgs=>imgs.some(i=>i.complete&&i.naturalWidth>0)"))
            check("Desktop has no overflow", page.evaluate("document.body.scrollWidth===1440"))
            page.screenshot(path=str(out.parent / "anonymous-desktop.png"))
            check("No site runtime errors", not report["runtime_errors"], report["runtime_errors"])
    except Exception as error:
        report["fatal_error"] = str(error)
    finally:
        context.close()
        browser.close()

report["passed"] = not report.get("fatal_error") and (
    all(c["passed"] for c in report["checks"]) if args.expect_public else True
)
out.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps({
    "passed": report["passed"], "checks": len(report["checks"]),
    "initial_page": report.get("initial_page"),
    "failures": [c for c in report["checks"] if not c["passed"]],
    "fatal_error": report.get("fatal_error"),
}))
raise SystemExit(0 if report["passed"] else 1)
