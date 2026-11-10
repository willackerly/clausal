"""slicegen pipeline: commands gen / proofs / derive / adequacy / report / rules / steps / review."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from . import adequacy, emit
from .core import Bound, FeatureError, Problem, bind, load_glossary, parse_feature

ROOT = Path(__file__).resolve().parent.parent
LEAN = ROOT / "lean"
OUT = ROOT / "out"

PROOF_STUB = """/-
Proof of the scenario statement `{id}.stmt` (lean/Spec/Statements.lean).

Hand-written (by a person or an agent). slicegen created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `{id}`
and its type must be exactly `{id}.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Straight-line code: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped that way. Helper lemmas may go in
modules of their own under lean/Lemmas/ (library `Lemmas`), imported from here.
-/
import Spec.Statements{extra_imports}
open Aeneas Aeneas.Std Result

/-- {where}  {name} -/
theorem {id} : {id}.stmt := by
  sorry
"""


def proof_module(id_: str) -> str:
    """Spec.<feature>.<scenario> -> Spec.Proofs.<feature>.<scenario> (one Lean module per scenario)."""
    return "Spec.Proofs." + id_.split(".", 1)[1]


def proof_path(id_: str) -> Path:
    return LEAN.joinpath(*proof_module(id_).split(".")).with_suffix(".lean")


def wants_proof(b) -> bool:
    # no proof is wanted for a scenario expected to be false or vacuous
    return b.sc.expect not in ("REFUTED", "VACUOUS", "COUNTEREXAMPLE")


def crates() -> list:
    """The Rust crates under test, in translation order (../crates.txt, one directory name per line)."""
    p = ROOT / "crates.txt"
    return [l.strip() for l in p.read_text().splitlines() if l.strip() and not l.startswith("#")] if p.exists() else []


def spec_digest() -> str:
    """One hash over everything a mutation run depends on: the Rust crates, the features, the glossary
    (both readings), the hand-written lemmas and proofs. A mutation run's results.json records it; the report
    uses it to say whether those results belong to the current tree."""
    import hashlib
    h = hashlib.sha256()
    files = ([ROOT / c / "src" / "lib.rs" for c in crates()] + [ROOT / "glossary.yaml"]
             + sorted((LEAN / "Vocab").rglob("*.lean"))
             + [ROOT / "bdd" / "src" / "lib.rs", ROOT / "bdd" / "tests" / "bdd.rs"]
             + sorted((LEAN / "Lemmas").rglob("*.lean"))
             + sorted((ROOT / "features").glob("*.feature")) + sorted((LEAN / "Spec" / "Proofs").rglob("*.lean")))
    for f in files:
        h.update(str(f.relative_to(ROOT)).encode() + b"\0" + f.read_bytes() + b"\0")
    return h.hexdigest()


def proofs_state(st) -> dict:
    """out/proofs.json (written by `slicegen proofs`): which proof modules compiled in this run."""
    p = OUT / "proofs.json"
    if p.exists():
        return json.loads(p.read_text())
    mods = [proof_module(b.id) for b in st.bounds if proof_path(b.id).exists()]
    return {"build_ok": True, "built": mods, "failed": [], "errors": {}}


class State:
    def __init__(self):
        self.gloss = load_glossary(ROOT / "glossary.yaml", "glossary.yaml")
        paths = sorted((ROOT / "features").glob("*.feature"), key=lambda p: p.name)
        self.features = [parse_feature(p, f"features/{p.name}") for p in paths]
        self.translation = json.loads((LEAN / "translation.json").read_text())
        self.model_fns = {f["lean_name"]: f for f in self.translation["functions"]}
        for e in self.gloss.entries:
            if e.kind == "when":
                fn = self.model_fns.get(e.call)
                if fn is None:
                    raise FeatureError(f"glossary.yaml: {e.id}: `call: {e.call}` is not a function in lean/translation.json; "
                                       "a When must point at Aeneas-generated code")
                if fn["rust_name"] != e.rust_fn:
                    raise FeatureError(f"glossary.yaml: {e.id}: rust_fn `{e.rust_fn}` != translation.json `{fn['rust_name']}`")
            elif e.lean in self.model_fns:
                raise FeatureError(f"glossary.yaml: {e.id}: a Given/Then may not be bound to a model function")
        self.triv = adequacy.trivial_models(self.gloss)     # model function -> trivial models (suite adequacy note)
        self.results = []          # [(Scenario, Bound | Problem)]
        seen = {}
        for f in self.features:
            for sc in f.scenarios:
                if sc.id in seen:
                    raise FeatureError(f"{f.path}:{sc.line}: duplicate scenario id {sc.id} (also {seen[sc.id]})")
                seen[sc.id] = f"{f.path}:{sc.line}"
                self.results.append((sc, bind(sc, self.gloss)))

    @property
    def bounds(self):
        return [r for _, r in self.results if isinstance(r, Bound)]


def cmd_gen(st: State) -> int:
    (LEAN / "Spec").mkdir(exist_ok=True)
    (LEAN / "Run").mkdir(exist_ok=True)
    (ROOT / "build").mkdir(exist_ok=True)
    (LEAN / "Spec" / "Statements.lean").write_text(emit.statements_file(st.bounds))
    (LEAN / "Spec" / "Checks.lean").write_text(emit.checks_file(st.bounds))
    (LEAN / "Run" / "Search.lean").write_text(emit.search_file(st.bounds))
    (ROOT / "build" / "phrase_grid.tsv").write_text(emit.phrase_grid_tsv(st.gloss))
    (LEAN / "Run" / "Adequacy.lean").write_text(adequacy.search_file(st.bounds, st.triv))
    added, wanted = [], set()
    for b in st.bounds:
        if not wants_proof(b):
            continue
        p = proof_path(b.id)
        wanted.add(p)
        if not p.exists():         # a proof file is created once and never edited by the generator
            p.parent.mkdir(parents=True, exist_ok=True)
            extra = "".join(f"\nimport {m}" for m in st.gloss.raw.get("audit_imports", [])
                            if any(c.split(".")[0] == m.split(".")[0].lower() for c in b.calls))
            p.write_text(PROOF_STUB.format(id=b.id, where=f"{b.sc.feature.path}:{b.sc.line}", name=b.sc.name,
                                           extra_imports=extra))
            added.append(b.id)
    orphans = [p for p in sorted((LEAN / "Spec" / "Proofs").rglob("*.lean")) if p not in wanted]
    nrules = sum(len(f.rules) for f in st.features)
    print(f"slicegen gen: {len(st.results)} scenarios under {nrules} Rules, {len(st.bounds)} bound to statements; "
          f"suite adequacy note: {sum(len(t) for t in st.triv.values())} trivial models of {len(st.triv)} operations, "
          f"{len(adequacy.pairs(st.bounds, st.triv))} (scenario, trivial model) pairs")
    for sc, r in st.results:
        if isinstance(r, Problem):
            print(f"  {r.status}  {sc.feature.path}:{r.line}: {r.message}")
    for f in st.features:
        for r in f.rules:
            if not r.scenarios:
                print(f"  NOTE  {f.path}:{r.line}: Rule \"{r.name}\" has no scenario beneath it: nothing is stated or proved for it")
    for a in added:
        print(f"  created proof stub: {proof_path(a).relative_to(ROOT)}")
    for o in orphans:
        print(f"  ORPHAN proof file (no scenario wants it; not counted): {o.relative_to(ROOT)}")
    return 0


def cmd_proofs(st: State, argv) -> int:
    """Read out/proofs.log (output of `lake build`) and record which proof modules compiled."""
    rc = int(argv[0]) if argv else 0
    log = (OUT / "proofs.log").read_text() if (OUT / "proofs.log").exists() else ""
    mods = {proof_module(b.id): b.id for b in st.bounds if wants_proof(b)}
    failed, errors, libs = [], {}, []
    if rc != 0:
        named = set(re.findall(r"^- (\S+)$", log, re.M)) | set(re.findall(r"^✖ \[\d+/\d+\] \w+ (\S+)", log, re.M))
        failed = [m for m in mods if m in named]
        # a hand-written module failed: everything that imports it, directly or not, was not built either
        # (lake names only the module whose own text failed)
        broken = {n for n in named if not n.startswith("Spec.Proofs.")}

        def cause(module, seen=()):
            """A broken module that `module` depends on (through local modules), or None."""
            src = LEAN.joinpath(*module.split(".")).with_suffix(".lean")
            if module in seen or not src.exists():
                return None
            for dep in re.findall(r"^import (\S+)$", src.read_text(), re.M):
                if dep in broken:
                    return dep
                via = cause(dep, seen + (module,))
                if via:
                    return via
            return None
        for m in mods:
            c = cause(m)
            if m not in failed and c:
                failed.append(m)
                errors[m] = f"it depends on {c}, which does not compile (see out/proofs.log)"
        libs = sorted(broken | {m for m in st.gloss.raw.get("audit_imports", []) if cause(m)})
        if not named:
            failed = list(mods)    # the build failed and we cannot say where: count no proof at all
        for m in failed:
            if m in errors:
                continue
            path = "/".join(m.split(".")) + ".lean"
            hit = re.search(rf"^error: {re.escape(path)}:(\d+):\d+: (.*)$", log, re.M)
            errors[m] = f"{path}:{hit.group(1)}: {hit.group(2)[:160]}" if hit else "see out/proofs.log"
    built = [m for m in mods if m not in failed]
    (OUT / "proofs.json").write_text(json.dumps({"build_ok": rc == 0, "built": built, "failed": failed, "errors": errors,
                                                 "failed_libs": sorted(libs)}, indent=2))
    for lib in sorted(libs):
        print(f"  DOES NOT COMPILE: {lib} (a hand-written library; every proof that imports it is lost)")
    nsorry = len(re.findall(r"declaration uses .sorry.", log))
    print(f"proof modules: {len(built)} compiled, {len(failed)} FAILED; declarations still using sorry: {nsorry}")
    for m in failed:
        print(f"  DOES NOT COMPILE: {m}  ({errors[m]})")
    return 0


def parse_search(st: State) -> dict:
    """out/search.log -> {id: {tried, sat, bad, rows}} with grid indexes mapped back to values."""
    res = {b.id: {"tried": 0, "sat": None, "bad": None, "rows": []} for b in st.bounds}
    by_id = {b.id: b for b in st.bounds}
    log = (OUT / "search.log").read_text()

    def values(b, idx_text):
        idx = [int(x) for x in re.findall(r"\d+", idx_text)]
        vars_ = emit.search_vars(b)
        return {n: emit.grid_values(b, t)[i] for (n, t), i in zip(vars_, idx)}

    seen_search = set()
    for line in log.splitlines():
        p = line.split("\t")
        if p[0] == "ROW":
            _, id_, n, check, gbits, tbits, ret = p
            b = by_id[id_]
            src = b.sc.rows[int(n) - 1] if b.sc.outline else (b.sc.line, [])
            res[id_]["rows"].append({"n": int(n), "line": src[0], "cells": dict(zip(b.sc.header, src[1])),
                                     "check": check, "givens": gbits, "thens": tbits, "returned": ret})
        elif p[0] == "PHRASE":
            res.setdefault("__phrases__", {})[p[1]] = p[2]
        elif p[0] == "SEARCH":
            _, id_, tried, sat, bidx, bcheck, bthens, bret = p
            b = by_id[id_]
            seen_search.add(id_)
            res[id_]["tried"] = int(tried)
            if sat != "-":
                res[id_]["sat"] = values(b, sat)
            if bidx != "-":
                res[id_]["bad"] = {"values": values(b, bidx), "check": bcheck, "thens": bthens, "returned": bret}
    missing = set(by_id) - seen_search
    if missing:
        raise FeatureError(f"out/search.log has no SEARCH line for: {sorted(missing)} (did Run/Search.lean fail?)")
    return res


def cmd_derive(st: State) -> int:
    search = parse_search(st)
    (OUT / "search.json").write_text(json.dumps(search, indent=2))
    ps = proofs_state(st)
    mods = {b.id: proof_module(b.id) for b in st.bounds if wants_proof(b) and proof_module(b.id) in ps["built"]}
    extra = [m for m in st.gloss.raw.get("audit_imports", []) if m not in ps.get("failed_libs", [])]
    (LEAN / "Run" / "Audit.lean").write_text(emit.audit_file(st.bounds, search, list(st.model_fns), mods, extra))
    replay = ROOT / "build" / "replay"
    if replay.exists():
        for f in replay.glob("*.feature"):
            f.unlink()
    text = emit.replay_feature(st.bounds, search)
    if text:
        replay.mkdir(parents=True, exist_ok=True)
        (replay / "replay.feature").write_text(text)
    for b in st.bounds:
        s = search[b.id]
        print(f"  {b.id}: {s['tried']} grid points; Givens satisfiable: {'yes' if s['sat'] is not None else 'NO INPUT FOUND'}; "
              f"counterexample: {s['bad']['values'] if s['bad'] else 'none'}")
    return 0


def adequacy_search(st: State):
    """out/adequacy.log -> results per (scenario, trivial model) pair; ({} , why) if the search did not run or did not finish."""
    p = OUT / "adequacy.log"
    if not p.exists():
        return {}, "the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed)"
    res = adequacy.parse_search(p.read_text(), st.bounds, st.triv)
    want = len(adequacy.pairs(st.bounds, st.triv))
    if not want:
        return {}, "the glossary has no `trivial` section, so no trivial model was generated"
    if not res:
        return {}, "the adequacy search produced no result (see out/adequacy.log)"
    return res, ("" if len(res) == want else f"the adequacy search reported {len(res)} of {want} pairs (see out/adequacy.log)")


def cmd_adequacy(st: State) -> int:
    """After the adequacy search: write Run/AdequacyAudit.lean (kernel attempts for what the search found).
    Informational: always exits 0."""
    res, why = adequacy_search(st)
    if not res:
        print(f"  suite adequacy note: {why}")
        return 0
    text, names = adequacy.audit_file(st.bounds, st.triv, res)
    (LEAN / "Run" / "AdequacyAudit.lean").write_text(text)
    bad = sum(1 for r in res.values() if r["bad"] is not None)
    print(f"  suite adequacy note: {len(res)} (scenario, trivial model) pairs searched; the scenario is false of the trivial model "
          f"at some grid input for {bad}, no such input for {len(res) - bad}; {len(names)} kernel attempts generated"
          + (f"  [{why}]" if why else ""))
    return 0


def main(argv) -> int:
    if not argv:
        print(__import__("slicegen.__main__").__main__.__doc__)
        return 2
    if argv[0] == "rules":             # reads a stored graph only: no features, no glossary, no Lean
        from . import rules
        return rules.main(argv[1:])
    try:
        st = State()
        if argv[0] == "gen":
            return cmd_gen(st)
        if argv[0] == "derive":
            return cmd_derive(st)
        if argv[0] == "proofs":
            return cmd_proofs(st, argv[1:])
        if argv[0] == "adequacy":
            return cmd_adequacy(st)
        from . import report
        if argv[0] == "report":
            return report.cmd_report(st, argv[1:])
        if argv[0] == "steps":
            return report.cmd_steps(st)
        if argv[0] == "review":
            return report.cmd_review(st, argv[1:])
    except FeatureError as e:
        print(f"slicegen: {e}", file=sys.stderr)
        return 1
    print(f"unknown command {argv[0]}", file=sys.stderr)
    return 2
