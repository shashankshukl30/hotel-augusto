import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { ArrowDown, ArrowUpRight, ChevronRight } from "lucide-react";
import { Reveal } from "@/components/reveal";
import { hotel } from "@/content/hotel";
import "../hospitality-pages.css";

export const metadata: Metadata = {
  title: "Hotel Augusto, Varanasi | Our Hotel & Guest Facilities",
  description: "Get to know Hotel Augusto in Godowlia, Varanasi. Explore the hotel, guest facilities, vegetarian dining and our location near the temples and ghats.",
};

export default function HotelPage() {
  return <main id="main" className="hospitality-page hotel-page">
    <div className="hospitality-shell">
      <nav className="hospitality-breadcrumb" aria-label="Breadcrumb">
        <Link href="/">Home</Link><ChevronRight size={13} aria-hidden="true" /><span aria-current="page">The hotel</span>
      </nav>
      <section className="hospitality-hotel-hero" aria-labelledby="hotel-title">
        <Reveal className="hospitality-hotel-title">
          <p className="hospitality-context">August Kunda Road · Godowlia</p>
          <h1 id="hotel-title">Get to know<br />Augusto.</h1>
        </Reveal>
        <figure className="hospitality-hotel-exterior">
          <div className="hospitality-photo hospitality-exterior-frame">
            <Image src="/images/hotel-exterior-day.webp" alt="Hotel Augusto's street entrance and sign on August Kunda Road, Varanasi" fill preload sizes="(max-width: 760px) 750px, 90vw" quality={85} />
          </div>
          <figcaption><span>The hotel, from the street.</span><span>Varanasi, India</span></figcaption>
        </figure>
        <Reveal delay={0.1} className="hospitality-hotel-intro">
          <p>A stay in Godowlia, within walking distance of Shri Kashi Vishwanath Temple and Dashashwamedh Ghat. Come for the city. Make Augusto your base.</p>
          <Link href="/rooms" className="hospitality-link">Find your room <ArrowUpRight size={19} aria-hidden="true" /></Link>
          <a href="#inside" className="hospitality-scroll-link"><ArrowDown size={17} aria-hidden="true" /> Step inside</a>
        </Reveal>
      </section>
    </div>

    <section className="hospitality-shell hospitality-welcome" id="inside" aria-labelledby="welcome-title">
      <div className="hospitality-welcome-heading">
        <Reveal><p className="hospitality-context">Your arrival</p><h2 id="welcome-title">From the street<br />to your stay.</h2></Reveal>
        <Reveal delay={0.1}><p>Start at reception, leave your bags and get your bearings. With a 24-hour front desk, room service and housekeeping, the everyday details of your stay have a place to begin.</p><p>Arriving early or late? Share your travel plans so the hotel can confirm check-in arrangements before you set out.</p></Reveal>
      </div>
      <div className="hospitality-welcome-photos">
        <Reveal><figure><div className="hospitality-photo hospitality-lobby-frame"><Image src="/images/hotel-lobby.webp" alt="Hotel Augusto's lobby with seating, reception desk and lift entrance" fill sizes="(max-width: 760px) 100vw, 65vw" quality={85} /></div><figcaption>The lobby and seating area.</figcaption></figure></Reveal>
        <Reveal delay={0.12} className="hospitality-reception-photo"><figure><div className="hospitality-photo hospitality-reception-frame"><Image src="/images/hotel-reception.webp" alt="The reception counter and guest seating at Hotel Augusto" fill sizes="(max-width: 760px) 80vw, 40vw" quality={85} /></div><figcaption>Reception, at the heart of the hotel.</figcaption></figure></Reveal>
      </div>
    </section>

    <section className="hospitality-essentials" aria-labelledby="essentials-title">
      <div className="hospitality-shell hospitality-essentials-grid">
        <Reveal><p className="hospitality-context">The essentials</p><h2 id="essentials-title">Good to<br />come back to.</h2><p>Practical comforts for the time between temple visits, walks through the lanes and evenings by the river.</p></Reveal>
        <ul className="hospitality-amenity-list">
          {hotel.amenities.map((amenity, index) => <li key={amenity}><span aria-hidden="true">{String(index + 1).padStart(2, "0")}</span>{amenity}</li>)}
        </ul>
      </div>
    </section>

    <section className="hospitality-shell hospitality-location" aria-labelledby="location-title">
      <Reveal className="hospitality-location-heading"><p className="hospitality-context">Our neighbourhood</p><h2 id="location-title">A Godowlia<br />address.</h2><Link href="/varanasi" className="hospitality-link">Explore Varanasi <ArrowUpRight size={19} aria-hidden="true" /></Link></Reveal>
      <div className="hospitality-location-details">
        <address><strong>{hotel.name}</strong>{hotel.address.map(line => <span key={line}>{line}</span>)}</address>
        <p className="hospitality-landmark">Opposite State Bank of India</p>
        <a href={hotel.mapsUrl} target="_blank" rel="noopener noreferrer" className="hospitality-link">Open Google Maps <ArrowUpRight size={18} aria-hidden="true" /></a>
        <div className="hospitality-arrival-detail"><h3>Before the last turn.</h3><p>Travelling by car or taxi? Call the hotel for current approach, drop-off and parking guidance in Godowlia. Share any accessibility needs before you travel.</p><a href={hotel.phoneHref} className="hospitality-phone">{hotel.phone}</a></div>
      </div>
    </section>

    <section className="hospitality-shell hospitality-hotel-close" aria-label="Continue exploring Hotel Augusto">
      <Link href="/dining" className="hospitality-next-feature">
        <div className="hospitality-photo"><Image src="/images/dining-room.webp" alt="Tables and chairs in Hotel Augusto's vegetarian restaurant" fill sizes="(max-width: 760px) 100vw, 45vw" /></div>
        <div><span className="hospitality-context">Also at Augusto</span><h2>Stay for<br />a meal.</h2><span className="hospitality-link">Discover dining <ArrowUpRight size={20} aria-hidden="true" /></span></div>
      </Link>
      <div className="hospitality-booking-line"><p>Have your dates in mind?</p><Link href="/contact#enquire" className="hospitality-solid-link" style={{ color: "var(--paper)" }}>Plan your stay <ArrowUpRight size={18} aria-hidden="true" /></Link></div>
    </section>
  </main>;
}
