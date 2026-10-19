"use client";

import Image from "next/image";
import Link from "next/link";
import { useState } from "react";
import { ArrowLeft, ArrowRight, ArrowUpRight } from "lucide-react";
import { rooms } from "@/content/hotel";

export function RoomShowcase() {
  const [selected, setSelected] = useState(0);
  const room = rooms[selected];
  return <div className="room-showcase">
    <div className="room-tabs" role="tablist" aria-label="Explore room types">{rooms.map((item, i) => <button key={item.slug} id={`room-tab-${i}`} role="tab" aria-controls="room-panel" aria-selected={i === selected} tabIndex={i === selected ? 0 : -1} onClick={() => setSelected(i)} onKeyDown={(event) => {
      let next: number | undefined;
      if (event.key === "ArrowRight") next = (i + 1) % rooms.length;
      if (event.key === "ArrowLeft") next = (i + rooms.length - 1) % rooms.length;
      if (event.key === "Home") next = 0;
      if (event.key === "End") next = rooms.length - 1;
      if (next !== undefined) { event.preventDefault(); setSelected(next); document.getElementById(`room-tab-${next}`)?.focus(); }
    }}><span>0{i + 1}</span>{item.name}</button>)}</div>
    <div className="room-panel" id="room-panel" role="tabpanel" aria-labelledby={`room-tab-${selected}`}>
      <Link className="room-showcase-image image-wrap" href={`/rooms/${room.slug}`} aria-label={`Explore the ${room.name}`}><Image src={room.image} alt={room.alt} fill sizes="(max-width: 800px) 100vw, 60vw" quality={85}/><span className="image-explore"><ArrowUpRight size={24}/></span></Link>
      <div className="room-showcase-copy"><span className="eyebrow">{room.eyebrow}</span><h3>{room.name}</h3><p>{room.description}</p><div className="room-essentials"><span>{room.bedLabel}</span><span>Air conditioning</span><span>Wi-Fi</span></div><Link href={`/rooms/${room.slug}`} className="text-link">A closer look <ArrowUpRight size={18}/></Link><div className="room-controls"><span>0{selected + 1}<span className="room-count"> / 0{rooms.length}</span></span><div><button className="icon-button" aria-label="Previous room type" onClick={() => setSelected((selected + rooms.length - 1) % rooms.length)}><ArrowLeft size={18}/></button><button className="icon-button" aria-label="Next room type" onClick={() => setSelected((selected + 1) % rooms.length)}><ArrowRight size={18}/></button></div></div></div>
    </div>
  </div>;
}
