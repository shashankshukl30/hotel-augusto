/**
 * Hotel services and practical content, checked 20 October 2026.
 * Evidence: research/hotel-facts.json and
 * research/hospitality-revision/content-journey-plan.json.
 * Availability, fees, policy conflicts and access needs remain hotel-confirmed.
 */
export const services = [
  { id: "air-conditioning", title: "Air-conditioned rooms", category: "In your room", description: "A place to cool down between walks through the city.", sourceIds: ["S01", "S04", "S05"] },
  { id: "wifi", title: "Wi-Fi", category: "In your room", description: "Stay connected during your visit. Ask reception for the network details.", sourceIds: ["S01", "S02", "S04"] },
  { id: "bathroom", title: "Private bathrooms", category: "In your room", description: "Each room has its own bathroom, so you can get ready at your own pace.", sourceIds: ["S05", "S07", "S10"] },
  { id: "television", title: "Television", category: "In your room", description: "A familiar comfort for a little downtime at the hotel.", sourceIds: ["S01", "S02", "S10"] },
  { id: "restaurant", title: "Vegetarian restaurant", category: "At the hotel", description: "Sit down for a vegetarian meal without leaving the hotel. Check the current menu and serving times with the team.", sourceIds: ["S02", "S05"] },
  { id: "room-service", title: "Room service", category: "At the hotel", description: "Prefer to stay in your room? Ask what can be ordered, when it is available and any applicable charges.", sourceIds: ["S02", "S04", "S10", "HR-MMT"] },
  { id: "reception", title: "24-hour reception", category: "During your stay", description: "Reception is available around the clock. Share early or late arrival plans so the hotel can confirm your check-in arrangements.", sourceIds: ["S01", "S05", "S10"] },
  { id: "housekeeping", title: "Housekeeping", category: "During your stay", description: "Speak with the team about room cleaning and any housekeeping requests during your stay.", sourceIds: ["S04", "S10", "HR-MMT"] },
  { id: "luggage", title: "Luggage assistance & storage", category: "During your stay", description: "Ask about help with bags and storage around your arrival or departure. Confirm availability and any charges in advance.", sourceIds: ["S04", "S05", "HR-MMT"] },
  { id: "lift", title: "Lift", category: "During your stay", description: "The hotel has a lift. If steps or mobility are a concern, confirm the complete entrance-to-room route before booking.", sourceIds: ["S02", "HR-MMT"] },
  { id: "laundry", title: "Laundry service", category: "During your stay", description: "Ask the team about the current laundry service, turnaround and charges.", sourceIds: ["S02", "S05", "HR-MMT"] },
  { id: "lounge", title: "Lobby seating", category: "At the hotel", description: "A shared place to sit, meet your travel companions and get your bearings before heading out.", sourceIds: ["S05", "HR-MMT"] },
] as const;

export const reviewSources = [
  {
    name: "Google",
    href: "https://www.google.com/maps/place/HOTEL+AUGUSTO+VARANASI/@25.3084409,83.0065447,17z/data=!4m9!3m8!1s0x398e2e1d7775c433:0x6b2c6055668741f4!5m2!4m1!1i2!8m2!3d25.3084409!4d83.0065447!16s%2Fg%2F11b6dg6mk3",
    description: "Visit the hotel’s Google profile and guest reviews.",
  },
  {
    name: "MakeMyTrip",
    href: "https://www.makemytrip.com/hotels/hotel_augusto-details-varanasi.html",
    description: "Read guest experiences on the property listing.",
  },
  {
    name: "Tripadvisor",
    href: "https://www.tripadvisor.in/Hotel_Review-g297685-d6540696-Reviews-HOTEL_AUGUSTO-Varanasi_Varanasi_District_Uttar_Pradesh.html",
    description: "Explore independently published traveller reviews.",
  },
] as const;

/** Exact excerpt; source capture and limitations: research/hospitality-revision/guest-review-evidence.json. */
export const guestReviewHighlight = {
  quote: "very fast service food also very good",
  author: "Flyer47905230766",
  platform: "Tripadvisor",
  attribution: "Flyer47905230766 · Tripadvisor",
  href: "https://www.tripadvisor.com/ShowUserReviews-g297685-d6540696-r1063977750",
} as const;

export const arrivalModes = [
  {
    id: "air",
    label: "By air",
    title: "From the airport, towards Godowlia.",
    paragraphs: [
      "Share your flight’s arrival time with the hotel before travelling. Ask for the current approach and drop-off guidance for August Kunda Road.",
      "Keep the hotel address ready for your driver. If you need help planning transport, ask what is currently available and confirm the cost before making arrangements.",
    ],
    message: "Hello Hotel Augusto, I will be arriving by air. Please share the current approach and drop-off guidance for the hotel. I can send my arrival date, flight time and luggage details.",
  },
  {
    id: "rail",
    label: "By rail",
    title: "Start with your station and arrival time.",
    paragraphs: [
      "Send the hotel the station name shown on your ticket and your expected arrival time. This helps the team advise you about reaching the correct address.",
      "Before leaving the station, check the final drop-off point and keep the hotel’s phone number available for your driver.",
    ],
    message: "Hello Hotel Augusto, I will be arriving by train. Please help me plan the approach and drop-off. I can share my station, arrival date and time.",
  },
  {
    id: "road",
    label: "By road",
    title: "Check the last part of your journey.",
    paragraphs: [
      "Coming by car or taxi? Contact the hotel for current vehicle access, drop-off and parking guidance before entering Godowlia.",
      "Let the team know if you have several bags or any mobility needs. Parking location, charges and access arrangements should be confirmed directly.",
    ],
    message: "Hello Hotel Augusto, I plan to arrive by car or taxi. Could you confirm current vehicle access, the drop-off point and parking arrangements? I can share my arrival time and luggage details.",
  },
] as const;

export const practicalFaqs = [
  { topic: "Location", question: "Where exactly is Hotel Augusto?", answer: "Hotel Augusto is at D 36/1, August Kunda Road, Godowlia, Jangambari, Varanasi 221001, opposite State Bank of India. Use the hotel’s map link and confirm the final approach before travelling by car." },
  { topic: "Location", question: "Can I walk to the temple and the ghats?", answer: "Shri Kashi Vishwanath Temple and Dashashwamedh Ghat are within walking distance. Allow time for the lanes, crowds and current entry arrangements rather than relying on a fixed walking time." },
  { topic: "Arrival", question: "Is parking available?", answer: "Please ask the hotel for current parking and drop-off guidance before arrival. On-site or complimentary parking is not guaranteed." },
  { topic: "Arrival", question: "Can I arrive early or leave late?", answer: "Share your travel dates and arrival or departure time with the hotel. The team will confirm check-in arrangements, room availability and any additional charge." },
  { topic: "Arrival", question: "Can the hotel help with luggage?", answer: "Luggage assistance and storage are listed facilities. Confirm availability, timing and any charges with the hotel before relying on storage outside your stay." },
  { topic: "Rooms", question: "Which bed arrangements can I choose?", answer: "The Deluxe Room has a double bed, the Deluxe Twin Room has two single beds, and the Family Room has two beds. Share the number of adults and children so the hotel can confirm a suitable arrangement." },
  { topic: "Rooms", question: "Is there a lift?", answer: "Yes, the hotel has a lift. This does not establish that every part of the property is step-free. Tell the hotel about any mobility or accessibility needs before booking." },
  { topic: "Dining", question: "Does the hotel serve vegetarian food?", answer: "Yes. Hotel Augusto has an on-site vegetarian restaurant and room service. Ask for the current menu and serving times." },
  { topic: "Dining", question: "Is breakfast included?", answer: "Breakfast inclusion depends on the room plan you choose. Confirm the meals included, serving times and any additional charges when asking for your rate." },
  { topic: "Booking", question: "Does sending an enquiry reserve a room?", answer: "No. You can send an email enquiry or prepare a WhatsApp message through the website. The hotel must confirm availability, price, payment terms and your reservation." },
  { topic: "Booking", question: "What should I confirm before booking?", answer: "Confirm your room arrangement, guest identification requirements, check-in and check-out times, meal inclusions, payment terms and cancellation conditions directly with the hotel." },
] as const;
