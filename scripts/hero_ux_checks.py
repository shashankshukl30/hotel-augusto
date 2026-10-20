"""Browser checks for the hero/dock boundary and accessible picture motion."""
import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

VIEWPORTS = [
    (1876, 771), (1920, 1080), (1440, 900), (1366, 768), (1280, 720),
    (1536, 616), (1280, 600), (1024, 768), (768, 1024), (390, 844),
    (375, 667), (360, 640), (320, 568), (844, 390), (667, 375),
    (568, 320), (480, 320),
]


def verify_hero(page, base, check, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    page.emulate_media(reduced_motion="reduce")
    for width, height in VIEWPORTS:
        page.set_viewport_size({"width": width, "height": height})
        page.goto(base + "/", wait_until="networkidle")
        geometry = page.evaluate("""() => {
          const rect = selector => {
            const r = document.querySelector(selector).getBoundingClientRect();
            return { top:r.top, bottom:r.bottom, left:r.left, right:r.right };
          };
          return {
            hero:rect('.hero-media'), title:rect('.hero-intro h1'),
            intro:rect('.hero-intro'), actions:rect('.hero-actions'),
            controls:rect('.hero-scene-controls'), dock:rect('.booking-dock'),
            overflow:document.body.scrollWidth > innerWidth
          };
        }""")
        label = f"{width}x{height}"
        check("Hero clears booking dock " + label,
              geometry["hero"]["bottom"] <= geometry["dock"]["top"] - 10, geometry)
        check("Hero actions and scene controls stay separate " + label,
              geometry["actions"]["bottom"] <= geometry["controls"]["top"] - 6)
        check("Hero content stays inside photograph " + label,
              geometry["title"]["top"] >= geometry["hero"]["top"]
              and geometry["title"]["left"] >= geometry["hero"]["left"]
              and geometry["title"]["right"] <= geometry["hero"]["right"]
              and geometry["controls"]["bottom"] <= geometry["hero"]["bottom"] - 7)
        check("No horizontal overflow " + label, not geometry["overflow"])
        check("Booking action text fits " + label, page.locator(".dock-submit").evaluate(
            "e=>e.scrollWidth<=e.clientWidth && e.scrollHeight<=e.clientHeight"))
        if width in [1876, 390, 375, 568, 480]:
            page.screenshot(path=str(output / f"hero-{label}.png"))

    # The hero must respond to a real measured dock-height change, not a
    # separately guessed footer constant.
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto(base + "/", wait_until="networkidle")
    page.locator(".booking-dock").evaluate("e=>e.style.paddingBottom='48px'")
    page.wait_for_timeout(150)
    check("Hero follows a taller measured booking dock", page.evaluate("""()=>{
      return document.querySelector('.hero-media').getBoundingClientRect().bottom
        <= document.querySelector('.booking-dock').getBoundingClientRect().top - 10;
    }"""))

    for width in [1440, 390]:
        page.set_viewport_size({"width": width, "height": 900 if width == 1440 else 844})
        page.goto(base + "/", wait_until="networkidle")
        page.locator(".itinerary-stage").evaluate(
            "e=>window.scrollTo(0,e.getBoundingClientRect().top+scrollY-120)")
        page.wait_for_function("""Array.from(document.querySelectorAll(
          '.itinerary-image-layer[aria-hidden=false] img')).every(i=>i.complete&&i.naturalWidth>0)""")
        check("KASHI is raised and remains partly behind photograph " + str(width),
              page.locator(".itinerary-stage").evaluate("""e=>{
                const text=e.querySelector('.itinerary-city-name').getBoundingClientRect();
                const photo=e.querySelector('.itinerary-image').getBoundingClientRect();
                return parseFloat(getComputedStyle(e.querySelector('.itinerary-city-name')).top)<0
                  && photo.top>text.top && photo.top<text.bottom;
              }"""))
        check("KASHI word fits horizontally " + str(width),
              page.locator(".itinerary-stage").evaluate(
                  "e=>e.querySelector('.itinerary-city-name').getBoundingClientRect().width<=e.clientWidth"))
        page.screenshot(path=str(output / f"kashi-{width}.png"))

    page.set_viewport_size({"width": 1440, "height": 900})
    page.emulate_media(reduced_motion="no-preference")
    page.goto(base + "/", wait_until="networkidle")
    page.mouse.move(1300, 300)
    page.wait_for_timeout(500)

    def transform():
        return page.locator(".hero-photographs").evaluate("e=>getComputedStyle(e).transform")

    def photo_scale():
        # Pointer springs can still settle after a click; the scale isolates
        # autonomous photograph playback from that direct pointer response.
        return page.locator(".hero-photographs").evaluate(
            "e=>new DOMMatrixReadOnly(getComputedStyle(e).transform).a")

    before = transform()
    page.wait_for_timeout(1800)
    check("Photographs animate while pointer rests on image", before != transform())
    selected = page.locator(".hero-scene-buttons [aria-pressed=true]").inner_text()
    page.wait_for_function(
        "(label)=>document.querySelector('.hero-scene-buttons [aria-pressed=true]').textContent!==label",
        arg=selected, timeout=11000)
    check("Ready photographs crossfade automatically", True)
    page.wait_for_timeout(850)
    page.screenshot(path=str(output / "animated-next-scene.png"))
    page.get_by_role("button", name="Pause hotel slideshow", exact=True).click()
    page.mouse.move(1300, 300)
    page.wait_for_timeout(350)
    before = photo_scale()
    page.wait_for_timeout(1100)
    check("Pause freezes automatic photograph animation", before == photo_scale(),
          {"before": before, "after": photo_scale()})
    page.get_by_role("button", name="Play hotel slideshow", exact=True).click()
    page.mouse.move(1300, 300)
    page.wait_for_timeout(350)
    before = transform()
    page.wait_for_timeout(1100)
    check("Play resumes photograph animation", before != transform())
    page.get_by_role("button", name="Show vegetarian dining", exact=True).click()
    page.wait_for_function("""document.querySelector(
      '.hero-scene-buttons [aria-pressed=true]').textContent==='Dining'""")
    check("Manual scene selection pauses rotation",
          page.get_by_role("button", name="Play hotel slideshow", exact=True).count() == 1)
    play = page.get_by_role("button", name="Play hotel slideshow", exact=True)
    play.focus()
    play.press("Shift")
    play.click()
    page.mouse.move(1300, 300)
    page.wait_for_timeout(350)
    before = transform()
    page.wait_for_timeout(1100)
    check("Mouse Play resumes after keyboard focus", before != transform())
    pause = page.get_by_role("button", name="Pause hotel slideshow", exact=True)
    pause.focus()
    pause.press("Shift")
    page.mouse.move(1300, 300)
    page.wait_for_timeout(350)
    before = photo_scale()
    page.wait_for_timeout(800)
    check("Keyboard focus independently pauses photo motion", before == photo_scale(),
          {"before": before, "after": photo_scale()})
    page.emulate_media(reduced_motion="reduce")
    page.goto(base + "/", wait_until="networkidle")
    before = transform()
    page.wait_for_timeout(1000)
    check("Reduced motion keeps photographs static", before == transform() and before == "none")
    check("Reduced motion disables automatic-play control", page.locator(".hero-pause").is_disabled())
    page.get_by_role("button", name="Show the hotel lounge", exact=True).click()
    page.wait_for_function("""document.querySelector(
      '.hero-scene-buttons [aria-pressed=true]').textContent==='Lounge'""")
    check("Reduced motion retains manual scene selection", True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:3081")
    parser.add_argument("--output", default="evidence/hero-refinement/local-qa.json")
    args = parser.parse_args()
    report = {"checks": [], "errors": []}

    def check(name, passed, detail=None):
        report["checks"].append({"name": name, "passed": bool(passed), "detail": detail})

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page()
        page.on("pageerror", lambda error: report["errors"].append(str(error)))
        try:
            verify_hero(page, args.base_url, check, Path(args.output).parent)
            page.set_viewport_size({"width": 390, "height": 844})
            routes = [
                "/", "/hotel", "/rooms", "/rooms/compare", "/rooms/deluxe-room",
                "/rooms/deluxe-twin-room", "/rooms/family-room", "/dining", "/varanasi",
                "/gallery", "/guides", "/guides/first-visit-to-kashi",
                "/guides/arriving-in-godowlia", "/guides/choosing-your-room",
                "/group-stays", "/contact", "/privacy",
            ]
            for route in routes:
                response = page.goto(args.base_url + route, wait_until="networkidle")
                check("Mobile route renders " + route,
                      response.status == 200 and page.locator("main h1").count() == 1)
                check("Mobile route has no overflow " + route, page.evaluate(
                    "document.body.scrollWidth===document.documentElement.clientWidth"))
        except Exception as error:
            report["fatal_error"] = str(error)
        browser.close()
    check("No browser runtime errors", not report["errors"], report["errors"])
    report["passed"] = not report.get("fatal_error") and all(c["passed"] for c in report["checks"])
    Path(args.output).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "checks": len(report["checks"]),
                      "failures": [c for c in report["checks"] if not c["passed"]],
                      "fatal_error": report.get("fatal_error")}))
    raise SystemExit(0 if report["passed"] else 1)
