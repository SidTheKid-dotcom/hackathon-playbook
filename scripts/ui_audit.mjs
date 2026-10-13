#!/usr/bin/env node
// UI audit for any web app: routes x widths x languages.
// Flags: sideways scroll, clipped text, overlapping text, small tap targets (touch widths), console/page errors.
// Saves one screenshot per page so you can build contact sheets (contact_sheet.py) and LOOK at them.
//
// Usage:
//   node ui_audit.mjs --base http://localhost:5173 --routes "/,/about,/item/1" \
//     [--widths 320,360,390,412,768,1024,1280,1440,1920] [--landscape] \
//     [--langs en,mr,hi --lang-param lang] [--out audit] [--wait 800] [--full]
// Needs Playwright: `npm i -D playwright && npx playwright install chromium`
//   or set PLAYWRIGHT_PATH=/path/to/playwright-core/index.js and CHROME_PATH=/path/to/chrome.
import fs from "fs";
import path from "path";

const args = Object.fromEntries(process.argv.slice(2).reduce((acc, a, i, all) => {
  if (a.startsWith("--")) acc.push([a.slice(2), all[i + 1] && !all[i + 1].startsWith("--") ? all[i + 1] : "true"]);
  return acc;
}, []));
if (!args.base || !args.routes) {
  console.error("Usage: node ui_audit.mjs --base <url> --routes \"/,/x\" [--widths ..] [--langs en,hi --lang-param lang] [--out dir]");
  process.exit(2);
}
const base = args.base.replace(/\/$/, "");
const routes = args.routes.split(",").map((r) => r.trim()).filter(Boolean);
const widths = (args.widths || "320,360,390,412,768,1024,1280,1440,1920").split(",").map(Number);
const langs = args.langs ? args.langs.split(",") : [null];
const langParam = args["lang-param"] || "lang";
const out = args.out || "audit";
const wait = Number(args.wait || 800);
fs.mkdirSync(out, { recursive: true });

async function loadPlaywright() {
  const tries = [process.env.PLAYWRIGHT_PATH, "playwright", "playwright-core"].filter(Boolean);
  for (const t of tries) {
    try { const m = await import(t); return m.default || m; } catch { /* try next */ }
  }
  console.error("Playwright not found. Run `npm i -D playwright && npx playwright install chromium`, or set PLAYWRIGHT_PATH.");
  process.exit(2);
}
const pw = await loadPlaywright();
const launch = { headless: true };
if (process.env.CHROME_PATH) launch.executablePath = process.env.CHROME_PATH;
const browser = await pw.chromium.launch(launch);

// Runs inside the page. Returns a list of problems.
function inspect([touch, W]) {
  // W is the viewport width we asked for; on mobile emulation innerWidth can grow to fit wide content.
  const problems = [];
  const visible = (el) => {
    for (let x = el; x && x !== document.documentElement; x = x.parentElement) {
      const cs = getComputedStyle(x);
      if (cs.display === "none" || cs.visibility === "hidden" || Number(cs.opacity) < 0.05) return false;
    }
    const r = el.getBoundingClientRect();
    return r.width > 1 && r.height > 1;
  };
  const label = (el) => {
    const t = (el.innerText || el.getAttribute("aria-label") || el.tagName).replace(/\s+/g, " ").trim();
    return `${el.tagName.toLowerCase()}${el.className && typeof el.className === "string" ? "." + el.className.split(" ")[0] : ""} "${t.slice(0, 40)}"`;
  };
  if (document.documentElement.scrollWidth > W + 1) problems.push({ type: "sideways-scroll", detail: `page is ${document.documentElement.scrollWidth}px wide in a ${W}px viewport` });

  // Elements that own visible text directly.
  const textEls = [...document.querySelectorAll("body *")].filter((el) =>
    [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 1) && visible(el) && !el.closest("[aria-hidden=true], .sr-only, .visually-hidden"));

  // Clipped text: content larger than its box while overflow hides it. An ellipsis is reported as info only.
  for (const el of textEls) {
    const cs = getComputedStyle(el);
    const hidesX = /hidden|clip/.test(cs.overflowX), hidesY = /hidden|clip/.test(cs.overflowY);
    if (hidesX && el.scrollWidth > el.clientWidth + 2)
      problems.push({ type: cs.textOverflow === "ellipsis" ? "info-truncated" : "clipped-text", detail: `${label(el)} needs ${el.scrollWidth}px, has ${el.clientWidth}px` });
    else if (hidesY && el.scrollHeight > el.clientHeight + 2) problems.push({ type: "clipped-text", detail: `${label(el)} needs ${el.scrollHeight}px tall, has ${el.clientHeight}px` });
    const r = el.getBoundingClientRect();
    // text inside its own horizontal scroller (e.g. a wide table wrapper) is by design, not off-screen
    let scroller = false;
    for (let x = el.parentElement; x && x !== document.body; x = x.parentElement) if (/auto|scroll|hidden|clip/.test(getComputedStyle(x).overflowX)) { scroller = true; break; }
    if (r.right > W + 1 && cs.position !== "fixed" && !scroller) problems.push({ type: "off-screen-text", detail: `${label(el)} ends at ${Math.round(r.right)}px` });
  }

  // Overlap: compare per-line text boxes (so wrapped inline text is not a false hit) with other text and with
  // images, video and controls. Skipped: decorative layers (aria-hidden, pointer-events:none, unlabelled svg),
  // anything inside a fixed or sticky layer (those cover content by design while scrolling), ancestor/descendant pairs.
  const layered = (el) => { for (let x = el; x && x !== document.body; x = x.parentElement) { const p = getComputedStyle(x).position; if (p === "fixed" || p === "sticky") return true; } return false; };
  const decorative = (el) => !!el.closest("[aria-hidden=true]") || getComputedStyle(el).pointerEvents === "none";
  const textRects = (el) => {
    const range = document.createRange(), out = [];
    for (const n of el.childNodes) if (n.nodeType === 3 && n.textContent.trim()) {
      range.selectNodeContents(n);
      for (const r of range.getClientRects()) if (r.width > 1 && r.height > 1) out.push(r);
    }
    return out;
  };
  const media = [...document.querySelectorAll("img, video, canvas, button, input, select, textarea, [role=button], svg[role=img]")]
    .filter((el) => visible(el) && !decorative(el) && !layered(el));
  const items = textEls.filter((el) => !layered(el) && !decorative(el)).map((el) => ({ el, rs: textRects(el) })).filter((x) => x.rs.length)
    .concat(media.map((el) => ({ el, rs: [el.getBoundingClientRect()], media: true })));
  const seen = new Set();
  for (let i = 0; i < items.length; i++) for (let j = i + 1; j < items.length; j++) {
    const A = items[i], B = items[j];
    if (A.media && B.media) continue;
    if (A.el.contains(B.el) || B.el.contains(A.el)) continue;
    let hit = null;
    for (const a of A.rs) for (const b of B.rs) {
      const ox = Math.min(a.right, b.right) - Math.max(a.left, b.left), oy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      if (ox > 3 && oy > Math.max(4, 0.3 * Math.min(a.height, b.height))) { hit = [ox, oy]; break; }
    }
    if (!hit) continue;
    const k = label(A.el) + "|" + label(B.el); if (seen.has(k)) continue; seen.add(k);
    problems.push({ type: "overlap", detail: `${label(A.el)} overlaps ${label(B.el)} by ${Math.round(hit[0])}x${Math.round(hit[1])}px` });
  }

  // Tap targets on touch screens: controls under 44x44 px (Apple/AAA); links inside a sentence are exempt
  // (WCAG 2.5.8 inline exception) unless under 24 px tall.
  if (touch) for (const el of document.querySelectorAll("a, button, input, select, [role=button]")) {
    if (!visible(el)) continue;
    const r = el.getBoundingClientRect();
    const inline = el.tagName === "A" &&
      [...(el.parentElement?.childNodes || [])].some((n) => n !== el && n.textContent.trim().length > 2);
    if (inline ? r.height < 24 : (r.width < 44 || r.height < 44))
      problems.push({ type: "small-tap-target", detail: `${label(el)} is ${Math.round(r.width)}x${Math.round(r.height)}px` });
  }
  return problems;
}

const report = [];
const viewports = widths.map((w) => ({ w, h: w <= 820 ? 844 : 900 }));
if (args.landscape) viewports.push({ w: 844, h: 390 });
let pages = 0;
for (const lang of langs) for (const vp of viewports) {
  const touch = vp.w <= 820;
  const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h }, hasTouch: touch, isMobile: touch && vp.w < 700, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  const errors = [];
  page.on("console", (m) => m.type() === "error" && !/favicon/.test(m.location()?.url || "") && errors.push(m.text().slice(0, 160)));
  page.on("pageerror", (e) => errors.push("pageerror " + String(e).slice(0, 160)));
  for (const route of routes) {
    let url = base + route;
    if (lang) url += (url.includes("?") ? "&" : "?") + `${langParam}=${encodeURIComponent(lang)}`;
    errors.length = 0;
    try { await page.goto(url, { waitUntil: "networkidle", timeout: 30000 }); }
    catch (e) { report.push({ lang, width: vp.w, height: vp.h, route, problems: [{ type: "load-failed", detail: String(e).slice(0, 160) }] }); continue; }
    await page.waitForTimeout(wait);
    const problems = await page.evaluate(inspect, [touch, vp.w]);
    for (const e of errors) problems.push({ type: "console-error", detail: e });
    const name = `${lang || "x"}_${vp.w}x${vp.h}_${route.replace(/[^a-z0-9]+/gi, "_").replace(/^_|_$/g, "") || "home"}.png`;
    await page.screenshot({ path: path.join(out, name), fullPage: args.full === "true" });
    report.push({ lang, width: vp.w, height: vp.h, route, screenshot: name, problems });
    pages++;
  }
  await ctx.close();
}
await browser.close();
fs.writeFileSync(path.join(out, "report.json"), JSON.stringify(report, null, 1));

const counts = {}, groups = {};
for (const r of report) for (const p of r.problems) {
  counts[p.type] = (counts[p.type] || 0) + 1;
  if (p.type.startsWith("info")) continue; // listed in report.json only
  const g = (groups[p.type + "|" + p.detail] ||= { type: p.type, detail: p.detail, where: [] });
  g.where.push(`${r.lang ? r.lang + " " : ""}${r.width}px ${r.route}`);
}
console.log(`${pages} page loads (${langs.length} lang x ${viewports.length} viewports x ${routes.length} routes). Screenshots + report.json in ${out}/`);
console.log("problems by type:", Object.keys(counts).length ? counts : "none");
for (const g of Object.values(groups).sort((x, y) => y.where.length - x.where.length).slice(0, 40))
  console.log(`  [${g.type}] ${g.detail}  (${g.where.length} page${g.where.length > 1 ? "s" : ""}: ${g.where.slice(0, 3).join(", ")}${g.where.length > 3 ? ", ..." : ""})`);
console.log("Next: build a contact sheet and LOOK at it: python3 contact_sheet.py sheet.png " + out + "/*.png");
process.exit(Object.keys(counts).some((k) => ["sideways-scroll", "load-failed", "console-error", "off-screen-text"].includes(k)) ? 1 : 0);
