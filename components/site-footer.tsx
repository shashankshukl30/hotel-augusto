import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { Brand } from "./brand";
import { WhatsAppIcon } from "./whatsapp-icon";
import { hotel } from "@/content/hotel";

export function SiteFooter() {
  const whatsapp = `https://wa.me/${hotel.whatsappNumber}?text=${encodeURIComponent("Namaste Hotel Augusto! I would like to enquire about a stay in Varanasi.")}`;
  return <>
    <footer className="site-footer">
      <div className="container">
        <div className="footer-invitation">
          <div><span className="eyebrow">Hotel Augusto, Varanasi</span><h2>Let’s plan<br/>your stay.</h2></div>
          <div className="footer-invitation-action"><p>Send your dates. We’ll help you choose a room.</p><a className="button" href={whatsapp} target="_blank" rel="noopener noreferrer" style={{ color: "var(--paper)" }}><WhatsAppIcon /> Enquire on WhatsApp</a><span className="footer-small">Speak directly with the hotel.</span></div>
        </div>
        <div className="footer-details">
          <Link href="/" className="brand-link" title="Hotel Augusto home"><Brand large /></Link>
          <div><h3>Find us</h3><p>{hotel.address.map((line) => <span key={line}>{line}<br/></span>)}</p><a href={hotel.mapsUrl} className="footer-link" target="_blank" rel="noopener noreferrer">Get directions <ArrowUpRight size={15}/></a></div>
          <div><h3>Explore</h3><Link href="/hotel">The hotel</Link><Link href="/rooms">Our rooms</Link><Link href="/rooms/compare">Compare rooms</Link><Link href="/dining">Dining</Link><Link href="/group-stays">Group & business stays</Link><Link href="/varanasi">Varanasi</Link><Link href="/gallery">Gallery</Link><Link href="/guides">Stay guide</Link><Link href="/contact">Contact & enquiries</Link></div>
          <div><h3>Contact</h3><a href={hotel.phoneHref}>{hotel.phone}</a><a className="footer-email" style={{overflowWrap:"anywhere"}} href={`mailto:${hotel.email}`}>{hotel.email}</a><a href={whatsapp} target="_blank" rel="noopener noreferrer">WhatsApp the hotel <ArrowUpRight size={14}/></a><h3 className="footer-booking-label">Also find us on</h3><a href="https://www.makemytrip.com/hotels/hotel_augusto-details-varanasi.html" target="_blank" rel="noopener noreferrer">MakeMyTrip <ArrowUpRight size={14}/></a><a href={hotel.mapsUrl} target="_blank" rel="noopener noreferrer">Google Maps <ArrowUpRight size={14}/></a></div>
        </div>
        <div className="footer-bottom"><span>© {new Date().getFullYear()} Hotel Augusto.</span><Link href="/privacy">Privacy & photo credits</Link><span>Made with <span className="credit-heart">♥</span> by <a href="https://digiocular.com" target="_blank" rel="noopener noreferrer">Digiocular</a></span></div>
      </div>
    </footer>
  </>;
}
