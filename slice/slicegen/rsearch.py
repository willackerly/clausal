"""slicegen rsearch: every compiled reading evaluated on generated inputs, TWO ways.

lean/Run/ReadingSearch.lean (generated; run once per pipeline run by the interpreter) walks a grid of
outline parameters, states and inputs for every reading (scenario or Rule) and, at each point and for each
frame the reading is made of, evaluates

    decide (F.at op holes st inp)      the DEFINITION of the frame at that call (lean/Frames/Frames.lean)
    Frames.Check.F op holes st inp     the independent EXECUTABLE reading          (lean/Frames/Check.lean)

It reports, per reading: how many points were tried, how many are in scope, on how many (point, frame)
evaluations the two readings agree, the first point where they differ, and the first point where the
definition says the reading is false (a counterexample to the reading itself, found without the old
glossary). This is the FRET practice of giving each template two semantics and testing one against the
other; here it is done on the concrete operations of the project, and it doubles as the counterexample
search for `Rule:` statements.
"""
from __future__ import annotations

import json
import re

from . import emit
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


def grid(voc, rd: Reading, b: Bound | None) -> dict:
    """{vars: [(name, lean type, [literal text], [lean term])], st: Lean term, inp: Lean term}."""
    vars_ = []
    gl = voc.gloss

    def var(name, typ):
        vals = sample(voc, typ, b)
        vars_.append((name, voc.pts[typ]["lean"], vals, [lit(voc, typ, v) for v in vals]))
        return name

    def actor(name, atype):
        bd = gl.actors[atype]["build"]
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
        parts = [actor(fresh(a.split()[-1].lower() + "_state"), t) for a, (_, t) in zip(info["st_actors"], ops[0]["state"])]
        st = parts[0] if len(parts) == 1 else "(" + ", ".join(parts) + ")"
        for a in info["bystanders"]:
            st = f"({st}, {actor(fresh(a.split()[-1].lower() + '_state'), ctx.actor_type[a])})"
        ins = []
        for k, (o, bind) in enumerate(zip(ops, info["binds"])):
            if not o["input"]:
                ins.append("()")
                continue
            leaf = bind[o["input"][0][0]]
            ins.append(var(fresh(leaf.param), leaf.type) if leaf.how == "param" else ctx.value(leaf))
        return {"vars": vars_, "st": st, "inp": nest(ins)}
    ops = rd.info["clauses"][0]["ops"]
    # named "the_<role>": a bare role name such as `ledger` would shadow the Lean namespace of the model
    parts = [actor(fresh("the_" + r), t) for r, t in ops[0]["state"]]
    st = parts[0] if len(parts) == 1 else "(" + ", ".join(parts) + ")"
    ins = [var(fresh("the_" + o["input"][0][0]), o["input"][0][1]) if o["input"] else "()" for o in ops]
    return {"vars": vars_, "st": st, "inp": nest(ins)}


def same_grid(rd: Reading) -> bool:
    """A Rule whose clauses are about different operations has no single grid; it is searched clause by clause
    only if every clause shares the state and input types of the first."""
    if rd.kind != "rule":
        return True
    cl = rd.info["clauses"]
    return all(c["state_type"] == cl[0]["state_type"] and c["input_type"] == cl[0]["input_type"] for c in cl)


def search_file(voc, items) -> tuple:
    """items: [(Reading, Bound | None)]. Returns (Lean text, sidecar dict id -> grid description)."""
    out = [HEADER + "-- Run once per pipeline run with `lake env lean Run/ReadingSearch.lean` (interpreter).\n"
           "-- Every compiled reading on a grid of generated inputs, evaluated two ways: through the DEFINITION of\n"
           "-- each frame (decide (F.at ...)) and through its independent executable reading (Frames.Check.F ...).\n"
           "import Wallet.Readings\nimport Wallet.Vocab\nimport Ledger.Vocab\nopen Aeneas Aeneas.Std Result\n"
           "set_option linter.unusedVariables false\n\n"
           "def rbits (l : List Bool) : String := String.ofList (l.map fun b => if b then '1' else '0')\n"]
    side, main = {}, []
    for k, (rd, b) in enumerate(items):
        if not same_grid(rd):
            side[rd.id] = {"skipped": "its clauses are about operations with different states or inputs"}
            continue
        g = grid(voc, rd, b)
        side[rd.id] = {"vars": [(n, vals) for n, _, vals, _ in g["vars"]], "frames": [c.frame["id"] for c in rd.claims],
                       "st": g["st"], "inp": g["inp"], "terms": {n: terms for n, _, _, terms in g["vars"]}}
        fn = [f"def rs{k} : IO Unit := do",
              "  let mut tried := 0", "  let mut inScope := 0", "  let mut evals := 0", "  let mut agree := 0",
              "  let mut diff : Option String := none", "  let mut bad : Option String := none",
              "  let mut sat : Option String := none"]
        ind = "  "
        for i, (n, typ, _, terms) in enumerate(g["vars"]):
            fn.append(f"{ind}for ({n}, i{i}) in ([{', '.join(terms)}] : List ({typ})).zipIdx do")
            ind += "  "
        idx = "[" + ", ".join(f"i{i}" for i in range(len(g["vars"]))) + "]" if g["vars"] else "([] : List Nat)"
        scope = " || ".join(f"decide (({op}).scope st inp)" for op in dict.fromkeys(c.op for c in rd.claims))
        ats = ", ".join(f"decide ({c.at} st inp)" for c in rd.claims)
        cks = ", ".join(f"{c.check} st inp" for c in rd.claims)
        fn += [f"{ind}let st : {rd.state_type} := {g['st']}",
               f"{ind}let inp : {rd.input_type} := {g['inp']}",
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
               f"  IO.println s!\"RSEARCH\\t{rd.id}\\t{{tried}}\\t{{inScope}}\\t{{evals}}\\t{{agree}}\\t{{diff.getD \"-\"}}\\t{{bad.getD \"-\"}}\\t{{sat.getD \"-\"}}\""]
        out.append("\n".join(fn) + "\n")
        main.append(f"  rs{k}")
    out.append("#eval show IO Unit from do\n" + ("\n".join(main) if main else "  pure ()") + "\n")
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
        _, id_, tried, ins, evals, agree, diff, bad, sat = p
        r = {"tried": int(tried), "in_scope": int(ins), "evals": int(evals), "agree": int(agree), "diff": None, "bad": None,
             "sat": None, "frames": side[id_]["frames"]}
        if diff != "-":
            _, a, c = diff.split("/")
            r["diff"] = {"values": values(id_, diff), "definition": a, "checker": c}
        if bad != "-":
            r["bad"] = {"values": values(id_, bad), "bits": bad.split("/")[1], "index": [int(x) for x in re.findall(r"\d+", bad.split("/")[0])]}
        if sat != "-":
            r["sat"] = {"values": values(id_, sat), "index": [int(x) for x in re.findall(r"\d+", sat)]}
        res[id_] = r
    for id_, s in side.items():
        if "skipped" in s:
            res[id_] = {"skipped": s["skipped"]}
    return res


def point_terms(side_entry: dict, index: list) -> dict:
    """Lean terms of the state and the input at one grid point (for a kernel-checked refutation)."""
    st, inp = side_entry["st"], side_entry["inp"]
    for (n, _), i in zip(side_entry["vars"], index):
        t = side_entry["terms"][n][i]
        st = re.sub(rf"\b{re.escape(n)}\b", lambda _m: t, st)
        inp = re.sub(rf"\b{re.escape(n)}\b", lambda _m: t, inp)
    outer = {n: side_entry["terms"][n][i] for (n, _), i in zip(side_entry["vars"], index)}
    return {"st": st, "inp": inp, "outer": outer}


def dump_side(side: dict) -> str:
    return json.dumps(side, indent=1, ensure_ascii=False)
