"""clausal rules: the per-Rule block of the report, computed from the refinement graph and NOTHING else.

    python3 -m clausal rules [graph.json]      print the blocks of a stored graph (default out/graph.json)

`blocks(graph)` takes the parsed JSON of out/graph.json. `clausal report` writes the graph to disk, reads the
file back and renders these blocks from what it read, so the block in out/report.md cannot say anything the
graph does not (docs/PLAN.md node X1a). Each block:

    Rule       the rule line and the text under it, as written (NOT compiled)
    Verdict    of the scenarios beneath it (the rule line has none of its own)
    Examples   rows passing on the compiled Rust and on the Lean model
    Suite      the adequacy note: which trivial implementations the rule's proved universal scenarios rule out
    Rests on   meaning / proof / translation / compilation, each with its kind of evidence
"""
from __future__ import annotations

import json
import re
import sys
import textwrap
from pathlib import Path

STD_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
PROVED = ("PROVED-FOR-ALL", "PROVED-INSTANCE")
FALSE = ("REFUTED", "COUNTEREXAMPLE")


ASSERTED = {"model": "model-asserted", "organisation": "organisation-asserted", "tool": "tested", "person": "human-asserted"}


def blocks(g: dict) -> list:
    nodes = {n["id"]: n for n in g["nodes"]}
    out_edges, in_edges = {}, {}
    for e in g["edges"]:
        out_edges.setdefault((e["from"], e["relation"]), []).append(e)
        in_edges.setdefault((e["to"], e["relation"]), []).append(e)
    verdicts = {}
    for v in g["verdicts"]:
        verdicts.setdefault(v["node"], []).append(v)
    runs = {r["id"]: r for r in g["runs"]}

    def scenario_info(sid):
        n = nodes[sid]
        v = next((x for x in verdicts.get(sid, [])), None)
        # two statements formalise a scenario: the reading compiled from the Clausebook (`.reading`) and the flat
        # statement the proofs are about (`.stmt`). Proofs, refutations and rows hang off the flat one.
        stmt = next((e["from"] for e in in_edges.get((sid, "formalises"), []) if e["from"].endswith(".stmt")), None)
        # a NEW sentence has no flat statement of the old glossary: its statement is the compiled reading itself
        new = stmt is None and bool(n.get("attrs", {}).get("reading", {}).get("compiled"))
        if new:
            stmt = next((e["from"] for e in in_edges.get((sid, "formalises"), []) if e["from"].endswith(".reading")), None)
        info = {"node": sid, "id": sid.split(":", 1)[1], "name": n.get("attrs", {}).get("name", sid),
                "scope": n.get("attrs", {}).get("scope"), "code": v["code"] if v else "NO-VERDICT",
                "expected": v.get("expected") if v else None, "as_expected": v.get("as_expected") if v else None,
                "flags": v["flags"] if v else [], "stmt": stmt, "rows": [], "phrases": [], "proof": None,
                "refutation": None, "vacuity": None, "fns": [], "reading": n.get("attrs", {}).get("reading") or {}, "new": new}
        for e in out_edges.get((sid, "composed_of"), []):
            pid = e["to"]
            b = next((x for x in out_edges.get((pid, "binds"), []) if x.get("attrs", {}).get("reading", "").startswith("Lean")), None)
            info["phrases"].append({"id": pid.split(":", 1)[1], "phrase": nodes[pid].get("attrs", {}).get("phrase", ""),
                                    "signed": bool(b and b.get("attrs", {}).get("signoff") == "valid"
                                                   and any(x["kind"] == "human-asserted" for x in b["evidence"])),
                                    "by": next((x["by"] for x in (b["evidence"] if b else []) if x["kind"] == "human-asserted"), None)})
        if stmt:
            for im in nodes[stmt]["implementations"]:
                k = next((x for x in im["realises"] if x["kind"] == "kernel-checked"), None)
                if k:
                    info["proof"] = {"theorem": k.get("artifact"), "axioms": k.get("axioms", []),
                                     "scope": k.get("scope", {}).get("quantifier"), "method": k.get("method")}
            for e in in_edges.get((stmt, "refutes"), []):
                how = e.get("attrs", {}).get("how")
                if nodes[e["from"]]["kind"] != "statement":
                    continue
                for im in nodes[e["from"]]["implementations"]:
                    k = next((x for x in im["realises"] if x["kind"] == "kernel-checked"), None)
                    if k:
                        info["refutation" if how == "falsity" else "vacuity"] = {"theorem": k.get("artifact"), "axioms": k.get("axioms", [])}
            for e in in_edges.get((stmt, "instance_of"), []):
                a = nodes[e["from"]].get("attrs", {})
                info["rows"].append({"model": a.get("model"), "rust": a.get("rust")})
            for e in out_edges.get((stmt, "uses"), []):
                if nodes[e["to"]]["kind"] != "function":
                    continue
                for t in out_edges.get((e["to"], "translates"), []):
                    tt = next((x for x in t["evidence"] if x["kind"] == "tool-trusted"), None)
                    info["fns"].append({"lean": e["to"].split(":", 2)[2], "rust": t["to"].split(":", 2)[2],
                                        "rust_file": nodes[t["to"]]["interface"].get("source", {}).get("file"),
                                        "run": tt.get("run") if tt else None})
        return info

    def assumption_info(aid, gid):
        t = nodes[f"assumption:{aid}"].get("attrs", {})
        conds = []
        for c in t.get("usage_conditions", []):
            if c.get("rule") is None:
                conds.append({"id": c["id"], "rule": None, "code": "CANNOT BE STATED", "text": c.get("unstated", "")})
            else:
                rn = f"group:rule:{c['rule']}"
                v_ = next(iter(verdicts.get(rn, [])), None)
                conds.append({"id": c["id"], "rule": c["rule"], "code": v_["code"] if v_ else "NO VERDICT IN THIS RUN", "this": rn == gid,
                              "text": nodes[rn]["interface"]["text"].splitlines()[0] if rn in nodes else "(no such Rule in the graph)"})
        # a vouch is a record of act vouched by a person or an organisation; a model's or a tool's record is listed apart
        recs = [x for x in t.get("attestations", []) if isinstance(x, dict)]
        vouch = next((x for x in recs if x.get("act") == "vouched" and x.get("kind") in ("person", "organisation")), None)
        others = sum(1 for m in g["nodes"] if m["id"] != gid and m["kind"] == "group"
                     and aid in ((m.get("attrs", {}).get("reading") or {}).get("assumptions") or []))
        return {"id": aid, "statement": t.get("statement", ""), "class": t.get("class"), "stand_in": bool(t.get("stand_in")),
                "attached": t.get("attached", []), "conditions": conds, "vouch": vouch, "records": [x for x in recs if x is not vouch],
                "not_covered": t.get("not_covered", []), "external_proof": t.get("external_proof"), "lean_axioms": t.get("lean_axioms", []),
                "review_by": t.get("review_by"), "others": others}

    def block(gid, kind):
        n = nodes[gid]
        a = n.get("attrs", {})
        scs = [scenario_info(e["to"]) for e in out_edges.get((gid, "contains"), []) if nodes[e["to"]]["kind"] == "claim"]
        if not scs and kind != "rule":
            return None
        lines = n["interface"]["text"].splitlines()
        src = n["interface"].get("source", {})
        b = {"node": gid, "kind": kind, "tags": a.get("tags", []),
             "title": lines[0] if kind == "rule" else f"(scenarios of `{lines[0]}` that are not under a Rule)",
             "description": lines[1:] if kind == "rule" else [],
             "source": f"{src.get('file')}:{src.get('line_start')}" if kind == "rule" else src.get("file"),
             "scenarios": scs, "suite": a.get("suite_lines", []), "suite_head": a.get("suite_headlines", a.get("suite_lines", [])[:1]),
             "suite_data": a.get("suite"), "reading": a.get("reading") or {}}
        # plan node W4: the entries of the assumption ledger the rule's words rest on, each with its usage conditions and THEIR
        # verdicts in this graph (read from the verdict of the condition's Rule node: the ledger node stores none)
        b["assumptions"] = [assumption_info(x, gid) for x in (b["reading"].get("assumptions") or []) if f"assumption:{x}" in nodes]
        # ... and the rule's own verdict record: its outcome (pass / review / fail) and the entries no person has reviewed
        own = next(iter(verdicts.get(gid, [])), None)
        b["own_verdict"] = {"outcome": own["outcome"], "unreviewed": len(own.get("unreviewed") or [])} if own else None
        # verdict
        univ = [s for s in scs if s["scope"] == "universal"]
        inst = [s for s in scs if s["scope"] != "universal"]
        counts = {}
        for s in scs:
            counts[s["code"]] = counts.get(s["code"], 0) + 1
        tally = ", ".join(f"{k} {c}" for c, k in counts.items())
        if not scs:
            head = ("no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)"
                    if (b["reading"] or {}).get("compiled") else
                    "NOTHING STATED: no scenario sits under this rule, so nothing was compiled, tested or proved for it")
        # the headline is about the scenarios: the rule line itself is not compiled, so it has no verdict of its own
        elif any(s["code"] in FALSE for s in scs):
            head = "A SCENARIO IS SHOWN FALSE"
        elif all(s["code"] in PROVED for s in scs):
            head = "SCENARIOS PROVED FOR ALL INPUTS" if univ else "SCENARIOS PROVED FOR THEIR LITERAL VALUES ONLY"
        elif any(s["code"] in PROVED for s in scs):
            head = "SOME SCENARIOS PROVED"
        else:
            head = "NO SCENARIO PROVED"
        parts = []
        if univ:
            parts.append(f"{sum(s['code'] == 'PROVED-FOR-ALL' for s in univ)} of {len(univ)} universal scenarios proved for all inputs")
        if inst:
            parts.append(f"{sum(s['code'] == 'PROVED-INSTANCE' for s in inst)} of {len(inst)} literal examples proved for their own values")
        exp = all(s["as_expected"] for s in scs)
        b["verdict"] = {"head": head, "detail": "; ".join(parts), "tally": tally, "as_expected": exp}
        # examples
        rows = [r for s in scs for r in s["rows"]]
        both = [r for r in rows if r["rust"] is not None and r["model"] is not None]
        b["examples"] = {"rows": len(rows), "model_pass": sum(r["model"] == "pass" for r in rows),
                         "rust_ran": bool(both) or not rows and "run:cucumber" in runs, "rust_pass": sum(r["rust"] == "pass" for r in both),
                         "both": len(both), "agree": sum(r["rust"] == r["model"] for r in both)}
        # rests on
        phrases = {}
        for s in scs:
            for p in s["phrases"]:
                phrases.setdefault(p["id"], p)
        # the Clausebook pieces the rule line and the scenario readings are composed of
        pieces = {}
        for src_ in [b["reading"]] + [s["reading"] for s in scs]:
            for p in src_.get("pieces", []):
                pieces.setdefault(p["id"], p)
        proofs = [s for s in scs if s["proof"]]
        refs = [s for s in scs if s["refutation"]]
        vacs = [s for s in scs if s["vacuity"]]
        ax = sorted({x for s in proofs for x in s["proof"]["axioms"]} | {x for s in refs for x in s["refutation"]["axioms"]}
                    | {x for s in vacs for x in s["vacuity"]["axioms"]},
                    key=lambda x: (STD_AXIOMS.index(x) if x in STD_AXIOMS else 99, x))
        fns = {}
        for s in scs:
            for f in s["fns"]:
                fns.setdefault(f["lean"], f)
        tr = runs.get("run:translate", {})
        cu = runs.get("run:cucumber")
        # the rule STATEMENT's own evidence (kept in the rule node): its proof or refutation, its model functions, the grid
        rp = b["reading"].get("proof") or None
        for name in b["reading"].get("model_fns") or []:
            for t in out_edges.get((f"fn:lean:{name}", "translates"), []):
                tt = next((x for x in t["evidence"] if x["kind"] == "tool-trusted"), None)
                fns.setdefault(name, {"lean": name, "rust": t["to"].split(":", 2)[2],
                                      "rust_file": nodes[t["to"]]["interface"].get("source", {}).get("file"), "run": tt.get("run") if tt else None})
        if rp:
            ax = sorted(set(ax) | set(rp.get("axioms", [])), key=lambda x: (STD_AXIOMS.index(x) if x in STD_AXIOMS else 99, x))
        b["grid"] = b["reading"].get("rust_grid") or {"ran": False}
        # plan node E1: what the generated property test and bounded check say, for the rule statement and per scenario
        b["ladder"] = {"rule": b["reading"].get("ladder"),
                       "scenarios": [{"name": s["name"], "id": s["id"], "ladder": s["reading"].get("ladder")} for s in scs]}
        b["rests"] = {
            "meaning": {"entries": list(phrases.values()), "signed": sum(p["signed"] for p in phrases.values()),
                        "by": sorted({p["by"] for p in phrases.values() if p["by"]}),
                        "pieces": list(pieces.values()), "pieces_signed": sum(bool(p["signed"]) for p in pieces.values()),
                        "linked": sum(1 for s in scs if s["reading"].get("linked") and not s["new"]),
                        "compiled": sum(1 for s in scs if s["reading"].get("compiled") and not s["new"]),
                        "new": sum(1 for s in scs if s["new"])},
            "proof": {"universal": [s["proof"]["theorem"] for s in proofs if s["proof"]["scope"] == "all"],
                      "instance": [s["proof"]["theorem"] for s in proofs if s["proof"]["scope"] != "all"],
                      "refutations": [s["refutation"]["theorem"] for s in refs],
                      "vacuity": [s["vacuity"]["theorem"] for s in vacs], "axioms": ax, "rule": rp,
                      "standard_only": set(ax) <= set(STD_AXIOMS),
                      "none": [s["id"] for s in scs if not s["proof"] and not s["refutation"] and not s["vacuity"]]},
            "translation": {"fns": list(fns.values()), "tool": tr.get("tool"), "toolchain": tr.get("toolchain", {}),
                            "rows": len(both), "agree": b["examples"]["agree"], "rust_ran": cu is not None},
            "compilation": {"rustc": (cu or {}).get("toolchain", {}).get("rustc"), "ran": cu is not None},
        }
        return b

    out = []
    for n in g["nodes"]:
        if n["kind"] != "group":
            continue
        level = n.get("attrs", {}).get("level")
        if level in ("feature", "rule"):
            b = block(n["id"], "rule" if level == "rule" else "loose")
            if b:
                out.append(b)
    return out


def _wrap(label: str, text: str, width: int = 100) -> list:
    """`label` in a 13-wide column, text wrapped beside it."""
    lines = textwrap.wrap(text, width, break_on_hyphens=False) or [""]
    return [f"    {label:<13}{lines[0]}"] + [f"    {'':<13}{l}" for l in lines[1:]]


def evidence_lines(b: dict) -> list:
    """THE EVIDENCE LADDER of a rule (plan node E1), weakest first: example rows, generated property test, generated
    bounded check, proof. Each rung says what it found and what it rests on; the last line names the strongest held.
    Nothing here is called proved without a kernel-checked theorem."""
    rd, ex, r = b["reading"], b["examples"], b["rests"]
    lad = b.get("ladder") or {}
    rl = lad.get("rule")
    scl = [x for x in lad.get("scenarios", []) if x.get("ladder")]
    compiled = b["kind"] == "rule" and rd.get("compiled")
    about = "the rule statement" if compiled else "the scenarios"
    o = ["", f"  Evidence  for {about}, weakest first; each rung with what it rests on"]

    def rung(label, text, rests):
        w = textwrap.wrap(text, 96, break_on_hyphens=False) or [""]
        out = [f"    {label:<17}{w[0]}"] + [f"    {'':<17}{x}" for x in w[1:]]
        w = textwrap.wrap("rests on: " + rests, 96, break_on_hyphens=False)
        return out + [f"    {'':<17}{x}" for x in w]
    tools = (rl or (scl[0]["ladder"] if scl else {}) or {}).get("tools", {})
    any_l = rl or (scl[0]["ladder"] if scl else None)
    # 1 example rows
    if ex["rows"] and ex["both"]:
        o += rung("1 example rows", f"{ex['rust_pass']} of {ex['both']} pass on the compiled Rust; {ex['model_pass']} of {ex['rows']} on the Lean model",
                  "the rows the author wrote, and nothing beyond them; cucumber-rs through the per-piece Rust readings; rustc   [tested]")
    elif ex["rows"]:
        o += rung("1 example rows", f"{ex['model_pass']} of {ex['rows']} pass on the Lean model; not run on the compiled Rust in this run",
                  "the rows the author wrote; the Lean model   [tested]")
    else:
        o += rung("1 example rows", "none" + ("" if b["scenarios"] else ": no scenario sits under this rule"), "nothing")

    def agg(key):
        xs = [x["ladder"][key] for x in scl if x["ladder"].get(key)]
        return xs
    # 2 property test
    held_prop = held_bound = False
    nothing_compiled = not compiled and not any(x["reading"].get("compiled") for x in b["scenarios"])
    if any_l is None:
        o += rung("2 property test", "none: no reading was compiled for this rule, so no test was generated" if nothing_compiled else
                  "not run (the compiled Rust was not exercised in this run)", "nothing")
    else:
        if compiled and rl:
            p = rl["property"]
            text = f"{p['text']} (seed {rl['seed']})"
            held_prop = p["status"] == "pass"
        else:
            ps = agg("property")
            text = (f"{sum(x['status'] == 'pass' for x in ps)} of {len(ps)} scenarios: none falsified in {sum(x['cases'] or 0 for x in ps if x['status'] == 'pass')} "
                    f"generated inputs in scope (seed {any_l['seed']})"
                    + "".join(f"; {x['name']}: {x['ladder']['property']['text']}" for x in scl if x["ladder"]["property"]["status"] != "pass"))
            held_prop = bool(ps) and all(x["status"] == "pass" for x in ps)
        if compiled and rl and scl:
            ps = agg("property")
            text += f"; of the {len(ps)} scenario{'s' if len(ps) != 1 else ''} beneath it, {sum(x['status'] == 'pass' for x in ps)} not falsified, {sum(x['status'] == 'fail' for x in ps)} shown false"
        o += rung("2 property test", text,
                  f"a test GENERATED from the same composition tree as the Lean statement (no test code written for this rule); proptest {tools.get('proptest', '?')} "
                  f"with shrinking; generators derived from the types and the Givens, edge-weighted, collections up to {any_l.get('size', 6)} items"
                  + ("".join(f", up to {n} {w} in a second call" for w, n in (any_l.get("limit") or {}).items() if n > any_l.get("size", 6)) if compiled and rl else "")
                  + "; the typed "
                  "piece readings, compared with the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about inputs it did not draw   [tested, sampled]")
    # 3 bounded check
    if any_l is None or any_l.get("quick") or not ((rl or {}).get("bounded") or agg("bounded")):
        o += rung("3 bounded check", "none: no reading was compiled for this rule" if nothing_compiled else
                  "not run" + (" (--quick skips it)" if any_l and any_l.get("quick") else ""), "nothing")
    else:
        if compiled and rl and rl.get("bounded"):
            bd = rl["bounded"]
            text = bd["text"]
            held_bound = bool(bd["verified"]) and bd["status"] not in ("failed", "unreproduced")
        else:
            bs = agg("bounded")
            text = (f"{sum(x['status'] == 'verified' for x in bs)} of {len(bs)} scenarios hold at every rung of the ladder, "
                    f"{sum(x['status'] == 'partial' for x in bs)} at some rungs only, {sum(x['status'] == 'failed' for x in bs)} shown false"
                    + "".join(f"; {x['name']}: {x['ladder']['bounded']['text']}" for x in scl if x["ladder"].get("bounded") and x["ladder"]["bounded"]["status"] != "verified"))
            held_bound = bool(bs) and all(x["verified"] for x in bs) and not any(x["status"] in ("failed", "unreproduced") for x in bs)
        o += rung("3 bounded check", text,
                  f"a harness GENERATED from the same tree, asserting the same generated predicate; {tools.get('kani') or 'Kani'} on the Rust's MIR; every integer "
                  f"symbolic; collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; {any_l.get('kani_timeout')} s per rung); "
                  "it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked, bounded]")
    # 4 proof
    p = r["proof"]
    rp = p.get("rule")
    refuted = bool(rp and rp.get("kind") == "refutation") or (not compiled and bool(p["refutations"]))
    scs_ = b["scenarios"]
    n_proved = sum(x["code"] in PROVED for x in scs_)
    proved = bool(rp and rp.get("kind") != "refutation") if compiled else bool(scs_) and n_proved == len(scs_)
    if rp and rp.get("kind") == "refutation":
        ce = rd.get("counterexample") or {}
        o += rung("4 proof", f"REFUTED in the kernel: theorem {', '.join(rp['theorems'])} (the negation of the rule statement) at "
                  f"{json.dumps(ce.get('values'), ensure_ascii=False)}; axioms: {', '.join(rp.get('axioms', [])) or 'none'}",
                  "Lean's kernel; the Lean model generated by charon + aeneas (trusted; the input also fails on the compiled Rust)   [kernel-checked]")
    elif rp:
        o += rung("4 proof", f"theorem {', '.join(rp['theorems'])}: the rule statement for all inputs and all sizes, {rp['kind']}; axioms: "
                  f"{', '.join(rp.get('axioms', [])) or 'none'}",
                  "Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and cross-checked only by the rungs above   [kernel-checked]"
                  + assumed_note(b))
    elif p["universal"] or p["instance"] or p["refutations"] or p["vacuity"]:
        bits = []
        if p["universal"]:
            bits.append(f"{len(p['universal'])} scenario theorem{'s' if len(p['universal']) != 1 else ''} for all inputs ({', '.join(p['universal'])})")
        if p["instance"]:
            bits.append(f"{len(p['instance'])} for literal values only")
        if p["refutations"]:
            bits.append(f"{len(p['refutations'])} scenario{'s' if len(p['refutations']) != 1 else ''} REFUTED ({', '.join(p['refutations'])})")
        if p["vacuity"]:
            bits.append(f"{len(p['vacuity'])} shown true of nothing")
        o += rung("4 proof", ("no theorem about the rule statement itself; " if compiled else "") + "; ".join(bits) + f"; axioms: {', '.join(p['axioms']) or 'none'}",
                  "Lean's kernel; the Lean model generated by charon + aeneas (trusted)   [kernel-checked]")
    else:
        o += rung("4 proof", "none: nothing about this rule is kernel-checked", "nothing")
    # every falsifying input the generated harnesses found, with its source and what the model said
    ws = [(None, w) for w in (rl or {}).get("witnesses", [])] + [(x["name"], w) for x in scl for w in x["ladder"].get("witnesses", [])]
    for name, w in ws:
        what = ("MODEL MISMATCH: the compiled Rust " + str(w["rust"]) + " and the Lean model " + str(w["model"]) + " (a finding about the translation link)"
                if w.get("mismatch") else
                f"COUNTEREXAMPLE: on the compiled Rust it {w['rust']}; on the Lean model the reading {w['model']}" if w.get("model") != "not evaluated" else
                f"falsifying input: on the compiled Rust it {w['rust']}; NOT EVALUATED on the Lean model"
                + (f" ({w['model_note']})" if w.get("model_note") else ""))
        t = (f"[{name}] " if name else "") + f"{json.dumps(w['values'], ensure_ascii=False)}   source: generated {w['source']} ({w.get('note')}). {what}"
        w_ = textwrap.wrap(t, 96, break_on_hyphens=False)
        o += [f"    {'found false at':<17}{w_[0]}"] + [f"    {'':<17}{x}" for x in w_[1:]]
    # the strongest evidence held
    ce = rd.get("counterexample") if compiled else None
    if refuted:
        src_ = (ce or {}).get("source")
        strongest = ("a kernel-checked REFUTATION: the rule is false" if compiled else "a kernel-checked REFUTATION of a scenario beneath it")
        if compiled:
            strongest += f" (the input was found by {'the generated ' + src_ if src_ else 'the grid search of the reading'})"
    elif compiled and ce:
        strongest = "a COUNTEREXAMPLE on the Lean model and the compiled Rust, not confirmed in the kernel   [tested]"
    elif any(w.get("mismatch") for _, w in ws):
        strongest = "none that can be relied on: the compiled Rust and the Lean model DISAGREE at an input (MODEL MISMATCH)"
    elif any(w.get("rust") == "fails" for _, w in ws):
        strongest = "a falsifying input on the compiled Rust   [tested]"
    elif proved:
        strongest = "PROOF: kernel-checked for all inputs and sizes, on the Lean model" + ("" if compiled else " (every scenario; literal ones for their own values)")
        if b.get("assumptions"):
            na = len(b["assumptions"])
            strongest += (f", GIVEN {na} ASSUMPTION{'S' if na != 1 else ''} THAT NOTHING HERE CHECKS (" + "; ".join(f"{a['id']}: {open_text(a)}" for a in b["assumptions"])
                          + "): NOT a proof of what is assumed; see `Rests on`")
    elif not compiled and n_proved:
        strongest = (f"PROOF for {n_proved} of {len(scs_)} scenarios (kernel-checked, on the Lean model); the others hold what the rungs above "
                     "say and are NOT PROVED")
    elif held_bound:
        strongest = ("BOUNDED CHECK only: it holds at the sizes where Kani answered (listed above); it is NOT PROVED at any size where "
                     "Kani gave no answer, nor beyond")
    elif held_prop:
        strongest = "PROPERTY TEST only: no generated input falsifies it; NOT PROVED"
    elif ex["rows"] and ex["model_pass"] == ex["rows"]:
        strongest = "EXAMPLE ROWS only" + ("; some scenarios beneath it are proved, the rule as a whole is not" if p["universal"] or p["instance"] else "")
    else:
        strongest = "none"
    # plan node E2: the largest size each layer tried, when the statement speaks of a collection of open length and is
    # neither proved for all inputs nor shown false (clausal/sizes.py)
    flagged = [(None, rd.get("sizes"))] if compiled else [(x["name"], x["reading"].get("sizes")) for x in b["scenarios"]]
    flagged = [(n, s) for n, s in flagged if s and s.get("flag")]
    for n, s in flagged:
        w = textwrap.wrap((f"[{n}] " if n else "") + s["text"], 96, break_on_hyphens=False)
        o += [f"    {'sizes tried':<17}{w[0]}"] + [f"    {'':<17}{x}" for x in w[1:]]
    if flagged and not refuted:
        strongest += ("; LARGER INPUTS NOT EXAMINED (sizes tried, above)" if compiled else
                      f"; LARGER INPUTS NOT EXAMINED for {len(flagged)} scenario{'s' if len(flagged) != 1 else ''} (sizes tried, above)")
    w = textwrap.wrap(strongest, 96, break_on_hyphens=False)
    o += [f"    {'STRONGEST HELD':<17}{w[0]}"] + [f"    {'':<17}{x}" for x in w[1:]]
    o.append("")
    return o


def open_text(a: dict) -> str:
    """What is open about one assumption, in words: who vouches, and the usage conditions that are not proved or not stateable."""
    cs = a["conditions"]
    nu = sum(c["rule"] is None for c in cs)
    bad = sum(c["rule"] is not None and c["code"] != "PROVED-FOR-ALL" for c in cs)
    bits = [("vouched by " + (a["vouch"].get("name") or a["vouch"]["by"])) if a["vouch"] else "vouched by nobody"]
    if bad:
        bits.append(f"{bad} usage condition{'s' if bad != 1 else ''} NOT PROVED")
    if nu:
        bits.append(f"{nu} usage condition{'s' if nu != 1 else ''} cannot be stated")
    return ", ".join(bits)


def assumed_note(b: dict) -> str:
    """Appended to what the proof rung rests on, when the rule rests on an assumption: the proof does not reach it."""
    if not b.get("assumptions"):
        return ""
    return "; and, NOT covered by the proof, " + "; ".join(
        "the assumption " + a["id"] + (" behind the word " + ", ".join(w["id"] for w in a["attached"]) if a["attached"] else "")
        + (" (STAND-IN: the proof is about what the word is bound to in this tree, a toy)" if a["stand_in"] else "")
        for a in b["assumptions"]) + ": nothing here checks it, see `Rests on`   [assumed]"


TIERS = ["OPEN: not vouched, a usage condition not met or not stateable, or a meaning no person has reviewed",
         "NOTHING IN THIS RUN CHECKS IT",
         "CHECKED IN THIS RUN, or cross-checked"]
RANK = ["assumed", "meaning", "translation", "compilation", "proof"]


def assumption_tier(a: dict) -> int:
    """0 (open) unless a person or an organisation vouches AND every usage condition is proved in this graph; then 1: it is
    still something nothing here checks. An assumption is never in the last tier."""
    return 1 if (a["vouch"] and all(c["code"] == "PROVED-FOR-ALL" for c in a["conditions"])) else 0


def assumption_lines(a: dict) -> list:
    """One entry of the assumption ledger, as the block of a rule that rests on it prints it: the assumed fact, the word it hangs
    on, who vouches, each usage condition with its verdict in this graph, what is not covered, the external proof link."""
    o = _wrap("ASSUMED", f"{a['statement']} ({a['id']}" + ("; STAND-IN: what the word is bound to in this tree is a toy, not the real thing"
                                                           if a["stand_in"] else "") + ")   [assumed: nothing here checks it]")
    for w in a["attached"]:
        o += _wrap("", f"through the word {w['id']}: \"{w['form']}\"")
    v = a["vouch"]
    o += _wrap("", "vouched by: " + (f"{v.get('name') or v['by']} ({v['kind']}" + ("; claims to be, no signature is checked" if v["kind"] == "person" else "")
                                     + f"), {str(v.get('at'))[:10]}   [{v.get('evidence_kind')}]" if v else "nobody (AWAITED)"))
    for x in a["records"]:
        o += _wrap("", f"on record, not a vouch: {x.get('act')} by {x.get('by')} ({x.get('kind')})   [{x.get('evidence_kind')}]")
    cs = a["conditions"]
    np_, nu = sum(c["code"] == "PROVED-FOR-ALL" for c in cs), sum(c["rule"] is None for c in cs)
    rest = len(cs) - np_ - nu
    o += _wrap("", f"usage conditions: {np_} of {len(cs)} proved in this run" + (f", {rest} NOT PROVED" if rest else "")
               + (f", {nu} cannot be stated" if nu else "")
               + "".join(f"; {c['id']} is THIS RULE ITSELF (of the other {len(cs) - 1}: {np_ - (c['code'] == 'PROVED-FOR-ALL')} proved)" for c in cs if c.get("this")))
    for c in cs:
        text = f"{c['id']}  {c['code']:<16} " + (("[THIS RULE ITSELF] " if c.get("this") else "") + f"{c['text']}  ({c['rule']})" if c["rule"] else c["text"])
        w = textwrap.wrap(text, 96, break_on_hyphens=False, subsequent_indent=" " * 22) or [""]
        o += [f"    {'':<13}  {x}" for x in w]
    o += _wrap("", "not covered by the assumption or its conditions: " + ("; ".join(a["not_covered"]) or "nothing is listed"))
    x = a["external_proof"]
    o += _wrap("", "external proof: " + (f"{x['pointer']}, theorem {x['theorem']}, commit {x['commit']}, sha256 {x['sha256']} (a link and a hash: "
                                         "not fetched, read or checked here)" if x else "none"))
    o += _wrap("", "Lean axioms a proof resting on it may use: " + (", ".join(a["lean_axioms"]) or "none"))
    o += _wrap("", f"review by {a['review_by']}; {a['others']} other Rule statement{'s' if a['others'] != 1 else ''} rest{'' if a['others'] != 1 else 's'} on it")
    return o


def ranked_rests(assumptions: list, sections: dict, tiers: dict) -> list:
    """`Rests on`, heaviest first: tier (0 open, 1 nothing in this run checks it, 2 the rest), then assumed, meaning,
    translation, compilation, proof; assumptions among themselves by how many other rules rest on them, then by id."""
    items = [(assumption_tier(a), RANK.index("assumed"), -a["others"], a["id"], assumption_lines(a)) for a in assumptions]
    items += [(tiers[k], RANK.index(k), 0, k, lines) for k, lines in sections.items() if lines]
    items.sort(key=lambda x: x[:4])
    o = ["", "  Rests on   heaviest first"]
    tier = None
    for k, (ti, _, _, _, lines) in enumerate(items, 1):
        if ti != tier:
            o.append(f"    -- {TIERS[ti]}")
            tier = ti
        o.append(f" {k:>2} " + lines[0][4:])
        o += lines[1:]
    return o


def render(b: dict) -> list:
    """The block as plain-text lines (used in the terminal and, fenced, in report.md).

    First the block in the form of the README's target: Rule, Reading, Verdict, Examples, (Generated,) Suite, Rests on
    (meaning / proof / translation / compilation, each with its kind of evidence). Then `Detail`: the reading slot by slot
    with every default, the evidence lines of the rule statement, and the scenarios beneath the rule."""
    o = [b["title"] + (f"   [{b['source']}]" if b["source"] else "") + (f"   tags {' '.join(b['tags'])}" if b["tags"] else "")]
    o += ["  " + d for d in b["description"]]
    rd = b["reading"]
    v = b["verdict"]
    compiled = b["kind"] == "rule" and rd.get("compiled")

    def row(label, text, width=104):
        w = textwrap.wrap(text, width, break_on_hyphens=False) or [""]
        return [f"  {label:<10}{w[0]}"] + [f"  {'':<10}{x}" for x in w[1:]]
    if b["kind"] == "rule":
        if compiled:
            o += row("Reading", rd.get("summary") or "(see Detail)")
            o += row("Verdict", rd["headline"] + ("" if rd["as_expected"] else f"   <-- EXPECTED {rd['expected']}")
                     + (f"   (expected: {rd['expected']})" if rd["as_expected"] and rd["expected"] != "PROVED-FOR-ALL" else ""))
            ov = b.get("own_verdict")
            if b.get("assumptions") and ov:
                # the outcome of the verdict record (out/graph.json), in words: a proved rule on an open assumption is never `pass`
                why = [f"the assumption {a['id']} is {open_text(a)}" for a in b["assumptions"] if assumption_tier(a) == 0]
                if ov["unreviewed"]:
                    why.append(f"{ov['unreviewed']} of the Clausebook entries it is read with {'have' if ov['unreviewed'] != 1 else 'has'} been reviewed by no person")
                o += row("Outcome", {"review": "REVIEW, NOT PASS: " + ("; ".join(why) or "see the flags under Detail"),
                                     "pass": "PASS"}.get(ov["outcome"], ov["outcome"].upper()) + f"   (outcome `{ov['outcome']}` in out/graph.json)")
        else:
            o += row("Reading", f"NONE: {rd.get('status', 'NOT COMPILED')}" + ("" if rd.get("as_expected", True) else f"   <-- EXPECTED {rd.get('expected')}")
                     + (f"   (expected: {rd.get('expected')})" if rd.get("as_expected") else ""))
            o += row("Verdict", "no statement: the rule line is not a composition of Clausebook pieces")
    else:
        o += row("Verdict", v["head"] + (f": {v['detail']}" if v["detail"] else ""))
    ex = b["examples"]
    if not ex["rows"]:
        o += row("Examples", "none: no scenario with Examples rows sits under this rule" if not b["scenarios"] else "none could be evaluated")
    elif ex["both"]:
        o += row("Examples", f"{ex['rust_pass']} of {ex['both']} pass on the compiled Rust; {ex['model_pass']} of {ex['rows']} pass on the Lean model"
                 + ("" if ex["agree"] == ex["both"] else "   <-- THE TWO DISAGREE"))
    else:
        o += row("Examples", f"{ex['model_pass']} of {ex['rows']} pass on the Lean model; not run on the compiled Rust in this run")
    gr = b.get("grid") or {}
    if compiled:
        if gr.get("ran") and not gr.get("error"):
            ce = rd.get("counterexample") or {}
            o += row("Generated", f"the rule statement at {gr['points']} generated inputs on the compiled Rust: the same result as on the Lean model at "
                     f"{gr['agree']} of {gr['evals']} evaluations"
                     + ("" if gr["agree"] == gr["evals"] else "   <-- THE TWO DISAGREE")
                     + (f"; none of them falsifies it (it is FALSE at {json.dumps(ce['values'], ensure_ascii=False)}, an input the generated "
                        f"{ce['source']} found on the compiled Rust; see Evidence)" if ce and ce.get("source") else
                        f"; it is FALSE at {json.dumps(ce['values'], ensure_ascii=False)}" + (f", on the compiled Rust too ({ce['replayed_on_rust']})"
                                                                                               if ce.get("replayed_on_rust") else "") if ce else
                        "; no input found at which it is false"))
        elif gr.get("ran"):
            o += row("Generated", f"NOT evaluated on the compiled Rust: {gr['error']}")
        else:
            o += row("Generated", "the rule statement was not evaluated on the compiled Rust in this run")
    o += evidence_lines(b)
    if b["suite"]:
        for k, l in enumerate(b["suite"]):
            w = textwrap.wrap(l, 108, subsequent_indent="  ", break_on_hyphens=False) or [""]
            o.append(f"  {'Suite' if k == 0 else '':<10}{w[0]}")
            o += [f"  {'':<10}{x}" for x in w[1:]]
    else:
        o.append(f"  {'Suite':<10}no adequacy note for this group")
    if compiled and rd.get("display"):      # plan node Q6: computed from the statement, stored in the graph; never compiler input
        try:
            from .displaytext import render as render_display
        except ImportError:                 # rules.py run as a file: the module beside it
            from displaytext import render as render_display
        o += render_display(rd["display"])
    r = b["rests"]
    head_at = len(o)
    o += ["", "  Rests on"]
    marks = {"meaning": len(o)}
    m = r["meaning"]
    n = len(m["pieces"])
    if not n:
        o += _wrap("meaning", "no Clausebook piece is used (no reading was compiled)")
    else:
        # "signed" = reviewed or approved by a PERSON (an attestation record of kind person). Records of another kind are counted
        # apart, per kind, under their own label: they are never added to the signed count and never make a piece signed.
        others = {}
        for p in m["pieces"]:
            for k in {a["kind"] for a in p.get("attested", [])}:
                others[k] = others.get(k, 0) + 1
        kind = ("human-asserted" if m["pieces_signed"] == n else ("NOT ASSERTED by any person" if others else "NOT ASSERTED by anyone") if m["pieces_signed"] == 0
                else "human-asserted in part")
        o += _wrap("meaning", f"{n} Clausebook pieces, {'all' if m['pieces_signed'] == n else m['pieces_signed']} signed   [{kind}]")
        for k, c in sorted(others.items()):
            o += _wrap("", f"{c} of {n} carry a record by a {k}   [{ASSERTED.get(k, k)}; not a person's review]")
        o += _wrap("", "(" + ", ".join(f"{p['id']}: {p['kind']}, " + (f"signed by {p['by']}" if p.get("signed") else "unsigned")
                                       + "".join(f"; {a['act']} by {a['by']}" for a in p.get("attested", [])) for p in m["pieces"]) + ")")
        if m["compiled"]:
            o += _wrap("", f"{m['linked']} of {m['compiled']} scenario readings proved equivalent to the flat statement their proof is about   [kernel-checked]")
        if m.get("new"):
            o += _wrap("", f"{m['new']} scenario{'s' if m['new'] != 1 else ''} beneath the rule {'are' if m['new'] != 1 else 'is a'} NEW "
                           f"sentence{'s' if m['new'] != 1 else ''}: read by the Clausebook alone, no entry of the old glossary")
    if m["entries"]:
        ne = len(m["entries"])
        o += _wrap("", f"the flat statements of the older scenarios still use {ne} whole-phrase entries of the old glossary, "
                       f"{'all' if m['signed'] == ne else m['signed']} signed")
    marks["proof"] = len(o)
    p = r["proof"]
    bits, names = [], []
    rp = p.get("rule")
    if rp and rp.get("kind") == "refutation":
        bits.append("the rule statement is refuted at a concrete input")
        names += rp["theorems"]
    elif rp:
        bits.append(f"the rule statement for all inputs, {rp['kind']}")
        names += rp["theorems"]
    if p["universal"]:
        bits.append(f"{len(p['universal'])} scenario theorem{'s' if len(p['universal']) != 1 else ''} for all inputs")
    if p["instance"]:
        bits.append(f"{len(p['instance'])} for literal values only")
    if p["refutations"]:
        bits.append(f"{len(p['refutations'])} refutation{'s' if len(p['refutations']) != 1 else ''} (the scenario is false)")
    if p["vacuity"]:
        bits.append(f"{len(p['vacuity'])} proof{'s' if len(p['vacuity']) != 1 else ''} that the Givens contradict each other (the scenario is true of nothing)")
    names += p["universal"] + p["instance"] + p["refutations"] + p["vacuity"]
    if bits:
        o += _wrap("proof", "checked by Lean's kernel: " + ", ".join(bits) + "; axioms: "
                   + (", ".join(p["axioms"]) or "none") + (" (the standard three only)" if p["standard_only"] and p["axioms"] else
                                                          "" if p["standard_only"] else "  <-- NOT ONLY THE STANDARD AXIOMS")
                   + "   [kernel-checked]")
        o += _wrap("", "(" + ", ".join(dict.fromkeys(names)) + ")")
    elif compiled:
        o += _wrap("proof", "none: nothing about this rule is kernel-checked" + ("; it is TESTED ONLY" if rd.get("status") == "TESTED-ONLY" else ""))
    if p["none"]:
        o += _wrap("proof" if not bits and not compiled else "", f"no kernel-checked theorem for: {', '.join(x.rsplit('.', 1)[1] for x in p['none'])}")
    marks["translation"] = len(o)
    t = r["translation"]
    if t["fns"]:
        tc = t["toolchain"]
        files = sorted({f["rust_file"] for f in t["fns"] if f["rust_file"]})
        o += _wrap("translation", f"Lean model{'s' if len(t['fns']) != 1 else ''} {', '.join(f['lean'] for f in t['fns'])} generated from "
                   f"{', '.join(files)} by charon {tc.get('charon', '?')} + aeneas {tc.get('aeneas', '?')}   [tool-trusted]")
        cross = []
        if t["rows"]:
            cross.append(f"{t['rows']} example rows ({t['agree']} give the same result on the compiled Rust and on the model)")
        if gr.get("ran") and not gr.get("error"):
            cross.append(f"{gr['points']} generated inputs of the rule statement ({gr['agree']} of {gr['evals']} evaluations the same)")
        o += _wrap("", ("cross-checked on " + " and on ".join(cross) + "   [tested]") if cross else
                       "not cross-checked in this run: nothing was run on both the compiled Rust and the model")
    else:
        o += _wrap("translation", "no model function is involved (no statement was generated)")
    marks["compilation"] = len(o)
    c = r["compilation"]
    o += _wrap("compilation", (f"{c['rustc']}, as used for the cucumber-rs test build   [trusted, not checked]" if c["ran"]
                               else "the compiled Rust was not exercised in this run"))
    if b.get("assumptions"):
        # plan node W4: a rule that rests on an assumption prints what it rests on HEAVIEST FIRST (trust/FREEZE-w46.md section 4)
        order = ["meaning", "proof", "translation", "compilation"]
        ends = [marks[k] for k in order[1:]] + [len(o)]
        sections = {k: o[marks[k]:e] for k, e in zip(order, ends)}
        cross = bool(t["rows"]) or bool(gr.get("ran") and not gr.get("error"))
        tiers = {"meaning": 0 if (n and m["pieces_signed"] < n) else 2, "proof": 2,
                 "translation": 1 if (t["fns"] and not cross) else 2, "compilation": 1 if c["ran"] else 2}
        o[head_at:] = ranked_rests(b["assumptions"], sections, tiers)
    # ---- detail
    o += ["", "  Detail"]
    if compiled:
        first = True
        for slot, text in rd["echo"]:
            if slot == "assuming" and b.get("assumptions"):
                # this slot echoes the sentence's conditions on the state and the input. It is NOT the assumption ledger: say so
                na = len(b["assumptions"])
                text = (("no condition on the state or the input: every state and every input" if text.startswith("nothing:") else text)
                        + f". (This slot is about inputs only. The rule ALSO rests on {na} assumption{'s' if na != 1 else ''} nothing here checks: "
                        + ", ".join(a["id"] for a in b["assumptions"]) + ", see `Rests on`)")
            w = textwrap.wrap(text, 98, break_on_hyphens=False) or [""]
            o.append(f"  {'Reading' if first else '':<10}{slot:<12}{w[0]}")
            o += [f"  {'':<10}{'':<12}{x}" for x in w[1:]]
            first = False
    if b["kind"] == "rule":
        for l in rd.get("lines", []):
            w = textwrap.wrap(l, 108, subsequent_indent="                 ", break_on_hyphens=False) or [""]
            o += [f"  {'':<10}{x}" for x in w]
        if rd.get("flags"):
            o.append(f"  {'':<10}flags            {'; '.join(rd['flags'])}")
    o += [f"  {'Scenarios':<10}{v['head']}" + (f": {v['detail']}" if v["detail"] else "")
          + ("" if v["as_expected"] else "   <-- NOT WHAT WAS EXPECTED")]
    parts = set(rd.get("parts") or [])
    for s in b["scenarios"]:
        role = ""
        if b["kind"] == "rule" and rd.get("compiled"):
            role = ("   [a part: the rule statement is proved from it]" if s["id"] in parts else
                    "   [an instance: literal values]" if s["scope"] != "universal" else "   [beneath the rule; not used to prove it]")
        o.append(f"  {'':<10}{s['code']:<16}{s['name']}"
                 + ("" if s["code"] in PROVED and s["as_expected"] else f"   (expected {s['expected']}"
                    + ("" if s["as_expected"] else ": MISMATCH") + ")") + role + ("   [NEW sentence]" if s.get("new") else ""))
    return o


def main(argv) -> int:
    path = Path(argv[0]) if argv else Path(__file__).resolve().parent.parent / "out" / "graph.json"
    g = json.loads(path.read_text())
    for b in blocks(g):
        print("\n".join(render(b)))
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
