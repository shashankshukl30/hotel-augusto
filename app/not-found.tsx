import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
export default function NotFound() {
  return <main id="main" className="container not-found"><span className="eyebrow">A LITTLE OFF THE BEATEN PATH · 404</span><h1 className="display">Let’s find<br/>your way back.</h1><p>This page isn’t here, but your next Varanasi stay could be.</p><Link href="/" className="button" style={{ color: "var(--paper)" }}>Back to Augusto <ArrowUpRight size={18}/></Link></main>;
}
