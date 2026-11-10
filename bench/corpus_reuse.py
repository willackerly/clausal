#!/usr/bin/env python3
"""Recurrence in the machine-generated corpus (corpora/ns), declaration level and inside proofs.

    python3 bench/corpus_reuse.py cluster     # declaration-level clusters + inputs of the Lean checks
    python3 bench/corpus_reuse.py inproof <sample>   # prepare / post-process one in-proof sample
    python3 bench/corpus_reuse.py report      # out/corpus/reuse/REUSE.md

Inputs (all produced by Lean, no source regex):
  out/corpus/ns/decls.jsonl            declaration graph (corpora/ns_export/Export.lean)
  out/corpus/reuse/stmt_keys.jsonl     statement / proof keys (corpora/ns_reuse/StmtKeys.lean)
  out/corpus/reuse/inproof_*/          in-proof dumps (corpora/ns_reuse/ReuseNS.lean = the root
                                       project's Rosette/Candidates.lean + Rosette/Reuse.lean)
  out/corpus/reuse/factor/*.jsonl      kernel-check results (corpora/ns_reuse/ReuseCheck.lean)
  out/reuse/summary.json               the Mathlib run, for comparison
Hand-entered: out/corpus/reuse/judgements.json (verdicts on the 20 largest clusters after reading
the source). Source text is read only to SHOW members and to count lines, never to decide anything.
"""
import json
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NS = ROOT / "out/corpus/ns"
OUT = ROOT / "out/corpus/reuse"
SRC = ROOT / "corpora/ns"

# statement-level keys, finest first; (key, short name, description)
LEVELS = [
    ("kE", "E", "exact statement"),
    ("pE", "E+perm", "exact, up to binder order"),
    ("kN", "N", "numerals abstracted"),
    ("pN", "N+perm", "numerals abstracted, up to binder order"),
    ("kL", "L", "numerals + leaf constants in argument position"),
    ("kP", "P", "numerals + project constants renamed (heads included)"),
    ("kLP", "LP", "L and P together"),
    ("pLP", "LP+perm", "L and P, up to binder order"),
]
JOINT = [
    ("svE", "SV-E", "statement and proof term identical"),
    ("svN", "SV-N", "statement and proof identical up to numerals"),
    ("svP", "SV-P", "statement and proof identical up to renaming of project constants"),
]


def load():
    D = {}
    for line in open(NS / "decls.jsonl"):
        d = json.loads(line)
        if d["kind"] == "theorem":
            D[d["name"]] = d
    K = {}
    for line in open(OUT / "stmt_keys.jsonl"):
        k = json.loads(line)
        if k["name"] in D:
            K[k["name"]] = k
    assert len(K) == len(D), (len(K), len(D))
    return D, K


def lines_of(d):
    return d["endLine"] - d["line"] + 1 if d.get("line") else 0


def source(d, maxl=None):
    p = SRC / (d["module"].replace(".", "/") + ".lean")
    ls = p.read_text().split("\n")[d["line"] - 1:d["endLine"]]
    return ls if maxl is None else ls[:maxl]


def clusters(D, K, key):
    m = defaultdict(list)
    for n, k in K.items():
        m[k[key]].append(n)
    return {h: sorted(v) for h, v in m.items() if len(v) >= 2}


def level_stats(D, K, key, total_proof, total_lines):
    cl = clusters(D, K, key)
    rows = list(cl.values())
    removable = sum(len(v) - 1 for v in rows)
    # the kept member is the one with the largest proof
    rem_proof = sum(sum(D[n]["proofSize"] for n in v) - max(D[n]["proofSize"] for n in v) for v in rows)
    rem_lines = 0
    for v in rows:
        keep = max(v, key=lambda n: D[n]["proofSize"])
        rem_lines += sum(lines_of(D[n]) for n in v if n != keep)
    hist = Counter()
    for v in rows:
        s = len(v)
        hist["2" if s == 2 else "3" if s == 3 else "4-9" if s <= 9 else "10-19" if s <= 19 else "20+"] += 1
    return {
        "clusters": len(rows), "theorems": sum(len(v) for v in rows), "removable": removable,
        "largest": max((len(v) for v in rows), default=0),
        "crossModule": sum(1 for v in rows if len({D[n]["module"] for n in v}) >= 2),
        "distinctExact": sum(1 for v in rows if len({K[n]["kE"] for n in v}) >= 2),
        "removableProof": rem_proof, "removableProofShare": rem_proof / total_proof,
        "removableLines": rem_lines, "removableLinesShare": rem_lines / total_lines,
        "hist": dict(hist),
    }


def cmd_cluster():
    D, K = load()
    total_proof = sum(d["proofSize"] for d in D.values())
    total_lines = sum(lines_of(d) for d in D.values())
    res = {"theorems": len(D), "totalProofSize": total_proof, "totalLines": total_lines, "levels": {}}
    for key, short, _ in LEVELS + JOINT:
        res["levels"][short] = level_stats(D, K, key, total_proof, total_lines)
    # how the P clusters split when the proof is taken into account
    clP = clusters(D, K, "kLP")
    res["LP_sameProofUpToRenaming"] = sum(1 for v in clP.values() if len({K[n]["svP"] for n in v}) == 1)
    res["LP_allProofsDifferent"] = sum(1 for v in clP.values() if len({K[n]["svP"] for n in v}) == len(v))
    # module pairs that share many SV-P twins (cloned modules)
    pair = Counter()
    nthm = Counter(d["module"] for d in D.values())
    for v in clusters(D, K, "svP").values():
        mods = sorted({D[n]["module"] for n in v})
        for i in range(len(mods)):
            for j in range(i + 1, len(mods)):
                pair[(mods[i], mods[j])] += 1
    res["modulePairs"] = [
        {"a": a, "b": b, "twins": c, "theoremsA": nthm[a], "theoremsB": nthm[b]}
        for (a, b), c in pair.most_common(40)]
    twin_mods = {m for (a, b), c in pair.items() for m in (a, b)
                 if c >= 0.5 * min(nthm[a], nthm[b]) and c >= 5}
    res["modulesHalfCloned"] = len(twin_mods)
    json.dump(res, open(OUT / "decl_levels.json", "w"), indent=1)

    # cluster dump (members with sizes), every level
    dump = {}
    for key, short, _ in LEVELS + JOINT:
        rows = []
        for h, v in clusters(D, K, key).items():
            rows.append({
                "key": h, "size": len(v), "distinctExact": len({K[n]["kE"] for n in v}),
                "distinctProofs": len({K[n]["svE"] for n in v}),
                "distinctProofsUpToRenaming": len({K[n]["svP"] for n in v}),
                "modules": len({D[n]["module"] for n in v}),
                "proofSizes": [D[n]["proofSize"] for n in v],
                "lines": sum(lines_of(D[n]) for n in v), "members": v})
        rows.sort(key=lambda r: (-r["size"], r["members"][0]))
        dump[short] = rows
    json.dump(dump, open(OUT / "decl_clusters.json", "w"), ensure_ascii=False)

    # inputs of the kernel checks
    F = OUT / "factor"
    F.mkdir(exist_ok=True)
    with open(F / "dups.jsonl", "w") as f:           # exact-statement duplicates: rep + others
        for r in dump["E"]:
            rep = max(r["members"], key=lambda n: (not D[n]["isPrivate"], -len(n), n))
            f.write(json.dumps({"rep": rep, "members": [n for n in r["members"] if n != rep]},
                               ensure_ascii=False) + "\n")
    big = dump["E"][0]["members"]
    (F / "nat_le_infty.txt").write_text("\n".join(big) + "\n")
    fact = [r for r in dump["E"] if "Fact (0 < 1)" in D[r["members"][0]]["statement"]]
    (F / "fact_zero_lt_one.txt").write_text("\n".join(fact[0]["members"]) + "\n" if fact else "")
    # SV-P twins between the two NaturalAxis modules and between the cylinder-algebra modules
    def twins(mod_a, mod_b):
        out = []
        for r in dump["SV-P"]:
            a = [n for n in r["members"] if D[n]["module"] == mod_a]
            b = [n for n in r["members"] if D[n]["module"] == mod_b]
            if len(a) == 1 and len(b) == 1:
                out.append((a[0], b[0]))
        return sorted(out)
    json.dump({"naturalAxis": twins("NavierStokes.NaturalAxisData", "NavierStokes.NaturalAxisRange"),
               "cylinder": twins("Euler.GeneralCylinderAlgebra", "Euler.H5CylinderAlgebra")
               + twins("Euler.GeneralRealCylinderAlgebra", "Euler.H5RealCylinderAlgebra")},
              open(F / "twins.json", "w"), indent=1)
    print(json.dumps({k: {x: v[x] for x in ("clusters", "theorems", "removable", "largest")}
                      for k, v in res["levels"].items()}, indent=1))
    print("LP clusters:", len(clP), "same proof up to renaming:", res["LP_sameProofUpToRenaming"],
          "all proofs different:", res["LP_allProofsDifferent"])
    for p in res["modulePairs"][:12]:
        print(p)
    print("modules half cloned:", res["modulesHalfCloned"])

# ---------------------------------------------------------------- in-proof pipeline

EXACT_CAP = 8000          # `exact?` is run on at most this many recurring statements (largest gross first)
VARIANT = "_reproof"      # second view of a sample, see cmd_inproof / after-exact


def _shards(O):
    return sorted(p for p in (O / "shards").iterdir() if p.is_dir())


def _cover(keys, key_decls, ncand, shards, fname):
    """Give every key one theorem that contains it (the cheapest to re-enumerate) and spread the
    theorems over the shards."""
    by_decl = defaultdict(list)
    for k in keys:
        d = min(key_decls[k], key=lambda d: (ncand.get(d, 0), d))
        by_decl[d].append(k)
    order = sorted(by_decl, key=lambda d: -len(by_decl[d]))
    for sh in shards:
        (sh / fname).unlink(missing_ok=True)
    buckets = [{"decls": [], "keys": []} for _ in shards]
    for i, d in enumerate(order):
        b = min(buckets, key=lambda b: len(b["keys"]))
        b["decls"].append(d)
        b["keys"] += by_decl[d]
    for sh, b in zip(shards, buckets):
        if b["keys"]:
            json.dump(b, open(sh / fname, "w"), ensure_ascii=False)
    return sum(len(b["keys"]) for b in buckets)


def _key_decls(O):
    """exact key -> theorems it occurs in (non-root candidates), and candidates per theorem."""
    kd = defaultdict(set)
    ncand = Counter()
    for line in open(O / "candidates.jsonl"):
        r = json.loads(line)
        if r["record"] == "decl":
            ncand[r["decl"]] = r["numCandidates"]
        elif r["role"] != "root":
            kd[r["stmtHash"]].add(r["decl"])
    return kd, ncand


def _run_reuse_py(O):
    subprocess.run([sys.executable, str(ROOT / "bench/reuse.py"), str(O)], check=True,
                   stdout=subprocess.DEVNULL)
    # bench/reuse.py writes a REUSE.md whose verdict text was written for the Mathlib run; only
    # its numbers (summary.json, clusters.json) are used here
    (O / "REUSE.md").unlink(missing_ok=True)


def cmd_inproof(sample, stage, arg=None):
    O = OUT / f"inproof_{sample}"
    V = OUT / f"inproof_{sample}{VARIANT}"
    if stage == "split":
        n = int(arg or 8)
        rows = [l for l in open(O / "sample.txt") if l.strip()]
        for k in range(n):
            d = O / "shards" / f"{k:02d}"
            d.mkdir(parents=True, exist_ok=True)
            (d / "sample.txt").write_text("".join(rows[k::n]))
        print(f"{len(rows)} theorems in {n} shards")
    elif stage == "merge":
        shards = _shards(O)
        stm = {}
        runs = []
        with open(O / "candidates.jsonl", "w") as f:
            for sh in shards:
                f.write((sh / "candidates.jsonl").read_text())
                for line in open(sh / "statements.jsonl"):
                    r = json.loads(line)
                    stm.setdefault(r["stmtHash"], r)
                runs.append(json.load(open(sh / "run.json")))
        with open(O / "statements.jsonl", "w") as f:
            for r in stm.values():
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        (O / "lgg.jsonl").write_text("")
        slices = Counter()
        for r in runs:
            for s in r["slices"]:
                slices[s["slice"]] += s["used"]
        run = {
            "minTheoremProof": 800, "minCandidateProof": runs[0]["minCandidateProof"],
            "slices": [{"slice": k, "prefixes": [k + "."], "eligible": v, "used": v} for k, v in slices.items()],
            "theorems": sum(r["theorems"] for r in runs), "ok": sum(r["ok"] for r in runs),
            "failed": sum(r["failed"] for r in runs), "truncated": sum(r["truncated"] for r in runs),
            "candidates": sum(r["candidates"] for r in runs), "distinctStatements": len(stm),
            "libraryTheoremsHashed": runs[0]["libraryTheoremsHashed"],
            "projectTheoremsHashed": runs[0]["projectTheoremsHashed"],
            "probeBudgetK": runs[0]["probeBudgetK"], "leanVersion": runs[0]["leanVersion"],
            "enumerationSeconds": sum(r["enumerationSeconds"] for r in runs), "shards": len(runs),
            "exactTried": 0, "exactSeconds": 0, "traversal": "dag"}
        json.dump(run, open(O / "run.json", "w"), indent=1)
        # keys for exact?: recurring, not a typeclass, no library hash match (as in Rosette/Reuse.lean)
        agg = {}
        seen = set()
        for line in open(O / "candidates.jsonl"):
            r = json.loads(line)
            if r["record"] != "candidate" or r["role"] == "root":
                continue
            k = (r["decl"], r["stmtHash"], r["proofHash"])
            if k in seen:
                continue
            seen.add(k)
            a = agg.setdefault(r["stmtHash"], {"decls": set(), "sum": 0, "max": 0, "cls": False})
            a["decls"].add(r["decl"])
            a["sum"] += r["proofSizeDag"]
            a["max"] = max(a["max"], r["proofSizeDag"])
            a["cls"] = a["cls"] or r["stmtIsClass"]
        todo = [(a["sum"] - a["max"], h) for h, a in agg.items()
                if len(a["decls"]) >= 2 and not a["cls"] and not stm[h]["inLib"]]
        todo.sort(key=lambda t: (-t[0], t[1]))
        keys = [h for _, h in todo[:EXACT_CAP]]
        kd, ncand = _key_decls(O)
        n = _cover(keys, kd, ncand, shards, "exact_keys.json")
        run["exactEligible"] = len(todo)
        run["exactTried"] = n
        json.dump(run, open(O / "run.json", "w"), indent=1)
        print(json.dumps(run, indent=1))
    elif stage == "after-exact":
        shards = _shards(O)
        ex = {}
        for sh in shards:
            if (sh / "exact.jsonl").exists():
                for line in open(sh / "exact.jsonl"):
                    r = json.loads(line)
                    ex[r["stmtHash"]] = r
        rows = []
        for line in open(O / "statements.jsonl"):
            r = json.loads(line)
            if r["stmtHash"] in ex:
                r.update(ex[r["stmtHash"]])
            rows.append(r)
        with open(O / "statements.jsonl", "w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        # second view: a statement that `exact?` closes with a PROJECT lemma is not treated as
        # "already in the library"; it falls through to the later filters (one-lemma if the
        # occurrence simply applies that lemma, substantive if it re-proves it)
        V.mkdir(exist_ok=True)
        for name in ("candidates.jsonl", "lgg.jsonl", "run.json"):
            (V / name).write_bytes((O / name).read_bytes())
        with open(V / "statements.jsonl", "w") as f:
            for r in rows:
                r = dict(r)
                if r.get("exact") == "closed" and r.get("exactLemmaProj"):
                    r["exact"] = "open"
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        keys = set()
        for d in (O, V):
            (d / "probe.jsonl").unlink(missing_ok=True)
            _run_reuse_py(d)
            keys |= set(json.load(open(d / "probe_keys.json"))["keys"])
        kd, ncand = _key_decls(O)
        n = _cover(sorted(keys), kd, ncand, shards, "probe_keys.json")
        print(f"exact? results merged: {Counter(r['exact'] for r in ex.values())}; probe keys: {n}")
    elif stage == "after-probe":
        with open(O / "probe.jsonl", "w") as f:
            for sh in _shards(O):
                if (sh / "probe.jsonl").exists():
                    f.write((sh / "probe.jsonl").read_text())
        (V / "probe.jsonl").write_bytes((O / "probe.jsonl").read_bytes())
        for d in (O, V):
            _run_reuse_py(d)
            s = json.load(open(d / "summary.json"))
            print(d.name, "substantive:", s["substantive"], "E net share:", s["levels"]["E"]["netSavingShare"])
    else:
        raise SystemExit("unknown stage " + stage)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "report"
    if cmd == "cluster":
        cmd_cluster()
    elif cmd == "inproof":
        cmd_inproof(*sys.argv[2:])
    else:
        raise SystemExit("unknown command " + cmd)
