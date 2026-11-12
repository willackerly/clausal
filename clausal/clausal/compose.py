"""clausal compose: CANDIDATE CANONICAL SENTENCES for a rough English sentence (plan node L1, suggest mode, first version).

    python3 -m clausal compose "<rough English>" [--domain D] [--json] [--top N] [--ask K] [--no-ask]
                                                 [--choose K] [--write FILE.feature]

Given a sentence in ordinary English, this lists sentences of the Clausebook that are close to it. It is a
phrasing aid. It adds no form to the language, it is not a step of run.sh and it changes no verdict.

NO LANGUAGE MODEL IS USED. The steps are:

  1. tokenise  lower-case words of the rough sentence, minus STOP, through `stem` (a fixed suffix stripper);
  2. anchor    the operations whose nouns, `when` form or echo share a token with the sentence (all operations of
               the system if none does);
  3. generate  for each anchored operation (or two anchored operations in sequence, if the sentence has a
               sequencing cue): fill the typed holes of the book's forms top-down, to DEPTH pieces, leaves being the
               operation's roles ("the ledger", "the amount") and the numbers written in the rough sentence. One
               form per piece (see `Gen.forms`). At every category only the BEAM best fillers are kept;
  4. rank      by the RANKING RULE below (`score`), a deterministic function of the tokens, the forms used and CUES;
  5. verify    the best COMPILE_LIMIT sentences are compiled with the ordinary compiler (`vocab.Compiler.rule`).
               A sentence is kept only if it compiles, to the composition it was generated from. Readings with the
               same Lean term are merged (the best-ranked sentence stays);
  6. ask       (interactive mode) for the top candidates that differ, `clausal separate` (plan node L3) is asked
               for an input on which one holds and the other fails, and the question is printed. Nothing is chosen
               unless the author chooses.

EVERY SENTENCE PRINTED COMPILES AS WRITTEN: `checked` recompiles each candidate just before output and raises if
one does not come back as the same Lean term. The reading shown beside a candidate is the compiler's own echo.

THE RANKING RULE (frozen with CUES, STOP, IRREGULAR, the limits below and the form choice before the first run on the
48 trial sentences; see clausal/COMPOSE.md):

    R        the set of tokens of the rough sentence
    parts    the pieces of a candidate (operation, scoping modifiers, frames, modifiers, domain words) and its leaves
    strong(p)  tokens of the literal words of the form of p that the candidate uses, of an operation's nouns, of a
               leaf's own words, and CUES[p]
    weak(p)    tokens of the echo of p (and of an operation's `when` form and echo)
    score = W_STRONG * |{t in R : t in strong(p) for some part p}|
          + W_WEAK   * |{t in R : t in weak(p) for some part p, and in no strong(p)}|
          - UNSUPPORTED * |{pieces p with some cue word, none of them in R}|
          - FOREIGN  * |{tokens of the candidate sentence that are not in R}|
          - PIECE    * |pieces|
    order: higher score first; then the longer common subsequence of the rough sentence's tokens and the candidate's
    tokens (the author's word order); then fewer pieces; then the shorter sentence; then the sentence, alphabetically.

    NOTHING THE AUTHOR DID NOT ASK FOR NARROWS THE RULE: a scoping piece (successful, rejected, internal, "for which",
    "followed by") is generated only if one of its cue words (CUES) is in R, and a second claim is joined by "and"
    only if the frames of both claims have a cue word in R. Operations: those with a noun token in R; if there is
    none, those whose `when` form or echo has a token in R; if there is none, every operation.

--json is the non-interactive mode (what plan node L4 scores): ranked candidates, `chosen` is the top one, taken with no
human choice. --write puts the chosen sentence into a .feature file and is never implied.

WHERE A LANGUAGE MODEL COULD SIT: `model_hook` (below). It is not called with any model here.
"""
from __future__ import annotations

import functools
import itertools
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from . import vocab
from .core import Feature, FeatureError, Problem, Rule, load_glossary, parse_feature
from .pipeline import ROOT

# --------------------------------------------------------------------------------------------- FROZEN PARAMETERS
SCHEMA = "clausal-compose-v1"
CANDIDATE_LIMIT = 10     # the most candidates ever returned (--top is capped by it)
DEFAULT_TOP = 5
ASK_DEFAULT = 3          # interactive mode: the top K candidates are compared pairwise through `clausal separate`
DEPTH = 4                # pieces below a claim or a condition, the leaf included
BEAM = {"claim": 30, "cond": 12, "": 8}       # fillers kept per category (after ranking)
PAIR_CLAIMS = 8          # two claims joined by "and" are tried among the best PAIR_CLAIMS claims of one voice
PRODUCT_LIMIT = 4000     # hole fillings tried per form
COMPILE_LIMIT = 150      # sentences compiled per run, best-ranked first
W_STRONG, W_WEAK, UNSUPPORTED, FOREIGN, PIECE = 4, 2, 2, 2, 1

STOP = set("""a an the of to in on at by for from with as is are be been being was were it its this these those who
and or do does did will would shall should must can could may might has have had there here than then so such also any into onto
about between per i we you they them their call calls operation operations system""".split())

# words the suffix stripper does not bring together
IRREGULAR = {"withdrawal": "withdraw", "withdrawals": "withdraw", "computation": "compute", "rejection": "reject",
             "acceptance": "accept", "successful": "succeed", "successfully": "succeed", "success": "succeed",
             "larger": "large", "smaller": "small", "greater": "great", "bigger": "big", "fewer": "few", "lower": "low",
             "higher": "high", "cannot": "not", "none": "no", "nothing": "no", "each": "every", "equals": "equal",
             "sum": "total", "identical": "same", "unchanged": "unchanged", "unaffected": "unchanged",
             "untouched": "unchanged", "unmodified": "unchanged", "fails": "fail", "failed": "fail", "failing": "fail",
             "failure": "fail", "lost": "lose", "loses": "lose", "losing": "lose",
             "succeed": "succeed", "succeeds": "succeed", "succeeded": "succeed", "succeeding": "succeed",
             "exceed": "exceed", "exceeds": "exceed", "exceeded": "exceed", "exceeding": "exceed"}

# ORDINARY-ENGLISH CUES per piece, beside the words of the piece's own forms and echo (which come from the book).
# Each line is justified by what the piece MEANS (its Lean definition and echo in clausebook.yaml), not by any trial
# sentence. A cue only moves a candidate up or down the list: what a candidate means is what the compiler says it means.
CUES = {
    # ---- frames
    "always_answers": "answer respond return terminate panic crash abort hang halt loop finish complete",   # D1: an answer for every input
    "never_changes": "unchanged same preserve conserve keep constant invariant alter modify affect remain stay equal create destroy",  # after = before
    "changes_only": "only other else unchanged rest remaining",        # every other part has what it had before
    "always": "always every",                                          # the class holds of every call in scope
    "never": "never no not",                                           # the class holds of no call in scope
    "if_then": "whenever when if enough sufficient cover",             # condition -> accepted
    "only_if": "only unless require need necessary",                   # accepted -> condition
    "exactly_when": "exactly precisely iff only if whenever",          # accepted <-> condition
    "rejected_unchanged": "reject fail refuse deny decline error no unchanged effect intact",   # a rejection, and state after = state before
    "increases_by": "increase add grow gain credit rise receive more plus exactly",  # after = before + t
    "decreases_by": "decrease subtract reduce lose debit drop deduct less minus exactly",  # after + t = before
    "becomes": "become now afterwards end set",                        # the measure after the call is t
    "result_is": "return result answer give report equal",             # the answer's quantity is t
    "result_at_most": "most exceed more above over bound",             # the answer's quantity <= t
    "result_at_least": "least below under fewer bound",                # t <= the answer's quantity
    "at_most": "most exceed above over overflow cap bound limit maximum",   # the measure after the call <= t
    "at_least": "least below under negative minimum bound limit",      # t <= the measure after the call
    "every_of": "every all afterwards",                                # every item read off the answer satisfies p afterwards
    "none_of": "no never afterwards",                                  # no item read off the answer satisfies p afterwards
    "monotone": "still also keep lose monotone remain",                # accepted for the first call -> accepted for the second
    "agrees_with": "agree match same equal equivalent like behave reference",   # answer and state = the reference's
    "same_answer": "same depend independent regardless irrespective matter answer",   # the two calls give the same answer
    "same_answer_if": "same depend independent regardless irrespective matter answer if",
    "within": "among subset only",                                     # every item read off the answer is in the collection
    "covers": "all every include",                                     # every item of the collection is read off the answer
    # ---- scoping modifiers and the operation's own acceptance
    "successful": "succeed accept ok valid complete",                  # accepted calls only
    "rejected": "reject fail refuse deny decline invalid unsuccessful error",   # rejected calls only
    "internal": "internal exist existing member",                      # every party the input names is a member of the state
    "given": "which that where whose when if provided assuming given",      # a condition on the state before the call and the input
    "and_then": "follow then after afterwards subsequent",             # a second call on the state the first leaves
    "accepted": "accept succeed ok allow permit go through",           # the answer is an acceptance
    # ---- modifiers
    "aggregate": "total overall combined altogether money funds whole",    # the sum of a collection of numbers
    "is": "is equal exactly",                                          # m = t
    "not_more_than": "most cover enough sufficient afford least exceed not more",   # t <= m
    "more_than": "exceed more great above over insufficient",          # m < t
    "exceeds": "exceed more great above over",                         # t < m
    "at_most_value": "most within exceed not more fit",                # m <= t
    "sum_within": "overflow fit room exceed within not",               # m + t <= z
    "sum_exceeds": "overflow exceed more above over",                  # z < m + t
    "zero": "zero empty no",                                           # 0
    "not": "not no never",                                             # the negation of the one condition it is written on
    "every": "every all",
    "no_such": "no never",
    "some_of": "some any least one",
    "the_first": "first",
}
SEQUENCE_CUES = "follow then after afterwards subsequent"      # two operations in sequence are tried only with one of these
# (Integration with plan nodes Q3 and Q4: the verb phrases "is always accepted" / "is always rejected" are forms of the book
# now, and the class a form leaves unwritten is the book's `implied:` field. Nothing of either is a constant here any more.)


# --------------------------------------------------------------------------------------------- tokens

@functools.lru_cache(maxsize=None)
def stem(w: str) -> str:
    w = w.lower()
    if w.endswith("'s"):
        w = w[:-2]
    if w in IRREGULAR:
        return stem(IRREGULAR[w]) if IRREGULAR[w] != w else w
    if w.isdigit() or len(w) <= 3:
        return w
    for suf, rep in (("ies", "y"), ("ied", "y"), ("sses", "ss"), ("ing", ""), ("ed", ""), ("es", ""), ("s", "")):
        if w.endswith(suf) and len(w) - len(suf) >= 3 and not (suf == "s" and w.endswith("ss")):
            w = w[:len(w) - len(suf)] + rep
            break
    if len(w) > 3 and w[-1] == w[-2] and w[-1] not in "aeiouls":
        w = w[:-1]
    if len(w) >= 4 and w.endswith("e"):
        w = w[:-1]
    return w


def words(text: str) -> list:
    return re.findall(r"[a-z]+(?:'s)?|\d+", text.lower())


def tokens(text: str) -> list:
    """The stemmed content words of a text, in order, without repeats."""
    out = []
    for w in words(text):
        if w in STOP or (w.endswith("'s") and w[:-2] in STOP):
            continue
        s = stem(w)
        if s and s not in out:
            out.append(s)
    return out


@functools.lru_cache(maxsize=None)
def bag(text: str) -> frozenset:
    return frozenset(tokens(re.sub(r"\{[^}]*\}", " ", text or "")))


CUE_BAGS = {k: bag(v) for k, v in CUES.items()}


# --------------------------------------------------------------------------------------------- parts and scores

@dataclass(frozen=True)
class Part:
    """One piece (or leaf) of a candidate, with the tokens that count as evidence for it."""
    id: str
    strong: frozenset
    weak: frozenset
    leaf: bool = False


@dataclass(frozen=True)
class Fill:
    text: str
    key: str | None          # vocab.describe of the tree this spells; None when it is not predicted (idioms)
    parts: tuple


def supported(p: Part, R: frozenset) -> bool:
    return bool((p.strong | p.weak) & R)


def score(parts, R: frozenset, text: str) -> tuple:
    """(score, strong tokens, weak-only tokens, unsupported piece ids, foreign tokens). THE RANKING RULE: see the module text."""
    strong, weak, unsupported = set(), set(), []
    for p in parts:
        s, w = p.strong & R, p.weak & R
        strong |= s
        weak |= w
        if not p.leaf and (p.strong or p.weak) and not s and not w and p.id not in unsupported:
            unsupported.append(p.id)
    weak -= strong
    foreign = sorted(bag(text) - R)
    return (W_STRONG * len(strong) + W_WEAK * len(weak) - UNSUPPORTED * len(unsupported) - FOREIGN * len(foreign)
            - PIECE * n_pieces(parts), strong, weak, unsupported, foreign)


def n_pieces(parts) -> int:
    return len([p for p in parts if not p.leaf])


def lcs(a: tuple, b: tuple) -> int:
    """Length of the longest common subsequence of two token sequences."""
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b, 1):
            cur.append(prev[j - 1] + 1 if x == y else max(prev[j], cur[j - 1]))
        prev = cur
    return prev[-1]


def order(items, toks: tuple, text=lambda x: x.text, parts=lambda x: x.parts) -> list:
    R = frozenset(toks)
    return sorted(items, key=lambda x: (-score(parts(x), R, text(x))[0], -lcs(toks, tuple(tokens(text(x)))),
                                        n_pieces(parts(x)), len(text(x)), text(x)))


def piece_part(owner: dict, form_text: str = "") -> Part:
    return Part(owner["id"], bag(form_text) | CUE_BAGS.get(owner["id"], frozenset()),
                bag(owner.get("echo", "")) | bag(owner.get("not_echo", "")))


def op_part(op: dict) -> Part:
    return Part(op["id"], frozenset(t for n in op["nouns"] for t in tokens(n)),
                frozenset(t for w in op["when"] for t in bag(w)) | bag(op.get("echo", "")))


# --------------------------------------------------------------------------------------------- the book

def load():
    """The Clausebook through its existing loader, and the ordinary compiler."""
    gl = load_glossary(ROOT / "glossary.yaml", "glossary.yaml")
    voc = vocab.load_project(ROOT, gl)
    return voc, vocab.Compiler(voc)


def compile_sentence(comp, sentence: str, hint=None):
    """The ordinary compiler on one Rule line: a vocab.Reading, or a Problem."""
    f = Feature(path="<compose>", name="compose", slug="compose")
    return comp.rule(Rule(feature=f, name=sentence, line=1, tags=["@id:candidate"]), hint)


def term(rd) -> str:
    return rd.lean_def().split(":=", 1)[1].strip()


def reading_key(rd) -> str:
    return " | ".join(c["key"] for c in rd.info["clauses"])


# --------------------------------------------------------------------------------------------- generation

class Gen:
    """Every filler of a category for one subject (an operation, or two in sequence), best BEAM kept."""

    def __init__(self, voc, ops: list, toks: tuple, numbers: list, rough: str):
        self.voc, self.ops, self.toks, self.R, self.numbers, self.rough = voc, ops, toks, frozenset(toks), numbers, rough.lower()
        self.domain = ops[0]["domain"]
        self.roles = {}
        for o in ops:
            self.roles.update(vocab.op_roles(o, voc))
        self.parser = vocab.Parser(voc, self.domain, "rule", self.roles)
        self.memo = {}

    def lexical(self, cat: str) -> list:
        texts = [r for r in self.roles] + list(self.numbers)
        pt = self.voc.pts.get(cat) or {}
        texts += [e for e in pt.get("enum", []) if str(e).lower() in self.rough]
        out = []
        for t in texts:
            leaf = self.parser.lexical(cat, str(t))
            if leaf is not None:
                out.append(Fill(str(t), str(t), (Part("leaf:" + str(t), bag(str(t)) | frozenset([str(t).lower()]), frozenset(), True),)))
        return out

    def allowed(self, owner: dict) -> bool:
        """What vocab.Compiler.answer_check and op_check would refuse is not generated."""
        if owner.get("answer") and owner["answer"] != self.ops[-1]["answer"]:
            return False
        if owner.get("for_op") and (len(self.ops) != 1 or self.ops[0]["id"] != owner["for_op"]):
            return False
        return True

    def forms(self, cat: str, voice: str) -> list:
        """The forms of a category, grouped: [[Form, ...]] with one group per (piece, negated?, variant, holes).
        Forms of one group spell the same composition; `expand` takes the first of them (the first as listed in the
        book), unless it would say a word twice in a row ("the transfer the transfer", "account the account"), then the next."""
        groups = {}
        for f in self.parser.forms_for(cat, voice):
            if not self.allowed(f.owner):
                continue
            holes = tuple(sorted(s[1] for s in f.segs if s[0] == "hole"))
            groups.setdefault((f.owner["id"], f.neg, f.variant, f.idiom, holes), []).append(f)
        return list(groups.values())

    def fill(self, cat: str, depth: int, voice: str = "") -> list:
        if self.parser.is_lexical(cat):
            return self.lexical(cat)
        if depth <= 0:
            return []
        key = (cat, depth, voice)
        if key in self.memo:
            return self.memo[key]
        self.memo[key] = []                       # a form whose hole has its own category does not recurse for ever
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
        best = order(out.values(), self.toks)[:BEAM.get(vocab.base_cat(cat), BEAM[""])]
        self.memo[key] = best
        return best

    def expand(self, f, depth: int) -> list:
        holes = [s for s in f.segs if s[0] == "hole"]
        choices = [self.fill(*vocab.hole_voice(s[2])[:1], depth - 1, vocab.hole_voice(s[2])[1]) for s in holes]   # `class@first`: the form of that position
        if any(not c for c in choices):
            return []
        own = [piece_part(f.owner, f.text)] if not f.idiom else [Part(f.owner["id"], bag(f.owner["form"]), frozenset())]
        if f.neg:
            own.append(piece_part(self.voc.pieces["not"]))
        out = []
        for combo in itertools.islice(itertools.product(*choices), PRODUCT_LIMIT):
            it = iter(combo)
            text = "".join(s[1] if s[0] == "lit" else next(it).text for s in f.segs)
            parts = list(own)
            for c in combo:
                parts += c.parts
            out.append(Fill(text, self.key(f, holes, combo, parts), tuple(parts)))
        return out

    def key(self, f, holes, combo, parts) -> str | None:
        """vocab.describe of the tree vocab.Parser._build and Compiler.rule_part make of this form."""
        if f.idiom or any(c.key is None for c in combo):
            return None
        id_ = f.owner["id"]
        args = [c.key for c in combo]
        if id_ == "changes_only":
            by = {s[1]: c.key for s, c in zip(holes, combo)}
            args = [by["c"], by["x"] + " + " + by["y"]]
        for hole, pid in (f.owner.get("implied") or {}).items():      # a hole the form does not write: the book's `implied:`
            if hole not in [s[1] for s in holes]:
                args.append(pid)
                parts.append(piece_part(self.voc.pieces[pid]))
        k = id_ + ("(" + ", ".join(args) + ")" if args else "")
        return f"not({k})" if f.neg else k


def article(noun: str) -> str:
    return "an " if noun[0] in "aeiou" else "a "


def subjects(voc, gen: Gen) -> list:
    """[(text, key, parts)] for every scoping of the subject: none / successful / rejected / internal, with and without
    'for which <condition>'."""
    ops = gen.ops
    conds = [None] + (gen.fill("cond", DEPTH) if CUE_BAGS["given"] & gen.R and voc.relatives else [])
    out = []
    mods = [None, "successful", "rejected"] + (["internal"] if len(ops) == 1 and "internal" in ops[0] else [])
    for m in mods:
        if m and not CUE_BAGS[m] & gen.R:
            continue
        # the word each scoping piece is WRITTEN with is the book's live one (Q3, Q4: `successful` is written "accepted"),
        # and so are the words that join a sequence and a condition to the subject. A piece with no live word is not written.
        if m and m not in voc.live_word or (len(ops) > 1 and not voc.sequences):
            continue
        w = voc.live_word[m] if m else None
        head = (article(w) + w + " " if m else article(ops[0]["nouns"][0])) + ops[0]["nouns"][0]
        for o in ops[1:]:
            head += voc.sequences[0] + article(o["nouns"][0]) + o["nouns"][0]
        parts = [op_part(o) for o in ops]
        if len(ops) > 1:
            parts.append(piece_part(voc.pieces["and_then"], voc.sequences[0]))
        if m:
            parts.append(piece_part(voc.pieces[m], w))
        key = "+".join(o["id"] for o in ops) + ("/" + m if m else "")
        for c in conds:
            if c is None:
                out.append((head, key, tuple(parts)))
            elif c.key is not None:
                out.append((head + voc.relatives[0] + c.text, key + "/given " + c.key,
                            tuple(parts) + (piece_part(voc.pieces["given"], voc.relatives[0]),) + c.parts))
    return out


def sentences(voc, gen: Gen) -> list:
    """[Fill]: every sentence for this subject, one clause, one claim or two joined by "and"."""
    subs = subjects(voc, gen)
    by_voice = {}
    for voice in ("vp", "then"):
        cl = gen.fill("claim", DEPTH, voice)
        if voice == "then":      # a frame with a Rule voice is written in it; "For <subject>, ..." is for the frames with none
            vp_frames = {p.parts[0].id for p in by_voice["vp"]}
            cl = [c for c in cl if c.parts[0].id not in vp_frames]
        by_voice[voice] = cl
    out = []
    for voice, claims in by_voice.items():
        singles = [(c.text, c.key, c.parts) for c in claims]
        top = [c for c in claims if supported(c.parts[0], gen.R)][:PAIR_CLAIMS]
        pairs = [(a.text + " and " + b.text, None if a.key is None or b.key is None else a.key + " & " + b.key, a.parts + b.parts)
                 for a, b in itertools.combinations(top, 2)]
        for ctext, ckey, cparts in singles + pairs:
            for stext, skey, sparts in subs:
                text = f"{stext} {ctext}" if voice == "vp" else f"for {stext}, {ctext}"
                out.append(Fill(text[0].upper() + text[1:], None if ckey is None else f"{skey} :: {ckey}", sparts + cparts))
    return out


# --------------------------------------------------------------------------------------------- the model hook

def model_hook(rough: str, voc, ranked: list) -> tuple:
    """=== HOOK FOR A LANGUAGE MODEL: NOT IMPLEMENTED, NOTHING IS CALLED ===

    A later version may let a language model (a) PROPOSE further sentences and (b) REORDER the list. The contract:

      * it is given the rough sentence, the book (`voc`) and the ranked sentences (strings);
      * it returns (extra_sentences, order): strings to add, and a permutation of the final list, or None;
      * it is TRUSTED FOR NOTHING. Every sentence it proposes goes through `compile_sentence` exactly like a
        generated one and is dropped unless it compiles; the reading shown is the compiler's echo, never the model's
        words; it cannot add a form, and in interactive mode the author still answers the separating questions.

    This version returns nothing, so the list is exactly what the deterministic rule above produces."""
    return [], None


# --------------------------------------------------------------------------------------------- the whole question

def anchors(voc, R: frozenset, domain: str | None) -> tuple:
    ops = [o for o in voc.ops.values() if domain in (None, o["domain"])]
    named = [o for o in ops if op_part(o).strong & R]
    hinted = [o for o in ops if op_part(o).weak & R]
    return (named or hinted or ops), ("noun" if named else "when form or echo" if hinted else None)


def subject_ops(voc, ops: list, R: frozenset) -> list:
    """Single operations, and pairs in sequence when both are named by a noun and the sentence has a sequencing cue."""
    out = [[o] for o in ops]
    if bag(SEQUENCE_CUES) & R:
        named = [o for o in ops if op_part(o).strong & R]
        for a, b in itertools.permutations(named, 2):
            if a["domain"] == b["domain"] and [t for _, t in a["state"]] == [t for _, t in b["state"]] \
                    and not {r for r, _ in a["input"]} & {r for r, _ in b["input"]}:
                out.append([a, b])
    return out


def compose(rough: str, domain: str | None = None, top: int = DEFAULT_TOP) -> dict:
    voc, comp = load()
    systems = sorted({o["domain"] for o in voc.ops.values()})
    if domain is not None and domain not in systems:
        raise FeatureError(f"--domain {domain}: the systems of the Clausebook are {', '.join(systems)}")
    toks = tokens(rough)
    R = frozenset(toks)
    numbers = list(dict.fromkeys(re.findall(r"\d+", rough)))
    ops, anchored = anchors(voc, R, domain)
    pool = {}
    for seq in subject_ops(voc, ops, R):
        gen = Gen(voc, seq, tuple(toks), numbers, rough)
        for s in sentences(voc, gen):
            pool.setdefault(s.text, (s, seq[0]["domain"]))
    ranked = order(pool.values(), tuple(toks), text=lambda x: x[0].text, parts=lambda x: x[0].parts)
    extra, _reorder = model_hook(rough, voc, [s.text for s, _ in ranked[:COMPILE_LIMIT]])      # returns nothing: see the hook
    assert not extra and _reorder is None, "the model hook is not implemented in this version"
    top = max(1, min(top, CANDIDATE_LIMIT))
    out, seen_terms = [], {}
    refused = {"did_not_compile": 0, "another_composition": 0, "same_term_as_a_better_candidate": 0, "reads_in_two_systems": [],
               "ambiguous_as_written": []}
    tried = 0
    for s, d in ranked[:COMPILE_LIMIT]:
        if len(out) >= top:
            break
        tried += 1
        rd = compile_sentence(comp, s.text, domain)
        if isinstance(rd, Problem):
            in_d = compile_sentence(comp, s.text, d) if domain is None else rd
            if not isinstance(in_d, Problem) and len(refused["reads_in_two_systems"]) < 5:
                refused["reads_in_two_systems"].append(s.text)     # AMBIGUOUS as written: it would need scenarios of one system beneath it
                # the same sentences with what the author needs to act on them: the systems each reads in, and the rank of the
                # candidate it was ranked ahead of (`render` prints these whether or not there are candidates)
                refused["ambiguous_as_written"].append({
                    "sentence": s.text, "ahead_of_rank": len(out) + 1,
                    "systems": [x for x in systems if not isinstance(compile_sentence(comp, s.text, x), Problem)]})
            refused["did_not_compile"] += 1
            continue
        if s.key is not None and reading_key(rd) != s.key:
            refused["another_composition"] += 1
            continue
        t = term(rd)
        if t in seen_terms:
            refused["same_term_as_a_better_candidate"] += 1
            continue
        seen_terms[t] = s.text
        sc, strong, weak, unsupported, foreign = score(s.parts, R, s.text)
        out.append({"rank": len(out) + 1, "sentence": s.text, "system": rd.info["domain"], "score": sc,
                    "explained": {"by_form_or_cue": [t_ for t_ in toks if t_ in strong], "by_echo_only": [t_ for t_ in toks if t_ in weak]},
                    "unexplained": [t_ for t_ in toks if t_ not in strong and t_ not in weak],
                    "unsupported_pieces": unsupported, "words_not_yours": foreign, "pieces": list(rd.used), "key": reading_key(rd),
                    "operations": [[o["id"] for o in c["ops"]] for c in rd.info["clauses"]],
                    "echo": [list(e) for e in rd.echo], "lean": rd.lean_def(),
                    "compiles_as_written": domain is None or not isinstance(compile_sentence(comp, s.text, None), Problem)})
    res = {"schema": SCHEMA, "rough": rough, "system_asked": domain, "tokens": toks,
           "operations_tried": [[o["id"] for o in seq] for seq in subject_ops(voc, ops, R)], "anchored": anchored,
           "generated": len(ranked), "compiled": tried, "refused": refused, "candidates": out,
           "chosen": 0 if out else None, "chosen_by": "rank (no human choice)" if out else None,
           "language_model": "none (the hook `compose.model_hook` is not implemented)",
           "limits": {"candidates": CANDIDATE_LIMIT, "depth": DEPTH, "beam": BEAM, "pair_claims": PAIR_CLAIMS,
                      "compile": COMPILE_LIMIT, "weights": {"strong": W_STRONG, "weak": W_WEAK, "unsupported": UNSUPPORTED, "foreign": FOREIGN, "piece": PIECE}}}
    return checked(res, comp)


def checked(res: dict, comp=None) -> dict:
    """THE GUARANTEE: every candidate about to be printed compiles, as written, to the term shown. Raises otherwise."""
    comp = comp or load()[1]
    for c in res["candidates"]:
        rd = compile_sentence(comp, c["sentence"], res["system_asked"])
        assert not isinstance(rd, Problem), f"compose would print a sentence that does not compile: {c['sentence']!r}: {getattr(rd, 'message', '')}"
        assert rd.lean_def() == c["lean"], f"compose would print a sentence whose reading changed on recompiling: {c['sentence']!r}"
    return res


# --------------------------------------------------------------------------------------------- the questions (L3)

def questions(res: dict, k: int) -> list:
    """For each pair among the top k candidates: the verdict of `clausal separate` and the question it leaves the author."""
    from . import separate
    out = []
    cands = res["candidates"][:k]
    for a, b in itertools.combinations(cands, 2):
        try:
            r = separate.separate([a["sentence"], b["sentence"]])
        except Exception as e:                       # the Lean libraries not built, cargo missing, ...
            out.append({"a": a["rank"], "b": b["rank"], "verdict": "NOT-SEARCHED", "question": None, "detail": [f"clausal separate failed: {e}"],
                        "asks": True})
            continue
        la, lb = f"A/{a['system']}", f"B/{b['system']}"
        cmp_ = next((c for c in r["comparisons"] if c["a"] == la and c["b"] == lb), None)
        q = {"a": a["rank"], "b": b["rank"], "verdict": cmp_["verdict"] if cmp_ else "NOT-SEARCHED", "question": None, "detail": [],
             "asks": True, "lean": (r.get("lean") or {}).get("command"), "rust": (r.get("rust") or {}).get("command")}
        name = {la: f"candidate {a['rank']}", lb: f"candidate {b['rank']}"}
        if cmp_ is None:
            q["detail"].append("clausal separate returned no comparison for this pair")
        elif cmp_["verdict"] == "SEPARATED":
            # One question PER separating input, each naming its input by number and values: two inputs can point opposite
            # ways (holds and fails swapped), so a single question about "the input above" would be wrong for one of them.
            sep = cmp_["separating"]
            q["inputs"], asks = [], []
            for n, p in enumerate(sep, 1):
                values = separate.say_values(p["a"]["values"])
                tag = f"input {n}" if len(sep) > 1 else "input"
                q["detail"].append(f"{tag}: {values}")
                rv = (p["a"].get("rust") or {})
                q["detail"] += separate.say_calls(rv, "  ") if rv else []
                q["detail"].append(f"  {name[p['holds']]} HOLDS here; {name[p['fails']]} FAILS here")
                q["inputs"].append({"n": n, "values": values, "holds": {la: a["rank"], lb: b["rank"]}[p["holds"]],
                                    "fails": {la: a["rank"], lb: b["rank"]}[p["fails"]]})
                asks.append((f"On {tag} ({values}): should" if len(sep) > 1 else "Should")
                            + f" your rule hold there (then you do not mean {name[p['fails']]}) "
                            f"or fail there (then you do not mean {name[p['holds']]})?")
            q["question"] = (f"Candidates {a['rank']} and {b['rank']} differ on "
                             + (f"the input above ({q['inputs'][0]['values']}). " if len(sep) == 1
                                else f"each of the {len(sep)} inputs above"
                                + (", and not the same way on each" if len({(i["holds"], i["fails"]) for i in q["inputs"]}) > 1 else "")
                                + "; answer for each. ")
                             + " ".join(asks))
            if cmp_.get("operations_differ"):
                q["detail"].append("NOTE: " + cmp_["operations_differ"])
        elif cmp_["verdict"] == "DIFFERENT-OPERATIONS":
            q["detail"].append(cmp_["why"])
            q["question"] = (f"Candidates {a['rank']} and {b['rank']} are about different operations ({' then '.join(a['operations'][0])} "
                             f"and {' then '.join(b['operations'][0])}). Which operation is your rule about?")
        elif cmp_["verdict"] in ("SAME-TERM", "PROVED-EQUAL"):
            q["asks"] = False
            q["detail"].append(cmp_["why"])
        else:                                        # NONE-FOUND, NOT-SEARCHED
            q["detail"].append(cmp_["why"] or "")
            q["question"] = (f"No input was found that separates candidates {a['rank']} and {b['rank']}, and they are not shown equal. "
                             "Read both echoes: which do you mean?")
        out.append(q)
    return out


# --------------------------------------------------------------------------------------------- output

def not_offered(res: dict) -> list:
    """The sentences refused only because they read in more than one system, and the question that leaves the author.
    Printed whether or not there are candidates: such a sentence can be closer to the rough one than every candidate
    shown, and dropping it without a word would be choosing a system (none) for the author."""
    amb = res["refused"].get("ambiguous_as_written") or []
    if not amb:
        return []
    n = len(res["candidates"])
    o = ["", "NOT OFFERED: these read in more than one system, so each is AMBIGUOUS as written (a Rule line alone names no system)."
             + (" Each was ranked ahead of a candidate above." if n else "")]
    for x in amb:
        where = (f"ranked ahead of [{x['ahead_of_rank']}]" if x["ahead_of_rank"] <= n else "ranked after the candidates above") if n else ""
        o.append(f"  - {x['sentence']}   (reads in: {', '.join(x['systems'])}" + (f"; {where}" if where else "") + ")")
    systems = sorted({s for x in amb for s in x["systems"]})
    o.append(f"  QUESTION: which system is your rule about ({' or '.join(systems)})? If you mean one of these sentences, run again "
             f"with --domain {'|'.join(systems)}; it is then offered, marked as needing scenarios of that system beneath it.")
    return o


def render(res: dict, qs: list | None) -> str:
    o = [f"Rough sentence: {res['rough']}", f"tokens: {' '.join(res['tokens'])}"]
    if not res["anchored"]:
        o.append("no operation of the Clausebook is named or hinted at in the sentence: every operation was tried")
    if not res["candidates"]:
        o.append(f"NO CANDIDATE: none of the {res['compiled']} best of {res['generated']} generated sentences compiles as written.")
        return "\n".join(o + not_offered(res))
    o.append(f"{len(res['candidates'])} candidate(s), best first. Each compiles as written; the reading under it is the compiler's echo.")
    ahead = [x for x in res["refused"].get("ambiguous_as_written") or [] if x["ahead_of_rank"] <= len(res["candidates"])]
    if ahead:
        o.append(f"{len(ahead)} sentence(s) ranked ahead of a candidate below are NOT OFFERED because they read in more than one system: "
                 "see NOT OFFERED after the candidates.")
    for c in res["candidates"]:
        o.append("")
        o.append(f"[{c['rank']}] {c['sentence']}")
        o.append(f"     system {c['system']}; score {c['score']}; your words it accounts for: "
                 + (", ".join(c['explained']['by_form_or_cue'] + c['explained']['by_echo_only']) or "none")
                 + ("; not accounted for: " + ", ".join(c["unexplained"]) if c["unexplained"] else "")
                 + ("; pieces none of your words ask for: " + ", ".join(c["unsupported_pieces"]) if c["unsupported_pieces"] else "")
                 + ("; words that are not yours: " + ", ".join(c["words_not_yours"]) if c["words_not_yours"] else ""))
        if not c["compiles_as_written"]:
            o.append(f"     NOTE: compiles in system {c['system']} only when the system is given (as under a Rule whose scenarios are in "
                     "it). Written alone it is AMBIGUOUS: it also reads in another system.")
        for a, b in c["echo"]:
            o.append(f"       {a:<12}{b}")
    o += not_offered(res)
    if qs is not None:
        o.append("")
        o.append("Do the top candidates say the same? (clausal separate)")
        for q in qs:
            o.append(f"  candidates {q['a']} and {q['b']}: {q['verdict']}")
            o += ["    " + l for l in q["detail"] if l]
            if q["question"]:
                o.append(f"    QUESTION: {q['question']}")
    o.append("")
    o.append("No candidate has been chosen. Choose with --choose K (add --write FILE.feature to put it in a feature file).")
    return "\n".join(o)


def write_feature(path: Path, sentence: str, system: str | None) -> None:
    """Append `Rule: <sentence>` to a feature file (made if missing), then compile the file's new rule; undo on failure."""
    before = path.read_text() if path.exists() else None
    text = before if before is not None else f"Feature: {path.stem}\n"
    text = text.rstrip("\n") + f"\n\n  Rule: {sentence}\n"
    path.write_text(text)
    try:
        f = parse_feature(path, str(path))
        r = next(x for x in f.rules if x.name.strip() == sentence)
        rd = vocab.Compiler(load()[0]).rule(r, system)
        if isinstance(rd, Problem):
            raise FeatureError(f"{path}: the sentence does not compile in the file: {rd.message}")
    except Exception:
        if before is None:
            path.unlink()
        else:
            path.write_text(before)
        raise


def main(argv) -> int:
    def opt(name):
        if name in argv:
            i = argv.index(name)
            v = argv[i + 1] if i + 1 < len(argv) else None
            del argv[i:i + 2]
            return v
        return None

    argv = list(argv)
    domain, top, ask, choose, write = opt("--domain"), opt("--top"), opt("--ask"), opt("--choose"), opt("--write")
    as_json, no_ask = "--json" in argv, "--no-ask" in argv
    rest = [a for a in argv if not a.startswith("--")]
    if len(rest) != 1:
        print(__doc__)
        return 2
    try:
        res = compose(rest[0], domain, int(top) if top else DEFAULT_TOP)
    except FeatureError as e:
        print(f"clausal compose: {e}", file=sys.stderr)
        return 1
    cands = res["candidates"]
    k = int(ask) if ask else (0 if as_json or no_ask else ASK_DEFAULT)
    qs = questions(res, k) if k >= 2 and len(cands) >= 2 else None
    chosen = None
    if as_json:
        chosen = 0 if cands else None                        # the non-interactive mode takes the top candidate
        if choose:
            chosen = int(choose) - 1
        res["questions"] = qs
        res["chosen"], res["chosen_by"] = chosen, (None if chosen is None else "--choose" if choose else "rank (no human choice)")
    else:
        res["chosen"], res["chosen_by"] = None, None
        print(render(res, qs))
        if choose:
            chosen = int(choose) - 1
        elif cands and sys.stdin.isatty():
            got = input(f"Which candidate do you mean? [1-{len(cands)}, or Enter for none] ").strip()
            chosen = int(got) - 1 if got.isdigit() else None
        if chosen is not None and not 0 <= chosen < len(cands):
            print(f"clausal compose: there is no candidate {chosen + 1}", file=sys.stderr)
            return 2
        if chosen is not None:
            res["chosen"], res["chosen_by"] = chosen, "--choose" if choose else "the author, at the prompt"
            print(f"chosen: [{chosen + 1}] {cands[chosen]['sentence']}")
    if chosen is not None and not 0 <= chosen < len(cands):
        print(f"clausal compose: there is no candidate {chosen + 1}", file=sys.stderr)
        return 2
    if write:
        if chosen is None:
            print("clausal compose: --write needs a chosen candidate (--choose K, the prompt, or --json for the top one)", file=sys.stderr)
            return 2
        c = cands[chosen]
        if not c["compiles_as_written"]:
            print("clausal compose: not written: the sentence is AMBIGUOUS without a system, and a Rule line alone gives none", file=sys.stderr)
            return 2
        try:
            write_feature(Path(write), c["sentence"], None)
        except FeatureError as e:
            print(f"clausal compose: {e}", file=sys.stderr)
            return 1
        res["written"] = str(write)
        if not as_json:
            print(f"written: Rule: {c['sentence']}  ->  {write}")
    if as_json:
        print(json.dumps(res, indent=1, ensure_ascii=False))
    return 0 if cands else 3
