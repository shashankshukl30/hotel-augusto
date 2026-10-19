"""Browser acceptance checks for the gallery and Varanasi editorial routes."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / "cinematic-redesign"
OUT.mkdir(exist_ok=True)
BASE = os.environ.get("HOTEL_QA_URL", "http://127.0.0.1:3082")
report = {"layouts": [], "gallery": {}, "errors": []}

with sync_playwright() as runner:
    browser = runner.chromium.launch(channel="msedge", headless=True)
    context = browser.new_context(viewport={"width": 390, "height": 844}, reduced_motion="reduce")
    page = context.new_page()
    page.on("pageerror", lambda error: report["errors"].append({"message": str(error), "stack": error.stack, "url": page.url, "step": report.get("currentStep")}))
    for route in ["gallery", "varanasi"]:
        for width in [360, 390, 768, 1440]:
            report["currentStep"] = f"{route} layout at {width}px"
            page.set_viewport_size({"width": width, "height": 900})
            page.goto(f"{BASE}/{route}", wait_until="networkidle")
            page.evaluate("""async () => {
                await document.fonts.ready;
                for (const image of document.images) image.loading = 'eager';
                await Promise.all([...document.images].map(image => image.decode()));
            }""")
            metrics = page.evaluate("""() => ({
                inner: innerWidth, client: document.documentElement.clientWidth,
                body: document.body.scrollWidth, title: document.title,
                titleLength: document.title.length,
                images: [...document.images].map(i => ({loaded:i.complete && i.naturalWidth > 0,src:i.currentSrc}))
            })""")
            assert metrics["inner"] == width, metrics
            assert metrics["body"] == metrics["client"], metrics
            assert all(image["loaded"] for image in metrics["images"]), metrics
            assert 50 <= metrics["titleLength"] <= 60, metrics
            report["layouts"].append({"route": route, "requestedWidth": width, **metrics})
            if width in [390, 1440]:
                page.screenshot(path=str(OUT / f"{route}-{width}.png"), full_page=True)

    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(f"{BASE}/gallery", wait_until="networkidle")
    report["currentStep"] = "Gallery filters and dialog"
    for category, count in [("Hotel", 4), ("Rooms", 6), ("Dining", 2), ("All", 12)]:
        page.get_by_role("button", name=category, exact=True).click()
        assert page.locator(".gallery-tile").count() == count
    report["gallery"]["filters"] = "Hotel 4 / Rooms 6 / Dining 2 / All 12"
    page.locator(".gallery-tile").first.click()
    dialog = page.locator(".gallery-dialog")
    assert dialog.evaluate("dialog => dialog.open")
    page.keyboard.press("Shift+Tab")
    assert page.evaluate("document.activeElement.getAttribute('aria-label')") == "Next photograph"
    report["gallery"]["focusTrap"] = "Shift+Tab from close wraps to next photograph"
    page.keyboard.press("ArrowRight")
    assert "02 / 12" in page.locator(".lightbox-description").inner_text()
    page.locator(".lightbox-image").evaluate("""element => {
        const start = new Touch({identifier:1,target:element,clientX:300,clientY:300});
        element.dispatchEvent(new TouchEvent('touchstart',{bubbles:true,touches:[start],changedTouches:[start]}));
        const end = new Touch({identifier:1,target:element,clientX:100,clientY:310});
        element.dispatchEvent(new TouchEvent('touchend',{bubbles:true,touches:[],changedTouches:[end]}));
    }""")
    assert "03 / 12" in page.locator(".lightbox-description").inner_text()
    report["gallery"]["navigation"] = "ArrowRight and horizontal swipe advance photographs"
    page.locator(".lightbox-image img").evaluate("image => image.decode()")
    page.screenshot(path=str(OUT / "gallery-dialog-390.png"))
    page.keyboard.press("Escape")
    assert not dialog.evaluate("dialog => dialog.open")
    assert page.evaluate("document.activeElement.getAttribute('aria-label')") == "Hotel lobby Hotel: enlarge photograph"
    report["gallery"]["close"] = "Escape closes and restores focus to opening photograph"
    page.goto(f"{BASE}/varanasi", wait_until="networkidle")
    report["currentStep"] = "Destination anchor navigation"
    for anchor in ["river", "temple", "aarti"]:
        assert page.locator(f"#{anchor}").count() == 1
        page.locator(f".destination-guide-nav a[href='#{anchor}']").click()
        assert page.evaluate("location.hash") == f"#{anchor}"
        header = page.locator(".site-header").bounding_box()
        target_y = page.locator(f"#{anchor}").bounding_box()["y"]
        assert header["y"] + header["height"] <= target_y <= 422, {"anchor": anchor, "top": target_y}
    report["anchors"] = ["river", "temple", "aarti"]
    context.close()
    browser.close()

(OUT / "verification.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
assert not report["errors"], report["errors"]
print(json.dumps({"layouts": len(report["layouts"]), "gallery": report["gallery"], "anchors": report["anchors"], "errors": report["errors"]}, indent=2))
