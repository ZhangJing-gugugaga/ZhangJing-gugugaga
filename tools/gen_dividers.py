"""divider-{rpd,lexinote,termify}.svg — 1300x44.
lemomo-style light sweep between two clipped segments, center pixel diamond
stepping rotation (steps(4) = true 8-bit feel), blinking end squares.
Accent color carries the project identity.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from palette import AMBER, CYAN, PINK, FAINT
from svgkit import SVG, sweep_bar
import pixelfont as pf

W, H = 1300, 44
MID = W // 2

def divider(accent, name):
    s = SVG(W, H, f"{name} 章节分隔线")
    # base line split by center motif
    s.add(f'<rect x="60" y="20.5" width="{MID-70-20}" height="3" fill="{FAINT}"/>')
    s.add(f'<rect x="{MID+70+20}" y="20.5" width="{W-MID-70-40}" height="3" fill="{FAINT}"/>')
    # light sweep (clip both segments)
    sweep_bar(s, 19, 6, W, accent, MID-70, MID+70)
    # center diamond, stepped rotation (8-bit)
    s.style(
        ".stp{transform-box:fill-box;transform-origin:center;"
        "animation:stp 3.2s steps(4) infinite}"
        "@keyframes stp{from{transform:rotate(0)}to{transform:rotate(360deg)}}"
    )
    import pixelfont as pf
    els, dw, dh = pf.text(MID-10, 10, "◆", 4, accent)
    s.add(f'<g class="stp">{els}</g>')
    # blinking end caps (alternating phases)
    s.use_blink(); s.style(".bl2{animation-delay:.5s}")
    s.add(f'<rect class="bl" x="60" y="18" width="14" height="8" fill="{accent}"/>')
    s.add(f'<rect class="bl2" x="{W-74}" y="18" width="14" height="8" fill="{accent}"/>')
    n = s.save(pathlib.Path(__file__).parent.parent / "assets" / f"divider-{name}.svg")
    print(f"divider-{name}.svg", n, "bytes")

divider(AMBER, "rpd")
divider(CYAN, "lexinote")
divider(PINK, "termify")
