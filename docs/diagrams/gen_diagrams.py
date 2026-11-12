#!/usr/bin/env python3
"""Deterministic generator for Clausal & Clausebook Vector180 0.1 diagrams.

Generates strictly native Vector180 0.1 SVG atoms (rect without rx, circle,
straight line, text in ABeeZee, group) on integer or half-unit coordinates:
  - how-it-works.vector180.svg (Hero: Clausal rule -> Lean 4 + cargo clausal test)
  - chain.vector180.svg        (Five-link Symmetric H-Bridge Meet-in-the-Middle)
  - vocabulary.vector180.svg   (The Clausebook public library & dual bindings)
  - compiler.vector180.svg     (Inside the Clausal compiler -> dual Lean/Rust targets)
  - evidence.vector180.svg     (Clausal compiler -> 4 graded tiers of evidence)
  - (optional) chain-spine.vector180.svg when --include-alt is passed

Usage:
    python3 docs/diagrams/gen_diagrams.py docs/diagrams
"""
import os
import sys

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

INK = "#17211e"
MUTED = "#4b5a55"
LINE = "#3f4f49"
ZONE = "#f1f4f2"
ZONE_GREEN = "#ebf5f0"
ZONE_BLUE = "#ebf2fa"
ZONE_AMBER = "#fcf6e8"
ZLAB = "#5c6b66"
BORDER = "#8c9994"

GREEN = "#1f7a5c"
PGREEN = "#dff1e8"
RED = "#b3402b"
PRED = "#fbe7e3"
AMBER = "#b7791f"
PAMBER = "#fdf1d8"
BLUE = "#2b5c9e"
PBLUE = "#e3edf9"
PURPLE = "#6a4aa3"
PPURPLE = "#efe9f8"
TEAL = "#1d6f7a"
PTEAL = "#def0f2"
GREY = "#6e7b76"
PGREY = "#e6eae8"
GOLD = "#d9a520"


def fmt(v):
    v = round(v * 2) / 2
    return str(int(v)) if v == int(v) else f"{v:.1f}"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Atom:
    def __init__(self, atom_id, w, h):
        self.id = atom_id
        self.w = w
        self.h = h
        self.out = []
        self.rect("background", 0, 0, w, h, "#ffffff", "none", 0)

    def open(self, gid):
        self.out.append(f'<g id="{self.id}.{gid}" data-vector180-role="group" {N}>')

    def close(self):
        self.out.append("</g>")

    def rect(self, rid, x, y, w, h, fill, stroke="none", sw=3):
        st = f'stroke="{stroke}" stroke-width="{fmt(sw)}"' if stroke != "none" else 'stroke="none"'
        self.out.append(
            f'<rect id="{self.id}.{rid}" data-vector180-role="shape" {N} '
            f'x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" fill="{fill}" {st}/>'
        )

    def circle(self, cid, cx, cy, r, fill, stroke="none", sw=2):
        st = f'stroke="{stroke}" stroke-width="{fmt(sw)}"' if stroke != "none" else 'stroke="none"'
        self.out.append(
            f'<circle id="{self.id}.{cid}" data-vector180-role="shape" {N} '
            f'cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(r)}" fill="{fill}" {st}/>'
        )

    def text_box(self, tid, x, y, w, s, size=20, fill=INK, anchor="start"):
        x, y, w = int(round(x)), int(round(y)), int(round(w))
        h = int(round(size * 1.5))
        base = y + int(round(size * 1.08))
        tx = x if anchor == "start" else (x + w // 2 if anchor == "middle" else x + w)
        self.out.append(
            f'<text id="{self.id}.{tid}" data-vector180-role="text" {N} '
            f'data-vector180-frame="{x} {y} {w} {h}" data-vector180-line-step="{h}" '
            f'x="{tx}" y="{base}" fill="{fill}" stroke="none" '
            f'font-family="ABeeZee" font-size="{size}" font-weight="400" '
            f'font-style="normal" text-anchor="{anchor}">{esc(s)}</text>'
        )

    def line(self, lid, x1, y1, x2, y2, stroke=LINE, sw=3, frm=None, to=None):
        ft = ""
        if frm and to:
            ft = f' data-vector180-from="{self.id}.{frm}" data-vector180-to="{self.id}.{to}"'
        self.out.append(
            f'<line id="{self.id}.{lid}" data-vector180-role="connector" {N}{ft} '
            f'x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}" '
            f'stroke="{stroke}" stroke-width="{fmt(sw)}"/>'
        )

    def arrow(self, aid, x1, y1, x2, y2, stroke=LINE, sw=3, k=9, frm=None, to=None):
        self.open(aid)
        self.line(f"{aid}.shaft", x1, y1, x2, y2, stroke, sw, frm=frm, to=to)
        if x1 == x2:
            d = 1 if y2 > y1 else -1
            self.line(f"{aid}.head1", x2 - k, y2 - d * k, x2, y2, stroke, sw)
            self.line(f"{aid}.head2", x2 + k, y2 - d * k, x2, y2, stroke, sw)
        else:
            d = 1 if x2 > x1 else -1
            self.line(f"{aid}.head1", x2 - d * k, y2 - k, x2, y2, stroke, sw)
            self.line(f"{aid}.head2", x2 - d * k, y2 + k, x2, y2, stroke, sw)
        self.close()

    def elbow_arrow(self, aid, pts, stroke=LINE, sw=3, head=True, k=9, frm=None, to=None):
        self.open(aid)
        n = len(pts) - 1
        for i in range(n):
            (x1, y1), (x2, y2) = pts[i], pts[i + 1]
            ex2, ey2 = x2, y2
            if i < n - 1:
                if x1 == x2:
                    ey2 = y2 + (1.5 if y2 > y1 else -1.5)
                else:
                    ex2 = x2 + (1.5 if x2 > x1 else -1.5)
            self.line(
                f"{aid}.s{i+1}",
                x1,
                y1,
                ex2,
                ey2,
                stroke,
                sw,
                frm=frm if i == 0 else None,
                to=to if i == 0 else None,
            )
        if head:
            (x1, y1), (x2, y2) = pts[-2], pts[-1]
            if x1 == x2:
                d = 1 if y2 > y1 else -1
                self.line(f"{aid}.h1", x2 - k, y2 - d * k, x2, y2, stroke, sw)
                self.line(f"{aid}.h2", x2 + k, y2 - d * k, x2, y2, stroke, sw)
            else:
                d = 1 if x2 > x1 else -1
                self.line(f"{aid}.h1", x2 - d * k, y2 - k, x2, y2, stroke, sw)
                self.line(f"{aid}.h2", x2 - d * k, y2 + k, x2, y2, stroke, sw)
        self.close()

    def diamond(self, did, cx, cy, hw, hh, stroke=LINE, sw=3):
        self.open(did)
        pts = [(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy)]
        for i in range(4):
            (xa, ya), (xb, yb) = pts[i], pts[(i + 1) % 4]
            self.line(f"{did}.e{i+1}", xa, ya, xb, yb, stroke, sw)
        self.close()

    def pill(self, pid, cx, cy, w, h, fill, label="", size=18, ink=INK):
        r = h // 2
        self.open(pid)
        self.rect(f"{pid}.body", cx - w // 2 + r, cy - r, w - h, h, fill, "none")
        self.circle(f"{pid}.capl", cx - w // 2 + r, cy, r, fill)
        self.circle(f"{pid}.capr", cx + w // 2 - r, cy, r, fill)
        if label:
            fw = w - h + 14
            self.text_box(f"{pid}.label", cx - fw // 2, cy - int(round(size * 0.72)), fw, label, size, ink, "middle")
        self.close()

    def pill2(self, pid, cx, cy, w, h, fill, l1, l2, s1=16, s2=14, ink1=INK, ink2=MUTED):
        r = h // 2
        self.open(pid)
        self.rect(f"{pid}.body", cx - w // 2 + r, cy - r, w - h, h, fill, "none")
        self.circle(f"{pid}.capl", cx - w // 2 + r, cy, r, fill)
        self.circle(f"{pid}.capr", cx + w // 2 - r, cy, r, fill)
        fw = w - h + 16
        self.text_box(f"{pid}.l1", cx - fw // 2, cy - int(round(s1 * 1.45)), fw, l1, s1, ink1, "middle")
        self.text_box(f"{pid}.l2", cx - fw // 2, cy + 1, fw, l2, s2, ink2, "middle")
        self.close()

    def num_badge(self, bid, cx, cy, num_str, fill_col, r=18):
        self.open(bid)
        self.circle(f"{bid}.c", cx, cy, r, fill_col)
        self.text_box(f"{bid}.t", cx - 16, cy - 14, 32, num_str, 20, "#ffffff", "middle")
        self.close()

    def legend_footer(self, ly1=764, ly2=808):
        self.text_box("leg.k", 40, ly1, 60, "Key:", 18, ZLAB)
        self.rect("leg.box", 104, ly1 + 2, 38, 22, "#ffffff", INK, 2.5)
        self.text_box("leg.box.t", 150, ly1, 100, "artefact", 18, MUTED)

        self.pill("leg.pill", 286, ly1 + 13, 52, 24, PGREY, "")
        self.arrow("leg.arr", 318, ly1 + 13, 350, ly1 + 13, LINE, 2.5, k=7)
        self.text_box("leg.pill.t", 360, ly1, 230, "tool / compiler", 18, MUTED)

        self.diamond("leg.dia", 604, ly1 + 13, 22, 14, INK, 2.5)
        self.text_box("leg.dia.t", 636, ly1, 230, "verification check", 18, MUTED)

        self.num_badge("leg.num", 898, ly1 + 13, "N", GREEN, r=17)
        self.text_box("leg.num.lbl", 926, ly1, 420, "numbered link (matches table 1-5)", 18, MUTED)

        self.text_box("leg.r", 40, ly2, 110, "Evidence:", 18, ZLAB)
        chips = [
            ("human", 156, 330, AMBER, "1: human-asserted (Clausebook)"),
            ("kernel", 518, 290, GREEN, "2, 3: kernel-checked (Lean 4)"),
            ("tested", 834, 372, BLUE, "4, 5: tool-trusted + tested on binary"),
            ("trusted", 1240, 280, GREY, "rustc / ISA: assumed"),
        ]
        for ck, cx0, cw0, ccol, clab in chips:
            self.rect(f"leg.c.{ck}", cx0, ly2 + 4, 18, 18, ccol, "none")
            self.text_box(f"leg.t.{ck}", cx0 + 26, ly2, cw0, clab, 18, MUTED)

    def write(self, path):
        body = "\n  ".join(self.out)
        svg = (
            f'{HEADER}<svg xmlns="http://www.w3.org/2000/svg" data-vector180-version="0.1"\n'
            f'  id="{self.id}" viewBox="0 0 {self.w} {self.h}">\n'
            f'  <metadata data-vector180-metadata="vector180-atom-metadata/0.1">'
            f'{{"styleFamily":{{"id":"office180.vector180.default","version":"1.0"}}}}</metadata>\n'
            f"  {body}\n</svg>\n"
        )
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(svg)


# ==============================================================================
# 1. Hero Figure: how-it-works.vector180.svg
# ==============================================================================
def build_how_it_works(out_dir):
    a = Atom("howitworks", 1600, 900)
    a.text_box("title", 40, 24, 1520, "Clausal: formal-English Gherkin dual-bound to Lean proofs and Rust tests", 31, INK)

    ZY, ZH = 96, 672
    zones = [
        ("gherkin", 40, 440, "CLAUSAL (.FEATURE)", "Formal-English Gherkin.", "Composed from the Clausebook."),
        ("lean", 520, 560, "LEAN 4 KERNEL & AUDIT", "Small trusted proof checker.", "Polices statements, proofs & witnesses."),
        ("rust", 1120, 440, "PRODUCTION CODE", "Profiled Rust (or polyglot target).", "Runs cucumber-rs BDD & ships to prod."),
    ]
    for k, x, w, name, s1, s2 in zones:
        a.rect(f"{k}.zone", x, ZY, w, ZH, ZONE)
        a.text_box(f"{k}.name", x + 24, ZY + 18, w - 48, name, 24, INK)
        a.text_box(f"{k}.sub1", x + 24, ZY + 58, w - 48, s1, 18, MUTED)
        a.text_box(f"{k}.sub2", x + 24, ZY + 84, w - 48, s2, 18, MUTED)

    R1 = 244
    a.rect("rule.box", 66, R1, 388, 140, "#ffffff", LINE, 3)
    a.text_box("rule.label", 86, R1 + 12, 348, "Clausal rule (features/*.feature)", 17, MUTED)
    a.text_box("rule.l1", 86, R1 + 44, 348, '"Every transfer, accepted or', 20, INK)
    a.text_box("rule.l2", 86, R1 + 74, 348, 'rejected, keeps total balance."', 20, INK)
    a.text_box("rule.l3", 86, R1 + 108, 348, "dual-binds to Lean 4 + cucumber-rs", 16, AMBER)

    a.rect("code.box", 1146, R1, 388, 140, "#ffffff", LINE, 3)
    a.text_box("code.label", 1166, R1 + 12, 348, "Implementation under check", 17, MUTED)
    a.text_box("code.l1", 1166, R1 + 44, 348, "fn transfer(from, to, amount)", 21, INK)
    a.text_box("code.l2", 1166, R1 + 76, 348, "or ABAC decide(req, snap)", 20, INK)
    a.text_box("code.l3", 1166, R1 + 108, 348, "and every helper it calls", 16, MUTED)

    a.rect("statement.box", 548, R1, 232, 140, "#ffffff", GREEN, 3)
    a.text_box("statement.label", 556, R1 + 12, 216, "from Clausebook", 16, MUTED, "middle")
    a.text_box("statement.l1", 556, R1 + 46, 216, "Exact Lean", 24, INK, "middle")
    a.text_box("statement.l2", 556, R1 + 80, 216, "statement", 24, INK, "middle")

    a.rect("model.box", 820, R1, 232, 140, "#ffffff", BLUE, 3)
    a.text_box("model.label", 828, R1 + 12, 216, "extracted via Aeneas", 16, MUTED, "middle")
    a.text_box("model.l1", 828, R1 + 46, 216, "Exact Lean", 24, INK, "middle")
    a.text_box("model.l2", 828, R1 + 80, 216, "model", 24, INK, "middle")

    a.arrow("rule.to.statement", 454, R1 + 70, 544, R1 + 70, GREEN, 3, k=11, frm="rule.box", to="statement.box")
    a.arrow("code.to.model", 1146, R1 + 70, 1056, R1 + 70, BLUE, 3, k=11, frm="code.box", to="model.box")
    a.text_box("flow.left1", 450, R1 + 82, 98, "Clausal", 15, GREEN, "middle")
    a.text_box("flow.left2", 450, R1 + 100, 98, "compiler", 15, GREEN, "middle")
    a.text_box("flow.right", 1056, R1 + 84, 90, "Aeneas", 16, BLUE, "middle")

    CX, CY, HW, HH = 800, 510, 224, 94
    a.diamond("question", CX, CY, HW, HH, LINE, 3)
    a.text_box("question.l1", CX - 156, CY - 34, 312, "Does the code obey", 20, INK, "middle")
    a.text_box("question.l2", CX - 156, CY - 4, 312, "the rule on every input?", 20, INK, "middle")

    def edge_y(x, upper):
        t = 1.0 - abs(x - CX) / HW
        val = (CY - t * HH) if upper else (CY + t * HH)
        return int(round(val))

    a.arrow("statement.to.q", 664, R1 + 140, 664, edge_y(664, True) - 4, LINE, 3, k=11)
    a.arrow("model.to.q", 936, R1 + 140, 936, edge_y(936, True) - 4, LINE, 3, k=11)

    AY, AH = 652, 92
    a.rect("yes.box", 544, AY, 240, AH, PGREEN, GREEN, 3)
    a.circle("yes.seal", 580, AY + 46, 16, GOLD)
    a.text_box("yes.title", 608, AY + 10, 168, "PROVED", 25, GREEN)
    a.text_box("yes.sub", 608, AY + 50, 168, "for every input", 17, MUTED)

    a.rect("no.box", 816, AY, 244, AH, PRED, RED, 3)
    a.text_box("no.title", 834, AY + 10, 216, "REFUTED", 25, RED)
    a.text_box("no.sub", 834, AY + 50, 216, "concrete failing case", 17, MUTED)

    a.arrow("q.to.yes", 664, edge_y(664, False) + 4, 664, AY - 4, GREEN, 3, k=11)
    a.arrow("q.to.no", 938, edge_y(938, False) + 4, 938, AY - 4, RED, 3, k=11)

    a.rect("answer.box", 66, AY - 14, 388, 120, "#ffffff", GREEN, 3)
    a.circle("answer.seal", 102, AY + 46, 16, GOLD)
    a.text_box("answer.l1", 130, AY + 2, 310, "Clausal verdict + report:", 19, INK)
    a.text_box("answer.l2", 130, AY + 32, 310, "names every assumption,", 18, MUTED)
    a.text_box("answer.l3", 130, AY + 60, 310, "axiom, bound & sign-off.", 18, MUTED)
    a.arrow("yes.to.answer", 544, AY + 46, 458, AY + 46, GREEN, 3, k=11, frm="yes.box", to="answer.box")

    a.rect("confirm.box", 1146, AY - 14, 388, 120, "#ffffff", BLUE, 3)
    a.text_box("confirm.l1", 1166, AY + 2, 348, "Dual-bound on compiled Rust:", 19, INK)
    a.text_box("confirm.l2", 1166, AY + 32, 348, "runs .feature via cucumber-rs", 18, MUTED)
    a.text_box("confirm.l3", 1166, AY + 60, 348, "& replays any counterexample.", 18, MUTED)
    a.arrow("code.to.confirm", 1340, R1 + 140, 1340, AY - 18, BLUE, 3, k=11, frm="code.box", to="confirm.box")
    a.pill("code.bdd.pill", 1340, 510, 214, 38, PBLUE, "cargo clausal test", 16, BLUE)
    a.arrow("no.to.confirm", 1060, AY + 46, 1142, AY + 46, RED, 3, k=11, frm="no.box", to="confirm.box")

    a.text_box(
        "foot1",
        40,
        792,
        1520,
        "Clausal (clausal compose) builds canonical .feature rules that run as BDD tests today and compile to Lean proofs.",
        20,
        MUTED,
    )
    a.text_box(
        "foot2",
        40,
        824,
        1520,
        "Unbound phrases are refused; vacuous rules and spec-gaming proofs are caught by automated Lean audit gates.",
        20,
        MUTED,
    )
    a.write(os.path.join(out_dir, "how-it-works.vector180.svg"))


# ==============================================================================
# 2. Five-Link Loop (Symmetric H-Bridge Meet-in-the-Middle): chain.vector180.svg
# ==============================================================================
def build_chain(out_dir):
    a = Atom("chain", 1600, 860)
    a.text_box("title", 40, 18, 1520, "The Clausal five-link loop: intent from the left, Rust from the right, verdict at center", 28, INK)
    a.text_box(
        "subtitle",
        40,
        56,
        1520,
        "Human policy and shipping code march inward to meet in Lean 4 (above) and binary BDD & replay (below).",
        19,
        MUTED,
    )

    a.rect("z.top", 332, 104, 936, 164, ZONE_GREEN)
    a.text_box("z.top.lbl", 350, 112, 420, "UPPER BRIDGE: UNBOUNDED PROOF (LEAN 4)", 16, GREEN)

    a.rect("z.left", 28, 336, 584, 186, ZONE)
    a.text_box("z.left.lbl", 44, 344, 200, "SPECIFICATION", 16, ZLAB)

    a.rect("z.right", 988, 336, 584, 186, ZONE)
    a.text_box("z.right.lbl", 1340, 344, 216, "IMPLEMENTATION", 16, ZLAB, "end")

    a.rect("z.bot", 332, 588, 936, 152, ZONE_BLUE)
    a.text_box("z.bot.lbl", 350, 712, 460, "LOWER BRIDGE: DUAL-BOUND BDD, FUZZ & REPLAY", 16, BLUE)

    EQY = 432
    UY = 200
    LY = 652

    # Left Equator
    a.rect("intent.box", 44, EQY - 46, 148, 92, "#ffffff", BORDER, 2.5)
    a.text_box("intent.t1", 52, EQY - 32, 132, "Domain", 20, INK, "middle")
    a.text_box("intent.t2", 52, EQY - 6, 132, "Intent", 20, INK, "middle")
    a.text_box("intent.t3", 52, EQY + 20, 132, "policy / rule", 15, MUTED, "middle")

    a.arrow("l1.arr", 192, EQY, 348, EQY, AMBER, 3, k=9, frm="intent.box", to="clausal.box")
    a.pill("l1.pill", 270, EQY - 30, 136, 32, PAMBER, "compose", 15, AMBER)
    a.num_badge("l1.num", 270, EQY - 66, "1", AMBER, r=17)
    a.text_box("l1.ev1", 196, EQY + 12, 148, "Clausebook", 15, AMBER, "middle")
    a.text_box("l1.ev2", 192, EQY + 32, 156, "(human-asserted)", 14, MUTED, "middle")

    a.rect("clausal.box", 352, EQY - 60, 240, 120, "#ffffff", INK, 3)
    a.text_box("clausal.t1", 364, EQY - 46, 216, "Clausal (.feature)", 22, INK, "middle")
    a.text_box("clausal.t2", 364, EQY - 14, 216, "canonical Gherkin", 17, GREEN, "middle")
    a.text_box("clausal.t3", 364, EQY + 18, 216, "dual-binds to Lean & Rust", 15, MUTED, "middle")

    # Right Equator
    a.rect("dev.box", 1408, EQY - 46, 148, 92, "#ffffff", BORDER, 2.5)
    a.text_box("dev.t1", 1416, EQY - 32, 132, "Engineer /", 19, INK, "middle")
    a.text_box("dev.t2", 1416, EQY - 6, 132, "AI Agent", 19, INK, "middle")
    a.text_box("dev.t3", 1416, EQY + 20, 132, "authors code", 15, MUTED, "middle")

    a.arrow("dev.arr", 1408, EQY, 1252, EQY, GREY, 3, k=9, frm="dev.box", to="rust.box")
    a.pill("dev.pill", 1330, EQY - 30, 116, 32, PGREY, "writes", 15, GREY)
    a.text_box("dev.ev1", 1254, EQY + 12, 152, "untrusted input", 15, GREY, "middle")
    a.text_box("dev.ev2", 1254, EQY + 32, 152, "(models propose)", 14, MUTED, "middle")

    a.rect("rust.box", 1008, EQY - 60, 240, 120, "#ffffff", INK, 3)
    a.text_box("rust.t1", 1020, EQY - 46, 216, "Rust Source Code", 22, INK, "middle")
    a.text_box("rust.t2", 1020, EQY - 14, 216, "crate + BDD steps", 17, BLUE, "middle")
    a.text_box("rust.t3", 1020, EQY + 18, 216, "(or polyglot target)", 15, MUTED, "middle")

    # Upper Vertical Risers
    a.arrow("l2.arr", 472, EQY - 60, 472, UY + 52, GREEN, 3, k=9, frm="clausal.box", to="stmt.box")
    a.pill("l2.pill", 472, 304, 198, 36, PGREEN, "Clausal compiler", 16, GREEN)
    a.num_badge("l2.num", 350, 304, "2", GREEN, r=18)

    a.arrow("l4.arr", 1128, EQY - 60, 1128, UY + 52, BLUE, 3, k=9, frm="rust.box", to="model.box")
    a.pill("l4.pill", 1128, 304, 192, 36, PBLUE, "Aeneas / Oracle", 16, BLUE)
    a.num_badge("l4.num", 1250, 304, "4", BLUE, r=18)

    # Upper Bridge
    a.rect("stmt.box", 352, UY - 48, 240, 96, "#ffffff", GREEN, 3)
    a.text_box("stmt.t1", 364, UY - 32, 216, "Lean Statement", 21, INK, "middle")
    a.text_box("stmt.t2", 364, UY + 6, 216, "fail-closed Prop", 16, MUTED, "middle")

    a.rect("model.box", 1008, UY - 48, 240, 96, "#ffffff", BLUE, 3)
    a.text_box("model.t1", 1020, UY - 32, 216, "Lean Code Model", 21, INK, "middle")
    a.text_box("model.t2", 1020, UY + 6, 216, "pure functions", 16, MUTED, "middle")

    a.arrow("l3.l", 592, UY, 688, UY, GREEN, 3, k=8)
    a.arrow("l3.r", 1008, UY, 912, UY, GREEN, 3, k=8)
    a.diamond("l3.dia", 800, UY, 108, 56, GREEN, 3.5)
    a.text_box("l3.t1", 720, UY - 24, 160, "Lean 4 Kernel", 18, INK, "middle")
    a.text_box("l3.t2", 720, UY + 2, 160, "+ Spec Audit", 17, GREEN, "middle")
    a.num_badge("l3.num", 800, 124, "3", GREEN, r=17)

    # Lower Vertical Drops
    a.arrow("l5.drop", 472, EQY + 60, 472, LY - 48, BLUE, 3, k=9, frm="clausal.box", to="bdd.box")
    a.pill("l5.dpill", 472, 554, 198, 36, PBLUE, "dual-bound BDD", 16, BLUE)
    a.num_badge("l5.num", 350, 554, "5", BLUE, r=18)

    a.arrow("rustc.drop", 1128, EQY + 60, 1128, LY - 48, GREY, 3, k=9, frm="rust.box", to="bin.box")
    a.pill("rustc.pill", 1128, 554, 168, 36, PGREY, "rustc + ISA", 16, GREY)
    a.text_box("rustc.ev", 1222, 542, 110, "assumed", 15, GREY)

    # Lower Bridge
    a.rect("bdd.box", 352, LY - 44, 240, 88, "#ffffff", BLUE, 3)
    a.text_box("bdd.t1", 364, LY - 30, 216, "cucumber + proptest", 19, BLUE, "middle")
    a.text_box("bdd.t2", 364, LY + 4, 216, "BDD rows & fuzzing", 16, MUTED, "middle")

    a.rect("bin.box", 1008, LY - 44, 240, 88, "#ffffff", INK, 3)
    a.text_box("bin.t1", 1020, LY - 30, 216, "Running Binary", 21, INK, "middle")
    a.text_box("bin.t2", 1020, LY + 4, 216, "compiled crate + tests", 16, MUTED, "middle")

    a.arrow("l5.l", 592, LY, 688, LY, BLUE, 3, k=8)
    a.arrow("l5.r", 1008, LY, 912, LY, BLUE, 3, k=8)
    a.diamond("l5.dia", 800, LY, 108, 54, BLUE, 3.5)
    a.text_box("l5.t1", 720, LY - 24, 160, "BDD & Replay", 18, INK, "middle")
    a.text_box("l5.t2", 720, LY + 2, 160, "match on binary", 16, BLUE, "middle")

    a.elbow_arrow("replay.ch", [(1008, UY + 28), (972, UY + 28), (972, LY - 28), (860, LY - 28)], BLUE, 2.5, head=True, k=8)
    a.text_box("replay.l1", 864, 520, 100, "witness", 15, BLUE, "end")
    a.text_box("replay.l2", 864, 540, 100, "replay", 15, BLUE, "end")

    # Central Verdict Bullseye
    a.rect("verdict.box", 646, EQY - 52, 308, 104, "#ffffff", GREEN, 3.5)
    a.circle("verdict.seal", 678, EQY, 15, GOLD)
    a.text_box("verdict.t1", 704, EQY - 38, 238, "CLAUSAL VERDICT", 21, INK)
    a.text_box("verdict.t2", 704, EQY - 8, 238, "Proved / Bounded / Refuted", 16, GREEN)
    a.text_box("verdict.t3", 704, EQY + 18, 238, "logs links 1-5 separately", 15, MUTED)

    a.arrow("v.top", 800, UY + 56, 800, EQY - 56, GREEN, 3, k=9)
    a.text_box("v.top.lbl", 636, 302, 152, "unbounded proof", 15, GREEN, "end")

    a.arrow("v.bot", 800, LY - 54, 800, EQY + 56, BLUE, 3, k=9)
    a.text_box("v.bot.lbl", 636, 530, 152, "tested on binary", 15, BLUE, "end")

    a.legend_footer()
    a.write(os.path.join(out_dir, "chain.vector180.svg"))


# ==============================================================================
# 3. Clausebook Public Library Figure: vocabulary.vector180.svg
# ==============================================================================
def build_vocabulary(out_dir):
    a = Atom("vocabulary", 1600, 890)
    a.text_box("title", 40, 22, 1520, "The Clausebook: typed pieces that make Clausal dual-bind to Lean and Rust", 31, INK)
    a.text_box(
        "subtitle",
        40,
        68,
        1520,
        "clausal compose builds canonical Clausal (.feature) from signed Clausebook pieces; projects bind only local nouns.",
        20,
        MUTED,
    )

    Y1 = 120
    a.text_box("r1.tag", 40, Y1 + 16, 190, "Project A (Ledger):", 19, MUTED, "end")
    segs1 = [
        ("r1.s1", 246, 144, "Internal", PPURPLE, PURPLE),
        ("r1.s2", 390, 220, "fund transfers", PBLUE, BLUE),
        ("r1.s3", 610, 220, "never change", PGREEN, GREEN),
        ("r1.s4", 830, 176, "aggregate", PPURPLE, PURPLE),
        ("r1.s5", 1006, 224, "account value", PTEAL, TEAL),
    ]
    for sid, sx, sw, stxt, sfill, sstroke in segs1:
        a.rect(f"{sid}.box", sx, Y1, sw, 58, sfill, sstroke, 2.5)
        a.text_box(f"{sid}.txt", sx + 6, Y1 + 13, sw - 12, stxt, 22, INK, "middle")
    a.pill("r1.reuse", 1400, Y1 + 29, 300, 42, PGREEN, "4 Clausebook + 1 local", 17, GREEN)

    Y2 = 194
    a.text_box("r2.tag", 40, Y2 + 16, 190, "Project B (ABAC):", 19, MUTED, "end")
    segs2 = [
        ("r2.s1", 246, 210, "Higher clearance", PTEAL, TEAL),
        ("r2.s2", 456, 260, "more-never-loses", PGREEN, GREEN),
        ("r2.s3", 716, 166, "accepted", PPURPLE, PURPLE),
        ("r2.s4", 882, 348, "key-release decision", PBLUE, BLUE),
    ]
    for sid, sx, sw, stxt, sfill, sstroke in segs2:
        a.rect(f"{sid}.box", sx, Y2, sw, 58, sfill, sstroke, 2.5)
        a.text_box(f"{sid}.txt", sx + 6, Y2 + 13, sw - 12, stxt, 22, INK, "middle")
    a.pill("r2.reuse", 1400, Y2 + 29, 300, 42, PGREEN, "3 Clausebook + 1 local", 17, GREEN)

    ZY, ZH = 282, 356
    a.rect("pub.zone", 40, ZY, 1140, ZH, ZONE, BORDER, 2)
    a.text_box("pub.label", 60, ZY + 12, 840, "CLAUSEBOOK PUBLIC LIBRARY (versioned, content-hashed, shared across projects)", 19, INK)
    a.pill("pub.badge", 1040, ZY + 25, 240, 34, PAMBER, "signed once per piece", 16, AMBER)

    a.rect("loc.zone", 1204, ZY, 356, ZH, ZONE, BORDER, 2)
    a.text_box("loc.label", 1222, ZY + 12, 320, "PER-PROJECT BINDINGS", 19, INK)
    a.text_box("loc.sub", 1222, ZY + 38, 320, "dual-bound to Lean & Rust", 16, MUTED)

    CY, CH = 348, 270
    cards = [
        (
            "frames",
            60,
            352,
            PGREEN,
            GREEN,
            "1. Core Frames",
            "universal logical shapes",
            [
                "never changes, always,",
                "only if, exactly when,",
                "more never loses, at most,",
                "independent of, agrees with",
                "",
                "Fail-closed by construction.",
            ],
        ),
        (
            "modifiers",
            432,
            352,
            PPURPLE,
            PURPLE,
            "2. Modifiers",
            "typed piece transformers",
            [
                "internal, aggregate,",
                "accepted, rejected,",
                "bystander, given, then",
                "",
                "Narrow, sum, or filter",
                "without raw Prop escapes.",
            ],
        ),
        (
            "packs",
            804,
            356,
            PTEAL,
            TEAL,
            "3. Domain Packs",
            "reusable domain clauses",
            [
                "clausebook/abac: dominance,",
                "  allOf, anyOf, Permit / Dek",
                "clausebook/ledger: balances",
                "clausebook/quota: epochs",
                "",
                "+ kernel @[step] proof lemmas.",
            ],
        ),
        (
            "local",
            1222,
            320,
            PBLUE,
            BLUE,
            "4. Dual Bindings",
            "Lean model + Rust BDD",
            [
                "Ledger::transfer",
                "Kas::decide_release",
                "",
                "Binds nouns & ops once to",
                "both Aeneas Lean models",
                "and cucumber-rs / proptest.",
            ],
        ),
    ]
    centers = []
    for cid, cx, cw, cfill, cstroke, ctitle, csub, clines in cards:
        a.rect(f"card.{cid}.box", cx, CY, cw, CH, "#ffffff", cstroke, 3)
        a.rect(f"card.{cid}.hdr", cx, CY, cw, 66, cfill, cstroke, 2)
        a.text_box(f"card.{cid}.title", cx + 16, CY + 8, cw - 32, ctitle, 23, INK)
        a.text_box(f"card.{cid}.sub", cx + 16, CY + 38, cw - 32, csub, 16, cstroke)
        for idx, ln in enumerate(clines):
            if ln:
                a.text_box(f"card.{cid}.l{idx+1}", cx + 16, CY + 78 + idx * 29, cw - 32, ln, 18, MUTED)
        centers.append((cid, cx + cw // 2, cstroke))

    BY, BH = 682, 184
    a.rect("compiled.box", 40, BY, 1520, BH, "#ffffff", LINE, 3)
    for cid, midx, cstroke in centers:
        a.arrow(f"to.compiled.{cid}", midx, CY + CH, midx, BY - 4, cstroke, 3, k=11, frm=f"card.{cid}.box", to="compiled.box")

    a.text_box("compiled.hdr", 64, BY + 12, 860, "CANONICAL CLAUSAL (.FEATURE) + DUAL BINDING (LEAN 4 + CUCUMBER-RS)", 19, GREEN)
    a.pill("compiled.check", 1300, BY + 29, 460, 36, PGREEN, "conformance-checked across Lean & Rust", 16, GREEN)
    a.text_box(
        "compiled.gherkin",
        64,
        BY + 50,
        1470,
        'Clausal (.feature): "Rule: Every internal fund transfer, accepted or rejected, never changes aggregate account value."',
        19,
        INK,
    )
    a.text_box(
        "compiled.formula",
        64,
        BY + 86,
        1470,
        "Lean 4 Prop: Clausebook.NeverChanges.at (Clausebook.internal Ledger.transfer) (Clausebook.aggregate Ledger.balance)",
        19,
        GREEN,
    )
    a.text_box(
        "compiled.bdd",
        64,
        BY + 120,
        1470,
        "Rust BDD + Fuzz: executes Scenario tables via cucumber-rs and checks Rule invariants via proptest on compiled Rust.",
        19,
        BLUE,
    )
    a.text_box(
        "compiled.gov",
        64,
        BY + 152,
        1470,
        "Clausebook governance: new @[step] lemmas need only Lean's kernel; changing meaning requires proved <-> or a new hash.",
        17,
        AMBER,
    )
    a.write(os.path.join(out_dir, "vocabulary.vector180.svg"))


# ==============================================================================
# 4. Inside the Clausal Compiler: compiler.vector180.svg
# ==============================================================================
def build_compiler(out_dir):
    a = Atom("compiler", 1600, 860)
    a.text_box("title", 40, 18, 1520, "Inside the Clausal compiler: one Gherkin sentence, dual formal & executable targets", 29, INK)
    a.text_box(
        "subtitle",
        40,
        56,
        1520,
        "Zero LLM guesswork and zero raw Prop holes—the compiler assembles typed Clausebook slots or refuses.",
        19,
        MUTED,
    )

    a.rect("src.zone", 40, 108, 1520, 142, ZONE, BORDER, 2)
    a.text_box("src.hdr", 62, 118, 1120, "1. INPUT: CANONICAL CLAUSAL SENTENCE IN features/*.feature (100% VALID GHERKIN)", 17, ZLAB)
    a.pill("src.ok", 1390, 132, 286, 32, PGREEN, "built via clausal compose", 15, GREEN)

    SY = 160
    toks = [
        ("t1", 62, 168, "Rule: Every", "Quantifier", PGREEN, GREEN),
        ("t2", 240, 232, "internal transfer,", "Modifier + Local Op", PBLUE, BLUE),
        ("t3", 482, 276, "accepted or rejected,", "Fail-Closed Default", PAMBER, AMBER),
        ("t4", 768, 224, "never changes", "Core Frame", PGREEN, GREEN),
        ("t5", 1002, 214, "aggregate", "Modifier", PPURPLE, PURPLE),
        ("t6", 1226, 310, "account balance.", "Local Measure", PTEAL, TEAL),
    ]
    for tid, tx, tw, tword, tkind, tfill, tcol in toks:
        a.rect(f"{tid}.b", tx, SY, tw, 72, "#ffffff", tcol, 2.5)
        a.rect(f"{tid}.h", tx, SY + 46, tw, 26, tfill, "none")
        a.text_box(f"{tid}.w", tx + 6, SY + 8, tw - 12, tword, 19, INK, "middle")
        a.text_box(f"{tid}.k", tx + 6, SY + 48, tw - 12, tkind, 14, tcol, "middle")

    CY = 304
    a.arrow("in.to.comp", 800, 250, 800, CY - 4, LINE, 3.5, k=10)

    a.rect("cb.box", 40, CY + 10, 344, 152, ZONE_AMBER, AMBER, 2.5)
    a.text_box("cb.t1", 58, CY + 24, 308, "The Clausebook", 23, INK)
    a.text_box("cb.t2", 58, CY + 58, 308, "Signed frames, modifiers,", 17, MUTED)
    a.text_box("cb.t3", 58, CY + 84, 308, "domain packs & local nouns", 17, MUTED)
    a.text_box("cb.t4", 58, CY + 116, 308, "content-hashed & human-signed", 15, AMBER)
    a.arrow("cb.to.comp", 384, CY + 86, 472, CY + 86, AMBER, 3, k=9)

    a.rect("comp.box", 476, CY, 648, 172, "#ffffff", INK, 3.5)
    a.rect("comp.hdr", 476, CY, 648, 52, PGREEN, INK, 2)
    a.text_box("comp.title", 498, CY + 10, 604, "2. CLAUSAL COMPILER (clausal / cargo clausal)", 22, INK, "middle")
    a.text_box("comp.s1", 502, CY + 66, 604, "• Slot-checks grammar & algebraic sorts (Op, Measure, Cond)", 18, INK)
    a.text_box("comp.s2", 502, CY + 96, 604, "• Enforces fail-closed Op.HoldsAt (no panic / silent drop)", 18, GREEN)
    a.text_box("comp.s3", 502, CY + 126, 604, "• Emits dual ASTs with zero raw Prop escape hatches", 18, BLUE)

    a.arrow("comp.to.ref", 1124, CY + 86, 1212, CY + 86, RED, 3, k=9)
    a.rect("ref.box", 1216, CY + 10, 344, 152, PRED, RED, 2.5)
    a.text_box("ref.t1", 1234, CY + 24, 308, "Refused if Unbound", 22, RED)
    a.text_box("ref.t2", 1234, CY + 58, 308, "• Unknown word -> UNBOUND", 17, INK)
    a.text_box("ref.t3", 1234, CY + 86, 308, "• Sort mismatch -> ILL-TYPED", 17, INK)
    a.text_box("ref.t4", 1234, CY + 114, 308, "• 2 readings -> witness prompt", 17, MUTED)

    BY = 556
    a.elbow_arrow("to.lean", [(680, CY + 172), (680, 514), (352, 514), (352, BY - 4)], GREEN, 3.5, head=True, k=10)
    a.elbow_arrow("to.rust", [(920, CY + 172), (920, 514), (1248, 514), (1248, BY - 4)], BLUE, 3.5, head=True, k=10)

    a.rect("lean.box", 40, BY, 624, 214, ZONE_GREEN, GREEN, 3)
    a.text_box("lean.hdr", 62, BY + 14, 580, "3A. FORMAL TARGET: LEAN 4 (clausal prove)", 20, GREEN)
    a.rect("lean.code", 62, BY + 52, 580, 74, "#ffffff", GREEN, 2)
    a.text_box("lean.c1", 78, BY + 62, 548, "theorem transfer_keeps_total :", 18, INK)
    a.text_box("lean.c2", 78, BY + 90, 548, "  NeverChanges.at (internal transfer) (aggregate balance)", 17, GREEN)
    a.text_box("lean.f1", 62, BY + 140, 580, "+ Generates .sat non-vacuity & reading <-> stmt link checks", 17, MUTED)
    a.text_box("lean.f2", 62, BY + 168, 580, "+ Proved over Aeneas-extracted pure Lean code model", 17, MUTED)

    a.rect("rust.box", 936, BY, 624, 214, ZONE_BLUE, BLUE, 3)
    a.text_box("rust.hdr", 958, BY + 14, 580, "3B. EXECUTABLE TARGET: RUST (clausal test)", 20, BLUE)
    a.rect("rust.code", 958, BY + 52, 580, 74, "#ffffff", BLUE, 2)
    a.text_box("rust.c1", 974, BY + 62, 548, "cucumber-rs #[given/when/then] + Rule invariant check", 18, INK)
    a.text_box("rust.c2", 974, BY + 90, 548, "proptest! { |(s, tx)| assert_never_changes(s, tx) }", 17, BLUE)
    a.text_box("rust.f1", 958, BY + 140, 580, "+ Runs immediately via standard cargo test (no Lean needed)", 17, MUTED)
    a.text_box("rust.f2", 958, BY + 168, 580, "+ Emits bounded Kani harnesses & replays counterexamples", 17, MUTED)

    a.arrow("conf.l", 664, BY + 107, 700, BY + 107, GREEN, 3, k=8)
    a.arrow("conf.r", 936, BY + 107, 900, BY + 107, BLUE, 3, k=8)
    a.diamond("conf.dia", 800, BY + 107, 96, 58, INK, 3)
    a.text_box("conf.t1", 722, BY + 82, 156, "Conformance", 17, INK, "middle")
    a.text_box("conf.t2", 722, BY + 108, 156, "grid check", 17, GREEN, "middle")
    a.text_box("conf.sub", 680, BY + 174, 240, "verifies Lean == Rust", 15, MUTED, "middle")

    a.text_box(
        "foot",
        40,
        800,
        1520,
        "Result: product/policy owners read row 1; cargo test executes 3B in seconds; Lean's kernel proves 3A for every input.",
        19,
        MUTED,
    )
    a.write(os.path.join(out_dir, "compiler.vector180.svg"))


# ==============================================================================
# 5. Four-Tier Evidence Pipeline: evidence.vector180.svg
# ==============================================================================
def build_evidence(out_dir):
    a = Atom("evidence", 1600, 840)
    a.text_box("title", 40, 18, 1520, "The Clausal compiler turns one .feature rule into four graded tiers of evidence", 29, INK)
    a.text_box(
        "subtitle",
        40,
        56,
        1520,
        "Tiers 1-3 compile directly to Rust test harnesses (no Lean needed); Tier 4 proves the theorem in Lean 4.",
        19,
        MUTED,
    )

    a.rect("in.box", 40, 114, 308, 88, "#ffffff", INK, 3)
    a.text_box("in.t1", 56, 126, 276, "Clausal (.feature)", 22, INK, "middle")
    a.text_box("in.t2", 56, 162, 276, "Rule + Scenario tables", 17, GREEN, "middle")

    a.arrow("in.to.c", 348, 158, 420, 158, LINE, 3.5, k=9)
    a.pill("comp.pill", 554, 158, 260, 56, PGREEN, "Clausal compiler", 21, INK)

    a.rect("rail.rust", 40, 224, 1134, 46, ZONE_BLUE, BLUE, 2)
    a.text_box("rail.rust.t", 60, 234, 1094, "RUST EXECUTABLE BACKEND (cargo clausal test — runs on any Rust crate in seconds)", 18, BLUE, "middle")

    a.rect("rail.lean", 1198, 224, 362, 46, ZONE_GREEN, GREEN, 2)
    a.text_box("rail.lean.t", 1210, 234, 338, "LEAN 4 BACKEND (clausal prove)", 18, GREEN, "middle")

    a.arrow("bus.rust", 554, 186, 554, 220, BLUE, 3, k=8)
    a.elbow_arrow("bus.lean", [(684, 158), (1379, 158), (1379, 220)], GREEN, 3, head=True, k=8)
    a.text_box("bus.lean.lbl", 850, 130, 380, "Aeneas model + typed Frames.Op", 16, GREEN, "middle")

    tiers = [
        (
            "t1",
            40,
            "#ffffff",
            BORDER,
            MUTED,
            "1. Cucumber BDD",
            "concrete Scenario rows",
            [
                "Executes formalized",
                ".feature steps via",
                "cucumber-rs against",
                "the compiled binary.",
            ],
            "tested (examples)",
        ),
        (
            "t2",
            426,
            PBLUE,
            BLUE,
            BLUE,
            "2. Property Fuzz",
            "thousands of random inputs",
            [
                "Auto-generated proptest",
                "harnesses on Rule lines",
                "with shrinking to a",
                "minimal failing input.",
            ],
            "tested (sampled)",
        ),
        (
            "t3",
            812,
            PTEAL,
            TEAL,
            TEAL,
            "3. Bounded Check",
            "exhaustive up to size k",
            [
                "Symbolic / Kani bit-vector",
                "verification across all",
                "inputs within a stated",
                "loop & slice bound.",
            ],
            "bounded-checked",
        ),
        (
            "t4",
            1198,
            PGREEN,
            GREEN,
            GREEN,
            "4. Kernel Proof",
            "every input, every size",
            [
                "Unbounded Lean 4 proof",
                "over the code model,",
                "audited against sorry,",
                "vacuity & custom axioms.",
            ],
            "kernel-checked",
        ),
    ]

    TY, TH = 296, 360
    for tid, tx, tfill, tstroke, tcol, ttitle, tsub, tlines, ttag in tiers:
        mid = tx + 181
        a.arrow(f"drop.{tid}", mid, 270, mid, TY - 4, BLUE if tid != "t4" else GREEN, 3, k=8)
        a.rect(f"{tid}.box", tx, TY, 362, TH, "#ffffff", tstroke, 3)
        a.rect(f"{tid}.hdr", tx, TY, 362, 82, tfill, tstroke, 2)
        a.text_box(f"{tid}.title", tx + 20, TY + 12, 322, ttitle, 24, INK)
        a.text_box(f"{tid}.sub", tx + 20, TY + 48, 322, tsub, 17, tcol)
        for idx, ln in enumerate(tlines):
            a.text_box(f"{tid}.l{idx+1}", tx + 20, TY + 102 + idx * 32, 322, ln, 19, MUTED)
        a.rect(f"{tid}.tagbox", tx + 20, TY + TH - 58, 322, 40, tfill, tstroke, 2)
        a.text_box(f"{tid}.tag", tx + 28, TY + TH - 50, 306, ttag, 18, tcol, "middle")

    a.arrow("axis", 40, 686, 1556, 686, LINE, 3, k=10)
    a.text_box("axis.l", 40, 698, 620, "runs in seconds via cargo test; catches 95%+ of bugs", 18, MUTED)
    a.text_box("axis.r", 920, 698, 640, "unbounded mathematical certainty; zero sample or size gaps", 18, GREEN, "end")

    a.rect("replay.box", 40, 742, 1520, 78, "#ffffff", BORDER, 2.5)
    a.text_box(
        "replay.l1",
        62,
        750,
        1476,
        "Closed-loop counterexample replay: any witness from Tiers 2-4 is replayed on both the Lean model and compiled binary.",
        19,
        INK,
    )
    a.text_box(
        "replay.l2",
        62,
        782,
        1476,
        "If the Lean model and binary ever disagree on a replay, Clausal halts and flags a TRANSLATION / MODEL DIVERGENCE.",
        18,
        RED,
    )

    a.write(os.path.join(out_dir, "evidence.vector180.svg"))


if __name__ == "__main__":
    target = sys.argv[1]
    os.makedirs(target, exist_ok=True)
    build_how_it_works(target)
    build_chain(target)
    build_vocabulary(target)
    build_compiler(target)
    build_evidence(target)
    print("Generated 5 Clausal Vector180 SVG atoms in", target)
