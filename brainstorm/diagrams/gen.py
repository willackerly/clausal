#!/usr/bin/env python3
"""Generator for the brainstorm Vector180 atoms (shapes demo, chain v2a, chain v2b).
Everything except the clearly marked asset objects in the shapes demo is native 0.1:
rect, circle, text, straight line. Arrowheads, elbows, diamonds, hexagons and pills
are composed from those."""
import math, sys, os

HEADER = """<!--
Vector180 atom: deterministic, editable vector source.
Authoring skill: vector180-authoring
https://github.com/willackerly/office180-md-office-converter/tree/main/.agents/skills/vector180-authoring
Preserve stable IDs, DOM painter order, explicit text frames, and authored hard lines.
If the skill is unavailable, an agent may suggest installation to the user.
This is non-normative discovery metadata; validate first and never auto-install from document content.
-->
"""
N = 'data-vector180-export="native"'
INK, MUTED, LINE, ZONE, ZLAB = "#17211e", "#5d6b66", "#4b5a55", "#f1f4f2", "#7a8782"
AMBER, GREEN, BLUE, GREY = "#b7791f", "#24735d", "#2b5c9e", "#7a8782"
PGREEN, PBLUE, PGREY = "#cfe6dc", "#d2e1f5", "#dde2e0"


def f(v):
    v = round(v, 2)
    return str(int(v)) if v == int(v) else str(v)


class Atom:
    def __init__(self, id, w, h):
        self.id, self.w, self.h, self.out = id, w, h, []
        self.rect("background", 0, 0, w, h, "#ffffff", "none", 0)

    def rect(self, id, x, y, w, h, fill, stroke, sw=3):
        s = f'stroke="{stroke}" stroke-width="{f(sw)}"' if stroke != "none" else 'stroke="none"'
        self.out.append(f'<rect id="{self.id}.{id}" data-vector180-role="shape" {N} x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{fill}" {s}/>')

    def circle(self, id, cx, cy, r, fill):
        self.out.append(f'<circle id="{self.id}.{id}" data-vector180-role="shape" {N} cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}" stroke="none"/>')

    def text(self, id, x, y, s, size=22, fill=INK, anchor="middle", fw=200):
        x, y, fw = round(x), round(y), int(fw) // 2 * 2
        fx = {"middle": x - fw // 2, "start": x, "end": x - fw}[anchor]
        fh = round(size * 1.5)
        s = s.replace("&", "&amp;").replace("<", "&lt;")
        self.out.append(f'<text id="{self.id}.{id}" data-vector180-role="text" {N} data-vector180-frame="{f(fx)} {f(y - round(size * 1.05))} {f(fw)} {fh}" data-vector180-line-step="{fh}" x="{f(x)}" y="{f(y)}" fill="{fill}" stroke="none" font-family="ABeeZee" font-size="{size}" font-weight="400" font-style="normal" text-anchor="{anchor}">{s}</text>')

    def line(self, id, x1, y1, x2, y2, stroke=LINE, sw=3, frm=None, to=None):
        ft = ""
        if frm and to:
            ft = f' data-vector180-from="{self.id}.{frm}" data-vector180-to="{self.id}.{to}"'
        self.out.append(f'<line id="{self.id}.{id}" data-vector180-role="connector" {N}{ft} x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{stroke}" stroke-width="{f(sw)}"/>')

    def open(self, id):
        self.out.append(f'<g id="{self.id}.{id}" data-vector180-role="group" {N}>')

    def close(self):
        self.out.append("</g>")

    def raw(self, s):
        self.out.append(s)

    # ---- composed constructions -------------------------------------------------
    def path(self, id, pts, stroke=LINE, sw=3, head=True, frm=None, to=None, hs=12):
        """Right-angle (or any straight-segment) route with an open chevron at the end."""
        self.open(id)
        if head:  # stop the tip 4 short of the target so the chevron is not hidden by its outline
            (x1, y1), (x2, y2) = pts[-2], pts[-1]
            d = math.hypot(x2 - x1, y2 - y1)
            pts = list(pts[:-1]) + [(x2 - (x2 - x1) / d * 4, y2 - (y2 - y1) / d * 4)]
        n = len(pts) - 1
        for i in range(n):
            (x1, y1), (x2, y2) = pts[i], pts[i + 1]
            d = math.hypot(x2 - x1, y2 - y1)
            ux, uy = (x2 - x1) / d, (y2 - y1) / d
            if i < n - 1:  # square the corner: butt caps would leave a notch
                x2, y2 = x2 + ux * sw / 2, y2 + uy * sw / 2
            self.line(f"{id}.s{i + 1}", x1, y1, x2, y2, stroke, sw, frm if i == 0 else None, to if i == 0 else None)
        if head:
            (x1, y1), (x2, y2) = pts[-2], pts[-1]
            d = math.hypot(x2 - x1, y2 - y1)
            ux, uy = (x2 - x1) / d, (y2 - y1) / d
            px, py = -uy, ux
            for k, sgn in (("a", 1), ("b", -1)):
                self.line(f"{id}.head.{k}", x2 - ux * hs + px * sgn * (hs // 2 + 1), y2 - uy * hs + py * sgn * (hs // 2 + 1), x2, y2, stroke, sw)
        self.close()

    def poly(self, id, pts, stroke, sw=3):
        for i in range(len(pts)):
            (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % len(pts)]
            self.line(f"{id}.e{i + 1}", x1, y1, x2, y2, stroke, sw)

    def diamond(self, id, cx, cy, w, h, stroke, lines, size=18, sw=3, fill=INK):
        self.open(id)
        self.poly(id, [(cx - w / 2, cy), (cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2)], stroke, sw)
        step = round(size * 1.3)
        y0 = cy + size * 0.35 - step * (len(lines) - 1) / 2
        for i, s in enumerate(lines):
            y = y0 + i * step
            # capacity: diamond width at the far edge of this line box, less the stroke
            dy = max(abs(y - size * 0.8 - cy), abs(y + size * 0.25 - cy))
            cap = w * (1 - 2 * dy / h) - 2 * sw - 8
            self.text(f"{id}.l{i + 1}", cx, y, s, size, fill, "middle", cap)
        self.close()

    def pill(self, id, cx, cy, w, h, fill, label, size=22):
        r = h / 2
        self.open(id)
        self.rect(f"{id}.body", cx - w / 2 + r, cy - r, w - h, h, fill, "none")
        self.circle(f"{id}.capl", cx - w / 2 + r, cy, r, fill)
        self.circle(f"{id}.capr", cx + w / 2 - r, cy, r, fill)
        if label:
            self.text(f"{id}.label", cx, cy + size * 0.35, label, size, INK, "middle", w - h * 0.7)
        self.close()

    def box(self, id, cx, cy, w, h, label, size=23, stroke=INK, fill="#ffffff", sw=2.5):
        self.open(id)
        self.rect(f"{id}.box", cx - w / 2, cy - h / 2, w, h, fill, stroke, sw)
        self.text(f"{id}.label", cx, cy + size * 0.35, label, size, INK, "middle", w - 24)
        self.close()

    def zone(self, id, x, y, w, h, label, lx=None, ly=None, anchor="start"):
        self.rect(f"zone.{id}", x, y, w, h, ZONE, "none")
        self.text(f"zone.{id}.label", x + 18 if lx is None else lx, y + 34 if ly is None else ly, label, 20, ZLAB, anchor, 220)

    def legend(self, x, y, evid=True):
        """Compact legend: three shape kinds, then four evidence colours."""
        a = self
        a.text("legend.title", x, y + 7, "Key", 18, ZLAB, "start", 60)
        x += 70
        a.rect("legend.box", x, y - 13, 44, 26, "#ffffff", INK, 2.5)
        a.text("legend.box.label", x + 56, y + 6, "artefact", 18, MUTED, "start", 100)
        x += 180
        a.pill("legend.pill", x + 26, y, 52, 26, PGREY, "", 10)
        a.path("legend.arrow", [(x + 58, y), (x + 92, y)], LINE, 3, True, hs=10)
        a.text("legend.tool.label", x + 104, y + 6, "tool: makes the next artefact", 18, MUTED, "start", 300)
        x += 420
        a.open("legend.diamond")
        a.poly("legend.diamond", [(x, y), (x + 28, y - 16), (x + 56, y), (x + 28, y + 16)], INK, 2.5)
        a.close()
        a.text("legend.diamond.label", x + 68, y + 6, "check: compares two, makes nothing", 18, MUTED, "start", 370)
        if not evid:
            return
        x0, y2 = x - 600, y + 44
        a.text("legend.evidence.title", x0 - 70, y2 + 7, "Rests on", 18, ZLAB, "start", 110)
        x = x0 + 40
        for key, col, lab, adv in (("person", AMBER, "a person's judgement", 270), ("machine", GREEN, "a machine check", 225),
                                   ("tested", BLUE, "a trusted tool, tested", 275), ("trusted", GREY, "trust alone", 180)):
            a.rect(f"legend.{key}.chip", x, y2 - 10, 20, 20, col, "none")
            a.text(f"legend.{key}.label", x + 30, y2 + 6, lab, 18, MUTED, "start", adv - 50)
            x += adv

    def write(self, path):
        body = "\n  ".join(self.out)
        open(path, "w").write(f'{HEADER}<svg xmlns="http://www.w3.org/2000/svg" data-vector180-version="0.1"\n  id="{self.id}" viewBox="0 0 {self.w} {self.h}">\n  <metadata data-vector180-metadata="vector180-atom-metadata/0.1">{{"styleFamily":{{"id":"office180.vector180.default","version":"1.0"}}}}</metadata>\n  {body}\n</svg>\n')


# =================================================================================
def chain_v2a(path):
    """Three lanes by KIND: checks above, artefacts in the middle, tools below."""
    a = Atom("chain-v2a", 1600, 810)
    a.text("title", 45, 58, "Two things people write are brought into Lean, where the proof is", 30, INK, "start", 1500)
    a.zone("checks", 30, 88, 1540, 232, "Checks")
    a.zone("artefacts", 30, 332, 1540, 150, "Artefacts")
    a.zone("tools", 30, 494, 1540, 186, "Tools")
    W, H, CY = 214, 84, 420
    cx = [152 + 260 * i for i in range(6)]
    top, bot = CY - H / 2, CY + H / 2
    names = ["rule", "reading", "statement", "model", "source", "binary"]
    labels = ["English rule", "Reading", "Lean statement", "Lean model", "Rust source", "Running code"]
    # tools (drawn first so arrows sit under nothing)
    PY = 588
    a.path("compile.in", [(cx[0], bot), (cx[0], PY), (cx[1] - 132, PY)], frm="rule", to="compiler")
    a.path("compile.reading", [(cx[1], PY - 28), (cx[1], bot)], frm="compiler", to="reading")
    a.path("compile.statement", [(cx[1] + 132, PY), (cx[2], PY), (cx[2], bot)], frm="compiler", to="statement")
    a.path("translate.in", [(cx[4] - 30, bot), (cx[4] - 30, PY), (cx[3] + 85, PY)], frm="source", to="translator")
    a.path("translate.out", [(cx[3], PY - 28), (cx[3], bot)], frm="translator", to="model")
    a.path("rustc.in", [(cx[4] + 30, bot), (cx[4] + 30, PY), (cx[5] - 100, PY)], frm="source", to="rustc")
    a.path("rustc.out", [(cx[5], PY - 28), (cx[5], bot)], frm="rustc", to="binary")
    a.pill("compiler", cx[1], PY, 264, 56, PGREEN, "Sentence compiler")
    a.pill("translator", cx[3], PY, 170, 56, PBLUE, "Translator")
    a.pill("rustc", cx[5], PY, 200, 56, PGREY, "Rust compiler")
    a.text("compiler.tag", cx[1], 650, "output is checked", 17, GREEN, "middle", 230)
    a.text("translator.tag", cx[3], 650, "trusted tool", 17, BLUE, "middle", 170)
    a.text("rustc.tag", cx[5], 650, "trusted", 17, GREY, "middle", 170)
    # checks
    DY, DW, DH = 196, 220, 128
    def check(id, g, col, lines, tag, right=None, w=DW, h=DH):
        lx, rx = g - w / 2, g + w / 2
        a.line(f"{id}.leg.left", lx, DY, lx, top, col, 3)
        if right is None:
            a.line(f"{id}.leg.right", rx, DY, rx, top, col, 3)
        else:
            a.path(f"{id}.leg.right", [(rx, DY), (right, DY), (right, top)], col, 3, head=False)
        a.diamond(id, g, DY, w, h, col, lines)
        a.text(f"{id}.tag", g, DY + h / 2 + 30, tag, 17, col, "middle", w - 40)
    check("meaning", 282, AMBER, ["Author", "confirms"], "human-asserted")
    check("typecheck", 542, GREEN, ["Lean", "type-checks"], "machine-checked")
    check("proof", 802, GREEN, ["Kernel", "checks proof"], "kernel-checked")
    check("crosscheck", 1062, BLUE, ["Same inputs", "run on both"], "tested", right=cx[5] - 20)
    a.text("nocheck", 1322, 290, "compiler: no check", 17, GREY, "middle", 200)
    for i in range(6):
        a.box(names[i], cx[i], CY, W, H, labels[i])
    a.legend(45, 722)
    a.write(path)


def chain_v2b(path):
    """Zones by LAYER: requirement (left) and code (right) descend and meet in Lean."""
    a = Atom("chain-v2b", 1600, 870)
    a.text("title", 45, 58, "Two things people write are brought into Lean, where the proof is", 30, INK, "start", 1500)
    a.zone("requirement", 40, 90, 700, 350, "Requirement")
    a.zone("code", 860, 90, 700, 350, "Code", lx=1542, anchor="end")
    a.zone("lean", 40, 460, 1190, 240, "Lean")
    W, H = 214, 84
    T, M, B = 190, 345, 580          # row centres
    LX, RX, SX, BX = 250, 560, 1060, 1400
    # requirement side
    a.path("compile.in", [(LX, T + H / 2), (LX, M - 28)], frm="rule", to="compiler")
    a.path("compile.reading", [(LX + 132, M), (RX - W / 2, M)], frm="compiler", to="reading")
    a.path("compile.statement", [(LX, M + 28), (LX, B - H / 2)], frm="compiler", to="statement")
    a.line("meaning.leg.rule", LX + W / 2, T, RX - 110, T, AMBER, 3)
    a.line("meaning.leg.reading", RX, T + 64, RX, M - H / 2, AMBER, 3)
    a.diamond("meaning", RX, T, 220, 128, AMBER, ["Author", "confirms"])
    a.text("meaning.tag", RX + 16, T + 86, "human-asserted", 17, AMBER, "start", 160)
    a.pill("compiler", LX, M, 264, 56, PGREEN, "Sentence compiler")
    a.text("compiler.tag", LX + 16, M + 62, "output is checked", 17, GREEN, "start", 190)
    # code side
    a.path("translate.in", [(SX, T + H / 2), (SX, M - 28)], frm="source", to="translator")
    a.path("translate.out", [(SX, M + 28), (SX, B - H / 2)], frm="translator", to="model")
    a.path("rustc.in", [(SX + W / 2, T), (BX - 100, T)], frm="source", to="rustc")
    a.path("rustc.out", [(BX, T + 28), (BX, M - H / 2)], frm="rustc", to="binary")
    a.pill("translator", SX, M, 170, 56, PBLUE, "Translator")
    a.text("translator.tag", SX + 16, M + 62, "trusted tool", 17, BLUE, "start", 150)
    a.pill("rustc", BX, T, 200, 56, PGREY, "Rust compiler")
    a.text("rustc.tag", BX - 16, T + 64, "trusted, no check", 17, GREY, "end", 180)
    # Lean row
    PX = (LX + SX) / 2
    a.line("proof.leg.statement", LX + W / 2, B, PX - 130, B, GREEN, 3)
    a.line("proof.leg.model", PX + 130, B, SX - W / 2, B, GREEN, 3)
    a.diamond("proof", PX, B, 260, 150, GREEN, ["Kernel", "checks proof"], 20)
    a.text("proof.tag", PX, B + 104, "kernel-checked", 17, GREEN, "middle", 200)
    a.line("crosscheck.leg.model", SX + W / 2, B, BX - 110, B, BLUE, 3)
    a.line("crosscheck.leg.binary", BX, B - 64, BX, M + H / 2, BLUE, 3)
    a.diamond("crosscheck", BX, B, 220, 128, BLUE, ["Same inputs", "run on both"])
    a.text("crosscheck.tag", BX, B + 92, "tested", 17, BLUE, "middle", 150)
    for id, x, y, lab in (("rule", LX, T, "English rule"), ("reading", RX, M, "Reading"), ("statement", LX, B, "Lean statement"),
                          ("model", SX, B, "Lean model"), ("source", SX, T, "Rust source"), ("binary", BX, M, "Running code")):
        a.box(id, x, y, W, H, lab)
    a.legend(45, 762)
    a.write(path)


def shapes_demo(path, native_only=False):
    a = Atom("shapes-demo" if not native_only else "shapes-demo-native", 1600, 700 if not native_only else 400)
    a.text("title", 45, 56, "Vector180 0.1: arrows, diamonds and other shapes", 30, INK, "start", 1500)
    a.text("row.native", 45, 112, "Native only: straight lines, rect, circle, text. Compiles to editable PowerPoint objects.", 20, MUTED, "start", 1500)
    y = 220
    a.box("n.from", 120, y, 150, 70, "from", 20)
    a.box("n.to", 420, y, 150, 70, "to", 20)
    a.path("n.arrow", [(195, y), (345, y)], frm="n.from", to="n.to")
    a.text("n.arrow.cap", 270, 330, "arrow: 1 line + 2 head lines", 17, MUTED, "middle", 330)
    a.path("n.elbow", [(560, y - 50), (640, y - 50), (640, y + 50), (720, y + 50)])
    a.text("n.elbow.cap", 640, 330, "elbow: 3 lines + head", 17, MUTED, "middle", 250)
    a.diamond("n.diamond", 900, y, 200, 120, GREEN, ["Check", "passes?"])
    a.text("n.diamond.cap", 900, 330, "diamond: 4 lines, no fill", 17, MUTED, "middle", 250)
    hx, hw, hh = 1150, 200, 100
    a.open("n.hex")
    a.poly("n.hex", [(hx - hw / 2, y), (hx - hw / 2 + 30, y - hh / 2), (hx + hw / 2 - 30, y - hh / 2), (hx + hw / 2, y), (hx + hw / 2 - 30, y + hh / 2), (hx - hw / 2 + 30, y + hh / 2)], BLUE)
    a.text("n.hex.label", hx, y + 7, "Hexagon", 20, INK, "middle", 130)
    a.close()
    a.text("n.hex.cap", hx, 330, "hexagon: 6 lines, no fill", 17, MUTED, "middle", 250)
    a.pill("n.pill", 1420, y, 200, 60, PGREEN, "Pill", 20)
    a.text("n.pill.cap", 1420, 330, "pill: rect + 2 circles, no outline", 17, MUTED, "middle", 290)
    if not native_only:
        a.text("row.asset", 45, 420, "Asset groups (role asset, export svg): any SVG inside. Valid and resolvable; refused by compile today.", 20, MUTED, "start", 1500)
        y = 530
        A = 'data-vector180-role="asset" data-vector180-export="svg"'
        a.raw(f'<g id="shapes-demo.a.arrow" {A} data-vector180-bounds="60 {y - 60} 420 120">'
              f'<defs><marker id="shapes-demo.a.arrow.marker" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L12 6 L0 12 Z" fill="{LINE}"/></marker></defs>'
              f'<path d="M70 {y + 40} C 170 {y + 40}, 170 {y - 40}, 270 {y - 40} L 300 {y - 40}" fill="none" stroke="{LINE}" stroke-width="2.5" marker-end="url(#shapes-demo.a.arrow.marker)"/>'
              f'<line x1="330" y1="{y + 20}" x2="456" y2="{y + 20}" stroke="{LINE}" stroke-width="2.5" stroke-dasharray="8 6"/>'
              f'<polygon points="470,{y + 20} 454,{y + 12} 454,{y + 28}" fill="{LINE}"/></g>')
        a.text("a.arrow.cap", 270, 640, "curve, marker, dashes, filled head", 17, MUTED, "middle", 330)
        a.open("a.diamond")
        a.raw(f'<g id="shapes-demo.a.diamond.art" {A} data-vector180-bounds="798 {y - 62} 204 124"><polygon points="800,{y} 900,{y - 60} 1000,{y} 900,{y + 60}" fill="{PGREEN}" stroke="{GREEN}" stroke-width="3" stroke-linejoin="round"/></g>')
        a.text("a.diamond.l1", 900, y - 5, "Check", 19, INK, "middle", 110)
        a.text("a.diamond.l2", 900, y + 20, "passes?", 19, INK, "middle", 110)
        a.close()
        a.text("a.diamond.cap", 900, 640, "filled diamond + native text", 17, MUTED, "middle", 250)
        a.open("a.hex")
        a.raw(f'<g id="shapes-demo.a.hex.art" {A} data-vector180-bounds="{hx - 102} {y - 52} 204 104"><path d="M{hx - 100} {y} L{hx - 70} {y - 50} L{hx + 70} {y - 50} L{hx + 100} {y} L{hx + 70} {y + 50} L{hx - 70} {y + 50} Z" fill="{PBLUE}" stroke="{BLUE}" stroke-width="3" stroke-linejoin="round"/></g>')
        a.text("a.hex.label", hx, y + 7, "Hexagon", 20, INK, "middle", 130)
        a.close()
        a.text("a.hex.cap", hx, 640, "filled hexagon + native text", 17, MUTED, "middle", 250)
        a.open("a.round")
        a.rect("a.round.box", 1320, y - 35, 200, 70, "#ffffff", INK, 2.5)
        a.out[-1] = a.out[-1].replace(' fill=', ' rx="16" ry="16" fill=')
        a.text("a.round.label", 1420, y + 7, "rect rx", 20, INK, "middle", 150)
        a.close()
        a.text("a.round.cap", 1420, 640, "native rect with rx: also no compile", 17, MUTED, "middle", 330)
    a.write(path)


if __name__ == "__main__":
    out = sys.argv[1]
    shapes_demo(os.path.join(out, "shapes-demo.vector180.svg"))
    shapes_demo(os.path.join(out, "shapes-demo-native.vector180.svg"), native_only=True)
    chain_v2a(os.path.join(out, "chain-v2a.vector180.svg"))
    chain_v2b(os.path.join(out, "chain-v2b.vector180.svg"))
