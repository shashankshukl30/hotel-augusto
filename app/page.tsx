import Image from "next/image";
import Link from "next/link";
import { ChevronRight, ArrowUpRight } from "lucide-react";
import { HomeHero } from "@/components/home-hero";
import { RoomShowcase } from "@/components/room-showcase";
import { Reveal } from "@/components/reveal";
import "./home.css";

export default function Home() {
  return <main id="main">
    <HomeHero/>
    <section id="welcome" className="welcome-section container">
      <Reveal><h2>Stay close to what<br/>brought you here.</h2></Reveal>
      <Reveal><p><strong>Godowlia is your starting point.</strong> The temples, the ghats, the old-city lanes. Spend the day discovering Varanasi, then come back to a comfortable room and a familiar welcome.</p><Link href="/contact" className="text-link">Find Hotel Augusto <ChevronRight size={17}/></Link></Reveal>
    </section>
    <section className="home-rooms section-space" aria-labelledby="rooms-title"><div className="container">
      <Reveal><div className="home-section-heading"><h2 id="rooms-title">Your room.<br/><span>Your kind of stay.</span></h2><Link href="/rooms" className="text-link">Explore the rooms <ChevronRight size={17}/></Link></div></Reveal>
      <RoomShowcase/>
    </div></section>
    <section className="hotel-highlights section-space" aria-labelledby="highlights-title"><div className="container">
      <Reveal><div className="home-section-heading"><h2 id="highlights-title">A little more<br/>to come home to.</h2><Link href="/gallery" className="text-link">See the hotel <ChevronRight size={17}/></Link></div></Reveal>
      <div className="highlight-grid">
        <Reveal><Link href="/gallery" className="highlight-card"><div className="highlight-copy"><p>Vegetarian dining</p><h3>Good food.<br/>Right here.</h3></div><Image src="/images/dining-room.webp" alt="The vegetarian dining room at Hotel Augusto" fill sizes="(max-width:600px) 90vw, 45vw" quality={85}/><span className="highlight-plus"><ArrowUpRight size={23}/></span></Link></Reveal>
        <Reveal delay={.1}><Link href="/gallery" className="highlight-card"><div className="highlight-copy"><p>Make yourself comfortable</p><h3>A welcome<br/>you can feel.</h3></div><Image src="/images/hotel-lobby.webp" alt="The reception and lobby at Hotel Augusto" fill sizes="(max-width:600px) 90vw, 45vw" quality={85}/><span className="highlight-plus"><ArrowUpRight size={23}/></span></Link></Reveal>
      </div>
      <p className="highlights-footnote">Air-conditioned rooms. Wi-Fi. Room service. The essentials, taken care of.</p>
    </div></section>
    <section className="home-city" aria-labelledby="city-title">
      <div className="container"><Reveal><div className="home-section-heading"><h2 id="city-title">Varanasi is calling.</h2><Link href="/varanasi" className="text-link">Get to know the city <ChevronRight size={17}/></Link></div></Reveal></div>
      <div className="city-feature"><Image src="/images/varanasi-ghats.webp" alt="Life and boats along the riverfront ghats of Varanasi" fill sizes="(max-width:600px) 1000px, 100vw" quality={85}/><div className="city-feature-shade"/><div className="city-feature-copy"><p>Beyond your room</p><h3>The river. The rituals.<br/>The feeling of being here.</h3><Link href="/varanasi" className="button button-light" style={{color:"var(--ink)"}}>Explore Varanasi <ChevronRight size={17}/></Link></div><span className="city-photo-label">The ghats of Varanasi · Destination photograph</span></div>
    </section>
    <section className="stay-simple container section-space">
      <Reveal><h2>A stay worth planning.<br/><span>Made simple.</span></h2></Reveal>
      <div className="stay-simple-content"><p>Choose your room. Tell us your dates.<br/>Speak directly with the hotel on WhatsApp<br className="desktop-break"/> for availability and the details of your stay.</p><Link href="/contact#enquire" className="button" style={{color:"var(--paper)"}}>Let’s plan your stay</Link></div>
    </section>
  </main>;
}
