import type { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  const published = process.env.SITE_INDEXABLE === "true";
  const site = process.env.NEXT_PUBLIC_SITE_URL;
  return { rules: { userAgent: "*", ...(published ? { allow: "/" } : { disallow: "/" }) }, ...(published && site ? { sitemap: `${site.replace(/\/$/, "")}/sitemap.xml` } : {}) };
}
