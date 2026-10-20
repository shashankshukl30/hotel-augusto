"use client";

import { useId, useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowUpRight } from "lucide-react";
import { rooms } from "@/content/hotel";
import { localToday, nextDate, stayNights, validateEnquiry, type Enquiry, type EnquiryErrors } from "@/lib/booking";
import { stayQuery } from "@/lib/stay-query";
import { DateField } from "./date-field";
import "./stay-bar.css";

export function StayBar({ compact = false, room = "" }: { compact?: boolean; room?: string }) {
  const id = useId();
  const router = useRouter();
  const [arrival, setArrival] = useState("");
  const [departure, setDeparture] = useState("");
  const nights = stayNights(arrival, departure);
  const [errors, setErrors] = useState<EnquiryErrors>({});
  return <form className={`stay-bar${compact ? " stay-bar-compact" : ""}`} noValidate onSubmit={event => {
    event.preventDefault();
    const data = { ...Object.fromEntries(new FormData(event.currentTarget)), name: "", notes: "" } as Enquiry;
    const result = validateEnquiry(data, localToday());
    setErrors(result);
    if (Object.keys(result).length) {
      const field = event.currentTarget.elements.namedItem(Object.keys(result)[0]);
      if (field instanceof HTMLElement) field.focus();
      return;
    }
    router.push(`/contact?${stayQuery(data)}#enquire`);
  }}>
    <div className="stay-bar-heading"><span className="eyebrow">Plan your stay.</span><p>Your dates. Your room. Let’s find the right fit.</p></div>
    <div className="stay-fields">
      <div className="stay-field"><label htmlFor={`${id}-arrival`}>Arrival</label><DateField id={`${id}-arrival`} name="arrival" label="Arrival date" minToday required value={arrival} onValueChange={value => { setArrival(value); setErrors({}); }} aria-invalid={!!errors.arrival} aria-describedby={errors.arrival ? `${id}-error` : undefined}/></div>
      <div className="stay-field"><label htmlFor={`${id}-departure`}>Departure</label><DateField id={`${id}-departure`} name="departure" label="Departure date" required value={departure} onValueChange={value => { setDeparture(value); setErrors({}); }} min={arrival ? nextDate(arrival) : undefined} aria-invalid={!!errors.departure} aria-describedby={errors.departure ? `${id}-error` : undefined}/></div>
      <div className="stay-field stay-guests"><label htmlFor={`${id}-adults`}>Guests</label><div><select id={`${id}-adults`} name="adults" defaultValue="2">{Array.from({length:8},(_,i)=><option key={i} value={i+1}>{i+1} adult{i ? "s" : ""}</option>)}</select><select name="children" aria-label="Children" defaultValue="0">{Array.from({length:7},(_,i)=><option key={i} value={i}>{i ? `${i} ${i===1?"child":"children"}` : "No children"}</option>)}</select></div></div>
      <div className="stay-field stay-room"><label htmlFor={`${id}-room`}>Room preference</label><select id={`${id}-room`} name="room" defaultValue={room}><option value="">Help me choose</option>{rooms.map(room=><option key={room.slug} value={room.slug}>{room.name}</option>)}</select></div>
      <div className="stay-field stay-count"><label htmlFor={`${id}-room-count`}>Rooms</label><select id={`${id}-room-count`} name="roomCount" defaultValue="1">{Array.from({length:8},(_,index)=><option key={index} value={index+1}>{index+1} room{index ? "s" : ""}</option>)}</select></div>
      <button className="button stay-submit" type="submit" style={{color:"var(--paper)"}}>Plan my stay <ArrowUpRight size={20}/></button>
    </div>
    {Object.keys(errors).length>0 && <p id={`${id}-error`} className="stay-error" role="alert">{Object.values(errors).join(" ")}</p>}
    <p className="stay-footnote">{nights > 0 && <strong>{nights} night{nights === 1 ? "" : "s"}. </strong>}Enquire directly with the hotel. Availability and rates confirmed on WhatsApp.</p>
  </form>;
}
