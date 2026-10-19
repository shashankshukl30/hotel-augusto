"use client";

import Image from "next/image";
import Link from "next/link";
import { useState } from "react";
import { ChevronRight, ArrowLeft, ArrowRight } from "lucide-react";
import { rooms } from "@/content/hotel";
import { motion, useReducedMotion } from "framer-motion";

export function RoomShowcase() {
  const [selected, setSelected] = useState(0);
  const reduced = useReducedMotion();
  const room = rooms[selected];
  return <div className="room-showcase">
    <div className="room-panel" id="room-panel" role="tabpanel" aria-labelledby={`room-tab-${selected}`}>
      <Link className="room-showcase-image image-wrap" href={`/rooms/${room.slug}`} aria-label={`Explore the ${room.name}`}>{rooms.map((item,index)=><motion.div key={item.slug} aria-hidden={index!==selected} initial={false} animate={{opacity:index===selected?1:0}} transition={{duration:reduced?0:.45}} style={{position:"absolute",inset:0}}><Image src={item.image} alt={index===selected?item.alt:""} fill sizes="(max-width:600px) 700px, 90vw" quality={85}/></motion.div>)}</Link>
      <div className="room-showcase-info">
        <div><p className="room-bed-label">{room.bedLabel}</p><h3>{room.name}</h3><Link href={`/rooms/${room.slug}`} className="text-link">Take a closer look <ChevronRight size={17}/></Link></div>
        <p>{room.description}</p>
      </div>
    </div>
    <div className="room-showcase-bottom">
      <div className="room-tabs" role="tablist" aria-label="Explore room types">{rooms.map((item,i)=><button key={item.slug} id={`room-tab-${i}`} role="tab" aria-controls="room-panel" aria-selected={i===selected} tabIndex={i===selected?0:-1} onClick={()=>setSelected(i)} onKeyDown={event=>{
        let next:number|undefined;
        if(event.key==="ArrowRight") next=(i+1)%rooms.length;
        if(event.key==="ArrowLeft") next=(i+rooms.length-1)%rooms.length;
        if(event.key==="Home") next=0;
        if(event.key==="End") next=rooms.length-1;
        if(next!==undefined){event.preventDefault();setSelected(next);document.getElementById(`room-tab-${next}`)?.focus();}
      }}>{item.name.replace(" Room","").replace("Deluxe Twin","Twin")}</button>)}</div>
      <div className="room-controls"><button className="icon-button" aria-label="Previous room type" onClick={()=>setSelected((selected+rooms.length-1)%rooms.length)}><ArrowLeft size={19}/></button><button className="icon-button" aria-label="Next room type" onClick={()=>setSelected((selected+1)%rooms.length)}><ArrowRight size={19}/></button></div>
    </div>
  </div>;
}
