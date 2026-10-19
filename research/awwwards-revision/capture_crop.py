from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=p.chromium.launch(channel="msedge",headless=True)
    for width,height in [(1440,900),(390,844)]:
        page=browser.new_page(viewport={"width":width,"height":height},device_scale_factor=1)
        page.goto((ROOT/"crop-preview.html").as_uri(),wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.screenshot(path=str(ROOT/f"hero-crop-{width}.png"),full_page=True)
        print(width,page.evaluate("({body:document.body.scrollWidth,client:document.documentElement.clientWidth,images:[...document.images].every(i=>i.complete&&i.naturalWidth>0)})"))
        page.close()
    browser.close()
