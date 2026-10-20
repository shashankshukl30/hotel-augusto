import type { Metadata, Viewport } from "next";
import localFont from "next/font/local";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { ScrollReset } from "@/components/scroll-reset";
import { hotel } from "@/content/hotel";
import "./globals.css";

const manrope = localFont({ src: "../node_modules/@fontsource-variable/manrope/files/manrope-latin-wght-normal.woff2", variable: "--font-manrope", weight: "200 800", display: "swap" });
const bodoni = localFont({ src: [
  { path: "../node_modules/@fontsource-variable/bodoni-moda/files/bodoni-moda-latin-wght-normal.woff2", weight: "400 900", style: "normal" },
  { path: "../node_modules/@fontsource-variable/bodoni-moda/files/bodoni-moda-latin-wght-italic.woff2", weight: "400 900", style: "italic" },
], variable: "--font-bodoni", display: "swap" });

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || (process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : "http://localhost:3080")),
  title: "Hotel Augusto Varanasi | A Stay in the Heart of Kashi",
  description: "Make yourself at home at Hotel Augusto in Godowlia, Varanasi. Explore our rooms, vegetarian dining and the old city. Enquire directly on WhatsApp.",
  applicationName: "Hotel Augusto",
  robots: { index: process.env.SITE_INDEXABLE === "true", follow: process.env.SITE_INDEXABLE === "true" },
  openGraph: { type: "website", locale: "en_IN", siteName: "Hotel Augusto", title: "Hotel Augusto · Your place in Kashi.", description: "Rooms, vegetarian dining and a warm welcome in Godowlia, Varanasi.", images: [{ url: "/opengraph-image", width: 1200, height: 630 }] },
  twitter: { card: "summary_large_image" },
};
export const viewport: Viewport = { width: "device-width", initialScale: 1, themeColor: "#f7f3eb" };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  const schema = { "@context": "https://schema.org", "@type": "Hotel", name: hotel.name, telephone: hotel.phone, address: { "@type": "PostalAddress", streetAddress: hotel.address[0] + ", " + hotel.address[1], addressLocality: "Varanasi", addressRegion: "Uttar Pradesh", postalCode: "221001", addressCountry: "IN" }, hasMap: hotel.mapsUrl };
  return <html lang="en" className={manrope.variable + " " + bodoni.variable}><head><script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema).replace(/</g, "\\u003c") }}/></head><body><a className="skip-link" href="#main">Skip to content</a><ScrollReset/><SiteHeader/>{children}<SiteFooter/></body></html>;
}
