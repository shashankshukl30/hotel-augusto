"use client";

import Image from "next/image";
import { useRef, useState } from "react";
import { ArrowLeft, ArrowRight, Expand, X } from "lucide-react";
import type { RoomPhotograph } from "@/content/room-images";

export function RoomPhotographs({ images, roomName }: { images: RoomPhotograph[]; roomName: string }) {
  const [selected, setSelected] = useState(0);
  const dialog = useRef<HTMLDialogElement>(null);
  const opener = useRef<HTMLButtonElement | null>(null);
  const touch = useRef<{ x: number; y: number } | null>(null);
  const photograph = images[selected];
  const change = (direction: number) => setSelected(current => (current + direction + images.length) % images.length);

  return <section className="room-photographs" aria-label={`${roomName} photographs`}>
    <div className="room-photo-layout">
      <button type="button" className="room-photo-main" aria-label={`View larger photograph: ${photograph.caption}`}
        onClick={event => { opener.current = event.currentTarget; dialog.current?.showModal(); }}
        onKeyDown={event => {
          if (event.key === "ArrowRight") { event.preventDefault(); change(1); }
          if (event.key === "ArrowLeft") { event.preventDefault(); change(-1); }
        }}>
        {images.map((image, index) => <span className="room-photo-layer" key={image.src} aria-hidden={index !== selected} style={{ opacity: index === selected ? 1 : 0 }}>
          <Image src={image.src} alt={index === selected ? image.alt : ""} fill preload={index === 0} sizes="(max-width: 760px) 100vw, 90vw" quality={85}/>
        </span>)}
        <span className="room-photo-expand"><Expand size={18}/><span>View larger</span></span>
      </button>
      <div className="room-photo-thumbnails" role="group" aria-label="Choose a room photograph">
        {images.map((image, index) => <button type="button" key={image.src} aria-label={`Show photograph ${index + 1}: ${image.caption}`} aria-pressed={index === selected} onClick={() => setSelected(index)}>
          <Image src={image.src} alt="" fill sizes="(max-width: 760px) 72px, 86px" quality={75}/><span aria-hidden="true" className="room-thumbnail-mark"/>
        </button>)}
      </div>
    </div>
    <div className="room-photo-toolbar"><p className="room-photo-caption" aria-live="polite">{photograph.caption}</p><div className="room-photo-controls"><span aria-live="polite">{selected + 1} / {images.length}</span>
      <button type="button" aria-label="Previous room photograph" onClick={() => change(-1)}><ArrowLeft size={20}/></button>
      <button type="button" aria-label="Next room photograph" onClick={() => change(1)}><ArrowRight size={20}/></button>
    </div></div>
    <dialog ref={dialog} className="room-photo-dialog" aria-label={`${roomName} photograph viewer`}
      onClose={() => opener.current?.focus()}
      onClick={event => { if (event.target === event.currentTarget) dialog.current?.close(); }}
      onKeyDown={event => {
        if (event.key === "ArrowRight") { event.preventDefault(); change(1); }
        if (event.key === "ArrowLeft") { event.preventDefault(); change(-1); }
        if (event.key === "Tab") {
          const controls = dialog.current?.querySelectorAll<HTMLButtonElement>("button");
          const first = controls?.[0];
          const last = controls?.[controls.length - 1];
          if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
          if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
        }
      }}>
      <div className="room-viewer-top"><span>{roomName}</span><button type="button" aria-label="Close room photograph viewer" onClick={() => dialog.current?.close()} autoFocus><X size={24}/></button></div>
      <div className="room-viewer-image" onTouchStart={event => { touch.current = { x: event.touches[0].clientX, y: event.touches[0].clientY }; }} onTouchEnd={event => {
        if (!touch.current) return;
        const x = event.changedTouches[0].clientX - touch.current.x;
        const y = event.changedTouches[0].clientY - touch.current.y;
        if (Math.abs(x) > 55 && Math.abs(x) > Math.abs(y) * 1.3) change(x < 0 ? 1 : -1);
        touch.current = null;
      }}><Image src={photograph.src} alt={photograph.alt} fill sizes="94vw" quality={85}/></div>
      <div className="room-viewer-bottom"><p aria-live="polite">{photograph.caption}</p><div className="room-photo-controls"><span aria-live="polite">{selected + 1} / {images.length}</span>
        <button type="button" aria-label="Previous enlarged room photograph" onClick={() => change(-1)}><ArrowLeft size={21}/></button>
        <button type="button" aria-label="Next enlarged room photograph" onClick={() => change(1)}><ArrowRight size={21}/></button>
      </div></div>
    </dialog>
  </section>;
}
