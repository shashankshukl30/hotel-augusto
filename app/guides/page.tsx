import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { Reveal } from "@/components/reveal";
import { guides } from "@/content/guides";
import "../editorial-pages.css";
import "./guides.css";

export const metadata: Metadata = {
  title: { absolute: "Practical Travel Guides for Varanasi | Hotel Augusto" },
  description: "Plan your stay at Hotel Augusto with practical guides to Kashi Vishwanath, arriving in Godowlia and choosing the right room.",
  alternates: { canonical: "/guides" },
};

export default function GuidesPage() {
  return (
    <main id="main" className="editorial-page guides-page">
      <section className="container editorial-intro">
        <Reveal className="intro-title"><p className="page-context">Hotel Augusto / Travel notes</p><h1>Before<br />you arrive.</h1></Reveal>
        <Reveal className="intro-note" delay={0.1}><p>A few practical notes for your room, your arrival and your first days in Kashi.</p><Link href="/contact#enquire" className="editorial-link">Plan your stay <ArrowUpRight size={18} aria-hidden="true" /></Link></Reveal>
      </section>
      <section className="container guide-index" aria-label="Practical travel guides">
        {guides.map((guide, index) => <Reveal key={guide.slug}><article className="guide-index-entry">
          <Link href={`/guides/${guide.slug}`} className="guide-index-photo" tabIndex={-1} aria-hidden="true"><Image src={guide.image} alt="" fill sizes="(max-width: 760px) calc(100vw - 48px), 42vw" style={{ objectPosition: guide.imagePosition }} priority={index === 0} /></Link>
          <div className="guide-index-copy"><p className="feature-context">{guide.category}</p><h2><Link href={`/guides/${guide.slug}`}>{guide.title}</Link></h2><p>{guide.description}</p><Link className="editorial-link" href={`/guides/${guide.slug}`}>Read the guide <ArrowUpRight size={18} aria-hidden="true" /></Link></div>
        </article></Reveal>)}
        <div className="guide-index-contact"><p>Ready to make your plans?</p><Link className="editorial-link" href="/contact#enquire">Speak with Hotel Augusto <ArrowUpRight size={18} aria-hidden="true" /></Link></div>
      </section>
    </main>
  );
}
