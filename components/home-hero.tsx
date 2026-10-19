"use client";

import Image from "next/image";
import Link from "next/link";
import { ArrowDown, ArrowUpRight } from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";

export function HomeHero() {
  const reduced = useReducedMotion();
  return <section className="home-hero" aria-labelledby="hero-title">
    <motion.div className="hero-image" initial={false} animate={reduced ? {} : { scale: [1.045, 1] }} transition={{ duration: 2.8, ease: [0.22, 1, 0.36, 1] }}><Image src="/images/varanasi-ghats.webp" alt="Boats on the Ganges before the riverfront ghats of Varanasi" fill preload sizes="(max-width: 600px) 1200px, 100vw" quality={85}/></motion.div>
    <div className="hero-shade"/>
    <div className="hero-topline"><span>GODOWLIA, VARANASI</span><span>A CITY TO FEEL. A PLACE TO STAY.</span></div>
    <div className="hero-copy">
      <motion.p className="eyebrow" initial={false} animate={reduced ? {} : { y: [12,0], opacity: [0,1] }} transition={{ duration: .8, delay: .1 }}>WELCOME TO HOTEL AUGUSTO</motion.p>
      <motion.h1 id="hero-title" initial={false} animate={reduced ? {} : { y: [26,0], opacity: [0,1] }} transition={{ duration: 1, delay: .15, ease: [.22,1,.36,1] }}>Let Varanasi<br/><em>stay with you.</em></motion.h1>
      <motion.div initial={false} animate={reduced ? {} : { y: [16,0], opacity: [0,1] }} transition={{ duration: .8, delay: .35 }}><p>A warm welcome. A room to return to.<br/>The old city, just outside.</p><Link href="/rooms" className="hero-link">Find your room <ArrowUpRight size={20}/></Link></motion.div>
    </div>
    <div className="hero-bottom"><a href="#welcome" className="hero-discover"><ArrowDown size={19}/><span>TAKE A LOOK AROUND</span></a><span className="hero-caption">Life along the Ganges · Varanasi</span></div>
  </section>;
}
