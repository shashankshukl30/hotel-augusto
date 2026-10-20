"""Capture the actual release layout, one browser at a time."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--base-url", default="http://127.0.0.1:3080")
parser.add_argument("--city-only", action="store_true")
args = parser.parse_args()
OUT = ROOT / "evidence/apple-dominant-revision"
OUT.mkdir(parents=True, exist_ok=True)
routes = {
    "/": [("hero", None), ("stay", ".home-reservation"), ("welcome", "#discover"),
          ("rooms", ".home-rooms"), ("dining", ".home-dining"),
          ("city", ".city-itinerary"), ("city-photo", ".itinerary-stage"),
          ("arrival", ".arrival-guide"), ("reserve", ".home-reserve")],
    "/rooms": [("intro", None)],
    "/rooms/deluxe-room": [("intro", None), ("details", ".room-detail-overview")],
    "/rooms/compare": [("intro", None)],
    "/hotel": [("intro", None)],
    "/dining": [("intro", None)],
    "/group-stays": [("intro", None)],
    "/varanasi": [("intro", None), ("city", ".city-itinerary")],
    "/gallery": [("intro", None)],
    "/guides": [("intro", None)],
    "/guides/first-visit-to-kashi": [("intro", None)],
    "/contact": [("intro", None), ("form", "#enquire")],
}
if args.city_only:
    routes = {"/": [("city", ".city-itinerary"), ("city-photo", ".itinerary-stage")]}
report = {"date": datetime.now(timezone.utc).isoformat(), "base": args.base_url,
          "captures": [], "errors": []}
with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    for width, height in [(1440, 1000), (390, 844)]:
        context = browser.new_context(viewport={"width": width, "height": height},
                                      reduced_motion="reduce")
        page = context.new_page()
        page.on("pageerror", lambda error: report["errors"].append(str(error)))
        for route, captures in routes.items():
            page.goto(args.base_url.rstrip("/") + route, wait_until="networkidle")
            page.evaluate("""async()=>{
              document.documentElement.style.scrollBehavior='auto';
              for(const image of document.images) image.loading='eager';
              await Promise.allSettled([...document.images].map(image=>image.decode()));
              await document.fonts.ready;
            }""")
            for name, selector in captures:
                if selector:
                    page.locator(selector).scroll_into_view_if_needed()
                    page.locator(selector).evaluate("e=>{scrollTo(0,scrollY+e.getBoundingClientRect().top-96)}")
                else:
                    page.evaluate("scrollTo(0,0)")
                page.wait_for_timeout(180)
                filename = f"{route.strip('/').replace('/', '-') or 'home'}-{width}-{name}.png"
                page.screenshot(path=str(OUT / filename))
                state = page.evaluate("""()=>({
                  bodyWidth:document.body.scrollWidth, viewport:innerWidth,
                  headingFont:getComputedStyle(document.querySelector('h1')).fontFamily,
                  headingWeight:getComputedStyle(document.querySelector('h1')).fontWeight,
                  scroll:scrollY
                })""")
                report["captures"].append({"route": route, "width": width,
                                           "selector": selector, "file": filename, **state})
        context.close()
    browser.close()
report["passed"] = not report["errors"] and all(
    capture["bodyWidth"] == capture["viewport"] for capture in report["captures"])
(OUT / ("visual-review-city.json" if args.city_only else "visual-review-captures.json")).write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps({"captures": len(report["captures"]), "passed": report["passed"],
                  "errors": report["errors"]}))
raise SystemExit(0 if report["passed"] else 1)
