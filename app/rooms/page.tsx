import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { ArrowRight, ChevronRight, Snowflake, Wifi, Tv, Bath } from "lucide-react";
import { rooms } from "@/content/hotel";
import { Reveal } from "@/components/reveal";
import "./rooms.css";

export const metadata: Metadata = {
  title: "Rooms at Hotel Augusto Varanasi | Make Yourself at Home",
  description: "Compare Deluxe, Deluxe Twin and Family Rooms at Hotel Augusto, Godowlia. Find your preferred bed arrangement and enquire directly with the hotel.",
};

const roomSummaries: Record<string, string> = {
  "deluxe-room": "A double-bed room for your stay in the old city.",
  "deluxe-twin-room": "Share a room, with a separate bed for each of you.",
  "family-room": "A two-bed arrangement for travelling together.",
};

const essentials = [
  { Icon: Snowflake, label: "Air conditioning" },
  { Icon: Wifi, label: "Wi-Fi" },
  { Icon: Bath, label: "Private bathroom" },
  { Icon: Tv, label: "Television" },
];

export default function RoomsPage() {
  return <main id="main" className="rooms-page">
    <section className="rooms-container rooms-intro" aria-labelledby="rooms-title">
      <Reveal>
        <p className="room-kicker">Rooms at Augusto</p>
        <h1 id="rooms-title">Find your room.</h1>
        <p className="rooms-intro-description">Double, twin or family. Three ways to stay<br className="rooms-desktop-break"/> in the heart of Varanasi.</p>
      </Reveal>
    </section>

    <section className="rooms-lineup-section" aria-label="Compare our rooms">
      <div className="room-lineup" role="region" aria-label="Room types. Scroll to compare." tabIndex={0}>
        {rooms.map((room, index) => <article className="room-product" key={room.slug}>
          <Link href={`/rooms/${room.slug}`} className="room-product-photo" aria-label={`Explore the ${room.name}`}>
            <Image src={room.image} alt={room.alt} fill sizes="(max-width: 700px) 90vw, (max-width: 1000px) 48vw, 33vw" preload={index === 0} quality={85}/>
          </Link>
          <div className="room-product-copy">
            <h2>{room.name}</h2>
            <p className="room-product-bed">{room.bedLabel}</p>
            <p className="room-product-description">{roomSummaries[room.slug]}</p>
            <div className="room-product-actions">
              <Link href={`/rooms/${room.slug}`} className="room-capsule" style={{ color: "var(--paper)" }}>Explore room</Link>
              <Link href={`/contact?room=${room.slug}#enquire`} className="room-inline-link">Enquire <ChevronRight size={17}/></Link>
            </div>
          </div>
        </article>)}
      </div>
      <p className="rooms-swipe-note">Scroll to explore all three rooms <ArrowRight size={15}/></p>
    </section>

    <section className="rooms-container room-essentials" aria-labelledby="essentials-title">
      <Reveal><h2 id="essentials-title">The essentials.<br/><span>In every room.</span></h2></Reveal>
      <div className="room-essentials-list">
        {essentials.map(({ Icon, label }) => <div key={label}><Icon size={33} strokeWidth={1.5}/><h3>{label}</h3></div>)}
      </div>
      <p>Room service and vegetarian dining are available at the hotel.<br className="rooms-desktop-break"/> Ask about meal inclusions when you enquire.</p>
    </section>

    <section className="rooms-container">
      <div className="rooms-help">
        <Reveal><h2>A little help<br/>choosing?</h2></Reveal>
        <div><p>Tell us your dates and who’s coming. We’ll help you find the right arrangement and confirm availability.</p><Link href="/contact#enquire" className="room-inline-link">Talk to the hotel <ChevronRight size={18}/></Link></div>
      </div>
    </section>
  </main>;
}
