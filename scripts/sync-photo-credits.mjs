import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";

// Research stays local; only the fields rendered by the privacy page ship.
const root = new URL("../", import.meta.url);
const readJson = async (path) => JSON.parse(await readFile(new URL(path, root), "utf8"));
const manifest = await readJson("research/assets/asset-manifest.json");
const hero = await readJson("research/awwwards-revision/hero-asset.json");
const credits = [
  ...manifest.assets.filter((asset) => asset.kind === "destination" && Boolean(asset.public_path)),
  { ...hero, rights: hero.license },
].map(({ id, author, source_page, rights, license_url }) => ({
  id, author, source_page, rights, license_url,
}));

const output = new URL("content/photo-credits.json", root);
const serialized = `${JSON.stringify(credits, null, 2)}\n`;
if (process.argv.includes("--check")) {
  assert.equal(await readFile(output, "utf8"), serialized, "Photo credits are stale. Run npm run credits:sync.");
  console.log(`Verified ${credits.length} destination photo credits.`);
} else {
  await writeFile(output, serialized, "utf8");
  console.log(`Synced ${credits.length} destination photo credits.`);
}
