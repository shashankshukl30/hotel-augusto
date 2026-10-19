"use client";

import { useEffect } from "react";
import { usePathname } from "next/navigation";

if (typeof window !== "undefined" && "scrollRestoration" in window.history) window.history.scrollRestoration = "manual";

export function ScrollReset() {
  const pathname = usePathname();
  useEffect(() => {
    if (!window.location.hash) { window.scrollTo({ top: 0, behavior: "instant" }); return; }
    let id = window.location.hash.slice(1);
    try { id = decodeURIComponent(id); } catch { /* Invalid URL escapes keep their literal fragment. */ }
    let cancelled = false;
    const move = () => { if (!cancelled) document.getElementById(id)?.scrollIntoView({ behavior: "instant", block: "start" }); };
    const frame = window.requestAnimationFrame(move);
    document.fonts.ready.then(move);
    return () => { cancelled = true; window.cancelAnimationFrame(frame); };
  }, [pathname]);
  return null;
}
