export type RoomPhotograph = { src: string; alt: string; caption: string };

export const roomImages: Record<string, RoomPhotograph[]> = {
  "deluxe-room": [
    { src: "/images/deluxe-room.webp", alt: "Hotel Augusto Deluxe Room with double bed and wood finishes", caption: "A double bed, cushioned headboard and wood finishes." },
    { src: "/images/deluxe-room-blue.webp", alt: "Another double-room layout at Augusto, with a blue upholstered headboard", caption: "An alternative double-room layout at Augusto." },
    { src: "/images/deluxe-room-tv.webp", alt: "A double bed with a tufted headboard facing the television unit in a Hotel Augusto room", caption: "The bed faces a wall-mounted television and storage unit." },
    { src: "/images/deluxe-room-blue-sofa.webp", alt: "A blue sofa, wall-mounted television and patterned curtains in a Hotel Augusto double room", caption: "A sofa and television in the blue-headboard layout." },
    { src: "/images/deluxe-room-wardrobe.webp", alt: "A double bed, wardrobe and television wall in a Hotel Augusto guest room", caption: "A wardrobe and dressing counter beside the door." },
    { src: "/images/room-tea.webp", alt: "Tea and coffee setup photographed in an Augusto guest room", caption: "A tea and coffee setup photographed at the hotel." },
  ],
  "deluxe-twin-room": [
    { src: "/images/twin-room.webp", alt: "Separate single beds in a Deluxe Twin Room at Hotel Augusto", caption: "Two separate single beds in the Deluxe Twin Room." },
    { src: "/images/twin-room-tv.webp", alt: "Two single beds facing a wall-mounted television in a Hotel Augusto twin room", caption: "Both beds face a wall-mounted television." },
    { src: "/images/twin-room-orange.webp", alt: "Two single beds with orange runners in a Hotel Augusto twin room", caption: "An alternative twin-bed room at Augusto." },
    { src: "/images/room-bathroom.webp", alt: "A bathroom photographed at Hotel Augusto", caption: "A private bathroom photographed at the hotel." },
    { src: "/images/twin-room-window.webp", alt: "Two single beds beneath a small window in a Hotel Augusto twin room", caption: "Another view of the twin-bed layout." },
    { src: "/images/room-tea.webp", alt: "In-room tea and coffee setup at Hotel Augusto", caption: "A tea and coffee setup photographed at the hotel." },
  ],
  "family-room": [
    { src: "/images/family-room.webp", alt: "Two-bed Family Room at Hotel Augusto with sitting area", caption: "Two beds and a sitting area in the Family Room." },
    { src: "/images/family-room-wide.webp", alt: "A wide view of a Hotel Augusto family room with two beds, wardrobe and wall-mounted television", caption: "A wardrobe and television across from the beds." },
    { src: "/images/family-room-alternate.webp", alt: "An alternative family-room layout at Hotel Augusto with two beds and brown headboards", caption: "An alternative family-room layout at Augusto." },
    { src: "/images/family-room-long.webp", alt: "A long family room at Hotel Augusto with a dressing mirror, red armchair and two beds", caption: "A dressing mirror and armchair along the room." },
    { src: "/images/room-tea.webp", alt: "Tea and coffee setup at Hotel Augusto", caption: "A tea and coffee setup photographed at the hotel." },
  ],
};
