import type { Metadata } from "next";
import Link from "next/link";
import { ArrowUpRight, BedDouble, BellRing, ChevronRight, Coffee, ConciergeBell, Mail, MapPin, Phone, Plus, Snowflake, Utensils, Wifi } from "lucide-react";
import { HomeHero } from "@/components/home-hero";
import { KineticText } from "@/components/kinetic-text";
import { HomeGallery } from "@/components/home-gallery";
import { StayBar } from "@/components/stay-bar";
import { Reveal } from "@/components/reveal";
import { ScrollPhoto } from "@/components/scroll-photo";
import { CityItinerary } from "@/components/city-itinerary";
import { ArrivalGuide } from "@/components/arrival-guide";
import { WhatsAppIcon } from "@/components/whatsapp-icon";
import { RoomPhotoLink } from "@/components/room-photo-link";
import { hotel, rooms } from "@/content/hotel";
import { guestReviewHighlight, practicalFaqs, reviewSources } from "@/content/hospitality";
import { googleReviewSnapshot, proximityHighlights } from "@/content/social-proof";
import "./home.css";

export const metadata: Metadata = {
  alternates: { canonical: "/" },
};

const essentials = [
  {icon:Snowflake,label:"Air-conditioned rooms"},{icon:Wifi,label:"Wi-Fi"},
  {icon:Utensils,label:"Vegetarian dining"},{icon:ConciergeBell,label:"24-hour reception"},
  {icon:Coffee,label:"Room service"},{icon:BellRing,label:"Housekeeping"},
];

export default function Home() {
  const whatsapp = `https://wa.me/${hotel.whatsappNumber}?text=${encodeURIComponent(hotel.bookingMessage)}`;
  return <main id="main">
    <HomeHero/>
    <div className="home-reservation home-location-band container"><span><MapPin size={16}/> Godowlia, Varanasi</span><span>Walk to the temple and ghats.</span><a href={hotel.mapsUrl} target="_blank" rel="noopener noreferrer">Get directions <ArrowUpRight size={16}/></a></div>

    <section id="discover" className="home-welcome container section-space">
      <Reveal className="home-welcome-copy"><p className="eyebrow">Meet Augusto.</p><h2><KineticText text="The city at your doorstep."/><br/><span className="heading-secondary"><KineticText text="A place to come back to." delay={.12}/></span></h2><div className="home-welcome-detail"><p>Stay in Godowlia, within walking distance of Shri Kashi Vishwanath Temple and Dashashwamedh Ghat. Come back to an air-conditioned room, a vegetarian meal and a team available at reception around the clock.</p><Link href="/hotel" className="text-link">Explore the hotel <ChevronRight size={19}/></Link></div></Reveal>
      <ScrollPhoto className="welcome-photo-main" src="/images/hotel-lounge.webp" alt="The lounge and seating area inside Hotel Augusto" sizes="(max-width:600px) 90vw, 85vw"/>
      <div className="home-amenities" aria-label="Hotel essentials">{essentials.map(({icon:Icon,label}) => <span key={label}><Icon strokeWidth={1.5}/>{label}</span>)}</div>
    </section>

    <section className="home-rooms section-space" id="rooms" aria-labelledby="home-rooms-title"><div className="container">
      <Reveal className="home-section-heading"><div><p className="eyebrow">Rooms at Augusto.</p><h2 id="home-rooms-title"><KineticText text="Find your room."/></h2></div><Link href="/rooms/compare" className="text-link">Compare rooms <ChevronRight size={19}/></Link></Reveal>
      <div className="home-room-collection">{rooms.map(room => <article className="home-room-card" key={room.slug}>
        <RoomPhotoLink slug={room.slug} name={room.name} image={room.image} alt={room.alt} className="home-room-main" sizes="(max-width:600px) 85vw, (max-width:1000px) 43vw, 30vw"/>
        <div className="home-room-copy"><h3>{room.name}</h3><p className="home-room-bed"><BedDouble size={18} strokeWidth={1.5}/>{room.bedLabel}</p><p>{room.description}</p><div className="home-room-actions"><Link href={`/rooms/${room.slug}`} className="button" style={{color:"var(--paper)"}}>Explore room</Link><Link href={`/contact?room=${room.slug}#enquire`} className="text-link">Enquire <ChevronRight size={17}/></Link></div></div>
      </article>)}</div>
      <p className="room-compare-note">Three room choices. Tell us your dates and who’s travelling — we’ll help you choose.</p>
    </div></section>

    <section className="home-dining section-space"><div className="container"><Reveal className="home-section-heading"><div><p className="eyebrow">Dining.</p><h2><KineticText text="Take a seat."/><br/><span className="heading-secondary"><KineticText text="Take your time." delay={.1}/></span></h2></div><div className="home-heading-detail"><p>Vegetarian meals in the restaurant.<br/>Room service when you’d rather stay in.</p><Link href="/dining" className="text-link">Explore dining <ChevronRight size={19}/></Link></div></Reveal><ScrollPhoto className="home-dining-photo" src="/images/google-dining-room.webp" alt="Marble-topped tables and seating in Hotel Augusto's vegetarian restaurant" sizes="(max-width:600px) 90vw, 85vw"/><p className="home-dining-caption">The restaurant at Hotel Augusto. Ask us about the current menu and serving times.</p></div></section>

    <CityItinerary compact/>

    <section className="home-gallery container section-space"><Reveal className="home-section-heading"><div><p className="eyebrow">See for yourself.</p><h2><KineticText text="Inside Augusto."/></h2></div><Link href="/gallery" className="text-link">Open the gallery <ChevronRight size={19}/></Link></Reveal><HomeGallery/></section>

    <section className="home-reviews"><div className="container"><Reveal className="review-heading"><div><p className="eyebrow">Guest experiences.</p><h2><KineticText text="See it through"/><br/><KineticText text="their eyes." delay={.1}/></h2></div><p>Independent reviews. Real guest photographs. Get a fuller picture before your stay.</p></Reveal><div className="review-evidence"><a className="google-review-badge" href={googleReviewSnapshot.href} target="_blank" rel="noopener noreferrer" aria-label={`${googleReviewSnapshot.countLabel}, ${googleReviewSnapshot.scoreLabel}. ${googleReviewSnapshot.dateLabel}. Read on Google.`}><span className="review-platform">On Google <ArrowUpRight size={18}/></span><span className="review-score">{googleReviewSnapshot.score}<small> / {googleReviewSnapshot.scale}</small></span><span>{googleReviewSnapshot.countLabel}</span><small>{googleReviewSnapshot.dateLabel}</small></a><div className="guest-review-highlight"><blockquote cite={guestReviewHighlight.href}>“{guestReviewHighlight.quote}”</blockquote><a href={guestReviewHighlight.href} target="_blank" rel="noopener noreferrer">{guestReviewHighlight.attribution}<ArrowUpRight size={16}/></a></div></div><div className="review-source-links">{reviewSources.slice(0,2).map(source => <a key={source.name} href={source.href} target="_blank" rel="noopener noreferrer"><div><strong>{source.name}</strong><small>{source.name === "Google" ? "Explore guest reviews and photographs." : source.description}</small></div><ArrowUpRight size={22}/></a>)}</div></div></section>

    <section className="home-neighbourhood container section-space"><Reveal className="home-section-heading"><div><p className="eyebrow">Step outside.</p><h2><KineticText text="Kashi starts"/><br/><KineticText text="at your doorstep." delay={.1}/></h2></div><p className="neighbourhood-intro">Stay in Godowlia, with the old city’s temples and riverfront within walking distance.</p></Reveal><div className="neighbourhood-routes">{proximityHighlights.map((place,index)=><a href={place.href} key={place.id} target="_blank" rel="noopener noreferrer"><span className="route-number">0{index+1}</span><div><small>{place.label}</small><h3>{place.name}</h3><p>{place.description}</p></div><span className="route-action">{place.action}<ArrowUpRight size={21}/></span></a>)}</div></section>

    <ArrivalGuide className="container"/>

    <section className="home-practical"><div className="container home-practical-grid"><Reveal className="home-practical-intro"><p className="eyebrow">Good to know.</p><h2><KineticText text="A few details."/><br/><span className="heading-secondary"><KineticText text="Before you arrive." delay={.1}/></span></h2><Link href="/contact#faq-title" className="text-link">More questions? <ChevronRight size={19}/></Link></Reveal><div className="home-faq">{practicalFaqs.filter(faq => ["Can I walk to the temple and the ghats?","Which bed arrangements can I choose?","Is breakfast included?","Can I arrive early or leave late?","What should I confirm before booking?"].includes(faq.question)).map(faq => <details key={faq.question} name="home-questions"><summary>{faq.question}<Plus size={20}/></summary><p>{faq.answer}</p></details>)}</div></div></section>

    <section className="home-guides container section-space"><Reveal className="home-section-heading"><div><p className="eyebrow">Your stay guide.</p><h2><KineticText text="A little local knowledge."/></h2></div><Link href="/guides" className="text-link">All guides <ChevronRight size={19}/></Link></Reveal><div className="home-guide-links"><Link href="/guides/first-visit-to-kashi"><span>Explore</span><h3>Your first visit to Kashi.</h3><p>Plan time for the river, the temple and the old city.</p><ChevronRight size={20}/></Link><Link href="/guides/arriving-in-godowlia"><span>Arrive</span><h3>Getting to Godowlia.</h3><p>Address, drop-off details and the hotel contact.</p><ChevronRight size={20}/></Link><Link href="/guides/choosing-your-room"><span>Stay</span><h3>Choose your room.</h3><p>Double, twin or family. Find the right arrangement.</p><ChevronRight size={20}/></Link></div></section>

    <section className="home-reserve" id="reserve"><div className="container home-reserve-grid"><Reveal className="home-reserve-copy"><p className="eyebrow">Your next trip.</p><h2><KineticText text="See you"/><br/><KineticText text="in Varanasi." delay={.1}/></h2><p>Send your dates and guest details. The hotel will confirm room availability and rates directly.</p><div className="home-reserve-contact"><a href={whatsapp} target="_blank" rel="noopener noreferrer"><WhatsAppIcon size={18}/> WhatsApp the hotel</a><a href={hotel.phoneHref}><Phone size={16}/> {hotel.phone}</a><a href={`mailto:${hotel.email}`} style={{overflowWrap:"anywhere"}}><Mail size={16}/> {hotel.email}</a></div></Reveal><StayBar compact/></div></section>
  </main>;
}
