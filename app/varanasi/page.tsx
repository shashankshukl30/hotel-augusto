import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { ArrowUpRight, ChevronRight, MapPin } from "lucide-react";
import { Reveal } from "@/components/reveal";
import { hotel } from "@/content/hotel";
import "../editorial-pages.css";

export const metadata: Metadata = {
  title: { absolute: "Explore Varanasi: Ghats and Temples | Hotel Augusto" },
  description: "Discover Varanasi from Hotel Augusto in Godowlia. Explore the Ganga, Kashi Vishwanath Temple and the evening aarti at Dashashwamedh Ghat.",
};

export default function VaranasiPage() {
  return (
    <main id="main" className="destination-page apple-editorial">
      <section className="container apple-page-intro">
        <Reveal><p className="page-context">Around Hotel Augusto</p><h1>Explore Varanasi.</h1><p className="page-lead">The temple. The river. The city around you.</p><p className="page-description">Stay in Godowlia, within walking distance of Kashi Vishwanath Temple and Dashashwamedh Ghat.</p><Link href="/contact" className="button" style={{ color: "var(--paper)" }}>Find the hotel <ChevronRight size={18} aria-hidden="true" /></Link></Reveal>
      </section>

      <div className="container destination-panorama">
        <figure><div className="destination-hero"><Image src="/images/varanasi-ghats.webp" alt="Rowboats on the Ganga with the buildings and stone steps of Varanasi's riverfront behind them" fill priority sizes="(max-width: 760px) 92vw, 88vw" /></div><figcaption>Along the Ganga in Varanasi.</figcaption></figure>
      </div>

      <section className="destination-experiences" aria-labelledby="experiences-heading">
        <div className="container">
          <Reveal className="destination-section-heading"><h2 id="experiences-heading">From sunrise<br />to evening aarti.</h2><p>Explore the river, the temple and the ghats.</p></Reveal>
          <article className="river-feature" id="river" aria-labelledby="river-heading">
            <div className="river-feature-image"><Image src="/images/ganges-dawn.webp" alt="Boats on the Ganga in the soft golden light of sunrise" fill sizes="(max-width: 760px) 88vw, 49vw" /></div>
            <div className="river-feature-copy"><Reveal><p className="feature-context">On the water</p><h3 id="river-heading">The Ganga<br />at sunrise.</h3><p>See Varanasi from the river. Dawn brings soft light to the ghats, with boats on the water and the city beginning its day along the steps.</p><p>Boat rides are available around Dashashwamedh Ghat. Confirm the route and fare locally before setting out.</p><a className="editorial-link" href="https://varanasi.nic.in/gallery/places-of-tourist-attraction/" target="_blank" rel="noreferrer">Explore the riverfront <ArrowUpRight size={16} aria-hidden="true" /></a></Reveal></div>
          </article>
          <div className="destination-card-grid">
            <article className="destination-card" id="temple" aria-labelledby="temple-heading">
              <div className="destination-card-image temple-image"><Image src="/images/kashi-vishwanath.webp" alt="The golden shrine of Shri Kashi Vishwanath Temple with visitors in the courtyard" fill sizes="(max-width: 760px) 88vw, 43vw" /></div>
              <div className="destination-card-copy"><p className="feature-context">A place of devotion</p><h3 id="temple-heading">Shri Kashi<br />Vishwanath Temple.</h3><p>Dedicated to Lord Shiva, Kashi Vishwanath is one of the twelve Jyotirlingas. It stands on the western bank of the Ganga, within walking distance of the hotel.</p><a className="editorial-link" href="https://varanasi.nic.in/tourist-place/shri-kashi-vishwanath-temple/" target="_blank" rel="noreferrer">About the temple <ArrowUpRight size={16} aria-hidden="true" /></a><p className="destination-credit">Photo: <a href="https://commons.wikimedia.org/wiki/File:Kashi_Vishwanath_Temple_in_2025.jpg" target="_blank" rel="noreferrer">Pradum Shukla</a> · <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noreferrer">CC BY 4.0</a></p></div>
            </article>
            <article className="destination-card" id="aarti" aria-labelledby="aarti-heading">
              <div className="destination-card-image evening-image"><Image src="/images/ganges-boats.webp" alt="A wooden boat on the Ganga beneath the orange sun in Varanasi" fill sizes="(max-width: 760px) 88vw, 43vw" /><span className="destination-image-caption">Along the Ganga.</span></div>
              <div className="destination-card-copy"><p className="feature-context">At Dashashwamedh Ghat</p><h3 id="aarti-heading">An evening<br />at the Ganga Aarti.</h3><p>Lamps, chants and bells bring the riverfront together at the evening aarti. Leave time to reach the ghat and find a place to take it in.</p><a className="editorial-link" href="https://kashi.gov.in/listing-details/dashashwamedh-ghat" target="_blank" rel="noreferrer">Discover Dashashwamedh <ArrowUpRight size={16} aria-hidden="true" /></a></div>
            </article>
          </div>
        </div>
      </section>

      <section className="container destination-arrival" aria-labelledby="arrival-heading">
        <Reveal><div className="arrival-icon"><MapPin size={28} strokeWidth={1.7} aria-hidden="true" /></div><h2 id="arrival-heading">Your address in Godowlia.</h2><p>{hotel.address[0]}. {hotel.address[1]}.<br />{hotel.address[2]}.</p><div className="arrival-actions"><a href={hotel.mapsUrl} target="_blank" rel="noreferrer" className="button" style={{ color: "var(--paper)" }}>Get directions <ArrowUpRight size={17} aria-hidden="true" /></a><Link href="/rooms" className="editorial-link">Explore rooms <ChevronRight size={18} aria-hidden="true" /></Link></div></Reveal>
      </section>
    </main>
  );
}
