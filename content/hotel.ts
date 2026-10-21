/**
 * Hotel content checked against research/hotel-facts.json on 19 October 2026.
 * Booking contact is centralized here for the later booking-engine integration.
 * Conflicting policies, room dimensions, capacities and rates are intentionally
 * kept out of guest-facing content. Contact verification notes live in research.
 */
export const hotel = {
  name: "Hotel Augusto",
  locality: "Godowlia, Varanasi",
  phone: "+91 80817 09146",
  phoneHref: "tel:+918081709146",
  whatsappNumber: "918081709146",
  email: "aromaofkashi@gmail.com",
  address: [
    "D 36/1, August Kunda Road",
    "Godowlia, Jangambari",
    "Varanasi, Uttar Pradesh 221001",
  ],
  mapsUrl:
    "https://www.google.com/maps/search/?api=1&query=Hotel+Augusto%2C+D+36%2F1%2C+Jangambari%2C+Varanasi",
  coordinates: { latitude: 25.3084409, longitude: 83.0065447 },
  description:
    "A welcoming stay in Godowlia, with the temples, ghats and everyday life of Varanasi within easy reach.",
  bookingMessage:
    "Hello Hotel Augusto, I would like to enquire about a stay. Please share room availability and rates.",
  amenities: [
    "Air-conditioned rooms",
    "Wi-Fi",
    "On-site restaurant",
    "Room service",
    "24-hour reception",
    "Housekeeping",
  ],
} as const;

export interface Room {
  slug: string;
  name: string;
  eyebrow: string;
  description: string;
  bedLabel: string;
  image: string;
  alt: string;
  features: string[];
}

export const rooms: Room[] = [
  {
    slug: "deluxe-room",
    name: "Deluxe Room",
    eyebrow: "A little time to yourself",
    description:
      "Set down your bags, cool off and settle in. A double bed and the comforts you need between early temple visits and evenings by the river.",
    bedLabel: "Double bed",
    image: "/images/deluxe-room.webp",
    alt: "Double-bed guest room at Hotel Augusto, Varanasi",
    features: ["Air conditioning", "Private bathroom", "Television", "Wi-Fi"],
  },
  {
    slug: "deluxe-twin-room",
    name: "Deluxe Twin Room",
    eyebrow: "Travel together. Rest your way.",
    description:
      "Two separate beds make sharing a room easy. An uncomplicated base for friends or family, close to the places you came to see.",
    bedLabel: "Two single beds",
    image: "/images/twin-room.webp",
    alt: "Twin-bed guest room at Hotel Augusto, Varanasi",
    features: ["Air conditioning", "Private bathroom", "Television", "Wi-Fi"],
  },
  {
    slug: "family-room",
    name: "Family Room",
    eyebrow: "Keep everyone close",
    description:
      "A room for the journey you share. Two beds bring the family together, with a comfortable place to return to after a day around Kashi.",
    bedLabel: "Two beds",
    image: "/images/family-room.webp",
    alt: "Family guest room at Hotel Augusto, Varanasi",
    features: ["Air conditioning", "Private bathroom", "Television", "Wi-Fi"],
  },
];

export const faqs = [
  {
    question: "Where is Hotel Augusto?",
    answer:
      "We are on August Kunda Road in Godowlia, Jangambari, Varanasi, opposite State Bank of India. Shri Kashi Vishwanath Temple and Dashashwamedh Ghat are within walking distance.",
  },
  {
    question: "How do I book a room?",
    answer:
      "Send your travel dates, number of guests and preferred room through the enquiry form, email us or use WhatsApp. You can also call the hotel. The team will confirm availability, the rate and payment details before you book.",
  },
  {
    question: "Which room types can I choose from?",
    answer:
      "Choose a Deluxe Room with a double bed, a Deluxe Twin Room with separate single beds, or a Family Room. Share the number of adults and children so the hotel can recommend the right arrangement.",
  },
  {
    question: "Is food available at the hotel?",
    answer:
      "Yes. The hotel has an on-site restaurant with vegetarian dining and room service. Ask about breakfast and the meals included in your room rate when you enquire.",
  },
  {
    question: "What are the check-in and check-out times?",
    answer:
      "Please confirm your arrival and departure times with the hotel when booking. If you are arriving early or leaving late, share your travel plans so the team can check what is available.",
  },
  {
    question: "Can I arrive by car?",
    answer:
      "Contact the hotel before you travel for current approach, drop-off and parking guidance in Godowlia. Share your arrival time and whether you will have a car or taxi.",
  },
  {
    question: "Do the rooms have air conditioning and Wi-Fi?",
    answer:
      "Yes, the hotel offers air-conditioned rooms and Wi-Fi. Guest rooms also have private bathrooms and televisions.",
  },
  {
    question: "What should I confirm before booking?",
    answer:
      "Confirm the room arrangement, guest identification requirements, meal inclusions, payment terms and cancellation conditions with the hotel. Let the team know about any accessibility needs or special requests in advance.",
  },
];

export const destinations = [
  {
    slug: "dashashwamedh-ghat",
    name: "Dashashwamedh Ghat",
    kicker: "An evening by the Ganga",
    description:
      "As evening arrives, lamps, bells and chanting gather along the river for Ganga Aarti. Dashashwamedh is one of the city's best-known ghats, within walking distance of the hotel.",
    image: "/images/varanasi-ghats.webp",
    alt: "Boats beside the Ganges riverfront in Varanasi",
    imageCaption: "Along the ghats of Varanasi",
    sourceUrl: "https://kashi.gov.in/listing-details/dashashwamedh-ghat",
  },
  {
    slug: "kashi-vishwanath",
    name: "Shri Kashi Vishwanath",
    kicker: "At the heart of Kashi",
    description:
      "Dedicated to Lord Shiva, Kashi Vishwanath is one of the twelve Jyotirlingas. Stay nearby and give your visit the time it deserves; confirm current entry arrangements before you set out.",
    image: "/images/kashi-vishwanath.webp",
    alt: "The golden temple and courtyard of Shri Kashi Vishwanath in Varanasi",
    imageCaption: "Shri Kashi Vishwanath Temple · Pradum Shukla / CC BY 4.0",
    sourceUrl:
      "https://varanasi.nic.in/tourist-place/shri-kashi-vishwanath-temple/",
  },
  {
    slug: "ganges-at-dawn",
    name: "The Ganges at dawn",
    kicker: "See the city wake",
    description:
      "The first light changes the riverfront. Watch the boats, walk the ghats or arrange a local boat ride, and leave a little of the morning unplanned.",
    image: "/images/ganges-boats.webp",
    alt: "A boat on the Ganges at sunrise in Varanasi",
    imageCaption: "Sunrise on the Ganges",
    sourceUrl:
      "https://varanasi.nic.in/gallery/places-of-tourist-attraction/",
  },
];
