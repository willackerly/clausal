#!/usr/bin/env python3
"""Cost of each P2 arm from its own logs: attempt log, the full build log of every attempt, and file times.

    python3 p2/score/attempts.py <arm-dir> <buildlog-dir> <out.json>

Reads only. Per attempt (one line of effort/attempts.tsv): time, targets, function, ok/FAILED, the arm's NOTE,
and the error messages from the full lake log that lakebuild.sh left in $TMPDIR (copied to <buildlog-dir> by the
scorer; matched to the attempt by time and module names). A FAILED attempt is classed as
  probe     - its NOTE says it was built to read goals (probe/view/read/show goals) AND every error is
              "unsolved goals" (goals deliberately left open, the only way lakebuild.sh shows them);
  mixed     - NOTE says probe, but some error is something else (a real mistake in the same build);
  real      - anything else.
Per function: attempts, FAILED, real FAILED, the active span (first attempt that touches the function to its last
ok build) and the increment (previous function's last ok build to this one's; the first function starts at the
working copy's creation).
"""
import csv
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

FUNC_OF_MODULE = {
    # arm-fable
    "Stock": "stock_of", "Find": "find_bin", "Restock": "restock", "Take": "take", "Fill": "fill_orders",
    "Count": "product_count", "Dominant": "dominant_product",
    # arm-opus
    "Basic": "stock_of", "StockOf": "stock_of", "FindBin": "find_bin", "FillOrders": "fill_orders",
    "ProductCount": "product_count", "ProbeStep": "(post-hoc probe)",
}
ORDER = ["stock_of", "find_bin", "restock", "take", "fill_orders", "product_count", "dominant_product"]
PROBE_NOTE = re.compile(r"probe|view|read unsolved|show goals", re.I)
EST = dt.timezone(dt.timedelta(hours=-5))


def scen_func(p2: Path):
    rows = list(csv.DictReader((p2 / "base/SCENARIOS.tsv").open(), delimiter="\t"))
    out = {}
    for r in rows:
        out[r["scenario"].split(".")[-1]] = r["rust_function"].split("::")[-1]
    return out


def birth(path: Path):
    s = subprocess.run(["stat", "-f", "%B", str(path)], capture_output=True, text=True).stdout.strip()
    return dt.datetime.fromtimestamp(int(s), dt.timezone.utc) if s else None


def kind(msg: str) -> str:
    m = msg.lower()
    for k, pat in [("unsolved goals", "unsolved goals"), ("unknown identifier/constant", "unknown "),
                   ("type mismatch", "type mismatch"), ("rewrite failed", "rewrite"),
                   ("motive not type correct", "motive is not type correct"), ("simp failed/no progress", "simp"),
                   ("omega failed", "omega"), ("scalar_tac failed", "scalar_tac"), ("no goals", "no goals"),
                   ("application type mismatch", "application type mismatch"), ("deprecated", "deprecated"),
                   ("could not synthesize", "synthesize"), ("linarith failed", "linarith"),
                   ("don't know how to synthesize placeholder", "placeholder"), ("rfl failed", "rfl"), ("step failed", "step failed"),
                   ("anonymous-constructor notation", "invalid `⟨...⟩` notation"), ("function expected", "function expected")]:
        if pat in m:
            return k
    return "other: " + msg[:60]


def errors_of(text: str):
    errs = []
    for line in text.splitlines():
        m = re.match(r"error: (?:\S+?\.lean:\d+:\d+: )?(.*)", line)
        if m and not line.startswith("error: Lean exited") and "build failed" not in line \
                and not re.match(r"error: \S+: bad import", line):
            errs.append(m.group(1).strip())
    return [e for e in errs if e and not e.startswith("Lean exited") and not e.startswith("Some required targets")]


def main():
    arm = Path(sys.argv[1]).resolve()
    logs = Path(sys.argv[2]).resolve()
    out = Path(sys.argv[3]).resolve()
    p2 = arm.parent
    sf = scen_func(p2)
    rows = [l.rstrip("\n").split("\t") for l in (arm / "effort/attempts.tsv").read_text().splitlines() if l.strip()]
    loglist = []
    for f in sorted(logs.glob("*.log")):
        m = re.search(r"(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)", f.name)
        t = dt.datetime.strptime(m.group(1), "%Y-%m-%dT%H:%M:%S").replace(tzinfo=EST)
        loglist.append((t, f, f.read_text(errors="replace")))
    used = set()
    attempts = []
    for r in rows:
        t = dt.datetime.strptime(r[0], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
        targets, status, secs, nerr = r[1].split(), r[2], int(r[3]), int(r[4])
        note = r[5] if len(r) > 5 else ""
        mods = [x.split(".")[-1] for x in targets]
        fns = set()
        for x in targets:
            if x.startswith("Spec.Proofs.inventory."):
                fns.add(sf.get(x.split(".")[-1], "?"))
            elif x.startswith("Lemmas."):
                fns.add(FUNC_OF_MODULE.get(x.split(".")[-1], "?"))
        fn = sorted(fns)[0] if len(fns) == 1 else "+".join(sorted(fns))
        # matching full log: written at most a few seconds before the tsv line, mentions one of the targets
        own = {p.stem for p in (arm / "lean/Lemmas").glob("*.lean")} | ({"ProbeStep"} if "ProbeStep" in r[1] else set())

        def fits(txt):
            if any(mm in txt for mm in targets):
                return 0
            named = set(re.findall(r"Lemmas[./](\w+)", txt))
            return 1 if named and named <= own else None
        cand = [(fits(txt), abs((t - lt).total_seconds()), f, txt) for lt, f, txt in loglist
                if f not in used and -1 <= (t - lt).total_seconds() <= 4]
        cand = [(a, b, f, txt) for a, b, f, txt in cand if a is not None]
        cand.sort(key=lambda c: (c[0], c[1]))
        cand = [(b, f, txt) for a, b, f, txt in cand]
        errs, logname, nsorry = [], None, None
        if cand:
            _, f, txt = cand[0]
            used.add(f)
            logname = f.name
            errs = errors_of(txt)
            nsorry = len(re.findall(r"declaration uses .sorry.", txt))
        kinds = [kind(e) for e in errs]
        cls = None
        if status == "FAILED":
            labelled = bool(PROBE_NOTE.search(note))
            all_open = bool(kinds) and all(k == "unsolved goals" for k in kinds)
            cls = "probe" if labelled and all_open else ("mixed" if labelled else "real")
        attempts.append({"utc": r[0], "targets": targets, "function": fn, "status": status, "seconds": secs,
                         "error_lines": nerr, "note": note, "log": logname, "sorry_warnings": nsorry, "errors": errs[:12], "kinds": kinds,
                         "failed_class": cls, "post_hoc_probe": "ProbeStep" in r[1]})
    created = birth(arm / "effort/attempts.tsv")
    report = arm / "out/report.md"
    final_run = dt.datetime.fromtimestamp(report.stat().st_mtime, dt.timezone.utc) if report.exists() else None
    proof_att = [a for a in attempts if not a["post_hoc_probe"]]
    ts = lambda a: dt.datetime.strptime(a["utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    per_fn = {}
    prev_done = created
    for fn in ORDER:
        aa = [a for a in proof_att if fn in a["function"].split("+")]
        oks = [a for a in aa if a["status"] == "ok"]
        done = max(ts(a) for a in oks) if oks else None
        first = min(ts(a) for a in aa) if aa else None
        per_fn[fn] = {"attempts": len(aa), "failed": sum(a["status"] == "FAILED" for a in aa),
                      "failed_real": sum(a["failed_class"] == "real" for a in aa),
                      "failed_mixed": sum(a["failed_class"] == "mixed" for a in aa),
                      "failed_probe": sum(a["failed_class"] == "probe" for a in aa),
                      "active_min": round((done - first).total_seconds() / 60, 1) if done and first else None,
                      "increment_min": round((done - prev_done).total_seconds() / 60, 1) if done and prev_done else None,
                      "build_seconds": sum(a["seconds"] for a in aa)}
        if done:
            prev_done = done
    summary = {
        "arm": arm.name, "copy_created_utc": created.isoformat() if created else None,
        "first_attempt_utc": attempts[0]["utc"] if attempts else None,
        "last_attempt_utc": attempts[-1]["utc"] if attempts else None,
        "last_proof_attempt_utc": proof_att[-1]["utc"] if proof_att else None,
        "final_report_utc": final_run.isoformat() if final_run else None,
        "attempts_all": len(attempts), "failed_all": sum(a["status"] == "FAILED" for a in attempts),
        "attempts_proof": len(proof_att), "failed_proof": sum(a["status"] == "FAILED" for a in proof_att),
        "failed_real": sum(a["failed_class"] == "real" for a in proof_att),
        "failed_mixed": sum(a["failed_class"] == "mixed" for a in proof_att),
        "failed_probe": sum(a["failed_class"] == "probe" for a in proof_att),
        "post_hoc_probe_attempts": sum(a["post_hoc_probe"] for a in attempts),
        "logs_matched": sum(1 for a in attempts if a["log"]),
        "ok_builds_with_sorry": sum(1 for a in proof_att if a["status"] == "ok" and a["sorry_warnings"]),
        "build_seconds_proof": sum(a["seconds"] for a in proof_att),
    }
    if attempts and created:
        summary["minutes_copy_to_last_proof_attempt"] = round((ts(proof_att[-1]) - created).total_seconds() / 60, 1)
        summary["minutes_first_to_last_proof_attempt"] = round((ts(proof_att[-1]) - ts(proof_att[0])).total_seconds() / 60, 1)
    if final_run and created:
        summary["minutes_copy_to_final_report"] = round((final_run - created).total_seconds() / 60, 1)
    out.write_text(json.dumps({"summary": summary, "per_function": per_fn, "attempts": attempts}, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
