"""clausal converse: THE DIALOGUE of composer version 2 (plan node L1d). An answer of the author REMOVES candidates and the
next question is asked, at most MAX_QUESTIONS times. With an ORACLE AUTHOR (someone who has the intended reading as a
sentence of the book and answers every question from it, mechanically) this is how an ASK is scored.

    python3 -m clausal converse "<rough English>" --gold "<the intended reading, a sentence of the book>" [--gold "..."]
                                [--domain D] [--json] [--max N]
    python3 -m clausal converse "<rough English>"              the same dialogue at the terminal: you answer

NO LANGUAGE MODEL IS USED. Nothing here chooses a reading: the composer (clausal/compose2.py) decides ANSWER / ASK /
DECLINE exactly as it does alone; this module turns an ASK into ONE question, takes ONE answer, and asks the composer
again with what the answer removed.

THE QUESTIONS (one per turn; each turn counts as one question, whatever its kind)
  system     "which system is your rule about?"                answer: a system         -> composed again in that system
  operation  "which operation is your rule about?"             answer: an operation id  -> composed again with --operation
  input      two candidates with full coverage differ at a concrete input of the grid (`relate`, the search of `clausal
             separate` run once for all the candidates compared): "should your rule hold at this input?"
                                                               answer: holds / fails    -> EVERY compared candidate that
             answers the other way at that input is removed (one that cannot be evaluated there is kept)
  which      two candidates with full coverage are not shown equal and no input of the grid separates them (NONE-FOUND,
             NOT-SEARCHED), or they are about operations with no common input: "read both; which do you mean?"
                                                               answer: one of them, or neither -> the other, or both, removed
  accept     no candidate has full coverage; up to three are shown with what each drops and adds (ASK (dropped)):
             "do you accept one of these as it is?"            answer: one of them (recorded as an ACKNOWLEDGEMENT by the
             author, with the dropped words: the dialogue ends there), or none -> all shown are removed, the next are shown

HOW IT ENDS
  ANSWER      the composer answers (one reading with full coverage is left, or those left are shown equal)
  CHOSEN      the author accepted a candidate of an ASK (dropped): chosen by the author, with the acknowledgement
  UNRESOLVED  the question limit is reached, or the author cannot answer (an input the intended reading has no value at)
  DECLINE     the composer declines (also: every candidate has been turned down)

THE ORACLE AUTHOR (`Oracle`). Given the intended reading as one or more sentences of the book (alternatives; each must
compile), it answers
  system, operation   the system and the (first) operation of the first gold sentence
  input               the value of the FIRST gold sentence at the input, on the Lean model, through the same search (`relate`);
                      "cannot say" if the input is not an input of the gold reading (another operation, another grid)
  which, accept       the candidate that IS a gold reading: the same Lean term as a gold sentence, or proved equal to one
                      by Lean's kernel (the equality scripts of `clausal separate`); none if there is none
It never looks at the rough sentence and never prefers a candidate for its wording. WHAT IT IS NOT: a person. A person
answering "should your rule hold here" can be wrong, and can accept a candidate that is not what they meant; the
oracle cannot. The numbers it gives are an upper bound on what the questions can do for a careful author.

WHAT "ENDS AT THE GOLD READING" MEANS (`at_gold`): the sentence the dialogue ends with is the same term as a gold
sentence, or proved equal to one. An ANSWER that survives every question and is NOT that (it agrees with the gold
reading on every input asked about, and differs elsewhere, or is only not separated on the grid) is reported as
`ended at another reading`, with the verdict of the comparison with the gold (SEPARATED: wrong; NONE-FOUND: not shown).
"""
from __future__ import annotations

import hashlib
import json
import sys

from . import compose2, rsearch, separate
from .core import Feature, FeatureError, Problem, Rule

MAX_QUESTIONS = 3
COMPARED = compose2.L3_PAIRS        # full candidates compared at a reading question, best-ranked first
SCHEMA = "clausal-dialogue-v1"


# --------------------------------------------------------------------------------------------- comparing readings

def compile_as(comp, sentence: str, system, ident: str):
    """The ordinary compiler on one Rule line, with a reading id of its own (several readings go into one Lean file)."""
    f = Feature(path="<dialogue>", name="dialogue", slug="dialogue")
    return comp.rule(Rule(feature=f, name=sentence, line=1, tags=[f"@id:{ident}"]), system)


_RELATED = {}


class Related:
    """Several compiled readings searched on the grid in ONE Lean run, with one kernel attempt at `A <-> B` per pair asked
    for. Everything is `clausal separate`'s: the script (`separate.lean_script`), the run, the parse, the comparison of two
    readings on their common grid (`separate.compare`), the equality scripts. No Rust is run here: the questions of a
    dialogue are answered on the Lean model (the composer's own ASK (reading) output shows the compiled Rust too)."""

    def __init__(self, voc, readings: list, pairs: list, prove: bool = True):
        self.voc, self.rds, self.pairs = voc, readings, [tuple(p) for p in pairs]
        self.terms = [separate.term(rd) for rd in readings]
        self.eq = [(i, j) for i, j in self.pairs if prove and self.terms[i] != self.terms[j]
                   and readings[i].state_type == readings[j].state_type and readings[i].input_type == readings[j].input_type]
        self.rs, self.side, self.log, self.work, self.ran = {}, {}, "", None, False
        if all(self.terms[i] == self.terms[j] for i, j in self.pairs) and self.pairs:
            return                               # equal as terms: nothing to search
        digest = hashlib.sha256(json.dumps([self.terms, self.pairs, prove]).encode()).hexdigest()[:12]
        if digest in _RELATED:
            self.rs, self.side, self.log, self.work = _RELATED[digest]
            self.ran = True
            return
        self.work = separate.WORK.parent / "dialogue" / digest
        self.work.mkdir(parents=True, exist_ok=True)
        text, self.side = separate.lean_script(voc, list(readings), [(readings[i], readings[j]) for i, j in self.eq])
        self.log = separate.run_lean(self.work, text)
        self.rs = rsearch.parse(self.log, self.side) if "RSEARCH" in self.log else {}
        self.ran = True
        _RELATED[digest] = (self.rs, self.side, self.log, self.work)

    def searched(self, i: int) -> bool:
        return "bits" in (self.rs.get(self.rds[i].id) or {})

    def verdict(self, i: int, j: int) -> dict:
        """The verdict of `clausal separate` for readings i and j: SAME-TERM, PROVED-EQUAL, SEPARATED (with the first input of
        each direction), NONE-FOUND, DIFFERENT-OPERATIONS, NOT-SEARCHED."""
        if self.terms[i] == self.terms[j]:
            return {"verdict": "SAME-TERM", "points": []}
        a, b = self.rds[i], self.rds[j]
        if not (self.searched(i) and self.searched(j)):
            return {"verdict": "NOT-SEARCHED", "points": [],
                    "why": "; ".join((self.rs.get(r.id) or {}).get("skipped", "Lean printed no result (see the log)") for r in (a, b))}
        got = None
        if a.info["domain"] == b.info["domain"]:
            got = separate.compare(self.rs[a.id], self.rs[b.id], self.side[a.id], self.side[b.id])
        if got is None:
            return {"verdict": "DIFFERENT-OPERATIONS", "points": []}
        points = [{"values": got["first"][w]["values"], "holds": h, "fails": f}
                  for w, h, f in (("a_only", i, j), ("b_only", j, i)) if got["first"][w]]
        if points:
            return {"verdict": "SEPARATED", "points": points, "bounds": got["bounds"]}
        k = next((n for n, p in enumerate(self.eq) if p == (i, j)), None)
        by = separate.proved(self.log, k) if k is not None else None
        if by:
            return {"verdict": "PROVED-EQUAL", "points": [], "by": by}
        return {"verdict": "NONE-FOUND", "points": [], "bounds": got["bounds"]}

    def second_vars(self) -> list:
        """The grid variables that build a SECOND call in some reading here (a reading that compares two calls)."""
        return sorted(set().union(*(separate.second_call_vars(self.side[rd.id]) for rd in self.rds if rd.id in self.side)) if self.side else set())

    def holds_at(self, i: int, values: dict, second=()):
        """Does reading i hold at the input `values` ({grid variable: value})? None if the input is not a point of its grid
        (a variable of its own is missing from `values`, or a value is not on its grid, or the input has a variable the
        reading does not take): it cannot be evaluated there. `second`: variables of `values` that build the second call of
        a reading that compares two calls; a reading about one call is evaluated at the first call (as `separate.align`)."""
        if not self.searched(i):
            return None
        r, vars_ = self.rs[self.rds[i].id], self.side[self.rds[i].id]["vars"]
        idx = []
        for n, vals in vars_:
            if n not in values or values[n] not in list(vals):
                return None
            idx.append(list(vals).index(values[n]))
        if set(values) - {n for n, _ in vars_} - set(second) - set(self.second_vars()):
            return None                          # the input has a variable this reading does not take: not the same call
        return separate.holds(r, separate.point_bits(r, separate.flat(idx, [len(v) for _, v in vars_])))


def equal(v: dict) -> bool:
    return v["verdict"] in ("SAME-TERM", "PROVED-EQUAL")


# --------------------------------------------------------------------------------------------- the authors

class Oracle:
    """The oracle author: answers every question from the intended reading (see the module text)."""
    name = "oracle"

    def __init__(self, gold: list, system: str | None = None):
        self.voc, self.comp = compose2.load()
        self.sentences = list(gold)
        self.rds = []
        for k, s in enumerate(gold):
            rd = compile_as(self.comp, s, system, f"gold{k}")
            if isinstance(rd, Problem):
                raise FeatureError(f"the gold sentence does not compile: {s!r}: {rd.message}")
            self.rds.append(rd)
        self.terms = [separate.term(rd) for rd in self.rds]
        self.lean_runs = 0

    def system(self, systems: list):
        return self.rds[0].info["domain"]

    def operation(self, operations: list):
        return self.rds[0].info["clauses"][0]["ops"][0]["id"]

    def at_input(self, values: dict, second=()):
        rel = Related(self.voc, [self.rds[0]], [])
        self.lean_runs += rel.ran
        got = rel.holds_at(0, values, second)
        return None if got is None else "holds" if got else "fails"

    def is_gold(self, cands: list) -> list:
        """Per candidate ({sentence, system}): the verdict against the gold sentences, the best of them first
        (SAME-TERM, PROVED-EQUAL, then whatever the first gold gives)."""
        rds = [compile_as(self.comp, c["sentence"], c.get("system"), f"cand{k}") for k, c in enumerate(cands)]
        out = [None] * len(cands)
        for k, rd in enumerate(rds):
            if isinstance(rd, Problem):
                out[k] = {"verdict": "DOES-NOT-COMPILE", "points": []}
            elif separate.term(rd) in self.terms:
                out[k] = {"verdict": "SAME-TERM", "points": []}
        todo = [k for k in range(len(cands)) if out[k] is None]
        if todo:
            n = len(self.rds)
            rel = Related(self.voc, self.rds + [rds[k] for k in todo], [(g, n + x) for x in range(len(todo)) for g in range(n)])
            self.lean_runs += rel.ran
            for x, k in enumerate(todo):
                vs = [rel.verdict(g, n + x) for g in range(n)]
                out[k] = next((v for v in vs if equal(v)), vs[0])
        return out

    def pick(self, cands: list):
        """The (first) candidate that is a gold reading, or None."""
        return next((k for k, v in enumerate(self.is_gold(cands)) if equal(v)), None)

    which = pick
    accept = pick


class Terminal:
    """A person at the terminal. Every question is printed by `converse`; this reads the answer."""
    name = "terminal"
    lean_runs = 0

    def ask(self, prompt, ok):
        while True:
            got = input(prompt + " ").strip().lower()
            if ok(got):
                return got

    def system(self, systems):
        return self.ask(f"Which system? [{' / '.join(systems)}]", lambda g: g in systems)

    def operation(self, operations):
        ids = [o["id"] for o in operations]
        return self.ask(f"Which operation? [{' / '.join(ids)}]", lambda g: g in [i.lower() for i in ids])

    def at_input(self, values, second=()):
        got = self.ask("Should your rule hold at this input? [holds / fails / cannot say]", lambda g: g in ("holds", "fails", "cannot say"))
        return None if got == "cannot say" else got

    def which(self, cands):
        got = self.ask(f"Which do you mean? [1-{len(cands)}, or n for neither]", lambda g: g == "n" or g.isdigit() and 1 <= int(g) <= len(cands))
        return None if got == "n" else int(got) - 1

    accept = which


# --------------------------------------------------------------------------------------------- the dialogue

def brief(c: dict) -> dict:
    return {"sentence": c["sentence"], "system": c["system"], "term_sha256": c["term_sha256"], "operations": c["operations"],
            "dropped": c["coverage"]["dropped"], "added": c["coverage"]["added"], "condition_dropped": c["coverage"]["condition_dropped"]}


def reading_question(voc, comp, cands: list):
    """For candidates with full coverage that the composer could not tell apart without a search: compare the first
    COMPARED of them. Returns ("one", candidate) if they are one reading, or ("input" | "which", question)."""
    top = cands[:COMPARED]
    rds = [compile_as(comp, c["sentence"], c["system"], f"cand{k}") for k, c in enumerate(top)]
    pairs = [(i, j) for i in range(len(top)) for j in range(i + 1, len(top))]
    rel = Related(voc, rds, pairs)
    vs = {p: rel.verdict(*p) for p in pairs}
    if len(cands) <= COMPARED and all(equal(v) for v in vs.values()):
        return "one", top[0], rel
    # the first pair that is separated by an input; else the first pair not shown equal
    for (i, j), v in vs.items():
        if v["verdict"] == "SEPARATED":
            p = v["points"][0]
            at = {k: rel.holds_at(k, p["values"]) for k in range(len(top))}
            return "input", {"kind": "input", "values": p["values"], "between": [i, j], "second_call_variables": rel.second_vars(),
                             "holds": [k for k, h in at.items() if h is True], "fails": [k for k, h in at.items() if h is False],
                             "not_evaluated": [k for k, h in at.items() if h is None], "candidates": [brief(c) for c in top]}, rel
    (i, j), v = next(((p, v) for p, v in vs.items() if not equal(v)), (pairs[0], vs[pairs[0]]))
    return "which", {"kind": "which", "verdict": v["verdict"], "between": [i, j], "candidates": [brief(top[i]), brief(top[j])]}, rel


def converse(rough: str, author, domain: str | None = None, max_questions: int = MAX_QUESTIONS, operation: str | None = None,
             say=None) -> dict:
    """The dialogue on one rough sentence. `author`: an object with system / operation / at_input / which / accept.
    `say`: a function that is given each question as text (the terminal), or None."""
    voc, comp = compose2.load()
    exclude, turns = set(), []
    out = {"schema": SCHEMA, "rough": rough, "author": author.name, "max_questions": max_questions, "turns": turns, "end": None,
           "sentence": None, "system": None, "term_sha256": None, "acknowledgement": None, "why": None, "lean_runs": 0}

    def end(kind, c=None, why=None, ack=None):
        out.update(end=kind, why=why, questions=len(turns), acknowledgement=ack)
        if c is not None:
            out.update(sentence=c["sentence"], system=c["system"], term_sha256=c["term_sha256"], operations=c["operations"],
                       coverage={k: c["coverage"][k] for k in ("dropped", "added", "condition_dropped", "full")})
        out["lean_runs"] += getattr(author, "lean_runs", 0)
        return out

    while True:
        res = compose2.compose(rough, domain, l3=False, operation=operation, exclude=frozenset(exclude))
        out["last_outcome"] = res["outcome"] + (f" ({res['ask']})" if res["ask"] else "")
        if res["outcome"] == "ANSWER":
            return end("ANSWER", res["answer"], res["why"])
        if res["outcome"] == "DECLINE":
            return end("DECLINE", None, res["why"])
        full = res["ask"] == "reading"
        q = rel = None
        if full:
            # the composer was asked without the search (l3=False): the search is run here, once, for the candidates compared
            cands = res["candidates"] if len(res["candidates"]) >= 2 else res["candidates"]
            kind, q, rel = reading_question(voc, comp, cands)
            out["lean_runs"] += rel.ran
            if kind == "one":
                return end("ANSWER", q, "the candidates with full coverage that are left are shown equal: one reading")
        if len(turns) >= max_questions:
            return end("UNRESOLVED", None, f"the limit of {max_questions} questions is reached; still open: ASK ({res['ask']})")
        if res["ask"] == "system":
            ans = author.system(res["systems"])
            turns.append({"kind": "system", "systems": res["systems"], "answer": ans})
            if say:
                say(f"QUESTION {len(turns)} (system): {res['why']}\n  answer: {ans}")
            if ans not in res["systems"]:
                return end("UNRESOLVED", None, f"the author's system ({ans}) is not one the sentence names an operation of ({', '.join(res['systems'])})")
            domain = ans
        elif res["ask"] == "operation":
            ops = res["operation_question"]["operations"]
            ans = author.operation(ops)
            turns.append({"kind": "operation", "operations": [o["id"] for o in ops], "answer": ans})
            if say:
                say(f"QUESTION {len(turns)} (operation): {res['why']}\n  answer: {ans}")
            if ans not in [o["id"] for o in ops]:
                return end("UNRESOLVED", None, f"the author's operation ({ans}) is not one of the operations offered")
            operation = ans
        elif res["ask"] == "dropped":
            shown = res["candidates"]
            if say:
                say(f"QUESTION {len(turns) + 1} (accept): no sentence accounts for every word of yours. Do you accept one of these as it is?\n"
                    + "\n".join(f"  [{k + 1}] {c['sentence']}\n" + "\n".join(compose2.say_cov(c)) for k, c in enumerate(shown)))
            k = author.accept([brief(c) for c in shown])
            turns.append({"kind": "accept", "shown": [brief(c) for c in shown], "answer": None if k is None else k + 1})
            if k is not None:
                c = shown[k]
                ack = {"candidate": k + 1, "sentence": c["sentence"], "term_sha256": c["term_sha256"], "by": author.name,
                       "dropped_words": c["coverage"]["dropped"], "added_pieces": c["coverage"]["added"],
                       "conditions_dropped": c["coverage"]["condition_dropped"],
                       "what": "the author's answer in a dialogue, as the harness recorded it; not a signature"}
                return end("CHOSEN", c, "the author accepted a candidate that does not account for every word, with what it drops and adds listed", ack)
            exclude |= {c["term_sha256"] for c in shown}
        elif q["kind"] == "input":
            top = cands[:COMPARED]
            if say:
                say(f"QUESTION {len(turns) + 1} (input): candidates differ at the input {separate.say_values(q['values'])}:\n"
                    + "\n".join(f"  [{k + 1}] {'HOLDS' if k in q['holds'] else 'FAILS' if k in q['fails'] else 'not evaluated'} there: {c['sentence']}" for k, c in enumerate(top)))
            ans = author.at_input(q["values"], q["second_call_variables"])
            turns.append(dict(q, answer=ans))
            if ans is None:
                return end("UNRESOLVED", None, "the author cannot say whether the rule holds at the separating input (it is not an input of the intended reading)")
            gone = q["fails"] if ans == "holds" else q["holds"]
            exclude |= {top[k]["term_sha256"] for k in gone}
        else:
            pair = [cands[k] for k in q["between"]]
            if say:
                say(f"QUESTION {len(turns) + 1} (which): these are not shown equal and no input of the grid separates them ({q['verdict']}). Which do you mean?\n"
                    + "\n".join(f"  [{k + 1}] {c['sentence']}" for k, c in enumerate(pair)))
            k = author.which([brief(c) for c in pair])
            turns.append(dict(q, answer=None if k is None else k + 1))
            exclude |= {c["term_sha256"] for n, c in enumerate(pair) if n != k}


def resolve(sentences: list, author, max_questions: int = MAX_QUESTIONS, systems=None) -> dict:
    """The reading questions alone, on a GIVEN list of candidate sentences of the book (no rough sentence, no coverage): how a
    dialogue among them ends. A sentence two systems read is one candidate per system. Used on the clausal/separate_tests
    cases: the candidates are the case's sentences, the intended reading is one of them."""
    voc, comp = compose2.load()
    cands = []
    for n, s in enumerate(sentences):
        for c in separate.candidates(voc, comp, s, f"c{n}"):     # once per system, as `clausal separate` compiles a sentence
            if c["compiled"] and (systems is None or c["domain"] in systems):
                rd = c["reading"]
                if not any(x["term"] == separate.term(rd) and x["system"] == c["domain"] for x in cands):
                    cands.append({"sentence": s, "system": c["domain"], "term": separate.term(rd), "rd": rd, "operations": separate.op_ids(rd)})
    turns = []
    out = {"schema": SCHEMA, "candidates": [{"sentence": c["sentence"], "system": c["system"]} for c in cands], "turns": turns, "end": None,
           "sentence": None, "system": None}
    live = list(range(len(cands)))

    def end(kind, k=None, why=None):
        out.update(end=kind, why=why, questions=len(turns))
        if k is not None:
            out.update(sentence=cands[k]["sentence"], system=cands[k]["system"])
        return out

    while True:
        if not live:
            return end("DECLINE", None, "every candidate has been turned down")
        if len(live) == 1:
            return end("ANSWER", live[0], "one candidate is left")
        # the system first, as the composer asks it: before anything is compared
        sysv = sorted({cands[k]["system"] for k in live})
        if len(sysv) > 1:
            if len(turns) >= max_questions:
                return end("UNRESOLVED", None, "the question limit is reached")
            ans = author.system(sysv)
            turns.append({"kind": "system", "systems": sysv, "answer": ans})
            live = [k for k in live if cands[k]["system"] == ans]
            continue
        rel = Related(voc, [cands[k]["rd"] for k in live], [(i, j) for i in range(len(live)) for j in range(i + 1, len(live))])
        vs = {(i, j): rel.verdict(i, j) for i in range(len(live)) for j in range(i + 1, len(live))}
        if all(equal(v) for v in vs.values()):
            return end("ANSWER", live[0], "the candidates left are shown equal (" + ", ".join(sorted({v['verdict'] for v in vs.values()})) + "): one reading")
        if len(turns) >= max_questions:
            return end("UNRESOLVED", None, "the question limit is reached")
        sep = next(((p, v) for p, v in vs.items() if v["verdict"] == "SEPARATED"), None)
        if sep:
            (i, j), v = sep
            values = v["points"][0]["values"]
            at = {n: rel.holds_at(n, values) for n in range(len(live))}
            ans = author.at_input(values, rel.second_vars())
            turns.append({"kind": "input", "values": values, "holds": [live[n] for n, h in at.items() if h is True],
                          "fails": [live[n] for n, h in at.items() if h is False], "answer": ans})
            if ans is None:
                return end("UNRESOLVED", None, "the author cannot say whether the rule holds at the separating input")
            live = [live[n] for n in range(len(live)) if at[n] is None or at[n] is (ans == "holds")]
            continue
        (i, j), v = next((p, v) for p, v in vs.items() if not equal(v))
        if v["verdict"] == "DIFFERENT-OPERATIONS":
            # no common input: the composer's question for such a pair is which operation the rule is about
            ops = [{"id": cands[live[n]]["operations"][0][0]} for n in (i, j)]
            ans = author.operation(ops)
            turns.append({"kind": "operation", "operations": [o["id"] for o in ops], "answer": ans})
            keep = [n for n in (i, j) if cands[live[n]]["operations"][0][0] == ans]
        else:
            k = author.which([{"sentence": cands[live[n]]["sentence"], "system": cands[live[n]]["system"]} for n in (i, j)])
            turns.append({"kind": "which", "verdict": v["verdict"], "between": [live[i], live[j]], "answer": None if k is None else k + 1})
            keep = [] if k is None else [(i, j)[k]]
        live = [live[n] for n in range(len(live)) if n not in (i, j) or n in keep]


def at_gold(out: dict, oracle: Oracle) -> dict:
    """Is the sentence a dialogue ended with a gold reading? {verdict, at_gold}."""
    if out.get("sentence") is None:
        return {"verdict": None, "at_gold": False}
    v = oracle.is_gold([{"sentence": out["sentence"], "system": out.get("system")}])[0]
    return {"verdict": v["verdict"], "at_gold": equal(v)}


def render(out: dict) -> str:
    o = [f"Rough sentence: {out['rough']}", f"author: {out['author']}; questions asked: {out['questions']} (limit {out['max_questions']})"]
    for n, t in enumerate(out["turns"], 1):
        if t["kind"] == "input":
            o.append(f"  {n}. input {separate.say_values(t['values'])}: should the rule hold there? -> {t['answer'] or 'cannot say'}")
        elif t["kind"] == "accept":
            o.append(f"  {n}. accept one of {len(t['shown'])} candidates that drop or add something? -> " + (f"candidate {t['answer']}" if t["answer"] else "none"))
            o += [f"       [{k + 1}] {c['sentence']}" + (f"   (dropped: {', '.join(c['dropped'])})" if c["dropped"] else "")
                  + (f"   (added: {', '.join(c['added'])})" if c["added"] else "") for k, c in enumerate(t["shown"])]
        elif t["kind"] == "which":
            o.append(f"  {n}. which of two candidates not shown equal ({t['verdict']})? -> " + (f"candidate {t['answer']}" if t["answer"] else "neither"))
        else:
            o.append(f"  {n}. {t['kind']}? -> {t['answer']}")
    o.append(f"{out['end']}: " + (f"\"{out['sentence']}\"" if out["sentence"] else "no sentence") + f". {out['why']}")
    if out.get("gold"):
        o.append(f"against the gold reading: {out['gold']['verdict']}" + (" (ends at the gold reading)" if out["gold"]["at_gold"] else " (NOT the gold reading)"))
    return "\n".join(o)


def main(argv) -> int:
    argv = list(argv)
    gold, domain, mx = [], None, MAX_QUESTIONS
    while "--gold" in argv:
        i = argv.index("--gold")
        gold.append(argv[i + 1])
        del argv[i:i + 2]
    if "--domain" in argv:
        i = argv.index("--domain")
        domain = argv[i + 1]
        del argv[i:i + 2]
    if "--max" in argv:
        i = argv.index("--max")
        mx = int(argv[i + 1])
        del argv[i:i + 2]
    as_json = "--json" in argv
    rest = [a for a in argv if not a.startswith("--")]
    if len(rest) != 1:
        print(__doc__)
        return 2
    try:
        author = Oracle(gold) if gold else Terminal()
        out = converse(rest[0], author, domain, mx, say=None if gold else print)
        if gold:
            out["gold"] = dict(at_gold(out, author), sentences=gold)
    except FeatureError as e:
        print(f"clausal converse: {e}", file=sys.stderr)
        return 1
    print(json.dumps(out, indent=1, ensure_ascii=False) if as_json else render(out))
    return {"ANSWER": 0, "CHOSEN": 0, "UNRESOLVED": 4, "DECLINE": 3}[out["end"]]
