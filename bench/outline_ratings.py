#!/usr/bin/env python3
"""Score blind readability ratings of the two outlines of the machine corpus.

Inputs
  out/corpus/outline2/rating_items.json   60 entries; `hidden.source` says which
                                          outline an entry came from (dominator =
                                          old lemma-based, outline2 = new
                                          definition-centred). Readers never saw it.
  out/corpus/outline2/ratings/*.json      one file per reader:
      {"schema": "outline-ratings/1", "reader": "<name>",
       "kind": "proxy" | "human", "model": "<family or null>",
       "ratings": [{"id": "R01", "label": "<one of LABELS>", "reason": "..."}]}
  out/corpus/outline2/ratings/READING.md  optional hand-written reading, copied
                                          into the report verbatim.

Outputs
  out/corpus/outline2/RATINGS.md
  out/corpus/outline2/ratings_summary.json

Adding a human mathematician: drop another reader file in ratings/ with
"kind": "human" and rerun. A reader may rate a subset of the entries. When more
than one kind is present every table is also given per kind.

No Lean is run here: the entries were printed by Lean earlier (bench/outline2.py);
this script only counts labels.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out/corpus/outline2"
LABELS = ["milestone", "technical-step", "opaque", "unreadable"]
SOURCES = ["dominator", "outline2"]
SOURCE_NAME = {"dominator": "old (lemma-based, dominator)", "outline2": "new (definition-centred)"}
# Derived binary outcomes: name -> label indices that count.
OUTCOMES = {
    "milestone": [0],
    "technical-step": [1],
    "opaque": [2],
    "unreadable": [3],
    "readable (milestone or technical-step)": [0, 1],
    "opaque or unreadable": [2, 3],
}
SEED = 20261110
B = 10000


# ---------------------------------------------------------------- loading

def load(items_path: Path, ratings_dir: Path):
    items = json.loads(items_path.read_text())["items"]
    ids = [it["id"] for it in items]
    pos = {i: k for k, i in enumerate(ids)}
    readers = []
    for f in sorted(ratings_dir.glob("*.json")):
        d = json.loads(f.read_text())
        if d.get("schema") != "outline-ratings/1":
            raise SystemExit(f"{f}: schema is not outline-ratings/1")
        if d.get("kind") not in ("proxy", "human"):
            raise SystemExit(f"{f}: kind must be proxy or human")
        row = np.full(len(ids), -1, dtype=int)
        for r in d["ratings"]:
            if r["id"] not in pos:
                raise SystemExit(f"{f}: unknown entry {r['id']}")
            if r["label"] not in LABELS:
                raise SystemExit(f"{f}: unknown label {r['label']!r} on {r['id']}")
            if row[pos[r["id"]]] != -1:
                raise SystemExit(f"{f}: {r['id']} rated twice")
            row[pos[r["id"]]] = LABELS.index(r["label"])
        readers.append({"reader": d["reader"], "kind": d["kind"], "model": d.get("model"),
                        "file": f.name, "row": row,
                        "reasons": {r["id"]: r.get("reason", "") for r in d["ratings"]}})
    if not readers:
        raise SystemExit(f"no reader files in {ratings_dir}")
    names = [r["reader"] for r in readers]
    if len(set(names)) != len(names):
        raise SystemExit("duplicate reader names")
    return items, readers


# ---------------------------------------------------------------- statistics

def onehot(L: np.ndarray) -> np.ndarray:
    """L[reader, item] in {-1,0..3} -> O[reader, item, label] (0/1; all 0 if missing)."""
    O = np.zeros(L.shape + (len(LABELS),))
    for k in range(len(LABELS)):
        O[..., k] = L == k
    return O


def shares(O: np.ndarray, cols: np.ndarray) -> np.ndarray:
    """Share of each label over all (reader, item) ratings in the given item columns."""
    s = O[:, cols, :].sum(axis=(0, 1))
    return s / s.sum() if s.sum() else np.full(len(LABELS), np.nan)


def bootstrap(O, strata, src_of_stratum, mode, rng, reps=B):
    """Resample readers and/or entries. Entries are resampled within the strata the
    sample was drawn from (outline x paper). Returns reps x source x label shares."""
    nR = O.shape[0]
    out = np.empty((reps, len(SOURCES), len(LABELS)))
    for b in range(reps):
        ridx = rng.integers(0, nR, nR) if mode in ("both", "readers") else np.arange(nR)
        Ob = O[ridx]
        acc = np.zeros((len(SOURCES), len(LABELS)))
        for cols, s in zip(strata, src_of_stratum):
            c = cols[rng.integers(0, len(cols), len(cols))] if mode in ("both", "entries") else cols
            acc[s] += Ob[:, c, :].sum(axis=(0, 1))
        out[b] = acc / acc.sum(axis=1, keepdims=True)
    return out


def ci(x):
    x = x[~np.isnan(x)]
    if len(x) == 0:
        return (float("nan"), float("nan"))
    lo, hi = np.percentile(x, [2.5, 97.5])
    return (float(lo), float(hi))


def fleiss(L: np.ndarray, merge=None):
    """Fleiss' kappa on entries every reader rated. merge maps label index -> category."""
    full = (L >= 0).all(axis=0)
    M = L[:, full]
    n, N = M.shape
    if n < 2 or N == 0:
        return float("nan"), int(N)
    if merge is not None:
        M = np.vectorize(merge.get)(M)
    cats = sorted(set(M.flatten().tolist()))
    counts = np.array([[(M[:, i] == c).sum() for c in cats] for i in range(N)], dtype=float)
    Pi = ((counts ** 2).sum(axis=1) - n) / (n * (n - 1))
    pj = counts.sum(axis=0) / (N * n)
    Pe = (pj ** 2).sum()
    if Pe >= 1:
        return float("nan"), int(N)
    return float((Pi.mean() - Pe) / (1 - Pe)), int(N)


def cohen(a: np.ndarray, b: np.ndarray):
    m = (a >= 0) & (b >= 0)
    a, b = a[m], b[m]
    if len(a) == 0:
        return float("nan"), float("nan"), 0
    po = float((a == b).mean())
    pe = sum(float((a == k).mean()) * float((b == k).mean()) for k in range(len(LABELS)))
    return (float((po - pe) / (1 - pe)) if pe < 1 else float("nan")), po, int(len(a))


MERGE3 = {0: 0, 1: 1, 2: 2, 3: 2}          # opaque and unreadable merged
MERGE_MS = {0: 0, 1: 1, 2: 1, 3: 1}        # milestone against the rest
MERGE_RD = {0: 0, 1: 0, 2: 1, 3: 1}        # readable against not


def analyse(items, readers, rng):
    L = np.array([r["row"] for r in readers])
    O = onehot(L)
    src = np.array([SOURCES.index(it["hidden"]["source"]) for it in items])
    paper = [it["hidden"]["key"] for it in items]
    papers = sorted(set(paper))
    strata, s_of = [], []
    for s in range(len(SOURCES)):
        for p in papers:
            cols = np.array([i for i in range(len(items)) if src[i] == s and paper[i] == p])
            if len(cols):
                strata.append(cols)
                s_of.append(s)
    res = {"readers": [r["reader"] for r in readers], "n_readers": len(readers),
           "n_entries": {SOURCES[s]: int((src == s).sum()) for s in range(len(SOURCES))},
           "n_ratings": int((L >= 0).sum())}

    point = np.array([shares(O, np.where(src == s)[0]) for s in range(len(SOURCES))])
    boots = {m: bootstrap(O, strata, s_of, m, rng) for m in ("both", "entries", "readers")}

    def outcome(arr, idx):
        return arr[..., idx].sum(axis=-1)

    res["shares"] = {}
    for s, sname in enumerate(SOURCES):
        res["shares"][sname] = {
            name: {"share": float(outcome(point[s], idx)),
                   "ci95": ci(outcome(boots["both"][:, s, :], idx))}
            for name, idx in OUTCOMES.items()}
    res["difference_new_minus_old"] = {}
    for name, idx in OUTCOMES.items():
        d = {"diff": float(outcome(point[1], idx) - outcome(point[0], idx))}
        for m in boots:
            x = outcome(boots[m][:, 1, :], idx) - outcome(boots[m][:, 0, :], idx)
            d[f"ci95_{m}"] = ci(x)
        res["difference_new_minus_old"][name] = d

    res["by_paper"] = {
        f"{SOURCES[s]}:{p}": {name: float(outcome(shares(O, np.array(
            [i for i in range(len(items)) if src[i] == s and paper[i] == p])), idx))
            for name, idx in OUTCOMES.items()}
        for s in range(len(SOURCES)) for p in papers}

    res["by_reader"] = {}
    for r, row in zip(readers, L):
        res["by_reader"][r["reader"]] = {
            "kind": r["kind"], "model": r["model"], "n": int((row >= 0).sum()),
            **{SOURCES[s]: {lab: int(((row == k) & (src == s)).sum()) for k, lab in enumerate(LABELS)}
               for s in range(len(SOURCES))}}

    # Agreement.
    ag = {}
    for tag, merge in (("four labels", None), ("opaque+unreadable merged", MERGE3),
                       ("milestone vs rest", MERGE_MS), ("readable vs not", MERGE_RD)):
        ag[tag] = {"all entries": fleiss(L, merge)[0]}
        for s, sname in enumerate(SOURCES):
            ag[tag][sname] = fleiss(L[:, src == s], merge)[0]
    res["fleiss"] = ag
    res["fleiss_n_entries"] = fleiss(L)[1]
    full = np.where((L >= 0).all(axis=0))[0]
    if len(readers) >= 2 and len(full):
        ks = [fleiss(L[:, rng.choice(full, len(full))])[0] for _ in range(2000)]
        res["fleiss_four_labels_ci95_entries"] = ci(np.array(ks))
    pairs = []
    for (i, a), (j, b) in itertools.combinations(enumerate(readers), 2):
        k, po, n = cohen(L[i], L[j])
        pairs.append({"a": a["reader"], "b": b["reader"], "kappa": k, "agree": po, "n": n,
                      "same_model": a["model"] is not None and a["model"] == b["model"],
                      "kinds": sorted({a["kind"], b["kind"]})})
    res["pairwise"] = pairs

    # Per-entry disagreement.
    ent = []
    for i, it in enumerate(items):
        col = L[:, i]
        c = Counter(LABELS[k] for k in col if k >= 0)
        n = sum(c.values())
        H = -sum(v / n * math.log2(v / n) for v in c.values()) if n else 0.0
        rd = sum(c[l] for l in LABELS[:2])
        ent.append({"id": it["id"], "source": it["hidden"]["source"], "paper": it["hidden"]["key"],
                    "name": it["hidden"]["name"], "counts": dict(c), "n": n,
                    "distinct": len(c), "entropy_bits": H,
                    "readable_votes": rd, "split_on_readable": 0 < rd < n,
                    "chars_shown": len(it["text"]),
                    "by_reader": {r["reader"]: LABELS[k] for r, k in zip(readers, col) if k >= 0}})
    res["entries"] = ent
    res["unanimous"] = {SOURCES[s]: sum(1 for e in ent if e["distinct"] == 1 and e["source"] == SOURCES[s])
                        for s in range(len(SOURCES))}
    res["chars_shown_median"] = {SOURCES[s]: float(np.median([len(it["text"]) for it in items
                                                              if it["hidden"]["source"] == SOURCES[s]]))
                                 for s in range(len(SOURCES))}
    return res


# ---------------------------------------------------------------- report

def pct(x):
    return "n/a" if x != x else f"{100 * x:.1f}%"


def pp(x):
    return "n/a" if x != x else f"{100 * x:+.1f}"


def iv(c, f=pct):
    return f"{f(c[0])} to {f(c[1])}"


def k2(x):
    return "n/a" if x != x else f"{x:.2f}"


def section(title, res, out):
    n = res["n_readers"]
    out.append(f"## {title}\n")
    out.append(f"{n} reader(s): {', '.join(res['readers'])}. {res['n_ratings']} ratings on "
               f"{res['n_entries']['dominator']} old and {res['n_entries']['outline2']} new entries.\n")
    out.append("### Share of each label, per outline\n")
    out.append("Share of all (reader, entry) ratings. Interval: 95% percentile bootstrap, "
               f"{B} draws, resampling readers and entries together (entries within outline and paper).\n")
    out.append("| Label | Old (lemma-based) | 95% interval | New (definition-centred) | 95% interval |")
    out.append("|---|---|---|---|---|")
    for name in OUTCOMES:
        a, b = res["shares"]["dominator"][name], res["shares"]["outline2"][name]
        out.append(f"| {name} | {pct(a['share'])} | {iv(a['ci95'])} | {pct(b['share'])} | {iv(b['ci95'])} |")
    out.append("")
    out.append("### Difference between outlines (new minus old, percentage points)\n")
    out.append("| Outcome | Difference | 95% interval, readers and entries | entries only | readers only |")
    out.append("|---|---|---|---|---|")
    for name in ("milestone", "opaque or unreadable", "opaque", "unreadable", "technical-step",
                 "readable (milestone or technical-step)"):
        d = res["difference_new_minus_old"][name]
        out.append(f"| {name} | {pp(d['diff'])} | {iv(d['ci95_both'], pp)} | "
                   f"{iv(d['ci95_entries'], pp)} | {iv(d['ci95_readers'], pp)} |")
    out.append("")
    if n < 5:
        out.append(f"With {n} reader(s) the reader half of the bootstrap is close to meaningless; "
                   "read the entries-only column and treat it as a lower bound on the width.\n")
    out.append("By paper (point shares only, 15 entries per cell):\n")
    out.append("| Outline : paper | milestone | technical-step | opaque | unreadable |")
    out.append("|---|---|---|---|---|")
    for k, v in res["by_paper"].items():
        out.append(f"| {k} | {pct(v['milestone'])} | {pct(v['technical-step'])} | {pct(v['opaque'])} | {pct(v['unreadable'])} |")
    out.append("")
    out.append("### Each reader's labels (counts)\n")
    out.append("| Reader | Kind | Model | Old: milestone / technical / opaque / unreadable | New: milestone / technical / opaque / unreadable |")
    out.append("|---|---|---|---|---|")
    for r, v in res["by_reader"].items():
        f = lambda d: " / ".join(str(d[l]) for l in LABELS)
        out.append(f"| {r} | {v['kind']} | {v['model'] or ''} | {f(v['dominator'])} | {f(v['outline2'])} |")
    out.append("")
    if n >= 2:
        out.append("### Agreement between readers\n")
        out.append(f"Fleiss' kappa on the {res['fleiss_n_entries']} entries every reader rated "
                   "(1 = perfect, 0 = chance for these label frequencies).\n")
        out.append("| Labels compared | All entries | Old outline | New outline |")
        out.append("|---|---|---|---|")
        for tag, v in res["fleiss"].items():
            out.append(f"| {tag} | {k2(v['all entries'])} | {k2(v['dominator'])} | {k2(v['outline2'])} |")
        out.append("")
        if "fleiss_four_labels_ci95_entries" in res:
            out.append(f"Four labels, all entries: 95% interval {iv(res['fleiss_four_labels_ci95_entries'], k2)} "
                       "(bootstrap over entries, 2000 draws).\n")
        out.append("Pairwise (Cohen's kappa, four labels; raw agreement in brackets):\n")
        out.append("| Pair | Kappa | Same model |")
        out.append("|---|---|---|")
        for p in sorted(res["pairwise"], key=lambda p: -p["kappa"] if p["kappa"] == p["kappa"] else 9):
            out.append(f"| {p['a']} and {p['b']} | {k2(p['kappa'])} ({pct(p['agree'])}) | {'yes' if p['same_model'] else 'no'} |")
        out.append("")
        same = [p["kappa"] for p in res["pairwise"] if p["same_model"]]
        diff = [p["kappa"] for p in res["pairwise"] if not p["same_model"]]
        if same and diff:
            out.append(f"Mean kappa: {k2(float(np.mean(same)))} over {len(same)} same-model pairs, "
                       f"{k2(float(np.mean(diff)))} over {len(diff)} different-model pairs.\n")
        ne = res["n_entries"]
        out.append(f"Unanimous entries: {res['unanimous']['dominator']} of {ne['dominator']} old, "
                   f"{res['unanimous']['outline2']} of {ne['outline2']} new.\n")
        out.append("### Entries where readers disagreed most\n")
        out.append("Ranked by entropy of the label distribution (bits), then by number of distinct labels. "
                   "\"Split\" marks entries where readers fell on both sides of the readable line.\n")
        out.append("| Entry | Outline : paper | Declaration | Labels | Entropy | Split | Characters shown |")
        out.append("|---|---|---|---|---|---|---|")
        top = sorted(res["entries"], key=lambda e: (-e["entropy_bits"], -e["distinct"], e["id"]))
        for e in [e for e in top if e["distinct"] > 1][:15]:
            lab = ", ".join(f"{l} {e['counts'][l]}" for l in LABELS if l in e["counts"])
            short = e["name"].split(".", 1)[-1]
            out.append(f"| {e['id']} | {e['source']} : {e['paper']} | `{short}` | {lab} | "
                       f"{e['entropy_bits']:.2f} | {'yes' if e['split_on_readable'] else 'no'} | {e['chars_shown']} |")
        out.append("")
        nsplit = {s: sum(1 for e in res["entries"] if e["split_on_readable"] and e["source"] == s) for s in SOURCES}
        out.append(f"Entries split across the readable line: {nsplit['dominator']} of {ne['dominator']} old, "
                   f"{nsplit['outline2']} of {ne['outline2']} new.\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--items", type=Path, default=OUT / "rating_items.json")
    ap.add_argument("--ratings", type=Path, default=OUT / "ratings")
    ap.add_argument("--out", type=Path, default=OUT / "RATINGS.md")
    ap.add_argument("--json", type=Path, default=OUT / "ratings_summary.json")
    a = ap.parse_args()

    items, readers = load(a.items, a.ratings)
    kinds = sorted({r["kind"] for r in readers})
    groups = [("All readers" if len(kinds) > 1 else
               ("Proxy readers (models, not mathematicians)" if kinds == ["proxy"] else "Human readers"),
               readers)]
    if len(kinds) > 1:
        for k in kinds:
            groups.append(("Human readers only" if k == "human" else "Proxy readers only (models)",
                           [r for r in readers if r["kind"] == k]))
    models = sorted({r["model"] for r in readers if r["kind"] == "proxy" and r["model"]})
    summary = {"seed": SEED, "bootstrap_draws": B, "labels": LABELS, "groups": {}}
    out = ["# Proxy ratings of the two outlines (blind to the source label, not to the format)\n",
           "Generated by `bench/outline_ratings.py` from `rating_items.json` and `ratings/*.json`; "
           "numbers are in `ratings_summary.json`. Do not edit by hand: rerun the script. "
           "The hand-written reading at the end is copied from `ratings/READING.md`.\n"]
    nprox = sum(r["kind"] == "proxy" for r in readers)
    nhum = len(readers) - nprox
    out.append(f"**Readers: {nprox} model proxies, {nhum} human mathematicians.** "
               + ("Every number below comes from model readers. " if nhum == 0 else "")
               + "Proxy rows are labelled as such throughout.\n")
    out.append("- Entries: 60, 15 per outline per paper, drawn by a fixed seed before any rating "
               "(rule in `rating_items.json`). Old outline = dominator outline of lemmas (`out/corpus/outline/`); "
               "new = definition-centred outline (`OUTLINE2.md`).")
    out.append("- Rubric, four labels: milestone (a step you could name in a talk), technical-step "
               "(readable, supporting), opaque (cannot tell what it says from what is shown), unreadable (too much to take in).")
    out.append("- Readers did not see which outline an entry came from. They could see the format, and the two "
               "formats differ: new entries carry their chapter context (with corpus docstrings in 23 of 30) and a statement cut at 900 characters; old entries are a statement cut at 420 characters with no docstring.")
    med = analyse(items, readers, np.random.default_rng(SEED))["chars_shown_median"]
    out.append(f"- Median characters shown per entry: {med['dominator']:.0f} old, {med['outline2']:.0f} new.\n")

    for title, rs in groups:
        res = analyse(items, rs, np.random.default_rng(SEED))
        summary["groups"][title] = res
        section(title, res, out)

    if len(models) > 1:
        out.append("## Difference by model family (proxy readers)\n")
        out.append("New minus old, percentage points; interval from entries and that family's readers. "
                   "Shows how far the result depends on which model read.\n")
        out.append("| Model | Readers | milestone | opaque or unreadable | unreadable |")
        out.append("|---|---|---|---|---|")
        summary["by_model"] = {}
        for m in models:
            rs = [r for r in readers if r["kind"] == "proxy" and r["model"] == m]
            res = analyse(items, rs, np.random.default_rng(SEED))
            summary["by_model"][m] = {k: res[k] for k in ("readers", "shares", "difference_new_minus_old")}
            d = res["difference_new_minus_old"]
            cell = lambda k: f"{pp(d[k]['diff'])} ({iv(d[k]['ci95_both'], pp)})"
            out.append(f"| {m} | {len(rs)} | {cell('milestone')} | {cell('opaque or unreadable')} | {cell('unreadable')} |")
        out.append("")

    out.append("## What model readers can and cannot tell us\n")
    out.append("Can:\n")
    out.append("- Whether an entry, as printed, states its conclusion and names only things that are shown. "
               "Truncation and undefined names are visible to any careful reader, and the reasons in the reader files are checkable against the text.")
    out.append("- Whether the printed text is too long to take in at a sitting, as a rough signal.")
    out.append("- How noisy the rubric is: if copies of one model disagree, the label boundaries are not sharp.\n")
    out.append("Cannot:\n")
    out.append("- Say whether a statement is a milestone of this argument. That needs someone who knows the mathematics; "
               "a model's \"milestone\" means \"sounds like a nameable step\", and names alone can produce that impression.")
    out.append("- Stand in for a mathematician's tolerance of long context. A model does not tire, and can also call a "
               "long block unreadable without reading it; either error is possible and these data cannot separate them.")
    out.append("- Count as independent readers. Copies of one model share blind spots, and different model families share "
               "training. The reader half of the bootstrap treats them as a sample of readers; it understates the "
               "uncertainty about what mathematicians would say.")
    out.append("- Rate blind to format. The two outlines look different on the page, so a reader can react to the format "
               "rather than the content.\n")
    out.append("To add a mathematician: copy a reader file in `ratings/`, set `\"kind\": \"human\"`, `\"model\": null`, "
               "fill `ratings` (any subset of the 60 ids; strip `hidden` from the items before showing them), rerun "
               "`python3 bench/outline_ratings.py`. Tables then appear for all readers, humans only and proxies only.\n")

    reading = a.ratings / "READING.md"
    if reading.exists():
        out.append(reading.read_text().rstrip() + "\n")

    a.out.write_text("\n".join(out))
    a.json.write_text(json.dumps(summary, indent=1, ensure_ascii=False,
                                 default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)))
    print(f"wrote {a.out} and {a.json}")


if __name__ == "__main__":
    main()
