"use client";

import { motion, useReducedMotion } from "framer-motion";
import type { ReactNode } from "react";

/** Adapted from Magic UI Blur Fade (MIT). Kept visible in SSR for progressive enhancement. */
export function Reveal({ children, className, delay = 0 }: { children: ReactNode; className?: string; delay?: number }) {
  const reduced = useReducedMotion();
  return <motion.div className={className} initial={false} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.12 }}
    style={{ opacity: 1 }} transition={{ duration: reduced ? 0 : 0.8, delay: reduced ? 0 : delay, ease: [0.22, 1, 0.36, 1] }}>
    <motion.div initial={false} whileInView={reduced ? {} : { y: [18, 0] }} viewport={{ once: true, amount: 0.12 }} transition={{ duration: reduced ? 0 : 0.9, delay, ease: [0.22, 1, 0.36, 1] }}>{children}</motion.div>
  </motion.div>;
}
