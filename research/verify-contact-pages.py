"""Independent contact/privacy UI review. Never sends a message."""
from pathlib import Path
from datetime import date, timedelta
from urllib.parse import urlparse, parse_qs
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "contact-review"
OUT.mkdir(parents=True, exist_ok=True)
results = []


def inspect(page, route, width):
    page.evaluate("document.documentElement.style.scrollBehavior='auto'")
    height = page.evaluate("document.documentElement.scrollHeight")
    for y in range(0, height, 650):
        page.evaluate("y => window.scrollTo(0,y)", y)
        page.wait_for_timeout(130)
    page.wait_for_timeout(600)
    page.evaluate("window.scrollTo(0,0)")
    page.wait_for_timeout(400)
    result = page.evaluate("""() => ({
      title: document.title,
      h1: [...document.querySelectorAll('h1')].map(x=>x.textContent),
      width: innerWidth,
      scrollWidth: document.body.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      badImages: [...document.images].filter(x=>!x.complete||!x.naturalWidth).map(x=>x.src),
      overflowElements: [...document.querySelectorAll('main *')].filter(x=>{
        const r=x.getBoundingClientRect(); return r.width>0&&(r.right>innerWidth+1||r.left< -1);
      }).slice(0,20).map(x=>({tag:x.tagName,cls:x.className,text:x.textContent.slice(0,80)}))
    })""")
    result.update(route=route)
    label = route.strip("/")
    page.screenshot(path=str(OUT / f"{label}-{width}-top.png"))
    page.screenshot(path=str(OUT / f"{label}-{width}-full.png"), full_page=True)
    return result


with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    for width in (390, 1440):
        context = browser.new_context(viewport={"width": width, "height": 900}, device_scale_factor=1)
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        for route in ("/contact", "/privacy"):
            errors.clear()
            response = page.goto("http://127.0.0.1:3080" + route, wait_until="networkidle", timeout=60000)
            result = inspect(page, route, width)
            result["status"] = response.status if response else None
            result["consoleErrors"] = list(errors)
            if route == "/contact":
                summaries = page.locator(".contact-faq-item summary")
                summaries.first.click()
                result["faqFirstOpened"] = page.locator(".contact-faq-item").first.get_attribute("open") is not None
                summaries.nth(1).focus()
                page.keyboard.press("Enter")
                result["faqKeyboardOpened"] = page.locator(".contact-faq-item").nth(1).get_attribute("open") is not None
                result["faqPreviousClosed"] = page.locator(".contact-faq-item").first.get_attribute("open") is None
                result["phoneHref"] = page.locator(".contact-phone").get_attribute("href")
                result["mapsHref"] = page.get_by_role("link", name="Open in Google Maps").get_attribute("href")
                result["duplicateFormHeadingVisible"] = page.locator(".contact-form-panel .form-heading").is_visible()
                page.goto("http://127.0.0.1:3080/contact?room=family-room#enquire", wait_until="networkidle")
                result["roomPreselection"] = page.locator("#room").input_value()
                page.get_by_role("button", name="Prepare WhatsApp enquiry").click()
                result["invalidFormFocus"] = page.evaluate("document.activeElement.id")
                result["invalidFormAlert"] = page.locator(".booking-form [role=alert]").inner_text()
                today = date.today()
                page.locator("#arrival").fill(str(today + timedelta(days=7)))
                page.locator("#departure").fill(str(today + timedelta(days=10)))
                page.locator("#name").fill("Review & Family")
                page.locator("#notes").fill("Please confirm arrival arrangements.")
                page.get_by_role("button", name="Prepare WhatsApp enquiry").click()
                draft = page.locator("#whatsapp-draft")
                result["draftHref"] = draft.get_attribute("href")
                result["draftFocus"] = page.evaluate("document.activeElement.id")
                result["draftMessage"] = parse_qs(urlparse(result["draftHref"]).query).get("text", [""])[0]
                result["submittedToWhatsApp"] = False
                page.locator("#enquire").screenshot(path=str(OUT / f"enquiry-{width}.png"))
            else:
                result["credits"] = page.locator(".privacy-credit").all_inner_texts()
                result["creditLinks"] = page.locator(".privacy-credit a").evaluate_all("els=>els.map(e=>e.href)")
            results.append(result)
            (OUT / "review-results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
            print(width, route, result["status"], "overflow", result["scrollWidth"] - result["clientWidth"], "badImages", len(result["badImages"]), flush=True)
        context.close()
    browser.close()
print("Contact/privacy review complete; no message sent.")
