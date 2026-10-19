import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { ArrowUpRight, Snowflake, Wifi, Tv, Bath, ConciergeBell, Utensils } from "lucide-react";
import { rooms } from "@/content/hotel";
import { Reveal } from "@/components/reveal";
import "./rooms.css";

export const metadata: Metadata = { title: "Rooms at Hotel Augusto Varanasi | Make Yourself at Home", description: "Explore Deluxe, Deluxe Twin and Family Rooms at Hotel Augusto, Godowlia. Air conditioning, Wi-Fi and the old city close by. Enquire directly with the hotel." };

export default function RoomsPage() {
  return <main id="main" className="rooms-page">
    <div className="container page-intro rooms-intro"><Reveal><span className="eyebrow">STAY A LITTLE. REMEMBER A LOT.</span><h1>Find your<br/><em>kind of comfort.</em></h1></Reveal><div><p>A morning at the temple. An evening by the Ganges. And in between, a room that feels like yours.</p><span className="eyebrow">THREE WAYS TO STAY AT AUGUSTO</span></div></div>
    <section className="container room-list" aria-label="Our rooms">{rooms.map((room,i)=><article className="room-list-item" key={room.slug}>
      <Reveal className="room-list-photo"><Link href={`/rooms/${room.slug}`} className="image-wrap"><Image src={room.image} alt={room.alt} fill sizes="(max-width: 800px) 90vw, 55vw" preload={i===0} quality={85}/><span className="room-photo-button" aria-hidden="true"><ArrowUpRight size={25}/></span></Link></Reveal>
      <Reveal className="room-list-copy"><div className="room-list-number">0{i+1}<span>/ THE ROOMS</span></div><span className="eyebrow">{room.eyebrow}</span><h2>{room.name}</h2><p>{room.description}</p><span className="room-bed">{room.bedLabel}</span><div className="room-list-actions"><Link href={`/rooms/${room.slug}`} className="text-link">Explore this room <ArrowUpRight size={18}/></Link><Link href={`/contact?room=${room.slug}#enquire`} className="room-enquire">Enquire about a stay <ArrowUpRight size={14}/></Link></div></Reveal>
    </article>)}</section>
    <section className="room-comforts"><div className="container"><Reveal><span className="eyebrow">THE EVERYDAY ESSENTIALS</span><h2 className="display">It’s the little things.</h2></Reveal><div className="comfort-list">{[{Icon:Snowflake,label:"Air conditioning"},{Icon:Wifi,label:"Wi-Fi"},{Icon:Bath,label:"Private bathroom"},{Icon:Tv,label:"Television"},{Icon:ConciergeBell,label:"Room service"},{Icon:Utensils,label:"Vegetarian dining"}].map(({Icon,label})=><div key={label}><Icon size={23} strokeWidth={1.2}/><span>{label}</span></div>)}</div><p>Planning a family trip or have a particular need? Tell us when you enquire so we can help you choose the right room.</p><Link href="/contact#enquire" className="text-link">Talk to the hotel <ArrowUpRight size={18}/></Link></div></section>
  </main>;
}
