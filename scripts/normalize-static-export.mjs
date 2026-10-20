import { createHash } from "node:crypto";
import { lstat, readFile, readdir, realpath, writeFile } from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

const hash = (bytes) => createHash("sha256").update(bytes).digest("hex");

function assertInside(root, filename) {
  const relative = path.relative(root, filename);
  if (relative === ".." || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) {
    throw new Error(`Static payload path escapes export directory: ${filename}`);
  }
}

async function regularTree(root, directory, files) {
  assertInside(root, directory);
  for (const entry of (await readdir(directory, { withFileTypes: true })).sort((a, b) => a.name.localeCompare(b.name))) {
    const filename = path.join(directory, entry.name);
    const info = await lstat(filename);
    if (info.isSymbolicLink()) throw new Error(`Refusing symlink in static export: ${filename}`);
    if (info.isDirectory()) await regularTree(root, filename, files);
    else if (info.isFile()) files.push(filename);
    else throw new Error(`Refusing non-regular export entry: ${filename}`);
  }
}

/**
 * Next 16.4.2 collects exported RSC segment paths with path.relative(), then
 * replaces only "/" in its filename encoder. On Windows, remaining backslashes
 * create nested directories instead of the dotted URLs its browser requests.
 * Add byte-identical aliases after export; keep every original payload intact.
 */
export async function normalizeStaticExport(directory) {
  const root = path.resolve(directory);
  const rootInfo = await lstat(root);
  if (!rootInfo.isDirectory() || rootInfo.isSymbolicLink()) {
    throw new Error(`Static export root must be a regular directory: ${root}`);
  }
  if (path.relative(root, await realpath(root)) !== "") {
    throw new Error(`Static export root resolves through a symbolic path: ${root}`);
  }
  const files = [];
  await regularTree(root, root, files);
  const plan = [];
  const plannedDestinations = new Map();
  for (const source of files) {
    if (!source.endsWith(".txt")) continue;
    const parts = path.relative(root, source).split(path.sep);
    const segmentIndex = parts.findIndex((part) => /^__next(?:\.|$)/.test(part));
    if (segmentIndex < 0 || segmentIndex === parts.length - 1) continue;
    const destination = path.join(root, ...parts.slice(0, segmentIndex), parts.slice(segmentIndex).join("."));
    assertInside(root, destination);
    const bytes = await readFile(source);
    const digest = hash(bytes);
    const duplicate = plannedDestinations.get(destination);
    if (duplicate && duplicate !== digest) {
      throw new Error(`Conflicting generated static payload destination: ${destination}`);
    }
    plannedDestinations.set(destination, digest);
    let existing = false;
    try {
      const info = await lstat(destination);
      if (!info.isFile() || info.isSymbolicLink()) throw new Error(`Non-regular static payload destination: ${destination}`);
      if (!(await readFile(destination)).equals(bytes)) throw new Error(`Conflicting static payload destination: ${destination}`);
      existing = true;
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
    plan.push({ source, destination, bytes, digest, existing });
  }
  // Validate the entire plan before writing any alias.
  const results = [];
  for (const item of plan) {
    if (!item.existing) {
      try {
        await writeFile(item.destination, item.bytes, { flag: "wx" });
      } catch (error) {
        if (error.code !== "EEXIST") throw error;
        const info = await lstat(item.destination);
        if (!info.isFile() || info.isSymbolicLink() || !(await readFile(item.destination)).equals(item.bytes)) {
          throw new Error(`Static payload destination changed during normalization: ${item.destination}`);
        }
        item.existing = true;
      }
    }
    if (!(await readFile(item.destination)).equals(item.bytes)) {
      throw new Error(`Static payload alias verification failed: ${item.destination}`);
    }
    results.push({
      source: path.relative(root, item.source).split(path.sep).join("/"),
      destination: path.relative(root, item.destination).split(path.sep).join("/"),
      bytes: item.bytes.length, sha256: item.digest,
      action: item.existing ? "already-identical" : "created",
    });
  }
  return {
    exportDirectory: root,
    candidates: results.length,
    created: results.filter((item) => item.action === "created").length,
    alreadyIdentical: results.filter((item) => item.action === "already-identical").length,
    originalsPreserved: true,
    payloads: results,
  };
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  if (process.env.SITE_STATIC_EXPORT !== "true") {
    console.log("Static payload normalization skipped: normal Next.js build.");
  } else {
    try {
      console.log(JSON.stringify(await normalizeStaticExport(path.resolve("out")), null, 2));
    } catch (error) {
      console.error(error.message);
      process.exitCode = 1;
    }
  }
}
