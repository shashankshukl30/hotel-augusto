"use client";

import Image from "next/image";
import Link from "next/link";
import { ArrowDown, ArrowUpRight, ChevronRight } from "lucide-react";
import { motion, useScroll, useTransform } from "framer-motion";
import { useMotionPreference } from "./use-motion-preference";
import { useRef } from "react";
import { hotel } from "@/content/hotel";

export function HomeHero() {
  const reduced = useMotionPreference();
  const scene = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({ target: scene, offset: ["start end", "start start"] });
  const scale = useTransform(scrollYProgress, [0, 1], [.94, 1]);
  const imageY = useTransform(scrollYProgress, [0, 1], ["-3%", "3%"]);
  const radius = useTransform(scrollYProgress, [0, 1], [40, 20]);
  const whatsapp = `https://wa.me/${hotel.whatsappNumber}?text=${encodeURIComponent(hotel.bookingMessage)}`;
  const enter = { duration: 1.05, ease: [.22, 1, .36, 1] as [number, number, number, number] };
  return <section className="home-hero" aria-labelledby="hero-title">
    <div className="hero-copy">
      <motion.p className="hero-location" initial={false} animate={reduced ? {} : { y: [18, 0] }} transition={enter}>Hotel Augusto · Godowlia, Varanasi</motion.p>
      <h1 id="hero-title">
        <motion.span className="hero-title-line" initial={false} animate={reduced ? {} : { y: [34, 0] }} transition={enter}>Augusto.</motion.span>
        <motion.span className="hero-title-line hero-title-secondary" initial={false} animate={reduced ? {} : { y: [44, 0] }} transition={{ ...enter, duration: 1.25 }}>Varanasi, up close.</motion.span>
      </h1>
      <motion.div className="hero-actions" initial={false} animate={reduced ? {} : { y: [24, 0] }} transition={{ ...enter, duration: 1.35 }}>
        <Link href="/rooms" className="button" style={{ color: "var(--paper)" }}>Find your room <ArrowUpRight size={20}/></Link>
        <a href={whatsapp} target="_blank" rel="noopener noreferrer" className="hero-whatsapp">Book on WhatsApp <ChevronRight size={20}/></a>
      </motion.div>
    </div>
    <div ref={scene} className="hero-scene-anchor">
      <motion.div className="hero-scene" style={{ scale: reduced ? 1 : scale, borderRadius: reduced ? 28 : radius }}>
        <motion.div className="hero-scene-image" style={{ y: reduced ? 0 : imageY }}>
          <Image src="/images/varanasi-hero.webp" alt="Golden riverfront buildings and boats along the ghats of Varanasi" fill preload sizes="(max-width:600px) 1000px, 100vw" quality={85}/>
        </motion.div>
        <div className="hero-scene-shade"/>
        <div className="hero-scene-caption"><p>A city like no other.<br/>A place to call your own.</p><span>Along the Ganges · Varanasi</span></div>
        <Link href="/hotel" className="hero-stay-link"><div className="hero-stay-image"><Image src="/images/google-double-room.webp" alt="A double-bed guest room shared on Hotel Augusto’s Google profile" fill sizes="(max-width:600px) 120px, 180px" quality={85}/></div><div className="hero-stay-copy"><span>Inside Augusto</span><strong>Make yourself<br/>at home.</strong><span className="hero-stay-action">Meet the hotel <ArrowUpRight size={18}/></span></div></Link>
      </motion.div>
    </div>
    <a href="#discover" className="hero-scroll"><span>There’s more to your stay</span><span className="hero-scroll-icon"><ArrowDown size={20}/></span></a>
  </section>;
}
