// Shared helpers for render.mjs and dwell.mjs: a tiny static server and Playwright loading.
import http from "http";
import fs from "fs";
import path from "path";

const TYPES = { ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript", ".json": "application/json",
  ".css": "text/css", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp",
  ".svg": "image/svg+xml", ".woff2": "font/woff2", ".ttf": "font/ttf", ".mp4": "video/mp4", ".wav": "audio/wav" };

// Serve a directory on a free port. Returns { url, close }.
export function serve(dir) {
  const root = path.resolve(dir);
  const server = http.createServer((req, res) => {
    const p = path.join(root, decodeURIComponent(req.url.split("?")[0]));
    if (!p.startsWith(root) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { "content-type": TYPES[path.extname(p).toLowerCase()] || "application/octet-stream" });
    fs.createReadStream(p).pipe(res);
  });
  return new Promise((ok) => server.listen(0, "127.0.0.1", () =>
    ok({ url: `http://127.0.0.1:${server.address().port}`, close: () => server.close() })));
}

export async function chromium() {
  const tries = [process.env.PLAYWRIGHT_PATH, "playwright", "playwright-core"].filter(Boolean);
  for (const t of tries) {
    try { const m = await import(t); return (m.default || m).chromium; } catch { /* next */ }
  }
  console.error("Playwright not found: `npm i -D playwright && npx playwright install chromium`, or set PLAYWRIGHT_PATH.");
  process.exit(2);
}

export async function launch() {
  const c = await chromium();
  return c.launch(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {});
}

export function args(defaults) {
  const a = { ...defaults };
  const argv = process.argv.slice(2);
  for (let i = 0; i < argv.length; i++) if (argv[i].startsWith("--")) {
    const k = argv[i].slice(2), v = argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : "true";
    a[k] = typeof defaults[k] === "number" ? Number(v) : v;
  }
  return a;
}
