export type Enquiry = {
  arrival: string;
  departure: string;
  adults: string;
  children: string;
  room: string;
  name: string;
  notes: string;
};
export type EnquiryErrors = Partial<Record<keyof Enquiry, string>>;

function validDate(value: string) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const date = new Date(`${value}T12:00:00Z`);
  return !Number.isNaN(date.valueOf()) && date.toISOString().slice(0, 10) === value;
}
export function localToday() {
  const date = new Date();
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2,"0")}-${String(date.getDate()).padStart(2,"0")}`;
}
export function nextDate(value: string) {
  if (!validDate(value)) return "";
  const date = new Date(`${value}T12:00:00Z`);
  date.setUTCDate(date.getUTCDate() + 1);
  return date.toISOString().slice(0,10);
}
export function validateEnquiry(data: Enquiry, today: string): EnquiryErrors {
  const errors: EnquiryErrors = {};
  if (!validDate(data.arrival)) errors.arrival = "Choose a valid arrival date.";
  else if (data.arrival < today) errors.arrival = "Your arrival date must be today or later.";
  if (!validDate(data.departure)) errors.departure = "Choose a valid departure date.";
  else if (validDate(data.arrival) && data.departure <= data.arrival) errors.departure = "Departure must be after your arrival.";
  if (!/^[1-8]$/.test(data.adults)) errors.adults = "Choose between 1 and 8 adults.";
  if (!/^[0-6]$/.test(data.children)) errors.children = "Choose between 0 and 6 children.";
  if (data.name.length > 80) errors.name = "Please keep your name to 80 characters.";
  if (data.notes.length > 600) errors.notes = "Please keep your note to 600 characters.";
  return errors;
}
function prettyDate(value: string) {
  return new Intl.DateTimeFormat("en-GB", { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" }).format(new Date(`${value}T12:00:00Z`));
}
/** Replace this channel adapter when a booking engine is supplied. No data is stored here. */
export function buildWhatsAppUrl(number: string, data: Enquiry) {
  if (!/^[1-9]\d{8,14}$/.test(number)) throw new Error("A valid international WhatsApp number is required.");
  const lines = [
    "Namaste Hotel Augusto! I would like to enquire about a stay.",
    data.name.trim() ? `Name: ${data.name.trim()}` : "",
    `Arrival: ${prettyDate(data.arrival)}`,
    `Departure: ${prettyDate(data.departure)}`,
    `Guests: ${data.adults} adult${data.adults === "1" ? "" : "s"}${data.children !== "0" ? `, ${data.children} child${data.children === "1" ? "" : "ren"}` : ""}`,
    `Room preference: ${data.room || "Please recommend a room"}`,
    data.notes.trim() ? `Note: ${data.notes.trim()}` : "",
    "Please share availability, room rates and booking conditions. Thank you!",
  ];
  return `https://wa.me/${number}?text=${encodeURIComponent(lines.filter(Boolean).join("\n"))}`;
}
