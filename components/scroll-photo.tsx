"use client";

import Image from "next/image";
import { useRef } from "react";
import { motion, useMotionTemplate, useScroll, useTransform } from "framer-motion";
import { useMotionPreference } from "./use-motion-preference";

/** The frame opens as the photograph enters; scrolling remains entirely native. */
export function ScrollPhoto({ src, alt, className, sizes, position = "center" }: {
  src: string; alt: string; className: string; sizes: string; position?: string;
}) {
  const target = useRef<HTMLDivElement>(null);
  const reduced = useMotionPreference();
  const { scrollYProgress } = useScroll({ target, offset: ["start end", "end start"] });
  const y = useTransform(scrollYProgress, [0, 1], ["-4%", "4%"]);
  const scale = useTransform(scrollYProgress, [0, .5, 1], [1.16, 1.04, 1.04]);
  const inset = useTransform(scrollYProgress, [0, .42, 1], [12, 0, 0]);
  const clipPath = useMotionTemplate`inset(0% ${inset}% 0% ${inset}% round 24px)`;
  return <motion.div ref={target} className={`${className} scroll-photo-window`}
    style={{ clipPath: reduced ? "none" : clipPath }}>
    <motion.div className="scroll-photo-layer" style={{ y: reduced ? 0 : y, scale: reduced ? 1 : scale }}>
      <Image src={src} alt={alt} fill sizes={sizes} quality={85} style={{ objectFit: "cover", objectPosition: position }}/>
    </motion.div>
  </motion.div>;
}
