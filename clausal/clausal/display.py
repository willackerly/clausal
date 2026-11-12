"""clausal display: a COMPUTED DISPLAY for a compiled Rule line (plan node Q6).

    python3 -m clausal show "<sentence>" [--json] [--no-refusal] [--no-separate] [--no-rust]
    python3 -m clausal display            after lean/Run/Display.lean ran: out/display.json, and the checks (run.sh)

For every claim of a compiled Rule line it shows

  covers      which calls the claim is about, and whether a call that gives no answer breaks it
  outcomes    (a claim that compares two calls) each combination of first-call and second-call outcome
              (accepted, rejected, no answer), marked allowed or forbidden by the rule
  allowed     one concrete case the rule allows
  forbidden   one concrete case the rule forbids
  neighbour   the nearest neighbouring sentence that ALLOWS the forbidden case, if one compiles

WHERE IT COMES FROM. Only from the frame's statement at a call (`F.at`, lean/Frames/Frames.lean), the executable reading
of the same frame (`Frames.Check.F`, `Frames.Op.observe`; lean/Frames/Check.lean) and the Calls value the claim's
operation carries. Lean evaluates the claim of the operation with its `run` REPLACED (`Disp.withRun`: same scope, same
acceptance, same Calls value): by the outcome the model really gives, and by substituted outcomes (the outcomes the model
gives anywhere on the search grid, and "no answer"). Nothing is read off the echo text (`Reading.echo`, `Claim.echo`),
the book's `flat:` or `coverage:` texts, or the words of the sentence; `selftest` checks that this module does not
touch them. The words printed around the computed values are the constants below.

IT IS NEVER COMPILER INPUT. Nothing here is written into a .feature file, a book or a statement; the compiler
(clausal/vocab.py) does not import this module. It is printed in the report (clausal/rules.py, from out/graph.json) and
by `clausal show`.

WHAT A CASE IS. A state and an input of the search grid (clausal/rsearch.py: the `sample` values of glossary.yaml), and
what the call does: an answer and the state it leaves, or no answer. "model": the outcome is what the Lean model of the
code gives there. "substituted": the same call made to give an outcome the model gives at ANOTHER grid point; the code
does not do this, the rule is asked what it would say if it did. A rule the code keeps has only substituted forbidden
cases.

Design, limits and the frozen tests: clausal/display_tests/README.md.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from . import projects, rsearch, vocab
from .core import Feature, Problem, Rule, load_glossary
from .pipeline import LEAN, OUT, ROOT
from .displaytext import KINDS, LETTER, render, say_values
from .vocab import Reading, base_cat, frame_text, state_paths

LIB = Path(__file__).with_name("display_lib.lean.txt")
WORK = ROOT / "build" / "display"
LEAN_TIMEOUT = 1800

# ------------------------------------------------------------------------------------------ units: one per claim

def clause_reading(rd: Reading, k: int) -> Reading:
    """One clause of a Rule line as a reading of its own, so that `rsearch.grid` gives the grid of THAT clause's operation."""
    g = rd.info["clauses"][k]
    r = Reading(rd.id, "rule", rd.source, rd.text)
    r.info = {"clauses": [g], "domain": rd.info["domain"]}
    r.claims = list(g["claims"])
    r.state_type, r.input_type = g["state_type"], g["input_type"]
    return r


def any_texts(voc, g: dict, c) -> tuple:
    """(operation, F.at, Frames.Check.F) of a claim as Lean text, with the operation's `run` a variable `run`: the claim
    as it would be stated of an operation that does something else. Built exactly as `Compiler.claim` builds `any_run`
    (the scoped operation with any `run`, then the claim's own modifiers), from the frame's `at:` and `check:` templates."""
    s = g["s"]
    op2 = s["op_any"]
    for m in c.mods:
        op2 = voc.pieces[m]["lean"].replace("{op}", op2)
    ctx = g["ctx"]
    keep, ctx.opbase = ctx.opbase, s["base_any"]
    try:
        at = frame_text(c.frame["at"], c.node, ctx, op2)
        chk = frame_text(c.frame["check"], c.node, ctx, op2)
    finally:
        ctx.opbase = keep
    mine = f"(Disp.withRun ({s['base']}) run)"       # see display_tests/README.md: the compiler's `{ op with run := run }` does not elaborate under `decide`
    return tuple(t.replace(s["base_any"], mine) for t in (op2, at, chk))


def first_vars(g: dict) -> list:
    """The grid variables that build the FIRST call (a two-call grid also has those of the second, over the same samples)."""
    second = {a[2] for a in g.get("actors2") or [] if a[2]} | {i[1] for i in g.get("inputs2") or [] if i[1]}
    return [v for v in g["vars"] if v[0] not in second]


def answer_printer(voc, op: dict) -> str:
    """How an answer of the operation is printed: the printer the old glossary names for the same model function, else by type."""
    for e in voc.gloss.entries if voc.gloss is not None and hasattr(voc.gloss, "entries") else []:
        if e.kind == "when" and getattr(e, "call", None) == op["model"] and e.raw.get("outcome_show"):
            return e.raw["outcome_show"]
    return "Disp.Show.text"


def state_printer(voc, ops: list) -> str:
    roles = ops[0]["state"]
    paths, _ = state_paths(len(roles), 0)
    shows = [voc.gloss.actors[t].get("show") for _, t in roles]
    if any(s is None for s in shows):
        return 'fun _ => "(a state with no printer)"'
    if len(roles) == 1:
        return f"fun st => {shows[0]} st"
    return "fun st => s!\"" + "; ".join(f"{r}: {{{sh} st{p}}}" for (r, _), sh, p in zip(roles, shows, paths)) + "\""


def units(voc, rd: Reading) -> list:
    out, n = [], 0
    for k, g in enumerate(rd.info["clauses"]):
        cr = clause_reading(rd, k)
        grid = rsearch.grid(voc, cr, None)
        for c in g["claims"]:
            out.append({"unit": f"{rd.id}#{n}", "rule": rd.id, "claim": n, "clause": k, "frame": c.frame["id"], "runs": c.runs,
                        "calls": c.calls, "c": c, "g": g, "grid": grid})
            n += 1
    return out


def unit_lean(voc, u: dict, name: str, neigh: list) -> str:
    """The Lean of one unit. `neigh`: [(clause dict, [claims])] of the neighbouring sentences (same operation, same runs)."""
    c, g, grid = u["c"], u["g"], u["grid"]
    two = c.runs == 2
    base = g["base"]
    op_any, at_any, chk_any = any_texts(voc, g, c)
    fv = first_vars(grid)
    pt = "st inp st2 inp2" if two else "st inp"
    L = [f"abbrev {name}.S := {g['state_type']}", f"abbrev {name}.A := {g['input_type']}", f"abbrev {name}.R := Disp.ansOf ({base})",
         f"def {name}.pts : Array ({name}.S × {name}.A) := Id.run do", f"  let mut out : Array ({name}.S × {name}.A) := #[]"]
    ind = "  "
    for n, typ, _, terms in fv:
        L.append(f"{ind}for {n} in ([{', '.join(terms)}] : List ({typ})) do")
        ind += "  "
    L += [f"{ind}out := out.push (({grid['st']} : {name}.S), ({grid['inp']} : {name}.A))", "  return out"]
    kind = "Two" if two else "One"
    L += [f"def {name}.unit : Disp.{kind} {name}.S {name}.A {name}.R where",
          f"  id := {json.dumps(u['unit'], ensure_ascii=False)}",
          f"  pts := {name}.pts",
          f"  real := ({base}).run",
          f"  acc := fun r => decide (({base}).accepted r)",
          f"  inScope := fun st inp => decide (({c.op}).scope st inp)"]
    if two:
        L.append(f"  rel := fun st inp st2 inp2 => decide ({rsearch.rel_of(voc, c)} st inp st2 inp2)")
    L += [f"  chkReal := fun {pt} => {c.check} {pt}",
          f"  chk := fun run {pt} => {chk_any} {pt}",
          f"  atd := fun run {pt} => decide ({at_any} {pt})",
          f"  obs := fun run st inp => Disp.seen (Frames.Op.observe ({op_any}) st inp)",
          f"  showAns := fun r => {answer_printer(voc, g['ops'][-1])} r",
          f"  showSt := {state_printer(voc, g['ops'])}"]
    fs = []
    for ng, ncs in neigh:
        fs.append(f"fun run {pt} => " + " && ".join(f"({any_texts(voc, ng, nc)[2]} {pt})" for nc in ncs))
    L.append("  neigh := #[" + ",\n            ".join(fs) + "]")
    L.append(f"#eval {name}.unit.run")
    return "\n".join(L) + "\n"


# ------------------------------------------------------------------------------------------ neighbouring sentences

def live_forms(voc, p: dict) -> list:
    out = []
    for field in ("forms", "vp_forms", "then_forms"):
        for f in p.get(field) or []:
            if (p["id"], field, f) not in voc.retired:
                out.append(f)
    return out


def shape(text: str) -> tuple:
    segs = vocab.segments(text)
    return [s[1] for s in segs if s[0] == "lit"], [s[2] for s in segs if s[0] == "hole"], [s[0] for s in segs]


def swap_form(sentence: str, old: str, new: str) -> str | None:
    """`sentence` with the literal words of form `old` replaced by those of form `new` (same holes, in the same order)."""
    lo, ho, ko = shape(old)
    ln, hn, kn = shape(new)
    if ho != hn or ko != kn or not lo:
        return None
    pos, out = 0, []
    for a, b in zip(lo, ln):
        at = sentence.find(a.strip(), pos)
        if at < 0:
            return None
        out.append(sentence[pos:at] + b.strip())
        pos = at + len(a.strip())
    return "".join(out) + sentence[pos:]


def neighbour_sentences(voc, rd: Reading, sentence: str) -> list:
    """[(sentence, what was changed)]: sentences one edit away from a single-clause Rule line. Candidates only: each is
    compiled by the ordinary compiler before it is used, and one that does not compile is dropped.
      1. a domain word or a frame of a claim swapped for another piece of the same category with the same holes
         (the variation: "the amount is the same or smaller" / "... or larger"; the frame: "never loses acceptance
         when" / "gives the same answer when");
      2. the subject narrowed to accepted or to rejected calls, or its narrowing word taken off;
      3. the subject's "for which <condition>" taken off."""
    if len(rd.info["clauses"]) != 1:
        return []
    g = rd.info["clauses"][0]
    text = sentence.strip()
    out = []

    def add(t, how):
        if t and t != text and all(t != x for x, _ in out):
            out.append((t, how))
    dom = rd.info["domain"]
    for c in g["claims"]:
        for n in vocab.walk([c.node]):
            if not isinstance(n, vocab.Node) or not n.form:
                continue
            p = n.piece
            for q in voc.pieces.values():
                if q is p or base_cat(q.get("cat", "")) != base_cat(p.get("cat", "")) or q.get("kind") != p.get("kind"):
                    continue
                if q.get("domain") not in (None, dom) or q.get("for_op") != p.get("for_op"):
                    continue
                for f in live_forms(voc, q):
                    add(swap_form(text, n.form, f), f"`{p['id']}` replaced by `{q['id']}`")
    art, words, noun = g["s"]["written"][0]
    old = art + "".join(w + " " for w in words) + noun
    at = text.lower().find(old.lower())
    if at >= 0:
        def subject(ws):
            first = (ws + [noun])[0]
            new = vocab.an(first, voc.live_articles) + "".join(w + " " for w in ws) + noun
            if at == 0 or text[at - 1] == " ":
                new = (new[0].upper() + new[1:]) if text[at].isupper() else new
            return text[:at] + new + text[at + len(old):]
        narrowing = [(m, w) for m, w in voc.live_word.items() if "calls" in voc.pieces[m]]
        mine = [w for w in words if any(w == x for _, x in narrowing)]
        if mine:
            add(subject([w for w in words if w not in mine]), f"the narrowing word '{mine[0]}' taken off the subject")
        else:
            for m, w in narrowing:
                add(subject([w] + words), f"the subject narrowed to {voc.pieces[m]['calls']} calls ('{w}')")
    for sep in voc.relatives:
        subj = g["subject"]
        if sep in subj and subj in text[0].lower() + text[1:]:
            low = text[0].lower() + text[1:]
            t = low.replace(subj, subj.split(sep)[0], 1)
            add(t[0].upper() + t[1:] if text[0].isupper() else t, "the condition on the subject taken off")
    return out


def distance(a: str, b: str) -> int:
    """How far a neighbour is: the number of words inserted, deleted or replaced."""
    x, y = a.split(), b.split()
    return sum(max(i2 - i1, j2 - j1) for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=x, b=y, autojunk=False).get_opcodes() if tag != "equal")


def neighbours(voc, comp, rd: Reading, sentence: str, books=None) -> list:
    """Compiled neighbours of a single-clause Rule line, nearest first: [{sentence, how, distance, reading}]. Kept only
    if the ordinary compiler (refusals on) compiles it in the same system, to a different term, about the SAME operation
    (same unscoped operation text, so the same state, input and answer), with every claim comparing as many calls."""
    g = rd.info["clauses"][0] if len(rd.info["clauses"]) == 1 else None
    if g is None:
        return []
    runs = {c.runs for c in g["claims"]}
    f = Feature(path="<neighbour>", name="neighbour", slug="neighbour")
    out = []
    for k, (t, how) in enumerate(neighbour_sentences(voc, rd, sentence)):
        got = comp.rule(Rule(feature=f, name=t, line=k + 1, tags=[f"@id:n{k}"]), rd.info["domain"], books)
        if isinstance(got, Problem) or len(got.info["clauses"]) != 1:
            continue
        ng = got.info["clauses"][0]
        if ng["base"] != g["base"] or {c.runs for c in ng["claims"]} != runs or len(runs) != 1:
            continue
        if got.lean_def().split(":=", 1)[1] == rd.lean_def().split(":=", 1)[1]:
            continue
        out.append({"sentence": t, "how": how, "distance": distance(sentence, t), "reading": got})
    out.sort(key=lambda n: n["distance"])
    return out


# ------------------------------------------------------------------------------------------ the script

def script(voc, items: list) -> tuple:
    """items: [{reading, sentence, neighbours}]. Returns (Lean text, sidecar)."""
    lib = LIB.read_text()
    imports = list(dict.fromkeys(list(voc.raw["lean_imports"]) + projects.load().search_imports()))
    head = ("-- GENERATED by clausal (clausal/display.py, plan node Q6). Do not edit; overwritten on every run.\n"
            "-- Run with `lake env lean` (interpreter). The computed display of every compiled Rule line: each claim evaluated on\n"
            "-- the model's outcomes and on substituted outcomes, through the frame's definition and its executable reading.\n"
            + "".join(f"import {i}\n" for i in imports)
            + "open Aeneas Aeneas.Std Result\nset_option linter.unusedVariables false\n\n" + lib + "\n")
    out, side, n = [head], {"units": {}, "rules": {}}, 0
    line = head.count("\n") + 1
    for it in items:
        rd = it["reading"]
        us = units(voc, rd)
        nbs = it.get("neighbours") or []
        side["rules"][rd.id] = {"sentence": it["sentence"], "source": rd.source, "units": [u["unit"] for u in us],
                                "neighbours": [{"sentence": x["sentence"], "how": x["how"], "distance": x["distance"]} for x in nbs]}
        for u in us:
            neigh = [(x["reading"].info["clauses"][0], x["reading"].info["clauses"][0]["claims"]) for x in nbs] if len(us) == 1 else []
            text = f"-- {u['unit']}: {it['sentence']}\n" + unit_lean(voc, u, f"DU{n}", neigh)
            fv = first_vars(u["grid"])
            side["units"][u["unit"]] = {"rule": rd.id, "claim": u["claim"], "clause": u["clause"], "frame": u["frame"], "runs": u["runs"],
                                        "calls": u["calls"], "vars": [(v[0], v[2]) for v in fv], "lines": [line, line + text.count("\n")],
                                        "operation": [o["id"] for o in u["g"]["ops"]],
                                        "nouns": [vocab.an(o["nouns"][0], voc.live_articles) + o["nouns"][0] for o in u["g"]["ops"]],
                                        "neighbours": len(neigh)}
            out.append(text)
            line += text.count("\n") + 1
            n += 1
    return "\n".join(out), side


# ------------------------------------------------------------------------------------------ reading Lean's answer

def point(vars_: list, i: int) -> dict:
    """The values of grid point `i` (the LAST variable runs fastest, as in the generated loops)."""
    idx = []
    for _, vals in reversed(vars_):
        idx.append(i % len(vals))
        i //= len(vals)
    idx.reverse()
    return {n: vals[j] for (n, vals), j in zip(vars_, idx)}


def outcome(fields: list) -> dict:
    k = int(fields[0])
    return {"kind": KINDS[k]} if k == 2 else {"kind": KINDS[k], "answer": fields[1], "after": fields[2]}


def frac(t: str):
    a, b = t.split("/")
    return [int(a), int(b)]


def parse(log: str, side: dict) -> dict:
    """unit id -> what Lean printed for it (raw), or {"error": ...}."""
    res = {u: {"cells": {}, "cases": []} for u in side["units"]}
    for l in log.splitlines():
        p = l.split("\t")
        if len(p) < 2 or p[1] not in res:
            continue
        r, s = res[p[1]], side["units"][p[1]]
        if p[0] == "DPOOL":
            r["pool"], r["pool_kinds"] = int(p[2]), p[3]
        elif p[0] == "DKINDS":
            r["point_kinds"] = p[2]
        elif p[0] == "DPTS":
            r["points"], r["in_scope"], r["third"] = int(p[2]), int(p[3]), int(p[4])
        elif p[0] == "DGRID":
            r["grid"] = {"n": int(p[2]), "agree": int(p[3]), "first_difference": None if p[4] == "-" else p[4]}
        elif p[0] == "DPROBE":
            r["probe"] = {"accepted": frac(p[2]), "rejected": frac(p[3]), "silent": None if p[4] == "-" else frac(p[4])}
        elif p[0] == "DAGREE":
            r["definition"] = {"n": int(p[2]), "agree": int(p[3]), "first_difference": None if p[4] == "-" else p[4]}
        elif p[0] == "DREF":
            r["reference"] = [point(s["vars"], int(p[2])), point(s["vars"], int(p[3]))]
        elif p[0] == "DNOREF":
            r["no_reference"] = True
        elif p[0] == "DCELL":
            r["cells"][LETTER[int(p[2])] + LETTER[int(p[3])]] = {"n": int(p[4]), "true": int(p[5]), "eq": int(p[6]), "seen": int(p[7])}
        elif p[0] == "DCASE":
            r["cases"].append({"which": p[2], "how": p[3], "values": point(s["vars"], int(p[4])), "outcome": outcome(p[5:8])})
        elif p[0] == "DCASE2":
            r["cases"].append({"which": p[2], "how": p[3], "values": point(s["vars"], int(p[4])), "values2": point(s["vars"], int(p[5])),
                               "outcome": outcome(p[6:9]), "outcome2": outcome(p[9:12])})
        elif p[0] == "DNEIGH":
            r["neigh"] = p[2] if len(p) > 2 else ""
        elif p[0] == "DONE":
            r["done"] = True
    errs = {}
    for m in re.finditer(r"^\S*?:(\d+):\d+: error[^\n]*(?:\n(?!\S*?:\d+:\d+: )[^\n]*){0,6}", log, re.M):
        errs.setdefault(int(m.group(1)), m.group(0).strip()[:900])
    for u, r in res.items():
        if not r.get("done"):
            a, b = side["units"][u]["lines"]
            mine = [t for ln, t in sorted(errs.items()) if a <= ln <= b]
            res[u] = {"error": mine[0] if mine else "Lean printed no result for this claim (see the log)"}
    return res


def label(cell: dict) -> str:
    if cell["n"] == 0:
        return "empty"
    if cell["true"] == cell["n"]:
        return "allowed"
    if cell["true"] == 0:
        return "forbidden"
    return "same" if cell["eq"] == cell["n"] else "mixed"


def calls_seen(r: dict, two: bool) -> dict:
    """What the executable reading does with an accepted answer, a rejected answer and no answer, and which Calls values
    that is consistent with. None: not probed (the operation has no such outcome among the samples)."""
    def looked(x):
        return None if x[1] == 0 else True if x[0] == x[1] else False if x[0] == 0 else "partly"
    a, rj = looked(r["probe"]["accepted"]), looked(r["probe"]["rejected"])
    if two:
        cells = [c for k, c in r["cells"].items() if "n" in k and c["n"]]
        silent = None if not cells else True if all(c["true"] == 0 for c in cells) else False if all(c["true"] == c["n"] for c in cells) else "partly"
    else:
        silent = looked(r["probe"]["silent"])
    want = {"every": (True, True, True), "accepted": (True, False, False), "rejected": (False, True, False)}
    ok = [k for k, w in want.items() if all(x is None or x == y for x, y in zip((a, rj, silent), w))]
    return {"accepted_looked_at": a, "rejected_looked_at": rj, "no_answer_breaks": silent, "consistent_with": ok}


def summarise(side: dict, raw: dict) -> dict:
    """rule id -> the display (JSON): per claim the covers line, the table, the cases, the neighbour and the checks."""
    out = {}
    for rid, rs in side["rules"].items():
        d = {"rule": rid, "sentence": rs["sentence"], "source": rs["source"], "claims": []}
        for u in rs["units"]:
            s, r = side["units"][u], raw[u]
            c = {"unit": u, "frame": s["frame"], "runs": s["runs"], "calls": s["calls"], "operation": s["operation"], "nouns": s["nouns"],
                 "variables": [n for n, _ in s["vars"]], "samples": {n: len(v) for n, v in s["vars"]}}
            if "error" in r:
                c["error"] = r["error"]
                d["claims"].append(c)
                continue
            two = s["runs"] == 2
            seen = calls_seen(r, two) if not r.get("no_reference") else {"consistent_with": [s["calls"]], "not_probed": True}
            c["covers"] = {"calls": seen["consistent_with"][0] if len(seen["consistent_with"]) == 1 else s["calls"] if s["calls"] in seen["consistent_with"] else None,
                           "seen": seen, "agrees_with_calls_value": s["calls"] in seen["consistent_with"],
                           "points": r["points"], ("pairs_in_scope" if two else "in_scope"): r["in_scope"],
                           **({"pairs_of_different_calls": r["third"]} if two else {})}
            if two:
                c["table"] = None if r.get("no_reference") else {
                    "cells": {k: {"label": label(v), "outcome_pairs": v["n"], "allowed": v["true"], "model_pairs_on_grid": v["seen"]}
                              for k, v in sorted(r["cells"].items(), key=lambda kv: (LETTER.index(kv[0][0]), LETTER.index(kv[0][1])))},
                    "outcomes_substituted": r["pool"], "at": r.get("reference")}
                c["point_kinds"] = r.get("point_kinds")
            ok = [x for x in r["cases"] if x["which"] == "allowed"]
            bad = sorted((x for x in r["cases"] if x["which"] == "forbidden"),
                         key=lambda x: (not (x["how"] == "model"), x["how"] == "silent"))
            # the model's own violation first, then a substituted answer, then silence (the same order as the script's)
            real = [x for x in r["cases"] if x["which"] == "forbidden" and x["how"] == "model"]
            c["allowed"] = ok[0] if ok else None
            c["forbidden"] = (real or bad or [None])[0]
            c["forbidden_cases"] = len(bad)
            c["checks"] = {"table_or_reading_against_Claim_check_on_grid": r.get("grid"), "definition_against_executable_reading": r.get("definition")}
            c["neighbour"] = None
            if c["forbidden"] and s["neighbours"] and r.get("neigh") is not None:
                allows = [n for n, b in zip(rs["neighbours"], r["neigh"]) if b == "1"]
                c["neighbours_tried"] = len(rs["neighbours"])
                c["neighbours_allowing"] = [n["sentence"] for n in allows]
                if allows:
                    c["neighbour"] = dict(allows[0])
            d["claims"].append(c)
        out[rid] = d
    return out


def problems(disp: dict, rs: dict | None = None, side: dict | None = None) -> list:
    """What must hold of every display (gates T1, T1b, T4, T5, T6 of display_tests/expected.json), as a list of faults."""
    bad = []
    for rid, d in disp.items():
        for c in d["claims"]:
            u = c["unit"]
            if "error" in c:
                bad.append(f"{u}: no display: {c['error'].splitlines()[0][:300]}")
                continue
            g = c["checks"]["table_or_reading_against_Claim_check_on_grid"]
            if c["runs"] == 2 and c["table"] is None:
                bad.append(f"{u}: no outcome table: the grid has no pair of different calls in scope and related")
            elif g is None or (g["n"] == 0 and c["runs"] == 2):
                bad.append(f"{u}: nothing on the grid is in scope, so the table was compared with nothing")
            elif g["agree"] != g["n"]:
                bad.append(f"{u}: the {'table' if c['runs'] == 2 else 'reading with the outcome substituted'} differs from the compiler's "
                           f"executable reading at {g['n'] - g['agree']} of {g['n']} grid {'pairs' if c['runs'] == 2 else 'points'} (first: {g['first_difference']})")
            e = c["checks"]["definition_against_executable_reading"]
            if e and e["agree"] != e["n"]:
                bad.append(f"{u}: the frame's definition and its executable reading differ on {e['n'] - e['agree']} of {e['n']} substituted outcomes")
            if not c["covers"]["agrees_with_calls_value"]:
                bad.append(f"{u}: the claim's Calls value is `{c['calls']}`, but on substituted outcomes the executable reading behaves as "
                           f"{c['covers']['seen']}")
    if rs is not None and side is not None:
        for rid, d in disp.items():
            bad += [f"{rid}: {x}" for x in against_search(d, rs.get(rid), side)]
    return bad


def against_search(d: dict, r: dict | None, side: dict) -> list:
    """T1b, the independent path: the cell labels of a two-call table against the bits the READING SEARCH printed
    (`decide (F.at ...)` of the model at every pair; clausal/rsearch.py). Only for a Rule line of one clause and one claim."""
    if not r or "bits" not in r or len(d["claims"]) != 1:
        return []
    c = d["claims"][0]
    if c.get("error") or c["runs"] != 2 or not c.get("table") or r.get("layout") != [["scope", 0], ["rel", 0], ["at", 0]]:
        return []
    kinds = c["point_kinds"]
    n, w = len(kinds), r["width"]
    if len(r["bits"]) != n * n * w:
        return [f"the reading search has {len(r['bits'])} bits where {n}*{n}*{w} were expected"]
    bit = lambda i, j, k: r["bits"][(i * n + j) * w + k] == "1"
    scope = [bit(i, 0, 0) for i in range(n)]
    bad, seen = [], 0
    for i in range(n):
        for j in range(n):
            if scope[i] and scope[j] and bit(i, j, 1):
                seen += 1
                lab = c["table"]["cells"][LETTER[int(kinds[i])] + LETTER[int(kinds[j])]]["label"]
                if (lab == "allowed" and not bit(i, j, 2)) or (lab in ("forbidden", "empty") and bit(i, j, 2)):
                    bad.append(f"pair ({i}, {j}): the table says {lab}, the reading search says the statement is {'true' if bit(i, j, 2) else 'false'} there")
    c["checks"]["cells_against_the_reading_search"] = {"pairs": seen, "inconsistent": len(bad)}
    return bad[:5]


# ------------------------------------------------------------------------------------------ running

def env() -> dict:
    e = dict(os.environ)
    e["PATH"] = f"{Path.home()}/.elan/bin:{Path.home()}/.cargo/bin:" + e.get("PATH", "")
    return e


def run_lean(path: Path, log: Path) -> str:
    try:
        p = subprocess.run(["lake", "env", "lean", str(path)], cwd=LEAN, env=env(), capture_output=True, text=True, timeout=LEAN_TIMEOUT)
        text = p.stdout + p.stderr
    except subprocess.TimeoutExpired as e:
        text = (e.stdout.decode() if isinstance(e.stdout, bytes) else e.stdout or "") + f"\nDISPLAY-TIMEOUT after {LEAN_TIMEOUT} s\n"
    log.write_text(text)
    return text


def compute(voc, items: list, work: Path) -> tuple:
    """Write the script for `items`, run it, read it back: (rule id -> display, sidecar, raw log path)."""
    work.mkdir(parents=True, exist_ok=True)
    text, side = script(voc, items)
    (work / "Display.lean").write_text(text)
    (work / "display_side.json").write_text(json.dumps(side, indent=1, ensure_ascii=False))
    log = run_lean(work / "Display.lean", work / "display.log")
    return summarise(side, parse(log, side)), side, work / "display.log"


# ---- the pipeline: every compiled Rule line of the fixtures (clausal gen writes the script, run.sh runs it, `clausal display` reads it)

def fixture_items(st) -> list:
    comp = vocab.Compiler(st.voc)
    out = []
    for r, rd in st.rules:
        if isinstance(rd, Reading):
            books = projects.books_of(st.projects, r.feature.path)
            out.append({"reading": rd, "sentence": r.name.strip(), "neighbours": neighbours(st.voc, comp, rd, r.name.strip(), books)})
    return out


def write_script(st) -> dict:
    text, side = script(st.voc, fixture_items(st))
    (LEAN / "Run" / "Display.lean").write_text(text)
    (ROOT / "build").mkdir(exist_ok=True)
    (ROOT / "build" / "display.json").write_text(json.dumps(side, indent=1, ensure_ascii=False))
    return side


def cmd_collect() -> int:
    """After lean/Run/Display.lean ran: out/display.json, and the checks. Exit 1 on a fault of the display (never a verdict)."""
    side = json.loads((ROOT / "build" / "display.json").read_text())
    log = (OUT / "display.log").read_text() if (OUT / "display.log").exists() else ""
    disp = summarise(side, parse(log, side))
    rs = None
    if (OUT / "rsearch.log").exists() and (ROOT / "build" / "rsearch_grid.json").exists():
        rs = rsearch.parse((OUT / "rsearch.log").read_text(), json.loads((ROOT / "build" / "rsearch_grid.json").read_text()))
    bad = problems(disp, rs, side)
    cl = [c for d in disp.values() for c in d["claims"]]
    two = [c for c in cl if c["runs"] == 2 and "error" not in c]
    counts = {"rules": len(disp), "claims": len(cl), "errors": sum("error" in c for c in cl), "two_call_claims": len(two),
              "grid_evaluations": sum((c["checks"]["table_or_reading_against_Claim_check_on_grid"] or {}).get("n", 0) for c in cl if "error" not in c),
              "grid_agree": sum((c["checks"]["table_or_reading_against_Claim_check_on_grid"] or {}).get("agree", 0) for c in cl if "error" not in c),
              "two_call_pairs": sum(c["checks"]["table_or_reading_against_Claim_check_on_grid"]["n"] for c in two if c["checks"]["table_or_reading_against_Claim_check_on_grid"]),
              "two_call_pairs_agree": sum(c["checks"]["table_or_reading_against_Claim_check_on_grid"]["agree"] for c in two if c["checks"]["table_or_reading_against_Claim_check_on_grid"]),
              "substituted_evaluations": sum((c["checks"]["definition_against_executable_reading"] or {}).get("n", 0) for c in cl if "error" not in c),
              "substituted_agree": sum((c["checks"]["definition_against_executable_reading"] or {}).get("agree", 0) for c in cl if "error" not in c),
              "search_pairs": sum(c["checks"].get("cells_against_the_reading_search", {}).get("pairs", 0) for c in two),
              "search_inconsistent": sum(c["checks"].get("cells_against_the_reading_search", {}).get("inconsistent", 0) for c in two),
              "covers_mismatches": sum(not c["covers"]["agrees_with_calls_value"] for c in cl if "error" not in c),
              "claims_without_forbidden_case": [c["unit"] for c in cl if "error" not in c and not has_forbidden(c)],
              "rules_with_neighbour": sum(any(c.get("neighbour") for c in d["claims"]) for d in disp.values())}
    OUT.mkdir(exist_ok=True)
    (OUT / "display.json").write_text(json.dumps({"ok": not bad, "problems": bad, "counts": counts, "displays": disp}, indent=1, ensure_ascii=False))
    print(f"  display (Q6): {counts['claims'] - counts['errors']} of {counts['claims']} claims of {counts['rules']} compiled Rule lines displayed; "
          f"against the compiler's executable reading on the grid: {counts['grid_agree']} of {counts['grid_evaluations']} evaluations the same "
          f"(two-call tables: {counts['two_call_pairs_agree']} of {counts['two_call_pairs']} pairs, {counts['two_call_claims']} tables); "
          f"definition against executable reading on substituted outcomes: {counts['substituted_agree']} of {counts['substituted_evaluations']}; "
          f"table cells against the reading search: {counts['search_inconsistent']} inconsistent of {counts['search_pairs']} pairs; "
          f"covers line against the Calls value: {counts['covers_mismatches']} mismatches; "
          f"{len(counts['claims_without_forbidden_case'])} claims with no forbidden case found; a neighbour for {counts['rules_with_neighbour']} Rule lines")
    for b in bad:
        print(f"  DISPLAY CHECK FAILED: {b}")
    return 1 if bad else 0


def has_forbidden(c: dict) -> bool:
    if c["runs"] == 2 and c.get("table"):
        return any(x["label"] in ("forbidden", "same", "mixed") for x in c["table"]["cells"].values())
    return c.get("forbidden") is not None


def load_out() -> dict:
    p = OUT / "display.json"
    return json.loads(p.read_text())["displays"] if p.exists() else {}


# ---- clausal show

def show(sentence: str, refuse: bool = True, sep: bool = True, rust: bool = True) -> dict:
    gl = load_glossary(ROOT / "glossary.yaml", "glossary.yaml")
    voc = vocab.load_project(ROOT, gl)
    comp = vocab.Compiler(voc, refuse_vacuous=refuse)
    strict = vocab.Compiler(voc)                    # a neighbour is a sentence of the language: always compiled with the refusals on
    f = Feature(path="<show>", name="show", slug="show")
    res = {"sentence": sentence, "refusal_switched_off": not refuse, "systems": []}
    items = []
    for n, d in enumerate(sorted({o["domain"] for o in voc.ops.values()})):
        got = comp.rule(Rule(feature=f, name=sentence, line=n + 1, tags=[f"@id:show_{d}"]), d)
        if isinstance(got, Problem):
            res["systems"].append({"system": d, "compiled": False, "status": got.status, "code": got.code, "message": got.message, "hint": got.hint})
        else:
            res["systems"].append({"system": d, "compiled": True, "id": got.id, "lean": got.lean_def()})
            items.append({"reading": got, "sentence": sentence, "neighbours": neighbours(voc, strict, got, sentence)})
    if not items:
        return res
    digest = hashlib.sha256(json.dumps([sentence, refuse, [it["reading"].lean_def() for it in items]], ensure_ascii=False).encode()).hexdigest()[:12]
    work = WORK / digest
    disp, side, log = compute(voc, items, work)
    res["lean"] = {"script": str(work / "Display.lean"), "log": str(log), "command": f"(cd {LEAN} && lake env lean {work / 'Display.lean'})"}
    res["problems"] = problems(disp)
    for s in res["systems"]:
        if s["compiled"]:
            s["display"] = disp[s["id"]]
            if sep:
                for c in s["display"]["claims"]:
                    confirm(c, sentence, s["system"], rust)
    return res


def confirm(c: dict, sentence: str, system: str, rust: bool) -> None:
    """`clausal separate` on the rule and each neighbour that allows the forbidden case, nearest first (at most three): the
    first for which it finds a separating input ON THE MODEL is the neighbour shown, with that input; if it finds none,
    the nearest stays and the line says so (the two differ on a substituted outcome only: nothing the code does tells them apart)."""
    from . import separate
    tried = []
    for t in (c.get("neighbours_allowing") or [])[:3]:
        r = separate.separate([sentence, t], rust=rust)
        cmp_ = next((x for x in r["comparisons"] if x["a"] == f"A/{system}" and x["b"] == f"B/{system}"), None)
        v = cmp_["verdict"] if cmp_ else "NOT-COMPARED"
        tried.append((t, v, cmp_))
        if v == "SEPARATED":
            break
    if not tried or not c.get("neighbour"):
        return
    t, v, cmp_ = next((x for x in tried if x[1] == "SEPARATED"), tried[0])
    if t != c["neighbour"]["sentence"]:
        c["neighbour"]["sentence"] = t
    c["neighbour"]["separate_verdict"] = v
    c["neighbour"]["separate_tried"] = [[x, y] for x, y, _ in tried]
    if v == "SEPARATED":
        p = cmp_["separating"][0]
        c["neighbour"]["separating_input"] = p["values"]
        c["neighbour"]["separate"] = (f"clausal separate: SEPARATED on the model at {say_values(p['values'])} "
                                      f"({'the rule' if p['holds'].startswith('A') else 'the neighbour'} holds there, the other fails)")
    else:
        c["neighbour"]["separate"] = (f"clausal separate: {v} on the model's grid: the two differ on the substituted outcome above, "
                                      "and on nothing the model does within the bounds searched")


def render_show(res: dict) -> str:
    o = [f"Rule: {res['sentence']}" + ("   [compiled with the refusal of rules that say nothing SWITCHED OFF]" if res["refusal_switched_off"] else "")]
    got = [s for s in res["systems"] if s["compiled"]]
    if not got:
        # the refusal shown: one that says the line IS a composition and says nothing (it was read; the others were not), else
        # the one the compiler itself would report across systems
        best = sorted(res["systems"], key=lambda s: (s["status"] != "SAYS-NOTHING", vocab.rank_problem(Problem(s["status"], s["code"], 0, s["message"], "")),
                                                     -len(s["message"])))[0]
        o.append(f"  REFUSED ({best['status']}): no display. {best['message']}")
        if best.get("hint"):
            o.append(f"  {best['hint']}")
        return "\n".join(o)
    for s in got:
        if len(got) > 1:
            o.append(f"-- read as a statement of the {s['system']}")
        o.append("  " + s["lean"].split(":=", 1)[1].strip().replace("\n", "\n  "))
        o += render(s["display"])
    for p in res.get("problems", []):
        o.append(f"  DISPLAY CHECK FAILED: {p}")
    o.append(f"  (script and log: {res['lean']['script']}, {res['lean']['log']})")
    return "\n".join(o)


def main(argv) -> int:
    flags = {a for a in argv if a.startswith("--")}
    sentences = [a for a in argv if not a.startswith("--")]
    if len(sentences) != 1 or flags - {"--json", "--no-refusal", "--no-separate", "--no-rust"}:
        print(__doc__)
        return 2
    res = show(sentences[0], refuse="--no-refusal" not in flags, sep="--no-separate" not in flags, rust="--no-rust" not in flags)
    print(json.dumps(res, indent=1, ensure_ascii=False) if "--json" in flags else render_show(res))
    return 0 if any(s["compiled"] for s in res["systems"]) and not res.get("problems") else 1
