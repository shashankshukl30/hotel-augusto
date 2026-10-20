import type { Metadata, Viewport } from "next";
import localFont from "next/font/local";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { ScrollReset } from "@/components/scroll-reset";
import { hotel } from "@/content/hotel";
import "./globals.css";

const inter = localFont({ src: "../node_modules/@fontsource-variable/inter/files/inter-latin-wght-normal.woff2", variable: "--font-inter", weight: "100 900", display: "swap" });
const manrope = localFont({ src: "../node_modules/@fontsource-variable/manrope/files/manrope-latin-wght-normal.woff2", variable: "--font-manrope", weight: "200 800", display: "swap" });

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || (process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : "http://localhost:3080")),
  title: "Hotel Augusto Varanasi | A Stay in the Heart of Kashi",
  description: "Make yourself at home at Hotel Augusto in Godowlia, Varanasi. Explore our rooms, vegetarian dining and the old city. Enquire directly on WhatsApp.",
  applicationName: "Hotel Augusto",
  robots: { index: process.env.SITE_INDEXABLE === "true", follow: process.env.SITE_INDEXABLE === "true" },
  openGraph: { type: "website", locale: "en_IN", siteName: "Hotel Augusto", title: "Hotel Augusto · Varanasi, up close.", description: "Your place in Godowlia. Explore the hotel, rooms, dining and Varanasi.", images: [{ url: "/opengraph-image", width: 1200, height: 630 }] },
  twitter: { card: "summary_large_image" },
};
export const viewport: Viewport = { width: "device-width", initialScale: 1, themeColor: "#fafaf9" };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  const schema = { "@context": "https://schema.org", "@type": "Hotel", name: hotel.name, telephone: hotel.phone, address: { "@type": "PostalAddress", streetAddress: hotel.address[0] + ", " + hotel.address[1], addressLocality: "Varanasi", addressRegion: "Uttar Pradesh", postalCode: "221001", addressCountry: "IN" }, hasMap: hotel.mapsUrl };
  return <html lang="en" className={inter.variable + " " + manrope.variable}><head><script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema).replace(/</g, "\\u003c") }}/></head><body><a className="skip-link" href="#main">Skip to content</a><ScrollReset/><SiteHeader/>{children}<SiteFooter/></body></html>;
}
