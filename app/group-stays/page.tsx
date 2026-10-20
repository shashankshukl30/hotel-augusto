import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { ArrowDown, ArrowUpRight, Phone } from "lucide-react";
import { GroupEnquiry } from "@/components/group-enquiry";
import { Reveal } from "@/components/reveal";
import { hotel } from "@/content/hotel";
import "./group-stays.css";

export const metadata: Metadata = {
  title: "Group Stays in Varanasi | Enquire with Hotel Augusto",
  description: "Planning a family, friends or business stay in Varanasi? Share your dates, requested rooms and guest details with Hotel Augusto in Godowlia.",
};

export default function GroupStaysPage() {
  return <main id="main" className="group-page">
    <section className="container group-intro">
      <Reveal className="group-intro-copy">
        <p className="group-kicker">Hotel Augusto / Group stays</p>
        <h1>A stay.<br/>For everyone.</h1>
        <p>Family, friends or colleagues. Bring your plans together, then ask the hotel about the rooms you need.</p>
        <a href="#group-enquire" className="text-link">Plan a group stay <ArrowDown size={18} aria-hidden="true"/></a>
      </Reveal>
      <Reveal className="group-intro-visual" delay={0.1}>
        <figure><div className="group-intro-photo"><Image src="/images/hotel-lounge.webp"
          alt="Shared lounge seating at Hotel Augusto in Godowlia, Varanasi"
          fill preload sizes="(max-width: 800px) 90vw, 48vw" quality={85}/></div>
          <figcaption>A place to meet before heading out.</figcaption>
        </figure>
      </Reveal>
    </section>

    <section className="group-planning" id="group-enquire" aria-labelledby="group-planning-title">
      <div className="container group-planning-grid">
        <div className="group-planning-copy">
          <Reveal>
            <p className="group-kicker">One place to start</p>
            <h2 id="group-planning-title">Your group.<br/>Your plans.</h2>
            <p>Tell us when you’re coming, how many people are travelling and how many rooms you would like. The hotel will confirm what is available for your dates.</p>
          </Reveal>
          <dl className="group-planning-details">
            <div><dt>Rooms for your party</dt><dd>Choose a preferred room type, request a mix or ask the hotel to help. Mention separate-bed needs and children’s ages.</dd></div>
            <div><dt>Meals and arrival</dt><dd>Ask about vegetarian dining, meal inclusions and your arrival plans together, so the team has the details of your stay.</dd></div>
            <div><dt>Travelling for work</dt><dd>Add your company name and any billing questions. The hotel can confirm the arrangements before you book.</dd></div>
          </dl>
          <a className="group-call" href={hotel.phoneHref}><Phone size={18} aria-hidden="true"/> Speak with the hotel <ArrowUpRight size={16} aria-hidden="true"/></a>
          <div className="group-planning-links">
            <Link href="/rooms/compare">Compare rooms <ArrowUpRight size={16} aria-hidden="true"/></Link>
            <Link href="/dining">Explore dining <ArrowUpRight size={16} aria-hidden="true"/></Link>
            <Link href="/guides/arriving-in-godowlia">Plan your arrival <ArrowUpRight size={16} aria-hidden="true"/></Link>
          </div>
        </div>
        <GroupEnquiry/>
      </div>
    </section>
  </main>;
}
