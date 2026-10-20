import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { ArrowDown, ArrowRight, ArrowUpRight, Check } from "lucide-react";
import { rooms } from "@/content/hotel";
import { roomImages } from "@/content/room-images";
import { Reveal } from "@/components/reveal";
import "./rooms.css";

export const metadata: Metadata = {
  title: "Rooms at Hotel Augusto Varanasi | Find Your Kashi Stay",
  description: "Explore Deluxe, Twin and Family rooms at Hotel Augusto in Godowlia, Varanasi. Compare bed arrangements, see real photographs and enquire with the hotel.",
};
const summaries: Record<string, string> = {
  "deluxe-room": "A double bed, warm wood finishes and your own space to return to. Settle in between early temple visits and evenings along the ghats.",
  "deluxe-twin-room": "Travel together, with a bed of your own. Two separate single beds make this an easy arrangement for friends and travelling companions.",
  "family-room": "Keep the journey together. A two-bed arrangement gives your family a shared place to settle in after a day around Kashi.",
};

export default function RoomsPage() {
  return <main id="main" className="rooms-page">
    <section className="rooms-container rooms-masthead" aria-labelledby="rooms-title">
      <div className="rooms-masthead-copy"><p className="room-context">Hotel Augusto · Godowlia, Varanasi</p><h1 id="rooms-title">A place to<br/><em>settle in.</em></h1><p className="rooms-masthead-description">Three room arrangements. The same welcome to Kashi. Find the one that suits the way you travel.</p><div className="rooms-masthead-actions"><a href="#room-collection" className="room-action" style={{ color: "var(--paper)" }}>Explore the rooms <ArrowDown size={18}/></a><Link href="/rooms/compare" className="room-text-link">Compare rooms <ArrowUpRight size={17}/></Link></div></div>
      <div className="rooms-masthead-visual"><div className="rooms-masthead-photo"><Image src="/images/deluxe-room-blue.webp" alt="A double-bed room at Hotel Augusto with a blue upholstered headboard and seating" fill preload sizes="(max-width: 760px) 100vw, 58vw" quality={85}/></div><span className="rooms-masthead-caption">Inside Augusto <span>Rooms & stays</span></span></div>
    </section>
    <nav className="rooms-container rooms-directory" aria-label="Explore room types">{rooms.map((room, index) => <Link key={room.slug} href={`/rooms/${room.slug}`}><span className="room-directory-number" aria-hidden="true">0{index + 1}</span><span>{room.name}<small>{room.bedLabel}</small></span><ArrowUpRight size={21} strokeWidth={1.4}/></Link>)}</nav>
    <section id="room-collection" className="rooms-container room-stories" aria-labelledby="room-stories-title">
      <div className="rooms-section-heading"><div><p className="room-context">Our rooms</p><h2 id="room-stories-title">Rest, your way.</h2></div><p>Real spaces, photographed at Augusto.<br/>Take a closer look before you choose.</p></div>
      {rooms.map((room, index) => { const detail = roomImages[room.slug][1]; return <article id={room.slug} className={`room-story${index === 1 ? " room-story-reverse" : ""}`} key={room.slug} aria-labelledby={`${room.slug}-title`}>
        <Reveal className="room-story-visual"><Link href={`/rooms/${room.slug}`} className="room-story-photo" aria-label={`View the ${room.name}`}><Image src={room.image} alt={room.alt} fill sizes="(max-width: 760px) 94vw, 55vw" quality={85}/></Link><figure className="room-story-detail"><div><Image src={detail.src} alt={detail.alt} fill sizes="(max-width: 760px) 38vw, 23vw" quality={75}/></div><figcaption>{room.slug === "deluxe-twin-room" ? "A bathroom at the hotel" : "Another room layout"}</figcaption></figure></Reveal>
        <Reveal className="room-story-copy" delay={.08}><p className="room-story-bed">{room.bedLabel}</p><h3 id={`${room.slug}-title`}>{room.name}</h3><p className="room-story-description">{summaries[room.slug]}</p><ul className="room-feature-list">{room.features.map(feature => <li key={feature}><Check size={14} strokeWidth={1.5}/>{feature}</li>)}</ul><div className="room-story-actions"><Link href={`/rooms/${room.slug}`} className="room-action" style={{ color: "var(--paper)" }}>Explore this room <ArrowUpRight size={18}/></Link><Link href={`/contact?room=${room.slug}#enquire`} className="room-text-link">Enquire <ArrowRight size={17}/></Link></div></Reveal>
      </article>; })}
    </section>
    <section className="room-compare-invitation"><div className="rooms-container room-compare-invitation-inner"><Reveal><p className="room-context">Find your arrangement</p><h2>A double. Two singles.<br/>A room <em>for the family.</em></h2></Reveal><div><p>See the differences together, then share your dates and the number of guests. The hotel will confirm the right arrangement and rate for your stay.</p><Link href="/rooms/compare" className="room-action" style={{ color: "var(--paper)" }}>Compare all three rooms <ArrowUpRight size={18}/></Link></div></div></section>
    <section className="rooms-container room-inclusions"><div><p className="room-context">Beyond your room</p><h2>A little more<br/>to your stay.</h2></div><div><p>Vegetarian dining and room service are available at the hotel. Ask about meal inclusions when you enquire, and let the team know about your arrival plans.</p><div className="room-inclusion-links"><Link href="/dining" className="room-text-link">Dining at Augusto <ArrowUpRight size={17}/></Link><Link href="/contact#find-us" className="room-text-link">Finding the hotel <ArrowUpRight size={17}/></Link></div></div></section>
  </main>;
}
