#!/usr/bin/env python3
"""Parse a leanblueprint LaTeX tree into JSON.

  parse_blueprint.py <blueprint_src_dir> <entry.tex> <out_dir> [--resolve]

Phase 1 (no --resolve): writes <out_dir>/blueprint_lean_names.txt (one \\lean name per line).
Phase 2 (--resolve): reads decls.jsonl, all_names.jsonl, name_check.json from <out_dir>
(written by ExportDecls.lean) and writes blueprint.json + blueprint_summary.json.
LaTeX is parsed with regexes; this is not Lean data.
"""
import json, os, re, sys

ENVS = ["definition", "lemma", "sublemma", "theorem", "proposition", "corollary", "cor", "remark", "example", "examples"]
NORM = {"cor": "corollary", "examples": "example"}

def strip_comments(s):
    return re.sub(r"(?<!\\)%.*", "", s)

def load(src, rel, seen):
    p = os.path.join(src, rel if rel.endswith(".tex") else rel + ".tex")
    if p in seen or not os.path.exists(p):
        return []
    seen.add(p)
    out = []
    text = strip_comments(open(p, encoding="utf-8").read())
    pos = 0
    for m in re.finditer(r"\\(?:input|include)\{([^}]*)\}", text):
        out.append((p, text[pos:m.start()]))
        out.extend(load(src, m.group(1), seen))
        pos = m.end()
    out.append((p, text[pos:]))
    return out

def args(cmd, body):
    r = []
    for m in re.finditer(r"\\" + cmd + r"\s*\{([^}]*)\}", body):
        r.extend(x.strip() for x in m.group(1).split(",") if x.strip())
    return r

def parse(src, entry):
    nodes, chapter, section = [], None, None
    last = None
    tok = re.compile(r"\\(chapter|section)\*?\{((?:[^{}]|\{[^{}]*\})*)\}|\\begin\{(" + "|".join(ENVS + ["proof"]) + r")\}(\[(?:[^\[\]]|\[[^\]]*\])*\])?")
    for path, text in load(src, entry, set()):
        i = 0
        while True:
            m = tok.search(text, i)
            if not m:
                break
            if m.group(1) == "chapter":
                chapter, section = m.group(2), None; i = m.end(); continue
            if m.group(1) == "section":
                section = m.group(2); i = m.end(); continue
            env = m.group(3)
            e = text.find("\\end{" + env + "}", m.end())
            if e < 0:
                e = len(text)
            body = text[m.end():e]
            i = e
            if env == "proof":
                if last is not None and not last["hasProof"]:
                    last["hasProof"] = True
                    last["proofUses"] = sorted(set(args("uses", body)))
                    last["proofLeanok"] = "\\leanok" in body
                    last["proofChars"] = len(body.strip())
                continue
            labels = args("label", body)
            node = {
                "label": labels[0] if labels else None,
                "kind": NORM.get(env, env),
                "title": (m.group(4) or "")[1:-1] or None,
                "chapter": chapter, "section": section,
                "file": os.path.relpath(path, src),
                "lean": args("lean", body),
                "uses": sorted(set(args("uses", body))),
                "leanok": "\\leanok" in body,
                "notready": "\\notready" in body,
                "mathlibok": "\\mathlibok" in body,
                "statementChars": len(body.strip()),
                "hasProof": False, "proofUses": [], "proofLeanok": False, "proofChars": 0,
            }
            nodes.append(node)
            last = node
    return nodes

def main():
    src, entry, out = sys.argv[1:4]
    nodes = parse(src, entry)
    names = sorted({n for nd in nodes for n in nd["lean"]})
    if "--resolve" not in sys.argv:
        open(os.path.join(out, "blueprint_lean_names.txt"), "w").write("\n".join(names) + "\n")
        print(len(nodes), "nodes;", len(names), "distinct lean names")
        return
    decls = [json.loads(l) for l in open(os.path.join(out, "decls.jsonl"))]
    by_user = {}
    for d in decls:
        by_user.setdefault(d["userName"], []).append(d)
    auto = {}
    for l in open(os.path.join(out, "all_names.jsonl")):
        a = json.loads(l)
        if a["auto"]:
            auto[a["userName"]] = a
    check = json.load(open(os.path.join(out, "name_check.json")))
    labels = {}
    for nd in nodes:
        if nd["label"]:
            labels.setdefault(nd["label"], 0); labels[nd["label"]] += 1
    covered = {}
    status_count = {}
    for nd in nodes:
        res = []
        for n in nd["lean"]:
            if n in by_user:
                d = by_user[n][0]
                r = {"name": n, "status": "exported", "decl": d["name"], "kind": d["kind"]}
                covered.setdefault(d["name"], []).append(nd["label"])
            elif n in auto:
                r = {"name": n, "status": "project-auxiliary", "parent": auto[n]["parent"]}
            elif check.get(n, {}).get("exists"):
                r = {"name": n, "status": "external", "module": check[n]["module"]}
            else:
                r = {"name": n, "status": "unresolved"}
            status_count[r["status"]] = status_count.get(r["status"], 0) + 1
            res.append(r)
        nd["leanResolved"] = res
        nd["usesUnresolved"] = [u for u in nd["uses"] + nd["proofUses"] if u not in labels]
    json.dump(nodes, open(os.path.join(out, "blueprint.json"), "w"), indent=1, ensure_ascii=False)
    thms = [d for d in decls if d["kind"] == "theorem"]
    defs = [d for d in decls if d["kind"] != "theorem"]
    kinds = {}
    for nd in nodes:
        kinds[nd["kind"]] = kinds.get(nd["kind"], 0) + 1
    cov_thm = [d for d in thms if d["name"] in covered]
    cov_def = [d for d in defs if d["name"] in covered]
    def mainline(ds):
        return [d for d in ds if not any(x in d["module"] for x in (".Mathlib.", ".ForMathlib.", ".ToMathlib.", ".Tactic.", ".Examples"))]
    summ = {
        "numNodes": len(nodes),
        "nodesByKind": kinds,
        "nodesWithLean": sum(1 for nd in nodes if nd["lean"]),
        "nodesWithoutLean": [nd["label"] for nd in nodes if not nd["lean"]],
        "nodesWithoutLabel": sum(1 for nd in nodes if not nd["label"]),
        "duplicateLabels": [l for l, c in labels.items() if c > 1],
        "nodesWithProof": sum(1 for nd in nodes if nd["hasProof"]),
        "statementUsesEdges": sum(len(nd["uses"]) for nd in nodes),
        "proofUsesEdges": sum(len(nd["proofUses"]) for nd in nodes),
        "usesToUnknownLabel": sorted({u for nd in nodes for u in nd["usesUnresolved"]}),
        "leanNameMentions": sum(len(nd["lean"]) for nd in nodes),
        "distinctLeanNames": len(names),
        "leanNameStatus": status_count,
        "unresolvedLeanNames": sorted({r["name"] for nd in nodes for r in nd["leanResolved"] if r["status"] == "unresolved"}),
        "externalLeanNames": sorted({r["name"] for nd in nodes for r in nd["leanResolved"] if r["status"] == "external"}),
        "auxiliaryLeanNames": sorted({r["name"] for nd in nodes for r in nd["leanResolved"] if r["status"] == "project-auxiliary"}),
        "exportedDeclsCovered": len(covered),
        "theoremsTotal": len(thms), "theoremsTagged": len(cov_thm),
        "theoremsTaggedFraction": round(len(cov_thm) / max(1, len(thms)), 4),
        "nonTheoremsTotal": len(defs), "nonTheoremsTagged": len(cov_def),
        "theoremsTotalMainline": len(mainline(thms)), "theoremsTaggedMainline": len(mainline(cov_thm)),
        "theoremsTaggedFractionMainline": round(len(mainline(cov_thm)) / max(1, len(mainline(thms))), 4),
        "mainlineDefinition": "module path contains none of .Mathlib. .ForMathlib. .ToMathlib. .Tactic. .Examples",
        "declsTaggedByMultipleNodes": sum(1 for v in covered.values() if len(set(v)) > 1),
    }
    json.dump(summ, open(os.path.join(out, "blueprint_summary.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in summ.items() if not isinstance(v, list) or len(v) < 15}, indent=1, ensure_ascii=False))

main()
