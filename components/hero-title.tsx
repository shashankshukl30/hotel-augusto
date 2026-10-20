"use client";

import { useEffect } from "react";
import { stagger, useAnimate } from "framer-motion";
import { useMotionPreference } from "./use-motion-preference";

export function HeroTitle() {
  const reduced = useMotionPreference();
  const [scope, animate] = useAnimate<HTMLHeadingElement>();
  useEffect(() => {
    if (reduced || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const entrance = animate(".hero-title-line", { y: ["120%", "0%"], rotate: [2, 0] }, {
      duration: 1.05, delay: stagger(.13, { startDelay: .08 }), ease: [.16, 1, .3, 1],
    });
    return () => entrance.stop();
  }, [animate, reduced]);
  return <h1 ref={scope} className="hero-title" aria-label="Your place in Kashi.">
    {["Your place", "in Kashi."].map(line =>
      <span className="hero-title-mask" key={line}><span className="hero-title-line">
        {line}
      </span></span>)}
  </h1>;
}
