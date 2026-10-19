import type { Metadata, Viewport } from "next";
import localFont from "next/font/local";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { ScrollReset } from "@/components/scroll-reset";
import { hotel } from "@/content/hotel";
import "./globals.css";

const display = localFont({ src: [
  { path: "../node_modules/@fontsource/libre-bodoni/files/libre-bodoni-latin-400-normal.woff2", weight: "400", style: "normal" },
  { path: "../node_modules/@fontsource/libre-bodoni/files/libre-bodoni-latin-400-italic.woff2", weight: "400", style: "italic" },
], variable: "--font-display", display: "swap" });
const body = localFont({ src: [
  { path: "../node_modules/@fontsource/public-sans/files/public-sans-latin-400-normal.woff2", weight: "400", style: "normal" },
  { path: "../node_modules/@fontsource/public-sans/files/public-sans-latin-500-normal.woff2", weight: "500", style: "normal" },
  { path: "../node_modules/@fontsource/public-sans/files/public-sans-latin-600-normal.woff2", weight: "600", style: "normal" },
], variable: "--font-body", display: "swap" });

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || (process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : "http://localhost:3080")),
  title: "Hotel Augusto Varanasi | A Stay in the Heart of Kashi",
  description: "Make yourself at home at Hotel Augusto in Godowlia, Varanasi. Explore our rooms, vegetarian dining and the old city. Enquire directly on WhatsApp.",
  applicationName: "Hotel Augusto",
  robots: { index: process.env.SITE_INDEXABLE === "true", follow: process.env.SITE_INDEXABLE === "true" },
  openGraph: { type: "website", locale: "en_IN", siteName: "Hotel Augusto", title: "Hotel Augusto · At home in Varanasi", description: "The heart of Kashi. A place of your own.", images: [{ url: "/opengraph-image", width: 1200, height: 630 }] },
  twitter: { card: "summary_large_image" },
};
export const viewport: Viewport = { width: "device-width", initialScale: 1, themeColor: "#f5f1e9" };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  const schema = { "@context": "https://schema.org", "@type": "Hotel", name: hotel.name, telephone: hotel.phone, address: { "@type": "PostalAddress", streetAddress: hotel.address[0] + ", " + hotel.address[1], addressLocality: "Varanasi", addressRegion: "Uttar Pradesh", postalCode: "221001", addressCountry: "IN" }, hasMap: hotel.mapsUrl };
  return <html lang="en" className={`${display.variable} ${body.variable}`}><head><script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema).replace(/</g, "\\u003c") }}/></head><body><a className="skip-link" href="#main">Skip to content</a><ScrollReset/><SiteHeader/>{children}<SiteFooter/></body></html>;
}
