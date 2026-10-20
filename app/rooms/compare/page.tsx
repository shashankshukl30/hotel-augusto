import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { RoomComparison } from "@/components/room-comparison";
import "../rooms.css";

export const metadata: Metadata = {
  title: "Compare Rooms at Hotel Augusto Varanasi | Find Your Stay",
  description: "Compare Deluxe, Twin and Family room arrangements at Hotel Augusto. See genuine room photographs and shared comforts, then enquire directly for your dates.",
};

export default function CompareRoomsPage() {
  return <main id="main" className="rooms-page room-compare-page">
    <div className="rooms-container room-detail-breadcrumb"><Link href="/rooms" className="room-back-link"><ArrowLeft size={16}/> All rooms</Link></div>
    <header className="rooms-container room-compare-heading"><p className="room-context">Rooms at Augusto</p><h1>Which room is<br/>right for you?</h1><p>Compare the bed arrangements and shared essentials. The hotel will confirm the right room for your guests.</p></header>
    <section className="rooms-container" aria-label="Compare room arrangements"><RoomComparison/></section>
    <section className="rooms-container room-compare-help"><div><h2>A little help choosing?</h2><p>Share your dates and who is travelling.</p></div><Link href="/contact#enquire" className="room-action" style={{ color: "var(--paper)" }}>Ask the hotel <ArrowRight size={18}/></Link></section>
  </main>;
}
