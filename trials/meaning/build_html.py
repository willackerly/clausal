#!/usr/bin/env python3
"""Build trial.html (the browser version of the trial) and, optionally, a reader kit.

    python3 build_html.py                # writes BANK/trial.html
    python3 build_html.py --kit DIR      # also copies what a reader needs into DIR
    python3 build_html.py --bank DIR     # another item bank

trial.html is a single self-contained file built from items.json and the brief.
This script does not read the answer key, and the kit never contains it: the kit is
take_trial.py, items.json, the brief and trial.html, and nothing else.

Standard library only; Python 3.8 or later.
"""
import argparse
import hashlib
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PLACEHOLDER = "/*__MATERIAL__*/"
FORBIDDEN_FIELDS = ("faithful", "errorKind", "error_kind", "explanation", "structure")


def main():
    ap = argparse.ArgumentParser(description="Build trial.html and optionally a reader kit.")
    ap.add_argument("--bank", default=HERE, help="directory holding items.json and the brief")
    ap.add_argument("--kit", default=None, help="directory to fill with the files a reader needs")
    args = ap.parse_args()

    with open(os.path.join(args.bank, "items.json"), "rb") as f:
        items_bytes = f.read()
    material = json.loads(items_bytes.decode("utf-8"))
    brief_name = os.path.basename(material["brief_file"])
    with open(os.path.join(args.bank, brief_name), "rb") as f:
        brief_bytes = f.read()
    for item in material["items"]:
        bad = [k for k in FORBIDDEN_FIELDS if k in item]
        if bad:
            sys.exit("items.json item %s carries key fields %s; refusing to build" % (item["id"], bad))
        extra = set(item) - {"id", "kind", "first", "second"}
        if extra:
            sys.exit("items.json item %s has unexpected fields %s; refusing to build" % (item["id"], sorted(extra)))
    sha = hashlib.sha256(items_bytes + b"\n" + brief_bytes).hexdigest()
    bundle = json.dumps({"material": material, "brief": brief_bytes.decode("utf-8"), "sha": sha}, ensure_ascii=False)
    bundle = bundle.replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    with open(os.path.join(HERE, "trial.template.html"), encoding="utf-8") as f:
        template = f.read()
    if template.count(PLACEHOLDER) != 1:
        sys.exit("trial.template.html must contain the placeholder exactly once")
    out = os.path.join(args.bank, "trial.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(template.replace(PLACEHOLDER, bundle))
    print("wrote %s\nmaterial_sha256 %s" % (out, sha))

    if args.kit:
        os.makedirs(args.kit, exist_ok=True)
        if os.path.abspath(args.kit) != os.path.abspath(args.bank):
            for src in (os.path.join(HERE, "take_trial.py"), os.path.join(args.bank, "items.json"),
                        os.path.join(args.bank, brief_name), out):
                shutil.copy2(src, os.path.join(args.kit, os.path.basename(src)))
        print("reader kit in %s: take_trial.py, items.json, %s, trial.html" % (args.kit, brief_name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
