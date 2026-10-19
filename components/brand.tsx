export function Brand({ large = false }: { large?: boolean }) {
  return <span className={`brand${large ? " brand-large" : ""}`}><span className="brand-name">Augusto<span className="brand-dot">.</span></span></span>;
}
