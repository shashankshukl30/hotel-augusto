"""Generate matching Markdown and Word handoffs from current project evidence."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import re
import subprocess
from zipfile import ZipFile

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from docx.opc.constants import RELATIONSHIP_TYPE as RT

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BLUE = "0066CC"
INK = "23252B"
MUTED = "565B65"
Block = tuple[str, str]


def read_json(relative: str):
    path = ROOT / relative
    return json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else None


def latest_qa() -> tuple[Path | None, dict]:
    candidates = []
    for path in (ROOT / "evidence").glob("qa*.json"):
        try:
            report = json.loads(path.read_text(encoding="utf-8-sig"))
        except (ValueError, OSError):
            continue
        if isinstance(report, dict) and report.get("completed") and report.get("summary"):
            candidates.append((report["completed"], path, report))
    if not candidates:
        return None, {}
    _, path, report = max(candidates, key=lambda item: item[0])
    return path, report


def git_origin() -> str:
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"], cwd=ROOT,
        capture_output=True, text=True, check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def build_blocks() -> list[Block]:
    generated = datetime.now(timezone.utc).strftime("%d %B %Y, %H:%M UTC")
    package = read_json("package.json")
    ledger = read_json("research/source-ledger.json") or {}
    source_count = len(ledger.get("sources", []))
    image_count = len(list((ROOT / "public/images").glob("*.webp")))
    origin = git_origin()
    qa_path, qa = latest_qa()
    hospitality = read_json("evidence/apple-premium/hospitality-review.json") or []
    security = read_json("evidence/security-review.json") or {}
    dev_cleanup = read_json("evidence/dev-output-cleanup.json") or {}
    dependency = security.get("dependency_review", {})
    blocks: list[Block] = [
        ("title", "Hotel Augusto"),
        ("subtitle", "Website handoff · Digiocular · Varanasi"),
        ("small", f"Generated {generated}. Regenerate after final verification or deployment changes."),
        ("h", "Current delivery"),
        ("p", f"Independent project: `D:\\Digiocular\\Websites\\Hotel Augusto`. Next.js {package['dependencies']['next']}, strict TypeScript, Tailwind v4 and Framer Motion. The website provides room information and WhatsApp enquiries; there is no live booking engine, payment flow or enquiry database."),
        ("p", "No production domain has been changed. This handoff records the local implementation and the available evidence; it does not assert a public launch."),
        ("p", f"Git origin at generation: `{origin}`." if origin else "Git is initialized locally; no `origin` remote is configured at this snapshot. Create and push the project's private GitHub repository before any Vercel deployment."),
        ("h", "Visual system"),
        ("p", "The 20 October correction restores the Apple-inspired foundation the user explicitly liked, now larger and more animated. Local Manrope display at weight 650 and Inter body, pearl surfaces, charcoal text and a restrained blue accent support large real photographs, generous spacing and rounded panels. Interior titles reach roughly 80–104px on desktop and 52–64px on mobile, with 18px desktop / 17px mobile body copy and readable labels. All 11 pages and the improved Varanasi hero remain."),
        ("p", "Hotel and dining retain their distinct compositions. Photography and form panels use soft 24–32px corners; primary actions and enquiry controls are approximately 56px desktop / 50px mobile. Contact fields stay at 17px or larger on mobile. Visible entrance and scroll motion respect reduced-motion preferences and native scrolling. See [current Apple premium contract](../research/apple-premium-direction.md) and [implementation plan](plans/2026-10-19-website.md). The previous verdigris and smaller Apple revisions remain historical references."),
        ("h", "Pages and editing locations"),
        ("bullet", "`/` — hotel introduction, room selection, dining and Varanasi photography."),
        ("bullet", "`/hotel` — the property, reception, facilities and arrival guidance; `/dining` — vegetarian restaurant, room service and meal-plan enquiries."),
        ("bullet", "`/rooms` and `/rooms/deluxe-room`, `/rooms/deluxe-twin-room`, `/rooms/family-room` — comparison and individual room pages."),
        ("bullet", "`/varanasi` — destination guide; `/gallery` — filters and keyboard/touch image viewer."),
        ("bullet", "`/contact` — enquiry, phone, directions and FAQs; `/privacy` — actual data handling and destination photo credits."),
        ("p", "Edit facts and the contact number in `content/hotel.ts`; room photographs in `content/room-images.ts`; visual tokens in `app/globals.css`. Booking validation and WhatsApp URL generation live in `lib/booking.ts`, with the form in `components/booking-form.tsx`. Replace that handoff deliberately when integrating an approved booking engine."),
        ("h", "Content, photographs and owner confirmations"),
        ("p", f"Research retains {source_count} source entries covering Google, OTAs, destination authorities and contact verification. The public image set contains {image_count} WebP files. Property photographs show Hotel Augusto; destination photographs are separately identified. No generated hotel photographs or unrelated room stand-ins are used."),
        ("bullet", "Confirm that +91 80817 09146 is the hotel's active WhatsApp booking account. It is the Google-listed telephone and its public WhatsApp link resolves, which does not establish registration or account ownership. Testing sent no enquiry."),
        ("bullet", "Confirm permission to reuse property photographs collected from public hotel listings. Public visibility alone is not a reuse licence. Preserve originals, hashes and provenance in `research/assets/` and `research/ota-revision/`; Google uploader display names alone do not establish copyright ownership."),
        ("bullet", "Destination images use Unsplash licences and a CC BY 4.0 temple photo by Pradum Shukla. Keep the visible temple attribution and `/privacy` credits. The Augusto wordmark is an original typographic treatment, not a recovered official logo."),
        ("bullet", "Confirm current check-in/out, guest identification, parking, meal inclusions and cancellation/payment terms with the hotel. Conflicting published policies, room areas/capacities, live rates and availability have not been promoted as established facts."),
        ("p", "Evidence: [fact sheet](../research/hotel-fact-sheet.md), [source ledger](../research/source-ledger.md), [asset manifest](../research/assets/asset-manifest.json), [Maps verification](../research/map-link-verification.json), [WhatsApp verification](../research/whatsapp-public-check.json). Research documents also have DOCX twins."),
        ("p", "The user-supplied MakeMyTrip dated route was tried in a fresh browser and returned an HTTP/2 transport error. The canonical indexed MMT property page corroborates the address, room categories and vegetarian dining; it does not verify live dated availability. Google’s rendered profile and eight accessible still-photo entries were inspected, and three additional real property photographs were collected. See [OTA revision record](../research/ota-revision/SOURCE-REVIEW.md), [source-to-page mapping](../research/ota-revision/source-to-page-mapping.json) and [new asset ledger](../research/ota-revision/asset-candidates.json)."),
        ("h", "Run, deploy and configure"),
        ("p", "Use Node.js 22.9+; this workspace used Node 24. From the project folder:"),
        ("code", "npm ci\nnpm run dev"),
        ("p", "Local preview: `http://localhost:3080`. Before release, run the following. Stop the dev server before starting production on the same port."),
        ("code", "npm run lint\nnpm run typecheck\nnpm test\nnpm run build\nnpm run start\npython scripts/browser_qa.py --base-url http://127.0.0.1:3080"),
        ("bullet", "Set `NEXT_PUBLIC_SITE_URL` to the approved HTTPS origin. Keep `SITE_INDEXABLE=false` on previews; set it to `true` only for approved production. These settings control absolute metadata URLs, robots and sitemap behavior. `.env.example` documents the values."),
        ("bullet", "Push the independent private repository before the first deployment. Import it into Vercel as Next.js; `vercel.json` pins region `sin1`. Run the browser checks against the deployed URL and check canonical/OG output before connecting the approved domain."),
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
            blocks.append(("p", f"The initial report recorded {qa.get('initialSummary', {}).get('failures', 'unrecorded')} failed automated check. The final report includes {retest_count} targeted keyboard-link retests using a 1px outer-edge rounding tolerance and fully visible text bounds. The original run, retest evidence and timestamps remain preserved in that report; no application change was required between those runs."))
        if not summary.get("passed"):
            names = [item.get("test") or item.get("error") or str(item.get("failures", "See report")) for item in qa.get("failures", [])]
            blocks.append(("p", "Recorded items requiring review: " + "; ".join(str(name).splitlines()[0][:180] for name in names[:3]) + "."))
    else:
        blocks.append(("p", "No completed shared QA report was available at generation. Final verification remains unrecorded; do not infer a pass from this document."))
    if hospitality:
        passed = all(item.get("scrollWidth") == item.get("clientWidth") and not item.get("errors") and all(image.get("loaded") for image in item.get("images", [])) for item in hospitality)
        widths = ", ".join(str(width) for width in sorted({item['viewport'] for item in hospitality}))
        blocks.append(("p", f"Focused hotel, dining, contact and privacy review: {len(hospitality)} route/viewport records at {widths}px; layout/image/runtime checks {'pass' if passed else 'require review'}. The rendered screenshots were inspected for type scale, image framing and control alignment. Evidence: [page review](../evidence/apple-premium/hospitality-review.json)."))
    blocks += [
        ("p", "Current revision evidence is in `evidence/apple-premium/`; the intended final report is `evidence/qa-apple-premium-production.json`. Earlier Apple/cinematic reports and `research/awwwards-revision/` remain reference history. Use the latest completed report and its remaining failures; earlier passes do not certify later edits. Browser checks do not establish hotel policy accuracy or photo rights."),
        ("p", "Release evidence: [production audit](../evidence/production-audit.json), [scoped storage cleanup](../evidence/storage-cleanup.json), and [inactive development output cleanup](../evidence/dev-output-cleanup.json). " + (f"The development cleanup records {dev_cleanup['removedBytes']:,} bytes removed after stopping the dev session; production was verified afterwards. " if dev_cleanup.get("productionVerifiedAfter") and "removedBytes" in dev_cleanup else "") + "The local preview remains noindex. An approved public domain and route canonical configuration still require launch verification."),
        ("p", "Render-cleanup limitation: automatic approval review rejected removal of the verified OTA-document render scratch with the reason 'blocked by policy'. Its 447,116 bytes remain under `research/ota-revision/.document-review/`; no further removal was attempted. The retained source twins and scratch hashes are recorded in `research/ota-revision/source-review-verification.json`. Final handoff render evidence is retained with `docs/handoff-verification.json`."),
        ("h", "Security and maintenance"),
        ("p", f"The recorded production dependency audit has {dependency.get('production_audit', {}).get('vulnerabilities', 'unrecorded')} vulnerabilities. The full audit records {dependency.get('full_audit', {}).get('high', 'unrecorded')} high findings from one development-only ESLint chain ending in braces 3.0.3. [GHSA-vfj7-8cjw-p6xm](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm) had no official patched release at the 19 October 2026 review. Keep the lockfile, recheck upstream and do not force-downgrade Next.js to silence it. Details: [security review](../evidence/security-review.json)."),
        ("p", "The enquiry stays in browser memory until the visitor opens the encoded WhatsApp link. No silent message sending, payment collection, analytics or enquiry persistence is installed. Security headers, Hotel JSON-LD, local fonts and a 1200×630 OG image are included. Revisit privacy and security when a booking engine or analytics is added."),
        ("h", "Primary reference links"),
        ("p", "Design: [The Drake on Awwwards](https://www.awwwards.com/sites/the-drake-hotel), [Kaskady on Awwwards](https://www.awwwards.com/sites/hotel-spa-resort-kaskady), [Casa Cook on Awwwards](https://www.awwwards.com/sites/casa-cook-hotels), [Apple typography](https://developer.apple.com/design/human-interface-guidelines/typography). Property: [MakeMyTrip Hotel Augusto](https://www.makemytrip.com/hotels/hotel_augusto-details-varanasi.html). Destination: [Kashi Vishwanath](https://varanasi.nic.in/tourist-place/shri-kashi-vishwanath-temple/), [Dashashwamedh Ghat](https://kashi.gov.in/listing-details/dashashwamedh-ghat). Credits: [Pradum Shukla temple photo](https://commons.wikimedia.org/wiki/File:Kashi_Vishwanath_Temple_in_2025.jpg), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), [Unsplash licence](https://unsplash.com/license)."),
        ("small", "Regenerate both handoff files with: python scripts/generate_handoff.py. The generator uses python-docx and verifies that its DOCX can be reopened."),
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
    color.set(qn("w:val"), BLUE)
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
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(7)
    heading = doc.styles["Heading 1"]
    heading.font.size = Pt(14)
    heading.font.bold = True
    heading.paragraph_format.space_before = Pt(15)
    heading.paragraph_format.space_after = Pt(7)
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
        if kind == "h" and text in ("Content, photographs and owner confirmations", "Verification snapshot"):
            p.paragraph_format.page_break_before = True
        inline(p, text)
        if kind == "small":
            for run in p.runs:
                run.font.size = Pt(8)
                run.font.color.rgb = RGBColor.from_string(MUTED)
    doc.core_properties.title = "Hotel Augusto — Website Handoff"
    doc.core_properties.author = "Digiocular"
    doc.core_properties.subject = "Enlarged Apple-inspired hotel website, motion, source evidence and launch instructions"
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
