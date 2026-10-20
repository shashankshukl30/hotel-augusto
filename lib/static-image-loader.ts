"use client";

import type { ImageLoaderProps } from "next/image";
import manifest from "../content/responsive-images.json" with { type: "json" };

const photographs = manifest as Record<string, Array<{ width: number; src: string }>>;

// Enabled only for static exports. Normal deployments retain Next's optimizer.
// The generated preview files use one WebP quality85 profile and never upscale.
export default function staticImageLoader({ src, width }: ImageLoaderProps): string {
  const variants = photographs[src.split(/[?#]/, 1)[0]];
  if (!variants) return src; // Brand artwork, SVGs and metadata assets stay intact.
  if (!Number.isFinite(width) || width <= 0) {
    throw new Error(`Invalid responsive image width for ${src}`);
  }
  return (variants.find(candidate => candidate.width >= width) ?? variants[variants.length - 1]).src;
}
