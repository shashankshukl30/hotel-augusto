"use client";

import { useId, useRef, useState } from "react";
import { ArrowUpRight, Check, Mail } from "lucide-react";
import { hotel, rooms } from "@/content/hotel";
import {
  buildWhatsAppUrl, localToday, nextDate, stayNights, validateEnquiry,
  type Enquiry, type EnquiryErrors,
} from "@/lib/booking";
import { WhatsAppIcon } from "./whatsapp-icon";
import { DateField } from "./date-field";
import { validateReplyDetails, type ReplyErrors } from "@/lib/enquiry-email";
import { useEmailEnquiry } from "./use-email-enquiry";
import { EmailConsent, EmailFeedback, EnquiryHoneypot, ReplyFields } from "./email-enquiry-fields";

type GroupErrors = EnquiryErrors & ReplyErrors & { company?: string };
type Draft = { href: string; message: string };

export function GroupEnquiry() {
  const id = useId();
  const [arrival, setArrival] = useState("");
  const [departure, setDeparture] = useState("");
  const [errors, setErrors] = useState<GroupErrors>({});
  const delivery = useEmailEnquiry();
  const [draft, setDraft] = useState<Draft | null>(null);
  const draftLink = useRef<HTMLAnchorElement>(null);
  const nights = stayNights(arrival, departure);
  const fieldId = (field: string) => `${id}-${field}`;
  const description = (field: keyof GroupErrors) => errors[field] ? fieldId(`${field}-error`) : undefined;
  const error = (field: keyof GroupErrors) => errors[field]
    ? <span className="group-field-error" id={fieldId(`${field}-error`)}>{errors[field]}</span>
    : null;

  return <form className="group-enquiry" noValidate aria-labelledby={fieldId("title")} aria-busy={delivery.pending}
    onChange={() => { if (draft) setDraft(null); if (!delivery.pending) delivery.reset(); }}
    onSubmit={async event => {
      event.preventDefault();
      if (delivery.pending) return;
      const whatsapp = (event.nativeEvent as SubmitEvent).submitter?.getAttribute("value") === "whatsapp";
      if (!whatsapp && delivery.status === "accepted") return;
      const form = event.currentTarget;
      const fields = new FormData(form);
      const value = (name: string) => String(fields.get(name) ?? "").trim();
      const company = value("company");
      const data: Enquiry = {
        arrival: value("arrival"), departure: value("departure"),
        roomCount: value("roomCount"), adults: value("adults"), children: value("children"),
        room: value("room"), name: value("name"), notes: value("notes"),
      };
      // A group request is not an occupancy allocation. Reuse the shared date,
      // requested-room and text checks; validate the total party separately.
      const reply = { email: value("email"), phone: value("phone") };
      const validation: GroupErrors = { ...validateEnquiry({ ...data, adults: "2", children: "0" }, localToday()), ...(!whatsapp ? validateReplyDetails(reply) : {}) };
      if (!/^(?:[1-9]|[1-4]\d|50)$/.test(data.adults)) validation.adults = "Enter the total adults travelling, from 1 to 50.";
      if (!/^(?:\d|[12]\d|30)$/.test(data.children)) validation.children = "Enter the total children travelling, from 0 to 30.";
      if (company.length > 100) validation.company = "Keep the company or group name to 100 characters.";
      if (data.notes.length > 420) validation.notes = "Keep your request to 420 characters.";
      setErrors(validation);
      if (Object.keys(validation).length) {
        const field = form.elements.namedItem(Object.keys(validation)[0]);
        if (field instanceof HTMLElement) field.focus();
        return;
      }
      if (whatsapp) {
        delivery.reset();
        const notes = [
          "Group accommodation enquiry.",
          company ? `Company or group: ${company}` : "",
          data.notes,
        ].filter(Boolean).join("\n");
        const href = buildWhatsAppUrl(hotel.whatsappNumber, { ...data, notes });
        setDraft({ href, message: new URL(href).searchParams.get("text") || "" });
        window.requestAnimationFrame(() => draftLink.current?.focus());
        return;
      }
      setDraft(null);
      await delivery.submit("group", {
        Name: data.name, "Company or group": company, Arrival: data.arrival, Departure: data.departure,
        Adults: data.adults, Children: data.children, "Rooms requested": data.roomCount || "2",
        "Room preference": data.room || "Help us choose", Notes: data.notes,
      }, reply, value("_honey"));
    }}>
    <div className="group-form-heading">
      <p className="group-kicker">Your request</p>
      <h2 id={fieldId("title")}>Start with the details.</h2>
      <p>Send your plans to the hotel with a reply email, or continue on WhatsApp.</p>
    </div>

    <fieldset className="group-fieldset" disabled={delivery.pending}>
      <legend>When are you travelling?</legend>
      <div className="group-fields group-date-fields">
        <div className="group-field"><label htmlFor={fieldId("arrival")}>Arrival</label>
          <DateField id={fieldId("arrival")} name="arrival" label="Arrival date" minToday required value={arrival}
            onValueChange={value => { setArrival(value); setDraft(null); setErrors({}); delivery.reset(); }}
            aria-invalid={!!errors.arrival} aria-describedby={description("arrival")}/>
          {error("arrival")}
        </div>
        <div className="group-field"><label htmlFor={fieldId("departure")}>Departure</label>
          <DateField id={fieldId("departure")} name="departure" label="Departure date" required value={departure}
            min={arrival ? nextDate(arrival) : undefined} onValueChange={value => { setDeparture(value); setDraft(null); setErrors({}); delivery.reset(); }}
            aria-invalid={!!errors.departure} aria-describedby={description("departure")}/>
          {error("departure")}
        </div>
      </div>
      <p className="group-nights" aria-live="polite">{nights > 0 ? `${nights} night${nights === 1 ? "" : "s"} requested.` : "Choose your arrival and departure dates."}</p>
    </fieldset>

    <fieldset className="group-fieldset" disabled={delivery.pending}>
      <legend>Rooms and guests requested</legend>
      <div className="group-fields">
        <div className="group-field group-room-count"><label htmlFor={fieldId("roomCount")}>Rooms requested</label>
          <select id={fieldId("roomCount")} name="roomCount" defaultValue="2"
            aria-invalid={!!errors.roomCount} aria-describedby={description("roomCount")}>
            {Array.from({ length: 8 }, (_, index) => index + 1).map(count =>
              <option key={count} value={count}>{count} room{count === 1 ? "" : "s"}</option>)}
          </select>{error("roomCount")}
        </div>
        <div className="group-field group-room-preference"><label htmlFor={fieldId("room")}>Room preference</label>
          <select id={fieldId("room")} name="room" defaultValue="">
            <option value="">Help us choose</option>
            {rooms.map(room => <option key={room.slug} value={room.name}>{room.name}</option>)}
            <option value="A mix of room types">A mix of room types</option>
          </select>
        </div>
        <div className="group-field"><label htmlFor={fieldId("adults")}>Total adults</label>
          <input id={fieldId("adults")} name="adults" type="number" inputMode="numeric"
            min={1} max={50} step={1} defaultValue="2" required
            aria-invalid={!!errors.adults} aria-describedby={description("adults")}/>
          {error("adults")}
        </div>
        <div className="group-field"><label htmlFor={fieldId("children")}>Total children</label>
          <input id={fieldId("children")} name="children" type="number" inputMode="numeric"
            min={0} max={30} step={1} defaultValue="0"
            aria-invalid={!!errors.children} aria-describedby={description("children")}/>
          {error("children")}
        </div>
      </div>
      <p className="group-field-note">These are your requested numbers. The hotel will confirm room availability and a suitable arrangement for everyone.</p>
    </fieldset>

    <fieldset className="group-fieldset" disabled={delivery.pending}>
      <legend>A little more about your stay</legend>
      <div className="group-fields">
        <div className="group-field"><label htmlFor={fieldId("name")}>Your name <span>Optional</span></label>
          <input id={fieldId("name")} name="name" autoComplete="name" maxLength={80}
            aria-invalid={!!errors.name} aria-describedby={description("name")}/>
          {error("name")}
        </div>
        <div className="group-field"><label htmlFor={fieldId("company")}>Company or group <span>Optional</span></label>
          <input id={fieldId("company")} name="company" autoComplete="organization" maxLength={100}
            aria-invalid={!!errors.company} aria-describedby={description("company")}/>
          {error("company")}
        </div>
        <ReplyFields prefix={fieldId("reply")} errors={errors} fieldClass="group-field group-field-wide"/>
        <div className="group-field group-field-wide"><label htmlFor={fieldId("notes")}>Anything to plan around? <span>Optional</span></label>
          <textarea id={fieldId("notes")} name="notes" rows={4} maxLength={420}
            placeholder="Children’s ages, separate beds, arrival plans, meals or billing questions."
            aria-invalid={!!errors.notes} aria-describedby={description("notes")}/>
          {error("notes")}
        </div>
      </div>
    </fieldset>
    <EnquiryHoneypot/>
    {Object.keys(errors).length > 0 && <p className="group-form-alert" role="alert">Please check the highlighted details.</p>}
    <EmailConsent/>
    <button className="button group-submit" type="submit" disabled={delivery.pending || delivery.status === "accepted"} style={{color:"var(--paper)"}}>
      <Mail size={19}/>{delivery.pending ? "Sending…" : delivery.status === "accepted" ? "Enquiry submitted" : "Send enquiry"}<ArrowUpRight size={19} aria-hidden="true"/>
    </button>
    <EmailFeedback status={delivery.status} message={delivery.message}/>
    {draft ? <div className="group-draft" aria-live="polite">
      <h3><Check size={22} aria-hidden="true"/> Your WhatsApp enquiry is ready.</h3>
      <p className="group-draft-message">{draft.message}</p>
      <a ref={draftLink} className="button" href={draft.href} target="_blank"
        rel="noopener noreferrer" style={{ color: "var(--paper)" }}>
        <WhatsAppIcon size={19}/> Open WhatsApp & send <ArrowUpRight size={18} aria-hidden="true"/>
      </a>
      <p className="group-field-note">Review the message in WhatsApp, then tap Send. Editing this form clears the prepared message.</p>
    </div> : <button className="enquiry-whatsapp-alternative" type="submit" name="channel" value="whatsapp" disabled={delivery.pending} style={{ color: "var(--accent)" }}>
      <WhatsAppIcon size={19}/> Prefer WhatsApp? Prepare a message
    </button>}
    <p className="group-form-footnote">This is an enquiry. Availability, rates, meal inclusions and booking terms are confirmed directly by the hotel.</p>
  </form>;
}
