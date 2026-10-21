import type { Metadata } from "next";
import Link from "next/link";
import { Reveal } from "@/components/reveal";
import { hotel } from "@/content/hotel";
import credits from "@/content/photo-credits.json";
import "../contact/contact.css";

export const metadata: Metadata = {
  alternates: { canonical: "/privacy" },
  title: "Privacy & Photo Credits | Hotel Augusto in Varanasi",
  description:
    "How the Hotel Augusto website handles stay enquiries, links to WhatsApp and basic technical information, with credits for destination photography.",
};

const photoNames: Record<string, string> = {
  "varanasi-ghats": "The Varanasi riverfront",
  "ganges-dawn": "Morning on the Ganges",
  "ganges-boats": "Boats on the Ganges",
  "kashi-vishwanath": "Shri Kashi Vishwanath Temple",
  "kashi-vishwanath-2025": "Shri Kashi Vishwanath Temple",
  "varanasi-hero": "The sunlit ghats of Varanasi",
};
export default function PrivacyPage() {
  return (
    <main id="main" className="privacy-page">
      <section className="container privacy-intro">
        <Reveal>
          <h1>Privacy.<br />In plain language.</h1>
          <p className="privacy-intro-copy">
            How this website handles your information, with credits for
            the photographs that bring Varanasi to these pages.
          </p>
          <p className="privacy-updated">Last updated: 21 October 2026</p>
        </Reveal>
      </section>

      <div className="container privacy-body">
        <div className="privacy-body-inner">
          <nav className="privacy-navigation" aria-label="On this page">
            <a href="#stay-enquiries">Stay enquiries</a>
            <a href="#technical-information">Browsing</a>
            <a href="#external-services">External services</a>
            <a href="#privacy-questions">Questions</a>
            <a href="#photo-credits">Photo credits</a>
          </nav>

          <div className="privacy-content">
            <section className="privacy-section" id="stay-enquiries">
              <h2>Your stay enquiry</h2>
              <p>
                Stay, dining and group enquiry forms ask for your travel plans
                and a reply email address. Your name, phone number, company and
                additional requests are optional. When you choose Send enquiry,
                the details are sent through FormSubmit to the hotel at{" "}
                <a href={`mailto:${hotel.email}`}>{hotel.email}</a> so its team can respond.
              </p>
              <p>The website does not maintain its own enquiry database. FormSubmit processes the submitted details and basic connection information to forward the email; the hotel and its email provider handle the resulting message. A successful submission means the service accepted the enquiry, not that it has reached the hotel’s inbox or that a room is reserved.</p>
              <p>
                When you open WhatsApp, the prepared message is passed to that
                service. If you send it, the hotel receives your message and the
                contact information your WhatsApp account shares. Contact the
                hotel directly about information you have sent in a conversation.
              </p>
              <p>
                This website does not collect payment details or confirm
                reservations. Availability, rates and booking terms are agreed
                directly with the hotel.
              </p>
              <p>The date and guest selector carries your travel dates, party size, requested room count and room preference to the enquiry page in its URL. These preferences may remain in your browser history. Your name and personal notes are not included in that link.</p>
              <p>If you choose the WhatsApp alternative, the form prepares a message on your device. Your reply email and optional phone are not added to that message. You review it in WhatsApp and tap Send there. Nothing is sent to FormSubmit when you use this alternative.</p>
              <p>Please avoid including payment-card details or sensitive personal information in an enquiry. Contact the hotel to ask about access to or deletion of messages you have sent.</p>
            </section>

            <section className="privacy-section" id="technical-information">
              <h2>Browsing the website</h2>
              <p>
                No advertising pixels or visitor analytics are installed on this
                website. Fonts and photographs are served as website assets.
                There is no embedded social-media feed.
              </p>
              <p>
                The hosting service may process basic technical information,
                such as your IP address, browser, requested pages and access
                times, to deliver the website and maintain its security.
              </p>
            </section>

            <section className="privacy-section" id="external-services">
              <h2>When you follow a link</h2>
              <p>Sending an email enquiry connects your browser to <a href="https://formsubmit.co/" target="_blank" rel="noopener noreferrer">FormSubmit</a>. It is a separate form-to-email service. Email links open your chosen email app instead; messages sent that way are handled by your email provider and the hotel’s provider.</p>
              <p>The arrival guide offers an optional Google map. It loads only after you select “Load Google map”. At that point, your browser connects to Google, which may receive technical information such as your IP address and apply its own privacy policy.</p>
              <p>
                WhatsApp, Google Maps and other websites linked from these pages
                are operated separately. When you open them, their terms and
                privacy policies apply. Read the{" "}
                <a href="https://www.whatsapp.com/legal/privacy-policy" target="_blank" rel="noopener noreferrer">
                  WhatsApp Privacy Policy
                </a>{" "}
                for information about that service.
              </p>
              <p>
                If a booking engine or analytics service is introduced here,
                this notice will need to reflect how that feature works.
              </p>
            </section>

            <section className="privacy-section" id="privacy-questions">
              <h2>Questions about your information</h2>
              <p>
                Email <a href={`mailto:${hotel.email}`}>{hotel.email}</a>,
                call Hotel Augusto on <a href={hotel.phoneHref}>{hotel.phone}</a>{" "}
                or use the options on our <Link href="/contact">contact page</Link>.
                The hotel can help with questions about a stay enquiry or a
                conversation you have had with its team.
              </p>
            </section>

            <section className="privacy-section" id="photo-credits">
              <h2>Photo credits</h2>
              <p>
                The rooms, dining spaces and exterior photographs show Hotel
                Augusto. The city photographs show Varanasi and are separate
                from the property photography.
              </p>
              <div className="privacy-credits">
                {credits.map((credit) => (
                  <div className="privacy-credit" key={credit.id}>
                    <div>
                      <strong>{photoNames[credit.id] ?? "Varanasi destination photograph"}</strong>
                      <span>{credit.author ?? "Photographer credited at source"}</span>
                    </div>
                    <div>
                      <a href={credit.source_page} target="_blank" rel="noopener noreferrer">Original photograph</a>
                      <span>
                        {credit.license_url ? (
                          <a href={credit.license_url} target="_blank" rel="noopener noreferrer">{credit.rights}</a>
                        ) : credit.rights}
                      </span>
                      <small>Resized and cropped for this website.</small>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          </div>
        </div>
      </div>
    </main>
  );
}
