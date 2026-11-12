"""Trust policies and strict mode (plan node W3). The keys are frozen in trust/FREEZE.md, section 3.

A POLICY is one file per project, named by `trust:` in projects.yaml. It names ROOTS (whose records the project admits) and
REQUIREMENTS (which act, by which signer kinds, of which roots, a kind of subject needs), and says which requirements
strict mode DEMANDS.

    python3 -m clausal trust [--graph out/graph.json] [--policy FILE] [--strict] [--json]

Strict mode is a function of (the graph, the policy) and of nothing else: this module reads a stored graph and policy files.
The graph is the same whatever the policy (clausal/report.py never reads a policy to build it), so two policies over one
tree give the same evidence and may give different strict outcomes. What is fixed in code and no policy can change is in
attest.py: a signer's kind is its own, and `kinds: [person]` is met by a person's record only.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import yaml

from . import attest, graphlint
from .core import FeatureError

ROOT = Path(__file__).resolve().parent.parent
TOP_KEYS = {"version", "project", "roots", "requirements", "recorded_not_counted", "strict"}
ROOT_KEYS = {"id", "signer", "ssh_key", "on_behalf_of", "roles"}
REQ_KEYS = {"subject", "books", "act", "kinds", "roots", "roles"}
STRICT_KEYS = {"demands", "unsigned_person_record"}
SUBJECTS = {"piece", "separation", "glossary-entry"}                 # what this build can evaluate
SUBJECTS_LATER = {"assumption", "specialist-term"}                   # W4, W8: a policy may state them; strict fails closed
NOTHING_STALE = "nothing-stale"
# The old strict mode, as a policy: every entry a proved verdict rests on is reviewed or approved by a person. Used for a
# project that names no policy. `human:*` (any person) can be written here only; a policy file names its roots.
BUILTIN = {"version": 1, "project": "*",
           "roots": [{"id": "any-person", "signer": "human:*"}],
           "requirements": {"meaning.pieces": {"subject": "piece", "act": ["reviewed", "approved"], "kinds": ["person"]},
                            "meaning.separations": {"subject": "separation", "act": ["reviewed", "approved"], "kinds": ["person"]},
                            "meaning.glossary": {"subject": "glossary-entry", "act": ["reviewed", "approved"], "kinds": ["person"]}},
           "strict": {"demands": ["meaning.pieces", "meaning.glossary"], "unsigned_person_record": "accept-as-claim"}}


class Policy:
    def __init__(self, raw: dict, where: str, sha256: str | None = None, builtin: bool = False):
        self.where, self.sha256, self.builtin = where, sha256, builtin
        bad = lambda m: FeatureError(f"{where}: {m}")
        if not isinstance(raw, dict):
            raise bad("a policy is a mapping")
        if set(raw) - TOP_KEYS:
            raise bad(f"unknown key(s) {sorted(set(raw) - TOP_KEYS)}")
        if raw.get("version") != 1:
            raise bad("`version: 1` is the only version")
        if not isinstance(raw.get("project"), str):
            raise bad("`project` names the project of projects.yaml the policy is for")
        self.project = raw["project"]
        self.roots = {}
        for r in raw.get("roots") or []:
            if not isinstance(r, dict) or set(r) - ROOT_KEYS or not isinstance(r.get("id"), str):
                raise bad(f"a root has an `id` and the keys {', '.join(sorted(ROOT_KEYS))}; got {r!r}")
            if r["id"] in self.roots:
                raise bad(f"root `{r['id']}` is named twice")
            s = r.get("signer")
            kind = None
            if s is not None:
                kind = "person" if (builtin and s == "human:*") else attest.kind_of_id(s)
                if kind is None:
                    raise bad(f"root `{r['id']}`: `{s}` is not a signer id (prefix {', '.join(attest.KINDS.values())}); use `signer: null` "
                              "for someone awaited")
            if r.get("ssh_key") is not None:
                raise bad(f"root `{r['id']}`: `ssh_key` must be null, signatures are not checked in this build (plan node W9)")
            obo = r.get("on_behalf_of")
            if obo is not None and not (isinstance(obo, list) and all(attest.kind_of_id(x) for x in obo)):
                raise bad(f"root `{r['id']}`: `on_behalf_of` is a list of agent ids")
            self.roots[r["id"]] = {"id": r["id"], "signer": s, "kind": kind, "on_behalf_of": obo, "roles": list(r.get("roles") or [])}
        self.requirements = {}
        for name, q in (raw.get("requirements") or {}).items():
            if not isinstance(q, dict):
                raise bad(f"requirement `{name}` is a mapping")
            if set(q) == {"every_condition"}:
                self.requirements[name] = {"name": name, "every_condition": q["every_condition"]}
                continue
            if set(q) - REQ_KEYS:
                raise bad(f"requirement `{name}`: unknown key(s) {sorted(set(q) - REQ_KEYS)}")
            if q.get("subject") not in SUBJECTS | SUBJECTS_LATER:
                raise bad(f"requirement `{name}`: `subject` is one of {', '.join(sorted(SUBJECTS | SUBJECTS_LATER))}")
            acts = q.get("act")
            acts = [acts] if isinstance(acts, str) else list(acts or [])
            if not acts or set(acts) - set(attest.ACTS):
                raise bad(f"requirement `{name}`: `act` is one or more of {', '.join(attest.ACTS)}")
            kinds = list(q.get("kinds") or [])
            if not kinds or set(kinds) - set(attest.KINDS):
                raise bad(f"requirement `{name}`: `kinds` lists signer kinds ({', '.join(attest.KINDS)})")
            if "tool" in kinds and set(acts) - attest.TOOL_ACTS:
                raise bad(f"requirement `{name}`: a tool can only have authored or tested something; it cannot meet `{', '.join(acts)}`")
            if "roots" in q:
                for x in q["roots"] or []:
                    if x not in self.roots:
                        raise bad(f"requirement `{name}` names the root `{x}`, which the policy does not list")
                    if self.roots[x]["kind"] is not None and self.roots[x]["kind"] not in kinds:
                        raise bad(f"requirement `{name}` asks for {' or '.join(kinds)} and names the root `{x}`, a {self.roots[x]['kind']}: "
                                  "that root could never meet it")
            if "books" in q and q["subject"] not in ("piece", "separation"):
                raise bad(f"requirement `{name}`: `books` is for pieces and separations")
            self.requirements[name] = {"name": name, "subject": q["subject"], "books": q.get("books"), "acts": acts, "kinds": kinds,
                                       "roots": q.get("roots"), "roles": q.get("roles")}
        self.recorded_not_counted = []
        for x in raw.get("recorded_not_counted") or []:
            if not isinstance(x, dict) or set(x) - {"act", "kinds"} or set(x.get("act") or []) - set(attest.ACTS) or set(x.get("kinds") or []) - set(attest.KINDS):
                raise bad(f"`recorded_not_counted` entries are {{act: [acts], kinds: [signer kinds]}}; got {x!r}")
            self.recorded_not_counted.append({"act": list(x.get("act") or []), "kinds": list(x.get("kinds") or [])})
        for x in self.recorded_not_counted:              # a policy may not say of the same records that they count and that they do not
            for name, q in self.requirements.items():
                if "subject" in q and set(q["kinds"]) & set(x["kinds"]) and set(q["acts"]) & set(x["act"]):
                    raise bad(f"`recorded_not_counted` lists {sorted(set(q['acts']) & set(x['act']))} by {sorted(set(q['kinds']) & set(x['kinds']))}, "
                              f"and requirement `{name}` is met by exactly such a record: it cannot be both")
        st = raw.get("strict") or {}
        if not isinstance(st, dict) or set(st) - STRICT_KEYS:
            raise bad(f"`strict` has the keys {', '.join(sorted(STRICT_KEYS))}")
        self.demands = list(st.get("demands") or [])
        for d in self.demands:
            if d != NOTHING_STALE and d not in self.requirements:
                raise bad(f"strict demands `{d}`, which is not a requirement of the policy")
        self.unsigned_person = st.get("unsigned_person_record", "accept-as-claim")
        if self.unsigned_person not in ("accept-as-claim", "refuse"):
            raise bad("`strict.unsigned_person_record` is `accept-as-claim` or `refuse`")

    # ---- which records a requirement admits
    def roots_of(self, q: dict) -> list:
        rs = [self.roots[x] for x in q["roots"]] if q.get("roots") is not None else list(self.roots.values())
        if q.get("roles"):
            rs = [r for r in rs if set(r["roles"]) & set(q["roles"])]
        return rs

    def admitted(self, q: dict, a: dict) -> bool:
        """Is the stored record `a` (attest.brief: act, kind, by, on_behalf_of) admitted for requirement `q`? The record's kind
        is the signer's own; nothing here can turn one kind into another."""
        if a["act"] not in q["acts"] or a["kind"] not in q["kinds"]:
            return False
        if a["kind"] == "person" and self.unsigned_person == "refuse":
            return False                       # no record carries a checked signature before W9
        for r in self.roots_of(q):
            if r["signer"] is None or r["kind"] != a["kind"]:
                continue
            if r["signer"] != a["by"] and not (self.builtin and r["signer"] == "human:*"):
                continue
            if r["on_behalf_of"] is not None and a.get("on_behalf_of") not in r["on_behalf_of"]:
                continue
            return True
        return False

    def covers(self, q: dict, n: dict) -> bool:
        t = n.get("attrs", {})
        return t.get("subject_kind") == q["subject"] and (not q.get("books") or t.get("book") in q["books"])

    def awaited(self) -> list:
        return [r["id"] for r in self.roots.values() if r["signer"] is None]


def load_policy(path: Path, where: str | None = None) -> Policy:
    if not path.exists():
        raise FeatureError(f"{where or path}: the trust policy file does not exist")
    data = path.read_bytes()
    try:
        raw = yaml.safe_load(data)
    except yaml.YAMLError as e:
        raise FeatureError(f"{where or path}: not YAML ({e})")
    return Policy(raw, where or str(path), hashlib.sha256(data).hexdigest())


def builtin_policy() -> Policy:
    return Policy(BUILTIN, "the built-in policy (the old strict mode: every entry reviewed or approved by a person)", None, builtin=True)


def policies(pr, override: Path | None = None) -> dict:
    """Project name -> Policy: the file its entry of projects.yaml names (`trust:`), the built-in one if it names none, or
    `override` for every project (the tests; the policy's `project` is then not compared)."""
    out = {}
    for p in pr:
        if override is not None:
            out[p.name] = load_policy(override)
        elif getattr(p, "trust", None):
            pol = load_policy(pr.root / p.trust, p.trust)
            if pol.project != p.name:
                raise FeatureError(f"{p.trust}: the policy is for project `{pol.project}`, and projects.yaml names it for `{p.name}`")
            out[p.name] = pol
        else:
            out[p.name] = builtin_policy()
    return out


# --------------------------------------------------------------------------- evaluation over a stored graph

def graph_digest(g: dict) -> str:
    """sha256 of everything in the graph except the clock (`generated_at`)."""
    return hashlib.sha256(json.dumps({k: v for k, v in g.items() if k != "generated_at"}, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def subjects_of(g_nodes: dict, composed: dict, v: dict) -> list:
    """The attestable entries a verdict rests on: the Clausebook entries of its node's reading, and the entries of the old
    glossary its scenario is composed of."""
    n = g_nodes.get(v["node"], {})
    ids = [f"piece:{p['id']}" for p in (n.get("attrs", {}).get("reading") or {}).get("pieces", [])] + composed.get(v["node"], [])
    return [g_nodes[i] for i in dict.fromkeys(ids) if i in g_nodes]


def evaluate(g: dict, pr, pols: dict) -> dict:
    nodes = {n["id"]: n for n in g["nodes"]}
    composed = {}
    for e in g["edges"]:
        if e["relation"] == "composed_of":
            composed.setdefault(e["from"], []).append(e["to"])
    stale = set(graphlint.staleness(g)["verdicts"])
    out = {"graph_sha256": graph_digest(g), "projects": {}, "verdicts": []}
    stats = {}
    for p in pr:
        pol = pols[p.name]
        out["projects"][p.name] = {"policy": pol.where, "policy_sha256": pol.sha256, "demands": pol.demands, "awaited_roots": pol.awaited(),
                                   "roots": [{"id": r["id"], "signer": r["signer"], "kind": r["kind"]} for r in pol.roots.values()],
                                   "requirements": {}, "recorded_not_counted": {}}
        stats[p.name] = {name: {} for name in pol.requirements}        # requirement -> subject id -> kinds that met it
    for v in g["verdicts"]:
        n = nodes.get(v["node"])
        if n is None or not v["code"].startswith("PROVED"):
            continue
        p = pr.of_feature((n["interface"].get("source") or {}).get("file", ""))
        if p is None:
            continue
        pol, subs, unmet, model_only = pols[p.name], subjects_of(nodes, composed, v), [], False
        for name, q in pol.requirements.items():
            if "every_condition" in q or q["subject"] in SUBJECTS_LATER:
                if name in pol.demands:
                    unmet.append({"requirement": name, "why": "cannot be evaluated by this build (the assumption ledger and specialist terms "
                                                              "are plan nodes W4 and W8): strict mode fails closed"})
                continue
            missing = []
            for s in subs:
                if not pol.covers(q, s):
                    continue
                ok = [a for a in s["attrs"].get("attestations", []) if pol.admitted(q, a)]
                stats[p.name][name][s["id"]] = sorted({a["kind"] for a in ok})
                if not ok:
                    missing.append(s["id"])
                elif name in pol.demands and all(a["kind"] == "model" for a in ok):
                    model_only = True
            if missing and name in pol.demands:
                unmet.append({"requirement": name, "subjects": missing})
        if NOTHING_STALE in pol.demands and v["node"] in stale:
            unmet.append({"requirement": NOTHING_STALE, "why": "the verdict is stale: something it was computed from has changed"})
        out["verdicts"].append({"node": v["node"], "project": p.name, "code": v["code"], "strict": "fail" if unmet else "pass", "unmet": unmet,
                                "flags": ["MEANING-MODEL-ONLY"] if (model_only and not unmet) else []})
        for s in subs:                                                  # what is on record and meets nothing: under its own label
            for a in s["attrs"].get("attestations", []):
                if not any("subject" in q and pol.covers(q, s) and pol.admitted(q, a) for q in pol.requirements.values()):
                    out["projects"][p.name]["recorded_not_counted"].setdefault(f"{a['kind']} {a['act']}", set()).add(s["id"])
    for name, pj in out["projects"].items():
        pj["recorded_not_counted"] = {k: len(v) for k, v in sorted(pj["recorded_not_counted"].items())}
        for rname, subj in stats[name].items():
            by_kind = {}
            for kinds in subj.values():
                for k in kinds:
                    by_kind[k] = by_kind.get(k, 0) + 1
            # counts per kind are kept apart and never summed: a subject met by a person and by a model is in both
            pj["requirements"][rname] = {"subjects": len(subj), "met": sum(bool(k) for k in subj.values()), "unmet": sum(not k for k in subj.values()),
                                         "met_by_kind": by_kind, "demanded": rname in pols[name].demands}
        vs = [x for x in out["verdicts"] if x["project"] == name]
        pj["proved"], pj["strict_pass"], pj["strict_fail"] = len(vs), sum(x["strict"] == "pass" for x in vs), sum(x["strict"] == "fail" for x in vs)
        pj["model_only"] = sum(bool(x["flags"]) for x in vs)
    out["strict_fail"] = sum(pj["strict_fail"] for pj in out["projects"].values())
    return out


def lines(res: dict) -> list:
    L = []
    for name, pj in res["projects"].items():
        L.append(f"trust, project {name}: {pj['policy']}" + (f" (sha256 {pj['policy_sha256'][:12]})" if pj["policy_sha256"] else ""))
        for r in pj["roots"]:
            L.append(f"    root {r['id']}: " + (f"{r['signer']} ({r['kind']})" if r["signer"] else "AWAITED (nobody named)"))
        for rn, q in pj["requirements"].items():
            met = ", ".join(f"{n} by a {k}" for k, n in sorted(q["met_by_kind"].items())) or "none"
            L.append(f"    {'demanded' if q['demanded'] else 'stated  '} {rn}: {q['subjects']} entries under proved verdicts; met: {met}; unmet: {q['unmet']}")
        if pj["recorded_not_counted"]:
            L.append("    recorded, not counted: " + "; ".join(f"{n} entries {k}" for k, n in pj["recorded_not_counted"].items()))
        L.append(f"    strict: {pj['strict_pass']} of {pj['proved']} proved verdicts pass, {pj['strict_fail']} fail"
                 + (f"; MEANING-MODEL-ONLY on {pj['model_only']}" if pj["model_only"] else "")
                 + (f"; awaited: {', '.join(pj['awaited_roots'])}" if pj["awaited_roots"] else ""))
    return L


def main(argv) -> int:
    from . import projects
    graph, override, strict, as_json = ROOT / "out" / "graph.json", None, False, False
    it = iter(argv)
    for a in it:
        if a == "--graph":
            graph = Path(next(it))
        elif a == "--policy":
            override = Path(next(it))
        elif a == "--strict":
            strict = True
        elif a == "--json":
            as_json = True
        else:
            print(__doc__)
            return 2
    pr = projects.load()
    res = evaluate(json.loads(graph.read_text()), pr, policies(pr, override))
    if as_json:
        print(json.dumps(res, indent=1, ensure_ascii=False))
    else:
        print("\n".join(lines(res)))
        print(f"graph {res['graph_sha256'][:16]} (sha256 of everything but the clock); strict mode would fail {res['strict_fail']} proved verdicts")
    return 1 if (strict and res["strict_fail"]) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
