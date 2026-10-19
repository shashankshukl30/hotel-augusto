import asyncio
import json
import sys
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent
SITES = [
    ("kaskady", "https://www.resortkaskady.com/"),
    ("drake", "https://www.thedrake.ca/"),
    ("casa-cook", "https://casacook.com/"),
]

async def inspect(browser, slug, url):
    results = []
    for width in (1440, 390):
        context = await browser.new_context(viewport={"width": width, "height": 900 if width == 1440 else 844}, device_scale_factor=1)
        page = await context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=45000)
            await page.wait_for_timeout(7000)
            for name in ["Reject all", "Decline", "Accept all", "Accept All", "Allow all", "Accept cookies", "Accept", "I agree"]:
                control = page.get_by_role("button", name=name, exact=True)
                if await control.count() and await control.first.is_visible():
                    await control.first.click(timeout=3000)
                    break
            await page.wait_for_timeout(1500)
            await page.screenshot(path=str(ROOT / f"{slug}-{width}-hero.png"))
            content = await page.evaluate("""() => ({title:document.title,url:location.href,h1:[...document.querySelectorAll('h1')].map(e=>e.innerText),navigation:[...document.querySelectorAll('header a, nav a')].slice(0,50).map(e=>({text:e.innerText.trim(),href:e.href})),bodyWidth:document.body.scrollWidth,viewport:innerWidth,images:[...document.images].filter(e=>e.getBoundingClientRect().top<innerHeight).map(e=>({src:e.currentSrc,loaded:e.complete&&e.naturalWidth>0})),text:document.body.innerText.slice(0,12000)})""")
            await page.evaluate("window.scrollTo(0, Math.round(innerHeight*.82))")
            await page.wait_for_timeout(1700)
            await page.screenshot(path=str(ROOT / f"{slug}-{width}-section.png"))
            content.update(slug=slug,width=width,errors=errors)
            results.append(content)
        except Exception as error:
            results.append({"slug":slug,"width":width,"error":str(error)})
        finally:
            await context.close()
    return results

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge",headless=True)
        sites = [site for site in SITES if len(sys.argv) == 1 or site[0] == sys.argv[1]]
        groups = await asyncio.gather(*(inspect(browser,*site) for site in sites))
        await browser.close()
    results = [r for group in groups for r in group]
    if len(sys.argv) > 1 and (ROOT / "live-inspection.json").exists():
        previous = json.loads((ROOT / "live-inspection.json").read_text(encoding="utf-8"))
        results = [r for r in previous if r.get("slug") != sys.argv[1]] + results
    (ROOT / "live-inspection.json").write_text(json.dumps(results,indent=2),encoding="utf-8")
    print(json.dumps([{k:v for k,v in r.items() if k in ["slug","width","title","url","error"]} for r in results],indent=2))

asyncio.run(main())
