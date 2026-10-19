"use client";

import { usePathname } from "next/navigation";
import { useSyncExternalStore } from "react";
import { WhatsAppIcon } from "./whatsapp-icon";

function subscribe(callback: () => void) {
  window.addEventListener("scroll", callback, { passive: true });
  return () => window.removeEventListener("scroll", callback);
}
function pastHero() { return window.scrollY > Math.max(480, window.innerHeight - 160); }
function initialScroll() { return false; }

export function FloatingWhatsApp({ href }: { href: string }) {
  const pathname = usePathname();
  const show = useSyncExternalStore(subscribe, pastHero, initialScroll);
  if (pathname === "/" && !show) return null;
  return <aside aria-label="Booking assistance"><a className="whatsapp-float" href={href} target="_blank" rel="noopener noreferrer" aria-label="Let’s plan your stay on WhatsApp" style={{ color: "var(--paper)" }}><WhatsAppIcon size={22}/><span>Let’s plan your stay</span></a></aside>;
}
