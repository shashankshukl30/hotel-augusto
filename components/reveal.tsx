"use client";

import { motion } from "framer-motion";
import { useMotionPreference } from "./use-motion-preference";
import type { ReactNode } from "react";

/** Adapted from Magic UI Blur Fade (MIT). Kept visible in SSR for progressive enhancement. */
export function Reveal({ children, className, delay = 0 }: { children: ReactNode; className?: string; delay?: number }) {
  const reduced = useMotionPreference();
  return <motion.div className={`motion-reveal${className ? ` ${className}` : ""}`} initial={false}
    whileInView={reduced ? {} : { y: [32, 0], opacity: [.72, 1] }}
    viewport={{ once: true, amount: .18 }}
    transition={{ duration: reduced ? 0 : .9, delay: reduced ? 0 : delay, ease: [.22, 1, .36, 1] }}>
    {children}
  </motion.div>;
}
