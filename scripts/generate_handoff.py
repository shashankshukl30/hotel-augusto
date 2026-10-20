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
ACCENT = "795938"
INK = "25313D"
MUTED = "69645C"
QA_REPORT = ROOT / "evidence/hospitality-revision/production-qa.json"
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
    return QA_REPORT, report


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
    hospitality = read_json("evidence/hospitality-revision/hotel-dining-review.json") or {}
    security = read_json("evidence/security-review.json") or {}
    audit = read_json("evidence/production-audit.json") or {}
    dev_cleanup = read_json("evidence/dev-output-cleanup.json") or {}
    dependency = security.get("dependency_review", {})
    blocks: list[Block] = [
        ("title", "Hotel Augusto"),
        ("subtitle", "Website handoff · Digiocular · Varanasi"),
        ("small", f"Generated {generated}. Regenerate after final verification or deployment changes."),
        ("h", "Current delivery"),
        ("p", f"Independent project: `D:\\Digiocular\\Websites\\Hotel Augusto`. Next.js {package['dependencies']['next']}, strict TypeScript, Tailwind v4 and Framer Motion. The website provides room information and WhatsApp enquiries; there is no live booking engine, payment flow or enquiry database."),
        ("p", "No production domain has been changed. This handoff records the local implementation and the available evidence; it does not assert a public launch."),
        ("p", "An owner-private Sites preview is configured at [hotel-augusto.candy-okapi-4696.chatgpt.site](https://hotel-augusto.candy-okapi-4696.chatgpt.site). Current publication status is recorded in [the deployment record](../evidence/hospitality-revision/private-deployment.json); the public hotel launch remains separate. `.openai/hosting.json` records the existing Sites project."),
        ("p", f"Git origin at generation: `{origin}`." if origin else "Git is initialized locally; no `origin` remote is configured at this snapshot. Create and push the project's private GitHub repository before any Vercel deployment."),
        ("h", "Visual system"),
        ("p", "The latest 20 October brief brings most Hotel Vagmi elements into Augusto's own hospitality identity. Local Bodoni Moda at weight 400 and Manrope body combine with ivory, ink blue and bronze. Genuine property photographs lead the hero, all three room categories are visible, and detailed dining, arrival and city content give the hotel substance across 16 pages. Asymmetric spreads, fine rules and modest 4–8px corners replace the earlier product-like Apple treatment."),
        ("p", "Interior titles reach roughly 76–104px on desktop and 48–58px on mobile; body copy is 18px desktop / 17px mobile. Rectangular actions are approximately 52–54px high. Hero scene controls, a pause action, photo transitions and reveals respect reduced motion and native scrolling. See the [hospitality reference study](../research/hospitality-revision/reference-study.md), [feature and fact plan](../research/hospitality-revision/content-journey-plan.json) and [implementation plan](plans/2026-10-19-website.md). Earlier design documents remain historical."),
        ("h", "Pages and editing locations"),
        ("bullet", "`/` — genuine-property hero, dated StayBar, welcome, all rooms, dining, city itinerary, an attributed guest excerpt and review links, gallery, arrival, FAQs, guides and a final enquiry."),
        ("bullet", "`/hotel` — the property, reception, facilities and arrival guidance; `/dining` — vegetarian restaurant, room service and meal-plan enquiries."),
        ("bullet", "`/rooms`, `/rooms/compare` and three room-detail pages — visible categories, factual bed layouts, a mobile two-room selector, photo walkthroughs and room-prefilled enquiries."),
        ("bullet", "`/varanasi` — destination guide; `/gallery` — filters and keyboard/touch image viewer."),
        ("bullet", "`/guides` and `/guides/first-visit-to-kashi`, `/guides/arriving-in-godowlia`, `/guides/choosing-your-room` — practical planning articles."),
        ("bullet", "`/contact` — enquiry, phone, directions and FAQs; `/privacy` — actual data handling and destination photo credits."),
        ("p", "Core facts and contact: `content/hotel.ts`. Facilities, review links and arrival: `content/hospitality.ts`. Guides: `content/guides.ts`. Photos: `content/room-images.ts`. Tokens: `app/globals.css`. Booking validation and WhatsApp URLs: `lib/booking.ts`; page-to-page travel preferences: `lib/stay-query.ts`. The reusable `StayBar` and `ArrivalGuide` components serve multiple pages. Adapt the enquiry handoff deliberately when adding an approved booking engine."),
        ("h", "Content, photographs and owner confirmations"),
        ("p", f"Research retains {source_count} source entries covering Google, OTAs, destination authorities and contact verification. The public image set contains {image_count} WebP files. Property photographs show Hotel Augusto; destination photographs are separately identified. No generated hotel photographs or unrelated room stand-ins are used."),
        ("bullet", "Confirm that +91 80817 09146 is the hotel's active WhatsApp booking account. It is the Google-listed telephone and its public WhatsApp link resolves, which does not establish registration or account ownership. Testing sent no enquiry."),
        ("bullet", "Confirm permission to reuse property photographs collected from public hotel listings. Public visibility alone is not a reuse licence. Preserve originals, hashes and provenance in `research/assets/` and `research/ota-revision/`; Google uploader display names alone do not establish copyright ownership."),
        ("bullet", "Destination images use Unsplash licences and a CC BY 4.0 temple photo by Pradum Shukla. Keep the visible temple attribution and `/privacy` credits. The Augusto wordmark is an original typographic treatment, not a recovered official logo."),
        ("bullet", "Confirm current check-in/out, guest identification, parking, meal inclusions and cancellation/payment terms with the hotel. Conflicting published policies, room areas/capacities, live rates and availability have not been promoted as established facts."),
        ("p", "Evidence: [fact sheet](../research/hotel-fact-sheet.md), [source ledger](../research/source-ledger.md), [asset manifest](../research/assets/asset-manifest.json), [Maps verification](../research/map-link-verification.json), [WhatsApp verification](../research/whatsapp-public-check.json). Research documents also have DOCX twins."),
        ("p", "The user-supplied dated MakeMyTrip route returned a browser HTTP/2 transport error. Its indexed canonical page corroborates stable property facts; a fresh 20 October amenities index supports the expanded service details, not live dated availability. Google's rendered profile and accessible property photos were inspected. See [OTA source record](../research/ota-revision/SOURCE-REVIEW.md), [photo mapping](../research/ota-revision/source-to-page-mapping.json), [new feature evidence](../research/hospitality-revision/content-journey-plan.json), [guest-excerpt evidence](../research/hospitality-revision/guest-review-evidence.json) and [official visitor-link checks](../research/hospitality-revision/additional-source-checks.json)."),
        ("h", "Run, deploy and configure"),
        ("p", "Use Node.js 22.9+; this workspace used Node 24. From the project folder:"),
        ("code", "npm ci\nnpm run dev"),
        ("p", "Local preview: `http://localhost:3080`. Before release, run the following. Stop the dev server before starting production on the same port."),
        ("code", "npm run lint\nnpm run typecheck\nnpm test\nnpm run build\nnpm run start\npython scripts/qa_hospitality_revision.py --base-url http://127.0.0.1:3080"),
        ("bullet", "Set `NEXT_PUBLIC_SITE_URL` to the approved HTTPS origin. Keep `SITE_INDEXABLE=false` on previews; set it to `true` only for approved production. These settings control absolute metadata URLs, robots and sitemap behavior. `.env.example` documents the values."),
        ("bullet", "Push the independent private repository before the first deployment. Import it into Vercel as Next.js; `vercel.json` pins region `sin1`. Run the browser checks against the deployed URL and check canonical/OG output before connecting the approved domain."),
        ("bullet", "Normal Next.js/Vercel operation is the default. For the private static preview only, set `SITE_STATIC_EXPORT=true` before `npm run build`; the result is `out/`. Unset the flag for the next normal build. Static export disables server image optimization; the static host must supply response headers. Keep previews noindex and verify their deployed behavior."),
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
        blocks.append(("p", "Final production verification for this hospitality revision is pending. No completed current-revision report was available at generation. Historical Apple/cinematic passes do not certify the new pages or interactions."))
    if qa_path and audit.get("generated", "") >= qa.get("completed", ""):
        samples = audit.get("performance", {}).get("samples", [])
        mobile = [sample for sample in samples if sample.get("throttled")]
        sizes = " × ".join(str(value) for value in audit.get("og", {}).get("size", []))
        sample_text = "; ".join(
            f"LCP {sample.get('lcp', 0):.0f}ms / CLS {sample.get('cls', 0):.4f}"
            for sample in mobile
        )
        blocks.append(("p", f"The refreshed production audit is dated {audit['generated']}; its OG image is {sizes}px. Throttled mobile samples: {sample_text or 'not recorded'}. These are local synthetic measurements, not field Core Web Vitals or a Lighthouse score. The audit retains response headers and runtime observations."))
    if hospitality:
        pages = hospitality.get("pages", [])
        widths = ", ".join(str(width) for width in sorted({item['viewport'] for item in pages}))
        state = "pass" if hospitality.get("passed") else "require review"
        visual = "Screenshots and the activated Hotel Augusto map pin were visually inspected." if hospitality.get("visuallyInspected") else "Visual review is not yet recorded."
        blocks.append(("p", f"Focused hotel/dining review: {len(pages)} route/viewport records at {widths}px and {len(hospitality.get('interactions', []))} interactions; checks {state}. {visual} This focused dev check supplements the production report. Evidence: [page review](../evidence/hospitality-revision/hotel-dining-review.json)."))
    blocks += [
        ("p", "Current revision evidence is in `evidence/hospitality-revision/`; the final report is `evidence/hospitality-revision/production-qa.json`. Earlier Apple/cinematic reports remain history. Browser checks do not establish hotel policy accuracy, live availability or photo rights."),
        ("p", "Release evidence: [production audit](../evidence/production-audit.json), [scoped storage cleanup](../evidence/storage-cleanup.json), and [inactive development output cleanup](../evidence/dev-output-cleanup.json). " + (f"The development cleanup records {dev_cleanup['removedBytes']:,} bytes removed after stopping the dev session; production was verified afterwards. " if dev_cleanup.get("productionVerifiedAfter") and "removedBytes" in dev_cleanup else "") + "The local preview remains noindex. An approved public domain and route canonical configuration still require launch verification."),
        ("p", "Render-cleanup limitation: automatic approval review rejected removal of the verified OTA-document render scratch with the reason 'blocked by policy'. Its 447,116 bytes remain under `research/ota-revision/.document-review/`; no further removal was attempted. The retained source twins and scratch hashes are recorded in `research/ota-revision/source-review-verification.json`. Final handoff render evidence is retained with `docs/handoff-verification.json`."),
        ("p", "A separate 29,539-byte generated handoff bytecode file was also rejected for cleanup by automatic approval review. It remains retained; no retry is part of this revision. Current scoped cleanup records preserve all source, licensed assets and review evidence."),
        ("h", "Security and maintenance"),
        ("p", f"The recorded production dependency audit has {dependency.get('production_audit', {}).get('vulnerabilities', 'unrecorded')} vulnerabilities. The full audit records {dependency.get('full_audit', {}).get('high', 'unrecorded')} high findings from one development-only ESLint chain ending in braces 3.0.3. [GHSA-vfj7-8cjw-p6xm](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm) had no official patched release at the 19 October 2026 review. Keep the lockfile, recheck upstream and do not force-downgrade Next.js to silence it. Details: [security review](../evidence/security-review.json)."),
        ("p", "StayBar passes validated dates, party size and room preference through the contact URL; these may remain in browser history. Names and personal notes stay off that URL. The form prepares a WhatsApp draft without saving enquiries or sending silently. The Google map iframe loads only on explicit activation. No payment collection or analytics is installed. Security headers, Hotel JSON-LD, local fonts and a 1200×630 OG image are included. Privacy must be revisited when these features change."),
        ("h", "Primary reference links"),
        ("p", "Design: [Hotel Vagmi](https://hotelvagmi.com/), [The Drake on Awwwards](https://www.awwwards.com/sites/the-drake-hotel), plus Shree Ganesha Palace and live reference captures in `research/hospitality-revision/`. Property: [MakeMyTrip Hotel Augusto](https://www.makemytrip.com/hotels/hotel_augusto-details-varanasi.html). Destination: [official temple visitor portal](https://www.shrikashivishwanath.org/), [Kashi Vishwanath government page](https://varanasi.nic.in/tourist-place/shri-kashi-vishwanath-temple/), [Dashashwamedh Ghat](https://kashi.gov.in/listing-details/dashashwamedh-ghat). Credits: [Pradum Shukla temple photo](https://commons.wikimedia.org/wiki/File:Kashi_Vishwanath_Temple_in_2025.jpg), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), [Unsplash licence](https://unsplash.com/license)."),
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
        if kind == "h" and text in ("Content, photographs and owner confirmations", "Verification snapshot"):
            p.paragraph_format.page_break_before = True
        inline(p, text)
        if kind == "small":
            for run in p.runs:
                run.font.size = Pt(8)
                run.font.color.rgb = RGBColor.from_string(MUTED)
    doc.core_properties.title = "Hotel Augusto — Website Handoff"
    doc.core_properties.author = "Digiocular"
    doc.core_properties.subject = "Hotel hospitality website, stay-planning features, factual evidence and launch instructions"
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
