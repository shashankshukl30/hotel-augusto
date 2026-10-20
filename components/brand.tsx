import Image from "next/image";

export function Brand({ large = false }: { large?: boolean }) {
  return <span className={`brand${large ? " brand-large" : ""}`}><span className="brand-artwork"><Image src="/brand/logo.jpeg" alt="Hotel Augusto" width={1254} height={1254} unoptimized/></span>{large && <span className="brand-place">Godowlia, Varanasi.</span>}</span>;
}
