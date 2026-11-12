"""clausal rsearch: every compiled reading evaluated on generated inputs, TWO ways.

lean/Run/ReadingSearch.lean (generated; run once per pipeline run by the interpreter) walks a grid of
outline parameters, states and inputs for every reading (scenario or Rule) and, at each point and for each
frame the reading is made of, evaluates

    decide (F.at op holes st inp)      the DEFINITION of the frame at that call (lean/Frames/Frames.lean)
    Frames.Check.F op holes st inp     the independent EXECUTABLE reading          (lean/Frames/Check.lean)

It reports, per reading: how many points were tried, how many are in scope, on how many (point, frame)
evaluations the two readings agree, the first point where they differ, and the first point where the
definition says the reading is false (a counterexample to the reading itself, found without the old
glossary). Per frame of the reading it also counts the points at which the definition is FALSE, at which
the call is in scope and gives NO ANSWER, and at which the call gives an answer the frame is ABOUT: so a
clause about rejected calls that covers no call is seen, and so is a comparison that never met a false
claim or a silent call (such a comparison cannot tell a right checker from a wrong one). This is the FRET practice of giving each template two semantics and testing one against the
other; here it is done on the concrete operations of the project, and it doubles as the counterexample
search for `Rule:` statements.
"""
from __future__ import annotations

import json
import re

from . import emit, projects
from .core import Bound
from .vocab import Reading


def nest(parts) -> str:
    cur = parts[0]
    for p in parts[1:]:
        cur = f"({cur}, {p})"
    return cur

HEADER = emit.HEADER


def lit(voc, typ: str, text: str) -> str:
    t = emit.lit_term(voc.pts, typ, text)
    return t if "enum" in voc.pts[typ] else "(" + t + ")"


def sample(voc, typ: str, b: Bound | None) -> list:
    if b is not None:
        return emit.grid_values(b, typ)
    pt = voc.pts[typ]
    return list(pt["enum"]) if "enum" in pt else [str(v) for v in pt.get("sample", [])]


def two_run(rd: Reading) -> bool:
    return any(c.runs == 2 for c in rd.claims)


def grid(voc, rd: Reading, b: Bound | None) -> dict:
    """{vars: [(name, lean type, [literal text], [lean term])], st: Lean term, inp: Lean term} and, for the Rust side
    (clausal/trees.py), which grid variable builds which actor and which is which input:
    actors: [(actor as written, actor type, grid variable)], inputs: [(type | None, grid variable | None, literal | None, name in the trees)],
    types: grid variable -> literal type. A reading that compares two calls also has st2 / inp2 / actors2 / inputs2."""
    vars_ = []
    gl = voc.gloss
    types, actors_, inputs_ = {}, [], []

    def var(name, typ):
        vals = sample(voc, typ, b)
        vars_.append((name, voc.pts[typ]["lean"], vals, [lit(voc, typ, v) for v in vals]))
        types[name] = typ
        return name

    def actor(name, atype, text=None, into=None):
        bd = gl.actors[atype]["build"]
        (actors_ if into is None else into).append((text, atype, name))
        return "(" + bd["with"].format(var(name, bd["param_type"])) + ")"

    taken = {"st", "inp"} | {n for n, _ in rd.outer}

    def fresh(name):
        name = re.sub(r"\W", "_", name)
        while name in taken:
            name += "_"
        taken.add(name)
        return name

    if rd.kind == "scenario":
        info = rd.info
        for n, _ in rd.outer:
            var(n, info["ptypes"][n])
        ops, ctx = info["ops"], info["ctx"]
        # each actor's state is its own grid variable, named after the actor ("Alice" -> alice_state)
        parts = [actor(fresh(a.split()[-1].lower() + "_state"), t, a) for a, (_, t) in zip(info["st_actors"], ops[0]["state"])]
        st = parts[0] if len(parts) == 1 else "(" + ", ".join(parts) + ")"
        for a in info["bystanders"]:
            st = f"({st}, {actor(fresh(a.split()[-1].lower() + '_state'), ctx.actor_type[a], a)})"
        ins = []
        for k, (o, bind) in enumerate(zip(ops, info["binds"])):
            if not o["input"]:
                ins.append("()")
                inputs_.append((None, None, None, None))
                continue
            leaf = bind[o["input"][0][0]]
            if leaf.how == "param":
                v = var(fresh(leaf.param), leaf.type)
                ins.append(v)
                inputs_.append((leaf.type, v, None, leaf.param))
            else:
                ins.append(ctx.value(leaf))
                inputs_.append((leaf.type, None, leaf.text, None))
        return {"vars": vars_, "st": st, "inp": nest(ins), "actors": actors_, "inputs": inputs_, "types": types}
    ops = rd.info["clauses"][0]["ops"]
    if rd.info["clauses"][0].get("tie") is not None:
        ops = ops[:1]       # a tied sequence has ONE input, the first call's: the tie makes the second call's (on both sides)
    # named "the_<role>": a bare role name such as `ledger` would shadow the Lean namespace of the model
    parts = [actor(fresh("the_" + r), t, "the " + r) for r, t in ops[0]["state"]]
    st = parts[0] if len(parts) == 1 else "(" + ", ".join(parts) + ")"
    ins = []
    for o in ops:
        if o["input"]:
            v = var(fresh("the_" + o["input"][0][0]), o["input"][0][1])
            ins.append(v)
            inputs_.append((o["input"][0][1], v, None, "the " + o["input"][0][0]))
        else:
            ins.append("()")
            inputs_.append((None, None, None, None))
    out = {"vars": vars_, "st": st, "inp": nest(ins), "actors": actors_, "inputs": inputs_, "types": types}
    if two_run(rd):      # the second call: its own state and input, over the same samples
        a2, i2 = [], []
        parts = [actor(fresh("the_" + r + "_2"), t, "the " + r, a2) for r, t in ops[0]["state"]]
        ins = []
        for o in ops:
            if o["input"]:
                v = var(fresh("the_" + o["input"][0][0] + "_2"), o["input"][0][1])
                ins.append(v)
                i2.append((o["input"][0][1], v, None, "the " + o["input"][0][0]))
            else:
                ins.append("()")
                i2.append((None, None, None, None))
        out.update({"st2": parts[0] if len(parts) == 1 else "(" + ", ".join(parts) + ")", "inp2": nest(ins), "actors2": a2, "inputs2": i2})
    return out


def same_grid(rd: Reading) -> bool:
    """A Rule whose clauses are about different operations has no single grid; it is searched clause by clause
    only if every clause shares the state and input types of the first."""
    if rd.kind != "rule":
        return True
    cl = rd.info["clauses"]
    return all(c["state_type"] == cl[0]["state_type"] and c["input_type"] == cl[0]["input_type"] for c in cl)


def unit_ops(rd: Reading) -> list:
    """The scoped operation of each unit of a reading (a scenario: one; a Rule: one per clause), with its claims' indexes."""
    if rd.kind == "scenario":
        return [(rd.op, list(range(len(rd.claims))))]
    out, k = [], 0
    for g in rd.info["clauses"]:
        out.append((g["op"], list(range(k, k + len(g["claims"])))))
        k += len(g["claims"])
    return out


def rel_of(voc, c) -> str | None:
    """The relation between the two calls a two-run claim compares, as Lean text."""
    from .vocab import Node, base_cat, render
    for v in (c.node.args.values() if c.node is not None else []):
        if isinstance(v, Node) and base_cat(v.cat) == "variation":
            return v.piece["lean"]
    return None


def row_point(voc, rd: Reading, sc, cells: dict) -> dict | None:
    """The state and the input of ONE Examples row (or of a plain Scenario), as Lean terms: each actor is built from the
    Given that fixes it (`<measure that is the whole actor> is <value>`). None if some actor has no such Given."""
    from .vocab import Leaf, Node
    gl, info = voc.gloss, rd.info
    ctx = info["ctx"]

    def val(leaf):
        return lit(voc, leaf.type, cells[leaf.param] if leaf.how == "param" else leaf.text)
    built = {}
    for c in rd.conds:
        n = c["node"]
        if isinstance(n, Node) and n.id == "is" and isinstance(n.args["m"], Node) and n.args["m"].piece.get("builds"):
            who = next(iter(n.args["m"].args.values()))
            t = n.args["t"]
            leaf = next(iter(t.args.values())) if isinstance(t, Node) and len(t.args) == 1 else None
            if isinstance(who, Leaf) and isinstance(leaf, Leaf) and leaf.kind == "value" and who.text not in built:
                bd = gl.actors[who.type]["build"]
                if leaf.type == bd["param_type"]:
                    built[who.text] = "(" + bd["with"].format(val(leaf)) + ")"
    names = info["st_actors"] + info["bystanders"]
    if any(a not in built for a in names):
        return None
    parts = [built[a] for a in info["st_actors"]]
    st = parts[0] if len(parts) == 1 else "(" + ", ".join(parts) + ")"
    for a in info["bystanders"]:
        st = f"({st}, {built[a]})"
    ins = []
    for o, bind in zip(info["ops"], info["binds"]):
        ins.append(val(bind[o["input"][0][0]]) if o["input"] else "()")
    outer = {n: lit(voc, info["ptypes"][n], cells[n]) for n, _ in rd.outer}
    return {"st": st, "inp": nest(ins), "outer": outer}


def rows_of(sc) -> list:
    """[(row number, line, {column: cell})] of a scenario: its Examples rows, or itself if it is a plain Scenario."""
    if sc.outline:
        return [(n, line, dict(zip(sc.header, cells))) for n, (line, cells) in enumerate(sc.rows, 1)]
    return [(1, sc.line, {})]


def search_file(voc, items, rows=()) -> tuple:
    """items: [(Reading, Bound | None)]; rows: [(Reading, Scenario)] whose Examples rows are evaluated on the model through
    the reading itself (the NEW sentences). Returns (Lean text, sidecar dict id -> grid description)."""
    out = [HEADER + "-- Run once per pipeline run with `lake env lean Run/ReadingSearch.lean` (interpreter).\n"
           "-- Every compiled reading on a grid of generated inputs, evaluated two ways: through the DEFINITION of\n"
           "-- each frame (decide (F.at ...)) and through its independent executable reading (Frames.Check.F ...).\n"
           "import Wallet.Readings\n" + "".join(f"import {m}\n" for m in projects.load().search_imports())
           + "open Aeneas Aeneas.Std Result\n"
           "set_option linter.unusedVariables false\n\n"
           "def rbits (l : List Bool) : String := String.ofList (l.map fun b => if b then '1' else '0')\n"
           "def radd (a l : List Nat) : List Nat := List.zipWith (· + ·) a l\n"
           "def rnums (l : List Nat) : String := \",\".intercalate (l.map toString)\n"
           "/-- what one call showed: (in scope and no answer, an answer the claim is about) -/\n"
           "def rseen {ρ σ : Type} : Frames.Seen ρ σ → Nat × Nat\n"
           "  | .noAnswer => (1, 0)\n  | .answered _ _ => (0, 1)\n  | _ => (0, 0)\n"]
    side, main = {}, []
    for k, (rd, b) in enumerate(items):
        if not same_grid(rd):
            side[rd.id] = {"skipped": "its clauses are about operations with different states or inputs"}
            continue
        g = grid(voc, rd, b)
        two = two_run(rd)
        side[rd.id] = {"vars": [(n, vals) for n, _, vals, _ in g["vars"]], "frames": [c.frame["id"] for c in rd.claims],
                       "claims": [{"frame": c.frame["id"], "mods": c.mods, "calls": c.calls, "echo": c.echo} for c in rd.claims],
                       "st": g["st"], "inp": g["inp"], "terms": {n: terms for n, _, _, terms in g["vars"]},
                       "st2": g.get("st2"), "inp2": g.get("inp2"),
                       "rust": {"actors": g["actors"], "inputs": g["inputs"], "types": g["types"],
                                "actors2": g.get("actors2"), "inputs2": g.get("inputs2")}}
        fn = [f"def rs{k} : IO Unit := do",
              "  let mut tried := 0", "  let mut inScope := 0", "  let mut evals := 0", "  let mut agree := 0",
              "  let mut diff : Option String := none", "  let mut bad : Option String := none",
              "  let mut sat : Option String := none",
              "  let mut bits : String := \"\"",
              f"  let mut nFalse : List Nat := List.replicate {len(rd.claims)} 0",
              f"  let mut nSilent : List Nat := List.replicate {len(rd.claims)} 0",
              f"  let mut nAbout : List Nat := List.replicate {len(rd.claims)} 0"]
        ind = "  "
        for i, (n, typ, _, terms) in enumerate(g["vars"]):
            fn.append(f"{ind}for ({n}, i{i}) in ([{', '.join(terms)}] : List ({typ})).zipIdx do")
            ind += "  "
        idx = "[" + ", ".join(f"i{i}" for i in range(len(g["vars"]))) + "]" if g["vars"] else "([] : List Nat)"
        def pt(c):
            return "st inp st2 inp2" if c.runs == 2 else "st inp"

        def in_scope(c):
            if c.runs == 2:
                return f"decide (({c.op}).scope st inp ∧ ({c.op}).scope st2 inp2 ∧ {rel_of(voc, c)} st inp st2 inp2)"
            return f"decide (({c.op}).scope st inp)"
        scope = " || ".join(dict.fromkeys(in_scope(c) for c in rd.claims))
        ats = ", ".join(f"decide ({c.at} {pt(c)})" for c in rd.claims)
        cks = ", ".join(f"{c.check} {pt(c)}" for c in rd.claims)
        seen = ", ".join(f"rseen (Frames.Op.observe ({c.op}) st inp)" for c in rd.claims)
        # what the Rust side evaluates too, point by point (clausal/trees.py): per unit its scope, then per claim the
        # relation between the two calls (a two-run claim) and the claim itself
        cmp_ = []
        for op, claim_ix in unit_ops(rd):
            cmp_.append(f"decide (({op}).scope st inp)")
            for j in claim_ix:
                c = rd.claims[j]
                if c.runs == 2:
                    cmp_.append(f"decide ({rel_of(voc, c)} st inp st2 inp2)")
                cmp_.append(f"decide ({c.at} {pt(c)})")
        fn += [f"{ind}let st : {rd.state_type} := {g['st']}",
               f"{ind}let inp : {rd.input_type} := {g['inp']}"]
        if two:
            fn += [f"{ind}let st2 : {rd.state_type} := {g['st2']}",
                   f"{ind}let inp2 : {rd.input_type} := {g['inp2']}"]
        fn += [f"{ind}bits := bits ++ rbits [{', '.join(cmp_)}]",
               f"{ind}tried := tried + 1",
               f"{ind}if {scope} then",
               f"{ind}  inScope := inScope + 1",
               f"{ind}  if sat.isNone then sat := some (toString {idx})",
               f"{ind}  let ats : List Bool := [{ats}]",
               f"{ind}  let cks : List Bool := [{cks}]",
               f"{ind}  evals := evals + ats.length",
               f"{ind}  agree := agree + ((ats.zip cks).filter fun p => p.1 == p.2).length",
               f"{ind}  if ats != cks && diff.isNone then diff := some s!\"{{{idx}}}/{{rbits ats}}/{{rbits cks}}\"",
               f"{ind}  if ats.any (· == false) && bad.isNone then bad := some s!\"{{{idx}}}/{{rbits ats}}\"",
               f"{ind}  let seen : List (Nat × Nat) := [{seen}]",
               f"{ind}  nFalse := radd nFalse (ats.map fun b => if b then 0 else 1)",
               f"{ind}  nSilent := radd nSilent (seen.map (·.1))",
               f"{ind}  nAbout := radd nAbout (seen.map (·.2))",
               f"  IO.println s!\"RSEARCH\\t{rd.id}\\t{{tried}}\\t{{inScope}}\\t{{evals}}\\t{{agree}}\\t{{diff.getD \"-\"}}\\t{{bad.getD \"-\"}}\\t{{sat.getD \"-\"}}\\t{{rnums nFalse}}/{{rnums nSilent}}/{{rnums nAbout}}\"",
              f"  IO.println s!\"RBITS\\t{rd.id}\\t{{bits}}\""]
        side[rd.id]["width"] = len(cmp_)
        # what each character of a grid point's bits is: ("scope", unit) / ("rel", claim) / ("at", claim)
        lay = []
        for u, (op, claim_ix) in enumerate(unit_ops(rd)):
            lay.append(["scope", u])
            for j in claim_ix:
                if rd.claims[j].runs == 2:
                    lay.append(["rel", j])
                lay.append(["at", j])
        side[rd.id]["layout"] = lay
        out.append("\n".join(fn) + "\n")
        main.append(f"  rs{k}")
    # Examples rows of the NEW sentences, on the model, through the reading itself
    rmain = []
    for rd, sc in rows:
        side.setdefault(rd.id, {})["rows"] = []
        for n, line, cells in rows_of(sc):
            p = row_point(voc, rd, sc, cells)
            side[rd.id]["rows"].append({"n": n, "line": line, "cells": cells, "evaluated": p is not None})
            if p is None:
                continue
            op = rd.op
            for name, term in p["outer"].items():
                pass
            lets = "".join(f"  let {name} : {typ} := {p['outer'][name]}\n" for name, typ in rd.outer)
            rmain.append(f"  -- {rd.id} row {n}\n" + lets +
                         f"  let st : {rd.state_type} := {p['st']}\n  let inp : {rd.input_type} := {p['inp']}\n"
                         f"  IO.println s!\"RROW\\t{rd.id}\\t{n}\\t{{rbits [decide (({op}).scope st inp)]}}\\t"
                         f"{{rbits [{', '.join(f'decide ({c.at} st inp)' for c in rd.claims)}]}}\"")
    out.append("#eval show IO Unit from do\n" + ("\n".join(main) if main else "  pure ()") + "\n")
    for chunk in rmain:
        out.append("#eval show IO Unit from do\n" + chunk + "\n")
    return "\n".join(out), side


def parse(log: str, side: dict) -> dict:
    """out/rsearch.log -> id -> {tried, in_scope, evals, agree, diff, bad: {values, bits}, sat}."""
    res = {}

    def values(id_, text):
        idx = [int(x) for x in re.findall(r"\d+", text.split("/")[0])]
        return {n: vals[i] for (n, vals), i in zip(side[id_]["vars"], idx)}

    for line in log.splitlines():
        p = line.split("\t")
        if p[0] != "RSEARCH":
            continue
        _, id_, tried, ins, evals, agree, diff, bad, sat = p[:9]
        r = {"tried": int(tried), "in_scope": int(ins), "evals": int(evals), "agree": int(agree), "diff": None, "bad": None,
             "sat": None, "frames": side[id_]["frames"], "claims": side[id_].get("claims", [])}
        if len(p) > 9:      # per frame of the reading: points where the definition is false / the call is silent / the frame is about the call
            r["false"], r["silent"], r["about"] = ([int(x) for x in part.split(",") if x] for part in p[9].split("/"))
        if diff != "-":
            _, a, c = diff.split("/")
            r["diff"] = {"values": values(id_, diff), "definition": a, "checker": c}
        if bad != "-":
            r["bad"] = {"values": values(id_, bad), "bits": bad.split("/")[1], "index": [int(x) for x in re.findall(r"\d+", bad.split("/")[0])]}
        if sat != "-":
            r["sat"] = {"values": values(id_, sat), "index": [int(x) for x in re.findall(r"\d+", sat)]}
        res[id_] = r
        res[id_]["two_run"] = bool(side[id_].get("st2"))
        res[id_]["layout"] = side[id_].get("layout")
        res[id_]["sizes"] = [len(vals) for _n, vals in side[id_]["vars"]]
    for line in log.splitlines():
        p = line.split("\t")
        if p[0] == "RBITS" and p[1] in res:
            res[p[1]]["bits"] = p[2] if len(p) > 2 else ""
            res[p[1]]["width"] = side[p[1]].get("width")
        elif p[0] == "RROW" and p[1] in side:
            row = next(r for r in side[p[1]]["rows"] if r["n"] == int(p[2]))
            row["scope"], row["claims"] = p[3], p[4]
    for id_, s in side.items():
        if "skipped" in s:
            res[id_] = {"skipped": s["skipped"]}
        if "rows" in s and id_ in res:
            res[id_]["rows"] = s["rows"]
    return res


def covers_no_call(r: dict) -> list:
    """The clauses of a searched reading that are narrowed to accepted or to rejected calls and were ABOUT no call
    on the grid: [(echo of the clause, which calls it asked for)]. Such a clause holds there because it says nothing."""
    if not r or "about" not in r or not r.get("in_scope"):
        return []
    return [(c["echo"], c.get("calls") or ("rejected" if "rejected" in c["mods"] else "accepted"))     # the claim's Calls value
            for c, n in zip(r.get("claims", []), r["about"]) if c["mods"] and n == 0]


def point_terms(side_entry: dict, index: list) -> dict:
    """Lean terms of the state and the input at one grid point (for a kernel-checked refutation)."""
    out = {k: side_entry.get(k) for k in ("st", "inp", "st2", "inp2")}
    for (n, _), i in zip(side_entry["vars"], index):
        t = side_entry["terms"][n][i]
        for k in out:
            if out[k] is not None:
                out[k] = re.sub(rf"\b{re.escape(n)}\b(?!')", lambda _m: t, out[k])
    out["outer"] = {n: side_entry["terms"][n][i] for (n, _), i in zip(side_entry["vars"], index)}
    return out


def dump_side(side: dict) -> str:
    return json.dumps(side, indent=1, ensure_ascii=False)
