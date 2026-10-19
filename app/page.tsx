import Image from "next/image";
import Link from "next/link";
import { ArrowUpRight, MoveUpRight } from "lucide-react";
import { HomeHero } from "@/components/home-hero";
import { RoomShowcase } from "@/components/room-showcase";
import { Reveal } from "@/components/reveal";
import "./home.css";

export default function Home() {
  return <main id="main">
    <HomeHero/>
    <div className="welcome-strip"><span>IN THE HEART OF GODOWLIA</span><i/><span>ROOMS FOR YOUR KIND OF STAY</span><i/><span>PURE VEGETARIAN DINING</span></div>
    <section id="welcome" className="welcome-section container section-space">
      <Reveal className="welcome-heading"><span className="eyebrow">01 / YOUR PLACE IN THE CITY</span><h2 className="display">All the life of Kashi.<br/><em>A little room<br className="desktop-break"/> to pause.</em></h2></Reveal>
      <Reveal className="welcome-story" delay={.12}><span className="small-rule"/><p>Some cities are visited. Varanasi is felt. In its winding lanes, along its river, and in the everyday rituals that make it unlike anywhere else.</p><p>At Hotel Augusto, you’re right here in Godowlia. Set out for the ghats and temples, find your own rhythm, then come back to a comfortable room and a familiar welcome.</p><Link href="/contact" className="text-link">Find us in Godowlia <ArrowUpRight size={18}/></Link></Reveal>
      <Reveal className="welcome-photo"><div className="image-wrap"><Image src="/images/hotel-lobby.webp" alt="Warm wood finishes and seating in the real Hotel Augusto lobby" fill sizes="(max-width: 800px) 90vw, 54vw" quality={85}/></div><span className="photo-caption">Step inside · The lobby at Hotel Augusto</span></Reveal>
      <Reveal className="welcome-aside"><span className="welcome-script">Namaste.</span><p>Make yourself<br/>at home in Kashi.</p><svg width="104" height="112" viewBox="0 0 104 112" aria-hidden="true" fill="none"><path d="M22 91V40a30 30 0 0 1 60 0v51M31 91V41a21 21 0 0 1 42 0v50M40 91V42a12 12 0 0 1 24 0v49M14 92h76M7 101h90M0 110h104M52 0v7" stroke="currentColor" strokeWidth=".8"/></svg></Reveal>
    </section>
    <section className="home-rooms section-space" aria-labelledby="rooms-title"><div className="container"><Reveal className="section-heading"><div><span className="eyebrow">02 / A GOOD NIGHT, A NEW DAY</span><h2 id="rooms-title" className="display">Unpack. Unwind.<br/><em>You’re here.</em></h2></div><div className="section-heading-note"><p>For a trip together, a family gathering,<br/>or time spent finding your own way.</p><Link href="/rooms" className="text-link">Explore all rooms <ArrowUpRight size={18}/></Link></div></Reveal><RoomShowcase/></div></section>
    <section className="dining-section" aria-labelledby="dining-title"><div className="container dining-grid"><Reveal className="dining-copy"><span className="eyebrow">03 / A TABLE TO COME BACK TO</span><h2 className="display" id="dining-title">Good food.<br/><em>Easy company.</em></h2><p>A day in Varanasi works up an appetite. Settle in at our pure vegetarian restaurant, or make an evening of staying in with room service.</p><p className="dining-small">Simple comforts, right where you’re staying.</p><Link href="/contact#enquire" className="text-link">Ask us about dining <ArrowUpRight size={18}/></Link></Reveal><Reveal className="dining-photo"><div className="image-wrap"><Image src="/images/dining-room.webp" alt="Tables and upholstered chairs in Hotel Augusto’s vegetarian dining room" fill sizes="(max-width: 800px) 90vw, 50vw" quality={85}/></div><span className="dining-photo-label">AT THE HOTEL / VEGETARIAN DINING</span></Reveal></div></section>
    <section className="city-section container section-space" aria-labelledby="city-title"><Reveal className="section-heading"><div><span className="eyebrow">04 / STEP OUTSIDE</span><h2 id="city-title" className="display">A city of a thousand<br/><em>little moments.</em></h2></div><Link href="/varanasi" className="text-link">Meet Varanasi <ArrowUpRight size={18}/></Link></Reveal><div className="city-spread"><Reveal className="city-photo"><div className="image-wrap"><Image src="/images/ganges-boats.webp" alt="A wooden boat on the Ganges in the warm light of a Varanasi sunrise" fill sizes="(max-width: 800px) 90vw, 50vw" quality={85}/></div><span className="photo-caption">The Ganges at first light · Varanasi</span></Reveal><div className="city-notes"><span className="eyebrow">GO SLOW. LOOK CLOSER.</span>{[
      { number: "01", title: "Mornings by the river", text: "Start with the ghats, the water and the city slowly finding its voice.", href: "/varanasi#river" },
      { number: "02", title: "The heart of Kashi", text: "Make time for Shri Kashi Vishwanath Temple and the lanes that surround it.", href: "/varanasi#temple" },
      { number: "03", title: "An evening to remember", text: "Head to Dashashwamedh Ghat for the lamps and sounds of the Ganga Aarti.", href: "/varanasi#aarti" },
    ].map(item => <Reveal key={item.number}><Link href={item.href} className="city-note"><span>{item.number}</span><div><h3>{item.title}</h3><p>{item.text}</p></div><MoveUpRight size={20}/></Link></Reveal>)}<p className="city-footnote">Our Godowlia address puts you close to the old city.<br/>Ask the hotel for the best way to arrive and explore.</p></div></div></section>
    <section className="home-gallery container" aria-labelledby="gallery-title"><div className="gallery-teaser-top"><span className="eyebrow">05 / A FEW MOMENTS AT AUGUSTO</span><Link href="/gallery" className="text-link" id="gallery-title">The full picture <ArrowUpRight size={18}/></Link></div><div className="gallery-teaser-images">{[
      { src: "/images/hotel-exterior.webp", alt: "The illuminated Hotel Augusto entrance in Godowlia", caption: "A familiar welcome" },
      { src: "/images/deluxe-room-blue.webp", alt: "Hotel Augusto guest room with a blue upholstered headboard", caption: "A place to settle in" },
      { src: "/images/room-tea.webp", alt: "Tea and coffee facilities in a Hotel Augusto guest room", caption: "The little comforts" },
    ].map((item,index) => <Reveal key={item.src} delay={index*.08}><Link href="/gallery" className="gallery-teaser"><div className="image-wrap"><Image src={item.src} alt={item.alt} fill sizes="(max-width: 600px) 60vw, 30vw"/></div><span>{item.caption}<ArrowUpRight size={16}/></span></Link></Reveal>)}</div></section>
  </main>;
}
