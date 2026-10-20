"""Verify the private Sites publication using an existing owner-scoped QA token.

The token is accepted through a hidden prompt and sent only to the exact Site
origin. This script does not create tokens or alter the Site's access policy.
"""
import argparse
import getpass
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--base-url", required=True)
parser.add_argument("--output", default="evidence/hospitality-revision/private-preview-qa.json")
args = parser.parse_args()
base = args.base_url.rstrip("/")
origin = urlsplit(base).netloc
token = getpass.getpass("Existing private Site QA token (hidden): ")
headers = {"OAI-Sites-Authorization": "Bearer " + token}
routes = ["/", "/hotel", "/rooms", "/rooms/compare", "/rooms/deluxe-room",
          "/rooms/deluxe-twin-room", "/rooms/family-room", "/dining", "/varanasi",
          "/gallery", "/guides", "/guides/first-visit-to-kashi",
          "/guides/arriving-in-godowlia", "/guides/choosing-your-room", "/group-stays", "/contact", "/privacy"]
report = {"date": datetime.now(timezone.utc).isoformat(), "base_url": base,
          "checks": [], "errors": [], "failed_responses": [], "external_messages_sent": 0}

def check(name, passed, detail=None):
    report["checks"].append({"name": name, "passed": bool(passed), "detail": detail})

def authorize(route):
    request = route.request
    if urlsplit(request.url).netloc == origin:
        route.continue_(headers={**request.headers, **headers})
    else:
        route.continue_()

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    context = browser.new_context(viewport={"width":390, "height":844})
    context.route("**/*", authorize)
    page = context.new_page()
    page.on("pageerror", lambda error: report["errors"].append(str(error)))
    page.on("console", lambda message: report["errors"].append({"text": message.text, "location": message.location}) if message.type == "error" else None)
    page.on("response", lambda response: report["failed_responses"].append({"url":response.url,"status":response.status,"resource_type":response.request.resource_type}) if response.status >= 400 else None)
    for path in routes:
        response = page.goto(base + path, wait_until="networkidle", timeout=60000)
        check("Clean URL renders " + path, response.status == 200 and page.locator("main h1").count() == 1,
              {"status": response.status, "title": page.title()})
        check("Mobile width " + path, page.evaluate("document.body.scrollWidth === document.documentElement.clientWidth"))
    missing = context.request.get(base + "/does-not-exist", headers=headers, max_redirects=0)
    check("Unknown route returns 404", missing.status == 404, missing.status)
    og = context.request.get(base + "/opengraph-image", headers=headers, max_redirects=0)
    check("Share image resolves as PNG", og.status == 200 and og.body().startswith(b"\x89PNG"),
          {"status":og.status, "content_type":og.headers.get("content-type")})
    page.goto(base + "/", wait_until="networkidle")
    page.evaluate("window.__augustoNavigationCheck = 'same-document'")
    page.get_by_role("button", name="Open navigation", exact=True).click()
    page.locator(".navigation-content").get_by_role("link", name="Stay guide", exact=False).click()
    page.wait_for_url("**/guides")
    check("Client navigation reaches guides", page.locator("main h1").count() == 1)
    check("Client navigation preserves the document",
          page.evaluate("window.__augustoNavigationCheck === 'same-document'"))
    arrival = (date.today() + timedelta(days=45)).isoformat()
    departure = (date.today() + timedelta(days=48)).isoformat()
    page.goto(base + f"/contact?arrival={arrival}&departure={departure}&adults=3&children=1&room=family-room#enquire", wait_until="networkidle")
    page.wait_for_timeout(200)
    check("Travel preferences hydrate on static contact page",
          page.locator("#room").input_value() == "Family Room"
          and page.locator("#adults").input_value() == "3"
          and page.locator("#arrival").input_value() == arrival)
    page.get_by_role("button", name="Prepare WhatsApp enquiry", exact=True).click()
    draft = page.locator("#whatsapp-draft").get_attribute("href")
    check("Static enquiry prepares the correct WhatsApp destination",
          draft.startswith("https://wa.me/918081709146?text="))
    page.set_viewport_size({"width":1440,"height":1000})
    page.goto(base + "/", wait_until="networkidle")
    page.wait_for_timeout(500)
    check("Desktop has no overflow", page.evaluate("document.body.scrollWidth === 1440"))
    check("Desktop property hero is present", page.locator(".hero-photo img").count() == 3)
    if "apple-dominant" in args.output:
        check("Published hero uses the current sans typography",
              page.locator("main h1").evaluate("e=>{const s=getComputedStyle(e);return s.fontFamily.toLowerCase().includes('inter') && Number(s.fontWeight)>=600;}"))
    check("No missing page resources", not report["failed_responses"], report["failed_responses"])
    check("No browser errors", not report["errors"], report["errors"])
    context.close()
    browser.close()
report["passed"] = all(item["passed"] for item in report["checks"])
output = ROOT / args.output
output.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps({"passed":report["passed"],"checks":len(report["checks"]),
                  "failures":[item for item in report["checks"] if not item["passed"]]}))
raise SystemExit(0 if report["passed"] else 1)
