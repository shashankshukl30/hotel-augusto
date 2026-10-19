import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ChevronLeft, ChevronRight, Snowflake, Wifi, Tv, Bath } from "lucide-react";
import { rooms } from "@/content/hotel";
import { roomImages } from "@/content/room-images";
import { Reveal } from "@/components/reveal";
import "../rooms.css";

export const dynamicParams = false;
export function generateStaticParams() { return rooms.map(room => ({ slug: room.slug })); }
export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const room = rooms.find(item => item.slug === slug);
  return { title: room ? `${room.name} | Hotel Augusto, Varanasi — Book Direct` : "Room Not Found | Hotel Augusto Varanasi", description: room?.description };
}

const roomSummaries: Record<string, string> = {
  "deluxe-room": "A double bed, air conditioning and a private bathroom. Your base in Godowlia, with the temples and ghats close by.",
  "deluxe-twin-room": "Two separate single beds, air conditioning and a private bathroom. A shared room with a bed of your own.",
  "family-room": "A two-bed room with air conditioning and a private bathroom. Share your guest numbers so we can confirm the right arrangement for your family.",
};
const captions: Record<string, string> = {
  "/images/deluxe-room-blue.webp": "Another double-room layout at Augusto.",
  "/images/room-bathroom.webp": "A private bathroom at the hotel.",
  "/images/family-room-alternate.webp": "Another view of the Family Room.",
  "/images/room-tea.webp": "Tea and coffee setup at Augusto.",
};
const featureIcons = [Snowflake, Bath, Tv, Wifi];

export default async function RoomPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const room = rooms.find(item => item.slug === slug);
  if (!room) notFound();
  const images = roomImages[slug];
  const enquiry = `/contact?room=${room.slug}#enquire`;

  return <main id="main" className="room-detail-page">
    <div className="rooms-container room-detail-intro">
      <Link href="/rooms" className="room-back-link"><ChevronLeft size={17}/> All rooms</Link>
      <div className="room-detail-heading">
        <Reveal><h1>{room.name}</h1><p>{room.bedLabel}. Your stay at Augusto.</p></Reveal>
        <Link className="room-capsule" href={enquiry} style={{ color: "var(--paper)" }}>Enquire about this room</Link>
      </div>
    </div>

    <div className="rooms-container">
      <div className="room-detail-hero"><Image src={room.image} alt={room.alt} fill preload sizes="(max-width: 700px) 1200px, 90vw" quality={85}/></div>
    </div>

    <section className="rooms-container room-detail-overview" aria-labelledby="room-overview-title">
      <Reveal><div className="room-overview-copy"><h2 id="room-overview-title">Settle in.</h2><p>{roomSummaries[slug]}</p></div></Reveal>
      <ul className="room-feature-list">{room.features.map((feature, index) => {
        const Icon = featureIcons[index];
        return <li key={feature}><Icon size={27} strokeWidth={1.5}/><span>{feature}</span></li>;
      })}</ul>
    </section>

    <section className="rooms-container room-detail-gallery" aria-label={`${room.name} and hotel details`}>
      {images.slice(1).map(img => <Reveal key={img.src}><figure><div className="room-detail-photo"><Image src={img.src} alt={img.alt} fill sizes="(max-width: 700px) 90vw, 55vw" quality={85}/></div><figcaption>{captions[img.src]}</figcaption></figure></Reveal>)}
    </section>

    <div className="rooms-container"><p className="room-detail-note">Photographs show rooms and details at Hotel Augusto. Layouts and furnishings may vary. We’ll confirm the room arrangement, guest capacity, meals and rate when you enquire.</p></div>

    <section className="rooms-container">
      <div className="room-enquiry-panel"><Reveal><h2>Make it your stay.</h2><p>Send us your dates. We’ll take it from there.</p></Reveal><Link href={enquiry} className="room-capsule" style={{ color: "var(--paper)" }}>Plan your stay</Link></div>
    </section>

    <section className="rooms-container other-rooms" aria-labelledby="other-rooms-title">
      <div className="other-rooms-heading"><h2 id="other-rooms-title">Explore the other rooms.</h2><Link href="/rooms" className="room-inline-link">Compare all rooms <ChevronRight size={17}/></Link></div>
      <div className="other-rooms-grid">{rooms.filter(item => item.slug !== slug).map(item => <Link href={`/rooms/${item.slug}`} key={item.slug}>
        <div className="other-room-photo"><Image src={item.image} alt={item.alt} fill sizes="(max-width: 600px) 90vw, 45vw" quality={85}/></div>
        <div><h3>{item.name}</h3><ChevronRight size={22}/></div><p>{item.bedLabel}</p>
      </Link>)}</div>
    </section>
  </main>;
}
