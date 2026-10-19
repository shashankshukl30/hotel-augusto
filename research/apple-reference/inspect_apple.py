import json
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent
result = []
targets = [("iphone", "https://www.apple.com/iphone/"), ("macbook-pro", "https://www.apple.com/macbook-pro/")]

with sync_playwright() as runner:
    browser = runner.chromium.launch(channel="msedge", headless=True)
    for slug, url in targets:
        for width in [1440, 390]:
            context = browser.new_context(viewport={"width":width,"height":1000 if width>700 else 844}, device_scale_factor=1)
            page = context.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            page.evaluate("() => document.fonts.ready")
            page.wait_for_timeout(3500)
            page.screenshot(path=str(OUT / f"{slug}-{width}-hero.png"))
            data = page.evaluate("""() => ({
                url:location.href,title:document.title,width:innerWidth,
                headings:[...document.querySelectorAll('main h1,main h2,main h3')].filter(e=>e.getBoundingClientRect().width>0).slice(0,22).map(e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return{text:e.textContent.trim().replace(/\\s+/g,' '),font:s.fontFamily,size:s.fontSize,weight:s.fontWeight,lineHeight:s.lineHeight,tracking:s.letterSpacing,left:r.x,width:r.width,top:r.y}}),
                controls:[...document.querySelectorAll('.button,.card,.card-container,.gallery-item')].filter(e=>e.getBoundingClientRect().width>0).slice(0,12).map(e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return{tag:e.tagName,cls:e.className,text:e.textContent.trim().replace(/\\s+/g,' ').slice(0,80),font:s.fontSize,radius:s.borderRadius,padding:s.padding,width:r.width,height:r.height,background:s.backgroundColor}}),
                body:{font:getComputedStyle(document.body).fontFamily,size:getComputedStyle(document.body).fontSize,lineHeight:getComputedStyle(document.body).lineHeight}
            })""")
            headings = page.locator("h2")
            target = None
            for index in range(headings.count()):
                if not headings.nth(index).is_visible():
                    continue
                text = headings.nth(index).inner_text().strip()
                if "highlights" in text.lower() or "Switch to iPhone" in text:
                    target = headings.nth(index)
                    break
            if target:
                target.evaluate("element => element.scrollIntoView({block:'start'})")
                page.wait_for_timeout(1500)
                page.screenshot(path=str(OUT / f"{slug}-{width}-section.png"))
            result.append({"slug":slug,**data})
            context.close()
    for slug in ["layout","typography"]:
        page = browser.new_page(viewport={"width":1440,"height":1000})
        page.goto(f"https://developer.apple.com/design/human-interface-guidelines/{slug}",wait_until="domcontentloaded",timeout=45000)
        page.wait_for_timeout(2500)
        (OUT / f"hig-{slug}.txt").write_text(page.locator("body").inner_text(),encoding="utf-8")
        page.screenshot(path=str(OUT / f"hig-{slug}.png"))
        page.close()
    browser.close()
(OUT / "computed-styles.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))
