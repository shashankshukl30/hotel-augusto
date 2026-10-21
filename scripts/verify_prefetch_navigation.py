"""Trace WebKit navigation/prefetch failures with narrow versus broad routing; no form submissions."""
import argparse
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from playwright.sync_api import sync_playwright

from verify_client_contacts import ROOT

FORM_SUBMIT = re.compile(r"https?://(?:[^/]+\.)?formsubmit\.co(?:/|$)")
EXPECTED = {"/rooms": "find your room", "/hotel": "welcome to hotel augusto",
            "/guides": "before you arrive", "/contact": "let’s plan your stay", "/privacy": "privacy. in plain language"}
RAPID_ROUTES = ["/varanasi", "/gallery", "/guides", "/guides/first-visit-to-kashi",
                "/guides/arriving-in-godowlia", "/group-stays", "/contact", "/privacy"]


def headers(values):
    return {key: "[redacted]" if key.lower() in {"authorization", "cookie", "set-cookie", "proxy-authorization"} else value
            for key, value in values.items()}


def safe(action):
    try:
        return action()
    except Exception as error:
        return {"unavailable": str(error)}


class Trace:
    def __init__(self, args):
        self.args = args
        self.output = ROOT / args.output
        self.output.parent.mkdir(parents=True, exist_ok=True)
        self.report = {"recorded_at_utc": datetime.now(timezone.utc).isoformat(), "base": args.base,
                       "browser": args.browser, "cases": [], "checks": [], "external_emails_sent": 0,
                       "limitations": ["HTTP replays supplement actual browser request traces; they do not independently prove browser CORS behavior."]}
        self.case = None
        self.started = time.monotonic()

    def stamp(self):
        return {"ms": round((time.monotonic() - self.started) * 1000, 1), "utc": datetime.now(timezone.utc).isoformat()}

    def check(self, name, passed, detail=None):
        self.report["checks"].append({"mode": self.case["mode"], "scenario": self.case["scenario"],
                                      "name": name, "passed": bool(passed), "detail": detail})
        print(f"{'PASS' if passed else 'FAIL'} {self.case['mode']}/{self.case['scenario']} {name}", flush=True)

    def save(self):
        self.report["summary"] = {"passed": sum(x["passed"] for x in self.report["checks"]),
                                  "failed": sum(not x["passed"] for x in self.report["checks"]),
                                  "page_errors": sum(len(c["page_errors"]) for c in self.report["cases"])}
        self.output.write_text(json.dumps(self.report, indent=2), encoding="utf-8")

    def run(self, browser, mode, scenario):
        self.case = {"mode": mode, "scenario": scenario, "requests": [], "navigations": [], "page_errors": [],
                     "console": [], "route_events": [], "lifecycle": [], "blocked": [], "replays": [], "correlations": [], "fetch_events": []}
        case = self.case
        self.report["cases"].append(case)
        context = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True,
                                      timezone_id="Asia/Kolkata", reduced_motion="no-preference", service_workers="block")
        page = context.new_page()
        page.set_default_timeout(15000)
        page.set_default_navigation_timeout(60000)
        page.add_init_script("""(()=>{const nativeFetch=window.fetch,token=location.pathname+'@'+performance.timeOrigin;
          let unloading=false;
          const log=(event,detail={})=>console.debug('__PREFETCH_TRACE__'+JSON.stringify({event,document_token:token,
            document_url:location.href,wall_ms:Date.now(),performance_ms:performance.now(),unloading,
            visibility:document.visibilityState,...detail}));
          addEventListener('beforeunload',()=>{unloading=true;log('beforeunload')});
          addEventListener('pagehide',event=>{unloading=true;log('pagehide',{persisted:event.persisted})});
          window.fetch=function(input,options){const raw=typeof input==='string'?input:input.url||String(input);
            if(!raw?.includes('_rsc='))return nativeFetch.apply(this,arguments);
            const url=new URL(raw,location.href).href,signal=options?.signal||input?.signal;
            log('fetch-start',{url,signal_aborted:signal?.aborted||false});
            return nativeFetch.apply(this,arguments).then(response=>{log('fetch-response',{url,status:response.status});return response},
              error=>{log('fetch-reject',{url,name:error.name,message:error.message,signal_aborted:signal?.aborted||false});throw error});
          };})();""")
        records = {}

        def request_record(request):
            key = request
            if key not in records:
                row = {"id": len(case["requests"]) + 1, "start": self.stamp(), "url": request.url,
                       "method": request.method, "resource_type": request.resource_type,
                       "navigation": request.is_navigation_request(), "page_url_at_start": safe(lambda: page.url),
                       "frame_url": safe(lambda: request.frame.url), "headers": headers(request.headers),
                       "redirected_from": request.redirected_from.url if request.redirected_from else None}
                records[key] = row
                case["requests"].append(row)
            return records[key]

        def response_event(response):
            row = request_record(response.request)
            row["response"] = {**self.stamp(), "url": response.url, "status": response.status,
                               "status_text": response.status_text, "headers": headers(response.headers),
                               "from_service_worker": response.from_service_worker}

        def finished(request):
            request_record(request)["finished"] = {**self.stamp(), "timing": safe(lambda: request.timing)}

        def failed(request):
            request_record(request)["failed"] = {**self.stamp(), "failure": request.failure,
                                                 "timing": safe(lambda: request.timing), "page_url": safe(lambda: page.url)}

        def route_request(route):
            request, parsed = route.request, urlsplit(route.request.url)
            record = request_record(request)
            host = (parsed.hostname or "").lower()
            case["route_events"].append({**self.stamp(), "request_id": record["id"], "url": request.url, "event": "intercept"})
            if host == "formsubmit.co" or host.endswith(".formsubmit.co"):
                case["blocked"].append({"url": request.url, "method": request.method, "reason": "no-email-safety"})
                route.abort()
                return
            if host in {"wa.me", "api.whatsapp.com", "web.whatsapp.com"} or (
                request.method in {"POST", "PUT", "PATCH", "DELETE"} and parsed.netloc != urlsplit(self.args.base).netloc):
                case["blocked"].append({"url": request.url, "method": request.method, "reason": "broad-audit-safety"})
                route.abort()
                return
            try:
                route.continue_()
                case["route_events"].append({**self.stamp(), "request_id": record["id"], "event": "continue-returned"})
            except Exception as error:
                case["route_events"].append({**self.stamp(), "request_id": record["id"], "event": "continue-error", "error": str(error)})

        context.route("**/*" if mode == "broad" else FORM_SUBMIT, route_request)
        page.on("request", request_record)
        page.on("response", response_event)
        page.on("requestfinished", finished)
        page.on("requestfailed", failed)
        page.on("pageerror", lambda error: case["page_errors"].append({**self.stamp(), "url": safe(lambda: page.url),
                     "name": error.name, "message": str(error), "stack": error.stack}))
        def console_event(message):
            if message.text.startswith("__PREFETCH_TRACE__"):
                case["fetch_events"].append({**self.stamp(), **json.loads(message.text[len("__PREFETCH_TRACE__"):])})
            elif message.type in {"error", "warning"}:
                case["console"].append({**self.stamp(), "type": message.type, "text": message.text, "location": message.location})
        page.on("console", console_event)
        page.on("framenavigated", lambda frame: case["lifecycle"].append({**self.stamp(), "event": "framenavigated",
                                 "url": frame.url, "main_frame": frame == page.main_frame}))
        page.on("domcontentloaded", lambda: case["lifecycle"].append({**self.stamp(), "event": "domcontentloaded", "url": page.url}))
        page.on("load", lambda: case["lifecycle"].append({**self.stamp(), "event": "load", "url": page.url}))
        try:
            if scenario == "stable-ui-clicks":
                self.navigate(page, "/", "goto")
                page.wait_for_timeout(2500)
                for target in EXPECTED:
                    self.navigate(page, target, "click")
                    page.wait_for_timeout(2500)
                    h1 = " ".join(page.locator("main h1").inner_text().lower().split())
                    self.check(f"Real UI navigation reaches {target}", urlsplit(page.url).path == target and EXPECTED[target] in h1, {"url": page.url, "h1": h1})
            else:
                for target in RAPID_ROUTES:
                    self.navigate(page, target, "goto")
                    # Match the original full contact-suite sweep's rendered waits.
                    for fraction in [0, .25, .5, .75, 1]:
                        page.evaluate("f=>scrollTo({top:(document.documentElement.scrollHeight-innerHeight)*f,behavior:'instant'})", fraction)
                        page.wait_for_timeout(160)
                    self.check(f"Rapid document navigation reaches {target}", urlsplit(page.url).path == target and page.locator("main").is_visible(), page.url)
            case["lifecycle"].append({**self.stamp(), "event": "settle-start", "url": page.url})
            page.wait_for_timeout(4000)
            case["lifecycle"].append({**self.stamp(), "event": "settle-end", "url": page.url})
            page.screenshot(path=str(self.output.parent / f"prefetch-{mode}-{scenario}-{self.args.browser}.png"))
            self.replay_failures(context)
        except Exception as error:
            self.check("Scenario completes", False, {"type": type(error).__name__, "message": str(error)})
        finally:
            case["lifecycle"].append({**self.stamp(), "event": "context-close-start", "url": safe(lambda: page.url)})
            context.close()
            case["lifecycle"].append({**self.stamp(), "event": "context-close-finished"})
            self.correlate()
            self.save()
            print(f"TRACE {mode}/{scenario}: {len(case['page_errors'])} page errors; "
                  f"{sum('failed' in r for r in case['requests'])} failed requests", flush=True)

    def navigate(self, page, target, kind):
        action = {"target": target, "kind": kind, "start": self.stamp(), "from_url": page.url}
        self.case["navigations"].append(action)
        if kind == "goto":
            response = page.goto(self.args.base + target, wait_until="domcontentloaded")
            action["document_status"] = response.status if response else None
            self.check(f"Document {target} returns 200", response is not None and response.status == 200, action["document_status"])
        elif target == "/privacy":
            link = page.locator('.site-footer a[href="/privacy"]')
            link.evaluate("e=>scrollTo({top:e.getBoundingClientRect().top+scrollY-innerHeight*.25,behavior:'instant'})")
            link.click()
        else:
            page.evaluate("scrollTo({top:0,behavior:'instant'})")
            page.locator(".menu-trigger").click()
            page.locator(".navigation-dialog[open]").wait_for()
            link = page.locator(f'.navigation-dialog a[href="{target}"]').first
            link.scroll_into_view_if_needed()
            link.click()
        page.wait_for_url(lambda url: urlsplit(str(url)).path == target, wait_until="domcontentloaded")
        page.locator("main").wait_for()
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(900)
        action["completed"] = self.stamp()
        action["landed_url"] = page.url
        action["h1"] = safe(lambda: page.locator("main h1").inner_text())

    def replay_failures(self, context):
        selected = [r for r in self.case["requests"] if "_rsc=" in r["url"] and ("failed" in r or r.get("response", {}).get("status", 200) >= 400)]
        for request in selected[:8]:
            replay = {"original_request_id": request["id"], "url": request["url"], "start": self.stamp()}
            request_headers = {k: v for k, v in request["headers"].items() if k.lower() in {
                "rsc", "next-router-prefetch", "next-router-state-tree", "next-url", "next-router-segment-prefetch", "accept", "origin", "referer"}}
            replay["request_headers"] = request_headers
            try:
                response = context.request.get(request["url"], headers=request_headers, timeout=15000, max_redirects=0)
                replay.update({"status": response.status, "headers": headers(response.headers), "body_prefix": response.text()[:500], "finished": self.stamp()})
            except Exception as error:
                replay["error"] = str(error)
            self.case["replays"].append(replay)

    def correlate(self):
        case = self.case
        for error in case["page_errors"]:
            match = re.search(r"[?&]_rsc=([^\s\"'<>]+)", error["message"])
            token = match.group(1).rstrip(".,)") if match else None
            requests = [r for r in case["requests"] if token and parse_qs(urlsplit(r["url"]).query).get("_rsc") == [token]]
            evidence = []
            for request in requests:
                failure = request.get("failed", {})
                boundaries = [n for n in case["navigations"] if n["kind"] == "goto" and request["start"]["ms"] < n["start"]["ms"] <= error["ms"] + 100]
                classification = "unresolved-request-failure"
                if request.get("response", {}).get("status", 200) >= 400:
                    classification = "http-error-response"
                elif re.search(r"cancel|abort", failure.get("failure") or "", re.I) and boundaries:
                    classification = "explicit-request-cancellation-overlapping-document-navigation"
                elif boundaries:
                    classification = "request-overlaps-document-navigation-without-explicit-cancel-reason"
                evidence.append({"request_id": request["id"], "url": request["url"], "start": request["start"],
                                 "failure": failure, "response": request.get("response"), "document_navigations": boundaries,
                                 "classification": classification})
            case["correlations"].append({"error": error, "rsc_token": token, "exact_request_matches": evidence,
                                         "matched": bool(requests), "exact_fetch_events": [e for e in case["fetch_events"]
                                          if token and parse_qs(urlsplit(e.get("url", "")).query).get("_rsc") == [token]]})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="https://hotel-augusto-brown.vercel.app")
    parser.add_argument("--browser", choices=["webkit", "chromium"], default="webkit")
    parser.add_argument("--mode", choices=["both", "narrow", "broad"], default="both")
    parser.add_argument("--scenario", choices=["both", "stable-ui-clicks", "rapid-document-goto"], default="both")
    parser.add_argument("--output", default="evidence/client-handoff-20261021/prefetch-navigation-trace.json")
    args = parser.parse_args()
    args.base = args.base.rstrip("/")
    trace = Trace(args)
    with sync_playwright() as playwright:
        browser = getattr(playwright, args.browser).launch(headless=True, **({"channel": "msedge"} if args.browser == "chromium" else {}))
        try:
            for mode in ["narrow", "broad"] if args.mode == "both" else [args.mode]:
                for scenario in ["stable-ui-clicks", "rapid-document-goto"] if args.scenario == "both" else [args.scenario]:
                    trace.run(browser, mode, scenario)
        finally:
            browser.close()
    trace.save()
    return int(bool(trace.report["summary"]["failed"]))


if __name__ == "__main__":
    raise SystemExit(main())
