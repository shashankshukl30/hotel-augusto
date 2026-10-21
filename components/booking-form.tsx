"use client";

import { useEffect, useRef, useState } from "react";
import { ArrowUpRight, Check, Mail } from "lucide-react";
import { hotel, rooms } from "@/content/hotel";
import { buildWhatsAppUrl, localToday, nextDate, validateEnquiry, type Enquiry, type EnquiryErrors } from "@/lib/booking";
import { readStayQuery } from "@/lib/stay-query";
import { WhatsAppIcon } from "./whatsapp-icon";
import { DateField } from "./date-field";
import { validateReplyDetails, type ReplyErrors } from "@/lib/enquiry-email";
import { useEmailEnquiry } from "./use-email-enquiry";
import { EmailConsent, EmailFeedback, EnquiryHoneypot, ReplyFields } from "./email-enquiry-fields";
import "./booking-form.css";

export function BookingForm({ room = "", query }: { room?: string; query?: string }) {
  const form = useRef<HTMLFormElement>(null);
  const [errors, setErrors] = useState<EnquiryErrors & ReplyErrors>({});
  const delivery = useEmailEnquiry();
  const { reset: resetEmail } = delivery;
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
    resetEmail();
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
  }, [query, room, resetEmail]);
  const error = (field: keyof Enquiry) => errors[field] ? <span className="field-error" id={`${field}-error`}>{errors[field]}</span> : null;
  return <form ref={form} className="booking-form" noValidate aria-busy={delivery.pending} onChange={() => { if (draft) setDraft(null); if (!delivery.pending) resetEmail(); }} onSubmit={async (event) => {
    event.preventDefault();
    if (delivery.pending) return;
    const whatsapp = (event.nativeEvent as SubmitEvent).submitter?.getAttribute("value") === "whatsapp";
    if (!whatsapp && delivery.status === "accepted") return;
    const fields = new FormData(event.currentTarget);
    const data = Object.fromEntries(fields) as Enquiry;
    const reply = { email: String(fields.get("email") ?? ""), phone: String(fields.get("phone") ?? "") };
    const validation = { ...validateEnquiry(data, localToday()), ...(!whatsapp ? validateReplyDetails(reply) : {}) };
    setErrors(validation);
    if (Object.keys(validation).length) {
      const key = Object.keys(validation)[0];
      (event.currentTarget.elements.namedItem(key) as HTMLElement | null)?.focus();
      return;
    }
    if (whatsapp) {
      resetEmail();
      setDraft(buildWhatsAppUrl(hotel.whatsappNumber, data));
      window.requestAnimationFrame(() => form.current?.querySelector<HTMLElement>("#whatsapp-draft")?.focus());
      return;
    }
    setDraft(null);
    await delivery.submit("stay", {
      Name: data.name, Arrival: data.arrival, Departure: data.departure,
      Adults: data.adults, Children: data.children, "Rooms requested": data.roomCount || "1",
      "Room preference": data.room || "Help me choose", Notes: data.notes,
    }, reply, String(fields.get("_honey") ?? ""));
  }}>
    <div className="form-heading"><h3>Plan your stay.</h3><p>Share your dates and a reply email. Send your enquiry to the hotel, or continue on WhatsApp.</p></div>
    <fieldset className="enquiry-inputs" disabled={delivery.pending}>
    <div className="booking-fields">
      <div className="form-field"><label htmlFor="arrival">Arrival <span>*</span></label><DateField id="arrival" name="arrival" label="Arrival date" minToday required value={arrival} onValueChange={value => { setArrival(value); setDraft(null); setErrors({}); resetEmail(); }} aria-invalid={!!errors.arrival} aria-describedby={errors.arrival ? "arrival-error" : undefined}/>{error("arrival")}</div>
      <div className="form-field"><label htmlFor="departure">Departure <span>*</span></label><DateField id="departure" name="departure" label="Departure date" required value={departure} min={arrival ? nextDate(arrival) : undefined} onValueChange={value => { setDeparture(value); setDraft(null); setErrors({}); resetEmail(); }} aria-invalid={!!errors.departure} aria-describedby={errors.departure ? "departure-error" : undefined}/>{error("departure")}</div>
      <div className="form-field"><label htmlFor="adults">Adults <span>*</span></label><select id="adults" name="adults" defaultValue="2" aria-invalid={!!errors.adults}>{Array.from({length:8},(_,i)=>i+1).map(n=><option value={n} key={n}>{n} adult{n===1?"":"s"}</option>)}</select>{error("adults")}</div>
      <div className="form-field"><label htmlFor="children">Children</label><select id="children" name="children" defaultValue="0" aria-invalid={!!errors.children}>{Array.from({length:7},(_,i)=>i).map(n=><option value={n} key={n}>{n===0?"No children":`${n} ${n===1?"child":"children"}`}</option>)}</select>{error("children")}</div>
      <div className="form-field full-field"><label htmlFor="room">Your room preference</label><select id="room" name="room" defaultValue={room}><option value="">Help me choose</option>{rooms.map(item=><option key={item.slug} value={item.name}>{item.name}</option>)}</select></div>
      <div className="form-field full-field"><label htmlFor="roomCount">Rooms requested</label><select id="roomCount" name="roomCount" defaultValue="1" aria-invalid={!!errors.roomCount}>{Array.from({length:8},(_,index)=><option key={index} value={index+1}>{index+1} room{index ? "s" : ""}</option>)}</select>{error("roomCount")}</div>
      <div className="form-field full-field"><label htmlFor="name">Your name <span className="optional">optional</span></label><input type="text" id="name" name="name" autoComplete="name" maxLength={80} placeholder="How should we address you?"/>{error("name")}</div>
      <ReplyFields prefix="booking" errors={errors} fieldClass="form-field full-field"/>
      <div className="form-field full-field"><label htmlFor="notes">Anything else? <span className="optional">optional</span></label><textarea id="notes" name="notes" rows={3} maxLength={600} placeholder="Arrival time, children’s ages, or a special request…"/>{error("notes")}</div>
    </div>
    <EnquiryHoneypot/>
    </fieldset>
    {Object.keys(errors).length > 0 && <p role="alert" className="form-error-summary">Please check the highlighted details above.</p>}
    <EmailConsent/>
    <button type="submit" className="button booking-submit" disabled={delivery.pending || delivery.status === "accepted"} style={{color:"var(--paper)"}}><Mail size={19}/>{delivery.pending ? "Sending…" : delivery.status === "accepted" ? "Enquiry submitted" : "Send enquiry"}<ArrowUpRight size={18}/></button>
    <EmailFeedback status={delivery.status} message={delivery.message}/>
    {draft ? <div className="booking-draft" aria-live="polite"><p><Check size={16}/> Your WhatsApp enquiry is ready.</p><a id="whatsapp-draft" href={draft} target="_blank" rel="noopener noreferrer" className="button" style={{color:"var(--paper)"}}><WhatsAppIcon/> Open WhatsApp & send <ArrowUpRight size={18}/></a><p className="draft-note">WhatsApp will open with your details. Tap Send there to reach the hotel.</p></div> : <button type="submit" name="channel" value="whatsapp" disabled={delivery.pending} className="enquiry-whatsapp-alternative" style={{color:"var(--accent)"}}><WhatsAppIcon size={19}/> Prefer WhatsApp? Prepare a message</button>}
    <p className="form-footnote">This is an enquiry, not a confirmed reservation. The hotel will confirm availability, rates and booking terms.</p>
  </form>;
}
