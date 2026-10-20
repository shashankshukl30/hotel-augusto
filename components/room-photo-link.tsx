"use client";

import Image from "next/image";
import Link from "next/link";
import { useRef, useState, type PointerEvent } from "react";
import { motion, useMotionValue, useSpring } from "framer-motion";
import { ArrowUpRight } from "lucide-react";
import { roomImages } from "@/content/room-images";
import { useMotionPreference } from "./use-motion-preference";
import "./room-photo-link.css";

const revealEase = [.22, 1, .36, 1] as const;
const pointerSpring = { stiffness: 210, damping: 24, mass: .45 };

export function RoomPhotoLink({ slug, name, image, alt, className, sizes }: {
  slug: string; name: string; image: string; alt: string; className: string; sizes: string;
}) {
  const [engaged, setEngaged] = useState(false);
  const [requested, setRequested] = useState(false);
  const [loaded, setLoaded] = useState(false);
  const hovered = useRef(false);
  const focused = useRef(false);
  const pointerX = useMotionValue(0);
  const pointerY = useMotionValue(0);
  const invitationX = useSpring(pointerX, pointerSpring);
  const invitationY = useSpring(pointerY, pointerSpring);
  const reduced = useMotionPreference();
  const detail = roomImages[slug]?.[1];
  const showingPreview = engaged && loaded;
  const engage = () => {
    setRequested(true);
    setEngaged(true);
  };
  const resetPointer = () => {
    pointerX.set(0);
    pointerY.set(0);
  };
  const movePointer = (event: PointerEvent<HTMLAnchorElement>) => {
    if (event.pointerType !== "mouse" || !hovered.current || reduced) return;
    const bounds = event.currentTarget.getBoundingClientRect();
    const x = Math.max(-1, Math.min(1, ((event.clientX - bounds.left) / bounds.width - .5) * 2));
    const y = Math.max(-1, Math.min(1, ((event.clientY - bounds.top) / bounds.height - .5) * 2));
    // Only the invitation moves: the photograph and its link target stay fixed.
    pointerX.set(x * 6);
    pointerY.set(y * 5);
  };
  return <Link className={`${className} room-photo-link`} href={`/rooms/${slug}`} aria-label={`Explore ${name}`}
    data-engaged={engaged || undefined} data-preview-ready={loaded || undefined}
    onPointerEnter={event => {
      if (event.pointerType !== "mouse" || !window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;
      hovered.current = true;
      engage();
      movePointer(event);
    }}
    onPointerMove={movePointer}
    onPointerLeave={() => {
      hovered.current = false;
      resetPointer();
      setEngaged(focused.current);
    }}
    onFocus={event => {
      if (!event.currentTarget.matches(":focus-visible")) return;
      focused.current = true;
      resetPointer();
      engage();
    }}
    onBlur={() => {
      focused.current = false;
      setEngaged(hovered.current);
    }}>
    <Image src={image} alt={alt} fill sizes={sizes} quality={85}/>
    {requested && detail && <motion.span className="room-photo-preview" aria-hidden="true"
      initial={false}
      animate={{ clipPath: showingPreview ? "inset(0% 0% 0% 0%)" : "inset(100% 0% 0% 0%)" }}
      transition={{ duration: reduced ? 0 : showingPreview ? .72 : .48, ease: revealEase }}>
      <motion.span className="room-photo-preview-image"
        initial={false}
        animate={{ scale: showingPreview || reduced ? 1 : 1.08, y: showingPreview || reduced ? "0%" : "4%" }}
        transition={{ duration: reduced ? 0 : .9, ease: revealEase }}>
        <Image src={detail.src} alt="" fill sizes={sizes} quality={85}
          onLoad={event => setLoaded(event.currentTarget.naturalWidth > 0)} onError={() => setLoaded(false)}/>
      </motion.span>
    </motion.span>}
    <motion.span className="room-photo-invitation" aria-hidden="true"
      style={{ x: reduced ? 0 : invitationX, y: reduced ? 0 : invitationY }}>
      <span className="room-photo-invitation-label"><span>Take a closer look</span></span>
      <motion.span className="room-photo-invitation-arrow" initial={false}
        animate={{ rotate: engaged && !reduced ? 45 : 0 }}
        transition={{ type: "spring", stiffness: 260, damping: 25 }}>
        <ArrowUpRight size={20}/>
      </motion.span>
    </motion.span>
  </Link>;
}
