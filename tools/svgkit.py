"""svgkit — shared SVG document scaffolding for the pixel-arcade profile assets.

Every asset gets: proper viewBox, role/aria, one <title>, a single <style> block
with only the keyframes it actually uses, and the prefers-reduced-motion kill
switch. No external references, no <text>, no SMIL.
"""

MOTION_RESET = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


class SVG:
    def __init__(self, w, h, title):
        self.w, self.h, self.title = w, h, title
        self.styles = []   # css rules/keyframes
        self.defs = []     # gradients/clipPaths
        self.body = []     # drawable elements

    def style(self, css):
        self.styles.append(css)

    def defs(self, markup):
        self.defs.append(markup)

    def add(self, markup):
        self.body.append(markup)

    # ---- standard motion presets (tuned once, reused everywhere) ----
    def use_blink(self, dur="1s", delay="0s"):
        self.style(
            f".bl{{animation:bl {dur} steps(2,end) infinite;animation-delay:{delay}}}"
            "@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:.12}}"
        )

    def use_twinkle(self, dur="2.6s", delay="0s"):
        self.style(
            f".tw{{transform-box:fill-box;transform-origin:center;"
            f"animation:tw {dur} ease-in-out infinite;animation-delay:{delay}}}"
            "@keyframes tw{0%,100%{transform:scale(1) rotate(0)}"
            "45%{transform:scale(.55) rotate(45deg);opacity:.55}"
            "60%{transform:scale(1.18) rotate(90deg)}}"
        )

    def use_sweep(self, dist=1620, dur="4.5s", delay="0s"):
        self.style(
            f".sw{{animation:sw {dur} cubic-bezier(.45,0,.25,1) infinite;animation-delay:{delay}}}"
            f"@keyframes sw{{0%{{transform:translateX(0)}}70%,100%{{transform:translateX({dist}px)}}}}"
        )

    def use_rise(self, dur="0.7s", delay="0s", dy=14):
        """One-shot entrance: rise + fade. forwards fill; runs once on load."""
        self.style(
            f".rise{{animation:rs {dur} cubic-bezier(.2,.7,.3,1) {delay} both}}"
            f"@keyframes rs{{from{{transform:translateY({dy}px);opacity:0}}"
            f"to{{transform:translateY(0);opacity:1}}}}"
        )

    def use_typewriter(self, n_steps, dur="1.6s", delay="0s"):
        """One-shot stepped reveal via clipPath rect width. Arcade boot feel."""
        self.style(
            f".type{{animation:tp {dur} steps({n_steps}) {delay} both}}"
            f"@keyframes tp{{from{{width:0}}to{{width:100%}}}}"
        )

    def use_breathe(self, dur="3s", delay="0s", lo=".35", hi="1"):
        self.style(
            f".br{{animation:br {dur} ease-in-out infinite;animation-delay:{delay}}}"
            f"@keyframes br{{0%,100%{{opacity:{hi}}}50%{{opacity:{lo}}}}}"
        )

    def render(self):
        css = "\n".join(self.styles) + "\n" + MOTION_RESET
        defs = "".join(self.defs)
        body = "".join(self.body)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
            f'width="{self.w}" height="{self.h}" role="img" aria-labelledby="t">'
            f'<title id="t">{self.title}</title>'
            f"<style>{css}</style>"
            f"<defs>{defs}</defs>"
            f"{body}</svg>"
        )

    def save(self, path):
        svg = self.render()
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        return len(svg)


# ---- shared drawing helpers ----

def pixel_frame(s, border, faint="#1F2A38", inset=6):
    """CRT double-border frame on transparent canvas (bg drawn by caller)."""
    w, h = s.w, s.h
    s.add(
        f'<rect x="0" y="0" width="{w}" height="{h}" fill="#0B0F14"/>'
        f'<rect x="{inset}" y="{inset}" width="{w-2*inset}" height="{h-2*inset}" '
        f'fill="none" stroke="{border}" stroke-width="3"/>'
        f'<rect x="{inset+8}" y="{inset+8}" width="{w-2*(inset+8)}" height="{h-2*(inset+8)}" '
        f'fill="none" stroke="{faint}" stroke-width="2"/>'
    )


def star(s, cx, cy, r, color, cls=""):
    """4-point pixel star: plus + diagonal dots."""
    a = r
    b = r // 2
    s.add(
        f'<g class="{cls}"><rect x="{cx-b}" y="{cy-a}" width="{2*b}" height="{2*a}" fill="{color}"/>'
        f'<rect x="{cx-a}" y="{cy-b}" width="{2*a}" height="{2*b}" fill="{color}"/>'
        f'<rect x="{cx-b}" y="{cy-b}" width="{b}" height="{b}" fill="{color}"/>'
        f'<rect x="{cx+b}" y="{cy+b}" width="{b}" height="{b}" fill="{color}"/></g>'
    )


def sweep_bar(s, y, height, w, color, gap_left, gap_right, cls="sw"):
    """lemomo-style light sweep clipped between two gaps."""
    seg_w = (gap_left - 60) + (w - gap_right - 60)
    s.defs(
        f'<linearGradient id="swg" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{color}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{color}"/>'
        f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient>'
        f'<clipPath id="swc"><rect x="60" y="{y}" width="{gap_left-60-40}" height="{height}"/>'
        f'<rect x="{gap_right+40}" y="{y}" width="{w-gap_right-40-60}" height="{height}"/></clipPath>'
    )
    s.add(
        f'<rect x="60" y="{y}" width="{gap_left-60-40}" height="{height}" fill="none" stroke="#1F2A38" stroke-width="1"/>'
        f'<rect x="{gap_right+40}" y="{y}" width="{w-gap_right-40-60}" height="{height}" fill="none" stroke="#1F2A38" stroke-width="1"/>'
        f'<g clip-path="url(#swc)"><rect class="{cls}" x="-320" y="{y+1}" width="320" '
        f'height="{height-2}" fill="url(#swg)"/></g>'
    )
