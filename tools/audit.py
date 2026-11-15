"""audit.py — regression gate for the pixel-arcade profile assets.

Run after every asset regeneration, BEFORE pushing:
    python -I tools/audit.py

Checks (all gates must pass):
  G1  no <text> elements (GitHub SVG font rule)
  G2  no external references (http src/href, url(http, @import)
  G3  every asset: prefers-reduced-motion kill switch
  G4  every asset: role="img" + aria-labelledby + <title>
  G5  README asset refs == assets on disk; all refs share one ?v=N
  G6  per-asset size cap (130KB)
  G7  keyframes count >= baseline (motion-regression guard)
  G8  every animation class referenced has its keyframes defined
Exit code 0 = all green.
"""
import collections, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
README = ROOT / "README.md"
SIZE_CAP = 130 * 1024
KF_BASELINE = 40  # v3 shipped 45; alert if motion regresses below 40

failures = []
warns = []
files = sorted(ASSETS.glob("*.svg"))
print(f"assets on disk: {len(files)}")

readme = README.read_text(encoding="utf-8")
refs = re.findall(r'assets/([a-z0-9-]+\.svg)\?v=(\d+)', readme)
versions = {v for _, v in refs}
print(f"README refs: {len(refs)}  versions: {versions}")

# G5
disk = {f.name for f in files}
refd = {r[0] for r in refs}
if disk != refd:
    failures.append(f"G5 asset/ref mismatch: disk-only={disk-refd} ref-only={refd-disk}")
if len(versions) != 1:
    failures.append(f"G5 mixed ?v versions: {versions}")

kf_total = 0
for f in files:
    s = f.read_text(encoding="utf-8")
    rel = f.name
    # G1
    if re.search(r"<text[\s>]", s):
        failures.append(f"G1 {rel}: <text> element found")
    # G2
    if re.search(r'(src|href)="http|url\(http|@import', s):
        failures.append(f"G2 {rel}: external reference found")
    # G3
    if "prefers-reduced-motion" not in s:
        failures.append(f"G3 {rel}: no reduced-motion kill switch")
    # G4
    if 'role="img"' not in s or "aria-labelledby" not in s or "<title" not in s:
        failures.append(f"G4 {rel}: missing a11y attrs/title")
    # G6
    if f.stat().st_size > SIZE_CAP:
        failures.append(f"G6 {rel}: {f.stat().st_size}B > cap {SIZE_CAP}B")
    # G7
    kfs = re.findall(r"@keyframes\s+([A-Za-z0-9_-]+)", s)
    kf_total += len(set(kfs))
    dupes = [k for k, c in collections.Counter(kfs).items() if c > 1]
    if dupes:
        warns.append(f"G7 {rel}: duplicate @keyframes {dupes}")
    # G8 — every animated class has keyframes (ignore animation:none kill switch)
    used = set(re.findall(r"animation:(?!none)[a-z0-9_]+", s))
    used = {u.split(":")[1] for u in used}
    missing = {u for u in used if u not in set(kfs)}
    if missing:
        failures.append(f"G8 {rel}: animated classes missing keyframes: {missing}")

if kf_total < KF_BASELINE:
    failures.append(f"G7 total keyframes {kf_total} < baseline {KF_BASELINE} (motion regression?)")

# delay-without-fill scan (stuck-before-delay artifact)
for f in files:
    s = f.read_text(encoding="utf-8")
    for m in re.finditer(r"animation:[a-z0-9_]+ [^;}]*s\s+[^;}]*s[^;}]*;", s):
        seg = m.group(0)
        if "both" not in seg and "backwards" not in seg and "infinite" not in seg:
            warns.append(f"G-delay {f.name}: delayed one-shot without fill → {seg[:60]}")

print(f"total @keyframes definitions: {kf_total}")
for w in warns:
    print("WARN:", w)
if failures:
    print("\nFAIL:")
    for x in failures:
        print(" -", x)
    sys.exit(1)
print("\nALL GATES GREEN")
