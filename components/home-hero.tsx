"use client";

import Image from "next/image";
import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { ArrowDown, ArrowUpRight, Pause, Play } from "lucide-react";
import { useMotionPreference } from "./use-motion-preference";

const scenes = [
  { src:"/images/deluxe-room-blue.webp", alt:"A double-bed room at Hotel Augusto with warm wood finishes and blue upholstery", detail:"Guest rooms", position:"50% 58%" },
  { src:"/images/hotel-lounge.webp", alt:"Hotel Augusto's lounge with carved stone panels, seating and a lift entrance", detail:"The hotel lounge", position:"50% 55%" },
  { src:"/images/dining-room-wide.webp", alt:"The vegetarian restaurant at Hotel Augusto, Varanasi", detail:"Vegetarian dining", position:"50% 50%" },
];

export function HomeHero() {
  const [selected, setSelected] = useState(0);
  const [paused, setPaused] = useState(false);
  const [hovered, setHovered] = useState(false);
  const reduced = useMotionPreference();
  const scene = useRef<HTMLElement>(null);
  const {scrollYProgress} = useScroll({target:scene,offset:["start start","end start"]});
  const y = useTransform(scrollYProgress,[0,1],["0%","12%"]);
  useEffect(()=>{
    if(reduced || paused || hovered) return;
    const interval = window.setInterval(()=>setSelected(index=>(index+1)%scenes.length),6500);
    return ()=>window.clearInterval(interval);
  },[reduced,paused,hovered]);
  const enter = {duration:1.15,ease:[.22,1,.36,1] as [number,number,number,number]};
  return <section ref={scene} className="home-hero" aria-roledescription="carousel" aria-label="Welcome to Hotel Augusto" onMouseEnter={()=>setHovered(true)} onMouseLeave={()=>setHovered(false)} onFocusCapture={()=>setHovered(true)} onBlurCapture={event=>{if(!event.currentTarget.contains(event.relatedTarget))setHovered(false);}}>
    <motion.div className="hero-photographs" style={{y:reduced?0:y}}>
      {scenes.map((photo,index)=><motion.div className="hero-photo" key={photo.src}
        aria-hidden={selected!==index} initial={false}
        animate={{opacity:selected===index?1:0,scale:reduced?1:selected===index?1.04:1}}
        transition={{opacity:{duration:reduced?0:1.2},scale:{duration:6.5,ease:"linear"}}}>
        <Image src={photo.src} alt={selected===index?photo.alt:""} fill
          preload={index===0} loading={index===0?undefined:"eager"} sizes="100vw"
          quality={85} style={{objectPosition:photo.position}}/>
      </motion.div>)}
    </motion.div>
    <div className="hero-veil"/>
    <div className="hero-content container">
      <motion.p className="hero-location eyebrow" initial={false} animate={reduced?{}:{y:[20,0]}} transition={enter}>Hotel Augusto · Godowlia, Varanasi</motion.p>
      <h1><motion.span initial={false} animate={reduced?{}:{y:[38,0]}} transition={enter}>Your place</motion.span><motion.em initial={false} animate={reduced?{}:{y:[48,0]}} transition={{...enter,duration:1.35}}>in Kashi.</motion.em></h1>
      <div className="hero-bottom">
        <div><p className="hero-description">Comfortable rooms. Vegetarian dining.<br/>The old city, right on your doorstep.</p><Link href="/rooms" className="hero-room-link">Discover your stay <ArrowUpRight size={20}/></Link></div>
        <div className="hero-scene-controls">
          <p><span>{String(selected+1).padStart(2,"0")} / 03</span><span>{scenes[selected].detail}</span></p>
          <div className="hero-scene-buttons">{scenes.map((photo,index)=><button key={photo.src} className={selected===index?"is-selected":""} aria-label={`Show ${photo.detail.toLowerCase()}`} aria-pressed={selected===index} onClick={()=>{setSelected(index);setPaused(true);}}><span aria-hidden="true"/></button>)}<button className="hero-pause" onClick={()=>setPaused(!paused)} aria-label={paused?"Play hotel slideshow":"Pause hotel slideshow"} aria-pressed={paused} disabled={reduced}>{paused?<Play size={16}/>:<Pause size={16}/>}</button></div>
          <Link href="/gallery">Explore the gallery <ArrowUpRight size={16}/></Link>
        </div>
      </div>
    </div>
    <a className="hero-scroll" href="#discover"><ArrowDown size={18}/><span>Step inside</span></a>
  </section>;
}
