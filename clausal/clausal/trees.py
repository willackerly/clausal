"""clausal trees: the COMPOSITION TREES the Rust side evaluates (build/trees.json).

The Rust side has no step and no predicate per sentence. It has ONE reading per Clausebook piece
(wallet-bdd/src/pieces.rs: one function per domain word, modifier and frame) and an evaluator of composition
trees. This module writes the trees:

  steps      one entry per distinct step FORM of the feature files: a regular expression that matches the step with
             every actor name, literal and <parameter> captured, and the tree of pieces the step compiles to with those
             captures as its leaves. wallet-bdd/tests/bdd.rs registers every regex with the same generic step function;
             the entry is found through a named, empty capture group (`T<n>`). A step that does not compile has no
             entry, so cucumber reports it as undefined and skips the rest of its scenario.
  readings   every compiled reading (scenario or Rule) with the grid of generated inputs it is searched on
             (lean/Run/ReadingSearch.lean). wallet-bdd/tests/grid.rs evaluates each reading at each grid point on the
             COMPILED RUST and writes the same bit string the Lean side prints (`RBITS`): per unit its scope, per claim
             the relation between two calls (two-run frames) and the claim. The report compares the two strings: that
             is the per-piece second reading compared with the Lean piece on generated inputs, and it is also the
             compiled-Rust confirmation of a counterexample to a Rule.

Like the rest of clausal this is untrusted: a wrong tree shows up as a disagreement with the Lean side.
"""
from __future__ import annotations

import json
import re

from .core import Problem, literal_regex, nocapture
from .vocab import Leaf, Node, Reading, match_when, walk

META = re.compile(r"([.^$*+?()\[\]{}|\\])")


def esc(text: str) -> str:
    return META.sub(r"\\\1", text)


def tj(x, slot_of=None):
    """A parse tree as JSON. Leaves name where their value comes from: a capture of the step (`slot`), a name bound by
    the caller (`ref`: an outline parameter, a role of a Rule, an actor), or a literal (`lit`)."""
    if isinstance(x, list):
        return [tj(y, slot_of) for y in x]
    if isinstance(x, Leaf):
        d = {"k": x.kind, "type": x.type}
        if slot_of is not None:
            d["slot"] = slot_of[x.text]
        elif x.kind == "actor":
            d["ref"] = x.text
        elif x.how == "param":
            d["ref"] = x.param
        elif x.how == "role":
            d["ref"] = x.text
        else:
            d["lit"] = x.text
        return d
    d = {"p": x.id, "a": {k: tj(v, slot_of) for k, v in x.args.items()}}
    if x.variant == "per_actor":
        d["per_actor"] = x.piece["per_actor"]["type"]
    return d


def capture(voc, leaf: Leaf) -> str:
    if leaf.kind == "actor":
        a = voc.actors[leaf.type]
        return nocapture(a.get("mention", a["name_regex"]))
    pt = voc.pts[leaf.type]
    if "enum" in pt:
        return "|".join(esc(k) for k in pt["enum"])
    return nocapture(literal_regex(voc.pts, leaf.type))


def template(voc, text: str, leaves: list) -> tuple:
    """(regex body, {leaf text: slot}) for a step text whose leaves are given: every occurrence of a leaf's text is
    replaced by a named capture of that leaf's type; a leaf's slot is its first occurrence."""
    by_text = {}
    for l in leaves:
        by_text.setdefault(l.text, l)
    order = sorted(by_text, key=len, reverse=True)
    out, slot_of, pos, n = "", {}, 0, 0
    while pos < len(text):
        hit = None
        for t in order:
            if text.startswith(t, pos):
                before = text[pos - 1] if pos else " "
                after = text[pos + len(t)] if pos + len(t) < len(text) else " "
                if t.startswith("<") or not (before.isalnum() or after.isalnum()):
                    hit = t
                    break
        if hit is None:
            out += esc(text[pos])
            pos += 1
            continue
        out += f"(?P<s{n}>{capture(voc, by_text[hit])})"
        slot_of.setdefault(hit, n)
        n += 1
        pos += len(hit)
    return out, slot_of


def step_entries(st) -> tuple:
    """([entry], [problem text]): one entry per distinct step form of the compiled scenarios."""
    voc = st.voc
    by_key, problems = {}, []

    META = ("kind", "body", "example", "system", "by_system")

    def add(kind, body, entry, where, system):
        """Two SYSTEMS may say the same words of their answers (the wallet's and the ledger's "it is accepted"): a Then form
        then has one tree per system (`by_system`), and the generic Rust step takes the one of the system the scenario's When
        belongs to. The same form with two trees inside one system, or a Given or a When, is still a clash."""
        key = (kind, body)
        old = by_key.get(key)
        if old is None:
            entry.update({"kind": kind, "body": body, "example": where, "system": system})
            by_key[key] = entry
            return
        alts = old.get("by_system") or {old["system"]: {k: v for k, v in old.items() if k not in META}}
        if system in alts:
            if alts[system] != entry:
                problems.append(f"{where}: this step has the same form as {old['example']} but compiles to a different tree; the first is kept")
        elif kind == "then":
            alts[system] = entry
            old["by_system"] = alts
        else:
            problems.append(f"{where}: this step has the same form as {old['example']} (another system) but compiles to a different tree; the first is kept")

    for sc, _ in st.results:
        rd = st.readings.get(sc.id)
        if not isinstance(rd, Reading):
            continue
        info = rd.info
        system = info["ops"][0]["domain"]
        for w, op, bind in zip(info["whens"], info["ops"], info["binds"]):
            body, slot_of = template(voc, w.text, list(bind.values()))
            add("when", body, {"op": op["id"], "roles": {r: tj(l, slot_of) for r, l in bind.items()}}, f"{sc.feature.path}:{w.line}", system)
        for s, t, _ in info["givens"]:
            leaves = [x for x in walk(t) if isinstance(x, Leaf)]
            body, slot_of = template(voc, s.text, leaves)
            add("given", body, {"tree": tj(t, slot_of)}, f"{sc.feature.path}:{s.line}", system)
        for j, (s, t, mods) in enumerate(info["thens"]):
            claims = [c for c in rd.claims if c.step == j]
            leaves = [x for c in claims for x in walk(c.node) if isinstance(x, Leaf)]
            body, slot_of = template(voc, s.text, leaves)
            add("then", body, {"claims": [{"frame": c.frame["id"], "mods": c.mods, "node": tj(c.node, slot_of)} for c in claims]},
                f"{sc.feature.path}:{s.line}", system)
    out = []
    for n, e in enumerate(by_key.values()):
        e["regex"] = f"^(?P<T{n}>){e.pop('body')}$"
        out.append(e)
    return out, problems


def reading_entry(voc, rd: Reading, side: dict) -> dict | None:
    """One compiled reading with its grid, for evaluation on the compiled Rust; None if it has no grid."""
    if "skipped" in side or "rust" not in side:
        return None
    g = side["rust"]

    def claims(cs, base):
        return [{"index": base + j, "frame": c.frame["id"], "mods": c.mods, "runs": c.runs, "node": tj(c.node) if c.node is not None else None}
                for j, c in enumerate(cs)]
    units = []
    if rd.kind == "scenario":
        info = rd.info
        units.append({"ops": [o["id"] for o in info["ops"]], "state": info["st_actors"], "bystanders": info["bystanders"],
                      "internal": False, "conds": [tj(c["node"]) for c in rd.conds if c["node"] is not None],
                      "claims": claims(rd.claims, 0)})
    else:
        k = 0
        for cl in rd.info["clauses"]:
            units.append({"ops": [o["id"] for o in cl["ops"]], "state": ["the " + r for r, _ in cl["ops"][0]["state"]], "bystanders": [],
                          "internal": cl["internal"], "conds": [tj(t) for t in cl["cond_trees"]], "claims": claims(cl["claims"], k)})
            k += len(cl["claims"])

    def run(actors, inputs):
        return {"actors": [{"ref": a, "type": t, "var": v} for a, t, v in actors],
                "inputs": [{"type": t, "var": v, "lit": l, "ref": r} for t, v, l, r in inputs]}
    return {"id": rd.id, "kind": rd.kind, "width": side.get("width"),
            "vars": [{"name": n, "type": g["types"][n], "values": vals} for n, vals in side["vars"]],
            "run1": run(g["actors"], g["inputs"]), "run2": run(g["actors2"], g["inputs2"]) if g.get("actors2") else None,
            "units": units}


def build(st, side: dict) -> dict:
    voc = st.voc
    steps, problems = step_entries(st)
    readings = []
    for rd, _ in st.compiled:
        e = reading_entry(voc, rd, side.get(rd.id, {}))
        if e:
            readings.append(e)
    ops = {o["id"]: {"state": o["state"], "input": o["input"], "shape": o["shape"], "system": o["domain"]} for o in voc.ops.values()}
    types = {k: {"list_of": v.get("list_of"), "enum": sorted(v["enum"]) if "enum" in v else None} for k, v in voc.pts.items()}
    builds = {t: a["build"]["param_type"] for t, a in voc.actors.items()}
    measures = {p["id"]: True for p in voc.pieces.values() if p.get("builds")}
    return {"steps": steps, "readings": readings, "ops": ops, "types": types, "actor_built_from": builds,
            "building_measures": sorted(measures), "problems": problems}


def dump(data: dict) -> str:
    return json.dumps(data, indent=1, ensure_ascii=False)
