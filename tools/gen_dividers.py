"""dividers v3 — same height/frame language, three distinct center behaviors:
rpd      = light sweep + stepped-rotate diamond (kept, the family baseline)
lexinote = echo sweep (double pulse) + scale-pulse diamond
termify  = terminal marquee marching left + glitch-jitter diamond
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from palette import AMBER, CYAN, PINK, FAINT, DIM
from svgkit import SVG, sweep_bar
import pixelfont as pf

W, H = 1300, 44
MID = W // 2

def base_line(accent):
    s = SVG(W, H, "章节分隔线")
    s.add(f'<rect x="60" y="20.5" width="{MID-70-20}" height="3" fill="{FAINT}"/>')
    s.add(f'<rect x="{MID+70+20}" y="20.5" width="{W-MID-70-40}" height="3" fill="{FAINT}"/>')
    s.use_sweep()  # defines .sw class + @keyframes sw — sweep_bar only draws rects
    sweep_bar(s, 19, 6, W, accent, MID-70, MID+70)
    s.use_blink(); s.style(".bl2{animation-delay:.5s}")
    s.add(f'<rect class="bl" x="60" y="18" width="14" height="8" fill="{accent}"/>')
    s.add(f'<rect class="bl2" x="{W-74}" y="18" width="14" height="8" fill="{accent}"/>')
    return s

def save(s, name):
    n = s.save(pathlib.Path(__file__).parent.parent / "assets" / f"divider-{name}.svg")
    print(f"divider-{name}.svg", n, "bytes")

# ---- rpd: baseline (sweep + stepped rotate) ----
s = base_line(AMBER)
s.style(".stp{transform-box:fill-box;transform-origin:center;"
        "animation:stp 3.2s steps(4) infinite}"
        "@keyframes stp{from{transform:rotate(0)}to{transform:rotate(360deg)}}")
els, _, _ = pf.text(MID-10, 10, "◆", 4, AMBER)
s.add(f'<g class="stp">{els}</g>')
save(s, "rpd")

# ---- lexinote: echo sweep + pulsing diamond ----
s = base_line(CYAN)
s.use_echo(dur="3.6s", delay="1.2s", opacity=".35")
s.add(f'<rect class="echo" x="-320" y="20" width="320" height="4" fill="url(#swg)" '
      f'clip-path="url(#swc)"/>')
s.use_twinkle(dur="2.2s")
els, _, _ = pf.text(MID-10, 10, "◆", 4, CYAN)
s.add(f'<g class="tw">{els}</g>')
save(s, "lexinote")

# ---- termify: cursor comet train + glitch diamond ----
s = base_line(PINK)
# comet: 3 shrinking blocks crossing the clipped segments (reuse sweep clip)
s.style(".comet{animation:cmt 2.8s steps(12,end) infinite}"
        "@keyframes cmt{from{transform:translateX(0)}to{transform:translateX(1300px)}}")
s.add(
    '<g clip-path="url(#swc)"><g class="comet">'
    f'<rect x="-40" y="18" width="10" height="8" fill="{PINK}"/>'
    f'<rect x="-52" y="19" width="8" height="6" fill="{PINK}" opacity=".55"/>'
    f'<rect x="-61" y="20" width="6" height="4" fill="{PINK}" opacity=".28"/>'
    "</g></g>"
)
s.use_glitch(amp=2, dur="0.44s")
els, _, _ = pf.text(MID-10, 10, "◆", 4, PINK)
s.add(f'<g class="gl">{els}</g>')
save(s, "termify")
