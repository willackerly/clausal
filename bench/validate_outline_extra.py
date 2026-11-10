#!/usr/bin/env python3
"""Follow-up diagnostics for H3 (run after validate_outline.py). Writes out/corpus/validation/extra.json.
1. Chain effect: are the top untagged theorems (by dominated mass) dominator-tree neighbours or name
   variants (', _aux, _optimized ...) of a tagged declaration?
2. Docstring style (source text, diagnostic only): share of docstrings containing LaTeX `$`.
3. Where tagged theorems sit: reachable / leaf / nontrivial dominator shares against untagged.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validate_outline as V

def stem(n):
    n = n.split(".")[-1]
    n = re.sub(r"['′]+", "", n)
    n = re.sub(r"(_aux\d*|_optimized|_main|_prelim|_specific|_step|\d+)$", "", n)
    return re.sub(r"['′]+$", "", n)

out = {}
for c in ["pfr", "carleson"]:
    decls, bp, roots = V.load(c)
    G, idx, roots = V.build(decls, roots)
    F, idom, bits = V.features(decls, G, idx, roots)
    tagged = {r["decl"] for nd in bp for r in nd.get("leanResolved", []) if r.get("status") == "exported"}
    by = {d["name"]: d for d in decls}
    kids = {}
    for v, p in idom.items():
        if v != p:
            kids.setdefault(p, []).append(v)
    tstems = {stem(by[t]["userName"]) for t in tagged if t in by}
    thm = [f for f in F if f["kind"] == "theorem"]
    res = {}
    for K in (25, 50, 100):
        top = sorted([f for f in thm if f["name"] not in tagged], key=lambda f: -f["dom_mass"])[:K]
        par = sum(1 for f in top if idom.get(f["name"]) in tagged)
        chi = sum(1 for f in top if any(k in tagged for k in kids.get(f["name"], [])))
        nb = sum(1 for f in top if idom.get(f["name"]) in tagged or any(k in tagged for k in kids.get(f["name"], [])))
        st = sum(1 for f in top if stem(f["userName"]) in tstems)
        either = sum(1 for f in top if stem(f["userName"]) in tstems or idom.get(f["name"]) in tagged
                     or any(k in tagged for k in kids.get(f["name"], [])))
        res[f"top{K}"] = dict(dom_parent_tagged=par, has_tagged_dom_child=chi, dom_neighbour_tagged=nb,
                              name_variant_of_tagged=st, either=either)
    # base rate of the same neighbour property over all untagged reachable theorems
    un = [f for f in thm if f["name"] not in tagged and f["reachable"]]
    res["base_rate_untagged_reachable"] = dict(
        n=len(un),
        dom_neighbour_tagged=sum(1 for f in un if idom.get(f["name"]) in tagged or any(k in tagged for k in kids.get(f["name"], []))),
        name_variant_of_tagged=sum(1 for f in un if stem(f["userName"]) in tstems))
    # 3. shares
    sh = {}
    for lab, S in (("tagged", [f for f in thm if f["name"] in tagged]), ("untagged", [f for f in thm if f["name"] not in tagged])):
        n = len(S)
        sh[lab] = dict(n=n, reachable=sum(f["reachable"] for f in S) / n,
                       nontrivial_dominator=sum(f["nontrivial_dom"] for f in S) / n,
                       no_project_deps=sum(1 for f in S if f["out_degree"] == 0) / n,
                       no_users=sum(1 for f in S if f["in_degree"] == 0) / n,
                       exactly_one_user=sum(1 for f in S if f["in_degree"] == 1) / n,
                       mainline=sum(f["mainline"] for f in S) / n,
                       median_proof_size=sorted(f["proof_size"] for f in S)[n // 2],
                       median_statement_size=sorted(f["statement_size"] for f in S)[n // 2])
    # 2. docstrings with LaTeX
    cache = {}
    dl = {"tagged": [0, 0], "untagged": [0, 0]}
    for d in decls:
        if d["kind"] != "theorem" or not d["hasDocstring"]:
            continue
        p = os.path.join(V.REPO, "corpora", c, d["module"].replace(".", "/") + ".lean")
        if p not in cache:
            cache[p] = open(p, encoding="utf-8").read().split("\n")
        src = cache[p]; j = d["line"] - 1; lo = j
        while lo > 0 and "/--" not in src[lo] and j - lo < 60: lo -= 1
        hi = j
        while hi < len(src) - 1 and "-/" not in src[hi] and hi - j < 60: hi += 1
        k = "tagged" if d["name"] in tagged else "untagged"
        dl[k][0] += 1
        dl[k][1] += "$" in "\n".join(src[lo:hi + 1])
    out[c] = dict(chain=res, shares=sh, docstring_with_latex={k: dict(docstrings=v[0], with_dollar=v[1]) for k, v in dl.items()})
json.dump(out, open(os.path.join(V.OUT, "extra.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
