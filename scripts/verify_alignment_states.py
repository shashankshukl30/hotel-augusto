"""Audit enquiry layout states without opening WhatsApp or sending messages."""
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
WIDTHS = [320, 390, 768, 1024, 1440]
FORMS = [("/contact", ".booking-form", ".booking-draft"),
         ("/group-stays", ".group-enquiry", ".group-draft"),
         ("/dining", ".dining-enquiry-form", ".dining-form-draft")]
WHATSAPP = re.compile(r"https?://(?:wa\.me|(?:api|web)\.whatsapp\.com)(?:/|$)")
RUNTIME = re.compile(r"maximum (?:update depth|call stack)|too much recursion|"
                     r"uncaught|unhandled|hydration|Minified React error", re.I)
CTA_GEOMETRY = r"""e=>{
 const box=r=>({left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height});
 const outer=box(e.getBoundingClientRect()),s=getComputedStyle(e),content={
   left:outer.left+parseFloat(s.borderLeftWidth)+parseFloat(s.paddingLeft),
   right:outer.right-parseFloat(s.borderRightWidth)-parseFloat(s.paddingRight),
   top:outer.top+parseFloat(s.borderTopWidth)+parseFloat(s.paddingTop),
   bottom:outer.bottom-parseFloat(s.borderBottomWidth)-parseFloat(s.paddingBottom)};
 const parts=[],walker=document.createTreeWalker(e,NodeFilter.SHOW_TEXT);let node;
 while(node=walker.nextNode())if(node.textContent.trim()){
   const range=document.createRange();range.selectNodeContents(node);
   for(const r of range.getClientRects())if(r.width&&r.height)parts.push({kind:'text',text:node.textContent.trim(),box:box(r)});}
 for(const svg of e.querySelectorAll('svg')){const r=svg.getBoundingClientRect();
   if(r.width&&r.height)parts.push({kind:'svg',box:box(r)});}
 const outside=parts.filter(p=>p.box.left<content.left-2||p.box.right>content.right+2||
   p.box.top<content.top-2||p.box.bottom>content.bottom+2);
 const clipped=[];
 for(let p=e;p;p=p.parentElement){const style=getComputedStyle(p),r=p.getBoundingClientRect();
   const x=/hidden|clip|auto|scroll/.test(style.overflowX),y=/hidden|clip|auto|scroll/.test(style.overflowY);
   const bounds={left:r.left+parseFloat(style.borderLeftWidth),right:r.right-parseFloat(style.borderRightWidth),
     top:r.top+parseFloat(style.borderTopWidth),bottom:r.bottom-parseFloat(style.borderBottomWidth)};
   for(const part of parts)if((x&&(part.box.left<bounds.left-2||part.box.right>bounds.right+2))||
     (y&&(part.box.top<bounds.top-2||part.box.bottom>bounds.bottom+2)))clipped.push({ancestor:p.className,part,bounds});
   if(style.clipPath!=='none')clipped.push({ancestor:p.className,clipPath:style.clipPath});
   if(p.tagName==='FORM')break;}
 return {outer,content,parts,outside,clipped,whiteSpace:s.whiteSpace,href:e.href};
}"""


class Audit:
    def __init__(self, args):
        self.args, self.scope = args, {}
        self.output = ROOT / args.output
        self.output.parent.mkdir(parents=True, exist_ok=True)
        self.report = {"date": datetime.now(timezone.utc).isoformat(), "base_url": args.base_url,
                       "engines": args.engines, "widths": WIDTHS,
                       "home_compact_widths": [601, 640, 768, 1024], "room_widths": [901, 1024, 1100],
                       "checks": [], "runtime_errors": [],
                       "console_errors": [], "screenshots": [], "blocked_external_requests": [],
                       "external_messages_sent": 0,
                       "limitations": ["WebKit engine coverage is not physical iPhone verification.",
                                        "Enquiry links are inspected only; WhatsApp is never opened."]}

    def check(self, name, passed, detail=None):
        self.report["checks"].append({**self.scope, "name": name, "passed": bool(passed), "detail": detail})
        print(f"{'PASS' if passed else 'FAIL'} {self.scope} {name}", flush=True)

    def save(self):
        self.report["summary"] = {"passed": sum(c["passed"] for c in self.report["checks"]),
                                  "failed": sum(not c["passed"] for c in self.report["checks"]),
                                  "runtime_errors": len(self.report["runtime_errors"])}
        self.output.write_text(json.dumps(self.report, indent=2), encoding="utf-8")

    def watch(self, context, page):
        def block(route):
            self.report["blocked_external_requests"].append({**self.scope, "url": route.request.url})
            route.abort()
        context.route(WHATSAPP, block)
        page.set_default_timeout(15000)
        page.set_default_navigation_timeout(60000)
        page.on("pageerror", lambda error: self.report["runtime_errors"].append({
            **self.scope, "url": page.url, "name": error.name, "message": str(error), "stack": error.stack}))

        def console(message):
            if message.type == "error":
                entry = {**self.scope, "url": page.url, "message": message.text, "location": message.location}
                self.report["console_errors"].append(entry)
                if RUNTIME.search(message.text):
                    self.report["runtime_errors"].append({**entry, "name": "ConsoleRuntimeError", "stack": None})
        page.on("console", console)

    def overflow(self, page, state):
        size = page.evaluate("({body:document.body.scrollWidth,document:document.documentElement.scrollWidth,viewport:document.documentElement.clientWidth})")
        self.check(f"{state}: body and document have no horizontal overflow",
                   size["body"] <= size["viewport"] + 1 and size["document"] <= size["viewport"] + 1, size)

    def position(self, locator):
        locator.evaluate("e=>scrollTo({top:Math.max(0,e.getBoundingClientRect().top+scrollY-innerHeight*.25),behavior:'instant'})")

    def screenshot(self, locator, name):
        slug = self.scope["route"].strip("/").replace("/", "-") or "home"
        path = self.output.parent / f"states-{self.scope['engine']}-{self.scope['width']}-{slug}-{name}.png"
        try:
            locator.screenshot(path=str(path), animations="allow", timeout=20000)
            self.report["screenshots"].append({**self.scope, "path": str(path)})
        except Exception as error:
            self.check(f"Screenshot {name}", False, str(error))

    def placeholders(self, page):
        dates = page.locator("input.date-input")
        measured = []
        page.evaluate("document.activeElement?.blur()")
        for index in range(dates.count()):
            field = dates.nth(index)
            if not field.is_visible() or field.input_value():
                continue
            self.position(field)
            page.wait_for_timeout(100)
            measured.append(field.evaluate("""e=>{const p=e.parentElement.querySelector('.date-field-placeholder'),r=e.getBoundingClientRect(),s=getComputedStyle(e);
              return {id:e.id,name:e.name,inputType:e.type,expectedLeft:r.left+parseFloat(s.borderLeftWidth)+parseFloat(s.paddingLeft),
                placeholderLeft:p?.getBoundingClientRect().left,visible:!!p&&getComputedStyle(p).visibility!=='hidden',
                padding:s.paddingLeft,border:s.borderLeftWidth}}"""))
        self.check("All empty visible date placeholders align with native input content left",
                   bool(measured) and all(m["visible"] and abs(m["placeholderLeft"] - m["expectedLeft"]) <= 2 for m in measured), measured)

    def submit(self, page, form):
        button = form.locator('button[type="submit"]')
        self.position(button)
        page.wait_for_timeout(100)
        button.click()
        page.wait_for_timeout(200)

    def set_field(self, form, name, value):
        field = form.locator(f'[name="{name}"]')
        if field.count() != 1:
            raise AssertionError(f"Expected exactly one {name} field, found {field.count()}")
        if field.evaluate("e=>e.tagName") == "SELECT":
            field.select_option(str(value))
        else:
            field.fill(str(value))
        field.evaluate("e=>e.blur()")

    def dining_columns(self, page):
        if self.scope["width"] <= 760:
            return
        columns = page.evaluate("""()=>['.hospitality-dining-introduction > :nth-child(2)',
          '.hospitality-dining-enquiries > .dining-enquiry-form','.hospitality-dining-questions > div'].map(selector=>{
            const e=document.querySelector(selector),r=e?.getBoundingClientRect();return {selector,left:r?.left,right:r?.right}})""")
        self.check("Dining intro, enquiry form and FAQ share desktop right-column edges",
                   all(c.get("left") is not None and c.get("right") is not None for c in columns)
                   and all(abs(c[edge] - columns[0][edge]) <= 2 for c in columns for edge in ["left", "right"]), columns)

    def enquiry(self, page, selector, draft_selector):
        form = page.locator(selector)
        form.wait_for()
        self.placeholders(page)
        self.position(form)
        page.wait_for_timeout(800)
        self.overflow(page, "Empty")
        self.check("Empty form has no prepared enquiry", form.locator(draft_selector).count() == 0)
        self.submit(page, form)
        self.check("Empty submission displays validation and no draft",
                   form.locator('[role="alert"]').count() > 0 and form.locator(draft_selector).count() == 0)
        self.overflow(page, "Missing required values")
        dates = page.evaluate("""()=>[30,32].map(offset=>{const d=new Date();d.setDate(d.getDate()+offset);
          return [d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-')})""")
        dining = self.scope["route"] == "/dining"
        if dining:
            self.set_field(form, "date", dates[0])
            self.set_field(form, "guests", 0)
        else:
            self.set_field(form, "arrival", dates[0])
            self.set_field(form, "departure", dates[0])
            for name, value in [("adults", 2), ("children", 0), ("roomCount", 2)]:
                self.set_field(form, name, value)
        self.submit(page, form)
        self.check("Invalid values display validation and prevent preparation",
                   form.locator('[role="alert"]').count() > 0 and form.locator(draft_selector).count() == 0)
        self.overflow(page, "Invalid values")
        self.set_field(form, "guests" if dining else "departure", 2 if dining else dates[1])
        self.submit(page, form)
        draft = form.locator(draft_selector)
        draft.wait_for(state="visible")
        cta = draft.locator('a[href^="https://wa.me/"]')
        self.check("Valid local future dates prepare one WhatsApp link", cta.count() == 1, {"dates": dates})
        self.position(cta)
        page.wait_for_timeout(200)
        geometry = cta.evaluate(CTA_GEOMETRY)
        parsed = urlsplit(geometry["href"])
        text = parse_qs(parsed.query).get("text", [""])[0]
        self.check("Prepared link targets wa.me with an enquiry, without navigation",
                   parsed.scheme == "https" and parsed.hostname == "wa.me" and bool(text)
                   and urlsplit(page.url).path.rstrip("/") == self.scope["route"], {"host": parsed.hostname, "message_length": len(text)})
        self.check("Prepared CTA text and SVGs remain inside its content padding",
                   bool(geometry["parts"]) and not geometry["outside"], geometry)
        self.check("Prepared CTA content is not clipped", not geometry["clipped"], geometry["clipped"])
        self.overflow(page, "Prepared enquiry")
        if dining:
            self.dining_columns(page)
        if self.scope["width"] == 320:
            self.screenshot(form, "prepared-form")
            self.screenshot(draft, "prepared-cta")

    def room(self, page):
        panel = page.locator(".room-stay-panel")
        panel.wait_for()
        self.placeholders(page)
        self.position(panel)
        page.wait_for_timeout(800)
        state = panel.evaluate("""e=>{const b=e=>{const r=e.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height}};
          const form=e.querySelector('.stay-bar-compact'),grid=e.querySelector('.stay-fields'),s=getComputedStyle(form),r=b(form);
          const controls=[...e.querySelectorAll('input:not([type="hidden"]),select')].map(c=>({name:c.name,...b(c)})),pairs=[];
          for(let i=0;i<controls.length;i++)for(let j=i+1;j<controls.length;j++){const a=controls[i],c=controls[j];
            if((a.right<=c.left+2||c.right<=a.left+2)&&Math.min(a.bottom,c.bottom)-Math.max(a.top,c.top)>Math.min(a.height,c.height)*.5)
              pairs.push({first:a,second:c,aligned:Math.abs(a.top-c.top)<=2&&Math.abs(a.bottom-c.bottom)<=2});}
          return {containerWidth:r.width-parseFloat(s.paddingLeft)-parseFloat(s.paddingRight)-parseFloat(s.borderLeftWidth)-parseFloat(s.borderRightWidth),
            grid:b(grid),fields:[...grid.querySelectorAll(':scope > .stay-field')].map(f=>({className:f.className,...b(f)})),pairs}}""")
        narrow = state["containerWidth"] <= 400.5
        self.check("Room fields fill narrow containers and retain readable columns when wider",
                   bool(state["fields"]) and (
                       all(abs(f[edge] - state["grid"][edge]) <= 2 for f in state["fields"] for edge in ["left", "right"])
                       if narrow else all(f["width"] >= 155 for f in state["fields"])), state)
        self.check("Shared-row room form controls have matching baselines",
                   all(pair["aligned"] for pair in state["pairs"]), state["pairs"])
        self.overflow(page, "Tablet room form")
        self.screenshot(panel, "tablet-room-form")

    def home_compact(self, page):
        form = page.locator(".home-reserve .stay-bar-compact")
        form.wait_for()
        self.placeholders(page)
        self.position(form)
        page.evaluate("document.activeElement?.blur()")
        page.wait_for_timeout(800)
        state = form.evaluate("""e=>{
          const b=e=>{const r=e.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height}};
          const r=b(e),s=getComputedStyle(e),content={left:r.left+parseFloat(s.borderLeftWidth)+parseFloat(s.paddingLeft),
            right:r.right-parseFloat(s.borderRightWidth)-parseFloat(s.paddingRight)};
          const dates=[...e.querySelectorAll('input.date-input')].map(input=>{
            const control=input.closest('.date-control'),placeholder=control.querySelector('.date-field-placeholder'),
              trigger=control.querySelector('.date-picker-trigger'),r=b(input),s=getComputedStyle(input),tr=b(trigger),
              left=r.left+parseFloat(s.borderLeftWidth)+parseFloat(s.paddingLeft),
              right=r.right-parseFloat(s.borderRightWidth)-parseFloat(s.paddingRight),range=document.createRange();
            range.selectNodeContents(placeholder);const text=b(range),triggerVisible=tr.width>0&&getComputedStyle(trigger).visibility!=='hidden';
            return {name:input.name,input:r,text,trigger:tr,triggerVisible,
              nativeContentWidth:right-left,usableDateWidth:Math.min(right,triggerVisible?tr.left:right)-left,
              placeholderFits:text.left>=left-2&&text.right<=(triggerVisible?tr.left:right)+2&&text.top>=r.top-2&&text.bottom<=r.bottom+2};
          });
          const controls=[...e.querySelectorAll('input:not([type="hidden"]),select')].map(c=>({name:c.name,...b(c),field:b(c.closest('.stay-field'))})),pairs=[];
          for(let i=0;i<controls.length;i++)for(let j=i+1;j<controls.length;j++){
            const a=controls[i],c=controls[j];
            if((a.right<=c.left+2||c.right<=a.left+2)&&Math.min(a.bottom,c.bottom)-Math.max(a.top,c.top)>Math.min(a.height,c.height)*.5)
              pairs.push({first:a.name,second:c.name,firstBox:a,secondBox:c,aligned:Math.abs(a.top-c.top)<=2&&Math.abs(a.bottom-c.bottom)<=2});
          }
          return {content,dates,controls,pairs};
        }""")
        self.check("Homepage compact form has both date controls", len(state["dates"]) == 2, state["dates"])
        self.check("Visible Choose date text stays clear of calendar trigger",
                   all(d["placeholderFits"] for d in state["dates"]), state["dates"])
        self.check("Homepage native date content has at least 100px of usable width",
                   all(d["nativeContentWidth"] >= 100 and d["usableDateWidth"] >= 100 for d in state["dates"]), state["dates"])
        self.check("Homepage compact controls stay within their fields and form padding",
                   all(c["left"] >= max(c["field"]["left"], state["content"]["left"]) - 2
                       and c["right"] <= min(c["field"]["right"], state["content"]["right"]) + 2
                       for c in state["controls"]), state["controls"])
        self.check("Homepage shared-row controls have matching baselines",
                   all(p["aligned"] for p in state["pairs"]), state["pairs"])
        self.overflow(page, "Homepage compact form")
        if self.scope["width"] in [601, 768]:
            self.screenshot(form, "compact-form")


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:3082")
    parser.add_argument("--output", default="evidence/alignment/alignment-states-qa.json")
    parser.add_argument("--engines", nargs="+", default=["chromium"], help="chromium webkit; commas also accepted")
    parser.add_argument("--only-home", action="store_true", help="Run the narrow homepage form regression only")
    parser.add_argument("--routes", nargs="+", help="Limit a regression rerun to these routes")
    args = parser.parse_args()
    args.base_url = args.base_url.rstrip("/")
    args.engines = list(dict.fromkeys(e for value in args.engines for e in value.split(",")))
    if any(e not in ["chromium", "webkit"] for e in args.engines):
        parser.error("--engines supports chromium and webkit")
    if "webkit" in args.engines and urlsplit(args.base_url).scheme != "https":
        parser.error("WebKit requires HTTPS because this site's CSP upgrades insecure requests")
    return args


def main():
    audit = Audit(parse_args())
    cases = [(width, route, selector, draft) for width in WIDTHS for route, selector, draft in FORMS]
    cases += [(width, "/rooms/deluxe-room", None, None) for width in [901, 1024, 1100]]
    cases += [(width, "/", None, None) for width in [601, 640, 768, 1024]]
    if audit.args.only_home:
        cases = [case for case in cases if case[1] == "/"]
    if audit.args.routes:
        cases = [case for case in cases if case[1] in audit.args.routes]
    try:
        with sync_playwright() as playwright:
            for engine in audit.args.engines:
                browser = getattr(playwright, engine).launch(headless=True, **({"channel": "msedge"} if engine == "chromium" else {}))
                try:
                    for width, route, selector, draft in cases:
                        audit.scope = {"engine": engine, "width": width, "route": route}
                        context = browser.new_context(viewport={"width": width, "height": 844 if width <= 768 else 1000},
                                                      timezone_id="Asia/Kolkata", reduced_motion="no-preference")
                        try:
                            page = context.new_page()
                            audit.watch(context, page)
                            response = page.goto(audit.args.base_url + route, wait_until="networkidle")
                            audit.check("Route responds successfully", bool(response and response.ok))
                            page.locator("main").wait_for()
                            page.evaluate("document.fonts.ready")
                            if route == "/":
                                audit.home_compact(page)
                            elif selector:
                                audit.enquiry(page, selector, draft)
                            else:
                                audit.room(page)
                        except Exception as error:
                            audit.check("State audit completes", False, {"name": type(error).__name__, "message": str(error)})
                        finally:
                            context.close()
                            audit.save()
                finally:
                    browser.close()
    except Exception as error:
        audit.check("Browser audit completes", False, {"name": type(error).__name__, "message": str(error)})
    finally:
        audit.check("No JavaScript runtime errors", not audit.report["runtime_errors"], audit.report["runtime_errors"])
        audit.check("No WhatsApp navigation attempted", not audit.report["blocked_external_requests"], audit.report["blocked_external_requests"])
        audit.save()
    return 1 if audit.report["summary"]["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
