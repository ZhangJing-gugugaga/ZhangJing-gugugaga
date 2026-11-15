"""footer.svg — 1300x170. Thanks line, bilingual; arcade CONTINUE prompt.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from palette import GREEN, TEXT, DIM, AMBER
from svgkit import SVG, pixel_frame, star
import pixelfont as pf

W, H = 1300, 170
s = SVG(W, H, "如果这些项目帮到了你，一颗 star 就是最大的鼓励")
pixel_frame(s, GREEN)

zh = "如果这些项目帮到了你，一颗 star 就是最大的鼓励。"
els, zw, _ = pf.text((W-zw)//2 if (zw:=pf.measure(zh,2)[0]) else 0, 0, "", 2, TEXT)  # guard
zw = pf.measure(zh, 2)[0]
els, _, _ = pf.text((W-zw)//2, 42, zh, 2, TEXT)
s.add(els)

en = "IF ANY OF THESE HELP YOU, A STAR MEANS A LOT. THANKS FOR STOPPING BY."
ew = pf.measure(en, 2)[0]
els, _, _ = pf.text((W-ew)//2, 82, en, 2, DIM)
s.add(els)

# CONTINUE prompt with blinking ▶ and flanking diamonds
s.use_blink(); s.use_twinkle(dur="2.6s")
prompt = "CONTINUE"
pw = pf.measure(prompt + " ▶", 2)[0]
px = (W-pw)//2
els, _, _ = pf.text(px, 124, prompt, 2, GREEN)
s.add(els)
els, _, _ = pf.text(px+pw-12, 124, "▶", 2, GREEN)
s.add(f'<g class="bl">{els}</g>')
star(s, px-30, 130, 6, AMBER, cls="tw")
star(s, px+pw+34, 130, 6, AMBER, cls="tw")

n = s.save(pathlib.Path(__file__).parent.parent / "assets" / "footer.svg")
print("footer.svg", n, "bytes")
