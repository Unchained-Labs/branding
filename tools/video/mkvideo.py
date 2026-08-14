#!/usr/bin/env python3
"""Renders a terminal-session recording to MP4 and GIF, in Unchained Labs brand.

Not a slideshow: commands type character by character, output streams in line by
line, and the cursor blinks while idle — the shape of a real session. Every frame
is drawn with PIL rather than screen-captured, so the result is deterministic and
re-renderable, and the colours come from the brand tokens rather than a terminal
theme that happens to be installed.

The text is REAL captured CLI output. A promo video with invented output would be
a lie told in the most persuasive available medium.

Usage: mkvideo.py <cast.json> <out-dir>
"""
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

# ---- brand -------------------------------------------------------------------
# Mirrors branding/tokens/tokens.css. Kept as literals here only because this is
# a build tool outside the token pipeline; if these drift, tokens.css wins.
BG = (15, 20, 25)          # --ul-bg          #0F1419
RAISED = (23, 29, 38)      # --ul-bg-raised   #171D26
INSET = (11, 15, 19)       # --ul-bg-inset    #0B0F13
LINE = (35, 43, 53)        # --ul-line        #232B35
HEADING = (232, 237, 242)  # --ul-heading     #E8EDF2
BODY = (168, 179, 191)     # --ul-body        #A8B3BF
MUTED = (124, 136, 150)    # --ul-muted       #7C8896
FAINT = (90, 102, 115)     # --ul-faint       #5A6673
ACCENT = (0, 212, 170)     # --ul-accent      #00D4AA
UP = (74, 222, 128)        # --ul-up          #4ADE80
WARN = (232, 179, 57)      # --ul-warn        #E8B339
DOWN = (229, 72, 77)       # --ul-down        #E5484D

PALETTE = {
    "ok": UP, "er": DOWN, "wa": WARN, "ac": ACCENT,
    "dim": FAINT, "mut": MUTED, "hi": HEADING, "": BODY,
}

FONT_DIR = pathlib.Path.home() / ".local/share/fonts"
REG = FONT_DIR / "JetBrainsMonoNerdFont-Regular.ttf"
BOLD = FONT_DIR / "JetBrainsMonoNerdFont-Bold.ttf"

SCALE = 2                  # render at 2x, downscale for crispness
FPS = 20
FONT_PX = 15 * SCALE
PAD = 22 * SCALE
CHROME_H = 34 * SCALE
RADIUS = 9 * SCALE


class Renderer:
    def __init__(self, title: str, cols: int, rows: int):
        self.title = title
        self.font = ImageFont.truetype(str(REG), FONT_PX)
        self.bold = ImageFont.truetype(str(BOLD), FONT_PX)
        # Monospace metrics: measure once.
        self.cw = self.font.getlength("M")
        self.lh = int(FONT_PX * 1.55)
        self.w = int(self.cw * cols) + PAD * 2
        self.h = CHROME_H + self.lh * rows + PAD * 2
        self.rows = rows

    def frame(self, lines: list[tuple[str, str]], cursor: bool) -> Image.Image:
        """lines: (text, class) pairs. class picks a colour from PALETTE."""
        img = Image.new("RGB", (self.w, self.h), BG)
        d = ImageDraw.Draw(img)

        # window
        d.rounded_rectangle([0, 0, self.w - 1, self.h - 1], RADIUS, fill=INSET, outline=LINE, width=SCALE)
        d.rounded_rectangle([0, 0, self.w - 1, CHROME_H], RADIUS, fill=RAISED)
        d.rectangle([0, CHROME_H - SCALE, self.w, CHROME_H], fill=LINE)

        # three dots, brand-tinted rather than macOS traffic lights
        cy = CHROME_H // 2
        for i, col in enumerate((FAINT, FAINT, ACCENT)):
            cx = PAD + i * 13 * SCALE
            r = 4 * SCALE
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)

        tw = self.bold.getlength(self.title)
        d.text(((self.w - tw) / 2, cy - FONT_PX * 0.62), self.title, font=self.bold, fill=MUTED)

        # body — only the last `rows` lines are visible (a real terminal scrolls)
        visible = lines[-self.rows:]
        y = CHROME_H + PAD
        for text, cls in visible:
            self._draw_line(d, PAD, y, text, cls)
            y += self.lh

        if cursor and visible:
            last_text, _ = visible[-1]
            x = PAD + self.cw * self._visible_len(last_text)
            ty = CHROME_H + PAD + self.lh * (len(visible) - 1)
            d.rectangle([x, ty, x + self.cw * 0.85, ty + FONT_PX * 1.05], fill=ACCENT)

        return img.resize((self.w // SCALE, self.h // SCALE), Image.LANCZOS)

    def _visible_len(self, text: str) -> int:
        """Length ignoring {cls}…{/cls} markers. Unknown tags count as text —
        a path parameter like {user_id} is content, not markup."""
        out, i = 0, 0
        while i < len(text):
            if text[i] == "{":
                j = text.find("}", i)
                if j != -1 and self._is_tag(text[i + 1 : j]):
                    i = j + 1
                    continue
            out += 1
            i += 1
        return out

    @staticmethod
    def _is_tag(body: str) -> bool:
        return body in PALETTE or (body.startswith("/") and body[1:] in PALETTE)

    def _draw_line(self, d: ImageDraw.ImageDraw, x: float, y: float, text: str, cls: str) -> None:
        """Draw a line, honouring inline {ok}…{/ok} spans."""
        base = PALETTE.get(cls, BODY)
        font = self.bold if cls == "cmd" else self.font
        if cls == "cmd":
            base = HEADING
        i, cur = 0, base
        stack: list[tuple[int, int, int]] = []
        while i < len(text):
            if text[i] == "{":
                j = text.find("}", i)
                tag = text[i + 1 : j] if j != -1 else ""
                if j != -1 and self._is_tag(tag):
                    if tag.startswith("/"):
                        cur = stack.pop() if stack else base
                    else:
                        stack.append(cur)
                        cur = PALETTE[tag]
                    i = j + 1
                    continue
                # not a colour tag — fall through and draw the brace literally
            d.text((x, y), text[i], font=font, fill=cur)
            x += self.cw
            i += 1


def build_frames(cast: dict, out: pathlib.Path) -> int:
    r = Renderer(cast["title"], cast.get("cols", 92), cast.get("rows", 24))
    frames = out / "frames"
    if frames.exists():
        shutil.rmtree(frames)
    frames.mkdir(parents=True)

    lines: list[tuple[str, str]] = []
    n = 0

    def emit(cursor: bool = True, count: int = 1) -> None:
        nonlocal n
        img = r.frame(lines, cursor)
        for _ in range(count):
            n += 1
            img.save(frames / f"f{n:05d}.png")

    emit(True, FPS // 2)  # a beat before anything happens

    for step in cast["steps"]:
        kind = step["type"]

        if kind == "cmd":
            prompt = step.get("prompt", "$ ")
            lines.append((f"{{ac}}{prompt}{{/ac}}", "cmd"))
            typed = ""
            for ch in step["text"]:
                typed += ch
                lines[-1] = (f"{{ac}}{prompt}{{/ac}}{typed}", "cmd")
                # ~28 chars/sec: fast enough not to bore, slow enough to read
                emit(True, 1 if len(step["text"]) > 30 else 2)
            emit(True, int(FPS * step.get("pause", 0.5)))

        elif kind == "out":
            for raw in step["lines"]:
                lines.append((raw, step.get("cls", "")))
                emit(False, max(1, int(FPS * step.get("speed", 0.06))))
            emit(False, int(FPS * step.get("pause", 0.8)))

        elif kind == "blank":
            lines.append(("", ""))
            emit(False, 1)

        elif kind == "hold":
            emit(step.get("cursor", True), int(FPS * step["seconds"]))

        elif kind == "clear":
            lines = []
            emit(True, int(FPS * 0.2))

    emit(True, int(FPS * 1.6))  # let the last frame breathe
    return n


def encode(out: pathlib.Path, name: str, n: int) -> None:
    frames = out / "frames" / "f%05d.png"

    mp4 = out / f"{name}.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "slow", "-crf", "20",
         # even dimensions are required by yuv420p
         "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "-movflags", "+faststart", str(mp4)],
        check=True,
    )

    # Two-pass GIF: a per-clip palette is the difference between crisp text and
    # dithered mush.
    pal = out / "palette.png"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames),
         "-vf", "palettegen=max_colors=128:stats_mode=diff", str(pal)],
        check=True,
    )
    gif = out / f"{name}.gif"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames),
         "-i", str(pal), "-lavfi", "paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle",
         "-loop", "0", str(gif)],
        check=True,
    )
    pal.unlink(missing_ok=True)
    shutil.rmtree(out / "frames")

    print(f"   {name}.mp4  {mp4.stat().st_size // 1024}KB")
    print(f"   {name}.gif  {gif.stat().st_size // 1024}KB   ({n} frames, {n / FPS:.1f}s)")


if __name__ == "__main__":
    cast = json.loads(pathlib.Path(sys.argv[1]).read_text())
    out = pathlib.Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    count = build_frames(cast, out)
    encode(out, cast["name"], count)
