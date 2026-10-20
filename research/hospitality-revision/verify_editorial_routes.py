"""Bounded responsive, interaction and accessibility checks for owned routes."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "qa-editorial"
OUT.mkdir(exist_ok=True)
BASE = os.environ.get("HOTEL_QA_URL", "http://127.0.0.1:3082")
ROUTES = ["gallery", "varanasi", "guides", "guides/first-visit-to-kashi", "guides/arriving-in-godowlia", "guides/choosing-your-room"]
report = {"layouts": [], "interactions": [], "accessibility": [], "errors": [], "consoleErrors": []}

def decode(page):
    page.evaluate("""async () => {
        await document.fonts.ready;
        for (const image of document.images) image.loading='eager';
        await Promise.all([...document.images].map(image=>image.decode()));
    }""")

def reveal_all(page):
    page.evaluate("scrollTo(0,0)")
    height = page.evaluate("document.documentElement.scrollHeight")
    for y in range(0, height, 650):
        page.evaluate("(y)=>scrollTo(0,y)", y)
        page.wait_for_timeout(70)
    page.wait_for_timeout(850)
    page.evaluate("scrollTo(0,0)")
    page.wait_for_timeout(200)

with sync_playwright() as runner:
    browser = runner.chromium.launch(channel="msedge", headless=True)
    context = browser.new_context(viewport={"width":390,"height":844}, reduced_motion="reduce")
    page = context.new_page()
    page.on("pageerror", lambda error: report["errors"].append({"message":str(error),"stack":error.stack,"url":page.url,"step":report.get("step")}))
    page.on("console", lambda message: report["consoleErrors"].append({"message":message.text,"url":page.url,"step":report.get("step")}) if message.type == "error" else None)
    try:
        for route in ROUTES:
            for width in [360, 390, 768, 1440]:
                report["step"] = f"{route} layout at {width}px"
                page.set_viewport_size({"width":width,"height":900})
                response = page.goto(f"{BASE}/{route}", wait_until="networkidle")
                assert response.status == 200, {"route":route,"status":response.status}
                decode(page)
                metrics = page.evaluate("""() => ({
                    inner:innerWidth,client:document.documentElement.clientWidth,body:document.body.scrollWidth,
                    title:document.title,titleLength:document.title.length,h1s:document.querySelectorAll('h1').length,
                    h1Font:getComputedStyle(document.querySelector('h1')).fontFamily,
                    images:[...document.images].map(i=>({loaded:i.complete&&i.naturalWidth>0,src:i.currentSrc}))
                })""")
                assert metrics["inner"] == width and metrics["body"] == metrics["client"], metrics
                assert all(image["loaded"] for image in metrics["images"]), metrics
                assert 50 <= metrics["titleLength"] <= 60 and metrics["h1s"] == 1, metrics
                report["layouts"].append({"route":route,"width":width,**metrics})
                if width in [390,1440]:
                    name = route.replace("/","-")
                    page.screenshot(path=str(OUT/f"{name}-{width}-top.png"))
                    if route in ["gallery","varanasi"]:
                        page.screenshot(path=str(OUT/f"{name}-{width}-full.png"),full_page=True)
                if width == 390:
                    await_script = ROOT/"node_modules/axe-core/axe.min.js"
                    page.add_script_tag(path=str(await_script))
                    result = page.evaluate("async()=>await axe.run(document.querySelector('main'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})")
                    violations = [{"id":v["id"],"impact":v["impact"],"nodes":[{"target":n["target"],"summary":n["failureSummary"]} for n in v["nodes"]]} for v in result["violations"]]
                    report["accessibility"].append({"route":route,"violations":violations})

        page.set_viewport_size({"width":390,"height":844})
        page.goto(f"{BASE}/gallery",wait_until="networkidle")
        report["step"] = "gallery interactions"
        for category,count in [("Hotel",4),("Rooms",6),("Dining",2),("All",12)]:
            page.get_by_role("button",name=category,exact=True).click()
            assert page.locator(".gallery-tile").count() == count
        page.locator(".gallery-tile").first.click()
        dialog = page.locator(".gallery-dialog")
        assert dialog.evaluate("d=>d.open")
        page.keyboard.press("Shift+Tab")
        assert page.evaluate("document.activeElement.getAttribute('aria-label')") == "Next photograph"
        page.keyboard.press("ArrowRight")
        assert "02 / 12" in page.locator(".lightbox-description").inner_text()
        page.locator(".lightbox-image").evaluate("""element=>{
            const start=new Touch({identifier:1,target:element,clientX:300,clientY:300});
            element.dispatchEvent(new TouchEvent('touchstart',{bubbles:true,touches:[start],changedTouches:[start]}));
            const end=new Touch({identifier:1,target:element,clientX:100,clientY:310});
            element.dispatchEvent(new TouchEvent('touchend',{bubbles:true,touches:[],changedTouches:[end]}));
        }""")
        assert "03 / 12" in page.locator(".lightbox-description").inner_text()
        page.locator(".lightbox-image img").evaluate("i=>i.decode()")
        page.screenshot(path=str(OUT/"gallery-dialog-390.png"))
        page.keyboard.press("Escape")
        assert not dialog.evaluate("d=>d.open")
        assert page.evaluate("document.activeElement.getAttribute('aria-label')") == "Hotel lobby Hotel: enlarge photograph"
        report["interactions"].append("Gallery: 4 filters/counts, native dialog, focus trap, arrow navigation, swipe, Escape and focus return passed.")

        for motion in ["reduce","no-preference"]:
            page.emulate_media(reduced_motion=motion)
            for width in [390,1440]:
                report["step"] = f"itinerary {motion} at {width}"
                page.set_viewport_size({"width":width,"height":900})
                page.goto(f"{BASE}/varanasi",wait_until="networkidle")
                decode(page)
                tabs = page.locator(".itinerary-tabs [role=tab]")
                tabs.first.scroll_into_view_if_needed()
                tabs.first.focus()
                page.keyboard.press("ArrowRight")
                assert tabs.nth(1).get_attribute("aria-selected") == "true"
                assert tabs.nth(1).evaluate("el=>el===document.activeElement")
                page.keyboard.press("End")
                assert tabs.nth(3).get_attribute("aria-selected") == "true"
                page.keyboard.press("Home")
                assert tabs.nth(0).get_attribute("aria-selected") == "true"
                heights = []
                for index in range(4):
                    tabs.nth(index).click()
                    page.wait_for_timeout(650)
                    assert tabs.nth(index).get_attribute("aria-selected") == "true"
                    assert page.locator(".itinerary-copy[aria-hidden=false]").count() == 1
                    assert page.locator(".itinerary-copy[inert]").count() == 3
                    heights.append(page.locator(".itinerary-panel").bounding_box()["height"])
                    assert page.evaluate("document.body.scrollWidth===document.documentElement.clientWidth")
                assert max(heights)-min(heights)<=1, heights
                tabs.first.click()
                page.wait_for_timeout(650)
                page.locator(".city-itinerary").screenshot(path=str(OUT/f"itinerary-{width}-{motion}.png"))
                report["interactions"].append({"itinerary":motion,"width":width,"keyboard":"ArrowRight/End/Home","allFourTabs":True,"panelHeights":heights,"inactivePanelsInert":True})

        page.emulate_media(reduced_motion="reduce")
        page.set_viewport_size({"width":390,"height":844})
        page.goto(f"{BASE}/varanasi",wait_until="networkidle")
        for anchor in ["river","temple","aarti"]:
            page.locator(f".destination-guide-nav a[href='#{anchor}']").click()
            assert page.evaluate("location.hash") == f"#{anchor}"
            top = page.locator(f"#{anchor}").bounding_box()["y"]
            header = page.locator(".site-header").bounding_box()
            assert header["y"]+header["height"]<=top<=422,{"anchor":anchor,"top":top}
        report["interactions"].append("City: river/temple/aarti anchors retain clear header offset.")

        for route in ROUTES[3:]:
            report["step"] = f"guide interactions {route}"
            page.goto(f"{BASE}/{route}",wait_until="networkidle")
            for item in page.locator(".guide-questions details").all():
                item.locator("summary").click()
                assert item.get_attribute("open") is not None
                item.locator("summary").click()
            toc = page.locator(".guide-contents ol a").nth(2)
            target = toc.get_attribute("href")
            toc.click()
            assert page.evaluate("location.hash") == target
            top = page.locator(target).bounding_box()["y"]
            header = page.locator(".site-header").bounding_box()
            assert header["y"]+header["height"]<=top<=260,{"route":route,"anchor":target,"top":top}
            assert page.locator(".guide-related a").count() == 2
            report["interactions"].append({"guide":route,"faqCount":3,"toc":target,"relatedGuides":2})

        page.emulate_media(reduced_motion="no-preference")
        for route in ["gallery","guides"]:
            page.goto(f"{BASE}/{route}",wait_until="networkidle")
            decode(page)
            reveal_all(page)
            report["interactions"].append({"normalMotionRoute":route,"overflow":page.evaluate("document.body.scrollWidth!==document.documentElement.clientWidth")})
            assert page.evaluate("document.body.scrollWidth===document.documentElement.clientWidth")
            page.screenshot(path=str(OUT/f"{route}-390-motion.png"))
        assert not report["errors"],report["errors"]
        assert not report["consoleErrors"],report["consoleErrors"]
        assert not any(item["violations"] for item in report["accessibility"]), report["accessibility"]
        report["passed"] = True
    finally:
        (OUT/"verification.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
        context.close()
        browser.close()
print(json.dumps({"passed":report.get("passed",False),"layouts":len(report["layouts"]),"accessibilityAudits":len(report["accessibility"]),"interactions":len(report["interactions"]),"runtimeErrors":report["errors"]},indent=2))
