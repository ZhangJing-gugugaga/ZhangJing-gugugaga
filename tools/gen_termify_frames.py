"""M4 — Termify turns a 2-frame GIF into the terminal's ASCII animation.

Frame A: star. Frame B: star scaled in with sparkle pixels. Both converted
by Termify itself (the bootstrap story: the terminal plays a Termify-made
animation). Outputs src/termify_star_f1.txt / f2.txt (equal size).
"""
import subprocess, sys, pathlib
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).parent
TERMIFY = HERE.parent.parent / "termify-scratch"


def make_gif(path):
    W, H = 64, 44
    frames = []
    for sparkle in (False, True):
        img = Image.new("L", (W, H), 255)
        d = ImageDraw.Draw(img)
        import math
        cx, cy, R, r2 = 32, 23, (15 if sparkle else 17), (6 if sparkle else 7)
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rad = R if i % 2 == 0 else r2
            pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
        d.polygon(pts, fill=40)
        if sparkle:
            for (sx, sy) in [(10, 8), (54, 10), (14, 34), (52, 32), (32, 4)]:
                d.rectangle([sx, sy, sx + 2, sy + 2], fill=120)
        frames.append(img)
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=600, loop=0)
    print("gif ok:", path)


def termify_ascii(gif_path, out_prefix):
    """Run Termify's engine on the GIF; dump each frame as plain text."""
    sys.path.insert(0, str(TERMIFY))
    # engine lives in the cloned repo; import fresh
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "termify_engine", TERMIFY / "termify" / "engine.py")
    # engine imports sibling modules; add repo root to path instead
    if str(TERMIFY) not in sys.path:
        sys.path.insert(0, str(TERMIFY))
    import termify.engine as eng
    r = eng.convert(str(gif_path), "ascii", width=46, height=16, color_mode="mono")
    frames = r.lines_per_frame
    outs = []
    for i, lines in enumerate(frames, 1):
        out = HERE / "src" / f"{out_prefix}_f{i}.txt"
        out.write_text("\n".join(lines), encoding="utf-8")
        outs.append(out)
        print(f"frame {i}: {len(lines)} lines -> {out.name}")
    assert len(frames) >= 2, "expected 2 frames from the GIF"
    # normalize: same width
    w1 = max(len(l) for l in frames[0]); w2 = max(len(l) for l in frames[1])
    print("frame widths:", w1, w2)
    return outs


gif = HERE / "src" / "_star2.gif"
make_gif(gif)
termify_ascii(gif, "termify_star")
