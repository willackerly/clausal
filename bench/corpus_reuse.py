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


# ---------------------------------------------------------------- report helpers


def pct(x, d=1):
    return f"{100 * x:.{d}f}%"


def code(s, n=200):
    s = " ".join(s.split())
    s = s if len(s) <= n else s[:n] + " …"
    return "`" + s.replace("`", "'").replace("|", "∣") + "`"


def short(n):
    """Readable name: drop the private prefix."""
    if n.startswith("_private."):
        n = n.split(".0.", 1)[1] + " (private)"
    return n


def load_all_decls():
    A = {}
    for line in open(NS / "decls.jsonl"):
        d = json.loads(line)
        A[d["name"]] = d
    return A


def reachable(A, roots):
    seen = set()
    stack = [r for r in roots if r in A]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        d = A[n]
        stack.extend(x for x in d["typeDeps"] + d["valueDeps"] if x not in seen)
    return seen


def factor_results():
    res = {}
    for f in sorted((OUT / "factor").glob("F*.jsonl")):
        rows = [json.loads(l) for l in open(f)]
        res[f.stem] = rows
    return res


def removable_union(D, K, keys):
    """Theorems that go away if every cluster of every key in `keys` keeps one member
    (union-find over the clusterings)."""
    parent = {n: n for n in D}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for key in keys:
        for v in clusters(D, K, key).values():
            for n in v[1:]:
                parent[find(n)] = find(v[0])
    comp = defaultdict(list)
    for n in D:
        comp[find(n)].append(n)
    removed = []
    for v in comp.values():
        if len(v) > 1:
            keep = max(v, key=lambda n: D[n]["proofSize"])
            removed += [n for n in v if n != keep]
    return removed


# ---------------------------------------------------------------- report

FACTOR_DOC = {
    "F1_ExactDuplicates": ("exact-statement duplicates, whole corpus",
                           "each member is re-proved by the bare constant of one representative; then the two "
                           "largest clusters are re-proved from ONE freshly written lemma each"),
    "F2_CylinderAlgebra": ("a threshold proved twice (`q ≥ 6` and `q ≥ 5`)",
                           "no new lemma needed: each `q ≥ 6` theorem is one line from its `q ≥ 5` twin, which "
                           "the corpus proves by copying the proof"),
    "F3_SobolevOrder": ("one estimate for two Sobolev orders (3 and 6)",
                        "NEW general lemma `ReuseFactor.sobolevNorm_le_pure_derivatives (d s : ℕ)` (39 lines, the "
                        "order-6 proof with `6` replaced by `s` and the weight inequality as a hypothesis); both "
                        "originals follow by `simpa`"),
    "F4_NaturalAxis": ("a parameter range proved twice (`SmallParameters` and the wider `Parameters`)",
                       "no new lemma needed: the narrow version is the wide one composed with the existing "
                       "`ofSmall`; pairs whose conclusions carry different numerical constants cannot follow"),
    "F5_LambdaPower": ("one inequality for two exponents (`lam ^ 28 ≤ lam`, `lam ^ 29 ≤ lam`)",
                       "NEW general lemma `ReuseFactor.lam_pow_le_self (d) (hn : n ≠ 0) : d.core.lam ^ n ≤ d.core.lam` "
                       "(one line from Mathlib's `pow_le_of_le_one`)"),
    "F6_ClonedModules": ("theorems of the 13 cloned modules against their originals",
                         "the ORIGINAL theorem as a bare constant is offered as proof of the copy; this can only "
                         "succeed when the copied definitions in the statement unfold to the originals"),
}


def cmd_report():
    D, K = load()
    A = load_all_decls()
    lv = json.load(open(OUT / "decl_levels.json"))
    dump = json.load(open(OUT / "decl_clusters.json"))
    judge = json.load(open(OUT / "judgements.json"))
    fac = factor_results()
    samples = json.load(open(OUT / "samples.json"))
    mains = [m["name"] for m in json.load(open(NS / "main_theorems.json"))["mainTheorems"]]
    R = reachable(A, mains)
    n_thm = len(D)
    tot_proof = lv["totalProofSize"]
    tot_lines = lv["totalLines"]
    src_lines = sum(sum(1 for _ in open(p)) for lib in ("NavierStokes", "Euler") for p in (SRC / lib).rglob("*.lean"))
    L = []
    w = L.append

    def lvl(short):
        return lv["levels"][short]

    # ---------- declaration level: tables
    T1 = []
    T1.append("| key | what is identified | clusters | theorems in clusters | removable (members − 1) | "
              "… of all theorems | largest | span ≥ 2 modules | proof size of the removable | their source lines |")
    T1.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for key, short_, doc in LEVELS + JOINT:
        r = lvl(short_)
        T1.append(f"| {short_} | {doc} | {r['clusters']} | {r['theorems']} | {r['removable']} | "
                  f"{pct(r['removable'] / n_thm)} | {r['largest']} | {r['crossModule']} | "
                  f"{pct(r['removableProofShare'], 2)} | {r['removableLines']} ({pct(r['removableLinesShare'], 2)}) |")
    T2 = ["| members | " + " | ".join(s for _, s, _ in LEVELS + JOINT) + " |",
          "|---|" + "---:|" * len(LEVELS + JOINT)]
    for b in ("2", "3", "4-9", "10-19", "20+"):
        T2.append(f"| {b} | " + " | ".join(str(lvl(s)["hist"].get(b, 0)) for _, s, _ in LEVELS + JOINT) + " |")

    def new_at(short_, finer_key):
        """clusters at this level that are not already clusters at the finer key"""
        return [r for r in dump[short_] if len({K[n][finer_key] for n in r["members"]}) >= 2]

    def examples(rows, k, by="size"):
        out = []
        rows = sorted(rows, key=lambda r: (-r["size"], -max(r["proofSizes"]))) if by == "size" else \
            sorted(rows, key=lambda r: -sum(r["proofSizes"]))
        for r in rows[:k]:
            ms = r["members"]
            out.append(f"- {r['size']} theorems, {r['modules']} module(s), proof sizes "
                       f"{sorted(r['proofSizes'], reverse=True)[:4]}{' …' if r['size'] > 4 else ''}, "
                       f"{r['distinctProofsUpToRenaming']} distinct proof(s) up to renaming:")
            for n in ms[:2]:
                out.append(f"  - {code(D[n]['statement'], 230)}")
        return out

    newN = new_at("N", "kE")
    newPerm = new_at("E+perm", "kE")
    newL = new_at("L", "kN")
    newP = new_at("P", "kN")
    newN_sameproof = [r for r in newN if r["distinctProofsUpToRenaming"] == 1]
    clone_pairs = json.load(open(OUT / "factor/clone_modules.json"))
    clone_mods = {m for pr in clone_pairs for m in pr}
    svp = dump["SV-P"]
    svp_dup = [r for r in svp if r["distinctExact"] == 1]
    svp_clone = [r for r in svp if r["distinctExact"] > 1 and any(D[n]["module"] in clone_mods for n in r["members"])]
    svp_other = [r for r in svp if r["distinctExact"] > 1 and not any(D[n]["module"] in clone_mods for n in r["members"])]

    def rem_lines(rows):
        t = 0
        for r in rows:
            keep = max(r["members"], key=lambda n: D[n]["proofSize"])
            t += sum(lines_of(D[n]) for n in r["members"] if n != keep)
        return t

    # ---------- factoring table
    TF = ["| experiment | what | members checked | follow (kernel) | failed | source lines of the members that follow | how |",
          "|---|---|---:|---:|---:|---:|---|"]
    fac_tot_ok = 0
    fac_summary = {}
    for name, rows in fac.items():
        if name == "F1_ExactDuplicates":
            groups = [("F1a", "exact duplicates, by representative constant", [r for r in rows if r["tag"] == "dup"]),
                      ("F1b", "`nat_le_infty` (83 copies) from one new lemma", [r for r in rows if r["tag"] == "nat_le_infty"]),
                      ("F1c", "`Fact (0 < 1)` (22 copies) from one new lemma", [r for r in rows if r["tag"] == "fact_zero_lt_one"])]
        else:
            groups = [(name.split("_")[0], FACTOR_DOC[name][0], rows)]
        for tag, what, rs in groups:
            ok = [r for r in rs if r["ok"]]
            bad = [r for r in rs if not r["ok"]]
            ln = sum(lines_of(D[r["member"]]) for r in ok if r["member"] in D)
            how = FACTOR_DOC[name][1] if tag in ("F1a",) or not tag.startswith("F1") else "see F1a"
            TF.append(f"| {tag} | {what} | {len(rs)} | {len(ok)} | {len(bad)} | {ln} | {how} |")
            fac_summary[tag] = {"checked": len(rs), "ok": len(ok), "failed": len(bad), "lines": ln,
                                "failNotes": dict(Counter(r["note"][:70] for r in bad))}
            if tag != "F1b" and tag != "F1c":
                fac_tot_ok += len(ok)

    # ---------- cloned modules
    TC = ["| clone module | lines | base module | lines | theorems (clone) | twins of a base theorem | "
          "copy proved by the original constant | declarations of the clone used by a headline theorem |",
          "|---|---:|---|---:|---:|---:|---:|---:|"]
    f6 = {r["member"]: r["ok"] for r in fac.get("F6_ClonedModules", [])}
    clone_lines = 0
    clone_thms = 0
    for base, clone in clone_pairs:
        lc = sum(1 for _ in open(SRC / (clone.replace(".", "/") + ".lean")))
        lb = sum(1 for _ in open(SRC / (base.replace(".", "/") + ".lean")))
        tc = [n for n, d in D.items() if d["module"] == clone]
        tw = [n for n in tc if n in f6]
        used = sum(1 for n, d in A.items() if d["module"] == clone and n in R)
        clone_lines += lc
        clone_thms += len(tc)
        TC.append(f"| `{clone}` | {lc} | `{base.split('.')[-1]}` | {lb} | {len(tc)} | {len(tw)} | "
                  f"{sum(1 for n in tw if f6[n])} | {used} |")

    # ---------- removal estimate
    rem_E = removable_union(D, K, ["kE"])
    rem_SV = removable_union(D, K, ["kE", "svP"])
    rem_P = removable_union(D, K, ["kE", "svP", "kLP"])

    def share(names):
        return (len(names), sum(lines_of(D[n]) for n in names),
                sum(D[n]["proofSize"] for n in names) / tot_proof, sum(1 for n in names if n in R))
    unreach = [n for n in D if n not in R]

    # ---------- in-proof
    def load_sample(name):
        d = OUT / f"inproof_{name}"
        if not (d / "summary.json").exists():
            return None
        s = json.load(open(d / "summary.json"))
        s["run"] = json.load(open(d / "run.json"))
        s["clusters"] = json.load(open(d / "clusters.json"))["E"]
        decls = [json.loads(l) for l in open(d / "candidates.jsonl") if '"record":"decl"' in l]
        s["truncatedDecls"] = sum(1 for r in decls if r["truncated"])
        s["medianProof"] = statistics.median(r["proofSizeDag"] for r in decls)
        s["truncNotes"] = dict(Counter((r["note"] or "")[:40] for r in decls if r["truncated"]))
        return s
    ml = json.load(open(ROOT / "out/reuse/summary.json"))
    ml["run"] = json.load(open(ROOT / "out/reuse/run.json"))
    ml["truncatedDecls"] = ml["run"]["truncated"]
    cols = [("Mathlib (human)", ml)]
    for nm, label in (("dense", "NS/Euler, dense sample"), ("uniform", "NS/Euler, uniform sample"),
                      ("dense" + VARIANT, "dense, re-proofs counted"), ("uniform" + VARIANT, "uniform, re-proofs counted")):
        sm = load_sample(nm)
        if sm:
            cols.append((label, sm))
    TI = ["| | " + " | ".join(c for c, _ in cols) + " |", "|---|" + "---:|" * len(cols)]

    def row(label, f):
        TI.append(f"| {label} | " + " | ".join(str(f(s)) for _, s in cols) + " |")
    row("theorems", lambda s: s["theorems"])
    row("… truncated by a budget", lambda s: s["truncatedDecls"])
    row("total proof size (DAG nodes)", lambda s: s["totalTheoremProofSize"])
    row("candidate occurrences", lambda s: s["occurrences"])
    row("distinct closed statements", lambda s: s["levels"]["E"]["clusters"])
    row("recurring statements (≥ 2 theorems)", lambda s: s["levels"]["E"]["recurring"])
    row("… share of occurrences", lambda s: pct(s["levels"]["E"]["shareOfOccurrences"]))
    row("theorems with ≥ 1 recurring statement", lambda s: s["levels"]["E"]["theoremsWithRecurring"])
    row("recurring, spanning ≥ 2 modules", lambda s: s["levels"]["E"]["crossModule"])
    row("upper estimate: net saving of all exact recurrence", lambda s: pct(s["levels"]["E"]["netSavingShare"]))
    row("trivial-class share of recurring statements",
        lambda s: pct(1 - s["substantive"]["clusters"] / max(1, s["levels"]["E"]["recurring"])))
    row("substantive recurring statements", lambda s: s["substantive"]["clusters"])
    row("… with positive net saving", lambda s: s["substantive"]["netPositive"])
    row("… of those, spanning ≥ 2 modules", lambda s: s["substantive"]["crossModule"])
    row("… of those, identical proof term everywhere", lambda s: s["substantive"]["sameProof"])
    row("**substantive net saving, nodes**", lambda s: s["substantive"]["netSaving"])
    row("**… as share of proof size (headline)**", lambda s: "**" + pct(s["substantive"]["netSavingShare"], 2) + "**")
    row("`exact?`: closed / open / timeout",
        lambda s: f"{s['exactQ'].get('closed', 0)} / {s['exactQ'].get('open', 0)} / {s['exactQ'].get('timeout', 0)}")
    row("one-tactic probe: tried / closed", lambda s: f"{s['probe']['tried']} / {s['probe']['closed']}")
    CL = ["instance", "in-mathlib", "exact?", "no-lemma", "one-lemma", "automation-glue",
          "tactic-certificate", "side-goal", "in-mathlib-L1", "one-tactic", "substantive"]
    TK = ["| class | " + " | ".join(f"{c}: clusters | net saving" for c, _ in cols) + " |",
          "|---|" + "---:|---:|" * len(cols)]
    for c in CL:
        TK.append(f"| {c} | " + " | ".join(
            f"{s['classes'][c]['clusters']} | {pct(s['classes'][c]['netSaving'] / s['totalTheoremProofSize'], 2)}"
            for _, s in cols) + " |")

    n_circ = 0
    for line in open(OUT / "factor/dups.jsonl"):
        r = json.loads(line)
        Rrep = reachable(A, [r["rep"]])
        for m in r["members"]:
            if m in Rrep or r["rep"] in reachable(A, [m]):
                n_circ += 1
    facts = {
        "dupsDerivedFromEachOther": n_circ,
        "theorems": n_thm, "totalProofSize": tot_proof, "theoremLines": tot_lines, "sourceLines": src_lines,
        "levels": lv["levels"], "newN": len(newN), "newN_theorems": sum(r["size"] for r in newN),
        "newN_sameProof": len(newN_sameproof), "newPerm": len(newPerm),
        "newPerm_theorems": sum(r["size"] for r in newPerm), "newL": len(newL), "newP": len(newP),
        "LP_sameProofUpToRenaming": lv["LP_sameProofUpToRenaming"], "LP_allProofsDifferent": lv["LP_allProofsDifferent"],
        "svp": {"dup": [len(svp_dup), sum(r["size"] - 1 for r in svp_dup), rem_lines(svp_dup)],
                "clone": [len(svp_clone), sum(r["size"] - 1 for r in svp_clone), rem_lines(svp_clone)],
                "other": [len(svp_other), sum(r["size"] - 1 for r in svp_other), rem_lines(svp_other)]},
        "factor": fac_summary, "cloneLines": clone_lines, "cloneTheorems": clone_thms,
        "removal": {"E": share(rem_E), "E+SV": share(rem_SV), "E+SV+LP": share(rem_P),
                    "unreachable": share(unreach)},
        "top20yes": sum(1 for t in judge["top20"] if t["verdict"] == "yes"),
        "inproof": {c: {"headline": s["substantive"]["netSavingShare"], "upper": s["levels"]["E"]["netSavingShare"],
                        "substantive": s["substantive"]} for c, s in cols},
    }
    json.dump(facts, open(OUT / "report_facts.json", "w"), indent=1, ensure_ascii=False)
    return dict(D=D, K=K, A=A, R=R, lv=lv, dump=dump, judge=judge, fac=fac, samples=samples, facts=facts,
                T1=T1, T2=T2, TF=TF, TC=TC, TI=TI, TK=TK, cols=cols, examples=examples,
                newN=newN, newPerm=newPerm, newL=newL, newP=newP, newN_sameproof=newN_sameproof,
                svp_other=svp_other, share=share, rem_E=rem_E, rem_SV=rem_SV, rem_P=rem_P, unreach=unreach)


def write_report(c):
    D, K, f, judge = c["D"], c["K"], c["facts"], c["judge"]
    lv = f["levels"]
    n_thm = f["theorems"]
    L = []
    w = L.append
    rem = f["removal"]
    fs = f["factor"]
    cols = c["cols"]
    ip = f["inproof"]

    def ipv(label, field="headline"):
        return ip[label][field] if label in ip else None

    w("# Recurrence in a machine-generated corpus (OpenAI Navier–Stokes / Euler)")
    w("")
    w("Generated by `bench/corpus_reuse.py report`. Numbers come from Lean dumps "
      "(`out/corpus/ns/decls.jsonl`, `out/corpus/reuse/stmt_keys.jsonl`, `out/corpus/reuse/inproof_*/`, "
      "`out/corpus/reuse/factor/*.jsonl`); the judgements on clusters are hand-entered in "
      "`out/corpus/reuse/judgements.json` and marked as such. Corpus: `openai/NavierStokesAndEuler` at "
      f"`f9e8bc5`, Lean 4.34.0-rc2, {n_thm} theorems, {f['sourceLines']} source lines "
      f"({f['theoremLines']} of them inside theorem declarations), total theorem proof size "
      f"{f['totalProofSize']} DAG nodes.")
    w("")
    w("## Verdict")
    w("")
    w(VERDICT.format(**c["verdict_args"]))
    w("")
    w("## 1. Declaration level: all theorem statements of the corpus")
    w("")
    w("### 1.1 Keys")
    w("")
    w("Every key is a 64-bit structural hash of the theorem's type computed by "
      "`corpora/ns_reuse/StmtKeys.lean` from the built environment. All keys ignore binder names, binder "
      "kinds, `mdata` and universe levels.")
    w("")
    w("- **E** exact statement.")
    w("- **N** numeric literals abstracted: `@OfNat.ofNat T n inst` becomes `NUM(T)`, any other raw literal `LIT`.")
    w("- **L** N, plus every constant standing without arguments in an argument position is a numbered hole "
      "(first-occurrence numbering, so the renaming is consistent). One level of leaf abstraction: types, "
      "instances and named constants are leaves, heads of applications are kept.")
    w("- **P** N, plus every constant declared in the project is a numbered hole wherever it occurs, heads "
      "included. Equal P means: same statement after renaming project definitions and changing numerals. A head "
      "is a second-order parameter, so the common generalisation need not be true.")
    w("- **LP** both. This is the approximation of anti-unification used below.")
    w("- **+perm** the same key made invariant under reordering of binders: a binder whose variable occurs "
      "nowhere else (a hypothesis, an unused variable) is *floating*; the key hashes the conclusion, the other "
      "binder types with variables numbered by first occurrence, and the sorted multiset of floating binders. "
      "Equal keys imply equality up to binder order; the numbering is a heuristic, so some pairs can be missed.")
    w("- **SV-E / SV-N / SV-P** joint keys of statement AND proof term: identical; identical up to numerals; "
      "identical up to one consistent renaming of project constants in statement and proof, where each renamed "
      "constant must also agree in kind and in the shape of its own type. SV-P says the two theorems are the "
      "same derivation from parallel ingredients.")
    w("")
    w("### 1.2 Clusters by key")
    w("")
    w("*Removable* = members minus one per cluster: what disappears if one statement (or one general lemma) "
      "replaces the cluster. Proof-size and line shares keep the member with the largest proof.")
    w("")
    L.extend(c["T1"])
    w("")
    w("Clusters by number of members:")
    w("")
    L.extend(c["T2"])
    w("")
    w(f"- **Exact duplicates are rare**: {lv['E']['removable']} removable theorems "
      f"({pct(lv['E']['removable'] / n_thm)}), {pct(lv['E']['removableProofShare'], 2)} of proof size. Only "
      f"{lv['SV-E']['removable']} of them also have an identical proof term; the rest are the same statement "
      "proved again by another route.")
    w("- The four largest binder-order-only clusters are a theorem and its own `_aux` restatement with the "
      "binders in another order, i.e. not independent proofs.")
    w(f"- **Permuted hypotheses add little**: {f['newPerm']} clusters ({f['newPerm_theorems']} theorems) are equal "
      "only up to binder order.")
    w(f"- **Numerals add little**: {f['newN']} clusters ({f['newN_theorems']} theorems) differ only in numeric "
      f"literals; in {f['newN_sameProof']} of them the proofs also agree up to renaming, which is the pattern "
      "\"same estimate proved for several exponents\".")
    w(f"- **Renaming project constants adds a lot, and most of it is not redundancy**: P has "
      f"{lv['P']['clusters']} clusters covering {lv['P']['theorems']} theorems ({pct(lv['P']['theorems'] / n_thm)}). "
      f"Of the {lv['LP']['clusters']} LP clusters, {f['LP_sameProofUpToRenaming']} have the same proof up to "
      f"renaming and {f['LP_allProofsDifferent']} have pairwise different proofs. See 1.4.")
    w("")
    w("### 1.3 Examples")
    w("")
    w("Largest clusters that exist at N but not at E (numerals only), by total proof size:")
    w("")
    L.extend(c["examples"](c["newN"], 6, by="proof"))
    w("")
    w("Largest clusters that exist only up to binder order:")
    w("")
    L.extend(c["examples"](c["newPerm"], 4, by="proof"))
    w("")
    w("Largest clusters that exist at L but not at N (a leaf constant differs):")
    w("")
    L.extend(c["examples"](c["newL"], 4))
    w("")
    w("### 1.4 The 20 largest clusters (key LP), judged from the source")
    w("")
    w("Hand judgement by the analysing agent after reading members' source; not reviewed by a mathematician.")
    w("")
    w("| # | members | distinct exact statements | distinct proofs up to renaming | example member | one general lemma? | why |")
    w("|---:|---:|---:|---:|---|---|---|")
    by_key = {r["key"]: r for r in c["dump"]["LP"]}
    for i, t in enumerate(judge["top20"], 1):
        r = by_key[t["key"]]
        w(f"| {i} | {r['size']} | {r['distinctExact']} | {r['distinctProofsUpToRenaming']} | "
          f"{code(D[r['members'][0]]['statement'], 110)} | **{t['verdict']}** | {t['note']} |")
    w("")
    w(f"{f['top20yes']} of 20 can be replaced by one lemma, and both are exact duplicates. The other "
      f"{20 - f['top20yes']} are *attribute families*: the same property (positivity, non-negativity, smoothness, "
      "an evaluation identity) stated for many different definitions. Their anti-unifier (`∀ c, 0 < c`, "
      "`∀ f, ContDiff ℝ ∞ f`) is false, and the proofs are different. Statement shape alone therefore "
      "over-counts parameterised redundancy by an order of magnitude; the joint key SV-P is the usable estimate.")
    w("")
    w("### 1.5 How many theorems are instances of a common parameterised statement")
    w("")
    sv = f["svp"]
    w("| estimate | clusters | removable theorems | source lines | status |")
    w("|---|---:|---:|---:|---|")
    w(f"| statement shape (LP), upper bound | {lv['LP']['clusters']} | {lv['LP']['removable']} | "
      f"{lv['LP']['removableLines']} | not usable: 18 of the 20 largest are attribute families |")
    w(f"| same derivation (SV-P), all | {lv['SV-P']['clusters']} | {lv['SV-P']['removable']} | "
      f"{lv['SV-P']['removableLines']} | candidate; splits into the three rows below |")
    w(f"| … identical statement as well | {sv['dup'][0]} | {sv['dup'][1]} | {sv['dup'][2]} | "
      "exact duplicates, kernel-checked in F1 |")
    w(f"| … a member lies in a cloned module | {sv['clone'][0]} | {sv['clone'][1]} | {sv['clone'][2]} | "
      "dead copies, see 1.7 |")
    w(f"| … other (different statements, live modules) | {sv['other'][0]} | {sv['other'][1]} | {sv['other'][2]} | "
      "sampled by hand below; F2–F5 kernel-check 31 members |")
    w(f"| numerals only (N, not E) with the same proof up to renaming | {f['newN_sameProof']} | "
      f"{sum(r['size'] - 1 for r in c['newN_sameproof'])} | | F2, F3, F5 are of this kind |")
    w("")
    s_ = judge["svpSample"]
    w(f"Hand reading of a seeded sample of {s_['sampled']} of the {sv['other'][0]} \"other\" SV-P clusters: "
      f"{s_['sharedHelperOrClonedDefinition']} are copies of a helper or of a lemma about a locally re-declared "
      f"definition, {s_['siblingOneLiners']} are sibling one- to four-line lemmas about parallel fields or "
      f"components (forward/backward, angular/axial) where a common lemma is possible but saves no text, "
      f"{s_['indexable']} is one computation repeated for two indices. The median member of these clusters is "
      "4 source lines long.")
    w("")
    w("### 1.6 Factoring that was actually done (kernel-checked)")
    w("")
    w("Lean files: `corpora/ns_reuse/Factor/F1..F6_*.lean`, run by `corpora/ns_reuse/run_factor.sh`. The "
      "command `#follows` (`corpora/ns_reuse/ReuseCheck.lean`) elaborates the given proof term against exactly "
      "the member's type, refuses `sorry` and any term that mentions the member, sends the new theorem through "
      "the kernel synchronously, and requires its axioms to be within `propext`, `Classical.choice`, "
      "`Quot.sound`. The corpus sources are not modified: this shows that each member FOLLOWS from the general "
      "statement, it does not rebuild the corpus with the member deleted.")
    w("")
    L.extend(c["TF"])
    w("")
    w(f"- **F1.** {fs['F1a']['ok']} of {fs['F1a']['checked']} duplicates are proved by a bare reference to "
      f"another copy. The {fs['F1a']['failed']} failures have a different number of universe parameters "
      "(the key ignores universe levels; one copy is stated for `Type`, the other for `Type u`), so the "
      f"mechanical term does not apply. In {f['dupsDerivedFromEachOther']} of the {fs['F1a']['checked']} pairs "
      "the corpus itself proves one copy from the other (a restatement under a second name).")
    w("- **F3 and F5 are the two cases where a new general lemma had to be written.** Both compiled on the "
      "first attempt. F3 is a real proof (39 lines, Fourier-side Sobolev estimate); the generalisation consisted "
      "of replacing the numeral by a variable and turning the one order-specific ingredient into a hypothesis.")
    w(f"- **F2 and F4 need no new lemma**: the corpus already contains the general statement and proves the "
      f"special one again by copying. F4 fails on {fs['F4']['failed']} of {fs['F4']['checked']} pairs, as it must: "
      "those pairs have the same proof shape but different numerical constants in the conclusion "
      "(`A h ≤ 501/1000` against `A h ≤ 51/100`), which the numeral-abstracting key cannot tell apart. "
      "This is a measured false-positive rate of SV-P on one family: 3 of 21.")
    w(f"- **F6** is the control for the harness as well: {fs['F6']['failed']} of {fs['F6']['checked']} copies are "
      "rejected by the kernel with a type mismatch, because their statements mention a copied structure.")
    w("- A first version of the harness used `Lean.addDecl`, which on this toolchain checks asynchronously and "
      "only logs a kernel error; it reported 312 of 312 for F6. The numbers above are from the corrected, "
      "synchronous check; F1–F5 were rerun with it and did not change.")
    w("")
    w("### 1.7 Cloned modules")
    w("")
    w("Thirteen modules named `…NoOptions` or `…Investigation` are copies of a base module under a new "
      "namespace (the header of the largest says it is an independent copy made to remove a heartbeat override).")
    w("")
    L.extend(c["TC"])
    w("")
    w(f"Together {f['cloneLines']} lines ({pct(f['cloneLines'] / f['sourceLines'], 2)} of the source) and "
      f"{f['cloneTheorems']} theorems. **No declaration of any clone is used by a headline theorem**: they are "
      "dead code, and removing them needs no generalisation.")
    w("")
    w("### 1.8 What a deduplication / generalisation pass could remove")
    w("")
    w("| pass | theorems removed | of all theorems | source lines | of theorem lines | proof size | of them reachable from a headline theorem |")
    w("|---|---:|---:|---:|---:|---:|---:|")
    for label, key in (("exact duplicates (E)", "E"), ("E + same derivation (SV-P), optimistic", "E+SV"),
                       ("E + SV-P + statement shape (LP): NOT achievable, shown for scale", "E+SV+LP"),
                       ("for comparison: theorems not used by any headline theorem", "unreachable")):
        n, ln, ps, rc = rem[key]
        w(f"| {label} | {n} | {pct(n / n_thm)} | {ln} | {pct(ln / f['theoremLines'])} | {pct(ps, 2)} | {rc} |")
    w("")
    w("The SV-P row is optimistic for three reasons: it counts a member as removed although a call to the "
      "general lemma remains (one to three lines against a median of four); F4 shows a false-positive rate of "
      "3 in 21 on the one family that was checked completely; and where the renamed constants are definitions "
      "the general lemma needs them as parameters with hypotheses, which was only done by hand in F3 and F5.")
    w("")
    w("## 2. Inside proofs: sampled theorems")
    w("")
    sm = c["samples"]
    w("Method of `out/reuse/REUSE.md` (the Mathlib run): every Prop-typed proof subterm with proof DAG size ≥ 20 "
      "is closed over the local hypotheses it uses; closed statements are hashed; a statement is *recurring* if it "
      "occurs in ≥ 2 theorems; each recurring statement gets the first trivial class that applies; the headline is "
      "the net saving of the statements no filter explains, as a share of total proof size. The Lean code is "
      "`Rosette/Candidates.lean` + `Rosette/Reuse.lean` copied into `corpora/ns_reuse/ReuseNS.lean` by "
      "`mk_reuse_ns.py` (it compiled on Lean 4.34 without API changes); the classification is `bench/reuse.py`, "
      "unchanged.")
    w("")
    w(f"- **Population**: theorems with proof DAG size ≥ 800, the Mathlib threshold: {sm['eligible']} of "
      f"{sm['theorems']} theorems, carrying {pct(sm['eligibleProofSize'] / sm['theoremProofSize'])} of all "
      "theorem proof size.")
    w(f"- **Uniform sample**: 500 drawn uniformly (seed {sm['seed']}).")
    dn = sm["dense"]
    w(f"- **Dense sample**: all eligible theorems of consecutive modules (sorted by name) from a seeded start, "
      f"until ≥ 250 per library: {dn['NavierStokes']['theorems']} from {len(dn['NavierStokes']['modules'])} "
      f"NavierStokes modules (`{dn['NavierStokes']['modules'][0].split('.')[-1]}` … "
      f"`{dn['NavierStokes']['modules'][-1].split('.')[-1]}`), {dn['Euler']['theorems']} from "
      f"{len(dn['Euler']['modules'])} Euler modules. The Mathlib run took all eligible theorems of three "
      "directory slices, so the dense sample is the like-for-like one; the uniform sample shows what "
      "recurrence between unrelated theorems looks like.")
    w("- **Differences from the Mathlib run**, all forced: (a) the traversal is DAG-aware. The original walks the "
      "proof term as a tree; on these terms a third of the first 129 theorems hit the 300,000-visit budget with "
      "proof DAG sizes of 1–3 thousand. Here a subterm met again inside one theorem is not re-entered; if it is "
      "a candidate, its extra position is still recorded. Nested candidates lose their extra positions, which "
      "can only lower the saving. (b) `exact?` searches the whole environment, which here includes the project's "
      "own lemmas; the columns \"re-proofs counted\" undo that: a statement closed by a PROJECT lemma is not "
      "treated as trivial and falls through to the later filters. (c) The anti-unifier pass (levels L1/L2 of the "
      "Mathlib report) was not run.")
    w("")
    L.extend(c["TI"])
    w("")
    w("Recurring statements by class (first matching class; net saving as share of the sample's proof size):")
    w("")
    L.extend(c["TK"])
    w("")
    w("The two \"re-proofs counted\" columns add substantive clusters but none with a positive net saving, so "
      "their top lists are the same as the strict ones and are not repeated.")
    w("")
    for label, s in cols[1:3]:
        subs = sorted((r for r in s["clusters"] if r["class"] == "substantive" and r.get("subNet", 0) > 0),
                      key=lambda r: -r["subNet"])
        if not subs:
            continue
        w(f"### Substantive recurring statements with the largest net saving — {label}")
        w("")
        w("| net | theorems | modules | proof (max) | same proof | statement | where |")
        w("|---:|---:|---:|---:|---|---|---|")
        for r in subs[:12]:
            ds = r["decls"]
            w(f"| {r['subNet']} | {r['theorems']} | {r['modules']} | {r['maxProof']} | "
              f"{'yes' if r['sameProof'] else 'no'} | {code(r['statement'], 190)} | "
              f"`{short(ds[0])}`, `{short(ds[1])}`{' +' + str(len(ds) - 2) if len(ds) > 2 else ''} |")
        w("")
    w("## 3. Limits")
    w("")
    for t in LIMITS:
        w("- " + t)
    w("")
    w("## 4. Review notes (2026-11-10)")
    w("")
    w("An independent reviewing agent recomputed the cluster table from `stmt_keys.jsonl` (all keys reproduce), the "
      "468 kernel-accepted theorems and the E + SV-P union bound, and reran F2 to F5 on Lean 4.34.0-rc2. Its findings "
      "were all minor; none changes a conclusion. They are recorded here rather than folded into the tables.")
    w("")
    w("- **The E + SV-P removal bound is about twice what is realistic.** In a seeded sample of 20 same-derivation "
      "clusters with differing statements the reviewer found 9 true copies (cloned-module pairs, `q ≥ 5`/`q ≥ 6` twins, "
      "a narrow/wide parameter pair) and 11 sibling lemmas about different definitions, where one general lemma would "
      "have to quantify over the definition and its properties; two of the 11 differ in the conclusion itself. This "
      "agrees with the 14-cluster sample in `judgements.json` (5 copies, 1 same computation for two indices, 8 "
      "siblings). Read the bound as: at most the "
      "figure in the table, realistically about half of it.")
    w("- **Two totals are in use for the in-proof \"substantive\" class.** In the dense sample the headline row "
      "sums 1,556 nodes of net saving (0.15% of proof size, 17 statements with positive saving); the class table "
      "sums 1,193 nodes (0.11%; the reviewer counts 14 statements with positive saving under that definition). The "
      "reviewer reports the same gap in the Mathlib column (0.20% against 0.18%). "
      "The two definitions live in `bench/reuse.py` and were not unified here because that script belongs to the "
      "Mathlib run. Either figure supports the same reading: the same magnitude as Mathlib, and small.")
    w("- **Indirect circularity.** `#follows` only checks that a derived proof does not mention the member it "
      "replaces directly. The reviewer added a transitive check over project constants to copies of F2 to F5: 31 "
      "derived theorems, none reaches its member, all types equal the member's. F1 and F6 were not rerun with that "
      "check; section 1 already notes that in 8 duplicate pairs the corpus itself proves one copy from the other.")
    w("- **Not rerun in the review:** the in-proof pipeline and the Mathlib comparison figures.")
    w("")
    w("## 5. Files")
    w("")
    for t in FILES:
        w("- " + t)
    w("")
    (OUT / "REUSE.md").write_text("\n".join(L) + "\n")
    print("wrote", OUT / "REUSE.md", len(L), "lines")


# The numbers are computed; the sentences were written against the run of 2026-11-10 and must be
# re-read if the data changes.
VERDICT = """**Is there materially more redundancy in the machine corpus than in Mathlib? Of the kind this project was \
looking for, no. Of two other kinds, yes.**

1. *Inside proofs, the comparable figure is of the same size, and small.* Non-trivial recurring statements are worth \
**{dense_head}** of proof size in the dense sample ({dense_n} theorems of neighbouring modules) and \
**{uni_head}** in the uniform sample ({uni_n} theorems), against **{ml_head}** for human-written Mathlib. \
Counting inline re-proofs of the project's own named lemmas as redundancy does not change either figure \
({dense_re}, {uni_re}). (The traversal used here differs from the Mathlib run in a way that can only lower \
the machine figures, see section 2; the comparison is of magnitudes, not of third digits.) {dense_pos} statements in the dense sample would save anything; {dense_same} of them \
have the identical proof term at every occurrence and {dense_cross} cross a module boundary. They are side \
conditions (`t ∈ Ioo 0 T → t ≤ T`, an `eventually` membership, arithmetic on indices), not lemmas. \
The hypothesis recorded in `out/reuse/REUSE.md`, that a generator which never names a fact would repeat \
substantive sub-proofs, is **not supported**.
2. *Raw term-level recurrence is two to three times higher, and it is automation residue.* Replacing every \
repeated closed statement by a call would remove at most {dense_up} (dense) and {uni_up} (uniform) of the \
proof terms, against {ml_up} in Mathlib; {dense_triv} of the recurring statements fall in a trivial class \
(`ring` normal forms, typeclass instances, statements `exact?` closes). This matters for term size and \
checking time, not for readability, and the DAG-aware traversal used here can only understate it.
3. *At declaration level, exact duplication is at the level of human projects.* {e_rem} of {n_thm} theorems \
({e_pct}) restate another theorem exactly; the same count on the human blueprint corpora gives {pfr_pct} \
(PFR) and {carl_pct} (Carleson) with their exporter's hash, which is universe-sensitive and gives 357 here. {f1_ok} of the {e_rem} were re-proved through the kernel by a bare reference \
to another copy.
4. *What is specific to the machine corpus is copy-and-modify instead of generalise.* \
(a) Thirteen modules are namespace-renamed copies of other modules ({clone_lines} lines; the largest is a \
5,573-line copy), all of them dead. \
(b) {sv_other_c} clusters of theorems outside those modules are the same derivation from parallel ingredients \
(same statement and proof term up to renaming project constants): the same estimate for `q ≥ 6` and `q ≥ 5`, for \
Sobolev order 3 and 6, for a narrow and a wide parameter range, for the angular and the axial component; \
by a hand-read sample most of them are sibling lemmas of one to four lines. \
(c) A private helper is restated in 82 modules. \
Statement shape alone is misleading here: {lp_pct} of theorems share their statement up to renaming, but 18 of \
the 20 largest such clusters are families like `0 < c` or `ContDiff ℝ ∞ f` for different definitions, whose \
common generalisation is false.
5. *The factoring goes through.* Six experiments, {kc_total} distinct theorems re-derived and accepted by the \
kernel. Two needed a new general lemma, written here and compiled at the first attempt (a 39-line Sobolev \
estimate for arbitrary order; a one-line power inequality). Two needed none, because the corpus already \
contains the general statement and proves the special case again. Failures are reported: {f4_fail} of \
{f4_n} pairs in one family have different constants in the conclusion, and {f6_fail} of {f6_n} cloned \
theorems mention a cloned structure and cannot be proved by the original.
6. *How much could a deduplication / generalisation pass remove?* With what these keys can find, at most **{esv_n} theorems = {esv_pct} of \
theorems, {esv_lines} of theorem source lines, {esv_proof} of proof size**, and that is optimistic (a call \
replaces each removed member; the median member of the non-duplicate clusters is four lines long). The part \
verified by the kernel is {kc_total} theorems. For scale: {un_n} theorems ({un_pct}) are not used by any of \
the four headline theorems at all, so removing dead declarations is an order of magnitude larger than \
anything deduplication offers. Redundancy is not what makes this corpus hard to read."""
LIMITS = [
    "All keys are 64-bit hashes; collisions were not checked, and no key was validated on hand-made "
    "alpha-equivalent pairs.",
    "L and P are one fixed approximation of anti-unification. P renames heads, so equal keys do not imply "
    "a true common statement; that is why SV-P and the kernel checks are used for every claim of removability.",
    "SV-P requires the WHOLE proof term to be parallel. Two proofs of the same parameterised fact written "
    "differently are missed (the corpus has such pairs: the two `lam ^ n ≤ lam` lemmas of F5 are found only by "
    "the numeral key). SV-P also abstracts numerals, which produced 3 false twins in 21 in F4.",
    "Only theorems are clustered. Duplicated definitions, structures and instances are not counted, although "
    "the cloned modules copy 80 non-theorem declarations as well.",
    "The factoring experiments show that members follow from a general statement. The corpus was not rebuilt "
    "with the members deleted, so knock-on effects (simp sets, name resolution, private scope) are untested.",
    "In-proof: two samples of about 500 from 16,885 eligible theorems. Recurrence between theorems that are "
    "not in the same sample is invisible, so a whole-corpus figure would be higher than either sample's; the "
    "dense sample bounds this for neighbouring modules only.",
    "In-proof: the traversal differs from the Mathlib run (DAG-aware here), the Mathlib figures were not "
    "recomputed, and the class rules are the same name- and text-based heuristics as before.",
    "In-proof: `exact?` and each probe tactic ran with 20,000k heartbeats; a timeout leaves the statement in "
    "whatever later class applies, so the substantive counts are upper bounds on real discoveries.",
    "The judgements in 1.4 and 1.5 were made by the analysing agent, not by a mathematician.",
]
FILES = [
    "`corpora/ns_reuse/StmtKeys.lean` (+ `stmtkeys` binary): statement and proof keys → `out/corpus/reuse/stmt_keys.jsonl`.",
    "`corpora/ns_reuse/mk_reuse_ns.py` → `ReuseNS.lean`: the root project's candidate enumeration ported to the corpus; "
    "`mk_samples.py`, `run_inproof.sh`, `run_inproof_all.sh`: sampling and the sharded pipeline.",
    "`corpora/ns_reuse/ReuseCheck.lean`, `Factor/F1…F6_*.lean`, `run_factor.sh`: the kernel checks; results and logs in "
    "`out/corpus/reuse/factor/`.",
    "`bench/corpus_reuse.py`: clustering (`cluster`), in-proof pipeline stages (`inproof`), this report (`report`).",
    "`out/corpus/reuse/decl_levels.json`, `decl_clusters.json` (every cluster with its members), `judgements.json`, "
    "`report_facts.json`, `samples.json`.",
    "`out/corpus/reuse/inproof_{dense,uniform}/` (strict classes) and `inproof_{dense,uniform}_reproof/`: "
    "`candidates.jsonl`, `statements.jsonl`, `probe.jsonl`, `clusters.json`, `summary.json`, `run.json`.",
]


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "report"
    if cmd == "cluster":
        cmd_cluster()
    elif cmd == "inproof":
        cmd_inproof(*sys.argv[2:])
    elif cmd == "report":
        ctx = cmd_report()
        f = ctx["facts"]
        ip = f["inproof"]
        cols = dict(ctx["cols"])
        dn, un, ml = cols["NS/Euler, dense sample"], cols["NS/Euler, uniform sample"], cols["Mathlib (human)"]
        ok_members = {r["member"] for rows in ctx["fac"].values() for r in rows if r["ok"]}
        human = {}
        for cname in ("pfr", "carleson"):
            g = Counter()
            n = 0
            for line in open(ROOT / "out/corpus" / cname / "decls.jsonl"):
                d = json.loads(line)
                if d["kind"] == "theorem":
                    n += 1
                    g[d["statementHash"]] += 1
            human[cname] = sum(v - 1 for v in g.values() if v > 1) / n
        f["humanExactDuplicateShare"] = human
        f["kernelCheckedMembers"] = len(ok_members)
        json.dump(f, open(OUT / "report_facts.json", "w"), indent=1, ensure_ascii=False)
        lvE = f["levels"]["E"]
        esv = f["removal"]["E+SV"]
        unr = f["removal"]["unreachable"]
        ctx["verdict_args"] = dict(
            dense_head=pct(dn["substantive"]["netSavingShare"], 2), uni_head=pct(un["substantive"]["netSavingShare"], 2),
            ml_head=pct(ml["substantive"]["netSavingShare"], 2), dense_n=dn["theorems"], uni_n=un["theorems"],
            dense_re=pct(cols["dense, re-proofs counted"]["substantive"]["netSavingShare"], 2),
            uni_re=pct(cols["uniform, re-proofs counted"]["substantive"]["netSavingShare"], 2),
            dense_pos=dn["substantive"]["netPositive"], dense_same=dn["substantive"]["sameProof"],
            dense_cross=dn["substantive"]["crossModule"],
            dense_up=pct(dn["levels"]["E"]["netSavingShare"]), uni_up=pct(un["levels"]["E"]["netSavingShare"]),
            ml_up=pct(ml["levels"]["E"]["netSavingShare"]),
            dense_triv=pct(1 - dn["substantive"]["clusters"] / dn["levels"]["E"]["recurring"]),
            e_rem=lvE["removable"], n_thm=f["theorems"], e_pct=pct(lvE["removable"] / f["theorems"]),
            pfr_pct=pct(human["pfr"]), carl_pct=pct(human["carleson"]), f1_ok=f["factor"]["F1a"]["ok"],
            clone_lines=f["cloneLines"], sv_other_c=f["svp"]["other"][0],
            lp_pct=pct(f["levels"]["LP"]["theorems"] / f["theorems"]), kc_total=len(ok_members),
            f4_fail=f["factor"]["F4"]["failed"], f4_n=f["factor"]["F4"]["checked"],
            f6_fail=f["factor"]["F6"]["failed"], f6_n=f["factor"]["F6"]["checked"],
            esv_n=esv[0], esv_pct=pct(esv[0] / f["theorems"]), esv_lines=pct(esv[1] / f["theoremLines"]),
            esv_proof=pct(esv[2]), un_n=unr[0], un_pct=pct(unr[0] / f["theorems"]))
        write_report(ctx)
    else:
        raise SystemExit("unknown command " + cmd)
