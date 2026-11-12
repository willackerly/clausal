"""clausal pipeline: commands gen / proofs / derive / adequacy / report / rules / steps / review."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from . import adequacy, emit, evgen, evidence, links, narrowing, oblig, rsearch, trees, vocab
from .core import Bound, FeatureError, Problem, bind, load_glossary, parse_feature

ROOT = Path(__file__).resolve().parent.parent
LEAN = ROOT / "lean"
OUT = ROOT / "out"

PROOF_STUB = """/-
Proof of the scenario statement `{id}.stmt` (lean/Wallet/Statements.lean).

Hand-written (by a person or an agent). clausal created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `{id}`
and its type must be exactly `{id}.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Usual recipe: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped: use its hand-proved `@[step]` lemma
(lean/Ledger/Lemmas/), which carries the loop invariant.
-/
import Wallet.Statements{extra_imports}
open Aeneas Aeneas.Std Result

/-- {where}  {name} -/
theorem {id} : {id}.stmt := by
  sorry
"""


OBLIGATION_STUB = """/-
Proof of the flat proof obligation `{id}.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the Clausebook pieces of this NEW sentence:

{text}

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The theorem must be named exactly `{id}` and its type must be exactly
`{id}.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`{id}.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
makes the sentence PROVED-FOR-ALL; while it is `sorry` the sentence is TESTED-ONLY.

Usual recipe: `intro` the variables and hypotheses, get what the call returns from the hand-proved step lemma
of the model function (`Bdd.ok_of_spec (ledger.Ledger.apply.spec st inp)`; lean/Ledger/Lemmas/), then
`refine ⟨_, _, e, ?_⟩` and arithmetic. For a straight-line function: `unfold` it and `step*`.
-/
import Wallet.Obligations{extra_imports}
open Aeneas Aeneas.Std Result

/-- {where} -/
theorem {id} : {id}.obligation := by
  sorry
"""


def proof_module(id_: str) -> str:
    """Spec.<feature>.<scenario> -> Wallet.Proofs.<feature>.<scenario> (one Lean module per scenario)."""
    return "Wallet.Proofs." + id_.split(".", 1)[1]


def proof_path(id_: str) -> Path:
    return LEAN.joinpath(*proof_module(id_).split(".")).with_suffix(".lean")


def rule_proof_module(rule_id: str) -> str:
    """Rule.<feature>.<rule> -> Wallet.RuleProofs.<feature>.<rule>: a hand-written proof of a rule statement, where the
    generated glue from the scenarios does not go through. Optional; clausal never creates one."""
    return "Wallet.RuleProofs." + rule_id.split(".", 1)[1]


def rule_proof_path(rule_id: str) -> Path:
    return LEAN.joinpath(*rule_proof_module(rule_id).split(".")).with_suffix(".lean")


def wants_proof(b) -> bool:
    # no proof is wanted for a scenario expected to be false or vacuous
    return b.sc.expect not in ("REFUTED", "VACUOUS", "COUNTEREXAMPLE")


def spec_digest() -> str:
    """One hash over everything a mutation run depends on: the Rust crate, the features, the glossary
    (both readings) and the hand-written proofs. mutation/results.json records it; the report uses it
    to say whether those results belong to the current tree."""
    import hashlib
    h = hashlib.sha256()
    files = ([ROOT / "wallet" / "src" / "lib.rs", ROOT / "ledger" / "src" / "lib.rs", ROOT / "glossary.yaml", ROOT / vocab.BOOK_DIR / vocab.PROJECT_FILE]
             + [p for p, _ in vocab.project_books(ROOT)]
             + [
              LEAN / "Wallet" / "Vocab.lean", LEAN / "Wallet" / "Pieces.lean",
              ROOT / "wallet-bdd" / "src" / "lib.rs", ROOT / "wallet-bdd" / "src" / "pieces.rs", ROOT / "wallet-bdd" / "tests" / "bdd.rs",
              ROOT / "wallet-bdd" / "tests" / "grid.rs"]
             + sorted((LEAN / "Ledger").rglob("*.lean")) + sorted((LEAN / "Frames").rglob("*.lean"))
             + sorted((ROOT / "features").glob("*.feature")) + sorted((ROOT / "controls").glob("*.feature"))
             + sorted((LEAN / "Wallet" / "Proofs").rglob("*.lean"))
             + sorted((LEAN / "Wallet" / "RuleProofs").rglob("*.lean")))
    for f in files:
        h.update(str(f.relative_to(ROOT)).encode() + b"\0" + f.read_bytes() + b"\0")
    return h.hexdigest()


def proofs_state(st) -> dict:
    """out/proofs.json (written by `clausal proofs`): which proof modules compiled in this run."""
    p = OUT / "proofs.json"
    if p.exists():
        return json.loads(p.read_text())
    mods = [proof_module(b.id) for b in st.bounds if proof_path(b.id).exists()]
    mods += [proof_module(sc.id) for sc, _ in st.new_scenarios if proof_path(sc.id).exists()]
    mods += [rule_proof_module(r.id) for r, _ in st.rules if rule_proof_path(r.id).exists()]
    return {"build_ok": True, "built": mods, "failed": [], "errors": {}}


class State:
    def __init__(self):
        self.gloss = load_glossary(ROOT / "glossary.yaml", "glossary.yaml")
        order = ["wallet.feature", "ledger.feature"]
        paths = sorted((ROOT / "features").glob("*.feature"),
                       key=lambda p: (order.index(p.name) if p.name in order else len(order), p.name))
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
        # THE COMPOSABLE CLAUSEBOOK (plan nodes V2, V3): every scenario and every Rule line compiled from typed pieces.
        # `results` above is the OLD whole-phrase binding; it is kept as the flat statement the proofs, the search and the
        # refutations are about, and each reading is proved equivalent to it (clausal/links.py).
        self.voc = vocab.load_project(ROOT, self.gloss)
        comp = vocab.Compiler(self.voc)
        self.readings = {sc.id: comp.scenario(sc) for sc, _ in self.results}       # scenario id -> Reading | Problem
        self.rules = []                                                             # [(Rule, Reading | Problem)]
        for f in self.features:
            for r in f.rules:
                hint = next((self.readings[sc.id].info["ops"][0]["domain"] for sc in r.scenarios
                             if isinstance(self.readings.get(sc.id), vocab.Reading)), None)
                self.rules.append((r, comp.rule(r, hint)))

    def narrowing_controls(self) -> list:
        """controls/*.feature (plan nodes Q1, Q2): each Rule line compiled with the refusal of vacuous narrowed claims and
        without it. [{rule, on, off}]. Not fixtures: no verdict; lean/Run/Narrowing.lean asks the kernel about them."""
        on, off = vocab.Compiler(self.voc), vocab.Compiler(self.voc, refuse_vacuous=False)
        out = []
        for p in sorted((ROOT / "controls").glob("*.feature")):
            f = parse_feature(p, f"controls/{p.name}")
            out += [{"rule": r, "on": on.rule(r, None), "off": off.rule(r, None)} for r in f.rules]
        return out

    @property
    def new_scenarios(self):
        """[(Scenario, Reading)]: NEW sentences. The composable Clausebook reads the scenario; the old whole-phrase glossary
        has no flat statement for it. Its verdict comes from the reading alone: flat obligation generated from the pieces
        (clausal/oblig.py), proof supplied or not, search and refutation through the reading."""
        return [(sc, self.readings[sc.id]) for sc, r in self.results
                if isinstance(r, Problem) and isinstance(self.readings[sc.id], vocab.Reading)]

    @property
    def with_obligation(self):
        """Every reading a flat proof obligation is generated for: the new scenarios, and every Rule line."""
        return [rd for _, rd in self.new_scenarios] + [rd for _, rd in self.rules if isinstance(rd, vocab.Reading)]

    def rule_wants_stub(self, rule, rd) -> bool:
        """A Rule line gets a proof stub of its own when nothing beneath it could prove it: it compiles, it is expected to
        hold, and no universal scenario beneath it is a usable part."""
        if not isinstance(rd, vocab.Reading) or any(t in rule.tags for t in ("@expect-refuted", "@expect-unbound", "@expect-unproved")):
            return False
        return not [p for p in self.rule_parts(rule) if links.usable_part(p)]

    @property
    def bounds(self):
        return [r for _, r in self.results if isinstance(r, Bound)]

    @property
    def link_pairs(self):
        """[(Reading, Bound)]: scenarios that have both a compiled reading and a flat statement."""
        return [(self.readings[sc.id], r) for sc, r in self.results
                if isinstance(r, Bound) and isinstance(self.readings[sc.id], vocab.Reading)]

    @property
    def compiled(self):
        """[(Reading, Bound | None)]: every compiled reading, scenarios first, then Rule lines."""
        out = [(self.readings[sc.id], r if isinstance(r, Bound) else None) for sc, r in self.results
               if isinstance(self.readings[sc.id], vocab.Reading)]
        return out + [(rd, None) for _, rd in self.rules if isinstance(rd, vocab.Reading)]

    def rule_parts(self, rule) -> list:
        """The universal scenarios beneath a Rule that are meant to hold: the parts its statement is proved from."""
        return [self.readings[sc.id] for sc in rule.scenarios
                if sc.outline and not sc.expect and isinstance(self.readings.get(sc.id), vocab.Reading)]


def cmd_gen(st: State) -> int:
    (LEAN / "Wallet").mkdir(exist_ok=True)
    (LEAN / "Run").mkdir(exist_ok=True)
    (ROOT / "build").mkdir(exist_ok=True)
    (LEAN / "Wallet" / "Statements.lean").write_text(emit.statements_file(st.bounds))
    (LEAN / "Wallet" / "Checks.lean").write_text(emit.checks_file(st.bounds))
    (LEAN / "Run" / "Search.lean").write_text(emit.search_file(st.bounds))
    (ROOT / "build" / "phrase_grid.tsv").write_text(emit.phrase_grid_tsv(st.gloss))
    (LEAN / "Run" / "Adequacy.lean").write_text(adequacy.search_file(st.bounds, st.triv))
    (LEAN / "Wallet" / "Readings.lean").write_text(vocab.readings_file(st.voc, [rd for rd, _ in st.compiled]))
    (LEAN / "Wallet" / "Obligations.lean").write_text(oblig.obligations_file(st.voc, st.with_obligation))
    text, side = rsearch.search_file(st.voc, st.compiled, rows=[(rd, sc) for sc, rd in st.new_scenarios])
    (LEAN / "Run" / "ReadingSearch.lean").write_text(text)
    (ROOT / "build" / "rsearch_grid.json").write_text(rsearch.dump_side(side))
    # plan nodes Q1 and Q2: the questions about narrowed claims that are put to Lean on every run (clausal/narrowing.py)
    ntext, nside = narrowing.script(st.voc, [rd for rd, _ in st.compiled], st.narrowing_controls())
    (LEAN / "Run" / "Narrowing.lean").write_text(ntext)
    (ROOT / "build" / "narrowing.json").write_text(json.dumps(nside, indent=1, ensure_ascii=False))
    # the composition trees the Rust side evaluates: the generic cucumber steps and the grid comparison
    tr = trees.build(st, side)
    (ROOT / "build" / "trees.json").write_text(trees.dump(tr))
    # plan node E1: from the same trees, a property test and a bounded-checking harness per reading (evidence/)
    ev_info = evgen.write_all(ROOT, tr)
    added, wanted = [], set()
    lemma_imports = "".join(f"\nimport {m}" for m in st.gloss.raw.get("audit_imports", []))
    for sc, rd in st.new_scenarios:
        if sc.expect in ("REFUTED", "VACUOUS", "COUNTEREXAMPLE", "UNBOUND"):
            continue
        p = proof_path(sc.id)
        wanted.add(p)
        if not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(OBLIGATION_STUB.format(id=sc.id, where=f"{sc.feature.path}:{sc.line}  {sc.name}", extra_imports=lemma_imports,
                                                text="\n".join("    " + l for l in oblig.obligation_def(rd).split("\ndef ", 1)[1].splitlines())))
            added.append(sc.id)
    for r, rd in st.rules:
        if st.rule_wants_stub(r, rd) and not rule_proof_path(r.id).exists():
            p = rule_proof_path(r.id)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(OBLIGATION_STUB.format(id=r.id, where=f"{r.feature.path}:{r.line}  Rule: {r.name}", extra_imports=lemma_imports,
                                                text="\n".join("    " + l for l in oblig.obligation_def(rd).split("\ndef ", 1)[1].splitlines())))
            added.append(r.id)
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
    orphans = [p for p in sorted((LEAN / "Wallet" / "Proofs").rglob("*.lean")) if p not in wanted]
    nrules = sum(len(f.rules) for f in st.features)
    print(f"clausal gen: {len(st.results)} scenarios under {nrules} Rules, {len(st.bounds)} bound to statements; "
          f"suite adequacy note: {sum(len(t) for t in st.triv.values())} trivial models of {len(st.triv)} operations, "
          f"{len(adequacy.pairs(st.bounds, st.triv))} (scenario, trivial model) pairs")
    for sc, r in st.results:
        if isinstance(r, Problem):
            old_only = "(old glossary only; this sentence is read by the Clausebook) " if isinstance(st.readings.get(sc.id), vocab.Reading) else ""
            print(f"  {r.status}  {old_only}{sc.feature.path}:{r.line}: {r.message}")
    kinds = st.voc.kinds()
    nsc = sum(isinstance(x, vocab.Reading) for x in st.readings.values())
    nru = sum(isinstance(x, vocab.Reading) for _, x in st.rules)
    print(f"Clausebook: {kinds['domain']} domain words, {kinds['modifier']} modifiers, {kinds['frame']} frames, {len(st.voc.idioms)} idioms; "
          f"compiled {nsc} of {len(st.results)} scenarios and {nru} of {len(st.rules)} Rule lines to readings")
    for sc, _ in st.results:
        x = st.readings[sc.id]
        if isinstance(x, Problem):
            print(f"  {x.status}  (Clausebook) {x.message}")
    for r, x in st.rules:
        if isinstance(x, Problem):
            print(f"  {x.status}  (Clausebook, Rule line) {x.message}")
    rule_reading = {id(r): x for r, x in st.rules}
    for f in st.features:
        for r in f.rules:
            if not r.scenarios:
                tail = ("it has no Examples rows; the rule line itself is compiled, searched, run on the compiled Rust and given a verdict"
                        if isinstance(rule_reading.get(id(r)), vocab.Reading) else
                        "and the rule line did not compile, so nothing is stated or proved for it")
                print(f"  NOTE  {f.path}:{r.line}: Rule \"{r.name}\" has no scenario beneath it: {tail}")
    print(f"new sentences: {len(st.new_scenarios)} scenarios with no entry in the old glossary; flat proof obligations generated for them and for "
          f"{len(st.with_obligation) - len(st.new_scenarios)} Rule lines (lean/Wallet/Obligations.lean); "
          f"Rust side: {len(tr['steps'])} step forms and {len(tr['readings'])} readings as composition trees (build/trees.json), 0 hand-written steps")
    for x in tr["problems"]:
        print(f"  STEP FORM CLASH  {x}")
    for a in added:
        print(f"  created proof stub: {(proof_path(a) if a.startswith('Spec.') else rule_proof_path(a)).relative_to(ROOT)}")
    for o in orphans:
        print(f"  ORPHAN proof file (no scenario wants it; not counted): {o.relative_to(ROOT)}")
    return 0


def cmd_proofs(st: State, argv) -> int:
    """Read out/proofs.log (output of `lake build`) and record which proof modules compiled."""
    rc = int(argv[0]) if argv else 0
    log = (OUT / "proofs.log").read_text() if (OUT / "proofs.log").exists() else ""
    mods = {proof_module(b.id): b.id for b in st.bounds if wants_proof(b)}
    mods.update({proof_module(sc.id): sc.id for sc, _ in st.new_scenarios if proof_path(sc.id).exists()})
    mods.update({rule_proof_module(r.id): r.id for r, _ in st.rules if rule_proof_path(r.id).exists()})
    failed, errors, libs = [], {}, []
    if rc != 0:
        named = set(re.findall(r"^- (\S+)$", log, re.M)) | set(re.findall(r"^✖ \[\d+/\d+\] \w+ (\S+)", log, re.M))
        failed = [m for m in mods if m in named]
        # a hand-written module failed: everything that imports it, directly or not, was not built either
        # (lake names only the module whose own text failed)
        broken = {n for n in named if not n.startswith("Wallet.Proofs.") and not n.startswith("Wallet.RuleProofs.")}

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
    # FEED-BACK (plan node E1): a falsifying input a generated harness found on the compiled Rust, which fails as one more
    # row of the flat statement on the model, is that scenario's counterexample where the grid found none
    res["__fed_back__"] = evidence.feed_back_flat(evidence.load(), res, st)
    return res


def cmd_derive(st: State) -> int:
    search = parse_search(st)
    ps = proofs_state(st)
    mods = {b.id: proof_module(b.id) for b in st.bounds if wants_proof(b) and proof_module(b.id) in ps["built"]}
    extra = [m for m in st.gloss.raw.get("audit_imports", []) if m not in ps.get("failed_libs", [])]
    (OUT / "search.json").write_text(json.dumps(search, indent=2))
    (LEAN / "Run" / "Audit.lean").write_text(emit.audit_file(st.bounds, search, list(st.model_fns), mods, extra))
    # the compiled readings: NEW ↔ OLD, non-vacuity, each Rule against its scenarios (lean/Run/Links.lean)
    rs = {}
    if (OUT / "rsearch.log").exists():
        side = json.loads((ROOT / "build" / "rsearch_grid.json").read_text())
        rs = rsearch.parse((OUT / "rsearch.log").read_text(), side)
        # FEED-BACK (plan node E1): a falsifying input the generated harnesses found on the compiled Rust, which fails on
        # the model too, becomes the counterexample of its reading where the grid search found none
        fed = list(dict.fromkeys(evidence.feed_back(evidence.load(), rs) + [tuple(x) for x in search.get("__fed_back__", [])]))
        for id_, source in fed:
            print(f"  fed back: {id_} is false at an input found by the generated {source}; it fails on the Lean model too")
        (OUT / "rsearch.json").write_text(json.dumps(rs, indent=1, ensure_ascii=False))
        (OUT / "search.json").write_text(json.dumps(search, indent=2))
        (LEAN / "Run" / "Audit.lean").write_text(emit.audit_file(st.bounds, search, list(st.model_fns), mods, extra))
        text, meta = links.build(st, search, rs, side, ps, extra, mods)
        (LEAN / "Run" / "Links.lean").write_text(text)
        (ROOT / "build" / "links.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
        bad_rules = [k for k, v in rs.items() if k.startswith("Rule.") and v.get("bad")]
        print(f"  readings: {len(meta['iffs'])} equivalences NEW <-> OLD and {len(meta['sats'])} non-vacuity theorems generated; "
              f"{len(meta['imps'])} Rule statements with glue from their scenarios, {len(meta['nots'])} with a refutation; "
              f"the reading search found a counterexample to {len(bad_rules)} Rule statement(s)")
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


def cmd_witness(st: State) -> int:
    """After the generated harnesses ran: write lean/Run/Witness.lean (every falsifying input they found, on the model)."""
    ev = evidence.load()
    side = json.loads((ROOT / "build" / "rsearch_grid.json").read_text())
    text, meta = evidence.witness_file(st, ev, side)
    (LEAN / "Run" / "Witness.lean").write_text(text)
    (ROOT / "build" / "witness.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    (OUT / "evidence.json").write_text(json.dumps(ev, indent=1, ensure_ascii=False))      # with the reason where an input cannot be put to the model
    total = len(evidence.witness_list(ev))
    print(f"  {len(meta)} of {total} falsifying input(s) from the generated harnesses to evaluate on the Lean model (lean/Run/Witness.lean)"
          + ("" if len(meta) == total else f"; {total - len(meta)} cannot be written there (an account number above 4294967295)"))
    return 0


def cmd_witness_collect(st: State) -> int:
    """After lean/Run/Witness.lean ran: record in out/evidence.json what the model said at each falsifying input."""
    ev = evidence.load()
    if ev is None:
        return 0
    meta = json.loads((ROOT / "build" / "witness.json").read_text())
    log = (OUT / "witness.log").read_text() if (OUT / "witness.log").exists() else ""
    ev = evidence.parse_witness(log, meta, ev)
    (OUT / "evidence.json").write_text(json.dumps(ev, indent=1, ensure_ascii=False))
    ws = [w for _, _, w in evidence.witness_list(ev)]
    mm = [(i, w) for i, _, w in evidence.witness_list(ev) if w.get("mismatch")]
    print(f"  falsifying inputs on the Lean model: {sum(w['model'] == 'fails' for w in ws)} of {len(ws)} fail there too; "
          f"{len(mm)} MODEL MISMATCH; {sum(w['model'] == 'not evaluated' for w in ws)} not evaluated")
    for i, w in mm:
        print(f"  MODEL MISMATCH: {i} at {json.dumps(w['values'], ensure_ascii=False)} ({w['source']}): the compiled Rust {w['rust']}, the Lean model {w['model']}")
    return 0


def cmd_narrowing() -> int:
    """After lean/Run/Narrowing.lean ran: compare what Lean said with what the compiler did (plan nodes Q1, Q2).
    Writes out/narrowing.json. Exit 1 if anything differs: a fault of the book or of the generator, never a verdict."""
    side = json.loads((ROOT / "build" / "narrowing.json").read_text())
    log = (OUT / "narrowing.log").read_text() if (OUT / "narrowing.log").exists() else ""
    res = narrowing.collect(side, log)
    OUT.mkdir(exist_ok=True)
    (OUT / "narrowing.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    c = res["counts"]
    print(f"  narrowing (Q1): {c['facts_declared']} declared facts about what narrowing settles kernel-checked, "
          f"{c['facts_not_declared']} undeclared ones attempted and not provable; {c['controls_refused']} control sentences refused "
          f"({c['refused_claims']} claims proved to hold of every operation, each through the theorem the refusal names); "
          f"{c['narrowed_not_refused']} narrowed claims not refused ({c['narrowed_not_refused_fixture_rules']} in fixture Rules), "
          f"none provable for every operation by the fixed tactic" if res["ok"] else
          f"  narrowing: {len(res['problems'])} PROBLEM(S)")
    print(f"  coverage (Q2): Lean reported the Calls value of {c['calls_reported']} of {c['claims']} claims in {c['readings']} compiled readings "
          f"({c['fixture_rule_readings']} fixture Rule lines, {c['fixture_scenario_readings']} fixture scenarios, {c['control_readings']} control lines); "
          f"printed coverage differs from it in {c['coverage_mismatches']} ({c['sequence_claims']} claims are about a sequence, according to Lean)")
    print(f"  narrowed twice: {c['controls_narrowed_twice']} control sentences that narrow or scope one clause with more than one word, each refused; "
          f"statements that did not elaborate (other than the one broken on purpose): {len(c['bad_statements'])}")
    for p in res["problems"]:
        print(f"  NARROWING CHECK FAILED: {p}")
    return 0 if res["ok"] else 1


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
        print(__import__("clausal.__main__").__main__.__doc__)
        return 2
    if argv[0] == "compile":           # NEW sentences, from the Clausebook alone (no flat statement, no features/)
        from . import newrules
        return newrules.cmd_compile(argv[1:])
    if argv[0] == "evidence":          # run the generated property tests and bounded checks (reads build/ only)
        return evidence.cmd_evidence(argv[1:])
    if argv[0] == "narrowing":         # reads build/narrowing.json and out/narrowing.log only
        return cmd_narrowing()
    if argv[0] == "book":              # checks on the Clausebook itself: core stands alone; the registration lint
        from . import book
        try:
            return book.main(argv[1:])
        except FeatureError as e:
            print(f"clausal book: {e}", file=sys.stderr)
            return 1
    if argv[0] == "duplicates":        # plan node Q5: sentences with the same statement (informational)
        from . import duplicates
        try:
            return duplicates.main(argv[1:])
        except FeatureError as e:
            print(f"clausal duplicates: {e}", file=sys.stderr)
            return 1
    if argv[0] == "rules":             # reads a stored graph only: no features, no glossary, no Lean
        from . import rules
        return rules.main(argv[1:])
    try:
        st = State()
        if argv[0] == "gen":
            return cmd_gen(st)
        if argv[0] == "derive":
            return cmd_derive(st)
        if argv[0] == "witness":
            return cmd_witness_collect(st) if "--collect" in argv else cmd_witness(st)
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
        print(f"clausal: {e}", file=sys.stderr)
        return 1
    print(f"unknown command {argv[0]}", file=sys.stderr)
    return 2
