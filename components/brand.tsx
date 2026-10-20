export function Brand({ large = false }: { large?: boolean }) {
  return <span className={`brand${large ? " brand-large" : ""}`}><span className="brand-name">AUGUSTO</span><span className="brand-place">HOTEL · VARANASI</span></span>;
}
