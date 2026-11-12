"""clausal compose2: composer VERSION 2, first part (plan nodes L1a, L1b; the tree interface L1e is clausal/ctree.py).

    python3 -m clausal compose2 "<rough English>" [--domain D] [--json] [--no-l3]
                                                  [--acknowledge K --by NAME] [--write FILE.feature]

NO LANGUAGE MODEL IS USED. Version 1 (clausal/compose.py, `clausal compose`) is unchanged and is still what arm A0 measures;
this module uses its generator, its ranking rule and its cue table AS THEY ARE (nothing of them is retuned here) and
changes what is done with the candidates. Design: docs/studies/2026-11-12/composer-v2.md sections 4.1 and 4.2; notes and
measurements: clausal/COMPOSE2.md.

THREE OUTCOMES, decided mechanically. No score threshold is used anywhere.

  ANSWER   one sentence. Either the rough sentence IS a sentence of the book (it compiles as written: it is its own
           answer), or exactly one reading survives: every candidate that passes the filters and has FULL COVERAGE is the
           same Lean term, or is shown equal to the others by `clausal separate` (SAME-TERM / PROVED-EQUAL).
  ASK      system   the operation named is an operation of two systems and no word of the sentence that only one of them
                    has settles which. Asked BEFORE anything is generated.
           reading  two or more full-coverage candidates are not shown equal: the separating inputs of `clausal separate`
                    are shown (NONE-FOUND and NOT-SEARCHED also ask).
           dropped  no candidate has full coverage, and at least one candidate is ASKABLE (below): "your sentence also says
                    X; this sentence does not. Accept without it?". Nothing is chosen without a recorded acknowledgement.
  DECLINE  no operation is anchored (version 1 then tried every operation; version 2 never does; an operation is anchored by
           EVERY word of one of its nouns, or by the verb of its `when` form), or no candidate is askable.
           Printed: the words nothing accounts for, the nearest pieces, and the kind of missing piece if a phrase names it.

FILTERS, before any outcome (a candidate that fails one is counted and never shown):
  refused            the compiler refuses the sentence (this includes Q1: a narrowed claim that says nothing)
  other-book         the sentence uses an entry of a book that the project of its operation does not list (projects.yaml):
                     `clausal gen` would stop on it in that project's feature file
  opposite-narrowing the subject is narrowed to accepted (or rejected) calls and a claim says of them the class the
                     narrowing excludes ("a rejected transfer is always accepted", "an accepted transfer is rejected and
                     changes nothing"); decided with `narrowing.polarity`, the book's own `narrowing:` facts
  by-zero            "increases / decreases ... by exactly zero": the book's sentence for that is "never changes ..."
  same-sides         a piece whose two holes are filled with the same term ("the sender ... equals the sender ...")

COVERAGE ACCOUNTING (`coverage`). Every word of the rough sentence that is not on STOP2 (articles and auxiliaries,
printed with every result) gets EXACTLY ONE status against a candidate:
  MAPPED   to one piece instance of the candidate, `via`
             form   the word is a word the candidate's sentence writes for that piece (matched occurrence by occurrence:
                    a word said twice in the rough sentence needs two occurrences in the candidate)
             cue    the word is in version 1's cue table for that piece (compose.CUES), and the piece has not already
                    accounted for as many words as its own form has (CUE CAPACITY: a piece cannot absorb a clause)
             noun   the word is a word of another noun the book gives the candidate's operation ("fund transfer")
             when   the word is the verb of the operation's `when` form (how an operation is anchored without its noun)
             opener the word opens a condition span (below) that is matched with a condition of the candidate
  DEFAULT  the word belongs to a phrase that a NAMED DEFAULT of the candidate's reading covers (DEFAULT_PHRASES)
  DROPPED  nothing of the candidate accounts for it
and the reverse: every piece instance of the candidate that no word is mapped to is ADDED. A role or literal counts as a
piece here when it was a CHOICE ("the sender" where "the receiver" could stand; "the amount" as the term of a claim; a
number). Exempt: a role that is the one filler of its hole ("of the ledger"), pieces a form implies, pieces whose form
writes no word of its own, grammar words. The function asserts the partition.
  CONDITION SPANS. A word of OPENERS ("if", "when", "unless", "only", "for which", "that", ...) opens a span, to the next
  opener or punctuation mark, unless it is a form word of the candidate that introduces no condition there ("only" of
  "only X and Y change", "that" of "never loses that ..."). Each span must be matched,
  one to one, with a CONDITION UNIT of the candidate (a narrowing word; "for which" and its condition; a frame's
  condition, variation or first-call class) that some word of the span is mapped to. A span left over is printed as
  CONDITION DROPPED, whatever the statuses of its words.
  FULL COVERAGE = no DROPPED word, no ADDED piece, no CONDITION DROPPED. Only a full candidate can be an ANSWER.
  A narrowing word written before the operation's noun ("an accepted lookup") is a span of one word: a candidate that
  turns it into a claim ("a lookup is always accepted") has dropped a condition.
  ASKABLE = the candidate's operation is not ADDED and every claim of it has a word of the author's mapped into it: what
  the candidate claims, and of what, is something the author's words ask for. (A candidate with a claim no word asks for
  is not put to the author as a question.)

ACKNOWLEDGEMENT. `--acknowledge K --by NAME` records that NAME accepts candidate K of an ASK (dropped) with its dropped
words, added pieces and dropped conditions listed. The record is part of the result and, with --write, of the sidecar
`<FILE>.compose.json` (one record per composed rule, keyed by the digest of its Lean term). It is the harness's
statement of what was run and typed, not a cryptographic one. Without it nothing with a dropped word is ever chosen.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from . import compose as v1
from . import ctree, narrowing, projects, vocab
from .core import FeatureError, Problem
from .pipeline import ROOT
from .vocab import Leaf, Node, base_cat, hole_voice, segments

SCHEMA = "clausal-compose-v2"
SHOW = 3                 # candidates shown with an ASK
L3_PAIRS = 3             # full candidates compared pairwise by `clausal separate` before an ANSWER
COMPILE_LIMIT = v1.COMPILE_LIMIT

# THE STOP LIST OF VERSION 2: articles and auxiliaries, nothing else. (Version 1's list also had prepositions, pronouns,
# "and", "or", "than", "then": every one of those is a content word here and gets a status.)
STOP2 = frozenset("a an the "
                  "is are am be been being was were do does did will would shall should must can could may might has have had".split())

# Words that open a condition span (study 4.2), longest first. "that" and "which" alone are this module's addition: a
# relative clause ("a withdrawal that fails") narrows the subject as "for which" does.
OPENERS = [("as", "long", "as"), ("for", "which"), ("only", "if"), ("only", "when"), ("that", "is"), ("that", "are"),
           ("if",), ("when",), ("whenever",), ("unless",), ("only",), ("provided",), ("whose",), ("that",), ("which",)]
BOUNDARY = {",", ";", ":"}

# PHRASES A NAMED DEFAULT COVERS. Each line: the default, a pattern over the lower-cased words of the rough sentence, and why
# the default's text (clausebook/core.yaml `defaults:`) covers it. A phrase counts only if the candidate's reading APPLIES that
# default (it is among the reading's printed defaults), so "whether accepted or rejected" is not covered by a narrowed candidate.
DEFAULT_PHRASES = [
    # D2 "rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects it"
    ("D2", r"\bwhether (?:or not )?(?:it |they )?(?:is |are |was |gets )?(?:accepted|successful|succeeds|succeed) or (?:it |they )?(?:is |are )?(?:rejected|refused|not|fails|fail|failed)\b"),
    ("D2", r"\b(?:accepted|successful) or (?:rejected|refused|not)\b"),
    ("D2", r"\bin (?:every|all|any|either) cases?\b"),
    # D4 "for all values: ... every state and every input is universally quantified at the front"
    ("D4", r"\balways\b"),
    ("D4", r"\b(?:any|every|all|each|whatever|whichever)(?= (?:the )?(?:%ROLES%)\b)"),
    # D3 "before / after one call: ... compare the state before one call with the state after it"
    ("D3", r"\bafterwards?\b"),
    ("D3", r"\b(?:before|after) (?:the|that|this|each|every|any|a|one) (?:call|operation)\b"),
]

# PHRASES THAT NAME A KIND OF PIECE THE BOOK DOES NOT HAVE (clausebook/l2/FREEZE.md, the rows judged "add later" or "compose").
# Advisory: printed with a DECLINE or an ASK, never used to decide an outcome.
MISSING_KINDS = [
    (r"\b(?:any|every|no) (?:sequence|series|number) of\b|\bstarting from\b|\bhowever many\b", "a claim about any sequence of operations (an invariant of the state): the book states one call, or two in sequence"),
    (r"\beither\b.*\bor\b", "an either / or between two claims: the book joins claims with 'and' only"),
    (r"\bboth\b.*\band\b|\bneither\b.*\bnor\b", "a conjunction of two conditions: the book has one condition per clause"),
    (r"\bsame (?:state|result|outcome|ledger|balances?) as\b|\bas if\b", "a comparison of two sequences of calls: the book compares two calls of one operation"),
    (r"\botherwise\b", "an if / otherwise: write two clauses, one per case"),
]


# --------------------------------------------------------------------------------------------- the words of a sentence

def lex(text: str) -> list:
    """[(word, boundary before it?)] of a text, lower-cased; "n't" and "cannot" are written out as "not"."""
    t = text.lower().replace("cannot", "can not")
    t = re.sub(r"n['’]t\b", " not", t).replace("’", "'")
    out, bound = [], False
    for m in re.finditer(r"[a-z]+(?:'s)?|\d+|[,;:]", t):
        w = m.group(0)
        if w in BOUNDARY:
            bound = True
            continue
        out.append((w, bound))
        bound = False
    return out


def content(w: str) -> bool:
    return w not in STOP2 and not (w.endswith("'s") and w[:-2] in STOP2)


def stems(text: str) -> list:
    """The stemmed content words of a text, every occurrence. (A form writes "{w:wallet}'s balance": the "'s" left of a
    hole is no word.)"""
    return [v1.stem(w) for w, _ in lex(re.sub(r"(^|\s)'s\b", " ", text)) if content(w)]


# --------------------------------------------------------------------------------------------- the pieces of a candidate

@dataclass
class Inst:
    """One piece instance of a candidate sentence, with the words the sentence writes for it."""
    n: int
    id: str
    kind: str                 # op | narrowing | given | piece | frame | idiom | choice | leaf | implied | silent | grammar
    words: list               # stems of its content words, as written
    neg: bool = False
    units: list = field(default_factory=list)      # the condition units it belongs to
    taken: int = 0            # rough words mapped to it
    connectives: set = field(default_factory=set)  # the words its form writes just before a condition hole ("whenever", "when")
    claim: int | None = None  # which claim of the sentence it is part of (None: the subject)


def literal(form: str) -> str:
    return " ".join(s[1] for s in segments(form) if s[0] == "lit")


class Pieces:
    """The piece instances of a compiled Rule line, in the order written, and its condition units."""

    def __init__(self, voc, rd):
        self.voc, self.items, self.units, self.roles, self.claim, self.claims = voc, [], 0, {}, None, 0
        word_mod = {w.strip(): m for w, m in voc.subject_words}
        clauses = rd.info["clauses"]
        for k, g in enumerate(clauses):
            if k:
                self.add("g.clauses", "grammar", voc.clause_seps[0])
            s = g["s"]
            self.roles = s["roles"]
            for j, (_, ws, noun) in enumerate(s["written"]):
                if j:
                    self.add("and_then", "piece", voc.sequences[0])
                for w in ws:
                    self.add(word_mod[w], "narrowing", w, [self.unit()])
                self.add(g["ops"][j]["id"], "op", noun)
            if s["tie"] is not None:
                self.add("tied", "piece", voc.ties[0])
                self.walk(s["tie"], [])
            for c in s["cond_trees"]:
                u = [self.unit()]
                self.add("given", "given", voc.relatives[0], u)
                self.walk(c, u)
            if g["voice"] == "then":
                self.add("g.rule_for", "grammar", voc.for_shapes[0][0])
            for j, t in enumerate(g["trees"]):
                if j:
                    self.add("g.claims", "grammar", voc.claim_seps[0])
                self.claim, self.claims = self.claims, self.claims + 1
                self.walk(t, [], claim=True)
                self.claim = None

    def unit(self) -> int:
        self.units += 1
        return self.units - 1

    def add(self, id_, kind, text, units=(), neg=False) -> Inst:
        i = Inst(len(self.items), id_, kind, stems(text), neg, list(units), claim=self.claim)
        self.items.append(i)
        return i

    def forced(self, leaf: Leaf) -> bool:
        """Is this role the only thing its hole could have been filled with (the one role of its type)?"""
        return leaf.how == "role" and len({r[2] for r in self.roles.values() if r[1] == leaf.type}) == 1

    def walk(self, x, units, claim=False, under_silent=False):
        if isinstance(x, list):
            if x and all(isinstance(y, Node) and y.idiom and y.said is x[0].said for y in x):
                x = x[0]
            else:
                for y in x:
                    self.walk(y, units)
                return
        if isinstance(x, Leaf):
            # a role that is the one filler of its hole under a piece with words of its own ("of the ledger") is exempt; a role
            # chosen among several ("the sender"), a literal, and what fills a wordless piece ("the amount" as a term) must be asked for
            self.add("\"" + x.text + "\"", "leaf" if self.forced(x) and not under_silent else "choice", x.text, units)
            return
        if x.idiom:
            self.add(x.idiom, "frame" if claim else "idiom", literal(x.form), units)
            for v in (x.said or {}).values():
                self.walk(v, units)
            return
        node, neg = (x.args["p"], True) if x.id == "not" and x.neg else (x, False)
        if not x.form and not node.args:
            self.add(node.id, "implied", "", units)
            return
        me = self.add(node.id, "frame" if claim else "piece", literal(x.form), units, neg)
        if not me.words:
            me.kind = "silent"                   # a piece whose form writes no word of its own ("{l:ledger}" read as a measure; "{a} is {t}"): said by what fills it
        args = dict(node.args)
        if node.id == "changes_only" and "xs" in args:
            args["x"], args["y"] = args["xs"]
        written, before = set(), ""
        for s in segments(x.form):
            if s[0] == "lit":
                before = s[1]
            if s[0] != "hole" or s[1] not in args:
                continue
            written.add(s[1])
            cat, hv = hole_voice(s[2])
            if base_cat(cat) in ("cond", "variation") or hv == "first":
                u = self.unit()                  # a condition of the claim: the frame's connective and what fills the hole
                me.units = me.units + [u]
                me.connectives |= set(stems(before))
                self.walk(args[s[1]], list(units) + [u])
            else:
                self.walk(args[s[1]], units, under_silent=me.kind == "silent")
        for h, a in node.args.items():           # a hole the form does not write (`implied:`): said by the frame's own words
            if h not in written and h != "xs" and isinstance(a, Node):
                self.add(a.id, "implied", "", units)


# --------------------------------------------------------------------------------------------- coverage

EXEMPT = ("leaf", "implied", "silent", "grammar")     # instances no word has to ask for, and that take no cue word


def lcs_pairs(a: list, b: list) -> list:
    """Index pairs of one longest common subsequence of two lists (the first found, deterministically)."""
    n, m = len(a), len(b)
    t = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            t[i][j] = t[i + 1][j + 1] + 1 if a[i] == b[j] else max(t[i + 1][j], t[i][j + 1])
    out, i, j = [], 0, 0
    while i < n and j < m:
        if a[i] == b[j]:
            out.append((i, j))
            i, j = i + 1, j + 1
        elif t[i + 1][j] >= t[i][j + 1]:
            i += 1
        else:
            j += 1
    return out


def role_words(voc) -> str:
    ws = set()
    for o in voc.ops.values():
        for n in o["nouns"]:
            ws.add(n.split()[0])
        for r, _ in o["state"] + o["input"]:
            ws.add(r)
    return "|".join(sorted(re.escape(w) + "s?" for w in ws))


def when_verbs(voc, op: dict) -> frozenset:
    """The words by which an operation is anchored when its noun is not written: the tokens of its `when` forms that are
    not a word of any role, noun or domain piece of its system (ALL of them must be in the rough sentence)."""
    other = set()
    for o in voc.ops.values():
        for r, _ in o["state"] + o["input"]:
            other |= set(v1.tokens(r))
    for p in voc.pieces.values():
        if p.get("kind") == "domain":
            for f in p.get("forms") or []:
                other |= v1.bag(f)
    out = set()
    for w in op["when"]:
        out |= v1.bag(w)
    return frozenset(out - other)


def coverage(voc, rough: str, rd, hinted=None) -> dict:
    """The accounting of one candidate reading `rd` against the rough sentence. See the module text."""
    hinted = hinted or {}
    lx = lex(rough)
    occ = [{"i": i, "word": w, "stem": v1.stem(w), "status": "STOP" if not content(w) else None, "piece": None, "via": None, "inst": None}
           for i, (w, _) in enumerate(lx)]
    R = [o for o in occ if o["status"] is None]
    P = Pieces(voc, rd)
    C = [(w, inst) for inst in P.items for w in inst.words]

    def take(o, inst, via):
        o["status"], o["piece"], o["via"], o["inst"] = "MAPPED", inst.id + (" (negated)" if inst.neg else ""), via, inst.n
        inst.taken += 1

    # 1. form words, occurrence by occurrence: first in the author's order (a longest common subsequence), then the rest
    used = set()
    for i, j in lcs_pairs([o["stem"] for o in R], [w for w, _ in C]):
        take(R[i], C[j][1], "form")
        used.add(j)
    for o in R:
        if o["status"] is None:
            j = next((j for j, (w, _) in enumerate(C) if j not in used and w == o["stem"]), None)
            if j is not None:
                take(o, C[j][1], "form")
                used.add(j)
    # 2. phrases a named default of this reading covers
    text = " ".join(w for w, _ in lx)
    starts, pos = [], 0
    for w, _ in lx:
        starts.append(pos)
        pos += len(w) + 1
    for d, pat in DEFAULT_PHRASES:
        if d not in rd.defaults:
            continue
        for m in re.finditer(pat.replace("%ROLES%", role_words(voc)), text):
            for o in occ:
                if m.start() <= starts[o["i"]] < m.end() and o["status"] is None:
                    o["status"], o["piece"], o["via"] = "DEFAULT", d, "default"
    # 3. the cue table of version 1, and the verb of a `when` form, with the cue capacity
    for o in R:
        if o["status"] is not None:
            continue
        for inst in P.items:
            if inst.kind in EXEMPT or inst.kind == "choice":
                continue
            nouns = [stems(n) for n in voc.ops[inst.id]["nouns"]] if inst.kind == "op" else []
            cap = max([1, len(inst.words)] + [len(n) for n in nouns])
            if inst.taken >= cap:
                continue
            if inst.kind == "op" and any(o["stem"] in n for n in nouns):
                take(o, inst, "noun")              # a word of another noun the book gives the operation ("fund transfer")
                break
            if inst.kind == "op" and o["stem"] in hinted.get(inst.id, ()):
                take(o, inst, "when")
                break
            cues = v1.CUE_BAGS.get(inst.id, frozenset()) | (v1.CUE_BAGS["not"] if inst.neg else frozenset())
            if o["stem"] in cues:
                take(o, inst, "cue")
                break
    for o in R:
        if o["status"] is None:
            o["status"] = "DROPPED"
    assert all(o["status"] in ("STOP", "MAPPED", "DEFAULT", "DROPPED") for o in occ), "coverage: a word without a status"
    assert all((o["status"] == "MAPPED") == (o["inst"] is not None) for o in occ), "coverage: a mapped word names its piece"
    # condition spans; the opener of a span that is matched with a condition unit is accounted for by that unit
    spans = condition_spans(lx, occ, P)
    in_unit = {u: {i.n for i in P.items if u in i.units} for u in range(P.units)}
    can = {k: [u for u in in_unit if any(o["inst"] in in_unit[u] for o in sp["occ"])] for k, sp in enumerate(spans)}
    match = match_spans(can)
    for k, u in match.items():
        head = P.items[min(in_unit[u])]
        for o in spans[k]["opener"]:
            if o["status"] == "DROPPED":
                take(o, head, "opener")
    added = [i for i in P.items if i.kind not in EXEMPT and i.taken == 0]
    dropped_spans = [" ".join(o["word"] for o in sp["occ"]) for k, sp in enumerate(spans) if k not in match]
    dropped = [o["word"] for o in occ if o["status"] == "DROPPED"]
    # askable: the operation is asked for, and so is every claim (some word of the author's is mapped into it)
    askable = not any(i.kind == "op" for i in added) and all(any(i.taken for i in P.items if i.claim == k) for k in range(P.claims))
    return {"words": [{k: o[k] for k in ("word", "status", "piece", "via")} for o in occ],
            "dropped": dropped, "added": [i.id + (" (negated)" if i.neg else "") for i in added],
            "condition_dropped": dropped_spans, "defaults_used": sorted({o["piece"] for o in occ if o["status"] == "DEFAULT"}),
            "spans": [" ".join(o["word"] for o in sp["occ"]) for sp in spans],
            "full": not dropped and not added and not dropped_spans, "askable": askable}


def condition_spans(lx, occ, P) -> list:
    """The condition spans of the rough sentence against one candidate: [{occ: the words of the span}]. An opener that is
    itself a form word of a piece outside every condition unit ("only" of "only X and Y change") opens nothing."""
    words = [w for w, _ in lx]
    # a form word of a piece opens nothing unless the piece writes it to introduce a condition: "that" of "never loses that
    # ... when ..." opens nothing, its "when" does; the words of a narrowing and of "for which" always do
    unitless = {i.n for i in P.items if not i.units}
    intro = {i.n: i.connectives for i in P.items if i.units and i.kind not in ("narrowing", "given")}
    def live(k, hit) -> bool:
        cont = [occ[k + d] for d in range(len(hit)) if occ[k + d]["status"] != "STOP"]
        return not cont or not all(o["via"] == "form" and (o["inst"] in unitless or (o["inst"] in intro and o["stem"] not in intro[o["inst"]]))
                                   for o in cont)

    at, k = [], 0
    while k < len(words):
        hit = next((op for op in OPENERS if tuple(words[k:k + len(op)]) == op), None)
        if hit and live(k, hit):
            if at and at[-1][1] == k:            # "only" + "if": one opener
                at[-1] = (at[-1][0], k + len(hit))
            else:
                at.append((k, k + len(hit)))
            k += len(hit)
        else:
            k += 1
    spans = []
    # a narrowing word before the operation's noun ("an accepted lookup", "a refused bump") is a span of its own: it must be
    # matched with a narrowing or a condition of the candidate, and a claim ("... is always accepted") does not match it
    nouns = {t for i in P.items if i.kind == "op" for n in P.voc.ops[i.id]["nouns"] for t in stems(n)}
    narrow = set().union(*(v1.CUE_BAGS[m] for m in ("successful", "rejected", "internal"))) | {v1.stem(w.strip()) for w, _ in P.voc.subject_words}
    for k in range(len(words) - 1):
        if occ[k]["stem"] in narrow and occ[k + 1]["stem"] in nouns and occ[k]["status"] != "STOP":
            spans.append({"occ": [occ[k]], "opener": []})
    for n, (a, b) in enumerate(at):
        end = at[n + 1][0] if n + 1 < len(at) else len(words)
        for j in range(b, end):
            if lx[j][1]:
                end = j
                break
        spans.append({"occ": [occ[j] for j in range(a, end) if occ[j]["status"] != "STOP"],
                      "opener": [occ[j] for j in range(a, b) if occ[j]["status"] != "STOP"]})
    return [s for s in spans if s["occ"]]


def match_spans(can: dict) -> dict:
    """A largest one-to-one matching span -> condition unit (augmenting paths; spans in order)."""
    owner = {}

    def place(k, seen):
        for u in can[k]:
            if u in seen:
                continue
            seen.add(u)
            if u not in owner or place(owner[u], seen):
                owner[u] = k
                return True
        return False

    for k in can:
        place(k, set())
    return {k: u for u, k in owner.items()}


# --------------------------------------------------------------------------------------------- the filters

def outside_books(voc, rd, projs=None) -> list:
    """The entries a compiled sentence uses from a book that the project of its operations does not list (projects.yaml).
    `clausal gen` stops on such a sentence in a feature file, so it is not a sentence its author could write. The books are
    loaded as one merged book, and the compiler offers every `shared` piece to every system: the counter lists no pack, and
    "the amount" as a term is the ledger pack's `amount_value`."""
    projs = projs if projs is not None else list(projects.load(ROOT))
    ops = [o["id"] for c in rd.info["clauses"] for o in c["ops"]]
    worst = None
    for p in projs:
        books = {projects.BOOK_PREFIX + b for b in p.books}
        if all(voc.home[o].rel in books for o in ops):
            strays = [i for i in rd.used if i in voc.home and voc.home[i].rel not in books]
            if not strays:
                return []
            worst = worst or strays
    return worst or ["no project lists the books of " + ", ".join(ops)]


def filtered(voc, rd, projs=None) -> str | None:
    """The filter a compiled candidate fails, or None."""
    if outside_books(voc, rd, projs):
        return "other-book"
    for g in rd.info["clauses"]:
        kinds = [k for k, m in narrowing.WORD.items() if m in g["s"]["mods"]]
        op = g["ops"][-1]
        for t in g["trees"]:
            nodes = [n for n in vocab.walk(t) if isinstance(n, Node)]
            top = t[0] if isinstance(t, list) else t
            for kind in kinds:
                cls = top.args.get("c") if isinstance(top, Node) else None
                pol = narrowing.polarity(cls, op, kind)
                if top.id in ("always", "if_then", "only_if", "exactly_when", "monotone", "same_answer_if") and pol is False:
                    return "opposite-narrowing"
                if top.id == "never" and pol is True:
                    return "opposite-narrowing"
                if top.id == "rejected_unchanged" and kind == "accepted":
                    return "opposite-narrowing"
            for n in nodes:
                if n.id in ("increases_by", "decreases_by"):
                    a = n.args.get("t")
                    if (isinstance(a, Node) and a.id == "zero") or (isinstance(a, Node) and len(a.args) == 1
                                                                    and all(isinstance(v, Leaf) and v.text == "0" for v in a.args.values())):
                        return "by-zero"
        for t in g["trees"] + g["s"]["cond_trees"]:
            for n in vocab.walk(t):
                if isinstance(n, Node) and len(n.args) >= 2:
                    said = [vocab.describe(a) for a in n.args.values()]
                    if len(set(said)) < len(said):
                        return "same-sides"
    return None


# --------------------------------------------------------------------------------------------- the system question

def system_words(voc) -> dict:
    """{system: the tokens that name only that system}: its name, the nouns of its operations, its roles and their types,
    minus every word another system's operations or domain words use and every word of a shared form."""
    own, all_ = {}, {}
    for o in voc.ops.values():
        b = own.setdefault(o["domain"], set())
        b |= set(v1.tokens(o["domain"]))
        for n in o["nouns"]:
            b |= set(v1.tokens(n))
        for r, t in o["state"] + o["input"]:
            b |= set(v1.tokens(r)) | set(v1.tokens(t))
        a = all_.setdefault(o["domain"], set())
        for w in o["when"]:
            a |= v1.bag(w)
    shared = set()
    for p in voc.pieces.values():
        d = p.get("domain", "shared")
        for key in vocab.RETIRABLE:
            for f in p.get(key) or []:
                (all_.setdefault(d, set()) if d in own else shared).update(v1.bag(f))
    return {d: frozenset(b - shared - set().union(*(own[e] | all_.get(e, set()) for e in own if e != d))) for d, b in own.items()}


def anchor(voc, rough: str, domain: str | None) -> dict:
    """Which operations the rough sentence is about, and in which system. Never every operation."""
    R = frozenset(v1.tokens(rough))
    ops = [o for o in voc.ops.values() if domain in (None, o["domain"])]
    # NAMED: every word of one of the operation's nouns is in the sentence (version 1 took ANY shared word: "funds" anchored
    # the ledger's "fund transfer", "total" its "computation of the total"). An operation whose noun CONTAINS a named noun
    # ("batch applied as a whole" for "batch") is tried too: the author's word may be short for it.
    noun_bags = {o["id"]: [frozenset(v1.tokens(n)) for n in o["nouns"]] for o in ops}
    full = [o for o in ops if any(n <= R for n in noun_bags[o["id"]])]
    said = [n for o in full for n in noun_bags[o["id"]] if n <= R]
    named = [o for o in ops if o in full or any(n < m for n in said for m in noun_bags[o["id"]])]
    hints = {o["id"]: when_verbs(voc, o) for o in ops}
    hinted = [o for o in ops if hints[o["id"]] and hints[o["id"]] <= R]
    got = named or hinted
    res = {"by": "noun" if named else "the verb of a `when` form" if hinted else None, "ops": got,
           "hinted": {o["id"]: hints[o["id"]] for o in got} if not named else {}, "system": domain, "system_by": "--domain" if domain else None,
           "systems": sorted({o["domain"] for o in got}), "settling_words": {}}
    if not got or domain:
        return res
    if len(res["systems"]) == 1:
        res["system"], res["system_by"] = res["systems"][0], "the only system with such an operation"
        return res
    only = system_words(voc)
    hit = {d: sorted(only[d] & R) for d in res["systems"] if only[d] & R}
    res["settling_words"] = hit
    if len(hit) == 1:
        d = next(iter(hit))
        res["system"], res["system_by"] = d, "words only that system has: " + ", ".join(hit[d])
        res["ops"] = [o for o in got if o["domain"] == d]
    return res


# --------------------------------------------------------------------------------------------- the whole question

def candidate(voc, comp, rough, rd, sentence, rank, score, as_written, hinted) -> dict:
    cov = coverage(voc, rough, rd, hinted)
    try:
        tree = ctree.of_reading(rd)
    except ctree.TreeError:
        tree = None
    return {"rank": rank, "sentence": sentence, "system": rd.info["domain"], "v1_score": score, "key": v1.reading_key(rd),
            "operations": [[o["id"] for o in c["ops"]] for c in rd.info["clauses"]], "echo": [list(e) for e in rd.echo],
            "lean": rd.lean_def(), "term_sha256": ctree.body_sha(rd), "tree": tree, "compiles_as_written": as_written, "coverage": cov}


def missing_kinds(rough: str) -> list:
    t = " ".join(w for w, _ in lex(rough))
    return [k for pat, k in MISSING_KINDS if re.search(pat, t)]


def nearest(voc, rough: str, domain) -> list:
    """The pieces and operations of the book with most of the rough sentence's words in their forms or cues (at most five)."""
    R = frozenset(stems(rough))
    out = []
    for o in voc.ops.values():
        if domain in (None, o["domain"]):
            hit = R & frozenset(t for n in o["nouns"] for t in stems(n))
            if hit:
                out.append((len(hit), o["id"], f"operation ({o['domain']}): \"{o['nouns'][0]}\"", sorted(hit)))
    for p in voc.pieces.values():
        if domain is not None and p.get("domain", "shared") not in ("shared", domain):
            continue
        forms = [f for k in ("vp_forms", "then_forms", "forms", "subject_forms") for f in p.get(k) or []]
        if not forms:
            continue
        hit = R & (frozenset(t for f in forms for t in stems(literal(f))) | v1.CUE_BAGS.get(p["id"], frozenset()))
        if hit:
            out.append((len(hit), p["id"], f"\"{forms[0]}\"", sorted(hit)))
    out.sort(key=lambda x: (-x[0], x[1]))
    return [{"piece": i, "form": f, "your_words": h} for _, i, f, h in out[:5]]


def base(rough, domain) -> dict:
    return {"schema": SCHEMA, "rough": rough, "system_asked": domain, "system": None, "system_by": None, "anchored_by": None,
            "outcome": None, "ask": None, "why": None, "answer": None, "candidates": [], "questions": None, "decline": None,
            "counts": {}, "acknowledgement": None, "stop_list": sorted(STOP2),
            "language_model": "none", "missing_kinds": missing_kinds(rough)}


def compose(rough: str, domain: str | None = None, l3: bool = True, identity: bool = True) -> dict:
    """`identity=False` skips the first step (a sentence of the book is its own answer): used only to measure what the
    generator reaches (compose_tests/v2.py)."""
    voc, comp = v1.load()
    systems = sorted({o["domain"] for o in voc.ops.values()})
    if domain is not None and domain not in systems:
        raise FeatureError(f"--domain {domain}: the systems of the Clausebook are {', '.join(systems)}")
    res = base(rough, domain)
    # 0. a sentence of the book is its own answer
    if identity:
        rd = v1.compile_sentence(comp, rough.strip(), domain)
        if not isinstance(rd, Problem):
            as_written = domain is None or not isinstance(v1.compile_sentence(comp, rough.strip(), None), Problem)
            c = candidate(voc, comp, rough, rd, rough.strip(), 1, None, as_written, {})
            res.update(outcome="ANSWER", why="the sentence is a sentence of the Clausebook as written: it is its own answer", answer=c,
                       candidates=[c], system=rd.info["domain"], system_by="the sentence compiles", anchored_by="identity")
            return res
        if domain is None:
            reads = [d for d in systems if not isinstance(v1.compile_sentence(comp, rough.strip(), d), Problem)]
            if len(reads) > 1:
                res.update(outcome="ASK", ask="system", systems=reads,
                           why=f"the sentence is a sentence of the Clausebook in {len(reads)} systems ({', '.join(reads)}): its subject names an operation "
                               "of each, and no word of it says which. Run again with --domain " + "|".join(reads))
                return res
    # 1. the operation and the system, before anything is generated
    a = anchor(voc, rough, domain)
    res["anchored_by"], res["system"], res["system_by"] = a["by"], a["system"], a["system_by"]
    res["operations_anchored"] = [o["id"] for o in a["ops"]]
    if not a["ops"]:
        res.update(outcome="DECLINE", why="no operation of the Clausebook is named in the sentence (by a noun, or by the verb of a `when` form)"
                   + (f" in the system {domain}" if domain else "") + ". Version 2 does not try every operation.",
                   decline={"unmapped": [w for w, _ in lex(rough) if content(w)], "nearest": nearest(voc, rough, domain),
                            "operations": sorted({n for o in voc.ops.values() if domain in (None, o["domain"]) for n in o["nouns"]})})
        return res
    if a["system"] is None:
        res.update(outcome="ASK", ask="system", systems=a["systems"],
                   why=f"the sentence names an operation of {len(a['systems'])} systems ({', '.join(a['systems'])}: "
                       + "; ".join(f"{o['domain']}: {o['nouns'][0]}" for o in a["ops"]) + ") and "
                       + ("words of more than one of them (" + "; ".join(f"{d}: {', '.join(w)}" for d, w in a["settling_words"].items()) + ")"
                          if a["settling_words"] else "no word that only one of them has")
                       + ". Which system is your rule about? Run again with --domain " + "|".join(a["systems"]))
        return res
    system = a["system"]
    # 2. generate and rank: version 1's generator and ranking rule, unchanged
    toks = v1.tokens(rough)
    R = frozenset(toks)
    numbers = list(dict.fromkeys(re.findall(r"\d+", rough)))
    pool = {}
    for seq in v1.subject_ops(voc, a["ops"], R):
        gen = v1.Gen(voc, seq, tuple(toks), numbers, rough)
        for s in v1.sentences(voc, gen):
            pool.setdefault(s.text, s)
    ranked = v1.order(pool.values(), tuple(toks))
    # 3. compile, filter, account
    counts = {"generated": len(ranked), "compiled": 0, "refused": 0, "another_composition": 0, "same_term": 0,
              "filtered": {"other-book": 0, "opposite-narrowing": 0, "by-zero": 0, "same-sides": 0}, "passed": 0}
    cands, seen = [], set()
    projs = list(projects.load(ROOT))
    for s in ranked[:COMPILE_LIMIT]:
        counts["compiled"] += 1
        rd = v1.compile_sentence(comp, s.text, None)
        as_written = not isinstance(rd, Problem)
        if not as_written:
            rd = v1.compile_sentence(comp, s.text, system)
        if isinstance(rd, Problem):
            counts["refused"] += 1
            continue
        if rd.info["domain"] != system:
            counts["refused"] += 1
            continue
        if s.key is not None and v1.reading_key(rd) != s.key:
            counts["another_composition"] += 1
            continue
        t = v1.term(rd)
        if t in seen:
            counts["same_term"] += 1
            continue
        seen.add(t)
        f = filtered(voc, rd, projs)
        if f:
            counts["filtered"][f] += 1
            continue
        counts["passed"] += 1
        cands.append(candidate(voc, comp, rough, rd, s.text, len(cands) + 1, v1.score(s.parts, R, s.text)[0], as_written, a["hinted"]))
    res["counts"] = counts
    full = [c for c in cands if c["coverage"]["full"]]
    askable = [c for c in cands if c["coverage"]["askable"] and not c["coverage"]["full"]]
    if full:
        return decide_full(res, full, l3)
    if askable:
        # which to show: those that drop no condition first, then version 1's ranking rule (one ranking rule, not a second one)
        show = sorted(askable, key=lambda c: (bool(c["coverage"]["condition_dropped"]), c["rank"]))[:SHOW]
        for k, c in enumerate(show, 1):
            c["shown"] = k
        res.update(outcome="ASK", ask="dropped", candidates=show,
                   why="no sentence of the Clausebook that was generated accounts for every word of yours. The nearest are shown with what each "
                       "leaves out or adds. None is chosen unless you acknowledge one (--acknowledge K --by NAME)")
        return res
    best = min(cands, key=lambda c: (len(c["coverage"]["dropped"]), c["rank"]), default=None)
    res.update(outcome="DECLINE",
               why=("no candidate is good enough to ask about: " + (f"each of the {len(cands)} sentences that compile and pass the filters claims something "
                    "no word of yours asks for" if cands else f"none of the {counts['compiled']} best of {counts['generated']} generated sentences compiles and passes the filters")
                    + f" (refused by the compiler: {counts['refused']}; filtered: " + ", ".join(f"{k} {v}" for k, v in counts["filtered"].items()) + ")"),
               decline={"unmapped": best["coverage"]["dropped"] if best else [w for w, _ in lex(rough) if content(w)],
                        "nearest": nearest(voc, rough, system), "operations": [o["nouns"][0] for o in a["ops"]]})
    return res


def decide_full(res: dict, full: list, l3: bool) -> dict:
    """One or more candidates with full coverage: ANSWER if they are one reading, else ASK (reading)."""
    for k, c in enumerate(full, 1):
        c["shown"] = k
    if len(full) == 1:
        res.update(outcome="ANSWER", answer=full[0], candidates=full[:1],
                   why="one sentence of the Clausebook accounts for every word of yours, adds nothing, and no other candidate does")
        return res
    top = full[:L3_PAIRS]
    res["candidates"] = top
    if not l3:
        res.update(outcome="ASK", ask="reading", questions=[],
                   why=f"{len(full)} sentences account for every word of yours and are different Lean terms; they were not compared (--no-l3)")
        return res
    qs = v1.questions({"candidates": [dict(c, rank=c["shown"]) for c in top]}, len(top))
    res["questions"] = qs
    if len(full) <= L3_PAIRS and all(q["verdict"] in ("SAME-TERM", "PROVED-EQUAL") for q in qs):
        res.update(outcome="ANSWER", answer=top[0],
                   why=f"{len(full)} sentences account for every word of yours, and `clausal separate` shows them equal ("
                       + ", ".join(sorted({q['verdict'] for q in qs})) + "): one reading")
        return res
    res.update(outcome="ASK", ask="reading",
               why=f"{len(full)} sentences account for every word of yours and are not shown to say the same"
                   + (f" (the first {L3_PAIRS} were compared)" if len(full) > L3_PAIRS else "") + ". The questions below tell them apart")
    return res


def acknowledge(res: dict, k: int, by: str) -> dict:
    """Record that `by` accepts candidate `k` of an ASK (dropped), with what it leaves out and adds."""
    if res["outcome"] != "ASK" or res["ask"] != "dropped":
        raise FeatureError("--acknowledge is for an ASK (dropped): there is nothing to acknowledge here")
    if not by:
        raise FeatureError("--acknowledge needs --by NAME: an acknowledgement is someone's")
    c = next((c for c in res["candidates"] if c.get("shown") == k), None)
    if c is None:
        raise FeatureError(f"there is no candidate {k}")
    res["acknowledgement"] = {"candidate": k, "sentence": c["sentence"], "term_sha256": c["term_sha256"], "by": by,
                              "date": datetime.date.today().isoformat(), "dropped_words": c["coverage"]["dropped"],
                              "added_pieces": c["coverage"]["added"], "conditions_dropped": c["coverage"]["condition_dropped"],
                              "what": "the harness's record of what was typed at the command line; not a signature"}
    res["chosen"] = c
    return res


def record(res: dict, c: dict, voc) -> dict:
    """The provenance record of one composed rule (study 4.3; the proposer is always this rule-based composer here)."""
    return {"sentence": c["sentence"], "term_sha256": c["term_sha256"], "system": c["system"],
            "proposed_by": {"kind": "rule-based", "id": "clausal compose2 (no language model)"},
            "rough": res["rough"], "rough_sha256": hashlib.sha256(res["rough"].encode()).hexdigest(),
            "books": [{"book": b.rel, "sha256": hashlib.sha256(b.text.encode()).hexdigest()} for b in voc.books],
            "checks": {"compiled": True, "tree_round_trip": c["tree"] is not None, "outcome": res["outcome"], "ask": res["ask"],
                       "coverage": {k: c["coverage"][k] for k in ("dropped", "added", "condition_dropped", "defaults_used", "full")},
                       "words": c["coverage"]["words"], "questions": res.get("questions")},
            "acknowledgement": res.get("acknowledgement"),
            "chosen_by": (f"human:{res['acknowledgement']['by']}" if res.get("acknowledgement") else "rule (the one surviving reading)"),
            "date": datetime.date.today().isoformat()}


# --------------------------------------------------------------------------------------------- output

def say_cov(c: dict) -> list:
    cov = c["coverage"]
    o = []
    for sp in cov["condition_dropped"]:
        o.append(f"     CONDITION DROPPED: your sentence says \"{sp}\"; this sentence has no condition or narrowing for it")
    by = {}
    for w in cov["words"]:
        if w["status"] == "MAPPED":
            by.setdefault(f"{w['piece']} [{w['via']}]", []).append(w["word"])
    o.append("     your words -> pieces: " + ("; ".join(f"{' '.join(ws)} -> {p}" for p, ws in by.items()) or "none"))
    d = [w["word"] + f" [{w['piece']}]" for w in cov["words"] if w["status"] == "DEFAULT"]
    if d:
        o.append("     covered by a default of the reading: " + ", ".join(d))
    if cov["dropped"]:
        o.append("     DROPPED (your sentence also says; this sentence does not): " + ", ".join(cov["dropped"]))
    if cov["added"]:
        o.append("     ADDED (pieces of this sentence none of your words asks for): " + ", ".join(cov["added"]))
    return o


def render(res: dict) -> str:
    o = [f"Rough sentence: {res['rough']}",
         f"words not accounted (the stop list: articles and auxiliaries): {' '.join(res['stop_list'])}"]
    if res.get("system"):
        o.append(f"system: {res['system']} ({res['system_by']}); operation anchored by: {res['anchored_by']}")
    head = res["outcome"] + (f" ({res['ask']})" if res["ask"] else "")
    o += ["", f"{head}: {res['why']}"]
    for c in res["candidates"]:
        o.append("")
        o.append(f"[{c.get('shown', 1)}] {c['sentence']}")
        if not c["compiles_as_written"]:
            o.append(f"     NOTE: this is one statement only in the system {c['system']} (under a Rule whose scenarios are in it). Written "
                     "alone it is AMBIGUOUS: another system reads it too.")
        o += say_cov(c)
        for a, b in c["echo"]:
            o.append(f"       {a:<12}{b}")
    for q in res.get("questions") or []:
        o.append("")
        o.append(f"  candidates {q['a']} and {q['b']}: {q['verdict']}")
        o += ["    " + l for l in q["detail"] if l]
        if q["question"]:
            o.append(f"    QUESTION: {q['question']}")
    d = res.get("decline")
    if d:
        o.append("")
        o.append("  words nothing accounts for: " + (", ".join(d["unmapped"]) or "none"))
        if d["nearest"]:
            o.append("  nearest pieces of the Clausebook:")
            o += [f"    {n['piece']}: {n['form']}   (your words: {', '.join(n['your_words'])})" for n in d["nearest"]]
        o.append("  operations: " + ", ".join(d["operations"]))
    if res["missing_kinds"] and res["outcome"] != "ANSWER":
        o.append("")
        o += ["  the sentence may need a piece the Clausebook does not have (recognised by a phrase; advisory): " + k for k in res["missing_kinds"]]
    ack = res.get("acknowledgement")
    if ack:
        o += ["", f"ACKNOWLEDGED by {ack['by']} ({ack['date']}): candidate {ack['candidate']}, \"{ack['sentence']}\", without: "
                  + (", ".join(ack["dropped_words"]) or "nothing") + ("; with added: " + ", ".join(ack["added_pieces"]) if ack["added_pieces"] else "")
                  + ("; conditions dropped: " + "; ".join(ack["conditions_dropped"]) if ack["conditions_dropped"] else "")]
    return "\n".join(o)


def main(argv) -> int:
    argv = list(argv)

    def opt(name):
        if name in argv:
            i = argv.index(name)
            v = argv[i + 1] if i + 1 < len(argv) else None
            del argv[i:i + 2]
            return v
        return None

    domain, ack, by, write = opt("--domain"), opt("--acknowledge"), opt("--by"), opt("--write")
    as_json, no_l3 = "--json" in argv, "--no-l3" in argv
    rest = [a for a in argv if not a.startswith("--")]
    if len(rest) != 1:
        print(__doc__)
        return 2
    try:
        res = compose(rest[0], domain, l3=not no_l3)
        if ack:
            res = acknowledge(res, int(ack), by)
        chosen = res["answer"] if res["outcome"] == "ANSWER" else res.get("chosen")
        if write:
            if chosen is None:
                raise FeatureError("--write needs an ANSWER, or an ASK (dropped) with --acknowledge K --by NAME: nothing is written otherwise")
            if not chosen["compiles_as_written"]:
                raise FeatureError("not written: the sentence is AMBIGUOUS without a system, and a Rule line alone gives none")
            v1.write_feature(Path(write), chosen["sentence"], None)
            side = Path(write + ".compose.json")
            recs = json.loads(side.read_text()) if side.exists() else {"what": "provenance of the Rule lines written by `clausal compose2 --write` "
                                                                                "(the harness's record, not a signature)", "rules": {}}
            recs["rules"][chosen["term_sha256"]] = record(res, chosen, v1.load()[0])
            side.write_text(json.dumps(recs, indent=1, ensure_ascii=False) + "\n")
            res["written"] = {"feature": write, "record": str(side)}
    except FeatureError as e:
        print(f"clausal compose2: {e}", file=sys.stderr)
        return 1
    res.pop("chosen", None)
    if as_json:
        print(json.dumps(res, indent=1, ensure_ascii=False, default=lambda x: sorted(x) if isinstance(x, (set, frozenset)) else str(x)))
    else:
        print(render(res))
        if res.get("written"):
            print(f"\nwritten: Rule: {chosen['sentence']}  ->  {res['written']['feature']} (record: {res['written']['record']})")
    return {"ANSWER": 0, "ASK": 4, "DECLINE": 3}[res["outcome"]]
