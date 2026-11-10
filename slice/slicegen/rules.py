"""slicegen rules: the per-Rule block of the report, computed from the refinement graph and NOTHING else.

    python3 -m slicegen rules [graph.json]      print the blocks of a stored graph (default out/graph.json)

`blocks(graph)` takes the parsed JSON of out/graph.json. `slicegen report` writes the graph to disk, reads the
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
        # two statements formalise a scenario: the reading compiled from the vocabulary (`.reading`) and the flat
        # statement the proofs are about (`.stmt`). Proofs, refutations and rows hang off the flat one.
        stmt = next((e["from"] for e in in_edges.get((sid, "formalises"), []) if e["from"].endswith(".stmt")), None)
        info = {"node": sid, "id": sid.split(":", 1)[1], "name": n.get("attrs", {}).get("name", sid),
                "scope": n.get("attrs", {}).get("scope"), "code": v["code"] if v else "NO-VERDICT",
                "expected": v.get("expected") if v else None, "as_expected": v.get("as_expected") if v else None,
                "flags": v["flags"] if v else [], "stmt": stmt, "rows": [], "phrases": [], "proof": None,
                "refutation": None, "vacuity": None, "fns": [], "reading": n.get("attrs", {}).get("reading") or {}}
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
        # verdict
        univ = [s for s in scs if s["scope"] == "universal"]
        inst = [s for s in scs if s["scope"] != "universal"]
        counts = {}
        for s in scs:
            counts[s["code"]] = counts.get(s["code"], 0) + 1
        tally = ", ".join(f"{k} {c}" for c, k in counts.items())
        if not scs:
            head = "NOTHING STATED: no scenario sits under this rule, so nothing was compiled, tested or proved for it"
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
        # the vocabulary pieces the rule line and the scenario readings are composed of
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
        b["rests"] = {
            "meaning": {"entries": list(phrases.values()), "signed": sum(p["signed"] for p in phrases.values()),
                        "by": sorted({p["by"] for p in phrases.values() if p["by"]}),
                        "pieces": list(pieces.values()), "pieces_signed": sum(bool(p["signed"]) for p in pieces.values()),
                        "linked": sum(1 for s in scs if s["reading"].get("linked")),
                        "compiled": sum(1 for s in scs if s["reading"].get("compiled"))},
            "proof": {"universal": [s["proof"]["theorem"] for s in proofs if s["proof"]["scope"] == "all"],
                      "instance": [s["proof"]["theorem"] for s in proofs if s["proof"]["scope"] != "all"],
                      "refutations": [s["refutation"]["theorem"] for s in refs],
                      "vacuity": [s["vacuity"]["theorem"] for s in vacs], "axioms": ax,
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


def render(b: dict) -> list:
    """The block as plain-text lines (used in the terminal and, fenced, in report.md)."""
    o = [b["title"] + (f"   [{b['source']}]" if b["source"] else "") + (f"   tags {' '.join(b['tags'])}" if b["tags"] else "")]
    o += ["  " + d for d in b["description"]]
    rd = b["reading"]
    if b["kind"] == "rule":
        if rd.get("compiled"):
            first = True
            for slot, text in rd["echo"]:
                w = textwrap.wrap(text, 98, break_on_hyphens=False) or [""]
                o.append(f"  {'Reading' if first else '':<10}{slot:<12}{w[0]}")
                o += [f"  {'':<10}{'':<12}{x}" for x in w[1:]]
                first = False
            o.append(f"  {'Verdict':<10}{rd['headline']}" + ("" if rd["as_expected"] else f"   <-- EXPECTED {rd['expected']}")
                     + (f"   (expected: {rd['expected']})" if rd["as_expected"] and rd["expected"] != "PROVED-FOR-ALL" else ""))
            for l in rd.get("lines", []):
                w = textwrap.wrap(l, 108, subsequent_indent="                 ", break_on_hyphens=False) or [""]
                o += [f"  {'':<10}{x}" for x in w]
            if rd.get("flags"):
                o.append(f"  {'':<10}flags            {'; '.join(rd['flags'])}")
        else:
            o.append(f"  {'Reading':<10}NONE: {rd.get('status', 'NOT COMPILED')}" + ("" if rd.get("as_expected", True) else f"   <-- EXPECTED {rd.get('expected')}")
                     + (f"   (expected: {rd.get('expected')})" if rd.get("as_expected") else ""))
            for l in rd.get("lines", []):
                w = textwrap.wrap(l, 108, subsequent_indent="  ", break_on_hyphens=False) or [""]
                o += [f"  {'':<10}{x}" for x in w]
    v = b["verdict"]
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
                    + ("" if s["as_expected"] else ": MISMATCH") + ")") + role)
    ex = b["examples"]
    if not ex["rows"]:
        o.append(f"  {'Examples':<10}none could be evaluated")
    elif ex["both"]:
        o.append(f"  {'Examples':<10}{ex['rust_pass']} of {ex['both']} pass on the compiled Rust; {ex['model_pass']} of {ex['rows']} pass on the Lean model"
                 + ("" if ex["agree"] == ex["both"] else "   <-- THE TWO DISAGREE"))
    else:
        o.append(f"  {'Examples':<10}{ex['model_pass']} of {ex['rows']} pass on the Lean model; not run on the compiled Rust in this run")
    if b["suite"]:
        for k, l in enumerate(b["suite"]):
            w = textwrap.wrap(l, 108, subsequent_indent="  ", break_on_hyphens=False) or [""]
            o.append(f"  {'Suite' if k == 0 else '':<10}{w[0]}")
            o += [f"  {'':<10}{x}" for x in w[1:]]
    else:
        o.append(f"  {'Suite':<10}no adequacy note for this group")
    r = b["rests"]
    o += ["", "  Rests on"]
    m = r["meaning"]
    n = len(m["pieces"])
    if not n:
        o += _wrap("meaning", "no vocabulary piece is used (no reading was compiled)")
    else:
        kind = ("human-asserted" if m["pieces_signed"] == n else "NOT ASSERTED by anyone" if m["pieces_signed"] == 0
                else "human-asserted in part")
        o += _wrap("meaning", f"{n} vocabulary pieces, {'all' if m['pieces_signed'] == n else m['pieces_signed']} signed   [{kind}]")
        o += _wrap("", "(" + ", ".join(p["id"] for p in m["pieces"]) + ")")
        if m["compiled"]:
            o += _wrap("", f"{m['linked']} of {m['compiled']} scenario readings proved equivalent to the flat statement their proof is about   [kernel-checked]")
    if m["entries"]:
        ne = len(m["entries"])
        o += _wrap("", f"the flat statements and the Rust steps still use {ne} whole-phrase entries of the old glossary, "
                       f"{'all' if m['signed'] == ne else m['signed']} signed")
    p = r["proof"]
    bits = []
    if p["universal"]:
        bits.append(f"{len(p['universal'])} theorem{'s' if len(p['universal']) != 1 else ''} for all inputs")
    if p["instance"]:
        bits.append(f"{len(p['instance'])} for literal values only")
    if p["refutations"]:
        bits.append(f"{len(p['refutations'])} refutation{'s' if len(p['refutations']) != 1 else ''} (the scenario is false)")
    if p["vacuity"]:
        bits.append(f"{len(p['vacuity'])} proof{'s' if len(p['vacuity']) != 1 else ''} that the Givens contradict each other (the scenario is true of nothing)")
    if bits:
        o += _wrap("proof", "checked by Lean's kernel: " + ", ".join(bits) + "; axioms: "
                   + (", ".join(p["axioms"]) or "none") + (" (the standard three only)" if p["standard_only"] and p["axioms"] else
                                                          "" if p["standard_only"] else "  <-- NOT ONLY THE STANDARD AXIOMS")
                   + "   [kernel-checked]")
        o += _wrap("", "(" + ", ".join(p["universal"] + p["instance"] + p["refutations"] + p["vacuity"]) + ")")
    if p["none"]:
        o += _wrap("proof" if not bits else "", f"no kernel-checked theorem for: {', '.join(x.rsplit('.', 1)[1] for x in p['none'])}")
    t = r["translation"]
    if t["fns"]:
        tc = t["toolchain"]
        files = sorted({f["rust_file"] for f in t["fns"] if f["rust_file"]})
        o += _wrap("translation", f"Lean model{'s' if len(t['fns']) != 1 else ''} {', '.join(f['lean'] for f in t['fns'])} generated from "
                   f"{', '.join(files)} by charon {tc.get('charon', '?')} + aeneas {tc.get('aeneas', '?')}   [tool-trusted]")
        o += _wrap("", (f"cross-checked on {t['rows']} example rows: {t['agree']} give the same result on the compiled Rust and on the model   [tested]"
                        if t["rows"] else "not cross-checked in this run: no example row was run on both the compiled Rust and the model"))
    else:
        o += _wrap("translation", "no model function is involved (no statement was generated)")
    c = r["compilation"]
    o += _wrap("compilation", (f"{c['rustc']}, as used for the cucumber-rs test build   [trusted, not checked]" if c["ran"]
                               else "the compiled Rust was not exercised in this run"))
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
