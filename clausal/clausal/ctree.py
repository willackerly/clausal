"""clausal tree: the PARSE TREE OF A RULE LINE AS JSON, and its JSON SCHEMA GENERATED FROM THE BOOK (plan node L1e).

    python3 -m clausal tree "<rule sentence>" [--domain D]        the tree of a sentence that compiles, as JSON
    python3 -m clausal tree --from FILE.json                      the sentence a tree spells, compiled; exit 1 if it is refused
    python3 -m clausal tree --schema [--out FILE]                 the JSON schema of every tree the book's forms can spell
    python3 -m clausal tree --check                               the round trip on every Rule line of features/ and controls/ that compiles

This is the interface a proposer (a person's tool, later a language model: plan node L1f) uses to hand the composer a
reading WITHOUT WRITING TEXT. A tree names pieces of the book by id and the roles of the operation by their phrase; the
sentence is written from it by the compiler's own writer (`vocab.Compiler.canonical` and `surface`, the live form of
each piece), and it counts only if the ordinary compiler then reads that sentence as THE SAME TREE. Nothing here adds a
form, and nothing here is trusted: `sentence` compiles what it wrote and refuses unless the composition found is the
tree it was given.

THE FORMAT (`clausal-tree-v1`)

    { "schema": "clausal-tree-v1", "system": "ledger",
      "clauses": [ { "subject": { "operations": ["l.apply"],          operation ids, one or two (a sequence)
                                  "narrowing": null | "successful" | "rejected",
                                  "internal": false,
                                  "tie": null | NODE,                 how the second call's input is got from the first's
                                  "condition": null | NODE },         "for which <condition>"
                     "claims": [ NODE, ... ] } ] }                    one or more frames said of the subject

    NODE  { "piece": "<id>", "args": { "<hole>": NODE | LEAF | [NODE | LEAF, ...] } }
          { "idiom": "<id>", "args": { "<hole of the idiom's form>": NODE | LEAF } }
    LEAF  { "role": "the sender" }                                    a role of the subject's operation(s)
          { "value": "30", "type": "amount" }                         a literal of a literal type of the glossary

A negated piece (a `not_forms` surface: "differs from", "it is rejected") is the piece `not` around it, as in the
compiler's own tree. A hole a form leaves unwritten (`implied:` of a frame: the class in "is always accepted") is in
`args` with the piece the book names. The piece ids, the holes of each, the roles of each operation and the literal
types are the book's; the schema (`schema`) lists them, per subject, so that a tree that names a piece the book does not
have, a role of another operation or a hole the piece does not take is rejected before anything is compiled.

WHAT THE SCHEMA DOES NOT SAY (the compile step stays): the refusals that are about a whole statement (a narrowed claim
that says nothing, Q1; a narrowing word on a tied sequence; a sentence that reads in two systems), type clashes between
two operations of a sequence, and whether the sentence written from the tree is read back as that tree.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

from . import vocab
from .core import Feature, FeatureError, Problem, Rule, literal_regex, load_glossary, parse_feature
from .pipeline import ROOT
from .vocab import Leaf, Node, base_cat, hole_voice

SCHEMA = "clausal-tree-v1"
NARROWINGS = ("successful", "rejected")          # the scoping pieces that narrow by the answer (`calls:` in the book)


class TreeError(Exception):
    """A tree that cannot be written as a sentence of the book, or is not read back as itself."""


# --------------------------------------------------------------------------------------------- the book, the compiler

def load():
    gl = load_glossary(ROOT / "glossary.yaml", "glossary.yaml")
    voc = vocab.load_project(ROOT, gl)
    return voc, vocab.Compiler(voc)


def compile_sentence(comp, sentence: str, hint=None):
    f = Feature(path="<tree>", name="tree", slug="tree")
    return comp.rule(Rule(feature=f, name=sentence, line=1, tags=["@id:tree"]), hint)


def term_sha(rd) -> str:
    """The digest clausebook/terms.lock.json records for a compiled sentence."""
    return hashlib.sha256(rd.lean_def().encode()).hexdigest()


def body(rd) -> str:
    """The Lean term of a reading without the name it is defined under (two sentences say the same iff these are equal)."""
    return rd.lean_def().split(":=", 1)[1].strip()


def body_sha(rd) -> str:
    return hashlib.sha256(body(rd).encode()).hexdigest()


def reading_key(rd) -> str:
    return " | ".join(c["key"] for c in rd.info["clauses"])


# --------------------------------------------------------------------------------------------- reading -> JSON

def node_json(x):
    if isinstance(x, list):
        if x and all(isinstance(y, Node) and y.idiom and y.said is x[0].said for y in x):     # an idiom that means several claims
            return {"idiom": x[0].idiom, "args": {k: node_json(v) for k, v in x[0].said.items()}}
        return [node_json(y) for y in x]
    if isinstance(x, Leaf):
        return {"role": x.text} if x.how == "role" else {"value": x.text, "type": x.type}
    if x.idiom:
        if x.said is None:
            raise TreeError(f"idiom `{x.idiom}`: the tree does not record what filled its holes")
        return {"idiom": x.idiom, "args": {k: node_json(v) for k, v in x.said.items()}}
    return {"piece": x.id, "args": {k: node_json(v) for k, v in x.args.items()}}


def of_reading(rd) -> dict:
    """The tree of a compiled Rule line (a `vocab.Reading` of `Compiler.rule`)."""
    clauses = []
    for g in rd.info["clauses"]:
        s = g["s"]
        narrow = [m for m in s["mods"] if m in NARROWINGS]
        clauses.append({"subject": {"operations": [o["id"] for o in g["ops"]],
                                    "narrowing": narrow[0] if narrow else None,
                                    "internal": "internal" in s["used"],
                                    "tie": node_json(s["tie"]) if s["tie"] is not None else None,
                                    "condition": node_json(s["cond_trees"][0]) if s["cond_trees"] else None},
                        "claims": [node_json(t) for t in g["trees"]]})
    return {"schema": SCHEMA, "system": rd.info["domain"], "clauses": clauses}


def describe(j) -> str:
    """`vocab.describe` of the tree a JSON node stands for (an idiom is written `idiom:<id>(...)`: its expansion is the
    compiler's, and is compared after compiling, not predicted)."""
    if isinstance(j, list):
        return " + ".join(describe(x) for x in j)
    if "role" in j:
        return j["role"]
    if "value" in j:
        return j["value"]
    args = ", ".join(describe(a) for a in j["args"].values())
    return (j.get("piece") or "idiom:" + j["idiom"]) + (f"({args})" if j["args"] else "")


def canon(tree: dict) -> str:
    return json.dumps(tree, sort_keys=True, ensure_ascii=False)


# --------------------------------------------------------------------------------------------- JSON -> Node

class Builder:
    """JSON nodes to the compiler's `Node`s, for one subject. Every node is built THROUGH A FORM OF THE BOOK for the
    category its hole wants, so a tree that puts a piece where no form of the book puts it cannot be built."""

    def __init__(self, voc, ops: list, tied: bool):
        self.voc, self.ops = voc, ops
        roles = {}
        for k, o in enumerate(ops):
            for ph, r in vocab.op_roles(o, voc).items():
                if r[0] == "value" and tied and k > 0:
                    continue                      # the tied call has no input of its own: no role of it is named
                roles[ph] = r
        self.roles = roles
        self.parser = vocab.Parser(voc, ops[0]["domain"], "rule", roles)

    def forms(self, cat: str, voice: str) -> list:
        return self.parser.forms_for(cat, voice)

    def build(self, j, cat: str, voice: str = ""):
        cat, hv = hole_voice(cat)
        voice = hv or voice
        if self.parser.is_lexical(cat):
            if not isinstance(j, dict) or not ({"role"} == set(j) or {"value", "type"} == set(j)):
                raise TreeError(f"a {cat} is a leaf ({{\"role\": ...}} or {{\"value\": ..., \"type\": ...}}), given {json.dumps(j)[:80]}")
            text = j.get("role", j.get("value"))
            leaf = self.parser.lexical(cat, text)
            if leaf is None or ("role" in j) != (leaf.how == "role") or ("type" in j and j["type"] != leaf.type):
                raise TreeError(f"\"{text}\" is not a {cat} of {' followed by '.join(o['id'] for o in self.ops)}"
                                + (f" (its roles: {', '.join(self.roles)})" if "role" in j else ""))
            return leaf
        if not isinstance(j, dict) or "args" not in j or not ("piece" in j) ^ ("idiom" in j):
            raise TreeError(f"a {cat} is a node ({{\"piece\" | \"idiom\": id, \"args\": {{...}}}}), given {json.dumps(j)[:80]}")
        errs = []
        if "idiom" in j:
            for f in self.forms(cat, voice):
                if f.idiom and f.owner["id"] == j["idiom"]:
                    try:
                        binding = self.holes(f, j["args"])
                    except TreeError as e:
                        errs.append(str(e))
                        continue
                    got = self.parser._build(f, binding, cat)
                    if got and not self.notes(got[0]):
                        return got[0]
            raise TreeError(errs[0] if errs else f"the book has no idiom `{j['idiom']}` that is a {cat}" + (f" ({voice} form)" if voice else ""))
        neg = j["piece"] == "not" and set(j["args"]) == {"p"} and isinstance(j["args"]["p"], dict) and "piece" in j["args"]["p"]
        inner = j["args"]["p"] if neg else j
        for f in self.forms(cat, voice):
            if f.idiom or f.owner["id"] != inner["piece"] or f.neg != neg:
                continue
            try:
                binding = self.holes(f, inner["args"])
            except TreeError as e:
                errs.append(str(e))
                continue
            got = self.parser._build(f, binding, cat)
            if got and not self.notes(got[0]):
                node = got[0]
                for hole, pid in self.implied(f, inner["args"]).items():        # what `Compiler.fill_implied` adds
                    (node.args["p"] if neg else node).args[hole] = Node(self.voc.pieces[pid], {}, self.voc.pieces[pid]["cat"])
                return node
        raise TreeError(errs[0] if errs else f"the book has no form of `{inner['piece']}`" + (" (negated)" if neg else "") + f" that is a {cat}"
                        + (f" ({voice} form)" if voice else ""))

    def notes(self, node) -> list:
        return [n for x in vocab.walk(node) if isinstance(x, Node) for n in x.notes]

    def implied(self, f, args: dict) -> dict:
        """{hole: piece id} for the holes of the frame the form does not write and the book fills (`implied:`)."""
        written = {s[1] for s in f.segs if s[0] == "hole"}
        return {h: p for h, p in (f.owner.get("implied") or {}).items() if h not in written and not f.idiom}

    def holes(self, f, args: dict) -> dict:
        """The binding of a form's holes from a node's `args`; raises unless `args` is exactly what the form takes."""
        segs = [s for s in f.segs if s[0] == "hole"]
        names = [s[1] for s in segs]
        imp = self.implied(f, args)
        want = set(names) | set(imp)
        given = dict(args)
        if f.owner["id"] == "changes_only" and not f.idiom and isinstance(given.get("xs"), list) and len(given["xs"]) == 2:
            given["x"], given["y"] = given.pop("xs")
        if set(given) != want:
            raise TreeError(f"`{f.owner['id']}` (\"{f.text}\") takes the holes {sorted(want)}, given {sorted(given)}")
        for h, pid in imp.items():
            a = given[h]
            if not (isinstance(a, dict) and a.get("piece") == pid and not a.get("args")):
                raise TreeError(f"`{f.owner['id']}` (\"{f.text}\") says `{pid}` with its own words; its hole `{h}` cannot be {describe(a)}")
        return {s[1]: self.build(given[s[1]], s[2]) for s in segs}


def subject_ops(voc, system: str, ids: list) -> list:
    ops = []
    for i in ids:
        o = voc.ops.get(i)
        if o is None or o["domain"] != system:
            raise TreeError(f"`{i}` is not an operation of the system `{system}`")
        ops.append(o)
    if not 1 <= len(ops) <= 2:
        raise TreeError("a subject names one operation, or two in sequence")
    return ops


def clause_text(voc, comp, system: str, c: dict) -> str:
    """One clause of a tree written the one way the book has (`Compiler.canonical`)."""
    sj = c["subject"]
    ops = subject_ops(voc, system, sj["operations"])
    b = Builder(voc, ops, sj.get("tie") is not None)
    mods = [sj["narrowing"]] if sj.get("narrowing") else []
    if any(m not in NARROWINGS for m in mods):
        raise TreeError(f"a subject is narrowed by one of {', '.join(NARROWINGS)}, given `{mods[0]}`")
    tie = b.build(sj["tie"], "tie") if sj.get("tie") is not None else None
    cond = b.build(sj["condition"], "cond") if sj.get("condition") is not None else None
    trees = []
    for j in c["claims"]:
        err = None
        for voice in ("vp", "then"):                 # a frame with a Rule voice is written in it (`canonical` sees to that)
            try:
                trees.append(b.build(j, "claim", voice))
                err = None
                break
            except TreeError as e:
                err = err or e
        if err:
            raise err
    s = {"written": [("", [], o["nouns"][0]) for o in ops], "mods": mods, "used": ["internal"] if sj.get("internal") else [],
         "tie": tie, "cond_trees": [cond] if cond is not None else []}
    text = comp.canonical({"trees": trees, "voice": "then", "s": s})
    if text is None:
        raise TreeError("the book has no live form to write a part of this clause with")
    return text


def sentence(tree: dict, voc=None, comp=None) -> dict:
    """{sentence, reading, compiles_as_written}: the sentence a tree spells, COMPILED, and read back as the same tree.
    Raises TreeError otherwise (the message is the compiler's refusal, or what differs)."""
    if voc is None:
        voc, comp = load()
    if not isinstance(tree, dict) or tree.get("schema") != SCHEMA:
        raise TreeError(f"not a `{SCHEMA}` tree")
    system = tree.get("system")
    if system not in {o["domain"] for o in voc.ops.values()}:
        raise TreeError(f"`{system}` is not a system of the book")
    if not tree.get("clauses"):
        raise TreeError("a tree has at least one clause")
    text = voc.clause_seps[0].join(clause_text(voc, comp, system, c) for c in tree["clauses"])
    text = text[0].upper() + text[1:]
    rd = compile_sentence(comp, text, None)
    as_written = not isinstance(rd, Problem)
    if not as_written:
        rd = compile_sentence(comp, text, system)        # a sentence two systems read: one statement only under scenarios of one
    if isinstance(rd, Problem):
        raise TreeError(f"the sentence the tree spells is refused: \"{text}\": {rd.status}"
                        + (f" [{rd.code}]" if rd.code != rd.status else "") + f": {rd.message}")
    back = of_reading(rd)
    if canon(back) != canon(tree):
        raise TreeError(f"the sentence the tree spells, \"{text}\", is read as ANOTHER tree: {reading_key(rd)}")
    return {"sentence": text, "reading": rd, "compiles_as_written": as_written}


# --------------------------------------------------------------------------------------------- the schema

def contexts(voc) -> list:
    """Every subject the book can write: [(key, [operations], tied?)]. One operation; two in sequence with the same
    state types and no role named by both; two in sequence with a tie (the second call has no input roles)."""
    out = []
    ops = list(voc.ops.values())
    for o in ops:
        out.append((o["id"], [o], False))
    for a in ops:
        for b in ops:
            if a["domain"] != b["domain"] or [t for _, t in a["state"]] != [t for _, t in b["state"]] or not voc.sequences:
                continue
            if a is not b and not {r for r, _ in a["input"]} & {r for r, _ in b["input"]}:
                out.append((f"{a['id']}+{b['id']}", [a, b], False))
            if voc.ties and len(a["input"]) == 1 and len(b["input"]) == 1 and a["input"][0][1] == b["input"][0][1]:
                out.append((f"{a['id']}+{b['id']}+tied", [a, b], True))
    return out


def allowed(owner: dict, ops: list) -> bool:
    """What `Compiler.answer_check` and `op_check` refuse is not in the schema."""
    if owner.get("answer") and owner["answer"] != ops[-1]["answer"]:
        return False
    if owner.get("for_op") and (len(ops) != 1 or ops[0]["id"] != owner["for_op"]):
        return False
    return True


def schema(voc=None) -> dict:
    """The JSON schema (draft 2020-12) of the trees the book's forms can spell, generated from the loaded books.
    `$defs` has one entry per subject and category: `<subject>|<category>[@<position>]`."""
    if voc is None:
        voc = load()[0]
    defs = {}
    clause_alts = []
    for key, ops, tied in contexts(voc):
        b = Builder(voc, ops, tied)
        domain = ops[0]["domain"]
        done, todo = {}, []

        def ref(cat, voice=""):
            cat, hv = hole_voice(cat)
            voice = hv or voice
            name = f"{key}|{cat}" + (f"@{voice}" if voice else "")
            if name not in done:
                done[name] = None
                todo.append((name, cat, voice))
            return name

        def node_alts(cat, voice):
            alts = []
            if b.parser.is_lexical(cat):
                roles = sorted(ph for ph, r in b.roles.items() if r[1] == cat)
                if roles:
                    alts.append({"type": "object", "properties": {"role": {"enum": roles}}, "required": ["role"], "additionalProperties": False})
                if cat in voc.pts:
                    pt = voc.pts[cat]
                    val = {"enum": list(pt["enum"])} if "enum" in pt else {"type": "string", "pattern": "^(?:" + literal_regex(voc.pts, cat) + ")$"}
                    alts.append({"type": "object", "properties": {"value": val, "type": {"const": cat}}, "required": ["value", "type"],
                                 "additionalProperties": False})
                return alts, []
            deps = []
            for f in b.forms(cat, voice):
                if not allowed(f.owner, ops):
                    continue
                props, need = {}, []
                holes = [s for s in f.segs if s[0] == "hole"]
                for s in holes:
                    props[s[1]] = {"$ref": "#/$defs/" + ref(s[2])}
                    deps.append(ref(s[2]))
                    need.append(s[1])
                if f.idiom:
                    alts.append(({"type": "object", "properties": {"idiom": {"const": f.owner["id"]},
                                  "args": {"type": "object", "properties": props, "required": need, "additionalProperties": False}},
                                  "required": ["idiom", "args"], "additionalProperties": False}, [ref(s[2]) for s in holes]))
                    continue
                if f.owner["id"] == "changes_only":
                    x, y = props.pop("x"), props.pop("y")
                    props["xs"] = {"type": "array", "prefixItems": [x, y], "minItems": 2, "maxItems": 2}
                    need = [n for n in need if n not in ("x", "y")] + ["xs"]
                for h, pid in b.implied(f, {}).items():
                    props[h] = {"type": "object", "properties": {"piece": {"const": pid}, "args": {"type": "object", "maxProperties": 0}},
                                "required": ["piece", "args"], "additionalProperties": False}
                    need.append(h)
                n = {"type": "object", "properties": {"piece": {"const": f.owner["id"]},
                     "args": {"type": "object", "properties": props, "required": need, "additionalProperties": False}},
                     "required": ["piece", "args"], "additionalProperties": False}
                if f.neg:
                    n = {"type": "object", "properties": {"piece": {"const": "not"},
                         "args": {"type": "object", "properties": {"p": n}, "required": ["p"], "additionalProperties": False}},
                         "required": ["piece", "args"], "additionalProperties": False}
                alts.append((n, [ref(s[2]) for s in holes]))
            return alts, deps

        raw = {}
        roots = [ref("claim", "vp"), ref("claim", "then"), ref("cond")] + ([ref("tie")] if tied else [])
        while todo:
            name, cat, voice = todo.pop()
            alts, _ = node_alts(cat, voice)
            raw[name] = alts
        # a category nothing of the book fills (for this subject) cannot be written: drop the forms that need one, to a fixpoint
        lexical = {n for n, a in raw.items() if a and not isinstance(a[0], tuple)}
        alive = set(lexical)
        changed = True
        while changed:
            changed = False
            for n, a in raw.items():
                if n not in alive and any(isinstance(x, tuple) and all(d in alive for d in x[1]) for x in a):
                    alive.add(n)
                    changed = True
        for n, a in raw.items():
            if n in lexical:
                defs[n] = {"anyOf": a}
            elif n in alive:
                defs[n] = {"anyOf": [x[0] for x in a if all(d in alive for d in x[1])]}
            elif n in roots:
                defs[n] = False                    # no tree: nothing of the book is a <category> for this subject
        claim = {"anyOf": [{"$ref": "#/$defs/" + r} for r in roots[:2] if defs[r] is not False]}
        opt = lambda r: {"anyOf": [{"type": "null"}] + ([{"$ref": "#/$defs/" + r}] if defs[r] is not False else [])}
        internal = len(ops) == 1 and "internal" in ops[0] and "internal" in voc.live_word
        subj = {"type": "object",
                "properties": {"operations": {"const": [o["id"] for o in ops]},
                               "narrowing": {"enum": [None] if tied else [None] + [m for m in NARROWINGS if m in voc.live_word]},
                               "internal": {"type": "boolean"} if internal else {"const": False},
                               "tie": {"$ref": "#/$defs/" + roots[3]} if tied else {"type": "null"},
                               "condition": opt(roots[2]) if voc.relatives else {"type": "null"}},
                "required": ["operations", "narrowing", "internal", "tie", "condition"], "additionalProperties": False}
        clause_alts.append({"type": "object", "title": f"{domain}: {key}",
                            "properties": {"subject": subj, "claims": {"type": "array", "minItems": 1, "items": claim}},
                            "required": ["subject", "claims"], "additionalProperties": False})
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": "Clausal rule tree",
            "description": "GENERATED from the Clausebook by `python3 -m clausal tree --schema` (clausal/clausal/ctree.py); do not edit. "
                           "A tree that validates is not yet a sentence: `clausal tree --from` writes it, compiles it and checks it is read back as itself.",
            "x-books": [{"book": bk.rel, "sha256": hashlib.sha256(bk.text.encode()).hexdigest()} for bk in voc.books],
            "type": "object",
            "properties": {"schema": {"const": SCHEMA}, "system": {"enum": sorted({o["domain"] for o in voc.ops.values()})},
                           "clauses": {"type": "array", "minItems": 1, "items": {"anyOf": clause_alts}}},
            "required": ["schema", "system", "clauses"], "additionalProperties": False, "$defs": defs}


def validate(x, sch, root=None, path="$") -> list:
    """A validator for the keywords `schema` emits (type, const, enum, pattern, anyOf, $ref, properties, required,
    additionalProperties, maxProperties, items, prefixItems, minItems, maxItems, and the schema `false`). [] if valid, else reasons."""
    root = root if root is not None else sch
    if sch is False:
        return [f"{path}: nothing of the book fits here"]
    if sch is True:
        return []
    if "$ref" in sch:
        return validate(x, root["$defs"][sch["$ref"].split("/$defs/", 1)[1]], root, path)
    if "const" in sch:
        return [] if x == sch["const"] and type(x) is type(sch["const"]) else [f"{path}: must be {json.dumps(sch['const'])}"]
    if "enum" in sch:
        return [] if any(x == e and type(x) is type(e) for e in sch["enum"]) else [f"{path}: must be one of {json.dumps(sch['enum'])}"]
    if "anyOf" in sch:
        errs = []
        for alt in sch["anyOf"]:
            e = validate(x, alt, root, path)
            if not e:
                return []
            errs.append(e)
        if not errs:
            return [f"{path}: nothing of the book fits here"]
        return max(errs, key=lambda e: (max(m.split(":", 1)[0].count(".") + m.split(":", 1)[0].count("[") for m in e), -len(e)))   # the alternative that got deepest
    t = sch.get("type")
    ok = {"object": isinstance(x, dict), "array": isinstance(x, list), "string": isinstance(x, str),
          "boolean": isinstance(x, bool), "null": x is None, None: True}[t]
    if not ok:
        return [f"{path}: must be of type {t}"]
    out = []
    if t == "string" and "pattern" in sch and not re.search(sch["pattern"], x):
        out.append(f"{path}: \"{x}\" does not match {sch['pattern']}")
    if t == "object":
        props = sch.get("properties", {})
        out += [f"{path}: `{k}` is missing" for k in sch.get("required", []) if k not in x]
        if sch.get("additionalProperties") is False:
            out += [f"{path}: `{k}` is not a key here (keys: {', '.join(props)})" for k in x if k not in props]
        if "maxProperties" in sch and len(x) > sch["maxProperties"]:
            out.append(f"{path}: at most {sch['maxProperties']} key(s)")
        for k, v in x.items():
            if k in props:
                out += validate(v, props[k], root, f"{path}.{k}")
    if t == "array":
        if len(x) < sch.get("minItems", 0) or len(x) > sch.get("maxItems", len(x)):
            out.append(f"{path}: wrong number of items ({len(x)})")
        for k, v in enumerate(x):
            pre = sch.get("prefixItems", [])
            s = pre[k] if k < len(pre) else sch.get("items", True)
            out += validate(v, s, root, f"{path}[{k}]")
    return out


# --------------------------------------------------------------------------------------------- the round trip

def rule_lines(voc, comp) -> list:
    """[(id, source, sentence, system hint, reading | Problem)] for every Rule line of features/ and controls/, compiled as
    clausebook/terms.lock.json records it (`book.compiled_terms`): a Rule of features/ in the system of the scenarios
    beneath it, if any; a Rule of controls/ with no system given."""
    out = []
    for d in ("features", "controls"):
        for path in sorted((ROOT / d).glob("*.feature")):
            rel = f"{d}/{path.name}"
            f = parse_feature(path, rel)
            sc = {s.id: comp.scenario(s) for s in f.scenarios}
            for r in f.rules:
                hint = None if d == "controls" else next((sc[s.id].info["ops"][0]["domain"] for s in r.scenarios
                                                           if isinstance(sc.get(s.id), vocab.Reading)), None)
                out.append((r.id, f"{rel}:{r.line}", r.name.strip(), hint, comp.rule(r, hint)))
    return out


def norm(s: str) -> str:
    s = s.strip().rstrip(".")
    return s[:1].lower() + s[1:]


def check(voc=None, comp=None) -> dict:
    """THE ROUND TRIP on every Rule line of features/ and controls/ that compiles: sentence -> tree -> (schema) -> sentence -> compile ->
    the same Lean term and the same tree. Also: the digest of the term is the one clausebook/terms.lock.json records."""
    if voc is None:
        voc, comp = load()
    sch = schema(voc)
    lock = json.loads((ROOT / vocab.BOOK_DIR / "terms.lock.json").read_text())["sentences"]
    rows = []
    for id_, source, text, hint, rd in rule_lines(voc, comp):
        if isinstance(rd, Problem):
            rows.append({"id": id_, "source": source, "compiled": False, "status": rd.status})
            continue
        row = {"id": id_, "source": source, "compiled": True, "sentence": text}
        try:
            tree = of_reading(rd)
            row["schema_errors"] = validate(tree, sch)
            got = sentence(json.loads(json.dumps(tree)), voc, comp)
            row["written"] = got["sentence"]
            row["same_sentence"] = norm(got["sentence"]) == norm(text)
            row["same_term"] = body(got["reading"]) == body(rd)
            row["lock"] = (lock.get(id_) or {}).get("lean_sha256") == term_sha(rd)
            row["ok"] = not row["schema_errors"] and row["same_term"]
        except TreeError as e:
            row["ok"], row["error"] = False, str(e)
        rows.append(row)
    comp_rows = [r for r in rows if r["compiled"]]
    return {"rule_lines": len(rows), "compiled": len(comp_rows), "round_trip_same_term": sum(r["ok"] for r in comp_rows),
            "same_sentence": sum(bool(r.get("same_sentence")) for r in comp_rows), "term_is_the_locked_one": sum(bool(r.get("lock")) for r in comp_rows),
            "schema_valid": sum(r.get("schema_errors") == [] for r in comp_rows), "rows": rows}


def main(argv) -> int:
    argv = list(argv)

    def opt(name):
        if name in argv:
            i = argv.index(name)
            v = argv[i + 1] if i + 1 < len(argv) else None
            del argv[i:i + 2]
            return v
        return None

    domain, src, out = opt("--domain"), opt("--from"), opt("--out")
    voc, comp = load()
    if "--schema" in argv:
        text = json.dumps(schema(voc), indent=1, ensure_ascii=False) + "\n"
        if out:
            Path(out).write_text(text)
        else:
            sys.stdout.write(text)
        return 0
    if "--check" in argv:
        r = check(voc, comp)
        for row in r["rows"]:
            if row["compiled"] and not row["ok"]:
                print(f"FAIL  {row['id']} ({row['source']}): {row.get('error') or row.get('schema_errors') or 'another term'}")
        print(f"round trip (tree -> sentence -> compile -> the same Lean term): {r['round_trip_same_term']} of {r['compiled']} compiled Rule lines "
              f"({r['rule_lines'] - r['compiled']} Rule lines of features/ and controls/ are refused and have no tree); the tree validates against the generated "
              f"schema: {r['schema_valid']}; the sentence written is the fixture's own: {r['same_sentence']}; the term is the one in terms.lock.json: "
              f"{r['term_is_the_locked_one']}")
        return 0 if r["round_trip_same_term"] == r["compiled"] == r["schema_valid"] else 1
    try:
        if src:
            tree = json.loads(Path(src).read_text() if src != "-" else sys.stdin.read())
            errs = validate(tree, schema(voc))
            if errs:
                print("clausal tree: the tree does not fit the schema of the book:\n  " + "\n  ".join(errs[:8]), file=sys.stderr)
                return 1
            got = sentence(tree, voc, comp)
            print(json.dumps({"sentence": got["sentence"], "system": got["reading"].info["domain"], "compiles_as_written": got["compiles_as_written"],
                              "term_sha256": body_sha(got["reading"]), "echo": [list(e) for e in got["reading"].echo]}, indent=1, ensure_ascii=False))
            return 0
        rest = [a for a in argv if not a.startswith("--")]
        if len(rest) != 1:
            print(__doc__)
            return 2
        rd = compile_sentence(comp, rest[0], domain)
        if isinstance(rd, Problem):
            print(f"clausal tree: the sentence is refused: {rd.status}: {rd.message}", file=sys.stderr)
            return 1
        print(json.dumps(of_reading(rd), indent=1, ensure_ascii=False))
        return 0
    except (TreeError, FeatureError) as e:
        print(f"clausal tree: {e}", file=sys.stderr)
        return 1
