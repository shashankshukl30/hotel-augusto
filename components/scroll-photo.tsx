"use client";

import Image from "next/image";
import { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { useMotionPreference } from "./use-motion-preference";

/** A small, bounded image movement; the document always retains native scrolling. */
export function ScrollPhoto({ src, alt, className, sizes, position = "center" }: {
  src: string; alt: string; className: string; sizes: string; position?: string;
}) {
  const target = useRef<HTMLDivElement>(null);
  const reduced = useMotionPreference();
  const { scrollYProgress } = useScroll({ target, offset: ["start end", "end start"] });
  const y = useTransform(scrollYProgress, [0, 1], ["-4%", "4%"]);
  return <div ref={target} className={className}>
    <motion.div className="scroll-photo-layer" style={{ y: reduced ? 0 : y }}>
      <Image src={src} alt={alt} fill sizes={sizes} quality={85} style={{ objectFit: "cover", objectPosition: position }}/>
    </motion.div>
  </div>;
}
