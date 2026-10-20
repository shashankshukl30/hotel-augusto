"use client";

import { useSyncExternalStore } from "react";

const query = "(prefers-reduced-motion: reduce)";
function subscribe(callback: () => void) {
  const media = window.matchMedia(query);
  media.addEventListener("change", callback);
  return () => media.removeEventListener("change", callback);
}
const snapshot = () => window.matchMedia(query).matches;
const serverSnapshot = () => false;

/**
 * Keep the server and hydration render identical, then read the browser setting.
 * CSS media queries enforce the opt-out before hydration, including without JS.
 * https://react.dev/reference/react/useSyncExternalStore#adding-support-for-server-rendering
 */
export function useMotionPreference() {
  return useSyncExternalStore(subscribe, snapshot, serverSnapshot);
}
