"use client";

import { useEffect, useRef, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { ChevronRight } from "lucide-react";
import { rooms } from "@/content/hotel";
import { localToday, nextDate, validateEnquiry, type EnquiryErrors } from "@/lib/booking";
import { stayQuery } from "@/lib/stay-query";
import "./booking-dock.css";

/** Always within reach; the hotel confirms availability through the enquiry. */
export function BookingDock() {
  const router = useRouter();
  const pathname = usePathname();
  const dock = useRef<HTMLElement>(null);
  const [arrival, setArrival] = useState("");
  const [departure, setDeparture] = useState("");
  const [errors, setErrors] = useState<EnquiryErrors>({});
  const selectedRoom = rooms.find(room => pathname === `/rooms/${room.slug}`)?.slug || "";

  useEffect(() => {
    const element = dock.current;
    if (!element) return;
    const observer = new ResizeObserver(([entry]) => {
      document.documentElement.style.setProperty("--booking-dock-height", `${Math.ceil(entry.borderBoxSize[0]?.blockSize || element.offsetHeight)}px`);
    });
    observer.observe(element);
    return () => observer.disconnect();
  }, []);

  return <aside ref={dock} className="booking-dock" aria-label="Check room availability">
    <form className="booking-dock-inner" noValidate onSubmit={event => {
      event.preventDefault();
      const values = Object.fromEntries(new FormData(event.currentTarget));
      // The enquiry may contain newer preferences than its URL. Read only the
      // travel fields so a date change never exports a guest's name or notes.
      const enquiry = pathname === "/contact"
        ? document.querySelector<HTMLFormElement>(".booking-form")
        : null;
      const current = enquiry ? new FormData(enquiry) : null;
      const room = current
        ? rooms.find(item => item.name === current.get("room"))?.slug || ""
        : selectedRoom;
      const data = {
        arrival, departure, adults: String(values.adults || "2"),
        children: String(current?.get("children") ?? "0"),
        room, roomCount: String(current?.get("roomCount") ?? "1"), name: "", notes: "",
      };
      const validation = validateEnquiry(data, localToday());
      setErrors(validation);
      if (Object.keys(validation).length) {
        const name = Object.keys(validation)[0];
        (event.currentTarget.elements.namedItem(name) as HTMLElement | null)?.focus();
        return;
      }
      router.push(`/contact?${stayQuery(data)}#enquire`);
    }}>
      <div className="booking-dock-copy"><strong>Your stay at Augusto.</strong><span>Availability confirmed on WhatsApp.</span></div>
      <div className="booking-dock-fields">
        <div className="dock-date"><label htmlFor="dock-arrival">Check-in</label><input id="dock-arrival" name="arrival" type="date" required value={arrival} aria-invalid={!!errors.arrival} aria-describedby={errors.arrival ? "dock-error" : undefined} onFocus={event => { event.currentTarget.min = localToday(); }} onChange={event => {
          const value = event.target.value;
          setArrival(value);
          if (value && (!departure || departure <= value)) setDeparture(nextDate(value));
          setErrors({});
        }}/></div>
        <div className="dock-date"><label htmlFor="dock-departure">Check-out</label><input id="dock-departure" name="departure" type="date" required value={departure} min={arrival ? nextDate(arrival) : undefined} aria-invalid={!!errors.departure} aria-describedby={errors.departure ? "dock-error" : undefined} onChange={event => { setDeparture(event.target.value); setErrors({}); }}/></div>
        <div className="dock-guests"><label htmlFor="dock-adults">Adults</label><select id="dock-adults" name="adults" defaultValue="2" aria-label="Adults">{Array.from({length:8},(_,index)=><option key={index} value={index+1}>{index+1} adult{index ? "s" : ""}</option>)}</select></div>
        <button type="submit" className="button dock-submit" style={{color:"var(--paper)"}}>Check availability <ChevronRight size={18}/></button>
      </div>
      {Object.keys(errors).length > 0 && <p className="dock-error" id="dock-error" role="alert">{Object.values(errors)[0]}</p>}
    </form>
  </aside>;
}
