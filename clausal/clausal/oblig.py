"""clausal oblig: the FLAT PROOF OBLIGATION of a compiled reading, generated from the pieces.

A reading (lean/Wallet/Readings.lean) is frames of lean/Frames applied to an operation. To prove it, a person or
an agent wants the same thing written out with no frame library in it: quantifiers, the Givens as hypotheses,
the call of the Aeneas model function, and what must hold of what it returns. This module writes that statement
for every reading that has no flat statement in the old whole-phrase glossary (a NEW sentence), and everything
that ties it to the reading:

  <id>.obligation                 lean/Wallet/Obligations.lean (built by lake; proof files import it)
  <id>                            the PROOF of the obligation: lean/Wallet/Proofs/<feature>/<scenario>.lean or
                                  lean/Wallet/RuleProofs/<feature>/<rule>.lean. Created as a `sorry` stub; hand-written
  <id>.reading_iff_obligation     generated script, kernel-checked: reading ↔ obligation     (lean/Run/Links.lean)
  <id>.reading_holds / .holds     the reading itself as one theorem: the proof carried through the equivalence
  <id>.reading_sat                the scope of the reading is met at the input the reading search found
  <id>.refuted                    ¬ reading, at the input where the reading search found it false

The obligation is UNTRUSTED text (each frame's `flat:` template in clausebook.yaml, filled in by this module):
nothing rests on it unless the equivalence is kernel-checked, and the audit checks that the equivalence does not
use the proof of either side.

Shapes. For one unit (a scenario, or one clause of a Rule) about the operation `op` with hypotheses H:

  claims about every call (the default)       ∀ params st inp, H → ∃ ans st', RUN ∧ Q₁ ∧ … ∧ (acc ans → Qₖ) ∧ (¬ acc ans → Qₗ)
  only claims about accepted / rejected calls ∀ st inp, H → ∀ ans st', RUN → (acc ans → Q₁) ∧ …
  a claim that compares two calls             ∀ st inp st2 inp2, H → H₂ → rel → ∃ ans st' ans2 st2', RUN ∧ RUN₂ ∧ Q

RUN is the model call written out: `f st inp = ok (ans, st')` for a `&mut self` function, `f st inp = ok ans ∧ st' = st`
for a `&self` one, one ∃ per earlier call of a sequence, one per bystander.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from . import emit
from .vocab import Claim, Leaf, Node, Reading, base_cat, group, render, render_tmpl, wrap

SHAPE_LEMMA = {"mut": "Bdd.opMut_some", "mut2": "Bdd.opMut2_some", "read": "Bdd.opRead_some", "read0": "Bdd.opRead0_some"}


def paren(s: str) -> str:
    return s if re.fullmatch(r"[\w.']+", s) else f"({s})"


@dataclass
class Unit:
    ops: list
    bys: list                    # Lean types of the bystanders (scenarios only)
    base: str                    # the operation, no scope
    op: str                      # ... with the scope (Givens, "internal", "for which")
    layers: list                 # scope layers, outermost last: [[hypothesis text, ...], ...]
    claims: list                 # [(index in the reading, Claim)]
    ctx: object
    state_type: str
    input_type: str
    outer: list = field(default_factory=list)

    @property
    def acc(self) -> str:
        return self.ops[-1]["accepted"]

    @property
    def answer(self) -> str:
        return self.ops[-1]["answer"]

    @property
    def hyps(self) -> list:
        return [h for layer in self.layers for h in layer]

    def scope_term(self, names) -> str:
        """Proof of `(op).scope st inp` from one proof per hypothesis."""
        cur, it = "trivial", iter(names)
        for layer in self.layers:
            cur = "⟨" + ", ".join([cur] + [next(it) for _ in layer]) + "⟩"
        return cur

    def scope_pattern(self, names) -> str:
        cur, it = "-", iter(names)
        for layer in self.layers:
            cur = "⟨" + ", ".join([cur] + [next(it) for _ in layer]) + "⟩"
        return cur

    # ---- the call, written out
    def flat_single(self, o, s, i, r, s2) -> tuple:
        f = o["model"]
        if o["shape"] == "mut":
            return f"{f} {paren(s)} {paren(i)} = ok ({r}, {s2})", SHAPE_LEMMA["mut"]
        if o["shape"] == "mut2":
            return f"{f} {paren(s)}.1 {paren(s)}.2 {paren(i)} = ok ({r}, {s2})", SHAPE_LEMMA["mut2"]
        if o["shape"] == "read":
            return f"{f} {paren(s)} {paren(i)} = ok {r} ∧ {s2} = {s}", SHAPE_LEMMA["read"]
        return f"{f} {paren(s)} = ok {r} ∧ {s2} = {s}", SHAPE_LEMMA["read0"]

    def flat_seq(self, k, s, i, r, s2, tag="") -> tuple:
        if k == 1:
            return self.flat_single(self.ops[0], s, i, r, s2)
        rk, sk = f"r{tag}_{k - 1}", f"s{tag}_{k - 1}"
        a, pa = self.flat_seq(k - 1, s, f"{paren(i)}.1", rk, sk, tag)
        b, pb = self.flat_single(self.ops[k - 1], sk, f"{paren(i)}.2", r, s2)
        return (f"∃ {rk} {sk}, ({a}) ∧ ({b})",
                f"(Frames.Op.andThen_some.trans (exists_congr fun _ => exists_congr fun _ => and_congr {pa} {pb}))")

    def flat_run(self, s="st", i="inp", r="ans", s2="st'", tag="") -> tuple:
        """(text, proof term of `(base).run s i = some (r, s2) ↔ text`)."""
        def go(nb, s, s2):
            if nb == 0:
                return self.flat_seq(len(self.ops), s, i, r, s2, tag)
            t = f"t{tag}_{nb}"
            a, pa = go(nb - 1, f"{paren(s)}.1", t)
            return (f"∃ {t}, ({a}) ∧ {s2} = ({t}, {paren(s)}.2)",
                    f"(Frames.Op.beside_some.trans (exists_congr fun _ => and_congr {pa} Iff.rfl))")
        return go(len(self.bys), s, s2)

    def run_have(self, name="run") -> str:
        text, proof = self.flat_run()
        return (f"have {name} : ∀ (st : {self.state_type}) (inp : {self.input_type}) (ans : {self.answer}) (st' : {self.state_type}), "
                f"({self.base}).run st inp = some (ans, st') ↔ ({text}) := fun st inp ans st' => {proof}")


# --------------------------------------------------------------------------- the content of one frame, flat

def flat_q(c: Claim, u: Unit) -> str:
    """A frame's `flat:` template with its holes filled: the content of the claim at one call."""
    f, node, ctx = c.frame, c.node, u.ctx
    tmpl = f.get("flat")
    if tmpl is None:
        raise KeyError(f"frame `{f['id']}` has no `flat:` template in clausebook.yaml")
    out = tmpl.replace("{accepted}", f"{u.acc} ans")
    args = node.args if node is not None else {}

    def rend(val, sv):
        if isinstance(val, list):
            return "[" + ", ".join(render(v, ctx, sv) for v in val) + "]"
        if base_cat(val.cat) == "parts":
            return render(val, ctx, sv)
        return render(val, ctx, sv, item="x")
    for name, val in args.items():
        if isinstance(val, Node) and base_cat(val.cat) == "parts":
            out = out.replace("{pm'}", render_tmpl_on(val.piece["part_measure"], val, ctx, "st'"))
            out = out.replace("{pm}", render_tmpl_on(val.piece["part_measure"], val, ctx, "st"))
        r1 = rend(val, "st")
        out = out.replace("{" + name + "'}", wrap(rend(val, "st'")))
        out = out.replace("{" + name + "2}", wrap(re.sub(r"\bans\b", "ans2", r1)))
        out = out.replace("{" + name + "}", wrap(r1))
    left = re.findall(r"\{[a-z]\w*'?\}", out)
    if left:
        raise KeyError(f"frame `{f['id']}`: `flat:` template has unfilled holes {left}")
    return out.replace(f"({ctx.opbase}).accepted", u.acc)


def render_tmpl_on(tmpl: str, node: Node, ctx, sv: str) -> str:
    out = tmpl
    for name, val in node.args.items():
        out = out.replace("{" + name + "}", wrap(render(val, ctx, sv)))
    return out


def mod_guard(c: Claim, u: Unit, ans="ans") -> str:
    if "rejected" in c.mods:
        return f"¬ {u.acc} {ans}"
    if "successful" in c.mods:
        return f"{u.acc} {ans}"
    return ""


def guarded(c: Claim, u: Unit) -> str:
    g, q = mod_guard(c, u), flat_q(c, u)
    return f"({g} → {q})" if g else (q if " " not in q or c.frame["id"] == "always_answers" else f"({q})")


def on_second(text: str) -> str:
    """A hypothesis about (st, inp), restated for the second call (st2, inp2)."""
    return re.sub(r"\binp\b", "inp2", re.sub(r"\bst\b(?!')", "st2", text))


# --------------------------------------------------------------------------- units of a reading

def units(rd: Reading) -> list:
    if rd.kind == "scenario":
        info = rd.info
        ctx = info["ctx"]
        voc = ctx.voc
        bys = [voc.actors[ctx.actor_type[a]]["lean"] for a in info["bystanders"]]
        layers = [[c["lean"] for c in rd.conds]] if rd.conds else []
        return [Unit(info["ops"], bys, rd.base, rd.op, layers, list(enumerate(rd.claims)), ctx, rd.state_type, rd.input_type, list(rd.outer))]
    out, k = [], 0
    for g in rd.info["clauses"]:
        layers = []
        if g["internal"]:
            i = g["ops"][0]["internal"]
            layers.append([f"∀ p ∈ {i['parties']} inp, {i['member']} st p"])
        for t in g["cond_trees"]:
            layers.append([render(t, g["ctx"])])
        cl = [(k + j, c) for j, c in enumerate(g["claims"])]
        k += len(g["claims"])
        out.append(Unit(g["ops"], [], g["base"], g["op"], layers, cl, g["ctx"], g["state_type"], g["input_type"], []))
    return out


def parts(u: Unit) -> list:
    """The conjuncts of the obligation that unit `u` contributes: [(kind, [(index, Claim)], Lean text)]."""
    one = [(j, c) for j, c in u.claims if c.runs == 1]
    two = [(j, c) for j, c in u.claims if c.runs == 2]
    out = []
    binders = u.outer + [("st", u.state_type), ("inp", u.input_type)]
    hyp = "".join(f"({h}) → " for h in u.hyps)
    run, _ = u.flat_run()
    if one:
        qs = " ∧ ".join(guarded(c, u) for _, c in one)
        if any(not c.mods for _, c in one):
            out.append(("every", one, f"∀ {group(binders)}, {hyp}∃ (ans : {u.answer}) (st' : {u.state_type}), ({run}) ∧ {qs}"))
        else:
            out.append(("filtered", one, f"∀ {group(binders)}, {hyp}∀ (ans : {u.answer}) (st' : {u.state_type}), ({run}) → {qs}"))
    for j, c in two:
        b2 = u.outer + [("st", u.state_type), ("inp", u.input_type), ("st2", u.state_type), ("inp2", u.input_type)]
        hyp2 = hyp + "".join(f"({on_second(h)}) → " for h in u.hyps)
        rel = render(next(v for v in c.node.args.values() if isinstance(v, Node) and base_cat(v.cat) == "variation"), u.ctx)
        run2, _ = u.flat_run("st2", "inp2", "ans2", "st2'", tag="b")
        q = flat_q(c, u)
        ex = f"(ans : {u.answer}) (st' : {u.state_type}) (ans2 : {u.answer}) (st2' : {u.state_type})"
        if not c.mods:
            out.append(("two", [(j, c)], f"∀ {group(b2)}, {hyp2}{rel} st inp st2 inp2 → ∃ {ex}, ({run}) ∧ ({run2}) ∧ ({q})"))
        else:
            g1, g2 = mod_guard(c, u), mod_guard(c, u, "ans2")
            out.append(("two-filtered", [(j, c)], f"∀ {group(b2)}, {hyp2}{rel} st inp st2 inp2 → ∀ {ex}, ({run}) → ({run2}) → {g1} → {g2} → ({q})"))
    return out


def obligation_def(rd: Reading) -> str:
    ps = [t for u in units(rd) for _, _, t in parts(u)]
    doc = f"/-- {rd.source}\n" + "\n".join("    " + l for l in rd.text.splitlines()) + " -/"
    return doc + f"\ndef {rd.id}.obligation : Prop :=\n  " + " ∧\n  ".join("(" + p + ")" for p in ps)


def obligations_file(voc, readings) -> str:
    out = [emit.HEADER + "-- THE FLAT PROOF OBLIGATION of every NEW sentence (a scenario or a `Rule:` line that has no entry in the old\n"
           "-- whole-phrase glossary): the compiled reading of lean/Wallet/Readings.lean written out with no frame library in it,\n"
           "-- generated from the `flat:` template of each frame. A proof is supplied by hand in lean/Wallet/Proofs/ (scenarios) or\n"
           "-- lean/Wallet/RuleProofs/ (rules): a theorem named exactly `<id>` of type exactly `<id>.obligation`.\n"
           "-- UNTRUSTED text: lean/Run/Links.lean kernel-checks `<id>.reading_iff_obligation : <id>.reading ↔ <id>.obligation`.\n"
           + "".join(f"import {i}\n" for i in voc.raw["lean_imports"])
           + "open Aeneas Aeneas.Std Result\nset_option linter.unusedVariables false\n"]
    for rd in readings:
        out.append(obligation_def(rd) + "\n")
    return "\n".join(out)


# --------------------------------------------------------------------------- reading ↔ obligation

def proj(j: int, k: int) -> str:
    if k == 1:
        return ""
    return ".2" * j + (".1" if j < k - 1 else "")


def sp(ind: str, *words) -> str:
    """One line: the indentation, then the non-empty words separated by single spaces."""
    return ind + " ".join(w for w in words if w)


def iff_theorem(rd: Reading) -> str:
    us = units(rd)
    allparts = [(u, p) for u in us for p in parts(u)]
    m, k = len(allparts), len(rd.claims)
    outer = " ".join(n for n, _ in rd.outer)
    hO = f"(h {outer})" if outer else "h"
    L = [f"/-- The compiled reading says exactly what its flat proof obligation says. -/",
         f"theorem {rd.id}.reading_iff_obligation : {rd.name} ↔ {rd.id}.obligation := by"]
    for n, u in enumerate(us):
        L.append("  " + u.run_have(f"run{n}"))
    L.append("  constructor")
    # ---- reading → obligation
    L.append("  · intro h")
    if m > 1:
        L.append(f"    refine ⟨{', '.join(['?_'] * m)}⟩")
    for u, (kind, cl, _) in allparts:
        n = us.index(u)
        hn = [f"g{i + 1}" for i in range(len(u.hyps))]
        sc = u.scope_term(hn)
        if kind in ("every", "filtered"):
            L.append(sp("    ", "· intro", outer, "st inp", *hn))
            L.append(f"      have sc : ({u.op}).scope st inp := {sc}")
            if kind == "every":
                first = True
                for j, c in cl:
                    if c.mods:
                        continue
                    if first:
                        L.append(f"      obtain ⟨ans, st', e, q{j}⟩ := {hO}{proj(j, k)} st inp sc")
                        first = False
                    else:
                        L.append(f"      obtain ⟨r2, s2, e2, q{j}⟩ := {hO}{proj(j, k)} st inp sc")
                        L.append("      obtain ⟨u1, u2⟩ := Frames.Op.answer_unique e e2; subst u1 u2; clear e2")
                for j, c in cl:
                    if c.mods:
                        L.append(f"      have q{j} := {hO}{proj(j, k)} st inp sc ans st' e")
                L.append(f"      exact ⟨ans, st', (run{n} st inp ans st').mp e, {', '.join(f'q{j}' for j, _ in cl)}⟩")
            else:
                L.append("      intro ans st' x")
                L.append(f"      have e : ({u.base}).run st inp = some (ans, st') := (run{n} st inp ans st').mpr x")
                items = [f"{hO}{proj(j, k)} st inp sc ans st' e" for j, _ in cl]
                L.append("      exact " + (items[0] if len(items) == 1 else "⟨" + ", ".join(items) + "⟩"))
        else:
            j, c = cl[0]
            hn2 = [f"g{i + 1}b" for i in range(len(u.hyps))]
            L.append(sp("    ", "· intro st inp st2 inp2", *(hn + hn2), "rel"))
            L.append(f"      have sc : ({u.op}).scope st inp := {sc}")
            L.append(f"      have sc2 : ({u.op}).scope st2 inp2 := {u.scope_term(hn2)}")
            if kind == "two":
                L.append(f"      obtain ⟨ans, st', ans2, st2', e, e2, q⟩ := {hO}{proj(j, k)} st inp st2 inp2 sc sc2 rel")
                L.append(f"      exact ⟨ans, st', ans2, st2', (run{n} st inp ans st').mp e, (run{n} st2 inp2 ans2 st2').mp e2, q⟩")
            else:
                L.append("      intro ans st' ans2 st2' x x2 m1 m2")
                L.append(f"      exact {hO}{proj(j, k)} st inp st2 inp2 sc sc2 rel ans st' ans2 st2' ((run{n} st inp ans st').mpr x) "
                         f"((run{n} st2 inp2 ans2 st2').mpr x2) m1 m2")
    # ---- obligation → reading
    L.append("  · intro h")
    if m > 1:
        L.append(f"    obtain ⟨{', '.join(f'o{i}' for i in range(m))}⟩ := h")
    else:
        L.append("    have o0 := h")
    if outer:
        L.append(f"    intro {outer}")
    if k > 1:
        L.append(f"    refine ⟨{', '.join(['?_'] * k)}⟩")
    where = {}
    for i, (u, (kind, cl, _)) in enumerate(allparts):
        for pos, (j, c) in enumerate(cl):
            where[j] = (i, u, kind, cl, pos)
    for j, c in enumerate(rd.claims):
        i, u, kind, cl, pos = where[j]
        n = us.index(u)
        cn = [f"c{x + 1}" for x in range(len(u.hyps))]
        pat = u.scope_pattern(cn)
        take = f"      obtain {pat} := sc" if u.hyps else "      clear sc"
        args = " ".join(cn)
        if kind == "every":
            names = ", ".join(f"q{x}" for x, _ in cl)
            if not c.mods:
                L += ["    · intro st inp sc", take,
                      sp("      ", f"obtain ⟨ans, st', x, {names}⟩ := o{i}", outer, "st inp", args),
                      f"      exact ⟨ans, st', (run{n} st inp ans st').mpr x, q{j}⟩"]
            else:
                L += ["    · intro st inp sc r0 s0 e0 hm", take,
                      sp("      ", f"obtain ⟨ans, st', x, {names}⟩ := o{i}", outer, "st inp", args),
                      f"      obtain ⟨u1, u2⟩ := Frames.Op.answer_unique ((run{n} st inp ans st').mpr x) e0; subst u1 u2",
                      f"      exact q{j} hm"]
        elif kind == "filtered":
            L += ["    · intro st inp sc r0 s0 e0 hm", take,
                  sp("      ", f"exact (o{i} st inp", args, f"r0 s0 ((run{n} st inp r0 s0).mp e0)){proj(pos, len(cl))} hm")]
        else:
            cn2 = [f"c{x + 1}b" for x in range(len(u.hyps))]
            take2 = f"      obtain {u.scope_pattern(cn2)} := sc2" if u.hyps else "      clear sc2"
            L += ["    · intro st inp st2 inp2 sc sc2 rel", take, take2]
            a2 = " ".join(cn + cn2)
            if kind == "two":
                L += [sp("      ", f"obtain ⟨ans, st', ans2, st2', x, x2, q⟩ := o{i} st inp st2 inp2", a2, "rel"),
                      f"      exact ⟨ans, st', ans2, st2', (run{n} st inp ans st').mpr x, (run{n} st2 inp2 ans2 st2').mpr x2, q⟩"]
            else:
                L += ["      intro ans st' ans2 st2' e e2 m1 m2",
                      sp("      ", f"exact o{i} st inp st2 inp2", a2, f"rel ans st' ans2 st2' ((run{n} st inp ans st').mp e) ((run{n} st2 inp2 ans2 st2').mp e2) m1 m2")]
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------- non-vacuity and refutation at a grid point

def simp_sets(voc, gloss) -> tuple:
    hints = gloss.raw.get("proof_hints", {})
    old = [e.lean for e in gloss.entries if e.kind != "when"] + hints.get("simp", [])
    new = sorted({d for p in voc.pieces.values() for d in p.get("defs", []) if d.split(".")[0] in ("W", "L") and not d.endswith(".at")})
    for o in voc.ops.values():
        new.append(o["accepted"])
    s1 = ", ".join(dict.fromkeys([x for x in old + new if x not in ("L.mkBatch",)] + ["Vocab.mkWallet", "L.mkBatch_val", "Frames.aggregate", "Frames.every",
                                                                                "Frames.theFirst", "Frames.noneOf", "Frames.someOf"]))
    s2 = s1 + "".join(", " + x for x in hints.get("refute_simp", []))
    s3 = s2 + "".join(", " + x for x in hints.get("refute_simp_more", []))
    return s1, s2, s3


def leaf_tactics(voc, gloss) -> str:
    """`sat_leaf`: one scope condition (or a relation between two calls) at a concrete input."""
    s1, s2, _ = simp_sets(voc, gloss)
    return (f"macro \"sat_leaf\" : tactic => `(tactic| first\n"
            f"  | exact trivial\n  | rfl\n  | decide\n"
            f"  | (simp [{s1}]; done)\n  | (simp [{s1}]; scalar_tac)\n  | (simp [{s1}]; omega)\n"
            f"  | (simp [{s2}]; done)\n  | (simp [{s2}]; scalar_tac)\n  | (refine ⟨_, ?_, ?_⟩ <;> simp [{s2}] <;> scalar_tac))\n")


def scope_at(u: Unit) -> str:
    return u.scope_term(["(by sat_leaf)"] * len(u.hyps))


def sat_theorem(rd: Reading, point: dict) -> str:
    u = units(rd)[0]
    binders = rd.outer + [("st", rd.state_type), ("inp", rd.input_type)]
    vals = [point["outer"][n] for n, _ in rd.outer] + [point["st"], point["inp"]]
    return (f"/-- The reading is not vacuous: some state and input are in its scope. -/\n"
            f"theorem {rd.id}.reading_sat : ∃ {group(binders)}, ({u.op}).scope st inp :=\n"
            f"  ⟨{', '.join(vals)}, {scope_at(u)}⟩\n")


def spec_of(u: Unit, lemma_names: set) -> list:
    """Per call of the unit: the hand-proved `@[step]` lemma about its model function, or None."""
    out = []
    for o in u.ops:
        ns, fn = o["model"].split(".", 1)
        name = f"{ns}.{fn}.spec"
        out.append(name if name in lemma_names else None)
    return out


def closers(sets, ind="        ") -> str:
    alts = []
    for s in sets:
        alts += [f"(simp [{s}] at *; done)", f"(simp_all [{s}]; done)", f"(simp_all [{s}]; scalar_tac)", f"(simp_all [{s}]; omega)",
                 f"(intro hq; simp_all [{s}]; done)", f"(intro hq; simp_all [{s}]; scalar_tac)",
                 f"(simp [{s}] at *; simp_all; done)", f"(simp [{s}] at *; simp_all; scalar_tac)", f"(simp [{s}] at *; grind)",
                 f"(simp_all [{s}]; grind)"]
    alts += ["scalar_tac", "grind"]
    return f"{ind}all_goals first\n" + "".join(f"{ind}  | {a}\n" for a in alts)


def witness(u: Unit, st: str, inp: str, post: str, sets, name="w", ind="  ") -> list:
    """`name : ∃ out, <model> st inp = ok out ∧ post(out)` for a unit about ONE call: by stepping through the model
    (or through its hand-proved step lemma, for a loop)."""
    o = u.ops[0]
    call = f"{o['model']} {paren(st)}" + ("" if o["shape"] == "read0" else f" {paren(inp)}") if o["shape"] != "mut2" else \
        f"{o['model']} {paren(st)}.1 {paren(st)}.2 {paren(inp)}"
    return [f"{ind}have {name} : ∃ out, {call} = ok out ∧ ({post}) := by",
            f"{ind}  apply Bdd.ok_of_spec",
            f"{ind}  first",
            f"{ind}    | (unfold {o['model']}",
            f"{ind}       step*",
            closers(sets, ind + "       ").rstrip("\n") + ")",
            f"{ind}    | (step*",
            closers(sets, ind + "       ").rstrip("\n") + ")"]


def out_subst(text: str, o: dict, st: str, inp: str = "()") -> str:
    """A claim's content, restated about `out` (what the model function returned) at the concrete state and input."""
    if o["shape"] in ("mut", "mut2"):
        t = re.sub(r"\bans\b", "out.1", text).replace("st'", "out.2")
    else:
        t = re.sub(r"\bans\b", "out", text).replace("st'", paren(st))
    t = re.sub(r"\bst\b(?!')", lambda _m: paren(st), t)
    return re.sub(r"\binp\b", lambda _m: paren(inp), t)


def unify(o: dict, x: str, e0: str, ind="  ") -> list:
    """After `x : <flat run with ans, st'>` and `e0 : model = ok out`: make `out` the pair (ans, st')."""
    if o["shape"] in ("mut", "mut2"):
        return [f"{ind}have u := Bdd.ok_inj ({e0}.symm.trans {x}); subst u"]
    return [f"{ind}obtain ⟨{x}, u⟩ := {x}; subst u", f"{ind}have u := Bdd.ok_inj ({e0}.symm.trans {x}); subst u"]


def refutation(voc, gloss, rd: Reading, bad: dict, point: dict, lemma_names: set) -> str | None:
    """`¬ <id>.reading` at the grid point where the reading search found the reading false; None where no script is generated.

    Covered: a claim about every call, about accepted calls only, or about rejected calls only, of one operation; a claim
    that compares two calls of one operation; a claim about every call of a SEQUENCE of operations when each has a
    hand-proved step lemma."""
    j = bad["bits"].index("0")
    us = units(rd)
    u = next(x for x in us if any(i == j for i, _ in x.claims))
    c = rd.claims[j]
    n, k = us.index(u), len(rd.claims)
    sets = simp_sets(voc, gloss)
    outer = " ".join(point["outer"][x] for x, _ in rd.outer)
    hO = f"(h {outer})" if outer else "h"
    st, inp = point["st"], point["inp"]
    L = ["set_option maxHeartbeats 4000000 in      -- the script tries several ways of closing each goal; the failed ones count too",
         f"/-- The reading is FALSE: at this input the model gives an answer the claim does not allow. -/",
         f"theorem {rd.id}.refuted : ¬ {rd.name} := by",
         "  " + u.run_have("run"),
         "  intro h",
         f"  have hj := {hO}{proj(j, k)}"]
    o = u.ops[0]
    if c.runs == 2:
        if len(u.ops) != 1 or u.bys or c.mods:
            return None
        st2, inp2 = point["st2"], point["inp2"]
        cls = next((v for v in c.node.args.values() if isinstance(v, Node) and base_cat(v.cat) == "class"), None)
        cl = render(cls, u.ctx).replace(f"({u.ctx.opbase}).accepted", u.acc) if cls is not None else None
        acc = f"{u.acc} ans"
        if c.frame["id"] == "monotone":
            variants = [(cl, f"¬ ({cl})", "exact n2 (q n1)")]
        elif c.frame["id"] == "same_answer":
            variants = [(acc, f"¬ ({acc})", "subst q; exact n2 n1"), (f"¬ ({acc})", acc, "subst q; exact n1 n2")]
        elif c.frame["id"] == "same_answer_if":
            variants = [(f"({cl}) ∧ {acc}", f"¬ ({acc})", "have q := q n1.1; subst q; exact n2 n1.2"),
                        (f"({cl}) ∧ ¬ ({acc})", acc, "have q := q n1.1; subst q; exact n1.2 n2")]
        else:
            return None
        L += [f"  obtain ⟨ans, st', ans2, st2', e, e2, q⟩ := hj {st} {inp} {st2} {inp2} {scope_at(u)} {scope_at(u)} (by sat_leaf)",
              f"  have x := (run {st} {inp} ans st').mp e",
              f"  have x2 := (run {st2} {inp2} ans2 st2').mp e2",
              "  clear e e2 hj h run",
              "  first"]
        for p1, p2, fin in variants:
            i7 = "       "
            body = (witness(u, st, inp, out_subst(p1, o, st, inp), sets, "w1", i7)
                    + witness(u, st2, inp2, out_subst(p2, o, st2, inp2), sets, "w2", i7)
                    + [i7 + "obtain ⟨out, e0, n1⟩ := w1"] + unify(o, "x", "e0", i7)
                    + [i7 + "obtain ⟨out, e0, n2⟩ := w2"] + unify(o, "x2", "e0", i7)
                    + [i7 + fin])
            L.append("    | (" + body[0].strip())
            L += body[1:-1] + [body[-1] + ")"]
        return "\n".join(L) + "\n"
    if u.bys:
        return None
    q = flat_q(c, u)
    if len(u.ops) == 1:
        guard = mod_guard(c, u)
        post = f"¬ ({guard} → {q})" if guard else f"¬ ({q})"
        L += witness(u, st, inp, out_subst(post, o, st, inp), sets)
        L.append("  obtain ⟨out, e0, n0⟩ := w")
        if not c.mods:
            L += [f"  obtain ⟨ans, st', e, q⟩ := hj {st} {inp} {scope_at(u)}",
                  f"  have x := (run {st} {inp} ans st').mp e"] + unify(o, "x", "e0") + ["  exact n0 q"]
        else:
            if o["shape"] in ("mut", "mut2"):
                L += [f"  exact n0 (hj {st} {inp} {scope_at(u)} out.1 out.2 ((run {st} {inp} out.1 out.2).mpr e0))"]
            else:
                L += [f"  exact n0 (hj {st} {inp} {scope_at(u)} out {paren(st)} ((run {st} {inp} out {paren(st)}).mpr ⟨e0, rfl⟩))"]
        return "\n".join(L) + "\n"
    # a sequence: through the step lemma of each call
    specs = spec_of(u, lemma_names)
    if c.mods or any(s is None for s in specs) or len(u.ops) != 2:
        return None
    o1, o2 = u.ops
    L += [f"  obtain ⟨ans, st', e, q⟩ := hj {st} {inp} {scope_at(u)}",
          f"  obtain ⟨r1, s1, x1, x2⟩ := (run {st} {inp} ans st').mp e",
          "  clear e hj h run"]
    for o_, x, sp in ((o1, "x1", specs[0]), (o2, "x2", specs[1])):
        if o_["shape"] in ("read", "read0"):
            L.append(f"  obtain ⟨{x}, u⟩ := {x}; subst u")
        nargs = {"mut": 2, "mut2": 3, "read": 2, "read0": 1}[o_["shape"]]
        L.append(f"  have f{x[1:]} := Bdd.post_of_spec {x} ({sp} {' '.join(['_'] * nargs)})")
    L.append("  first")
    for s in sets:
        L += [f"    | (simp_all [{s}]; done)", f"    | (simp_all [{s}]; scalar_tac)", f"    | (simp_all [{s}]; omega)", f"    | (simp_all [{s}]; grind)"]
    L.append("    | grind")
    return "\n".join(L) + "\n"
