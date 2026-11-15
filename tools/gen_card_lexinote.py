"""card-lexinote.svg — 1300x360. LexiNote showcase: local-first HarmonyOS
notes app. Pixel phone mockup with markdown lines + knowledge-graph nodes
twinkling (feature-accurate: 双向链接/关系图谱). Feature chips staggered.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from palette import CYAN, TEXT, DIM, FAINT, PANEL, PANEL2, GREEN
from svgkit import SVG, pixel_frame
import pixelfont as pf

W, H = 1300, 360
s = SVG(W, H, "LexiNote 项目卡：本地优先的鸿蒙笔记应用")
pixel_frame(s, CYAN)
s.use_blink(); s.use_rise(); s.use_twinkle(dur="2.6s")

def txt(x, y, t, cell, color, shadow=None, cls=None):
    els, w, h = pf.text(x, y, t, cell, color, shadow)
    s.add(f'<g class="{cls}">{els}</g>' if cls else els)
    return w, h

# left column
txt(60, 46, "LEXINOTE", 6, CYAN, shadow="#0A2028")
txt(60, 112, "本地优先的鸿蒙 Markdown 笔记，", 2, TEXT)
txt(60, 140, "数据全程留在设备上。", 2, TEXT)
txt(60, 172, "LOCAL-FIRST NOTES FOR HARMONYOS", 2, DIM)

# feature chips
chips = ["MARKDOWN", "双向链接", "思维导图", "本地数据"]
cx = 60
for i, c in enumerate(chips):
    cw, _ = pf.measure(c, 2)
    pad = 14
    s.style(f".p{i}{{animation:rs .6s cubic-bezier(.2,.7,.3,1) {0.35+0.12*i:.2f}s both}}")
    s.add(
        f'<g class="p{i}"><rect x="{cx}" y="222" width="{cw+2*pad}" height="40" '
        f'fill="{PANEL2}" stroke="{FAINT}" stroke-width="2"/>'
    )
    els, _, _ = pf.text(cx + pad, 232, c, 2, CYAN if c[0].isascii() else TEXT)
    s.add(els + "</g>")
    cx += cw + 2 * pad + 16

txt(60, 300, "ARKTS · ARKUI · MULTI-DEVICE", 2, DIM)

# right: pixel phone mockup
px, py, pw, ph = 950, 40, 240, 288
s.style(".phone{animation:rs .8s cubic-bezier(.2,.7,.3,1) .1s both}")
phone = [
    f'<g class="phone"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="{PANEL}" '
    f'stroke="{FAINT}" stroke-width="3"/>',
    f'<rect x="{px+pw//2-24}" y="{py+8}" width="48" height="6" fill="{FAINT}"/>',  # speaker
]
sx, sy, sw_, sh_ = px + 12, py + 24, pw - 24, ph - 48
phone.append(f'<rect x="{sx}" y="{sy}" width="{sw_}" height="{sh_}" fill="#0B0F14" stroke="{FAINT}" stroke-width="2"/>')
# note title
phone.append(f'<rect x="{sx+10}" y="{sy+14}" width="96" height="7" fill="{CYAN}"/>')
# markdown body lines
line_ws = [150, 176, 128, 160, 104, 168, 132]
for i, lw in enumerate(line_ws):
    yy = sy + 34 + i * 12
    phone.append(f'<rect x="{sx+10}" y="{yy}" width="{lw}" height="4" fill="#3E4C5E"/>')
# blinking cursor on line 4
phone.append(f'<rect class="bl" x="{sx+10+104}" y="{sy+34+3*12-2}" width="6" height="8" fill="{CYAN}"/>')
# code block
phone.append(f'<rect x="{sx+10}" y="{sy+122}" width="{sw_-20}" height="22" fill="{PANEL2}"/>')
phone.append(f'<rect x="{sx+18}" y="{sy+130}" width="120" height="4" fill="{GREEN}"/>')
# knowledge graph: 5 nodes + edges
nodes = [(1052, 288), (1096, 272), (1130, 296), (1076, 304), (1114, 318)]
edges = [(0, 1), (1, 2), (1, 3), (2, 4), (3, 4)]
for a, b in edges:
    ax, ay = nodes[a]; bx, by = nodes[b]
    phone.append(f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="{FAINT}" stroke-width="2"/>')
for i, (nx, ny) in enumerate(nodes):
    phone.append(f'<rect class="tw t{i}" x="{nx-4}" y="{ny-4}" width="8" height="8" fill="{CYAN}"/>')
phone.append("</g>")
s.add("".join(phone))
s.style(".t0{animation-delay:0s}.t1{animation-delay:.5s}.t2{animation-delay:1s}"
        ".t3{animation-delay:1.5s}.t4{animation-delay:2s}")

n = s.save(pathlib.Path(__file__).parent.parent / "assets" / "card-lexinote.svg")
print("card-lexinote.svg", n, "bytes")
