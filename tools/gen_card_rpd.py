"""card-rpd.svg — 1300x360. RPD-Skill showcase: 51★ real stat, three entry
doors (level-select metaphor), staggered rise, one blinking ▶.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from palette import AMBER, TEXT, DIM, FAINT, PANEL2
from svgkit import SVG, pixel_frame
import pixelfont as pf

W, H = 1300, 360
s = SVG(W, H, "RPD-Skill 项目卡：三个入口覆盖项目全生命周期")
pixel_frame(s, AMBER)
s.use_blink(); s.use_rise(); s.use_breathe(dur="3.4s", lo=".7")

def txt(x, y, t, cell, color, shadow=None, cls=None, delay=None):
    els, w, h = pf.text(x, y, t, cell, color, shadow)
    if cls:
        s.add(f'<g class="{cls}">{els}</g>')
    else:
        s.add(els)
    return w, h

# left column
txt(60, 46, "RPD-SKILL", 6, AMBER, shadow="#241C06")
txt(60, 112, "三个入口覆盖项目全生命周期，", 2, TEXT)
txt(60, 140, "让 vibecoding 项目真正落地。", 2, TEXT)
txt(60, 172, "THREE ENTRIES · FULL PROJECT LIFECYCLE", 2, DIM)

# honest stat — '51' in arcade digits, star via CJK font (real five-point)
stat_cls = "br"
els, sw, sh = pf.text(60, 222, "51", 6, AMBER, shadow="#241C06")
s.add(f'<g class="{stat_cls}">{els}</g>')
els, stw, sth = pf.text(60 + sw + 12, 222, "★", 6, AMBER, cjk_cells=10)
s.add(f'<g class="{stat_cls}">{els}</g>')
txt(60, 288, "GITHUB STARS AND COUNTING", 2, DIM)

# right: three entry doors (level select)
doors = [("01", 720), ("02", 905), ("03", 1090)]
for i, (num, dx) in enumerate(doors):
    s.style(f".d{i}{{animation:rs .7s cubic-bezier(.2,.7,.3,1) {0.15*i:.2f}s both}}")
    s.add(
        f'<g class="d{i}"><rect x="{dx}" y="64" width="160" height="180" fill="{PANEL2}" '
        f'stroke="{FAINT}" stroke-width="2"/>'
    )
    nw, nh = pf.measure(num, 4)
    els, _, _ = pf.text(dx + (160 - nw) // 2, 100, num, 4, AMBER)
    s.add(els)
    ew, eh = pf.measure("ENTRY", 2)
    els, _, _ = pf.text(dx + (160 - ew) // 2, 190, "ENTRY", 2, DIM)
    s.add(els)
    s.add("</g>")
# blinking ▶ marker on middle door
els, _, _ = pf.text(905 + 160 - 30, 74, "▶", 2, AMBER)
s.add(f'<g class="bl">{els}</g>')
txt(720, 276, "同一套 skill，随项目阶段任选入口。", 2, DIM)

n = s.save(pathlib.Path(__file__).parent.parent / "assets" / "card-rpd.svg")
print("card-rpd.svg", n, "bytes")
