"use client";

import Image from "next/image";
import Link from "next/link";
import { useId, useRef, useState, type KeyboardEvent } from "react";
import { motion, useScroll, useSpring, useTransform } from "framer-motion";
import { ArrowUpRight } from "lucide-react";
import { useMotionPreference } from "./use-motion-preference";
import "./city-itinerary.css";

const stops = [
  {
    label: "The river",
    moment: "At first light",
    title: "The Ganga at dawn.",
    description: "Meet Varanasi from the riverfront. The early light brings the ghats, boats and steps into view as the city begins its day.",
    practical: "Boat rides are available around Dashashwamedh Ghat. Agree the route and fare locally before setting out.",
    image: "/images/ganges-dawn.webp",
    alt: "Small boats on the Ganga in the warm light of sunrise",
    caption: "Dawn on the Ganga · Destination photograph",
    position: "50% 58%",
    href: "/varanasi#river",
    link: "Explore the riverfront",
  },
  {
    label: "The temple",
    moment: "A visit to Kashi",
    title: "Kashi Vishwanath.",
    description: "Shri Kashi Vishwanath Temple is dedicated to Lord Shiva and is one of the twelve Jyotirlingas. It lies within walking distance of Augusto.",
    practical: "Check the temple’s current visitor instructions before you leave. Give this part of the day its own space.",
    image: "/images/kashi-vishwanath.webp",
    alt: "The golden shrine and courtyard at Shri Kashi Vishwanath Temple",
    caption: "Pradum Shukla / Wikimedia Commons · CC BY 4.0",
    credit: "https://commons.wikimedia.org/wiki/File:Kashi_Vishwanath_Temple_in_2025.jpg",
    position: "center 66%",
    href: "/guides/first-visit-to-kashi",
    link: "Plan your first visit",
  },
  {
    label: "The old city",
    moment: "Between visits",
    title: "Back at Augusto.",
    description: "Make your way through the old city at your own pace. Godowlia is your base, with a room and vegetarian dining to return to at Augusto.",
    practical: "Keep the hotel’s map pin handy and speak with the team if you need help planning your arrival or return.",
    image: "/images/hotel-exterior-day.webp",
    alt: "The daytime exterior of Hotel Augusto in Godowlia, Varanasi",
    caption: "Hotel Augusto, Godowlia · Property photograph",
    position: "center 48%",
    href: "/dining",
    link: "Dining at Augusto",
  },
  {
    label: "The evening",
    moment: "Back by the ghats",
    title: "Ganga Aarti.",
    description: "Dashashwamedh Ghat comes together for the evening Ganga Aarti. Lamps, chants and bells are part of the experience by the river.",
    practical: "Leave time to reach the ghat and find a place to take it in. Confirm the day’s arrangements locally.",
    image: "/images/ganges-boats.webp",
    alt: "A wooden boat on the Ganga beneath a low orange sun",
    caption: "Along the Ganga · Destination photograph",
    position: "center 70%",
    href: "/varanasi#aarti",
    link: "Discover the evening aarti",
  },
] as const;

export function CityItinerary({ compact = false }: { compact?: boolean }) {
  const [selected, setSelected] = useState(0);
  const [frame, setFrame] = useState({ current: 0, previous: 0 });
  const [failedImage, setFailedImage] = useState<number | null>(null);
  const requested = useRef(0);
  const readyImages = useRef(new Set<number>());
  const failedImages = useRef(new Set<number>());
  const stage = useRef<HTMLDivElement>(null);
  const reduced = useMotionPreference();
  const instance = useId().replaceAll(":", "");
  const stop = stops[frame.current];
  const tabId = (index: number) => `${instance}-city-tab-${index}`;
  const panelId = `${instance}-city-panel`;
  const { scrollYProgress } = useScroll({ target: stage, offset: ["start end", "end start"] });
  const progress = useSpring(scrollYProgress, { stiffness: 110, damping: 30, mass: 0.45 });
  const cityY = useTransform(progress, [0, 1], ["14%", "-10%"]);
  const photoY = useTransform(progress, [0, 1], ["-2.5%", "2.5%"]);
  const revealEase = [0.22, 1, 0.36, 1] as const;

  function showImage(index: number) {
    setFrame((current) => current.current === index ? current : { current: index, previous: current.current });
  }

  function selectStop(index: number) {
    requested.current = index;
    setSelected(index);
    setFailedImage(failedImages.current.has(index) ? index : null);
    if (readyImages.current.has(index)) showImage(index);
  }

  // Next's onLoad runs after decoding. Keep the last ready image underneath
  // the reveal, including when someone moves quickly through several tabs.
  function imageReady(index: number) {
    readyImages.current.add(index);
    failedImages.current.delete(index);
    if (requested.current === index) {
      setFailedImage(null);
      showImage(index);
    }
  }

  function imageFailed(index: number) {
    failedImages.current.add(index);
    if (requested.current === index) setFailedImage(index);
  }

  function move(event: KeyboardEvent<HTMLButtonElement>, index: number) {
    let next: number | undefined;
    if (event.key === "ArrowRight") next = (index + 1) % stops.length;
    if (event.key === "ArrowLeft") next = (index + stops.length - 1) % stops.length;
    if (event.key === "Home") next = 0;
    if (event.key === "End") next = stops.length - 1;
    if (next === undefined) return;
    event.preventDefault();
    selectStop(next);
    document.getElementById(tabId(next))?.focus({ preventScroll: true });
  }

  return (
    <section className={`city-itinerary${compact ? " city-itinerary-compact" : ""}`} aria-labelledby={`${instance}-city-heading`}>
      <div className="container">
        <div className="itinerary-heading">
          <div><p className="itinerary-kicker">Around the hotel</p><h2 id={`${instance}-city-heading`}>A day in<br />Varanasi.</h2></div>
          <p>Plan a river morning, a temple visit and the evening aarti, with time back at Augusto in between.</p>
        </div>
        <div className="itinerary-tabs" role="tablist" aria-label="Explore a day in Varanasi">
          {stops.map((item, index) => (
            <button type="button" role="tab" key={item.label} id={tabId(index)} aria-controls={panelId} aria-selected={selected === index} tabIndex={selected === index ? 0 : -1} onClick={() => selectStop(index)} onKeyDown={(event) => move(event, index)} style={{ backgroundColor: selected === index ? "transparent" : undefined, color: selected === index ? "var(--city-background)" : "var(--city-text)" }}>
              {selected === index && <motion.span className="itinerary-tab-pill" layoutId={`${instance}-city-tab-pill`} aria-hidden="true" initial={false} style={{ borderRadius: 999 }} transition={reduced ? { duration: 0 } : { type: "spring", stiffness: 420, damping: 36, mass: 0.8 }} />}
              <span className="itinerary-tab-label">{item.label}</span>
            </button>
          ))}
        </div>
        <div className="itinerary-panel" id={panelId} role="tabpanel" aria-labelledby={tabId(selected)} tabIndex={0}>
          <div className="itinerary-copies">
            {stops.map((item, index) => <div className="itinerary-copy" key={item.label} inert={index !== selected} aria-hidden={index !== selected} style={{ visibility: index === selected ? "visible" : "hidden" }}><motion.div className="itinerary-copy-motion" initial={false} animate={index === selected && !reduced ? { y: [16, 0], opacity: [0.7, 1] } : { y: 0, opacity: index === selected ? 1 : 0 }} transition={{ duration: reduced ? 0 : 0.5, ease: [0.22, 1, 0.36, 1] }}>
              <div className="itinerary-copy-lead"><p className="itinerary-moment">{item.moment}</p><h3>{item.title}</h3></div>
              <div className="itinerary-copy-detail"><p>{item.description}</p><p className="itinerary-practical">{item.practical}</p>
                <Link className="itinerary-link" href={item.href} tabIndex={index === selected ? 0 : -1}>{item.link}<ArrowUpRight size={19} aria-hidden="true" /></Link>
              </div>
            </motion.div></div>)}
          </div>
          <div className="itinerary-stage" ref={stage}>
            <div className="itinerary-city-name" aria-hidden="true"><motion.span className="itinerary-city-name-motion" style={{ y: reduced ? 0 : cityY }}>KASHI</motion.span></div>
            <figure className="itinerary-figure" aria-busy={selected !== frame.current && failedImage !== selected}>
              <div className="itinerary-image">
                <motion.div className="itinerary-image-parallax" style={{ y: reduced ? 0 : photoY }}>
                  {stops.map((item, index) => {
                    const active = index === frame.current;
                    const underneath = index === frame.previous;
                    return (
                      <motion.div
                        className="itinerary-image-layer"
                        key={item.image}
                        aria-hidden={!active}
                        initial={false}
                        style={{ zIndex: active ? 2 : underneath ? 1 : 0 }}
                        animate={{
                          opacity: active || underneath ? 1 : 0,
                          clipPath: active && !reduced
                            ? ["inset(0% 0% 100% 0%)", "inset(0% 0% 0% 0%)"]
                            : active || underneath ? "inset(0% 0% 0% 0%)" : "inset(0% 0% 100% 0%)",
                        }}
                        transition={{ opacity: { duration: 0 }, clipPath: { duration: reduced || !active ? 0 : 0.9, ease: revealEase } }}
                      >
                        <motion.div className="itinerary-image-zoom" initial={false} animate={{ scale: active && !reduced ? [1.13, 1] : 1 }} transition={{ duration: reduced || !active ? 0 : 1.15, ease: revealEase }}>
                          <Image src={item.image} alt={active ? item.alt : ""} fill loading={selected === index && selected !== 0 ? "eager" : "lazy"} sizes="(max-width: 760px) 760px, (max-width: 1480px) calc(100vw - 160px), 1320px" style={{ objectPosition: item.position }} onLoad={() => imageReady(index)} onError={() => imageFailed(index)} />
                        </motion.div>
                      </motion.div>
                    );
                  })}
                </motion.div>
              </div>
              <figcaption>{"credit" in stop ? <><a href={stop.credit} target="_blank" rel="noreferrer">Pradum Shukla / Wikimedia Commons</a> · <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noreferrer">CC BY 4.0</a></> : stop.caption}</figcaption>
              <span className="itinerary-image-status" role="status">{failedImage === selected ? "This photograph could not load." : ""}</span>
            </figure>
          </div>
        </div>
        {compact && <div className="itinerary-more"><Link className="itinerary-link" href="/varanasi">See the Varanasi guide <ArrowUpRight size={19} aria-hidden="true" /></Link></div>}
      </div>
    </section>
  );
}
