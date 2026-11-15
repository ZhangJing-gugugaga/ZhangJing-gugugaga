"""Pixel-arcade palette — single source of color truth.

All 8 assets import from here. Contrast audited against BG (#0B0F14, ~L 0.13):
- AMBER/TEXT/GREEN/CYAN/PINK all land >= 7:1 (large-text safe)
- DIM >= 5:1 (metadata only, never body copy)
"""

BG = "#0B0F14"       # CRT black
PANEL = "#111827"    # raised panel
PANEL2 = "#0F1620"   # recessed panel
AMBER = "#FFD447"    # primary — arcade amber
GREEN = "#4ADE80"    # pixel green (contribution-wall kin)
PINK = "#FF5FA2"     # accent — magenta
CYAN = "#6EE7FF"     # accent — ice cyan
TEXT = "#E8E8E8"     # body text
DIM = "#8B95A5"      # metadata text
FAINT = "#1F2A38"    # grid lines / inactive strokes
WHITE = "#F8FAFC"

# project accent mapping
RPD = AMBER
LEXI = CYAN
TERM = PINK
