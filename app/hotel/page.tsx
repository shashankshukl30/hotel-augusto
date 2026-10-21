import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { ArrowDown, ArrowUpRight, ChevronRight, Plus } from "lucide-react";
import { Reveal } from "@/components/reveal";
import { ArrivalGuide } from "@/components/arrival-guide";
import { hotel } from "@/content/hotel";
import { services } from "@/content/hospitality";
import "../hospitality-pages.css";

export const metadata: Metadata = {
  alternates: { canonical: "/hotel" },
  title: "Hotel Augusto, Varanasi | Our Hotel & Guest Facilities",
  description: "Step inside Hotel Augusto in Godowlia. Discover the rooms, vegetarian restaurant, reception, luggage support and practical facilities for your Varanasi stay.",
};

const serviceGroups = ["In your room", "At the hotel", "During your stay"] as const;

export default function HotelPage() {
  return (
    <main id="main" className="hospitality-page hotel-page">
      <div className="hospitality-shell">
        <nav className="hospitality-breadcrumb" aria-label="Breadcrumb">
          <Link href="/">Home</Link><ChevronRight size={13} aria-hidden="true" /><span aria-current="page">The hotel</span>
        </nav>
        <section className="hospitality-hotel-hero" aria-labelledby="hotel-title">
          <Reveal className="hospitality-hotel-title">
            <div>
              <p className="hospitality-context">The hotel</p>
              <h1 id="hotel-title">Welcome to<br />Hotel Augusto.</h1>
            </div>
            <div className="hospitality-hero-summary">
              <p>Air-conditioned rooms. Vegetarian dining. A Godowlia address within walking distance of Shri Kashi Vishwanath Temple and Dashashwamedh Ghat.</p>
              <Link href="/rooms" className="hospitality-solid-link" style={{ color: "var(--paper)" }}>Explore rooms <ArrowUpRight size={18} aria-hidden="true" /></Link>
              <a href="#inside" className="hospitality-scroll-link"><ArrowDown size={17} aria-hidden="true" /> Take a closer look</a>
            </div>
          </Reveal>
          <Reveal delay={0.1} className="hospitality-hotel-exterior">
            <figure>
              <div className="hospitality-photo hospitality-exterior-frame">
                <Image src="/images/hotel-exterior-day.webp" alt="Hotel Augusto’s street entrance and sign on August Kunda Road, Varanasi" fill preload sizes="(max-width: 760px) 100vw, 90vw" quality={85} />
              </div>
              <figcaption>The entrance on August Kunda Road.</figcaption>
            </figure>
          </Reveal>
        </section>
        <dl className="hospitality-stay-facts">
          <div><dt>Location</dt><dd>Godowlia, Varanasi</dd></div>
          <div><dt>Rooms</dt><dd>Three room categories</dd></div>
          <div><dt>Dining</dt><dd>Vegetarian restaurant</dd></div>
          <div><dt>Reception</dt><dd>Available 24 hours</dd></div>
        </dl>
      </div>
      <section className="hospitality-shell hospitality-welcome" id="inside" aria-labelledby="welcome-title">
        <div className="hospitality-welcome-heading">
          <Reveal><p className="hospitality-context">Inside Augusto</p><h2 id="welcome-title">Get to know<br />your hotel.</h2></Reveal>
          <Reveal delay={0.1}><p>Begin at reception, settle into your room, then make the day your own. Augusto brings together air-conditioned rooms, vegetarian dining and the practical help of a hotel in the old city.</p><p>From a room with separate beds to a question about your arrival, tell the team what matters to your stay. They can confirm the details before you travel.</p></Reveal>
        </div>
        <div className="hospitality-welcome-photos">
          <Reveal><figure><div className="hospitality-photo hospitality-lobby-frame"><Image src="/images/hotel-lobby.webp" alt="Hotel Augusto’s lobby with guest seating, reception and the lift entrance" fill sizes="(max-width: 760px) 100vw, 45vw" quality={85} /></div><figcaption>Guest seating in the lobby.</figcaption></figure></Reveal>
          <Reveal delay={0.14}><figure><div className="hospitality-photo hospitality-reception-frame"><Image src="/images/hotel-reception.webp" alt="The reception counter and seating at Hotel Augusto" fill sizes="(max-width: 760px) 100vw, 45vw" quality={85} /></div><figcaption>The reception desk.</figcaption></figure></Reveal>
        </div>
      </section>
      <section className="hospitality-services" aria-labelledby="services-title">
        <div className="hospitality-shell">
          <div className="hospitality-services-heading">
            <Reveal><p className="hospitality-context">Facilities</p><h2 id="services-title">The details<br />of your stay.</h2></Reveal>
            <p>A comfortable room is the beginning. Explore the facilities, and ask the hotel about the arrangements that matter to you.</p>
          </div>
          <div className="hospitality-service-groups">
            {serviceGroups.map((group) => (
              <div className="hospitality-service-group" key={group}>
                <h3>{group}</h3>
                <div>{services.filter((service) => service.category === group).map((service) => (
                  <details className="hospitality-service-detail" key={service.id}>
                    <summary>{service.title}<Plus size={18} aria-hidden="true" /></summary>
                    <p>{service.description}</p>
                  </details>
                ))}</div>
              </div>
            ))}
          </div>
          <p className="hospitality-services-note">For accessibility needs, meal inclusions or services with additional charges, confirm the details with the hotel before booking.</p>
        </div>
      </section>
      <div className="hospitality-shell"><ArrivalGuide /></div>
      <section className="hospitality-shell hospitality-next-stays" aria-label="Continue planning your stay">
        <Link href="/rooms" className="hospitality-next-story">
          <div className="hospitality-photo"><Image src="/images/twin-room.webp" alt="Two separate beds in a Deluxe Twin Room at Hotel Augusto" fill sizes="(max-width: 760px) 100vw, 45vw" /></div>
          <div><h2>Find your room.</h2><span className="hospitality-link">Explore three room categories <ArrowUpRight size={20} aria-hidden="true" /></span></div>
        </Link>
        <Link href="/dining" className="hospitality-next-story">
          <div className="hospitality-photo"><Image src="/images/google-dining-room.webp" alt="The tables and serving area in Hotel Augusto’s restaurant" fill sizes="(max-width: 760px) 100vw, 45vw" /></div>
          <div><h2>Dining at Augusto.</h2><span className="hospitality-link">Explore the restaurant <ArrowUpRight size={20} aria-hidden="true" /></span></div>
        </Link>
      </section>
      <div className="hospitality-shell hospitality-booking-line"><p>Bring your plans. We’ll talk through the details.</p><a href={hotel.phoneHref} className="hospitality-link">Call {hotel.phone} <ArrowUpRight size={18} aria-hidden="true" /></a></div>
    </main>
  );
}
