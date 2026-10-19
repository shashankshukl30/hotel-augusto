"""Open the public WhatsApp landing page only. Do not continue or send."""
from pathlib import Path
from datetime import datetime, timezone
import json
from playwright.sync_api import sync_playwright

result = {"checked_at": datetime.now(timezone.utc).isoformat(), "url_requested": "https://wa.me/918081709146", "message_sent": False}
with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True)
    try:
        page.goto(result["url_requested"], wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(3500)
        result.update({"url": page.url, "title": page.title(), "headings": page.locator("h1").all_text_contents(), "text": page.locator("body").inner_text()[:7000]})
        result["registration_verified"] = False
        result["verification_limit"] = "A generic WhatsApp phone landing page is not proof that the number is registered or controlled by the hotel. No Continue/Send action taken."
    except Exception as exc:
        result["error"] = str(exc)
    finally:
        browser.close()
Path(__file__).with_name("whatsapp-public-check.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(result, indent=2, ensure_ascii=True))
