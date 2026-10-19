import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, ArrowRight, ArrowUpRight } from "lucide-react";
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

const summaries: Record<string, string> = {
  "deluxe-room": "A double bed and your own space to settle into. With air conditioning and a private bathroom, the Deluxe Room is a comfortable base for your time in Godowlia.",
  "deluxe-twin-room": "A shared room with a bed of your own. Two separate single beds, air conditioning and a private bathroom make the Deluxe Twin Room a practical choice for travelling companions.",
  "family-room": "A two-bed room for a shared family stay. There’s air conditioning and a private bathroom; let us know who’s coming so we can confirm the arrangement for your family.",
};
const captions: Record<string, string> = {
  "/images/deluxe-room-blue.webp": "Another double-room layout at Augusto.",
  "/images/room-bathroom.webp": "A private bathroom at the hotel.",
  "/images/family-room-alternate.webp": "Another view of the Family Room.",
  "/images/room-tea.webp": "Tea and coffee setup at Augusto.",
};

export default async function RoomPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const room = rooms.find(item => item.slug === slug);
  if (!room) notFound();
  const images = roomImages[slug];
  const enquiry = `/contact?room=${room.slug}#enquire`;

  return <main id="main" className="room-detail-page" data-room={slug}>
    <div className="rooms-container room-detail-breadcrumb"><Link href="/rooms" className="room-back-link"><ArrowLeft size={16}/> All rooms</Link><span>Hotel Augusto, Varanasi</span></div>

    <section className="room-detail-hero" aria-labelledby="room-title">
      <Image src={room.image} alt={room.alt} fill preload sizes="(max-width: 700px) 1400px, 100vw" quality={85}/>
      <div className="room-detail-shade"/>
      <div className="rooms-container room-detail-hero-copy"><div><p>{room.bedLabel}</p><h1 id="room-title">{room.name}</h1></div><Link href={enquiry} className="room-action room-action-light" style={{ color: "var(--ink)" }}>Enquire about this room <ArrowUpRight size={18}/></Link></div>
    </section>

    <section className="rooms-container room-detail-overview" aria-labelledby="room-overview-title">
      <Reveal className="room-overview-copy"><p className="room-context">A closer look</p><h2 id="room-overview-title">Your room<br/>at Augusto.</h2><p className="room-overview-description">{summaries[slug]}</p></Reveal>
      <div className="room-facts"><div className="room-bed-fact"><span>Bed arrangement</span><strong>{room.bedLabel}</strong></div><h3>In your room</h3><ul>{room.features.map(feature => <li key={feature}>{feature}</li>)}</ul><p>Room layouts and furnishings may vary. We’ll confirm guest capacity, meal inclusions and the rate when you enquire.</p><Link href={enquiry} className="room-text-link">Ask about your dates <ArrowUpRight size={17}/></Link></div>
    </section>

    <section className="rooms-container room-detail-gallery" aria-label={`${room.name} and hotel details`}>
      {images.slice(1).map(img => <Reveal key={img.src}><figure><div className="room-detail-photo"><Image src={img.src} alt={img.alt} fill sizes="(max-width: 700px) 90vw, 55vw" quality={85}/></div><figcaption>{captions[img.src]}</figcaption></figure></Reveal>)}
    </section>

    <section className="rooms-container room-reservation-row"><div><h2>Stay in the {room.name}.</h2><p>Share your dates and travel plans directly with the hotel.</p></div><Link href={enquiry} className="room-action" style={{ color: "var(--paper)" }}>Plan your stay <ArrowUpRight size={18}/></Link></section>

    <section className="other-rooms" aria-labelledby="other-rooms-title"><div className="rooms-container">
      <div className="rooms-section-heading"><h2 id="other-rooms-title">Explore our other rooms.</h2><Link href="/rooms" className="room-text-link">All rooms <ArrowRight size={17}/></Link></div>
      <div className="other-rooms-grid">{rooms.filter(item => item.slug !== slug).map(item => <Link href={`/rooms/${item.slug}`} key={item.slug}>
        <div className="other-room-photo"><Image src={item.image} alt={item.alt} fill sizes="(max-width: 600px) 90vw, 45vw" quality={85}/></div>
        <div className="other-room-heading"><h3>{item.name}</h3><ArrowUpRight size={23} strokeWidth={1.5}/></div><p>{item.bedLabel}</p>
      </Link>)}</div>
    </div></section>
  </main>;
}
