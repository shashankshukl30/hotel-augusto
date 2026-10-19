import { ImageResponse } from "next/og";

export const alt = "Hotel Augusto — Varanasi, up close.";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function Image() {
  return new ImageResponse(<div style={{ width: "100%", height: "100%", background: "#fafafa", color: "#1d1d1f", display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", padding: "60px", fontFamily: "sans-serif" }}><div style={{display:"flex",fontSize:22,marginBottom:30}}>Hotel Augusto · Godowlia, Varanasi</div><div style={{display:"flex",fontSize:112,fontWeight:700,letterSpacing:-7,lineHeight:1.05}}>Augusto<span style={{color:"#0071e3"}}>.</span></div><div style={{display:"flex",fontSize:72,fontWeight:700,color:"#626267",letterSpacing:-4,lineHeight:1.2}}>Varanasi, up close.</div><div style={{display:"flex",fontSize:18,color:"#fafafa",background:"#0071e3",borderRadius:99,padding:"16px 30px",marginTop:42}}>Plan your stay</div></div>, size);
}
