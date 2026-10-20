"""Focused production regression check after the mobile Enquire label change."""
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence/hospitality-revision"
BASE = "http://127.0.0.1:3080"
checks, layouts, audits, errors, warnings = [], [], [], [], []
before = {d: shutil.disk_usage(d + ":/").free for d in ["C", "D"]}


def check(name, passed, detail=None):
    checks.append({"name": name, "passed": bool(passed), "detail": detail})


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel="msedge")
    try:
        for width in [360, 390, 768, 1024, 1440, 1920]:
            context = browser.new_context(viewport={"width": width, "height": 1000 if width >= 768 else 844}, device_scale_factor=1)
            page = context.new_page()
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("console", lambda message: errors.append(message.text) if message.type == "error" else warnings.append(message.text) if message.type == "warning" else None)
            page.goto(BASE, wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            data = page.evaluate("""() => {
              const parts=['.brand-link','.desktop-nav','.header-book','.menu-trigger'];
              const nodes=parts.map(selector=>{const e=document.querySelector('.site-header '+selector),r=e.getBoundingClientRect(),s=getComputedStyle(e);return {selector,text:e.innerText,visible:s.display!=='none',x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom,fontSize:parseFloat(s.fontSize),scrollWidth:e.scrollWidth,clientWidth:e.clientWidth}});
              return {viewport:innerWidth,bodyWidth:document.body.scrollWidth,clientWidth:document.documentElement.clientWidth,headerHeight:document.querySelector('.site-header').getBoundingClientRect().height,nodes};
            }""")
            data["width"] = width
            layouts.append(data)
            brand, navigation, cta, menu = data["nodes"]
            visible = [item for item in data["nodes"] if item["visible"]]
            check(f"{width}: exact viewport and no body overflow", data["viewport"] == width and data["bodyWidth"] == data["clientWidth"])
            check(f"{width}: all header elements inside viewport", all(item["x"] >= 0 and item["right"] <= width + .5 and item["y"] >= 0 and item["bottom"] <= data["headerHeight"] + .5 for item in visible))
            ordered = sorted(visible, key=lambda item: item["x"])
            check(f"{width}: header elements do not overlap", all(a["right"] <= b["x"] + .5 for a, b in zip(ordered, ordered[1:])))
            check(f"{width}: brand remains visible", brand["visible"] and "AUGUSTO" in brand["text"] and brand["width"] > 100)
            check(f"{width}: booking link target at least44px", cta["width"] >= 44 and cta["height"] >= 44)
            check(f"{width}: correct readable booking label", cta["text"].strip() == ("Enquire" if width <= 600 else "Enquire & book") and cta["fontSize"] >= 12)
            check(f"{width}: booking label not clipped", cta["scrollWidth"] <= cta["clientWidth"] + 1)
            check(f"{width}: navigation breakpoint matches viewport", menu["visible"] == (width <= 1050) and navigation["visible"] == (width > 1050))
            if width in [360, 390, 1440]:
                page.screenshot(path=str(OUT / f"header-refinement-{width}.png"))
            if width <= 1050:
                page.locator(".site-header .brand-link").focus()
                page.keyboard.press("Tab")
                check(f"{width}: keyboard reaches Enquire after brand", page.locator(".header-book").evaluate("e=>e===document.activeElement"))
            else:
                page.locator(".header-book").focus()
            check(f"{width}: Enquire focus indicator visible", page.locator(".header-book").evaluate("e=>{const s=getComputedStyle(e);return e.matches(':focus-visible') && s.outlineStyle!=='none' && parseFloat(s.outlineWidth)>=2}"))
            page.keyboard.press("Enter")
            page.wait_for_url("**/contact#enquire")
            check(f"{width}: Enquire opens contact form anchor", page.locator("#enquire").count() == 1 and page.locator("form.booking-form").is_visible())
            if menu["visible"]:
                trigger = page.get_by_role("button", name="Open navigation", exact=True)
                trigger.focus()
                page.keyboard.press("Enter")
                dialog = page.get_by_role("dialog", name="Hotel Augusto navigation")
                check(f"{width}: keyboard opens menu", dialog.is_visible())
                page.keyboard.press("Escape")
                check(f"{width}: Escape closes menu and restores focus", not dialog.is_visible() and trigger.evaluate("e=>e===document.activeElement"))
                page.keyboard.press("Enter")
                dialog.get_by_role("link", name="Rooms", exact=False).click()
                page.wait_for_url("**/rooms")
                check(f"{width}: menu route navigation works and closes dialog", page.locator("h1").count() == 1 and not dialog.is_visible())
            context.close()
        context = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1)
        page = context.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
        for route in ["/", "/contact"]:
            page.goto(BASE + route, wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            await_images = """async()=>{await Promise.allSettled([...document.images].filter(i=>i.getBoundingClientRect().top<innerHeight).map(i=>i.decode()))}"""
            page.evaluate(await_images)
            page.add_script_tag(path=str(ROOT / "node_modules/axe-core/axe.min.js"))
            result = page.evaluate("""async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','best-practice']}});return {violations:r.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))})),passes:r.passes.length,incomplete:r.incomplete.length}}""")
            audits.append({"route": route, "width": 390, **result})
            check(f"390: axe {route}", not result["violations"], result["violations"])
        context.close()
    finally:
        browser.close()

check("No page or console errors", not errors, errors)
failed = [item for item in checks if not item["passed"]]
report = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "scope": "Focused regression after mobile header label and target-size refinement. Previous102-layout/34-axe/40-interaction suite remains the earlier baseline; this is a separate later run.",
    "baseUrl": BASE, "status": "fail" if failed else "pass", "browserClosed": True,
    "summary": {"layoutWidths": len(layouts), "axeAudits": len(audits), "checks": len(checks), "passed": len(checks) - len(failed), "failed": len(failed)},
    "checks": checks, "layouts": layouts, "axe": audits, "errors": errors, "warnings": warnings,
    "cleanup": {"beforeFreeBytes": before, "afterFreeBytes": {d: shutil.disk_usage(d + ":/").free for d in ["C", "D"]}, "removed": [], "reason": "Retained focused release screenshots, report and reproducible runner; no disposable files."},
}
path = OUT / "header-refinement-qa.json"
path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf8")
print(json.dumps({"summary": report["summary"], "failures": failed, "browserClosed": True}))
if failed:
    raise SystemExit(1)
