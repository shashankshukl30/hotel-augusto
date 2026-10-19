import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, ArrowUpRight, Check } from "lucide-react";
import { rooms } from "@/content/hotel";
import { roomImages } from "@/content/room-images";
import { Reveal } from "@/components/reveal";
import "../rooms.css";

export const dynamicParams = false;
export function generateStaticParams() { return rooms.map(room=>({slug:room.slug})); }
export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const room = rooms.find(item=>item.slug===slug);
  return { title: room ? `${room.name} | Hotel Augusto, Varanasi — Book Direct` : "Room Not Found | Hotel Augusto Varanasi", description: room?.description };
}
export default async function RoomPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const room = rooms.find(item=>item.slug===slug);
  if(!room) notFound();
  const images = roomImages[slug];
  return <main id="main" className="room-detail-page">
    <div className="container room-detail-intro"><Link href="/rooms" className="back-link"><ArrowLeft size={15}/> All our rooms</Link><div><Reveal><span className="eyebrow">{room.eyebrow}</span><h1 className="display">{room.name}</h1></Reveal><Link className="button" href={`/contact?room=${room.slug}#enquire`} style={{color:"var(--paper)"}}>Enquire about this room <ArrowUpRight size={18}/></Link></div></div>
    <div className="container"><div className="room-detail-hero image-wrap"><Image src={room.image} alt={room.alt} fill preload sizes="90vw" quality={85}/><span>{room.bedLabel}</span></div></div>
    <section className="container room-detail-story section-space"><Reveal><span className="eyebrow">YOUR OWN CORNER OF KASHI</span><h2 className="display">Leave the day<br/><em>at the door.</em></h2></Reveal><div><p className="room-description">{room.description}</p><p>Take your time getting ready, settle in after a day out, and make the most of a Godowlia address close to the ghats and temples.</p><ul className="room-feature-list">{room.features.map(feature=><li key={feature}><Check size={15}/>{feature}</li>)}</ul><p className="room-detail-note">Room layouts and furnishings may vary. The hotel will confirm your room arrangement, guest capacity, meal inclusions and rate when you enquire.</p></div></section>
    <section className="container room-detail-gallery" aria-label={`${room.name} and hotel details`}>{images.slice(1).map((img,i)=><Reveal key={img.src}><figure><div className="image-wrap"><Image src={img.src} alt={img.alt} fill sizes="(max-width: 600px) 90vw, 45vw"/></div><figcaption>{i===0?"Another look inside Augusto":"The little comforts"}</figcaption></figure></Reveal>)}</section>
    <section className="container room-enquiry-band"><div><span className="eyebrow">THINKING OF STAYING?</span><h2 className="display">Let’s find your dates.</h2><p>Speak to us directly for availability and the details of your stay.</p></div><Link href={`/contact?room=${room.slug}#enquire`} className="button" style={{color:"var(--paper)"}}>Plan your stay <ArrowUpRight size={18}/></Link></section>
    <section className="container other-rooms"><span className="eyebrow">A DIFFERENT KIND OF STAY</span><div>{rooms.filter(item=>item.slug!==slug).map(item=><Link href={`/rooms/${item.slug}`} key={item.slug}><div className="image-wrap"><Image src={item.image} alt={item.alt} fill sizes="(max-width: 600px) 45vw, 35vw"/></div><h3>{item.name}<ArrowUpRight size={20}/></h3><span>{item.bedLabel}</span></Link>)}</div></section>
  </main>;
}
