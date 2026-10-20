"use client";

import { useRef } from "react";
import { motion, type MotionValue, useScroll, useTransform } from "framer-motion";
import { useMotionPreference } from "./use-motion-preference";

function Word({ children, progress, start, end, reduced }: {
  children: string; progress: MotionValue<number>; start: number; end: number; reduced: boolean;
}) {
  const opacity = useTransform(progress, [start, end], [.65, 1]);
  return <motion.span style={{ opacity: reduced ? 1 : opacity }}>{children}{" "}</motion.span>;
}

export function ScrollStatement() {
  const ref = useRef<HTMLHeadingElement>(null);
  const reduced = useMotionPreference();
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start .9", "end .5"] });
  const lines = ["The city at your door.", "Space to slow down."];
  const count = lines.join(" ").split(" ").length;
  let index = 0;
  return <h2 ref={ref} className="scroll-statement">
    {lines.map(line => <span className="statement-line" key={line}>{line.split(" ").map(word => {
      const start = index++ / count;
      return <Word key={`${start}-${word}`} progress={scrollYProgress} start={start} end={start + 1 / count} reduced={Boolean(reduced)}>{word}</Word>;
    })}</span>)}
  </h2>;
}
