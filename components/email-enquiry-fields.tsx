import { hotel } from "@/content/hotel";
import type { ReplyErrors } from "@/lib/enquiry-email";
import type { EmailStatus } from "./use-email-enquiry";
import "./email-enquiry.css";

export function ReplyFields({ prefix, errors, fieldClass }: { prefix: string; errors: ReplyErrors; fieldClass: string }) {
  return <>
    <div className={fieldClass}>
      <label htmlFor={`${prefix}-email`}>Your email <span aria-hidden="true">*</span></label>
      <input id={`${prefix}-email`} name="email" type="email" autoComplete="email" inputMode="email" required maxLength={254}
        placeholder="you@example.com" aria-invalid={!!errors.email} aria-describedby={errors.email ? `${prefix}-email-error` : undefined}/>
      {errors.email && <span className="enquiry-reply-error" id={`${prefix}-email-error`}>{errors.email}</span>}
    </div>
    <div className={fieldClass}>
      <label htmlFor={`${prefix}-phone`}>Phone <span>optional</span></label>
      <input id={`${prefix}-phone`} name="phone" type="tel" autoComplete="tel" inputMode="tel" maxLength={30}
        aria-invalid={!!errors.phone} aria-describedby={errors.phone ? `${prefix}-phone-error` : undefined}/>
      {errors.phone && <span className="enquiry-reply-error" id={`${prefix}-phone-error`}>{errors.phone}</span>}
    </div>
  </>;
}

export function EnquiryHoneypot() {
  return <div className="enquiry-honeypot" aria-hidden="true"><label>Leave this field empty<input name="_honey" type="text" tabIndex={-1} autoComplete="off"/></label></div>;
}

export function EmailFeedback({ status, message }: { status: EmailStatus; message: string }) {
  if (status === "idle") return null;
  return <div className={`enquiry-email-feedback enquiry-email-${status}`} role={status === "error" || status === "activation" ? "alert" : "status"} aria-live="polite">
    {status === "pending" && <p>Sending your enquiry…</p>}
    {status === "accepted" && <p>Your enquiry was accepted for forwarding to the hotel. The team will reply to your email. Your reservation is confirmed only when agreed with the hotel.</p>}
    {status === "activation" && <p>Email enquiries are awaiting activation by the hotel. Please email <a href={`mailto:${hotel.email}`}>{hotel.email}</a> directly or use WhatsApp for now.</p>}
    {status === "error" && <p>{message} <a href={`mailto:${hotel.email}`}>Email the hotel</a></p>}
  </div>;
}

export function EmailConsent() {
  return <p className="enquiry-email-consent">By choosing Send enquiry, you agree to share these details with the hotel through FormSubmit so the team can respond. <a href="/privacy#stay-enquiries">Privacy details</a></p>;
}
