"""card-termify v3 — layout STACKED (title row + full-width terminal below):
a completely different composition from the other two cards.
Motion: the terminal plays a REAL 2-frame ASCII animation made by Termify
(frameswap), step chips highlight in sequence, typed export line, CRT
scanline inside the terminal, blink cursor.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from palette import PINK, TEXT, DIM, FAINT, PANEL, PANEL2, GREEN
from svgkit import SVG, pixel_frame
import pixelfont as pf

W, H = 1300, 360
s = SVG(W, H, "Termify 项目卡：万物皆可终端，终端动画由 Termify 生成")
pixel_frame(s, PINK)
s.use_blink(); s.use_rise()
s.use_frameswap(dur="1.2s", delay="1.35s")
s.use_scanline(travel=260, dur="6s")

def txt(x, y, t, cell, color, shadow=None, cls=None):
    els, w, h = pf.text(x, y, t, cell, color, shadow)
    s.add(f'<g class="{cls}">{els}</g>' if cls else els)
    return w, h

# ---- top row: title left, 3-step chips right ----
txt(60, 36, "TERMIFY", 6, PINK, shadow="#260A18")
txt(60, 78, "万物皆可终端。下面的 ASCII 动画由 Termify 生成。", 2, TEXT)
txt(60, 106, "GIF / IMAGE / VIDEO -> TERMINAL IN 3 STEPS", 2, DIM)

steps = ["1 UPLOAD", "2 PICK STYLE", "3 EXPORT"]
chip_specs = []
for c in steps:
    cw, _ = pf.measure(c, 2)
    chip_specs.append((c, cw + 28))
total = sum(w for _, w in chip_specs) + 16 * (len(steps) - 1)
cx = W - 60 - total
for i, (c, cw) in enumerate(chip_specs):
    s.style(f".p{i}{{animation:rs .6s cubic-bezier(.2,.7,.3,1) {0.2+0.12*i:.2f}s both}}")
    s.add(
        f'<g class="p{i}"><rect x="{cx}" y="40" width="{cw}" height="40" '
        f'fill="{PANEL2}" stroke="{FAINT}" stroke-width="2"/>'
    )
    els, _, _ = pf.text(cx + 14, 50, c, 2, PINK if i == 0 else TEXT)
    s.add(els + "</g>")
    s.phase_visibility(f"c{i}", "4.5s", i, 3)
    s.add(f'<rect class="c{i}" x="{cx}" y="40" width="{cw}" height="40" '
          f'fill="none" stroke="{PINK}" stroke-width="2" opacity="0"/>')
    cx += cw + 16

# ---- full-width terminal ----
tx, ty, tw_, th = 60, 128, 1180, 212
s.style(".term{animation:rs .8s cubic-bezier(.2,.7,.3,1) .1s both}")
term = [
    f'<g class="term"><rect x="{tx}" y="{ty}" width="{tw_}" height="{th}" fill="{PANEL}" '
    f'stroke="{FAINT}" stroke-width="3"/>',
    f'<rect x="{tx}" y="{ty}" width="{tw_}" height="28" fill="{PANEL2}"/>',
]
for i in range(3):
    term.append(f'<rect x="{tx+16+i*20}" y="{ty+10}" width="10" height="10" fill="{FAINT}"/>')
term.append(f'<rect x="{tx+80}" y="{ty+11}" width="140" height="6" fill="#3E4C5E"/>')
els, _, _ = pf.text(tx + 20, ty + 40, "$ termify star2.gif --charset ascii", 2, GREEN)
term.append(els)
s.add("".join(term))

# ASCII animation: two Termify frames, staggered reveal on frame A
src = pathlib.Path(__file__).parent / "src"
f1 = (src / "termify_star_f1.txt").read_text(encoding="utf-8").splitlines()
f2 = (src / "termify_star_f2.txt").read_text(encoding="utf-8").splitlines()
art_x, art_y = tx + 40, ty + 66
cw, chh = 6, 9
TONE = {"@": "t3", "#": "t2", "%": "t1"}
TONE_COLOR = {"t3": PINK, "t2": "#D06CA6", "t1": "#9B5F80", "t0": "#6E4459"}

def art_runs(line):
    runs = []; rx = None; cur = None
    for gx, c in enumerate(list(line) + [" "]):
        k = TONE[c] if c in TONE else ("t0" if c != " " else None)
        if k != cur:
            if rx is not None and gx > rx:
                runs.append((rx, gx, cur))
            rx = gx if k else None
            cur = k
    return runs

fa = []
for li, row in enumerate(f1):
    delay = 0.15 + li * 0.055
    s.style(f".a{li}{{animation:rs .4s cubic-bezier(.2,.7,.3,1) {delay:.2f}s both}}")
    seg = ""
    for rx0, rx1, kind in art_runs(row):
        seg += (f'<rect x="{art_x + rx0*cw}" y="{art_y + li*chh}" '
                f'width="{(rx1-rx0)*cw}" height="{chh-2}" fill="{TONE_COLOR[kind]}"/>')
    fa.append(f'<g class="a{li}">{seg}</g>')
s.add(f'<g class="fa">{"".join(fa)}</g>')

fb = []
for li, row in enumerate(f2):
    seg = ""
    for rx0, rx1, kind in art_runs(row):
        seg += (f'<rect x="{art_x + rx0*cw}" y="{art_y + li*chh}" '
                f'width="{(rx1-rx0)*cw}" height="{chh-2}" fill="{TONE_COLOR[kind]}"/>')
    fb.append(seg)
s.add(f'<g class="fb" opacity="0">{"".join(fb)}</g>')

# typed export line + cursor (after the animation settles)
s.style(".ex{animation:ap .01s steps(1) 2.3s both}"
        "@keyframes ap{from{opacity:0}to{opacity:1}}")
els, exw, _ = pf.text(tx + 20, ty + 178, "$ export star.gif --mp4  OK", 2, GREEN)
s.add(f'<g class="ex">{els}</g>')
s.add(f'<rect class="bl" x="{tx+20+exw+8}" y="{ty+179}" width="9" height="11" fill="{GREEN}"/>')

# CRT scanline clipped to terminal screen
s.defs(f'<clipPath id="tscr"><rect x="{tx+4}" y="{ty+4}" width="{tw_-8}" height="{th-8}"/></clipPath>')
s.add(f'<g clip-path="url(#tscr)">'
      f'<rect class="scn" x="{tx+4}" y="0" width="{tw_-8}" height="20" fill="#FFFFFF" opacity="0.05"/></g>')
s.add("</g>")  # end term

n = s.save(pathlib.Path(__file__).parent.parent / "assets" / "card-termify.svg")
print("card-termify.svg", n, "bytes")
