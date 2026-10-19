export function Brand({ large = false }: { large?: boolean }) {
  return <span className={`brand${large ? " brand-large" : ""}`}>
    <svg className="brand-mark" width="40" height="44" viewBox="0 0 40 44" fill="none" aria-hidden="true">
      <path d="M8 35V18a12 12 0 0 1 24 0v17M13 35V19a7 7 0 0 1 14 0v16M4 35h32M1 40h38M20 1v4M2 10l4 3M38 10l-4 3" stroke="currentColor" strokeWidth="1.2"/>
    </svg>
    <span><span className="brand-name">augusto</span><span className="brand-place">HOTEL · VARANASI</span></span>
  </span>;
}
