import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { ArrowDown, ArrowRight, ArrowUpRight, Check } from "lucide-react";
import { rooms } from "@/content/hotel";
import { Reveal } from "@/components/reveal";
import { RoomPhotoLink } from "@/components/room-photo-link";
import "./rooms.css";

export const metadata: Metadata = {
  title: "Rooms at Hotel Augusto Varanasi | Find Your Kashi Stay",
  description: "Explore Deluxe, Twin and Family rooms at Hotel Augusto in Godowlia, Varanasi. Compare bed arrangements, see real photographs and enquire with the hotel.",
};
const summaries: Record<string, string> = {
  "deluxe-room": "A double bed, air conditioning and a private bathroom. A comfortable base for your time in Godowlia.",
  "deluxe-twin-room": "A shared room with two separate single beds. A practical choice for friends and travelling companions.",
  "family-room": "Two beds in one room. Share your guest details with the hotel to confirm the arrangement for your family.",
};
const labels: Record<string, string> = {
  "deluxe-room": "Deluxe", "deluxe-twin-room": "Twin", "family-room": "Family",
};

export default function RoomsPage() {
  return <main id="main" className="rooms-page">
    <section className="rooms-container rooms-masthead" aria-labelledby="rooms-title">
      <div className="rooms-masthead-copy">
        <p className="room-context">Rooms at Augusto</p>
        <h1 id="rooms-title">Find your room.</h1>
        <p className="rooms-masthead-description">Three bed arrangements. One address in Godowlia. Choose the room that works for your stay in Varanasi.</p>
        <div className="rooms-masthead-actions"><a href="#room-collection" className="room-action" style={{ color: "var(--paper)" }}>Explore the rooms <ArrowDown size={18}/></a><Link href="/rooms/compare" className="room-text-link">Compare rooms <ArrowRight size={18}/></Link></div>
      </div>
      <div className="rooms-masthead-photo"><Image src="/images/deluxe-room-blue.webp" alt="A double-bed room at Hotel Augusto with a blue upholstered headboard and seating" fill preload sizes="(max-width: 700px) 100vw, 90vw" quality={85}/></div>
      <nav className="rooms-directory" aria-label="Explore room types">{rooms.map(room => <Link key={room.slug} href={`/rooms/${room.slug}`}><span>{labels[room.slug]}<small>{room.bedLabel}</small></span><ArrowUpRight size={18}/></Link>)}</nav>
    </section>
    <section id="room-collection" className="rooms-container room-stories" aria-labelledby="room-stories-title">
      <div className="rooms-section-heading"><div><h2 id="room-stories-title">A closer look.</h2><p>Real rooms. The details that help you choose.</p></div><Link href="/rooms/compare" className="room-text-link">Compare all three <ArrowRight size={18}/></Link></div>
      {rooms.map(room => <article id={room.slug} className="room-story" key={room.slug} aria-labelledby={`${room.slug}-title`}>
        <Reveal className="room-story-visual"><RoomPhotoLink slug={room.slug} name={room.name} image={room.image} alt={room.alt} className="room-story-photo" sizes="(max-width: 900px) 90vw, 50vw"/></Reveal>
        <Reveal className="room-story-copy" delay={.08}>
          <p className="room-story-bed">{room.bedLabel}</p><h3 id={`${room.slug}-title`}>{room.name}</h3><p className="room-story-description">{summaries[room.slug]}</p>
          <ul className="room-feature-list">{room.features.map(feature => <li key={feature}><Check size={16}/>{feature}</li>)}</ul>
          <div className="room-story-actions"><Link href={`/rooms/${room.slug}`} className="room-action" style={{ color: "var(--paper)" }}>Explore this room <ArrowRight size={18}/></Link><Link href={`/contact?room=${room.slug}#enquire`} className="room-text-link">Enquire <ArrowUpRight size={18}/></Link></div>
        </Reveal>
      </article>)}
    </section>
    <section className="room-compare-invitation"><div className="rooms-container room-compare-invitation-inner"><Reveal><h2>Find the right fit.</h2><p>Compare bed arrangements, then share your dates and guest details. The hotel will confirm availability and rates.</p></Reveal><Link href="/rooms/compare" className="room-action" style={{ color: "var(--paper)" }}>Compare rooms <ArrowRight size={18}/></Link></div></section>
    <section className="rooms-container room-inclusions"><div><h2>More to your stay.</h2><p>Vegetarian dining and room service are available. Ask about meal inclusions and share your arrival plans when you enquire.</p></div><div className="room-inclusion-links"><Link href="/dining" className="room-text-link">Dining at Augusto <ArrowUpRight size={18}/></Link><Link href="/contact#find-us" className="room-text-link">Finding the hotel <ArrowUpRight size={18}/></Link></div></section>
  </main>;
}
