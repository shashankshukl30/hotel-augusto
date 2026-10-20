"""Check the Vercel preview with a temporary, scoped automation credential.

Uses the authenticated Vercel CLI. The credential stays in memory, is sent only
to the exact deployment origin, and is revoked in finally. No messages are sent.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ROUTES = [
    "/", "/hotel", "/rooms", "/rooms/compare", "/rooms/deluxe-room",
    "/rooms/deluxe-twin-room", "/rooms/family-room", "/dining", "/varanasi",
    "/gallery", "/guides", "/guides/first-visit-to-kashi",
    "/guides/arriving-in-godowlia", "/guides/choosing-your-room",
    "/group-stays", "/contact", "/privacy",
]
parser = argparse.ArgumentParser()
parser.add_argument("--base-url", required=True)
parser.add_argument("--project", required=True)
parser.add_argument("--scope", required=True)
parser.add_argument("--output", default="evidence/vercel-release/browser-qa.json")
args = parser.parse_args()
base = args.base_url.rstrip("/")
origin = urlsplit(base)
if origin.scheme != "https" or not origin.hostname.endswith(".vercel.app"):
    raise ValueError("Expected an HTTPS Vercel deployment URL")
cli = shutil.which("vercel.cmd") or shutil.which("vercel")
if not cli:
    raise RuntimeError("Authenticated Vercel CLI is required")
output = ROOT / args.output
output.parent.mkdir(parents=True, exist_ok=True)
report = {
    "date": datetime.now(timezone.utc).isoformat(), "base_url": base,
    "checks": [], "errors": [], "failed_responses": [],
    "external_messages_sent": 0,
    "temporary_qa_credential_created": False,
    "temporary_qa_credential_revoked": False,
}


def api(path, payload=None):
    command = [cli, "api", path, "--scope", args.scope]
    if payload is not None:
        command += ["--method", "PATCH", "--input", "-"]
    result = subprocess.run(
        command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
        input=json.dumps(payload) if payload is not None else None,
        env={**os.environ, "NO_UPDATE_NOTIFIER": "1"}, timeout=60,
    )
    if result.returncode:
        # Responses and stderr can contain credentials: never persist either.
        raise RuntimeError(f"Vercel API request failed: {path}")
    return json.loads(result.stdout)


def check(name, passed, detail=None):
    report["checks"].append({"name": name, "passed": bool(passed), "detail": detail})


secret = None
try:
    project = api(f"/v9/projects/{args.project}")
    check("GitHub integration uses the intended repository",
          project.get("link", {}).get("org") == "shashankshukl30"
          and project.get("link", {}).get("repo") == "hotel-augusto")
    protection_before = project.get("ssoProtection")
    known_secrets = set((project.get("protectionBypass") or {}).keys())
    generated = api(
        f"/v1/projects/{args.project}/protection-bypass",
        {"generate": {"note": "Temporary Hotel Augusto browser verification"}},
    )
    new_secrets = set((generated.get("protectionBypass") or {}).keys()) - known_secrets
    if len(new_secrets) != 1:
        raise RuntimeError("Could not isolate the temporary QA credential")
    secret = new_secrets.pop()
    report["temporary_qa_credential_created"] = True
    headers = {"x-vercel-protection-bypass": secret}

    def authorize(route):
        request = route.request
        if urlsplit(request.url).netloc == origin.netloc:
            route.continue_(headers={**request.headers, **headers})
        else:
            route.continue_()

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(viewport={"width": 390, "height": 844})
        context.route("**/*", authorize)
        page = context.new_page()
        page.on("pageerror", lambda error: report["errors"].append(str(error)))
        page.on("console", lambda message: report["errors"].append(message.text)
                if message.type == "error" else None)
        page.on("response", lambda response: report["failed_responses"].append({
            "url": response.url, "status": response.status,
            "resource_type": response.request.resource_type,
        }) if response.status >= 400 else None)
        for path in ROUTES:
            response = page.goto(base + path, wait_until="networkidle", timeout=60000)
            check("Clean URL renders " + path,
                  response.status == 200 and page.locator("main h1").count() == 1,
                  {"status": response.status, "heading": page.locator("main h1").inner_text()})
            check("Mobile width " + path, page.evaluate(
                "document.body.scrollWidth === document.documentElement.clientWidth"))
            check("Booking dock available " + path, page.locator(".booking-dock").is_visible())
            if path in ["/", "/rooms", "/dining", "/contact"]:
                page.screenshot(path=str(output.parent / (
                    "mobile-" + (path.strip("/") or "home") + ".png")))
            print("Checked mobile route " + path, flush=True)
        missing = context.request.get(base + "/does-not-exist", headers=headers)
        check("Unknown route returns 404", missing.status == 404, missing.status)
        og = context.request.get(base + "/opengraph-image", headers=headers)
        check("Share image resolves as PNG",
              og.status == 200 and og.body().startswith(b"\x89PNG"))
        robots = context.request.get(base + "/robots.txt", headers=headers)
        check("Preview remains noindex", robots.status == 200 and "Disallow: /" in robots.text())
        page.goto(base + "/", wait_until="networkidle")
        page.evaluate("window.__augustoNavigationCheck = 'same-document'")
        page.get_by_role("button", name="Open navigation", exact=True).click()
        page.locator(".navigation-content").get_by_role(
            "link", name="Stay guide", exact=False).click()
        page.wait_for_url("**/guides")
        check("Client navigation reaches guides", page.locator("main h1").count() == 1)
        check("Client navigation preserves the document",
              page.evaluate("window.__augustoNavigationCheck === 'same-document'"))
        arrival = (date.today() + timedelta(days=45)).isoformat()
        departure = (date.today() + timedelta(days=48)).isoformat()
        page.goto(base + f"/contact?arrival={arrival}&departure={departure}"
                  "&adults=3&children=1&room=family-room#enquire",
                  wait_until="networkidle")
        page.wait_for_function(
            "(value)=>document.querySelector('#arrival').value===value", arg=arrival)
        check("Travel preferences hydrate on contact",
              page.locator("#room").input_value() == "Family Room"
              and page.locator("#adults").input_value() == "3"
              and page.locator("#arrival").input_value() == arrival)
        page.get_by_role("button", name="Prepare WhatsApp enquiry", exact=True).click()
        draft = page.locator("#whatsapp-draft").get_attribute("href")
        check("Enquiry prepares correct WhatsApp destination",
              draft.startswith("https://wa.me/918081709146?text="))
        page.locator("#name").fill("Preview verification")
        page.locator("#notes").fill("Please confirm arrival guidance.")
        page.locator("#roomCount").select_option("3")
        revised_arrival = (date.today() + timedelta(days=50)).isoformat()
        revised_departure = (date.today() + timedelta(days=53)).isoformat()
        page.locator("#dock-arrival").fill(revised_arrival)
        page.locator("#dock-departure").fill(revised_departure)
        page.locator(".dock-submit").click()
        page.wait_for_function(
            "(value)=>document.querySelector('#arrival').value===value", arg=revised_arrival)
        check("Dock preserves unfinished contact details",
              page.locator("#name").input_value() == "Preview verification"
              and page.locator("#notes").input_value() == "Please confirm arrival guidance."
              and page.locator("#roomCount").input_value() == "3"
              and page.locator("#children").input_value() == "1"
              and page.locator("#room").input_value() == "Family Room")
        check("Personal text stays out of URL",
              "Preview" not in page.url and "guidance" not in page.url)
        for asset in ["/brand/logo.jpeg", "/downloads/hotel-augusto-dining-guide.pdf"]:
            response = context.request.get(base + asset, headers=headers)
            expected = (ROOT / "public" / asset.lstrip("/")).read_bytes()
            check("Published asset matches source " + asset,
                  response.status == 200 and
                  hashlib.sha256(response.body()).digest() == hashlib.sha256(expected).digest())
        page.set_viewport_size({"width": 1440, "height": 1000})
        response = page.goto(base + "/", wait_until="networkidle")
        page.wait_for_timeout(500)
        check("Desktop has no overflow", page.evaluate("document.body.scrollWidth === 1440"))
        check("Desktop property hero is present", page.locator(".hero-photo img").count() == 3)
        check("Desktop hero image loaded", page.locator(".hero-photo img").evaluate_all(
            "imgs => imgs.some(img => img.complete && img.naturalWidth > 0)"))
        check("Current sans typography", page.locator("main h1").evaluate(
            "e=>{const s=getComputedStyle(e);return s.fontFamily.toLowerCase().includes('inter')"
            " && Number(s.fontWeight)>=600;}"))
        check("Hosted security headers active",
              response.headers.get("x-content-type-options") == "nosniff"
              and response.headers.get("x-frame-options") == "DENY")
        page.screenshot(path=str(output.parent / "desktop-home.png"))
        check("No missing page resources", not report["failed_responses"], report["failed_responses"])
        check("No browser errors", not report["errors"], report["errors"])
        context.close()
        browser.close()
except Exception as error:
    # Secrets are not included in exception text from our API wrapper.
    report["fatal_error"] = str(error).replace(secret, "[redacted]") if secret else str(error)
finally:
    if secret:
        try:
            api(f"/v1/projects/{args.project}/protection-bypass",
                {"revoke": {"secret": secret, "regenerate": False}})
            after = api(f"/v9/projects/{args.project}")
            report["temporary_qa_credential_revoked"] = secret not in (after.get("protectionBypass") or {})
            check("Deployment protection retained", after.get("ssoProtection") == protection_before)
        except Exception as error:
            report["cleanup_error"] = str(error).replace(secret, "[redacted]")
        check("Temporary QA credential revoked", report["temporary_qa_credential_revoked"])
    report["passed"] = (
        not report.get("fatal_error")
        and bool(report["checks"])
        and all(item["passed"] for item in report["checks"])
    )
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({
        "passed": report["passed"], "checks": len(report["checks"]),
        "failures": [item for item in report["checks"] if not item["passed"]],
        "fatal_error": report.get("fatal_error"),
        "temporary_qa_credential_revoked": report["temporary_qa_credential_revoked"],
    }))
raise SystemExit(0 if report["passed"] else 1)
