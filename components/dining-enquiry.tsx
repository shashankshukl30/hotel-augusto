"use client";

import { useRef, useState } from "react";
import { ArrowUpRight, Check } from "lucide-react";
import { hotel } from "@/content/hotel";
import { localToday } from "@/lib/booking";
import { buildDiningWhatsAppUrl, diningInterests, validateDiningEnquiry, type DiningEnquiry as DiningData, type DiningErrors } from "@/lib/dining-enquiry";
import { WhatsAppIcon } from "./whatsapp-icon";
import "./dining-enquiry.css";

export function DiningEnquiry() {
  const [errors, setErrors] = useState<DiningErrors>({});
  const [draft, setDraft] = useState<string | null>(null);
  const [today, setToday] = useState("");
  const draftLink = useRef<HTMLAnchorElement>(null);
  const error = (field: keyof DiningData) => errors[field] ? <span id={`dining-${field}-error`} className="dining-field-error">{errors[field]}</span> : null;

  return <form className="dining-enquiry-form" noValidate aria-label="Dining enquiry" onChange={() => { if (draft) setDraft(null); }} onSubmit={(event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const fields = new FormData(form);
    const data = Object.fromEntries(fields) as DiningData;
    const validation = validateDiningEnquiry(data, localToday());
    setErrors(validation);
    if (Object.keys(validation).length) {
      const first = form.elements.namedItem(Object.keys(validation)[0]);
      if (first instanceof HTMLElement) first.focus();
      return;
    }
    setDraft(buildDiningWhatsAppUrl(hotel.whatsappNumber, data));
    window.requestAnimationFrame(() => draftLink.current?.focus());
  }}>
    <div className="dining-form-fields">
      <div className="dining-field dining-field-wide"><label htmlFor="dining-interest">What are you planning?</label><select id="dining-interest" name="interest" defaultValue={diningInterests[0]} aria-invalid={!!errors.interest} aria-describedby={errors.interest ? "dining-interest-error" : undefined}>{diningInterests.map(interest => <option key={interest}>{interest}</option>)}</select>{error("interest")}</div>
      <div className="dining-field"><label htmlFor="dining-date">Preferred date <span aria-hidden="true">*</span></label><input id="dining-date" name="date" type="date" required min={today || undefined} onFocus={() => setToday(localToday())} aria-invalid={!!errors.date} aria-describedby={errors.date ? "dining-date-error" : undefined} />{error("date")}</div>
      <div className="dining-field"><label htmlFor="dining-guests">People in your party <span aria-hidden="true">*</span></label><input id="dining-guests" name="guests" type="number" inputMode="numeric" min={1} max={99} step={1} required defaultValue={2} aria-invalid={!!errors.guests} aria-describedby={errors.guests ? "dining-guests-error" : undefined} />{error("guests")}</div>
      <div className="dining-field dining-field-wide"><label htmlFor="dining-name">Your name <span>optional</span></label><input id="dining-name" name="name" type="text" autoComplete="name" maxLength={80} aria-invalid={!!errors.name} aria-describedby={errors.name ? "dining-name-error" : undefined} />{error("name")}</div>
      <div className="dining-field dining-field-wide"><label htmlFor="dining-notes">Anything to add? <span>optional</span></label><textarea id="dining-notes" name="notes" rows={3} maxLength={600} placeholder="Preferred time, your room plan, or a dietary request…" aria-invalid={!!errors.notes} aria-describedby={errors.notes ? "dining-notes-error" : undefined} />{error("notes")}</div>
    </div>
    {Object.keys(errors).length > 0 && <p role="alert" className="dining-field-error">Please check the highlighted details.</p>}
    {draft ? <div className="dining-form-draft" aria-live="polite"><p><Check size={19} aria-hidden="true" /> Your dining enquiry is ready.</p><a ref={draftLink} href={draft} target="_blank" rel="noopener noreferrer" className="button" style={{ color: "var(--paper)" }}><WhatsAppIcon size={20} />Open WhatsApp <ArrowUpRight size={18} aria-hidden="true" /></a><p>Review the message in WhatsApp, then tap Send.</p></div> : <button type="submit" className="button dining-form-submit" style={{ color: "var(--paper)" }}><WhatsAppIcon size={20} />Prepare dining enquiry <ArrowUpRight size={18} aria-hidden="true" /></button>}
    <p className="dining-form-note">The hotel will confirm your dining arrangements, menu and charges. Your details are not saved on this website. <a href="/privacy">Privacy</a></p>
  </form>;
}
