import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, ArrowUpRight, Plus } from "lucide-react";
import { guides, guideBySlug } from "@/content/guides";
import "../../editorial-pages.css";
import "../guides.css";

export const dynamicParams = false;
export function generateStaticParams() { return guides.map(({ slug }) => ({ slug })); }

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const guide = guideBySlug(slug);
  if (!guide) notFound();
  return { title: { absolute: guide.metaTitle }, description: guide.description, alternates: { canonical: `/guides/${guide.slug}` } };
}

export default async function GuidePage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const guide = guideBySlug(slug);
  if (!guide) notFound();
  const related = guides.filter((item) => item.slug !== slug);
  return (
    <main id="main" className="editorial-page guide-page">
      <header className="container guide-article-intro">
        <Link href="/guides" className="guide-back"><ArrowLeft size={17} aria-hidden="true" />All travel notes</Link>
        <p className="page-context">{guide.category}</p><h1>{guide.title}</h1><p className="guide-deck">{guide.introduction}</p>
      </header>
      <div className="container"><figure className="guide-article-photo"><div><Image src={guide.image} alt={guide.alt} fill priority sizes="(max-width: 760px) calc(100vw - 48px), 89vw" style={{ objectPosition: guide.imagePosition }} /></div>
        <figcaption>{slug === "first-visit-to-kashi" ? <>Shri Kashi Vishwanath Temple · <a href="https://commons.wikimedia.org/wiki/File:Kashi_Vishwanath_Temple_in_2025.jpg" target="_blank" rel="noreferrer">Pradum Shukla</a> · <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noreferrer">CC BY 4.0</a></> : guide.imageCaption}</figcaption>
      </figure></div>
      <div className="container guide-body-layout">
        <aside className="guide-contents"><nav aria-label="On this page"><p>In this guide</p><ol>{guide.sections.map((section) => <li key={section.id}><a href={`#${section.id}`}>{section.title}</a></li>)}</ol><a href="#guest-questions">Questions guests ask</a></nav></aside>
        <article className="guide-article-body">
          <section className="guide-checklist" aria-labelledby="before-you-go"><p className="feature-context">A quick checklist</p><h2 id="before-you-go">Before you begin.</h2><ul>{guide.checklist.map((item) => <li key={item}>{item}</li>)}</ul></section>
          {guide.sections.map((section) => <section className="guide-prose-section" id={section.id} key={section.id}><h2>{section.title}</h2>{section.paragraphs.map((paragraph) => <p key={paragraph}>{paragraph}</p>)}</section>)}
          <section className="guide-questions" id="guest-questions" aria-labelledby="questions-heading"><p className="feature-context">Useful to know</p><h2 id="questions-heading">Questions guests ask.</h2>{guide.questions.map((item) => <details key={item.question}><summary>{item.question}<Plus size={20} aria-hidden="true" /></summary><p>{item.answer}</p></details>)}</section>
          <section className="guide-useful-links" aria-labelledby="useful-links-heading"><h2 id="useful-links-heading">Useful links.</h2><ul>{guide.links.map((link) => <li key={link.href}>{link.href.startsWith("/") ? <Link href={link.href}>{link.label}<ArrowUpRight size={16} aria-hidden="true" /></Link> : <a href={link.href} target="_blank" rel="noreferrer">{link.label}<ArrowUpRight size={16} aria-hidden="true" /></a>}</li>)}</ul></section>
          <div className="guide-stay-enquiry"><h2>Plan your stay.</h2><p>Send your dates, guest details and room preference. The Augusto team will help with the next steps.</p><Link href="/contact#enquire" className="button" style={{ color: "var(--paper)" }}>Enquire about a stay <ArrowUpRight size={18} aria-hidden="true" /></Link></div>
        </article>
      </div>
      <section className="container guide-related" aria-labelledby="more-guides-heading"><p className="feature-context">Keep planning</p><h2 id="more-guides-heading">More from the guide.</h2><div>{related.map((item) => <Link href={`/guides/${item.slug}`} key={item.slug}><span>{item.category}</span><h3>{item.title}</h3><ArrowUpRight size={24} aria-hidden="true" /></Link>)}</div></section>
    </main>
  );
}
