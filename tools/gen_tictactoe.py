"""gen_tictactoe.py — pre-stage the pixel tic-tac-toe easter egg (HUMAN_QUEUE #2).

kylepls-style: the ENTIRE game tree is hardcoded as markdown anchors — zero
Actions, zero server. Visitor plays ✖️ (X, always first), the house plays ⭕ (O)
with minimax-optimal moves, so the visitor can never win (that's the tease).

Output: tools/output/tictactoe-section.md — NOT wired into README until the
user approves (HUMAN_QUEUE #2). Self-tests prove tree integrity before writing.

Markdown shape per decision state (visitor to move):
    <a name="sN"></a>
    ✖️ [⬜](#sM) [⬜](#sK) ⭕<br>[⬜](#sP) [⬜](#sN) ⬜<br>⬜ ✖️ ⬜
House response is baked into the target state (visitor move + optimal reply).
"""
import functools, pathlib, sys

X, O, E = "X", "O", " "
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def winner(b):
    for a, c, d in LINES:
        if b[a] != E and b[a] == b[c] == b[d]:
            return b[a]
    return None


def minimax_score(b, player):
    """Score from O's perspective: O win=1, draw=0, X win=-1 (O minimizes X)."""
    w = winner(b)
    if w == O:
        return 1
    if w == X:
        return -1
    if E not in b:
        return 0
    scores = []
    for i, c in enumerate(b):
        if c == E:
            nb = b[:i] + (player,) + b[i + 1:]
            scores.append(minimax_score(nb, X if player == O else O))
    return max(scores) if player == O else min(scores)


def house_move(b):
    """O's optimal move (win > draw > lose)."""
    best, best_i = -2, None
    for i, c in enumerate(b):
        if c == E:
            s = minimax_score(b[:i] + (O,) + b[i + 1:], X)
            if s > best:
                best, best_i = s, i
    return best_i


def encode(b):
    return "s" + "".join({"X": "2", "O": "1", E: "0"}[c] for c in b)


def tile_md(c, target):
    if c == X:
        return "✖️"
    if c == O:
        return "⭕"
    return f"[⬜](#{target})"


# ---- generate the reachable tree ----
states = {}          # board -> {"lines": [row, row, row] as markdown, "result": str|None}
order = []           # stable output order


def build(b):
    """b = board with visitor (X) to move. Returns after registering state."""
    if b in states:
        return
    key = encode(b)
    rows = []
    result = None
    if winner(b) or E not in b:
        result = "⭕ WINS" if winner(b) == O else "DRAW"
    for r in range(3):
        row = []
        for cidx in range(3):
            i = r * 3 + cidx
            c = b[i]
            if c != E:
                row.append(tile_md(c, None))
            elif result:
                row.append("⬜")
            else:
                nb = b[:i] + (X,) + b[i + 1:]
                if winner(nb) == X:
                    raise AssertionError("visitor win reachable — house not optimal?!")
                if E not in nb:
                    nxt = nb  # visitor filled last tile → draw terminal
                else:
                    m = house_move(nb)
                    nxt = nb[:m] + (O,) + nb[m + 1:]
                build(nxt)
                row.append(tile_md(E, encode(nxt)))
        rows.append(row)
    states[b] = {"key": key, "rows": rows, "result": result}
    order.append(b)


build((E,) * 9)

# ---- self-tests ----
assert states[(E,) * 9] is not None
targets = []
for b, st in states.items():
    if st["result"]:
        continue
    for r in st["rows"]:
        for cell in r:
            if cell.startswith("[⬜](#"):
                targets.append(cell[5:-1])
missing = [t for t in set(targets) if t not in {encode(b) for b in states}]
assert not missing, f"links to missing anchors: {missing[:5]}"
# every path from empty ends in terminal (full DFS)
stack = [(E,) * 9]
seen = set()
while stack:
    b = stack.pop()
    if b in seen:
        continue
    seen.add(b)
    st = states[b]
    if st["result"]:
        continue
    for i, c in enumerate(b):
        if c == E:
            nb = b[:i] + (X,) + b[i + 1:]
            assert winner(nb) != X, "X win reachable"
            if E not in nb:
                continue
            m = house_move(nb)
            stack.append(nb[:m] + (O,) + nb[m + 1:])

# ---- render markdown ----
out = ["## 🕹️ TIC-TAC-TOE — beat the house", "",
       "You are ✖️ and move first. Click a square; the house answers. **Nobody has ever won.**", ""]
for b in order:
    st = states[b]
    out.append(f'<a name="{st["key"]}"></a>')
    if st["result"]:
        out.append(f"<b>{st['result']}</b> — [PLAY AGAIN](#s000000000)")
    else:
        out.append("<br>".join(" ".join(r) for r in st["rows"]))
    out.append("")
section = "\n".join(out)
dest = pathlib.Path(__file__).parent / "output" / "tictactoe-section.md"
dest.parent.mkdir(exist_ok=True)
dest.write_text(section, encoding="utf-8")
print(f"states: {len(states)}  links: {len(targets)}  section: {len(section)}B -> {dest.name}")
