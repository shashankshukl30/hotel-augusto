"""Complete Hotel Augusto browser QA. Does not open or send WhatsApp drafts."""
from pathlib import Path
from datetime import datetime, timezone, date, timedelta
from urllib.parse import urlsplit, parse_qs, unquote
import argparse, asyncio, json, shutil, time
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]
ROUTES=['/','/rooms','/rooms/deluxe-room','/rooms/deluxe-twin-room','/rooms/family-room','/varanasi','/gallery','/contact','/privacy','/does-not-exist']
WIDTHS=[360,390,768,1024,1440,1920]
AXE=ROOT/'node_modules'/'axe-core'/'axe.min.js'
parser=argparse.ArgumentParser()
parser.add_argument('--base-url',default='http://127.0.0.1:3080')
parser.add_argument('--output',default='qa-report.json')
parser.add_argument('--smoke',action='store_true',help='Production smoke at 390 and 1440; still runs axe and interactions.')
args=parser.parse_args()
BASE=args.base_url.rstrip('/')
OUT=ROOT/'evidence'
OUT.mkdir(exist_ok=True)
report={'started':datetime.now(timezone.utc).isoformat(),'base_url':BASE,'mode':'production-smoke' if args.smoke else 'comprehensive','browser':'Fresh headless Microsoft Edge contexts, deviceScaleFactor=1','viewports':[],'interactions':[],'failures':[],'notes':[],'external_messages_sent':0}
report_path=OUT/args.output

def save():
    temporary=report_path.with_suffix('.tmp')
    temporary.write_text(json.dumps(report,indent=2),encoding='utf-8')
    # Windows indexers/readers can briefly hold the destination without delete sharing.
    for attempt in range(12):
        try:
            temporary.replace(report_path)
            break
        except PermissionError:
            if attempt==11: raise
            time.sleep(.05*(attempt+1))

def add_check(name,passed,evidence=None):
    item={'test':name,'passed':bool(passed),'evidence':evidence}
    report['interactions'].append(item)
    if not passed: report['failures'].append({'type':'interaction',**item})
    save()

async def ready(page,route):
    response=await page.goto(BASE+route,wait_until='networkidle',timeout=60000)
    await page.evaluate("document.documentElement.style.scrollBehavior='auto'")
    await page.wait_for_timeout(100)
    return response

async def load_images(page):
    height=await page.evaluate('document.documentElement.scrollHeight')
    for y in range(0,height,800):
        await page.evaluate('(y)=>scrollTo(0,y)',y)
        await page.wait_for_timeout(45)
    await page.evaluate('''async()=>{await Promise.race([Promise.allSettled([...document.images].filter(i=>i.getClientRects().length>0).map(i=>i.decode())),new Promise(r=>setTimeout(r,12000))])}''')
    await page.evaluate('scrollTo(0,0)')
    await page.wait_for_timeout(120)

async def anchor_alignment(page,selector):
    return await page.locator(selector).evaluate('''e=>{const top=e.getBoundingClientRect().top;const expected=(parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop)||0)+(parseFloat(getComputedStyle(e).scrollMarginTop)||0);return {hash:location.hash,scrollY,top,expected,aligned:Math.abs(top-expected)<=2}}''')

async def sweep_width(browser,width,semaphore):
    async with semaphore:
        context=await browser.new_context(viewport={'width':width,'height':900},device_scale_factor=1)
        page=await context.new_page()
        page_errors=[]
        console_errors=[]
        page.on('pageerror',lambda e:page_errors.append(str(e)))
        page.on('console',lambda m:console_errors.append(m.text) if m.type=='error' else None)
        for route in ROUTES:
            page_errors.clear();console_errors.clear()
            try:
                response=await ready(page,route)
                await load_images(page)
                state=await page.evaluate('''() => ({
                  innerWidth,clientWidth:document.documentElement.clientWidth,bodyScrollWidth:document.body.scrollWidth,
                  h1:[...document.querySelectorAll('h1')].map(e=>e.textContent.trim()),
                  title:document.title,titleLength:document.title.length,
                  description:document.querySelector('meta[name=description]')?.content,
                  robots:document.querySelector('meta[name=robots]')?.content,
                  ogImage:document.querySelector('meta[property="og:image"]')?.content,
                  viewport:document.querySelector('meta[name=viewport]')?.content,
                  schemaInHead:[...document.head.querySelectorAll('script[type="application/ld+json"]')].map(s=>JSON.parse(s.textContent)),
                  images:[...document.images].filter(e=>e.getClientRects().length>0).map(e=>({alt:e.alt,source:e.currentSrc,complete:e.complete,naturalWidth:e.naturalWidth,width:Math.round(e.getBoundingClientRect().width),height:Math.round(e.getBoundingClientRect().height)})),
                  ids:[...document.querySelectorAll('[id]')].map(e=>e.id),
                  links:[...document.querySelectorAll('a[href]')].map(e=>({href:e.getAttribute('href'),name:(e.getAttribute('aria-label')||e.textContent).trim()})),
                  brokenAriaControls:[...document.querySelectorAll('[aria-controls]')].filter(e=>!document.getElementById(e.getAttribute('aria-controls'))).map(e=>({name:e.textContent,id:e.getAttribute('aria-controls')})),
                  overflows:[...document.querySelectorAll('body *:not(nextjs-portal)')].filter(e=>{const r=e.getBoundingClientRect();let left=r.left,right=r.right;for(let a=e.parentElement;a&&a!==document.body;a=a.parentElement){if(['hidden','clip','auto','scroll'].includes(getComputedStyle(a).overflowX)){const clip=a.getBoundingClientRect();left=Math.max(left,clip.left);right=Math.min(right,clip.right)}}return r.width>0&&(left < -1||right>innerWidth+1)&&getComputedStyle(e).position!=='fixed'}).slice(0,10).map(e=>({tag:e.tagName,class:String(e.className),left:e.getBoundingClientRect().left,right:e.getBoundingClientRect().right,text:e.textContent?.slice(0,60)}))
                })''')
                state.update(route=route,width=width,status=response.status if response else None,pageErrors=list(page_errors),consoleErrors=list(console_errors))
                state['failures']=[]
                expected=404 if route=='/does-not-exist' else 200
                if state['status']!=expected: state['failures'].append(f'HTTP {state["status"]}, expected {expected}')
                if state['innerWidth']!=width or state['clientWidth']!=width: state['failures'].append('CSS viewport mismatch')
                if state['bodyScrollWidth']!=state['clientWidth'] or state['overflows']: state['failures'].append('Horizontal overflow')
                if len(state['h1'])!=1: state['failures'].append('Expected exactly one H1')
                if not 50<=state['titleLength']<=60: state['failures'].append('Title outside 50-60 characters')
                if not state.get('description') or not state.get('ogImage') or not state.get('viewport'): state['failures'].append('Missing required metadata')
                if not any(s.get('@type')=='Hotel' for s in state['schemaInHead']): state['failures'].append('Hotel JSON-LD missing in head')
                if any(not i['complete'] or i['naturalWidth']==0 for i in state['images']): state['failures'].append('Visible image failed decode')
                if state['brokenAriaControls']: state['failures'].append('aria-controls references missing element')
                if page_errors: state['failures'].append('Browser runtime errors')
                meaningful_console=[e for e in console_errors if not (route=='/does-not-exist' and '404' in e)]
                if meaningful_console: state['failures'].append('Browser console errors')
                if width in [390,1440]:
                    await page.add_script_tag(path=str(AXE))
                    axe=await page.evaluate("async()=>{const r=await axe.run({exclude:[['nextjs-portal']]},{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return {violations:r.violations.map(v=>({id:v.id,impact:v.impact,description:v.description,help:v.help,helpUrl:v.helpUrl,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))})),passes:r.passes.length,incomplete:r.incomplete.length}}")
                    state['axe']=axe
                    if axe['violations']: state['failures'].append('axe violations')
                if route=='/' and width in [390,1440]:
                    await page.screenshot(path=str(OUT/f'qa-home-{width}.png'))
                if state['failures']:
                    report['failures'].append({'type':'viewport','route':route,'width':width,'failures':state['failures']})
                    if len(report['failures'])<=6: await page.screenshot(path=str(OUT/f'qa-problem-{route.strip("/").replace("/","-") or "home"}-{width}.png'))
                report['viewports'].append(state)
                save()
                print(f'{width:4} {route:26} {state["status"]} '+('PASS' if not state['failures'] else 'FAIL '+', '.join(state['failures'])),flush=True)
            except Exception as exc:
                report['failures'].append({'type':'execution','width':width,'route':route,'error':str(exc)})
                print('ERROR',width,route,str(exc),flush=True)
                save()
        await context.close()

async def interaction_checks(browser):
    context=await browser.new_context(viewport={'width':390,'height':844},device_scale_factor=1)
    page=await context.new_page()
    # All outbound actions are deliberately left unclicked. No messages are sent.
    await ready(page,'/')
    headline=await page.locator('#hero-title').inner_text()
    add_check('Final homepage headline is current', 'Augusto.' in headline and 'Varanasi, up close.' in headline,headline)
    await page.wait_for_timeout(300)
    before_parallax=await page.locator('.hero-scene-image').evaluate('e=>getComputedStyle(e).transform')
    await page.locator('.hero-scene').evaluate('e=>scrollTo(0,e.offsetTop+100)')
    await page.wait_for_timeout(300)
    after_parallax=await page.locator('.hero-scene-image').evaluate('e=>getComputedStyle(e).transform')
    add_check('Hero image parallax responds to scroll',before_parallax!=after_parallax,{'before':before_parallax,'after':after_parallax})
    await page.evaluate('scrollTo(0,0)')
    menu=page.get_by_role('button',name='Open navigation',exact=True)
    await menu.click()
    focused=await page.evaluate('document.activeElement.getAttribute("aria-label")')
    add_check('Mobile menu opens, focuses close, locks body',await page.locator('.navigation-dialog').evaluate('e=>e.open') and focused=='Close navigation' and await page.evaluate('getComputedStyle(document.body).overflow')=='hidden',focused)
    focus_sequence=[]
    for key in ['Shift+Tab','Shift+Tab','Tab','Tab']:
        await page.keyboard.press(key)
        focus_sequence.append(await page.evaluate('''()=>({tag:document.activeElement.tagName,inside:document.querySelector('.navigation-dialog').contains(document.activeElement),backgroundFocus:document.activeElement!==document.body&&!document.querySelector('.navigation-dialog').contains(document.activeElement)})'''))
    add_check('Mobile menu prevents focus to background controls',not any(s['backgroundFocus'] for s in focus_sequence),focus_sequence)
    await page.keyboard.press('Escape')
    add_check('Menu Escape closes and restores focus',not await page.locator('.navigation-dialog').evaluate('e=>e.open') and await menu.evaluate('e=>e===document.activeElement'))
    tabs=page.get_by_role('tab')
    await tabs.nth(0).focus()
    await page.keyboard.press('ArrowRight')
    add_check('Room tab ArrowRight updates selected and focus',await page.locator('[role=tab][aria-selected=true]').get_attribute('id')=='room-tab-1' and await tabs.nth(1).evaluate('e=>e===document.activeElement'))
    await page.keyboard.press('End')
    add_check('Room tab End selects last room',await page.locator('[role=tab][aria-selected=true]').get_attribute('id')=='room-tab-2')
    await page.keyboard.press('Home')
    add_check('Room tab Home selects first room',await page.locator('[role=tab][aria-selected=true]').get_attribute('id')=='room-tab-0')
    await page.keyboard.press('ArrowLeft')
    add_check('Room tab ArrowLeft wraps to last room',await page.locator('[role=tab][aria-selected=true]').get_attribute('id')=='room-tab-2')
    await page.set_viewport_size({'width':1440,'height':900})
    await page.get_by_role('button',name='Next room type',exact=True).click()
    add_check('Next room control wraps to first room',await page.locator('[role=tab][aria-selected=true]').get_attribute('id')=='room-tab-0')
    await page.get_by_role('button',name='Previous room type',exact=True).click()
    add_check('Previous room control wraps to last room',await page.locator('[role=tab][aria-selected=true]').get_attribute('id')=='room-tab-2')
    for index,slug in enumerate(['deluxe-room','deluxe-twin-room','family-room']):
        await tabs.nth(index).click()
        add_check('Room panel matches selected '+slug,await page.locator('#room-panel').get_attribute('aria-labelledby')=='room-tab-'+str(index) and await page.locator('#room-panel a').first.get_attribute('href')=='/rooms/'+slug)
        await page.wait_for_timeout(550)
        layers=await page.locator('.room-showcase-image>div').evaluate_all('items=>items.map(e=>({hidden:e.getAttribute("aria-hidden"),opacity:parseFloat(getComputedStyle(e).opacity),alt:e.querySelector("img").alt,decoded:e.querySelector("img").complete&&e.querySelector("img").naturalWidth>0}))')
        add_check('Room image crossfade settles correctly for '+slug,len(layers)==3 and all((v['opacity']>=.99 and v['alt'] and v['decoded']) if i==index else (v['opacity']<=.01 and v['hidden']=='true') for i,v in enumerate(layers)),layers)
    await page.set_viewport_size({'width':390,'height':844})
    await page.evaluate('scrollTo(0,1600)')
    await page.reload(wait_until='networkidle')
    add_check('Reload without hash returns to top',await page.evaluate('scrollY')<2,await page.evaluate('scrollY'))
    await page.evaluate('scrollTo(0,1600)')
    await page.locator('header .brand-link').click()
    await page.wait_for_timeout(900)
    add_check('Same-route navbar brand scrolls to top',await page.evaluate('scrollY')<2,await page.evaluate('scrollY'))
    await ready(page,'/contact#enquire')
    await page.wait_for_timeout(350)
    anchor=await anchor_alignment(page,'#enquire')
    add_check('Hash navigation aligns enquiry section below fixed header',anchor['aligned'],anchor)
    await page.reload(wait_until='networkidle')
    anchor=await anchor_alignment(page,'#enquire')
    add_check('Hash reload remains aligned to enquiry section',anchor['hash']=='#enquire' and anchor['aligned'],anchor)
    for anchor in ['river','temple','aarti']:
        await ready(page,'/varanasi#'+anchor)
        target=page.locator('#'+anchor)
        alignment=await anchor_alignment(page,'#'+anchor) if await target.count() else {'aligned':False,'missing':True}
        add_check('Varanasi #'+anchor+' target exists and aligns below fixed header',alignment['aligned'],alignment)
    await ready(page,'/gallery')
    for name,count in [('Hotel',4),('Rooms',6),('Dining',2),('All',12)]:
        await page.get_by_role('button',name=name,exact=True).click()
        add_check('Gallery filter '+name,await page.locator('.gallery-tile').count()==count,await page.locator('.gallery-tile').count())
    await page.locator('.gallery-tile').first.click()
    first_alt=await page.locator('.lightbox-image img').get_attribute('alt')
    await page.keyboard.press('ArrowRight')
    next_alt=await page.locator('.lightbox-image img').get_attribute('alt')
    add_check('Gallery arrow advances photograph',first_alt!=next_alt)
    await page.keyboard.press('Shift+Tab')
    add_check('Gallery dialog traps focus',await page.evaluate('document.querySelector(".gallery-dialog").contains(document.activeElement)'))
    await page.keyboard.press('Escape')
    add_check('Gallery Escape closes and restores tile focus',not await page.locator('.gallery-dialog').evaluate('e=>e.open') and await page.evaluate('document.activeElement.classList.contains("gallery-tile")'))
    await ready(page,'/contact?room=family-room#enquire')
    add_check('Room query preselects family room',await page.locator('#room').input_value()=='Family Room',await page.locator('#room').input_value())
    submit=page.get_by_role('button',name='Prepare WhatsApp enquiry',exact=False)
    await submit.click()
    add_check('Empty form reports required dates and focuses arrival',await page.locator('#arrival-error').count()==1 and await page.locator('#departure-error').count()==1 and await page.evaluate('document.activeElement.id')=='arrival')
    today=date.fromisoformat(await page.evaluate('new Date().getFullYear()+"-"+String(new Date().getMonth()+1).padStart(2,"0")+"-"+String(new Date().getDate()).padStart(2,"0")'))
    future=(today+timedelta(days=30)).isoformat();later=(today+timedelta(days=33)).isoformat()
    await page.locator('#arrival').fill(future)
    await page.locator('#departure').fill(future)
    await submit.click()
    add_check('Same-day departure rejected',await page.locator('#departure-error').count()==1 and 'after' in await page.locator('#departure-error').inner_text())
    await page.locator('#departure').fill((today+timedelta(days=29)).isoformat())
    await submit.click()
    add_check('Reversed dates rejected',await page.locator('#departure-error').count()==1 and await page.locator('#whatsapp-draft').count()==0)
    await page.locator('#arrival').fill((today-timedelta(days=1)).isoformat())
    await page.locator('#departure').fill(later)
    await submit.click()
    add_check('Past arrival rejected',await page.locator('#arrival-error').count()==1 and 'today or later' in await page.locator('#arrival-error').inner_text())
    await page.locator('#arrival').fill(future)
    await page.locator('#departure').fill(later)
    await page.locator('#adults').select_option('3')
    await page.locator('#children').select_option('2')
    await page.locator('#name').fill('QA Guest & Family')
    await page.locator('#notes').fill('Late arrival & quiet room?\nChildren ages 4 and 7.')
    await submit.click()
    draft=page.locator('#whatsapp-draft')
    href=await draft.get_attribute('href') if await draft.count() else ''
    parts=urlsplit(href);message=parse_qs(parts.query).get('text',[''])[0]
    add_check('Valid future enquiry prepares correctly encoded WhatsApp draft',parts.netloc=='wa.me' and parts.path=='/918081709146' and 'QA Guest & Family' in message and '3 adults, 2 children' in message and 'Family Room' in message and 'Late arrival & quiet room?\nChildren ages 4 and 7.' in message,{'urlHost':parts.netloc,'number':parts.path,'decodedMessage':message,'url':href})
    add_check('Draft receives keyboard focus',await draft.evaluate('e=>e===document.activeElement'))
    await page.locator('#notes').fill('Changed request')
    add_check('Changing form details invalidates old draft',await draft.count()==0 and await submit.count()==1)
    for slug,name in [('deluxe-room','Deluxe Room'),('deluxe-twin-room','Deluxe Twin Room'),('family-room','Family Room')]:
        await ready(page,'/rooms/'+slug)
        await page.get_by_role('link',name='Enquire about this room',exact=False).click()
        await page.wait_for_url('**/contact?room='+slug+'#enquire')
        await page.wait_for_timeout(150)
        add_check('Room-detail enquiry preselects '+name,await page.locator('#room').input_value()==name)
    await ready(page,'/rooms')
    lineup=page.locator('.room-lineup')
    await lineup.focus()
    await page.keyboard.press('ArrowRight')
    await page.wait_for_timeout(600)
    add_check('Mobile room comparison supports keyboard scrolling',await lineup.evaluate('e=>e.scrollLeft>0'),await lineup.evaluate('e=>({scrollLeft:e.scrollLeft,clientWidth:e.clientWidth,scrollWidth:e.scrollWidth})'))
    await lineup.evaluate('e=>e.scrollTo({left:0,behavior:"instant"})')
    await lineup.focus()
    focused_cards=[]
    for _ in range(9):
        await page.keyboard.press('Tab')
        await page.wait_for_timeout(100)
        focused_cards.append(await page.evaluate('''()=>{const e=document.activeElement,r=e.getBoundingClientRect();return {label:e.getAttribute('aria-label')||e.textContent,href:e.getAttribute('href'),left:r.left,right:r.right,visible:r.left>=0&&r.right<=innerWidth,inside:!!e.closest('.room-product')}}'''))
    add_check('Keyboard focus exposes all room comparison links',all(v['visible'] and v['inside'] for v in focused_cards),focused_cards)
    await menu.click()
    await page.get_by_role('navigation',name='Mobile navigation').get_by_role('link',name='Welcome',exact=False).click()
    await page.wait_for_url(BASE+'/')
    add_check('Mobile navigation links change route and close menu',not await page.locator('.navigation-dialog').evaluate('e=>e.open') and await page.locator('#hero-title').count()==1)
    await context.close()
    reduced=await browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce')
    page=await reduced.new_page()
    await ready(page,'/')
    add_check('Reduced motion preference honored',await page.evaluate('matchMedia("(prefers-reduced-motion: reduce)").matches') and await page.locator('#hero-title').evaluate('e=>getComputedStyle(e).opacity')=='1')
    await page.locator('.hero-scene').evaluate('e=>scrollTo(0,e.offsetTop+100)')
    await page.wait_for_timeout(100)
    transform=await page.locator('.hero-scene-image').evaluate('e=>getComputedStyle(e).transform')
    add_check('Reduced motion disables hero parallax',transform in ['none','matrix(1, 0, 0, 1, 0, 0)'],transform)
    await reduced.close()

async def main():
    before={d:shutil.disk_usage(d+':/').free for d in ['C','D']}
    async with async_playwright() as p:
        browser=await p.chromium.launch(channel='msedge',headless=True)
        sem=asyncio.Semaphore(2)
        widths=[390,1440] if args.smoke else WIDTHS
        await asyncio.gather(*(sweep_width(browser,width,sem) for width in widths))
        try: await interaction_checks(browser)
        except Exception as exc:
            report['failures'].append({'type':'interaction-execution','error':str(exc)})
            print('INTERACTION ERROR',str(exc),flush=True)
        # Cross-check internal links and hash targets against captured route IDs.
        route_ids={r['route']:set(r['ids']) for r in report['viewports']}
        invalid=[]
        for r in report['viewports']:
            for link in r['links']:
                href=link['href']
                if not href.startswith(('/','#')): continue
                parsed=urlsplit(href)
                target=parsed.path or r['route']
                if target not in route_ids: invalid.append({'from':r['route'],'href':href,'reason':'Unknown internal route'})
                elif parsed.fragment and unquote(parsed.fragment) not in route_ids[target]: invalid.append({'from':r['route'],'href':href,'reason':'Missing target id'})
        unique=list({json.dumps(i,sort_keys=True):i for i in invalid}.values())
        add_check('All rendered internal route and hash links resolve',not unique,unique)
        await browser.close()
    report['completed']=datetime.now(timezone.utc).isoformat()
    report['summary']={'viewportChecks':len(report['viewports']),'axeAudits':sum('axe'in r for r in report['viewports']),'interactionChecks':len(report['interactions']),'failures':len(report['failures']),'passed':not report['failures']}
    report['cleanup']={'freeBeforeBytes':before,'freeAfterBytes':{d:shutil.disk_usage(d+':/').free for d in ['C','D']},'removed':[],'note':'Fresh Edge contexts and browser closed. No disposable task files created; concise JSON and requested evidence screenshots retained.'}
    save()
    print(json.dumps(report['summary']),flush=True)

asyncio.run(main())
