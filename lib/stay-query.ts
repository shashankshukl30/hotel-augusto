import { localToday, validateEnquiry, type Enquiry } from "./booking";

export type StaySelection = Pick<Enquiry, "arrival" | "departure" | "adults" | "children" | "room" | "roomCount">;

/** Only travel preferences are handed between pages. Names and private notes stay off the URL. */
export function stayQuery(data: StaySelection) {
  const query = new URLSearchParams();
  for (const key of ["arrival", "departure", "adults", "children", "room", "roomCount"] as const) {
    if (data[key]) query.set(key, data[key]);
  }
  return query.toString();
}

export function readStayQuery(query: URLSearchParams, roomSlugs: readonly string[], today = localToday()): StaySelection {
  const data: Enquiry = {
    arrival: query.get("arrival") || "",
    departure: query.get("departure") || "",
    adults: query.get("adults") || "2",
    children: query.get("children") || "0",
    room: query.get("room") || "",
    roomCount: query.get("roomCount") || "1",
    name: "",
    notes: "",
  };
  const errors = validateEnquiry(data, today);
  return {
    arrival: errors.arrival ? "" : data.arrival,
    departure: errors.departure || errors.arrival ? "" : data.departure,
    adults: errors.adults ? "2" : data.adults,
    children: errors.children ? "0" : data.children,
    room: roomSlugs.includes(data.room) ? data.room : "",
    roomCount: errors.roomCount ? "1" : data.roomCount,
  };
}
