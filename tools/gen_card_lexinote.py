"""card-lexinote v3 — layout MIRRORED (phone left / text right) for variety.
Motion: note title types on + cursor, graph edges self-draw (知识连接 made
literal), nodes float with phases, one active node blinks, SAVED flash.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from palette import CYAN, TEXT, DIM, FAINT, PANEL, PANEL2, GREEN
from svgkit import SVG, pixel_frame
import pixelfont as pf

W, H = 1300, 360
s = SVG(W, H, "LexiNote 项目卡：本地优先的鸿蒙笔记应用")
pixel_frame(s, CYAN)
s.use_blink(); s.use_rise()
s.use_float(dur="2.8s", dy=4, delay="0s")

def txt(x, y, t, cell, color, shadow=None, cls=None):
    els, w, h = pf.text(x, y, t, cell, color, shadow)
    s.add(f'<g class="{cls}">{els}</g>' if cls else els)
    return w, h

# ---- phone mockup (LEFT) ----
px, py, pw, ph = 60, 40, 240, 288
s.style(".phone{animation:rs .8s cubic-bezier(.2,.7,.3,1) .1s both}")
sx, sy, sw_, sh_ = px + 12, py + 24, pw - 24, ph - 48
phone = [
    f'<g class="phone"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="{PANEL}" '
    f'stroke="{FAINT}" stroke-width="3"/>',
    f'<rect x="{px+pw//2-24}" y="{py+8}" width="48" height="6" fill="{FAINT}"/>',
    f'<rect x="{sx}" y="{sy}" width="{sw_}" height="{sh_}" fill="#0B0F14" stroke="{FAINT}" stroke-width="2"/>',
]
# note title types on, cursor blinks after
phone.append(f'<rect class="tpw" x="{sx+10}" y="{sy+14}" width="96" height="7" fill="{CYAN}"/>')
s.style(".tpw{animation:tpw 1.1s steps(8) .5s both}@keyframes tpw{from{width:0}}")
phone.append(f'<rect class="bl" x="{sx+108}" y="{sy+13}" width="6" height="8" fill="{CYAN}"/>')
# markdown body lines (static — reading content)
for i, lw in enumerate([150, 176, 128, 160, 104, 168, 132]):
    yy = sy + 34 + i * 12
    phone.append(f'<rect x="{sx+10}" y="{yy}" width="{lw}" height="4" fill="#3E4C5E"/>')
# code block
phone.append(f'<rect x="{sx+10}" y="{sy+122}" width="{sw_-20}" height="22" fill="{PANEL2}"/>')
phone.append(f'<rect x="{sx+18}" y="{sy+130}" width="120" height="4" fill="{GREEN}"/>')
# knowledge graph: nodes float, edges self-draw, one active node blinks
nodes = [(92, 228), (136, 212), (170, 236), (116, 244), (154, 258)]
nodes = [(px + dx, py + dy - 40) for (dx, dy) in nodes]  # keep inside screen
edges = [(0, 1), (1, 2), (1, 3), (2, 4), (3, 4)]
for k, (a, b) in enumerate(edges):
    (ax, ay), (bx, by) = nodes[a], nodes[b]
    ln = ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5
    s.style(f".dw{k}{{animation:dw{k}k .5s ease-out {0.9+0.12*k:.2f}s both}}"
            f"@keyframes dw{k}k{{from{{stroke-dashoffset:{ln:.0f}}}}}")
    phone.append(f'<line class="dw{k}" x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" '
                 f'stroke="{FAINT}" stroke-width="2" stroke-dasharray="{ln:.0f}"/>')
for i, (nx, ny) in enumerate(nodes):
    cls = "flt t" + str(i) if i != 1 else "bl"
    phone.append(f'<rect class="{cls}" x="{nx-4}" y="{ny-4}" width="8" height="8" fill="{CYAN}"/>')
s.style(".t0{animation-delay:0s}.t1{animation-delay:.7s}.t2{animation-delay:1.4s}"
        ".t3{animation-delay:2.1s}")
# SAVED flash (bottom-right of screen)
svx, svy = sx + sw_ - 66, sy + sh_ - 18
phone.append(f'<rect class="sv" x="{svx-12}" y="{svy+1}" width="5" height="5" fill="{GREEN}"/>')
phone.append("</g>")
s.add("".join(phone))
s.style('.sv{animation:svk 4.5s steps(1,end) infinite}'
        '@keyframes svk{0%,9%{opacity:1}10%,100%{opacity:0}}')
els, _, _ = pf.text(svx - 2, svy, "SAVED", 2, GREEN)
# wrap in .sv too — rebuild as group
s.add(f'<g class="sv">{els}</g>')

# ---- text column (RIGHT) ----
txt(360, 46, "LEXINOTE", 6, CYAN, shadow="#0A2028")
txt(360, 112, "本地优先的鸿蒙 Markdown 笔记，", 2, TEXT)
txt(360, 140, "数据全程留在设备上。", 2, TEXT)
txt(360, 172, "LOCAL-FIRST NOTES FOR HARMONYOS", 2, DIM)

chips = ["MARKDOWN", "双向链接", "思维导图", "本地数据"]
cx = 360
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

txt(360, 300, "ARKTS · ARKUI · MULTI-DEVICE", 2, DIM)

n = s.save(pathlib.Path(__file__).parent.parent / "assets" / "card-lexinote.svg")
print("card-lexinote.svg", n, "bytes")
