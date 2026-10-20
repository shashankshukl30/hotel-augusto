"use client";

import Image from "next/image";
import Link from "next/link";
import { useState } from "react";
import { motion } from "framer-motion";
import { ArrowUpRight } from "lucide-react";
import { roomImages } from "@/content/room-images";
import { useMotionPreference } from "./use-motion-preference";
import "./room-photo-link.css";

export function RoomPhotoLink({ slug, name, image, alt, className, sizes }: {
  slug: string; name: string; image: string; alt: string; className: string; sizes: string;
}) {
  const [engaged, setEngaged] = useState(false);
  const [requested, setRequested] = useState(false);
  const [loaded, setLoaded] = useState(false);
  const reduced = useMotionPreference();
  const detail = roomImages[slug]?.[1];
  const engage = () => { setRequested(true); setEngaged(true); };
  return <Link className={`${className} room-photo-link`} href={`/rooms/${slug}`} aria-label={`Explore ${name}`}
    onPointerEnter={event => { if (event.pointerType === "mouse") engage(); }} onPointerLeave={() => setEngaged(false)}
    onFocus={engage} onBlur={() => setEngaged(false)}>
    <Image src={image} alt={alt} fill sizes={sizes} quality={85}/>
    {requested && detail && <motion.span className="room-photo-preview" aria-hidden="true"
      initial={{opacity:0}} animate={{opacity:engaged && loaded ? 1 : 0}} transition={{duration:reduced ? 0 : .5}}>
      <Image src={detail.src} alt="" fill sizes={sizes} quality={85} onLoad={() => setLoaded(true)}/>
    </motion.span>}
    <span className="room-photo-invitation" aria-hidden="true"><span>Take a closer look</span><ArrowUpRight size={20}/></span>
  </Link>;
}
