"use client";

import Image from "next/image";
import Link from "next/link";
import { useState } from "react";
import { ArrowUpRight, Check } from "lucide-react";
import { rooms } from "@/content/hotel";
import "./room-comparison.css";

export function RoomComparison() {
  const [first, setFirst] = useState(rooms[0].slug);
  const [second, setSecond] = useState(rooms[1].slug);
  const mobile = [rooms.find(room => room.slug === first)!, rooms.find(room => room.slug === second)!];
  const essentials = rooms[0].features;

  return <div className="room-comparison">
    <div className="comparison-desktop"><table><caption className="comparison-sr-only">Three room arrangements at Hotel Augusto</caption>
      <thead><tr><td/>{rooms.map(room => <th key={room.slug} scope="col"><Link href={`/rooms/${room.slug}`}><span className="comparison-image"><Image src={room.image} alt={room.alt} fill sizes="28vw" quality={85}/></span><span className="comparison-name">{room.name}</span></Link></th>)}</tr></thead>
      <tbody><tr><th scope="row">Bed arrangement</th>{rooms.map(room => <td key={room.slug} className="comparison-bed">{room.bedLabel}</td>)}</tr>
        {essentials.map(feature => <tr key={feature}><th scope="row">{feature}</th>{rooms.map(room => <td key={room.slug}><Check size={18} aria-hidden="true"/><span className="comparison-sr-only">Included</span></td>)}</tr>)}
        <tr className="comparison-actions"><th scope="row"><span className="comparison-sr-only">Explore or enquire</span></th>{rooms.map(room => <td key={room.slug}><Link href={`/rooms/${room.slug}`} className="comparison-detail-link">Explore room <ArrowUpRight size={16}/></Link><Link href={`/contact?room=${room.slug}#enquire`} className="room-action" style={{ color: "var(--paper)" }}>Choose this room <ArrowUpRight size={16}/></Link></td>)}</tr>
      </tbody>
    </table></div>
    <div className="comparison-mobile"><div className="comparison-selectors">
      <div><label htmlFor="compare-first">First room</label><select id="compare-first" value={first} onChange={event => { const value = event.target.value; setFirst(value); if (value === second) setSecond(first); }}>{rooms.map(room => <option value={room.slug} key={room.slug}>{room.name}</option>)}</select></div>
      <div><label htmlFor="compare-second">Compare with</label><select id="compare-second" value={second} onChange={event => { const value = event.target.value; setSecond(value); if (value === first) setFirst(second); }}>{rooms.map(room => <option value={room.slug} key={room.slug}>{room.name}</option>)}</select></div>
    </div><div className="comparison-mobile-grid" aria-live="polite">{mobile.map((room, index) => <article className="comparison-mobile-room" key={`${index}-${room.slug}`}>
      <Link href={`/rooms/${room.slug}`} className="comparison-image"><Image src={room.image} alt={room.alt} fill sizes="45vw" quality={85}/></Link><h2>{room.name}</h2><dl><div><dt>Bed arrangement</dt><dd>{room.bedLabel}</dd></div></dl>
      <Link href={`/rooms/${room.slug}`} className="comparison-detail-link">Explore room <ArrowUpRight size={16}/></Link><Link href={`/contact?room=${room.slug}#enquire`} className="room-action" style={{ color: "var(--paper)" }}>Choose room <ArrowUpRight size={16}/></Link>
    </article>)}</div><div className="comparison-shared"><h3>In both rooms</h3><ul>{essentials.map(feature => <li key={feature}><Check size={16}/>{feature}</li>)}</ul></div></div>
    <p className="comparison-note">Room layouts and furnishings may vary. Guest capacity, rates, meal inclusions and booking terms are confirmed by the hotel when you enquire.</p>
  </div>;
}
