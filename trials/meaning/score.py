#!/usr/bin/env python3
"""Score a meaning trial and write REPORT.md, SUMMARY.md and results.json.

    python3 score.py                 # bank next to this script
    python3 score.py --bank DIR      # another item bank

Reads items.json, key.json, responses/*.json and, if present, item_flags.json
and analyst_notes.md. Proxy (model) readers and human readers are never pooled
together. REPORT.md names items and so gives the key away; SUMMARY.md does not.

Standard library only; Python 3.8 or later.
"""
import argparse
import datetime
import glob
import hashlib
import itertools
import json
import math
import os
import random
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
Z = 1.959964
BOOT_N = 4000
BOOT_SEED = 20261110
READER_TYPES = ("proxy", "human")
KEY_FIELDS = ("faithful", "errorKind", "error_kind", "explanation", "structure")


# ---------- statistics ----------

def wilson(k, n):
    if n == 0:
        return None
    p = k / n
    d = 1 + Z * Z / n
    c = (p + Z * Z / (2 * n)) / d
    h = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def boot_items(per_item):
    """Percentile interval for a pooled rate, resampling items (the unit that
    repeats across readers). per_item: list of (k, n) per item."""
    per_item = [x for x in per_item if x[1] > 0]
    if len(per_item) < 2:
        return None
    rng = random.Random(BOOT_SEED)
    m = len(per_item)
    rates = []
    for _ in range(BOOT_N):
        k = n = 0
        for _ in range(m):
            a, b = per_item[rng.randrange(m)]
            k += a
            n += b
        rates.append(k / n)
    rates.sort()
    return (rates[int(0.025 * BOOT_N)], rates[int(0.975 * BOOT_N) - 1])


def cohen_kappa(a, b):
    n = len(a)
    if n == 0:
        return None
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return None if pe >= 1 else (po - pe) / (1 - pe)


def fleiss_kappa(matrix):
    """matrix: one row per item, each row a list of 0/1 ratings, same length."""
    if not matrix or len(matrix[0]) < 2:
        return None
    n = len(matrix[0])
    big_n = len(matrix)
    p1 = sum(sum(r) for r in matrix) / (big_n * n)
    pe = p1 * p1 + (1 - p1) * (1 - p1)
    pbar = sum((sum(r) ** 2 + (n - sum(r)) ** 2 - n) / (n * (n - 1)) for r in matrix) / big_n
    return None if pe >= 1 else (pbar - pe) / (1 - pe)


# ---------- formatting ----------

def pct(x):
    return "%.1f%%" % (100 * x)


def rate(k, n):
    if n == 0:
        return "no items"
    lo, hi = wilson(k, n)
    return "%d/%d = %s [%s, %s]" % (k, n, pct(k / n), pct(lo), pct(hi))


def interval(iv):
    return "n/a" if iv is None else "[%s, %s]" % (pct(iv[0]), pct(iv[1]))


def num(x, digits=2):
    return "n/a" if x is None else ("%." + str(digits) + "f") % x


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join(["---"] * len(header)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "\\|").replace("\n", " ") for c in r) + " |")
    return "\n".join(out)


def shorten(text, n=110):
    text = " ".join(text.split())
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


# ---------- loading ----------

def load(bank_dir, responses_dir, excluded):
    problems = []
    with open(os.path.join(bank_dir, "items.json"), "rb") as f:
        items_bytes = f.read()
    material = json.loads(items_bytes.decode("utf-8"))
    with open(os.path.join(bank_dir, os.path.basename(material["brief_file"])), "rb") as f:
        sha = hashlib.sha256(items_bytes + b"\n" + f.read()).hexdigest()
    with open(os.path.join(bank_dir, "key.json"), encoding="utf-8") as f:
        key = json.load(f)
    if key.get("material_sha256") != sha:
        problems.append("key.json was written for a different version of items.json or the brief (hash mismatch).")
    items = {i["id"]: i for i in material["items"]}
    if set(items) != set(key["items"]):
        sys.exit("items.json and key.json do not cover the same item ids: %s"
                 % sorted(set(items) ^ set(key["items"])))
    for i in material["items"]:
        leaked = [k for k in KEY_FIELDS if k in i]
        if leaked:
            sys.exit("items.json item %s carries key fields %s" % (i["id"], leaked))
    flags = {}
    fp = os.path.join(bank_dir, "item_flags.json")
    if os.path.exists(fp):
        with open(fp, encoding="utf-8") as f:
            flags = json.load(f).get("flags", {})
        for fid in flags:
            if fid not in items:
                sys.exit("item_flags.json names an unknown item %s" % fid)
    readers = []
    for path in sorted(glob.glob(os.path.join(responses_dir, "*.json"))):
        with open(path, encoding="utf-8") as f:
            r = json.load(f)
        name = r.get("reader") or os.path.splitext(os.path.basename(path))[0]
        if name in excluded:
            continue
        if r.get("reader_type") not in READER_TYPES:
            sys.exit("%s: reader_type must be 'proxy' or 'human'" % path)
        ans = {}
        for a in r.get("answers", []):
            if a["id"] not in items:
                sys.exit("%s: unknown item id %s" % (path, a["id"]))
            if a["id"] in ans:
                sys.exit("%s: item %s answered twice" % (path, a["id"]))
            if a.get("judgement") not in material["judgements"]:
                sys.exit("%s: item %s has judgement %r" % (path, a["id"], a.get("judgement")))
            ans[a["id"]] = a
        if r.get("material_sha256") != sha:
            problems.append("%s answered a different version of the items or brief (hash mismatch)." % name)
        r["_name"], r["_answers"] = name, ans
        readers.append(r)
    names = [r["_name"] for r in readers]
    if len(set(names)) != len(names):
        sys.exit("two response files share a reader name")
    return material, key, sha, items, flags, readers, problems


# ---------- analysis ----------

def flagged(answer):
    return answer["judgement"] == "not-faithful"


class Analysis:
    def __init__(self, material, key, items, readers):
        self.material, self.key, self.items, self.readers = material, key["items"], items, readers
        self.order = [i["id"] for i in material["items"]]

    def counts(self, readers=None, ids=None):
        """(caught, unfaithful answered, false alarms, faithful answered)."""
        readers = self.readers if readers is None else readers
        ids = self.order if ids is None else ids
        c = u = fa = f = 0
        for r in readers:
            for i in ids:
                a = r["_answers"].get(i)
                if a is None:
                    continue
                if self.key[i]["faithful"]:
                    f += 1
                    fa += flagged(a)
                else:
                    u += 1
                    c += flagged(a)
        return c, u, fa, f

    def per_item(self, ids, readers=None):
        readers = self.readers if readers is None else readers
        out = []
        for i in ids:
            got = [r["_answers"][i] for r in readers if i in r["_answers"]]
            out.append((sum(flagged(a) for a in got), len(got)))
        return out

    def ids(self, kind=None, faithful=None, structure=None, error_kind=None, exclude=()):
        out = []
        for i in self.order:
            k = self.key[i]
            if i in exclude:
                continue
            if kind is not None and self.items[i]["kind"] != kind:
                continue
            if faithful is not None and k["faithful"] != faithful:
                continue
            if structure is not None and k.get("structure") != structure:
                continue
            if error_kind is not None and k["error_kind"] != error_kind:
                continue
            out.append(i)
        return out

    def pooled_row(self, label, ids, readers=None):
        c, u, fa, f = self.counts(readers, ids)
        bad = [i for i in ids if not self.key[i]["faithful"]]
        good = [i for i in ids if self.key[i]["faithful"]]
        return {"label": label, "caught": c, "unfaithful": u, "false_alarms": fa, "faithful": f,
                "n_unfaithful_items": len(bad), "n_faithful_items": len(good),
                "catch_boot": boot_items(self.per_item(bad, readers)),
                "fa_boot": boot_items(self.per_item(good, readers))}

    def agreement(self, ids):
        pairs = []
        for a, b in itertools.combinations(self.readers, 2):
            common = [i for i in ids if i in a["_answers"] and i in b["_answers"]]
            if not common:
                continue
            x = [int(flagged(a["_answers"][i])) for i in common]
            y = [int(flagged(b["_answers"][i])) for i in common]
            pairs.append({"a": a["_name"], "b": b["_name"], "n": len(common),
                          "agree": sum(1 for p, q in zip(x, y) if p == q) / len(common),
                          "kappa": cohen_kappa(x, y)})
        full = [r for r in self.readers if all(i in r["_answers"] for i in ids)]
        matrix = [[int(flagged(r["_answers"][i])) for r in full] for i in ids]
        unanimous = sum(1 for row in matrix if len(set(row)) == 1) if full else 0
        kappas = [p["kappa"] for p in pairs if p["kappa"] is not None]
        return {"pairs": pairs, "n_pairs": len(pairs),
                "mean_agree": statistics.mean(p["agree"] for p in pairs) if pairs else None,
                "min_agree": min((p["agree"] for p in pairs), default=None),
                "mean_kappa": statistics.mean(kappas) if kappas else None,
                "min_kappa": min(kappas, default=None),
                "fleiss": fleiss_kappa(matrix) if len(full) >= 2 else None,
                "n_full_readers": len(full), "n_items": len(ids), "unanimous": unanimous}


def render_group(an, rtype, flags, targets, public=False):
    """Markdown for one reader type. public=True leaves out everything that names an item."""
    L = []
    rs = an.readers
    parts = an.material["parts"]
    data = {"readers": [], "pooled": [], "by_model": [], "sensitivity": [], "agreement": {}, "missed": [], "false_alarms": []}
    if not rs:
        L.append("No %s readers have taken this trial yet." % rtype)
        return "\n".join(L), data

    # readers
    rows = []
    for r in rs:
        rows.append([r["_name"], r.get("model_id") or r.get("model") or "-", "%d of %d" % (len(r["_answers"]), len(an.order)),
                     r.get("presentation") or "-", r.get("caveat") or ""])
    L += ["### Readers", "", table(["reader", "model", "answered", "how the items were shown", "caveat"], rows), ""]

    # per reader
    head = ["reader"]
    for p in parts:
        head += [p["kind"] + ": caught", p["kind"] + ": false alarms"]
    head += ["all: caught", "all: false alarms"]
    rows = []
    for r in rs:
        row = [r["_name"]]
        rec = {"reader": r["_name"], "model": r.get("model"), "answered": len(r["_answers"])}
        for p in parts:
            c, u, fa, f = an.counts([r], an.ids(kind=p["kind"]))
            row += [rate(c, u), rate(fa, f)]
            rec[p["kind"]] = {"caught": c, "unfaithful": u, "false_alarms": fa, "faithful": f}
        c, u, fa, f = an.counts([r])
        row += [rate(c, u), rate(fa, f)]
        rec["all"] = {"caught": c, "unfaithful": u, "false_alarms": fa, "faithful": f}
        rows.append(row)
        data["readers"].append(rec)
    L += ["### Per reader", "",
          "Share of unfaithful items the reader flagged (caught) and share of faithful items the reader flagged "
          "(false alarms), each with a 95% Wilson interval.", "", table(head, rows), ""]

    # pooled
    strata = [("all items", an.ids())]
    for p in parts:
        strata.append((p["kind"] + " items", an.ids(kind=p["kind"])))
    for s in ("single-piece", "composition"):
        ids = an.ids(structure=s)
        if ids:
            strata.append(("wrong in a single piece" if s == "single-piece" else "wrong only through composition", ids))
        for p in parts:
            ids2 = an.ids(kind=p["kind"], structure=s)
            if ids2 and len(ids2) != len(ids):
                strata.append(("  %s, %s" % (p["kind"], s), ids2))
    kinds = []
    for i in an.order:
        ek = an.key[i]["error_kind"]
        if not an.key[i]["faithful"] and ek not in kinds:
            kinds.append(ek)
    for ek in sorted(kinds):
        strata.append(("error kind: " + ek, an.ids(error_kind=ek)))
    rows = []
    for label, ids in strata:
        pr = an.pooled_row(label, ids)
        data["pooled"].append(pr)
        rows.append([label.replace("  ", "&nbsp;&nbsp;"), pr["n_unfaithful_items"], rate(pr["caught"], pr["unfaithful"]), interval(pr["catch_boot"]),
                     pr["n_faithful_items"] or "-", rate(pr["false_alarms"], pr["faithful"]) if pr["faithful"] else "-",
                     interval(pr["fa_boot"]) if pr["faithful"] else "-"])
    L += ["### Pooled over %s readers" % rtype, "",
          "Every reader's judgement of every item counts once. The Wilson interval treats those judgements as "
          "independent, which they are not (the same items repeat across readers), so it is too narrow. The "
          "'items resampled' interval is a bootstrap that resamples items instead (%d draws, seed %d); it is "
          "the better guide to what a different item bank might give, and it collapses to a single point when "
          "every item in the row has the same result." % (BOOT_N, BOOT_SEED), "",
          table(["items", "wrong items", "caught (Wilson 95%)", "caught, items resampled", "faithful items",
                 "false alarms (Wilson 95%)", "false alarms, items resampled"], rows), ""]
    if targets:
        L += ["Plan targets, as a signal and not a gate: at least %s caught, at most %s false alarms (%s)."
              % (pct(targets["catch_rate_min"]), pct(targets["false_alarm_rate_max"]), targets.get("source", "")), ""]

    # by model
    models = []
    for r in rs:
        m = r.get("model_id") or r.get("model") or "-"
        if m not in models:
            models.append(m)
    if rtype == "proxy" and len(models) > 1:
        rows = []
        for m in models:
            sub = [r for r in rs if (r.get("model_id") or r.get("model") or "-") == m]
            c, u, fa, f = an.counts(sub)
            rows.append([m, len(sub), rate(c, u), rate(fa, f)])
            data["by_model"].append({"model": m, "readers": len(sub), "caught": c, "unfaithful": u, "false_alarms": fa, "faithful": f})
        L += ["### By model", "", table(["model", "readers", "caught", "false alarms"], rows), ""]

    # sensitivity
    debatable = [i for i, v in flags.items() if v.get("severity") == "key-debatable"]
    caveated = [r for r in rs if r.get("caveat")]
    variants = [("all readers, all items", rs, ())]
    if debatable:
        variants.append(("without items whose key is flagged as debatable" + ("" if public else " (%s)" % ", ".join(sorted(debatable))), rs, debatable))
    if caveated and len(caveated) < len(rs):
        variants.append(("without readers carrying a caveat (%s)" % ", ".join(r["_name"] for r in caveated),
                         [r for r in rs if not r.get("caveat")], ()))
        if debatable:
            variants.append(("without both", [r for r in rs if not r.get("caveat")], debatable))
    if len(variants) > 1:
        rows = []
        for label, sub, excl in variants:
            c, u, fa, f = an.counts(sub, an.ids(exclude=excl))
            rows.append([label, rate(c, u), rate(fa, f)])
            data["sensitivity"].append({"variant": label, "caught": c, "unfaithful": u, "false_alarms": fa, "faithful": f})
        L += ["### Sensitivity", "", "The same pooled rates with flagged items or caveated readers left out. "
              "Nothing is dropped from the tables above.", "", table(["variant", "caught", "false alarms"], rows), ""]

    # agreement
    rows = []
    for label, ids in [("all items", an.ids())] + [(p["kind"] + " items", an.ids(kind=p["kind"])) for p in parts]:
        ag = an.agreement(ids)
        data["agreement"][label] = {k: v for k, v in ag.items() if k != "pairs"}
        rows.append([label, ag["n_pairs"], pct(ag["mean_agree"]) if ag["mean_agree"] is not None else "n/a",
                     pct(ag["min_agree"]) if ag["min_agree"] is not None else "n/a",
                     num(ag["mean_kappa"]), num(ag["min_kappa"]), num(ag["fleiss"]),
                     "%d of %d" % (ag["unanimous"], ag["n_items"]) if ag["n_full_readers"] >= 2 else "n/a"])
    if len(rs) >= 2:
        L += ["### Agreement between readers", "",
              "Pairwise agreement on the faithful / not-faithful judgement, Cohen's kappa per pair, Fleiss' kappa over "
              "readers who answered every item, and the number of items on which those readers were unanimous. "
              "Agreement is between readers, whether or not they agree with the key.", "",
              table(["items", "reader pairs", "mean agreement", "lowest pair", "mean Cohen kappa", "lowest kappa",
                     "Fleiss kappa", "unanimous items"], rows), ""]
    else:
        L += ["### Agreement between readers", "", "Only one reader; no agreement figures.", ""]

    # confidence and time
    right, wrong = [], []
    for r in rs:
        for i, a in r["_answers"].items():
            if a.get("confidence") is None:
                continue
            ok = flagged(a) != an.key[i]["faithful"]
            (right if ok else wrong).append(a["confidence"])
    L += ["### Confidence and time", ""]
    L.append("- Mean stated confidence on answers that match the key: %s (n = %d); on answers that do not: %s (n = %d)."
             % (num(statistics.mean(right)) if right else "n/a", len(right),
                num(statistics.mean(wrong)) if wrong else "n/a", len(wrong)))
    data["confidence"] = {"mean_when_matching_key": statistics.mean(right) if right else None, "n_matching": len(right),
                          "mean_when_not": statistics.mean(wrong) if wrong else None, "n_not": len(wrong)}
    timed = []
    for r in rs:
        secs = [a["seconds"] for a in r["_answers"].values() if a.get("seconds") is not None]
        if secs:
            timed.append("%s: median %.0f s per item, %.0f min in total" % (r["_name"], statistics.median(secs), sum(secs) / 60))
    L.append("- Time per item: " + ("; ".join(timed) + "." if timed else "not recorded for these readers."))
    L.append("")

    if public:
        return "\n".join(L), data

    # misses and false alarms by item
    for faithful, title, word, store in ((False, "Unfaithful items most often missed", "missed", "missed"),
                                         (True, "Faithful items most often flagged", "flagged", "false_alarms")):
        rows = []
        for i in an.ids(faithful=faithful):
            got = [(r, r["_answers"][i]) for r in rs if i in r["_answers"]]
            hit = [(r, a) for r, a in got if flagged(a) == faithful]
            if not hit:
                continue
            k = an.key[i]
            data[store].append({"id": i, "error_kind": k["error_kind"], "structure": k.get("structure"),
                                "count": len(hit), "of": len(got), "readers": [r["_name"] for r, _ in hit]})
            reasons = "<br>".join("%s (%.2f): %s" % (r["_name"], a.get("confidence") or 0, shorten(a.get("reason") or "", 200))
                                  for r, a in hit)
            flag = " **[flagged: %s]**" % flags[i].get("severity") if i in flags else ""
            what = ("" if faithful else "%s, %s. " % (k["error_kind"], k.get("structure"))) + shorten(an.items[i]["first"], 120)
            rows.append((len(hit), [i + flag, "%d of %d" % (len(hit), len(got)), what, reasons]))
        rows.sort(key=lambda x: -x[0])
        L += ["### " + title, ""]
        if rows:
            L += [table(["item", word + " by", "kind and first text" if not faithful else "first text",
                         "who, their confidence and their reason"], [r for _, r in rows]), ""]
        else:
            L += ["None: no %s reader %s any such item." % (rtype, "missed" if not faithful else "flagged"), ""]
        if not faithful:
            never = [i for i in an.ids(faithful=False) if i not in [d["id"] for d in data["missed"]]]
            L += ["Caught by every %s reader who answered it: %s." % (rtype, ", ".join(never) or "none"), ""]
    return "\n".join(L), data


def item_table(an_by_type, material, key, flags):
    rows = []
    for i in material["items"]:
        k = key["items"][i["id"]]
        row = [i["id"], i["kind"], "faithful" if k["faithful"] else "NOT faithful", k["error_kind"] if not k["faithful"] else "-",
               k.get("structure") or "-"]
        for t in READER_TYPES:
            an = an_by_type[t]
            got = [r["_answers"][i["id"]] for r in an.readers if i["id"] in r["_answers"]]
            row.append("%d of %d" % (sum(flagged(a) for a in got), len(got)) if got else "-")
        row.append(flags.get(i["id"], {}).get("severity", ""))
        rows.append(row)
    return table(["item", "part", "key", "error kind", "structure", "proxy readers who flagged it",
                  "human readers who flagged it", "flag"], rows)


def headline(an, rtype):
    if not an.readers:
        return ["- **%s readers:** none yet." % rtype.capitalize()]
    out = []
    c, u, fa, f = an.counts()
    answered = "%d reader%s" % (len(an.readers), "" if len(an.readers) == 1 else "s")
    out.append("- **%s readers (%s), all items:** caught %s; false alarms %s." % (rtype.capitalize(), answered, rate(c, u), rate(fa, f)))
    for p in an.material["parts"]:
        c, u, fa, f = an.counts(ids=an.ids(kind=p["kind"]))
        out.append("  - %s items: caught %s; false alarms %s." % (p["kind"], rate(c, u), rate(fa, f)))
    for s, label in (("single-piece", "wrong in a single piece"), ("composition", "wrong only through composition")):
        ids = an.ids(structure=s)
        if ids:
            c, u, _, _ = an.counts(ids=ids)
            out.append("  - %s: caught %s." % (label, rate(c, u)))
    per = []
    for r in an.readers:
        c, u, fa, f = an.counts([r])
        if u:
            per.append(c / u)
    if per:
        out.append("  - per reader, share caught ranges from %s to %s." % (pct(min(per)), pct(max(per))))
    return out


def main():
    ap = argparse.ArgumentParser(description="Score a meaning trial.")
    ap.add_argument("--bank", default=HERE)
    ap.add_argument("--responses-dir", default=None)
    ap.add_argument("--out", default=None, help="directory for REPORT.md, SUMMARY.md and results.json (default: the bank)")
    ap.add_argument("--exclude-reader", action="append", default=[], help="leave a reader out (repeatable); named in the report")
    args = ap.parse_args()
    responses_dir = args.responses_dir or os.path.join(args.bank, "responses")
    out_dir = args.out or args.bank
    os.makedirs(out_dir, exist_ok=True)
    material, key, sha, items, flags, readers, problems = load(args.bank, responses_dir, set(args.exclude_reader))
    targets = key.get("targets")
    an = {t: Analysis(material, key, items, [r for r in readers if r["reader_type"] == t]) for t in READER_TYPES}
    stamp = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    n_bad = sum(1 for v in key["items"].values() if not v["faithful"])

    common = ["Generated by `score.py` on %s. Items and brief: `%s`, sha256 `%s`. %d items, %d of them unfaithful by the key."
              % (stamp, material["bank"], sha[:16], len(items), n_bad)]
    if args.exclude_reader:
        common.append("Readers left out on the command line: %s." % ", ".join(args.exclude_reader))
    for p in problems:
        common.append("**Warning:** " + p)
    incomplete = [r["_name"] for r in readers if len(r["_answers"]) < len(items)]
    if incomplete:
        common.append("Readers who have not answered every item (scored on what they answered): %s." % ", ".join(incomplete))

    notes_path = os.path.join(args.bank, "analyst_notes.md")
    notes = open(notes_path, encoding="utf-8").read().strip() if os.path.exists(notes_path) else None

    results = {"generated": stamp, "bank": material["bank"], "material_sha256": sha, "targets": targets,
               "excluded_readers": args.exclude_reader, "warnings": problems, "flags": flags}

    for public in (False, True):
        L = ["# %s: %s" % (material.get("title", material["bank"]), "summary without the key" if public else "report"), ""]
        if public:
            L += ["This file names no items and can be shown to people who have not yet taken the trial. "
                  "The full report (`REPORT.md`) gives the key away and is kept with the key.", ""]
        else:
            L += ["**This report gives the answer key away. Do not show it to anyone who may take the trial.**", ""]
        L += common + ["", "## Headline", ""]
        for t in READER_TYPES:
            L += headline(an[t], t)
        L += ["", "Proxy readers are language models answering in place of people. Their numbers are reported "
              "separately from human readers' and are not evidence about people.", ""]
        if targets:
            L += ["Plan targets (a signal, not a gate): at least %s of unfaithful items caught, at most %s false alarms."
                  % (pct(targets["catch_rate_min"]), pct(targets["false_alarm_rate_max"])), ""]
        if notes and not public:
            L += [notes, ""]
        for t in READER_TYPES:
            L += ["## %s readers" % t.capitalize(), ""]
            text, data = render_group(an[t], t, flags, targets, public)
            L += [text, ""]
            if not public:
                results[t] = data
        if not public:
            L += ["## Every item", "", item_table(an, material, key, flags), ""]
            if flags:
                L += ["### Flags", ""] + ["- **%s** (%s): %s" % (i, v.get("severity"), v.get("note", "")) for i, v in sorted(flags.items())] + [""]
        L += ["## Method", "",
              "- A reader judges each item faithful or not-faithful. An unfaithful item is *caught* when the reader says "
              "not-faithful; a *false alarm* is a faithful item the reader says is not-faithful. The reason a reader gives "
              "is recorded but not marked: a catch for the wrong reason still counts as a catch.",
              "- Intervals are 95%% Wilson score intervals. With %d unfaithful items, one reader who catches all of them "
              "has an interval of %s, so a single reader cannot be placed above or below a 90%% target."
              % (n_bad, interval(wilson(n_bad, n_bad))),
              "- Proxy and human readers are scored by the same code and never pooled together.",
              "- Readers who have answered only some items are scored on the items they answered.",
              "- Re-run `python3 score.py` after adding a file to `responses/`.", ""]
        name = "SUMMARY.md" if public else "REPORT.md"
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
            f.write("\n".join(L).rstrip() + "\n")
    with open(os.path.join(out_dir, "results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        f.write("\n")
    for t in READER_TYPES:
        for line in headline(an[t], t):
            print(line)
    for p in problems:
        print("WARNING: " + p)
    print("wrote %s" % ", ".join(os.path.join(out_dir, n) for n in ("REPORT.md", "SUMMARY.md", "results.json")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
