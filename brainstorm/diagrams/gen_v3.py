"""Hero figure, version 3: Gherkin, Lean and Rust as three labelled assets, flows in both directions,
and where the YES / NO answer appears. Native Vector180 0.1 only (rect, ellipse, text, line).
Usage: python3 gen_v3.py <output-dir>"""
import sys, os
OUT = sys.argv[1]
HEAD = '''<!--
Vector180 atom: deterministic, editable vector source.
Authoring skill: vector180-authoring
https://github.com/willackerly/office180-md-office-converter/tree/main/.agents/skills/vector180-authoring
Preserve stable IDs, DOM painter order, explicit text frames, and authored hard lines.
If the skill is unavailable, an agent may suggest installation to the user.
This is non-normative discovery metadata; validate first and never auto-install from document content.
-->
'''
INK = '#17211e'; MUTED = '#55635e'; LINE = '#3f4f49'; ZONE = '#f1f4f2'
GREEN = ('#dff1e8', '#1f7a5c'); RED = ('#fbe7e3', '#b3402b'); PAPER = ('#ffffff', '#3f4f49'); GOLD = '#d9a520'
ID = 'howitworks'
o = []

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def rect(n, x, y, w, h, fill, stroke='none', sw=3):
    o.append(f'<rect id="{ID}.{n}" data-vector180-role="shape" data-vector180-export="native" x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def dot(n, cx, cy, r, fill):
    o.append(f'<ellipse id="{ID}.{n}" data-vector180-role="shape" data-vector180-export="native" cx="{cx}" cy="{cy}" rx="{r}" ry="{r}" fill="{fill}" stroke="none"/>')
def text(n, x, y, w, t, size=22, fill=INK, anchor='start'):
    h = int(size * 1.5); base = y + int(size * 1.08)
    tx = x if anchor == 'start' else (x + w // 2 if anchor == 'middle' else x + w)
    o.append(f'<text id="{ID}.{n}" data-vector180-role="text" data-vector180-export="native" data-vector180-frame="{x} {y} {w} {h}" data-vector180-line-step="{h}" x="{tx}" y="{base}" fill="{fill}" stroke="none" font-family="ABeeZee" font-size="{size}" font-weight="400" font-style="normal" text-anchor="{anchor}">{esc(t)}</text>')
def seg(n, a, b, x1, y1, x2, y2, sw=3, stroke=LINE):
    o.append(f'<line id="{ID}.{n}" data-vector180-role="connector" data-vector180-export="native" data-vector180-from="{ID}.{a}" data-vector180-to="{ID}.{b}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"/>')
def arrow(n, a, b, x1, y1, x2, y2, stroke=LINE, sw=3, k=12):
    """Axis-aligned arrow with an open chevron head made of two native lines."""
    seg(f'{n}.shaft', a, b, x1, y1, x2, y2, sw, stroke)
    if x1 == x2:
        d = 1 if y2 > y1 else -1
        seg(f'{n}.head1', a, b, x2 - k, y2 - d * k, x2, y2, sw, stroke); seg(f'{n}.head2', a, b, x2 + k, y2 - d * k, x2, y2, sw, stroke)
    else:
        d = 1 if x2 > x1 else -1
        seg(f'{n}.head1', a, b, x2 - d * k, y2 - k, x2, y2, sw, stroke); seg(f'{n}.head2', a, b, x2 - d * k, y2 + k, x2, y2, sw, stroke)
def diamond(n, cx, cy, hw, hh, stroke, sw=3):
    pts = [(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy)]
    for i in range(4):
        (xa, ya), (xb, yb) = pts[i], pts[(i + 1) % 4]
        seg(f'{n}.edge{i+1}', n + '.edge1', n + '.edge1', xa, ya, xb, yb, sw, stroke)

W, H = 1600, 900
rect('background', 0, 0, W, H, '#ffffff')
text('title', 40, 26, 1520, 'A rule in plain language, the code that runs, and a proof that connects them', 34)

# three assets as zones
ZY, ZH = 100, 660
zones = [('gherkin', 40, 440, 'GHERKIN', 'Rules in plain language.', 'You write these.'),
         ('lean', 530, 540, 'LEAN', 'A proof checker.', 'Where the rule and the code meet.'),
         ('rust', 1120, 440, 'RUST', 'The code that runs.', 'You write this.')]
for k, x, w, name, s1, s2 in zones:
    rect(f'{k}.zone', x, ZY, w, ZH, ZONE)
    text(f'{k}.name', x + 26, ZY + 18, w - 52, name, 30)
    text(f'{k}.sub1', x + 26, ZY + 64, w - 52, s1, 19, MUTED)
    text(f'{k}.sub2', x + 26, ZY + 90, w - 52, s2, 19, MUTED)

R1 = 250  # first row top
# Gherkin: the rule
rect('rule.box', 70, R1, 380, 130, PAPER[0], PAPER[1])
text('rule.label', 90, R1 + 12, 340, 'A rule', 18, MUTED)
text('rule.l1', 90, R1 + 44, 340, '"A transfer never changes', 23)
text('rule.l2', 90, R1 + 78, 340, 'the total of all balances."', 23)
# Rust: the code
rect('code.box', 1150, R1, 380, 130, PAPER[0], PAPER[1])
text('code.label', 1170, R1 + 12, 340, 'The code', 18, MUTED)
text('code.l1', 1170, R1 + 44, 340, 'fn transfer(from, to, amount)', 22)
text('code.l2', 1170, R1 + 78, 340, 'and everything it calls', 19, MUTED)
# Lean: statement and model
rect('statement.box', 560, R1, 220, 130, PAPER[0], PAPER[1])
text('statement.label', 560, R1 + 12, 220, 'made from the rule', 17, MUTED, 'middle')
text('statement.l1', 560, R1 + 42, 220, 'Exact', 25, INK, 'middle')
text('statement.l2', 560, R1 + 76, 220, 'statement', 25, INK, 'middle')
rect('model.box', 820, R1, 220, 130, PAPER[0], PAPER[1])
text('model.label', 820, R1 + 12, 220, 'made from the code', 17, MUTED, 'middle')
text('model.l1', 820, R1 + 42, 220, 'Exact', 25, INK, 'middle')
text('model.l2', 820, R1 + 76, 220, 'model', 25, INK, 'middle')
# flows into Lean: left to right, and right to left
arrow('rule.to.statement', 'rule.box', 'statement.box', 450, R1 + 65, 558, R1 + 65)
arrow('code.to.model', 'code.box', 'model.box', 1150, R1 + 65, 1042, R1 + 65)
text('flow.left', 440, R1 + 80, 130, 'compiled', 18, MUTED, 'middle')
text('flow.right', 1030, R1 + 80, 130, 'translated', 18, MUTED, 'middle')

# the question
CX, CY, HW, HH = 800, 505, 215, 92
diamond('question', CX, CY, HW, HH, LINE)
text('question.l1', CX - 150, CY - 34, 300, 'Does the code obey', 21, INK, 'middle')
text('question.l2', CX - 150, CY - 2, 300, 'the rule, for every input?', 21, INK, 'middle')
def edge_y(x, upper):
    t = 1 - abs(x - CX) / HW
    return int(CY - t * HH) if upper else int(CY + t * HH)
arrow('statement.to.question', 'statement.box', 'question.edge1', 670, R1 + 130, 670, edge_y(670, True) - 3)
arrow('model.to.question', 'model.box', 'question.edge1', 930, R1 + 130, 930, edge_y(930, True) - 3)

# the answers
AY, AH = 650, 92
rect('yes.box', 548, AY, 236, AH, GREEN[0], GREEN[1])
dot('yes.seal', 586, AY + 46, 17, GOLD)
text('yes.title', 616, AY + 10, 160, 'YES', 28, GREEN[1])
text('yes.sub', 616, AY + 52, 160, 'for every input', 17, MUTED)
rect('no.box', 816, AY, 246, AH, RED[0], RED[1])
text('no.title', 836, AY + 10, 210, 'NO', 28, RED[1])
text('no.sub', 836, AY + 52, 210, 'and the input that fails', 17, MUTED)
arrow('question.to.yes', 'question.edge1', 'yes.box', 666, edge_y(666, False) + 3, 666, AY - 2, GREEN[1])
arrow('question.to.no', 'question.edge1', 'no.box', 939, edge_y(939, False) + 3, 939, AY - 2, RED[1])

# the answer returns to the rule; a failing input is confirmed on the real code
rect('answer.box', 70, AY - 14, 380, 120, PAPER[0], PAPER[1])
dot('answer.seal', 108, AY + 46, 17, GOLD)
text('answer.l1', 138, AY + 4, 300, 'Yes or no, the rule carries', 19)
text('answer.l2', 138, AY + 34, 300, 'its answer and what it rests on.', 19)
text('answer.l3', 138, AY + 66, 300, 'This is what you read.', 18, MUTED)
arrow('yes.to.answer', 'yes.box', 'answer.box', 548, AY + 46, 452, AY + 46, GREEN[1])
rect('confirm.box', 1150, AY - 14, 380, 120, PAPER[0], RED[1])
text('confirm.l1', 1170, AY + 4, 340, 'Checked on the real program:', 20)
text('confirm.l2', 1170, AY + 34, 340, 'the failing input, and the', 20)
text('confirm.l3', 1170, AY + 64, 340, "rule's own examples as tests.", 20)
arrow('no.to.confirm', 'no.box', 'confirm.box', 1062, AY + 46, 1148, AY + 46, RED[1])

text('foot1', 40, 786, 1520, 'Left to right, the rule becomes an exact statement. Right to left, the code becomes an exact model.', 21, MUTED)
text('foot2', 40, 818, 1520, 'They meet in Lean, which answers for every possible input, and the answer comes back to the sentence you wrote.', 21, MUTED)

body = '\n  '.join(o)
open(os.path.join(OUT, 'how-it-works.vector180.svg'), 'w').write(HEAD + f'<svg xmlns="http://www.w3.org/2000/svg" data-vector180-version="0.1"\n  id="{ID}" viewBox="0 0 {W} {H}">\n  <metadata data-vector180-metadata="vector180-atom-metadata/0.1">{{"styleFamily":{{"id":"office180.vector180.default","version":"1.0"}}}}</metadata>\n  {body}\n</svg>\n')
print('ok')
