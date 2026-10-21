"use client";

import Image from "next/image";
import { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { useMotionPreference } from "./use-motion-preference";

/** The photograph moves inside a stable frame aligned with surrounding content. */
export function ScrollPhoto({ src, alt, className, sizes, position = "center" }: {
  src: string; alt: string; className: string; sizes: string; position?: string;
}) {
  const target = useRef<HTMLDivElement>(null);
  const reduced = useMotionPreference();
  const { scrollYProgress } = useScroll({ target, offset: ["start end", "end start"] });
  const y = useTransform(scrollYProgress, [0, 1], ["-4%", "4%"]);
  const scale = useTransform(scrollYProgress, [0, .5, 1], [1.16, 1.04, 1.04]);
  return <div ref={target} className={`${className} scroll-photo-window`}>
    <motion.div className="scroll-photo-layer" style={{ y: reduced ? 0 : y, scale: reduced ? 1 : scale }}>
      <Image src={src} alt={alt} fill sizes={sizes} quality={85} style={{ objectFit: "cover", objectPosition: position }}/>
    </motion.div>
  </div>;
}
