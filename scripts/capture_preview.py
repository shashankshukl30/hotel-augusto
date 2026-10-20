from pathlib import Path
import argparse
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--base-url', default='http://127.0.0.1:3080')
parser.add_argument('--output', default='evidence/current-design')
args = parser.parse_args()
OUT = ROOT / args.output
OUT.mkdir(parents=True, exist_ok=True)
results = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel='msedge')
    for width, height in [(1440,1000),(390,844)]:
        context = browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1)
        page = context.new_page()
        errors = []
        page.on('pageerror',lambda error: errors.append(str(error)))
        page.goto(args.base_url,wait_until='networkidle')
        scene = page.get_by_role('button', name='Show guest rooms', exact=True)
        if scene.count():
            scene.click()
        page.evaluate("document.documentElement.style.scrollBehavior='auto'")
        for y in range(0,page.evaluate('document.body.scrollHeight'),700):
            page.evaluate('(y)=>window.scrollTo(0,y)',y)
            page.wait_for_timeout(80)
        page.evaluate('''async()=>{await Promise.allSettled([...document.images].filter(i=>i.getClientRects().length).map(i=>i.decode()))}''')
        page.evaluate('window.scrollTo(0,0)')
        page.wait_for_timeout(1200)
        page.screenshot(path=str(OUT/f'home-{width}-top.png'))
        page.screenshot(path=str(OUT/f'home-{width}-full.png'),full_page=True)
        results.append({'width':width,'actualWidth':page.evaluate('document.body.scrollWidth'),'font':page.locator('h1').evaluate('e=>getComputedStyle(e).fontFamily'),'h1':page.locator('h1').inner_text(),'errors':errors})
        context.close()
    browser.close()
(OUT/'capture.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results))
