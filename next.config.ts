import type { NextConfig } from "next";

const staticExport = process.env.SITE_STATIC_EXPORT === "true";

const nextConfig: NextConfig = {
  ...(staticExport ? { output: "export" as const } : {}),
  poweredByHeader: false,
  images: {
    formats: ["image/avif", "image/webp"],
    qualities: [75, 85],
    ...(staticExport ? { unoptimized: true } : {}),
  },
  turbopack: { root: process.cwd() },
  // Static hosting supplies response headers; Next's headers() needs a server.
  headers: staticExport ? undefined : async () => {
    return [{
      source: "/(.*)",
      headers: [
        { key: "X-Content-Type-Options", value: "nosniff" },
        { key: "X-Frame-Options", value: "DENY" },
        { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
        { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
        { key: "Content-Security-Policy", value: "base-uri 'self'; object-src 'none'; frame-ancestors 'none'; form-action 'self' https://wa.me; upgrade-insecure-requests" },
        { key: "Strict-Transport-Security", value: "max-age=31536000; includeSubDomains" }
      ]
    }];
  },
};
export default nextConfig;
