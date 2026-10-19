import type { Metadata } from "next";
import Image from "next/image";
import { ArrowUpRight, MapPin, Phone } from "lucide-react";
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
      <section className="container page-intro contact-intro">
        <div className="contact-intro-grid">
          <Reveal>
            <span className="eyebrow">A conversation before the journey</span>
            <h1>Your next chapter starts <em>here.</em></h1>
          </Reveal>
          <Reveal delay={0.12} className="contact-intro-note">
            <p>
              A room for a few nights. A family visit to Kashi. Tell us what
              brings you to Varanasi, and let’s plan your stay.
            </p>
            <a className="text-link" href="#enquire">
              Make a stay enquiry <ArrowUpRight size={17} aria-hidden="true" />
            </a>
          </Reveal>
        </div>
        <div className="contact-direct">
          <div>
            <span className="eyebrow">Call the hotel</span>
            <a className="contact-phone" href={hotel.phoneHref}>
              {hotel.phone} <Phone size={18} aria-hidden="true" />
            </a>
          </div>
          <a
            className="button contact-whatsapp"
            href={whatsappUrl}
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: "var(--paper)" }}
          >
            <WhatsAppIcon size={20} /> Chat on WhatsApp
            <ArrowUpRight size={16} aria-hidden="true" />
          </a>
        </div>
      </section>

      <section className="container contact-arrival" aria-labelledby="find-us">
        <Reveal>
          <div className="contact-wayfinding">
            <div className="contact-address-panel">
              <div className="contact-address-top">
                <span className="eyebrow">Find your way to us</span>
                <MapPin size={24} strokeWidth={1.2} aria-hidden="true" />
              </div>
              <h2 className="display" id="find-us">In the heart<br />of <em>Godowlia.</em></h2>
              <address>
                <strong>{hotel.name}</strong>
                {hotel.address.map((line) => <span key={line}>{line}</span>)}
              </address>
              <p className="contact-landmark">Opposite State Bank of India</p>
              <a
                className="text-link"
                href={hotel.mapsUrl}
                target="_blank"
                rel="noopener noreferrer"
              >
                Open in Google Maps <ArrowUpRight size={17} aria-hidden="true" />
              </a>
            </div>
            <figure className="contact-exterior">
              <div className="contact-exterior-image">
                <Image
                  src="/images/hotel-exterior.webp"
                  alt="The illuminated Hotel Augusto entrance and sign in Godowlia, Varanasi"
                  fill
                  sizes="(max-width: 760px) 100vw, 55vw"
                />
              </div>
              <figcaption>Look for Hotel Augusto on August Kunda Road.</figcaption>
            </figure>
          </div>
        </Reveal>
        <div className="contact-arrival-note">
          <span className="eyebrow">Before you set out</span>
          <p>
            Arriving by car or taxi? Call ahead for current approach, drop-off
            and parking guidance. Share your arrival time so the hotel can help
            you plan the last part of your journey.
          </p>
        </div>
      </section>

      <section className="contact-enquiry section-space" id="enquire" aria-labelledby="enquiry-title">
        <div className="container contact-enquiry-grid">
          <Reveal className="contact-enquiry-intro">
            <span className="eyebrow">Let’s make a plan</span>
            <h2 className="display" id="enquiry-title">When shall we<br /><em>expect you?</em></h2>
            <p>
              Share a few details about your trip. We’ll prepare a message for
              you to send to the hotel on WhatsApp.
            </p>
            <p className="contact-enquiry-note">
              Your stay is confirmed once the hotel has agreed availability,
              the rate and booking terms with you.
            </p>
          </Reveal>
          <div className="contact-form-panel">
            <BookingForm />
          </div>
        </div>
      </section>

      <section className="container section-space contact-faq" aria-labelledby="faq-title">
        <Reveal className="contact-faq-heading">
          <span className="eyebrow">A few helpful answers</span>
          <h2 className="display" id="faq-title">Before your <em>stay.</em></h2>
        </Reveal>
        <div className="contact-faq-list">
          {faqs.map((faq, index) => (
            <details key={faq.question} name="hotel-questions" className="contact-faq-item">
              <summary>
                <span className="contact-faq-index" aria-hidden="true">{String(index + 1).padStart(2, "0")}</span>
                <span>{faq.question}</span>
                <span className="contact-faq-marker" aria-hidden="true" />
              </summary>
              <div className="contact-faq-answer"><p>{faq.answer}</p></div>
            </details>
          ))}
        </div>
      </section>
    </main>
  );
}
