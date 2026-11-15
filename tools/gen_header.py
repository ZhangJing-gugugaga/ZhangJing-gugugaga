"""header.svg v3 — motion matrix: power-on flicker (one-shot), boot typing,
cursor blink, invader patrol + 2-frame walk cycle, star variety (twinkle /
float / meteor streak), CRT scanline. Layout unchanged (user loves it).
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from palette import AMBER, CYAN, PINK, TEXT, DIM, FAINT, GREEN
from svgkit import SVG, pixel_frame, star
import pixelfont as pf

W, H = 1300, 210
s = SVG(W, H, "ZJ — 程序员 · AI Agent 开发者")
pixel_frame(s, AMBER)
s.use_blink()
s.use_poweron()
s.use_patrol(90, dur="7s")
s.use_frameswap(dur="0.5s")
s.use_twinkle(dur="2.6s", delay="0s"); s.style(".t2{animation-delay:1.4s}")
s.use_float(dur="2.8s", dy=5, delay="0s")
s.use_scanline(travel=250, dur="7s", delay="3.5s")

s.add('<g class="pon">')  # CRT flicker-on wraps everything

# ---- typed title ----
title = "ZJ.DEV"
cell = 8
char_adv = cell * 6
tw = len(title) * char_adv
tx, ty = 60, 52
s.style("@keyframes ap{from{opacity:0}to{opacity:1}}")  # shared reveal keyframes
for i, ch in enumerate(title):
    els, _, _ = pf.text(tx + i * char_adv, ty, ch, cell, AMBER, shadow="#171F0B")
    s.style(f".c{i}{{animation:ap .01s steps(1) {0.25*i:.2f}s both}}")
    s.add(f'<g class="c{i}">{els}</g>')
s.add(f'<rect class="bl" x="{tx+tw+18}" y="{ty+8}" width="{cell*2}" height="{cell*7-8}" fill="{AMBER}"/>')

# ---- taglines ----
s.style(".fade{animation:ap .01s steps(1) 1.75s both}"
        ".fade2{animation:ap .01s steps(1) 1.95s both}")
els, _, _ = pf.text(62, 132, "程序员 · AI Agent 开发者", 2, TEXT, shadow="#0E1520")
s.add(f'<g class="fade">{els}</g>')
els, _, _ = pf.text(62, 166, "PROGRAMMER · AGENT BUILDER · OPEN SOURCE", 2, DIM)
s.add(f'<g class="fade2">{els}</g>')

# ---- hi-score ----
hi_x = W - 60 - (pf.measure("HI-SCORE", 2)[0] + 12 + pf.measure("51", 2)[0] + 14)
els, _, _ = pf.text(hi_x, 26, "HI-SCORE", 2, DIM)
s.add(els)
els, fw, _ = pf.text(hi_x, 44, "51", 2, AMBER)
s.add(els)
els, _, _ = pf.text(hi_x + fw + 4, 44, "★", 2, AMBER, cjk_cells=10)
s.add(els)

# ---- invader: patrols right field, 2-frame walk ----
INV_A = [
    "00100000100", "00010001000", "00111111100", "01101110110",
    "11111111111", "10111111101", "10100000101", "00011011000",
]
INV_B = [
    "00100000100", "00010001000", "00111111100", "01101110110",
    "11111111111", "10111111101", "01000001010", "00110110100",
]
icell, ix0, iy0 = 3, 930, 92
def inv(rows):
    return "".join(
        f'<rect x="{ix0 + x*icell}" y="{iy0 + y*icell}" width="{icell}" height="{icell}" fill="{GREEN}"/>'
        for y, row in enumerate(rows) for x, c in enumerate(row) if c == "1")
s.add(f'<g class="pt"><g class="fa">{inv(INV_A)}</g><g class="fb" opacity="0">{inv(INV_B)}</g></g>')

# ---- star field: three different behaviors ----
star(s, 1040, 66, 9, AMBER, cls="tw")
star(s, 1150, 128, 7, CYAN, cls="flt t2")
star(s, 1075, 168, 5, PINK, cls="tw")

# ---- meteor streak (rare, diagonal) ----
s.style(".mt{animation:mtk 9s linear infinite}"
        "@keyframes mtk{0%,78%{opacity:0;transform:translate(0,0)}"
        "80%{opacity:.9}90%{opacity:.9;transform:translate(240px,86px)}"
        "92%,100%{opacity:0;transform:translate(264px,94px)}}")
s.add('<g class="mt" opacity="0"><rect x="1020" y="52" width="26" height="3" fill="#FFC0D9"/>'
      f'<rect x="1046" y="55" width="4" height="4" fill="{PINK}"/></g>')

s.add("</g>")  # end pon

# ---- CRT scanline band on top (hidden entirely when animations are off) ----
s.style("@media (prefers-reduced-motion: reduce){.scn{opacity:0!important}}")
s.add(f'<rect class="scn" x="10" y="0" width="{W-20}" height="24" fill="#FFFFFF" opacity="0.05"/>')

n = s.save(pathlib.Path(__file__).parent.parent / "assets" / "header.svg")
print("header.svg", n, "bytes")
