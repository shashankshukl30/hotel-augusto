"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef, useState, useSyncExternalStore } from "react";
import { motion } from "framer-motion";
import { useMotionPreference } from "./use-motion-preference";
import { ArrowUpRight, Menu, X, Phone, MapPin } from "lucide-react";
import { Brand } from "./brand";
import { hotel } from "@/content/hotel";
import "./interaction-polish.css";

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
        <Link href="/contact#enquire" className="header-book" style={{ color: "var(--paper)" }}><span>Enquire<span className="header-book-extra"> & book</span></span><ArrowUpRight size={18} /></Link>
        <button className="menu-trigger icon-button" ref={trigger} aria-label="Open navigation" aria-haspopup="dialog" aria-expanded={menuOpen} onClick={() => { dialog.current?.showModal(); setMenuOpen(true); }}><Menu size={25} /></button>
      </div>
    </header>
    <dialog className="navigation-dialog" ref={dialog} onClose={() => { setMenuOpen(false); trigger.current?.focus(); }} aria-label="Hotel Augusto navigation" onClick={(event) => { if (event.target === dialog.current) close(); }}>
      <motion.div className="navigation-content" initial={false} animate={menuOpen && !reduced ? { opacity:[.92,1] } : { opacity:1 }} transition={{duration:reduced?0:.25,ease:[.22,1,.36,1]}}>
        <div className="navigation-top"><Brand /><button className="icon-button" aria-label="Close navigation" onClick={close}><X size={26} /></button></div>
        <p className="eyebrow">Hotel Augusto</p>
        <nav aria-label="Mobile navigation">
          {mobileLinks.map((link, index) => <motion.div key={link.href} className="navigation-menu-entry"
            initial={false}
            animate={menuOpen && !reduced ? { y:[12,0], opacity:[0,1] } : { y:0, opacity:1 }}
            transition={{ duration:reduced?0:.38, delay:reduced?0:index*.028, ease:[.22,1,.36,1] }}>
            <Link href={link.href} onClick={close}
              aria-current={pathname === link.href || (link.href !== "/" && pathname.startsWith(link.href + "/")) ? "page" : undefined}>
              <span>{link.label}</span><ArrowUpRight size={22} aria-hidden="true"/>
            </Link>
          </motion.div>)}
        </nav>
        <Link href="/contact#enquire" className="button" style={{ color: "var(--paper)" }} onClick={close}>Plan your stay <ArrowUpRight size={19} /></Link>
        <div className="navigation-contact"><a href={hotel.phoneHref}><Phone size={16}/> Call the hotel</a><a href={hotel.mapsUrl} target="_blank" rel="noopener noreferrer"><MapPin size={16}/> Directions</a></div>
        <p className="navigation-note">Hotel Augusto<br/>Godowlia, Varanasi.</p>
      </motion.div>
    </dialog>
  </>;
}
