"""Production QA for the hospitality revision. All booking tests stop at draft URLs."""
import argparse
import asyncio
import json
from datetime import datetime, timezone, date, timedelta
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ["/", "/hotel", "/rooms", "/rooms/compare", "/rooms/deluxe-room", "/rooms/deluxe-twin-room", "/rooms/family-room",
          "/dining", "/varanasi", "/gallery", "/guides", "/guides/first-visit-to-kashi", "/guides/arriving-in-godowlia",
          "/guides/choosing-your-room", "/contact", "/privacy", "/does-not-exist"]
parser = argparse.ArgumentParser()
parser.add_argument("--base-url", default="http://127.0.0.1:3080")
parser.add_argument("--smoke", action="store_true")
args = parser.parse_args()
BASE = args.base_url.rstrip("/")
OUT = ROOT / "evidence/hospitality-revision"
OUT.mkdir(exist_ok=True, parents=True)
report = {"started": datetime.now(timezone.utc).isoformat(), "base_url": BASE,
          "browser": "Fresh Microsoft Edge contexts", "external_messages_sent": 0,
          "viewport_checks": [], "accessibility": [], "interactions": [], "failures": []}

def save():
    (OUT / "production-qa.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

def check(name, passed, evidence=None):
    item = {"test": name, "passed": bool(passed), "evidence": evidence}
    report["interactions"].append(item)
    if not passed:
        report["failures"].append(item)
    save()

async def ready(page, route):
    response = await page.goto(BASE + route, wait_until="networkidle", timeout=60000)
    await page.evaluate("document.documentElement.style.scrollBehavior='auto'")
    await page.wait_for_timeout(100)
    return response

async def load_images(page):
    await page.evaluate("""async()=>{
      for (const img of document.images) if(img.loading==='lazy') img.loading='eager';
      await Promise.allSettled([...document.images].map(img=>img.decode()));
      for(let y=0;y<document.body.scrollHeight;y+=850){scrollTo(0,y);await new Promise(r=>setTimeout(r,25));}
      scrollTo(0,0);
    }""")
    await page.wait_for_timeout(150)

async def sweep(browser, width):
    context = await browser.new_context(viewport={"width":width,"height":900}, device_scale_factor=1)
    page = await context.new_page()
    runtime = []
    console = []
    page.on("pageerror", lambda error: runtime.append(str(error)))
    page.on("console", lambda message: console.append(message.text) if message.type=="error" else None)
    for route in ROUTES:
        runtime.clear(); console.clear()
        try:
            response = await ready(page, route)
            await load_images(page)
            state = await page.evaluate("""()=>{
              const header=document.querySelector('.site-header').getBoundingClientRect();
              const h1=document.querySelector('h1'),s=h1?getComputedStyle(h1):null;
              return {
                clientWidth:document.documentElement.clientWidth,bodyWidth:document.body.scrollWidth,
                title:document.title,titleLength:document.title.length,
                headings:[...document.querySelectorAll('h1')].map(e=>e.innerText),
                titleSize:s?.fontSize,titleFont:s?.fontFamily,
                schema:[...document.head.querySelectorAll('script[type="application/ld+json"]')].map(e=>JSON.parse(e.textContent)),
                missingImages:[...document.images].filter(e=>!e.complete||!e.naturalWidth).map(e=>e.currentSrc),
                missingAlt:[...document.images].filter(e=>!e.hasAttribute('alt')).map(e=>e.src),
                ids:[...document.querySelectorAll('[id]')].map(e=>e.id),
                links:[...document.querySelectorAll('a[href]')].map(e=>e.getAttribute('href')),
                header:{left:header.left,right:header.right},
                primaryControls:[...document.querySelectorAll('main .button, main .room-action')].filter(e=>e.getClientRects().length)
                  .map(e=>({text:e.innerText,height:e.getBoundingClientRect().height,size:getComputedStyle(e).fontSize}))
              };
            }""")
            issues = []
            expected = 404 if route=="/does-not-exist" else 200
            if response.status!=expected: issues.append(f"HTTP {response.status}")
            if state["clientWidth"]!=width or state["bodyWidth"]!=width: issues.append("Horizontal overflow")
            if len(state["headings"])!=1: issues.append("Requires exactly one h1")
            if not state["schema"]: issues.append("Missing head JSON-LD")
            if state["missingImages"] or state["missingAlt"]: issues.append("Broken/unlabelled image")
            if len(state["ids"])!=len(set(state["ids"])): issues.append("Duplicate IDs")
            if state["titleLength"]<50 or state["titleLength"]>60: issues.append("Title length outside release bounds")
            for control in state["primaryControls"]:
                if control["height"]<43 or float(control["size"].replace("px",""))<13: issues.append("Primary control too small")
            bad_links = []
            for href in state["links"]:
                if not href or not href.startswith("/") or href.startswith("//"): continue
                target = urlsplit(href).path
                if target not in ROUTES and not target.startswith(("/images/","/opengraph","/icon")):
                    bad_links.append(href)
            if bad_links: issues.append("Unknown internal route")
            # The intentional not-found fetch produces a browser's 404 console entry.
            actionable_console = [entry for entry in console if not (route=="/does-not-exist" and "404" in entry)]
            if runtime or actionable_console: issues.append("Browser runtime or console errors")
            item = {"route":route,"width":width,"passed":not issues,"issues":issues,"state":state,
                    "runtime":runtime.copy(),"console":actionable_console,"bad_links":bad_links}
            report["viewport_checks"].append(item)
            if issues: report["failures"].append({"route":route,"width":width,"issues":issues})
            if width in (390,1440):
                await page.add_script_tag(path=str(ROOT/"node_modules/axe-core/axe.min.js"))
                axe = await page.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}});return r.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))}));}")
                audit = {"route":route,"width":width,"violations":axe,"passed":not axe}
                report["accessibility"].append(audit)
                if axe: report["failures"].append(audit)
            save()
        except Exception as error:
            report["failures"].append({"route":route,"width":width,"error":str(error)})
            save()
    await context.close()

async def interactions(browser):
    context = await browser.new_context(viewport={"width":390,"height":844}, permissions=["clipboard-read","clipboard-write"])
    page = await context.new_page()
    errors = []
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.on("console",lambda m:errors.append(m.text) if m.type=="error" else None)
    await ready(page,"/")
    check("Hotel photography leads the homepage", await page.locator(".hero-photo").count()==3 and
          await page.locator(".hero-photo img").first.get_attribute("src") is not None)
    await page.get_by_role("button",name="Show the hotel lounge",exact=True).click()
    check("Hero manual scene selection and pause",await page.get_by_role("button",name="Show the hotel lounge",exact=True).get_attribute("aria-pressed")=="true" and await page.get_by_role("button",name="Play hotel slideshow",exact=True).count()==1)
    await page.get_by_role("button",name="Show guest rooms",exact=True).click()
    check("All three rooms are immediately discoverable",await page.locator(".home-room-spread").count()==3)
    bar = page.locator(".home-reservation .stay-bar")
    await bar.get_by_role("button",name="Plan my stay",exact=True).click()
    check("Stay bar rejects missing dates",await bar.locator("[role=alert]").count()==1 and "/contact" not in page.url)
    arrival=(date.today()+timedelta(days=45)).isoformat()
    departure=(date.today()+timedelta(days=48)).isoformat()
    await bar.locator("[name=arrival]").fill(arrival)
    await bar.locator("[name=departure]").fill(arrival)
    await bar.get_by_role("button",name="Plan my stay",exact=True).click()
    check("Stay bar rejects zero-night stays","Departure must be after" in await bar.inner_text())
    await bar.locator("[name=departure]").fill(departure)
    await bar.locator("[name=adults]").select_option("3")
    await bar.locator("[name=children]").select_option("1")
    await bar.locator("[name=room]").select_option("family-room")
    await bar.get_by_role("button",name="Plan my stay",exact=True).click()
    await page.wait_for_url("**/contact?**#enquire")
    await page.wait_for_timeout(350)
    restored={key:await page.locator("#"+key).input_value() for key in ["arrival","departure","adults","children","room"]}
    check("Travel preferences survive homepage-to-contact handoff",restored=={"arrival":arrival,"departure":departure,"adults":"3","children":"1","room":"Family Room"},restored)
    check("Handoff lands at the enquiry section",await page.locator("#enquire").evaluate("e=>{const r=e.getBoundingClientRect();return r.top>=0&&r.top<innerHeight}"))
    await page.locator("#name").fill("Asha & Ravi")
    await page.locator("#notes").fill("Arriving by train. Please confirm the family arrangement.")
    await page.get_by_role("button",name="Prepare WhatsApp enquiry",exact=True).click()
    draft=await page.locator("#whatsapp-draft").get_attribute("href")
    parts=urlsplit(draft);text=parse_qs(parts.query)["text"][0]
    check("WhatsApp draft uses the hotel number and every entered preference",parts.hostname=="wa.me" and parts.path=="/918081709146" and all(value in text for value in ["Asha & Ravi","3 adults","1 child","Family Room","Arriving by train."]),text)
    await page.locator("#notes").fill("Updated arrival details.")
    check("Editing invalidates a prepared enquiry",await page.locator("#whatsapp-draft").count()==0)
    await ready(page,"/contact?arrival=2020-01-01&departure=bad&adults=99&children=-1&room=fake#enquire")
    restored={key:await page.locator("#"+key).input_value() for key in ["arrival","departure","adults","children","room"]}
    check("Malformed URL preferences are discarded",restored=={"arrival":"","departure":"","adults":"2","children":"0","room":""},restored)
    await ready(page,"/")
    await page.get_by_role("button",name="Open navigation",exact=True).click()
    check("Mobile menu opens a native modal",await page.locator("dialog.navigation-dialog").evaluate("e=>e.open"))
    await page.keyboard.press("Escape")
    check("Mobile menu closes and restores keyboard focus",await page.get_by_role("button",name="Open navigation",exact=True).evaluate("e=>document.activeElement===e"))
    await page.get_by_role("button",name="Open navigation",exact=True).click()
    await page.locator(".navigation-content").get_by_role("link",name="Stay guide",exact=False).click()
    await page.wait_for_url("**/guides")
    check("Mobile navigation reaches the guide directory",await page.locator("main h1").count()==1 and not await page.locator(".navigation-dialog").evaluate("e=>e.open"))
    await ready(page,"/")
    for index in range(4):
        tab=page.locator(".itinerary-tabs [role=tab]").nth(index)
        await tab.click()
        check(f"City itinerary stage {index+1}",await tab.get_attribute("aria-selected")=="true" and await page.locator(".itinerary-copy:visible").count()==1)
    first=page.locator(".itinerary-tabs [role=tab]").first
    await first.focus();await page.keyboard.press("End")
    check("City itinerary keyboard selection",await page.locator(".itinerary-tabs [role=tab]").last.get_attribute("aria-selected")=="true")
    for label in ["By rail","By road","By air"]:
        await page.locator(".arrival-guide").get_by_role("tab",name=label,exact=True).click()
        check("Arrival guidance: "+label,await page.locator(".arrival-guide").get_by_role("tab",name=label,exact=True).get_attribute("aria-selected")=="true")
    check("Google map does not load without a visitor action",await page.locator(".arrival-guide iframe").count()==0)
    await page.locator(".arrival-guide").get_by_role("button",name="Copy address",exact=False).click()
    clipboard=await page.evaluate("navigator.clipboard.readText()")
    check("Copy address includes the hotel and street",all(x in clipboard for x in ["Hotel Augusto","D 36/1","August Kunda Road"]))
    await page.locator(".home-faq summary").first.click()
    check("Practical hotel answers expand",await page.locator(".home-faq details").first.evaluate("e=>e.open"))
    await ready(page,"/gallery")
    for category in ["Rooms","Dining","Hotel","All"]:
        await page.get_by_role("button",name=category,exact=True).click()
        check("Gallery filter: "+category,await page.locator(".gallery-grid button").count()>0)
    # Room/photo/compare route-specific tests are also recorded by the room QA runner.
    for slug in ["first-visit-to-kashi","arriving-in-godowlia","choosing-your-room"]:
        await ready(page,"/guides/"+slug)
        check("Guide article and practical FAQs: "+slug,await page.locator("main h2").count()>=3 and await page.locator("main details").count()>=2)
    await ready(page,"/")
    await page.evaluate("scrollTo(0,1800)")
    await page.reload(wait_until="networkidle")
    await page.wait_for_timeout(450)
    check("Reload restores the top",await page.evaluate("scrollY")<2)
    await page.evaluate("scrollTo(0,1400)")
    await page.locator(".site-header .brand-link").click()
    await page.wait_for_timeout(850)
    check("Same-route brand returns to the top",await page.evaluate("scrollY")<2)
    check("Functional journeys have no browser errors",not errors,errors)
    await context.close()

async def motion(browser):
    for reduced in [False,True]:
        context=await browser.new_context(viewport={"width":1440,"height":900},reduced_motion="reduce" if reduced else "no-preference")
        page=await context.new_page(); errors=[]
        page.on("pageerror",lambda e:errors.append(str(e)))
        page.on("console",lambda m:errors.append(m.text) if m.type=="error" else None)
        await ready(page,"/")
        await page.wait_for_timeout(400)
        await page.get_by_role("button",name="Show guest rooms",exact=True).click()
        def transform_script(selector):
            return f"()=>getComputedStyle(document.querySelector('{selector}')).transform"
        before=await page.evaluate(transform_script(".hero-photographs"))
        await page.evaluate("scrollTo(0,450)")
        await page.wait_for_timeout(300)
        after=await page.evaluate(transform_script(".hero-photographs"))
        check("Reduced motion disables hero parallax" if reduced else "Hero parallax responds to native scrolling",
              before==after if reduced else before!=after,{"before":before,"after":after})
        await page.locator(".itinerary-tabs [role=tab]").nth(1).click()
        await page.wait_for_timeout(600)
        check(("Reduced" if reduced else "Normal")+" motion leaves city content visible",await page.locator(".itinerary-copy:visible").count()==1)
        check(("Reduced" if reduced else "Normal")+" motion has no hydration/runtime errors",not errors,errors)
        await context.close()

async def main():
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True,channel="msedge")
        for width in ([390,1440] if args.smoke else [360,390,768,1024,1440,1920]):
            await sweep(browser,width)
        for name,fn in [("interactions",interactions),("motion",motion)]:
            try: await fn(browser)
            except Exception as error:
                report["failures"].append({"suite":name,"error":str(error)});save()
        await browser.close()
    report["completed"]=datetime.now(timezone.utc).isoformat()
    report["summary"]={"viewportChecks":len(report["viewport_checks"]),"axeAudits":len(report["accessibility"]),
                       "interactionChecks":len(report["interactions"]),"failures":len(report["failures"]),
                       "passed":not report["failures"]}
    save();print(json.dumps(report["summary"]))
    if report["failures"]: print(json.dumps(report["failures"],indent=2)[:16000])
    raise SystemExit(0 if not report["failures"] else 1)

asyncio.run(main())
