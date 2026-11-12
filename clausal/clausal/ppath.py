"""clausal ppath: verdicts for NEW SENTENCES, and what the compiled Rust says about every compiled reading.

A new sentence is a scenario (or a Rule line) that the composable Clausebook reads and the old whole-phrase glossary
does not. Nothing about it goes through the old glossary:

  statement    the compiled reading (lean/Wallet/Readings.lean) and its flat proof obligation, generated from the
               pieces (lean/Wallet/Obligations.lean), tied by a kernel-checked equivalence
  PROVED-*     a supplied proof of the obligation, carried to the reading through that equivalence, and the scope shown
               to be non-empty in the kernel
  REFUTED      the reading search found an input at which the reading is false and `¬ reading` is kernel-checked there
  TESTED-ONLY  neither: the Examples rows pass on the compiled Rust and on the model, no counterexample on the grid
  rows         cucumber-rs through the generic step (compiled Rust); the reading itself at the row (Lean model)

For EVERY compiled reading, old or new, `grid_compare` sets the Lean side's evaluation of the reading on its grid
(the Lean pieces on the Aeneas model) against the Rust side's (the Rust reading of each piece on the compiled crate).
"""
from __future__ import annotations

import json

from . import vreport
from .pipeline import OUT, ROOT, proof_module, proof_path
from .vocab import Reading


def load_rust_bits():
    """reading id -> the bit string tests/grid.rs wrote; None if the Rust side did not run."""
    p = OUT / "rust_bits.tsv"
    if not p.exists():
        return None
    out = {}
    for line in p.read_text().splitlines():
        if "\t" in line:
            k, v = line.split("\t", 1)
            out[k] = v
    return out


def point_no(index: list, sizes: list) -> int:
    n = 0
    for i, s in zip(index, sizes):
        n = n * s + i
    return n


def compare(id_: str, rs: dict, rust) -> dict:
    if rust is None or not rs or "bits" not in rs:
        return {"ran": False}
    lean, r = rs["bits"], rust.get(id_)
    w = rs.get("width") or 1
    out = {"ran": True, "evals": len(lean), "points": len(lean) // w if w else 0, "agree": 0, "error": None, "first": None}
    if r is None:
        out["error"] = "the Rust side did not evaluate this reading"
    elif r.startswith("ERROR"):
        out["error"] = "the Rust side could not evaluate this reading: " + r[5:].strip()
    elif len(r) != len(lean):
        out["error"] = f"the Rust side evaluated {len(r)} points, the Lean side {len(lean)}"
    else:
        diff = [i for i in range(len(lean)) if lean[i] != r[i]]
        out["agree"] = len(lean) - len(diff)
        if diff:
            i = diff[0]
            what = (rs.get("layout") or [])[i % w] if rs.get("layout") else ["?", 0]
            out["first"] = {"point": i // w, "what": what, "lean": lean[i], "rust": r[i]}
    return out


def found_by(bad: dict) -> str:
    """Who found a counterexample: the reading search on the grid, or a generated harness (plan node E1)."""
    return {"property test": "the generated property test", "bounded check": "the generated bounded check (Kani)"}.get(
        bad.get("source"), "the reading search")


def rust_at(id_: str, rs: dict, rust, index: list, claim: int):
    """The Rust side's verdict on claim `claim` at the grid point `index`: True / False / None (not run)."""
    if index is None:
        # not a grid point: the input came from the generated property test or bounded check, which found it (or
        # replayed it) on the compiled Rust; it is here only because it fails on the model too (clausal/evidence.py)
        return False
    if rust is None or not rs or "bits" not in rs or id_ not in rust or not rs.get("layout"):
        return None
    w, lay = rs["width"], rs["layout"]
    off = next((k for k, x in enumerate(lay) if x == ["at", claim]), None)
    pos = point_no(index, rs["sizes"]) * w + (off or 0)
    r = rust[id_]
    if off is None or r.startswith("ERROR") or pos >= len(r):
        return None
    return r[pos] == "1"


def compare_line(cmp_: dict) -> str:
    if not cmp_.get("ran"):
        return "not compared     the reading was not evaluated on the compiled Rust in this run (cucumber-rs / the grid test did not run)"
    if cmp_["error"]:
        return f"NOT COMPARED     {cmp_['error']}"
    return (f"tested           the reading on the COMPILED RUST at the same {cmp_['points']} generated inputs, through the Rust reading of each piece "
            f"(wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on {cmp_['agree']} of {cmp_['evals']} evaluations"
            + ("" if cmp_["agree"] == cmp_["evals"] else "  <-- THEY DISAGREE"))


def apply_compare(obj, id_: str, rs: dict, ctx) -> dict:
    """Attach the comparison to a verdict object (scenario or Rule): flags and fatal on a disagreement."""
    cmp_ = compare(id_, rs, ctx.get("rust_bits"))
    obj.rust_grid = cmp_
    if cmp_.get("ran") and (cmp_["error"] or cmp_["agree"] != cmp_["evals"]):
        obj.flags.append("PIECE READINGS DISAGREE")
        obj.fatal.append("PIECE READINGS DISAGREE: " + (cmp_["error"] or
                         f"the Lean side and the compiled Rust differ at grid point {cmp_['first']['point']} on {cmp_['first']['what']} "
                         f"(Lean {cmp_['first']['lean']}, Rust {cmp_['first']['rust']})"))
    return cmp_


def piece_comparison(st, ctx) -> dict:
    """piece id -> {readings, points, bad}: through how many compiled readings, at how many generated inputs, the Rust
    reading of the piece was set against its Lean definition in this run."""
    rust, rs_all = ctx.get("rust_bits"), ctx["rs"]
    out = {}
    if rust is None:
        return out
    for rd, _ in st.compiled:
        rs = rs_all.get(rd.id, {})
        c = compare(rd.id, rs, rust)
        if not c.get("ran") or c["error"]:
            continue
        for i in rd.used:
            q = out.setdefault(i, {"readings": 0, "points": 0, "bad": False})
            q["readings"] += 1
            q["points"] += c["points"]
            q["bad"] = q["bad"] or c["agree"] != c["evals"]
    return out


# --------------------------------------------------------------------------- a NEW scenario

def obligation_text(id_: str) -> str:
    p = ROOT / "lean" / "Wallet" / "Obligations.lean"
    if not p.exists():
        return ""
    text = p.read_text()
    i = text.find(f"def {id_}.obligation ")
    if i < 0:
        return ""
    j = text.find("\n\n", i)
    return text[i:j if j > 0 else len(text)]


def new_scenario_verdict(v, st, ctx) -> str:
    """Fills `v` (report.Verdict) for a scenario with no flat statement in the old glossary; returns its status."""
    sc, rd, L = v.sc, v.reading, v.lines
    links, meta, cuc = ctx["links"], ctx["links_meta"], ctx["cuc"]
    rs = ctx["rs"].get(rd.id, {})
    base = sc.feature.path.rsplit("/", 1)[-1]
    v.new = True
    v.pieces = rd.used
    v.pieces_unreviewed = [i for i in rd.used if i not in ctx["piece_reviewed"]]
    if v.pieces_unreviewed:
        v.flags.append(f"UNREVIEWED CLAUSEBOOK ({len(v.pieces_unreviewed)} of {len(rd.used)})")
    off = vreport.outside_allowlist(links, st.voc, rd)
    if off:
        v.flags.append("GENERATOR-CHECK-FAILED")
        v.fatal.append("GENERATOR-CHECK-FAILED: the reading mentions " + ", ".join(off) + ", which none of its Clausebook pieces accounts for")
    if rs.get("diff"):
        v.flags.append("FRAME READINGS DISAGREE")
        v.fatal.append("FRAME READINGS DISAGREE: the definition and the executable reading of a frame differ at " + json.dumps(rs["diff"]["values"]))
    # rows: the reading at the row on the Lean model; cucumber-rs through the generic step on the compiled Rust
    for row in rs.get("rows", []):
        if not row.get("evaluated") or "claims" not in row:
            model = None
        else:
            model = "givenFalse" if row["scope"] != "1" else "pass" if set(row["claims"]) <= {"1"} else "fail"
        rust = cuc.get((base, row["line"])) if cuc is not None else None
        v.rows.append({"n": row["n"], "line": row["line"], "cells": row["cells"], "model": model, "rust": rust,
                       "agree": rust is None or model is None or rust == model})
    if any(not x["agree"] for x in v.rows):
        v.flags.append("MODEL/GLUE MISMATCH")
        v.fatal.append("MODEL/GLUE MISMATCH")
    if any(x["model"] == "givenFalse" for x in v.rows):
        v.flags.append("ROW OUTSIDE GIVENS")
    cmp_ = apply_compare(v, rd.id, rs, ctx)
    iff, sat, holds = rd.id + ".reading_iff_obligation", rd.id + ".reading_sat", rd.id + ".reading_holds"
    signed = len(rd.used) - len(v.pieces_unreviewed)
    meaning = ((f"human-asserted   {signed} of {len(rd.used)} Clausebook pieces signed off" if signed else
                f"NOT ASSERTED     0 of {len(rd.used)} Clausebook pieces signed off by anyone")
               + ("" if not v.pieces_unreviewed else f" - UNREVIEWED: {', '.join(v.pieces_unreviewed)}"))
    fns = [o["model"] for o in rd.info["ops"]]
    tool = st.tool
    about = f"about            the Lean model {', then '.join(fns)}, not the Rust source"
    trust = [f"tool-trusted     model = Rust: {tool['rustc']}, charon {tool['charon']}, aeneas {tool['aeneas']}",
             f"tool-trusted     reading compiled by {tool['generator']} from {len(rd.used)} Clausebook pieces; echoed above for comparison with the scenario",
             "new sentence     no entry of the old whole-phrase glossary is involved: no flat statement of that kind, no hand-written step, "
             "no hand-written Rust predicate"]
    two = ("" if not rs or "skipped" in rs else
           f"tested           the reading on {rs['tried']} generated inputs ({rs['in_scope']} in scope) on the Lean model: "
           + ("no counterexample" if not rs.get("bad") else
              f"no counterexample on the grid (the counterexample came from the generated {rs['bad']['source']})" if rs["bad"].get("source") else "counterexample found")
           + f"; the definition of each frame and its executable reading agree on {rs['agree']} of {rs['evals']} evaluations")
    nr = len(v.rows)
    if nr:
        mp = sum(x["model"] == "pass" for x in v.rows)
        if cuc is None:
            tested = f"tested           {mp} of {nr} rows pass on the Lean model; cucumber-rs did not run"
        else:
            rp = sum(x["rust"] == "pass" for x in v.rows)
            tested = (f"tested           {rp} of {nr} rows pass on compiled Rust (cucumber-rs, generic step: the composition tree evaluated by the "
                      f"per-piece Rust readings); {mp} of {nr} pass on the Lean model; "
                      + ("they agree" if all(x["agree"] for x in v.rows) else "THEY DISAGREE"))
    else:
        tested = "tested           no rows could be evaluated (an actor has no Given that fixes it)"
    tail = [about] + trust + [meaning] + [x for x in (tested, two, compare_line(cmp_)) if x]
    human = ["human-asserted"] if signed else []
    if not vreport.lclean(links, iff):
        L.append(f"NOT LINKED       the flat proof obligation is NOT proved equivalent to the reading ({vreport.lwhy(links, iff)}); "
                 "nothing about the obligation counts for the reading")
    if rs.get("bad"):
        bad = rs["bad"]
        j = bad["bits"].index("0")
        kernel = vreport.lclean(links, rd.id + ".refuted")
        on_rust = rust_at(rd.id, rs, ctx.get("rust_bits"), bad["index"], j)
        v.replay = None if on_rust is None else ("reproduced" if on_rust is False else "NOT reproduced (the compiled Rust satisfies the claim there)")
        v.counterexample = {"values": bad["values"], "failed_thens": [rd.claims[j].echo], "held_thens": [], "kernel_checked": kernel,
                            "replayed_on_rust": v.replay, "returned": None, "check": None}
        if kernel:
            L.append(f"kernel-checked   theorem {rd.id}.refuted : ¬ {rd.name}; axioms {', '.join(vreport.lthm(links, rd.id + '.refuted')['axioms'])}")
        else:
            L.append(f"tested           counterexample found by {found_by(bad)}; kernel confirmation "
                     + ("not generated" if not vreport.lthm(links, rd.id + ".refuted").get("exists") else "attempted and FAILED"))
        if bad.get("source"):
            L.append(f"source           the input was found on the compiled Rust by {found_by(bad)}, then evaluated on the Lean model, where the reading fails too")
            v.counterexample["source"] = bad["source"]
        L.append("counterexample   " + ", ".join(f"{k.replace('_state', '')} = {val}" for k, val in bad["values"].items()))
        L.append("                 at this input the reading does not hold: NOT \"" + rd.claims[j].echo + "\"")
        if v.replay:
            L.append(f"tested           the same input on the compiled Rust (per-piece Rust readings): {v.replay}")
        L += tail
        if v.rows and all(x["model"] == "pass" for x in v.rows):
            L.append("note             every Examples row passes; the examples alone would not have caught this")
        v.rests_on = (["kernel-checked"] if kernel else []) + ["tool-trusted", "tested"] + human
        return "REFUTED" if kernel else "COUNTEREXAMPLE"
    if rs and "skipped" not in rs and rs.get("in_scope") == 0:
        L.append(f"tested           no input satisfying the Givens among the {rs['tried']} generated inputs: the scenario may be true of nothing")
        L += tail
        v.rests_on = ["tested"]
        return "VACUOUS-SUSPECTED"
    proof_ok = vreport.lclean(links, rd.id) and vreport.lthm(links, rd.id).get("module") == proof_module(sc.id)
    if proof_ok and vreport.lclean(links, iff) and vreport.lclean(links, holds) and vreport.lclean(links, sat):
        L.append(f"kernel-checked   theorem {holds} : {rd.name}  (THE READING ITSELF, as one theorem: the supplied proof of its flat obligation "
                 f"carried through the equivalence; type checked by the audit); axioms {', '.join(vreport.lthm(links, holds)['axioms'])}")
        L.append(f"kernel-checked   theorem {rd.id} : {rd.id}.obligation  (hand-written, {proof_path(sc.id).relative_to(ROOT)}; type checked by the audit)")
        L.append(f"kernel-checked   theorem {iff} : {rd.name} ↔ {rd.id}.obligation  (generated script; the audit checked its type and that its "
                 f"proof uses no proof of either side); axioms {', '.join(vreport.lthm(links, iff)['axioms'])}; reading non-vacuous ({sat})")
        L.append("scope            " + ("every input satisfying the Givens" if sc.outline else "THIS input only (plain Scenario: the values are literals)"))
        L += tail
        v.rests_on = ["kernel-checked", "tool-trusted"] + human + (["tested"] if nr else [])
        return "PROVED-FOR-ALL" if sc.outline else "PROVED-INSTANCE"
    t = vreport.lthm(links, rd.id)
    if not proof_path(sc.id).exists():
        why = f"no proof of the obligation has been supplied ({proof_path(sc.id).relative_to(ROOT)} does not exist)"
    elif proof_module(sc.id) in ctx["proofs"].get("failed", []):
        why = f"the proof does not compile ({ctx['proofs'].get('errors', {}).get(proof_module(sc.id), 'see out/proofs.log')})"
    elif "sorryAx" in t.get("axioms", []):
        why = f"proof incomplete (sorry): {proof_path(sc.id).relative_to(ROOT)} is still the generated stub, or part of it is"
    elif t.get("exists") and not t.get("type_ok"):
        why = f"a theorem named {rd.id} exists, but its type is NOT `{rd.id}.obligation`"
    elif not vreport.lclean(links, iff):
        why = "the obligation is proved, but it is not tied to the reading (see NOT LINKED above)"
    elif not vreport.lclean(links, sat):
        why = f"the obligation is proved, but the reading's own non-vacuity ({sat}) is not shown ({vreport.lwhy(links, sat)})"
    else:
        why = f"the theorem that carries the proof to the reading ({holds}) is not there ({vreport.lwhy(links, holds)})"
    L.append(f"not proved       {why}")
    L.append(f"obligation       {rd.id}.obligation (lean/Wallet/Obligations.lean), generated from the pieces; prove it in "
             f"{proof_path(sc.id).relative_to(ROOT)}")
    L += tail
    v.rests_on = ["tested", "tool-trusted"] + human
    return "TESTED-ONLY"


# --------------------------------------------------------------------------- the report section

def end_to_end_section(st, ctx, verdicts, rule_verdicts) -> list:
    """`## New sentences, end to end`: every scenario and Rule line that has no entry in the old glossary, with what it got."""
    from .vocab import Reading
    links, meta = ctx["links"], ctx["links_meta"]
    new_sc = [v for v in verdicts if v.new]
    old_rules = {r.id for f in st.features for r in f.rules
                 if any(not vv.new and isinstance(vv.reading, Reading) for vv in verdicts if vv.sc.rule is r)}
    new_rules = [rv for rv in rule_verdicts if isinstance(rv.rd, Reading) and rv.rule.id not in old_rules
                 and rv.rule.feature.path.endswith("ledger_rules.feature")]
    o = ["## New sentences, end to end", "",
         "A NEW sentence is a scenario or a `Rule:` line that the composable Clausebook reads and that has NO entry in the old "
         "whole-phrase glossary, no hand-written cucumber step and no hand-written Rust predicate. What each one gets, from the pieces alone:", "",
         "- **a reading** (the composition, type-checked by Lean) and its **echo**;",
         "- **a run on the compiled Rust**: Examples rows through the one generic cucumber step, and the reading itself at every point "
         "of its grid of generated inputs, both evaluated by the per-piece Rust readings;",
         "- **a flat proof obligation** generated from the `flat:` template of each frame (`lean/Wallet/Obligations.lean`), tied to the "
         "reading by a generated, kernel-checked equivalence, and a proof stub;",
         "- **a verdict**: PROVED-FOR-ALL when a proof of the obligation has been supplied (here: by an agent), TESTED-ONLY while the "
         "stub is `sorry`, REFUTED when the search finds an input at which the reading is false and the kernel confirms it there.", "",
         "| Sentence | Kind | Pieces | Verdict | How | Examples on Rust | Generated inputs: Rust = model | Obligation ↔ reading |", "|---|---|---|---|---|---|---|---|"]

    def gridcell(g):
        if not g.get("ran"):
            return "not run"
        if g.get("error"):
            return "**NOT COMPARED**"
        return f"{g['agree']} of {g['evals']} at {g['points']} inputs" + ("" if g["agree"] == g["evals"] else " **DISAGREE**")

    def iffcell(id_):
        n = id_ + ".reading_iff_obligation"
        return "kernel-checked" if vreport.lclean(links, n) else f"**NOT SHOWN** ({vreport.lwhy(links, n)})"
    for v in new_sc:
        rp = sum(x["rust"] == "pass" for x in v.rows)
        how = ("supplied proof of the obligation" if v.status.startswith("PROVED") else "kernel refutation at the counterexample" if v.status == "REFUTED"
               else "no proof supplied" if v.status == "TESTED-ONLY" else "-")
        o.append(f"| {vreport.md_escape(v.sc.name)} (`{v.sc.feature.path}:{v.sc.line}`) | scenario | {len(v.pieces)} | **{v.status}**"
                 + ("" if v.as_expected else " (NOT AS EXPECTED)") + f" | {how} | {rp} of {len(v.rows)} | {gridcell(v.rust_grid)} | {iffcell(v.reading.id)} |")
    for rv in new_rules:
        how = (rv.how or ("kernel refutation at the counterexample (" + (rv.proof or {}).get("theorems", ["?"])[0].rsplit(".", 1)[-1] + ")"
                          if rv.status == "REFUTED" else "no proof supplied (stub is `sorry`)" if rv.status == "TESTED-ONLY" else "-"))
        o.append(f"| {vreport.md_escape(rv.rule.name)} (`{rv.rule.feature.path}:{rv.rule.line}`) | Rule | {len(rv.pieces)} | **{rv.status}**"
                 + ("" if rv.as_expected else " (NOT AS EXPECTED)") + f" | {how} | - | {gridcell(rv.rust_grid)} | {iffcell(rv.rd.id)} |")
    n_ob = len(meta.get("oiffs", []))
    ok_ob = sum(1 for x in meta.get("oiffs", []) if vreport.lclean(links, x[0]))
    counts = {}
    for x in [v.status for v in new_sc] + [rv.status for rv in new_rules]:
        counts[x] = counts.get(x, 0) + 1
    o += ["", f"{len(new_sc)} new scenarios and {len(new_rules)} new Rule lines: " + ", ".join(f"{n} {k}" for k, n in counts.items()) + ". "
          f"A flat obligation is generated for every Rule line as well as for the new scenarios: {ok_ob} of {n_ob} are proved equivalent to "
          "their reading (kernel-checked; the audit checks the type of each and that its proof uses no proof of either side). "
          "The proofs of the obligations were written by an agent, from the hand-proved step lemmas of `lean/Ledger/Lemmas/`; one true rule "
          "is deliberately left with its generated stub to show the TESTED-ONLY state.", ""]
    for rv in new_rules[:0]:
        pass
    o += ["<details><summary>The flat proof obligation of each new sentence (<code>lean/Wallet/Obligations.lean</code>)</summary>", ""]
    for id_, title in [(v.reading.id, v.sc.name) for v in new_sc] + [(rv.rd.id, "Rule: " + rv.rule.name) for rv in new_rules]:
        t = obligation_text(id_)
        if t:
            o += [f"**{title}**", "", "```lean", t, "```", ""]
    o += ["</details>", ""]
    return o
