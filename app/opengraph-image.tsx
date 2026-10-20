/* eslint-disable @next/next/no-img-element -- ImageResponse requires native image elements. */
import { ImageResponse } from "next/og";
import { readFile } from "node:fs/promises";
import { join } from "node:path";

export const alt = "Hotel Augusto, Varanasi. Your place in Kashi.";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";
export const dynamic = "force-static";

// Genuine property photo reused unchanged; licensed static Inter derivative.
// Provenance: research/apple-dominant-revision/og-assets-manifest.json.
const assets = Promise.all([
  readFile(join(process.cwd(), "public/images/augusto-og-room-v1.jpg")),
  readFile(join(process.cwd(), "public/fonts/augusto-og-inter-600-v1.ttf")),
  readFile(join(process.cwd(), "public/brand/logo.jpeg")),
]);

export default async function Image() {
  const [photo, displayFont, logo] = await assets;

  return new ImageResponse(
    <div style={{
      width: "100%", height: "100%", display: "flex",
      background: "#fcfcfd", color: "#1a1c1f",
      fontFamily: "Augusto OG Sans", fontWeight: 600,
    }}>
      <div style={{
        display: "flex", flexDirection: "column", width: 560,
        padding: "48px 52px",
      }}>
        <div style={{display:"flex",width:160,height:104,overflow:"hidden",position:"relative"}}>
          <img src={`data:image/jpeg;base64,${logo.toString("base64")}`} alt="Hotel Augusto" width={160} height={160} style={{position:"absolute",top:-28,left:0}}/>
        </div>
        <div style={{
          display: "flex", flexDirection: "column", marginTop: 62,
          fontSize: 82, lineHeight: 1.06, letterSpacing: -4,
        }}>
          <span>Your place</span>
          <span style={{ color: "#5d6166" }}>in Kashi.</span>
        </div>
        <div style={{
          display: "flex", alignItems: "center",
          marginTop: "auto", color: "#5d6166", fontSize: 20, letterSpacing: -.4,
        }}>
          <span>Godowlia, Varanasi</span>
        </div>
      </div>
      <div style={{
        display: "flex", width: 616, height: 582, marginTop: 24,
        overflow: "hidden", borderRadius: 28,
      }}>
        <img
          src={`data:image/jpeg;base64,${photo.toString("base64")}`}
          width={616}
          height={582}
          alt="Hotel Augusto bedroom with a blue upholstered headboard and double bed"
          style={{ objectFit: "cover", objectPosition: "48% 55%" }}
        />
      </div>
    </div>,
    {
      ...size,
      fonts: [
        { name: "Augusto OG Sans", data: displayFont, weight: 600, style: "normal" },
      ],
    },
  );
}
