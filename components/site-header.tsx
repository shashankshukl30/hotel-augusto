"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef, useState, useSyncExternalStore } from "react";
import { motion } from "framer-motion";
import { useMotionPreference } from "./use-motion-preference";
import { ArrowUpRight, Menu, X, Phone, MapPin } from "lucide-react";
import { Brand } from "./brand";
import { WhatsAppIcon } from "./whatsapp-icon";
import { hotel } from "@/content/hotel";
import "./interaction-polish.css";
import "./whatsapp-chat.css";

const links = [
  { href: "/hotel", label: "The hotel" },
  { href: "/rooms", label: "Rooms" },
  { href: "/dining", label: "Dining" },
  { href: "/varanasi", label: "Varanasi" },
  { href: "/gallery", label: "Gallery" },
  { href: "/guides", label: "Stay guide" },
  { href: "/contact", label: "Contact" },
];
const mobileLinks = [
  { href: "/", label: "Welcome" },
  ...links.slice(0, 6),
  { href: "/group-stays", label: "Group stays" },
  links[6],
];
const menuEase = [.22, 1, .36, 1] as const;

const subscribeScroll = (callback: () => void) => {
  window.addEventListener("scroll", callback, { passive: true });
  return () => window.removeEventListener("scroll", callback);
};

export function SiteHeader() {
  const pathname = usePathname();
  const reduced = useMotionPreference();
  const [menuOpen, setMenuOpen] = useState(false);
  const scrolled = useSyncExternalStore(subscribeScroll, () => window.scrollY > 40, () => false);
  const dialog = useRef<HTMLDialogElement>(null);
  const trigger = useRef<HTMLButtonElement>(null);
  const whatsapp = `https://wa.me/${hotel.whatsappNumber}?text=${encodeURIComponent(hotel.bookingMessage)}`;
  useEffect(() => { dialog.current?.close(); }, [pathname]);
  const close = () => dialog.current?.close();
  return <>
    <header className={`site-header${pathname === "/" ? " header-home" : ""}${scrolled ? " is-scrolled" : ""}`}>
      <div className="header-inner">
        <Link href="/" className="brand-link" title="Hotel Augusto home" onClick={(event) => {
          if (pathname === "/" && event.button === 0 && !event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey) { event.preventDefault(); window.scrollTo({ top: 0, behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth" }); }
        }}><Brand /></Link>
        <nav className="desktop-nav" aria-label="Main navigation">
          {links.map(link => <Link href={link.href} key={link.href} aria-current={pathname === link.href || pathname.startsWith(link.href + "/") ? "page" : undefined}>{link.label}</Link>)}
        </nav>
        <a href={whatsapp} target="_blank" rel="noopener noreferrer" className="header-book header-whatsapp" style={{ color: "var(--paper)" }} aria-label="Enquire with Hotel Augusto on WhatsApp (opens in a new tab)"><WhatsAppIcon size={19}/><span>WhatsApp</span></a>
        <button className="menu-trigger icon-button" ref={trigger} aria-label="Open navigation" aria-haspopup="dialog" aria-expanded={menuOpen} onClick={() => { dialog.current?.showModal(); setMenuOpen(true); }}><Menu size={25} /></button>
      </div>
    </header>
    <dialog className="navigation-dialog" ref={dialog} onClose={() => { setMenuOpen(false); trigger.current?.focus(); }} aria-label="Hotel Augusto navigation" onClick={(event) => { if (event.target === dialog.current) close(); }}>
      <motion.div className="navigation-content" initial={false}
        animate={menuOpen && !reduced ? { y:[20,0], opacity:[.96,1] } : { y:0, opacity:1 }}
        transition={{duration:reduced ? 0 : .48,ease:menuEase}}>
        <div className="navigation-top"><Brand /><button className="icon-button" aria-label="Close navigation" onClick={close}><X size={26} /></button></div>
        <p className="eyebrow">Hotel Augusto</p>
        <nav aria-label="Mobile navigation">
          {mobileLinks.map((link, index) => <div key={link.href} className="navigation-menu-entry">
            <Link href={link.href} onClick={close}
              aria-current={pathname === link.href || (link.href !== "/" && pathname.startsWith(link.href + "/")) ? "page" : undefined}>
              <span className="navigation-menu-mask">
                <motion.span className="navigation-menu-label" initial={false}
                  animate={menuOpen && !reduced ? { y:["112%","0%"] } : { y:"0%" }}
                  transition={{ duration:reduced ? 0 : .6, delay:reduced ? 0 : .07+index*.035, ease:menuEase }}>
                  {link.label}
                </motion.span>
              </span>
              <motion.span className="navigation-menu-arrow" aria-hidden="true" initial={false}
                animate={menuOpen && !reduced ? { x:[-10,0], opacity:[0,1] } : { x:0, opacity:1 }}
                transition={{ duration:reduced ? 0 : .45, delay:reduced ? 0 : .16+index*.035, ease:menuEase }}>
                <ArrowUpRight size={22}/>
              </motion.span>
            </Link>
          </div>)}
        </nav>
        <Link href="/contact#enquire" className="button" style={{ color: "var(--paper)" }} onClick={close}>Plan your stay <ArrowUpRight size={19} /></Link>
        <div className="navigation-contact"><a href={whatsapp} target="_blank" rel="noopener noreferrer" onClick={close} aria-label="Chat with Hotel Augusto on WhatsApp (opens in a new tab)"><WhatsAppIcon size={18}/> WhatsApp</a><a href={hotel.phoneHref}><Phone size={16}/> Call the hotel</a><a href={hotel.mapsUrl} target="_blank" rel="noopener noreferrer"><MapPin size={16}/> Directions</a></div>
        <p className="navigation-note">Hotel Augusto<br/>Godowlia, Varanasi.</p>
      </motion.div>
    </dialog>
  </>;
}
