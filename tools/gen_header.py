"""header.svg — 1300x210. Arcade boot screen: ZJ.DEV types itself in,
cursor blinks forever, three stars twinkle, bilingual tagline fades in.
One bold move = the boot typing; everything else quiet.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from palette import BG, AMBER, CYAN, PINK, TEXT, DIM, FAINT, GREEN
from svgkit import SVG, pixel_frame, star
import pixelfont as pf

W, H = 1300, 210
s = SVG(W, H, "ZJ — 程序员 · AI Agent 开发者")
pixel_frame(s, AMBER)

# ---- typed title "ZJ.DEV" (per-char stepped reveal, fails visible) ----
title = "ZJ.DEV"
cell = 8
char_adv = cell * (5 + 1)          # glyph advance = 6 cells
tw = len(title) * char_adv
tx, ty = 60, 52
s.use_blink()                       # .bl
for i, ch in enumerate(title):
    els, cw, chh = pf.text(tx + i * char_adv, ty, ch, cell, AMBER, shadow="#171F0B")
    s.style(
        f".c{i}{{animation:ap .01s steps(1) {0.25*i:.2f}s both}}"
        "@keyframes ap{from{opacity:0}to{opacity:1}}"
    )
    s.add(f'<g class="c{i}">{els}</g>')
# cursor block after title
s.add(f'<rect class="bl" x="{tx+tw+18}" y="{ty+8}" width="{cell*2}" height="{cell*7-8}" fill="{AMBER}"/>')

# ---- taglines (fade in after boot) ----
s.style(".fade{animation:ap 0.01s steps(1) 1.75s both}")
s.style(".fade2{animation:ap 0.01s steps(1) 1.95s both}")
zh = "程序员 · AI Agent 开发者"
els, zw, zh_h = pf.text(62, 132, zh, 2, TEXT, shadow="#0E1520")
s.add(f'<g class="fade">{els}</g>')
en = "PROGRAMMER · AGENT BUILDER · OPEN SOURCE"
els, ew, eh = pf.text(62, 166, en, 2, DIM)
s.add(f'<g class="fade2">{els}</g>')

# ---- hi-score badge (honest: RPD-Skill 51 stars) ----
hi_x = W - 60 - (pf.measure("HI-SCORE", 2)[0] + 12 + pf.measure("51", 2)[0] + 14)
els, _, _ = pf.text(hi_x, 26, "HI-SCORE", 2, DIM)
s.add(els)
els, fw, _ = pf.text(hi_x, 44, "51", 2, AMBER)
s.add(els)
els, _, _ = pf.text(hi_x + fw + 4, 44, "★", 2, AMBER, cjk_cells=10)
s.add(els)

# ---- three twinkling stars, right field ----
s.use_twinkle(dur="2.6s", delay="0s"); s.style(".t2{animation-delay:.9s}.t3{animation-delay:1.7s}")
star(s, 1040, 66, 9, AMBER, cls="tw")
star(s, 1140, 118, 7, CYAN, cls="tw t2")
star(s, 1075, 160, 5, PINK, cls="tw t3")

# ---- tiny invader, bobbing (steps = 8-bit movement) ----
s.style(".bob{animation:bob 0.8s steps(2,end) infinite alternate}"
        "@keyframes bob{from{transform:translateY(0)}to{transform:translateY(4px)}}")
INVADER = [
    "00100000100",
    "00010001000",
    "00111111100",
    "01101110110",
    "11111111111",
    "10111111101",
    "10100000101",
    "00011011000",
]
ic, ix, iy, icell = GREEN, 930, 96, 3
inv = "".join(
    f'<rect x="{ix + x * icell}" y="{iy + y * icell}" width="{icell}" height="{icell}" fill="{ic}"/>'
    for y, row in enumerate(INVADER)
    for x, c in enumerate(row)
    if c == "1"
)
s.add(f'<g class="bob">{inv}</g>')

n = s.save(pathlib.Path(__file__).parent.parent / "assets" / "header.svg")
print("header.svg", n, "bytes")
