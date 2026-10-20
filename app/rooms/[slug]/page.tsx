import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, ArrowRight, ArrowUpRight, Check, Phone } from "lucide-react";
import { hotel, rooms } from "@/content/hotel";
import { roomImages } from "@/content/room-images";
import { Reveal } from "@/components/reveal";
import { StayBar } from "@/components/stay-bar";
import { RoomPhotographs } from "../room-photographs";
import "../rooms.css";

export const dynamicParams = false;
export function generateStaticParams() { return rooms.map(room => ({ slug: room.slug })); }
export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const room = rooms.find(item => item.slug === slug);
  return { title: room ? `${room.name} | Hotel Augusto, Varanasi — Book Direct` : "Room Not Found | Hotel Augusto Varanasi", description: room?.description };
}
const summaries: Record<string, string> = {
  "deluxe-room": "A double bed, air conditioning and your own bathroom. The Deluxe Room gives you a comfortable base for exploring Godowlia.",
  "deluxe-twin-room": "Two separate single beds in a shared room. The Deluxe Twin Room works well for friends and travelling companions.",
  "family-room": "Two beds in one room. Let the hotel know how many adults and children are travelling so the room arrangement can be confirmed.",
};

export default async function RoomPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const room = rooms.find(item => item.slug === slug);
  if (!room) notFound();
  const enquiry = `/contact?room=${room.slug}#enquire`;
  return <main id="main" className="room-detail-page" data-room={slug}>
    <div className="rooms-container room-detail-breadcrumb"><Link href="/rooms" className="room-back-link"><ArrowLeft size={16}/> All rooms</Link><Link href="/rooms/compare" className="room-back-link">Compare rooms <ArrowUpRight size={16}/></Link></div>
    <header className="rooms-container room-detail-heading"><div><p className="room-context">{room.bedLabel}</p><h1 id="room-title">{room.name}</h1></div><div className="room-heading-action"><p>Hotel Augusto. Godowlia, Varanasi.</p><a href="#room-enquiry" className="room-action" style={{ color: "var(--paper)" }}>Plan your stay <ArrowUpRight size={18}/></a></div></header>
    <div className="rooms-container"><RoomPhotographs images={roomImages[slug]} roomName={room.name}/></div>
    <section className="rooms-container room-detail-overview" aria-labelledby="room-overview-title"><Reveal className="room-overview-copy"><h2 id="room-overview-title">Your room,<br/>at a glance.</h2><p className="room-overview-description">{summaries[slug]}</p><Link href="/hotel" className="room-text-link">Explore the hotel <ArrowUpRight size={17}/></Link></Reveal><div className="room-facts"><div className="room-bed-fact"><span>Bed arrangement</span><strong>{room.bedLabel}</strong></div><h3>In your room</h3><ul>{room.features.map(feature => <li key={feature}><Check size={16} strokeWidth={1.5}/>{feature}</li>)}</ul><p>Photographs show room examples and hotel details. Layouts and furnishings may vary.</p></div></section>
    <section className="room-planning-section" id="room-enquiry" aria-labelledby="room-enquiry-title"><div className="rooms-container room-planning-layout"><div className="room-planning-copy"><h2 id="room-enquiry-title">Plan your stay.</h2><p>Choose your dates and guests. The hotel will confirm availability, the room arrangement and your rate.</p><dl className="room-planning-notes"><div><dt>Meals</dt><dd>Vegetarian dining and room service are available. Ask about meal inclusions.</dd></div><div><dt>Arrival & departure</dt><dd>Confirm timings with the hotel, especially if you’re arriving early or leaving late.</dd></div><div><dt>Travelling together?</dt><dd>Share children’s ages and any additional room or accessibility needs when you enquire.</dd></div></dl><a href={hotel.phoneHref} className="room-text-link"><Phone size={16}/> Speak with the hotel</a></div><div className="room-stay-panel"><div className="room-stay-summary"><span>Your room preference</span><h3>{room.name}</h3><p>{room.bedLabel}</p></div><StayBar compact room={room.slug}/><Link href={enquiry} className="room-panel-link">Add a special request <ArrowUpRight size={16}/></Link></div></div></section>
    <section className="rooms-container other-rooms" aria-labelledby="other-rooms-title"><div className="rooms-section-heading"><div><h2 id="other-rooms-title">More ways to stay.</h2></div><Link href="/rooms/compare" className="room-text-link">Compare arrangements <ArrowRight size={17}/></Link></div><div className="other-rooms-grid">{rooms.filter(item => item.slug !== slug).map(item => <Link href={`/rooms/${item.slug}`} key={item.slug}><div className="other-room-photo"><Image src={item.image} alt={item.alt} fill sizes="(max-width: 700px) 90vw, 45vw" quality={85}/></div><div className="other-room-heading"><h3>{item.name}</h3><ArrowUpRight size={23} strokeWidth={1.5}/></div><p>{item.bedLabel}</p></Link>)}</div></section>
  </main>;
}
