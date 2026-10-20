export type RoomPhotograph = { src: string; alt: string; caption: string };

export const roomImages: Record<string, RoomPhotograph[]> = {
  "deluxe-room": [
    { src: "/images/deluxe-room.webp", alt: "Hotel Augusto Deluxe Room with double bed and wood finishes", caption: "A double bed, cushioned headboard and wood finishes." },
    { src: "/images/deluxe-room-blue.webp", alt: "Another double-room layout at Augusto, with a blue upholstered headboard", caption: "An alternative double-room layout at Augusto." },
    { src: "/images/room-tea.webp", alt: "Tea and coffee setup photographed in an Augusto guest room", caption: "A tea and coffee setup photographed at the hotel." },
  ],
  "deluxe-twin-room": [
    { src: "/images/twin-room.webp", alt: "Separate single beds in a Deluxe Twin Room at Hotel Augusto", caption: "Two separate single beds in the Deluxe Twin Room." },
    { src: "/images/room-bathroom.webp", alt: "A bathroom photographed at Hotel Augusto", caption: "A private bathroom photographed at the hotel." },
    { src: "/images/room-tea.webp", alt: "In-room tea and coffee setup at Hotel Augusto", caption: "A tea and coffee setup photographed at the hotel." },
  ],
  "family-room": [
    { src: "/images/family-room.webp", alt: "Two-bed Family Room at Hotel Augusto with sitting area", caption: "Two beds and a sitting area in the Family Room." },
    { src: "/images/family-room-alternate.webp", alt: "An alternative family-room layout at Hotel Augusto with two beds and brown headboards", caption: "An alternative family-room layout at Augusto." },
    { src: "/images/room-tea.webp", alt: "Tea and coffee setup at Hotel Augusto", caption: "A tea and coffee setup photographed at the hotel." },
  ],
};
