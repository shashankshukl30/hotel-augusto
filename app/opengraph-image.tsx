/* eslint-disable @next/next/no-img-element -- ImageResponse requires native image elements. */
import { ImageResponse } from "next/og";
import { readFile } from "node:fs/promises";
import { join } from "node:path";

export const alt = "Hotel Augusto, Varanasi. Stay closer.";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default async function Image() {
  const photo = await readFile(join(process.cwd(), "research/awwwards-revision/martijn-ghats.jpg"));
  return new ImageResponse(<div style={{ width:"100%",height:"100%",display:"flex",background:"#173c39",color:"#f6f5f0",fontFamily:"sans-serif" }}>
    <img src={`data:image/jpeg;base64,${photo.toString("base64")}`} width={1200} height={800} alt="" style={{position:"absolute",left:0,top:-90,objectFit:"cover"}}/>
    <div style={{position:"absolute",left:0,top:0,width:1200,height:630,background:"linear-gradient(90deg,rgba(15,38,36,.88),rgba(15,38,36,.12))",display:"flex"}}/>
    <div style={{position:"relative",display:"flex",flexDirection:"column",padding:"52px 70px",width:"100%"}}>
      <div style={{display:"flex",fontSize:34,fontWeight:700,letterSpacing:-2}}>Augusto.</div>
      <div style={{display:"flex",fontSize:16,letterSpacing:3,marginTop:45}}>HOTEL AUGUSTO · GODOWLIA, VARANASI</div>
      <div style={{display:"flex",flexDirection:"column",fontSize:100,fontWeight:500,lineHeight:1.03,letterSpacing:-6,marginTop:26}}><span>Varanasi.</span><span>Stay closer.</span></div>
      <div style={{display:"flex",fontSize:18,marginTop:42}}>Your place in the city.</div>
    </div>
  </div>,size);
}
