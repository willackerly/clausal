#!/usr/bin/env python3
"""Independent recomputation of the K2 detection matrix from the raw per-mutant JSON.

Written for the review, from PREREG.md's definition of detection, without importing
harness/analyse.py. Reads results/raw/*.json and results/raw/confirm/*.json (or another raw
directory given as argv[1]); writes review/recomputed.json and prints every figure it checks
against results/summary.json, results/results.json and the numbers quoted in TRADES.md.

    python3 review/recompute.py [raw dir]
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMPARE = HERE.parent
RAW = Path(sys.argv[1]) if len(sys.argv) > 1 else COMPARE / "results" / "raw"
RULES = json.loads((COMPARE / "rules.json").read_text())["rules"]
KIND = {r["id"]: r["kind"] for r in RULES}
CRATE = {r["id"]: r["crate"] for r in RULES}
KINDS = ["safety", "exact", "rejection", "progress", "bound"]
ARMS = ["a", "bp", "be", "c", "d"]


def load():
    raw = {}
    for p in sorted(RAW.glob("*.json")):
        raw[p.stem] = json.loads(p.read_text())
    conf = {}
    if (RAW / "confirm").exists():
        for p in sorted((RAW / "confirm").glob("*.json")):
            conf[p.stem] = json.loads(p.read_text())
    return raw, conf


def classify(m, base, conf):
    """Per rule of the mutated crate: what each arm says, by PREREG's table."""
    out = {}
    d = m.get("d") or {}
    proofs = d.get("proofs")
    failed = set((proofs or {}).get("failed", []))
    built = set((proofs or {}).get("built", []))
    cf = (conf.get(m["id"]) or {}).get("rules", {})
    for rid in [r["id"] for r in RULES if r["crate"] == m["crate"]]:
        o = {}
        # a: an Examples row that passes on the unmutated code does not pass (or the run hangs)
        brows = base["a"]["rows"].get(rid, {})
        mrows = m["a"]["rows"].get(rid, {})
        bad = []
        for line, x in brows.items():
            if x["status"] != "pass":
                continue
            y = mrows.get(line)
            if y is None:
                bad.append((line, "missing"))
            elif y["status"] != "pass":
                bad.append((line, y["status"] + (" GIVEN-FALSE" if "GIVEN-FALSE" in y.get("message", "") else "")))
        if "hang" in mrows:
            bad.append(("hang", "hang"))
        o["a"] = bool(bad)
        o["a_why"] = bad
        # b
        for prof, key in (("plain", "bp"), ("edge", "be")):
            pr = m["b"][prof]["rules"].get(rid)
            o[key] = bool(pr) and pr["status"] in ("fail", "hang")
            o[key + "_status"] = pr["status"] if pr else "not run"
            o[key + "_calls"] = pr["calls_to_first_failure"] if pr and pr["status"] == "fail" else None
        # c
        cr = m["c"]["rules"].get(rid)
        o["c"] = bool(cr) and cr["status"] == "failed"
        o["c_status"] = cr["status"] if cr else "not run"
        o["c_checks"] = cr["failed_checks"] if cr else []
        # d
        key = f"{m['crate']}.{rid}"
        v = (d.get("verdicts") or {}).get(key)
        module = f"Wallet.Proofs.{m['crate']}.{rid}"
        srch = ((d.get("search") or {}).get(key) or {})
        rowfail = [x for x in srch.get("rows", []) if x.get("check") not in ("pass", "givenFalse")]
        c = cf.get(rid) or {}
        if v in ("REFUTED", "COUNTEREXAMPLE"):
            dout = "own:" + v
        elif v is not None and not v.startswith("PROVED") and rowfail:
            dout = "own:row-on-model"
        elif v is not None and v.startswith("PROVED"):
            dout = "proved"
        elif v is None and proofs is None:
            dout = "no-model"
        elif v is None and module in built:
            dout = "proved(no audit: pipeline stopped)"
        elif v == "TESTED-ONLY" or (v is None and module in failed):
            dout = ("lost+confirmed:" + str(c.get("confirmed_on"))) if c.get("confirmed") else "lost"
        else:
            dout = f"OTHER:{v}"
        o["d_out"] = dout
        o["d_own"] = dout.startswith("own:")
        o["d"] = dout.startswith("own:") or dout.startswith("lost+confirmed")
        o["d_module_failed"] = module in failed
        out[rid] = o
    return out


def main():
    raw, conf = load()
    base = raw.pop("baseline")
    muts = json.loads((COMPARE / "mutants/cargo-mutants.json").read_text())["mutants"] + \
        json.loads((COMPARE / "mutants/hand-written.json").read_text())["mutants"]
    meta = {m["id"]: m for m in muts}
    missing = [m for m in meta if m not in raw]
    recs = {}
    for mid, m in raw.items():
        if "harness_error" in m:
            print("HARNESS ERROR", mid)
            continue
        if not m.get("viable", True):
            recs[mid] = {"viable": False}
            continue
        recs[mid] = {"viable": True, "set": m["set"], "crate": m["crate"], "author": m.get("author"),
                     "oracle_differs": m["oracle"]["differs"], "oracle_ok": m["oracle"]["ok"], "rules": classify(m, base, conf)}
    print(f"raw files: {len(raw)} mutants; missing from raw: {missing}; unviable: {[k for k, r in recs.items() if not r['viable']]}")
    print("oracle not ok:", [k for k, r in recs.items() if r["viable"] and not r["oracle_ok"]],
          "| oracle finds no difference:", [k for k, r in recs.items() if r["viable"] and not r["oracle_differs"]])

    def S(st):
        return {k: r for k, r in recs.items() if r.get("set") == st}

    # ---------- baseline
    bl = []
    for r in RULES:
        rid = r["id"]
        rows = base["a"]["rows"].get(rid, {})
        bl.append((rid, len(rows), all(x["status"] == "pass" for x in rows.values()),
                   base["b"]["plain"]["rules"][rid]["status"], base["b"]["edge"]["rules"][rid]["status"],
                   base["c"]["rules"][rid]["status"], base["d"]["verdicts"].get(f"{r['crate']}.{rid}")))
    print("baseline all discharged:", all(x[2] and x[3] == "pass" and x[4] == "pass" and x[5] == "verified" and x[6] == "PROVED-FOR-ALL" for x in bl))

    # ---------- mutant-level counts
    groups = {"cm-wallet": lambda r: r["set"] == "cargo-mutants" and r["crate"] == "wallet",
              "cm-ledger": lambda r: r["set"] == "cargo-mutants" and r["crate"] == "ledger",
              "cm-all": lambda r: r["set"] == "cargo-mutants",
              "hw-wallet": lambda r: r["set"] == "hand-written" and r["crate"] == "wallet",
              "hw-ledger-builder": lambda r: r["set"] == "hand-written" and r["crate"] == "ledger" and r["author"] == "builder",
              "hw-ledger-reviewer": lambda r: r["set"] == "hand-written" and r["author"] == "reviewer",
              "hw-all": lambda r: r["set"] == "hand-written"}
    counts = {}
    for g, f in groups.items():
        rs = [r for r in recs.values() if r["viable"] and f(r)]
        c = {a: sum(1 for r in rs if any(o[a] for o in r["rules"].values())) for a in ARMS}
        c["n"] = len(rs)
        c["d_own"] = sum(1 for r in rs if any(o["d_own"] for o in r["rules"].values()))
        c["d_conf_only"] = c["d"] - c["d_own"]
        c["no_arm"] = sum(1 for r in rs if not any(o[a] for o in r["rules"].values() for a in ARMS))
        c["d_lost_only"] = sum(1 for r in rs if not any(o["d"] for o in r["rules"].values()) and any(o["d_out"] == "lost" for o in r["rules"].values()))
        c["d_no_model"] = sum(1 for r in rs if any(o["d_out"] == "no-model" for o in r["rules"].values()))
        counts[g] = c
        print(f"{g:20s} n={c['n']:2d} a={c['a']} bp={c['bp']} be={c['be']} c={c['c']} d={c['d']} ({c['d_own']}+{c['d_conf_only']}) "
              f"lost-only={c['d_lost_only']} no-model={c['d_no_model']} no-arm={c['no_arm']}")

    # ---------- pair-level by kind
    bykind = {}
    for st in ("cargo-mutants", "hand-written"):
        bykind[st] = {}
        tot = Counter()
        for k in KINDS:
            pairs = [(mid, rid, o) for mid, r in S(st).items() if r["viable"] for rid, o in r["rules"].items() if KIND[rid] == k]
            false = [(mid, rid, o) for mid, rid, o in pairs if any(o[a] for a in ARMS)]
            row = {"rules": len({rid for _, rid, _ in pairs}), "all_pairs": len(pairs), "false_pairs": len(false),
                   "false_mutants": len({mid for mid, _, _ in false})}
            for a in ARMS:
                row[a] = sum(1 for _, _, o in false if o[a])
                row[a + "_mut"] = len({mid for mid, _, o in false if o[a]})
            row["d_own"] = sum(1 for _, _, o in false if o["d_own"])
            row["c_timeout"] = sum(1 for _, _, o in pairs if o["c_status"] == "timeout")
            row["d_lost"] = sum(1 for _, _, o in pairs if o["d_out"] == "lost")
            row["d_lost_kani_verified_no_prop"] = sum(1 for _, _, o in pairs if o["d_out"] == "lost" and o["c_status"] == "verified" and not o["bp"] and not o["be"])
            row["d_proved"] = sum(1 for _, _, o in pairs if o["d_out"].startswith("proved"))
            bykind[st][k] = row
            for x in ("false_pairs", "a", "bp", "be", "c", "d", "d_own", "all_pairs", "d_lost", "d_proved"):
                tot[x] += row[x]
        bykind[st]["all"] = dict(tot)
        print(f"\n{st}: kind | rules | false pairs (mut) | a | bp | be | c | d (own) | c timeouts | d lost (Kani-verified & no prop failure) | d proved | all pairs")
        for k in KINDS + ["all"]:
            r = bykind[st][k]
            if k == "all":
                print(f"  all | | {r['false_pairs']} | {r['a']} | {r['bp']} | {r['be']} | {r['c']} | {r['d']} ({r['d_own']}) | | {r['d_lost']} | {r['d_proved']} | {r['all_pairs']}")
            else:
                print(f"  {k} | {r['rules']} | {r['false_pairs']} ({r['false_mutants']}) | {r['a']} ({r['a_mut']}) | {r['bp']} ({r['bp_mut']}) | {r['be']} ({r['be_mut']}) | "
                      f"{r['c']} ({r['c_mut']}) | {r['d']} ({r['d_mut']}); {r['d_own']} own | {r['c_timeout']} | {r['d_lost']} ({r['d_lost_kani_verified_no_prop']}) | {r['d_proved']} | {r['all_pairs']}")

    # ---------- Lean outcomes
    print("\nLean outcome per pair:")
    for st in ("cargo-mutants", "hand-written"):
        print(" ", st, dict(Counter(o["d_out"] for r in S(st).values() if r["viable"] for o in r["rules"].values())))

    # ---------- checks of specific claims
    print("\nChecks:")
    for st in ("cargo-mutants", "hand-written"):
        rs = {k: r for k, r in S(st).items() if r["viable"]}
        # proof alone: a mutant detected by d and by no other arm
        only_d = [k for k, r in rs.items() if any(o["d"] for o in r["rules"].values()) and not any(o[a] for o in r["rules"].values() for a in ("a", "bp", "be", "c"))]
        # pairs d detects that no other arm detects
        d_alone_pairs = [f"{k}:{rid}" for k, r in rs.items() for rid, o in r["rules"].items() if o["d"] and not any(o[a] for a in ("a", "bp", "be", "c"))]
        # still proved but some arm detects (disagreement)
        dis = [f"{k}:{rid}:{a}" for k, r in rs.items() for rid, o in r["rules"].items() if o["d_out"].startswith("proved") for a in ("a", "bp", "be", "c") if o[a]]
        proved_not_kani_verified = [f"{k}:{rid}:{o['c_status']}" for k, r in rs.items() for rid, o in r["rules"].items() if o["d_out"].startswith("proved") and o["c_status"] != "verified"]
        lost = [(k, rid, o) for k, r in rs.items() for rid, o in r["rules"].items() if o["d_out"] == "lost"]
        lost_not_clean = [f"{k}:{rid}: c={o['c_status']} bp={o['bp']} be={o['be']} a={o['a']}" for k, rid, o in lost if not (o["c_status"] == "verified" and not o["bp"] and not o["be"])]
        lost_total = sum(1 for k, r in rs.items() for rid, o in r["rules"].items() if o["d_module_failed"] or o["d_out"].startswith("lost"))
        noaudit = [f"{k}:{rid}" for k, r in rs.items() for rid, o in r["rules"].items() if o["d_out"] == "proved(no audit: pipeline stopped)"]
        a_nonfail = [f"{k}:{rid}:{o['a_why']}" for k, r in rs.items() for rid, o in r["rules"].items() if o["a"] and not any(w[1] == "fail" or w[1] == "hang" for w in o["a_why"])]
        a_given_false = [f"{k}:{rid}" for k, r in rs.items() for rid, o in r["rules"].items() if any("GIVEN-FALSE" in w[1] for w in o["a_why"])]
        unwind_only = [f"{k}:{rid}" for k, r in rs.items() for rid, o in r["rules"].items()
                       if o["c"] and all("unwinding" in x for x in o["c_checks"])]
        hang_only = {a: [f"{k}:{rid}" for k, r in rs.items() for rid, o in r["rules"].items() if o[a + "_status"] == "hang"] for a in ("bp", "be")}
        calls = [o[a + "_calls"] for r in rs.values() for o in r["rules"].values() for a in ("bp", "be") if o[a + "_calls"]]
        sole_pairs = defaultdict(list)
        for k, r in rs.items():
            for rid, o in r["rules"].items():
                f = [a for a in ("a", "be", "c") if o[a]] + (["d_own"] if o["d_own"] else [])
                if len(f) == 1:
                    sole_pairs[f[0]].append(f"{k}:{rid}")
        sole_pairs_plain = defaultdict(list)
        for k, r in rs.items():
            for rid, o in r["rules"].items():
                f = [a for a in ("a", "bp", "c") if o[a]] + (["d_own"] if o["d_own"] else [])
                if len(f) == 1:
                    sole_pairs_plain[f[0]].append(f"{k}:{rid}")
        misses = {}
        for a in ("a", "bp", "be", "c", "d_own"):
            misses[a] = [f"{k}:{rid}" for k, r in rs.items() for rid, o in r["rules"].items()
                         if any(o[x] for x in ARMS) and not (o["d_own"] if a == "d_own" else o[a])]
        print(f"  [{st}] mutants caught by proof alone: {only_d}; pairs only d detects: {d_alone_pairs}")
        print(f"  [{st}] disagreements (arm detects, kernel still proves): {dis}")
        print(f"  [{st}] still-proved pairs Kani does NOT verify: {proved_not_kani_verified}")
        print(f"  [{st}] proofs lost (module failed or lost/confirmed): {lost_total}; lost & not shown false: {len(lost)}; of which NOT (Kani verified and no proptest failure): {lost_not_clean}")
        print(f"  [{st}] 'still proved' without the audit (pipeline stopped before step 6): {len(noaudit)} {noaudit}")
        print(f"  [{st}] arm a detections not resting on a failing/hung row: {a_nonfail}; resting on GIVEN-FALSE: {a_given_false}")
        print(f"  [{st}] Kani detections resting only on unwinding assertions: {len(unwind_only)} {unwind_only}")
        print(f"  [{st}] proptest hang detections: {hang_only}")
        if calls:
            print(f"  [{st}] proptest calls to first failure: median {statistics.median(calls)} max {max(calls)} n={len(calls)}")
        print(f"  [{st}] sole finder pairs (edge as b): { {k: (len(v), v) for k, v in sole_pairs.items()} }")
        print(f"  [{st}] sole finder pairs (plain as b): { {k: len(v) for k, v in sole_pairs_plain.items()} } c-only: {sole_pairs_plain.get('c')}")
        print(f"  [{st}] misses per arm: { {a: len(v) for a, v in misses.items()} }")
        print(f"  [{st}]   Kani misses: {misses['c']}")
        print(f"  [{st}]   d_own misses: {misses['d_own']}")
        mut_sole = defaultdict(list)
        for k, r in rs.items():
            f = [a for a in ("a", "be", "c") if any(o[a] for o in r["rules"].values())] + (["d_own"] if any(o["d_own"] for o in r["rules"].values()) else [])
            if len(f) == 1:
                mut_sole[f[0]].append(k)
        print(f"  [{st}] sole finder mutants (edge as b): {dict(mut_sole)}")
        print(f"  [{st}] no arm: {[k for k, r in rs.items() if not any(o[a] for o in r['rules'].values() for a in ARMS)]}")
    (HERE / "recomputed.json").write_text(json.dumps({"raw": str(RAW), "counts": counts, "by_kind": bykind,
                                                       "records": recs}, indent=1, default=str) + "\n")


if __name__ == "__main__":
    main()
