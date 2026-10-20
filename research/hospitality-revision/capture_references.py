"""Read-only live reference inspection. Never starts or writes to sibling projects."""
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent
OUT.mkdir(exist_ok=True)
targets = [
    ("vagmi", "https://hotelvagmi.com"),
    ("sgp", "https://sgphotels.com"),
    ("drake", "https://thedrake.ca"),
    ("ddd", "https://dddhotel.jp/"),
]
report = {"date": "2026-10-20", "references": [], "limitations": []}
with sync_playwright() as runner:
    browser = runner.chromium.launch(channel="msedge", headless=True)
    try:
        for slug, url in targets:
            entry = {"id": slug, "requestedUrl": url, "screens": []}
            context = browser.new_context(viewport={"width": 1440, "height": 1000}, reduced_motion="no-preference")
            page = context.new_page()
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(5000)
                for label in ["Accept all", "Allow all", "Accept All Cookies", "Accept cookies", "I agree"]:
                    candidate = page.get_by_role("button", name=label, exact=True)
                    if candidate.count() and candidate.first.is_visible():
                        candidate.first.click()
                        page.wait_for_timeout(500)
                        break
                try:
                    page.evaluate("() => Promise.race([document.fonts.ready,new Promise(resolve=>setTimeout(resolve,3000))])")
                except Exception:
                    pass
                entry["landedUrl"] = page.url
                entry["title"] = page.title()
                entry["headings"] = page.locator("h1,h2,h3").all_text_contents()
                entry["links"] = page.locator("a").evaluate_all("""nodes => nodes.filter(n=>n.innerText.trim())
                    .slice(0,80).map(n=>({text:n.innerText.trim(),href:n.href}))""")
                entry["typography"] = page.locator("h1,h2,nav a,p").evaluate_all("""nodes => nodes.filter(n=>n.getBoundingClientRect().height)
                    .slice(0,20).map(n=>{const s=getComputedStyle(n);return {tag:n.tagName,text:n.innerText.slice(0,120),
                    font:s.fontFamily,size:s.fontSize,weight:s.fontWeight,lineHeight:s.lineHeight,color:s.color}})""")
                entry["video"] = page.locator("video").evaluate_all("""nodes=>nodes.map(n=>({src:n.currentSrc,paused:n.paused,
                    time:n.currentTime,width:n.videoWidth,height:n.videoHeight,muted:n.muted,loop:n.loop}))""")
                for step, scroll in [("hero", 0), ("section", 1000), ("rooms", 2000)]:
                    if scroll:
                        page.mouse.wheel(0, 1000)
                        page.wait_for_timeout(1800)
                    path = OUT / f"{slug}-1440-{step}.png"
                    page.screenshot(path=str(path))
                    entry["screens"].append(path.name)
                # Mobile receives its own navigation and first-screen composition.
                page.set_viewport_size({"width": 390, "height": 844})
                page.reload(wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(4500)
                path = OUT / f"{slug}-390-hero.png"
                page.screenshot(path=str(path))
                entry["screens"].append(path.name)
                page.mouse.wheel(0, 700)
                page.wait_for_timeout(1500)
                path = OUT / f"{slug}-390-section.png"
                page.screenshot(path=str(path))
                entry["screens"].append(path.name)
                entry["mobileMetrics"] = page.evaluate("({width:innerWidth,body:document.body.scrollWidth})")
            except Exception as error:
                entry["error"] = str(error)
            finally:
                report["references"].append(entry)
                context.close()
                (OUT / "live-inspection.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        # Award records are read independently from the currently deployed sites.
        context = browser.new_context(viewport={"width":1440,"height":1000})
        page = context.new_page()
        report["awardRecords"] = []
        for slug, url in [
            ("drake", "https://www.awwwards.com/sites/the-drake-hotel"),
            ("ddd", "https://www.awwwards.com/sites/ddd-hotel"),
        ]:
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(2000)
                text = page.locator("body").inner_text()
                path = OUT / f"awwwards-{slug}.png"
                page.screenshot(path=str(path))
                report["awardRecords"].append({"id":slug,"url":page.url,"text":text[:9000],"screen":path.name})
            except Exception as error:
                report["limitations"].append({"url":url,"error":str(error)})
        context.close()
    finally:
        browser.close()
(OUT / "live-inspection.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"references":[{"id":r["id"],"url":r.get("landedUrl"),"screens":r["screens"],"error":r.get("error")} for r in report["references"]],"limitations":report["limitations"]}, indent=2))
