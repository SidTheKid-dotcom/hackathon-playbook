#!/usr/bin/env node
// Render a seek(t) HTML composition to MP4, frame by frame, in parallel headless pages.
// The page must define: window.ready -> Promise<{ total }>, window.seek(t) (may be async), and optionally window.CUES.
// Usage: node render.mjs [--dir .] [--page composition.html] [--workers 6] [--fps 30] [--w 1920] [--h 1080] [--from 0] [--to 0]
// Output: out/video.mp4 (silent), out/cues.json (sound cues for mix.py). Needs ffmpeg + Playwright.
import fs from "fs";
import path from "path";
import { spawn, spawnSync } from "child_process";
import { serve, launch, args } from "./lib.mjs";

const A = args({ dir: ".", page: "composition.html", workers: 6, fps: 30, w: 1920, h: 1080, from: 0, to: 0, crf: 16 });
const out = path.join(A.dir, "out");
fs.mkdirSync(out, { recursive: true });
const srv = await serve(A.dir);
const browser = await launch();

const probe = await browser.newPage({ viewport: { width: A.w, height: A.h } });
const errors = [];
probe.on("pageerror", (e) => errors.push(String(e)));
await probe.goto(`${srv.url}/${A.page}`);
const info = await probe.evaluate(() => window.ready);
if (errors.length) { console.error("page errors:", errors); process.exit(1); }
fs.writeFileSync(path.join(out, "cues.json"), JSON.stringify(await probe.evaluate(() => window.CUES || [])));
await probe.close();

const t0 = A.from, t1 = A.to || info.total;
const N = Math.ceil((t1 - t0) * A.fps), per = Math.ceil(N / A.workers);
console.log(`rendering ${N} frames (${(t1 - t0).toFixed(2)} s at ${A.fps} fps) on ${A.workers} workers`);
const start = Date.now();

async function worker(wi) {
  const f0 = wi * per, f1 = Math.min(N, f0 + per);
  if (f0 >= f1) return null;
  const p = await browser.newPage({ viewport: { width: A.w, height: A.h } });
  p.on("pageerror", (e) => console.error(`w${wi} pageerror`, String(e)));
  await p.goto(`${srv.url}/${A.page}`); await p.evaluate(() => window.ready);
  const cdp = await p.context().newCDPSession(p);
  const file = path.join(out, `chunk_${String(wi).padStart(2, "0")}.mp4`);
  const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(A.fps), "-c:v", "mjpeg", "-i", "-",
    "-c:v", "libx264", "-preset", "slow", "-crf", String(A.crf), "-pix_fmt", "yuv420p", "-r", String(A.fps), file], { stdio: ["pipe", "inherit", "inherit"] });
  for (let f = f0; f < f1; f++) {
    await p.evaluate((t) => window.seek(t), t0 + f / A.fps);
    const r = await cdp.send("Page.captureScreenshot", { format: "jpeg", quality: 95 });
    if (!ff.stdin.write(Buffer.from(r.data, "base64"))) await new Promise((ok) => ff.stdin.once("drain", ok));
    if ((f - f0) % 300 === 0 && f > f0) console.log(`  w${wi} ${f - f0}/${f1 - f0}`);
  }
  ff.stdin.end(); await new Promise((ok) => ff.on("close", ok)); await p.close();
  return file;
}

const files = (await Promise.all([...Array(A.workers).keys()].map(worker))).filter(Boolean).sort();
await browser.close(); srv.close();
fs.writeFileSync(path.join(out, "chunks.txt"), files.map((f) => `file '${path.resolve(f)}'`).join("\n"));
spawnSync("ffmpeg", ["-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", path.join(out, "chunks.txt"), "-c", "copy", path.join(out, "video.mp4")], { stdio: "inherit" });
console.log(`done in ${((Date.now() - start) / 1000).toFixed(0)} s -> ${path.join(out, "video.mp4")}`);
