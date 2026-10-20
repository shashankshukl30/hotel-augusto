import { test } from "node:test";
import assert from "node:assert/strict";
import { readFile, readdir, stat } from "node:fs/promises";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
import { resolve } from "node:path";
import { createRequire } from "node:module";
import staticImageLoader from "../lib/static-image-loader.ts";

const require = createRequire(import.meta.url);
const { getImgProps } = require("next/dist/shared/lib/get-img-props.js");
const { imageConfigDefault } = require("next/dist/shared/lib/image-config.js");
const nextImageLoader = require("next/dist/shared/lib/image-loader.js").default;
const root = fileURLToPath(new URL("../", import.meta.url));
const report = JSON.parse(await readFile(resolve(root, "research/apple-dominant-revision/responsive-images.json"), "utf8"));
const configPath = new URL("../next.config.ts", import.meta.url);
const digest = data => createHash("sha256").update(data).digest("hex");

test("phone and thumbnail widths select smaller local files; high density uses a capped source", () => {
  const src = "/images/deluxe-room.webp";
  assert.equal(staticImageLoader({ src, width: 72 }), "/images/responsive/deluxe-room-96w.webp");
  assert.equal(staticImageLoader({ src, width: 180 }), "/images/responsive/deluxe-room-192w.webp");
  assert.equal(staticImageLoader({ src, width: 390 }), "/images/responsive/deluxe-room-480w.webp");
  assert.equal(staticImageLoader({ src, width: 780, quality: 85 }), "/images/responsive/deluxe-room-960w.webp");
  assert.equal(staticImageLoader({ src, width: 3200 }), src);
  assert.equal(staticImageLoader({ src: "/images/varanasi-hero.webp", width: 3200 }), "/images/responsive/varanasi-hero-1600w.webp");
});

test("smaller originals never upscale and unrelated brand artwork passes through unchanged", () => {
  assert.equal(staticImageLoader({ src: "/images/google-dining-room.webp", width: 1600 }), "/images/google-dining-room.webp");
  for (const src of ["/brand/logo.jpeg", "/icon.svg", "data:image/png;base64,AA=="]) {
    assert.equal(staticImageLoader({ src, width: 480 }), src);
  }
  assert.throws(() => staticImageLoader({ src: "/images/deluxe-room.webp", width: 0 }), /Invalid responsive/);
});

test("every local photograph has complete, smaller responsive files with intact source hashes", async () => {
  const originals = (await readdir(resolve(root, "public/images"))).filter(name => name.endsWith(".webp")).sort();
  assert.deepEqual(report.assets.map(asset => asset.source.replace("/images/", "")).sort(), originals);
  for (const asset of report.assets) {
    const source = await readFile(resolve(root, `public${asset.source}`));
    assert.equal(digest(source), asset.sourceSha256, asset.source);
    assert.ok(asset.provenance.ledger, asset.source);
    for (const width of [96, 192, 480, 960]) {
      assert.ok(asset.variants.some(variant => variant.width === width), `${asset.source} ${width}`);
    }
    for (const variant of asset.variants) {
      const file = resolve(root, `public${variant.src}`);
      assert.equal((await stat(file)).size, variant.bytes);
      assert.equal(digest(await readFile(file)), variant.sha256, variant.src);
      assert.ok(variant.width <= asset.sourceDimensions[0], variant.src);
      assert.ok(Math.abs(variant.height - asset.sourceDimensions[1] * variant.width / asset.sourceDimensions[0]) <= .5, variant.src);
      if (variant.width <= 960) assert.ok(variant.bytes < asset.sourceBytes, variant.src);
    }
  }
});

test("static export uses the local loader; normal builds retain Next AVIF/WebP optimization", async () => {
  const original = process.env.SITE_STATIC_EXPORT;
  try {
    process.env.SITE_STATIC_EXPORT = "true";
    const preview = (await import(`${configPath.href}?test=static-images`)).default;
    assert.equal(preview.output, "export");
    assert.equal(preview.images.loader, "custom");
    assert.equal(preview.images.loaderFile, "./lib/static-image-loader.ts");
    assert.notEqual(preview.images.unoptimized, true);
    assert.deepEqual(preview.images.deviceSizes, [480, 960, 1600]);
    process.env.SITE_STATIC_EXPORT = "false";
    const normal = (await import(`${configPath.href}?test=normal-images`)).default;
    assert.equal(normal.output, undefined);
    assert.equal(normal.images.loader, undefined);
    assert.equal(normal.images.loaderFile, undefined);
    assert.notEqual(normal.images.unoptimized, true);
    assert.deepEqual(normal.images.formats, ["image/avif", "image/webp"]);
    assert.deepEqual(normal.images.qualities, [75, 85]);
  } finally {
    if (original === undefined) delete process.env.SITE_STATIC_EXPORT;
    else process.env.SITE_STATIC_EXPORT = original;
  }
});

test("Next generates responsive static srcsets and keeps optimizer URLs for normal deployment", () => {
  const input = { src: "/images/deluxe-room.webp", alt: "Guest room", fill: true, sizes: "100vw", quality: 85 };
  const staticConfig = {
    ...imageConfigDefault, loader: "custom", deviceSizes: [480, 960, 1600],
    imageSizes: [96, 192], allSizes: [96, 192, 480, 960, 1600], qualities: [75, 85],
  };
  const preview = getImgProps(input, { imgConf: staticConfig, defaultLoader: staticImageLoader }).props;
  assert.equal(preview.sizes, "100vw");
  assert.equal(preview.srcSet, [
    "/images/responsive/deluxe-room-480w.webp 480w",
    "/images/responsive/deluxe-room-960w.webp 960w",
    "/images/deluxe-room.webp 1600w",
  ].join(", "));
  const thumbnail = getImgProps({ ...input, sizes: "72px" }, {
    imgConf: staticConfig, defaultLoader: staticImageLoader,
  }).props;
  assert.ok(thumbnail.srcSet.includes("/images/responsive/deluxe-room-96w.webp 96w"));
  assert.ok(thumbnail.srcSet.includes("/images/responsive/deluxe-room-192w.webp 192w"));
  const normalConfig = {
    ...imageConfigDefault, qualities: [75, 85],
    allSizes: [...imageConfigDefault.deviceSizes, ...imageConfigDefault.imageSizes].sort((a, b) => a - b),
  };
  const normal = getImgProps(input, { imgConf: normalConfig, defaultLoader: nextImageLoader }).props;
  assert.ok(normal.srcSet.includes("/_next/image?url="));
  assert.ok(!normal.srcSet.includes("/images/responsive/"));
});
