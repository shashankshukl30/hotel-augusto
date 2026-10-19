"""Read-only verification of the exact Google Maps link used by the website."""
from pathlib import Path
from datetime import datetime, timezone
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
URL = "https://www.google.com/maps/search/?api=1&query=Hotel+Augusto%2C+D+36%2F1%2C+Jangambari%2C+Varanasi"
result = {"checked_at": datetime.now(timezone.utc).isoformat(), "requested_url": URL}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True, device_scale_factor=1)
    try:
        page.goto(URL, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(5000)
        result.update({"url": page.url, "title": page.title(), "headings": page.locator("h1").all_text_contents()})
        text = page.locator("body").inner_text(timeout=10000)
        result["body_excerpt"] = text[:6000]
        result["hotel_name_found"] = "AUGUSTO" in text.upper()
        result["phone_found"] = "80817" in text
        result["address_found"] = "Jangambari" in text or "AUGUST KUNDA" in text.upper()
    except Exception as exc:
        result["error"] = str(exc)
    finally:
        browser.close()
(ROOT / "map-link-verification.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(result, indent=2, ensure_ascii=True))
