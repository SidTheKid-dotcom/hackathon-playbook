#!/usr/bin/env python3
"""Put images, or frames from a video, into one labelled grid so a person (or an agent) can review them by eye.

Usage:
  python3 contact_sheet.py sheet.png img1.png img2.png ...        [--cols 4] [--thumb 480]
  python3 contact_sheet.py sheet.png --video final.mp4 --every 1.0 [--start 0 --end 60] [--cols 6] [--thumb 320]
Large frame sets are split into several sheets: sheet_01.png, sheet_02.png ...
Needs Pillow (pip install pillow); --video needs ffmpeg.
"""
import argparse, glob, math, os, subprocess, sys, tempfile

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("Pillow is missing: pip install pillow")


def frames_from_video(video, every, start, end, tmp):
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                               capture_output=True, text=True, check=True).stdout)
    end = min(end or dur, dur)
    files, t = [], start
    while t < end:
        f = os.path.join(tmp, f"f_{t:09.3f}.jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1", "-q:v", "3", "-y", f], check=True)
        if os.path.exists(f):
            files.append((f, f"{int(t // 60)}:{t % 60:05.2f}"))
        t += every
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("images", nargs="*")
    ap.add_argument("--video"); ap.add_argument("--every", type=float, default=1.0)
    ap.add_argument("--start", type=float, default=0.0); ap.add_argument("--end", type=float, default=0.0)
    ap.add_argument("--cols", type=int, default=4); ap.add_argument("--thumb", type=int, default=480)
    ap.add_argument("--per-sheet", type=int, default=36)
    a = ap.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        if a.video:
            items = frames_from_video(a.video, a.every, a.start, a.end, tmp)
        else:
            paths = [p for x in a.images for p in (sorted(glob.glob(x)) or [x])]
            items = [(p, os.path.basename(p)) for p in paths if os.path.exists(p)]
        if not items:
            sys.exit("no images found")
        sheets = math.ceil(len(items) / a.per_sheet)
        stem, ext = os.path.splitext(a.out)
        for s in range(sheets):
            chunk = items[s * a.per_sheet:(s + 1) * a.per_sheet]
            ims = []
            for p, label in chunk:
                im = Image.open(p).convert("RGB")
                im.thumbnail((a.thumb, a.thumb * 3))
                ims.append((im, label))
            cw = max(i.width for i, _ in ims); ch = max(i.height for i, _ in ims) + 20
            cols = min(a.cols, len(ims)); rows = math.ceil(len(ims) / cols)
            sheet = Image.new("RGB", (cols * (cw + 8) + 8, rows * (ch + 8) + 8), "white")
            d = ImageDraw.Draw(sheet)
            for k, (im, label) in enumerate(ims):
                x, y = 8 + (k % cols) * (cw + 8), 8 + (k // cols) * (ch + 8)
                d.text((x + 2, y + 2), label[:60], fill="black")
                sheet.paste(im, (x, y + 18))
            name = a.out if sheets == 1 else f"{stem}_{s + 1:02}{ext}"
            sheet.save(name)
            print(name, sheet.size, f"{len(ims)} tiles")


if __name__ == "__main__":
    main()
