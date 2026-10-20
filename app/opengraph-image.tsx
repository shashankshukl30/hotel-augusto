/* eslint-disable @next/next/no-img-element -- ImageResponse requires native image elements. */
import { ImageResponse } from "next/og";
import { readFile } from "node:fs/promises";
import { join } from "node:path";

export const alt = "Hotel Augusto, Varanasi. Your place in Kashi.";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";
export const dynamic = "force-static";

// Tracked derivatives of the genuine property photograph and OFL fonts.
// Provenance: research/hospitality-revision/og-assets-manifest.json.
const assets = Promise.all([
  readFile(join(process.cwd(), "public/images/augusto-og-room-v1.jpg")),
  readFile(join(process.cwd(), "public/fonts/augusto-og-bodoni-400-v1.ttf")),
  readFile(join(process.cwd(), "public/fonts/augusto-og-manrope-500-v1.ttf")),
]);

export default async function Image() {
  const [photo, displayFont, bodyFont] = await assets;

  return new ImageResponse(
    <div style={{
      width: "100%", height: "100%", display: "flex",
      background: "#f8f3e9", color: "#18232e", fontFamily: "Augusto OG Body",
    }}>
      <div style={{
        display: "flex", flexDirection: "column", width: 558,
        padding: "46px 54px 44px",
      }}>
        <span style={{
          fontFamily: "Augusto OG Display", fontSize: 43,
          letterSpacing: 4, lineHeight: 1,
        }}>AUGUSTO</span>
        <span style={{
          marginTop: 15, fontSize: 14, letterSpacing: 2.5, color: "#745332",
        }}>HOTEL · VARANASI</span>
        <div style={{
          display: "flex", flexDirection: "column", marginTop: 102,
          fontFamily: "Augusto OG Display", fontSize: 86, fontWeight: 400,
          lineHeight: 1.04, letterSpacing: -1.5,
        }}>
          <span>Your place</span>
          <span>in Kashi.</span>
        </div>
        <div style={{
          display: "flex", alignItems: "center", gap: 17,
          marginTop: "auto", color: "#745332", fontSize: 17,
        }}>
          <div style={{ width: 42, height: 1, background: "#745332" }} />
          <span>Godowlia · Varanasi</span>
        </div>
      </div>
      <div style={{
        display: "flex", width: 622, height: 590, marginTop: 20,
        overflow: "hidden", borderRadius: 4,
      }}>
        <img
          src={`data:image/jpeg;base64,${photo.toString("base64")}`}
          width={622}
          height={590}
          alt="Hotel Augusto bedroom with a blue upholstered headboard and double bed"
          style={{ objectFit: "cover", objectPosition: "48% 55%" }}
        />
      </div>
    </div>,
    {
      ...size,
      fonts: [
        { name: "Augusto OG Display", data: displayFont, weight: 400, style: "normal" },
        { name: "Augusto OG Body", data: bodyFont, weight: 500, style: "normal" },
      ],
    },
  );
}
