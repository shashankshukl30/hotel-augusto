import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { ArrowDown, ArrowUpRight } from "lucide-react";
import { Reveal } from "@/components/reveal";
import "../editorial-pages.css";

export const metadata: Metadata = {
  title: { absolute: "Explore Varanasi: Ghats and Temples | Hotel Augusto" },
  description: "Discover Varanasi from Hotel Augusto in Godowlia. Explore the Ganga, Kashi Vishwanath Temple and the evening aarti at Dashashwamedh Ghat.",
};

export default function VaranasiPage() {
  return (
    <main id="main" className="destination-page">
      <section className="container page-intro destination-intro">
        <Reveal><p className="eyebrow">Beyond your room · Varanasi</p><h1 className="display">A city with<br />its own <em>rhythm.</em></h1></Reveal>
        <Reveal className="destination-intro-note" delay={0.1}>
          <p>First light on the Ganga. A walk to the temple. An evening by the ghats. There is more than one way to find your Varanasi.</p>
          <a className="text-link" href="#discover">A little inspiration <ArrowDown size={16} aria-hidden="true" /></a>
        </Reveal>
      </section>

      <figure className="destination-hero">
        <Image src="/images/varanasi-ghats.webp" alt="Rowboats on the Ganga with the buildings and stone steps of Varanasi's riverfront behind them" fill priority sizes="100vw" />
        <figcaption><span>Varanasi, from the river</span><span>Life along the Ganga</span></figcaption>
      </figure>

      <section className="container destination-location section-space" id="discover" aria-labelledby="location-heading">
        <Reveal><p className="eyebrow">Your address in the city</p><h2 className="display" id="location-heading">Stay close.<br /><em>Wander further.</em></h2></Reveal>
        <Reveal className="destination-location-copy" delay={0.1}>
          <p>Hotel Augusto places you in Godowlia, within walking distance of Kashi Vishwanath Temple and Dashashwamedh Ghat. Step out into the city, then return to a place of your own.</p>
          <Link className="text-link" href="/contact">Find Hotel Augusto <ArrowUpRight size={17} aria-hidden="true" /></Link>
        </Reveal>
      </section>

      <section className="container river-chapter section-space" id="river" aria-labelledby="river-heading">
        <Reveal><div className="river-chapter-image"><Image src="/images/ganges-dawn.webp" alt="Boats on the Ganga in the soft golden light of sunrise" fill sizes="(max-width: 760px) 88vw, 53vw" /><span className="image-footnote">First light on the Ganga · Varanasi</span></div></Reveal>
        <Reveal className="river-chapter-copy" delay={0.1}>
          <p className="eyebrow">01 / At first light</p>
          <h2 className="display" id="river-heading">Begin with<br /><em>the river.</em></h2>
          <p>See the ghats from a different perspective. Dawn brings soft light to the riverfront, with boats on the water and the city beginning its day along the steps.</p>
          <p>Boat rides are available around Dashashwamedh Ghat. Arrange your ride locally and confirm the route and fare before setting out.</p>
          <a className="text-link" href="https://varanasi.nic.in/gallery/places-of-tourist-attraction/" target="_blank" rel="noreferrer">The city&apos;s river guide <ArrowUpRight size={16} aria-hidden="true" /></a>
        </Reveal>
      </section>

      <section className="container city-chapters section-space" aria-label="Temples and evenings in Varanasi">
        <Reveal><figure className="temple-portrait"><div className="temple-image"><Image src="/images/kashi-vishwanath.webp" alt="The golden shrine of Shri Kashi Vishwanath Temple with visitors in the courtyard" fill sizes="(max-width: 760px) 88vw, 44vw" /></div><figcaption>Shri Kashi Vishwanath Temple<span>Photograph by <a href="https://commons.wikimedia.org/wiki/File:Kashi_Vishwanath_Temple_in_2025.jpg" target="_blank" rel="noreferrer">Pradum Shukla</a> · <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noreferrer">CC BY 4.0</a></span></figcaption></figure></Reveal>
        <div className="city-chapter-stories">
        <Reveal className="city-chapter">
          <p className="eyebrow">02 / A place of devotion</p>
          <h2 className="display" id="temple">Shri Kashi<br /><em>Vishwanath.</em></h2>
          <div className="city-chapter-copy"><p>Dedicated to Lord Shiva, Kashi Vishwanath is one of the twelve Jyotirlingas. The temple stands on the western bank of the Ganga, at the heart of the city&apos;s spiritual life.</p><a className="text-link" href="https://varanasi.nic.in/tourist-place/shri-kashi-vishwanath-temple/" target="_blank" rel="noreferrer">About the temple <ArrowUpRight size={16} aria-hidden="true" /></a></div>
        </Reveal>
        <Reveal className="city-chapter" delay={0.1}>
          <p className="eyebrow">03 / As evening arrives</p>
          <h2 className="display" id="aarti">The light<br /><em>of the aarti.</em></h2>
          <div className="city-chapter-copy"><p>At Dashashwamedh Ghat, the evening Ganga Aarti brings lamps, chants and bells to the riverfront. Leave time to reach the ghat and find a place to take it in.</p><a className="text-link" href="https://kashi.gov.in/listing-details/dashashwamedh-ghat" target="_blank" rel="noreferrer">Discover Dashashwamedh <ArrowUpRight size={16} aria-hidden="true" /></a></div>
        </Reveal>
        </div>
      </section>

      <section className="destination-close" aria-labelledby="destination-close-heading">
        <div className="container destination-close-inner">
          <Reveal><p className="eyebrow">A little room for the unexpected</p><h2 className="display" id="destination-close-heading">Make the city<br /><em>part of your stay.</em></h2></Reveal>
          <Reveal className="destination-close-note" delay={0.1}><p>Plan the moments that matter to you. Leave a little space for everything in between.</p><Link href="/rooms" className="button" style={{ color: "var(--paper)" }}>Find your room <ArrowUpRight size={18} aria-hidden="true" /></Link></Reveal>
        </div>
      </section>
    </main>
  );
}
