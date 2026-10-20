import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "qa-editorial"
result = {"layouts":[],"consoleErrors":[],"runtimeErrors":[]}
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge",headless=True)
    c = b.new_context(viewport={"width":390,"height":900},reduced_motion="reduce")
    page = c.new_page()
    page.on("pageerror",lambda e:result["runtimeErrors"].append(str(e)))
    page.on("console",lambda m:result["consoleErrors"].append(m.text) if m.type=="error" else None)
    try:
        for width in [360,390,768,1440]:
            page.set_viewport_size({"width":width,"height":900})
            page.goto("http://127.0.0.1:3082/varanasi",wait_until="networkidle")
            page.evaluate("async()=>{await document.fonts.ready;for(const i of document.images)i.loading='eager';await Promise.all([...document.images].map(i=>i.decode()))}")
            assert page.evaluate("document.body.scrollWidth===document.documentElement.clientWidth")
            for anchor in ["river","temple","aarti"]:
                page.locator(f".destination-guide-nav a[href='#{anchor}']").click()
                assert page.evaluate("location.hash") == "#"+anchor
            result["layouts"].append({"route":"varanasi","width":width,"overflow":False,"anchors":True})
            if width in [390,1440]:
                page.evaluate("scrollTo(0,0)")
                page.screenshot(path=str(OUT/f"varanasi-{width}-full.png"),full_page=True)
                page.screenshot(path=str(OUT/f"varanasi-{width}-top.png"))
            if width==390:
                page.add_script_tag(path=str(ROOT/"node_modules/axe-core/axe.min.js"))
                violations=page.evaluate("async()=>(await axe.run(document.querySelector('main'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations")
                assert not violations,violations
                result["cityAxeViolations"]=[]
        for width in [390,1440]:
            page.set_viewport_size({"width":width,"height":900})
            page.goto("http://127.0.0.1:3082/guides/first-visit-to-kashi",wait_until="networkidle")
            page.locator("#understand-the-place").scroll_into_view_if_needed()
            page.screenshot(path=str(OUT/f"guide-body-{width}.png"))
            assert page.evaluate("document.body.scrollWidth===document.documentElement.clientWidth")
            page.locator(".guide-questions summary").first.click()
            page.locator(".guide-questions").screenshot(path=str(OUT/f"guide-faq-{width}.png"))
            result["layouts"].append({"route":"guide-body","width":width,"overflow":False})
        assert not result["runtimeErrors"] and not result["consoleErrors"],result
        result["passed"]=True
    finally:
        (OUT/"final-visual-verification.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
        c.close()
        b.close()
print(json.dumps(result,indent=2))
