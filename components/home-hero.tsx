"use client";

import Image from "next/image";
import Link from "next/link";
import { ChevronRight } from "lucide-react";
import { motion, useReducedMotion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";
import { hotel } from "@/content/hotel";

export function HomeHero() {
  const reduced = useReducedMotion();
  const scene = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({ target: scene, offset: ["start end", "end start"] });
  const imageY = useTransform(scrollYProgress, [0, 1], ["-3%", "3%"]);
  const whatsapp = `https://wa.me/${hotel.whatsappNumber}?text=${encodeURIComponent(hotel.bookingMessage)}`;
  return <section className="home-hero" aria-labelledby="hero-title">
    <div className="hero-copy">
      <motion.p className="hero-location" initial={false} animate={reduced ? {} : { opacity: [0,1], y: [12,0] }} transition={{duration:.8}}>Hotel Augusto · Godowlia, Varanasi</motion.p>
      <motion.h1 id="hero-title" initial={false} animate={reduced ? {} : { y: [24,0], opacity: [0,1] }} transition={{duration:1,ease:[.22,1,.36,1]}}>Augusto.<br/><span>Varanasi, up close.</span></motion.h1>
      <motion.div className="hero-actions" initial={false} animate={reduced ? {} : { y:[12,0],opacity:[0,1] }} transition={{duration:.8,delay:.15}}>
        <Link href="/rooms" className="button" style={{color:"var(--paper)"}}>Explore rooms</Link>
        <a href={whatsapp} target="_blank" rel="noopener noreferrer" className="text-link">Book on WhatsApp <ChevronRight size={17}/></a>
      </motion.div>
    </div>
    <motion.div ref={scene} className="hero-scene" initial={false} animate={reduced?{}:{y:[24,0],opacity:[0,1]}} transition={{duration:1.2,ease:[.22,1,.36,1],delay:.2}}>
      <motion.div className="hero-scene-image" style={{ y: reduced ? 0 : imageY }}><Image src="/images/ganges-boats.webp" alt="A boat on the Ganges at sunrise in Varanasi" fill preload sizes="(max-width:600px) 1000px, 100vw" quality={85}/></motion.div>
      <div className="hero-scene-caption"><span>Wake up to a different kind of city.</span><span>The Ganges, Varanasi</span></div>
    </motion.div>
  </section>;
}
