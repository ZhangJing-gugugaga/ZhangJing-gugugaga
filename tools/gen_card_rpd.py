"""card-rpd v3 — layout: left text / right doors (kept). Motion: level-select
cursor cycling across doors with synced door highlight, lifecycle progress bar
filling in steps, Agensi Skill label, staggered door rise.
"""
import sys, pathlib
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from palette import AMBER, TEXT, DIM, FAINT, PANEL2
from svgkit import SVG, pixel_frame
import pixelfont as pf

W, H = 1300, 360
s = SVG(W, H, "RPD-Skill 项目卡：三个入口覆盖项目全生命周期")
pixel_frame(s, AMBER)
s.use_blink(); s.use_rise(); s.use_breathe(dur="3.4s", lo=".7")
s.use_cursor_cycle([0, 185, 370], period="6.6s")
s.use_fillbar(520, dur="3.6s")

def txt(x, y, t, cell, color, shadow=None, cls=None):
    els, w, h = pf.text(x, y, t, cell, color, shadow)
    s.add(f'<g class="{cls}">{els}</g>' if cls else els)
    return w, h

# left column
txt(60, 46, "RPD-SKILL", 6, AMBER, shadow="#241C06")
txt(60, 112, "三个入口覆盖项目全生命周期，", 2, TEXT)
txt(60, 140, "让 vibecoding 项目真正落地。", 2, TEXT)
txt(60, 172, "THREE ENTRIES · FULL PROJECT LIFECYCLE", 2, DIM)

txt(60, 232, "Agensi Skill", 4, AMBER, shadow="#241C06")
txt(60, 288, "PROJECT WORKFLOW", 2, DIM)

# right: doors + cycling level-select cursor
doors = [("01", 720), ("02", 905), ("03", 1090)]
for i, (num, dx) in enumerate(doors):
    s.style(f".d{i}{{animation:rs .7s cubic-bezier(.2,.7,.3,1) {0.15*i:.2f}s both}}")
    s.add(
        f'<g class="d{i}"><rect x="{dx}" y="64" width="160" height="180" fill="{PANEL2}" '
        f'stroke="{FAINT}" stroke-width="2"/>'
    )
    nw, _ = pf.measure(num, 4)
    els, _, _ = pf.text(dx + (160 - nw) // 2, 100, num, 4, AMBER)
    s.add(els)
    ew, _ = pf.measure("ENTRY", 2)
    els, _, _ = pf.text(dx + (160 - ew) // 2, 190, "ENTRY", 2, DIM)
    s.add(els)
    s.add("</g>")
    # synced highlight overlay
    s.phase_visibility(f"h{i}", "6.6s", i, 3)
    s.add(f'<rect class="h{i}" x="{dx}" y="64" width="160" height="180" '
          f'fill="none" stroke="{AMBER}" stroke-width="3" opacity="0"/>')
# cycling cursor above door centers
els, _, _ = pf.text(795, 44, "▶", 2, AMBER)
s.add(f'<g class="cyc">{els}</g>')

txt(720, 262, "同一套 skill，随项目阶段任选入口。", 2, DIM)
txt(720, 288, "PROJECT LIFECYCLE", 2, DIM)
s.add(f'<rect x="720" y="306" width="520" height="8" fill="{FAINT}"/>')
s.add(f'<rect class="flb" x="720" y="306" width="520" height="8" fill="{AMBER}"/>')

n = s.save(pathlib.Path(__file__).parent.parent / "assets" / "card-rpd.svg")
print("card-rpd.svg", n, "bytes")
