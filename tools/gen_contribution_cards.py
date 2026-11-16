from pathlib import Path
import base64
import sys
import re

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from palette import GREEN, CYAN, PINK, TEXT, DIM, FAINT, PANEL2, AMBER
from svgkit import SVG, pixel_frame
import pixelfont as pf

OUT = ROOT / 'assets'

def text(card, x, y, value, size=2, color=TEXT):
    markup, _, _ = pf.text(x, y, value, size, color)
    rectangles = re.findall(r'<rect x="([^"]+)" y="([^"]+)" width="([^"]+)" height="([^"]+)" fill="[^"]+"/>', markup)
    outlines = []
    for left, top, width, height in rectangles:
        outlines.append(f'M{left} {top}h{width}v{height}h-{width}z')
    card.add(f'<path fill="{color}" d="{"".join(outlines)}"/>')

def centered(card, x, y, width, value, size=2, color=TEXT):
    measured, _ = pf.measure(value, size)
    text(card, x + (width - measured) / 2, y, value, size, color)

def phase(card, name, index):
    if index == 0:
        frames = '0%,33.32%{opacity:1}33.33%,100%{opacity:0}'
    elif index == 1:
        frames = '0%,33.32%{opacity:0}33.33%,66.65%{opacity:1}66.66%,100%{opacity:0}'
    else:
        frames = '0%,66.65%{opacity:0}66.66%,100%{opacity:1}'
    card.style(f'.{name}{{animation:{name}k 7.2s steps(1,end) infinite}}'
               f'@keyframes {name}k{{{frames}}}')

def scaffold(title, description, detail, stars, color):
    card = SVG(1300, 360, f'{title} 开源贡献卡片')
    pixel_frame(card, color)
    text(card, 60, 30, '开源贡献', 2, color)
    text(card, 60, 68, title, 5, color)
    text(card, 60, 124, description)
    text(card, 60, 154, detail, color=DIM)
    text(card, 60, 219, stars, 6, color)
    number_width, _ = pf.measure(stars, 6)
    text(card, 60 + number_width + 14, 219, '★', 6, color)
    text(card, 60, 279, '上游仓库 Star', 2, DIM)
    text(card, 60, 310, 'GITHUB / 2026-11-16', 1, DIM)
    return card

tdd = scaffold('TDD GUARD', '让 Claude Code 按测试驱动开发。',
               '先写失败测试，再实现与重构。', '2.4K', GREEN)
stages = [('RED', 'FAILING TEST', '#FF6B80'),
          ('GREEN', 'MINIMAL CODE', GREEN),
          ('REFACTOR', 'LINT + CLEAN', CYAN)]
for index, (name, subtitle, color) in enumerate(stages):
    x = 664 + index * 198
    tdd.add(f'<rect x="{x}" y="65" width="180" height="94" fill="{PANEL2}" stroke="{FAINT}" stroke-width="2"/>')
    centered(tdd, x, 88, 180, name, 3, color)
    centered(tdd, x, 132, 180, subtitle, 1, DIM)
    phase(tdd, f'tdd{index}', index)
    tdd.add(f'<rect class="tdd{index}" opacity="{1 if index == 0 else 0}" x="{x}" y="65" width="180" height="94" fill="none" stroke="{color}" stroke-width="3"/>')
    if index < 2:
        text(tdd, x + 185, 105, '>', 2, DIM)

tdd.add(f'<rect x="664" y="189" width="576" height="126" fill="{PANEL2}" stroke="{FAINT}" stroke-width="2"/>')
terminal = [('WRITE A FAILING TEST', '先写测试，确认它失败。', '#FF6B80'),
            ('IMPLEMENT JUST ENOUGH', '通过当前测试，再继续。', GREEN),
            ('REFACTOR WITH LINT', '保持测试通过，整理实现。', CYAN)]
for index, (english, chinese, color) in enumerate(terminal):
    tdd.add(f'<g class="tdd{index}" opacity="{1 if index == 0 else 0}">')
    text(tdd, 687, 212, '> ' + english, 2, color)
    text(tdd, 687, 250, chinese, 2, TEXT)
    tdd.add('</g>')
text(tdd, 687, 291, 'CLAUDE CODE / TDD ENFORCEMENT', 1, DIM)
tdd.save(OUT / 'card-tdd-guard.svg')

mcp = scaffold('MCP SERVERS', '让 AI 通过 MCP 调用工具与数据。',
               '文件操作、持久记忆与网页内容。', '92K', CYAN)
for y in [88, 180, 272]:
    mcp.add(f'<path d="M 1000 180 H 1038 V {y} H 1070" fill="none" stroke="{FAINT}" stroke-width="3"/>')
mcp.add(f'<path d="M 814 180 H 860" fill="none" stroke="{FAINT}" stroke-width="3"/>')
nodes = [(664, 140, 150, 80, 'AI CLIENT', TEXT),
         (860, 140, 140, 80, 'MCP', CYAN),
         (1070, 56, 170, 64, 'FILESYSTEM', GREEN),
         (1070, 148, 170, 64, 'MEMORY', AMBER),
         (1070, 240, 170, 64, 'FETCH', PINK)]
for x, y, width, height, name, color in nodes:
    mcp.add(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{PANEL2}" stroke="{FAINT}" stroke-width="2"/>')
    centered(mcp, x, y + (height - 14) / 2, width, name, 2, color)

for index, (target_y, color) in enumerate([(88, GREEN), (180, AMBER), (272, PINK)]):
    phase(mcp, f'mcp{index}', index)
    mcp.add(f'<path class="mcp{index}" opacity="{1 if index == 0 else 0}" d="M 814 180 H 860 M 1000 180 H 1038 V {target_y} H 1070" fill="none" stroke="{color}" stroke-width="3"/>')
    mcp.add(f'<rect class="mcp{index}" opacity="{1 if index == 0 else 0}" x="1070" y="{target_y-32}" width="170" height="64" fill="none" stroke="{color}" stroke-width="3"/>')
    # The packet takes the same three-segment route as the visible connection.
    mcp.style(f'.packet{index}{{animation:packet{index}k 7.2s linear infinite}}'
              f'@keyframes packet{index}k{{'
              f'0%,{index*100/3:.3f}%{{transform:translate(0px,0px)}}'
              f'{index*100/3+12:.3f}%{{transform:translate(224px,0px)}}'
              f'{index*100/3+23:.3f}%{{transform:translate(224px,{target_y-180}px)}}'
              f'{(index+1)*100/3-.01:.3f}%,100%{{transform:translate(256px,{target_y-180}px)}}}}')
    mcp.add(f'<g class="mcp{index}" opacity="{1 if index == 0 else 0}"><rect class="packet{index}" x="810" y="176" width="8" height="8" fill="{color}"/></g>')
text(mcp, 664, 42, 'REFERENCE IMPLEMENTATIONS', 1, DIM)
text(mcp, 664, 316, 'TOOLS / RESOURCES / DATA', 1, DIM)
mcp.save(OUT / 'card-mcp-servers.svg')
