"""Verify rendered motion, fallback content and input behavior; sends no enquiries."""
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ["/", "/hotel", "/rooms", "/rooms/compare", "/rooms/deluxe-room",
          "/rooms/deluxe-twin-room", "/rooms/family-room", "/dining", "/varanasi",
          "/gallery", "/guides", "/guides/first-visit-to-kashi",
          "/guides/arriving-in-godowlia", "/guides/choosing-your-room",
          "/group-stays", "/contact", "/privacy"]
MATRIX = """e=>{const s=getComputedStyle(e),m=new DOMMatrixReadOnly(s.transform);
  return {x:m.m41,y:m.m42,sx:m.m11,sy:m.m22,transform:s.transform,clip:s.clipPath,
  opacity:parseFloat(s.opacity)}}"""
HERO_SAMPLER = """(()=>{window.__heroFrames=[];let last=0;
  const until=performance.now()+12000;function frame(t){
    const e=document.querySelector('.hero-title-line');
    if(e&&t-last>35){const s=getComputedStyle(e),m=new DOMMatrixReadOnly(s.transform);
      window.__heroFrames.push({t,y:m.m42,transform:s.transform});last=t;}
    if(t<until)requestAnimationFrame(frame);}requestAnimationFrame(frame);})();"""
parser = argparse.ArgumentParser()
parser.add_argument("--base-url", default="http://127.0.0.1:3082")
parser.add_argument("--output", default="evidence/lando-motion/motion-qa.json")
args = parser.parse_args()
base = args.base_url.rstrip("/")
output = ROOT / args.output
output.parent.mkdir(parents=True, exist_ok=True)
report = {"date": datetime.now(timezone.utc).isoformat(), "base_url": base,
          "checks": [], "runtime_errors": [], "screenshots": [], "external_messages_sent": 0}


def check(name, passed, detail=None):
    report["checks"].append({"name": name, "passed": bool(passed), "detail": detail})
    print(("PASS " if passed else "FAIL ") + name, flush=True)


def run(name, action):
    try:
        action()
    except Exception as error:
        check(name, False, str(error))


def watch(page):
    page.set_default_timeout(12000)
    page.on("pageerror", lambda error: report["runtime_errors"].append(str(error)))
    return page


def shot(page, name):
    path = output.parent / (name + ".png")
    page.screenshot(path=str(path), animations="allow")
    report["screenshots"].append({"path": str(path.relative_to(ROOT)),
                                  "page_time_ms": round(page.evaluate("performance.now()"))})


def place(page, selector, viewport_fraction):
    page.locator(selector).first.evaluate("""(e,f)=>window.scrollTo({
      top:Math.max(0,e.getBoundingClientRect().top+scrollY-innerHeight*f),behavior:'instant'})""",
                                         viewport_fraction)
    page.wait_for_timeout(180)


def state(page, selector):
    return page.locator(selector).first.evaluate(MATRIX)


def desktop(page):
    page.add_init_script(HERO_SAMPLER)
    page.goto(base, wait_until="domcontentloaded")
    page.locator(".hero-title-line").first.wait_for()
    page.wait_for_timeout(140)
    shot(page, "hero-entrance-early")
    page.wait_for_timeout(310)
    shot(page, "hero-entrance-middle")
    page.wait_for_function("window.__heroFrames.some(f=>Math.abs(f.y)>5)")
    page.wait_for_timeout(1500)
    frames = page.evaluate("window.__heroFrames")
    check("Hero title moves and settles", max(abs(f["y"]) for f in frames) > 5
          and abs(state(page, ".hero-title-line")["y"]) < .5, frames)
    shot(page, "hero-entrance-settled")
    place(page, ".scroll-photo-window", .88)
    first = state(page, ".scroll-photo-window")
    y1 = page.evaluate("scrollY")
    place(page, ".scroll-photo-window", .15)
    second = state(page, ".scroll-photo-window")
    # Computed CSS collapses equal sides to inset(0% round 24px).
    # Only inspect the inset values, never the corner radius.
    sides = [re.findall(r"[-\d.]+", s["clip"].split("round")[0]) for s in [first, second]]
    insets = [float(values[1] if len(values) > 1 else values[0]) for values in sides]
    check("Native scroll opens photograph crop", page.evaluate("scrollY") > y1 + 100
          and insets[0] > insets[1] + .5, {"before": first, "after": second})
    place(page, ".home-gallery-motion", .9)
    before = page.locator(".gallery-motion-card").evaluate_all(
        "es=>es.map(e=>new DOMMatrixReadOnly(getComputedStyle(e).transform).m42)")
    place(page, ".home-gallery-motion", .1)
    after = page.locator(".gallery-motion-card").evaluate_all(
        "es=>es.map(e=>new DOMMatrixReadOnly(getComputedStyle(e).transform).m42)")
    delta = [b - a for a, b in zip(before, after)]
    check("Gallery cards drift at different rates", len(delta) == 3
          and max(delta) - min(delta) > 5 and max(abs(v) for v in delta) > 8,
          {"before": before, "after": after})
    room = page.locator(".room-photo-link").first
    place(page, ".room-photo-link", .23)
    before_box = room.bounding_box()
    page.evaluate("""()=>{window.__roomFrames=[];const end=performance.now()+12000;
      function tick(t){const p=document.querySelector('.room-photo-preview');
        if(p){const i=p.querySelector('img');window.__roomFrames.push({
          inset:parseFloat(getComputedStyle(p).clipPath.replace('inset(','')),
          decoded:i.complete&&i.naturalWidth>0});}
        if(t<end)requestAnimationFrame(tick);}requestAnimationFrame(tick)}""")
    room.hover()
    page.wait_for_function("document.querySelector('.room-photo-link').dataset.previewReady==='true'")
    clip = state(page, ".room-photo-preview")["clip"]
    page.wait_for_timeout(220)
    shot(page, "room-preview-reveal")
    page.wait_for_timeout(850)
    preview = room.locator(".room-photo-preview img")
    room_frames = page.evaluate("window.__roomFrames")
    check("Room alternate photograph is decoded before reveal", preview.evaluate(
        "i=>i.complete&&i.naturalWidth>0") and any(f["inset"] < 1 for f in room_frames)
        and all(f["decoded"] for f in room_frames if f["inset"] < 99.9),
        {"early_clip": clip, "settled": state(page, ".room-photo-preview"), "frames": room_frames})
    check("Room preview animates a clipped reveal", any(1 < f["inset"] < 99 for f in room_frames))
    box = room.bounding_box()
    page.mouse.move(box["x"] + box["width"] * .88, box["y"] + box["height"] * .8)
    page.wait_for_timeout(450)
    invitation = state(page, ".room-photo-invitation")
    after_box = room.bounding_box()
    check("Room link stays stationary while invitation follows pointer",
          all(abs(before_box[k] - after_box[k]) < 1 for k in before_box)
          and .5 < abs(invitation["x"]) <= 6.1 and abs(invitation["y"]) <= 5.1,
          {"before": before_box, "after": after_box, "invitation": invitation})
    place(page, ".itinerary-tabs", .25)
    river = page.get_by_role("tab", name="The river", exact=True)
    river.focus()
    river.press("ArrowRight")
    temple = page.get_by_role("tab", name="The temple", exact=True)
    page.wait_for_function("""()=>document.querySelector(
      '.itinerary-image-layer[aria-hidden=false] img')?.alt.includes('golden shrine')""")
    city_early = state(page, ".itinerary-image-layer[aria-hidden=false]")
    zoom_early = state(page, ".itinerary-image-layer[aria-hidden=false] .itinerary-image-zoom")
    shot(page, "city-photo-reveal")
    page.wait_for_timeout(1250)
    city_late = state(page, ".itinerary-image-layer[aria-hidden=false]")
    check("City photograph visibly reveals and settles", city_early["clip"] != city_late["clip"]
          or zoom_early["sx"] > 1.001, {"early": city_early, "early_zoom": zoom_early, "settled": city_late})
    pill, tab = page.locator(".itinerary-tab-pill").bounding_box(), temple.bounding_box()
    check("City keyboard selection updates pill, caption and ready photograph",
          temple.get_attribute("aria-selected") == "true" and temple.evaluate("e=>e===document.activeElement")
          and abs(pill["x"] - tab["x"]) < 3 and abs(pill["width"] - tab["width"]) < 4
          and "Wikimedia" in page.locator(".itinerary-figure figcaption").inner_text()
          and page.locator(".itinerary-copy[aria-hidden=false] h3").inner_text() == "Kashi Vishwanath.",
          {"pill": pill, "tab": tab})
    temple.press("End")
    check("City End key selects final stop", page.get_by_role("tab", name="The evening").get_attribute("aria-selected") == "true")


def failed_image(page):
    page.route("**/*", lambda route: route.abort() if "kashi-vishwanath.webp" in
               unquote(route.request.url) else route.continue_())
    page.goto(base, wait_until="domcontentloaded")
    place(page, ".itinerary-stage", .3)
    page.wait_for_function("""()=>{const i=document.querySelector(
      '.itinerary-image-layer[aria-hidden=false] img');return i?.complete&&i.naturalWidth>0}""")
    caption = page.locator(".itinerary-figure figcaption").inner_text()
    page.get_by_role("tab", name="The temple", exact=True).click()
    page.get_by_role("status").filter(has_text="This photograph could not load.").wait_for()
    check("Failed destination image preserves last ready image and its attribution",
          page.locator(".itinerary-figure figcaption").inner_text() == caption
          and "sunrise" in page.locator(".itinerary-image-layer[aria-hidden=false] img").get_attribute("alt")
          and page.locator(".itinerary-figure").get_attribute("aria-busy") == "false"
          and page.get_by_role("tab", name="The temple", exact=True).get_attribute("aria-selected") == "true")


def mobile(page):
    page.goto(base, wait_until="networkidle")
    place(page, ".home-welcome-copy", .18)
    page.wait_for_timeout(1100)
    shot(page, "mobile-welcome-type")
    place(page, ".home-gallery-motion", .8)
    first = page.locator(".gallery-motion-card").evaluate_all("es=>es.map(e=>getComputedStyle(e).transform)")
    place(page, ".home-gallery-motion", .2)
    second = page.locator(".gallery-motion-card").evaluate_all("es=>es.map(e=>getComputedStyle(e).transform)")
    check("Mobile gallery removes differential drift", all(x == "none" for x in first + second))
    shot(page, "mobile-gallery")
    page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
    trigger = page.get_by_role("button", name="Open navigation", exact=True)
    for cycle in range(2):
        trigger.click()
        page.wait_for_timeout(110)
        early = state(page, ".navigation-menu-label")
        if cycle == 0:
            shot(page, "mobile-menu-opening")
        page.wait_for_timeout(1000)
        settled = state(page, ".navigation-menu-label")
        check(f"Menu entrance replays and settles on opening {cycle + 1}",
              early["y"] > .5 and abs(settled["y"]) < .5, {"early": early, "settled": settled})
        page.keyboard.press("Escape")
        page.wait_for_function("""!document.querySelector('.navigation-dialog').open&&
          document.querySelector('.menu-trigger').getAttribute('aria-expanded')==='false'""")
        check(f"Escape closes menu and restores focus {cycle + 1}",
              not page.locator(".navigation-dialog").evaluate("e=>e.open")
              and trigger.evaluate("e=>e===document.activeElement")
              and trigger.get_attribute("aria-expanded") == "false")
    place(page, ".room-photo-link", .25)
    target = page.locator(".room-photo-link").first
    expected = target.get_attribute("href")
    target.tap()
    page.wait_for_url(base + expected)
    check("First touch on room photograph navigates", page.locator("main h1").is_visible())
    for route in ROUTES:
        page.goto(base + route, wait_until="domcontentloaded")
        page.wait_for_timeout(120)
        check("Mobile width fits " + route, page.evaluate(
            "document.body.scrollWidth<=document.documentElement.clientWidth"))


def reduced(page):
    page.goto(base, wait_until="networkidle")
    transforms = ".hero-title-line,.kinetic-word,.scroll-photo-layer,.gallery-motion-card,.gallery-motion-image,.itinerary-city-name-motion,.itinerary-image-parallax,.itinerary-image-zoom"
    clips = ".scroll-photo-window,.hero-title-mask,.kinetic-word-mask,.hero-image-entrance"
    for selector in [".scroll-photo-window", ".itinerary-stage", ".home-gallery-motion"]:
        place(page, selector, .65)
        page.mouse.wheel(0, 220)
        page.wait_for_timeout(150)
        check("Reduced motion remains still after scrolling " + selector, page.locator(transforms).evaluate_all(
            "es=>es.every(e=>getComputedStyle(e).transform==='none')") and page.locator(clips).evaluate_all(
            "es=>es.every(e=>getComputedStyle(e).clipPath==='none')"))
    page.get_by_role("tab", name="The temple", exact=True).click()
    page.wait_for_timeout(250)
    check("Reduced-motion city copy and selection remain usable",
          state(page, ".itinerary-copy[aria-hidden=false] .itinerary-copy-motion")["transform"] == "none"
          and state(page, ".itinerary-tab-pill")["transform"] == "none")
    page.set_viewport_size({"width": 390, "height": 844})
    page.get_by_role("button", name="Open navigation", exact=True).click()
    check("Reduced-motion menu is immediately readable", page.locator(
        ".navigation-menu-label,.navigation-content").evaluate_all(
        "es=>es.every(e=>getComputedStyle(e).transform==='none'&&getComputedStyle(e).opacity==='1')"))


def no_javascript(page):
    page.goto(base, wait_until="networkidle")
    check("Server hero text is visible without JavaScript", page.locator("h1").is_visible()
          and "Your place" in page.locator("h1").inner_text()
          and page.locator(".hero-title-line").first.evaluate(
              "e=>getComputedStyle(e).transform==='none'"))
    check("Server primary links remain usable without JavaScript",
          page.locator(".hero-actions a").first.is_visible()
          and page.locator(".room-photo-link").count() == 3
          and all(page.locator(".room-photo-link").nth(i).get_attribute("href").startswith("/rooms/") for i in range(3)))


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(channel="msedge", headless=True)
    for name, action, options in [
        ("Desktop motion", desktop, {"viewport": {"width": 1440, "height": 900}}),
        ("Failed city image", failed_image, {"viewport": {"width": 1440, "height": 900}}),
        ("Mobile interactions", mobile, {"viewport": {"width": 390, "height": 844}, "is_mobile": True, "has_touch": True}),
        ("Reduced motion", reduced, {"viewport": {"width": 1440, "height": 900}, "reduced_motion": "reduce"}),
        ("No-JavaScript content", no_javascript, {"viewport": {"width": 1440, "height": 900}, "java_script_enabled": False}),
    ]:
        context = browser.new_context(**options)
        run(name, lambda action=action, context=context: action(watch(context.new_page())))
        context.close()
    browser.close()
check("No JavaScript runtime errors", not report["runtime_errors"], report["runtime_errors"])
report["passed"] = bool(report["checks"]) and all(item["passed"] for item in report["checks"])
output.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps({"passed": report["passed"], "checks": len(report["checks"]),
                  "failed": [item["name"] for item in report["checks"] if not item["passed"]]}))
raise SystemExit(0 if report["passed"] else 1)
