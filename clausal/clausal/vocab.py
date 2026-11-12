"""clausal vocab: the COMPOSABLE Clausebook (plan nodes V2 and V3).

A sentence is not bound as a whole. It is assembled from typed pieces of three kinds (the books of clausebook/, listed in
clausebook/project.yaml: core, word packs, local books):
domain words, modifiers, frames. This module

  * loads the Clausebook and turns every surface form into a small pattern with typed holes;
  * finds every way a step (or a `Rule:` line) can be built from those forms. Exactly one way: a reading.
    None: UNBOUND. None unless types are ignored: ILL-TYPED. Several: AMBIGUOUS. Always with file:line;
  * renders the one composition as (a) a Lean statement over the frame library (lean/Frames), (b) the
    pointwise form and the executable checker of each frame (the two readings that are compared), and
    (c) the slot-structured English echo, with every default that was applied.

Like the rest of clausal it is UNTRUSTED: Lean type-checks what it writes, a generated kernel-checked
equivalence ties each reading to the flat statement the proofs are about (clausal/links.py), and the echo
is printed for a person to compare with the sentence.

QUANTIFIER SCOPE, the one rule: every outline <parameter>, then the state, then the input are universally
quantified at the front of the statement, in that order, and Givens (scope conditions) restrict them.
Collection words ("every", "the first", "no") bind inside the one clause they occur in. Negation applies
to the one atomic condition it is written on. Nothing is ever existentially quantified over inputs.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from . import narrowing
from .core import FeatureError, Problem, literal_problem, literal_regex

HOLE = re.compile(r"\{(\w+)(?::([^}]+))?\}")
LAMBDA = {"measure": "fun st inp", "term": "fun st inp", "cond": "fun st inp", "class": "fun ans", "ameasure": "fun ans",
          "acoll": "fun st inp ans", "itempred": "fun st inp x", "coll": "fun st inp"}
CONSTANT_CATS = ("variation", "reference")     # domain words that are one Lean constant: no lambda is put around them


def base_cat(cat: str) -> str:
    return cat.split("<", 1)[0]


def hole_voice(cat):
    """`class@first` -> ("class", "first"): a hole filled by the form its category has in ANOTHER POSITION (the
    `first_call_forms` of a class: what is said of the first of two compared calls). Any other hole: (cat, "")."""
    if cat and "@" in cat:
        c, v = cat.split("@", 1)
        return c, v
    return cat, ""


RETIRED = "RETIRED-FORM"       # Problem.code of a sentence written with a form, or in a shape, the book no longer accepts
RETIRABLE = ("forms", "not_forms", "then_forms", "vp_forms", "subject_forms", "claim_forms", "first_call_forms", "first_call_not_forms")


# --------------------------------------------------------------------------- the parse tree

@dataclass
class Leaf:
    kind: str            # actor | value
    type: str            # wallet / ledger / amount / index / ...
    text: str            # as written: "Alice", "ledger Main", "<amount>", "30", "the sender", "the amount"
    how: str             # name | param | lit | enum | role

    @property
    def param(self):
        return self.text[1:-1] if self.how == "param" else None


@dataclass
class Node:
    piece: dict
    args: dict           # hole name -> Node | Leaf | [Node]
    cat: str
    form: str = ""
    neg: bool = False    # reached through a `not_forms` surface: the piece under "not"
    idiom: str | None = None
    variant: str = ""    # "per_actor": the plural of a per-actor measure
    notes: list = field(default_factory=list)     # type mismatches, in a relaxed parse
    now: str = ""        # the form that REPLACED the one this was read through (set only when the book is loaded with its retired forms)
    said: dict | None = None    # an idiom: what filled the holes of its form

    @property
    def id(self):
        return self.piece["id"]


def walk(x):
    """Every Node and Leaf of a tree (or list of trees)."""
    if isinstance(x, list):
        for y in x:
            yield from walk(y)
    elif isinstance(x, Node):
        yield x
        for v in x.args.values():
            yield from walk(v)
    elif isinstance(x, Leaf):
        yield x


# --------------------------------------------------------------------------- the Clausebook

@dataclass
class Form:
    owner: dict          # piece, idiom or operation
    text: str
    cat: str             # result category (T already replaced)
    segs: list           # [("lit", text) | ("hole", name, category)]
    neg: bool = False
    idiom: bool = False
    variant: str = ""
    voice: str = ""      # then | vp | first | "" (other categories)
    now: str = ""        # a RETIRED form (read only by the second pass that explains a refusal): the form that replaced it


def segments(text: str) -> list:
    out, pos = [], 0
    for m in HOLE.finditer(text):
        if m.start() > pos:
            out.append(("lit", text[pos:m.start()]))
        out.append(("hole", m.group(1), m.group(2)))
        pos = m.end()
    if pos < len(text):
        out.append(("lit", text[pos:]))
    return out


BOOK_DIR = "clausebook"
PROJECT_FILE = "project.yaml"


@dataclass
class Book:
    """One file of the Clausebook: core, a word pack, or a project's local book."""
    name: str            # `book:` of the file
    rel: str             # path as printed in messages (relative to the project root)
    path: Path
    text: str
    raw: dict
    lines: list = field(default_factory=list)

    @property
    def signoff_path(self) -> Path:
        """Sign-offs are stored per book, beside it: clausebook/core.yaml -> clausebook/core.signoff.json."""
        return self.path.with_suffix(".signoff.json")


def project_books(root: Path) -> list:
    """[(path, rel)] of the books a project loads, in order: `books:` of <root>/clausebook/project.yaml."""
    d = root / BOOK_DIR
    raw = yaml.safe_load((d / PROJECT_FILE).read_text())
    return [(d / b, f"{BOOK_DIR}/{b}") for b in raw["books"]]


def load_project(root: Path, gloss, overrides=None) -> "Vocabulary":
    """The Clausebook of the project at `root`: every book its project file lists."""
    return Vocabulary(project_books(root), gloss, overrides=overrides)


class NoGlossary:
    """A project with no literal and no actor types: what core is loaded with when it is loaded alone."""
    param_types: dict = {}
    actors: dict = {}


MERGED_MAPS = ("lean_files", "literal_lean", "type_echo", "defaults", "categories")
MERGED_LISTS = ("sorts", "introduced_by_kind", "frames_without_surface")
ENTRY_LISTS = ("operations", "pieces", "idioms", "coverage", "grammar", "separations")


class Vocabulary:
    """The Clausebook a project compiles against: a LIST OF BOOKS, in order (core first, then word packs, then the
    project's local books). An id may be defined once; a later book may use the pieces of an earlier one.

    `books`: [(path, rel)], or [Book]. `gloss`: the project's literal and actor types (None: none at all).
    `overrides`: {rel: text} read in place of the file of that name (for checks that edit a book in memory)."""

    def __init__(self, books, gloss=None, rel_or_gloss=None, overrides=None, legacy=False):
        if isinstance(books, Path):                      # the old signature (one flat file): Vocabulary(path, rel, gloss)
            books, gloss = [(books, gloss)], rel_or_gloss
        gloss = gloss if gloss is not None else NoGlossary()
        # `legacy`: the book WITH its retired forms put back, each marked with the form that replaced it. No sentence is
        # ever compiled against it: it is loaded only after a sentence was refused, to say which retired form it was
        # written with (Compiler.rule, Compiler.scenario). The book a project compiles against never holds them.
        self.legacy, self._legacy_voc = legacy, None
        self.books = []
        for b in books:
            if not isinstance(b, Book):
                path, rel = b
                text = (overrides or {}).get(rel)
                text = path.read_text() if text is None else text
                raw = yaml.safe_load(text) or {}
                b = Book(str(raw.get("book") or Path(rel).stem), rel, path, text, raw, text.splitlines())
            self.books.append(b)
        self.rel = ", ".join(b.rel for b in self.books)
        names = [b.name for b in self.books]
        for k, b in enumerate(self.books):
            if b.name in names[:k]:
                raise FeatureError(f"{b.rel}: a book named `{b.name}` is already loaded")
            for need in b.raw.get("needs", []):
                if need not in names[:k]:
                    raise FeatureError(f"{b.rel}: this book needs the book `{need}`, which is not loaded before it")
        # ---- the merged view: what the rest of the compiler reads
        self.raw = {k: {} for k in MERGED_MAPS} | {k: [] for k in MERGED_LISTS + ENTRY_LISTS}
        self.home = {}                                   # entry id -> the Book that defines it
        for b in self.books:
            for k in MERGED_MAPS:
                for key, val in (b.raw.get(k) or {}).items():
                    if k == "lean_files":                # a namespace may be served by several files, and named by several books
                        have = self.raw[k].setdefault(key, [])
                        have += [f for f in ([val] if isinstance(val, str) else val) if f not in have]
                    elif key in self.raw[k] and self.raw[k][key] != val:
                        raise FeatureError(f"{b.rel}: `{k}: {key}` is already given, differently, by an earlier book")
                    else:
                        self.raw[k][key] = val
            for k in MERGED_LISTS:
                self.raw[k] += [x for x in (b.raw.get(k) or []) if x not in self.raw[k]]
            for d in (b.raw.get("defaults") or {}):          # a default is an entry of the book: signed by id, under the digest
                if not isinstance(d, str) or d in self.home:
                    raise FeatureError(f"{b.rel}: `{d}` cannot be the id of a default here (already an entry, or not a word)")
                self.home[d] = b
            for k in ENTRY_LISTS:
                for e in b.raw.get(k) or []:
                    if not isinstance(e, dict) or "id" not in e:
                        raise FeatureError(f"{b.rel}: an entry of `{k}:` has no `id` (every entry is signed by its id)")
                    if e["id"] in self.home:
                        raise FeatureError(f"{b.rel}: `{e['id']}` is already an entry of {self.home[e['id']].rel}; "
                                           "a book may not redefine an entry of another")
                    self.home[e["id"]] = b
                    self.raw[k].append(e)
        # Lean imports of generated files: the most local book first (the last book's, then the one before, ...)
        self.raw["lean_imports"] = list(dict.fromkeys(i for b in reversed(self.books) for i in b.raw.get("lean_imports", [])))
        self.sorts = list(self.raw["sorts"])             # what `<T>` ranges over: every loaded book's `sorts:`, in order
        self.gloss = gloss                               # literal syntax and actor names only
        self.pts = {k: dict(v) for k, v in gloss.param_types.items()}
        for k, tmpl in self.raw["literal_lean"].items():
            self.pts[k]["lean_literal"] = tmpl
        self.actors = gloss.actors
        self.ops = {o["id"]: o for o in self.raw["operations"]}
        self.pieces = {p["id"]: p for p in self.raw["pieces"]}
        self.idioms = {i["id"]: i for i in self.raw["idioms"]}
        # COVERAGE (plan node Q2): what is printed about which calls a claim is about, one entry per constructor of
        # `Frames.Calls`. Entries of the book like any other: under the sign-off digest, used by the readings that print them.
        self.coverage = {c["id"]: c for c in self.raw["coverage"]}
        self.covers = {c["calls"]: c for c in self.coverage.values()}
        for c in self.coverage.values():
            c.setdefault("kind", "coverage")
        if set(self.covers) != {"every", "accepted", "rejected"} or len(self.covers) != len(self.coverage):
            raise FeatureError(f"{self.rel}: `coverage:` must have exactly one entry for each of the calls every, accepted, rejected "
                               "(the constructors of Frames.Calls)")
        # GRAMMAR (plan node Q3): the words that put a Rule line together and belong to no one piece.
        self.grammar = {g["id"]: g for g in self.raw["grammar"]}
        for g in self.grammar.values():
            g.setdefault("kind", "grammar")
        # SEPARATIONS (lint check 4 of `clausal book check`): two pieces whose forms share a literal skeleton, with one
        # sentence for each that the compiler reads as that piece and not the other. An entry of the book like any other:
        # signed by id (`clausal review <id>`), and in force only while that sign-off is valid (book.separation_state).
        self.separations = {s["id"]: s for s in self.raw["separations"]}
        for s in self.separations.values():
            s.setdefault("kind", "separation")
            named = set(self.ops) | set(self.pieces) | set(self.idioms)
            btw, inp = s.get("between"), s.get("inputs")
            if not (isinstance(btw, list) and len(btw) == 2 and btw[0] != btw[1] and all(x in named for x in btw)):
                raise FeatureError(f"{self.home[s['id']].rel}: separation `{s['id']}`: `between` must name two different entries "
                                   "(operations, pieces or idioms) of the Clausebook")
            if not (isinstance(inp, dict) and set(inp) == set(btw) and all(isinstance(x, str) and x.strip() for x in inp.values())):
                raise FeatureError(f"{self.home[s['id']].rel}: separation `{s['id']}`: `inputs` must give one Rule line for each of "
                                   f"`{btw[0]}` and `{btw[1]}` (a sentence the compiler reads as that entry and not the other)")
        for o in self.ops.values():
            o.setdefault("kind", "domain")
            o["cat"] = "op"
        # RETIRED FORMS (plan node Q4): `retired: [{in, was, now}]` of an entry. Not accepted; recorded so that the refusal of a
        # sentence written with one can name the form that replaced it.
        self.retired = {}                        # (entry id, field, old form) -> the form that replaced it
        for e in list(self.pieces.values()) + list(self.grammar.values()):
            for r in e.get("retired") or []:
                ok = isinstance(r, dict) and set(r) == {"in", "was", "now"} and all(isinstance(x, str) and x for x in r.values())
                if not ok or r["in"] not in RETIRABLE or r["was"] in (e.get(r["in"]) or []):
                    raise FeatureError(f"{self.at(e['id'])}: `{e['id']}`: an entry of `retired:` is {{in: <field>, was: <old form>, now: <new form>}}, "
                                       f"with <field> one of {', '.join(RETIRABLE)} and the old form no longer among the forms of that field")
                self.retired[(e["id"], r["in"], r["was"])] = r["now"]
                if legacy:
                    e[r["in"]] = list(e.get(r["in"]) or []) + [r["was"]]
        for i in list(self.ops) + list(self.pieces) + list(self.idioms) + list(self.coverage) + list(self.grammar) + list(self.separations):
            if not isinstance(i, str) or i == "all":       # YAML reads `no`, `yes`, `on` as booleans; `all` is a keyword of `review`
                raise FeatureError(f"{self.home[i].rel}: `{i}` cannot be the id of a Clausebook entry (write another word, or quote it)")
        self.forms: dict = {}                    # (category, voice) -> [Form]
        for p in self.pieces.values():
            p.setdefault("domain", "shared")
            for key, voice, neg in (("forms", "", False), ("not_forms", "", True), ("then_forms", "then", False),
                                    ("vp_forms", "vp", False), ("first_call_forms", "first", False), ("first_call_not_forms", "first", True)):
                for f in p.get(key, []):
                    self._add(p, f, p["cat"], neg=neg, voice=voice, now=self.retired.get((p["id"], key, f), ""))
            pa = p.get("per_actor")
            if pa:
                for f in pa["forms"]:
                    self._add(p, f, "per_actor", variant="per_actor")
            p["_args_declared"] = "args" in p        # for `clausal book check`: were the piece's holes written down, or read off a form?
            if "args" not in p:
                p["args"] = self._holes(p)
        for i in self.idioms.values():
            i.setdefault("kind", "idiom")
            self._add(i, i["form"], i["cat"], idiom=True, voice="then" if i["cat"] == "claim" else "")
        self._check()
        self._surface()
        narrowing.check_book(self)

    def _surface(self):
        """The words of a Rule line that are not the form of a piece's own category, READ FROM THE BOOK (plan node Q3):
        nothing below is a constant of the compiler. An entry or a form that is taken out of the book takes its
        sentences with it.
          subject_words   [(written before the operation noun, modifier id)]     `subject_forms: ["rejected {op}"]`
          relatives       [separator]  "<subject><separator><condition>"          `given`:    "{op} for which {c:cond}"
          sequences       [separator]  "<operation><separator><operation>"        `and_then`: "{op} followed by {op2}"
          claim_prefixes  [(written before a claim, modifier id)]                 `claim_forms: ["if it is rejected, {claim}"]`
          articles, role_prefixes, vp_seps, for_shapes, claim_seps, clause_seps   the `grammar:` entries of core"""
        def shape(owner, text):
            return [("hole", x[1]) if x[0] == "hole" else ("lit", x[1]) for x in segments(text)]
        def bad(owner, field, text):
            return FeatureError(f"{self.at(owner)}: `{owner}`: `{field}` form \"{text}\" has a shape the compiler cannot read")
        self.subject_words, self.relatives, self.sequences, self.claim_prefixes = [], [], [], []
        self.retired_words, self.live_word = {}, {}       # (legacy) a retired subject word -> the word that replaced it; modifier -> its live word
        for p in self.pieces.values():
            for f in p.get("subject_forms") or []:
                sh = shape(p["id"], f)
                kinds = [k for k, _ in sh]
                if kinds == ["lit", "hole"] and sh[1][1] == "op":
                    self.subject_words.append((sh[0][1], p["id"]))
                    now = self.retired.get((p["id"], "subject_forms", f))
                    if now is None:
                        self.live_word[p["id"]] = sh[0][1].strip()
                    else:
                        self.retired_words[sh[0][1]] = shape(p["id"], now)[0][1].strip()
                elif kinds == ["hole", "lit", "hole"] and sh[0][1] == "op" and sh[2][1] == "op2" and p["id"] == "and_then":
                    self.sequences.append(sh[1][1])
                elif kinds == ["hole", "lit", "hole"] and sh[0][1] == "op" and p["id"] == "given":
                    self.relatives.append(sh[1][1])
                else:
                    raise bad(p["id"], "subject_forms", f)
            for f in p.get("claim_forms") or []:
                sh = shape(p["id"], f)
                if [k for k, _ in sh] != ["lit", "hole"] or sh[1][1] != "claim":
                    raise bad(p["id"], "claim_forms", f)
                self.claim_prefixes.append((sh[0][1], p["id"]))
        def g(id_, want):
            out = []
            for f in (self.grammar.get(id_) or {}).get("forms") or []:
                sh = shape(id_, f)
                if [x if k == "hole" else k for k, x in sh] != want:
                    raise bad(id_, "forms", f)
                out.append(tuple(x for k, x in sh if k == "lit"))
            return out
        self.articles = [x[0] for x in g("g.subject", ["lit", "op"])]
        gone = {shape("g.subject", was)[0][1] for (i, _f, was) in self.retired if i == "g.subject"}
        self.live_articles = [a for a in self.articles if a not in gone]
        self.retired_articles = [a for a in self.articles if a in gone]
        # how "for <subject>, <claim>" is read (`g.rule_for`): which Then forms, and whether a narrowing may stand before the claim
        rf = self.grammar.get("g.rule_for") or {}
        self.for_reads, self.rule_prefixes = rf.get("reads"), rf.get("narrowing") != "on_subject"
        if rf.get("reads") not in (None, "no_verb_phrase") or rf.get("narrowing") not in (None, "on_subject"):
            raise FeatureError(f"{self.at('g.rule_for')}: `g.rule_for`: `reads` may only be `no_verb_phrase`, and `narrowing` only `on_subject`")
        self.role_prefixes = [x[0] for x in g("g.role", ["lit", "role"])]
        self.vp_seps = [x[0] for x in g("g.rule_vp", ["subject", "lit", "vp"])]
        self.for_shapes = g("g.rule_for", ["lit", "subject", "lit", "claim"])           # [(prefix, separator)]
        self.claim_seps = [x[0] for x in g("g.claims", ["claim", "lit", "claim"])]
        self.clause_seps = [x[0] for x in g("g.clauses", ["clause", "lit", "clause"])]
        line = self.grammar.get("g.line") or {}
        self.line_any_case = bool(line.get("first_letter_either_case"))
        self.line_stop_optional = bool(line.get("final_full_stop_optional"))
        # how each narrowing or scoping word is WRITTEN, for the refusal that quotes two of them
        self.word_of = {m: w.strip() for w, m in self.subject_words}
        self.prefix_of = {m: w.strip().rstrip(",") for w, m in self.claim_prefixes}
        for p in self.pieces.values():
            for hole, pid in (p.get("implied") or {}).items():
                if pid not in self.pieces:
                    raise FeatureError(f"{self.at(p['id'])}: `{p['id']}`: `implied: {hole} = {pid}` names no piece of the Clausebook")
            for hole, pid in (p.get("negated") or {}).items():
                if pid not in self.pieces or not (self.pieces[pid].get("then_forms") or self.pieces[pid].get("forms")):
                    raise FeatureError(f"{self.at(p['id'])}: `{p['id']}`: `negated: {hole} = {pid}` names no piece with a form to write instead")
            # `same_as: accepted`: the class IS the acceptance of every operation it can be said of. Not taken on trust: it must be
            # among what narrowing settles for each such operation (`narrowing:`), and those lines are kernel-checked on every run.
            if p.get("same_as"):
                for o in self.ops.values():
                    if o["domain"] == p.get("domain") and o["answer"] == p.get("answer"):
                        f = o.get("narrowing") or {}
                        if p["id"] not in ((f.get("accepted") or {}).get("holds") or []) or p["id"] not in ((f.get("rejected") or {}).get("fails") or []):
                            raise FeatureError(f"{self.at(p['id'])}: `{p['id']}` says `same_as: {p['same_as']}`, but the `narrowing:` of `{o['id']}` does not "
                                               f"list it under both `accepted: holds` and `rejected: fails`")

    def legacy_voc(self) -> "Vocabulary":
        """This book with its retired forms put back (see `legacy`). Built once, from the same texts."""
        if self._legacy_voc is None:
            self._legacy_voc = Vocabulary([(b.path, b.rel) for b in self.books], self.gloss,
                                          overrides={b.rel: b.text for b in self.books}, legacy=True)
        return self._legacy_voc

    def role_phrases(self, role: str) -> list:
        """How a role of an operation is written in a Rule line ("the sender"): every `g.role` form, the first one first."""
        return [pre + role for pre in self.role_prefixes]

    def default(self, d: str) -> str:
        """The text of a default the compiler applied. It is in the book or the sentence does not compile."""
        if d not in self.raw["defaults"]:
            raise FeatureError(f"{self.rel}: the reading rule `{d}` was applied to a sentence and is not among the `defaults:` of the Clausebook")
        return self.raw["defaults"][d]

    def book_of(self, id_: str) -> Book:
        return self.home[id_]

    def line_of(self, id_: str) -> int:
        """The line of an entry in ITS book."""
        b = self.home.get(id_)
        pat = rf"\s+{re.escape(id_)}:\s" if id_ in self.raw["defaults"] else rf"\s*-\s*\{{?\s*id:\s*{re.escape(id_)}\b"
        for n, l in enumerate(b.lines if b else [], 1):
            if re.match(pat, l):
                return n
        return 0

    def at(self, id_: str) -> str:
        """book file:line of an entry, for messages."""
        b = self.home.get(id_)
        return f"{b.rel}:{self.line_of(id_)}" if b else self.rel

    def _holes(self, p) -> dict:
        for key in ("forms", "then_forms", "vp_forms", "not_forms"):
            for f in p.get(key, []):
                return {s[1]: hole_voice(s[2])[0] for s in segments(f) if s[0] == "hole"}
        return {}

    def _add(self, owner, text, cat, neg=False, idiom=False, variant="", voice="", now=""):
        variants = self.sorts if re.search(r"<T>", text + cat) else [None]
        for t in variants:
            tx = text if t is None else text.replace("<T>", f"<{t}>")
            ct = cat if t is None else cat.replace("<T>", f"<{t}>")
            self.forms.setdefault((ct, voice), []).append(
                Form(owner, tx, ct, segments(tx), neg=neg, idiom=idiom, variant=variant, voice=voice, now=now))

    def _check(self):
        """Every hole names a known category; a book names only the literal and actor types it says it uses
        (`uses_types:`), and the project defines them; every idiom's meaning uses known pieces."""
        lexical = set(self.pts) | set(self.actors)
        known = lexical | {"per_actor"}
        cats = {base_cat(c) for (c, _v) in self.forms} | {"claim", "cond"} | set(self.raw["categories"])
        for b in self.books:
            for t in b.raw.get("uses_types") or []:
                if t not in lexical:
                    raise FeatureError(f"{b.rel}: `uses_types` names `{t}`, which is no literal type and no actor type of the project")
        def hole(owner, name, cat):
            b = self.home[owner["id"]]
            cat, v = hole_voice(cat)
            if v and v != "first":
                raise FeatureError(f"{self.at(owner['id'])}: `{owner['id']}`: hole `{{{name}:{cat}@{v}}}` names a position no piece has a form in")
            if cat and cat not in known and base_cat(cat) not in cats:
                raise FeatureError(f"{self.at(owner['id'])}: `{owner['id']}`: hole `{{{name}:{cat}}}` names no category of the Clausebook")
            if cat in lexical and "uses_types" in b.raw and cat not in b.raw["uses_types"]:
                raise FeatureError(f"{self.at(owner['id'])}: `{owner['id']}`: hole `{{{name}:{cat}}}` is of a type of the project "
                                   f"that the book does not list under `uses_types`")
        for (c, _v), fs in self.forms.items():
            for f in fs:
                for s in f.segs:
                    if s[0] == "hole":
                        hole(f.owner, s[1], s[2])
        for o in self.ops.values():
            for r, t in list(o["state"]) + list(o["input"]):
                hole(o, r, t)
        for p in self.pieces.values():
            for name, cat in (p.get("args") or {}).items():
                if isinstance(cat, str) and not cat.startswith("list<"):
                    hole(p, name, cat)
        for i in self.idioms.values():
            for name in re.findall(r"([A-Za-z_][\w.]*)\(", i["means"]):
                if name not in self.pieces:
                    raise FeatureError(f"{self.at(i['id'])}: idiom `{i['id']}` uses `{name}`, "
                                       "which is not a piece of the Clausebook")

    # ---- counts for the report
    def kinds(self) -> dict:
        out = {"domain": len(self.ops), "modifier": 0, "frame": 0}
        for p in self.pieces.values():
            out[p["kind"]] += 1
        return out

    def frames(self) -> list:
        return [p for p in self.pieces.values() if p["kind"] == "frame"]


# --------------------------------------------------------------------------- parsing

class Parser:
    """All the ways a text can be read as a piece of a given category.

    mode "scenario": actors are names, values are literals or <parameters>.
    mode "rule":     actors and values are the ROLES of the operation the rule is about ("the sender")."""

    def __init__(self, voc: Vocabulary, domain: str, mode: str, roles=None, ptypes=None, relaxed=False):
        self.voc, self.domain, self.mode, self.relaxed = voc, domain, mode, relaxed
        self.roles = roles or {}          # rule mode: role phrase -> (kind, type, role)
        self.ptypes = ptypes if ptypes is not None else {}
        self.memo = {}

    # ---- lexical categories
    def lexical(self, cat: str, text: str):
        v = self.voc
        if cat in v.actors:
            if self.mode == "rule":
                r = self.roles.get(text)
                if r and r[0] == "actor" and (r[1] == cat or self.relaxed):
                    return Leaf("actor", r[1], text, "role")
                return None
            if re.fullmatch(v.actors[cat].get("mention", v.actors[cat]["name_regex"]), text):
                return Leaf("actor", cat, text, "name")
            return None
        if cat in v.pts:
            pt = v.pts[cat]
            if self.mode == "rule":
                r = self.roles.get(text)
                if r and r[0] == "value" and (r[1] == cat or self.relaxed):
                    return Leaf("value", r[1], text, "role")
            m = re.fullmatch(r"<([A-Za-z_][A-Za-z0-9_]*)>", text)
            if m:
                have = self.ptypes.get(m.group(1))
                if have in (None, cat) or self.relaxed:
                    return Leaf("value", cat, text, "param")
                return None
            if "enum" in pt:
                return Leaf("value", cat, text, "enum") if text in pt["enum"] else None
            if re.fullmatch(literal_regex(v.pts, cat), text):
                return Leaf("value", cat, text, "lit")
        return None

    def is_lexical(self, cat: str) -> bool:
        return cat in self.voc.actors or cat in self.voc.pts

    # ---- forms
    def forms_for(self, cat: str, voice: str) -> list:
        out = []
        for (c, v), fs in self.voc.forms.items():
            if v != voice:
                continue
            if c == cat or (self.relaxed and base_cat(c) == base_cat(cat)):
                out += [f for f in fs if f.owner.get("domain", "shared") in ("shared", self.domain)]
        return out

    def parse(self, cat: str, text: str, voice: str = "") -> list:
        key = (cat, text, voice)
        if key in self.memo:
            return self.memo[key]
        self.memo[key] = []          # guards against a form whose first hole has its own category
        out = []
        for f in self.forms_for(cat, voice):
            for binding in self._match(f.segs, 0, text, 0, {}):
                out += self._build(f, binding, cat)
        self.memo[key] = out
        return out

    def _match(self, segs, i, text, pos, acc):
        """Every assignment of hole name -> parsed value under which `segs[i:]` spells `text[pos:]`."""
        if i == len(segs):
            if pos == len(text):
                yield dict(acc)
            return
        s = segs[i]
        if s[0] == "lit":
            if text.startswith(s[1], pos):
                yield from self._match(segs, i + 1, text, pos + len(s[1]), acc)
            return
        _, name, cat = s
        cat, hv = hole_voice(cat)
        nxt = segs[i + 1][1] if i + 1 < len(segs) and segs[i + 1][0] == "lit" else None
        ends = []
        if nxt is None:
            ends = [len(text)] if i + 1 == len(segs) else list(range(pos + 1, len(text)))
        else:
            j = text.find(nxt, pos + 1)
            while j != -1:
                ends.append(j)
                j = text.find(nxt, j + 1)
        for e in ends:
            chunk = text[pos:e]
            if not chunk or chunk != chunk.strip():
                continue
            if self.is_lexical(cat):
                leaf = self.lexical(cat, chunk)
                vals = [leaf] if leaf else []
            else:
                vals = self.parse(cat, chunk, hv)
            for v in vals:
                acc[name] = v
                yield from self._match(segs, i + 1, text, e, acc)
                del acc[name]

    def _build(self, f: Form, binding: dict, want: str) -> list:
        """The tree(s) a matched form stands for: the piece applied to its holes, or an idiom's meaning."""
        notes = []
        if f.cat != want:
            notes.append(f"`{f.owner['id']}` is a {f.cat}, where a {want} is needed")
        for s in f.segs:
            want_cat = hole_voice(s[2])[0] if s[0] == "hole" else None
            if s[0] == "hole" and isinstance(binding[s[1]], Node) and binding[s[1]].cat != want_cat and not self.is_lexical(want_cat):
                notes.append(f"`{binding[s[1]].id}` is a {binding[s[1]].cat}, where `{f.owner['id']}` takes a {want_cat}")
            if s[0] == "hole" and isinstance(binding[s[1]], Leaf) and binding[s[1]].type != want_cat:
                notes.append(f"\"{binding[s[1]].text}\" is a {binding[s[1]].type}, where `{f.owner['id']}` takes a {want_cat}")
        if f.idiom:
            trees = [self._expr(e.strip(), binding, f) for e in f.owner["means"].split(";")]
            said = dict(binding)
            for t in trees:
                t.idiom, t.form, t.now, t.said = f.owner["id"], f.text, f.now, said
                t.notes += notes
            return [trees] if len(trees) > 1 else trees
        p = f.owner
        args = dict(binding)
        if p["id"] == "changes_only":
            args = {"c": binding["c"], "xs": [binding["x"], binding["y"]]}
        node = Node(p, args, f.cat, form=f.text, variant=f.variant, notes=notes, now=f.now)
        if f.neg:
            node = Node(self.voc.pieces["not"], {"p": node}, f.cat, form=f.text, neg=True, notes=[], now=f.now)
        return [node]

    def _expr(self, e: str, binding: dict, f: Form):
        """An idiom's meaning: `piece(arg, arg)`, `[a, b]`, or the name of a hole of the idiom's form."""
        e = e.strip()
        if e.startswith("["):
            return [self._expr(x, binding, f) for x in split_args(e[1:-1])]
        m = re.fullmatch(r"([A-Za-z_][\w.]*)\((.*)\)", e, re.S)
        if not m:
            if e not in binding:
                raise FeatureError(f"{self.voc.at(f.owner['id'])}: idiom `{f.owner['id']}`: `{e}` is not a hole of its form")
            return binding[e]
        p = self.voc.pieces[m.group(1)]
        vals = [self._expr(x, binding, f) for x in split_args(m.group(2))]
        if len(vals) != len(p["args"]):
            raise FeatureError(f"{self.voc.at(f.owner['id'])}: idiom `{f.owner['id']}`: `{p['id']}` takes {len(p['args'])} "
                               f"argument(s) ({', '.join(p['args'])}), given {len(vals)}")
        cat = p["cat"]
        return Node(p, dict(zip(p["args"], vals)), cat, form=f.text)


def split_args(s: str) -> list:
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def fix_types(tree, voc: Vocabulary):
    """After an idiom is expanded its inner nodes carry the category their piece declares, with `T` not
    yet chosen. Choose it from the arguments (a measure<T> takes the T of what fills it)."""
    for n in walk(tree):
        if isinstance(n, Node) and "<T>" in n.cat:
            ts = {re.search(r"<(\w+)>", a.cat).group(1) for a in n.args.values()
                  if isinstance(a, Node) and re.search(r"<(\w+)>", a.cat) and "<T>" not in a.cat}
            if len(ts) == 1:
                n.cat = n.cat.replace("<T>", f"<{ts.pop()}>")


# --------------------------------------------------------------------------- compiled readings

@dataclass
class Claim:
    frame: dict          # the frame piece
    node: Node | None
    mods: list           # opmods applied to this claim only: "rejected" / "successful"
    op: str              # Lean text of the operation the claim is about (scope and modifiers applied)
    lean: str
    at: str
    check: str
    echo: str
    step: int = -1       # index of the Then step it came from (-1: added by a default)
    default: str = ""    # "D1" if the claim was added by a default
    clause: int = 0      # Rule: which clause
    calls: str = "every" # the constructor of `Frames.Calls` the emitted `op` carries: every | accepted | rejected. Set where
                         # `op` is written (Compiler.claim), compared with what Lean says of `op` on every run (narrowing.py)
    any_run: str = ""    # Rule: `lean` again, with the operation's `run` replaced by a variable `run` (the claim as it would
                         # be stated of ANY operation of these types; for the vacuity check of a narrowed claim)

    @property
    def runs(self) -> int:
        """1: a claim about one call; 2: a claim that compares two calls (monotone, same answer, ...)."""
        return int(self.frame.get("runs", 1))


@dataclass
class Reading:
    id: str                         # Spec.<feature>.<scenario>  /  Rule.<feature>.<rule>
    kind: str                       # scenario | rule
    source: str                     # file:line
    text: str                       # the sentence(s) as written
    outer: list = field(default_factory=list)      # [(name, Lean type)] quantified at the front
    state_type: str = ""
    input_type: str = ""
    base: str = ""                  # the operation with no scope (sequence and bystanders applied)
    op: str = ""                    # ... with the Givens applied
    conds: list = field(default_factory=list)      # [{lean, echo, node, step, pin}]
    claims: list = field(default_factory=list)
    used: list = field(default_factory=list)       # piece / operation / idiom ids, in order of first use
    regular: bool = True            # no idiom was needed
    echo: list = field(default_factory=list)       # the slot-structured English, as lines
    defaults: list = field(default_factory=list)   # default ids applied
    coverage: list = field(default_factory=list)   # the Calls value of each claim (every | accepted | rejected), as printed
    info: dict = field(default_factory=dict)       # what the link generator needs (state paths, inputs, stages)

    @property
    def name(self):
        return self.id + ".reading"

    def lean_def(self) -> str:
        body = " ∧\n    ".join(c.lean for c in self.claims)
        q = f"∀ {group(self.outer)},\n    " if self.outer else ""
        return f"def {self.name} : Prop :=\n  {q}{body}"


def group(pairs) -> str:
    out, i = [], 0
    while i < len(pairs):
        j = i
        while j < len(pairs) and pairs[j][1] == pairs[i][1]:
            j += 1
        out.append("(" + " ".join(n for n, _ in pairs[i:j]) + " : " + pairs[i][1] + ")")
        i = j
    return " ".join(out)


def wrap(s: str) -> str:
    """Parenthesise a rendered piece when it is put where one argument is expected."""
    if " " not in s or (s[0] == "(" and s[-1] == ")" and balanced(s[1:-1])) or (s[0] == "[" and s[-1] == "]"):
        return s
    return "(" + s + ")"


def balanced(s: str) -> bool:
    d = 0
    for ch in s:
        d += ch in "(["
        d -= ch in ")]"
        if d < 0:
            return False
    return d == 0


class Ctx:
    """Where the leaves of a tree point: actors to parts of the state, values to parameters, the input or literals."""

    def __init__(self, voc, mode):
        self.voc, self.mode = voc, mode
        self.actor_path = {}      # actor text -> path under the state variable ("" / ".1" / ".2" / ".1.1" ...)
        self.actor_type = {}
        self.actor_role = {}      # actor text -> role name (bystanders: "bystander")
        self.input_path = {}      # parameter name, or role phrase -> path under `inp`
        self.opbase = ""

    def actor(self, leaf: Leaf, sv: str) -> str:
        return sv + self.actor_path[leaf.text]

    def value(self, leaf: Leaf) -> str:
        from . import emit
        if leaf.how == "param":
            return "inp" + self.input_path[leaf.param] if leaf.param in self.input_path else leaf.param
        if leaf.how == "role":
            return "inp" + self.input_path[leaf.text]
        t = emit.lit_term(self.voc.pts, leaf.type, leaf.text)
        return t if leaf.how == "enum" else "(" + t + ")"

    def say(self, leaf: Leaf) -> str:
        """How a leaf is named in the echo. A value of a type the books list under `introduced_by_kind`, written as a
        parameter or a literal, is introduced by its kind ("the <type> <t>"); a role and everything else is shown as written."""
        if leaf.kind == "value" and leaf.how in ("param", "lit") and leaf.type in self.voc.raw["introduced_by_kind"]:
            return f"the {leaf.type} {leaf.text}"
        return leaf.text


def render(x, ctx: Ctx, sv: str = "st", item: str | None = None) -> str:
    """Lean text of a tree, read on the state variable `sv`."""
    if isinstance(x, list):
        return "[" + ", ".join(render(y, ctx, sv, item) for y in x) + "]"
    if isinstance(x, Leaf):
        return ctx.actor(x, sv) if x.kind == "actor" else ctx.value(x)
    p = x.piece
    if x.variant == "per_actor":
        typ = p["per_actor"]["type"]
        hole = next(iter(p["args"]))
        each = [a for a, t in ctx.actor_type.items() if t == typ]
        return ", ".join(p["lean"].replace("{" + hole + "}", sv + ctx.actor_path[a]) for a in each)
    tmpl = p["lean"]
    sub_item = item
    if "item" in p:                 # a quantifier: it says which item its item condition is about
        sub_item = "x" if p["item"] == "x" else render(x.args[p["item"].strip("{}")], ctx, sv, item)
    out = tmpl
    for name, val in x.args.items():
        if "{" + name + "}" not in out:
            continue
        r = render(val, ctx, sv, sub_item)
        out = out.replace("{" + name + "}", r if p["id"] in ("all_of", "holds_of") or isinstance(val, list) else wrap(r))
    out = out.replace("{item}", item or "x").replace("{opbase}", ctx.opbase)
    return out


def say(x, ctx: Ctx) -> str:
    """The English a tree contributes to the echo."""
    if isinstance(x, list):
        return " and ".join(say(y, ctx) for y in x)
    if isinstance(x, Leaf):
        return ctx.say(x)
    p = x.piece
    if x.variant == "per_actor":
        typ = p["per_actor"]["type"]
        names = [a for a, t in ctx.actor_type.items() if t == typ]
        return p["per_actor"]["echo"] + " (" + ", ".join(names) + ")"
    if p["id"] in ("not", "never"):          # a negated condition or class says what it denies, in its own words
        inner = x.args["p" if p["id"] == "not" else "c"]
        if "not_echo" in inner.piece:
            return fill(inner.piece["not_echo"], inner.args, ctx)
        return "it is NOT the case that " + say(inner, ctx)
    out = fill(p["echo"], x.args, ctx)
    if "{part}" in out:                      # "changes only": what is compared part by part is named by the domain word
        out = out.replace("{part}", next((a.piece["part_echo"] for a in x.args.values()
                                          if isinstance(a, Node) and "part_echo" in a.piece), "value"))
    return out


def fill(tmpl: str, args: dict, ctx: Ctx) -> str:
    out = tmpl
    for name, val in args.items():
        out = out.replace("{" + name + "}", say(val, ctx))
    return out


def lam(cat: str, body: str) -> str:
    return f"({LAMBDA[base_cat(cat)]} => {body})"


def frame_text(tmpl: str, node: Node, ctx: Ctx, op: str) -> str:
    """A frame's `lean` / `at` / `check` template with its holes filled by lambdas of the right type."""
    out = tmpl.replace("{op}", "(" + op + ")" if " " in op else op)
    for name, val in node.args.items():
        if isinstance(val, list):                                      # the parts a ChangesOnly lets change
            r = f"(fun st inp => {render(val, ctx)})"
        elif base_cat(val.cat) == "parts":
            r = f"(fun st => {render(val, ctx)}) (fun st k => {render_tmpl(val.piece['part_measure'], val, ctx)})"
        elif base_cat(val.cat) in CONSTANT_CATS:
            r = wrap(render(val, ctx))
        else:
            r = lam(val.cat, render(val, ctx, item="x"))
        out = out.replace("{" + name + "}", r)
    return out


def render_tmpl(tmpl: str, node: Node, ctx: Ctx) -> str:
    out = tmpl
    for name, val in node.args.items():
        out = out.replace("{" + name + "}", wrap(render(val, ctx)))
    return out


# --------------------------------------------------------------------------- compiling a scenario

def problem(status, line, msg, hint="") -> Problem:
    return Problem(status, status, line, msg, hint)


def nearest(voc: Vocabulary, cat: str, voice: str, domain: str, text: str) -> str:
    import difflib
    forms = sorted({f.text for (c, v), fs in voc.forms.items() if base_cat(c) == base_cat(cat) and v == voice
                    for f in fs if f.owner.get("domain", "shared") in ("shared", domain)})
    near = difflib.get_close_matches(text, forms, n=3, cutoff=0.0)
    return ("nearest forms of the Clausebook for a " + base_cat(cat) + ":\n" + "\n".join(f"  - {p}" for p in near)
            + "\na new sentence needs no new entry if it can be said with existing forms; otherwise add a piece (or an idiom) to the project's local book (clausebook/local/)")


def parse_step(voc, cat, voice, text, line, where, domain, mode, roles, ptypes):
    """One tree (or list of trees) for a step, or a Problem."""
    hits = Parser(voc, domain, mode, roles, ptypes).parse(cat, text, voice)
    if len(hits) == 1:
        fix_types(hits[0], voc)
        return hits[0]
    if len(hits) > 1:
        ways = "; ".join(sorted({describe(h) for h in hits}))
        return problem("AMBIGUOUS", line, f"{where}: \"{text}\" can be built from the Clausebook in {len(hits)} ways: {ways}")
    loose = Parser(voc, domain, mode, roles, ptypes, relaxed=True).parse(cat, text, voice)
    if loose:
        notes = [n for h in loose[:1] for x in walk(h) if isinstance(x, Node) for n in x.notes]
        return problem("ILL-TYPED", line, f"{where}: \"{text}\" fits a form of the Clausebook only if types are ignored: "
                       + ("; ".join(dict.fromkeys(notes)) or "a value of the wrong type fills a hole"))
    return problem("UNBOUND", line, f"{where}: no composition of Clausebook pieces reads \"{text}\" as a {base_cat(cat)}",
                   nearest(voc, cat, voice, domain, text))


def describe(t) -> str:
    if isinstance(t, list):
        return " + ".join(describe(x) for x in t)
    if isinstance(t, Leaf):
        return t.text
    return t.id + ("(" + ", ".join(describe(a) for a in t.args.values()) + ")" if t.args else "")


def op_roles(op: dict, voc) -> dict:
    """Rule mode: the phrase(s) each role of an operation goes by (the `g.role` forms of the book)."""
    out = {}
    for r, t in op["state"]:
        for ph in voc.role_phrases(r):
            out[ph] = ("actor", t, r)
    for r, t in op["input"]:
        for ph in voc.role_phrases(r):
            out[ph] = ("value", t, r)
    return out


def match_when(voc: Vocabulary, text: str):
    """[(operation, {role: Leaf})] for every `when` form the text matches."""
    hits = []
    for op in voc.ops.values():
        types = dict(op["state"]) | dict(op["input"])
        for form in op["when"]:
            segs = [("hole", s[1], types[s[1]]) if s[0] == "hole" else s for s in segments(form)]
            p = Parser(voc, op["domain"], "scenario")
            for b in p._match(segs, 0, text, 0, {}):
                hits.append((op, dict(b)))
    return hits


def state_paths(n_roles: int, n_by: int) -> tuple:
    """Paths under the state variable: ([path of each role], [path of each bystander])."""
    pre = ".1" * n_by
    roles = [pre] if n_roles == 1 else [pre + f".{k + 1}" for k in range(n_roles)]
    bys = [".1" * (n_by - 1 - j) + ".2" for j in range(n_by)]
    return roles, bys


def input_paths(n: int) -> list:
    """Path under `inp` of each When's input in a sequence of n Whens (left-nested pairs)."""
    if n == 1:
        return [""]
    return [".1" * (n - 1 - i) + (".2" if i > 0 else "") for i in range(n)]


TWICE = "NARROWED-TWICE"       # Problem.code of a sentence that scopes or narrows one clause with more than one word


def strip_words(text: str, table) -> tuple:
    """(rest, [modifier of every leading word of `table`, in the order written], [the words as written]). EVERY leading
    word is taken, so that a second one is seen and refused; it is never dropped and never overrides the first."""
    found, words = [], []
    while True:
        hit = next(((w, m) for w, m in table if text.startswith(w)), None)
        if hit is None:
            return text, found, words
        text = text[len(hit[0]):]
        found.append(hit[1])
        words.append(hit[0].strip().rstrip(","))


def narrowed_twice(voc, line: int, where: str, mods: list, words: list, what: str) -> Problem:
    """The refusal of a clause that is narrowed, or scoped, by more than one word. Which calls would it cover? Applying
    the words in turn gives an answer in Lean (the last `calls := ...` wins), but that answer is not what the English
    says, so the sentence is refused and nothing is guessed. The one pair that is read is a narrowing adjective followed
    by `internal` on the subject ("an accepted internal <operation>"). Every word quoted here is the book's."""
    said = " and ".join(f"'{w}'" for w in words)
    narrow = [voc.pieces[m]["calls"] for m in mods if "calls" in voc.pieces[m]]       # which calls each word asks for
    adj = [voc.live_word[m] for m in voc.live_word if "calls" in voc.pieces[m]]
    other = [voc.live_word[m] for m in voc.live_word if "calls" not in voc.pieces[m]]
    pre = [w for w, m in ((voc.prefix_of.get(m), m) for m in voc.pieces) if w]
    if len(set(narrow)) > 1:
        why = "no call is both accepted and rejected, so read literally the clause covers no call at all"
    elif len(narrow) > 1:
        why = "the same narrowing is asked for twice"
    else:
        why = (f"'{other[0] if other else 'internal'}' is written after the one narrowing word, never before it and never twice")
    one = " / ".join(adj)
    return Problem("UNSUPPORTED", TWICE, line,
                   f"{where}: {what} narrows or scopes one clause with more than one word ({said}): {why}. "
                   f"A Rule clause takes ONE of {one} on its subject, and {' / '.join(other) or 'no other word'} only after it; "
                   f"a Then step takes ONE of {' / '.join(repr(w + ',') for w in pre) or 'no prefix'}. "
                   "Refused: a word is never dropped and never overrides another",
                   "say which calls are meant with one word"
                   + (f". For the {adj[0]} (or {adj[-1]}) calls of an {other[0]} operation write both on the subject, in this order: "
                      f"'{adj[0]} {other[0]} <operation>'" if adj and other else ""))


def an(word: str, articles) -> str:
    """The article written before `word`: "an " before a, e, i, o, u, else "a " (if the book has both)."""
    want = "an " if word[:1].lower() in "aeiou" else "a "
    return want if want in articles else (articles[0] if articles else "")


ANY_RUN = "({{ {base} with run := run }})"     # the operation `base` with ANY `run`: same types, same notion of acceptance


class Compiler:
    def __init__(self, voc: Vocabulary, refuse_vacuous: bool = True):
        self.voc = voc
        self.strict, self._legacy, self._checking = self, None, False       # see `explain`
        # Plan node Q1. False ONLY for the controls: the sentences the refusal exists for are compiled without it, so that
        # the kernel can be asked whether each really holds of every operation (lean/Run/Narrowing.lean).
        self.refuse_vacuous = refuse_vacuous

    def calls_of(self, mods) -> str:
        """The constructor of `Frames.Calls` an operation carries after these modifiers, read off the book: a modifier that
        sets it says so (`calls:`). At most one modifier of a claim may set it: a sentence that asks for two is refused
        where it is read (`narrowed_twice`), because in the Lean the last `{ op with calls := ... }` would silently win."""
        setters = [m for m in mods if "calls" in self.voc.pieces[m]]
        if len(setters) > 1:      # refused before this point (`narrowed_twice`); never resolved as "the last one wins"
            raise FeatureError(f"internal: a claim narrowed by more than one modifier ({', '.join(setters)}) reached the emitter")
        return self.voc.pieces[setters[0]]["calls"] if setters else "every"

    def scoped(self, id_: str, **holes) -> str:
        """The Lean text of a scoping modifier (`given`, `and_then`, `beside`, `internal`), FROM ITS ENTRY IN THE BOOK: the
        `lean:` template with its holes filled. Nothing of that text is a constant of the compiler, so the text a person
        signs for the entry is the text that is emitted, and a sentence that needs an entry the book does not have is
        refused where it is read (`scenario`, `subjects`)."""
        p = self.voc.pieces.get(id_)
        if p is None:
            raise FeatureError(f"internal: the modifier `{id_}` is not in the Clausebook and a sentence that needs it reached the emitter")
        def one(m):
            if m.group(1) not in holes:
                raise FeatureError(f"{self.voc.at(id_)}: `{id_}`: its `lean:` text has a hole `{{{m.group(1)}}}` that the compiler "
                                   f"cannot fill (it fills {', '.join('{' + h + '}' for h in holes)})")
            return holes[m.group(1)]
        return re.sub(r"\{(\w+)\}", one, p["lean"])

    # ---- retired forms and shapes (plan node Q4): refused, and the refusal names what to write
    def explain(self, r, again):
        """`r`: what a sentence compiled to. If it was refused as no composition of the book, the sentence is read once more
        against the book WITH its retired forms (`Vocabulary.legacy_voc`): if it is a composition of those, the refusal says
        which retired form it is written with and what replaced it. The second reading never yields a statement."""
        if not isinstance(r, Problem) or r.status not in ("UNBOUND", "ILL-TYPED") or r.code == RETIRED or self.voc.legacy or not self.voc.retired:
            return r
        if self._legacy is None:
            self._legacy = Compiler(self.voc.legacy_voc(), refuse_vacuous=False)
            self._legacy.strict = self
        r2 = again(self._legacy)
        return r2 if isinstance(r2, Problem) and r2.code in (RETIRED, TWICE) else r

    def vp_of(self, t):
        """The verb phrase a frame read through its Then form has with the same holes (then it is the frame's one voice in
        a Rule line), or None."""
        if not isinstance(t, Node) or t.idiom or t.piece.get("kind") != "frame" or not t.form:
            return None
        names = lambda f: {s[1] for s in segments(f) if s[0] == "hole"}
        return next((f for f in t.piece.get("vp_forms") or [] if names(f) == names(t.form)), None)

    def spelled_out(self, n) -> bool:
        """"never loses that it is accepted": a frame that has a form whose words stand for a class (`implied:`), written
        with its other form and a class that IS that class (`same_as:`). Refused where the frame says `implied_only`."""
        if not isinstance(n, Node) or not n.piece.get("implied_only"):
            return False
        for hole, pid in (n.piece.get("implied") or {}).items():
            a = n.args.get(hole)
            if isinstance(a, Node) and not a.neg and a.piece.get("same_as") == pid and ("{" + hole) in n.form:
                return True
        return False

    def negated_hole(self, n):
        """(hole, the piece to say it with) if a frame that refuses a negated hole (`negated:`) has one, else None."""
        if isinstance(n, Node) and not n.neg:
            for hole, other in (n.piece.get("negated") or {}).items():
                a = n.args.get(hole)
                if isinstance(a, Node) and a.id == "not" and a.neg:
                    return hole, other
        return None

    def tree_violations(self, tree) -> list:
        """What in a parse tree the book no longer accepts, in words."""
        out, seen = [], set()
        for n in walk(tree):
            if not isinstance(n, Node):
                continue
            if n.now and (n.form, n.now) not in seen:
                seen.add((n.form, n.now))
                owner = n.idiom or (n.args["p"].id if n.id == "not" and n.neg else n.id)
                out.append(f"the form \"{n.form}\" of `{owner}` ({self.voc.at(owner)}) was replaced by \"{n.now}\"")
            neg = self.negated_hole(n)
            if neg:
                out.append(f"`{n.id}` (\"{n.form}\") is not said of a negated condition: the book has one sentence for that, the form of `{neg[1]}` "
                           f"(\"{(self.voc.pieces[neg[1]].get('then_forms') or self.voc.pieces[neg[1]].get('forms'))[0]}\")")
            if self.spelled_out(n):
                short = next(f for f in n.piece["vp_forms"] if not any(("{" + h) in f for h in n.piece["implied"]))
                out.append(f"`{n.id}` is written \"{short}\" when the class is the operation's own acceptance, not \"{n.form}\" with the class spelled out")
        return out

    def surface(self, x, voice="", form=None):
        """A parse tree written back as a sentence, WITH THE LIVE FORMS OF THE BOOK: each piece in its one form for the
        position, a retired form as the form that replaced it, a refused shape as the shape to write. None if it cannot
        be written (nothing is guessed: the caller then names the forms only)."""
        voc = self.voc
        if isinstance(x, Leaf):
            return x.text
        if isinstance(x, list):
            if not x or not all(isinstance(y, Node) and y.idiom and y.said is x[0].said for y in x):
                return None
            x = x[0]
        if x.idiom:
            if x.said is None:
                return None
            f, args = x.now or x.form, x.said
        else:
            p, args, neg = x.piece, x.args, False
            if x.id == "not" and x.neg:
                p, args, neg = x.args["p"].piece, x.args["p"].args, True
            if p["id"] == "changes_only":
                args = {"c": args["c"], "x": args["xs"][0], "y": args["xs"][1]}
            f = form
            if f is None and voice == "first":
                f = next(iter(p.get("first_call_not_forms" if neg else "first_call_forms") or []), None)
                if f is None:
                    return None
            if f is None:
                f = x.now or x.form
            hit = self.negated_hole(x)
            if hit and form is None:
                hole, other = hit
                inner = args[hole].args["p"]
                pos = next(iter(inner.piece.get("forms") or []), None)
                if pos is None:
                    return None
                f = (voc.pieces[other].get("then_forms") or voc.pieces[other].get("forms"))[0]
                args = dict(args)
                args[hole] = Node(inner.piece, inner.args, inner.cat, form=pos)
            if self.spelled_out(x) and form is None:
                f = next(v for v in p["vp_forms"] if not any(("{" + h) in v for h in p["implied"]))
        if not f:
            return None
        out = []
        for s in segments(f):
            if s[0] == "lit":
                out.append(s[1])
                continue
            a = args.get(s[1])
            r = None if a is None else self.surface(a, hole_voice(s[2])[1])
            if r is None:
                return None
            out.append(r)
        return "".join(out)

    def subject_text(self, s, more_mods=()):
        """The subject of a clause, written with the live words of the book: article, one narrowing word, `internal`, the noun."""
        voc = self.voc
        parts = []
        for k, (art, words, noun) in enumerate(s["written"]):
            ws = []
            if k == 0:
                mods = list(more_mods) + [m for m in s["mods"] if m not in more_mods] + (["internal"] if "internal" in s["used"] else [])
                if any(m not in voc.live_word for m in mods):
                    return None
                ws = [voc.live_word[m] for m in mods]
            parts.append(an((ws + [noun])[0], voc.live_articles) + "".join(w + " " for w in ws) + noun)
        out = voc.sequences[0].join(parts) if len(parts) > 1 else parts[0]
        for c in s["cond_trees"]:
            r = self.surface(c)
            if r is None:
                return None
            out += voc.relatives[0] + r
        return out

    def unwrap(self, t):
        """(the claim, [narrowing prefixes written before it]) of one claim of a Rule clause."""
        mods = []
        while isinstance(t, Node) and t.id in ("rejected", "successful") and t.cat == "claim" and "c" in t.args:
            mods.append(t.id)
            t = t.args["c"]
        return t, mods

    def clause_violations(self, h) -> list:
        """What in ONE clause of a Rule line the book no longer accepts: a retired word on the subject, a retired form, a
        narrowing before the claim, a Then form of a frame that has a verb phrase."""
        voc = self.voc
        out = list(h["s"]["retired"])
        for t in h["trees"]:
            c, mods = self.unwrap(t)
            if mods and not voc.rule_prefixes:
                out.append(" and ".join(f"'{voc.prefix_of[m]},'" for m in mods) + " before the claim is not read in a Rule line (a Then step reads it): "
                           f"a Rule line narrows on its subject (\"{an(voc.live_word[mods[0]], voc.live_articles)}{voc.live_word[mods[0]]} <operation>\")")
            vp = self.vp_of(c) if h["voice"] == "then" and voc.for_reads == "no_verb_phrase" else None
            if vp:
                out.append(f"`{c.id}` has a verb phrase, and that is its one voice in a Rule line: \"<subject> {vp}\", not \"for <subject>, {c.form}\"")
            out += self.tree_violations(c)
        out += self.tree_violations(h["s"]["cond_trees"])
        return list(dict.fromkeys(out))

    def canonical(self, h):
        """The clause `h` written the one way the book has: narrowing on the subject, each frame in its one voice (a clause
        whose claims do not all take the same voice or the same narrowing becomes several, in the order written), every piece
        in its live form. None if a part cannot be written."""
        voc = self.voc
        groups = []
        for t in h["trees"]:
            c, mods = self.unwrap(t)
            vp = self.vp_of(c) if h["voice"] == "then" else None
            voice = "vp" if vp else h["voice"]
            text = self.surface(c, form=vp)
            if text is None:
                return None
            if groups and groups[-1][0] == mods and groups[-1][1] == voice:
                groups[-1][2].append(text)
            else:
                groups.append((mods, voice, [text]))
        if not voc.clause_seps or not voc.claim_seps:
            return None
        clauses = []
        for mods, voice, texts in groups:
            subj = self.subject_text(h["s"], mods)
            if subj is None or (voice == "vp" and not voc.vp_seps) or (voice != "vp" and not voc.for_shapes):
                return None
            body = voc.claim_seps[0].join(texts)
            clauses.append(subj + voc.vp_seps[0] + body if voice == "vp" else voc.for_shapes[0][0] + subj + voc.for_shapes[0][1] + body)
        return voc.clause_seps[0].join(clauses)

    def compiles(self, text: str, domain: str) -> bool:
        """Is `text` (one or more clauses) a composition of the book as it stands? Asked of a rewritten sentence before it is offered."""
        c = self.strict
        keep, c._checking = c._checking, True
        try:
            return any(all(not isinstance(c.clause(x, domain, "", 0), Problem) for x in split) for split in splits(text, c.voc.clause_seps))
        finally:
            c._checking = keep

    def retired(self, line, where, text, viol, write=None, domain=None, unit="the clause") -> Problem:
        """The refusal of a sentence written with a retired form or in a retired shape. It names what replaced it, and the
        sentence to write when that sentence was checked to compile."""
        ok = bool(write) and write != text and (domain is None or self.compiles(write, domain))
        return Problem("UNBOUND", RETIRED, line,
                       f"{where}: \"{text}\" is written in a way the Clausebook no longer accepts (one live form per piece per position): "
                       + "; ".join(viol),
                       (f"write {unit} as: \"{write}\"" if ok else "write it with the form named above")
                       + "\na retired form is recorded in the `retired:` field of its entry; it is never accepted again by adding it back, only by replacing the live one")

    # ---- shared by scenarios and rules
    def claims_of(self, trees, ctx, op_text, step, clause=0, mods=(), any_op=None):
        """Then-trees -> Claims. A class standing alone is `always`; under "not" it is `never`."""
        out = []
        for t in (trees if isinstance(trees, list) else [trees]):
            node, m = t, list(mods)
            while isinstance(node, Node) and node.id in ("rejected", "successful") and node.cat == "claim":
                m.append(node.id)
                node = node.args["c"]
            if isinstance(node, list):
                out += self.claims_of(node, ctx, op_text, step, clause, m, any_op)
                continue
            if node.id == "always" and node.args["c"].id == "not":
                node = Node(self.voc.pieces["never"], {"c": node.args["c"].args["p"]}, "claim", form=node.form, idiom=node.idiom)
            out.append(self.claim(node, ctx, op_text, m, step, clause, any_op=any_op))
        return out

    def claim(self, node, ctx, op_text, mods, step, clause=0, default="", any_op=None):
        f = node.piece
        op = op_text
        for m in mods:
            op = self.voc.pieces[m]["lean"].replace("{op}", op)
        c = Claim(f, node, list(mods), op, frame_text(f["lean"], node, ctx, op), frame_text(f["at"], node, ctx, op),
                  frame_text(f["check"], node, ctx, op), say(node, ctx), step, default, clause, calls=self.calls_of(mods))
        if any_op is not None:            # (scoped operation, base) with `run` a variable: the same claim of any operation
            op2, base = any_op
            for m in mods:
                op2 = self.voc.pieces[m]["lean"].replace("{op}", op2)
            keep, ctx.opbase = ctx.opbase, base
            try:
                c.any_run = frame_text(f["lean"], node, ctx, op2)
            finally:
                ctx.opbase = keep
        return c

    def fill_implied(self, t, line, where):
        """"is accepted whenever / only if / exactly when", "never loses acceptance", "is always accepted": the form has no
        hole for the class; its words stand for it, and the book says which piece they mean (`implied:` of the frame).
        A form that leaves a hole of its frame unfilled, with no such piece named, is refused (a Problem); else None."""
        voc = self.voc
        for n in walk(t):
            if isinstance(n, Node) and n.piece.get("kind") == "frame":
                for hole in dict.fromkeys(m.group(1) for m in HOLE.finditer(n.piece["lean"])):      # the holes its Lean text has
                    if hole not in n.args and hole not in ("op", "opbase"):
                        pid = (n.piece.get("implied") or {}).get(hole)
                        if pid is None:
                            return problem("UNBOUND", line, f"{where}: \"{n.form}\" is a form of `{n.id}` that leaves its hole `{hole}` unfilled, "
                                           f"and the Clausebook names no piece its words stand for (`implied:` of `{n.id}`, {voc.at(n.id)})")
                        n.args[hole] = Node(voc.pieces[pid], {}, voc.pieces[pid]["cat"])
        return None

    def answer_check(self, trees, ops, line, where):
        """Answer words must be about the kind of answer the (last) operation gives."""
        want = ops[-1]["answer"]
        for n in walk(trees):
            if isinstance(n, Node) and n.piece.get("answer") and n.piece["answer"] != want:
                return problem("ILL-TYPED", line, f"{where}: `{n.id}` speaks about an answer of type `{n.piece['answer']}`, "
                               f"but the {'last ' if len(ops) > 1 else ''}operation (`{ops[-1]['id']}`) answers `{want}`")
        return None

    def op_check(self, trees, ops, line, where):
        """A relation between two calls, or a reference function, is a domain word OF ONE OPERATION."""
        for n in walk(trees):
            if isinstance(n, Node) and n.piece.get("for_op"):
                if len(ops) != 1 or ops[0]["id"] != n.piece["for_op"]:
                    return problem("ILL-TYPED", line, f"{where}: `{n.id}` is a {base_cat(n.cat)} of the operation `{n.piece['for_op']}`, "
                                   f"but the sentence is about `{' followed by '.join(o['id'] for o in ops)}`")
        return None

    def used(self, rd: Reading, *trees, extra=()):
        for i in extra:
            if i not in rd.used:
                rd.used.append(i)
        for n in walk(list(trees)):
            if isinstance(n, Node):
                if n.idiom and n.idiom not in rd.used:
                    rd.used.append(n.idiom)
                    rd.regular = False
                if n.id not in rd.used:
                    rd.used.append(n.id)

    # ---- a scenario
    def scenario(self, sc) -> Reading | Problem:
        return self.explain(self._scenario(sc), lambda c: c._scenario(sc))

    def _scenario(self, sc) -> Reading | Problem:
        voc = self.voc
        steps = list(sc.background) + list(sc.steps)
        where = f"{sc.feature.path}"
        rd = Reading(sc.id, "scenario", f"{sc.feature.path}:{sc.line}", sc.text)
        whens = [s for s in steps if s.kind == "when"]
        if not whens:
            return problem("UNSUPPORTED", sc.line, "at least one When is required")
        ops, binds = [], []
        for w in whens:
            hits = match_when(voc, w.text)
            if not hits:
                near = __import__("difflib").get_close_matches(w.text, [f for o in voc.ops.values() for f in o["when"]], n=3, cutoff=0.0)
                return problem("UNBOUND", w.line, f"{where}:{w.line}: no operation of the Clausebook is named by \"{w.text}\"",
                               "nearest `when` forms:\n" + "\n".join(f"  - {p}" for p in near))
            if len(hits) > 1:
                return problem("AMBIGUOUS", w.line, f"{where}:{w.line}: \"{w.text}\" names {len(hits)} operations: "
                               + ", ".join(o["id"] for o, _ in hits))
            ops.append(hits[0][0])
            binds.append(hits[0][1])
        domain = ops[0]["domain"]
        if any(o["domain"] != domain for o in ops):
            return problem("ILL-TYPED", whens[0].line, f"{where}:{whens[0].line}: the Whens of one scenario name operations of different systems")
        # the state: the roles of the first operation; every later When must act on the same actors
        st_roles = ops[0]["state"]
        st_actors = [binds[0][r].text for r, _ in st_roles]
        if len(set(st_actors)) != len(st_actors):
            return problem("UNSUPPORTED", whens[0].line, f"{where}:{whens[0].line}: the same actor fills two roles of one operation")
        for k, (o, b) in enumerate(zip(ops[1:], binds[1:]), 1):
            if [t for _, t in o["state"]] != [t for _, t in st_roles] or [b[r].text for r, _ in o["state"]] != st_actors:
                return problem("ILL-TYPED", whens[k].line, f"{where}:{whens[k].line}: this When acts on a different state from the first "
                               "(a sequence of Whens must be about the same actors, in the same roles)")
        ctx = Ctx(voc, "scenario")
        ptypes = {}
        # inputs: one per When (an operation here takes at most one input besides its state)
        ipaths = input_paths(len(ops))
        in_types, pins = [], []
        for k, (o, b) in enumerate(zip(ops, binds)):
            if not o["input"]:
                in_types.append("Unit")
                continue
            (role, typ), = o["input"]
            leaf = b[role]
            in_types.append(voc.pts[typ]["lean"])
            if leaf.how == "param":
                if ptypes.setdefault(leaf.param, typ) != typ:
                    return problem("ILL-TYPED", whens[k].line, f"{where}:{whens[k].line}: <{leaf.param}> is used as both "
                                   f"`{ptypes[leaf.param]}` and `{typ}`")
                if leaf.param in ctx.input_path:
                    return problem("UNSUPPORTED", whens[k].line, f"{where}:{whens[k].line}: <{leaf.param}> is the input of two Whens")
                ctx.input_path[leaf.param] = ipaths[k]
            else:
                bad = literal_problem(voc.pts, typ, leaf.text)
                if bad:
                    return problem("UNSUPPORTED", whens[k].line, f"{where}:{whens[k].line}: {bad}")
                pins.append((k, leaf))
        # Givens and Thens
        givens, thens = [], []
        roles = {}
        old = []                              # steps written with a retired form or shape: [(step, what, the step rewritten or None)]
        for s in steps:
            if s.kind == "when":
                continue
            cat, voice = ("cond", "") if s.kind == "given" else ("claim", "then")
            text, mods, words = s.text, [], []
            if s.kind == "then":
                text, mods, words = strip_words(text, voc.claim_prefixes)
                if len(mods) > 1:
                    return narrowed_twice(voc, s.line, f"{where}:{s.line}", mods, words, f"the Then \"{s.text}\"")
            t = parse_step(voc, cat, voice, text, s.line, f"{where}:{s.line}", domain, "scenario", roles, ptypes)
            if isinstance(t, Problem):
                return t
            for leaf in walk(t):
                if isinstance(leaf, Leaf) and leaf.how == "param":
                    if ptypes.setdefault(leaf.param, leaf.type) != leaf.type:
                        return problem("ILL-TYPED", s.line, f"{where}:{s.line}: <{leaf.param}> is used as both "
                                       f"`{ptypes[leaf.param]}` and `{leaf.type}`")
                if isinstance(leaf, Leaf) and leaf.how == "lit":
                    bad = literal_problem(voc.pts, leaf.type, leaf.text)
                    if bad:
                        return problem("UNSUPPORTED", s.line, f"{where}:{s.line}: {bad}")
            if s.kind == "then":
                bad = (self.fill_implied(t, s.line, f"{where}:{s.line}") or self.answer_check(t, ops, s.line, f"{where}:{s.line}")
                       or self.op_check(t, ops, s.line, f"{where}:{s.line}"))
                if bad:
                    return bad
            viol = self.tree_violations(t)
            if viol:
                new = self.surface(t)
                new = None if new is None else "".join(w + ", " for w in words) + new
                if new is not None and isinstance(parse_step(self.strict.voc, cat, voice, new[len(s.text) - len(text):], s.line, "", domain,
                                                             "scenario", roles, dict(ptypes)), Problem):
                    new = None                # the rewritten step is offered only if the book as it stands reads it
                old.append((s, viol, new))
            (givens if s.kind == "given" else thens).append((s, t, mods))
        if old:
            s0 = old[0][0]
            return Problem("UNBOUND", RETIRED, s0.line,
                           f"{where}:{s0.line}: " + " | ".join(f"\"{s.text}\" (line {s.line}) is written in a way the Clausebook no longer accepts "
                                                              f"(one live form per piece per position): {'; '.join(v)}" for s, v, _ in old),
                           "\n".join(f"write line {s.line} as: \"{new}\"" if new else f"write line {s.line} with the form named above" for s, _, new in old)
                           + "\na retired form is recorded in the `retired:` field of its entry; it is never accepted again by adding it back, only by replacing the live one")
        if not thens:
            return problem("UNSUPPORTED", sc.line, "a scenario needs at least one Then")
        for p in ptypes:
            if sc.outline and p not in sc.header:
                return problem("UNSUPPORTED", sc.line, f"<{p}> is not a column of the Examples table")
            if not sc.outline:
                return problem("UNSUPPORTED", sc.line, "<placeholders> are only allowed in a Scenario Outline")
        # actors: the roles of the state, then bystanders in order of first mention
        mentioned = []
        for _, t, _ in givens + thens:
            for leaf in walk(t):
                if isinstance(leaf, Leaf) and leaf.kind == "actor" and leaf.text not in mentioned:
                    mentioned.append(leaf.text)
                    ctx.actor_type.setdefault(leaf.text, leaf.type)
        bys = [a for a in mentioned if a not in st_actors]
        rpaths, bpaths = state_paths(len(st_roles), len(bys))
        ordered = {}
        for (r, t), a, p in zip(st_roles, st_actors, rpaths):
            ctx.actor_path[a], ctx.actor_role[a] = p, r
            ordered[a] = t
        for a, p in zip(bys, bpaths):
            ctx.actor_path[a], ctx.actor_role[a] = p, "bystander"
            ordered[a] = ctx.actor_type[a]
        ctx.actor_type = ordered              # roles first, then bystanders: the order "all ..." lists them in
        # the operation. What joins two Whens, sets a bystander beside the operation and puts the Givens before it is the
        # Lean text of a book entry (`and_then`, `beside`, `given`): with the entry gone, the scenario has no reading.
        for need, wanted, why in (("and_then", len(ops) > 1, f"it has {len(ops)} Whens"),
                                  ("beside", bool(bys), f"it names {', '.join(bys)}, which no When passes to the operation"),
                                  ("given", bool(givens or pins), "it has a Given, or a When with a literal input")):
            if wanted and need not in voc.pieces:
                return problem("UNBOUND", sc.line, f"{where}:{sc.line}: {why}, and the Clausebook has no entry `{need}` to read that with")
        base = ops[0]["lean"]
        for o in ops[1:]:
            base = self.scoped("and_then", op=base, op2=o["lean"])
        st_type = " × ".join(voc.actors[t]["lean"] for _, t in st_roles)
        for a in bys:
            base = self.scoped("beside", op=base, type=voc.actors[ctx.actor_type[a]]["lean"])
            st_type = f"({st_type}) × {voc.actors[ctx.actor_type[a]]['lean']}"
        ctx.opbase = base
        in_type = in_types[0]
        for t in in_types[1:]:
            in_type = f"({in_type}) × {t}"
        rd.base, rd.state_type, rd.input_type = base, st_type, in_type
        for s, t, _ in givens:
            rd.conds.append({"lean": render(t, ctx), "echo": say(t, ctx), "node": t, "step": s, "pin": None})
        for k, leaf in pins:
            rd.conds.append({"lean": f"inp{ipaths[k]} = {ctx.value(leaf)}", "pin": (k, leaf), "node": None, "step": whens[k],
                             "echo": f"the input{' of When ' + str(k + 1) if len(ops) > 1 else ''} is {leaf.text}"})
        rd.op = base if not rd.conds else self.scoped("given", op=base, c=" ∧ ".join(c["lean"] for c in rd.conds))
        for j, (s, t, mods) in enumerate(thens):
            rd.claims += self.claims_of(t, ctx, rd.op, j, mods=mods)
        if all(c.mods for c in rd.claims):            # D1: a scenario always includes "the call gives an answer"
            aa = Node(voc.pieces["always_answers"], {}, "claim")
            rd.claims.insert(0, self.claim(aa, ctx, rd.op, [], -1, default="D1"))
        rd.outer = [(h, voc.pts[ptypes[h]]["lean"]) for h in (sc.header if sc.outline else []) if h in ptypes and h not in ctx.input_path]
        self.used(rd, [t for _, t, _ in givens], extra=[o["id"] for o in ops] + (["and_then"] if len(ops) > 1 else [])
                  + (["beside"] if bys else []) + (["given"] if rd.conds else []))
        self.used(rd, [t for _, t, _ in thens], extra=[m for _, _, ms in thens for m in ms] + [c.frame["id"] for c in rd.claims])
        rd.info = {"ctx": ctx, "ops": ops, "binds": binds, "st_actors": st_actors, "bystanders": bys, "ipaths": ipaths,
                   "pins": pins, "givens": givens, "thens": thens, "ptypes": ptypes, "whens": whens}
        self.echo_scenario(rd, sc, ops, binds, bys, ctx)
        return rd

    def echo_scenario(self, rd, sc, ops, binds, bys, ctx):
        voc = self.voc
        def who(r, text):          # "sender (Alice)"; "ledger Main" when the name already says the role
            return text if text.startswith(r + " ") else f"{r} ({text})"
        whos = [who(r, binds[0][r].text) for r, _ in ops[0]["state"]]
        ins = []
        for k, (o, b) in enumerate(zip(ops, binds)):
            for r, _ in o["input"]:
                leaf = b[r]
                ins.append(typed(voc, f"{r} {leaf.text}", leaf.type) if leaf.how == "param" else f"the one {r} {leaf.text}")
        what = (voc.sequences[0] if voc.sequences else " followed by ").join(fill_op(o, b, ctx) for o, b in zip(ops, binds))
        cov = voc.covers                                   # the coverage texts of the book, by constructor of Frames.Calls
        filt = sorted({c.calls for c in rd.claims if c.calls != "every"})
        every = [c for c in rd.claims if c.calls == "every"]
        applies = (f"{what}: every {', every '.join(whos)}"
                   + (", and every " + " and every ".join(x for x in ins if not x.startswith("the one")) if any(not x.startswith("the one") for x in ins) else "")
                   + (", with " + " and ".join(x for x in ins if x.startswith("the one")) if any(x.startswith("the one") for x in ins) else ""))
        if rd.outer:
            applies += "; for every value of " + ", ".join(typed(voc, n, rd.info["ptypes"][n]) for n, _ in rd.outer)
        if not sc.outline:
            applies += " (a plain Scenario: the values are the literals written in it)"
        o = [("applies to", applies)]
        if bys:
            o.append(("", "beside it: " + ", ".join(bys) + " (named, but not passed to the operation, so unchanged by construction)"))
        # which calls: read off each claim's Calls value (the one its emitted operation carries), never off the words.
        # A scenario always requires an answer (D1: a claim about every call is added when every Then is narrowed), so
        # `every` is always among them; a narrowed claim is listed too and says so again on its own line.
        kinds = list(dict.fromkeys(c.calls for c in rd.claims))
        o.append(("covers", "; ".join(cov[k]["covers"] for k in kinds)))
        o.append(("assuming", "; ".join(c["echo"] for c in rd.conds) or "nothing: every state and every input"))
        first = True
        if every:
            o.append(("then", cov["every"]["answer"]))
            first = False
        for c in rd.claims:
            if c.default:
                continue
            if c.frame["id"] == "always_answers" and c.calls == "every":
                o[-1] = ("then", cov["every"]["answer_asked"].replace("{words}", c.node.form or "it answers"))      # the words as the book has them
                continue
            o.append(("then" if first else "", (cov[c.calls]["prefix"] if len(kinds) > 1 else "") + c.echo))
            first = False
        if len(ops) > 1:      # true of a scenario whatever its Thens: a claim about every call is always among its claims (D1)
            o.append(("", cov["every"]["sequence_scenario"]))
        if speaks_of_acceptance(rd.claims):
            o.append(("accepted", ops[-1]["accepted_echo"]))
        ds = ["D1", "D2", "D4"] if every else ["D1", "D4"]
        for c in rd.claims:
            for d in c.frame.get("defaults", []):
                if d not in ds and d not in cov[c.calls].get("removes", []):
                    ds.append(d)
        for n in walk([c["node"] for c in rd.conds if c["node"] is not None] + [c.node for c in rd.claims if c.node]):
            if isinstance(n, Node):
                for d in n.piece.get("defaults", []):
                    if d not in ds:
                        ds.append(d)
        ds += [d for d in reading_rules([c["node"] for c in rd.conds if c["node"] is not None] + [c.node for c in rd.claims if c.node],
                                        any(c["node"] is not None for c in rd.conds)) if d not in ds]
        rd.defaults = sorted(ds, key=lambda d: int(d[1:]))
        for k, d in enumerate(rd.defaults):
            o.append(("defaults" if k == 0 else "", f"{d} {voc.default(d)}"))
        for k in filt:
            o.append(("not default", cov[k]["weakening"]))
        rd.coverage = [c.calls for c in rd.claims]
        for k in dict.fromkeys(rd.coverage):               # the reading prints these entries: it rests on them
            if cov[k]["id"] not in rd.used:
                rd.used.append(cov[k]["id"])
        rd.used += [d for d in rd.defaults if d not in rd.used]      # ... and on every default printed with it
        rd.echo = o

    # ---- a Rule line
    def rule(self, rule, domain_hint=None) -> Reading | Problem:
        return self.explain(self._rule(rule, domain_hint), lambda c: c._rule(rule, domain_hint))

    def _rule(self, rule, domain_hint=None) -> Reading | Problem:
        voc = self.voc
        where = f"{rule.feature.path}:{rule.line}"
        text = rule.name.strip()
        if voc.line_stop_optional:
            text = text.rstrip(".")
        if voc.line_any_case and text:
            text = text[0].lower() + text[1:]
        rd = Reading(rule.id, "rule", where, f"Rule: {rule.name}")
        domains = [domain_hint] if domain_hint else sorted({o["domain"] for o in voc.ops.values()})
        results, problems = [], []
        for d in domains:
            for split in splits(text, voc.clause_seps):
                got = [self.clause(c, d, where, rule.line) for c in split]
                if all(not isinstance(g, Problem) for g in got):
                    results.append((d, got))
                else:
                    problems.append(next(g for g in got if isinstance(g, Problem)))
        if not results:
            problems.sort(key=lambda p: (rank_problem(p), -len(p.message)))
            return problems[0] if problems else problem("UNBOUND", rule.line, f"{where}: the rule line is empty")
        uniq = {}
        for d, got in results:
            uniq.setdefault((d, tuple(g["key"] for g in got)), (d, got))
        if len(uniq) > 1:
            return problem("AMBIGUOUS", rule.line, f"{where}: the rule line can be built from the Clausebook in {len(uniq)} ways: "
                           + "; ".join(sorted(f"[{d}] " + " | ".join(k) for d, k in uniq)))
        d, got = next(iter(uniq.values()))
        if self.refuse_vacuous:
            # Plan node Q1. The line HAS one composition; it is refused if a narrowed claim of it holds of EVERY operation
            # (it would say nothing about this one). The refusal names the theorem of lean/Frames/Narrowing.lean that proves
            # it (clausal/narrowing.py). Decided after the composition is settled, so it never changes which one is found.
            for g in got:
                bad = narrowing.refusal(voc, g["claims"], g["ops"], where, rule.line, g["text"])
                if bad:
                    return bad
        for k, g in enumerate(got):
            for c in g["claims"]:
                c.clause = k
            rd.claims += g["claims"]
            for i in g["used"]:
                if i not in rd.used:
                    rd.used.append(i)
            rd.regular = rd.regular and g["regular"]
        rd.info = {"clauses": got, "domain": d}
        rd.state_type, rd.input_type, rd.base = got[0]["state_type"], got[0]["input_type"], got[0]["base"]
        self.echo_rule(rd, got)
        # the grammar entries the line was read through, then every default printed with it: the reading rests on them
        gram = [i for g in got for i in g["grammar"]] + (["g.clauses"] if len(got) > 1 else []) + ["g.line"]
        rd.used += [i for i in dict.fromkeys(gram + rd.defaults) if i not in rd.used and (i in voc.grammar or i in voc.raw["defaults"])]
        return rd

    def clause(self, text: str, domain: str, where: str, line: int):
        """One clause of a rule line:  <subject> <vp> [and <vp>]   or   for <subject>, <claim> [and <claim>]."""
        voc = self.voc
        best = None
        hits = []
        shapes = []
        for pre, sep in voc.for_shapes:                # "for <subject>, <claim>" (g.rule_for)
            if re.fullmatch(re.escape(pre) + r"(.+?)" + re.escape(sep) + r"(.+)", text):
                for cut in [x.start() for x in re.finditer(re.escape(sep), text)]:
                    shapes.append((text[len(pre):cut], text[cut + len(sep):], "then", "g.rule_for"))
        if not shapes:
            for sep in voc.vp_seps:                    # "<subject> <verb phrase>" (g.rule_vp)
                for cut in [x.start() for x in re.finditer(re.escape(sep), text)]:
                    shapes.append((text[:cut], text[cut + len(sep):], "vp", "g.rule_vp"))
        for subj, rest, voice, gram in shapes:
            for s in self.subjects(subj, domain):
                if isinstance(s, Problem):
                    if s.code == TWICE:        # a subject with two narrowing words, or `internal` before one: refused, with the reason
                        p = narrowed_twice(voc, line, where, s.hint.split(","), s.message.split(","), f"the subject \"{subj}\"")
                        if best is None or rank_problem(p) < rank_problem(best):
                            best = p
                    continue
                ctx, ops = s["ctx"], s["ops"]
                roles = s["roles"]
                parts_list = splits(rest, voc.claim_seps)
                for parts in parts_list:
                    trees, bad = [], None
                    for part in parts:
                        t = self.rule_part(part, voice, domain, roles, where, line, ops)
                        if isinstance(t, Problem):
                            bad = t
                            break
                        trees.append(t)
                    on_claim = [t.id for t in trees if isinstance(t, Node) and t.id in ("rejected", "successful") and t.cat == "claim"]
                    if not bad and s["mods"] and on_claim:
                        # narrowed on the subject AND on the claim ("for an accepted transfer, if it is rejected, ..."):
                        # the Lean would be `((op).successful).rejected`, i.e. rejected calls; the English covers no call
                        bad = narrowed_twice(voc, line, where, s["mods"] + on_claim, s["mod_words"] + [voc.prefix_of[m] for m in on_claim],
                                             f"\"{text}\"")
                    if bad:
                        if best is None or rank_problem(bad) < rank_problem(best):
                            best = bad
                        continue
                    op_text = s["op"]
                    claims = []
                    for t in trees:
                        claims += self.claims_of(t, ctx, op_text, -1, mods=s["mods"], any_op=(s["op_any"], s["base_any"]))
                    rd = Reading("", "rule", where, text)
                    self.used(rd, s["cond_trees"], trees, extra=s["used"] + [c.frame["id"] for c in claims])
                    by_role = any(isinstance(x, Leaf) and x.how == "role" for x in walk(s["cond_trees"] + trees))
                    hits.append({"subject": subj, "ops": ops, "ctx": ctx, "claims": claims, "op": op_text, "base": s["base"],
                                 "s": s, "trees": trees, "voice": voice,
                                 "grammar": ["g.subject", gram] + (["g.role"] if by_role else []) + (["g.claims"] if len(parts) > 1 else []),
                                 "cond_trees": s["cond_trees"], "internal": "internal" in s["used"],
                                 "mods": s["mods"], "conds": s["conds"], "state_type": s["state_type"], "input_type": s["input_type"],
                                 "used": rd.used, "regular": rd.regular, "text": text,
                                 "key": s["key"] + " :: " + " & ".join(describe(t) for t in trees)})
        # A composition written with a retired form, or in a shape the book no longer reads (a narrowing before the claim,
        # the Then form of a frame that has a verb phrase), is NOT a reading: it is set aside, and counts only for the refusal.
        for h in hits:
            h["retired"] = self.clause_violations(h)
        uniq = {h["key"]: h for h in hits if not h["retired"]}
        if len(uniq) == 1:
            return next(iter(uniq.values()))
        if len(uniq) > 1:
            return problem("AMBIGUOUS", line, f"{where}: \"{text}\" can be built from the Clausebook in {len(uniq)} ways: " + "; ".join(sorted(uniq)))
        if best is not None and best.code == TWICE:
            return best
        old = {h["key"]: h for h in hits}
        if old:
            h = old[sorted(old)[0]]
            return self.retired(line, where, text, h["retired"], None if self._checking else self.canonical(h), domain)
        words = [voc.live_word[m] for m in voc.live_word]
        return best or problem("UNBOUND", line, f"{where}: no composition of Clausebook pieces reads \"{text}\" as a rule clause "
                               f"(<{' / '.join(a.strip() for a in voc.live_articles)}> [{' | '.join(words)}] <operation>"
                               + "".join(f" [{x.strip()} <operation>]" for x in voc.sequences[:1]) + "".join(f" [{x.strip()} <condition>]" for x in voc.relatives[:1])
                               + " <what it does>" + "".join(f", or: {pre.strip()} <such an operation>{sep.strip()} <what a Then would say>" for pre, sep in voc.for_shapes[:1]) + ")",
                               "operations of the Clausebook: " + ", ".join(sorted({n for o in voc.ops.values() if o['domain'] == domain for n in o['nouns']})))

    def rule_part(self, part, voice, domain, roles, where, line, ops):
        voc = self.voc
        text, mods = part, []
        if voice == "then":
            text, mods, words = strip_words(text, voc.claim_prefixes)
            if len(mods) > 1:
                return narrowed_twice(voc, line, where, mods, words, f"the claim \"{part}\"")
        t = parse_step(voc, "claim", voice, text, line, where, domain, "rule", roles, {})
        if isinstance(t, Problem):
            return t
        bad = self.fill_implied(t, line, where)
        if bad:
            return bad
        bad = self.answer_check(t, ops, line, where) or self.op_check(t, ops, line, where)
        if bad:
            return bad
        for m in mods:
            t = Node(voc.pieces[m], {"c": t}, "claim")
        return t

    def subjects(self, text: str, domain: str) -> list:
        """Every reading of a rule subject: [{ops, ctx, op (Lean, scoped), mods, conds, ...}]."""
        voc = self.voc
        out = []
        cond_text = None
        heads = [(text, None)]
        for sep in voc.relatives:                      # "<subject> for which <condition>" (`given`, subject_forms)
            for m in re.finditer(re.escape(sep), text):
                heads.append((text[:m.start()], text[m.end():]))
        for head, cond_text in heads:
            for names in follow_splits(head, voc.sequences):
                seqs = [[]]
                for k, nm in enumerate(names):
                    art = next((a for a in voc.articles if nm.startswith(a)), None)
                    if art is None:
                        seqs = []
                        break
                    rest, mods, words = strip_words(nm[len(art):], voc.subject_words)
                    cands = [o for o in voc.ops.values() if o["domain"] == domain and rest in o["nouns"]]
                    if k > 0 and mods:
                        cands = []            # a modifier is written on the whole sequence, i.e. on its first noun
                    # one narrowing word, then `internal`: "an accepted internal transfer". Any other two ("an internal accepted
                    # transfer", "an accepted rejected transfer") are refused in `clause`: nothing is dropped, nothing overrides
                    pair = len(mods) == 2 and "calls" in voc.pieces[mods[0]] and mods[1] == "internal"
                    if len(mods) > 1 and not pair:
                        if cands:
                            out.append(Problem("UNSUPPORTED", TWICE, 0, ",".join(words), ",".join(mods)))
                        cands = []
                    seqs = [s + [(o, mods, (art, words, rest))] for s in seqs for o in cands]
                for seq in seqs:
                    ops = [o for o, _, _ in seq]
                    mods = seq[0][1]
                    written = [w for _, _, w in seq]
                    gone = [f"the article '{a.strip()}' was replaced by '{an(x, voc.live_articles).strip()}'" for a, ws, n in written
                            for x in [(ws + [n])[0]] if a in voc.retired_articles]
                    gone += [f"the word '{w}' on the subject (`{m}`, {voc.at(m)}) was replaced by '{voc.retired_words[w + ' ']}'"
                             for w, m in zip(written[0][1], mods) if w + " " in voc.retired_words]
                    if any([t for _, t in o["state"]] != [t for _, t in ops[0]["state"]] for o in ops[1:]):
                        continue
                    if "internal" in mods and (len(ops) > 1 or "internal" not in ops[0]):
                        continue
                    ctx = Ctx(voc, "rule")
                    rp, _ = state_paths(len(ops[0]["state"]), 0)
                    roles = {}
                    for (r, t), p in zip(ops[0]["state"], rp):
                        for ph in voc.role_phrases(r):
                            ctx.actor_path[ph], ctx.actor_type[ph], ctx.actor_role[ph] = p, t, r
                            roles[ph] = ("actor", t, r)
                    ip = input_paths(len(ops))
                    in_types, clash = [], False
                    for k, o in enumerate(ops):
                        in_types.append(voc.pts[o["input"][0][1]]["lean"] if o["input"] else "Unit")
                        for r, t in o["input"]:
                            for ph in voc.role_phrases(r):
                                if ph in roles:
                                    clash = True
                                roles[ph] = ("value", t, r)
                                ctx.input_path[ph] = ip[k]
                    if clash:
                        continue              # two operations of a sequence give the same role name: which is meant?
                    base = ops[0]["lean"]
                    for o in ops[1:]:
                        base = self.scoped("and_then", op=base, op2=o["lean"])
                    ctx.opbase = base
                    base_any = ANY_RUN.format(base=base)
                    op, used = base, [o["id"] for o in ops] + (["and_then"] if len(ops) > 1 else [])
                    op_any = base_any                 # every scoping modifier below is applied to both
                    conds, cond_trees = [], []
                    if "internal" in mods:
                        i = ops[0]["internal"]
                        op = self.scoped("internal", op=op, member=i["member"], parties=i["parties"])
                        op_any = self.scoped("internal", op=op_any, member=i["member"], parties=i["parties"])
                        used.append("internal")
                        conds.append({"lean": None, "echo": i["echo"]})       # the operation's own line: what its parties and members are called
                    if cond_text is not None:
                        t = parse_step(voc, "cond", "", cond_text, 0, "", domain, "rule", roles, {})
                        if isinstance(t, Problem):
                            out.append(t)
                            continue
                        op = self.scoped("given", op=op, c=render(t, ctx))
                        op_any = self.scoped("given", op=op_any, c=render(t, ctx))
                        used.append("given")
                        conds.append({"lean": render(t, ctx), "echo": say(t, ctx)})
                        cond_trees.append(t)
                    call_mods = [m for m in mods if m != "internal"]
                    used += call_mods
                    st_type = " × ".join(voc.actors[t]["lean"] for _, t in ops[0]["state"])
                    in_type = in_types[0]
                    for t in in_types[1:]:
                        in_type = f"({in_type}) × {t}"
                    out.append({"ops": ops, "ctx": ctx, "roles": roles, "op": op, "base": base, "mods": call_mods, "conds": conds,
                                "written": written, "retired": gone, "mod_words": [w for w, m in zip(written[0][1], mods) if m != "internal"],
                                "op_any": op_any, "base_any": base_any,
                                "cond_trees": cond_trees, "used": used, "state_type": st_type, "input_type": in_type,
                                "key": "+".join(o["id"] for o in ops) + ("/" + ",".join(mods) if mods else "")
                                       + ("/given " + describe(cond_trees[0]) if cond_trees else "")})
        return out

    def echo_rule(self, rd, clauses):
        """The slot-structured English of a Rule line. WHICH CALLS each clause is about (the `covers` slot, the answer
        requirement, the sequence note, the two-call note, the defaults D1 / D2 / D10) is read off each claim's Calls value, the one its
        emitted operation carries (`Claim.calls`), through the `coverage:` entries of the book. It is NOT read off the
        words of the subject: "for a lookup, if it is accepted, ..." narrows the claim and leaves the subject bare
        (plan node Q2; readability critique 2.2)."""
        voc, cov = self.voc, self.voc.covers
        o, ds, weak = [], [], []
        for k, g in enumerate(clauses):
            ops = g["ops"]
            what = (voc.sequences[0] if voc.sequences else " followed by ").join(an(x["nouns"][0], voc.live_articles) + x["nouns"][0] for x in ops)
            who = [f"every {r}" for r, _ in ops[0]["state"]] + [typed(voc, f"every {r}", t) for x in ops for r, t in x["input"]]
            tag = f"clause {k + 1}: " if len(clauses) > 1 else ""
            o.append(("applies to" if k == 0 else "", f"{tag}{what}: {', '.join(who)}"))
            kinds = list(dict.fromkeys(c.calls for c in g["claims"]))      # the Calls values of this clause, in order
            mixed = len(kinds) > 1
            o.append(("covers", "; ".join(cov[x]["covers"] for x in kinds)))
            weak += [x for x in kinds if x != "every" and x not in weak]
            o.append(("assuming", "; ".join(c["echo"] for c in g["conds"]) or "nothing: every state and every input"))
            first = True
            if "every" in kinds:
                o.append(("then", cov["every"]["answer"]))
                first = False
            for c in g["claims"]:
                if c.frame["id"] == "always_answers" and c.calls == "every":
                    o[-1] = ("then", cov["every"]["answer_asked"].replace("{words}", c.node.form or "always answers"))      # the words as the book has them
                    continue
                o.append(("then" if first else "", (cov[c.calls]["prefix"] if mixed else "") + c.echo))
                first = False
            if len(ops) > 1:          # what a sequence must do to be covered depends on the Calls value: one note per value
                for x in kinds:
                    o.append(("", cov[x]["sequence"]))
            for x in dict.fromkeys(c.calls for c in g["claims"] if c.runs == 2):
                o.append(("", cov[x]["two_calls"]))
            if speaks_of_acceptance(g["claims"]) and ("accepted", ops[-1]["accepted_echo"]) not in o:
                o.append(("accepted", ops[-1]["accepted_echo"]))        # once per operation, at the first clause that needs it
            if "every" in kinds:
                ds += [d for d in ("D1", "D2") if d not in ds]
            ds += [d for d in reading_rules(g["cond_trees"] + [c.node for c in g["claims"] if c.node], bool(g["cond_trees"]) or g["internal"])
                   if d not in ds]
            for c in g["claims"]:
                # a default a frame names is printed unless this claim's narrowing removes it (D10 says both calls must
                # answer: true of a claim about every call, false of a narrowed one)
                ds += [d for d in c.frame.get("defaults", []) if d not in ds and d not in cov[c.calls].get("removes", [])]
                for n in walk(c.node):
                    if isinstance(n, Node) and n is not c.node:      # the pieces in its holes (the frame's own are above)
                        ds += [d for d in n.piece.get("defaults", []) if d not in ds]
        ds += ["D4"] if "D4" not in ds else []
        rd.defaults = sorted(ds, key=lambda d: int(d[1:]))
        for k, d in enumerate(rd.defaults):
            o.append(("defaults" if k == 0 else "", f"{d} {voc.default(d)}"))
        for x in weak:
            o.append(("not default", cov[x]["weakening"]))
        rd.coverage = [c.calls for c in rd.claims]
        for x in dict.fromkeys(rd.coverage):               # the reading prints these entries: it rests on them
            if cov[x]["id"] not in rd.used:
                rd.used.append(cov[x]["id"])
        rd.echo = o


def reading_rules(trees, has_cond: bool) -> list:
    """The reading rules that were APPLIED to these trees and are not tied to one piece: D5 (collection words bind
    inside their clause), D8 (conditions are judged before the call), D9 (negation binds to its one condition)."""
    ds = []
    nodes = [n for n in walk(trees) if isinstance(n, Node)]
    if any(base_cat(n.cat) in ("coll", "acoll") for n in nodes):
        ds.append("D5")
    if has_cond or any(n.id in ("if_then", "only_if", "exactly_when") for n in nodes):
        ds.append("D8")
    if any(n.id in ("every", "every_of") and isinstance(n.args.get("p"), Node) and n.args["p"].id == "not" for n in nodes):
        ds.append("D9")
    return ds


def speaks_of_acceptance(claims) -> bool:
    """Does a reading use the operation's notion of an accepted answer (successful / rejected / accepted)?"""
    return any(c.mods or c.frame["id"] == "rejected_unchanged"
               or any(isinstance(n, Node) and n.id == "accepted" for n in walk(c.node)) for c in claims)


def typed(voc, name: str, typ: str) -> str:
    e = voc.raw["type_echo"].get(typ)
    return f"{name} ({e})" if e else name


def rank_problem(p: Problem) -> int:
    if p.code == TWICE:        # the words were read and the sentence refused for what it asks: more telling than "no composition"
        return -2
    if p.code == RETIRED:      # ... and so is "this is how it was written before the form was replaced"
        return -1
    return {"ILL-TYPED": 0, "AMBIGUOUS": 1, "UNBOUND": 2}.get(p.status, 3)


def fill_op(o: dict, b: dict, ctx: Ctx) -> str:
    out = o["echo"]
    for r, leaf in b.items():
        out = out.replace("{" + r + "}", leaf.text)       # as written: the operation's own echo names the role
    return out


def splits(text: str, seps) -> list:
    """Every way of cutting a text at the separators `seps` (", and " between the clauses of a rule line, " and " between
    the claims of one clause: the `g.clauses` and `g.claims` forms of the book), fewest cuts first."""
    cuts = sorted((m.start(), len(sep)) for sep in seps for m in re.finditer(re.escape(sep), text))
    out = []
    for mask in range(1 << len(cuts)):
        parts, pos, ok = [], 0, True
        for k, (c, n) in enumerate(cuts):
            if mask >> k & 1:
                if c < pos:
                    ok = False
                    break
                parts.append(text[pos:c])
                pos = c + n
        if ok:
            parts.append(text[pos:])
            out.append(parts)
    return sorted(out, key=len)


def follow_splits(text: str, seps) -> list:
    """A subject as the operations of a sequence: cut at every separator of `and_then` ("<operation> followed by <operation>")."""
    parts = [text]
    for sep in seps:
        parts = [x for p in parts for x in p.split(sep)]
    return [parts]


# --------------------------------------------------------------------------- the generated Lean module

HEADER = "-- GENERATED by clausal from features/ + the Clausebook (clausebook/). Do not edit; overwritten on every run.\n"


def readings_file(voc: Vocabulary, readings) -> str:
    out = [HEADER + "-- The COMPILED READING of every scenario and of every `Rule:` line: one Lean statement each, built from\n"
           "-- the pieces of the Clausebook (domain words, modifiers, frames of lean/Frames). The sentence is in the\n"
           "-- comment above each; the slot-structured English echo is in out/report.md.\n"
           + "".join(f"import {i}\n" for i in voc.raw["lean_imports"])
           + "open Aeneas Aeneas.Std Result\nset_option linter.unusedVariables false\n"]
    for rd in readings:
        doc = f"/-- {rd.source}\n" + "\n".join("    " + l for l in rd.text.splitlines()) + " -/"
        out.append(doc + "\n" + rd.lean_def() + "\n")
    return "\n".join(out)
