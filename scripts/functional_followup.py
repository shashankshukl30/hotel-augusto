"""Targeted follow-up for ambiguous findings. No outbound links are activated."""
import asyncio, json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]

async def main():
    result = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='msedge', headless=True)
        context = await browser.new_context(viewport={'width':390,'height':844})
        page = await context.new_page()
        await page.goto('http://127.0.0.1:3080/',wait_until='networkidle')
        await page.get_by_role('button',name='Open navigation',exact=True).click()
        result['menuFocusSequence'] = []
        for key in ['', 'Shift+Tab', 'Shift+Tab', 'Tab', 'Tab', 'Tab']:
            if key: await page.keyboard.press(key)
            result['menuFocusSequence'].append(await page.evaluate('''(key)=>({key,tag:document.activeElement.tagName,text:document.activeElement.textContent.slice(0,80),label:document.activeElement.getAttribute('aria-label'),inside:document.querySelector('.navigation-dialog').contains(document.activeElement),backgroundFocus:document.activeElement!==document.body&&!document.querySelector('.navigation-dialog').contains(document.activeElement)})''',key))
        await page.keyboard.press('Escape')
        await page.goto('http://127.0.0.1:3080/contact#enquire',wait_until='networkidle')
        await page.wait_for_timeout(1300)
        expression='''()=>({hash:location.hash,scrollY,targetTop:document.getElementById('enquire').getBoundingClientRect().top,scrollMargin:getComputedStyle(document.getElementById('enquire')).scrollMarginTop,scrollRestoration:history.scrollRestoration})'''
        result['directHashNavigation'] = await page.evaluate(expression)
        await page.reload(wait_until='networkidle')
        await page.wait_for_timeout(1300)
        result['hashReload'] = await page.evaluate(expression)
        await browser.close()
    (ROOT/'evidence'/'functional-followup.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

asyncio.run(main())
