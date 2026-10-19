import { ImageResponse } from "next/og";
export const alt = "Hotel Augusto — At home in the heart of Kashi";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";
export default function Image() {
  return new ImageResponse(<div style={{ width: "100%", height: "100%", background: "#f5f1e9", color: "#873f2d", display: "flex", flexDirection: "column", justifyContent: "space-between", padding: "62px 80px", border: "18px solid #873f2d" }}><div style={{ display: "flex", justifyContent: "space-between", fontSize: 20, letterSpacing: 5 }}><span>HOTEL AUGUSTO</span><span>VARANASI, INDIA</span></div><div style={{ display: "flex", flexDirection: "column", fontFamily: "serif", fontSize: 108, lineHeight: 1.05 }}><span>At home in the</span><span>heart of Kashi.</span></div><div style={{ display: "flex", fontSize: 22 }}>GODOWLIA · ROOMS · VEGETARIAN DINING · WARM WELCOMES</div></div>, size);
}
