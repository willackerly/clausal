#!/usr/bin/env python3
"""Check an author's file for the sentences trial and, optionally, compile the rules exactly as written.

    python3 check_author.py FILE.json             # shape only: nothing else is needed
    python3 check_author.py FILE.json --compile   # also compile each rule as written (needs the scratch copy, see README.md)

FILE.json is one author in the shape of author_template.json, or a whole authors.json ({"authors": [...]}).
The same command serves a person's file and a model's. Nothing is written; the author's text is never changed.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def problems_of(a):
    out = []
    name = a.get("author")
    if not name:
        out.append("no author name")
    if a.get("author_type") not in ("human", "proxy") and not a.get("model"):
        out.append("author_type must be 'human' or 'proxy' (or give 'model' for a model author)")
    rules = a.get("rules") or []
    if not rules:
        out.append("no rules")
    seen = set()
    for r in rules:
        rid = r.get("id", "?")
        if rid in seen:
            out.append("rule id %s used twice" % rid)
        seen.add(rid)
        if not isinstance(r.get("rule"), str) or not r["rule"].strip():
            out.append("%s: no sentence" % rid)
        if not isinstance(r.get("meantToBeTrue"), bool):
            out.append("%s: meantToBeTrue must be true or false" % rid)
        ex = r.get("intentExamples")
        if not isinstance(ex, list) or len(ex) != 5 or not all(isinstance(e, str) and e.strip() for e in ex):
            out.append("%s: needs exactly five cases, each a line of text" % rid)
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    data = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    authors = data["authors"] if "authors" in data else [data]
    bad = 0
    for a in authors:
        kind = a.get("author_type") or ("proxy" if a.get("model") else "?")
        rules = a.get("rules") or []
        probs = problems_of(a)
        bad += len(probs)
        print("%s (%s%s): %d rules, %d meant true, %d meant false%s" % (
            a.get("author"), kind, ", " + str(a["model"]) if a.get("model") else "", len(rules),
            sum(r.get("meantToBeTrue") is True for r in rules), sum(r.get("meantToBeTrue") is False for r in rules),
            "" if not probs else "; PROBLEMS:"))
        for p in probs:
            print("   - " + p)
    if bad:
        return 1
    if "--compile" not in sys.argv:
        return 0
    if not (HERE / "work" / "clausal").is_dir():
        sys.exit("no scratch copy: run  bash ../../clausal/mutation/workcopy.sh \"$PWD/work/clausal\"  first (see README.md)")
    sys.path.insert(0, str(HERE))
    import try_compile                                   # changes directory into the scratch copy
    total = done = 0
    by_status = {}
    for a in authors:
        rules = a["rules"]
        _, _, res = try_compile.compile_lines([r["rule"] for r in rules], name="as_written_check")
        ok = sum(x["compiled"] for x in res)
        total += len(res)
        done += ok
        print("\n%s: %d of %d compile as written" % (a["author"], ok, len(res)))
        for r, x in zip(rules, res):
            by_status[x["status"]] = by_status.get(x["status"], 0) + 1
            print("  %-5s %-10s %s" % (r["id"], x["status"], r["rule"]))
            if x["compiled"]:
                for slot, text in x["echo"]:
                    print("        %-12s%s" % (slot, text))
    print("\nall authors: %d of %d compile as written; %s" % (
        done, total, ", ".join("%s %d" % kv for kv in sorted(by_status.items()))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
