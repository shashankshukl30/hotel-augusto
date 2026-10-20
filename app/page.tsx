import Image from "next/image";
import Link from "next/link";
import { ArrowUpRight, ArrowRight } from "lucide-react";
import { HomeHero } from "@/components/home-hero";
import { RoomShowcase } from "@/components/room-showcase";
import { Reveal } from "@/components/reveal";
import { ScrollPhoto } from "@/components/scroll-photo";
import { ScrollStatement } from "@/components/scroll-statement";
import "./home.css";

export default function Home() {
  return <main id="main">
    <HomeHero/>
    <nav className="home-directory" aria-label="Discover Hotel Augusto"><span>Make yourself at home.</span><Link href="/hotel">The hotel <ArrowUpRight size={16}/></Link><Link href="/rooms">Our rooms <ArrowUpRight size={16}/></Link><Link href="/dining">Dining <ArrowUpRight size={16}/></Link><Link href="/varanasi">The neighbourhood <ArrowUpRight size={16}/></Link></nav>
    <section id="discover" className="home-intro container section-space">
      <div className="home-intro-title"><p className="section-kicker">Welcome to Augusto.</p><ScrollStatement/></div>
      <ScrollPhoto className="home-intro-image" src="/images/hotel-lobby.webp" alt="The welcoming lobby and reception at Hotel Augusto" sizes="(max-width:600px) 100vw, 50vw" position="48% center"/>
      <Reveal className="home-intro-note"><p><strong>Varanasi starts right outside.</strong> From Godowlia, step into its lanes, temples and life along the Ganges.</p><p>Come back to a comfortable room, vegetarian dining and a familiar welcome. A little space to make the city your own.</p><Link href="/hotel" className="text-link">Get to know Augusto <ArrowUpRight size={20}/></Link><span className="intro-location">Godowlia · Varanasi · India</span></Reveal>
    </section>
    <section className="home-rooms section-space" aria-labelledby="rooms-title"><div className="container">
      <Reveal><div className="home-section-heading"><div><p className="section-kicker">Your room. Your downtime.</p><h2 id="rooms-title">Room to unwind.</h2></div><Link href="/rooms" className="text-link">Discover all rooms <ArrowUpRight size={20}/></Link></div></Reveal>
      <RoomShowcase/>
    </div></section>
    <section className="home-dining container section-space" aria-labelledby="dining-title">
      <Link className="home-dining-photo" href="/dining" aria-label="Explore dining at Hotel Augusto"><Image src="/images/google-dining-room.webp" alt="Tables and seating in Hotel Augusto’s dining room" fill sizes="(max-width:700px) 750px, 55vw" quality={85}/><span className="photo-link-arrow"><ArrowUpRight size={25}/></span></Link>
      <div className="home-dining-copy"><Reveal><p className="section-kicker">At the table.</p><h2 id="dining-title">A pause.<br/>A good meal.<br/>Back to the city.</h2></Reveal><p>Vegetarian dining, right here at Augusto. Settle in for a meal between the places you came to see.</p><Link href="/dining" className="text-link">Explore dining <ArrowUpRight size={20}/></Link></div>
    </section>
    <section className="home-city" aria-labelledby="city-title"><ScrollPhoto className="home-city-photo" src="/images/ganges-boats.webp" alt="A rowing boat on the Ganges at sunrise" sizes="100vw"/><div className="home-city-copy"><Reveal><p className="section-kicker">Beyond Augusto.</p><h2 id="city-title">Some places<br/>stay with you.</h2></Reveal><p>The first light on the Ganges. The lanes around Kashi Vishwanath. An evening by the ghats. Find your own way into Varanasi.</p><Link href="/varanasi" className="text-link">Explore the neighbourhood <ArrowUpRight size={20}/></Link><span className="city-photo-label">The Ganges, Varanasi · Destination photograph</span></div></section>
    <section className="home-gallery-link container"><p>A closer look at life inside Augusto.</p><Link href="/gallery">Visit the gallery <ArrowRight size={32}/></Link></section>
  </main>;
}
