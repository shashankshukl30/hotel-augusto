import { WhatsAppIcon } from "./whatsapp-icon";

/** A direct chat link; no message is sent until the guest chooses Send. */
export function WhatsAppChat({ href }: { href: string }) {
  return <a href={href} target="_blank" rel="noopener noreferrer"
    className="whatsapp-chat"
    style={{ color: "var(--paper)" }}
    aria-label="Chat with Hotel Augusto on WhatsApp (opens in a new tab)">
    <WhatsAppIcon size={28}/>
    <span className="whatsapp-chat-label" aria-hidden="true">Chat with us</span>
  </a>;
}
