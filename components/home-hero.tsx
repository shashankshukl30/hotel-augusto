"use client";

import Image from "next/image";
import Link from "next/link";
import { useEffect, useRef, useState, useSyncExternalStore } from "react";
import { animate, motion, stagger, useAnimate, useMotionValue, useScroll, useSpring, useTransform } from "framer-motion";
import { ArrowDown, ArrowUpRight, ChevronRight, Pause, Play } from "lucide-react";
import { useMotionPreference } from "./use-motion-preference";
import { HeroTitle } from "./hero-title";
import { hotel } from "@/content/hotel";
import "./home-hero.css";

const scenes = [
  { src:"/images/deluxe-room-blue.webp", alt:"A double-bed room at Hotel Augusto with warm wood finishes and blue upholstery", detail:"Guest rooms", label:"Rooms", position:"50% 60%" },
  { src:"/images/hotel-lounge.webp", alt:"Hotel Augusto's lounge with carved stone panels, seating and a lift entrance", detail:"The hotel lounge", label:"Lounge", position:"50% 55%" },
  { src:"/images/dining-room-wide.webp", alt:"The vegetarian restaurant at Hotel Augusto, Varanasi", detail:"Vegetarian dining", label:"Dining", position:"50% 50%" },
];

function subscribePageVisibility(callback: () => void) {
  document.addEventListener("visibilitychange", callback);
  return () => document.removeEventListener("visibilitychange", callback);
}
const pageIsVisible = () => document.visibilityState === "visible";
const serverPageIsVisible = () => true;

export function HomeHero() {
  const [selected, setSelected] = useState(0);
  const [requested, setRequested] = useState(0);
  const [readyScenes, setReadyScenes] = useState<number[]>([]);
  const [paused, setPaused] = useState(false);
  const [hovered, setHovered] = useState(false);
  const [focused, setFocused] = useState(false);
  const [visible, setVisible] = useState(true);
  const [firstPhotoReady, setFirstPhotoReady] = useState(false);
  const reduced = useMotionPreference();
  const pageVisible = useSyncExternalStore(subscribePageVisibility, pageIsVisible, serverPageIsVisible);
  const [scene, animateEntrance] = useAnimate<HTMLElement>();
  const requestMode = useRef<"auto" | "manual">("auto");
  const photoPlayback = useRef<ReturnType<typeof animate> | null>(null);
  const photoProgress = useMotionValue(0);
  const { scrollYProgress } = useScroll({ target:scene, offset:["start start","end start"] });
  const scrollScale = useTransform(scrollYProgress,[0,1],[1.035,1.09]);
  const driftX = useSpring(0, {stiffness:65,damping:24});
  const driftY = useSpring(0, {stiffness:65,damping:24});
  const scale = useTransform(() => scrollScale.get() + photoProgress.get() * .065);
  const panX = useTransform(() => driftX.get() - photoProgress.get() * 14);
  const panY = useTransform(() => driftY.get() + photoProgress.get() * 6);
  const canAnimate = !reduced && !paused && !hovered && !focused && visible && pageVisible && firstPhotoReady;
  useEffect(() => {
    if (reduced || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const imageEntrance = animateEntrance(".hero-image-entrance", {
      clipPath: ["inset(5% 3% 5% 3% round 24px)", "inset(0% 0% 0% 0% round 0px)"],
    }, { duration: 1.25, ease: [.16, 1, .3, 1] });
    const detailsEntrance = animateEntrance(".hero-entrance-detail", { y: [20, 0], opacity: [.2, 1] }, {
      duration: .75, delay: stagger(.12, { startDelay: .24 }), ease: [.16, 1, .3, 1],
    });
    return () => { imageEntrance.stop(); detailsEntrance.stop(); };
  }, [animateEntrance, reduced]);
  useEffect(() => {
    // One continuous motion value avoids per-frame React renders and resumes
    // from its current position after interaction or a hidden browser tab.
    const playback = animate(photoProgress, [0, 1], {
      duration: 16, ease: "easeInOut", repeat: Infinity, repeatType: "reverse", autoplay: false,
    });
    photoPlayback.current = playback;
    return () => {
      playback.stop();
      photoPlayback.current = null;
    };
  }, [photoProgress]);
  useEffect(() => {
    if (canAnimate && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) photoPlayback.current?.play();
    else photoPlayback.current?.pause();
  }, [canAnimate]);
  useEffect(() => {
    const target = scene.current;
    if (!target) return;
    const observer = new IntersectionObserver(([entry]) => setVisible(entry.isIntersecting), { threshold:.1 });
    observer.observe(target);
    return () => observer.disconnect();
  }, [scene]);
  useEffect(() => {
    if (!canAnimate) return;
    const interval = window.setInterval(() => {
      const next = (selected + 1) % scenes.length;
      requestMode.current = "auto";
      setRequested(next);
      if (readyScenes.includes(next)) setSelected(next);
    }, 8000);
    return () => window.clearInterval(interval);
  }, [canAnimate, selected, readyScenes]);
  return <section ref={scene} className="home-hero" aria-roledescription="carousel" aria-label="Welcome to Hotel Augusto" onPointerOver={event => {
    if (event.pointerType === "mouse") setHovered(event.target instanceof Element && !!event.target.closest("a,button"));
  }} onPointerLeave={() => setHovered(false)} onPointerDownCapture={() => setFocused(false)} onFocusCapture={event => {
    // Mouse-clicked Play should resume when the pointer leaves its control;
    // keyboard focus pauses independently until it leaves the carousel.
    setFocused(event.target instanceof HTMLElement && event.target.matches(":focus-visible"));
  }} onKeyDownCapture={() => setFocused(true)} onBlurCapture={event => { if (!event.currentTarget.contains(event.relatedTarget)) setFocused(false); }}>
    <div className="hero-media" onPointerMove={event => {
      if (reduced || event.pointerType !== "mouse") return;
      const box = event.currentTarget.getBoundingClientRect();
      driftX.set(((event.clientX-box.left)/box.width-.5)*-16);
      driftY.set(((event.clientY-box.top)/box.height-.5)*-10);
    }} onPointerLeave={() => { driftX.set(0); driftY.set(0); }}>
      <div className="hero-image-entrance">
      <motion.div className="hero-photographs" style={{ scale:reduced ? 1 : scale, x:reduced ? 0 : panX, y:reduced ? 0 : panY }}>
        {scenes.map((photo,index) => <motion.div className="hero-photo" key={photo.src} aria-hidden={selected !== index} initial={false} animate={{ opacity:selected === index ? 1 : 0 }} transition={{ duration:reduced ? 0 : .8 }}>
          {(index === 0 || index === selected || index === requested || (firstPhotoReady && !reduced)) && <Image src={photo.src} alt={selected === index ? photo.alt : ""} fill preload={index === 0} loading={index === 0 ? undefined : "eager"} fetchPriority={index === 0 ? "high" : "low"} onLoad={() => {
            setReadyScenes(previous => previous.includes(index) ? previous : [...previous, index]);
            if (index === 0) setFirstPhotoReady(true);
            if (requested === index && (requestMode.current === "manual" || canAnimate || index === 0)) setSelected(index);
          }} onError={index === 0 ? () => setFirstPhotoReady(true) : undefined} sizes="(max-width:600px) 1200px, 96vw" quality={85} style={{ objectPosition:photo.position }}/>}
        </motion.div>)}
      </motion.div>
      </div>
      <div className="hero-photo-shade" aria-hidden="true"/>
      <div className="hero-topline"><span>Hotel Augusto</span><a href={hotel.mapsUrl} target="_blank" rel="noopener noreferrer">Godowlia, Varanasi <ArrowUpRight size={16}/></a></div>
      <div className="hero-intro">
        <HeroTitle/>
        <p className="hero-description hero-entrance-detail">
          Comfortable rooms. Vegetarian dining.<br/>The old city, right outside.
        </p>
        <div className="hero-actions hero-entrance-detail">
          <Link href="/rooms" className="button button-light" style={{ color:"var(--ink)" }}>Explore rooms <ArrowUpRight size={18}/></Link><a href="#discover" className="hero-discover" aria-label="Discover Hotel Augusto"><ArrowDown size={20}/></a>
        </div>
      </div>
      <div className="hero-frame-note" aria-hidden="true"><span>{String(selected+1).padStart(2,"0")}</span><i/>03 <span>{scenes[selected].detail}</span></div>
      <div className="hero-scene-controls"><div className="hero-scene-buttons" aria-busy={requested !== selected}>{scenes.map((photo,index) => <button key={photo.src} className={selected === index ? "is-selected" : ""} aria-label={`Show ${photo.detail.toLowerCase()}`} aria-pressed={selected === index} onClick={() => { requestMode.current = "manual"; setRequested(index); if (readyScenes.includes(index)) setSelected(index); setPaused(true); }}>{photo.label}</button>)}</div><button className="hero-pause icon-button" onClick={() => setPaused(!paused)} aria-label={paused ? "Play hotel slideshow" : "Pause hotel slideshow"} aria-pressed={paused} disabled={reduced}>{paused ? <Play size={16}/> : <Pause size={16}/>}</button></div>
    </div>
    <div className="hero-media-footer container">
      <div className="hero-media-info"><span className="hero-photo-description">{scenes[selected].detail} at Hotel Augusto</span><Link className="text-link" href="/gallery">Open the gallery <ChevronRight size={17}/></Link></div>
      <span className="hero-footer-note">A closer look at your stay.</span>
    </div>
  </section>;
}
