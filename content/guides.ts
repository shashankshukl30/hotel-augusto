export type StayGuide = {
  slug: string;
  category: string;
  title: string;
  metaTitle: string;
  description: string;
  image: string;
  alt: string;
  imageCaption: string;
  imagePosition?: string;
  introduction: string;
  checklist: string[];
  sections: { id: string; title: string; paragraphs: string[] }[];
  questions: { question: string; answer: string }[];
  links: { label: string; href: string }[];
};

/** Practical editorial guidance grounded in the hotel and government-source ledgers.
 * No fixed opening hours, fares, room capacities or unverified hotel services. */
export const guides: StayGuide[] = [
  {
    slug: "first-visit-to-kashi",
    category: "Your first visit",
    title: "A first visit to Kashi.",
    metaTitle: "First Visit to Kashi Vishwanath | Hotel Augusto Guide",
    description: "Plan a first visit to Kashi Vishwanath and the Varanasi ghats from Hotel Augusto, with practical steps and official sources.",
    image: "/images/kashi-vishwanath.webp",
    alt: "Visitors in the courtyard of Shri Kashi Vishwanath Temple beneath its golden shrine",
    imageCaption: "Shri Kashi Vishwanath Temple · Pradum Shukla / CC BY 4.0",
    imagePosition: "center 67%",
    introduction: "A first visit to Kashi works best with a few clear plans and some time left open. From Augusto in Godowlia, Shri Kashi Vishwanath Temple and Dashashwamedh Ghat are within walking distance. Give each place its own visit, rather than treating the temple, the river and the evening aarti as a single stop.",
    checklist: [
      "Check current temple visitor information before you leave.",
      "Save the hotel’s address and map pin on your phone.",
      "Leave space between your temple visit and the evening aarti.",
      "Confirm boat routes and fares with the operator before boarding.",
    ],
    sections: [
      {
        id: "understand-the-place",
        title: "Begin with the place itself.",
        paragraphs: [
          "Shri Kashi Vishwanath Temple is dedicated to Lord Shiva and is one of the twelve Jyotirlingas. The Varanasi district administration places it on the western bank of the Ganga. This is a place of worship as well as one of the city’s best-known destinations, so plan a visit with time to follow the arrangements in place that day.",
          "The temple and Dashashwamedh Ghat are separate places. You can include both in your stay without rushing directly from one to the other. Choose the part of the day you want to spend at each, then leave the time in between flexible.",
        ],
      },
      {
        id: "before-you-leave",
        title: "Check the details before setting out.",
        paragraphs: [
          "Use current official visitor information for entry arrangements, any required reservations and what you may carry. Do this close to your visit: an old itinerary, an online photograph or a previous guest’s experience may not describe the arrangements on your day. Use the official links below as a starting point.",
          "If you have a particular darshan or visit in mind, confirm exactly what it includes and where you need to arrive. Keep any confirmation accessible. Ask the hotel about the walking route from Augusto, and carry only what you need for that part of the day.",
        ],
      },
      {
        id: "make-time-for-the-river",
        title: "Give the river its own morning.",
        paragraphs: [
          "The ghats offer a different way to experience Varanasi. At dawn, the light on the water and the activity along the steps make a riverfront visit worthwhile in its own right. The district’s tourism information describes boat outings from Dashashwamedh; the Kashi visitor guide also identifies the ghat as a boat-ride starting point.",
          "Before agreeing to a boat outing, ask the operator about the route, duration, total fare and return point. Arrange and pay for the outing separately from your room stay. A walk by the river can also be the whole plan; leave yourself time to enjoy the steps and the view.",
        ],
      },
      {
        id: "evening-aarti",
        title: "Keep the evening aarti unhurried.",
        paragraphs: [
          "Dashashwamedh Ghat is known for the evening Ganga Aarti. Confirm the day’s timing locally and allow time to reach the ghat and find a place. Keep the afternoon flexible so you can make your way to the river without rushing.",
          "Decide your return plan before the ceremony starts. Save the hotel pin, agree a meeting point if your group separates and keep the route back in mind. If the day has already been full, make the aarti your final outing and leave another part of the city for tomorrow.",
        ],
      },
      {
        id: "your-base",
        title: "Use Godowlia as your base.",
        paragraphs: [
          "Augusto gives you a place to pause between visits, with air-conditioned rooms and an on-site vegetarian restaurant. A break at the hotel can make the rest of the day more comfortable, particularly when different members of your group want different amounts of walking or time out.",
          "Before your stay, tell the hotel your dates and room preference. If easy access, separate beds or a particular sleeping arrangement matters, mention it in the enquiry. A clear room plan and a flexible city plan work well together.",
        ],
      },
    ],
    questions: [
      { question: "Can I walk from Augusto to the temple?", answer: "The temple and Dashashwamedh Ghat are within walking distance of the hotel. Ask the team for the route and current access information before setting out." },
      { question: "How do I arrange a boat ride or aarti seating?", answer: "Ask about the current options and agree the arrangement and total cost with the provider. Plan these separately from your room booking." },
      { question: "Where should I check temple entry arrangements?", answer: "Start with current official temple and destination information. Confirm the requirements for your particular visit before leaving the hotel." },
    ],
    links: [
      { label: "Official temple visitor information", href: "https://www.shrikashivishwanath.org/" },
      { label: "Kashi Vishwanath — Varanasi district", href: "https://varanasi.nic.in/tourist-place/shri-kashi-vishwanath-temple/" },
      { label: "Dashashwamedh Ghat — official Kashi guide", href: "https://kashi.gov.in/listing-details/dashashwamedh-ghat" },
      { label: "Varanasi places of interest — district guide", href: "https://varanasi.nic.in/gallery/places-of-tourist-attraction/" },
    ],
  },
  {
    slug: "arriving-in-godowlia",
    category: "Getting here",
    title: "Arriving in Godowlia.",
    metaTitle: "Arriving in Godowlia, Varanasi | Hotel Augusto Guide",
    description: "A practical arrival checklist for Hotel Augusto in Godowlia, Varanasi: address, map pin, luggage, room readiness and onward plans.",
    image: "/images/hotel-exterior-day.webp",
    alt: "The daytime facade and entrance of Hotel Augusto in Godowlia",
    imageCaption: "Hotel Augusto, Godowlia · Property photograph",
    imagePosition: "center 46%",
    introduction: "The most useful arrival plan begins with the right address and a short conversation with the hotel. Augusto is on August Kunda Road in Godowlia, Jangambari. Save the exact hotel pin, share your expected arrival time and confirm the last part of the journey before you travel.",
    checklist: [
      "Save Hotel Augusto’s exact address and map pin.",
      "Share your arrival date, approximate time and guest count.",
      "Ask where your driver should stop for the hotel entrance.",
      "Confirm room readiness if you expect an early or late arrival.",
    ],
    sections: [
      {
        id: "save-the-address",
        title: "Save the hotel, not just the neighbourhood.",
        paragraphs: [
          "Use the complete address: D 36/1, August Kunda Road, Godowlia, Jangambari, Varanasi, Uttar Pradesh 221001. Godowlia is the area; the hotel name and street address make the destination more precise. The contact page links to a map search for Hotel Augusto at this address.",
          "Send that pin and address to whoever is arranging your journey. Keep a copy available on your phone, along with the hotel’s contact number. It is easier to check the final approach when the driver and hotel are referring to the same destination.",
        ],
      },
      {
        id: "share-your-plan",
        title: "Tell the team when to expect you.",
        paragraphs: [
          "Share your check-in and check-out dates, the number of adults and children, and your expected arrival time in your enquiry. Add your preferred room type if you have one. If a train or flight forms part of the journey, its arrival time gives useful context without committing the hotel to an exact room-ready time.",
          "An early arrival and an early check-in are different things. If you plan to reach the city before your room is ready, ask what arrangements are possible and whether they carry a charge. Do the same for a late departure instead of assuming the room can be kept longer.",
        ],
      },
      {
        id: "last-part-of-the-journey",
        title: "Clarify the last part of the journey.",
        paragraphs: [
          "Ask the hotel where your driver should stop and how to reach the entrance from there. This is especially useful if you are travelling with several bags, children or someone who prefers a shorter walk. Confirm the instructions for your arrival day rather than relying on an older journey description.",
          "If you need parking, luggage help or a particular access arrangement, include it in your arrival message. Ask for the current drop-off point, the route to the entrance and any charges, so you and your driver can plan the final stretch together.",
        ],
      },
      {
        id: "transport-arrangements",
        title: "Keep transport arrangements clear.",
        paragraphs: [
          "For a taxi or other transfer, agree the destination, total fare and any waiting arrangements with the provider. Share the airport or station name, your arrival time and how much luggage you have. Ask for a quote for your specific journey before confirming.",
          "If you ask the hotel for help, clarify what is being arranged and what you will pay. Keep the driver's contact details and your transport confirmation alongside your room confirmation, ready for the day you travel.",
        ],
      },
      {
        id: "after-you-arrive",
        title: "Leave your first outing flexible.",
        paragraphs: [
          "Once you have settled in, use the hotel as a starting point for the old city. Shri Kashi Vishwanath Temple and Dashashwamedh Ghat are within walking distance. Ask for the walking route before heading out, particularly if you are returning after an evening visit.",
          "There is no need to commit your arrival day to a long itinerary. A meal at Augusto’s vegetarian restaurant, a pause in your room and one nearby outing may be enough. Keep the next morning open for the river or temple, depending on the arrangements you have confirmed.",
        ],
      },
    ],
    questions: [
      { question: "What address should I give my driver?", answer: "Hotel Augusto, D 36/1, August Kunda Road, Godowlia, Jangambari, Varanasi, Uttar Pradesh 221001. Send the map pin from the contact page as well." },
      { question: "Can I check in as soon as I reach Varanasi?", answer: "Confirm room readiness, check-in arrangements and any early-arrival charge directly with the hotel. An arrival time in your enquiry is not an early check-in confirmation." },
      { question: "How should I arrange parking or an airport transfer?", answer: "Send the hotel your travel details and ask about current parking, drop-off and transport options. Confirm the arrangement, provider and any separate cost before travelling." },
    ],
    links: [
      { label: "Hotel address, directions and contact", href: "/contact" },
      { label: "Explore the neighbourhood", href: "/varanasi" },
      { label: "Dining at Hotel Augusto", href: "/dining" },
    ],
  },
  {
    slug: "choosing-your-room",
    category: "Planning your stay",
    title: "Choose the room for your stay.",
    metaTitle: "Choosing Your Room in Varanasi | Hotel Augusto Guide",
    description: "Compare the bed layouts at Hotel Augusto and prepare a clear room enquiry, with questions about guests, inclusions and arrival needs.",
    image: "/images/family-room.webp",
    alt: "A guest room with two beds and green bed runners at Hotel Augusto",
    imageCaption: "A Family Room at Hotel Augusto · Property photograph",
    introduction: "Start with the sleeping arrangement your group needs, then confirm the details for your dates. Augusto presents three room categories: Deluxe Room, Deluxe Twin Room and Family Room. Their bed layouts offer a useful starting point; availability, guest capacity and any additional bedding should be confirmed with the hotel.",
    checklist: [
      "Choose a preferred bed layout.",
      "Include all adults and children in your enquiry.",
      "Ask what the quoted rate includes.",
      "Confirm additional bedding and arrival requirements before booking.",
    ],
    sections: [
      {
        id: "start-with-the-beds",
        title: "Start with the bed layout.",
        paragraphs: [
          "The Deluxe Room is shown with a double bed. The Deluxe Twin Room has two single beds, which makes the sleeping arrangement clear when you want separate beds. The Family Room is presented with two beds. Explore the photographs for each category to see the layout before deciding which one you prefer.",
          "Tell the hotel the total number of adults and children, including their ages, and ask it to suggest the appropriate category. Confirm the permitted occupancy and any extra bedding you need alongside the bed layout.",
        ],
      },
      {
        id: "look-through-the-photographs",
        title: "Look beyond the first photograph.",
        paragraphs: [
          "Use the room pages and gallery together. A main bedroom view helps explain the layout; additional photographs show the hotel’s bathrooms, reception, dining room and other spaces. The gallery separates rooms, hotel areas and dining so you can look at the parts of the stay that matter to you.",
          "Photographs show real spaces at Augusto, but they do not reserve a particular room for your dates. If a specific layout, bed position or feature is important, mention it when you enquire and ask the hotel to confirm the allocation it can offer.",
        ],
      },
      {
        id: "confirm-the-comforts",
        title: "Confirm the details that matter to you.",
        paragraphs: [
          "The room pages list air conditioning, a private bathroom, television and Wi-Fi. Use those as a starting point, then raise any particular needs in your message. For example, separate beds or a request concerning access is more useful to discuss before booking than after arriving.",
          "If you need extra bedding, a particular room location or another arrangement, ask whether it is available and whether there is an additional charge. A clear request gives the hotel a chance to answer specifically; a general room enquiry may leave those details unresolved.",
        ],
      },
      {
        id: "understand-the-quote",
        title: "Ask for a complete quote.",
        paragraphs: [
          "Send your stay dates and guest details together so the team can respond to the actual stay you are planning. Ask for the total room charge and what is included. Clarify whether meals, taxes or additional bedding form part of that quote rather than assuming every rate has the same inclusions.",
          "Also ask about the payment, cancellation and check-in arrangements attached to the offer. The team will confirm availability and the terms for your dates. Sending a WhatsApp enquiry begins that conversation; your reservation is complete when the hotel confirms it.",
        ],
      },
      {
        id: "send-one-clear-message",
        title: "Put the important details in one message.",
        paragraphs: [
          "A useful enquiry includes your check-in date, check-out date, number of rooms, adults and children, preferred room type and any essential request. If you expect an early arrival or a late departure, include that too. You can use the website’s enquiry form to begin the conversation on WhatsApp.",
          "Before you finish the conversation, make sure you understand which category is being offered, the agreed dates, the total charge and how the hotel confirms the reservation. Keep the confirmation accessible for arrival, then turn to planning the part of Varanasi you want to explore first.",
        ],
      },
    ],
    questions: [
      { question: "Which room has separate single beds?", answer: "The Deluxe Twin Room is presented with two single beds. Confirm its availability for your dates through the hotel." },
      { question: "How many guests can stay in the Family Room?", answer: "Tell the hotel the number of adults and children, including their ages. The team will confirm the permitted occupancy and the bedding arrangement for your group." },
      { question: "Does sending a WhatsApp enquiry reserve a room?", answer: "No. The message starts a conversation with the hotel. Availability, rate, payment arrangements and reservation confirmation are handled directly by the team." },
    ],
    links: [
      { label: "Compare Augusto’s room categories", href: "/rooms" },
      { label: "Look through the hotel gallery", href: "/gallery" },
      { label: "Send a stay enquiry", href: "/contact#enquire" },
    ],
  },
];

export function guideBySlug(slug: string) {
  return guides.find((guide) => guide.slug === slug);
}
