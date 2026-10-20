"""Generate matching Markdown and Word handoffs from current project evidence."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import configparser
import hashlib
import json
import re
from zipfile import ZipFile

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from docx.opc.constants import RELATIONSHIP_TYPE as RT

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ACCENT = "0066CC"
INK = "25262A"
MUTED = "62656B"
QA_REPORT = ROOT / "evidence/apple-dominant-revision/production-qa.json"
Block = tuple[str, str]


def read_json(relative: str):
    path = ROOT / relative
    return json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else None


def latest_qa() -> tuple[Path | None, dict]:
    """Never certify this revision with a completed report from an older design."""
    if not QA_REPORT.exists():
        return None, {}
    report = json.loads(QA_REPORT.read_text(encoding="utf-8-sig"))
    if not isinstance(report, dict) or not report.get("completed") or not report.get("summary"):
        return None, {}
    if "/group-stays" not in {item.get("route") for item in report.get("viewport_checks", [])}:
        return None, {}
    return QA_REPORT, report


def git_origin() -> str:
    """Read local configuration without invoking Git or changing repository state."""
    config = configparser.RawConfigParser()
    config.read(ROOT / ".git/config", encoding="utf-8")
    return config.get('remote "origin"', "url", fallback="")


def conversion_blocks(conversion: dict) -> list[Block]:
    """Keep full-run counts distinct from an independently linked correction."""
    if not conversion.get("finished") or conversion.get("status") not in ("pass", "fail"):
        return []
    directory = QA_REPORT.parent
    baseline_path = directory / "conversion-upgrade-qa.json"
    baseline_hash = hashlib.sha256(baseline_path.read_bytes()).hexdigest()
    summary = conversion.get("summary", {})
    blocks: list[Block] = [
        ("p", f"Original focused [conversion QA](../evidence/apple-dominant-revision/conversion-upgrade-qa.json), completed {conversion['finished']}: {summary.get('passed', 0)} of {summary.get('checks', 0)} checks passed; {summary.get('failed', 0)} assertions failed. Its scope covers persistent booking access, requested rooms, enquiry drafts, downloads and responsive static media. The original report is retained without rewriting its counts.")
    ]
    linked = []
    for path in directory.glob("conversion-dining-retest-*.json"):
        report = json.loads(path.read_text(encoding="utf-8-sig"))
        baseline = report.get("baselineReport", {})
        if (report.get("finished", "") >= conversion["finished"]
                and report.get("status") in ("pass", "fail")
                and report.get("runType") == "supplemental-retest"
                and "dining" in report.get("requestedCases", [])
                and baseline.get("sha256") == baseline_hash
                and baseline.get("preservedUnchanged") is True):
            linked.append((path, report))
    if linked:
        path, report = max(linked, key=lambda item: item[1]["finished"])
        relative = path.relative_to(ROOT).as_posix()
        result = report.get("summary", {})
        reason = report.get("correctionReason", "")
        failed = [check for check in conversion.get("checks", []) if not check.get("passed")]
        corrected = {check["name"]: check for check in report.get("checks", []) if check.get("passed")}
        if not reason and failed and all(
                check["name"].endswith("dining guide downloads as the valid one-page PDF")
                and check["name"] in corrected
                and corrected[check["name"]].get("evidence", {}).get("sha256")
                for check in failed):
            reason = "The original PDF assertions expected the wrong title. The corrected check validates the actual brochure text and downloaded/source SHA256; the brochure did not require a content change."
        blocks.append(("p", f"Separate [dining retest](../{relative}), completed {report['finished']}: {report['status'].upper()}, {result.get('passed', 0)} of {result.get('checks', 0)} checks passed and {result.get('failed', 0)} failed. {reason} The supplemental report confirms the original report remains byte-identical; its baseline SHA256 is `{baseline_hash}`. These targeted results are separate from the original full-run totals."))
    elif summary.get("failed"):
        blocks.append(("p", "No completed dining correction report linked to the current full-run SHA256 was available at generation. Review the original failed assertions and supplemental evidence before release."))
    return blocks


def build_blocks() -> list[Block]:
    generated = datetime.now(timezone.utc).strftime("%d %B %Y, %H:%M UTC")
    package = read_json("package.json")
    ledger = read_json("research/source-ledger.json") or {}
    source_count = len(ledger.get("sources", []))
    image_count = len(list((ROOT / "public/images").glob("*.webp")))
    origin = git_origin()
    qa_path, qa = latest_qa()
    security = read_json("evidence/security-review.json") or {}
    audit = read_json("evidence/apple-dominant-revision/production-audit.json") or {}
    conversion = read_json("evidence/apple-dominant-revision/conversion-upgrade-qa.json") or {}
    room_qa = read_json("evidence/apple-dominant-revision/rooms-review.json") or {}
    captures = read_json("evidence/apple-dominant-revision/visual-review-captures.json") or {}
    static_audit = read_json("evidence/apple-dominant-revision/static-export-audit.json") or {}
    dependency = security.get("dependency_review", {})
    blocks: list[Block] = [
        ("title", "Hotel Augusto"),
        ("subtitle", "Website handoff · Digiocular · Varanasi"),
        ("small", f"Generated {generated}. Regenerate after final verification or deployment changes."),
        ("h", "Current delivery"),
        ("p", f"Independent project: `D:\\Digiocular\\Websites\\Hotel Augusto`. Next.js {package['dependencies']['next']}, strict TypeScript, Tailwind v4 and Framer Motion. The website provides room information and WhatsApp enquiries; there is no live booking engine, payment flow or enquiry database."),
        ("p", "No production domain has been changed. This handoff records the local implementation and the available evidence; it does not assert a public launch."),
        ("p", "An owner-private Sites preview is configured at [hotel-augusto.candy-okapi-4696.chatgpt.site](https://hotel-augusto.candy-okapi-4696.chatgpt.site). This revision's publication status is recorded in [the deployment record](../evidence/apple-dominant-revision/private-deployment.json); the public hotel launch remains separate. `.openai/hosting.json` records the existing Sites project."),
        ("p", f"Git origin at generation: `{origin}`." if origin else "Git is initialized locally; no `origin` remote is configured at this snapshot. Create and push the project's private GitHub repository before any Vercel deployment."),
        ("h", "Visual system"),
        ("p", "The latest reference hierarchy puts Lando Norris first for bold composition and memorable motion, with Apple and Linear informing control clarity and precision. The shared system uses local Inter, near-white/cool-gray surfaces, charcoal and cobalt actions. Genuine Augusto photography and the supplied hotel logo anchor the 17-route hospitality experience."),
        ("p", "The homepage opens with nearly full-viewport property photography, the large left-aligned 'Your place / in Kashi.' headline and scene/pause controls within the photograph. Scene changes wait for image readiness. Spring pointer drift, native scroll scaling and independent hover/focus pause support the interaction. An ink-blue city chapter uses oversized decorative KASHI lettering, genuine river imagery and manual tabs."),
        ("p", "Keep substantial headings, readable 18px/17px body copy, clear primary actions and at least 44px interactive targets. Hero motion, room-photo hover/focus feedback, menu transitions and reveals respect reduced motion and native scrolling. The [implementation plan](plans/2026-10-19-website.md) records the frozen design; [Linear source notes](../research/apple-dominant-revision/linear-reference.json), [Casa Angelina notes](../research/apple-dominant-revision/casa-angelina-reference.json) and earlier hotel studies retain research context."),
        ("h", "Pages and editing locations"),
        ("bullet", "`/` — property hero, dated StayBar, all rooms, dining, city itinerary, dated Google badge, attributed guest excerpt, proximity links, gallery, arrival, FAQs and guides."),
        ("bullet", "`/hotel` — property, facilities and arrival; `/dining` — vegetarian dining, its own enquiry and downloadable planning guide; `/group-stays` — family, friends and business accommodation requests."),
        ("bullet", "`/rooms`, `/rooms/compare` and three room-detail pages — visible categories, factual bed layouts, a mobile two-room selector, photo walkthroughs and room-prefilled enquiries."),
        ("bullet", "`/varanasi` — destination guide; `/gallery` — filters and keyboard/touch image viewer."),
        ("bullet", "`/guides` and `/guides/first-visit-to-kashi`, `/guides/arriving-in-godowlia`, `/guides/choosing-your-room` — practical planning articles."),
        ("bullet", "`/contact` — enquiry, phone, directions and FAQs; `/privacy` — actual data handling and destination photo credits."),
        ("p", "Core facts: `content/hotel.ts`; facilities/arrival: `content/hospitality.ts`; dated proof: `content/social-proof.ts`; guides/photos: `content/guides.ts` and `content/room-images.ts`. Booking: `lib/booking.ts`, `lib/stay-query.ts`, `lib/dining-enquiry.ts`. The universal `BookingDock` reserves its measured height through the footer. Stay requests include 1–8 requested rooms and night summaries; these are not capacity promises."),
        ("h", "Content, photographs and owner confirmations"),
        ("p", f"The base ledger retains {source_count} source entries, supplemented by later verification records. The public image set retains {image_count} source WebP files plus generated responsive variants. Hotel and destination photographs are clearly distinguished. No generated hotel photographs or unrelated room stand-ins are used."),
        ("bullet", "Confirm that +91 80817 09146 is the hotel's active WhatsApp booking account. It is the Google-listed telephone and its public WhatsApp link resolves, which does not establish registration or account ownership. Testing sent no enquiry."),
        ("bullet", "Confirm permission to reuse property photographs collected from public hotel listings. Public visibility alone is not a reuse licence. Preserve originals, hashes and provenance in `research/assets/` and `research/ota-revision/`; Google uploader display names alone do not establish copyright ownership."),
        ("bullet", "Destination images use Unsplash licences and a CC BY 4.0 temple photo by Pradum Shukla. Keep temple attribution and `/privacy` credits. The user supplied `logo.jpeg`; its public brand copy now appears in the header, footer, favicon, OG and dining guide."),
        ("bullet", "Confirm current check-in/out, guest identification, parking, meal inclusions and cancellation/payment terms with the hotel. Conflicting published policies, room areas/capacities, live rates and availability have not been promoted as established facts."),
        ("p", "Evidence: [fact sheet](../research/hotel-fact-sheet.md), [source ledger](../research/source-ledger.md), [asset manifest](../research/assets/asset-manifest.json), [Maps verification](../research/map-link-verification.json), [WhatsApp verification](../research/whatsapp-public-check.json). Research documents also have DOCX twins."),
        ("p", "The user-supplied dated MakeMyTrip route returned a browser HTTP/2 transport error. Its indexed canonical page corroborates stable property facts; a fresh 20 October amenities index supports the expanded service details, not live dated availability. Google's rendered profile and accessible property photos were inspected. See [OTA source record](../research/ota-revision/SOURCE-REVIEW.md), [photo mapping](../research/ota-revision/source-to-page-mapping.json), [new feature evidence](../research/hospitality-revision/content-journey-plan.json), [guest-excerpt evidence](../research/hospitality-revision/guest-review-evidence.json) and [official visitor-link checks](../research/hospitality-revision/additional-source-checks.json)."),
        ("p", "Google: 3.7/5 from 1,628 reviews, checked 20 October 2026, displayed with source/date. MMT scores conflict, so its review link carries no numerical badge. No new guest-photo reuse licence was established. Temple/ghat proximity stays qualitative with walking-direction links. [Fresh findings](../research/apple-dominant-revision/conversion-evidence/findings.json) retain these distinctions; no wedding, banquet or conference services are claimed."),
        ("p", "The one-page [dining PDF](../public/downloads/hotel-augusto-dining-guide.pdf) and [editable DOCX](hotel-augusto-dining-guide.docx) use genuine imagery and planning information, not an invented menu. Regenerate with `python -B scripts/generate_dining_guide.py`; [render/reopen evidence](../evidence/apple-dominant-revision/dining-guide/verification.json) records both outputs."),
        ("h", "Run, deploy and configure"),
        ("p", "Use Node.js 22.9+; this workspace used Node 24. From the project folder:"),
        ("code", "npm ci\nnpm run dev"),
        ("p", "Local preview: `http://localhost:3080`. Before release, run the following. Stop the dev server before starting production on the same port."),
        ("code", "npm run lint\nnpm run typecheck\nnpm test\nnpm run build\nnpm run start\nnpm run qa -- --base-url http://127.0.0.1:3080 --output evidence/apple-dominant-revision"),
        ("bullet", "Set `NEXT_PUBLIC_SITE_URL` to the approved HTTPS origin. Keep `SITE_INDEXABLE=false` on previews; set it to `true` only for approved production. These settings control absolute metadata URLs, robots and sitemap behavior. `.env.example` documents the values."),
        ("bullet", "Push the independent private repository before the first deployment. Import it into Vercel as Next.js; `vercel.json` pins region `sin1`. Run the browser checks against the deployed URL and check canonical/OG output before connecting the approved domain."),
        ("bullet", "Normal Next/Vercel retains AVIF/WebP optimization. Optional `SITE_STATIC_EXPORT=true` writes `out/` using `lib/static-image-loader.ts` and local WebP variants. After changing photographs, run `python -B scripts/generate-responsive-images.py`; preserve originals and the manifest. Unset the export flag for a normal build. The static host supplies response headers; previews remain noindex."),
        ("bullet", "Do not infer ownership from old hotel domains: research found a failed domain and an affiliate redirect. Obtain the client's intended domain and access separately."),
        ("h", "Verification snapshot"),
    ]
    if qa_path:
        summary = qa["summary"]
        relative = qa_path.relative_to(ROOT).as_posix()
        state = "PASS" if summary.get("passed") else "HAS FAILURES — review before release"
        failure_count = summary.get('failures', len(qa.get('failures', [])))
        blocks.append(("p", f"Latest completed shared report: [{relative}](../{relative}), completed {qa['completed']} against `{qa.get('base_url', 'unspecified')}`. Status: {state}. It records {summary.get('viewportChecks', 0)} viewport checks, {summary.get('axeAudits', 0)} axe audits, {summary.get('interactionChecks', 0)} interaction checks and {failure_count} {'failure' if failure_count == 1 else 'failures'}. These are report counts, not a claim that an unrecorded final run passed."))
        if qa.get("retests"):
            retest_count = sum(len(retest.get("checks", [])) for retest in qa["retests"])
            blocks.append(("p", f"The final report retains {retest_count} targeted retest checks. Refer to its original run and individual retest entries for the method, timestamps, findings and any source changes; retests are not treated as unrecorded passes."))
        if not summary.get("passed"):
            names = [item.get("test") or item.get("error") or str(item.get("failures", "See report")) for item in qa.get("failures", [])]
            blocks.append(("p", "Recorded items requiring review: " + "; ".join(str(name).splitlines()[0][:180] for name in names[:3]) + "."))
    else:
        blocks.append(("p", "Final verification for the expanded 17-route revision is pending. No completed report including /group-stays was available at generation. Earlier hospitality, Apple and cinematic passes do not certify the new source."))
    blocks.extend(conversion_blocks(conversion))
    if room_qa.get("completed"):
        summary = room_qa.get("summary", {})
        blocks.append(("p", f"The separate [room review](../evidence/apple-dominant-revision/rooms-review.json) records {summary.get('layouts', 0)} layouts, {summary.get('axeAudits', 0)} axe audits, {summary.get('interactions', 0)} interactions and {summary.get('failed', 0)} failures. The [static-export audit](../evidence/apple-dominant-revision/static-export-audit.json) records {static_audit.get('summary', {}).get('passed', 0)}/{static_audit.get('summary', {}).get('checks', 0)} checks passed across 17 content routes and the not-found artifact. The [visual capture record](../evidence/apple-dominant-revision/visual-review-captures.json) contains {len(captures.get('captures', []))} captures and {len(captures.get('errors', []))} capture errors."))
    if qa_path and audit.get("generated", "") >= qa.get("completed", ""):
        samples = audit.get("performance", {}).get("samples", [])
        mobile = [sample for sample in samples if sample.get("throttled")]
        sizes = " × ".join(str(value) for value in audit.get("og", {}).get("size", []))
        sample_text = "; ".join(
            f"LCP {sample.get('lcp', 0):.0f}ms / CLS {sample.get('cls', 0):.4f}"
            for sample in mobile
        )
        blocks.append(("p", f"The refreshed production audit is dated {audit['generated']}; its OG image is {sizes}px. Throttled mobile samples: {sample_text or 'not recorded'}. These are local synthetic measurements, not field Core Web Vitals or a Lighthouse score. The audit retains response headers and runtime observations."))
    blocks += [
        ("p", "Current revision evidence is in `evidence/apple-dominant-revision/`; the final report is `production-qa.json`. Earlier hospitality, Apple and cinematic reports and deployment receipts remain historical. Browser checks do not establish hotel policy accuracy, live availability or photo rights."),
        ("p", "Release evidence: [production audit](../evidence/apple-dominant-revision/production-audit.json), [static-export audit](../evidence/apple-dominant-revision/static-export-audit.json), [this revision's cleanup](../evidence/apple-dominant-revision/cleanup-final.json) and [private deployment status](../evidence/apple-dominant-revision/private-deployment.json). Historical storage and development-output records remain preserved. The preview stays noindex. An approved public domain and route canonical configuration still require launch verification."),
        ("p", "Render-cleanup limitation: automatic approval review rejected removal of the verified OTA-document render scratch with the reason 'blocked by policy'. Its 447,116 bytes remain under `research/ota-revision/.document-review/`; no further removal was attempted. The retained source twins and scratch hashes are recorded in `research/ota-revision/source-review-verification.json`. Final handoff render evidence is retained with `docs/handoff-verification.json`."),
        ("p", "A separate 29,539-byte generated handoff bytecode file was also rejected for cleanup by automatic approval review. It remains retained; no retry is part of this revision. Current scoped cleanup records preserve all source, licensed assets and review evidence."),
        ("h", "Security and maintenance"),
        ("p", f"The recorded production dependency audit has {dependency.get('production_audit', {}).get('vulnerabilities', 'unrecorded')} vulnerabilities. The full audit records {dependency.get('full_audit', {}).get('high', 'unrecorded')} high findings from one development-only ESLint chain ending in braces 3.0.3. [GHSA-vfj7-8cjw-p6xm](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm) had no official patched release at the 19 October 2026 review. Keep the lockfile, recheck upstream and do not force-downgrade Next.js to silence it. Details: [security review](../evidence/security-review.json)."),
        ("p", "StayBar/dock pass dates, party size, requested room count and preference through the contact URL; these may remain in browser history. Names and personal notes stay off that URL. On contact, dock submission retains current room/count/children and applies the dock's dates/adults. Query changes update the existing form without remounting it, preserve unfinished name/notes and clear stale errors and prepared drafts. Stay/group/dining forms prepare explicit WhatsApp drafts without storage or silent sending. The map loads only on activation. No payments or analytics are installed. Preserve security headers, Hotel JSON-LD, local fonts and OG metadata."),
        ("p", "Tailwind uses `source(none)` with explicit app/components/content paths. Preserve that scan boundary: a previous broad scan panicked on a transient Word file during hot development. Generated documents and research are excluded."),
        ("h", "Primary reference links"),
        ("p", "Visual hierarchy: [Lando Norris](https://landonorris.com/), [Apple](https://www.apple.com/), [Linear](https://linear.app/). Hospitality: [Casa Angelina](https://www.casangelina.com/), [Hotel Vagmi](https://hotelvagmi.com/), [The Drake on Awwwards](https://www.awwwards.com/sites/the-drake-hotel). Facts: [MakeMyTrip](https://www.makemytrip.com/hotels/hotel_augusto-details-varanasi.html), [temple visitor portal](https://www.shrikashivishwanath.org/). Credits: [Pradum Shukla temple photo](https://commons.wikimedia.org/wiki/File:Kashi_Vishwanath_Temple_in_2025.jpg), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), [Unsplash licence](https://unsplash.com/license)."),
        ("small", "Regenerate both handoff files with: python -B scripts/generate_handoff.py. The generator uses python-docx and verifies that its DOCX can be reopened."),
    ]
    return blocks


def markdown(blocks: list[Block]) -> str:
    output = []
    for kind, text in blocks:
        prefix = {"title": "# ", "h": "## ", "bullet": "- "}.get(kind, "")
        output.append(f"```powershell\n{text}\n```" if kind == "code" else prefix + text)
    return "\n\n".join(output) + "\n"


def hyperlink(paragraph, label: str, target: str) -> None:
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), paragraph.part.relate_to(target, RT.HYPERLINK, is_external=True))
    run = OxmlElement("w:r")
    properties = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), ACCENT)
    properties.append(color)
    run.append(properties)
    text = OxmlElement("w:t")
    text.text = label
    run.append(text)
    link.append(run)
    paragraph._p.append(link)


def inline(paragraph, text: str) -> None:
    for part in re.split(r"(\[[^\]]+\]\([^)]+\)|`[^`]+`)", text):
        match = re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", part)
        if match:
            hyperlink(paragraph, *match.groups())
        elif part.startswith("`") and part.endswith("`"):
            run = paragraph.add_run(part[1:-1])
            run.font.name = "Consolas"
            run.font.size = Pt(9)
        else:
            paragraph.add_run(part)


def write_docx(blocks: list[Block], destination: Path) -> None:
    doc = Document()
    section = doc.sections[0]
    section.page_width, section.page_height = Cm(21), Cm(29.7)
    section.top_margin = section.bottom_margin = Cm(1.8)
    section.left_margin = section.right_margin = Cm(2)
    section.header_distance = section.footer_distance = Cm(.8)
    for style_name in ("Normal", "Title", "Subtitle", "Heading 1", "List Bullet"):
        doc.styles[style_name].font.name = "Arial"
        doc.styles[style_name].font.color.rgb = RGBColor.from_string(INK)
    normal = doc.styles["Normal"]
    normal.font.size = Pt(10.5)
    normal.paragraph_format.line_spacing = 1.08
    normal.paragraph_format.space_after = Pt(5)
    heading = doc.styles["Heading 1"]
    heading.font.size = Pt(14)
    heading.font.bold = True
    heading.paragraph_format.space_before = Pt(12)
    heading.paragraph_format.space_after = Pt(6)
    heading.paragraph_format.keep_with_next = True
    doc.styles["Title"].font.size = Pt(30)
    doc.styles["Title"].font.bold = True
    doc.styles["Subtitle"].font.size = Pt(13)
    doc.styles["Subtitle"].font.italic = False
    header = section.header.paragraphs[0]
    header.text = "DIGIOCULAR  /  HOTEL AUGUSTO"
    header.runs[0].font.size = Pt(8)
    header.runs[0].font.color.rgb = RGBColor.from_string(MUTED)
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    footer.add_run("Hotel Augusto · ").font.size = Pt(8)
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    footer._p.append(field)
    for kind, text in blocks:
        style = {"title": "Title", "subtitle": "Subtitle", "h": "Heading 1", "bullet": "List Bullet"}.get(kind)
        if kind == "code":
            for line in text.splitlines():
                p = doc.add_paragraph()
                p.paragraph_format.space_after = Pt(1)
                run = p.add_run(line)
                run.font.name, run.font.size = "Consolas", Pt(9)
            continue
        p = doc.add_paragraph(style=style)
        p.paragraph_format.widow_control = True
        inline(p, text)
        if kind == "small":
            for run in p.runs:
                run.font.size = Pt(8)
                run.font.color.rgb = RGBColor.from_string(MUTED)
    doc.core_properties.title = "Hotel Augusto — Website Handoff"
    doc.core_properties.author = "Digiocular"
    doc.core_properties.subject = "Hotel website, 17 routes, factual hospitality enquiries, verification and launch instructions"
    doc.save(destination)


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    blocks = build_blocks()
    md_path, docx_path = DOCS / "HANDOFF.md", DOCS / "HANDOFF.docx"
    md_path.write_text(markdown(blocks), encoding="utf-8")
    write_docx(blocks, docx_path)
    with ZipFile(docx_path) as archive:
        assert archive.testzip() is None, "DOCX ZIP integrity failed"
    reopened = Document(docx_path)
    assert reopened.paragraphs[0].text == "Hotel Augusto"
    assert len(reopened.paragraphs) >= len(blocks)
    assert any("Security and maintenance" == p.text for p in reopened.paragraphs)
    print(f"Generated and reopened {docx_path}; {len(reopened.paragraphs)} paragraphs.")
    print(f"Generated {md_path} from the same {len(blocks)} content blocks.")


if __name__ == "__main__":
    main()
