"use client";

import { useEffect, useRef, useState } from "react";
import { ArrowUpRight, Check } from "lucide-react";
import { hotel, rooms } from "@/content/hotel";
import { buildWhatsAppUrl, localToday, nextDate, validateEnquiry, type Enquiry, type EnquiryErrors } from "@/lib/booking";
import { readStayQuery } from "@/lib/stay-query";
import { WhatsAppIcon } from "./whatsapp-icon";
import { DateField } from "./date-field";
import "./booking-form.css";

export function BookingForm({ room = "", query }: { room?: string; query?: string }) {
  const form = useRef<HTMLFormElement>(null);
  const [errors, setErrors] = useState<EnquiryErrors>({});
  const [draft, setDraft] = useState<string | null>(null);
  const initialStay = readStayQuery(new URLSearchParams(query || ""), rooms.map(item => item.slug));
  const [arrival, setArrival] = useState(initialStay.arrival);
  const [departure, setDeparture] = useState(initialStay.departure);
  const queryKey = `${room}\0${query ?? ""}`;
  const [previousQuery, setPreviousQuery] = useState(queryKey);
  // Reset derived feedback before rendering a new selection. The form remains
  // mounted, preserving private, uncontrolled name and notes fields.
  if (previousQuery !== queryKey) {
    setPreviousQuery(queryKey);
    setErrors({});
    setDraft(null);
    setArrival(initialStay.arrival);
    setDeparture(initialStay.departure);
  }
  useEffect(() => {
    const element = form.current;
    if (!element) return;
    const stay = readStayQuery(new URLSearchParams(query ?? window.location.search), rooms.map(item => item.slug));
    const selected = rooms.find(item => item.slug === stay.room);
    const select = element.querySelector<HTMLSelectElement>("#room");
    if (select) select.value = selected?.name || room;
    for (const name of ["adults", "children", "roomCount"] as const) {
      const field = element.elements.namedItem(name) as HTMLInputElement | HTMLSelectElement | null;
      if (field) field.value = stay[name] || "";
    }
  }, [query, room]);
  const error = (field: keyof Enquiry) => errors[field] ? <span className="field-error" id={`${field}-error`}>{errors[field]}</span> : null;
  return <form ref={form} className="booking-form" noValidate onChange={() => { if (draft) setDraft(null); }} onSubmit={(event) => {
    event.preventDefault();
    const fields = new FormData(event.currentTarget);
    const data = Object.fromEntries(fields) as Enquiry;
    const validation = validateEnquiry(data, localToday());
    setErrors(validation);
    if (Object.keys(validation).length) {
      const key = Object.keys(validation)[0];
      (event.currentTarget.elements.namedItem(key) as HTMLElement | null)?.focus();
      return;
    }
    setDraft(buildWhatsAppUrl(hotel.whatsappNumber, data));
    window.requestAnimationFrame(() => form.current?.querySelector<HTMLElement>("#whatsapp-draft")?.focus());
  }}>
    <div className="form-heading"><h3>Plan your stay.</h3><p>Share a few details. We’ll prepare your enquiry to send directly to the hotel on WhatsApp.</p></div>
    <div className="booking-fields">
      <div className="form-field"><label htmlFor="arrival">Arrival <span>*</span></label><DateField id="arrival" name="arrival" label="Arrival date" minToday required value={arrival} onValueChange={value => { setArrival(value); setDraft(null); setErrors({}); }} aria-invalid={!!errors.arrival} aria-describedby={errors.arrival ? "arrival-error" : undefined}/>{error("arrival")}</div>
      <div className="form-field"><label htmlFor="departure">Departure <span>*</span></label><DateField id="departure" name="departure" label="Departure date" required value={departure} min={arrival ? nextDate(arrival) : undefined} onValueChange={value => { setDeparture(value); setDraft(null); setErrors({}); }} aria-invalid={!!errors.departure} aria-describedby={errors.departure ? "departure-error" : undefined}/>{error("departure")}</div>
      <div className="form-field"><label htmlFor="adults">Adults <span>*</span></label><select id="adults" name="adults" defaultValue="2" aria-invalid={!!errors.adults}>{Array.from({length:8},(_,i)=>i+1).map(n=><option value={n} key={n}>{n} adult{n===1?"":"s"}</option>)}</select>{error("adults")}</div>
      <div className="form-field"><label htmlFor="children">Children</label><select id="children" name="children" defaultValue="0" aria-invalid={!!errors.children}>{Array.from({length:7},(_,i)=>i).map(n=><option value={n} key={n}>{n===0?"No children":`${n} ${n===1?"child":"children"}`}</option>)}</select>{error("children")}</div>
      <div className="form-field full-field"><label htmlFor="room">Your room preference</label><select id="room" name="room" defaultValue={room}><option value="">Help me choose</option>{rooms.map(item=><option key={item.slug} value={item.name}>{item.name}</option>)}</select></div>
      <div className="form-field full-field"><label htmlFor="roomCount">Rooms requested</label><select id="roomCount" name="roomCount" defaultValue="1" aria-invalid={!!errors.roomCount}>{Array.from({length:8},(_,index)=><option key={index} value={index+1}>{index+1} room{index ? "s" : ""}</option>)}</select>{error("roomCount")}</div>
      <div className="form-field full-field"><label htmlFor="name">Your name <span className="optional">optional</span></label><input type="text" id="name" name="name" autoComplete="name" maxLength={80} placeholder="How should we address you?"/>{error("name")}</div>
      <div className="form-field full-field"><label htmlFor="notes">Anything else? <span className="optional">optional</span></label><textarea id="notes" name="notes" rows={3} maxLength={600} placeholder="Arrival time, children’s ages, or a special request…"/>{error("notes")}</div>
    </div>
    {Object.keys(errors).length > 0 && <p role="alert" className="form-error-summary">Please check the highlighted details above.</p>}
    {draft ? <div className="booking-draft" aria-live="polite"><p><Check size={16}/> Your enquiry is ready.</p><a id="whatsapp-draft" href={draft} target="_blank" rel="noopener noreferrer" className="button" style={{color:"var(--paper)"}}><WhatsAppIcon/> Open WhatsApp & send <ArrowUpRight size={18}/></a><p className="draft-note">WhatsApp will open with your details. Tap Send there to reach the hotel.</p></div> : <button type="submit" className="button booking-submit" style={{color:"var(--paper)"}}><WhatsAppIcon/> Prepare WhatsApp enquiry <ArrowUpRight size={18}/></button>}
    <p className="form-footnote">This is an enquiry, not a confirmed reservation. The hotel will confirm availability, rates and booking terms. Your details are not stored on this website.</p>
  </form>;
}
