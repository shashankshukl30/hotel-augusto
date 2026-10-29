import type { Metadata } from "next";
import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { Gallery, type GalleryImage } from "@/components/gallery";
import { Reveal } from "@/components/reveal";
import "../editorial-pages.css";

export const metadata: Metadata = {
  alternates: { canonical: "/gallery" },
  title: { absolute: "Hotel Augusto Gallery | Rooms and Spaces in Varanasi" },
  description: "Take a closer look at Hotel Augusto, Varanasi. Explore photographs of the guest rooms, reception, restaurant and the hotel before planning your stay.",
};

// Real property photography. Source URLs and file hashes are retained in
// research/assets/asset-manifest.json and research/ota-revision/asset-candidates.json.
// Destination imagery belongs on /varanasi.
const photographs: GalleryImage[] = [
  { src: "/images/hotel-lobby.webp", alt: "Hotel Augusto's entrance lobby with patterned seating and warm ceiling lights", caption: "Hotel lobby", category: "Hotel" },
  { src: "/images/deluxe-room.webp", alt: "Double-bed guest room with a tan upholstered headboard at Hotel Augusto", caption: "The Deluxe Room", category: "Rooms", position: "55% center" },
  { src: "/images/twin-room.webp", alt: "Two single beds with green runners in a guest room at Hotel Augusto", caption: "Deluxe Twin Room", category: "Rooms" },
  { src: "/images/google-double-room.webp", alt: "Double-bed guest room with a curved wooden headboard, wardrobe and television at Hotel Augusto", caption: "Double-bed guest room", category: "Rooms" },
  { src: "/images/dining-room.webp", alt: "Tables and upholstered dining chairs in Hotel Augusto's restaurant", caption: "Hotel restaurant", category: "Dining" },
  { src: "/images/hotel-reception.webp", alt: "Reception desk and seating at Hotel Augusto", caption: "Reception", category: "Hotel" },
  { src: "/images/family-room.webp", alt: "Family guest room with two beds at Hotel Augusto", caption: "Family Room", category: "Rooms" },
  { src: "/images/hotel-exterior.webp", alt: "Hotel Augusto's exterior and illuminated sign after dark", caption: "Augusto after dark", category: "Hotel", position: "center 45%" },
  { src: "/images/deluxe-room-blue-sofa.webp", alt: "A blue sofa, wall-mounted television and patterned curtains in a Hotel Augusto double room", caption: "Blue-headboard double room", category: "Rooms" },
  { src: "/images/hotel-lounge.webp", alt: "Sofas and a coffee table in the Hotel Augusto lounge", caption: "Guest lounge", category: "Hotel" },
  { src: "/images/twin-room-wide.webp", alt: "Two single beds with tufted headboards and teal runners in a Hotel Augusto twin room", caption: "Twin-bed room", category: "Rooms" },
  { src: "/images/dining-room-wide.webp", alt: "A wide view of Hotel Augusto's dining room", caption: "The dining room", category: "Dining" },
  { src: "/images/family-room-wide.webp", alt: "A wide view of a Hotel Augusto family room with two beds, wardrobe and wall-mounted television", caption: "Family room", category: "Rooms" },
  { src: "/images/hotel-corridor.webp", alt: "A guest-floor corridor at Hotel Augusto with terrazzo flooring and wooden room doors", caption: "Guest-floor corridor", category: "Hotel" },
  { src: "/images/deluxe-room-tv.webp", alt: "A double bed with a tufted headboard facing the television unit in a Hotel Augusto room", caption: "Double-bed guest room", category: "Rooms" },
  { src: "/images/hotel-lounge-seating.webp", alt: "Sofas and a glass-topped table in Hotel Augusto's ground-floor lounge, beside the hotel's tour-services board", caption: "Lounge seating", category: "Hotel" },
  { src: "/images/google-family-room.webp", alt: "Two beds with green runners and a small table in a Hotel Augusto guest room", caption: "Two-bed guest room", category: "Rooms" },
  { src: "/images/room-bathroom-wc.webp", alt: "A tiled guest bathroom at Hotel Augusto with a wash basin, WC and hand shower", caption: "Guest bathroom", category: "Rooms", position: "center 62%" },
  { src: "/images/twin-room-orange.webp", alt: "Two single beds with orange runners in a Hotel Augusto twin room", caption: "Twin room, orange runners", category: "Rooms" },
  { src: "/images/hotel-lobby-lift.webp", alt: "Patterned sofas and a glass-topped table in Hotel Augusto's lobby, with steps up to the lift", caption: "Lobby and lift", category: "Hotel" },
  { src: "/images/family-room-corner.webp", alt: "Two beds, a red armchair and a small table in a Hotel Augusto family room", caption: "Family room corner", category: "Rooms" },
  { src: "/images/room-bathroom.webp", alt: "A tiled private bathroom in a Hotel Augusto guest room", caption: "Shower area", category: "Rooms" },
];

export default function GalleryPage() {
  return (
    <main id="main" className="gallery-page editorial-page">
      <section className="container editorial-intro gallery-intro">
        <Reveal className="intro-title"><p className="page-context">Hotel Augusto / Gallery</p><h1>Inside<br />Augusto.</h1></Reveal>
        <Reveal className="intro-note" delay={0.1}><p>See the rooms, restaurant and shared spaces before your stay.</p><Link href="/rooms" className="editorial-link">Find your room <ArrowUpRight size={17} aria-hidden="true" /></Link></Reveal>
      </section>
      <section className="container gallery-collection" aria-label="Hotel photographs">
        <Gallery images={photographs} />
        <Reveal><div className="gallery-afterword"><div><p className="feature-context">Your stay at Augusto</p><h2>Choose your room.</h2><p>Have a preferred layout? Speak with the hotel before you book.</p></div><Link href="/rooms" className="button" style={{ color: "var(--paper)" }}>Explore rooms <ArrowUpRight size={20} aria-hidden="true" /></Link></div></Reveal>
      </section>
    </main>
  );
}
