export const diningInterests = ["Restaurant meal", "Breakfast", "Room service", "Menu and meal inclusions"] as const;
export type DiningEnquiry = { name: string; date: string; interest: string; guests: string; notes: string };
export type DiningErrors = Partial<Record<keyof DiningEnquiry, string>>;

function validDate(value: string) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const date = new Date(`${value}T12:00:00Z`);
  return !Number.isNaN(date.valueOf()) && date.toISOString().slice(0, 10) === value;
}

export function validateDiningEnquiry(data: DiningEnquiry, today: string): DiningErrors {
  const errors: DiningErrors = {};
  if (!validDate(data.date)) errors.date = "Choose a valid date.";
  else if (data.date < today) errors.date = "Choose today or a future date.";
  if (!(diningInterests as readonly string[]).includes(data.interest)) errors.interest = "Choose what you would like to ask about.";
  if (!/^[1-9]\d?$/.test(data.guests)) errors.guests = "Enter a whole number between 1 and 99.";
  if (data.name.length > 80) errors.name = "Please keep your name to 80 characters.";
  if (data.notes.length > 600) errors.notes = "Please keep your note to 600 characters.";
  return errors;
}

export function buildDiningWhatsAppUrl(number: string, data: DiningEnquiry) {
  if (!/^[1-9]\d{8,14}$/.test(number)) throw new Error("A valid international WhatsApp number is required.");
  if (Object.keys(validateDiningEnquiry(data, "0000-01-01")).length) throw new Error("Valid dining details are required.");
  const date = new Intl.DateTimeFormat("en-GB", { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" }).format(new Date(`${data.date}T12:00:00Z`));
  const lines = [
    "Hello Hotel Augusto, I would like to enquire about dining.",
    data.name.trim() ? `Name: ${data.name.trim()}` : "",
    `Preferred date: ${date}`,
    `Interested in: ${data.interest}`,
    `People in our party: ${data.guests}`,
    data.notes.trim() ? `Note: ${data.notes.trim()}` : "",
    "Please share the current menu, serving times, availability and charges. Please confirm any meal inclusions for my stay. Thank you!",
  ];
  return `https://wa.me/${number}?text=${encodeURIComponent(lines.filter(Boolean).join("\n"))}`;
}
