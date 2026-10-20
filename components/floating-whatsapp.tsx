"use client";

import { usePathname } from "next/navigation";
import { useSyncExternalStore } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { useMotionPreference } from "./use-motion-preference";
import { WhatsAppIcon } from "./whatsapp-icon";

function subscribe(callback: () => void) {
  window.addEventListener("scroll", callback, { passive: true });
  return () => window.removeEventListener("scroll", callback);
}
function pastHero() { return window.scrollY > Math.max(480, window.innerHeight - 160); }
function initialScroll() { return false; }

export function FloatingWhatsApp({ href }: { href: string }) {
  const pathname = usePathname();
  const reduced = useMotionPreference();
  const show = useSyncExternalStore(subscribe, pastHero, initialScroll);
  return <AnimatePresence initial={false}>{(pathname !== "/" || show) && <motion.aside key="booking-assistance" aria-label="Booking assistance"
    initial={{opacity:0}} animate={{opacity:1}} exit={{opacity:0}} transition={{duration:reduced?0:.25}}>
    <a className="whatsapp-float" href={href} target="_blank" rel="noopener noreferrer" aria-label="Let’s plan your stay on WhatsApp" style={{ color: "var(--paper)" }}><WhatsAppIcon size={22}/><span>Let’s plan your stay</span></a>
  </motion.aside>}</AnimatePresence>;
}
