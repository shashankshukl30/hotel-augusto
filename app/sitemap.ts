import type { MetadataRoute } from "next";
import { rooms } from "@/content/hotel";
import { guides } from "@/content/guides";

export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
  const site = process.env.NEXT_PUBLIC_SITE_URL;
  if (!site || process.env.SITE_INDEXABLE !== "true") return [];
  return ["/", "/hotel", "/rooms", "/rooms/compare", ...rooms.map(room => `/rooms/${room.slug}`), "/dining", "/varanasi", "/gallery", "/guides", ...guides.map(guide => `/guides/${guide.slug}`), "/contact", "/privacy"].map(path => ({ url: `${site.replace(/\/$/, "")}${path}` }));
}
