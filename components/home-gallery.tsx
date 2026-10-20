"use client";

import Image from "next/image";
import Link from "next/link";
import { useRef } from "react";
import { motion, useScroll, useTransform, type MotionValue } from "framer-motion";
import { ChevronRight } from "lucide-react";
import { useMotionPreference } from "./use-motion-preference";

const photographs = [
  { src: "hotel-lobby", label: "The hotel", alt: "Hotel Augusto lobby", drift: [54, 0, -24] },
  { src: "google-double-room", label: "The rooms", alt: "A double-bed guest room at Hotel Augusto", drift: [-28, 0, 24] },
  { src: "dining-room-wide", label: "The restaurant", alt: "Dining at Hotel Augusto", drift: [78, 0, -36] },
];

function GalleryPhotograph({ photo, progress }: {
  photo: typeof photographs[number]; progress: MotionValue<number>;
}) {
  const reduced = useMotionPreference();
  const y = useTransform(progress, [0, .42, 1], photo.drift);
  return <motion.div className="gallery-motion-card" style={{ y: reduced ? 0 : y }}>
    <Link href="/gallery" aria-label={`Open the gallery: ${photo.label}`}>
      <motion.div className="gallery-motion-image" initial={false}
        whileInView={reduced ? {} : { scale: [1.12, 1] }}
        viewport={{ once: true, amount: .01, margin: "0px 0px 40px 0px" }}
        transition={{ duration: reduced ? 0 : 1.15, ease: [.16, 1, .3, 1] }}>
        <Image src={`/images/${photo.src}.webp`} alt={photo.alt} fill sizes="(max-width:600px) 80vw, 33vw"/>
      </motion.div>
      <span>{photo.label}<ChevronRight size={16}/></span>
    </Link>
  </motion.div>;
}

export function HomeGallery() {
  const target = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({ target, offset: ["start end", "end start"] });
  return <div ref={target} className="home-gallery-strip home-gallery-motion">
    {photographs.map(photo => <GalleryPhotograph key={photo.src} photo={photo} progress={scrollYProgress}/>)}
  </div>;
}
