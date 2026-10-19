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
  { src: "/images/hotel-lobby.webp", alt: "Hotel Augusto's entrance lobby with patterned seating and warm ceiling lights", caption: "Hotel lobby", category: "Hotel" },
  { src: "/images/deluxe-room.webp", alt: "Double-bed guest room with a tan upholstered headboard at Hotel Augusto", caption: "The Deluxe Room", category: "Rooms", position: "55% center" },
  { src: "/images/twin-room.webp", alt: "Two single beds with green runners in a guest room at Hotel Augusto", caption: "Deluxe Twin Room", category: "Rooms" },
  { src: "/images/room-tea.webp", alt: "Kettle, cups and tea supplies on a tray in a Hotel Augusto guest room", caption: "In-room tea and coffee", category: "Rooms" },
  { src: "/images/dining-room.webp", alt: "Tables and upholstered dining chairs in Hotel Augusto's restaurant", caption: "Hotel restaurant", category: "Dining" },
  { src: "/images/hotel-reception.webp", alt: "Reception desk and seating at Hotel Augusto", caption: "Reception", category: "Hotel" },
  { src: "/images/family-room.webp", alt: "Family guest room with two beds at Hotel Augusto", caption: "Family Room", category: "Rooms" },
  { src: "/images/hotel-exterior.webp", alt: "Hotel Augusto's exterior and illuminated sign after dark", caption: "Augusto after dark", category: "Hotel", position: "center 45%" },
  { src: "/images/hotel-lounge.webp", alt: "Sofas and a coffee table in the Hotel Augusto lounge", caption: "Guest lounge", category: "Hotel" },
  { src: "/images/dining-room-wide.webp", alt: "A wide view of Hotel Augusto's dining room", caption: "The dining room", category: "Dining" },
  { src: "/images/deluxe-room-blue.webp", alt: "Double-bed guest room with a blue upholstered headboard at Hotel Augusto", caption: "Double-bed guest room", category: "Rooms" },
  { src: "/images/room-bathroom.webp", alt: "A tiled private bathroom in a Hotel Augusto guest room", caption: "Guest bathroom", category: "Rooms" },
];

export default function GalleryPage() {
  return (
    <main id="main" className="gallery-page apple-editorial">
      <section className="container apple-page-intro gallery-intro">
        <Reveal><p className="page-context">Hotel Augusto in pictures</p><h1>A look inside.</h1><p className="page-lead">Your room. And everything around it.</p><p className="page-description">Explore the rooms, restaurant and shared spaces before your stay.</p></Reveal>
      </section>
      <section className="container gallery-collection" aria-label="Hotel photographs">
        <Gallery images={photographs} />
        <div className="gallery-afterword"><div><h2>Find the room for your visit.</h2><p>Have a preferred layout? Speak with the hotel before you book.</p></div><Link href="/rooms" className="button" style={{ color: "var(--paper)" }}>Explore rooms <ArrowUpRight size={17} aria-hidden="true" /></Link></div>
      </section>
    </main>
  );
}
