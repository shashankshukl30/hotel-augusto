import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { ArrowDownToLine, ArrowUpRight, ChevronRight, FileText, Plus } from "lucide-react";
import { Reveal } from "@/components/reveal";
import { DiningEnquiry } from "@/components/dining-enquiry";
import { WhatsAppIcon } from "@/components/whatsapp-icon";
import { hotel } from "@/content/hotel";
import { practicalFaqs } from "@/content/hospitality";
import "../hospitality-pages.css";

export const metadata: Metadata = {
  alternates: { canonical: "/dining" },
  title: "Vegetarian Dining at Hotel Augusto | Varanasi Hotel",
  description: "A table at Hotel Augusto, Varanasi. Explore the vegetarian restaurant and room service, then ask about the menu, breakfast inclusions and your meal plans.",
};

const diningEnquiries = [
  { title: "See what’s on the menu", detail: "Ask for the current dishes, prices and restaurant serving times.", action: "Ask for the menu", message: "Hello Hotel Augusto, could you share the current vegetarian restaurant menu, prices and serving times? I am planning a stay." },
  { title: "Plan your breakfast", detail: "Check meal inclusions and serving times around your travel plans.", action: "Ask about breakfast", message: "Hello Hotel Augusto, I would like to check breakfast serving times and whether breakfast is included in the room plan for my stay. I can share my dates and guest details." },
  { title: "Prefer a meal in your room?", detail: "Find out what is available through room service and any charges.", action: "Ask about room service", message: "Hello Hotel Augusto, could you share the current room-service menu, availability and any applicable charges for my stay?" },
];

export default function DiningPage() {
  return (
    <main id="main" className="hospitality-page dining-page">
      <div className="hospitality-shell">
        <nav className="hospitality-breadcrumb" aria-label="Breadcrumb"><Link href="/">Home</Link><ChevronRight size={13} aria-hidden="true" /><span aria-current="page">Dining</span></nav>
        <section className="hospitality-dining-hero" aria-labelledby="dining-title">
          <Reveal className="hospitality-dining-hero-copy"><p className="hospitality-context">Dining at the hotel</p><h1 id="dining-title">Vegetarian dining.<br />Right here.</h1><p>Enjoy a meal at Hotel Augusto’s restaurant, or ask about room service. Plan your meals along with your stay.</p><a href="#dining-enquiries" className="hospitality-solid-link" style={{ color: "var(--paper)" }}>Plan your meals <ArrowUpRight size={19} aria-hidden="true" /></a></Reveal>
          <Reveal delay={0.12}><figure><div className="hospitality-photo hospitality-dining-hero-photo"><Image src="/images/dining-room-wide.webp" alt="The restaurant at Hotel Augusto, with tables arranged for guests" fill preload sizes="(max-width: 760px) 100vw, 62vw" quality={85} /></div><figcaption>Inside the restaurant at Hotel Augusto.</figcaption></figure></Reveal>
        </section>
        <div className="hospitality-dining-facts"><span>On-site restaurant</span><span>Vegetarian dining</span><span>Room service</span></div>
      </div>
      <section className="hospitality-shell hospitality-dining-introduction" aria-labelledby="dining-intro-title">
        <Reveal><p className="hospitality-context">Around your day</p><h2 id="dining-intro-title">Your meals.<br />Your plans.</h2></Reveal>
        <Reveal delay={0.1}><p>Some days begin with the temple. Others lead straight to the river. In between, the restaurant gives you a place to sit down for a vegetarian meal without heading back out.</p><p>Travelling together? Bring your meal plans into the conversation when you enquire about your room. The hotel can confirm the current menu, serving times and what your stay includes.</p></Reveal>
      </section>
      <section className="hospitality-dining-service" aria-labelledby="dining-service-title">
        <div className="hospitality-shell hospitality-dining-service-grid">
          <Reveal><figure><div className="hospitality-photo hospitality-dining-detail-photo"><Image src="/images/google-dining-room.webp" alt="Marble-topped tables and the serving counter in Hotel Augusto’s vegetarian restaurant" fill sizes="(max-width: 760px) 100vw, 55vw" quality={85} /></div><figcaption>A closer look at the hotel’s dining room.</figcaption></figure></Reveal>
          <Reveal delay={0.1} className="hospitality-dining-service-copy"><p className="hospitality-context">Two ways to dine</p><h2 id="dining-service-title">Restaurant.<br />Room service.</h2><div className="hospitality-dining-service-row"><h3>The restaurant</h3><p>Vegetarian dining is available on site. Ask the team about the current menu and share any dietary requirements before you order.</p></div><div className="hospitality-dining-service-row"><h3>Room service</h3><p>A meal in your room is another option. Confirm what can be ordered, service availability and any charges with the hotel.</p></div></Reveal>
        </div>
      </section>
      <section className="hospitality-shell hospitality-dining-enquiries" id="dining-enquiries" aria-labelledby="meal-enquiry-title">
        <Reveal className="hospitality-dining-enquiry-heading">
          <p className="hospitality-context">Ask the hotel</p><h2 id="meal-enquiry-title">Let’s plan<br />your meals.</h2>
          <p>Share your date, party size and meal plans. Send an email enquiry to the hotel, or continue on WhatsApp.</p>
          <a className="hospitality-dining-download" href="/downloads/hotel-augusto-dining-guide.pdf" download><FileText size={24} aria-hidden="true" /><span><strong>Your dining planning guide</strong><small>Download PDF · one page</small></span><ArrowDownToLine size={20} aria-hidden="true" /></a>
          <details className="hospitality-dining-quick"><summary>Just have a quick question?<Plus size={18} aria-hidden="true" /></summary><div className="hospitality-dining-enquiry-list">
            {diningEnquiries.map((item) => <div className="hospitality-dining-enquiry" key={item.title}><h3>{item.title}</h3><p>{item.detail}</p><a href={"https://wa.me/" + hotel.whatsappNumber + "?text=" + encodeURIComponent(item.message)} target="_blank" rel="noopener noreferrer" className="hospitality-link"><WhatsAppIcon size={17} />{item.action}<ArrowUpRight size={17} aria-hidden="true" /></a></div>)}
          </div></details>
        </Reveal>
        <DiningEnquiry />
      </section>
      <section className="hospitality-shell hospitality-dining-questions" aria-labelledby="dining-questions-title">
        <h2 id="dining-questions-title">Dining questions.</h2>
        <div>{practicalFaqs.filter((faq) => faq.topic === "Dining").map((faq) => <details className="hospitality-service-detail" key={faq.question}><summary>{faq.question}<Plus size={18} aria-hidden="true" /></summary><p>{faq.answer}</p></details>)}</div>
      </section>
      <nav className="hospitality-shell hospitality-related" aria-label="More at Hotel Augusto">
        <Link href="/hotel"><span>The hotel</span><strong>Get to know Augusto.</strong><ArrowUpRight size={25} aria-hidden="true" /></Link>
        <Link href="/contact#enquire"><span>Bring it all together</span><strong>Plan your whole stay.</strong><ArrowUpRight size={25} aria-hidden="true" /></Link>
      </nav>
    </main>
  );
}
