"""Rendered colour/contrast and responsive checks. No external enquiries sent."""
import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path

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
parser.add_argument("--base-url", default="http://127.0.0.1:3082")
parser.add_argument("--output", default="evidence/colour-extension")
args = parser.parse_args()
base = args.base_url.rstrip("/")
out = ROOT / args.output
out.mkdir(parents=True, exist_ok=True)
report = {
    "date": datetime.now(timezone.utc).isoformat(),
    "base_url": base,
    "viewports": [],
    "accessibility": [],
    "interaction_checks": [],
    "runtime_errors": [],
    "screenshots": [],
}


def save():
    (out / "colour-qa.json").write_text(json.dumps(report, indent=2), encoding="utf-8")


def audit(page, route, width, state="page"):
    page.add_script_tag(path=str(ROOT / "node_modules/axe-core/axe.min.js"))
    violations = page.evaluate("""async () => {
      const r = await axe.run(document, {
        runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa']}
      });
      return r.violations.map(v => ({
        id: v.id, impact: v.impact,
        nodes: v.nodes.map(n => ({target: n.target, summary: n.failureSummary}))
      }));
    }""")
    report["accessibility"].append({
        "route": route, "width": width, "state": state, "violations": violations,
    })
    save()


def check(name, passed, detail=None):
    report["interaction_checks"].append({
        "name": name, "passed": bool(passed), "detail": detail,
    })


def capture(page, selector, name):
    target = page.locator(selector).first
    viewport = page.viewport_size
    page.evaluate("document.activeElement?.blur()")
    height = math.ceil(target.bounding_box()["height"]) + 250
    page.set_viewport_size({"width": viewport["width"], "height": height})
    target.evaluate("e => scrollTo(0, e.getBoundingClientRect().top + scrollY - 100)")
    page.wait_for_timeout(200)
    target.screenshot(path=str(out / name))
    page.set_viewport_size(viewport)
    report["screenshots"].append(name)


with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    context = browser.new_context(reduced_motion="reduce", device_scale_factor=1)
    page = context.new_page()
    page.on("pageerror", lambda error: report["runtime_errors"].append(str(error)))
    for width in (1440, 390):
        page.set_viewport_size({"width": width, "height": 900 if width > 600 else 844})
        for route in ROUTES:
            response = page.goto(base + route, wait_until="networkidle")
            page.evaluate("""async () => {
              document.documentElement.style.scrollBehavior = 'auto';
              for (const img of document.images) img.loading = 'eager';
              await Promise.allSettled([...document.images].map(img => img.decode()));
              for (let y=0; y<document.body.scrollHeight; y+=700) {
                scrollTo(0,y); await new Promise(r => setTimeout(r,20));
              }
              scrollTo(0,0);
            }""")
            page.wait_for_timeout(100)
            state = page.evaluate("""() => ({
              bodyWidth: document.body.scrollWidth,
              viewportWidth: document.documentElement.clientWidth,
              missingImages: [...document.images].filter(i => !i.complete || !i.naturalWidth)
                .map(i => i.currentSrc),
              h1Count: document.querySelectorAll('main h1').length
            })""")
            report["viewports"].append({
                "route": route, "width": width, "http": response.status, **state,
                "passed": response.status == 200 and state["bodyWidth"] == width
                          and state["viewportWidth"] == width
                          and not state["missingImages"] and state["h1Count"] == 1,
            })
            audit(page, route, width)
            if route == "/":
                for selector, name in [
                    (".home-rooms", "rooms"), (".home-dining", "dining"),
                    (".city-itinerary", "kashi"), (".home-reviews", "reviews"),
                    (".site-footer", "footer"),
                ]:
                    capture(page, selector, f"home-{width}-{name}.png")
                tabs = page.locator(".itinerary-tabs [role=tab]")
                tabs.first.focus()
                tabs.first.press("ArrowRight")
                page.wait_for_timeout(100)
                check(f"City tabs keep keyboard selection and focus at {width}",
                      tabs.nth(1).get_attribute("aria-selected") == "true"
                      and tabs.nth(1).evaluate("e => e === document.activeElement"))
                check(f"City keyboard focus remains visible at {width}",
                      tabs.nth(1).evaluate("""e => {
                        const s=getComputedStyle(e);
                        return s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 2;
                      }"""))
                audit(page, route, width, "city keyboard selection")
                guide = page.locator(".home-guide-links a").first
                normal = guide.evaluate("e => getComputedStyle(e).backgroundColor")
                guide.hover()
                page.wait_for_timeout(250)
                hovered = guide.evaluate("e => getComputedStyle(e).backgroundColor")
                check(f"Travel guide hover feedback remains visible at {width}",
                      normal != hovered, {"normal": normal, "hover": hovered})
                audit(page, route, width, "travel guide hover")
            elif route == "/dining":
                capture(page, ".hospitality-dining-service", f"dining-{width}-service.png")
    context.close()
    browser.close()

report["passed"] = (
    all(v["passed"] for v in report["viewports"])
    and all(not a["violations"] for a in report["accessibility"])
    and all(c["passed"] for c in report["interaction_checks"])
    and not report["runtime_errors"]
)
report["summary"] = {
    "passed": report["passed"],
    "viewport_checks": len(report["viewports"]),
    "accessibility_audits": len(report["accessibility"]),
    "interaction_checks": len(report["interaction_checks"]),
    "runtime_errors": len(report["runtime_errors"]),
}
save()
print(json.dumps(report["summary"]))
print(json.dumps({
    "failed_viewports": [v for v in report["viewports"] if not v["passed"]],
    "violations": [a for a in report["accessibility"] if a["violations"]],
    "failed_interactions": [c for c in report["interaction_checks"] if not c["passed"]],
}))
raise SystemExit(0 if report["passed"] else 1)
