import Image from "next/image";
import Link from "next/link";
import { ArrowUpRight, BedDouble, BellRing, Coffee, ConciergeBell, MapPin, Phone, Plus, Snowflake, Utensils, Wifi } from "lucide-react";
import { HomeHero } from "@/components/home-hero";
import { StayBar } from "@/components/stay-bar";
import { Reveal } from "@/components/reveal";
import { ScrollPhoto } from "@/components/scroll-photo";
import { CityItinerary } from "@/components/city-itinerary";
import { ArrivalGuide } from "@/components/arrival-guide";
import { WhatsAppIcon } from "@/components/whatsapp-icon";
import { hotel, rooms } from "@/content/hotel";
import { guestReviewHighlight, practicalFaqs, reviewSources } from "@/content/hospitality";
import "./home.css";

const detailPhotos = [
  {src:"/images/deluxe-room-blue.webp",alt:"Another double-bed room layout at Hotel Augusto"},
  {src:"/images/room-bathroom.webp",alt:"A bathroom photographed at Hotel Augusto"},
  {src:"/images/family-room-alternate.webp",alt:"Another family-room layout at Hotel Augusto"},
];
const essentials = [
  {icon:Snowflake,label:"Air-conditioned rooms"},{icon:Wifi,label:"Wi-Fi"},
  {icon:Utensils,label:"Vegetarian dining"},{icon:ConciergeBell,label:"24-hour reception"},
  {icon:Coffee,label:"Room service"},{icon:BellRing,label:"Housekeeping"},
];

export default function Home() {
  const whatsapp = `https://wa.me/${hotel.whatsappNumber}?text=${encodeURIComponent(hotel.bookingMessage)}`;
  return <main id="main">
    <HomeHero/>
    <div className="home-reservation container"><StayBar/></div>
    <div className="home-location-band container"><span><MapPin size={15}/> August Kunda Road, Godowlia</span><span>A stay close to the temples & ghats</span><a href={hotel.mapsUrl} target="_blank" rel="noopener noreferrer">Find us in Varanasi <ArrowUpRight size={15}/></a></div>

    <section id="discover" className="home-welcome container section-space">
      <Reveal className="home-welcome-copy">
        <p className="eyebrow">Namaste. Welcome to Augusto.</p>
        <h2>In the heart of it.<br/><em>At home in it.</em></h2>
        <p>The lanes of Godowlia. The sound of temple bells. The river, waiting at the end of a walk. This is the Varanasi you came to meet.</p>
        <p>At Hotel Augusto, settle into an air-conditioned room, gather for a vegetarian meal and make the old city your neighbourhood. Shri Kashi Vishwanath Temple and Dashashwamedh Ghat are within walking distance.</p>
        <dl className="welcome-facts"><div><dt>Your neighbourhood</dt><dd>Godowlia, Varanasi</dd></div><div><dt>Your welcome</dt><dd>24-hour reception</dd></div></dl>
        <Link href="/hotel" className="text-link">Get to know the hotel <ArrowUpRight size={18}/></Link>
      </Reveal>
      <div className="home-welcome-photos"><ScrollPhoto className="welcome-photo-main" src="/images/hotel-lounge.webp" alt="The lounge and seating area inside Hotel Augusto" sizes="(max-width:600px) 90vw, 50vw"/><Reveal className="welcome-photo-detail"><Image src="/images/hotel-reception.webp" alt="Hotel Augusto's reception counter" fill sizes="(max-width:600px) 48vw, 24vw"/></Reveal><p className="welcome-photo-caption">A warm welcome.<br/>A place to return to.</p></div>
    </section>
    <div className="home-amenities" aria-label="Hotel essentials"><div className="container">{essentials.map(({icon:Icon,label})=><span key={label}><Icon strokeWidth={1.4}/>{label}</span>)}</div></div>

    <section className="home-rooms section-space" id="rooms" aria-labelledby="home-rooms-title"><div className="container">
      <Reveal className="home-section-heading"><div><p className="eyebrow">Rooms & restful nights</p><h2 id="home-rooms-title">Make yourself<br/><em>at home.</em></h2></div><p>Three room choices. Your own rhythm.<br/>Find the bed arrangement that suits the way you travel.</p></Reveal>
      <div className="home-room-collection">{rooms.map((room,index)=><article className="home-room-spread" key={room.slug}>
        <Reveal className="home-room-photos"><Link href={`/rooms/${room.slug}`} className="home-room-main" aria-label={`Explore ${room.name}`}><Image src={room.image} alt={room.alt} fill sizes="(max-width:800px) 90vw, 52vw" quality={85}/></Link><div className="home-room-detail"><Image src={detailPhotos[index].src} alt={detailPhotos[index].alt} fill sizes="(max-width:600px) 40vw, 20vw" quality={85}/></div></Reveal>
        <Reveal className="home-room-copy"><span className="room-number">0{index+1}</span><h3>{room.name}</h3><div className="home-room-bed"><BedDouble size={19} strokeWidth={1.4}/>{room.bedLabel}</div><p>{room.description}</p><ul className="home-room-features">{room.features.map(feature=><li key={feature}>{feature}</li>)}</ul><div className="home-room-actions"><Link href={`/rooms/${room.slug}`} className="button" style={{color:"var(--paper)"}}>Explore the room <ArrowUpRight size={18}/></Link><Link href={`/contact?room=${room.slug}#enquire`} className="text-link">Enquire <ArrowUpRight size={17}/></Link></div></Reveal>
      </article>)}</div>
      <div className="room-compare-line"><p>A double bed, separate singles or space to stay together?</p><Link className="text-link" href="/rooms/compare">Compare our rooms <ArrowUpRight size={19}/></Link></div>
    </div></section>

    <section className="home-dining"><div className="container home-dining-grid"><Reveal className="home-dining-copy"><p className="eyebrow">At the table</p><h2>A little time.<br/><em>A good meal.</em></h2><p>Come back from the lanes and take a seat. Our vegetarian restaurant is a place to eat together, pause between plans and enjoy being here.</p><p>Room service is available too. Ask the team about the current menu, serving times and meals included in your stay.</p><div className="dining-facts"><span>Vegetarian restaurant</span><span>Room service</span></div><Link href="/dining" className="text-link">Discover dining at Augusto <ArrowUpRight size={18}/></Link></Reveal><Reveal><div className="home-dining-photo"><Image src="/images/google-dining-room.webp" alt="Marble-topped tables and seating in Hotel Augusto's restaurant" fill sizes="(max-width:600px) 90vw, 60vw" quality={85}/></div><div className="home-dining-caption"><span>The restaurant at Hotel Augusto</span><span>Godowlia · Varanasi</span></div></Reveal></div></section>

    <CityItinerary compact/>
    <section className="home-reviews container" aria-labelledby="guest-experiences"><Reveal className="review-heading"><div><p className="eyebrow">The guest perspective</p><h2 id="guest-experiences">Before you make<br/><em>yourself at home.</em></h2></div><p>See the hotel through other travellers’ experiences. Read independently published reviews and photographs as you plan your stay.</p></Reveal><Reveal className="guest-review-highlight"><blockquote cite={guestReviewHighlight.href}>“{guestReviewHighlight.quote}”</blockquote><div><span>An excerpt from a guest review</span><a href={guestReviewHighlight.href} target="_blank" rel="noopener noreferrer">{guestReviewHighlight.attribution}<ArrowUpRight size={16}/></a></div></Reveal><div className="review-source-links">{reviewSources.slice(0,2).map(source=><a key={source.name} href={source.href} target="_blank" rel="noopener noreferrer"><div><strong>{source.name}</strong><small>{source.description}</small></div><ArrowUpRight size={23}/></a>)}</div></section>

    <section className="home-gallery container"><Reveal className="home-section-heading"><div><p className="eyebrow">A closer look</p><h2>Life <em>inside Augusto.</em></h2></div><Link href="/gallery" className="text-link">See the full gallery <ArrowUpRight size={20}/></Link></Reveal><div className="home-gallery-strip">{[{src:"hotel-lobby",label:"The welcome",alt:"Hotel Augusto lobby"},{src:"google-double-room",label:"The rooms",alt:"A double-bed guest room at Hotel Augusto"},{src:"dining-room-wide",label:"The table",alt:"Dining at Hotel Augusto"}].map(photo=><Link href="/gallery" key={photo.src}><Image src={`/images/${photo.src}.webp`} alt={photo.alt} fill sizes="(max-width:600px) 80vw, 33vw"/><span>{photo.label}</span></Link>)}</div></section>

    <ArrivalGuide/>
    <section className="home-practical"><div className="container home-practical-grid"><Reveal className="home-practical-intro"><p className="eyebrow">Good to know</p><h2>A little planning.<br/><em>An easier stay.</em></h2><p>From your room arrangement to the last turn into Godowlia, a few details make all the difference.</p><Link href="/contact#faq-title" className="text-link">All your stay questions <ArrowUpRight size={19}/></Link></Reveal><div className="home-faq">{practicalFaqs.filter(faq=>["Can I walk to the temple and the ghats?","Which bed arrangements can I choose?","Is breakfast included?","Can I arrive early or leave late?","What should I confirm before booking?"].includes(faq.question)).map(faq=><details key={faq.question} name="home-questions"><summary>{faq.question}<Plus size={20}/></summary><p>{faq.answer}</p></details>)}</div></div></section>

    <section className="home-guides container"><Reveal className="home-section-heading"><div><p className="eyebrow">A useful companion</p><h2>For your time <em>in Kashi.</em></h2></div><Link href="/guides" className="text-link">Explore the stay guide <ArrowUpRight size={19}/></Link></Reveal><div className="home-guide-links"><Link href="/guides/first-visit-to-kashi"><span>01 · Explore</span><h3>Your first visit to Kashi.</h3><p>Make room for the river, the temple and an unhurried walk.</p><ArrowUpRight size={20}/></Link><Link href="/guides/arriving-in-godowlia"><span>02 · Arrive</span><h3>The last part of your journey.</h3><p>Keep the address, drop-off details and hotel contact close.</p><ArrowUpRight size={20}/></Link><Link href="/guides/choosing-your-room"><span>03 · Stay</span><h3>Find your room arrangement.</h3><p>Double, twin or family: a practical guide to choosing your stay.</p><ArrowUpRight size={20}/></Link></div></section>

    <section className="home-reserve" id="reserve"><div className="container home-reserve-grid"><Reveal className="home-reserve-copy"><p className="eyebrow">Come, stay a while</p><h2>Kashi is calling.<br/><em>Your room awaits.</em></h2><p>Tell us when you’re coming and who you’re travelling with. We’ll help you plan your stay at Augusto.</p><div className="home-reserve-contact"><a href={whatsapp} target="_blank" rel="noopener noreferrer"><WhatsAppIcon size={18}/> WhatsApp the hotel</a><a href={hotel.phoneHref}><Phone size={16}/> {hotel.phone}</a></div></Reveal><StayBar compact/></div></section>
  </main>;
}
