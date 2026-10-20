import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { ArrowUpRight, ChevronRight } from "lucide-react";
import { Reveal } from "@/components/reveal";
import { WhatsAppIcon } from "@/components/whatsapp-icon";
import { hotel } from "@/content/hotel";
import "../hospitality-pages.css";

export const metadata: Metadata = {
  title: "Vegetarian Dining at Hotel Augusto | Varanasi Hotel",
  description: "Vegetarian dining and room service at Hotel Augusto, Varanasi. See the restaurant and ask the hotel about menus, serving times and breakfast inclusions.",
};

const mealDetails = [
  { title: "Breakfast & your room rate", text: "Planning an early start? Ask about breakfast serving times and whether it is included in the room plan you choose." },
  { title: "At the restaurant", text: "Vegetarian dining is available at the hotel. Speak with the team for the current menu, opening hours and any dietary requirements." },
  { title: "In your room", text: "Room service is available. Ask the hotel what can be ordered, the service times and applicable charges during your stay." },
];

export default function DiningPage() {
  const whatsapp = `https://wa.me/${hotel.whatsappNumber}?text=${encodeURIComponent("Hello Hotel Augusto, I am planning a stay. Could you share the restaurant menu, serving hours, and whether breakfast is included in my room rate?")}`;

  return <main id="main" className="hospitality-page dining-page">
    <div className="hospitality-shell"><nav className="hospitality-breadcrumb" aria-label="Breadcrumb"><Link href="/">Home</Link><ChevronRight size={13} aria-hidden="true" /><span aria-current="page">Dining</span></nav></div>

    <section className="hospitality-dining-hero" aria-labelledby="dining-title">
      <Image src="/images/dining-room-wide.webp" alt="A wide view of the dining room at Hotel Augusto, with tables arranged for guests" fill preload sizes="(max-width: 760px) 1100px, 100vw" quality={85} />
      <div className="hospitality-dining-shade" />
      <div className="hospitality-shell hospitality-dining-hero-copy">
        <Reveal><p className="hospitality-context">Vegetarian dining at Augusto</p><h1 id="dining-title">Take a seat.</h1></Reveal>
        <p>Make a little time<br />for a meal at the hotel.</p>
      </div>
    </section>
    <div className="hospitality-shell hospitality-dining-caption"><span>The restaurant at Hotel Augusto.</span><span>Godowlia, Varanasi</span></div>

    <section className="hospitality-shell hospitality-dining-introduction" aria-labelledby="dining-intro-title">
      <p className="hospitality-context">A table at your hotel</p>
      <Reveal><h2 id="dining-intro-title">Vegetarian dining.<br />A little closer.</h2><p>The on-site restaurant gives you a place to sit down for a vegetarian meal without heading back out. Between your plans for Kashi, leave a little room in the day to gather around the table.</p></Reveal>
    </section>

    <section className="hospitality-shell hospitality-dining-details" aria-labelledby="meal-title">
      <Reveal className="hospitality-dining-portrait"><figure><div className="hospitality-photo"><Image src="/images/google-dining-room.webp" alt="Marble-topped tables and the serving counter inside Hotel Augusto's restaurant" fill sizes="(max-width: 760px) 90vw, 50vw" quality={85} /></div><figcaption>A place to sit down together.</figcaption></figure></Reveal>
      <div className="hospitality-meal-copy">
        <Reveal><p className="hospitality-context">Plan around your day</p><h2 id="meal-title">Before you<br />pull up a chair.</h2></Reveal>
        <div className="hospitality-meal-rows">{mealDetails.map((detail, index) => <div key={detail.title}><span aria-hidden="true">{String(index + 1).padStart(2, "0")}</span><div><h3>{detail.title}</h3><p>{detail.text}</p></div></div>)}</div>
      </div>
    </section>

    <section className="hospitality-meal-enquiry" aria-labelledby="meal-enquiry-title">
      <div className="hospitality-shell hospitality-meal-enquiry-grid">
        <Reveal><figure><div className="hospitality-photo"><Image src="/images/room-tea.webp" alt="A kettle, tea and coffee supplies photographed in a guest room at Hotel Augusto" fill sizes="(max-width: 760px) 80vw, 35vw" quality={85} /></div><figcaption>A tea and coffee setup in a guest room.</figcaption></figure></Reveal>
        <Reveal><p className="hospitality-context">Let’s talk about your stay</p><h2 id="meal-enquiry-title">Your dates.<br />Your meal plans.</h2><p>Share when you’re visiting and what you’d like to know. The hotel can confirm the current menu, service hours and meal inclusions before you book.</p><a href={whatsapp} target="_blank" rel="noopener noreferrer" className="hospitality-solid-link" style={{ color: "var(--paper)" }}><WhatsAppIcon size={20} /> Ask about dining <ArrowUpRight size={18} aria-hidden="true" /></a><Link href="/contact#enquire" className="hospitality-link">Or plan your whole stay <ArrowUpRight size={18} aria-hidden="true" /></Link></Reveal>
      </div>
    </section>

    <nav className="hospitality-shell hospitality-related" aria-label="More at Hotel Augusto">
      <Link href="/hotel"><span>The hotel</span><strong>Get to know Augusto.</strong><ArrowUpRight size={25} aria-hidden="true" /></Link>
      <Link href="/rooms"><span>Your stay</span><strong>Find your room.</strong><ArrowUpRight size={25} aria-hidden="true" /></Link>
    </nav>
  </main>;
}
