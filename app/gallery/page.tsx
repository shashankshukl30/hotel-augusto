import type { Metadata } from "next";
import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { Gallery, type GalleryImage } from "@/components/gallery";
import { Reveal } from "@/components/reveal";
import "../editorial-pages.css";

export const metadata: Metadata = {
  title: { absolute: "Hotel Augusto Gallery | Rooms and Spaces in Varanasi" },
  description: "Take a closer look at Hotel Augusto, Varanasi. Explore photographs of the guest rooms, reception, restaurant and the hotel before planning your stay.",
};

// Real property photography. Source URLs and file hashes are retained in
// research/assets/asset-manifest.json; destination imagery belongs on /varanasi.
const photographs: GalleryImage[] = [
  { src: "/images/hotel-lobby.webp", alt: "Hotel Augusto's entrance lobby with patterned seating and warm ceiling lights", caption: "A first look inside", category: "Hotel" },
  { src: "/images/deluxe-room.webp", alt: "Double-bed guest room with a tan upholstered headboard at Hotel Augusto", caption: "The Deluxe Room", category: "Rooms", position: "55% center" },
  { src: "/images/twin-room.webp", alt: "Two single beds with green runners in a guest room at Hotel Augusto", caption: "A room to share", category: "Rooms" },
  { src: "/images/room-tea.webp", alt: "Kettle, cups and tea supplies on a tray in a Hotel Augusto guest room", caption: "The small comforts", category: "Rooms" },
  { src: "/images/dining-room.webp", alt: "Tables and upholstered dining chairs in Hotel Augusto's restaurant", caption: "Around the table", category: "Dining" },
  { src: "/images/hotel-reception.webp", alt: "Reception desk and seating at Hotel Augusto", caption: "A welcome in Godowlia", category: "Hotel" },
  { src: "/images/family-room.webp", alt: "Family guest room with two beds at Hotel Augusto", caption: "Stay together", category: "Rooms" },
  { src: "/images/hotel-exterior.webp", alt: "Hotel Augusto's exterior and illuminated sign after dark", caption: "Your address in Varanasi", category: "Hotel", position: "center 45%" },
  { src: "/images/hotel-lounge.webp", alt: "Sofas and a coffee table in the Hotel Augusto lounge", caption: "A moment between plans", category: "Hotel" },
  { src: "/images/dining-room-wide.webp", alt: "A wide view of Hotel Augusto's dining room", caption: "The dining room", category: "Dining" },
  { src: "/images/deluxe-room-blue.webp", alt: "Double-bed guest room with a blue upholstered headboard at Hotel Augusto", caption: "Another room, another detail", category: "Rooms" },
  { src: "/images/room-bathroom.webp", alt: "A tiled private bathroom in a Hotel Augusto guest room", caption: "A closer look", category: "Rooms" },
];

export default function GalleryPage() {
  return (
    <main id="main" className="gallery-page">
      <section className="container page-intro gallery-intro">
        <Reveal><p className="eyebrow">A closer look · Hotel Augusto</p><h1 className="display">Picture<br /><em>your stay.</em></h1></Reveal>
        <Reveal className="gallery-intro-note" delay={0.1}><p>From your first step inside to the room you make your own. Explore the spaces at Augusto, one photograph at a time.</p><Link href="/rooms" className="text-link">Explore our rooms <ArrowUpRight size={17} aria-hidden="true" /></Link></Reveal>
      </section>
      <section className="container section-space gallery-collection" aria-label="Hotel photographs">
        <Gallery images={photographs} />
        <div className="gallery-afterword"><p>Every room has its own details. For a particular layout or preference, speak with us before you book.</p><Link href="/contact" className="text-link">Let&apos;s plan your stay <ArrowUpRight size={17} aria-hidden="true" /></Link></div>
      </section>
    </main>
  );
}
