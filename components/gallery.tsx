"use client";

import Image from "next/image";
import { useEffect, useRef, useState } from "react";
import { ArrowLeft, ArrowRight, Expand, X } from "lucide-react";

export type GalleryImage = {
  src: string;
  alt: string;
  caption: string;
  category: "Hotel" | "Rooms" | "Dining";
  position?: string;
};

const categories = ["All", "Hotel", "Rooms", "Dining"] as const;
type Category = (typeof categories)[number];

export function Gallery({ images }: { images: GalleryImage[] }) {
  const [category, setCategory] = useState<Category>("All");
  const [selected, setSelected] = useState<number | null>(null);
  const dialog = useRef<HTMLDialogElement>(null);
  const opener = useRef<HTMLButtonElement | null>(null);
  const touchStart = useRef<{ x: number; y: number } | null>(null);
  const visible = images.filter((photo) => category === "All" || photo.category === category);
  const photograph = selected === null ? undefined : visible[selected];

  useEffect(() => {
    if (selected === null) return;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => { document.body.style.overflow = previousOverflow; };
  }, [selected]);

  function openPhoto(index: number, button: HTMLButtonElement) {
    opener.current = button;
    setSelected(index);
    dialog.current?.showModal();
  }

  function changePhoto(direction: number) {
    setSelected((current) => current === null ? null : (current + direction + visible.length) % visible.length);
  }

  function closePhoto() {
    dialog.current?.close();
  }

  return (
    <div className="photo-gallery">
      <div className="gallery-toolbar">
        <div className="gallery-filters" role="group" aria-label="Filter photographs">
          {categories.filter((item) => item === "All" || images.some((photo) => photo.category === item)).map((item) => (
            <button key={item} type="button" aria-pressed={category === item} onClick={() => setCategory(item)}>
              {item}
            </button>
          ))}
        </div>
        <p className="gallery-count" aria-live="polite">{String(visible.length).padStart(2, "0")} photographs</p>
      </div>

      <div className="gallery-grid">
        {visible.map((photo, index) => (
          <button className="gallery-tile" key={photo.src} type="button" aria-label={`${photo.caption} ${photo.category}: enlarge photograph`} onClick={(event) => openPhoto(index, event.currentTarget)}>
            <span className="gallery-image-wrap">
              <Image src={photo.src} alt={photo.alt} fill sizes="(max-width: 760px) 88vw, 43vw" style={{ objectPosition: photo.position }} priority={index === 0} />
              <span className="gallery-expand" aria-hidden="true"><Expand size={18} strokeWidth={1.5} /></span>
            </span>
            <span className="gallery-caption"><span>{photo.caption}</span>{" "}<span>{photo.category}</span></span>
          </button>
        ))}
      </div>

      <dialog
        ref={dialog}
        className="gallery-dialog"
        aria-label="Hotel Augusto photograph viewer"
        onClose={() => { setSelected(null); opener.current?.focus(); }}
        onClick={(event) => { if (event.target === event.currentTarget) closePhoto(); }}
        onKeyDown={(event) => {
          if (event.key === "ArrowRight") { event.preventDefault(); changePhoto(1); }
          if (event.key === "ArrowLeft") { event.preventDefault(); changePhoto(-1); }
          if (event.key === "Tab") {
            const controls = dialog.current?.querySelectorAll<HTMLButtonElement>("button:not([disabled])");
            const first = controls?.[0];
            const last = controls?.[controls.length - 1];
            if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
            if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
          }
        }}
      >
        <div className="lightbox-shell">
          <div className="lightbox-topline">
            <span className="lightbox-brand">Hotel Augusto</span>
            <button className="lightbox-icon" type="button" onClick={closePhoto} aria-label="Close photograph viewer" autoFocus><X size={24} strokeWidth={1.5} /></button>
          </div>
          <div
            className="lightbox-image"
            onTouchStart={(event) => { const touch = event.touches[0]; touchStart.current = { x: touch.clientX, y: touch.clientY }; }}
            onTouchEnd={(event) => {
              if (!touchStart.current) return;
              const touch = event.changedTouches[0];
              const distance = touch.clientX - touchStart.current.x;
              const vertical = touch.clientY - touchStart.current.y;
              if (Math.abs(distance) > 55 && Math.abs(distance) > Math.abs(vertical) * 1.3) changePhoto(distance < 0 ? 1 : -1);
              touchStart.current = null;
            }}
          >
            {photograph && <Image key={photograph.src} src={photograph.src} alt={photograph.alt} fill sizes="(max-width: 800px) 94vw, 90vw" style={{ objectFit: "contain" }} />}
          </div>
          <div className="lightbox-bottomline">
            <div className="lightbox-description" aria-live="polite">
              <span>{photograph?.caption}</span>
              <span>{selected === null ? "" : `${String(selected + 1).padStart(2, "0")} / ${String(visible.length).padStart(2, "0")}`}</span>
            </div>
            <div className="lightbox-navigation">
              <button className="lightbox-icon" type="button" aria-label="Previous photograph" onClick={() => changePhoto(-1)}><ArrowLeft size={22} /></button>
              <button className="lightbox-icon" type="button" aria-label="Next photograph" onClick={() => changePhoto(1)}><ArrowRight size={22} /></button>
            </div>
          </div>
          <p className="lightbox-hint">Use the arrow keys or swipe to explore. Escape closes the viewer.</p>
        </div>
      </dialog>
    </div>
  );
}
