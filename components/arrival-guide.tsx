"use client";

import Image from "next/image";
import { useId, useRef, useState, type KeyboardEvent } from "react";
import { ArrowUpRight, Check, Copy, MapPin } from "lucide-react";
import { hotel } from "@/content/hotel";
import { arrivalModes } from "@/content/hospitality";
import "./arrival-guide.css";

interface ArrivalGuideProps {
  title?: string;
  className?: string;
}

export function ArrivalGuide({
  title = "Find your way to Augusto.",
  className = "",
}: ArrivalGuideProps) {
  const id = useId();
  const [active, setActive] = useState(0);
  const [mapLoaded, setMapLoaded] = useState(false);
  const [copyState, setCopyState] = useState<"idle" | "copied" | "unavailable">("idle");
  const tabs = useRef<Array<HTMLButtonElement | null>>([]);
  const mode = arrivalModes[active];
  const address = `${hotel.name}, ${hotel.address.join(", ")}`;
  const enquiry = `https://wa.me/${hotel.whatsappNumber}?text=${encodeURIComponent(mode.message)}`;
  const mapUrl = `https://www.google.com/maps?q=${encodeURIComponent(address)}&z=17&output=embed`;

  async function copyAddress() {
    try {
      await navigator.clipboard.writeText(address);
      setCopyState("copied");
    } catch {
      setCopyState("unavailable");
    }
  }

  function moveTab(event: KeyboardEvent<HTMLButtonElement>, index: number) {
    let next = index;
    if (event.key === "ArrowRight") next = (index + 1) % arrivalModes.length;
    else if (event.key === "ArrowLeft") next = (index - 1 + arrivalModes.length) % arrivalModes.length;
    else if (event.key === "Home") next = 0;
    else if (event.key === "End") next = arrivalModes.length - 1;
    else return;
    event.preventDefault();
    setActive(next);
    tabs.current[next]?.focus();
  }

  return (
    <section className={`arrival-guide ${className}`} aria-labelledby={`${id}-title`}>
      <div className="arrival-guide-heading">
        <p className="arrival-guide-kicker">Getting here</p>
        <h2 id={`${id}-title`}>{title}</h2>
        <p>August Kunda Road, Godowlia. A little planning for the final part of your journey.</p>
      </div>
      <div className="arrival-guide-grid">
        <div className="arrival-guide-planning">
          <div className="arrival-guide-tabs" role="tablist" aria-label="How are you arriving?">
            {arrivalModes.map((item, index) => (
              <button key={item.id} type="button" role="tab"
                id={`${id}-${item.id}-tab`} aria-controls={`${id}-${item.id}-panel`}
                aria-selected={active === index} tabIndex={active === index ? 0 : -1}
                ref={(element) => { tabs.current[index] = element; }}
                onKeyDown={(event) => moveTab(event, index)}
                onClick={() => setActive(index)}>
                {item.label}
              </button>
            ))}
          </div>
          {arrivalModes.map((item, index) => (
            <div key={item.id} role="tabpanel" id={`${id}-${item.id}-panel`}
              aria-labelledby={`${id}-${item.id}-tab`} hidden={active !== index}
              className="arrival-guide-panel">
              <h3>{item.title}</h3>
              {item.paragraphs.map((paragraph) => <p key={paragraph}>{paragraph}</p>)}
            </div>
          ))}
          <div className="arrival-guide-actions">
            <a href={enquiry} target="_blank" rel="noopener noreferrer" className="arrival-guide-enquire">
              Ask about your arrival <ArrowUpRight size={18} aria-hidden="true" />
            </a>
            <a href={hotel.phoneHref} className="arrival-guide-phone">Call {hotel.phone}</a>
          </div>
        </div>
        <div className="arrival-guide-location">
          <div className="arrival-guide-map">
            {mapLoaded ? (
              <iframe src={mapUrl} title="Hotel Augusto location on Google Maps"
                loading="lazy" referrerPolicy="strict-origin-when-cross-origin" allowFullScreen />
            ) : (
              <>
                <Image src="/images/hotel-exterior-day.webp"
                  alt="Hotel Augusto’s entrance and sign on August Kunda Road"
                  fill sizes="(max-width: 760px) 100vw, 50vw" />
                <button type="button" className="arrival-guide-map-load" onClick={() => setMapLoaded(true)}>
                  <MapPin size={18} aria-hidden="true" /> Load Google map
                </button>
              </>
            )}
          </div>
          <div className="arrival-guide-address">
            <div>
              <p className="arrival-guide-landmark">Opposite State Bank of India</p>
              <address><strong>{hotel.name}</strong>{hotel.address.map((line) => <span key={line}>{line}</span>)}</address>
            </div>
            <button type="button" className="arrival-guide-copy" onClick={copyAddress}>
              {copyState === "copied" ? <Check size={17} aria-hidden="true" /> : <Copy size={17} aria-hidden="true" />}
              {copyState === "copied" ? "Copied" : "Copy address"}
            </button>
          </div>
          <p className="arrival-guide-copy-status" aria-live="polite">
            {copyState === "copied" ? "Hotel address copied." : copyState === "unavailable" ? "Please select and copy the address above." : ""}
          </p>
          <div className="arrival-guide-map-links">
            <a href={hotel.mapsUrl} target="_blank" rel="noopener noreferrer">Open directions <ArrowUpRight size={17} aria-hidden="true" /></a>
            <span>{mapLoaded ? "Interactive map provided by Google." : "The interactive map loads only when you choose."}</span>
          </div>
        </div>
      </div>
    </section>
  );
}
