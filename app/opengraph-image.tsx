/* eslint-disable @next/next/no-img-element -- ImageResponse requires native image elements. */
import { ImageResponse } from "next/og";
import { readFile } from "node:fs/promises";
import { join } from "node:path";

export const alt = "Hotel Augusto. Varanasi, up close.";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default async function Image() {
  const photo = await readFile(join(process.cwd(), "research/awwwards-revision/martijn-ghats.jpg"));
  return new ImageResponse(<div style={{ width:"100%",height:"100%",display:"flex",background:"#fafaf9",color:"#1c1d22",fontFamily:"sans-serif" }}>
    <div style={{position:"absolute",right:24,top:24,width:500,height:582,borderRadius:32,overflow:"hidden",display:"flex"}}>
      <img src={`data:image/jpeg;base64,${photo.toString("base64")}`} width={500} height={582} alt="" style={{objectFit:"cover",objectPosition:"65% center"}}/>
    </div>
    <div style={{display:"flex",flexDirection:"column",padding:"55px 58px",width:675}}>
      <div style={{display:"flex",fontSize:24,fontWeight:500}}>Hotel Augusto · Varanasi</div>
      <div style={{display:"flex",flexDirection:"column",fontSize:88,fontWeight:700,lineHeight:1.03,letterSpacing:-6,marginTop:76}}><span>Augusto.</span><span style={{color:"#62636a"}}>Varanasi,</span><span style={{color:"#62636a"}}>up close.</span></div>
      <div style={{display:"flex",fontSize:20,marginTop:45,color:"#145ba6"}}>Make yourself at home.</div>
    </div>
  </div>,size);
}
