"""clausal separate: SEPARATING INPUTS for two candidate readings (plan node L3).

    python3 -m clausal separate "<sentence A>" ["<sentence B>"] [--json] [--no-rust] [--no-prove]

Given two rule sentences (or one sentence that may name operations in more than one system), this compiles each
with the ordinary compiler, once per system, and for every pair of compiled readings answers ONE question: is
there a concrete input (state and arguments) on which one reading holds and the other fails?

Nothing here parses a sentence and nothing here evaluates one. The compiler is `vocab.Compiler.rule`, called with
its existing `domain_hint` once per system (that is how a sentence that the compiler would refuse as AMBIGUOUS
across systems, or silently read in the only system where it parses, is turned into its candidates). The search
is the existing reading search (`rsearch.search_file`, through `newrules.script`): each reading on the grid of
generated inputs of glossary.yaml `param_types.*.sample`, evaluated ON THE LEAN MODEL through the definition of
each frame. The replay is the existing tree evaluator on the COMPILED RUST (wallet-bdd/src/pieces.rs), driven by
wallet-bdd/examples/separate_replay.rs.

The verdict of a pair is exactly one of

  SEPARATED            an input of the grid on which one reading holds and the other fails (the first such grid
                       point for each direction that occurs), with what the compiled Rust answered there and the
                       state it left
  SAME-TERM            the two sentences compile to the same Lean term: no input can separate them, and no
                       search is needed to know it ("equal as terms")
  PROVED-EQUAL         different terms, and Lean's kernel accepted a proof of `A <-> B` (which script is named; the scripts name only the frame definitions)
  NONE-FOUND           different terms, no proof, and no grid point separates them. This is NOT "equal": the
                       bounds of the grid are printed, and readings that differ only beyond them land here
  DIFFERENT-OPERATIONS the readings are about different operations (different states or inputs), so there is no
                       common input to separate them on; each gets an input of its own
  NOT-SEARCHED         a reading could not be searched (the reason is given)

The module never edits the compiler and is not a verdict of the pipeline: it writes only under build/separate/.
See clausal/SEPARATE.md (design, limits) and clausal/separate_tests/ (cases with frozen expectations).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from itertools import combinations
from pathlib import Path

from . import newrules, rsearch, trees, vocab
from .core import Feature, Problem, Rule, load_glossary
from .pipeline import LEAN, ROOT

WORK = ROOT / "build" / "separate"
LEAN_TIMEOUT = 900          # seconds for the one Lean run (search and equality attempts)
RUST_TIMEOUT = 900
# The kernel-checked equality attempts, in order; the first whose theorem exists with no `sorryAx` names the verdict.
# They use the frame library only: nothing about a fixture, so a pair whose equality needs a fact about the code
# (for instance that the operation always answers) is not proved here and stays NONE-FOUND.
EQ_SCRIPTS = [
    ("rfl", "Iff.rfl"),
    ("pointwise", "by\n  unfold {a} {b}\n"
                  "  simp only [{frames}, Frames.Op.HoldsAt, Frames.Op.HoldsAt2, ← forall_and]\n"
                  "  refine forall_congr' fun s => forall_congr' fun a => ?_\n"
                  "  grind"),
]


# --------------------------------------------------------------------------------------------- compiling

def load():
    gl = load_glossary(ROOT / "glossary.yaml", "glossary.yaml")
    voc = vocab.Vocabulary(ROOT / "clausebook.yaml", "clausebook.yaml", gl)
    return voc, vocab.Compiler(voc)


def domains(voc) -> list:
    return sorted({o["domain"] for o in voc.ops.values()})


def candidates(voc, comp, sentence: str, label: str) -> list:
    """One entry per system: the sentence compiled there by the ordinary compiler, or its refusal."""
    f = Feature(path="<separate>", name="separate", slug="separate")
    out = []
    for n, d in enumerate(domains(voc)):
        r = Rule(feature=f, name=sentence, line=n + 1, tags=[f"@id:{label}_{d}"])
        got = comp.rule(r, d)
        c = {"label": f"{label}/{d}", "sentence": sentence, "domain": d, "which": label}
        if isinstance(got, Problem):
            c.update({"compiled": False, "status": got.status, "message": got.message, "hint": got.hint, "reading": None})
        else:
            c.update({"compiled": True, "status": "COMPILED", "reading": got, "id": got.id})
        out.append(c)
    return out


def term(rd) -> str:
    """The Lean term of a reading: its definition without its name."""
    return rd.lean_def().split(":=", 1)[1].strip()


def key(rd) -> list:
    return [c["key"] for c in rd.info["clauses"]]


def op_ids(rd) -> list:
    """Per clause, the operation (or sequence of operations) the clause is about."""
    return [[o["id"] for o in c["ops"]] for c in rd.info["clauses"]]


def op_words(voc, rd) -> str:
    out = []
    for c in rd.info["clauses"]:
        for o in c["ops"]:
            t = (f"{o['id']} ({o['domain']}: state " + ", ".join(f"{r}: {t}" for r, t in o["state"])
                 + "; input " + (", ".join(f"{r}: {t}" for r, t in o["input"]) or "none") + ")")
            if t not in out:
                out.append(t)
    return "; ".join(out)


def shared_nouns(voc, sentences) -> list:
    """Operation nouns of the Clausebook that name operations in more than one system and occur in a sentence."""
    by_noun = {}
    for o in voc.ops.values():
        for n in o["nouns"]:
            by_noun.setdefault(n, []).append(o)
    out = []
    for n, ops in sorted(by_noun.items()):
        if len({o["domain"] for o in ops}) < 2:
            continue
        where = [k for k, s in enumerate(sentences) if re.search(rf"(?<!\w){re.escape(n)}(?!\w)", s.lower())]
        if where:
            out.append({"noun": n, "in_sentences": where,
                        "operations": [{"id": o["id"], "domain": o["domain"]} for o in ops]})
    return out


# --------------------------------------------------------------------------------------------- comparing

def align(sa: dict, sb: dict):
    """The common grid of two searched readings, or None. Variables are named after the operation's roles
    (rsearch.grid), so two readings of the same operation have the same variables; a reading that compares two calls
    has the first call's variables and a second set. Returns (variables of the larger grid, positions of A's
    variables in it, positions of B's)."""
    va, vb = [(n, list(vals)) for n, vals in sa["vars"]], [(n, list(vals)) for n, vals in sb["vars"]]
    big = va if len(va) >= len(vb) else vb
    names = [n for n, _ in big]
    pos = []
    for vs in (va, vb):
        p = []
        for n, vals in vs:
            if n not in names or big[names.index(n)][1] != vals:
                return None
            p.append(names.index(n))
        pos.append(p)
    return big, pos[0], pos[1]


def point_bits(r: dict, index: int) -> str:
    w = r["width"]
    return r["bits"][index * w:(index + 1) * w]


def holds(r: dict, bits: str) -> bool:
    """A reading holds at a point iff every one of its claims does (a claim says nothing outside its scope)."""
    return all(bits[j] == "1" for j, (kind, _) in enumerate(r["layout"]) if kind == "at")


def in_scope(r: dict, bits: str) -> list:
    return [bits[j] == "1" for j, (kind, _) in enumerate(r["layout"]) if kind == "scope"]


def flat(index: list, sizes: list) -> int:
    k = 0
    for i, n in zip(index, sizes):
        k = k * n + i
    return k


def compare(ra: dict, rb: dict, sa: dict, sb: dict) -> dict | None:
    """Every point of the common grid: does A hold, does B hold. None if there is no common grid.
    The LAST variable runs fastest, as in the generated Lean loops."""
    al = align(sa, sb)
    if al is None:
        return None
    big, pa, pb = al
    sizes = [len(vals) for _, vals in big]
    total = 1
    for n in sizes:
        total *= n
    for r, p in ((ra, pa), (rb, pb)):
        n = 1
        for i in p:
            n *= sizes[i]
        if len(r["bits"]) != n * r["width"]:
            raise ValueError(f"the search printed {len(r['bits'])} evaluations where {n} points of {r['width']} were expected")
    counts = {"points": total, "both_hold": 0, "both_fail": 0, "a_only": 0, "b_only": 0}
    first = {"a_only": None, "b_only": None}
    idx = [0] * len(sizes)
    for _ in range(total):
        ia, ib = [idx[i] for i in pa], [idx[i] for i in pb]
        ba = point_bits(ra, flat(ia, [sizes[i] for i in pa]))
        bb = point_bits(rb, flat(ib, [sizes[i] for i in pb]))
        ha, hb = holds(ra, ba), holds(rb, bb)
        what = "both_hold" if ha and hb else "both_fail" if not ha and not hb else "a_only" if ha else "b_only"
        counts[what] += 1
        if what in first and first[what] is None:
            first[what] = {"index": list(idx), "values": {n: vals[i] for (n, vals), i in zip(big, idx)},
                           "a": {"holds": ha, "in_scope": in_scope(ra, ba), "bits": ba, "values": {big[i][0]: big[i][1][idx[i]] for i in pa}},
                           "b": {"holds": hb, "in_scope": in_scope(rb, bb), "bits": bb, "values": {big[i][0]: big[i][1][idx[i]] for i in pb}}}
        k = len(sizes)
        while k:
            k -= 1
            idx[k] += 1
            if idx[k] < sizes[k]:
                break
            idx[k] = 0
    return {"counts": counts, "first": first, "bounds": {"points": total, "variables": [{"name": n, "values": vals} for n, vals in big]}}


# --------------------------------------------------------------------------------------------- Lean and Rust

def env() -> dict:
    e = dict(os.environ)
    e["PATH"] = f"{Path.home()}/.elan/bin:{Path.home()}/.cargo/bin:" + e.get("PATH", "")
    return e


def frames_of(*rds) -> str:
    """The Lean names of the frames two readings use (and their pointwise forms), for the equality scripts."""
    names = []
    for rd in rds:
        for m in re.findall(r"Frames\.[A-Z]\w*", rd.lean_def()):
            for n in (m, m + ".at"):
                if n not in names:
                    names.append(n)
    return ", ".join(names)


def lean_script(voc, rds: list, pairs: list) -> tuple:
    """(Lean text, sidecar): the readings' definitions, the existing grid search for each, then one kernel attempt
    per (pair, script) at `A <-> B`. The attempts come last, so one that fails or runs long costs only itself."""
    text, side = newrules.script(voc, [{"result": rd} for rd in rds])
    text = text.replace("Run/NewReadings.lean", "../build/separate/<key>/Separate.lean (clausal separate)")
    out = [text]
    for k, (a, b) in enumerate(pairs):
        for name, script in EQ_SCRIPTS:
            proof = script.format(a=a.name, b=b.name, frames=frames_of(a, b))
            out.append(f"set_option maxHeartbeats 400000 in\ntheorem Separate.eq{k}_{name} : {a.name} ↔ {b.name} := {proof}\n"
                       f"#print axioms Separate.eq{k}_{name}\n")
    return "\n".join(out), side


def search_errors(text: str, log: str) -> list:
    """Lean errors in the definitions and the search (not in the equality attempts, where a failed script is the
    ordinary outcome and is read from `#print axioms`)."""
    at = text.find("theorem Separate.eq")
    last = text.count("\n", 0, at) if at >= 0 else text.count("\n") + 1      # the `set_option` line above the first attempt
    out = []
    for l in log.splitlines():
        m = re.search(r"Separate\.lean:(\d+):\d+: error:", l)
        if m and int(m.group(1)) < last:
            out.append(l)
    return out[:10]


def proved(log: str, k: int) -> str | None:
    """The first equality script whose theorem Lean's kernel accepted (it exists and does not rest on `sorryAx`)."""
    for name, _ in EQ_SCRIPTS:
        m = re.search(rf"'Separate\.eq{k}_{name}' (does not depend on any axioms|depends on axioms: \[([^\]]*)\])", log)
        if m and "sorryAx" not in (m.group(2) or ""):
            return name
    return None


def run_lean(work: Path, text: str) -> str:
    path = work / "Separate.lean"
    path.write_text(text)
    try:
        p = subprocess.run(["lake", "env", "lean", str(path)], cwd=LEAN, env=env(), capture_output=True, text=True, timeout=LEAN_TIMEOUT)
        log = p.stdout + p.stderr
    except subprocess.TimeoutExpired as e:
        log = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        log += f"\nSEPARATE-TIMEOUT after {LEAN_TIMEOUT} s\n"
    (work / "separate.log").write_text(log)
    return log


def run_rust(work: Path, voc, rds: dict, side: dict, points: list) -> dict:
    """Replay (reading id, values) points on the compiled Rust. Returns {(id, values as JSON): record} and the file."""
    entries = {}
    for id_, rd in rds.items():
        e = trees.reading_entry(voc, rd, side.get(id_, {}))
        if e:
            entries[id_] = e
    pts = [p for p in points if p["id"] in entries]
    path = work / "replay.json"
    path.write_text(json.dumps({"readings": entries, "points": pts}, indent=1, ensure_ascii=False))
    out = {"file": str(path), "command": f"(cd {ROOT / 'wallet-bdd'} && cargo run --quiet --example separate_replay -- {path})",
           "records": {}, "error": None}
    if not pts:
        return out
    try:
        p = subprocess.run(["cargo", "run", "--quiet", "--example", "separate_replay", "--", str(path)], cwd=ROOT / "wallet-bdd",
                           env=env(), capture_output=True, text=True, timeout=RUST_TIMEOUT)
    except subprocess.TimeoutExpired:
        out["error"] = f"the replay did not finish in {RUST_TIMEOUT} s"
        return out
    if p.returncode != 0:
        out["error"] = (p.stderr or p.stdout).strip()[-2000:]
        return out
    for line in p.stdout.splitlines():
        if line.startswith("{"):
            rec = json.loads(line)
            out["records"][pkey(rec["id"], rec["values"])] = rec
    return out


def pkey(id_: str, values: dict) -> str:
    return id_ + " " + json.dumps(values, sort_keys=True, ensure_ascii=False)


# --------------------------------------------------------------------------------------------- the whole question

def separate(sentences: list, rust: bool = True, prove: bool = True) -> dict:
    voc, comp = load()
    labels = ["A", "B"][:len(sentences)]
    cands = [c for s, l in zip(sentences, labels) for c in candidates(voc, comp, s, l)]
    ok = [c for c in cands if c["compiled"]]
    # which pairs: a reading of A against a reading of B; with one sentence, its readings against each other
    pairs = [(a, b) for a, b in combinations(ok, 2) if len(sentences) == 1 or a["which"] != b["which"]]
    res = {"sentences": sentences, "systems": domains(voc), "shared_nouns": shared_nouns(voc, sentences),
           "candidates": [], "comparisons": [], "lean": None, "rust": None}
    for c in cands:
        d = {k: c[k] for k in ("label", "sentence", "domain", "compiled", "status")}
        if c["compiled"]:
            rd = c["reading"]
            d.update({"id": rd.id, "lean": rd.lean_def(), "key": key(rd), "operations": op_ids(rd), "about": op_words(voc, rd),
                      "echo": [list(e) for e in rd.echo]})
        else:
            d.update({"message": c["message"], "hint": c["hint"]})
        res["candidates"].append(d)
    for s, l in zip(sentences, labels):       # the cross-system note: one sentence, more than one system
        mine = [c for c in cands if c["which"] == l]
        nouns = [n for n in res["shared_nouns"] if sentences.index(s) in n["in_sentences"]]
        if nouns:
            got = [c["domain"] for c in mine if c["compiled"]]
            res.setdefault("cross_system", []).append({
                "sentence": l, "nouns": [n["noun"] for n in nouns], "compiles_in": got,
                "refused_in": [{"domain": c["domain"], "status": c["status"], "message": c["message"]} for c in mine if not c["compiled"]],
                "statement": cross_statement(nouns, got)})
    if not ok:
        return res
    # equal as terms is decided on the compiled text alone; everything else needs the search
    same = {(a["label"], b["label"]): term(a["reading"]) == term(b["reading"]) for a, b in pairs}
    digest = hashlib.sha256(json.dumps([sentences, [term(c["reading"]) for c in ok]], ensure_ascii=False).encode()).hexdigest()[:12]
    work = WORK / digest
    work.mkdir(parents=True, exist_ok=True)
    rds = {c["reading"].id: c["reading"] for c in ok}
    eq_pairs = [(a, b) for a, b in pairs if prove and not same[(a["label"], b["label"])]
                and a["reading"].state_type == b["reading"].state_type and a["reading"].input_type == b["reading"].input_type]
    text, side = lean_script(voc, list(rds.values()), [(a["reading"], b["reading"]) for a, b in eq_pairs])
    log = run_lean(work, text)
    rs = rsearch.parse(log, side) if "RSEARCH" in log else {}
    res["lean"] = {"script": str(work / "Separate.lean"), "log": str(work / "separate.log"),
                   "command": f"(cd {LEAN} && lake env lean {work / 'Separate.lean'})",
                   "searched": sorted(i for i, r in rs.items() if "bits" in r),
                   "errors": search_errors(text, log)}
    points = []          # what to replay on the compiled Rust

    def want(c, values, why):
        points.append({"id": c["reading"].id, "values": values, "why": why})

    for a, b in pairs:
        ra, rb = rs.get(a["reading"].id), rs.get(b["reading"].id)
        cmp_ = {"a": a["label"], "b": b["label"], "same_term": same[(a["label"], b["label"])], "proved_equal_by": None,
                "verdict": None, "bounds": None, "counts": None, "separating": [], "own_inputs": None, "why": None}
        res["comparisons"].append(cmp_)
        if cmp_["same_term"]:
            cmp_["verdict"] = "SAME-TERM"
            cmp_["why"] = "both sentences compile to the same Lean term: " + term(a["reading"])
            continue
        missing = [c["label"] for c, r in ((a, ra), (b, rb)) if r is None or "bits" not in r]
        if missing:
            cmp_["verdict"] = "NOT-SEARCHED"
            cmp_["why"] = ("no search result for " + ", ".join(missing) + ": "
                           + "; ".join((rs.get(c["reading"].id) or {}).get("skipped", "Lean printed no result (see the log)")
                                       for c in (a, b) if c["label"] in missing))
            continue
        got = compare(ra, rb, side[a["reading"].id], side[b["reading"].id]) if a["domain"] == b["domain"] else None
        if got is None:
            cmp_["verdict"] = "DIFFERENT-OPERATIONS"
            cmp_["why"] = (f"{a['label']} is about {op_words(voc, a['reading'])}; {b['label']} is about {op_words(voc, b['reading'])}. "
                           "They take different states and inputs, so no input is an input of both and nothing can separate them: "
                           "which is meant is a choice of operation, not of wording.")
            own = {}
            for c, r in ((a, ra), (b, rb)):
                own[c["label"]] = {"points": r["tried"], "in_scope": r["in_scope"],
                                   "variables": [{"name": n, "values": vals} for n, vals in side[c["reading"].id]["vars"]],
                                   "holds_at": first_holding(r, side[c["reading"].id]),
                                   "fails_at": r["bad"]["values"] if r.get("bad") else None}
                for what in ("holds_at", "fails_at"):
                    if own[c["label"]][what]:
                        want(c, own[c["label"]][what], what)
            cmp_["own_inputs"] = own
            continue
        cmp_["counts"], cmp_["bounds"] = got["counts"], got["bounds"]
        k = next((i for i, (x, y) in enumerate(eq_pairs) if x is a and y is b), None)
        cmp_["proved_equal_by"] = proved(log, k) if k is not None else None
        for what, holder in (("a_only", a["label"]), ("b_only", b["label"])):
            p = got["first"][what]
            if p:
                p["holds"] = holder
                p["fails"] = b["label"] if holder == a["label"] else a["label"]
                cmp_["separating"].append(p)
                want(a, p["a"]["values"], "separating")
                want(b, p["b"]["values"], "separating")
        if cmp_["separating"]:
            cmp_["verdict"] = "SEPARATED"
            if cmp_["proved_equal_by"]:      # cannot happen unless the search and the kernel disagree
                cmp_["why"] = "FAULT: the kernel accepted A <-> B and the search found a separating input; distrust both"
        elif cmp_["proved_equal_by"]:
            cmp_["verdict"] = "PROVED-EQUAL"
            cmp_["why"] = f"different terms; Lean's kernel accepted a proof of A <-> B (script `{cmp_['proved_equal_by']}`)"
        else:
            cmp_["verdict"] = "NONE-FOUND"
            cmp_["why"] = ("different terms, not proved equal" + ("" if prove else " (no proof was attempted)")
                           + f", and no separating input among the {got['counts']['points']} grid points. "
                           "This does not say the readings are equal: they may differ on inputs outside these bounds.")
    if rust and points:
        rr = run_rust(work, voc, rds, side, points)
        res["rust"] = {"file": rr["file"], "command": rr["command"], "error": rr["error"]}
        for cmp_ in res["comparisons"]:
            a = next(c for c in ok if c["label"] == cmp_["a"])
            b = next(c for c in ok if c["label"] == cmp_["b"])
            for p in cmp_["separating"]:
                for side_, c in (("a", a), ("b", b)):
                    rec = rr["records"].get(pkey(c["reading"].id, p[side_]["values"]))
                    p[side_]["rust"] = rust_view(rec, p[side_]["bits"])
            for label, own in (cmp_["own_inputs"] or {}).items():
                c = a if label == a["label"] else b
                r = rs[c["reading"].id]
                own["rust"] = {}
                for what in ("holds_at", "fails_at"):
                    if own[what]:
                        idx = [vals.index(own[what][n]) for n, vals in side[c["reading"].id]["vars"]]
                        bits = point_bits(r, flat(idx, [len(vals) for _, vals in side[c["reading"].id]["vars"]]))
                        own["rust"][what] = rust_view(rr["records"].get(pkey(c["reading"].id, own[what])), bits)
    elif points:
        res["rust"] = {"file": None, "command": None, "error": "not replayed (--no-rust)"}
    return res


def first_holding(r: dict, s: dict):
    """The first grid point at which a reading is in scope (every unit) and holds, as values; None if there is none."""
    sizes = [len(vals) for _, vals in s["vars"]]
    total = 1
    for n in sizes:
        total *= n
    for i in range(total):
        bits = point_bits(r, i)
        if holds(r, bits) and all(in_scope(r, bits)):
            idx, k = [], i
            for n in reversed(sizes):
                idx.append(k % n)
                k //= n
            idx.reverse()
            return {n: vals[j] for (n, vals), j in zip(s["vars"], idx)}
    return None


def rust_view(rec, lean_bits: str) -> dict:
    if rec is None:
        return {"replayed": False, "why": "the replay printed nothing for this point"}
    if "error" in rec:
        return {"replayed": False, "why": rec["error"]}
    return {"replayed": True, "bits": rec["bits"], "agrees_with_lean": rec["bits"] == lean_bits, "calls": rec["calls"]}


def cross_statement(nouns, got) -> str:
    n = nouns[0]
    ops = ", ".join(f"{o['id']} ({o['domain']})" for o in n["operations"])
    if len(got) > 1:
        return (f"\"{n['noun']}\" names {ops}, and the sentence compiles in each of: {', '.join(got)}. The compiler refuses it as "
                "AMBIGUOUS; the candidates are compared below.")
    if len(got) == 1:
        return (f"\"{n['noun']}\" names {ops}, but the rest of the sentence is written in the words of {got[0]} only, so the compiler "
                f"reads it there without asking. If the other operation was meant, the sentence has to be reworded.")
    return f"\"{n['noun']}\" names {ops}; the sentence compiles in none of them."


# --------------------------------------------------------------------------------------------- printing

def say_values(values: dict) -> str:
    return ", ".join(f"{n.replace('_', ' ')} = {v}" for n, v in values.items())


def say_calls(rv: dict, ind: str) -> list:
    if not rv or not rv.get("replayed"):
        return [f"{ind}compiled Rust: not replayed" + (f" ({rv['why']})" if rv and rv.get("why") else "")]
    out, seen = [], set()
    for c in rv["calls"]:
        k = json.dumps([c["ops"], c["inputs"], c["before"]], sort_keys=True)
        if k in seen:
            continue
        seen.add(k)
        call = " then ".join(c["ops"]) + (" (second call)" if c["run"] == 2 else "")
        if c["answered"]:
            out.append(f"{ind}compiled Rust: {call} answered {c['answer']} ({'accepted' if c['accepted'] else 'rejected'}); "
                       f"state before {json.dumps(c['before'], ensure_ascii=False)}, after {json.dumps(c['after'], ensure_ascii=False)}")
        else:
            out.append(f"{ind}compiled Rust: {call} gave no answer; state before {json.dumps(c['before'], ensure_ascii=False)}")
    out.append(f"{ind}the reading on the compiled Rust at this input: {rv['bits']} "
               + ("(the same as on the Lean model)" if rv["agrees_with_lean"] else "(DIFFERENT from the Lean model: a fault, not a verdict)"))
    return out


def say_bounds(b: dict) -> list:
    out = [f"  bounds: {b['points']} grid points, the product of"]
    for v in b["variables"]:
        out.append(f"    {v['name'].replace('_', ' ')}: {len(v['values'])} values: " + "; ".join(v["values"]))
    return out


def render(res: dict) -> str:
    o = []
    for k, s in enumerate(res["sentences"]):
        o.append(f"{'AB'[k]}: {s}")
    o.append("")
    o.append("Candidates (the ordinary compiler, once per system):")
    for c in res["candidates"]:
        if c["compiled"]:
            o.append(f"  {c['label']:<10} COMPILED   {' & '.join(c['key'])}")
            o.append(f"             {c['lean'].split(':=', 1)[1].strip()}")
        else:
            o.append(f"  {c['label']:<10} {c['status']:<10} {c['message']}")
    for x in res.get("cross_system", []):
        o.append("")
        o.append(f"More than one system ({x['sentence']}): {x['statement']}")
    if not res["comparisons"]:
        o.append("")
        n = sum(c["compiled"] for c in res["candidates"])
        o.append("Nothing to compare: " + ("no sentence compiled." if n == 0 else "only one reading compiled."))
    for c in res["comparisons"]:
        o.append("")
        o.append(f"{c['a']} against {c['b']}: {c['verdict']}")
        if c["why"]:
            o.append(f"  {c['why']}")
        for p in c["separating"]:
            o.append(f"  input: {say_values(p['values'])}")
            o.append(f"    {p['holds']} holds, {p['fails']} fails")
            for side_, label in (("a", c["a"]), ("b", c["b"])):
                sc = p[side_]["in_scope"]
                o.append(f"    {label}: {'holds' if p[side_]['holds'] else 'FAILS'}"
                         + ("" if all(sc) else " (this call is outside what the reading is about)") + f"; Lean model bits {p[side_]['bits']}")
                o += say_calls(p[side_].get("rust"), "      ")
        if c["counts"]:
            n = c["counts"]
            o.append(f"  on the grid: both hold at {n['both_hold']}, both fail at {n['both_fail']}, only {c['a']} holds at {n['a_only']}, "
                     f"only {c['b']} holds at {n['b_only']}")
        if c["bounds"]:
            o += say_bounds(c["bounds"])
        for label, own in (c["own_inputs"] or {}).items():
            o.append(f"  {label}: searched alone on {own['points']} grid points")
            for what, word in (("holds_at", "holds"), ("fails_at", "FAILS")):
                if own[what]:
                    o.append(f"    {word} at: {say_values(own[what])}")
                    o += say_calls((own.get("rust") or {}).get(what), "      ")
                else:
                    o.append(f"    {word} at: no such grid point")
    if res["lean"]:
        o.append("")
        o.append(f"Lean script and log: {res['lean']['script']}, {res['lean']['log']}")
        o.append(f"  rerun: {res['lean']['command']}")
        for e in res["lean"]["errors"]:
            o.append(f"  Lean error: {e}")
    if res["rust"]:
        if res["rust"]["error"]:
            o.append(f"Replay on the compiled Rust: {res['rust']['error']}")
        if res["rust"]["command"]:
            o.append(f"Replay on the compiled Rust: {res['rust']['command']}")
    return "\n".join(o)


def main(argv) -> int:
    flags = {a for a in argv if a.startswith("--")}
    sentences = [a for a in argv if not a.startswith("--")]
    if not 1 <= len(sentences) <= 2 or flags - {"--json", "--no-rust", "--no-prove"}:
        print(__doc__)
        return 2
    res = separate(sentences, rust="--no-rust" not in flags, prove="--no-prove" not in flags)
    print(json.dumps(res, indent=1, ensure_ascii=False) if "--json" in flags else render(res))
    return 0 if res["comparisons"] or any(c["compiled"] for c in res["candidates"]) else 1
