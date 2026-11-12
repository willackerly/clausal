"""Plan node Q3b, section 3: can two bare-hole forms of different pieces read the same text at the same type?
Run from clausal/:  python3 clausebook/q3b/bare.py [--json]

A bare-hole form is a form with no literal word ("{x:amount}"): only the type of its hole tells it from another.
The lint (`clausal book check`, check 4) does not count a pair of them whose registered (category, position) sets
are disjoint. This script tests the claim that rule rests on, with the parser itself, over the book as it stands.

UNIVERSE. Every span of whole words of every step and every Rule line of features/ and controls/ and of the two
sentences of every separation of the book; every sample literal of glossary.yaml; every role phrase of every
operation. CONFIGURATIONS. The whole Clausebook (every book; the books of one project are a subset of it, so a
form tried there is tried here), for each system: scenario mode, and rule mode once for each operation (its roles).

T1  For every (category, position) under which a bare-hole form is registered and every text: the parser's strict
    readings of the text there, made through a bare-hole form, are all of ONE piece.        Expected: 0 exceptions.
T2  How many texts have a strict reading at two instances of one generic category (`term<num>` and `term<optnum>`)?
    Reported, with which pieces read them. Such a text is not a counterexample to T1 (two types, not one): it is the
    place where a frame generic in T could read one sentence at two types, which the compiler refuses as AMBIGUOUS.
Nothing is written. Exit 1 iff T1 has an exception."""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
from clausal import book, vocab                      # noqa: E402
from clausal.core import load_glossary, parse_feature   # noqa: E402
from clausal.pipeline import ROOT                    # noqa: E402


def universe(voc, gl) -> tuple:
    lines = []
    for d in ("features", "controls"):
        for path in sorted((ROOT / d).glob("*.feature")):
            f = parse_feature(path, f"{d}/{path.name}")
            for sc in f.scenarios:
                lines += [s.text for s in list(sc.background) + list(sc.steps)]
            for r in f.rules:
                t = r.name.strip().rstrip(".")
                lines.append(t[:1].lower() + t[1:])
    for s in voc.separations.values():
        lines += [t[:1].lower() + t[1:] for t in s["inputs"].values()]
    texts = set()
    for line in lines:
        ws = line.split()
        for i in range(len(ws)):
            for j in range(i + 1, len(ws) + 1):
                t = " ".join(ws[i:j])
                texts.add(t)
                texts.add(t.rstrip(","))
    for pt in gl.param_types.values():
        texts |= {str(x) for x in pt.get("sample") or []}
    for o in voc.ops.values():
        for r, _ in list(o["state"]) + list(o["input"]):
            texts |= set(voc.role_phrases(r))
    texts.discard("")
    return len(lines), sorted(texts)


def configurations(voc) -> list:
    out = []
    for d in sorted({o["domain"] for o in voc.ops.values()}):
        out.append((f"{d}, scenario", vocab.Parser(voc, d, "scenario")))
        for o in voc.ops.values():
            if o["domain"] == d:
                out.append((f"{d}, rule about {o['id']}", vocab.Parser(voc, d, "rule", vocab.op_roles(o, voc), {})))
    return out


def main(argv) -> int:
    gl = load_glossary(ROOT / "glossary.yaml", "glossary.yaml")
    voc = vocab.load_project(ROOT, gl)
    n_lines, texts = universe(voc, gl)
    bare = {}                                    # (category, position) -> {form text: piece}
    for (c, v), fs in voc.forms.items():
        for f in fs:
            if book.skeleton(f.text) == "{}":
                bare.setdefault((c, v), {})[f.text] = f.owner["id"]
    generic = {}                                 # (base category, position) -> its instances
    for (c, v) in voc.forms:
        if "<" in c:
            generic.setdefault((vocab.base_cat(c), v), []).append(c)
    generic = {k: sorted(set(cs)) for k, cs in generic.items() if len(set(cs)) > 1}
    confs = configurations(voc)
    t1_checked, t1_read, t1_bad, t2 = 0, 0, [], {}
    for name, p in confs:
        for u in texts:
            for (c, v), owners in bare.items():
                t1_checked += 1
                got = {owners[h.form] for h in p.parse(c, u, v) if isinstance(h, vocab.Node) and h.form in owners}
                t1_read += bool(got)
                if len(got) > 1:
                    t1_bad.append({"configuration": name, "text": u, "type": [c, v], "pieces": sorted(got)})
            for (b, v), cs in generic.items():
                hit = {c: sorted({h.id for h in p.parse(c, u, v) if isinstance(h, vocab.Node)}) for c in cs}
                hit = {c: ids for c, ids in hit.items() if ids}
                if len(hit) > 1:
                    t2.setdefault((u, b, v), {"text": u, "category": b, "position": v, "read_as": hit, "configurations": []})["configurations"].append(name)
    res = {"lines": n_lines, "texts": len(texts), "configurations": [n for n, _ in confs],
           "bare_forms": {f"{c}{' (' + v + ')' if v else ''}": o for (c, v), o in sorted(bare.items())},
           "T1": {"checked": t1_checked, "read_by_a_bare_form": t1_read, "read_by_two_pieces": t1_bad},
           "T2": {"generic_categories": {f"{b}{' (' + v + ')' if v else ''}": cs for (b, v), cs in sorted(generic.items())},
                  "texts_read_at_two_instances": sorted(t2.values(), key=lambda x: (x["category"], x["text"]))}}
    if "--json" in argv:
        print(json.dumps(res, indent=1, ensure_ascii=False))
        return 1 if t1_bad else 0
    print(f"universe: {len(texts)} texts (every span of whole words of {n_lines} steps and Rule lines of features/, controls/ and the separations; "
          "sample literals; role phrases)")
    print(f"configurations: {len(confs)} (each system in scenario mode, and in rule mode for each of its operations)")
    print("bare-hole forms as the parser has them registered:")
    for k, o in res["bare_forms"].items():
        print(f"  {k}: " + ", ".join(f"`{i}` \"{t}\"" for t, i in o.items()))
    print(f"T1: {t1_checked} (configuration, text, type) triples asked; {t1_read} have a reading through a bare-hole form; "
          f"{len(t1_bad)} are read by the bare-hole forms of two pieces")
    for x in t1_bad[:20]:
        print(f"  EXCEPTION: {x}")
    by = {}
    for x in res["T2"]["texts_read_at_two_instances"]:
        by.setdefault((x["category"], tuple(sorted((c, tuple(i)) for c, i in x["read_as"].items()))), []).append(x["text"])
    print(f"T2: {len(res['T2']['texts_read_at_two_instances'])} (text, generic category) pairs have a strict reading at two instances of the category:")
    for (b, ras), us in sorted(by.items()):
        print(f"  {b}: {len(us)} texts, read as " + "; ".join(f"{c} by {', '.join('`' + i + '`' for i in ids)}" for c, ids in ras)
              + ": " + ", ".join(f"\"{u}\"" for u in us[:8]) + (" ..." if len(us) > 8 else ""))
    return 1 if t1_bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
