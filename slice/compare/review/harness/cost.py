#!/usr/bin/env python3
"""Cost per rule and arm: lines written, and wall-clock on the unmutated code.

    python3 harness/cost.py [--time-proofs]      writes results/cost.json and results/cost.md

Lines are counted on the frozen snapshot (work/snapshot):
  a  the rule's Gherkin (tag, title, steps = "statement"; Examples header and rows = "rows"), non-blank,
     non-comment lines; shared: the cucumber step definitions and the Rust reading of each phrase.
  b  the lines between "// RULE <id>" and "// END RULE" in arms/proptests/src/main.rs (non-blank);
     shared: every other non-blank line of that file.
  c  the same for arms/kani/src/lib.rs.
  d  the rule's Gherkin statement; the tactic lines of its proof (as slice/effort/count.py counts them);
     the hand-written lemma modules its proof imports, directly or not (code lines as count.py counts
     them), given twice: in full ("rests on"), and divided equally among all scenario proofs that import
     the module ("share"); shared: the glossary definitions in Lean (Vocab) and glossary.yaml.
--time-proofs: in a scratch copy, rebuild each proof module on its own (`lake build <module>` after
changing a comment in it) and the lemma library, and record the seconds.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import COMPARE, RESULTS, RULES, SLICE, SNAPSHOT, WORK, feature_index, sh  # noqa: E402


def nonblank(text):
    return sum(1 for l in text.splitlines() if l.strip())


def rule_blocks(path: Path):
    text = path.read_text()
    blocks = {m.group(1): m.group(0) for m in re.finditer(r"// RULE (\w+)\n.*?// END RULE", text, re.S)}
    per = {k: nonblank(v) - 2 for k, v in blocks.items()}          # without the two marker lines
    shared = nonblank(text) - sum(nonblank(v) for v in blocks.values())
    return per, shared


def main():
    spec = importlib.util.spec_from_file_location("count", SNAPSHOT / "effort" / "count.py")
    count = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(count)
    lean = SNAPSHOT / "lean"
    index = feature_index(SNAPSHOT)
    # Gherkin
    gh = {}
    for name, spans in index.items():
        lines = (SNAPSHOT / "features" / name).read_text().splitlines()
        for (a, b, sid, tags, kind, title) in spans:
            body = [l.strip() for l in lines[a - 1:b] if l.strip() and not l.strip().startswith("#")]
            rows = [l for l in body if l.startswith("|")]
            ex = [l for l in body if l.startswith("Examples")]
            gh[sid] = {"statement": len(body) - len(rows) - len(ex), "rows_lines": len(rows) + len(ex), "example_rows": max(len(rows) - 1, 0)}
    prop, prop_shared = rule_blocks(COMPARE / "arms/proptests/src/main.rs")
    kani, kani_shared = rule_blocks(COMPARE / "arms/kani/src/lib.rs")
    # Lean: proofs and lemma modules
    lemma_dir = lean / "Ledger" / "Lemmas"
    lemma_code = {p.stem: count.lean_lines(p.read_text())[0] for p in sorted(lemma_dir.glob("*.lean"))}
    lemma_imports = {p.stem: re.findall(r"^import Ledger\.Lemmas\.(\w+)", p.read_text(), re.M) for p in sorted(lemma_dir.glob("*.lean"))}

    def closure(mods):
        seen, todo = set(), list(mods)
        while todo:
            m = todo.pop()
            if m not in seen:
                seen.add(m)
                todo += lemma_imports.get(m, [])
        return seen
    proofs = {}
    for p in sorted((lean / "Wallet" / "Proofs").glob("*/*.lean")):
        proofs[p.stem] = {"feature": p.parent.name, "lines": count.proof_lines(p),
                          "lemmas": sorted(closure(re.findall(r"^import Ledger\.Lemmas\.(\w+)", p.read_text(), re.M)))}
    importers = {m: sum(1 for q in proofs.values() if m in q["lemmas"]) for m in lemma_code}
    vocab = {"wallet": count.lean_lines((lean / "Wallet/Vocab.lean").read_text())[0], "ledger": count.lean_lines((lean / "Ledger/Vocab.lean").read_text())[0]}
    base = json.loads((RESULTS / "raw" / "baseline.json").read_text())
    timing = json.loads((RESULTS / "proof_times.json").read_text()) if (RESULTS / "proof_times.json").exists() else {}
    if "--time-proofs" in sys.argv:
        timing = time_proofs(proofs)
        (RESULTS / "proof_times.json").write_text(json.dumps(timing, indent=1) + "\n")
    rules = []
    for r in RULES:
        rid = r["id"]
        pf = proofs[rid]
        rules.append({"id": rid, "kind": r["kind"], "crate": r["crate"],
                      "gherkin_statement": gh[rid]["statement"], "gherkin_rows_lines": gh[rid]["rows_lines"], "example_rows": gh[rid]["example_rows"],
                      "a_lines": gh[rid]["statement"] + gh[rid]["rows_lines"],
                      "b_lines": prop[rid], "c_lines": kani[rid],
                      "d_proof_lines": pf["lines"], "d_lemma_modules": pf["lemmas"],
                      "d_lemma_lines_rests_on": sum(lemma_code[m] for m in pf["lemmas"]),
                      "d_lemma_lines_share": round(sum(lemma_code[m] / importers[m] for m in pf["lemmas"]), 1),
                      "b_plain_ms": base["b"]["plain"]["rules"][rid]["elapsed_ms"], "b_edge_ms": base["b"]["edge"]["rules"][rid]["elapsed_ms"],
                      "c_secs": base["c"]["rules"][rid]["secs"], "c_verification_secs": base["c"]["rules"][rid]["verification_secs"],
                      "d_proof_rebuild_secs": (timing.get("proofs") or {}).get(rid)})
    bdd = SNAPSHOT / "wallet-bdd"
    shared = {"a": {"cucumber step definitions (wallet-bdd/tests/bdd.rs), non-blank lines": nonblank((bdd / "tests/bdd.rs").read_text()),
                    "Rust reading of each phrase (wallet-bdd/src/lib.rs), non-blank lines": nonblank((bdd / "src/lib.rs").read_text()),
                    "scenarios served": sum(len(s) for s in index.values())},
              "b": {"generators, runner and registry (arms/proptests/src/main.rs outside the rule blocks), non-blank lines": prop_shared, "rules served": len(prop)},
              "c": {"input builders and helpers (arms/kani/src/lib.rs outside the rule blocks), non-blank lines": kani_shared, "rules served": len(kani)},
              "d": {"glossary definitions in Lean (Vocab), code lines": vocab, "glossary.yaml, non-blank lines": nonblank((SNAPSHOT / "glossary.yaml").read_text()),
                    "lemma library (lean/Ledger/Lemmas), code lines per module": lemma_code, "scenario proofs importing each lemma module (directly or not)": importers,
                    "proof lines of all scenario proofs": {f: sum(p["lines"] for p in proofs.values() if p["feature"] == f) for f in ("wallet", "ledger")}}}
    whole = {"a_cucumber_secs": base["a"]["secs"], "a_build_secs": base["a"]["build_secs"], "b_plain_secs": base["b"]["plain"]["secs"], "b_edge_secs": base["b"]["edge"]["secs"],
             "b_build_secs": base["b"]["build_secs"], "c_all_harnesses_secs": base["c"]["secs"], "c_build_secs": base["c"]["build_secs"],
             "d_pipeline_secs": base["d"]["secs"], "d_lemma_library_rebuild_secs": timing.get("lemma_library"), "d_all_proofs_rebuild_secs": timing.get("all_proofs")}
    out = {"rules": rules, "shared": shared, "whole_run_on_unmutated_code": whole,
           "effort_quoted_from_slice": {"source": "slice/DESIGN.md 12.4 and 12.8, slice/effort/attempts.tsv (builder's own tally, not re-measured)",
                                        "wallet": "8 proofs of 4 to 6 lines, no lemma, 2 failed builds in all",
                                        "ledger lemma library": "227 code lines, 18 theorems, 5 definitions, 2 loop invariants; about 30 builds of which 17 failed, an estimated 1.5 to 2 hours; plus about 60 lines and 11 builds (8 failed) for the exact-result part",
                                        "ledger scenario proofs": "12 universal proofs accepted at the first build; 4 added after the review in 3 builds (1 failed)"}}
    (RESULTS / "cost.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    hdr = ["Rule", "Kind", "Gherkin statement lines", "a: + rows lines (rows)", "b: property lines", "c: harness lines", "d: proof lines",
           "d: lemma lines it rests on (share)", "b ms plain / edge", "c seconds", "d seconds to re-check the proof"]
    rows = [[x["id"], x["kind"], x["gherkin_statement"], f"{x['gherkin_rows_lines']} ({x['example_rows']})", x["b_lines"], x["c_lines"], x["d_proof_lines"],
             f"{x['d_lemma_lines_rests_on']} ({x['d_lemma_lines_share']})" if x["d_lemma_modules"] else "0", f"{x['b_plain_ms']} / {x['b_edge_ms']}",
             f"{x['c_secs']:.0f}", x["d_proof_rebuild_secs"] if x["d_proof_rebuild_secs"] is not None else "-"] for x in rules]
    kinds = {}
    for crate in ("wallet", "ledger"):
        for k in ("safety", "exact", "rejection", "progress", "bound"):
            xs = [x for x in rules if x["kind"] == k and x["crate"] == crate]
            n = len(xs)
            if not n:
                continue
            avg = lambda f: round(sum(x[f] or 0 for x in xs) / n, 1)  # noqa: E731
            kinds[(crate, k)] = [crate + (" (straight-line)" if crate == "wallet" else " (loops, Vec)"), k, n, avg("gherkin_statement"), avg("gherkin_rows_lines"),
                                 avg("b_lines"), avg("c_lines"), avg("d_proof_lines"), avg("d_lemma_lines_share"), avg("d_lemma_lines_rests_on"),
                                 f"{avg('b_plain_ms')} / {avg('b_edge_ms')}", avg("c_secs"), avg("d_proof_rebuild_secs")]
    md = ["<!-- table:cost_rules -->", "| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)] + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    h2 = ["Crate", "Kind", "Rules", "Gherkin statement lines", "a: rows lines", "b: property lines", "c: harness lines", "d: proof lines",
          "d: lemma lines, share", "d: lemma lines the proof rests on", "b: ms plain / edge", "c: seconds", "d: seconds to re-check the proof"]
    md += ["", "<!-- table:cost_kinds -->", "| " + " | ".join(h2) + " |", "|" + "---|" * len(h2)] + ["| " + " | ".join(str(c) for c in r) + " |" for r in kinds.values()]
    # whole-run wall-clock on the unmutated code: measured alone, and (if kept) as measured inside the main run
    under = RESULTS / "baseline.under-load.json"
    u = json.loads(under.read_text()) if under.exists() else None
    led = lambda x: round(sum(v["secs"] for k, v in x["c"]["rules"].items() if next(r for r in RULES if r["id"] == k)["crate"] == "ledger"))  # noqa: E731
    f = lambda v: f"{v:.1f} s" if v < 20 else f"{v:.0f} s"  # noqa: E731
    pair = lambda get: f(get(base)) + (" (" + f(get(u)) + ")" if u else "")  # noqa: E731
    h3 = ["Arm", "Build", "Run", "Notes"]
    r3 = [["a. example rows", pair(lambda x: x["a"]["build_secs"]), pair(lambda x: x["a"]["secs"]), "all 35 scenarios of the three feature files"],
          ["b. proptest", pair(lambda x: x["b"]["build_secs"]), "plain " + pair(lambda x: x["b"]["plain"]["secs"]) + "; edge " + pair(lambda x: x["b"]["edge"]["secs"]),
           "23 properties, 10,000 cases each"],
          ["c. Kani", pair(lambda x: x["c"]["build_secs"]), pair(lambda x: x["c"]["secs"]) + ", of which the 16 ledger rules " + f(led(base)) + (" (" + f(led(u)) + ")" if u else ""),
           "23 harnesses run one at a time; per rule in appendix B"],
          ["d. Lean", "-", pair(lambda x: x["d"]["secs"]),
           "the whole pipeline: translation, build, search, audit, cucumber, report. Re-checking one proof after an edit: "
           + (f"{min(timing['proofs'].values()):.0f} to {max(timing['proofs'].values()):.0f} s; rebuilding the lemma library: {timing['lemma_library']:.0f} s" if timing.get("proofs") else "not timed")]]
    md += ["", "<!-- table:cost_whole -->", "| " + " | ".join(h3) + " |", "|" + "---|" * len(h3)] + ["| " + " | ".join(str(c) for c in r) + " |" for r in r3]
    (RESULTS / "cost.md").write_text("\n".join(md) + "\n")
    print("\n".join(md[:30]))
    print(json.dumps(shared, indent=1))
    print(json.dumps(whole, indent=1))


def time_proofs(proofs):
    """Seconds to re-check each scenario proof on its own, the lemma library, and all proofs, in a scratch copy."""
    work = WORK / "cost0"
    rc, out, _ = sh(f"'{COMPARE}/harness/workcopy.sh' '{SNAPSHOT}' '{work}' '{SLICE}'", COMPARE, 600)
    assert rc == 0, out
    rc, out, secs = sh("./run.sh --no-unit --no-rust", work, 1800)             # everything built once
    assert rc == 0, out[-800:]
    res = {"proofs": {}}
    stamp = f"-- timing {time.time()}\n"
    for name, p in proofs.items():
        f = work / "lean" / "Wallet" / "Proofs" / p["feature"] / f"{name}.lean"
        f.write_text(f.read_text() + stamp)
        rc, out, secs = sh(f"lake build Wallet.Proofs.{p['feature']}.{name}", work / "lean", 600)
        res["proofs"][name] = secs if rc == 0 else None
    for f in sorted((work / "lean" / "Ledger" / "Lemmas").glob("*.lean")):
        f.write_text(f.read_text() + stamp)
    rc, out, secs = sh("lake build Ledger", work / "lean", 1200)
    res["lemma_library"] = secs if rc == 0 else None
    rc, out, secs = sh("lake build", work / "lean", 1200)                         # every proof that depends on a lemma module
    res["all_proofs"] = secs if rc == 0 else None
    return res


if __name__ == "__main__":
    main()
