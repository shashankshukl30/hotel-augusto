import type { MetadataRoute } from "next";
import { rooms } from "@/content/hotel";

export default function sitemap(): MetadataRoute.Sitemap {
  const site = process.env.NEXT_PUBLIC_SITE_URL;
  if (!site || process.env.SITE_INDEXABLE !== "true") return [];
  return ["/", "/rooms", ...rooms.map(room => `/rooms/${room.slug}`), "/varanasi", "/gallery", "/contact", "/privacy"].map(path => ({ url: `${site.replace(/\/$/, "")}${path}` }));
}
