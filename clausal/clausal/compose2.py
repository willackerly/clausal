"""clausal compose2: composer VERSION 2, first part (plan nodes L1a, L1b; the tree interface L1e is clausal/ctree.py).

    python3 -m clausal compose2 "<rough English>" [--domain D] [--operation ID] [--json] [--no-l3]
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
           operation  (fix round) no operation is anchored, and the sentence has a word of a system of the book (its name, a
                    noun of one of its operations, a role or a role's type): the book may be able to say it, so the
                    operations of that system (or of every system with a word in the sentence) are listed and NOTHING IS
                    GENERATED. `--operation ID` (an id or a noun) is the author's answer: that one operation is tried, it
                    is recorded as stated by the author (`operation_stated`), and it is not counted as an ADDED piece.
  DECLINE  no operation is anchored (version 1 then tried every operation; version 2 never does; an operation is anchored by
           EVERY word of one of its nouns, or by the verb of its `when` form) AND no word of the sentence is a word of a
           system; or no candidate is askable.
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
  constants          (L1c) a piece all of whose holes are filled with terms that do not depend on the call ("the maximum equals
                     zero"): it is true of every call or of none

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
  THE SIDE OF A CONDITION (fix round; `wrong_side`). A word is mapped to a piece written INSIDE a condition unit only if
  the word is written in the condition span that is matched with that unit. "never" of "never changes the ledger when
  the amount is zero" is outside the span "when the amount is zero": it is not mapped to the negation of "for which the
  amount differs from zero", by cue or by form. A word of one span is not mapped into the unit of another. Not checked: a
  role that is the one filler of its hole. The mappings refused are listed (`refused_mappings`).
  ONE NEGATION WORD, ONE NEGATION (fix round). "not", "no", "never" (NEG): a piece takes one through a cue only while it has
  taken fewer negation words than it says negations (one, or as many as its form writes).
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
from . import ctree, cues2, narrowing, projects, vocab
from .core import FeatureError, Problem
from .pipeline import ROOT
from .vocab import Leaf, Node, base_cat, hole_voice, segments

SCHEMA = "clausal-compose-v2"
SHOW = 3                 # candidates shown with an ASK
L3_PAIRS = 3             # full candidates compared pairwise by `clausal separate` before an ANSWER
COMPILE_LIMIT = 2 * v1.COMPILE_LIMIT    # (L1c) twice version 1's: with phrase cues the sentence wanted is often further down version 1's list

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
    t = re.sub(r"\b(ca|wo|sha)n['’]t\b", lambda m: {"ca": "can", "wo": "will", "sha": "shall"}[m.group(1)] + " not", t)
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
    inner: list = field(default_factory=list)      # the condition units it is written INSIDE (a frame is not inside the condition it introduces)
    negs: int = 0             # negation words of the rough sentence mapped to it
    clause: int = 0           # which clause of the sentence it is written in
    repeat: bool = False      # the operation of a later clause, when it is the operation of the first: the book restates the subject
    holes: dict = field(default_factory=dict)      # {hole: the numbers of the instances written for it}
    dir: tuple | None = None  # a comparison: (REL, holes written before its comparison words, holes written after)
    lone: bool = False        # a domain piece with no hole that is the one piece of its category in its system ("the result")
    parent: int | None = None # the instance whose hole it fills
    forced: bool = False      # a role that is the one role of its type; or a domain piece that is the one piece of the book that
                              # makes its category out of that one role ("the wallet's balance": the one number of a wallet)


def literal(form: str) -> str:
    return " ".join(s[1] for s in segments(form) if s[0] == "lit")


class Pieces:
    """The piece instances of a compiled Rule line, in the order written, and its condition units."""

    def __init__(self, voc, rd):
        self.voc, self.items, self.units, self.roles, self.claim, self.claims, self.k = voc, [], 0, {}, None, 0, 0
        self.phrased = set()
        self.all_roles = {}
        word_mod = {w.strip(): m for w, m in voc.subject_words}
        clauses = rd.info["clauses"]
        first_op = clauses[0]["ops"][0]["id"]
        for k, g in enumerate(clauses):
            self.k = k
            self.all_roles.update(g["s"]["roles"])
            if k:
                self.add("g.clauses", "grammar", voc.clause_seps[0])
            s = g["s"]
            self.roles = s["roles"]
            for j, (_, ws, noun) in enumerate(s["written"]):
                if j:
                    self.add("and_then", "piece", voc.sequences[0])
                for w in ws:
                    self.add(word_mod[w], "narrowing", w, [self.unit()])
                me = self.add(g["ops"][j]["id"], "op", noun)
                me.repeat = k > 0 and j == 0 and len(s["written"]) == 1 and me.id == first_op
            if s["tie"] is not None:
                self.add("tied", "implied", voc.ties[0])     # "with <tie>": said by the tie that fills it
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
        i = Inst(len(self.items), id_, kind, stems(text), neg, list(units), claim=self.claim, inner=list(units), clause=self.k)
        self.items.append(i)
        return i

    def forced(self, leaf: Leaf) -> bool:
        """Is this role the only thing its hole could have been filled with (the one role of its type)?"""
        return leaf.how == "role" and len({r[2] for r in self.roles.values() if r[1] == leaf.type}) == 1

    def only_maker(self, node, form: str) -> bool:
        """Is this DOMAIN piece the one piece of its system that makes its category out of one role of that type and nothing
        else ("{w:wallet}'s balance": the one measure<num> of a wallet)? Then the role said is the piece said."""
        p = self.voc.pieces.get(node.id) or {}
        holes = [s for s in segments(form) if s[0] == "hole"]
        if p.get("kind") != "domain" or len(holes) != 1 or not isinstance(node.args.get(holes[0][1]), Leaf):
            return False
        cat, typ = p.get("cat") or p.get("category"), hole_voice(holes[0][2])[0]
        same = [q["id"] for q in self.voc.pieces.values() if q.get("kind") == "domain" and q.get("domain") == p.get("domain")
                and (q.get("cat") or q.get("category")) == cat
                and any([hole_voice(h[2])[0] for h in segments(f) if h[0] == "hole"] == [typ] for f in q.get("forms") or [])]
        return same == [node.id]

    def walk(self, x, units, claim=False, under_silent=False, parent=None):
        if isinstance(x, list):
            if x and all(isinstance(y, Node) and y.idiom and y.said is x[0].said for y in x):
                x = x[0]
            else:
                for y in x:
                    self.walk(y, units, parent=parent)
                return
        if isinstance(x, Leaf):
            # a role that is the one filler of its hole under a piece with words of its own ("of the ledger") is exempt; a role
            # chosen among several ("the sender"), a literal, and what fills a wordless piece ("the amount" as a term) must be asked for
            me = self.add("\"" + x.text + "\"", "leaf" if self.forced(x) and not under_silent else "choice", x.text, units)
            me.forced, me.parent = self.forced(x), parent
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
        me.parent, me.forced = parent, not claim and self.only_maker(node, x.form)
        pc = self.voc.pieces.get(node.id) or {}
        me.lone = (not claim and pc.get("kind") == "domain" and not node.args      # the one piece of its category, of any book of its system
                   and [q["id"] for q in self.voc.pieces.values() if q.get("domain", "shared") in ("shared", pc.get("domain"))
                        and (q.get("cat") or q.get("category")) == (pc.get("cat") or pc.get("category"))] == [node.id])
        if not me.words:
            me.kind = "silent"                   # a piece whose form writes no word of its own ("{l:ledger}" read as a measure; "{a} is {t}"): said by what fills it
        args = dict(node.args)
        if node.id == "changes_only" and "xs" in args:
            args["x"], args["y"] = args["xs"]
        written, before, lit, at = set(), "", "", {}
        for s in segments(x.form):
            if s[0] == "lit":
                before = s[1]
                lit += s[1]
            if s[0] != "hole" or s[1] not in args:
                continue
            written.add(s[1])
            at[s[1]] = len(lit)
            lit += " "
            start = len(self.items)
            cat, hv = hole_voice(s[2])
            if base_cat(cat) in ("cond", "variation") or hv == "first":
                u = self.unit()                  # a condition of the claim: the frame's connective and what fills the hole
                me.units = me.units + [u]
                me.connectives |= set(stems(before))
                self.walk(args[s[1]], list(units) + [u], parent=me.n)
            else:
                self.walk(args[s[1]], units, under_silent=me.kind == "silent", parent=me.n)
            me.holes[s[1]] = list(range(start, len(self.items)))
        d = cues2.form_direction("", lit.lower()) if len(at) >= 2 else None
        if d:                                    # a comparison: which holes are written before its words, which after
            rel, where = d
            left, right = [h for h, p in at.items() if p <= where], [h for h, p in at.items() if p > where]
            if left and right:
                me.dir = (rel, left, right)     # (a negated piece is written with its own negated form: "differs from")
        for h, a in node.args.items():           # a hole the form does not write (`implied:`): said by the frame's own words
            if h not in written and h != "xs" and isinstance(a, Node):
                self.add(a.id, "implied", "", units)


# --------------------------------------------------------------------------------------------- coverage

EXEMPT = ("leaf", "implied", "silent", "grammar")     # instances no word has to ask for, and that take no cue word


def lcs_pairs(a: list, b: list, ok=lambda i, j: True) -> list:
    """Index pairs of one longest common subsequence of two lists (the first found, deterministically); a pair (i, j) with
    `ok(i, j)` false is never matched."""
    n, m = len(a), len(b)
    eq = [[a[i] == b[j] and ok(i, j) for j in range(m)] for i in range(n)]
    t = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            t[i][j] = t[i + 1][j + 1] + 1 if eq[i][j] else max(t[i + 1][j], t[i][j + 1])
    out, i, j = [], 0, 0
    while i < n and j < m:
        if eq[i][j]:
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


NEG = v1.CUE_BAGS["not"]      # the negation words ("not", "no", "never"; "n't", "cannot", "none", "nothing" are written out as these)


def lexed_text(lx) -> tuple:
    """The words of a lexed sentence joined by one space, and the character offset of each word in it."""
    starts, pos = [], 0
    for w, _ in lx:
        starts.append(pos)
        pos += len(w) + 1
    return " ".join(w for w, _ in lx), starts


def words_in(spans, starts, lx) -> list:
    """The indices of the words that lie in one of the character spans."""
    return [i for i, st in enumerate(starts) if any(a <= st and st + len(lx[i][0]) <= b for a, b in spans)]


def sense_ids(voc) -> dict:
    """{sense: the piece ids that carry it} (cues2.SENSES, with each project's acceptance class)."""
    out = {}
    for name, d in cues2.SENSES.items():
        ids = set(d["ids"])
        if d["class_form"]:
            ids |= {p["id"] for p in voc.pieces.values() if d["class_form"] in (p.get("forms") or [])}
        out[name] = ids
    return out


def phrase_hits(voc, lx, P) -> list:
    """The phrase cues of the rough sentence against one candidate: [(via, word indices, the instances that may take it)].
    Phrases of a sense (cues2.PHRASES), an operation said by a verb phrase or after a light verb, the words of a comparison."""
    text, starts = lexed_text(lx)
    senses = sense_ids(voc)
    hits = []
    for sense, pat in cues2.PHRASES:
        for m in re.finditer(pat, text):
            hits.append(("phrase", words_in(cues2.groups(m), starts, lx), [i for i in P.items if i.id in senses[sense]], sense))
    for inst in P.items:
        if inst.kind != "op":
            continue
        for noun in P.voc.ops[inst.id]["nouns"]:
            if noun in cues2.OP_SYNONYMS:
                for m in re.finditer(cues2.OP_SYNONYMS[noun], text):
                    hits.append(("synonym", words_in(cues2.groups(m), starts, lx), [inst], noun))
            for m in re.finditer(cues2.LIGHT.replace("%NOUN%", re.escape(noun) + "s?"), text):
                hits.append(("light verb", words_in(cues2.groups(m), starts, lx), [inst], noun))
    for rel, spans, _ in cues2.directions(text):
        hits.append(("comparison", words_in(spans, starts, lx), [i for i in P.items if i.dir], rel))
    return hits


def role_cues(P, inst) -> frozenset:
    """The words that say a role beside its own name: the name of its type when several roles have that type ("the
    receiving wallet": a wallet), another word for the role's name, a participle for a role of the input ("requested")."""
    r = P.all_roles.get(inst.id.strip('"'))
    if r is None:
        return frozenset()
    out = set(v1.tokens(r[1])) | cues2.ROLE_WORDS.get(r[2], frozenset())
    if r[0] == "value":
        out |= cues2.INPUT_ROLE_WORDS
    return frozenset(out)


def account(voc, lx, rd, hinted, barred) -> tuple:
    """One pass of the accounting: every content word gets a status, never through a pair (word, piece instance) of `barred`.
    Returns (occ, P, spans, match span -> condition unit)."""
    occ = [{"i": i, "word": w, "stem": v1.stem(w), "status": "STOP" if not content(w) else None, "piece": None, "via": None, "inst": None}
           for i, (w, _) in enumerate(lx)]
    R = [o for o in occ if o["status"] is None]
    P = Pieces(voc, rd)

    def take(o, inst, via):
        o["status"], o["piece"], o["via"], o["inst"] = "MAPPED", inst.id + (" (negated)" if inst.neg else ""), via, inst.n
        inst.taken += 1
        inst.negs += o["stem"] in NEG

    # 0. phrase cues (plan node L1c): a phrase of the author's that says what a piece of the candidate means. One phrase per
    #    instance and kind; the first instance in the order written that may take it and is not barred
    text0, starts0 = lexed_text(lx)
    necessary = {i for m in re.finditer(cues2.NECESSARY, text0) for i in words_in(cues2.groups(m), starts0, lx)}
    for via, idxs, insts, sense in phrase_hits(voc, lx, P):
        ws = [occ[i] for i in idxs if occ[i]["status"] is None]
        if not ws or len(ws) != sum(occ[i]["status"] != "STOP" for i in idxs):
            continue
        for inst in insts:
            if (via, sense, inst.n) in P.phrased or any((o["i"], inst.n) in barred for o in ws):
                continue
            for o in ws:
                take(o, inst, via)
            P.phrased.add((via, sense, inst.n))
            break

    # 1. form words, occurrence by occurrence: first in the author's order (a longest common subsequence), then the rest
    R1 = [o for o in R if o["status"] is None]
    C = [(w, inst) for inst in P.items for w in inst.words]
    used = set()
    rel0 = {i for _, sp, _ in cues2.directions(lexed_text(lx)[0]) for i in words_in(sp, lexed_text(lx)[1], lx)}
    C = [(w, inst) for w, inst in C]

    def may(o, inst) -> bool:
        return (o["i"], inst.n) not in barred and not (o["i"] in rel0 and not inst.dir and inst.kind != "grammar")

    for i, j in lcs_pairs([o["stem"] for o in R1], [w for w, _ in C], lambda i, j: may(R1[i], C[j][1])):
        take(R1[i], C[j][1], "form")
        used.add(j)
    for o in R1:
        if o["status"] is None:
            j = next((j for j, (w, inst) in enumerate(C) if j not in used and w == o["stem"] and may(o, inst)), None)
            if j is not None:
                take(o, C[j][1], "form")
                used.add(j)
    # 2. phrases a named default of this reading covers
    text, starts = lexed_text(lx)
    for d, pat in DEFAULT_PHRASES:
        if d not in rd.defaults:
            continue
        for m in re.finditer(pat.replace("%ROLES%", role_words(voc)), text):
            for o in occ:
                if m.start() <= starts[o["i"]] < m.end() and o["status"] is None:
                    o["status"], o["piece"], o["via"] = "DEFAULT", d, "default"
    # 3. the cue tables (version 1's, and version 2's for the pieces of the last wave), the verb of a `when` form, a role said
    #    by its type or another word, the echo words of a domain piece; with the cue capacity
    relwords = {i for _, sp, _ in cues2.directions(text) for i in words_in(sp, starts, lx)}

    def coordinated(o, inst) -> bool:
        """Is this word joined by "or" / "and" to a word the piece already took through a cue ("create or destroy")? Then it
        does not count against the cue capacity: the two are one thing said twice."""
        j = o["i"] - 1
        if j < 1 or lx[j][0] not in cues2.COORDINATORS or lx[j][1]:
            return False
        return occ[j - 1]["inst"] == inst.n and occ[j - 1]["via"] == "cue"

    for o in R:
        if o["status"] is not None:
            continue
        for inst in P.items:
            if (o["i"], inst.n) in barred or (o["i"] in necessary and inst.id != cues2.NECESSARY_PIECE):
                continue
            if o["i"] in relwords and not inst.dir:
                continue                         # a comparison word of the author's ("equals", "more") is accounted for only by a piece that compares
            if inst.id.startswith('"'):          # a role or a literal: only the words that say that role
                if inst.taken < 2 and o["stem"] in role_cues(P, inst):
                    take(o, inst, "role")
                    break
                continue
            if inst.kind in EXEMPT:
                if inst.kind == "silent" and inst.taken < 2 and o["stem"] in cues2.echo_words(voc.pieces.get(inst.id) or {}):
                    take(o, inst, "echo")          # a domain piece with no word of its own ("the ledger" read as its balances)
                    break
                if inst.kind == "silent" and inst.taken < 1 and o["stem"] in (v1.CUE_BAGS.get(inst.id, frozenset()) | cues2.CUE2_BAGS.get(inst.id, frozenset())):
                    take(o, inst, "cue")           # a frame with no word of its own ("{a} is {t}": "gives back ...")
                    break
                continue
            nouns = [stems(n) for n in voc.ops[inst.id]["nouns"]] if inst.kind == "op" else []
            cap = max([1, len(inst.words)] + [len(n) for n in nouns]) + (inst.kind == "op") + (inst.id == "same_input")
            if inst.taken >= cap and not coordinated(o, inst):
                continue
            if inst.kind == "op" and any(o["stem"] in n for n in nouns):
                take(o, inst, "noun")              # a word of another noun the book gives the operation ("fund transfer")
                break
            if inst.kind == "op" and o["stem"] in hinted.get(inst.id, ()):
                take(o, inst, "when")
                break
            # ONE NEGATION WORD, ONE NEGATION: a piece takes a negation word through a cue only while it has taken fewer
            # negation words than it says negations (one, or as many as its own form writes). "is not an account of" has its
            # "not" from the author's "not": the author's "no" of "gives no result" is not also absorbed by it.
            if o["stem"] in NEG and inst.negs >= max(1, sum(w in NEG for w in inst.words)):
                continue
            if inst.id == "same_input" and o["stem"] in {v1.stem(r[2]) for r in P.all_roles.values() if r[0] == "value"}:
                take(o, inst, "role")              # "the same amount": the input the two calls share, said by its role
                break
            cues = (v1.CUE_BAGS.get(inst.id, frozenset()) | cues2.CUE2_BAGS.get(inst.id, frozenset())
                    | ((NEG | cues2.CUE2_NEG_BAGS.get(inst.id, frozenset())) if inst.neg else frozenset()))
            if o["stem"] in cues:
                take(o, inst, "cue")
                break
            if o["stem"] in cues2.echo_words(voc.pieces.get(inst.id) or {}):
                take(o, inst, "echo")              # a word of the book's own echo of a domain piece ("every balance": the ledger)
                break
    for o in R:
        if o["status"] is None:
            o["status"] = "DROPPED"
    # condition spans; the opener of a span that is matched with a condition unit is accounted for by that unit
    spans = condition_spans(lx, occ, P)
    in_unit = {u: {i.n for i in P.items if u in i.units} for u in range(P.units)}
    # the units a span can be matched with: first those a word of the span is mapped INSIDE (the condition itself), then
    # those it reaches only through the frame's own words ("when", "if" of a frame with two conditions)
    inside = {u: {i.n for i in P.items if u in i.inner} for u in range(P.units)}
    can = {k: sorted((u for u in in_unit if any(o["inst"] in in_unit[u] for o in sp["occ"])),
                     key=lambda u: (not any(o["inst"] in inside[u] for o in sp["occ"]), u)) for k, sp in enumerate(spans)}
    match = match_spans(can)
    for k, u in match.items():
        head = P.items[min(in_unit[u])]
        for o in spans[k]["opener"]:
            if o["status"] == "DROPPED" and (o["i"], head.n) not in barred and not (o["i"] in necessary and head.id != cues2.NECESSARY_PIECE):
                take(o, head, "opener")
    attach(occ, lx, P)
    assert all(o["status"] in ("STOP", "MAPPED", "DEFAULT", "DROPPED") for o in occ), "coverage: a word without a status"
    assert all((o["status"] == "MAPPED") == (o["inst"] is not None) for o in occ), "coverage: a mapped word names its piece"
    return occ, P, spans, match


LOOSE = ("attached", "pronoun")      # how a function word is accounted for: with its neighbour, not by a piece of its own


def attach(occ, lx, P) -> None:
    """FUNCTION WORDS (plan node L1c; cues2.FUNCTION). Each is a content word with a status. A word no piece took is
    accounted for only through its neighbours, and never across a punctuation mark:
      preposition   with its OBJECT, the next word that is not a function word (if that is mapped or covered by a default);
                    at the end of a stretch, with the word before it. A preposition whose object is dropped is dropped.
      particle      with the word before it ("goes through", "takes ... out"), else the next.
      coordinator   when the words on both sides of it are accounted for.
      pronoun       stands for the subject: the operation of the candidate (of its own clause, else the first)."""
    def neighbour(i, step):
        j = i + step
        while 0 <= j < len(occ):
            if (step > 0 and lx[j][1]) or (step < 0 and lx[j + 1][1]):
                return None                      # a punctuation mark between them
            if occ[j]["status"] != "STOP" and occ[j]["word"] not in cues2.FUNCTION:
                return occ[j]
            j += step
        return None

    def ok(x):
        return x is not None and x["status"] in ("MAPPED", "DEFAULT")

    ops = [i for i in P.items if i.kind == "op"]
    quantified = any(i.id in cues2.QUANTIFIER_PIECES for i in P.items)
    changed = True
    while changed:
        changed = False
        for o in occ:
            w = o["word"]
            if o["status"] != "DROPPED" or w not in cues2.FUNCTION:
                continue
            nxt, prv = neighbour(o["i"], 1), neighbour(o["i"], -1)
            to = None
            if w in cues2.PRONOUNS:
                if ops:
                    o["status"], o["piece"], o["via"], o["inst"] = "MAPPED", ops[0].id, "pronoun", ops[0].n
                    changed = True
                continue
            if w in cues2.DETERMINERS:
                to = nxt if ok(nxt) and not quantified else None
            elif w in cues2.COORDINATORS:
                to = prv if ok(nxt) and ok(prv) else None
            elif w in cues2.PARTICLES:
                to = prv if ok(prv) else nxt if ok(nxt) else None
            else:
                to = nxt if ok(nxt) else prv if nxt is None and ok(prv) else None
            if to is not None:
                o["status"], o["piece"], o["via"], o["inst"] = to["status"], to["piece"], "attached" if to["status"] == "MAPPED" else "default", to["inst"]
                changed = True


def wrong_side(occ, P, spans, match) -> set:
    """The pairs (word, piece instance) of one pass that put a word on the wrong side of a condition: the piece is written
    INSIDE a condition unit of the candidate (a narrowing word; what follows "for which"; what fills the condition hole of a
    frame), and the word is not written in the condition span that is matched with that unit. A role that is the one filler
    of its hole (kind `leaf`: "of the ledger") is not checked: nothing was chosen there."""
    where = {}
    for k, sp in enumerate(spans):
        if k in match:
            for o in sp["occ"]:
                where.setdefault(o["i"], set()).add(match[k])
    out = set()
    for o in occ:
        if o["inst"] is None or o["via"] in LOOSE:
            continue
        inst = P.items[o["inst"]]
        if inst.inner and inst.kind != "leaf" and not where.get(o["i"], set()) & set(inst.inner):
            out.add((o["i"], inst.n))
    return out


def wrong_order(occ, P, lx) -> tuple:
    """ARGUMENT ORDER IN COMPARISONS (plan node L1c). The author's comparison words ("more than", "at most", "enough to
    cover": cues2.DIRECTIONS) say a relation between what is written before them and what is written after. A candidate's
    comparison piece says a relation between the holes written before ITS comparison words and those after (read off its
    own form by the same table). A comparison word of the author's is mapped to such a piece only if the two agree:
      the same relation, with the author's words for the left holes before the comparison and those for the right holes
      after it; or the converse relation ("B is less than A" for "A is more than B") with the sides swapped.
    If a negation word stands before the author's comparison in the same stretch ("never ... more than"), the negated
    relation is allowed too. Returns (the pairs (word, instance) that do not agree, what to print)."""
    text, starts = lexed_text(lx)
    out, notes = set(), []
    for rel, spans, _ in cues2.directions(text):
        idxs = words_in(spans, starts, lx)
        got = {occ[i]["inst"] for i in idxs if occ[i]["inst"] is not None and occ[i]["via"] not in LOOSE}
        for n in got:
            inst = P.items[n]
            if not inst.dir:
                continue
            crel, left, right = inst.dir
            xs = {k for h in left for k in inst.holes[h]}
            ys = {k for h in right for k in inst.holes[h]}
            cs, ce = min(idxs), max(idxs)
            xpos = [o["i"] for o in occ if o["inst"] in xs and o["via"] not in LOOSE]
            ypos = [o["i"] for o in occ if o["inst"] in ys and o["via"] not in LOOSE]
            xb, xa = any(i < cs for i in xpos), any(i > ce for i in xpos)
            yb, ya = any(i < cs for i in ypos), any(i > ce for i in ypos)
            allowed = {rel}
            j = cs - 1
            while j >= 0 and not lx[j + 1][1]:
                if lx[j][0] in cues2.NEGATION_WORDS:
                    allowed.add(cues2.NEGATE[rel])
                j -= 1
            fine = False
            for r in allowed:
                if r == crel:
                    fine |= not ((xa and not xb) or (yb and not ya))
                elif r == cues2.CONVERSE[crel]:
                    fine |= not ((xb and not xa) or (ya and not yb))
            if not fine:
                out |= {(i, n) for i in idxs}
                notes.append({"words": " ".join(lx[i][0] for i in idxs), "piece": inst.id + (" (negated)" if inst.neg else ""),
                              "yours": sorted(allowed), "candidate": crel})
    return out, notes


def coverage(voc, rough: str, rd, hinted=None, stated=(), chunks=None) -> dict:
    """The accounting of one candidate reading `rd` against the rough sentence. See the module text. `stated`: the ids of
    operations the author named with --operation (the answer to ASK (operation)): asked for, though no word says them.
    `chunks`: for a candidate composed clause by clause, the clause each word of the rough sentence belongs to: a word of
    one clause of the author's is mapped only to pieces of the same clause of the candidate."""
    hinted = hinted or {}
    lx = lex(rough)
    if chunks is None:                           # the author's clauses against the candidate's, whenever they are as many
        ch = clause_chunks(rough)
        if len(ch) > 1 and len(rd.info["clauses"]) == len(ch):
            chunks = [next(k for k, (x, y, _) in enumerate(ch) if x <= i < y) for i in range(len(lx))]
    # THE SIDE OF A CONDITION, CLAUSE BY CLAUSE, ARGUMENT ORDER. The accounting is repeated, each time without the mappings the
    # pass before put on the wrong side of a condition (`wrong_side`) or in the wrong order of a comparison (`wrong_order`),
    # until a pass has none. The set only grows, so this ends.
    barred, notes = set(), []
    if chunks is not None:
        n = max(chunks) + 1
        for inst in Pieces(voc, rd).items:
            barred |= {(i, inst.n) for i, c in enumerate(chunks) if c != min(inst.clause, n - 1)}
    start = set(barred)
    while True:
        occ, P, spans, match = account(voc, lx, rd, hinted, barred)
        wo, ns = wrong_order(occ, P, lx)
        new = (wrong_side(occ, P, spans, match) | wo) - barred
        notes += [x for x in ns if x not in notes]
        if not new:
            break
        barred |= new
    refused = [{"word": occ[i]["word"], "piece": P.items[n].id + (" (negated)" if P.items[n].neg else "")} for i, n in sorted(barred - start)]
    def said_otherwise(i) -> bool:
        """Not ADDED though no word is mapped to it: the operation the author stated or the book restates; a role that is the
        one filler of its hole under a wordless piece that IS asked for ("every balance": the ledger); a domain piece that is
        the one way to make its category from a role that IS asked for ("out of the wallet": the wallet's balance)."""
        if i.kind == "op":
            return i.id in stated or i.repeat
        if i.kind == "choice":
            return i.forced and i.parent is not None and P.items[i.parent].kind == "silent" and P.items[i.parent].taken > 0
        par = P.items[i.parent] if i.parent is not None else None
        if par is not None and par.dir and par.dir[0] in ("EQ", "NE") and par.kind != "silent":
            # "from an account to itself": the reflexive stands for the other side of the equation
            sides = [ks for ks in par.holes.values()]
            if (any(o["inst"] == par.n and o["word"] in cues2.REFLEXIVES for o in occ)
                    and any(P.items[k].taken > 0 for ks in sides if i.n not in ks for k in ks)):
                return True
        if i.lone and par is not None and par.taken > 0:
            return True                          # "gives back ...": the result, the one thing of its kind the frame can be about
        if not i.forced:
            return False
        kids = {k for ks in i.holes.values() for k in ks}
        said = [o["i"] for o in occ if o["inst"] in kids and o["via"] not in LOOSE]
        # inside a condition, only by a word written in the span matched with that condition ("bumping the counter by zero":
        # "counter" is not in "by zero", so it does not ask for "the counter's count is zero")
        return any(not i.inner or where.get(w, set()) & set(i.inner) for w in said)

    where = {}
    for k, sp in enumerate(spans):
        if k in match:
            for o in sp["occ"]:
                where.setdefault(o["i"], set()).add(match[k])

    # a piece that compares (its form has comparison words: "never leaves ... above", "is at most") is asked for only by a
    # comparison word of the author's; its other words ("never", "leaves") do not ask for it
    text, starts = lexed_text(lx)
    relwords = {i for _, sp, _ in cues2.directions(text) for i in words_in(sp, starts, lx)}

    def unasked(i) -> bool:
        if i.kind in EXEMPT:
            return False
        if i.dir and i.dir[0] in ("LE", "GE", "GT", "LT") and not any(o["inst"] == i.n and o["i"] in relwords for o in occ):
            return True                          # (an equation is also said with "is", which is on the stop list: not required of it)
        return i.taken == 0 and not said_otherwise(i)

    added = [i for i in P.items if unasked(i)]
    dropped_spans = [" ".join(o["word"] for o in sp["occ"]) for k, sp in enumerate(spans) if k not in match]
    dropped = [o["word"] for o in occ if o["status"] == "DROPPED"]
    # askable: the operation is asked for, and so is every claim (some word of the author's is mapped into it)
    askable = not any(i.kind == "op" for i in added) and all(any(i.taken for i in P.items if i.claim == k) for k in range(P.claims))
    return {"words": [{k: o[k] for k in ("word", "status", "piece", "via")} for o in occ],
            "dropped": dropped, "added": [i.id + (" (negated)" if i.neg else "") for i in added],
            "condition_dropped": dropped_spans, "defaults_used": sorted({o["piece"] for o in occ if o["status"] == "DEFAULT"}),
            "spans": [" ".join(o["word"] for o in sp["occ"]) for sp in spans], "refused_mappings": refused, "order_refused": notes,
            "operation_stated": sorted(i.id for i in P.items if i.kind == "op" and i.id in stated and i.taken == 0),
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
        if cont and all(o["via"] == "phrase" for o in cont):
            return False                         # a word of a phrase cue ("and refused when it does not": the other half of an "exactly when")
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
        j = k + 1
        while j < len(words) - 1 and occ[j]["stem"] in narrow:      # "an accepted internal transfer": each word is a span
            j += 1
        if occ[k]["stem"] in narrow and occ[j]["stem"] in nouns and occ[k]["status"] != "STOP":
            spans.append({"occ": [occ[k]], "opener": []})
    # (plan node L1c) a preposition right after the operation's noun, or after the verb that names the operation, opens a
    # span too ("a transfer FROM an account to itself is refused", "bumping BY zero"): it runs to the next auxiliary, opener
    # or punctuation mark. Such a span is a condition the author put on the subject without a "that" or a "when".
    anchors = nouns | {t for i in P.items if i.kind == "op" for t in when_verbs(P.voc, P.voc.ops[i.id])}
    openers_at = {a for a, _ in at}
    pre = {}
    for k in range(len(words) - 1):
        if occ[k]["stem"] in anchors and words[k + 1] in cues2.PREPOSITIONS and occ[k + 1]["via"] != "form" and not lx[k + 1][1]:
            end = k + 2
            while end < len(words) and not lx[end][1] and end not in openers_at and words[end] not in STOP2 - {"a", "an", "the"}:
                end += 1
            if end in openers_at and end > k + 2:
                pre[end] = k + 1                 # "a lookup OF an account THAT is not in the ledger": one condition, not two
            elif end > k + 2:
                spans.append({"occ": [occ[j] for j in range(k + 1, end) if occ[j]["status"] != "STOP"], "opener": [occ[k + 1]]})
    for n, (a, b) in enumerate(at):
        end = at[n + 1][0] if n + 1 < len(at) else len(words)
        for j in range(b, end):
            if lx[j][1]:
                end = j
                break
        spans.append({"occ": [occ[j] for j in range(pre.get(a, a), end) if occ[j]["status"] != "STOP"],
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


def constant(voc, x) -> bool:
    """A term that does not depend on the call: a written number, or a piece of a `term` category with no hole ("zero", "the
    maximum")."""
    if isinstance(x, Leaf):
        return x.how != "role"
    if isinstance(x, Node) and not x.idiom and not x.args:
        p = voc.pieces.get(x.id) or {}
        return str(p.get("cat") or p.get("category") or "").startswith("term")
    return False


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
                    if all(constant(voc, a) for a in n.args.values()):
                        return "constants"
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


def system_vocab(voc) -> dict:
    """{system: every token of its name, of the nouns of its operations, and of its roles and their types} (shared or not)."""
    out = {}
    for o in voc.ops.values():
        b = out.setdefault(o["domain"], set())
        b |= set(v1.tokens(o["domain"]))
        for n in o["nouns"]:
            b |= set(v1.tokens(n))
        for r, t in o["state"] + o["input"]:
            b |= set(v1.tokens(r)) | set(v1.tokens(t))
    return out


def operation_question(voc, rough: str, domain: str | None):
    """Nothing is anchored. The systems the sentence has a word of, and their operations to choose from: None if no word of
    the sentence is a word of any system of the book (then the sentence is declined). A word only one system has settles
    the system, as in `anchor`; otherwise the operations of every system with a word in the sentence are listed."""
    R = frozenset(v1.tokens(rough))
    sv = system_vocab(voc)
    if domain is not None:
        systems, words = [domain], {domain: sorted(sv[domain] & R)}
    else:
        only = system_words(voc)
        hit = {d: sorted(only[d] & R) for d in sorted(sv) if only[d] & R}
        if len(hit) == 1:
            systems, words = sorted(hit), hit
        else:
            words = {d: sorted(sv[d] & R) for d in sorted(sv) if sv[d] & R}
            systems = sorted(words)
    if not systems:
        return None
    ops = [{"id": o["id"], "system": o["domain"], "noun": o["nouns"][0], "when": (o["when"] or [None])[0]}
           for d in systems for o in voc.ops.values() if o["domain"] == d]
    return {"systems": systems, "words": words, "operations": ops}


def stated_operation(voc, operation: str, domain: str | None) -> dict:
    """The operation `--operation` names: an id of the book ("w.withdraw"), or one of an operation's nouns ("withdrawal")."""
    ops = [o for o in voc.ops.values() if domain in (None, o["domain"])]
    got = [o for o in ops if o["id"] == operation] or [o for o in ops if operation.strip().lower() in [n.lower() for n in o["nouns"]]]
    if len(got) != 1:
        raise FeatureError(f"--operation {operation}: " + ("no such operation" if not got else "an operation of " + ", ".join(sorted(o["domain"] for o in got))
                           + " (give its id, or --domain)") + (f" in the system {domain}" if domain and not got else "")
                           + ". The operations: " + ", ".join(f"{o['id']} (\"{o['nouns'][0]}\")" for o in ops))
    return got[0]


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
    # (plan node L1c) an operation said by a verb phrase that is ordinary English for its noun ("putting money into": a
    # deposit; cues2.OP_SYNONYMS). Tried only when nothing is named and nothing is hinted.
    text = " ".join(w for w, _ in lex(rough))
    said_by = [o for o in ops if any(n in cues2.OP_SYNONYMS and re.search(cues2.OP_SYNONYMS[n], text) for n in o["nouns"])] if not (named or hinted) else []
    got = named or hinted or said_by
    res = {"by": "noun" if named else "the verb of a `when` form" if hinted else "a synonym of its noun" if said_by else None, "ops": got,
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

_BOOK = []


def load():
    """The book and the compiler, loaded once per process (a dialogue composes the same sentence several times)."""
    if not _BOOK:
        _BOOK.extend(v1.load())
    return _BOOK[0], _BOOK[1]


def candidate(voc, comp, rough, rd, sentence, rank, score, as_written, hinted, stated=(), chunks=None) -> dict:
    cov = coverage(voc, rough, rd, hinted, stated, chunks)
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


def compose(rough: str, domain: str | None = None, l3: bool = True, identity: bool = True, operation: str | None = None,
            exclude=()) -> dict:
    """`identity=False` skips the first step (a sentence of the book is its own answer): used only to measure what the
    generator reaches (compose_tests/v2.py). `operation`: the author's answer to ASK (operation), an id or a noun.
    `exclude`: term digests of candidates the author has turned down (a dialogue: clausal/dialogue.py)."""
    voc, comp = load()
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
    stated = ()
    if operation is not None:
        # the author's answer to ASK (operation): that one operation, in its system; nothing else is tried
        op = stated_operation(voc, operation, domain)
        a = {"by": "--operation", "ops": [op], "hinted": {}, "system": op["domain"], "system_by": "--operation", "systems": [op["domain"]], "settling_words": {}}
        stated = (op["id"],)
        res["operation_stated"] = {"id": op["id"], "noun": op["nouns"][0], "by": "--operation: the author's answer to the operation question; no word of the rough sentence names it"}
    else:
        a = anchor(voc, rough, domain)
    res["anchored_by"], res["system"], res["system_by"] = a["by"], a["system"], a["system_by"]
    res["operations_anchored"] = [o["id"] for o in a["ops"]]
    if not a["ops"]:
        why = "no operation of the Clausebook is named in the sentence (by a noun, or by the verb of a `when` form)" + (f" in the system {domain}" if domain else "")
        q = operation_question(voc, rough, domain)
        if q is not None:
            # ASK (operation): the sentence has words of a system of the book, so the book may be able to say it; which operation
            # it is about is the author's to say. Nothing is generated: version 2 does not try every operation.
            res.update(outcome="ASK", ask="operation", systems=q["systems"], operation_question=q,
                       system=q["systems"][0] if len(q["systems"]) == 1 else None,
                       system_by=None if len(q["systems"]) != 1 else "--domain" if domain else "words only that system has: " + ", ".join(q["words"][q["systems"][0]]),
                       why=why + ", but it has words of " + "; ".join(f"{d} ({', '.join(w)})" for d, w in q["words"].items() if w or domain)
                           + ". Which operation is your rule about? Run again with --operation ID. Nothing was generated: version 2 does not try every operation")
            return res
        res.update(outcome="DECLINE", why=why + ", and no word of it is a word of a system of the Clausebook. Version 2 does not try every operation.",
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
    # 2, 3. generate, rank, compile, filter, account (`gather`); 4. decide
    key = (rough, system, tuple(o["id"] for o in a["ops"]), stated)
    if key not in _GATHERED:
        _GATHERED[key] = gather(voc, comp, rough, a, system, stated)
    cands, counts = _GATHERED[key]
    return decide(res, [dict(c) for c in cands], dict(counts), l3, frozenset(exclude), a, system)


_GATHERED = {}       # (rough, system, operations, stated) -> (candidates, counts): a dialogue asks again without generating again


JOIN_TOP = {2: 6, 3: 4}      # clause by clause: the candidates kept per clause of the author's, for two and for three clauses
MAX_CHUNKS = 3


def hint_tokens(voc, rough: str) -> list:
    """Tokens added to the rough sentence's own FOR VERSION 1'S GENERATOR AND RANKING RULE ONLY (plan node L1c): the form
    words of the pieces that a phrase cue, a version 2 word cue or a comparison word of the sentence points to. Version 1
    generates a narrowing or a condition only if one of ITS cue words is in the sentence, and ranks by its own table; this
    is how a phrase ("goes through") reaches it without changing it. Coverage never sees these tokens."""
    lx = lex(rough)
    text, _ = lexed_text(lx)
    R = frozenset(v1.tokens(rough))
    out = []

    def forms_of(pid):
        p = voc.pieces.get(pid) or {}
        for k in ("vp_forms", "then_forms", "forms", "subject_forms"):
            for f in (p.get(k) or [])[:1]:
                out.extend(v1.tokens(literal(f)))

    for sense, pat in cues2.PHRASES:
        if re.search(pat, text):
            out += v1.tokens(cues2.SENSE_HINT[sense])
    # a piece one of whose cue words (either table) is in the sentence: its own form words, so that version 1 does not count
    # them as words that are not the author's
    for pid in sorted(set(v1.CUE_BAGS) | set(cues2.CUE2_BAGS) | set(cues2.CUE2_NEG_BAGS)):
        if (v1.CUE_BAGS.get(pid, frozenset()) | cues2.CUE2_BAGS.get(pid, frozenset()) | cues2.CUE2_NEG_BAGS.get(pid, frozenset())) & R:
            forms_of(pid)
    cond = bool(cues2.directions(text)) or bool((cues2.CUE2_BAGS["equals"] | cues2.CUE2_NEG_BAGS["equals"]) & R)
    if cond:
        out += v1.tokens("most least more exceed above below")
    if cond or any(tuple(w for w, _ in lx[k:k + len(op)]) == op for op in OPENERS for k in range(len(lx))):
        out.append("if")                         # version 1 writes "for which" only with one of its own condition words
    return [t for t in dict.fromkeys(out) if t not in R]


BEAM2 = {"claim": 6, "cond": 6, "": 10}       # version 2's generator keeps, per category: the best 6 claims and 6 conditions OF EACH
                                              # FRAME OR PIECE, and the best 10 of any other category (version 1: the best 30
                                              # claims, 12 conditions, 8 others, whatever their piece)


class Gen2(v1.Gen):
    """Version 1's generator with another rule for what is kept at each category (plan node L1c). Version 1 keeps the best 30
    claims and 12 conditions by its ranking rule, so one frame's variants can fill the list and a condition such as "the
    sender of the transfer equals the receiver of the transfer" is cut. Here the best BEAM2 of EACH frame or piece are kept,
    in version 2's order (`order2`). Nothing else differs; version 1 itself (`clausal compose`, arm A0) runs with its own."""

    def fill(self, cat: str, depth: int, voice: str = "") -> list:
        if self.parser.is_lexical(cat):
            return self.lexical(cat)
        if depth <= 0:
            return []
        key = (cat, depth, voice)
        if key in self.memo:
            return self.memo[key]
        self.memo[key] = []
        out = {}
        for group in self.forms(cat, voice):
            seen = {}
            for f in group:
                for x in self.expand(f, depth):
                    args = tuple(p.id for p in x.parts)
                    doubled = re.search(r"\b(\w+) (the )?\1\b", x.text) is not None
                    if args not in seen or (seen[args][0] and not doubled):
                        seen[args] = (doubled, x)
            for _, x in seen.values():
                out.setdefault(x.text, x)
        ranked = order2(self.voc, out.values(), self.rough)
        base = vocab.base_cat(cat)
        if base in ("claim", "cond"):
            kept, best = {}, []
            for x in ranked:
                k = x.parts[0].id
                kept[k] = kept.get(k, 0) + 1
                if kept[k] <= BEAM2[base]:
                    best.append(x)
        else:
            best = ranked[:BEAM2[""]]
        self.memo[key] = best
        return best


_MARKS = {}


def order2(voc, fills, rough: str) -> list:
    """THE ORDER IN WHICH GENERATED SENTENCES ARE COMPILED in version 2 (plan node L1c). Version 1's rule counts every book
    word the author did not write against a sentence ("balance" in "the wallet's balance") and counts the words version 2
    adds for the generator ("if", "which") for it; with phrase cues the sentence wanted was often past the compile limit.
    This order is by what the author's words give evidence for, piece by piece:
        evidence(p) = the author's stemmed words in p's form words, in either cue table for p, in the echo of a domain piece
                      outside its parentheses, in the verb of an operation's `when` form; and one mark per phrase cue of the
                      sentence whose sense p carries (a comparison word: every piece whose form compares)
        score = 4 * |union of evidence| - 3 * |pieces with none| - |leaves with none| - |pieces|
    then, as in version 1: the longer common subsequence with the author's words, fewer pieces, the shorter sentence, the
    sentence. It decides only WHICH sentences are compiled; coverage and the outcome do not use it."""
    if rough not in _MARKS:
        lx = lex(rough)
        text, _ = lexed_text(lx)
        senses = sense_ids(voc)
        marks = {}
        for sense, pat in cues2.PHRASES:
            if re.search(pat, text):
                for pid in senses[sense]:
                    marks.setdefault(pid, set()).add("§" + sense)
        for o in voc.ops.values():               # an operation said by a verb phrase for its noun
            if any(n in cues2.OP_SYNONYMS and re.search(cues2.OP_SYNONYMS[n], text) for n in o["nouns"]):
                marks.setdefault(o["id"], set()).add("§synonym")
        if cues2.directions(text):               # a comparison word of the author's: evidence for every piece whose form compares
            for pid, pc in voc.pieces.items():
                if cues2.directions(" ".join(literal(f).lower() for k in ("forms", "vp_forms", "then_forms") for f in pc.get(k) or [])):
                    marks.setdefault(pid, set()).add("§comparison")
        _, starts = lexed_text(lx)
        rel = {i for _, sp, _ in cues2.directions(text) for i in words_in(sp, starts, lx)}
        _MARKS.clear()
        # the author's comparison words ("no more than") are evidence for a piece that compares, through its mark, and for nothing else
        _MARKS[rough] = ({v1.stem(w) for i, (w, _) in enumerate(lx) if content(w) and i not in rel}, tuple(v1.tokens(rough)), marks, {})
    words, toks, marks, memo = _MARKS[rough]

    def ev(p):
        if p not in memo:
            own = p.strong | cues2.CUE2_BAGS.get(p.id, frozenset()) | cues2.CUE2_NEG_BAGS.get(p.id, frozenset())
            if p.id in voc.pieces:               # a domain piece: the words of its echo outside its parentheses, as in the accounting
                own |= cues2.echo_words(voc.pieces[p.id])
            elif p.id in voc.ops:
                own |= when_verbs(voc, voc.ops[p.id])
            memo[p] = frozenset(own & words) | frozenset(marks.get(p.id, ()))
        return memo[p]

    def key(x):
        got, none, bare = set(), 0, 0
        for p in x.parts:
            e = ev(p)
            got |= e
            if not e:
                if p.leaf:
                    bare += 1
                else:
                    none += 1
        return (-(4 * len(got) - 3 * none - bare - v1.n_pieces(x.parts)), -v1.lcs(toks, tuple(v1.tokens(x.text))), v1.n_pieces(x.parts), len(x.text), x.text)

    return sorted(fills, key=key)


def sequences(voc, ops: list, R: frozenset, rough: str) -> list:
    """The subjects tried: [(operations, tied?)]. Version 1's (single operations; two named operations in sequence with a
    sequencing word), and for plan node L1c: two ANCHORED operations in sequence (named, or said by a verb), and the
    same with the tie "with the same input" when the sentence has a word for it and the two take one type of input."""
    out = [(seq, False) for seq in v1.subject_ops(voc, ops, R)]
    said = {v1.stem(w) for w, _ in lex(rough)}       # version 1's tokens leave out "then"
    if not ({v1.stem(w) for w in v1.SEQUENCE_CUES.split()} | {"then"}) & said or not voc.sequences:
        return out
    tie = bool(cues2.CUE2_BAGS["same_input"] & said) and bool(voc.ties) and "same_input" in voc.pieces

    def at(o):                                   # where the operation is first said in the sentence (its noun or a verb of its `when` form)
        ws = [t for n in o["nouns"] for t in v1.tokens(n)] + sorted(when_verbs(voc, o))
        toks = v1.tokens(rough)
        return min((toks.index(w) for w in ws if w in toks), default=len(toks))

    import itertools
    for x, y in itertools.permutations(ops, 2):
        if x["domain"] != y["domain"] or [t for _, t in x["state"]] != [t for _, t in y["state"]] or at(x) >= at(y):
            continue                             # the two must be said at two places, in this order ("batch" names two operations at one place)
        clash = bool({r for r, _ in x["input"]} & {r for r, _ in y["input"]})
        if not clash and ([x, y], False) not in out:
            out.append(([x, y], False))
        if tie and [t for _, t in x["input"]] == [t for _, t in y["input"]]:
            out.append(([x, y], True))
    return out


def generate(voc, comp, text: str, ops: list, system, counts: dict, seen: set, projs) -> list:
    """Version 1's generator and ranking rule on `text` for the anchored operations; each sentence compiled and filtered.
    [(sentence, reading, compiles as written, version 1's score)], best-ranked first, one per Lean term."""
    toks = v1.tokens(text)
    toks = toks + hint_tokens(voc, text)
    R = frozenset(toks)
    numbers = list(dict.fromkeys(re.findall(r"\d+", text)))
    pool = {}
    for seq, tied in sequences(voc, ops, R, text):
        gen = Gen2(voc, seq, tuple(toks), numbers, text)
        head = None
        if tied:
            head = seq[0]["nouns"][0] + voc.sequences[0] + v1.article(seq[1]["nouns"][0]) + seq[1]["nouns"][0]
            tie_text = voc.ties[0] + (voc.pieces["same_input"].get("forms") or ["the same input"])[0]
            extra = (v1.piece_part(voc.pieces["tied"], voc.ties[0]), v1.piece_part(voc.pieces["same_input"], tie_text))
        for s in v1.sentences(voc, gen):
            if tied:
                if head not in s.text:
                    continue
                s = v1.Fill(s.text.replace(head, head + tie_text, 1), None, s.parts + extra)
            pool.setdefault(s.text, s)
    ranked = order2(voc, pool.values(), text)
    counts["generated"] += len(ranked)
    out = []
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
        out.append((s.text, rd, as_written, v1.score(s.parts, R, s.text)[0]))
    return out


def clause_chunks(rough: str) -> list:
    """THE CLAUSES OF THE AUTHOR'S SENTENCE (plan node L1c): it is cut before each "and" / "but" that follows a punctuation
    mark (", and", "; but"). [(first word index, end index, text of the clause without that "and")]. One clause: no cut."""
    lx = lex(rough)
    cuts = [0] + [i for i, (w, b) in enumerate(lx) if i and b and w in ("and", "but")] + [len(lx)]
    out = []
    for a, b in zip(cuts, cuts[1:]):
        ws = lx[a + (1 if a else 0):b]
        if not ws:
            return [(0, len(lx), rough)]
        out.append((a, b, "".join((", " if bd and k else " " if k else "") + w for k, (w, bd) in enumerate(ws))))
    return out if 1 < len(out) <= MAX_CHUNKS else [(0, len(lx), rough)]


def gather(voc, comp, rough, a, system, stated) -> tuple:
    """Generate, compile, filter and account. (candidates, counts). First the whole sentence as ONE clause (version 1's
    generator writes one clause). Then, if the author's sentence has two or three clauses (`clause_chunks`), CLAUSE BY
    CLAUSE: each clause of the author's is composed alone, for the operations it names itself or else those of the whole
    sentence ("..., and be refused when it doesn't": the subject is not said again); the best JOIN_TOP of each (fewest words
    dropped and pieces added within the clause, then version 1's rank) are joined with the book's clause separator, every
    combination compiled and filtered like any other candidate, and accounted against the WHOLE sentence, each word of a
    clause of the author's only to pieces of the same clause of the candidate."""
    counts = {"generated": 0, "compiled": 0, "refused": 0, "another_composition": 0, "same_term": 0,
              "filtered": {"other-book": 0, "opposite-narrowing": 0, "by-zero": 0, "same-sides": 0, "constants": 0}, "passed": 0, "clause_by_clause": None}
    cands, seen = [], set()
    projs = list(projects.load(ROOT))
    for text, rd, as_written, sc in generate(voc, comp, rough, a["ops"], system, counts, seen, projs):
        cands.append(candidate(voc, comp, rough, rd, text, len(cands) + 1, sc, as_written, a["hinted"], stated))
    chunks = clause_chunks(rough)
    if len(chunks) > 1 and voc.clause_seps:
        import itertools
        lx = lex(rough)
        chunk_of = [next(k for k, (x, y, _) in enumerate(chunks) if x <= i < y) for i in range(len(lx))]
        hinted, per = dict(a["hinted"]), []
        for _, _, text in chunks:
            ak = anchor(voc, text, system)
            ops = [o for o in ak["ops"] if o["domain"] == system] or a["ops"]
            hinted.update(ak["hinted"])
            got = []
            for t, rd, aw, sc in generate(voc, comp, text, ops, system, counts, set(), projs):
                cov = coverage(voc, text, rd, hinted, tuple(o["id"] for o in ops))
                got.append((len(cov["dropped"]) + len(cov["added"]) + 2 * len(cov["condition_dropped"]), len(got), t))
            per.append([t for _, _, t in sorted(got)[:JOIN_TOP[len(chunks)]]])
        joined = 0
        for combo in itertools.product(*per):
            text = voc.clause_seps[0].join([combo[0]] + [t[0].lower() + t[1:] for t in combo[1:]])
            joined += 1
            rd = v1.compile_sentence(comp, text, None)
            as_written = not isinstance(rd, Problem)
            if not as_written:
                rd = v1.compile_sentence(comp, text, system)
            if isinstance(rd, Problem) or rd.info["domain"] != system or len(rd.info["clauses"]) != len(chunks):
                counts["refused"] += 1
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
            c = candidate(voc, comp, rough, rd, text, len(cands) + 1, None, as_written, hinted, stated, chunk_of)
            c["clause_by_clause"] = True
            cands.append(c)
        counts["clause_by_clause"] = {"clauses": [t for _, _, t in chunks], "kept_per_clause": [len(x) for x in per], "joined": joined}
    return cands, counts


def decide(res: dict, cands: list, counts: dict, l3: bool, exclude: frozenset, a: dict, system) -> dict:
    """The outcome, from the candidates that pass the filters. `exclude`: the term digests of candidates the author has
    turned down in a dialogue (clausal/dialogue.py): they are not shown again and cannot be the answer."""
    if exclude:
        counts["excluded_by_the_author"] = sum(c["term_sha256"] in exclude for c in cands)
        cands = [c for c in cands if c["term_sha256"] not in exclude]
    res["counts"] = counts
    full = [c for c in cands if c["coverage"]["full"]]
    askable = [c for c in cands if c["coverage"]["askable"] and not c["coverage"]["full"]]
    if full:
        return decide_full(res, full, l3)
    if askable:
        # which to show: those that drop no condition first, then the fewest words dropped and pieces added (a role of the
        # operation that is added, "the amount", counts half: it is what a sentence most often leaves unsaid), then the rank. (L1ab showed by version 1's rank alone; with the accounting of L1c the count is the better order on the
        # development set: see COMPOSE2.md.)
        show = sorted(askable, key=lambda c: (bool(c["coverage"]["condition_dropped"]),
                                              len(c["coverage"]["dropped"]) + sum(0.5 if x.startswith('"the ') else 1 for x in c["coverage"]["added"]), c["rank"]))[:SHOW]
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
                    + f" (refused by the compiler: {counts['refused']}; filtered: " + ", ".join(f"{k} {v}" for k, v in counts["filtered"].items()) + ")"
                    + (f"; turned down by the author: {counts['excluded_by_the_author']}" if exclude else "")),
               decline={"unmapped": best["coverage"]["dropped"] if best else [w for w, _ in lex(rough_of(res)) if content(w)],
                        "nearest": nearest(v1.load()[0], rough_of(res), system), "operations": [o["nouns"][0] for o in a["ops"]]})
    return res


def rough_of(res: dict) -> str:
    return res["rough"]


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
            "operation_stated": res.get("operation_stated"),
            "books": [{"book": b.rel, "sha256": hashlib.sha256(b.text.encode()).hexdigest()} for b in voc.books],
            "checks": {"compiled": True, "tree_round_trip": c["tree"] is not None, "outcome": res["outcome"], "ask": res["ask"],
                       "coverage": {k: c["coverage"][k] for k in ("dropped", "added", "condition_dropped", "defaults_used", "refused_mappings", "operation_stated", "full")},
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
    if cov["refused_mappings"]:
        o.append("     not mapped (the word is not written in the condition this piece is in): "
                 + ", ".join(f"{m['word']} -/-> {m['piece']}" for m in cov["refused_mappings"]))
    for x in cov.get("order_refused") or []:
        o.append(f"     ARGUMENT ORDER: your \"{x['words']}\" is not mapped to {x['piece']}: with the words on each side of it as you wrote them, "
                 f"yours says {' or '.join(x['yours'])} and this sentence says {x['candidate']} (LE at most, GE at least, GT more than, LT less than)")
    if cov["operation_stated"]:
        o.append("     the operation is yours by --operation; no word of the sentence names it: " + ", ".join(cov["operation_stated"]))
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
    q = res.get("operation_question")
    if q:
        o.append("")
        o.append("  operations to choose from:")
        o += [f"    --operation {x['id']:<16}{x['system']}: \"{x['noun']}\"" + (f" (\"{x['when']}\")" if x["when"] else "") for x in q["operations"]]
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

    domain, ack, by, write, operation = opt("--domain"), opt("--acknowledge"), opt("--by"), opt("--write"), opt("--operation")
    as_json, no_l3 = "--json" in argv, "--no-l3" in argv
    rest = [a for a in argv if not a.startswith("--")]
    if len(rest) != 1:
        print(__doc__)
        return 2
    try:
        res = compose(rest[0], domain, l3=not no_l3, operation=operation)
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
