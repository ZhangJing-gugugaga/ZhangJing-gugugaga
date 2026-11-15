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
        self._defs = []    # gradients/clipPaths
        self.body = []     # drawable elements

    def style(self, css):
        self.styles.append(css)

    def defs(self, markup):
        self._defs.append(markup)

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

    # ---- M2: richer motion primitives (variety beyond blink) ----
    # "fails visible" contract: every animated property has a natural attribute
    # state that is correct when animations are off (reduced-motion / old renderers).

    def use_frameswap(self, dur="0.6s", delay="0s"):
        """Two stacked groups .fa (natural visible) / .fb (set opacity="0" attr!)
        alternate every dur/2. With animations off: fa shows, fb hidden."""
        self.style(
            f".fa{{animation:fsa {dur} steps(1,end) infinite;animation-delay:{delay}}}"
            f".fb{{animation:fsb {dur} steps(1,end) infinite;animation-delay:{delay}}}"
            "@keyframes fsa{0%,49%{opacity:1}50%,100%{opacity:0}}"
            "@keyframes fsb{0%,49%{opacity:0}50%,100%{opacity:1}}"
        )

    def use_patrol(self, dist, dur="7s", delay="0s"):
        """March right, flip, march back. scaleX passes through 0 = turn squash."""
        self.style(
            f".pt{{animation:pt {dur} ease-in-out {delay} infinite}}"
            f"@keyframes pt{{0%,6%{{transform:translateX(0) scaleX(1)}}"
            f"44%,50%{{transform:translateX({dist}px) scaleX(1)}}"
            f"56%,94%{{transform:translateX(0) scaleX(-1)}}"
            f"100%{{transform:translateX(0) scaleX(1)}}}}"
        )

    def use_float(self, dur="3s", dy=4, delay="0s"):
        self.style(
            f".flt{{animation:flt {dur} ease-in-out {delay} infinite alternate}}"
            f"@keyframes flt{{from{{transform:translateY(0)}}to{{transform:translateY({dy}px)}}}}"
        )

    def use_scanline(self, travel, dur="8s", delay="0s"):
        """CRT refresh band. Caller draws the band rect with class .scn at y=0.
        Delay de-syncs from same-period loops; `both` holds the off-canvas
        from-state during the delay (no stuck band at load)."""
        self.style(
            f".scn{{animation:scn {dur} linear {delay} infinite both}}"
            f"@keyframes scn{{from{{transform:translateY(-40px)}}to{{transform:translateY({travel}px)}}}}"
        )

    def use_poweron(self, dur="0.7s"):
        """One-shot CRT flicker-on for a content group."""
        self.style(
            f".pon{{animation:pon {dur} steps(6,end) both}}"
            "@keyframes pon{0%{opacity:0}38%{opacity:1}52%{opacity:.15}"
            "66%{opacity:1}80%{opacity:.4}100%{opacity:1}}"
        )

    def use_fillbar(self, w, dur="3.2s", delay="0s"):
        """Progress bar fill (bar rect width attr = w; chunky steps fill, hold, snap)."""
        self.style(
            f".flb{{animation:flb {dur} steps(14,end) {delay} infinite}}"
            f"@keyframes flb{{0%{{width:0}}62%,94%{{width:{w}px}}99.9%{{width:{w}px}}}}"
        )

    def use_cursor_cycle(self, xs, period="6.6s", delay="0s"):
        """Cursor jumps through x positions (plateau keyframes = discrete hops).
        Last stop extends to 99.9% so the loop wraps as a jump, not a slide."""
        stops = []
        n = len(xs)
        for i, x in enumerate(xs):
            a = i / n * 100
            b = 99.9 if i == n - 1 else ((i + 1) / n * 100) - (100 / n * 0.1)
            stops.append(f"{a:.1f}%,{b:.2f}%{{transform:translateX({x}px)}}")
        self.style(
            f".cyc{{animation:cyc {period} steps(1,end) infinite;animation-delay:{delay}}}"
            f"@keyframes cyc{{{','.join(stops)}}}"
        )

    def phase_visibility(self, cls, period, i, n, delay="0s"):
        """Element of a cycle: visible only during phase i of n (plateau).
        Shape: [0,a)=off, [a,b)=on, [b,100]=off — steps() holds each plateau.
        Last phase runs to 99.9%; phase 0 starts at 0.4% to avoid a duplicate
        0% keyframe edge case."""
        a = max(i / n * 100, 0.4 if i == 0 else 0)
        b = 99.9 if i == n - 1 else ((i + 1) / n * 100) - (100 / n * 0.1)
        self.style(
            f".{cls}{{animation:{cls}k {period} steps(1,end) infinite;animation-delay:{delay}}}"
            f"@keyframes {cls}k{{0%{{opacity:0}}{a:.2f}%{{opacity:1}}"
            f"{b:.2f}%{{opacity:0}}100%{{opacity:0}}}}"
        )

    _dw = 0

    def draw_line(self, x1, y1, x2, y2, color, width=2, delay="0s", dur="0.5s"):
        """Self-drawing line (stroke-dashoffset). Fails visible: attr offset=0."""
        import math
        ln = math.hypot(x2 - x1, y2 - y1)
        c = f"dw{self._dw}"
        self._dw += 1
        self.style(
            f".{c}{{animation:dwk {dur} ease-out {delay} both}}"
            f"@keyframes dwk{{from{{stroke-dashoffset:{ln:.0f}}}}}"
        )
        self.add(
            f'<line class="{c}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="{width}" stroke-dasharray="{ln:.0f}"/>'
        )

    def use_glitch(self, amp=2, dur="0.5s"):
        """Center-motif jitter: rapid ±amp steps on x."""
        self.style(
            f".gl{{animation:gl {dur} steps(2,end) infinite}}"
            f"@keyframes gl{{0%,49%{{transform:translateX(0)}}50%,100%{{transform:translateX({amp}px)}}}}"
        )

    def use_echo(self, dur="3.6s", delay="1.2s", opacity=".3"):
        """Second sweep bar echoing the first at lower opacity (call use_sweep too)."""
        self.style(
            f".echo{{animation:sw {dur} cubic-bezier(.45,0,.25,1) infinite;animation-delay:{delay};opacity:{opacity}}}"
        )

    def render(self):
        css = "\n".join(self.styles) + "\n" + MOTION_RESET
        defs = "".join(self._defs)
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
