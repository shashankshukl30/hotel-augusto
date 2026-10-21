export type ReplyDetails = { email: string; phone: string };
export type ReplyErrors = Partial<Record<keyof ReplyDetails, string>>;
export type EnquiryKind = "stay" | "dining" | "group";
export type EmailResult = "accepted" | "activation";

export function validateReplyDetails(data: ReplyDetails): ReplyErrors {
  const errors: ReplyErrors = {};
  const email = data.email.trim();
  if (!email || email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    errors.email = "Enter an email address so the hotel can reply.";
  }
  if (data.phone.trim() && (!/^[+\d\s().-]{6,30}$/.test(data.phone.trim()) || data.phone.replace(/\D/g, "").length < 6)) {
    errors.phone = "Enter a valid phone number, or leave this blank.";
  }
  return errors;
}

const subjects: Record<EnquiryKind, string> = {
  stay: "Hotel Augusto — Stay enquiry",
  dining: "Hotel Augusto — Dining enquiry",
  group: "Hotel Augusto — Group stay enquiry",
};

/** The recipient is fixed by the caller from hotel.email, never a form field. */
export function buildEmailPayload(kind: EnquiryKind, details: Record<string, string>, reply: ReplyDetails, honey: string) {
  if (Object.keys(validateReplyDetails(reply)).length) throw new Error("Valid reply details are required.");
  if (honey) throw new Error("This enquiry could not be submitted. Please contact the hotel directly.");
  // Do not let arbitrary detail keys override FormSubmit's routing options.
  const safeDetails = Object.fromEntries(Object.entries(details).filter(([key]) => !key.startsWith("_") && !["email", "phone", "recipient"].includes(key)));
  return {
    ...safeDetails,
    email: reply.email.trim(),
    phone: reply.phone.trim() || "Not supplied",
    _subject: subjects[kind],
    _template: "table",
    _honey: "",
  };
}

export function parseEmailResponse(value: unknown): EmailResult {
  if (!value || typeof value !== "object") throw new Error("The email service did not confirm your enquiry.");
  const response = value as { success?: unknown; message?: unknown };
  const message = typeof response.message === "string" ? response.message : "";
  if (/activat|confirm.{0,50}(email|address)|check.{0,50}(inbox|email)/i.test(message)) return "activation";
  if (response.success !== true && response.success !== "true") throw new Error("The email service did not confirm your enquiry.");
  return "accepted";
}
