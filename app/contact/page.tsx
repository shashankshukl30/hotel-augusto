import type { Metadata } from "next";
import Image from "next/image";
import { ChevronDown, Phone } from "lucide-react";
import { BookingForm } from "@/components/booking-form";
import { Reveal } from "@/components/reveal";
import { WhatsAppIcon } from "@/components/whatsapp-icon";
import { ArrivalGuide } from "@/components/arrival-guide";
import { faqs, hotel } from "@/content/hotel";
import "./contact.css";

export const metadata: Metadata = {
  title: "Contact Hotel Augusto Varanasi | Plan Your Kashi Stay",
  description:
    "Speak with Hotel Augusto about your Varanasi stay. Find our Godowlia address, call the hotel or send your travel dates and room enquiry on WhatsApp.",
};

export default function ContactPage() {
  const whatsappUrl = `https://wa.me/${hotel.whatsappNumber}?text=${encodeURIComponent(hotel.bookingMessage)}`;

  return (
    <main id="main" className="contact-page">
      <section className="container contact-intro">
        <Reveal>
          <p className="contact-context">Hotel Augusto, Varanasi</p>
          <h1>Your stay.<br/><em>Let’s make it yours.</em></h1>
          <p className="contact-intro-copy">
            A few nights in Kashi. A visit with the family. Get in touch
            for room availability, rates and a little help with your journey.
          </p>
          <div className="contact-actions">
            <a className="button contact-whatsapp" href={whatsappUrl} target="_blank"
              rel="noopener noreferrer" style={{ color: "var(--paper)" }}>
              <WhatsAppIcon size={19} /> Chat on WhatsApp
            </a>
            <a className="contact-call" href={hotel.phoneHref}>
              <Phone size={18} aria-hidden="true" /> {hotel.phone}
            </a>
          </div>
          <a className="contact-enquiry-jump" href="#enquire">
            Or start with your travel dates <ChevronDown size={16} aria-hidden="true" />
          </a>
        </Reveal>
        <Reveal className="contact-intro-photo"><Image src="/images/google-double-room.webp" alt="A double-bed guest room at Hotel Augusto" fill preload sizes="(max-width:760px) 90vw, 42vw" quality={85}/><span>Your room in Godowlia, Varanasi.</span></Reveal>
      </section>

      <section className="container contact-enquiry" id="enquire" aria-labelledby="enquiry-title">
        <div className="contact-enquiry-content">
          <Reveal className="contact-section-heading">
            <h2 id="enquiry-title">Your stay starts here.</h2>
            <p>Choose your dates and room. We’ll prepare a message for you to
              review and send to the hotel on WhatsApp.</p>
          </Reveal>
          <div className="contact-form-panel"><BookingForm /></div>
        </div>
      </section>

      <ArrivalGuide/>
      <section className="container contact-faq" aria-labelledby="faq-title">
        <div className="contact-faq-content">
          <Reveal className="contact-section-heading">
            <h2 id="faq-title">Good to know.</h2>
            <p>A few helpful answers before you arrive.</p>
          </Reveal>
          <div className="contact-faq-list">
            {faqs.map((faq) => (
              <details key={faq.question} name="hotel-questions" className="contact-faq-item">
                <summary>
                  <span>{faq.question}</span>
                  <ChevronDown className="contact-faq-marker" size={22} strokeWidth={1.7} aria-hidden="true" />
                </summary>
                <div className="contact-faq-answer"><p>{faq.answer}</p></div>
              </details>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
