"""T0 placeholder assets — pixel-arcade loading panels.

Generates all 8 SVGs referenced by README.md so the live profile shows
intentional dark panels instead of broken images. Replaced by real assets in T2.
Zero <text> elements; zero external references; CSS blink only + reduced-motion.
"""
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"

W, H = 1300, 0  # width shared; height per asset
DEFS = """<defs>
  <style>
    .bl{animation:bl 1s steps(2,end) infinite}
    .bl2{animation:bl 1s steps(2,end) infinite;animation-delay:.5s}
    @keyframes bl{0%,49%{opacity:1}50%,100%{opacity:.15}}
    @media (prefers-reduced-motion: reduce){*{animation:none!important}}
  </style>
</defs>"""

BG = "#0B0F14"
PANEL = "#111827"
AMBER = "#FFD447"
GREEN = "#4ADE80"
PINK = "#FF5FA2"
CYAN = "#6EE7FF"
FAINT = "#1F2A38"


def frame(w, h, border=AMBER):
    """Pixel double-border frame."""
    return (
        f'<rect x="0" y="0" width="{w}" height="{h}" fill="{BG}"/>'
        f'<rect x="6" y="6" width="{w-12}" height="{h-12}" fill="none" stroke="{border}" stroke-width="3"/>'
        f'<rect x="14" y="14" width="{w-28}" height="{h-28}" fill="none" stroke="{FAINT}" stroke-width="2"/>'
    )


def corner_sq(x, y, c, s=10):
    return f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{c}"/>'


def blocks(x, y, seq, s=12, gap=4):
    """A row of small squares = pseudo pixel-text."""
    out = []
    for i, c in enumerate(seq):
        if c != " ":
            out.append(corner_sq(x + i * (s + gap), y, c, s))
    return "".join(out)


def svg(w, h, body, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-labelledby="t"><title id="t">{label}</title>{DEFS}{body}</svg>'
    )


def loading_panel(w, h, accent):
    """Center: pixel blocks + blinking cursor block."""
    body = frame(w, h)
    cx, cy = w // 2, h // 2
    # pseudo word "LOADING" as blocks: 7 letters
    word = [1, 1, 1, 1, 1, 1, 1]
    x0 = cx - (len(word) * 16) // 2
    body += blocks(x0, cy - 6, [c for c in "ABCDEFG"[: len(word)]], s=10, gap=6)
    body += f'<rect class="bl" x="{cx + len(word) * 16 // 2 + 10}" y="{cy - 6}" width="10" height="10" fill="{accent}"/>'
    return svg(w, h, body, "loading")


assets = {
    "header.svg": (1300, 210, AMBER),
    "divider-rpd.svg": (1300, 44, AMBER),
    "divider-lexinote.svg": (1300, 44, CYAN),
    "divider-termify.svg": (1300, 44, PINK),
    "card-rpd.svg": (1300, 360, AMBER),
    "card-lexinote.svg": (1300, 360, CYAN),
    "card-termify.svg": (1300, 360, PINK),
    "footer.svg": (1300, 170, GREEN),
}

OUT.mkdir(exist_ok=True)
for name, (w, h, accent) in assets.items():
    if h == 44:  # divider: slim line + blinking end squares
        body = (
            f'<rect x="0" y="20.5" width="{w}" height="3" fill="{FAINT}"/>'
            f'<rect class="bl" x="60" y="18" width="14" height="8" fill="{accent}"/>'
            f'<rect class="bl2" x="{w-74}" y="18" width="14" height="8" fill="{accent}"/>'
        )
        content = svg(w, h, body, "section divider")
    else:
        content = loading_panel(w, h, accent)
    (OUT / name).write_text(content, encoding="utf-8")
    print(f"{name}: {len(content)}B")
