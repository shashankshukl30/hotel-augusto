import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { lstat, mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";
import test from "node:test";
import { normalizeStaticExport } from "../scripts/normalize-static-export.mjs";

const root = fileURLToPath(new URL("..", import.meta.url));
const fixtureScope = path.join(root, ".openai");

async function fixture(t) {
  await mkdir(fixtureScope, { recursive: true });
  const directory = await mkdtemp(path.join(fixtureScope, "static-payload-test-"));
  t.after(async () => {
    const resolved = path.resolve(directory);
    assert.equal(path.dirname(resolved), fixtureScope);
    assert.ok(path.basename(resolved).startsWith("static-payload-test-"));
    assert.equal((await lstat(resolved)).isSymbolicLink(), false);
    await rm(resolved, { recursive: true });
  });
  return directory;
}

async function file(rootDirectory, relative, content) {
  const filename = path.join(rootDirectory, ...relative.split("/"));
  await mkdir(path.dirname(filename), { recursive: true });
  await writeFile(filename, content);
  return filename;
}

test("repairs nested Windows segment filenames including dynamic $d$slug; retains originals and is idempotent", async (t) => {
  const directory = await fixture(t);
  const examples = [
    ["contact/__next.contact/__PAGE__.txt", "contact/__next.contact.__PAGE__.txt", "contact-flight\n"],
    ["rooms/deluxe-room/__next.rooms/$d$slug/__PAGE__.txt", "rooms/deluxe-room/__next.rooms.$d$slug.__PAGE__.txt", "room-flight\n"],
  ];
  for (const [source, , bytes] of examples) await file(directory, source, bytes);
  const result = await normalizeStaticExport(directory);
  assert.equal(result.created, 2);
  assert.equal(result.originalsPreserved, true);
  for (const [source, destination, bytes] of examples) {
    assert.equal(await readFile(path.join(directory, source), "utf8"), bytes);
    assert.equal(await readFile(path.join(directory, destination), "utf8"), bytes);
  }
  const repeated = await normalizeStaticExport(directory);
  assert.equal(repeated.created, 0);
  assert.equal(repeated.alreadyIdentical, 2);
});

test("accepts a correct existing payload with identical bytes and ignores already-flat output", async (t) => {
  const directory = await fixture(t);
  await file(directory, "hotel/__next.hotel/__PAGE__.txt", "same");
  await file(directory, "hotel/__next.hotel.__PAGE__.txt", "same");
  await file(directory, "__next.__PAGE__.txt", "root");
  const result = await normalizeStaticExport(directory);
  assert.equal(result.candidates, 1);
  assert.equal(result.created, 0);
  assert.equal(result.alreadyIdentical, 1);
});

test("conflicting destination fails before any alias is written", async (t) => {
  const directory = await fixture(t);
  await file(directory, "contact/__next.contact/__PAGE__.txt", "contact");
  await file(directory, "rooms/__next.rooms/__PAGE__.txt", "expected");
  await file(directory, "rooms/__next.rooms.__PAGE__.txt", "conflict");
  await assert.rejects(normalizeStaticExport(directory), /Conflicting static payload destination/);
  await assert.rejects(lstat(path.join(directory, "contact/__next.contact.__PAGE__.txt")), { code: "ENOENT" });
  assert.equal(await readFile(path.join(directory, "rooms/__next.rooms.__PAGE__.txt"), "utf8"), "conflict");
});

test("rejects a file masquerading as export root", async (t) => {
  const directory = await fixture(t);
  const invalid = await file(directory, "out", "not-a-directory");
  await assert.rejects(normalizeStaticExport(invalid), /regular directory/);
});

test("postbuild guard leaves ordinary Next builds alone", async (t) => {
  const directory = await fixture(t);
  const result = await promisify(execFile)(
    process.execPath, [path.join(root, "scripts/normalize-static-export.mjs")],
    { cwd: directory, env: { ...process.env, SITE_STATIC_EXPORT: "false" } },
  );
  assert.match(result.stdout, /skipped: normal Next.js build/);
  await assert.rejects(lstat(path.join(directory, "out")), { code: "ENOENT" });
});
