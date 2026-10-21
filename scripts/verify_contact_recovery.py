"""Mocked timeout and contact-query recovery checks; never sends an email."""
import argparse
import time
from urllib.parse import parse_qs, unquote, urlencode, urlsplit

from playwright.sync_api import sync_playwright

from verify_client_contacts import Audit, FORMS, RECIPIENT, ROOT


class RecoveryAudit(Audit):
    def __init__(self, args):
        super().__init__(args)
        self.output = ROOT / "evidence/client-handoff-20261021" / f"contact-recovery-{args.browser}.json"
        self.report["timeout_clock"] = "Real elapsed time; each held request exercises the application's 20000ms abort timer."

    def dates(self, page):
        return page.evaluate("()=>[30,32,40,43].map(n=>{const d=new Date();d.setDate(d.getDate()+n);return [d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-')})")

    def fill_contact(self, form, dates):
        values = {"name": "Digiocular verification", "email": "digiocular@gmail.com", "phone": "+91 9999991234",
                  "notes": "QA recovery check - intercepted locally, never delivered.",
                  "arrival": dates[0], "departure": dates[1], "adults": "2", "children": "2",
                  "room": "Family Room", "roomCount": "3"}
        for name, value in values.items():
            self.set_field(form, name, value)
        return values

    def timeout(self, page, pending, route, selector):
        self.goto(page, route)
        form, dates = page.locator(selector), self.dates(page)
        if route == "/dining":
            values = {"date": dates[0], "guests": "2", "name": "Digiocular verification",
                      "email": "digiocular@gmail.com", "phone": "+91 9999991234", "notes": "QA timeout check - no delivery."}
            for name, value in values.items():
                self.set_field(form, name, value)
        else:
            self.fill_contact(form, dates)
        expected, before = self.values(form), len(self.report["requests"])
        start = time.monotonic()
        self.submit(page, form)
        self.await_post(page, pending)
        self.check("Timeout test holds exactly one intercepted request", len(pending) == 1 and len(self.report["requests"]) == before + 1)
        error = form.locator(".enquiry-email-error")
        error.wait_for(timeout=26000)
        elapsed = time.monotonic() - start
        self.check("Twenty-second timeout produces recovery guidance", elapsed >= 19 and "in time" in error.inner_text()
                   and "Check with the hotel before retrying" in error.inner_text(), {"elapsed_seconds": round(elapsed, 2), "text": error.inner_text()})
        self.check("Timeout retains all fields and releases disabled state", self.values(form) == expected
                   and form.get_attribute("aria-busy") == "false" and form.locator('button[type="submit"]').first.is_enabled()
                   and form.locator('[name="email"]').is_enabled())
        self.check("Timeout offers exact hotel email fallback", error.locator(f'a[href="mailto:{RECIPIENT}"]').count() == 1)
        self.position(error)
        self.screenshot(page, f"recovery-{route.strip('/')}-timeout-{self.scope['width']}")
        self.overflow(page, "Timeout recovery")
        expired = pending.pop(0)
        try:
            expired.abort()
        except Exception:
            pass  # The application's AbortController may already have closed this mocked route.
        self.submit(page, form)
        self.await_post(page, pending)
        self.check("Explicit retry after timeout sends one unchanged enquiry", len(self.report["requests"]) == before + 2
                   and self.report["requests"][-1]["payload"] == self.report["requests"][-2]["payload"])
        self.respond(pending)
        form.locator(".enquiry-email-accepted").wait_for()
        self.check("Timeout retry reaches accepted state without clearing fields", self.values(form) == expected)

    def query_sync(self, page, pending):
        self.goto(page, "/contact")
        dates = self.dates(page)
        initial = {"arrival": dates[0], "departure": dates[1], "adults": "2", "children": "0",
                   "room": "deluxe-room", "roomCount": "1"}
        self.goto(page, "/contact?" + urlencode(initial))
        form = page.locator(".booking-form")
        entered = self.fill_contact(form, dates)
        form.evaluate("e=>{window.__contactRecoveryForm=e}")
        # Create a stale prepared WhatsApp draft before changing only dock travel fields.
        alternative = form.locator('button[value="whatsapp"]')
        self.position(alternative)
        alternative.click()
        form.locator(".booking-draft").wait_for()
        before = len(self.report["requests"])
        dock = page.locator(".booking-dock-inner")
        for name, value in {"arrival": dates[2], "departure": dates[3], "adults": "4"}.items():
            self.set_field(dock, name, value)
        dock.locator('button[type="submit"]').click()
        page.wait_for_function("expected=>{const f=document.querySelector('.booking-form');return f?.elements.arrival.value===expected[0]&&f?.elements.departure.value===expected[1]&&f?.elements.adults.value==='4'}", arg=dates[2:])
        actual = self.values(form)
        self.check("Dock query navigation preserves the mounted contact form", form.evaluate("e=>e===window.__contactRecoveryForm"))
        self.check("Dock updates dates and adults", all(actual[k] == v for k, v in {"arrival": dates[2], "departure": dates[3], "adults": "4"}.items()), actual)
        retained = ["name", "email", "phone", "notes", "room", "roomCount", "children"]
        self.check("Dock preserves private fields and newer room preferences", all(actual[k] == entered[k] for k in retained), {k: actual[k] for k in retained})
        query = parse_qs(urlsplit(page.url).query)
        self.check("Only travel preferences enter the URL", set(query) == {"arrival", "departure", "adults", "children", "room", "roomCount"}
                   and query.get("room") == ["family-room"] and query.get("roomCount") == ["3"] and query.get("children") == ["2"], page.url)
        self.check("No private field value leaks into query", all(entered[k] not in unquote(page.url) for k in ["name", "email", "phone", "notes"]))
        self.check("Dock clears stale WhatsApp and email feedback without sending", form.locator(".booking-draft,.enquiry-email-feedback").count() == 0
                   and len(self.report["requests"]) == before and not pending)
        # An accepted email status must also be invalidated by a later dock change.
        self.submit(page, form)
        self.await_post(page, pending)
        self.respond(pending)
        form.locator(".enquiry-email-accepted").wait_for()
        self.set_field(dock, "adults", "5")
        dock.locator('button[type="submit"]').click()
        page.wait_for_function("()=>document.querySelector('.booking-form')?.elements.adults.value==='5'")
        page.wait_for_function("()=>!document.querySelector('.booking-form .enquiry-email-feedback')")
        final_values = self.values(form)
        self.check("Dock invalidates accepted email status and preserves private fields", form.locator('button[type="submit"]').first.is_enabled()
                   and all(final_values[k] == entered[k] for k in retained) and form.evaluate("e=>e===window.__contactRecoveryForm"))
        self.check("Dock never sends another email automatically", len(self.report["requests"]) == before + 1 and not pending)
        self.overflow(page, "Dock query synchronization")
        self.position(form.locator('[name="email"]'))
        self.screenshot(page, f"recovery-query-sync-{self.scope['width']}")

    def pending_query_sync(self, page, pending):
        # Observe the real fetch signal without replacing its behavior or timer.
        page.add_init_script("""(()=>{const original=window.fetch;window.__contactRecoverySignals=[];
          window.fetch=function(input,options){const url=typeof input==='string'?input:input.url;
            if(url?.startsWith('https://formsubmit.co/')&&options?.signal)
              window.__contactRecoverySignals.push(options.signal);
            return original.apply(this,arguments)};})();""")
        self.goto(page, "/contact")
        form, dates = page.locator(".booking-form"), self.dates(page)
        entered = self.fill_contact(form, dates)
        form.evaluate("e=>{window.__contactRecoveryForm=e}")
        before = len(self.report["requests"])
        self.submit(page, form)
        self.await_post(page, pending)
        self.check("Pending dock test starts with disabled preferences and one request",
                   form.get_attribute("aria-busy") == "true" and form.locator('[name="room"]').is_disabled()
                   and form.locator('[name="roomCount"]').is_disabled() and form.locator('[name="children"]').is_disabled()
                   and len(self.report["requests"]) == before + 1 and len(pending) == 1)
        dock = page.locator(".booking-dock-inner")
        changed = {"arrival": dates[2], "departure": dates[3], "adults": "4"}
        for name, value in changed.items():
            self.set_field(dock, name, value)
        dock.locator('button[type="submit"]').click()
        page.wait_for_function("expected=>{const f=document.querySelector('.booking-form');return f?.elements.arrival.value===expected[0]&&f?.elements.departure.value===expected[1]&&f?.elements.adults.value==='4'&&f?.getAttribute('aria-busy')==='false'}", arg=dates[2:])
        page.wait_for_function("()=>window.__contactRecoverySignals[0]?.aborted===true")
        actual = self.values(form)
        retained = ["name", "email", "phone", "notes", "room", "roomCount", "children"]
        self.check("Pending dock update preserves mounted form and all private/preferences values",
                   form.evaluate("e=>e===window.__contactRecoveryForm") and all(actual[k] == entered[k] for k in retained),
                   {k: actual[k] for k in retained})
        self.check("Pending dock update applies new dates and adults", all(actual[k] == v for k, v in changed.items()), actual)
        self.check("Original fetch is aborted and email state resets", page.evaluate("window.__contactRecoverySignals[0].aborted")
                   and form.locator(".enquiry-email-feedback").count() == 0
                   and form.locator('button[type="submit"]').first.is_enabled() and form.locator('[name="email"]').is_enabled())
        query = parse_qs(urlsplit(page.url).query)
        self.check("Pending dock URL preserves curated preferences only", set(query) == {"arrival", "departure", "adults", "children", "room", "roomCount"}
                   and query.get("room") == ["family-room"] and query.get("roomCount") == ["3"] and query.get("children") == ["2"], page.url)
        self.check("Pending dock change never submits a replacement email", len(self.report["requests"]) == before + 1 and len(pending) == 1)
        retired = pending.pop(0)
        try:
            retired.fulfill(status=200, content_type="application/json", headers={"Access-Control-Allow-Origin": "*"},
                            body='{"success":"true","message":"Late mocked response"}')
        except Exception:
            pass  # AbortController may already have closed the held intercepted route.
        page.wait_for_timeout(150)
        self.check("Late response cannot restore stale accepted status", form.locator(".enquiry-email-feedback").count() == 0)
        self.submit(page, form)
        self.await_post(page, pending)
        body = self.report["requests"][-1]["payload"]
        self.check("Explicit resubmission sends updated travel values and preserved preferences",
                   len(self.report["requests"]) == before + 2 and len(pending) == 1
                   and body.get("Arrival") == dates[2] and body.get("Departure") == dates[3] and body.get("Adults") == "4"
                   and body.get("Children") == "2" and body.get("Rooms requested") == "3" and body.get("Room preference") == "Family Room"
                   and body.get("email") == entered["email"] and body.get("phone") == entered["phone"]
                   and body.get("Name") == entered["name"] and body.get("Notes") == entered["notes"], body)
        self.respond(pending)
        form.locator(".enquiry-email-accepted").wait_for()
        self.check("Updated explicit enquiry reaches accepted state", form.locator('button[type="submit"]').first.is_disabled())
        self.overflow(page, "Pending dock query synchronization")
        self.position(form.locator(".enquiry-email-accepted"))
        self.screenshot(page, f"recovery-pending-query-sync-{self.scope['width']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="http://127.0.0.1:3080")
    parser.add_argument("--browser", choices=["chromium", "webkit"], default="chromium")
    parser.add_argument("--only-pending", action="store_true", help="Run pending-request dock regressions only; writes a separate report")
    args = parser.parse_args()
    args.base = args.base.rstrip("/")
    if args.browser == "webkit" and urlsplit(args.base).scheme != "https":
        parser.error("Use HTTPS for WebKit: the site CSP upgrades insecure requests.")
    audit = RecoveryAudit(args)
    if args.only_pending:
        audit.output = audit.output.with_name(f"contact-recovery-pending-{args.browser}.json")
    try:
        with sync_playwright() as playwright:
            browser = getattr(playwright, args.browser).launch(headless=True, **({"channel": "msedge"} if args.browser == "chromium" else {}))
            try:
                if not args.only_pending:
                    for route, selector, _ in FORMS:
                        audit.run_case(browser, 390, 844, lambda page, pending, r=route, s=selector: audit.timeout(page, pending, r, s))
                for width in [390, 1440]:
                    if not args.only_pending:
                        audit.run_case(browser, width, 844 if width == 390 else 1000, audit.query_sync)
                    audit.run_case(browser, width, 844 if width == 390 else 1000, audit.pending_query_sync)
            finally:
                browser.close()
    except Exception as error:
        audit.check("Recovery browser suite completes", False, str(error))
    audit.check("No runtime or recursion errors", not audit.report["runtime_errors"], audit.report["runtime_errors"])
    audit.check("No WhatsApp navigation attempted", not audit.report["blocked_whatsapp"], audit.report["blocked_whatsapp"])
    audit.check("No unexpected external write attempted", not audit.report["blocked_external_writes"], audit.report["blocked_external_writes"])
    audit.save()
    return int(bool(audit.report["summary"]["failed"]))


if __name__ == "__main__":
    raise SystemExit(main())
