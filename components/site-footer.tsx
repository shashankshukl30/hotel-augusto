import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { Brand } from "./brand";
import { WhatsAppIcon } from "./whatsapp-icon";
import { hotel } from "@/content/hotel";
import { FloatingWhatsApp } from "./floating-whatsapp";

export function SiteFooter() {
  const whatsapp = `https://wa.me/${hotel.whatsappNumber}?text=${encodeURIComponent("Namaste Hotel Augusto! I would like to enquire about a stay in Varanasi.")}`;
  return <>
    <footer className="site-footer">
      <div className="container">
        <div className="footer-invitation">
          <div><span className="eyebrow">YOUR VARANASI CHAPTER</span><h2>Some places stay<br/>with you. <em>Stay here.</em></h2></div>
          <div className="footer-invitation-action"><p>Tell us when you’re coming.<br/>We’ll help you find your room.</p><a className="button button-light" href={whatsapp} target="_blank" rel="noopener noreferrer" style={{ color: "var(--ink)" }}><WhatsAppIcon /> Enquire on WhatsApp <ArrowUpRight size={18}/></a><span className="footer-small">Speak directly with the hotel.</span></div>
        </div>
        <div className="footer-details">
          <Link href="/" className="brand-link" aria-label="Hotel Augusto home"><Brand large /></Link>
          <div><h3>FIND AUGUSTO</h3><p>{hotel.address.map((line) => <span key={line}>{line}<br/></span>)}</p><a href={hotel.mapsUrl} className="footer-link" target="_blank" rel="noopener noreferrer">Get directions <ArrowUpRight size={15}/></a></div>
          <div><h3>TAKE A LOOK AROUND</h3><Link href="/rooms">Our rooms</Link><Link href="/varanasi">Discover Varanasi</Link><Link href="/gallery">The gallery</Link><Link href="/contact">Contact & enquiries</Link></div>
          <div><h3>LET’S TALK</h3><a href={hotel.phoneHref}>{hotel.phone}</a><a href={whatsapp} target="_blank" rel="noopener noreferrer">WhatsApp the hotel <ArrowUpRight size={14}/></a><p className="footer-small">A warm welcome awaits<br/>in the heart of Godowlia.</p></div>
        </div>
        <div className="footer-bottom"><span>© {new Date().getFullYear()} Hotel Augusto.</span><Link href="/privacy">Privacy & photo credits</Link><span>Made with <span className="credit-heart">♥</span> by <a href="https://digiocular.com" target="_blank" rel="noopener noreferrer">Digiocular</a></span></div>
      </div>
    </footer>
    <FloatingWhatsApp href={whatsapp}/>
  </>;
}
