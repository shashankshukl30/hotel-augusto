"use client";

import Image from "next/image";
import Link from "next/link";
import { ArrowDown, ArrowUpRight } from "lucide-react";
import { motion, useReducedMotion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";
import { hotel } from "@/content/hotel";

export function HomeHero() {
  const reduced = useReducedMotion();
  const scene = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({ target: scene, offset: ["start start", "end start"] });
  const imageY = useTransform(scrollYProgress, [0, 1], ["0%", "14%"]);
  const whatsapp = `https://wa.me/${hotel.whatsappNumber}?text=${encodeURIComponent(hotel.bookingMessage)}`;
  return <section ref={scene} className="home-hero" aria-labelledby="hero-title">
    <motion.div className="hero-scene-image" style={{ y: reduced ? 0 : imageY }}>
      <Image src="/images/varanasi-hero.webp" alt="Golden riverfront buildings and boats along the ghats of Varanasi" fill preload sizes="(max-width:1000px) 1500px, 100vw" quality={85}/>
    </motion.div>
    <div className="hero-shade"/>
    <div className="hero-content">
      <motion.p className="hero-location" initial={false} animate={reduced ? {} : { y:[14,0] }} transition={{duration:1}}>HOTEL AUGUSTO <span/> GODOWLIA, VARANASI</motion.p>
      <motion.h1 id="hero-title" initial={false} animate={reduced ? {} : { y:[28,0] }} transition={{duration:1.15,ease:[.22,1,.36,1]}}>Varanasi.<br/><span>Stay closer.</span></motion.h1>
      <motion.div className="hero-introduction" initial={false} animate={reduced ? {} : { y:[20,0] }} transition={{duration:1.2,ease:[.22,1,.36,1]}}>
        <p>The old city outside.<br/>A place of your own inside.</p>
        <div className="hero-actions"><Link href="/rooms" className="button button-light" style={{color:"var(--ink)"}}>Find your room <ArrowUpRight size={18}/></Link><a href={whatsapp} target="_blank" rel="noopener noreferrer" className="hero-whatsapp">Book on WhatsApp <ArrowUpRight size={16}/></a></div>
      </motion.div>
    </div>
    <motion.div className="hero-stay" initial={false} animate={reduced ? {} : { y:[32,0] }} transition={{duration:1.4,ease:[.22,1,.36,1]}}>
      <Link href="/hotel" className="hero-stay-link"><div className="hero-stay-image"><Image src="/images/google-double-room.webp" alt="A double-bed guest room shared on Hotel Augusto’s Google profile" fill sizes="(max-width:600px) 160px, 280px" quality={85}/></div><div className="hero-stay-copy"><span>AT HOTEL AUGUSTO</span><strong>Your place in the city.</strong><span className="hero-stay-action">Meet the hotel <ArrowUpRight size={18}/></span></div></Link>
    </motion.div>
    <div className="hero-bottom"><a href="#discover" className="hero-scroll"><span className="hero-scroll-icon"><ArrowDown size={17}/></span> Take a look around</a><span className="hero-photo-credit">Along the Ganges · Varanasi</span></div>
  </section>;
}
