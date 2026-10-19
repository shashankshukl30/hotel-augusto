"use client";

import { useEffect } from "react";
import { usePathname } from "next/navigation";

if (typeof window !== "undefined" && "scrollRestoration" in window.history) window.history.scrollRestoration = "manual";

export function ScrollReset() {
  const pathname = usePathname();
  useEffect(() => {
    if (!window.location.hash) window.scrollTo({ top: 0, behavior: "instant" });
  }, [pathname]);
  return null;
}
