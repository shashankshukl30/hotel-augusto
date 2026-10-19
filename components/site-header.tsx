"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef, useSyncExternalStore } from "react";
import { ArrowUpRight, Menu, X } from "lucide-react";
import { Brand } from "./brand";

const links = [
  { href: "/hotel", label: "The hotel" },
  { href: "/rooms", label: "Rooms" },
  { href: "/dining", label: "Dining" },
  { href: "/varanasi", label: "Varanasi" },
  { href: "/gallery", label: "Gallery" },
  { href: "/contact", label: "Contact" },
];

const subscribeScroll = (callback: () => void) => {
  window.addEventListener("scroll", callback, { passive: true });
  return () => window.removeEventListener("scroll", callback);
};

export function SiteHeader() {
  const pathname = usePathname();
  const scrolled = useSyncExternalStore(subscribeScroll, () => window.scrollY > 40, () => false);
  const overHero = pathname === "/" && !scrolled;
  const dialog = useRef<HTMLDialogElement>(null);
  const trigger = useRef<HTMLButtonElement>(null);
  useEffect(() => { dialog.current?.close(); }, [pathname]);
  const close = () => dialog.current?.close();
  return <>
    <header className={`site-header${pathname === "/" ? " header-home" : ""}${scrolled ? " is-scrolled" : ""}`}>
      <div className="header-inner">
        <Link href="/" className="brand-link" title="Hotel Augusto home" onClick={(event) => {
          if (pathname === "/") { event.preventDefault(); window.scrollTo({ top: 0, behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth" }); }
        }}><Brand /></Link>
        <nav className="desktop-nav" aria-label="Main navigation">
          {links.map(link => <Link href={link.href} key={link.href} aria-current={pathname === link.href || pathname.startsWith(link.href + "/") ? "page" : undefined}>{link.label}</Link>)}
        </nav>
        <Link href="/contact#enquire" className="header-book" style={{ color: overHero ? "var(--ink)" : "var(--paper)" }}>Book a stay <ArrowUpRight size={17} /></Link>
        <button className="menu-trigger icon-button" ref={trigger} aria-label="Open navigation" aria-haspopup="dialog" onClick={() => dialog.current?.showModal()}><Menu size={25} /></button>
      </div>
    </header>
    <dialog className="navigation-dialog" ref={dialog} onClose={() => trigger.current?.focus()} aria-label="Hotel Augusto navigation" onClick={(event) => { if (event.target === dialog.current) close(); }}>
      <div className="navigation-content">
        <div className="navigation-top"><Brand /><button className="icon-button" aria-label="Close navigation" onClick={close}><X size={26} /></button></div>
        <p className="eyebrow">Hotel Augusto</p>
        <nav aria-label="Mobile navigation">
          {[{ href: "/", label: "Welcome" }, ...links].map((link, index) => <Link href={link.href} key={link.href} onClick={close}><span className="nav-number">0{index + 1}</span>{link.label}<ArrowUpRight size={22}/></Link>)}
        </nav>
        <Link href="/contact#enquire" className="button" style={{ color: "var(--paper)" }} onClick={close}>Plan your stay <ArrowUpRight size={19} /></Link>
        <p className="navigation-note">Hotel Augusto<br/>Godowlia, Varanasi.</p>
      </div>
    </dialog>
  </>;
}
