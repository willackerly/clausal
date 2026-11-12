#!/usr/bin/env python3
"""Sweep: take every entry, every form, every `implied`, every default and the two switches of g.line out of the books,
one at a time (in memory), and recompile every sentence of features/ and controls/.

    python3 mutation/removal_sweep.py [out.json]        (from clausal/; about 70 s; no Lean, no Rust)

Written by the reviewer of plan nodes C1 and Q3, kept with the fix round. Prints one line per removal, then
  * the entries whose removal leaves a sentence that USES them (lists them among its pieces) compiling to the same term:
    there must be none (exit 1 otherwise);
  * the removals that change no recorded term at all: forms no fixture sentence is written with (informational).
A removal after which the books do not load (LOADFAIL) or the compiler stops (COMPILEFAIL) counts as noticed.
"""
import sys, copy, json, yaml
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))
from clausal import vocab, book
from clausal.core import load_glossary, FeatureError, Problem
from clausal.pipeline import ROOT
gl = load_glossary(ROOT / "glossary.yaml", "glossary.yaml")
books = vocab.project_books(ROOT)
raws = {rel: yaml.safe_load(p.read_text()) for p, rel in books}
def terms(over):
    try:
        v = vocab.load_project(ROOT, gl, overrides=over)
    except Exception as e:
        return "LOADFAIL: " + str(e)[:150]
    try:
        return book.compiled_terms(v)
    except Exception as e:
        return "COMPILEFAIL: " + type(e).__name__ + " " + str(e)[:150]
base = terms({})
# sentences texts
from clausal.core import parse_feature
texts = {}
for d in ("features", "controls"):
    for path in sorted((ROOT / d).glob("*.feature")):
        f = parse_feature(path, f"{d}/{path.name}")
        for sc in f.scenarios:
            texts[sc.id] = " | ".join(s.text for s in sc.steps) if hasattr(sc, "steps") else ""
        for r in f.rules:
            texts[r.id] = r.name
FIELDS = ["forms", "not_forms", "then_forms", "vp_forms", "subject_forms", "claim_forms"]
results = []
def run(desc, rel, raw2):
    t = terms({rel: yaml.safe_dump(raw2, allow_unicode=True, sort_keys=False)})
    if isinstance(t, str):
        results.append((desc, t, [])); return
    changed = [i for i in base if i in t and any(base[i].get(k) != t[i].get(k) for k in ("compiled", "status", "code", "lean_sha256"))]
    newly_ok = [i for i in changed if t[i]["compiled"] and not base[i]["compiled"]]
    still_same_users = []
    results.append((desc, f"{len(changed)} changed (newly compiling: {len(newly_ok)})", changed))
for p, rel in books:
    raw = raws[rel]
    for sec in ("pieces", "operations", "idioms", "grammar", "coverage"):
        for k, e in enumerate(raw.get(sec) or []):
            # whole entry removal
            r2 = copy.deepcopy(raw); del r2[sec][k]
            run(f"ENTRY {rel} {e['id']}", rel, r2)
            for fld in FIELDS + (["when", "nouns"] if sec == "operations" else []):
                for j, f in enumerate(e.get(fld) or []):
                    r2 = copy.deepcopy(raw); del r2[sec][k][fld][j]
                    run(f"FORM {rel} {e['id']}.{fld}: {f}", rel, r2)
            if sec == "idioms":
                pass
            if "implied" in e:
                r2 = copy.deepcopy(raw); del r2[sec][k]["implied"]
                run(f"IMPLIED {rel} {e['id']}", rel, r2)
            for fl in ("first_letter_either_case", "final_full_stop_optional"):
                if e.get(fl):
                    r2 = copy.deepcopy(raw); r2[sec][k][fl] = False
                    run(f"FLAG {rel} {e['id']}.{fl}", rel, r2)
            if sec == "operations" and "internal" in e:
                r2 = copy.deepcopy(raw); del r2[sec][k]["internal"]["echo"]
                run(f"INTERNAL-ECHO {rel} {e['id']}", rel, r2)
    for d in (raw.get("defaults") or {}):
        r2 = copy.deepcopy(raw); del r2["defaults"][d]
        run(f"DEFAULT {rel} {d}", rel, r2)
if len(sys.argv) > 1:
    json.dump({"results": results, "texts": texts, "base": base}, open(sys.argv[1], "w"), indent=0)
for desc, s, ch in results:
    print(desc, "=>", s)

bad, quiet, n = [], [], 0
for desc, s, ch in results:
    if s.startswith(("LOADFAIL", "COMPILEFAIL")):
        continue
    if desc.startswith("ENTRY"):
        n += 1
        id_ = desc.split()[2]
        same = [i for i, t in base.items() if t.get("compiled") and id_ in t.get("pieces", []) and i not in ch]
        if same:
            bad.append((id_, same))
    if not ch:
        quiet.append(desc)
print(f"\n{len(results)} removals; {sum(1 for d, _, _ in results if d.startswith('ENTRY'))} of them whole entries")
print(f"entries whose removal leaves a sentence that uses them unchanged: {len(bad)}" + "".join(f"\n  {i}: {len(s)} ({', '.join(s[:3])})" for i, s in bad))
print(f"removals that change no recorded term (no fixture sentence is written with them): {len(quiet)}" + "".join(f"\n  {d}" for d in quiet))
sys.exit(1 if bad else 0)
