"""clausal narrowing: NARROWED CLAIMS (plan nodes Q1 and Q2).

"successful" / "rejected" narrow a claim to the calls that give an answer of that kind. Two things can go wrong, and
both were found by the readability critique (docs/studies/2026-11-12/readability-critique.md, sections 2.1 and 2.2):

Q1  A narrowed claim can hold of EVERY operation. "A successful transfer never loses acceptance when the amount is
    larger" assumes both calls accepted before it says anything, so no code can break it. `refusal` refuses such a
    Rule clause (status SAYS-NOTHING) and names the theorem of lean/Frames/Narrowing.lean that proves it.

    What the decision rests on. `REASONS` pairs each frame with the theorems `Frames.Narrowed.*` that can make it say
    nothing; each theorem needs one fact about the operation's notion of acceptance (every accepted answer is in the
    class; no rejected answer is; any two accepted answers are the same; there is no rejected answer at all). Those
    facts are declared per operation in the book that defines it (`narrowing:`; clausebook/local/*.yaml). NOTHING HERE IS TRUSTED. On every run
    lean/Run/Narrowing.lean (written by `script`, read back by `collect`)
      * kernel-checks every declared fact, and attempts every fact that was NOT declared: it must fail. So the lists
        in the book are exactly what Lean proves with the fixed tactic `narrow_side`;
      * for every control sentence that is refused (controls/narrowing.feature), compiled once more with the refusal
        off, kernel-checks the statement "for every `run`, the claim holds" THROUGH THE THEOREM THE REFUSAL NAMED;
      * for every narrowed claim that was NOT refused (every fixture Rule, every control that must compile), attempts
        the same statement with the fixed tactic `vacuous_by_narrowing`: it must fail. If it succeeds the claim says
        nothing and the table below missed it: the run fails.
    The table is therefore a way to decide quickly and to say why; whether a refused sentence really says nothing,
    and whether an accepted one really says something the tactic cannot discharge, is answered by the kernel.

Q2  The printed coverage ("covers ...") has to be the coverage of the Lean. It is chosen by `Claim.calls`, which is
    set where the claim's operation is written. On every run Lean is asked for `(op).calls` of every claim of every
    compiled reading (`#calls`), and `collect` compares (a) the constructor Lean reports with `Claim.calls`, and
    (b) the coverage lines the reading PRINTS with the lines the book gives for the constructors Lean reported:
    the `covers` slot, the answer requirement, the note of a sequence (Lean also says whether the claim's operation is
    one: its term mentions `Frames.Op.andThen`), the note of two compared calls, the stated weakenings.

A must-fail attempt (parts 2 and 4 of the script) counts only if its STATEMENT elaborated: `#narrowing_report` says
`notproved` for a failed script and `badstatement` for a statement Lean could not read, and only the first is an
answer. The script carries one statement that is broken on purpose, which must be reported `badstatement`.

Limits, stated: `narrow_side` and `vacuous_by_narrowing` are proof search. A fact they cannot prove is not declared
and a vacuous claim that needs it is not refused. Classes with holes ("is rejected with <error>") have no facts.
Only Rule lines are refused; a scenario's Then is not looked at.
"""
from __future__ import annotations

import json
import re

from .core import FeatureError, Problem

KINDS = ("accepted", "rejected")
WORD = {"accepted": "successful", "rejected": "rejected"}          # the modifier that asks for each narrowing
STATUS = "SAYS-NOTHING"
THEOREMS = "lean/Frames/Narrowing.lean"
TEXTS = ("covers", "two_calls", "weakening", "sequence", "sequence_scenario")     # the coverage lines a printed line is looked up among
BAD_STATEMENT = "NarrowingRun.control_bad_statement"     # broken on purpose: `#narrowing_report` must say `badstatement`
ABSENT = "NarrowingRun.control_never_declared"           # never declared: `#narrowing_report` must say `missing`

# frame id -> [(what the narrowing must settle, theorem of Frames.Narrowed, why it then says nothing)]
#   True / False   the class in hole `c`: every covered answer is in it / none is
#   "one_answer"   any two covered answers are the same answer (the frame compares the answers themselves)
#   None           nothing: the frame's content is empty under any narrowing
# `{kind}` is "accepted" or "rejected"; `{cls}` the class as composed.
REASONS = {
    "always_answers": [(None, "alwaysAnswers", "only calls that give an answer are covered, and that a call answers is all the clause claims")],
    "always": [(True, "always", "every {kind} answer is in the class `{cls}`, which is all the clause claims")],
    "never": [(False, "never", "no {kind} answer is in the class `{cls}`, which is all the clause claims")],
    "if_then": [(True, "ifThen", "every {kind} answer is in the class `{cls}`, whether or not the condition holds")],
    "only_if": [(False, "onlyIf", "no {kind} answer is in the class `{cls}`, so the condition is never asked for")],
    "monotone": [(True, "monotone_holds", "the second call is {kind} too, and every {kind} answer is in the class `{cls}`: nothing can be lost"),
                 (False, "monotone_fails", "the first call is {kind}, and no {kind} answer is in the class `{cls}`: there is nothing to lose")],
    "same_answer": [("one_answer", "independentOf", "both calls are {kind}, and any two {kind} answers of this operation are the same answer")],
    "same_answer_if": [(False, "independentGiven_fails", "the first call is {kind}, and no {kind} answer is in the class `{cls}`: the condition never holds"),
                       ("one_answer", "independentGiven_view", "both calls are {kind}, and any two {kind} answers of this operation are the same answer")],
}


def facts(op: dict, kind: str) -> dict:
    return (op.get("narrowing") or {}).get(kind) or {}


def check_book(voc):
    """The `narrowing:` lines of the operations name real classes of the operation's kind of answer, and nothing else;
    the coverage lines can be told apart (the check of the printed coverage looks a printed line up among them)."""
    texts = [c[f] for c in voc.coverage.values() for f in TEXTS if f in c]
    for k, c in voc.covers.items():
        for f in ("covers", "two_calls", "sequence") + (("answer", "answer_asked", "sequence_scenario") if k == "every" else ("weakening", "prefix")):
            if not isinstance(c.get(f), str):
                raise FeatureError(f"{voc.at(c['id'])}: the `coverage:` entry `{c['id']}` has no `{f}` text")
    if len(set(texts)) != len(texts) or any("; " in c["covers"] for c in voc.coverage.values()):
        raise FeatureError(f"{voc.rel}: the `coverage:` texts must differ from each other, and a `covers` text may not contain \"; \"")
    for o in voc.ops.values():
        nw = o.get("narrowing") or {}
        for kind, f in nw.items():
            where = f"{voc.at(o['id'])}: `{o['id']}`: narrowing"
            if kind not in KINDS:
                raise FeatureError(f"{where}: `{kind}` is not one of {', '.join(KINDS)}")
            for key, val in (f or {}).items():
                if key in ("one_answer", "no_call"):
                    if val is not True:
                        raise FeatureError(f"{where}.{kind}.{key} can only be `true` (leave it out otherwise)")
                elif key in ("holds", "fails"):
                    for cid in val:
                        if cid not in [p["id"] for p in classes_of(voc, o)]:
                            raise FeatureError(f"{where}.{kind}.{key}: `{cid}` is not a class (without holes) of answers of type `{o['answer']}`")
                else:
                    raise FeatureError(f"{where}.{kind}: unknown key `{key}` (holds, fails, one_answer, no_call)")
            if set((f or {}).get("holds", [])) & set((f or {}).get("fails", [])):
                raise FeatureError(f"{where}.{kind}: a class is listed under both `holds` and `fails`")


def classes_of(voc, op: dict) -> list:
    """The domain classes that can be said of this operation's answers and have no hole (a fact is about the class).
    A class of ANOTHER domain cannot be said of them: the parser offers a sentence only the forms of its own domain and the
    shared ones (vocab.Parser.forms_for). Before the third project (plan node X7) no two domains had operations with the
    same type of answer, so the type alone told them apart; the counter's `bump` and the ledger's `apply` both answer Bool,
    and the check asked the counter's book to state a fact about the ledger's word `l.accepted`."""
    return [p for p in voc.pieces.values()
            if p.get("cat") == "class" and p.get("kind") == "domain" and p.get("answer") == op["answer"] and not p.get("args")
            and p.get("domain", "shared") in ("shared", op["domain"])]


def polarity(node, op: dict, kind: str):
    """Of the answers a narrowing to `kind` covers: is every one in the class (True), none (False), or neither known (None)?"""
    if node is None or isinstance(node, list) or not hasattr(node, "piece"):
        return None
    if node.id == "not":
        p = polarity(node.args.get("p"), op, kind)
        return None if p is None else not p
    if node.id == "accepted":              # the operation's own notion of acceptance: settled by the narrowing, by definition
        return kind == "accepted"
    if node.args:
        return None
    f = facts(op, kind)
    return True if node.id in f.get("holds", []) else False if node.id in f.get("fails", []) else None


def describe_class(node) -> str:
    if node.id == "not":
        return "not " + describe_class(node.args["p"])
    return node.id


def vacuous(claim, ops) -> dict | None:
    """Why a narrowed claim holds of every operation: {theorem, why, kind, needs}, or None if no theorem applies."""
    kind = claim.calls
    if kind not in KINDS:
        return None
    op = ops[-1]                           # of a sequence: the answer spoken of, and its acceptance, are the last call's
    f = facts(op, kind)
    if f.get("no_call"):
        return {"theorem": "covers_no_call2" if claim.runs == 2 else "covers_no_call", "kind": kind, "needs": "no_call", "cls": None,
                "why": f"no answer of this operation is {'a rejection' if kind == 'rejected' else 'an acceptance'} "
                       f"({op['accepted_echo']}), so the clause covers no call at all"}
    cls = claim.node.args.get("c") if claim.node is not None else None
    pol = polarity(cls, op, kind)
    for needs, thm, why in REASONS.get(claim.frame["id"], []):
        ok = (needs is None or (needs == "one_answer" and f.get("one_answer"))
              or (isinstance(needs, bool) and pol is not None and pol == needs))
        if ok:
            return {"theorem": thm, "kind": kind, "needs": needs, "cls": describe_class(cls) if isinstance(needs, bool) else None,
                    "why": why.format(kind=kind, cls=describe_class(cls) if cls is not None and hasattr(cls, "piece") else "")}
    return None


def refusal(voc, claims, ops, where: str, line: int, text: str) -> Problem | None:
    """The refusal of one Rule clause, if a narrowed claim of it holds of every operation."""
    for c in claims:
        v = vacuous(c, ops)
        if v:
            kind = v["kind"]
            return Problem(STATUS, STATUS, line,
                           f"{where}: \"{text}\" SAYS NOTHING: vacuous by narrowing. The clause is about {kind} calls only "
                           f"(asked for by '{voc.live_word.get(WORD[kind], WORD[kind])}' on the subject), and {v['why']}. Its statement `{c.lean}` holds of EVERY "
                           f"possible operation with these types and this notion of acceptance, whatever the code does "
                           f"(theorem Frames.Narrowed.{v['theorem']}, {THEOREMS}), so no code can break the rule and it is refused",
                           f"say it of every call (drop '{voc.live_word.get(WORD[kind], WORD[kind])}'), or claim something the narrowing does not settle "
                           "(a quantity of the state, the result, a condition on the input).\n"
                           f"what narrowing settles for `{ops[-1]['id']}` is its `narrowing:` entry in {voc.book_of(ops[-1]['id']).rel}, kernel-checked on every run "
                           "(lean/Run/Narrowing.lean)")
    return None


# --------------------------------------------------------------------------- the generated script

def fact_items(voc) -> list:
    """Every fact about narrowing that could be written for an operation: [{name, op, kind, key, cls, declared, lean}]."""
    out = []
    for o in voc.ops.values():
        for kind in KINDS:
            f = facts(o, kind)
            cov = f"(({o['lean']}).{WORD[kind]}).covered"
            cand = [("no_call", None, f"∀ ans, ¬ {cov} ans", bool(f.get("no_call"))),
                    ("one_answer", None, f"∀ ans (_ : Unit) ans₂ (_ : Unit), {cov} ans → {cov} ans₂ → ans = ans₂", bool(f.get("one_answer")))]
            for p in classes_of(voc, o):
                cand.append(("holds", p["id"], f"∀ ans, {cov} ans → ({p['lean']})", p["id"] in f.get("holds", [])))
                cand.append(("fails", p["id"], f"∀ ans, {cov} ans → ¬ ({p['lean']})", p["id"] in f.get("fails", [])))
            for key, cls, lean, declared in cand:
                if f.get("no_call") and not declared:
                    continue               # with no call of that kind everything else holds too, and says nothing more
                out.append({"name": f"NarrowingRun.fact_{len(out)}", "op": o["id"], "kind": kind, "key": key, "cls": cls,
                            "declared": declared, "lean": lean})
    return out


def certificate(v: dict, runs: int) -> str:
    """The proof term of "for every run, the claim holds", through the theorem the refusal names."""
    t = "Frames.Narrowed." + v["theorem"]
    if v["theorem"] == "covers_no_call":
        return f"by intro run s a; exact {t} (by narrowed_calls) (by narrow_side) s a"
    if v["theorem"] == "covers_no_call2":
        return f"by intro run s a s₂ a₂; exact {t} (by narrowed_calls) (by narrow_side) s a s₂ a₂"
    if v["needs"] is None:
        return f"by intro run; exact {t} (by narrowed_calls)"
    return f"by intro run; exact {t} (by narrowed_calls) (by narrow_side)"


def claim_id(rd, j: int) -> str:
    return f"{rd.id}#{j}"


def script(voc, readings, controls) -> tuple:
    """(Lean text of lean/Run/Narrowing.lean, sidecar). `readings`: every compiled reading of the fixtures.
    `controls`: [{rule, on: Reading | Problem (compiled with the refusal), off: Reading | Problem (without it)}]."""
    from .vocab import HEADER, Reading, group
    out = [HEADER + "-- Run once per pipeline run with `lake env lean Run/Narrowing.lean`; read back by `clausal narrowing`.\n"
           "-- Plan nodes Q1 (narrowed claims that hold of every operation) and Q2 (the printed coverage is the Calls value).\n"
           "-- Theorems whose script fails are EXPECTED in parts 2 and 4: they are logged as errors and reported `notproved`.\n"
           "-- A statement that does not ELABORATE is never expected, except the one control of part 0: it is reported `badstatement`.\n"
           + "".join(f"import {i}\n" for i in voc.raw["lean_imports"])
           + "import Frames.Narrowing\nimport Bdd.NarrowingAudit\nopen Aeneas Aeneas.Std Result\n"
           "set_option linter.unusedVariables false\nset_option linter.unusedTactic false\nset_option linter.unreachableTactic false\n"]
    side = {"facts": fact_items(voc), "certs": [], "open": [], "calls": {}, "controls": []}
    names = [BAD_STATEMENT, ABSENT]
    out.append("-- ===== 0. THE CONTROL of the report itself: a statement that does not elaborate (the operation does not exist), with a\n"
               "--          script that fails. It must be reported `badstatement`, not `notproved`: a must-fail attempt below counts only\n"
               "--          if its statement was read. (The error logged for this line is expected.)")
    out.append(f"theorem {BAD_STATEMENT} : ∀ ans, ((Frames.NarrowingControl.noSuchOperation).successful).covered ans → False := by narrow_side\n")
    out.append("-- ===== 1. what narrowing settles, AS DECLARED in the Clausebook (`narrowing:`): each must be proved")
    for f in side["facts"]:
        if f["declared"]:
            out.append(f"theorem {f['name']} : {f['lean']} := by narrow_side")
            names.append(f["name"])
    out.append("\n-- ===== 2. what was NOT declared: each attempt must FAIL (else the book is missing a line)")
    for f in side["facts"]:
        if not f["declared"]:
            out.append(f"theorem {f['name']} : {f['lean']} := by narrow_side")
            names.append(f["name"])

    def narrowed(rd):
        ops_of = {k: g["ops"] for k, g in enumerate(rd.info["clauses"])}
        return [(j, c, ops_of[c.clause]) for j, c in enumerate(rd.claims) if c.calls in KINDS]

    out.append("\n-- ===== 3. the control sentences the compiler REFUSES, compiled without the refusal: each narrowed claim it names")
    out.append("--          holds for EVERY `run`, proved through the theorem the refusal names, and found by the fixed tactic")
    for x in controls:
        r, off = x["rule"], x["off"]
        rec = {"id": r.id, "source": f"{r.feature.path}:{r.line}", "text": r.name, "tags": list(r.tags),
               "on": getattr(x["on"], "status", "COMPILED"), "message": getattr(x["on"], "message", ""),
               "on_code": getattr(x["on"], "code", ""), "off_code": getattr(off, "code", ""),
               "off": getattr(off, "status", "COMPILED"), "certs": [], "open": []}
        side["controls"].append(rec)
        if not isinstance(off, Reading):
            continue
        out.append(f"-- {r.name}")
        for j, c, ops in narrowed(off):
            v = vacuous(c, ops)
            n = len(side["certs"]) + len(side["open"])
            if v:
                item = {"claim": claim_id(off, j), "theorem": v["theorem"], "cert": f"NarrowingRun.cert_{n}", "tactic": f"NarrowingRun.tactic_{n}",
                        "lean": c.lean}
                out.append(f"theorem {item['cert']} : ∀ run, {c.any_run} := {certificate(v, c.runs)}")
                out.append(f"theorem {item['tactic']} : ∀ run, {c.any_run} := by vacuous_by_narrowing")
                names += [item["cert"], item["tactic"]]
                side["certs"].append(item)
                rec["certs"].append(item)
            else:
                item = {"claim": claim_id(off, j), "tactic": f"NarrowingRun.open_{n}", "lean": c.lean, "source": rec["source"], "fixture": False}
                out.append(f"theorem {item['tactic']} : ∀ run, {c.any_run} := by vacuous_by_narrowing")
                names.append(item["tactic"])
                side["open"].append(item)
                rec["open"].append(item)
    out.append("\n-- ===== 4. every narrowed claim of a fixture Rule (none was refused): the fixed tactic must FAIL to prove it for every `run`")
    rule_rds = [rd for rd in readings if rd.kind == "rule"]
    for rd in rule_rds:
        for j, c, ops in narrowed(rd):
            n = len(side["certs"]) + len(side["open"])
            item = {"claim": claim_id(rd, j), "tactic": f"NarrowingRun.open_{n}", "lean": c.lean, "source": rd.source, "fixture": True}
            out.append(f"theorem {item['tactic']} : ∀ run, {c.any_run} := by vacuous_by_narrowing")
            names.append(item["tactic"])
            side["open"].append(item)
    control_ids = {x["off"].id for x in controls if isinstance(x["off"], Reading)}
    out.append("\n-- ===== 5. which calls each claim is about, ACCORDING TO LEAN: the constructor of Frames.Calls its operation carries")
    for rd in list(readings) + [x["off"] for x in controls if isinstance(x["off"], Reading)]:
        pre = f"fun {group(rd.outer)} => " if rd.outer else ""
        for j, c in enumerate(rd.claims):
            out.append(f"#calls \"{claim_id(rd, j)}\" : {pre}({c.op}).calls")
        side["calls"][rd.id] = {"source": rd.source, "kind": rd.kind, "printed": printed(voc, rd.echo), "control": rd.id in control_ids,
                                "claims": [{"calls": c.calls, "clause": c.clause, "runs": c.runs} for c in rd.claims]}
    out.append("\n#narrowing_report " + " ".join(names))
    out.append("#print axioms Frames.Narrowed.holdsAt\n#print axioms Frames.Narrowed.holdsAt2")
    return "\n".join(out) + "\n", side


# --------------------------------------------------------------------------- printed coverage against the Calls value

def printed(voc, echo) -> list:
    """The coverage a reading PRINTS, as tokens: read off the echo by looking each line up among the `coverage:` texts of
    the book. ["covers", [kinds]] per clause, ["answer"] where an answer is required, ["two", kind] per two-call note,
    ["seq", kind] per sequence note, ["weak", kind] per stated weakening."""
    cov = voc.covers
    by = {(f, c[f]): k for k, c in cov.items() for f in TEXTS if f in c}
    asked = cov["every"]["answer_asked"].split("{words}")
    out = []
    for slot, text in echo:
        if slot == "covers":
            out.append(["covers", [by.get(("covers", t), "?") for t in text.split("; ")]])
        elif text == cov["every"]["answer"] or (text.startswith(asked[0]) and text.endswith(asked[1])):
            out.append(["answer"])
        elif ("two_calls", text) in by:
            out.append(["two", by[("two_calls", text)]])
        elif ("sequence", text) in by:
            out.append(["seq", by[("sequence", text)]])
        elif ("sequence_scenario", text) in by:
            out.append(["seq", by[("sequence_scenario", text)]])
        elif text.startswith("(of a sequence"):          # a note about a sequence that is not a line of the book: never a match
            out.append(["seq", "?"])
        elif slot == "not default" and ("weakening", text) in by:
            out.append(["weak", by[("weakening", text)]])
    return out


def expected(kind: str, claims: list, runs: list) -> list:
    """The coverage tokens a reading must print, given the Calls constructor of each claim and whether its operation is a
    sequence, both as Lean reported them (`claims`: [{calls, clause, seq}]), and how many calls each claim compares. The
    order is the echo's: clause by clause, then the weakenings. A Rule clause about a sequence prints one sequence note
    per Calls value in it; a scenario about a sequence prints the note of `every` (it always has a claim about every call)."""
    out, weak = [], []
    clauses = sorted({c["clause"] for c in claims}) if kind == "rule" else [None]
    for k in clauses:
        mine = [(c, r) for c, r in zip(claims, runs) if k is None or c["clause"] == k]
        kinds = list(dict.fromkeys(c["calls"] for c, _ in mine))
        out.append(["covers", kinds])
        if "every" in kinds:
            out.append(["answer"])
        if any(c.get("seq") for c, _ in mine):
            out += [["seq", x] for x in (kinds if kind == "rule" else ["every"])]
        out += [["two", x] for x in dict.fromkeys(c["calls"] for c, r in mine if r == 2)]
        weak += [x for x in kinds if x != "every" and x not in weak]
    return out + [["weak", x] for x in (weak if kind == "rule" else sorted(weak))]


def coverage_mismatches(side_calls: dict, lean_calls: dict, lean_seq: dict | None = None) -> list:
    """[(reading id, what differs)]: Claim.calls against the constructor Lean reported, and the printed coverage against the
    coverage the book gives for the constructors Lean reported. `lean_calls`: claim id -> constructor; `lean_seq`: claim id ->
    is its operation a sequence, according to Lean (absent: no claim is)."""
    lean_seq = lean_seq or {}
    bad = []
    for rid, s in side_calls.items():
        got = [lean_calls.get(f"{rid}#{j}") for j in range(len(s["claims"]))]
        if None in got or "?" in got:
            bad.append((rid, f"Lean reported no Calls value for claim(s) {[j for j, g in enumerate(got) if g in (None, '?')]}"))
            continue
        for j, (c, g) in enumerate(zip(s["claims"], got)):
            if c["calls"] != g:
                bad.append((rid, f"claim {j}: the compiler took the calls to be `{c['calls']}`, the emitted Lean says `{g}`"))
        want = expected(s["kind"], [{"calls": g, "clause": c["clause"], "seq": lean_seq.get(f"{rid}#{j}", False)}
                                    for j, (c, g) in enumerate(zip(s["claims"], got))], [c["runs"] for c in s["claims"]])
        if s["printed"] != want:
            bad.append((rid, f"printed coverage {json.dumps(s['printed'])} is not the coverage of the emitted Lean {json.dumps(want)}"))
    return bad


# --------------------------------------------------------------------------- reading the script's output back

def parse_log(log: str) -> tuple:
    calls, thms, seq = {}, {}, {}
    for line in log.splitlines():
        p = line.split("\t")
        if p[0] == "CALLS" and len(p) == 4 and p[3] in ("single", "sequence"):
            calls[p[1]] = p[2]
            seq[p[1]] = p[3] == "sequence"
        elif p[0] == "NARROWING" and len(p) >= 3:
            thms[p[1]] = {"state": p[2], "axioms": [a for a in (p[3] if len(p) > 3 else "").split(", ") if a]}
    return calls, thms, seq


def collect(side: dict, log: str) -> dict:
    """Everything the run concluded about narrowing: {ok, problems: [...], counts}."""
    calls, thms, seq = parse_log(log)
    problems = []
    # the report itself: a statement that does not elaborate is told apart from a script that fails, and a name that was
    # never declared from both. Without this, a must-fail attempt whose STATEMENT is broken would pass as "not provable".
    for name, want in ((BAD_STATEMENT, "badstatement"), (ABSENT, "missing")):
        got = thms.get(name, {}).get("state", "no result")
        if got != want:
            problems.append(f"THE REPORT DOES NOT TELL A BROKEN STATEMENT FROM A FAILED PROOF: `{name}` must be reported `{want}`; Lean: {got}")

    def state(name):
        return thms.get(name, {}).get("state", "no result")

    def std(name):         # a proof counts only on the standard axioms
        return set(thms.get(name, {}).get("axioms", [])) <= {"propext", "Classical.choice", "Quot.sound"}
    n_decl = n_undecl = 0
    for f in side["facts"]:
        what = f"`{f['op']}`, {f['kind']} calls: {f['key']}" + (f" `{f['cls']}`" if f["cls"] else "")
        s = state(f["name"])
        if f["declared"]:
            n_decl += 1
            if s != "proved" or not std(f["name"]):
                problems.append(f"DECLARED BUT NOT PROVED: the Clausebook says of {what}; Lean: {s} (`{f['lean']}`)")
        else:
            n_undecl += 1
            if s != "notproved":
                problems.append(("NOT DECLARED BUT PROVED: Lean proves of " if s == "proved" else f"NO ANSWER ({s}) for ")
                                + f"{what} (`{f['lean']}`); the `narrowing:` entry of the operation has to say so")
    for c in side["certs"]:
        for key, how in (("cert", f"through Frames.Narrowed.{c['theorem']}"), ("tactic", "by the fixed tactic")):
            s = state(c[key])
            if s != "proved" or not std(c[key]):
                problems.append(f"REFUSAL NOT PROVED {how}: {c['claim']} `{c['lean']}` is refused as holding of every operation; Lean: {s}")
    for o in side["open"]:
        s = state(o["tactic"])
        if s != "notproved":
            problems.append((f"SAYS NOTHING BUT WAS NOT REFUSED: {o['source']} {o['claim']} `{o['lean']}` holds for every `run` (kernel-checked)"
                             if s == "proved" else f"NO ANSWER ({s}) for the vacuity attempt on {o['source']} {o['claim']} `{o['lean']}`"))
    n_ref = n_comp = n_twice = 0
    for x in side["controls"]:
        tags = x["tags"]
        if "@narrowed-twice" in tags:      # more than one narrowing / scoping word on one clause: refused, with or without the Q1 refusal
            n_twice += 1
            if x.get("on_code") != "NARROWED-TWICE" or x.get("off_code") != "NARROWED-TWICE":
                problems.append(f"CONTROL NOT REFUSED: {x['source']} \"{x['text']}\" narrows one clause twice and must be refused as NARROWED-TWICE; "
                                f"the compiler said {x['on']} {x.get('on_code')} (refusal of vacuous claims off: {x['off']} {x.get('off_code')})")
            continue
        want = next((t.split(":", 1)[1] for t in tags if t.startswith("@says-nothing:")), None)
        if want is not None:
            n_ref += 1
            if x["on"] != STATUS:
                problems.append(f"CONTROL NOT REFUSED: {x['source']} \"{x['text']}\" must be refused as {STATUS}; the compiler said {x['on']}")
            elif f"Frames.Narrowed.{want}," not in x["message"]:
                problems.append(f"CONTROL REFUSED FOR ANOTHER REASON: {x['source']} \"{x['text']}\": expected theorem {want}; message: {x['message']}")
            if x["off"] != "COMPILED" or [c["theorem"] for c in x["certs"]] != [want]:
                problems.append(f"CONTROL WITHOUT ITS CERTIFICATE: {x['source']} \"{x['text']}\" compiled without the refusal: {x['off']}, "
                                f"vacuous claims {[c['theorem'] for c in x['certs']]} (expected exactly [{want}])")
        else:
            n_comp += 1
            if x["on"] != "COMPILED":
                problems.append(f"CONTROL REFUSED: {x['source']} \"{x['text']}\" must compile; the compiler said {x['on']}: {x['message']}")
            for t in tags:
                if t.startswith("@covers:"):
                    kinds = [c["calls"] for c in side["calls"].get(x["id"], {}).get("claims", [])]
                    if set(kinds) != {t.split(":", 1)[1]}:
                        problems.append(f"CONTROL COVERAGE: {x['source']} \"{x['text']}\" must be about {t.split(':', 1)[1]} calls; the compiler says {kinds}")
    cov_bad = coverage_mismatches(side["calls"], calls, seq)
    problems += [f"COVERAGE MISMATCH: {rid}: {what}" for rid, what in cov_bad]
    n_claims = sum(len(s["claims"]) for s in side["calls"].values())
    return {"ok": not problems, "problems": problems,
            "counts": {"facts_declared": n_decl, "facts_not_declared": n_undecl, "refused_claims": len(side["certs"]),
                       "narrowed_not_refused": len(side["open"]),
                       "narrowed_not_refused_fixture_rules": sum(1 for o in side["open"] if o["fixture"]),
                       "controls_refused": n_ref, "controls_compiled": n_comp, "controls_narrowed_twice": n_twice,
                       "readings": len(side["calls"]), "rule_readings": sum(1 for s in side["calls"].values() if s["kind"] == "rule"),
                       "fixture_rule_readings": sum(1 for s in side["calls"].values() if s["kind"] == "rule" and not s["control"]),
                       "fixture_scenario_readings": sum(1 for s in side["calls"].values() if s["kind"] == "scenario"),
                       "control_readings": sum(1 for s in side["calls"].values() if s["control"]),
                       "claims": n_claims, "calls_reported": sum(1 for rid, s in side["calls"].items() for j in range(len(s["claims"]))
                                                                   if f"{rid}#{j}" in calls),
                       "sequence_claims": sum(1 for rid, s in side["calls"].items() for j in range(len(s["claims"])) if seq.get(f"{rid}#{j}")),
                       "bad_statements": sorted(n for n, t in thms.items() if t["state"] == "badstatement" and n != BAD_STATEMENT),
                       "coverage_mismatches": len(cov_bad)},
            "theorems": thms, "calls": calls}
