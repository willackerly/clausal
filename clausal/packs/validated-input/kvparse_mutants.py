#!/usr/bin/env python3
"""K1: the seeded bugs and the trivial implementations of the rule pack "validated input", as mutants of the toy parser
kvparse, and the strip test. Run from clausal/:

    ../tools/sem.sh 3 -- python3 packs/validated-input/kvparse_mutants.py [--only ID,ID] [--keep]

Each item is run in ONE scratch copy of clausal/ (mutation/workcopy.sh; build/k1-mutants/work; the real tree is never
touched), one after the other:

  baseline     the tree as it is:                         ./run.sh --no-unit --quick --no-adequacy --no-heldout
  strip        packs/ deleted, clausal/pack.py deleted, the bindings file deleted, the @pack tags stripped from the
               feature file (python3 -m clausal pack strip, run BEFORE pack.py is deleted): the same command. EVERY verdict
               code of out/graph.json must equal the baseline's.
  B1 .. B6     the seeded bugs of packs/validated-input/pack.yaml (B5 in both directions), each one textual change to
               kvparse/src/lib.rs: the same command.
  T-*          the trivial implementations of the pack's adequacy expectation, in the place of the parse.

A pack rule is SHOWN FALSE of a mutant if its verdict is REFUTED there and is not at the baseline (the frozen
criterion, packs/validated-input/FREEZE.md). COUNTEREXAMPLE (found false, not confirmed in the kernel) is listed
separately. A rule that only loses its proof (PROVED-FOR-ALL at the baseline, TESTED-ONLY on the mutant) is NOT shown
false; it is listed as `proof lost`.

--quick: the bounded checks (Kani) are not run. They would not look at a kvparse rule anyway: the generated property
tests and bounded checks have no typed reading of the kvparse words (clausal/evgen.py), so a kvparse rule is examined by
the grid search on the Lean model and by the same grid on the compiled Rust, and by nothing else.

Writes packs/validated-input/results/kvparse_mutants.json and .md; logs under build/k1-mutants/logs/.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))
LIB = "kvparse/src/lib.rs"
FEATURE = "features/kvparse_rules.feature"
BINDINGS = "features/kvparse_rules.pack.validated-input.yaml"
DEFAULT = "Record { has_a: false, a: 0, has_b: false, b: 0 }"
RUN = "./run.sh --no-unit --quick --no-adequacy --no-heldout"

# (id, what, [(old, new)]): each `old` must occur exactly once in kvparse/src/lib.rs when it is applied (in order)
MUTANTS = [
    ("B1", "trailing garbage accepted: after a field, a byte that is not `;` ends the record instead of rejecting it",
     [("        } else if inp[i] != b';' {\n            return None;\n", "        } else if inp[i] != b';' {\n            more = false;\n")]),
    ("B2", "unknown item skipped: a field with a key that is neither `a` nor `b` is passed over instead of rejected",
     [("    } else {\n        false\n    }\n}", "    } else {\n        true\n    }\n}")]),
    ("B3", "duplicate key, last wins: a repeated key is accepted and its last value kept",
     [("        if r.has_b {\n            return false;\n        }\n        r.has_b = true;", "        r.has_b = true;"),
      ("        if r.has_a || r.has_b {\n            return false;\n        }", "        if r.has_b {\n            return false;\n        }")]),
    ("B4", "case mismatch: the keys `A` and `B` are taken for `a` and `b`",
     [("    if k == b'a' {", "    if k == b'a' || k == b'A' {"), ("    } else if k == b'b' {", "    } else if k == b'b' || k == b'B' {")]),
    ("B5a", "length off by one: an input of exactly the limit is rejected",
     [("        if inp.len() > self.limit {", "        if inp.len() >= self.limit {")]),
    ("B5b", "length off by one: an input one byte longer than the limit is accepted",
     [("        if inp.len() > self.limit {", "        if inp.len() > self.limit && inp.len() - self.limit > 1 {")]),
    ("B6", "default value returned: a record is accepted and the default record is answered (= T-default of the adequacy expectation)",
     [("    Some(r)\n}", f"    Some({DEFAULT})\n}}")]),
    ("T-reject-all", "trivial implementation: rejects every input",
     [("        record(inp)\n    }", "        let _ = record(inp);\n        None\n    }")]),
    ("T-accept-all", "trivial implementation: accepts every input with one fixed value",
     [("        if inp.len() > self.limit {\n            return None;\n        }\n        record(inp)\n    }",
       f"        let _ = record(inp);\n        Some({DEFAULT})\n    }}")]),
]
# what the frozen pack expects to show each one false (pack.yaml `by:`), for the report
BY = {"B1": ["VI-2", "VI-7b", "VI-10"], "B2": ["VI-8", "VI-2", "VI-10"], "B3": ["VI-9", "VI-2", "VI-7b", "VI-10"],
      "B4": ["VI-8", "VI-2", "VI-10"], "B5a": ["VI-3"], "B5b": ["VI-4"], "B6": ["VI-7b", "VI-10"],
      "T-reject-all": ["VI-3"], "T-accept-all": ["VI-2"]}
FALSE = ("REFUTED",)


def sh(cmd, cwd, timeout=3600):
    r = subprocess.run('export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"; ' + cmd, cwd=cwd, shell=True, capture_output=True,
                       text=True, timeout=timeout, executable="/bin/bash")
    return r.returncode, r.stdout + r.stderr


def codes(work: Path) -> dict:
    p = work / "out/graph.json"
    return {v["node"]: v["code"] for v in json.loads(p.read_text())["verdicts"]} if p.exists() else {}


def member(node: str) -> str | None:
    pre = "group:rule:Rule.kvparse_rules.vi_"
    return "VI-" + node[len(pre):] if node.startswith(pre) else None


def where_false(text: str) -> dict:
    """Member -> where the rule is false, from the per-Rule blocks of a printed report (its lines are wrapped: the text of
    each block is put back on one line first)."""
    import re
    out = {}
    for blk in re.split(r"\n(?=Rule: )", text):
        m = re.search(r"@pack-rule:(\S+)", blk.split("\n", 1)[0])
        if not m:
            continue
        flat = " ".join(blk.split())
        w = re.search(r"it is FALSE at (\{.*?\})(, on the compiled Rust too \(reproduced\))?", flat)
        if w:
            out[m.group(1)] = w.group(1) + (w.group(2) or ", NOT reproduced on the compiled Rust")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--resummarise", action="store_true", help="write the .md again from the stored .json; runs nothing")
    a = ap.parse_args()
    if a.resummarise:
        # `where` is read again from the logs of the run, if they are still there (build/k1-mutants/logs/)
        stored = json.loads((HERE / "results" / "kvparse_mutants.json").read_text())
        for i in stored["items"]:
            log = ROOT / "build" / "k1-mutants" / "logs" / f"{i['id']}.log"
            if log.exists():
                i["where"] = {m: l for m, l in where_false(log.read_text()).items() if m in i["shown_false_by"] + i["counterexample_unconfirmed"]}
        (HERE / "results" / "kvparse_mutants.json").write_text(json.dumps(stored, indent=1, ensure_ascii=False) + "\n")
        (HERE / "results" / "kvparse_mutants.md").write_text(markdown(json.loads((HERE / "results" / "kvparse_mutants.json").read_text())))
        print("wrote packs/validated-input/results/kvparse_mutants.md from the stored .json")
        return 0
    only = set(a.only.split(",")) if a.only else None
    work = ROOT / "build" / "k1-mutants" / "work"
    logs = ROOT / "build" / "k1-mutants" / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    res = {"command": RUN, "started": time.strftime("%Y-%m-%d %H:%M:%S"), "items": []}

    def fresh():
        rc, out = sh(f"mutation/workcopy.sh '{work}'", ROOT)
        if rc:
            raise RuntimeError(out)

    def run(name):
        t = time.time()
        rc, out = sh(RUN, work)
        (logs / f"{name}.log").write_text(out)
        return rc, out, round(time.time() - t)

    fresh()
    rc, out, secs = run("baseline")
    base = codes(work)
    res["baseline"] = {"exit": rc, "seconds": secs, "verdicts": len(base),
                       "pack_rules": {member(k): v for k, v in sorted(base.items()) if member(k)}, "tail": out[-300:]}
    print(f"baseline: exit {rc}, {len(base)} verdicts, {secs} s; pack rules: {res['baseline']['pack_rules']}", flush=True)
    if rc or not base:
        print(out[-3000:])
        return 1

    if only is None or "strip" in only:
        fresh()
        rc0, o0 = sh(f"python3 -m clausal pack strip {FEATURE}", work)
        shutil.rmtree(work / "packs")
        (work / "clausal" / "pack.py").unlink()
        (work / BINDINGS).unlink()
        left = sh(f"grep -rl '@pack' features packs clausal/pack.py {BINDINGS} 2>/dev/null; ls packs clausal/pack.py {BINDINGS} 2>&1 | head -5", work)[1]
        rc, out, secs = run("strip")
        got = codes(work)
        diff = {k: [base.get(k), got.get(k)] for k in sorted(set(base) | set(got)) if base.get(k) != got.get(k)}
        res["strip"] = {"strip_exit": rc0, "strip_output": o0.strip(), "what_is_left": left.strip(), "exit": rc, "seconds": secs,
                        "verdicts": len(got), "differ": diff}
        print(f"strip: exit {rc}, {len(got)} verdicts, verdict codes that differ from the baseline: {len(diff)} of {len(set(base) | set(got))}", flush=True)

    for id_, what, subs in MUTANTS:
        if only is not None and id_ not in only:
            continue
        fresh()
        lib = work / LIB
        s = lib.read_text()
        for old, new in subs:
            assert s.count(old) == 1, f"{id_}: pattern occurs {s.count(old)} times: {old!r}"
            s = s.replace(old, new)
        lib.write_text(s)
        urc, uout = sh("cd kvparse && cargo test --quiet", work)
        compiles = "error[" not in uout and "could not compile" not in uout
        rc, out, secs = run(id_)
        got = codes(work)
        translated = "wrote lean/Generated/Wallet.lean" in out or "lean/Generated/Kvparse.lean" in out
        changed = {k: [base.get(k), got.get(k)] for k in sorted(set(base) | set(got)) if base.get(k) != got.get(k)}
        pack_changed = {member(k): v for k, v in changed.items() if member(k)}
        false = sorted((m for m, (b, g) in pack_changed.items() if g in FALSE and b not in FALSE), key=lambda m: (len(m), m))
        cex = sorted(m for m, (b, g) in pack_changed.items() if g == "COUNTEREXAMPLE")
        lost = sorted(m for m, (b, g) in pack_changed.items() if (b or "").startswith("PROVED") and g not in FALSE and g != "COUNTEREXAMPLE")
        item = {"id": id_, "what": what, "expected_by": BY[id_], "compiles": compiles, "translated": translated,
                "unit_tests": "caught" if urc else "MISSED", "exit": rc, "seconds": secs, "verdicts": len(got),
                "shown_false_by": false, "counterexample_unconfirmed": cex, "proof_lost": lost,
                "other_verdicts_changed": {k: v for k, v in changed.items() if not member(k)},
                "where": {m: l for m, l in where_false(out).items() if m in false + cex}}
        res["items"].append(item)
        print(f"{id_}: compiles {compiles}, unit tests {item['unit_tests']}, exit {rc}, {secs} s; SHOWN FALSE BY {false or 'NO PACK RULE'}"
              + (f"; counterexample not confirmed in the kernel: {cex}" if cex else "") + (f"; proof lost: {lost}" if lost else "")
              + (f"; other verdicts changed: {item['other_verdicts_changed']}" if item["other_verdicts_changed"] else ""), flush=True)
    if not a.keep:
        shutil.rmtree(work, ignore_errors=True)
    if only is None:
        out_dir = HERE / "results"
        out_dir.mkdir(exist_ok=True)
        (out_dir / "kvparse_mutants.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
        (out_dir / "kvparse_mutants.md").write_text(markdown(res))
        print(f"wrote {out_dir.relative_to(ROOT)}/kvparse_mutants.json and .md")
    return 0


def markdown(res: dict) -> str:
    def without(xs, drop):
        return [x for x in xs if x not in drop]

    def order(xs):
        return sorted(xs, key=lambda m: (len(m.rstrip("ab")), m))

    def cell(xs):
        return ", ".join(order(xs)) or "**NONE**"
    L = ["# K1: seeded bugs and trivial implementations against the pack's rules on kvparse", "",
         f"Written by `packs/validated-input/kvparse_mutants.py` ({res['started']}). Each row is one pipeline run in a scratch copy: `{res['command']}`.",
         "The kvparse rules are examined by the grid search on the Lean model and the same grid on the compiled Rust only (240 inputs:",
         "8 size limits x 30 messages, written by the builder, who knew the bug list). No generated property test or bounded check looks at them.", "",
         "Two columns, and they are not the same thing:", "",
         "- **REFUTED** is the frozen criterion (`FREEZE.md`): the rule's verdict on the mutant is REFUTED, a counterexample confirmed by a",
         "  kernel-checked theorem.",
         "- **COUNTEREXAMPLE** is the verdict `COUNTEREXAMPLE FOUND (not confirmed in the kernel)`: the rule's reading is false at a grid input on",
         "  the Lean model, and false at the same input on the compiled Rust. `mutation/run_mutants.py` counts both verdicts as shown false.", "",
         f"Baseline: exit {res['baseline']['exit']}, {res['baseline']['verdicts']} verdicts; pack rules: "
         + ", ".join(f"{k} {v}" for k, v in sorted(res["baseline"]["pack_rules"].items(), key=lambda kv: (len(kv[0].rstrip('ab')), kv[0]))), ""]
    if "strip" in res:
        s = res["strip"]
        L += [f"**Strip test**: `packs/`, `clausal/pack.py` and the bindings file deleted, `@pack` tags stripped: exit {s['exit']}, "
              f"{s['verdicts']} verdicts, **{len(s['differ'])} verdict codes differ from the baseline**."
              + ("" if not s["differ"] else " " + json.dumps(s["differ"])), ""]
    L += ["| Mutant | What | Unit tests | REFUTED (frozen criterion) | COUNTEREXAMPLE, not confirmed in the kernel | Expected by the pack | Proof lost |",
          "|---|---|---|---|---|---|---|"]
    for i in res["items"]:
        L.append(f"| {i['id']} | {i['what']} | {i['unit_tests']} | {cell(i['shown_false_by'])} | {cell(i['counterexample_unconfirmed'])} | "
                 f"{', '.join(i['expected_by'])} | {', '.join(order(i['proof_lost'])) or '–'} |")
    L += ["", "Either verdict (REFUTED or COUNTEREXAMPLE), with the members that pin the value or use the specification's parser left out:", "",
          "| Mutant | Any pack rule | Without VI-10 | Without VI-10, VI-7b | Without VI-10, VI-7b and the rules that use the well-formed word (VI-2, VI-3, VI-6) |",
          "|---|---|---|---|---|"]
    for i in res["items"]:
        f = i["shown_false_by"] + i["counterexample_unconfirmed"]
        L.append(f"| {i['id']} | {cell(f)} | {cell(without(f, ['VI-10']))} | {cell(without(f, ['VI-10', 'VI-7b']))} | "
                 f"{cell(without(f, ['VI-10', 'VI-7b', 'VI-2', 'VI-3', 'VI-6']))} |")
    n = len(res["items"])
    ref = [i["id"] for i in res["items"] if i["shown_false_by"]]
    either = [i["id"] for i in res["items"] if i["shown_false_by"] or i["counterexample_unconfirmed"]]
    L += ["", f"By the frozen criterion (REFUTED): {len(ref)} of {n} mutants are shown false by a pack rule"
          + (f" ({', '.join(ref)})" if ref else "") + f"; not: {', '.join(i['id'] for i in res['items'] if not i['shown_false_by']) or 'none'}.",
          f"By either verdict: {len(either)} of {n}; not: {', '.join(i['id'] for i in res['items'] if i['id'] not in either) or 'none'}.", "",
          "Where each is false (the grid input the rule's block names; `the_parser` is the size limit):", ""]
    for i in res["items"]:
        L.append(f"- {i['id']}: " + "; ".join(f"{m} at `{i['where'][m]}`" for m in order(i["where"])))
    other = {i["id"]: i["other_verdicts_changed"] for i in res["items"] if i["other_verdicts_changed"]}
    L += ["", "Verdicts of other projects that changed on a mutant: " + (json.dumps(other) if other else "none") + "."]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    sys.exit(main())
