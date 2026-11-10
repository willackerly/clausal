#!/usr/bin/env python3
"""Print the numbers the prose of TRADES.template.md quotes, so they can be checked after a rerun.

    python3 harness/facts.py
"""
import json
from collections import Counter
from pathlib import Path

R = Path(__file__).resolve().parent.parent / "results"
recs = json.loads((R / "results.json").read_text())["mutants"]
summ = json.loads((R / "summary.json").read_text())
ARMS = ["a", "b_plain", "b_edge", "c", "d"]
for st in ("cargo-mutants", "hand-written"):
    rs = [r for r in recs if r["set"] == st and r.get("rules")]
    print(f"== {st}: {len([r for r in recs if r['set'] == st])} mutants, {len(rs)} viable")
    print("  detected by arm (mutants):", {a: sum(1 for r in rs if r["detected_by"][a]) for a in ARMS},
          "| d by own search:", sum(1 for r in rs if any(o["d"]["outcome"].startswith("shown false") for o in r["rules"].values())),
          "| no arm:", [r["id"] for r in rs if not any(r["detected_by"][a] for a in ARMS)])
    out = Counter(o["d"]["outcome"] for r in rs for o in r["rules"].values())
    print("  Lean outcomes (pairs):", dict(out), "| all pairs:", sum(out.values()))
    false_pairs = [(r, rid, o) for r in rs for rid, o in r["rules"].items() if any(o[a]["detected"] for a in ARMS)]
    print("  pairs shown false by some arm:", len(false_pairs), "| by arm:", {a: sum(1 for _, _, o in false_pairs if o[a]["detected"]) for a in ARMS},
          "| d own:", sum(1 for _, _, o in false_pairs if o["d"]["outcome"].startswith("shown false")))
    conf = [(r["id"], rid, o["d"]["confirm"]["source"], o["d"]["confirm"]["confirmed_on"]) for r in rs for rid, o in r["rules"].items() if o["d"]["outcome"] == "proof lost, confirmed false"]
    print("  confirmed:", Counter((c[0], c[2], c[3]) for c in conf))
    lost = [(r, rid, o) for r in rs for rid, o in r["rules"].items() if o["d"]["outcome"] == "proof lost, not shown false"]
    holds = [(r["id"], rid) for r, rid, o in lost if rid in r["d_proof_lost_rule_holds_per_kani"]]
    print("  proof lost, not shown false:", len(lost), "| of which Kani verifies and proptest finds nothing:", len(holds),
          "| the rest:", [(r["id"], rid, o["c"]["status"], o["b_plain"]["status"], o["b_edge"]["status"]) for r, rid, o in lost if (r["id"], rid) not in holds])
    print("  no model pairs false on Rust per another arm:", sum(1 for r in rs for o in r["rules"].values() if o["d"]["outcome"] == "no model" and any(o[a]["detected"] for a in ("a", "b_plain", "b_edge", "c"))))
    print("  lost proofs in all (confirmed + not shown):", len(lost) + len(conf))
    pm = summ["pair_misses"][st]
    print("  pair misses:", {k: len(v) for k, v in pm.items()})
    print("     c:", pm["c"])
    print("     d_own:", Counter(x.split(":")[0] for x in pm["d_own"]))
    print("     b_plain:", Counter(x.split(":")[0] for x in pm["b_plain"]))
    print("     b_edge:", Counter(x.split(":")[0] for x in pm["b_edge"]))
    for b in ("with_b_plain", "with_b_edge"):
        f = summ["sole_finder"][st][b]
        print(f"  sole finders {b}: mutants {f['mutants']} | pairs { {k: v for k, v in f['pairs'].items()} }")
    print("  mutants missed by arm though another detects:", summ["missed"][st])
    by = summ["by_kind"][st]
    for k, v in by.items():
        print(f"  kind {k}: pairs {v['pairs']} ({v['mutants']} mutants) | " + ", ".join(f"{a} {v['arms'][a]['pairs']}" for a in ARMS)
              + f" | d own {v['d_pairs_shown_false_by_pipeline']} | lost-not-shown {v['d_proof_lost_not_shown_false']} (holds {v['d_proof_lost_rule_verified_by_kani']}) | still {v['d_still_proved']} | all {v['pairs_considered']}")
    uw = [(r["id"], rid) for r in rs for rid, o in r["rules"].items() if o["c"]["detected"] and all("unwinding" in c for c in o["c"]["failed_checks"])]
    print("  Kani unwinding-only pairs:", uw, "| Kani timeouts:", sum(len(r["c_timeouts"]) for r in rs), "| disagreements:", [r["id"] for r in rs if r["disagreements"]],
          "| oracle no difference:", [r["id"] for r in rs if not r["oracle"]["differs"]], "| hangs in a:", [r["id"] for r in rs if any(o["a"]["rows_failing"] == ["hang"] for o in r["rules"].values())])
    print("  reviewer mutants:", {r["id"]: {a: len(r["detected_by"][a]) for a in ARMS} for r in rs if r.get("author") == "reviewer"})
print("times:", json.dumps(summ["times"]))
print("baseline secs:", {k: v for k, v in summ["baseline_secs"].items() if not isinstance(v, dict)})
