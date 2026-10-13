#!/usr/bin/env node
// Reading-time audit: how long is every piece of on-screen text fully visible? Steps the composition at 10 fps.
// Flags text shown for less than 0.5 s + 0.22 s per word (minimum 1.2 s). Sources and credits count too.
// Usage: node dwell.mjs [--dir .] [--page composition.html] [--stage #stage] [--skip .cap] [--w 1920] [--h 1080]
import { serve, launch, args } from "./lib.mjs";

const A = args({ dir: ".", page: "composition.html", stage: "#stage", skip: ".cap", w: 1920, h: 1080, step: 0.1 });
const srv = await serve(A.dir);
const b = await launch();
const p = await b.newPage({ viewport: { width: A.w, height: A.h } });
await p.goto(`${srv.url}/${A.page}`);
const info = await p.evaluate(() => window.ready);
await p.evaluate(([stageSel, skip, W, H]) => {
  const stage = document.querySelector(stageSel) || document.body;
  window.__texts = [...stage.querySelectorAll("*")].filter((e) => !(skip && e.closest(skip)) &&
    [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 1));
  window.__vis = (e) => {
    let o = 1;
    for (let x = e; x && x !== stage.parentElement; x = x.parentElement) {
      const cs = getComputedStyle(x);
      if (cs.visibility === "hidden" || cs.display === "none") return 0;
      o *= +cs.opacity;
    }
    const r = e.getBoundingClientRect();
    return r.width < 2 || r.bottom < 0 || r.top > H || r.right < 0 || r.left > W ? 0 : o;
  };
}, [A.stage, A.skip, A.w, A.h]);
const N = Math.floor(info.total / A.step), seen = {};
for (let i = 0; i <= N; i++) {
  const t = i * A.step;
  await p.evaluate((t) => window.seek(t), t);
  const v = new Map(await p.evaluate(() => window.__texts.map((e, k) => [k, window.__vis(e)]).filter(([, o]) => o > 0.05)));
  for (const [k, s] of Object.entries(seen)) if (!v.has(+k) && s.cur) { s.runs.push(s.cur); s.cur = null; }
  for (const [k, o] of v) {
    const s = (seen[k] ||= { runs: [], cur: null, first: t });
    if (o >= 0.9) { if (!s.cur) s.cur = [t, t]; s.cur[1] = t; } else if (s.cur) { s.runs.push(s.cur); s.cur = null; }
  }
}
for (const s of Object.values(seen)) if (s.cur) s.runs.push(s.cur);
const texts = await p.evaluate(() => window.__texts.map((e) => e.textContent.replace(/\s+/g, " ").trim()));
await b.close(); srv.close();
const rows = Object.entries(seen).map(([k, s]) => {
  const words = texts[k].split(" ").length, need = Math.max(1.2, 0.5 + 0.22 * words);
  return { text: texts[k], first: s.first, best: Math.max(0, ...s.runs.map(([a, z]) => z - a + A.step)), need };
});
const short = rows.filter((r) => r.best < r.need).sort((a, z) => a.first - z.first);
console.log(`texts seen: ${rows.length}; under reading time (0.5 s + 0.22 s per word, min 1.2 s): ${short.length}`);
for (const r of short) console.log(`  ${(r.first / 60) | 0}:${(r.first % 60).toFixed(1).padStart(4, "0")}  shown ${r.best.toFixed(1)} s, needs ${r.need.toFixed(1)} s  "${r.text.slice(0, 80)}"`);
process.exit(short.length ? 1 : 0);
