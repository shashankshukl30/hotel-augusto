"""Focused visual and interaction checks for enlarged hotel, dining and enquiry UI."""
from __future__ import annotations
import asyncio
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
BASE = "http://127.0.0.1:3082"
ROUTES = ["hotel", "dining", "contact", "privacy"]

async def motion_sample(browser, preference):
    context = await browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion=preference)
    page = await context.new_page()
    await page.goto(BASE + "/hotel", wait_until="networkidle")
    target = page.locator(".hospitality-welcome-heading > div").first
    await target.evaluate("(e)=>window.scrollTo({top:e.getBoundingClientRect().top+scrollY-300,behavior:'instant'})")
    await page.wait_for_timeout(100)
    start = await target.evaluate("(e)=>({transform:getComputedStyle(e).transform,opacity:getComputedStyle(e).opacity})")
    await page.wait_for_timeout(1100)
    end = await target.evaluate("(e)=>({transform:getComputedStyle(e).transform,opacity:getComputedStyle(e).opacity})")
    await context.close()
    return {"preference": preference, "start": start, "end": end}

async def main():
    records, interactions = [], []
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        for width in [390, 1440]:
            context = await browser.new_context(viewport={"width": width, "height": 1000}, reduced_motion="reduce")
            for route in ROUTES:
                page = await context.new_page()
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                response = await page.goto(BASE + "/" + route, wait_until="networkidle")
                await page.evaluate("document.fonts.ready")
                await page.locator("footer").scroll_into_view_if_needed()
                await page.wait_for_timeout(150)
                await page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
                await page.screenshot(path=str(OUT / f"{route}-{width}.png"), full_page=True)
                data = await page.evaluate("""() => ({
                    h1:document.querySelector('h1')?.innerText,
                    title:document.title,scrollWidth:document.body.scrollWidth,clientWidth:document.documentElement.clientWidth,
                    headline:{size:getComputedStyle(document.querySelector('h1')).fontSize,weight:getComputedStyle(document.querySelector('h1')).fontWeight},
                    images:[...document.querySelectorAll('main img')].map(i=>({alt:i.alt,loaded:i.complete&&i.naturalWidth>0})),
                    smallText:[...document.querySelectorAll('main p,main figcaption,main label')].filter(e=>e.textContent.trim()&&parseFloat(getComputedStyle(e).fontSize)<14).map(e=>({text:e.textContent.slice(0,70),size:getComputedStyle(e).fontSize}))
                })""")
                data.update({"route":route,"viewport":width,"status":response.status,"errors":errors})
                records.append(data)
                if route == "contact":
                    date_metrics = await page.locator("#arrival, #departure").evaluate_all("""es=>es.map(e=>({id:e.id,font:getComputedStyle(e).fontSize,height:e.getBoundingClientRect().height,x:e.getBoundingClientRect().x,y:e.getBoundingClientRect().y,width:e.getBoundingClientRect().width}))""")
                    first_date, second_date = date_metrics
                    dates_aligned = (
                        abs(first_date["x"] - second_date["x"]) < 1
                        and abs(first_date["width"] - second_date["width"]) < 1
                        and second_date["y"] >= first_date["y"] + first_date["height"]
                    ) if width <= 420 else abs(first_date["y"] - second_date["y"]) < 1
                    await page.get_by_role("button", name="Prepare WhatsApp enquiry").click()
                    invalid = await page.locator("#arrival").evaluate("(e)=>document.activeElement===e&&e.getAttribute('aria-invalid')==='true'")
                    arrival = (datetime.now().date() + timedelta(days=28)).isoformat()
                    departure = (datetime.now().date() + timedelta(days=30)).isoformat()
                    await page.locator("#arrival").fill(arrival)
                    await page.locator("#departure").fill(departure)
                    await page.locator("#name").fill("Website preview")
                    await page.get_by_role("button", name="Prepare WhatsApp enquiry").click()
                    draft = page.locator("#whatsapp-draft")
                    await draft.wait_for(state="visible")
                    href = await draft.get_attribute("href")
                    message = parse_qs(urlparse(href).query).get("text", [""])[0]
                    expected_dates = [f"{datetime.fromisoformat(value).day} {datetime.fromisoformat(value):%b %Y}" for value in [arrival, departure]]
                    faq = page.locator(".contact-faq-item").first
                    await faq.locator("summary").focus()
                    await page.keyboard.press("Enter")
                    faq_open = await faq.get_attribute("open") is not None
                    focus = await page.locator("#arrival").evaluate("(e)=>{e.focus();return getComputedStyle(e).boxShadow}")
                    interactions.append({"viewport":width,"dateFields":date_metrics,"dateLayout":"stacked" if width <= 420 else "paired","dateFieldsAligned":dates_aligned,"invalidFocus":invalid,"draftPhoneCorrect":urlparse(href).netloc=="wa.me" and urlparse(href).path=="/918081709146","draftDatesIncluded":all(date in message for date in expected_dates),"faqKeyboardOpens":faq_open,"focusRing":focus,"messagesSent":0})
                await page.close()
                print(json.dumps({"route":route,"width":width,"overflow":data["scrollWidth"]!=data["clientWidth"],"errors":errors,"smallText":len(data["smallText"])}), flush=True)
            await context.close()
        motions = [await motion_sample(browser, p) for p in ["no-preference", "reduce"]]
        await browser.close()
    (OUT / "hospitality-review.json").write_text(json.dumps(records,indent=2),encoding="utf-8")
    (OUT / "hospitality-interactions.json").write_text(json.dumps({"completed":datetime.now(timezone.utc).isoformat(),"interactions":interactions,"motion":motions,"messagesSent":0},indent=2),encoding="utf-8")
    print(json.dumps({"interactions":interactions,"motion":motions},indent=2),flush=True)

if __name__ == "__main__":
    asyncio.run(main())
