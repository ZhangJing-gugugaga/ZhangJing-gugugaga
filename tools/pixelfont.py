"""pixelfont — render text as pixel <rect> grids. Zero <text>, zero external fonts.

GitHub sanitizes SVG: no external resources, no <text> with custom fonts.
So every glyph becomes merged pixel rects. Two sources:
  - ASCII: hand-drawn 5x7 bitmaps (authentic arcade look)
  - CJK:   PIL renders a CJK/mono font at 4x, block-downscales to a chunky grid

All rows run-length merged so a glyph costs ~1 rect per stroke, not per pixel.
"""
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- 5x7 ASCII
FONT5 = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    ",": ["00000", "00000", "00000", "00000", "00110", "00100", "01000"],
    ":": ["00000", "01100", "01100", "00000", "01100", "01100", "00000"],
    "!": ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    "?": ["01110", "10001", "00001", "00110", "00100", "00000", "00100"],
    "$": ["00100", "01111", "10100", "01110", "00101", "11110", "00100"],
    ">": ["10000", "01000", "00100", "00010", "00100", "01000", "10000"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    "_": ["00000", "00000", "00000", "00000", "00000", "00000", "11111"],
    "+": ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    "/": ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    "(": ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ")": ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    "'": ["00100", "00100", "01000", "00000", "00000", "00000", "00000"],
    '"': ["01010", "01010", "00000", "00000", "00000", "00000", "00000"],
    "★": ["00100", "00100", "11111", "00100", "00100", "00000", "00000"],
    "◆": ["00000", "00100", "01110", "11111", "01110", "00100", "00000"],
    "▶": ["10000", "11000", "11100", "11110", "11100", "11000", "10000"],
    "·": ["00000", "00000", "00000", "01100", "01100", "00000", "00000"],
}

ASCII_W, ASCII_H = 5, 7

_CJK_FONT_PATHS = [
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simsun.ttc",
]
_cjk_cache = {}


def _needs_cjk(s):
    # '★' needs the real five-point shape from the CJK font (5x7 can't do it)
    return any(ord(ch) > 0x2E80 or ch == "★" for ch in s)


def _cjk_font(size_px):
    key = size_px
    if key not in _cjk_cache:
        for p in _CJK_FONT_PATHS:
            try:
                _cjk_cache[key] = ImageFont.truetype(p, size_px)
                break
            except OSError:
                continue
        else:
            raise RuntimeError("no CJK font found in " + repr(_CJK_FONT_PATHS))
    return _cjk_cache[key]


def _string_grid(s, cell, cjk_cells=12, supersample=4):
    """Render string (ASCII or CJK or mixed) to a list of 0/1 row strings.

    cell = final svg px per pixel-cell.
    ASCII: native 5x7 bitmaps (1 glyph = 5x7 cells).
    CJK/mixed: PIL at cjk_cells*supersample, block-reduced by supersample,
    so one CJK glyph occupies ~cjk_cells cells of grid.
    """
    if not _needs_cjk(s):
        rows = [""] * ASCII_H
        for ch in s.upper():
            g = FONT5.get(ch, FONT5["?"])
            for r in range(ASCII_H):
                rows[r] += g[r] + "0"  # 1-cell letter spacing
        if s:
            for r in range(ASCII_H):
                rows[r] = rows[r][:-1]
        return rows
    # CJK / mixed path
    big = cjk_cells * supersample
    font = _cjk_font(big)
    tmp = Image.new("L", (1, 1))
    tmpd = ImageDraw.Draw(tmp)
    bx = tmpd.textbbox((0, 0), s, font=font)
    w, h = bx[2] - bx[0], bx[3] - bx[1]
    pad = big // 2
    img = Image.new("L", (w + pad * 2, h + pad * 2), 0)
    d = ImageDraw.Draw(img)
    d.text((pad - bx[0], pad - bx[1]), s, fill=255, font=font)
    W, H = img.size
    gw, gh = W // supersample, H // supersample
    small = img.resize((gw, gh), Image.BOX)  # coverage per cell
    pix = small.load()
    rows = []
    for y in range(gh):
        row = "".join("1" if pix[x, y] >= 90 else "0" for x in range(gw))
        rows.append(row)
    # trim empty rows/cols
    top = next((i for i, r in enumerate(rows) if "1" in r), 0)
    bot = next((gh - i for i, r in enumerate(reversed(rows)) if "1" in r), gh)
    cols_used = [any(r[x] == "1" for r in rows) for x in range(gw)]
    left = next((i for i, u in enumerate(cols_used) if u), 0)
    right = next((gw - i for i, u in enumerate(reversed(cols_used)) if u), gw)
    return [r[left:right] for r in rows[top:bot]]


def _rows_to_rects(rows, x, y, cell, color):
    """Run-length merge each row into wide rects."""
    out = []
    for gy, row in enumerate(rows):
        rx = -1
        for gx, c in enumerate(row + "0"):
            if c == "1" and rx < 0:
                rx = gx
            elif c == "0" and rx >= 0:
                out.append(
                    f'<rect x="{x + rx * cell}" y="{y + gy * cell}" '
                    f'width="{(gx - rx) * cell}" height="{cell}" fill="{color}"/>'
                )
                rx = -1
    return "".join(out)


def measure(s, cell, cjk_cells=12):
    rows = _string_grid(s, cell, cjk_cells)
    w = max((len(r) for r in rows), default=0) * cell
    return w, len(rows) * cell


def text(x, y, s, cell, color, shadow=None, cjk_cells=12):
    """Return (svg_elements, width, height). Shadow = 1-cell offset dup."""
    rows = _string_grid(s, cell, cjk_cells)
    w = max((len(r) for r in rows), default=0) * cell
    h = len(rows) * cell
    els = ""
    if shadow:
        els += _rows_to_rects(rows, x + cell, y + cell, cell, shadow)
    els += _rows_to_rects(rows, x, y, cell, color)
    return els, w, h


def text_centered(cx, y, s, cell, color, shadow=None, canvas_w=1300):
    w, h = measure(s, cell)
    return text((canvas_w - w) // 2, y, s, cell, color, shadow) + (h,)
