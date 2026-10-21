"""Check rendered gutters, overflow and alignment. Never submit forms or send messages."""
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ["/", "/hotel", "/rooms", "/rooms/compare", "/rooms/deluxe-room",
          "/rooms/deluxe-twin-room", "/rooms/family-room", "/dining", "/varanasi",
          "/gallery", "/guides", "/guides/first-visit-to-kashi",
          "/guides/arriving-in-godowlia", "/guides/choosing-your-room",
          "/group-stays", "/contact", "/privacy"]
TOLERANCE = 2
RUNTIME_PATTERN = re.compile(r"maximum (?:update depth|call stack)|too much recursion|"
                             r"uncaught|unhandled|hydration|Minified React error", re.I)
GEOMETRY = r"""()=>{
 const box=e=>{const r=e.getBoundingClientRect();return {left:r.left,right:r.right,
   top:r.top,bottom:r.bottom,width:r.width,height:r.height}};
 const label=e=>e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+
   (typeof e.className==='string'?'.'+e.className.trim().split(/\s+/).join('.'):'');
 const visible=e=>{if(e.closest('[hidden],[inert],[aria-hidden="true"]'))return false;
   const r=e.getBoundingClientRect();if(!r.width||!r.height)return false;
   for(let p=e;p;p=p.parentElement){const s=getComputedStyle(p);
     if(s.display==='none'||s.visibility==='hidden'||Number(s.opacity)===0)return false;}return true;};
 const content=e=>{const b=box(e),s=getComputedStyle(e);return {...b,
   left:b.left+parseFloat(s.paddingLeft)+parseFloat(s.borderLeftWidth),
   right:b.right-parseFloat(s.paddingRight)-parseFloat(s.borderRightWidth)}};
 const shells=[...document.querySelectorAll('main .container,main .rooms-container,main .hospitality-shell,.site-footer .container')]
   .filter(e=>visible(e)&&!e.parentElement.closest('.container,.rooms-container,.hospitality-shell'));
 const canonical=document.querySelector('.site-footer .container')||shells[0];
 const gutters=shells.map(e=>({element:label(e),box:content(e),intentional_layout:
   e.matches('.hero-media-footer.container')?'Controls follow the inset hero photograph':
   e.matches('.room-compare-heading.rooms-container')?'Comparison title uses a centered 920px reading measure':null}));
 const outside=[],suspicious=[];
 for(const e of document.querySelectorAll('main h1,main h2,main h3,main p,main a,main button,main input,main select,main label,main figcaption,main img')){
   if(!visible(e))continue;const r=box(e),shell=e.closest('.container,.rooms-container,.hospitality-shell');
   const c=shell?content(shell):{left:0,right:document.documentElement.clientWidth};
   if(r.left>=c.left-2&&r.right<=c.right+2)continue;
   let clipped=false;for(let p=e.parentElement;p&&p!==shell;p=p.parentElement){
     const s=getComputedStyle(p);if(/hidden|clip|scroll|auto/.test(s.overflowX)||s.clipPath!=='none')clipped=true;}
   if(clipped)continue; // Deliberately cropped photography and swipe tracks.
   const finding={element:label(e),text:(e.textContent||e.getAttribute('alt')||'').trim().slice(0,100),box:r,container:c};
   if(r.left < -2||r.right>document.documentElement.clientWidth+2)outside.push(finding);
   else suspicious.push(finding);
 }
 const fields=[];
 const controls=[...document.querySelectorAll('form input:not([type="hidden"]):not([type="checkbox"]),form select')].filter(visible);
 for(let i=0;i<controls.length;i++)for(let j=i+1;j<controls.length;j++){
   const a=controls[i],b=controls[j],selector='.field,.form-field,.group-field,.dining-field,.stay-field,.dock-date,.dock-guests';
   const wa=a.closest(selector)||a.parentElement,wb=b.closest(selector)||b.parentElement;
   if(wa===wb||wa.parentElement!==wb.parentElement)continue;
   const ra=box(a),rb=box(b),pa=box(wa),pb=box(wb);
   if(Math.abs(pa.top-pb.top)>2||!(ra.right<=rb.left+2||rb.right<=ra.left+2))continue;
   // A field can contain stacked controls (adult/child guest selects). Compare
   // the matching internal row, not its second select against a sibling's first.
   const internalRow=(control,wrapper)=>[...wrapper.querySelectorAll('input:not([type="hidden"]):not([type="checkbox"]),select')]
     .filter(p=>p!==control&&visible(p)&&box(p).bottom<=box(control).top+2).length;
   if(internalRow(a,wa)!==internalRow(b,wb))continue;
   fields.push({first:label(a),second:label(b),firstBox:ra,secondBox:rb,
     comparableHeight:Math.abs(ra.height-rb.height)<=2,
     aligned:Math.abs(ra.top-rb.top)<=2&&Math.abs(ra.bottom-rb.bottom)<=2});
 }
 return {viewport:document.documentElement.clientWidth,body:document.body.scrollWidth,
   document:document.documentElement.scrollWidth,canonical:canonical?content(canonical):null,
   gutters,outside:outside.slice(0,40),suspicious:suspicious.slice(0,40),fields};
}"""


class Audit:
    def __init__(self, args):
        self.args = args
        self.output = ROOT / args.output
        self.output.parent.mkdir(parents=True, exist_ok=True)
        self.scope = {}
        self.report = {"date": datetime.now(timezone.utc).isoformat(),
                       "base_url": args.base_url, "engines": args.engines,
                       "widths": args.widths, "routes": ROUTES, "checks": [],
                       "suspicious": [], "runtime_errors": [], "console_errors": [],
                       "screenshots": [], "external_messages_sent": 0,
                       "limitations": ["WebKit is engine emulation, not physical iPhone testing.",
                                        "Suspicious findings require visual review and do not fail the audit."]}

    def check(self, name, passed, detail=None):
        self.report["checks"].append({**self.scope, "name": name, "passed": bool(passed), "detail": detail})
        print(f"{'PASS' if passed else 'FAIL'} {self.scope} {name}", flush=True)

    def suspicious(self, name, detail):
        self.report["suspicious"].append({**self.scope, "name": name, "detail": detail})

    def save(self):
        checks = self.report["checks"]
        self.report["summary"] = {"passed": sum(c["passed"] for c in checks),
                                  "failed": sum(not c["passed"] for c in checks),
                                  "suspicious": len(self.report["suspicious"]),
                                  "runtime_errors": len(self.report["runtime_errors"])}
        self.output.write_text(json.dumps(self.report, indent=2), encoding="utf-8")

    def watch(self, page):
        page.set_default_timeout(15000)
        page.set_default_navigation_timeout(60000)
        page.on("pageerror", lambda error: self.report["runtime_errors"].append({
            **self.scope, "url": page.url, "name": error.name, "message": str(error),
            "stack": error.stack, "time": datetime.now(timezone.utc).isoformat()}))

        def console(message):
            if message.type == "error":
                entry = {**self.scope, "url": page.url, "message": message.text,
                         "location": message.location}
                self.report["console_errors"].append(entry)
                if RUNTIME_PATTERN.search(message.text):
                    self.report["runtime_errors"].append({**entry, "name": "ConsoleRuntimeError", "stack": None})
        page.on("console", console)

    def position(self, page, selector, fraction=.2):
        page.locator(selector).first.evaluate("""(e,f)=>scrollTo({top:Math.max(0,
          e.getBoundingClientRect().top+scrollY-innerHeight*f),behavior:'instant'})""", fraction)
        page.wait_for_timeout(200)

    def shot(self, page, name, selector=None, full_page=False):
        slug = "home" if self.scope["route"] == "/" else self.scope["route"].strip("/").replace("/", "-")
        path = self.output.parent / f"alignment-{self.scope['engine']}-{self.scope['width']}-{slug}-{name}.png"
        try:
            if selector:
                page.locator(selector).first.screenshot(path=str(path), animations="allow", timeout=20000)
            else:
                page.screenshot(path=str(path), full_page=full_page, animations="allow", timeout=20000)
            self.report["screenshots"].append({**self.scope, "name": name, "path": str(path)})
        except Exception as error:
            self.check(f"Capture {name}", False, str(error))

    def route_checks(self, page):
        samples = []
        height = page.evaluate("document.documentElement.scrollHeight")
        step = page.viewport_size["height"] * .8
        for y in range(0, int(height + step), int(step)):
            page.evaluate("y=>scrollTo({top:y,behavior:'instant'})", y)
            page.wait_for_timeout(100)
            samples.append(page.evaluate("({y:scrollY,body:document.body.scrollWidth,document:document.documentElement.scrollWidth,viewport:document.documentElement.clientWidth})"))
        page.wait_for_timeout(1000)
        state = page.evaluate(GEOMETRY)
        samples.append({key: state[key] for key in ["body", "document", "viewport"]})
        self.check("Body and document stay within viewport through full-page scroll",
                   all(s["body"] <= s["viewport"] + 1 and s["document"] <= s["viewport"] + 1 for s in samples), samples)
        self.check("Visible unclipped content stays within viewport", not state["outside"], state["outside"])
        reference = state["canonical"]
        self.check("Shared container reference exists", reference is not None)
        if reference:
            bad = [s for s in state["gutters"] if not s.get("intentional_layout") and not edges_match(s["box"], reference)]
            self.check("Container and hospitality-shell content gutters agree", not bad,
                       {"reference": reference, "mismatches": bad, "measured": state["gutters"]})
        for finding in state["suspicious"]:
            self.suspicious("Content extends beyond its nearest shared gutter", finding)
        comparable = [f for f in state["fields"] if f["comparableHeight"]]
        self.check("Comparable form fields in the same row share top and bottom baselines",
                   all(f["aligned"] for f in comparable), comparable)
        for field in state["fields"]:
            if not field["comparableHeight"]:
                self.suspicious("Same-row form fields have different control heights", field)
        page.evaluate("scrollTo({top:document.documentElement.scrollHeight,behavior:'instant'})")
        page.wait_for_timeout(150)
        footer = page.locator(".site-footer").bounding_box()
        dock = page.locator(".booking-dock").bounding_box()
        self.check("Footer clears fixed booking dock at document end",
                   bool(footer and dock and footer["y"] + footer["height"] <= dock["y"] + TOLERANCE),
                   {"footer": footer, "dock": dock})

    def homepage(self, page):
        for index in range(page.locator(".scroll-photo-window").count()):
            photo = page.locator(".scroll-photo-window").nth(index)
            samples = []
            for fraction in [.9, .55, .15]:
                photo.evaluate("(e,f)=>scrollTo({top:e.getBoundingClientRect().top+scrollY-innerHeight*f,behavior:'instant'})", fraction)
                page.wait_for_timeout(250)
                sample = photo.evaluate("e=>({clip:getComputedStyle(e).clipPath,width:e.getBoundingClientRect().width,scrollY})")
                sample["side_insets_px"] = side_insets(sample["clip"], sample["width"])
                samples.append(sample)
            known = [s for s in samples if s["side_insets_px"] is not None]
            self.check(f"ScrollPhoto {index + 1} retains its visible side edges at every sampled scroll position",
                       len(known) == len(samples) and all(max(s["side_insets_px"]) <= .5 for s in known), samples)
        self.position(page, ".home-amenities", .45)
        amenities = page.evaluate("""()=>{const b=e=>{const r=e.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom}};
          return {image:b(document.querySelector('.welcome-photo-main')),
            items:[...document.querySelectorAll('.home-amenities > span')].map(e=>{const icon=b(e.querySelector('svg'));
              const text=[...e.childNodes].filter(n=>n.nodeType===Node.TEXT_NODE&&n.textContent.trim()).map(n=>{
                const r=document.createRange();r.selectNodeContents(n);return b(r)});
              return {box:b(e),icon,content:{left:Math.min(icon.left,...text.map(t=>t.left)),
                right:Math.max(icon.right,...text.map(t=>t.right))}}})}}""")
        self.check("Amenity strip contains all six essentials", len(amenities["items"]) == 6, amenities)
        if self.scope["width"] > 900 and amenities["items"]:
            items = amenities["items"]
            self.check("First and last amenity content edges align with lounge photograph",
                       abs(items[0]["box"]["left"] - amenities["image"]["left"]) <= TOLERANCE
                       and abs(items[-1]["box"]["right"] - amenities["image"]["right"]) <= TOLERANCE, amenities)
            self.check("All desktop amenity icons share a baseline",
                       max(i["icon"]["bottom"] for i in items) - min(i["icon"]["bottom"] for i in items) <= TOLERANCE, items)
            if not edges_match({"left": items[0]["content"]["left"], "right": items[-1]["content"]["right"]}, amenities["image"]):
                self.suspicious("Amenity cell edges align but visible icon/text endpoints leave an inset", amenities)
        else:
            rows = {}
            for item in amenities["items"]:
                key = next((k for k in rows if abs(k - item["box"]["top"]) <= TOLERANCE), item["box"]["top"])
                rows.setdefault(key, []).append(item["icon"]["bottom"])
            self.check("Amenity icons align within each mobile/tablet row",
                       all(max(row) - min(row) <= TOLERANCE for row in rows.values()), rows)
        self.itinerary(page)
        if self.scope["width"] in [390, 1024, 1440]:
            for name, selector in [("welcome", ".home-welcome"), ("itinerary", ".city-itinerary"), ("stage", ".itinerary-stage")]:
                self.position(page, selector)
                page.wait_for_timeout(900)
                self.shot(page, name, selector)

    def itinerary(self, page):
        self.position(page, ".itinerary-tabs", .2)
        tabs = page.locator(".itinerary-tabs [role=tab]")
        self.check("Four manual itinerary tabs exist", tabs.count() == 4)
        columns = []
        for index in range(tabs.count()):
            tabs.nth(index).click()
            page.wait_for_timeout(650)
            state = page.evaluate("""()=>{const b=s=>{const e=document.querySelector(s),r=e.getBoundingClientRect();
              return {left:r.left,right:r.right,top:r.top,bottom:r.bottom}};
              return {heading:b('.itinerary-heading'),intro:b('.itinerary-heading > p'),tabs:b('.itinerary-tabs'),
                stage:b('.itinerary-stage'),image:b('.itinerary-image'),panel:b('.itinerary-panel'),
                lead:b('.itinerary-copy[aria-hidden=false] .itinerary-copy-lead'),
                detail:b('.itinerary-copy[aria-hidden=false] .itinerary-copy-detail')}}""")
            columns.append(state)
            self.check(f"Itinerary tab {index + 1}: heading, panel and stage share photograph edges",
                       all(edges_match(state[key], state["image"]) for key in ["heading", "panel", "stage"]), state)
            self.check(f"Itinerary tab {index + 1}: tablist starts at photograph gutter and stays inside it",
                       abs(state["tabs"]["left"] - state["image"]["left"]) <= TOLERANCE
                       and state["tabs"]["right"] <= state["image"]["right"] + TOLERANCE, state)
            if self.scope["width"] > 760:
                self.check(f"Itinerary tab {index + 1}: intro and body share a column start",
                           abs(state["intro"]["left"] - state["detail"]["left"]) <= TOLERANCE, state)
        self.check("All itinerary tabs preserve text-column positions",
                   all(edges_match(s["lead"], columns[0]["lead"]) and edges_match(s["detail"], columns[0]["detail"])
                       for s in columns), columns)
        tabs.first.click()
        page.wait_for_timeout(1200)


def edges_match(first, second):
    return all(abs(first[side] - second[side]) <= TOLERANCE for side in ["left", "right"])


def side_insets(clip, width):
    if clip == "none":
        return [0, 0]
    if not clip.startswith("inset("):
        return None
    tokens = re.findall(r"(-?[\d.]+)(%|px)?", clip.split("round")[0])
    if not 1 <= len(tokens) <= 4:
        return None
    values = [float(value) * width / 100 if unit == "%" else float(value) for value, unit in tokens]
    if len(values) == 1:
        return [values[0], values[0]]
    return [values[1], values[3] if len(values) == 4 else values[1]]


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:3082")
    parser.add_argument("--output", default="evidence/alignment/alignment-qa.json")
    parser.add_argument("--engines", nargs="+", default=["chromium"], help="chromium webkit; comma-separated also accepted")
    parser.add_argument("--widths", nargs="+", default=["390", "768", "1024", "1440"])
    parser.add_argument("--screenshots", action="store_true", help="Also capture every full page at 390/1440px; key homepage captures are always saved")
    args = parser.parse_args()
    args.base_url = args.base_url.rstrip("/")
    args.engines = list(dict.fromkeys(e for value in args.engines for e in value.split(",")))
    try:
        args.widths = list(dict.fromkeys(int(w) for value in args.widths for w in value.split(",")))
    except ValueError:
        parser.error("--widths must contain integer viewport widths")
    if not args.widths or any(w < 280 or w > 3840 for w in args.widths):
        parser.error("--widths must be between 280 and 3840")
    if any(e not in ["chromium", "webkit"] for e in args.engines):
        parser.error("--engines supports chromium and webkit")
    if "webkit" in args.engines and urlsplit(args.base_url).scheme != "https":
        parser.error("WebKit requires an HTTPS base URL because this site's CSP upgrades insecure requests")
    return args


def main():
    audit = Audit(parse_args())
    try:
        with sync_playwright() as playwright:
            for engine in audit.args.engines:
                browser = getattr(playwright, engine).launch(headless=True, **({"channel": "msedge"} if engine == "chromium" else {}))
                try:
                    for width in audit.args.widths:
                        context = browser.new_context(viewport={"width": width, "height": 844 if width <= 760 else 1000},
                                                      device_scale_factor=1, reduced_motion="no-preference")
                        try:
                            page = context.new_page()
                            audit.watch(page)
                            for route in ROUTES:
                                audit.scope = {"engine": engine, "width": width, "route": route}
                                try:
                                    response = page.goto(audit.args.base_url + route, wait_until="networkidle")
                                    audit.check("Route responds successfully", bool(response and response.ok))
                                    page.locator("main").wait_for()
                                    page.evaluate("document.fonts.ready")
                                    audit.route_checks(page)
                                    if route == "/":
                                        audit.homepage(page)
                                    if audit.args.screenshots and width in [390, 1440]:
                                        page.evaluate("scrollTo({top:0,behavior:'instant'})")
                                        page.wait_for_timeout(500)
                                        audit.shot(page, "full-page", full_page=True)
                                except Exception as error:
                                    audit.check("Route audit completes", False, {"name": type(error).__name__, "message": str(error)})
                                finally:
                                    audit.save()
                        finally:
                            context.close()
                finally:
                    browser.close()
    except Exception as error:
        audit.check("Browser audit completes", False, {"name": type(error).__name__, "message": str(error)})
    finally:
        audit.check("No JavaScript runtime errors", not audit.report["runtime_errors"], audit.report["runtime_errors"])
        audit.save()
    return 1 if audit.report["summary"]["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
