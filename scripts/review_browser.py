"""Independent visual/content/accessibility review in clean Edge contexts."""
from pathlib import Path
import json, time
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'evidence'/'independent-review'
OUT.mkdir(parents=True,exist_ok=True)
BASE='http://127.0.0.1:3080'
ROUTES=['/','/gallery','/varanasi','/contact','/privacy']
results=[]

def sweep(page):
    page.evaluate("document.documentElement.style.scrollBehavior='auto'")
    height=page.evaluate('document.documentElement.scrollHeight')
    for y in range(0,height,600):
        page.evaluate('(y)=>window.scrollTo(0,y)',y)
        page.wait_for_timeout(90)
    page.wait_for_timeout(600)
    page.evaluate('''async()=>{await Promise.allSettled([...document.images].filter(i=>i.getClientRects().length>0).map(i=>i.decode()))}''')
    page.evaluate('window.scrollTo(0,0)')
    page.wait_for_timeout(250)

with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    for width in [390,1440]:
        context=browser.new_context(viewport={'width':width,'height':900},device_scale_factor=1)
        page=context.new_page()
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        for route in ROUTES:
            errors.clear()
            response=page.goto(BASE+route,wait_until='networkidle',timeout=60000)
            page.wait_for_timeout(650)
            sweep(page)
            label='home' if route=='/' else route.strip('/')
            page.screenshot(path=str(OUT/f'{label}-{width}-top.png'))
            page.screenshot(path=str(OUT/f'{label}-{width}-full.png'),full_page=True)
            state=page.evaluate('''() => ({
              width:innerWidth,scrollWidth:document.body.scrollWidth,clientWidth:document.documentElement.clientWidth,
              h1:[...document.querySelectorAll('h1')].map(e=>e.textContent),
              title:document.title,titleLength:document.title.length,
              images:[...document.images].map(e=>({src:e.currentSrc||e.getAttribute('src'),alt:e.alt,visible:e.getClientRects().length>0,complete:e.complete,naturalWidth:e.naturalWidth})),
              overflows:[...document.querySelectorAll('body *')].filter(e=>{let r=e.getBoundingClientRect();return r.width>0&&(r.right>innerWidth+1||r.left< -1)&&getComputedStyle(e).position!=='fixed'}).slice(0,20).map(e=>({tag:e.tagName,cls:e.className,left:e.getBoundingClientRect().left,right:e.getBoundingClientRect().right,text:e.textContent?.slice(0,80)})),
              badIdRefs:[...document.querySelectorAll('[aria-controls]')].filter(e=>!document.getElementById(e.getAttribute('aria-controls'))).map(e=>({text:e.textContent,controls:e.getAttribute('aria-controls')})),
              headings:[...document.querySelectorAll('h1,h2,h3')].map(e=>({level:e.tagName,text:e.textContent})),
              links:[...document.querySelectorAll('a')].map(e=>({text:e.textContent.trim(),label:e.getAttribute('aria-label'),href:e.getAttribute('href')})),
              menuVisible:!!document.querySelector('.menu-trigger')&&getComputedStyle(document.querySelector('.menu-trigger')).display!=='none'
            })''')
            state.update(route=route,status=response.status if response else None,errors=list(errors))
            results.append(state)
            print(width,route,'status',state['status'],'overflow',state['scrollWidth']-state['clientWidth'],'broken images',len([i for i in state['images'] if not i['complete'] or i['naturalWidth']==0]),flush=True)
            if route=='/':
                tabs=page.get_by_role('tab')
                tabresults=[]
                for i in range(tabs.count()):
                    tabs.nth(i).click()
                    page.wait_for_timeout(350)
                    tabresults.append(page.locator('.room-panel').evaluate('''e=>({text:e.innerText,image:e.querySelector('img').getAttribute('src'),decoded:e.querySelector('img').naturalWidth>0,links:[...e.querySelectorAll('a')].map(a=>a.getAttribute('href'))})'''))
                tabs.nth(0).focus()
                page.keyboard.press('ArrowRight')
                state['tabs']={'clicks':tabresults,'arrowFocus':page.evaluate('document.activeElement.textContent'),'selected':page.locator('[role=tab][aria-selected=true]').inner_text()}
                page.locator('.room-panel').screenshot(path=str(OUT/f'home-room-panel-{width}.png'))
                if width==390:
                    page.get_by_role('button',name='Open navigation',exact=True).click()
                    page.screenshot(path=str(OUT/'mobile-navigation.png'))
                    state['menu']={'open':page.locator('.navigation-dialog').evaluate('e=>e.open'),'bodyOverflow':page.evaluate('getComputedStyle(document.body).overflow'),'focus':page.evaluate('document.activeElement.outerHTML'),'width':page.locator('.navigation-dialog').bounding_box()['width']}
                    page.keyboard.press('Escape')
                    state['menu']['escapeClosed']=not page.locator('.navigation-dialog').evaluate('e=>e.open')
                    state['menu']['focusReturned']=page.evaluate("document.activeElement.getAttribute('aria-label')")
            if route=='/gallery':
                state['filters']=[]
                for name in ['Hotel','Rooms','Dining','All photographs']:
                    page.get_by_role('button',name=name,exact=True).click()
                    page.wait_for_timeout(300)
                    state['filters'].append({'name':name,'tiles':page.locator('.gallery-tile').count(),'count':page.locator('.gallery-count').inner_text()})
                first=page.locator('.gallery-tile').first
                first.click()
                page.wait_for_timeout(500)
                state['lightbox']={'open':page.locator('.gallery-dialog').evaluate('e=>e.open'),'image':page.locator('.lightbox-image img').get_attribute('alt'),'focus':page.evaluate('document.activeElement.getAttribute("aria-label")')}
                page.screenshot(path=str(OUT/f'gallery-lightbox-{width}.png'))
                page.keyboard.press('ArrowRight')
                page.wait_for_timeout(350)
                state['lightbox']['nextImage']=page.locator('.lightbox-image img').get_attribute('alt')
                page.keyboard.press('Escape')
                state['lightbox']['escapeClosed']=not page.locator('.gallery-dialog').evaluate('e=>e.open')
                state['lightbox']['restoredFocus']=page.evaluate('document.activeElement.className')
            (OUT/'review-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
        context.close()
    browser.close()
print('Wrote evidence to',OUT)
