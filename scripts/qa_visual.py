"""Rendered type scale and scroll-motion checks for the Hotel Augusto QA runner."""

async def type_scale(page):
    return await page.evaluate("""() => {
      const metric=e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return {
        text:e.innerText.trim().slice(0,80),size:parseFloat(s.fontSize),
        weight:parseFloat(s.fontWeight),height:r.height
      }};
      return {
        heading:document.querySelector('h1')?metric(document.querySelector('h1')):null,
        controls:[...document.querySelectorAll('main .button,main .room-action,main form button[type="submit"]')].filter(e=>e.getClientRects().length).map(metric),
        body:[...document.querySelectorAll('.home-intro-note p,.rooms-masthead-description,.room-story-description,.room-overview-description')].map(metric)
      };
    }""")

def type_scale_failures(metrics,width,route):
    failures=[]
    heading=metrics['heading']
    minimum=48 if width<=600 or route=='/does-not-exist' else 56 if width<1024 else 64
    if not heading or heading['size']<minimum or heading['weight']<600:
        failures.append('Heading does not meet the larger type scale')
    if any(control['size']<14 or control['height']<49 for control in metrics['controls']):
        failures.append('Primary action is below the minimum type or touch size')
    if any(body['size']<(18 if width>=1024 else 17) for body in metrics['body']):
        failures.append('Main reading copy is below the larger type scale')
    return failures

async def hero_state(page):
    return await page.evaluate("""() => {
      const scene=document.querySelector('.hero-scene'),image=document.querySelector('.hero-scene-image');
      const matrix=e=>new DOMMatrixReadOnly(getComputedStyle(e).transform==='none'?undefined:getComputedStyle(e).transform);
      return {scale:matrix(scene).a,radius:parseFloat(getComputedStyle(scene).borderRadius),
        imageY:matrix(image).m42,imageHeight:image.getBoundingClientRect().height,
        documentHeight:document.documentElement.scrollHeight,scrollY};
    }""")

async def scroll_target(page,selector,viewport_fraction,after_element=False):
    target=await page.locator(selector).evaluate(
        "(e,args)=>Math.max(0,e.getBoundingClientRect().top+scrollY+(args.after?e.offsetHeight:0)-innerHeight*args.fraction)",
        {'fraction':viewport_fraction,'after':after_element})
    await page.evaluate('(top)=>scrollTo({top,behavior:"instant"})',target)
    await page.wait_for_timeout(160)
    return target

async def photo_state(page):
    return await page.locator('.home-intro-image').evaluate("""e=>{
      const layer=e.querySelector('.scroll-photo-layer'),s=getComputedStyle(layer);
      const matrix=new DOMMatrixReadOnly(s.transform==='none'?undefined:s.transform);
      const frame=e.getBoundingClientRect(),image=layer.getBoundingClientRect();
      return {y:matrix.m42,height:image.height,covered:image.top<=frame.top+1&&image.bottom>=frame.bottom-1};
    }""")

async def normal_motion_checks(page,add_check):
    before=await hero_state(page)
    target=await scroll_target(page,'.hero-scene-anchor',0)
    after=await hero_state(page)
    add_check('Hero image parallax responds to scroll',abs(after['imageY']-before['imageY'])>2,{'before':before,'after':after})
    add_check('Hero photograph expands with scroll and softens its corners',
        after['scale']>before['scale']+.01 and after['scale']<=1.001 and after['radius']<before['radius']-2,
        {'before':before,'after':after})
    add_check('Hero motion preserves native scrolling and stable page geometry',
        abs(after['scrollY']-target)<2 and abs(after['documentHeight']-before['documentHeight'])<2
        and abs(after['imageY'])<=after['imageHeight']*.04,
        {'requestedScroll':target,'before':before,'after':after})
    await scroll_target(page,'.scroll-statement',.95)
    before_words=await page.locator('.statement-line>span').evaluate_all('items=>items.map(e=>parseFloat(getComputedStyle(e).opacity))')
    await scroll_target(page,'.scroll-statement',.45,True)
    after_words=await page.locator('.statement-line>span').evaluate_all('items=>items.map(e=>parseFloat(getComputedStyle(e).opacity))')
    add_check('Scroll statement progressively reaches full legibility',
        bool(before_words) and len(before_words)==len(after_words)
        and any(a-b>.2 for b,a in zip(before_words,after_words))
        and all(a>=.99 for a in after_words),{'before':before_words,'after':after_words})
    await scroll_target(page,'.home-intro-image',.9)
    before_photo=await photo_state(page)
    await scroll_target(page,'.home-intro-image',.1,True)
    after_photo=await photo_state(page)
    add_check('Hotel photograph has bounded parallax without exposed image edges',
        abs(after_photo['y']-before_photo['y'])>2 and before_photo['covered'] and after_photo['covered']
        and all(abs(item['y'])<=item['height']*.041 for item in [before_photo,after_photo]),
        {'before':before_photo,'after':after_photo})
    await page.evaluate('scrollTo({top:0,behavior:"instant"})')

async def reduced_motion_checks(page,add_check):
    before=await hero_state(page)
    await scroll_target(page,'.hero-scene-anchor',0)
    after=await hero_state(page)
    add_check('Reduced motion disables hero parallax',abs(before['imageY'])<.01 and abs(after['imageY'])<.01,{'before':before,'after':after})
    add_check('Reduced motion keeps hero scale and corners static',
        all(abs(item['scale']-1)<.001 for item in [before,after])
        and abs(before['radius']-after['radius'])<.01,{'before':before,'after':after})
    words=await page.locator('.statement-line>span').evaluate_all('items=>items.map(e=>parseFloat(getComputedStyle(e).opacity))')
    add_check('Reduced motion presents every statement word at full opacity',bool(words) and all(opacity>=.99 for opacity in words),words)
    await scroll_target(page,'.home-intro-image',.9)
    before_photo=await photo_state(page)
    await scroll_target(page,'.home-intro-image',.1,True)
    after_photo=await photo_state(page)
    add_check('Reduced motion disables secondary photograph parallax',
        abs(before_photo['y'])<.01 and abs(after_photo['y'])<.01 and before_photo['covered'] and after_photo['covered'],
        {'before':before_photo,'after':after_photo})

async def mobile_room_stability(page,add_check):
    await page.locator('.room-tabs').scroll_into_view_if_needed()
    await page.wait_for_timeout(1000)
    states=[]
    for index in range(3):
        await page.get_by_role('tab').nth(index).click()
        await page.wait_for_timeout(550)
        states.append(await page.evaluate("""()=>{
          const panel=document.querySelector('#room-panel'),tabs=document.querySelector('.room-tabs');
          const p=panel.getBoundingClientRect(),t=tabs.getBoundingClientRect();
          return {panelHeight:p.height,panelTop:p.top+scrollY,tabsTop:t.top+scrollY,tabsLeft:t.left,
            heading:document.querySelector('.room-showcase-info[aria-hidden="false"] h3').innerText};
        }"""))
    stable=all(max(s[key] for s in states)-min(s[key] for s in states)<1
               for key in ['panelHeight','panelTop','tabsTop','tabsLeft'])
    add_check('Mobile room selection preserves panel and tab positions across all room types',
        stable and [s['heading'] for s in states]==['Deluxe Room','Deluxe Twin Room','Family Room'],states)
