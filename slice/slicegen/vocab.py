"""slicegen vocab: the COMPOSABLE vocabulary (plan nodes V2 and V3).

A sentence is not bound as a whole. It is assembled from typed pieces of three kinds (vocabulary.yaml):
domain words, modifiers, frames. This module

  * loads the vocabulary and turns every surface form into a small pattern with typed holes;
  * finds every way a step (or a `Rule:` line) can be built from those forms. Exactly one way: a reading.
    None: UNBOUND. None unless types are ignored: ILL-TYPED. Several: AMBIGUOUS. Always with file:line;
  * renders the one composition as (a) a Lean statement over the frame library (lean/Frames), (b) the
    pointwise form and the executable checker of each frame (the two readings that are compared), and
    (c) the slot-structured English echo, with every default that was applied.

Like the rest of slicegen it is UNTRUSTED: Lean type-checks what it writes, a generated kernel-checked
equivalence ties each reading to the flat statement the proofs are about (slicegen/links.py), and the echo
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

from .core import FeatureError, Problem, literal_problem, literal_regex

TYPES = ["num", "balances", "optnum", "acct", "transfer"]
HOLE = re.compile(r"\{(\w+)(?::([^}]+))?\}")
LAMBDA = {"measure": "fun st inp", "term": "fun st inp", "cond": "fun st inp", "class": "fun ans", "ameasure": "fun ans",
          "acoll": "fun st inp ans", "itempred": "fun st inp x", "coll": "fun st inp"}
CONSTANT_CATS = ("variation", "reference")     # domain words that are one Lean constant: no lambda is put around them
ARTICLES = ("a ", "an ", "every ", "any ")


def base_cat(cat: str) -> str:
    return cat.split("<", 1)[0]


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


# --------------------------------------------------------------------------- the vocabulary

@dataclass
class Form:
    owner: dict          # piece, idiom or operation
    text: str
    cat: str             # result category (T already replaced)
    segs: list           # [("lit", text) | ("hole", name, category)]
    neg: bool = False
    idiom: bool = False
    variant: str = ""
    voice: str = ""      # then | vp | "" (other categories)


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


class Vocabulary:
    def __init__(self, path: Path, rel: str, gloss):
        self.rel, self.text = rel, path.read_text()
        self.raw = yaml.safe_load(self.text)
        self.lines = self.text.splitlines()
        self.gloss = gloss                       # literal syntax and actor names only
        self.pts = {k: dict(v) for k, v in gloss.param_types.items()}
        for k, tmpl in (self.raw.get("literal_lean") or {}).items():
            self.pts[k]["lean_literal"] = tmpl
        self.actors = gloss.actors
        self.ops = {o["id"]: o for o in self.raw["operations"]}
        self.pieces = {p["id"]: p for p in self.raw["pieces"]}
        self.idioms = {i["id"]: i for i in self.raw.get("idioms", [])}
        for o in self.ops.values():
            o.setdefault("kind", "domain")
            o["cat"] = "op"
        for i in list(self.ops) + list(self.pieces) + list(self.idioms):
            if not isinstance(i, str) or i == "all":       # YAML reads `no`, `yes`, `on` as booleans; `all` is a keyword of `review`
                raise FeatureError(f"{rel}: `{i}` cannot be the id of a vocabulary entry (write another word, or quote it)")
        self.forms: dict = {}                    # (category, voice) -> [Form]
        for p in self.pieces.values():
            p.setdefault("domain", "shared")
            for key, voice, neg in (("forms", "", False), ("not_forms", "", True), ("then_forms", "then", False),
                                    ("vp_forms", "vp", False)):
                for f in p.get(key, []):
                    self._add(p, f, p["cat"], neg=neg, voice=voice)
            pa = p.get("per_actor")
            if pa:
                for f in pa["forms"]:
                    self._add(p, f, "per_actor", variant="per_actor")
            if "args" not in p:
                p["args"] = self._holes(p)
        for i in self.idioms.values():
            i.setdefault("kind", "idiom")
            self._add(i, i["form"], i["cat"], idiom=True, voice="then" if i["cat"] == "claim" else "")
        self._check()

    def line_of(self, id_: str) -> int:
        for n, l in enumerate(self.lines, 1):
            if re.match(rf"\s*-\s*\{{?\s*id:\s*{re.escape(id_)}\b", l):
                return n
        return 0

    def _holes(self, p) -> dict:
        for key in ("forms", "then_forms", "vp_forms", "not_forms"):
            for f in p.get(key, []):
                return {s[1]: s[2] for s in segments(f) if s[0] == "hole"}
        return {}

    def _add(self, owner, text, cat, neg=False, idiom=False, variant="", voice=""):
        variants = TYPES if re.search(r"<T>", text + cat) else [None]
        for t in variants:
            tx = text if t is None else text.replace("<T>", f"<{t}>")
            ct = cat if t is None else cat.replace("<T>", f"<{t}>")
            self.forms.setdefault((ct, voice), []).append(
                Form(owner, tx, ct, segments(tx), neg=neg, idiom=idiom, variant=variant, voice=voice))

    def _check(self):
        """Every hole names a known category; every idiom's meaning uses known pieces."""
        known = set(self.pts) | set(self.actors) | {"per_actor"}
        cats = {base_cat(c) for (c, _v) in self.forms} | {"claim", "cond"}
        for (c, _v), fs in self.forms.items():
            for f in fs:
                for s in f.segs:
                    if s[0] == "hole" and s[2] and s[2] not in known and base_cat(s[2]) not in cats:
                        raise FeatureError(f"{self.rel}:{self.line_of(f.owner['id'])}: `{f.owner['id']}`: hole "
                                           f"`{{{s[1]}:{s[2]}}}` names no category of the vocabulary")
        for i in self.idioms.values():
            for name in re.findall(r"([A-Za-z_][\w.]*)\(", i["means"]):
                if name not in self.pieces:
                    raise FeatureError(f"{self.rel}:{self.line_of(i['id'])}: idiom `{i['id']}` uses `{name}`, "
                                       "which is not a piece of the vocabulary")

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
                vals = self.parse(cat, chunk)
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
            if s[0] == "hole" and isinstance(binding[s[1]], Node) and binding[s[1]].cat != s[2] and not self.is_lexical(s[2]):
                notes.append(f"`{binding[s[1]].id}` is a {binding[s[1]].cat}, where `{f.owner['id']}` takes a {s[2]}")
            if s[0] == "hole" and isinstance(binding[s[1]], Leaf) and binding[s[1]].type != s[2]:
                notes.append(f"\"{binding[s[1]].text}\" is a {binding[s[1]].type}, where `{f.owner['id']}` takes a {s[2]}")
        if f.idiom:
            trees = [self._expr(e.strip(), binding, f) for e in f.owner["means"].split(";")]
            for t in trees:
                t.idiom, t.form = f.owner["id"], f.text
                t.notes += notes
            return [trees] if len(trees) > 1 else trees
        p = f.owner
        args = dict(binding)
        if p["id"] == "changes_only":
            args = {"c": binding["c"], "xs": [binding["x"], binding["y"]]}
        node = Node(p, args, f.cat, form=f.text, variant=f.variant, notes=notes)
        if f.neg:
            node = Node(self.voc.pieces["not"], {"p": node}, f.cat, form=f.text, neg=True, notes=[])
        return [node]

    def _expr(self, e: str, binding: dict, f: Form):
        """An idiom's meaning: `piece(arg, arg)`, `[a, b]`, or the name of a hole of the idiom's form."""
        e = e.strip()
        if e.startswith("["):
            return [self._expr(x, binding, f) for x in split_args(e[1:-1])]
        m = re.fullmatch(r"([A-Za-z_][\w.]*)\((.*)\)", e, re.S)
        if not m:
            if e not in binding:
                raise FeatureError(f"{self.voc.rel}: idiom `{f.owner['id']}`: `{e}` is not a hole of its form")
            return binding[e]
        p = self.voc.pieces[m.group(1)]
        vals = [self._expr(x, binding, f) for x in split_args(m.group(2))]
        if len(vals) != len(p["args"]):
            raise FeatureError(f"{self.voc.rel}: idiom `{f.owner['id']}`: `{p['id']}` takes {len(p['args'])} "
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
        """How a leaf is named in the echo. A transfer or a batch written as a parameter or a literal is introduced
        by its kind ("the transfer <t>"); a role ("the transfer") and everything else is shown as written."""
        if leaf.kind == "value" and leaf.how in ("param", "lit") and leaf.type in ("transfer", "batch"):
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
    return ("nearest forms of the vocabulary for a " + base_cat(cat) + ":\n" + "\n".join(f"  - {p}" for p in near)
            + "\na new sentence needs no new entry if it can be said with existing forms; otherwise add a piece (or an idiom) to vocabulary.yaml")


def parse_step(voc, cat, voice, text, line, where, domain, mode, roles, ptypes):
    """One tree (or list of trees) for a step, or a Problem."""
    hits = Parser(voc, domain, mode, roles, ptypes).parse(cat, text, voice)
    if len(hits) == 1:
        fix_types(hits[0], voc)
        return hits[0]
    if len(hits) > 1:
        ways = "; ".join(sorted({describe(h) for h in hits}))
        return problem("AMBIGUOUS", line, f"{where}: \"{text}\" can be built from the vocabulary in {len(hits)} ways: {ways}")
    loose = Parser(voc, domain, mode, roles, ptypes, relaxed=True).parse(cat, text, voice)
    if loose:
        notes = [n for h in loose[:1] for x in walk(h) if isinstance(x, Node) for n in x.notes]
        return problem("ILL-TYPED", line, f"{where}: \"{text}\" fits a form of the vocabulary only if types are ignored: "
                       + ("; ".join(dict.fromkeys(notes)) or "a value of the wrong type fills a hole"))
    return problem("UNBOUND", line, f"{where}: no composition of vocabulary pieces reads \"{text}\" as a {base_cat(cat)}",
                   nearest(voc, cat, voice, domain, text))


def describe(t) -> str:
    if isinstance(t, list):
        return " + ".join(describe(x) for x in t)
    if isinstance(t, Leaf):
        return t.text
    return t.id + ("(" + ", ".join(describe(a) for a in t.args.values()) + ")" if t.args else "")


def op_roles(op: dict) -> dict:
    """Rule mode: the phrase each role of an operation goes by."""
    out = {}
    for r, t in op["state"]:
        out["the " + r] = ("actor", t, r)
    for r, t in op["input"]:
        out["the " + r] = ("value", t, r)
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


class Compiler:
    def __init__(self, voc: Vocabulary):
        self.voc = voc

    # ---- shared by scenarios and rules
    def claims_of(self, trees, ctx, op_text, step, clause=0, mods=()):
        """Then-trees -> Claims. A class standing alone is `always`; under "not" it is `never`."""
        out = []
        for t in (trees if isinstance(trees, list) else [trees]):
            node, m = t, list(mods)
            while isinstance(node, Node) and node.id in ("rejected", "successful") and node.cat == "claim":
                m.append(node.id)
                node = node.args["c"]
            if isinstance(node, list):
                out += self.claims_of(node, ctx, op_text, step, clause, m)
                continue
            if node.id == "always" and node.args["c"].id == "not":
                node = Node(self.voc.pieces["never"], {"c": node.args["c"].args["p"]}, "claim", form=node.form, idiom=node.idiom)
            out.append(self.claim(node, ctx, op_text, m, step, clause))
        return out

    def claim(self, node, ctx, op_text, mods, step, clause=0, default=""):
        f = node.piece
        op = op_text
        for m in mods:
            op = self.voc.pieces[m]["lean"].replace("{op}", op)
        return Claim(f, node, list(mods), op, frame_text(f["lean"], node, ctx, op), frame_text(f["at"], node, ctx, op),
                     frame_text(f["check"], node, ctx, op), say(node, ctx), step, default, clause)

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
                return problem("UNBOUND", w.line, f"{where}:{w.line}: no operation of the vocabulary is named by \"{w.text}\"",
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
        for s in steps:
            if s.kind == "when":
                continue
            cat, voice = ("cond", "") if s.kind == "given" else ("claim", "then")
            text, mods = s.text, []
            if s.kind == "then":
                for pre, m in (("if it is rejected, ", "rejected"), ("if it is accepted, ", "successful")):
                    if text.startswith(pre):
                        text, mods = text[len(pre):], [m]
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
                bad = self.answer_check(t, ops, s.line, f"{where}:{s.line}") or self.op_check(t, ops, s.line, f"{where}:{s.line}")
                if bad:
                    return bad
            (givens if s.kind == "given" else thens).append((s, t, mods))
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
        # the operation
        base = ops[0]["lean"]
        for o in ops[1:]:
            base = f"({base}).andThen {o['lean']}"
        st_type = " × ".join(voc.actors[t]["lean"] for _, t in st_roles)
        for a in bys:
            base = f"({base}).beside {voc.actors[ctx.actor_type[a]]['lean']}"
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
        rd.op = base if not rd.conds else f"({base}).given (fun st inp => " + " ∧ ".join(c["lean"] for c in rd.conds) + ")"
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
        what = " followed by ".join(fill_op(o, b, ctx) for o, b in zip(ops, binds))
        filt = sorted({m for c in rd.claims for m in c.mods})
        every = [c for c in rd.claims if not c.mods]
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
        o.append(("", "every such call, accepted or rejected [default D2]" if every else "see each line of `then`"))
        o.append(("assuming", "; ".join(c["echo"] for c in rd.conds) or "nothing: every state and every input"))
        first = True
        if every:
            o.append(("then", "the call gives an answer [default D1]"))
            first = False
        for c in rd.claims:
            if c.default:
                continue
            pre = ""
            if c.frame["id"] == "always_answers" and not c.mods and every:
                o[-1] = ("then", "the call gives an answer [default D1; also asked for by 'it answers']")
                continue
            if "rejected" in c.mods:
                pre = "if the call is rejected: "
            elif "successful" in c.mods:
                pre = "if the call is accepted: "
            o.append(("then" if first else "", pre + c.echo))
            first = False
        if len(ops) > 1:
            o.append(("", "(of a sequence: every call in it must answer; the answer spoken of is the LAST call's; earlier answers are otherwise unconstrained)"))
        if speaks_of_acceptance(rd.claims):
            o.append(("accepted", ops[-1]["accepted_echo"]))
        ds = ["D1", "D2", "D4"] if every else ["D1", "D4"]
        for c in rd.claims:
            for d in c.frame.get("defaults", []):
                if d not in ds:
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
            o.append(("defaults" if k == 0 else "", f"{d} {voc.raw['defaults'][d]}"))
        for m in filt:
            o.append(("not default", voc.raw["weakenings"][m]))
        rd.echo = o

    # ---- a Rule line
    def rule(self, rule, domain_hint=None) -> Reading | Problem:
        voc = self.voc
        where = f"{rule.feature.path}:{rule.line}"
        text = rule.name.strip().rstrip(".")
        text = text[0].lower() + text[1:]
        rd = Reading(rule.id, "rule", where, f"Rule: {rule.name}")
        domains = [domain_hint] if domain_hint else sorted({o["domain"] for o in voc.ops.values()})
        results, problems = [], []
        for d in domains:
            for split in clause_splits(text):
                got = [self.clause(c, d, where, rule.line) for c in split]
                if all(not isinstance(g, Problem) for g in got):
                    results.append((d, got))
                else:
                    problems.append(next(g for g in got if isinstance(g, Problem)))
        if not results:
            rank = {"ILL-TYPED": 0, "AMBIGUOUS": 1, "UNBOUND": 2}
            problems.sort(key=lambda p: (rank.get(p.status, 3), -len(p.message)))
            return problems[0] if problems else problem("UNBOUND", rule.line, f"{where}: the rule line is empty")
        uniq = {}
        for d, got in results:
            uniq.setdefault((d, tuple(g["key"] for g in got)), (d, got))
        if len(uniq) > 1:
            return problem("AMBIGUOUS", rule.line, f"{where}: the rule line can be built from the vocabulary in {len(uniq)} ways: "
                           + "; ".join(sorted(f"[{d}] " + " | ".join(k) for d, k in uniq)))
        d, got = next(iter(uniq.values()))
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
        return rd

    def clause(self, text: str, domain: str, where: str, line: int):
        """One clause of a rule line:  <subject> <vp> [and <vp>]   or   for <subject>, <claim> [and <claim>]."""
        voc = self.voc
        best = None
        hits = []
        m = re.fullmatch(r"for (.+?), (.+)", text)
        shapes = []
        if m:
            for cut in [x.start() for x in re.finditer(", ", text)]:
                shapes.append((text[4:cut], text[cut + 2:], "then"))
        else:
            words = [x.start() for x in re.finditer(" ", text)]
            for cut in words:
                shapes.append((text[:cut], text[cut + 1:], "vp"))
        for subj, rest, voice in shapes:
            for s in self.subjects(subj, domain):
                if isinstance(s, Problem):
                    continue
                ctx, ops = s["ctx"], s["ops"]
                roles = s["roles"]
                parts_list = and_splits(rest)
                for parts in parts_list:
                    trees, bad = [], None
                    for part in parts:
                        t = self.rule_part(part, voice, domain, roles, where, line, ops)
                        if isinstance(t, Problem):
                            bad = t
                            break
                        trees.append(t)
                    if bad:
                        if best is None or rank_problem(bad) < rank_problem(best):
                            best = bad
                        continue
                    op_text = s["op"]
                    claims = []
                    for t in trees:
                        claims += self.claims_of(t, ctx, op_text, -1, mods=s["mods"])
                    rd = Reading("", "rule", where, text)
                    self.used(rd, s["cond_trees"], trees, extra=s["used"] + [c.frame["id"] for c in claims])
                    hits.append({"subject": subj, "ops": ops, "ctx": ctx, "claims": claims, "op": op_text, "base": s["base"],
                                 "cond_trees": s["cond_trees"], "internal": "internal" in s["used"],
                                 "mods": s["mods"], "conds": s["conds"], "state_type": s["state_type"], "input_type": s["input_type"],
                                 "used": rd.used, "regular": rd.regular, "text": text,
                                 "key": s["key"] + " :: " + " & ".join(describe(t) for t in trees)})
        uniq = {h["key"]: h for h in hits}
        if len(uniq) == 1:
            return next(iter(uniq.values()))
        if len(uniq) > 1:
            return problem("AMBIGUOUS", line, f"{where}: \"{text}\" can be built from the vocabulary in {len(uniq)} ways: " + "; ".join(sorted(uniq)))
        return best or problem("UNBOUND", line, f"{where}: no composition of vocabulary pieces reads \"{text}\" as a rule clause "
                               "(<a / an> [successful | rejected | internal] <operation> [followed by <operation>] [for which <condition>] <what it does>, "
                               "or: for <such an operation>, <what a Then would say>)",
                               "operations of the vocabulary: " + ", ".join(sorted({n for o in voc.ops.values() if o['domain'] == domain for n in o['nouns']})))

    def rule_part(self, part, voice, domain, roles, where, line, ops):
        voc = self.voc
        if voice == "vp":
            for words, fid, neg in (("is always accepted", "always", False), ("always succeeds", "always", False),
                                    ("is never accepted", "never", False), ("is always rejected", "never", False)):
                if part == words:
                    return Node(voc.pieces[fid], {"c": Node(voc.pieces["accepted"], {}, "class")}, "claim", form=words)
        text, mods = part, []
        if voice == "then":
            for pre, m in (("if it is rejected, ", "rejected"), ("if it is accepted, ", "successful")):
                if text.startswith(pre):
                    text, mods = text[len(pre):], [m]
        t = parse_step(voc, "claim", voice, text, line, where, domain, "rule", roles, {})
        if isinstance(t, Problem):
            return t
        for n in walk(t):          # "is accepted whenever / only if / exactly when", "never loses acceptance": the class is the operation's own
            if isinstance(n, Node) and n.id in ("if_then", "only_if", "exactly_when", "monotone") and "c" not in n.args:
                n.args["c"] = Node(voc.pieces["accepted"], {}, "class")
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
        for m in re.finditer(r" for which ", text):
            heads.append((text[:m.start()], text[m.end():]))
        for head, cond_text in heads:
            for names in follow_splits(head):
                seqs = [[]]
                for k, nm in enumerate(names):
                    art = next((a for a in ARTICLES if nm.startswith(a)), None)
                    if art is None:
                        seqs = []
                        break
                    rest = nm[len(art):]
                    mods = []
                    for adj, m in (("successful ", "successful"), ("rejected ", "rejected"), ("internal ", "internal")):
                        if rest.startswith(adj):
                            rest, mods = rest[len(adj):], [m]
                    cands = [o for o in voc.ops.values() if o["domain"] == domain and rest in o["nouns"]]
                    if k > 0 and mods:
                        cands = []            # a modifier is written on the whole sequence, i.e. on its first noun
                    seqs = [s + [(o, mods)] for s in seqs for o in cands]
                for seq in seqs:
                    ops = [o for o, _ in seq]
                    mods = seq[0][1]
                    if any([t for _, t in o["state"]] != [t for _, t in ops[0]["state"]] for o in ops[1:]):
                        continue
                    if "internal" in mods and (len(ops) > 1 or "internal" not in ops[0]):
                        continue
                    ctx = Ctx(voc, "rule")
                    rp, _ = state_paths(len(ops[0]["state"]), 0)
                    roles = {}
                    for (r, t), p in zip(ops[0]["state"], rp):
                        ctx.actor_path["the " + r], ctx.actor_type["the " + r], ctx.actor_role["the " + r] = p, t, r
                        roles["the " + r] = ("actor", t, r)
                    ip = input_paths(len(ops))
                    in_types, clash = [], False
                    for k, o in enumerate(ops):
                        in_types.append(voc.pts[o["input"][0][1]]["lean"] if o["input"] else "Unit")
                        for r, t in o["input"]:
                            if "the " + r in roles:
                                clash = True
                            roles["the " + r] = ("value", t, r)
                            ctx.input_path["the " + r] = ip[k]
                    if clash:
                        continue              # two operations of a sequence give the same role name: which is meant?
                    base = ops[0]["lean"]
                    for o in ops[1:]:
                        base = f"({base}).andThen {o['lean']}"
                    ctx.opbase = base
                    op, used = base, [o["id"] for o in ops] + (["and_then"] if len(ops) > 1 else [])
                    conds, cond_trees = [], []
                    if "internal" in mods:
                        i = ops[0]["internal"]
                        op = f"({op}).internal {i['member']} {i['parties']}"
                        used.append("internal")
                        conds.append({"lean": None, "echo": f"every account the {ops[0]['input'][0][0]} names is an account of the {ops[0]['state'][0][0]} (internal)"})
                    if cond_text is not None:
                        t = parse_step(voc, "cond", "", cond_text, 0, "", domain, "rule", roles, {})
                        if isinstance(t, Problem):
                            out.append(t)
                            continue
                        op = f"({op}).given (fun st inp => {render(t, ctx)})"
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
                                "cond_trees": cond_trees, "used": used, "state_type": st_type, "input_type": in_type,
                                "key": "+".join(o["id"] for o in ops) + ("/" + ",".join(mods) if mods else "")
                                       + ("/given " + describe(cond_trees[0]) if cond_trees else "")})
        return out

    def echo_rule(self, rd, clauses):
        voc = self.voc
        o, ds, weak = [], [], []
        for k, g in enumerate(clauses):
            ops = g["ops"]
            what = " followed by ".join("a " + x["nouns"][0] for x in ops)
            who = [f"every {r}" for r, _ in ops[0]["state"]] + [typed(voc, f"every {r}", t) for x in ops for r, t in x["input"]]
            tag = f"clause {k + 1}: " if len(clauses) > 1 else ""
            o.append(("applies to" if k == 0 else "", f"{tag}{what}: {', '.join(who)}"))
            if g["mods"]:
                o.append(("", f"{'ONLY ' + g['mods'][0] + ' calls [asked for]' }"))
                weak += [m for m in g["mods"] if m not in weak]
            else:
                o.append(("", "every such call, accepted or rejected [default D2]"))
            o.append(("assuming", "; ".join(c["echo"] for c in g["conds"]) or "nothing: every state and every input"))
            first = True
            if not g["mods"]:
                o.append(("then", "the call gives an answer [default D1]"))
                first = False
            for c in g["claims"]:
                pre = ""
                if c.frame["id"] == "always_answers" and not c.mods and not g["mods"]:
                    o[-1] = ("then", "the call gives an answer [default D1; also asked for by 'always answers']")
                    continue
                if "rejected" in c.mods and "rejected" not in g["mods"]:
                    pre = "if the call is rejected: "
                    weak += ["rejected"] if "rejected" not in weak else []
                if "successful" in c.mods and "successful" not in g["mods"]:
                    pre = "if the call is accepted: "
                    weak += ["successful"] if "successful" not in weak else []
                o.append(("then" if first else "", pre + c.echo))
                first = False
            if len(ops) > 1:
                o.append(("", "(of a sequence: every call in it must answer; the answer spoken of is the LAST call's)"))
            if any(c.runs == 2 for c in g["claims"]):
                o.append(("", "(TWO calls are compared: every pair of calls of the operation related as stated; both must be in scope "
                              "and both must give an answer [default D10])"))
            if speaks_of_acceptance(g["claims"]) and ("accepted", ops[-1]["accepted_echo"]) not in o:
                o.append(("accepted", ops[-1]["accepted_echo"]))        # once per operation, at the first clause that needs it
            if not g["mods"]:
                ds += [d for d in ("D1", "D2") if d not in ds]
            ds += [d for d in reading_rules(g["cond_trees"] + [c.node for c in g["claims"] if c.node], bool(g["cond_trees"]) or g["internal"])
                   if d not in ds]
            for c in g["claims"]:
                ds += [d for d in c.frame.get("defaults", []) if d not in ds]
                for n in walk(c.node):
                    if isinstance(n, Node):
                        ds += [d for d in n.piece.get("defaults", []) if d not in ds]
        ds += ["D4"] if "D4" not in ds else []
        rd.defaults = sorted(ds, key=lambda d: int(d[1:]))
        for k, d in enumerate(rd.defaults):
            o.append(("defaults" if k == 0 else "", f"{d} {voc.raw['defaults'][d]}"))
        for m in weak:
            o.append(("not default", voc.raw["weakenings"][m]))
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
    e = (voc.raw.get("type_echo") or {}).get(typ)
    return f"{name} ({e})" if e else name


def rank_problem(p: Problem) -> int:
    return {"ILL-TYPED": 0, "AMBIGUOUS": 1, "UNBOUND": 2}.get(p.status, 3)


def fill_op(o: dict, b: dict, ctx: Ctx) -> str:
    out = o["echo"]
    for r, leaf in b.items():
        out = out.replace("{" + r + "}", leaf.text)       # as written: the operation's own echo names the role
    return out


def clause_splits(text: str) -> list:
    """Every way of cutting a rule line into clauses at ', and '."""
    cuts = [m.start() for m in re.finditer(", and ", text)]
    out = []
    for mask in range(1 << len(cuts)):
        parts, pos = [], 0
        for k, c in enumerate(cuts):
            if mask >> k & 1:
                parts.append(text[pos:c])
                pos = c + len(", and ")
        parts.append(text[pos:])
        out.append(parts)
    return sorted(out, key=len)


def and_splits(text: str) -> list:
    cuts = [m.start() for m in re.finditer(" and ", text)]
    out = []
    for mask in range(1 << len(cuts)):
        parts, pos = [], 0
        for k, c in enumerate(cuts):
            if mask >> k & 1:
                parts.append(text[pos:c])
                pos = c + len(" and ")
        parts.append(text[pos:])
        out.append(parts)
    return sorted(out, key=len)


def follow_splits(text: str) -> list:
    parts = text.split(" followed by ")
    return [parts]


# --------------------------------------------------------------------------- the generated Lean module

HEADER = "-- GENERATED by slicegen from features/ + vocabulary.yaml. Do not edit; overwritten on every run.\n"


def readings_file(voc: Vocabulary, readings) -> str:
    out = [HEADER + "-- The COMPILED READING of every scenario and of every `Rule:` line: one Lean statement each, built from\n"
           "-- the pieces of the vocabulary (domain words, modifiers, frames of lean/Frames). The sentence is in the\n"
           "-- comment above each; the slot-structured English echo is in out/report.md.\n"
           + "".join(f"import {i}\n" for i in voc.raw["lean_imports"])
           + "open Aeneas Aeneas.Std Result\nset_option linter.unusedVariables false\n"]
    for rd in readings:
        doc = f"/-- {rd.source}\n" + "\n".join("    " + l for l in rd.text.splitlines()) + " -/"
        out.append(doc + "\n" + rd.lean_def() + "\n")
    return "\n".join(out)
