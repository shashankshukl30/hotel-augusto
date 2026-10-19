import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { ArrowDown, ArrowRight, ArrowUpRight } from "lucide-react";
import { rooms } from "@/content/hotel";
import { Reveal } from "@/components/reveal";
import "./rooms.css";

export const metadata: Metadata = {
  title: "Rooms at Hotel Augusto Varanasi | Make Yourself at Home",
  description: "Explore the Deluxe, Deluxe Twin and Family Rooms at Hotel Augusto in Godowlia, Varanasi. Choose your bed arrangement and enquire directly with the hotel.",
};

const summaries: Record<string, string> = {
  "deluxe-room": "A double bed and a room of your own in Godowlia. Settle in between early temple visits and evenings along the ghats.",
  "deluxe-twin-room": "Two separate single beds for a shared stay. An easy arrangement for travelling companions, with the old city close by.",
  "family-room": "Stay together in a two-bed room. Tell us how many adults and children are coming, and we’ll confirm the arrangement for your family.",
};

export default function RoomsPage() {
  return <main id="main" className="rooms-page">
    <section className="rooms-container rooms-masthead" aria-labelledby="rooms-title">
      <div className="rooms-masthead-copy">
        <p className="room-context">Your stay in Godowlia</p>
        <h1 id="rooms-title">Rooms at<br/>Augusto.</h1>
        <p className="rooms-masthead-description">A double bed, separate singles, or a room for the family. Find your place in Varanasi.</p>
        <nav className="rooms-directory" aria-label="Explore room types">
          {rooms.map(room => <Link key={room.slug} href={`/rooms/${room.slug}`}><span>{room.name}<small>{room.bedLabel}</small></span><ArrowUpRight size={22} strokeWidth={1.4}/></Link>)}
        </nav>
      </div>
      <div className="rooms-masthead-visual">
        <Image src="/images/deluxe-room-blue.webp" alt="A double-bed room at Hotel Augusto with a blue upholstered headboard and seating" fill preload sizes="(max-width: 700px) 900px, 60vw" quality={85}/>
        <Link href="/gallery" className="rooms-photo-link">View room photographs <ArrowUpRight size={17}/></Link>
      </div>
    </section>

    <section className="rooms-container room-stories" aria-labelledby="room-stories-title">
      <div className="rooms-section-heading"><h2 id="room-stories-title">Three ways to stay.</h2><a href="#deluxe-room" className="room-text-link">Explore the rooms <ArrowDown size={17}/></a></div>
      {rooms.map(room => <article id={room.slug} className="room-story" key={room.slug} aria-labelledby={`${room.slug}-title`}>
        <Reveal className="room-story-visual"><Link href={`/rooms/${room.slug}`} className="room-story-photo" aria-label={`View the ${room.name}`}><Image src={room.image} alt={room.alt} fill sizes="(max-width: 700px) 90vw, 60vw" quality={85}/></Link></Reveal>
        <Reveal className="room-story-copy"><p className="room-story-bed">{room.bedLabel}</p><h3 id={`${room.slug}-title`}>{room.name}</h3><p className="room-story-description">{summaries[room.slug]}</p><div className="room-story-actions"><Link href={`/rooms/${room.slug}`} className="room-action" style={{ color: "var(--paper)" }}>View room <ArrowUpRight size={18}/></Link><Link href={`/contact?room=${room.slug}#enquire`} className="room-text-link">Enquire <ArrowRight size={17}/></Link></div></Reveal>
      </article>)}
    </section>

    <section className="room-inclusions" aria-labelledby="inclusions-title"><div className="rooms-container room-inclusions-inner">
      <Reveal><p className="room-context">Across all our rooms</p><h2 id="inclusions-title">Comfort comes<br/>as standard.</h2></Reveal>
      <div><ul><li>Air conditioning</li><li>Private bathroom</li><li>Wi-Fi</li><li>Television</li></ul><p>Room service and vegetarian dining are available at the hotel. Ask about meal inclusions when you enquire.</p><Link href="/contact#enquire" className="room-text-link">Plan your stay with us <ArrowUpRight size={17}/></Link></div>
    </div></section>
  </main>;
}
