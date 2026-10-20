import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft, ArrowUpRight } from "lucide-react";
import { RoomComparison } from "@/components/room-comparison";
import "../rooms.css";

export const metadata: Metadata = {
  title: "Compare Rooms at Hotel Augusto Varanasi | Find Your Stay",
  description: "Compare Deluxe, Twin and Family room arrangements at Hotel Augusto. See genuine room photographs and shared comforts, then enquire directly for your dates.",
};

export default function CompareRoomsPage() {
  return <main id="main" className="rooms-page room-compare-page">
    <div className="rooms-container room-detail-breadcrumb"><Link href="/rooms" className="room-back-link"><ArrowLeft size={16}/> All rooms</Link><span>Hotel Augusto · Varanasi</span></div>
    <header className="rooms-container room-compare-heading"><p className="room-context">Find your arrangement</p><h1>Which room<br/><em>feels like yours?</em></h1><p>Start with the beds. Every room has the same everyday comforts; the hotel will help confirm the right arrangement for your guests.</p></header>
    <section className="rooms-container" aria-label="Compare room arrangements"><RoomComparison/></section>
    <section className="rooms-container room-compare-help"><div><h2>Still deciding?</h2><p>Tell us your dates and who’s travelling. We’ll help you choose.</p></div><Link href="/contact#enquire" className="room-action" style={{ color: "var(--paper)" }}>Ask the hotel <ArrowUpRight size={18}/></Link></section>
  </main>;
}
