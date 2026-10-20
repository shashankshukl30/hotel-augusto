"use client";

import { Fragment, useRef } from "react";
import { motion, useInView } from "framer-motion";
import { useMotionPreference } from "./use-motion-preference";

/** Word masks keep natural wrapping and the original, readable server markup. */
export function KineticText({ text, delay = 0 }: { text: string; delay?: number }) {
  const target = useRef<HTMLSpanElement>(null);
  const visible = useInView(target, { once: true, amount: .01, margin: "0px 0px 40px 0px" });
  const reduced = useMotionPreference();
  return <span ref={target} className="kinetic-text">
    {text.split(" ").map((word, index) => <Fragment key={`${word}-${index}`}>
      {index > 0 ? " " : null}
      <span className="kinetic-word-mask"><motion.span className="kinetic-word"
        initial={false}
        animate={visible && !reduced ? { y: ["115%", "0%"], rotate: [2.5, 0] } : { y: 0, rotate: 0 }}
        transition={{ duration: reduced ? 0 : .85, delay: reduced ? 0 : delay + Math.min(index, 8) * .045, ease: [.16, 1, .3, 1] }}>
        {word}
      </motion.span></span>
    </Fragment>)}
  </span>;
}
