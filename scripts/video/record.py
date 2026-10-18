"""Record the real product: a headed Chromium on a virtual display, captured with ffmpeg, with a
smooth, hand-like cursor and a log of when each action happens.

Usage:
  uv run --with playwright python record.py takes.py [take_name ...]
    takes.py defines `async def take_<name>(ctx, Take)`. In it: page = await ctx.new_page(); await page.goto(...);
    tk = Take(page, "<name>"); await tk.start(); ... tk.mark("event"); await tk.click(locator) ...; await tk.stop()
  Env: BASE (the URL your takes use), OUT (default ./rec), W/H (CSS size, default 1920x1080), DSF (default 1.5),
       CHROME (path to a Chromium; default: Playwright's), DISPLAY_NUM (default 99).
Output per take: OUT/<name>.mkv (H.264, CRF 12, 30 fps) and OUT/<name>.json (seconds of each mark).
Needs: Xvfb, ffmpeg, Playwright. Starts Xvfb itself if the display is not running.

Why headed + x11grab: headless screen recording is low quality and drops frames.
Gotchas seen: black frames on Xvfb (fixed by --ozone-platform=x11 --use-gl=swiftshader); the native mouse is not
captured (Playwright moves no real cursor), so a DOM cursor is injected; trim the browser tab strip later with ffmpeg crop.
"""
import asyncio, importlib.util, json, math, os, subprocess, sys, time
from playwright.async_api import async_playwright

W, H = int(os.environ.get("W", 1920)), int(os.environ.get("H", 1080))
DSF = float(os.environ.get("DSF", 1.5))
PX, PY = int(W * DSF), int(H * DSF)
OUT = os.environ.get("OUT", "rec")
DISP = f":{os.environ.get('DISPLAY_NUM', '99')}"

CURSOR = r"""(() => {
  const css = `::-webkit-scrollbar{display:none} html{scrollbar-width:none}
  #rec-cursor{position:fixed;left:0;top:0;width:26px;height:26px;z-index:2147483647;pointer-events:none;
    transform:translate(-100px,-100px);filter:drop-shadow(0 2px 3px rgba(0,0,0,.35))}
  .rec-ripple{position:fixed;z-index:2147483646;pointer-events:none;width:44px;height:44px;margin:-22px 0 0 -22px;
    border-radius:50%;border:3px solid rgba(47,95,179,.75);animation:recr .5s ease-out forwards}
  @keyframes recr{from{transform:scale(.3);opacity:1}to{transform:scale(1.4);opacity:0}}`;
  const add = () => {
    if (document.getElementById('rec-cursor')) return;
    const s = document.createElement('style'); s.textContent = css; document.head.appendChild(s);
    const c = document.createElement('div'); c.id = 'rec-cursor';
    c.innerHTML = '<svg viewBox="0 0 24 24" width="26" height="26"><path d="M4 2 L4 19 L8.6 14.8 L11.6 21.4 L14.4 20.2 L11.4 13.7 L17.6 13.7 Z" fill="#16130f" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>';
    document.body.appendChild(c);
  };
  document.addEventListener('mousemove', e => { const c = document.getElementById('rec-cursor'); if (c) c.style.transform = `translate(${e.clientX}px,${e.clientY}px)`; }, true);
  document.addEventListener('mousedown', e => { const r = document.createElement('div'); r.className = 'rec-ripple';
    r.style.left = e.clientX + 'px'; r.style.top = e.clientY + 'px'; document.body.appendChild(r); setTimeout(() => r.remove(), 600); }, true);
  if (document.readyState !== 'loading') add(); else document.addEventListener('DOMContentLoaded', add);
})();"""


class Take:
    def __init__(self, page, name):
        self.page, self.name, self.pos, self.marks, self.t0, self.proc = page, name, (W * 0.6, H * 0.55), {}, None, None

    async def start(self):
        os.makedirs(OUT, exist_ok=True)
        self.proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "x11grab", "-draw_mouse", "0", "-framerate", "30",
                                      "-video_size", f"{PX}x{PY}", "-i", f"{DISP}.0", "-c:v", "libx264", "-preset", "ultrafast",
                                      "-crf", "12", "-pix_fmt", "yuv420p", f"{OUT}/{self.name}.mkv"], stdin=subprocess.PIPE)
        await asyncio.sleep(0.6)
        self.t0 = time.monotonic()
        await self.page.mouse.move(*self.pos)

    def mark(self, key):
        self.marks[key] = round(time.monotonic() - self.t0, 3)

    async def stop(self, tail=0.8):
        await asyncio.sleep(tail)
        self.mark("end")
        self.proc.stdin.write(b"q"); self.proc.stdin.flush(); self.proc.wait(timeout=30)
        json.dump(self.marks, open(f"{OUT}/{self.name}.json", "w"), indent=1)
        print(self.name, self.marks, flush=True)

    async def move(self, x, y, dur=0.7):
        """Eased, slightly curved path, like a hand."""
        x0, y0 = self.pos
        steps = max(8, int(dur * 60))
        bend = 0.12 * math.hypot(x - x0, y - y0)
        nx, ny = -(y - y0), (x - x0)
        n = math.hypot(nx, ny) or 1
        cx, cy = (x0 + x) / 2 + nx / n * bend, (y0 + y) / 2 + ny / n * bend
        for i in range(1, steps + 1):
            e = (i / steps) ** 2 * (3 - 2 * i / steps)
            await self.page.mouse.move((1 - e) ** 2 * x0 + 2 * (1 - e) * e * cx + e * e * x,
                                       (1 - e) ** 2 * y0 + 2 * (1 - e) * e * cy + e * e * y)
            await asyncio.sleep(dur / steps)
        self.pos = (x, y)

    async def to(self, locator, dur=0.75, dx=0.5, dy=0.5):
        box = await locator.bounding_box()
        await self.move(box["x"] + box["width"] * dx, box["y"] + box["height"] * dy, dur)

    async def click(self, locator, dur=0.75, key=None, pause=0.18):
        await self.to(locator, dur)
        await asyncio.sleep(pause)
        if key:
            self.mark(key)
        await self.page.mouse.down(); await asyncio.sleep(0.07); await self.page.mouse.up()

    async def scroll(self, dy, dur=1.2):
        steps, done = int(dur * 60), 0
        for i in range(1, steps + 1):
            target = dy * (i / steps) ** 2 * (3 - 2 * i / steps)
            await self.page.mouse.wheel(0, target - done); done = target
            await asyncio.sleep(dur / steps)


def ensure_display():
    if os.path.exists(f"/tmp/.X11-unix/X{DISP[1:]}"):
        return None
    proc = subprocess.Popen(["Xvfb", DISP, "-screen", "0", f"{PX}x{PY}x24", "-nolisten", "tcp"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    time.sleep(1.5)
    return proc


async def main(takes_path, names):
    spec = importlib.util.spec_from_file_location("takes", takes_path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    takes = {k[5:]: v for k, v in vars(mod).items() if k.startswith("take_")}
    xvfb = ensure_display()
    os.environ["DISPLAY"] = DISP
    try:
        async with async_playwright() as p:
            args = ["--ozone-platform=x11", "--disable-gpu", "--use-gl=swiftshader", f"--window-size={W},{H}",
                    "--window-position=0,0", f"--force-device-scale-factor={DSF}", "--disable-infobars",
                    "--hide-scrollbars", "--noerrdialogs", "--disable-features=Translate"]
            kw = {"executable_path": os.environ["CHROME"]} if os.environ.get("CHROME") else {}
            browser = await p.chromium.launch(headless=False, args=args, **kw)
            ctx = await browser.new_context(no_viewport=True)
            await ctx.add_init_script(CURSOR)
            for name in names or list(takes):
                await takes[name](ctx, Take)
            await browser.close()
    finally:
        if xvfb:
            xvfb.terminate()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    asyncio.run(main(sys.argv[1], sys.argv[2:]))
