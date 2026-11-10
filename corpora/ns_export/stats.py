#!/usr/bin/env python3
"""Headline shape statistics of the exported declaration graph (reads decls.jsonl only)."""
import json, sys, collections, statistics

out_dir = sys.argv[1]
mains = sys.argv[2:]
D = [json.loads(l) for l in open(f"{out_dir}/decls.jsonl")]
by = {d["name"]: d for d in D}
assert len(by) == len(D), "duplicate names"


def pct(xs, qs=(0, 10, 25, 50, 75, 90, 95, 99, 99.9, 100)):
    xs = sorted(xs)
    if not xs:
        return {}
    r = {f"p{q}": xs[min(len(xs) - 1, int(round(q / 100 * (len(xs) - 1))))] for q in qs}
    r["mean"] = round(sum(xs) / len(xs), 2)
    r["n"] = len(xs)
    r["sum"] = sum(xs)
    return r


deps = {d["name"]: sorted(set(d["typeDeps"]) | set(d["valueDeps"])) for d in D}
dangling = sum(1 for n in deps for x in deps[n] if x not in by)
users = collections.defaultdict(set)
for n, ds in deps.items():
    for x in ds:
        users[x].add(n)

S = {}
S["declarations"] = len(D)
S["byKind"] = dict(collections.Counter(d["kind"] for d in D).most_common())
S["byRootLibrary"] = dict(collections.Counter(d["module"].split(".")[0] for d in D))
S["byRootLibraryAndKind"] = {
    lib: dict(collections.Counter(d["kind"] for d in D if d["module"].split(".")[0] == lib))
    for lib in S["byRootLibrary"]}
mods = collections.Counter(d["module"] for d in D)
S["modulesWithDeclarations"] = len(mods)
S["declsPerModule"] = pct(list(mods.values()))
S["danglingEdges"] = dangling
S["edges"] = {
    "typeEdges": sum(len(d["typeDeps"]) for d in D),
    "valueEdges": sum(len(d["valueDeps"]) for d in D),
    "unionEdges": sum(len(v) for v in deps.values()),
}
thm = [d for d in D if d["kind"] == "theorem"]
dfn = [d for d in D if d["kind"] == "def"]
S["fractionPrivate"] = {
    "all": round(sum(d["isPrivate"] for d in D) / len(D), 4),
    "theorems": round(sum(d["isPrivate"] for d in thm) / max(1, len(thm)), 4),
    "defs": round(sum(d["isPrivate"] for d in dfn) / max(1, len(dfn)), 4),
}
S["fractionDocstring"] = {
    "all": round(sum(d["hasDocstring"] for d in D) / len(D), 4),
    "theorems": round(sum(d["hasDocstring"] for d in thm) / max(1, len(thm)), 4),
    "defs": round(sum(d["hasDocstring"] for d in dfn) / max(1, len(dfn)), 4),
    "structures": round(sum(d["hasDocstring"] for d in D if d["kind"] == "structure")
                        / max(1, sum(1 for d in D if d["kind"] == "structure")), 4),
}
S["theorem"] = {
    "proofSize": pct([d["proofSize"] for d in thm]),
    "proofSizePlusAux": pct([d["proofSize"] + d["auxProofSize"] for d in thm]),
    "statementSize": pct([d["statementSize"] for d in thm]),
    "statementDagSize": pct([d["statementDagSize"] for d in thm]),
    "statementChars": pct([d["statementChars"] for d in thm]),
    "sourceLines": pct([d["endLine"] - d["line"] + 1 for d in thm if d["line"] is not None]),
    "statementTruncatedAt2000": sum(d["statementTruncated"] for d in thm),
    "withBodyAux": sum(1 for d in thm if d["numAux"] > 0),
}
S["def"] = {
    "valueSize": pct([d["proofSize"] for d in dfn]),
    "statementSize": pct([d["statementSize"] for d in dfn]),
}
S["structure"] = {"statementSize": pct([d["statementSize"] for d in D if d["kind"] == "structure"])}
S["ppFailures"] = sum(1 for d in D if not d["ppOk"])
S["noSourceRange"] = sum(1 for d in D if d["line"] is None)
S["outDegree"] = {
    "all": pct([len(deps[d["name"]]) for d in D]),
    "theorems": pct([len(deps[d["name"]]) for d in thm]),
    "theoremsTypeOnly": pct([len(d["typeDeps"]) for d in thm]),
    "theoremsValueOnly": pct([len(d["valueDeps"]) for d in thm]),
    "zero": sum(1 for d in D if not deps[d["name"]]),
}
indeg = {d["name"]: len(users.get(d["name"], ())) for d in D}
S["inDegree"] = {
    "all": pct(list(indeg.values())),
    "theorems": pct([indeg[d["name"]] for d in thm]),
    "defs": pct([indeg[d["name"]] for d in dfn]),
    "zero": sum(1 for v in indeg.values() if v == 0),
    "zeroTheorems": sum(1 for d in thm if indeg[d["name"]] == 0),
    "one": sum(1 for v in indeg.values() if v == 1),
    "oneTheorems": sum(1 for d in thm if indeg[d["name"]] == 1),
    "ge10": sum(1 for v in indeg.values() if v >= 10),
    "ge100": sum(1 for v in indeg.values() if v >= 100),
    "top20": sorted(((v, k, by[k]["kind"]) for k, v in indeg.items()), reverse=True)[:20],
}
S["externalConstants"] = {
    "theoremType": pct([d["numExtType"] for d in thm]),
    "theoremValue": pct([d["numExtValue"] for d in thm]),
}
# statement duplicates (binder-name-invariant hash)
hc = collections.Counter(d["statementHash"] for d in thm)
S["theoremStatementHash"] = {
    "distinct": len(hc),
    "theoremsInDuplicateGroups": sum(c for c in hc.values() if c > 1),
    "duplicateGroups": sum(1 for c in hc.values() if c > 1),
    "largestGroup": max(hc.values()) if hc else 0,
}


# cycles (Tarjan, iterative) over the union graph
def sccs():
    index = {}
    low = {}
    onst = set()
    st = []
    res = []
    c = 0
    for root in deps:
        if root in index:
            continue
        work = [(root, 0)]
        while work:
            v, i = work.pop()
            if i == 0:
                index[v] = low[v] = c
                c += 1
                st.append(v)
                onst.add(v)
            rec = False
            ds = deps[v]
            while i < len(ds):
                w = ds[i]
                i += 1
                if w not in deps:
                    continue
                if w not in index:
                    work.append((v, i))
                    work.append((w, 0))
                    rec = True
                    break
                elif w in onst:
                    low[v] = min(low[v], index[w])
            if rec:
                continue
            if low[v] == index[v]:
                comp = []
                while True:
                    w = st.pop()
                    onst.discard(w)
                    comp.append(w)
                    if w == v:
                        break
                if len(comp) > 1:
                    res.append(comp)
            if work:
                p = work[-1][0]
                low[p] = min(low[p], low[v])
    return res


cyc = sccs()
S["nontrivialSCCs"] = {"count": len(cyc), "sizes": sorted((len(c) for c in cyc), reverse=True)[:20],
                       "sample": [sorted(c)[:6] for c in cyc[:5]]}
incyc = {n for c in cyc for n in c}


def below(root):
    """reachable set, longest-path depth (edges), BFS depth (edges)."""
    seen = {root: 0}
    q = collections.deque([root])
    while q:
        v = q.popleft()
        for w in deps.get(v, ()):
            if w in by and w not in seen:
                seen[w] = seen[v] + 1
                q.append(w)
    # longest path by reverse post-order (cycle members contribute but back-edges are ignored)
    order = []
    state = {}
    stack = [(root, 0)]
    while stack:
        v, i = stack.pop()
        if i == 0:
            if v in state:
                continue
            state[v] = 1
        ds = [w for w in deps.get(v, ()) if w in by]
        pushed = False
        while i < len(ds):
            w = ds[i]
            i += 1
            if w not in state:
                stack.append((v, i))
                stack.append((w, 0))
                pushed = True
                break
        if not pushed:
            state[v] = 2
            order.append(v)
    h = {}
    for v in order:  # post-order: children first
        h[v] = 1 + max((h[w] for w in deps.get(v, ()) if w in h and w != v), default=-1)
    reach = set(seen)
    kinds = collections.Counter(by[n]["kind"] for n in reach)
    thm_reach = [by[n] for n in reach if by[n]["kind"] == "theorem"]
    return reach, {
        "reachableDecls": len(reach),
        "reachableByKind": dict(kinds),
        "reachableModules": len({by[n]["module"] for n in reach}),
        "reachableProofMass": sum(by[n]["proofSize"] + by[n]["auxProofSize"] for n in reach
                                  if by[n]["kind"] == "theorem"),
        "longestPathDepth": h[root],
        "bfsDepthMax": max(seen.values()),
        "bfsDepthHistogram": dict(sorted(collections.Counter(seen.values()).items())),
        "longestPathHistogramDeciles": pct([h[n] for n in reach], qs=(10, 25, 50, 75, 90, 100)),
        "rootDirectDeps": len([w for w in deps[root] if w in by]),
        "theoremStatementSizeMedian": statistics.median(d["statementSize"] for d in thm_reach)
        if thm_reach else None,
    }


S["mainTheorems"] = {}
allreach = set()
for m in mains:
    if m not in by:
        S["mainTheorems"][m] = "NOT IN EXPORT"
        continue
    reach, info = below(m)
    allreach |= reach
    info["statement"] = by[m]["statement"]
    info["module"] = by[m]["module"]
    info["proofSize"] = by[m]["proofSize"]
    info["statementSize"] = by[m]["statementSize"]
    S["mainTheorems"][m] = info
tot_mass = sum(d["proofSize"] + d["auxProofSize"] for d in thm)
S["unionOfMainTheorems"] = {
    "reachableDecls": len(allreach),
    "fractionOfDecls": round(len(allreach) / len(D), 4),
    "reachableTheorems": sum(1 for n in allreach if by[n]["kind"] == "theorem"),
    "fractionOfTheorems": round(sum(1 for n in allreach if by[n]["kind"] == "theorem") / len(thm), 4),
    "fractionOfTheoremProofMass": round(
        sum(by[n]["proofSize"] + by[n]["auxProofSize"] for n in allreach
            if by[n]["kind"] == "theorem") / tot_mass, 4),
    "unreachableByLibrary": dict(collections.Counter(
        d["module"].split(".")[0] for d in D if d["name"] not in allreach)),
    "unreachableModules": len({d["module"] for d in D}
                              - {by[n]["module"] for n in allreach}),
}
json.dump(S, open(f"{out_dir}/stats.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(S, indent=1, ensure_ascii=False))
