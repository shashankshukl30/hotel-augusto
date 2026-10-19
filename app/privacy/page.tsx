import type { Metadata } from "next";
import Link from "next/link";
import { Reveal } from "@/components/reveal";
import { hotel } from "@/content/hotel";
import assetManifest from "@/research/assets/asset-manifest.json";
import heroAsset from "@/research/awwwards-revision/hero-asset.json";
import "../contact/contact.css";

export const metadata: Metadata = {
  title: "Privacy & Photo Credits | Hotel Augusto in Varanasi",
  description:
    "How the Hotel Augusto website handles stay enquiries, links to WhatsApp and basic technical information, with credits for destination photography.",
};

interface CreditAsset {
  id: string;
  kind: string;
  source_page: string;
  author?: string;
  rights: string;
  license_url?: string;
  public_path?: string;
}

const photoNames: Record<string, string> = {
  "varanasi-ghats": "The Varanasi riverfront",
  "ganges-dawn": "Morning on the Ganges",
  "ganges-boats": "Boats on the Ganges",
  "kashi-vishwanath": "Shri Kashi Vishwanath Temple",
  "kashi-vishwanath-2025": "Shri Kashi Vishwanath Temple",
  "varanasi-hero": "The sunlit ghats of Varanasi",
};
const credits = [...(assetManifest.assets as CreditAsset[]).filter(
  (asset) => asset.kind === "destination" && Boolean(asset.public_path),
), { ...heroAsset, kind: "destination", rights: heroAsset.license }];

export default function PrivacyPage() {
  return (
    <main id="main" className="privacy-page">
      <section className="container privacy-intro">
        <Reveal>
          <h1>Your privacy.<br />In plain language.</h1>
          <p className="privacy-intro-copy">
            How this website handles your information, with credits for
            the photographs that bring Varanasi to these pages.
          </p>
          <p className="privacy-updated">Last updated: 19 October 2026</p>
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
                The enquiry form prepares a WhatsApp message on your device using
                the trip details you enter. This website does not store those
                details in its own database. You review and send the message
                through WhatsApp.
              </p>
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
            </section>

            <section className="privacy-section" id="technical-information">
              <h2>Browsing the website</h2>
              <p>
                No advertising pixels or visitor analytics are installed on this
                website. Fonts and photographs are served as website assets;
                there is no embedded map or social-media feed.
              </p>
              <p>
                The hosting service may process basic technical information,
                such as your IP address, browser, requested pages and access
                times, to deliver the website and maintain its security.
              </p>
            </section>

            <section className="privacy-section" id="external-services">
              <h2>When you follow a link</h2>
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
                If a booking engine, analytics service or another data-collection
                feature is introduced here, this notice will need to reflect how
                that feature works.
              </p>
            </section>

            <section className="privacy-section" id="privacy-questions">
              <h2>Questions about your information</h2>
              <p>
                Call Hotel Augusto on <a href={hotel.phoneHref}>{hotel.phone}</a>{" "}
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
