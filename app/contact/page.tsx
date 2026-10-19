import type { Metadata } from "next";
import Image from "next/image";
import { ArrowUpRight, ChevronDown, MapPin, Phone } from "lucide-react";
import { BookingForm } from "@/components/booking-form";
import { Reveal } from "@/components/reveal";
import { WhatsAppIcon } from "@/components/whatsapp-icon";
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
          <h1>Let’s plan your stay.</h1>
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

      <section className="container contact-arrival" aria-labelledby="find-us">
        <Reveal>
          <div className="contact-location-grid">
            <figure className="contact-exterior">
              <div className="contact-exterior-image">
                <Image src="/images/hotel-exterior.webp"
                  alt="The illuminated Hotel Augusto entrance and sign on August Kunda Road in Varanasi"
                  fill sizes="(max-width: 760px) 90vw, 45vw" />
              </div>
              <figcaption>The hotel entrance on August Kunda Road.</figcaption>
            </figure>
            <div className="contact-address-panel">
              <MapPin size={28} strokeWidth={1.6} aria-hidden="true" />
              <h2 id="find-us">Find us in Godowlia.</h2>
              <address>
                <strong>{hotel.name}</strong>
                {hotel.address.map((line) => <span key={line}>{line}</span>)}
              </address>
              <p className="contact-landmark">Opposite State Bank of India</p>
              <a className="contact-directions" href={hotel.mapsUrl} target="_blank" rel="noopener noreferrer">
                Get directions <ArrowUpRight size={17} aria-hidden="true" />
              </a>
              <div className="contact-arrival-note">
                <h3>Arriving by car or taxi?</h3>
                <p>Call ahead for current approach, drop-off and parking guidance.
                  Share your arrival time so the hotel can help you plan the last part of your journey.</p>
              </div>
            </div>
          </div>
        </Reveal>
      </section>

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
