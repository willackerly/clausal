#!/usr/bin/env python3
"""cargo-mutants mutants of inventory/src/lib.rs, run through the P2 pipeline, scored per arm.

    python3 p2/score/mutants.py setup  [--workers N]      make worker copies under p2/score/work/mutw<k>-{D,F,O}
    python3 p2/score/mutants.py run    [--workers N] [--only i,j,...]
    python3 p2/score/mutants.py table                     summarise results/mutants/*.json -> results/mutants.tsv
    python3 p2/score/mutants.py errors --only i,j [--worker k]   keep the Lean errors of both arms' broken proofs

The mutants are exactly cargo-mutants 27.1.0's list for the crate (results/mutants-diff.json, made with
`cargo mutants --list --diff --json`); nobody chose them. Each worker has three cold-made scratch copies:
  D  base (sorry stubs, no proofs): `./run.sh --no-unit --no-adequacy` on the mutated crate. Arm-independent:
     does a scenario come out REFUTED / COUNTEREXAMPLE (shown false on the Lean model), does an Examples row fail
     on the compiled Rust (cucumber-rs)? The crate's own unit tests are left out (--no-unit), so this is what
     the SCENARIOS show on their own; cargo-mutants' own run with the unit tests is reported separately.
  F  arm-fable's Lemmas + proofs, O  arm-opus's: the mutated model (copied from D after translation), then
     `lake build` and the pipeline's own `slicegen proofs` bookkeeping: which proof modules still compile.
     No evaluation happens there, so a mutant that makes a loop run forever cannot hang it.
A lost proof is not a detection (plan rule 5): it is reported as "proof lost", never as "caught".
Timeouts kill only the process group this script started.
"""
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SCORE = Path(__file__).resolve().parent
P2 = SCORE.parent
WORK = SCORE / "work"
RES = SCORE / "results"
MUT = RES / "mutants"
ENV = dict(os.environ, PATH=f"{Path.home()}/.elan/bin:{Path.home()}/.cargo/bin:" + os.environ.get("PATH", ""))
SCEN = ["stock_is_sum", "stock_too_big", "find_first_bin", "find_no_bin", "restock_adds", "restock_counts",
        "take_amount", "take_stock_down", "take_earliest_first", "fill_count", "fill_state", "fill_at_most",
        "count_products", "count_at_most_bins", "dominant_found", "dominant_none"]
FN = {"stock_is_sum": "stock_of", "stock_too_big": "stock_of", "find_first_bin": "find_bin", "find_no_bin": "find_bin",
      "restock_adds": "restock", "restock_counts": "restock", "take_amount": "take", "take_stock_down": "take",
      "take_earliest_first": "take", "fill_count": "fill_orders", "fill_state": "fill_orders",
      "fill_at_most": "fill_orders", "count_products": "product_count", "count_at_most_bins": "product_count",
      "dominant_found": "dominant_product", "dominant_none": "dominant_product"}
ARMS = {"F": "arm-fable", "O": "arm-opus"}
T_TRANSLATE, T_BUILD, T_RUN, T_RUN_HANG = 600, 1200, 1500, 420


def sh(cmd, cwd, timeout, log=None):
    """Run in its own process group; on timeout kill that group only. Returns (rc or 'timeout', seconds, output)."""
    t0 = time.time()
    p = subprocess.Popen(cmd, cwd=cwd, env=ENV, shell=isinstance(cmd, str), stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True, start_new_session=True)
    try:
        out, _ = p.communicate(timeout=timeout)
        rc = p.returncode
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        out, _ = p.communicate()
        rc = "timeout"
    if log:
        Path(log).write_text(out or "")
    return rc, round(time.time() - t0, 1), out or ""


def copies(k):
    return {r: WORK / f"mutw{k}-{r}" for r in "DFO"}


def setup(workers):
    src = {"D": P2 / "base", "F": P2 / "arm-fable", "O": P2 / "arm-opus"}
    warm = {"D": P2 / "base/lean/.lake/build", "F": WORK / "fable/lean/.lake/build", "O": WORK / "opus/lean/.lake/build"}
    for k in range(1, workers + 1):
        for r, d in copies(k).items():
            if (d / "lib.rs.pristine").exists():      # already set up (and warm): keep it
                continue
            subprocess.run([str(SCORE / "mkcopy.sh"), str(src[r]), str(d)], check=True, env=ENV,
                           stdout=subprocess.DEVNULL)
            if warm[r].exists():      # build cache of identical sources: APFS clone, so the first build is warm
                subprocess.run(["cp", "-cRp", str(warm[r]), str(d / "lean/.lake/build")], check=True)
            shutil.copy(d / "inventory/src/lib.rs", d / "lib.rs.pristine")
            (d / "out").mkdir(exist_ok=True)
        print(f"worker {k}: {', '.join(str(p) for p in copies(k).values())}")


def proofs_of(copy: Path, logname: str, timeout=T_BUILD):
    rc, secs, out = sh("lake build", copy / "lean", timeout, log=copy / "out/proofs.log")
    if rc == "timeout":
        return {"rc": "timeout", "seconds": secs, "built": [], "failed": SCEN}
    sh(f"python3 -m slicegen proofs {rc}", copy, 120)
    pj = json.loads((copy / "out/proofs.json").read_text())
    built = [m.split(".")[-1] for m in pj["built"]]
    return {"rc": rc, "seconds": secs, "built": built, "failed": [m.split(".")[-1] for m in pj["failed"]],
            "failed_libs": pj.get("failed_libs", []),
            "errors": {k.split(".")[-1]: v for k, v in pj.get("errors", {}).items()}}


def detection(copy: Path, timeout):
    rc, secs, out = sh("./run.sh --no-unit --no-adequacy", copy, timeout, log=copy / "out-run.log")
    res = {"rc": rc, "seconds": secs, "scenarios": {}}
    g = copy / "out/graph.json"
    rep = copy / "out/report.md"
    if rc == "timeout" or not g.exists():
        log = (copy / "out-run.log").read_text()
        res["stopped_at"] = [l for l in log.splitlines() if l.startswith("== ")][-1:] if log else []
        res["tail"] = log[-1500:]
        return res
    gj = json.loads(g.read_text())
    text = rep.read_text() if rep.exists() else ""
    for v in gj["verdicts"]:
        sid = v["node"].split(".")[-1]
        if sid not in SCEN:
            continue
        res["scenarios"][sid] = {"code": v["code"], "flags": v.get("flags", [])}
    # rows on Rust / Lean model, per scenario, from the report text
    cur = None
    import re
    for line in text.splitlines():
        m = re.search(r"id `Spec\.inventory\.(\w+)`", line)
        if m and m.group(1) in SCEN:
            cur = m.group(1)
        m2 = re.search(r"tested\s+(\d+) of (\d+) rows pass on compiled Rust \(cucumber-rs\); (\d+) of (\d+) pass on the Lean model", line)
        if m2 and cur in res["scenarios"]:
            res["scenarios"][cur]["rust_rows"] = [int(m2.group(1)), int(m2.group(2))]
            res["scenarios"][cur]["model_rows"] = [int(m2.group(3)), int(m2.group(4))]
        m3 = re.search(r"the same input on the compiled Rust \(cucumber-rs\): (.*)$", line)
        if m3 and cur in res["scenarios"]:
            res["scenarios"][cur]["replay"] = m3.group(1)
    return res


def run_one(k, idx, mut, hang):
    c = copies(k)
    rec = {"index": idx, "name": mut["name"], "function": mut["function"]["function_name"] if mut.get("function") else None,
           "genre": mut["genre"], "replacement": mut["replacement"], "worker": k, "cargo_mutants_timeout": hang}
    t0 = time.time()
    for d in c.values():
        shutil.copy(d / "lib.rs.pristine", d / "inventory/src/lib.rs")
        p = subprocess.run(["patch", "--silent", "--no-backup-if-mismatch", "inventory/src/lib.rs"],
                           input=mut["diff"], text=True, cwd=d, capture_output=True)
        if p.returncode != 0:
            rec["error"] = "patch failed: " + p.stdout + p.stderr
            return rec
    D = c["D"]
    # D's own ./run.sh translates the mutated crate (step 2); as soon as its provenance.json is rewritten the model
    # is complete, and F and O start building their proofs against it while D carries on.
    prov = D / "lean/provenance.json"
    with ThreadPoolExecutor(3) as ex:
        fd = ex.submit(detection, D, T_RUN_HANG if hang else T_RUN)
        ready = False
        while not fd.done():
            if prov.exists() and prov.stat().st_mtime >= t0:
                ready = True
                break
            time.sleep(2)
        rec["translate"] = {"rc": 0 if ready else "failed (run.sh stopped before a model was written)",
                            "seconds": round(time.time() - t0, 1)}
        fp = {}
        if ready:
            time.sleep(1)
            for r in "FO":
                for rel in ["lean/Generated/Inventory.lean", "lean/translation.json", "lean/provenance.json"]:
                    shutil.copy(D / rel, c[r] / rel)
            fp = {r: ex.submit(proofs_of, c[r], r) for r in "FO"}
        rec["detect"] = fd.result()
        if not ready:
            rec["translate"]["tail"] = rec["detect"].get("tail", "")
        rec["proofs"] = {ARMS[r]: f.result() for r, f in fp.items()}
    rec["seconds"] = round(time.time() - t0, 1)
    for d in c.values():
        shutil.copy(d / "lib.rs.pristine", d / "inventory/src/lib.rs")
    return rec


def classify(rec):
    """Per arm: for each scenario: shown-false / proof-kept / proof-lost; per mutant overall."""
    det = rec.get("detect", {})
    sc = det.get("scenarios", {})
    shown = sorted(s for s, v in sc.items() if v["code"] in ("REFUTED", "COUNTEREXAMPLE")
                   or (v.get("rust_rows") and v["rust_rows"][0] < v["rust_rows"][1]))
    out = {"shown_false_by": shown, "detect_rc": det.get("rc"), "translate_rc": rec.get("translate", {}).get("rc")}
    for arm, p in rec.get("proofs", {}).items():
        out[arm] = {"proofs_lost": sorted(set(SCEN) - set(p["built"])), "proofs_kept": sorted(p["built"])}
    return out


def run(workers, only=None):
    muts = json.loads((RES / "mutants-diff.json").read_text())
    unit = json.loads((RES / "unit/mutants.out/outcomes.json").read_text())
    hang_names = {o["scenario"]["Mutant"]["name"] for o in unit["outcomes"]
                  if isinstance(o["scenario"], dict) and o["summary"] == "Timeout"}
    MUT.mkdir(parents=True, exist_ok=True)
    todo = [(i, m) for i, m in enumerate(muts) if (only is None or i in only)
            and not (MUT / f"{i:03d}.json").exists()]
    print(f"{len(todo)} mutants to run on {workers} workers", flush=True)
    queue = list(todo)
    import threading
    lock = threading.Lock()

    def worker(k):
        while True:
            with lock:
                if not queue:
                    return
                i, m = queue.pop(0)
            rec = run_one(k, i, m, m["name"] in hang_names)
            rec["class"] = classify(rec)
            (MUT / f"{i:03d}.json").write_text(json.dumps(rec, indent=1))
            cl = rec["class"]
            print(f"[{i:03d}] w{k} {rec['seconds']}s {m['name'][11:80]} | shown false by: {len(cl['shown_false_by'])} | "
                  + " | ".join(f"{a}: lost {len(cl[a]['proofs_lost'])}" for a in ARMS.values() if a in cl), flush=True)
    with ThreadPoolExecutor(workers) as ex:
        list(ex.map(worker, range(1, workers + 1)))


def table():
    rows = []
    for f in sorted(MUT.glob("*.json")):
        rec = json.loads(f.read_text())
        cl = rec["class"]
        rows.append([str(rec["index"]), rec["name"], str(cl.get("translate_rc")), str(cl.get("detect_rc")),
                     ",".join(cl["shown_false_by"]),
                     ",".join(cl.get("arm-fable", {}).get("proofs_lost", ["-"])),
                     ",".join(cl.get("arm-opus", {}).get("proofs_lost", ["-"]))])
    hdr = ["index", "mutant", "translate_rc", "detect_rc", "shown_false_by", "fable_proofs_lost", "opus_proofs_lost"]
    (RES / "mutants.tsv").write_text("\t".join(hdr) + "\n" + "\n".join("\t".join(r) for r in rows) + "\n")
    print(f"{len(rows)} rows -> {RES / 'mutants.tsv'}")


def errors_for(indices, k=1):
    """For the given mutants, rebuild both arms' proofs on worker k's copies and keep the Lean error lines
    (results/mutant-errors/<index>-<arm>.log), to see WHY a proof broke. Run after `run` has finished."""
    muts = json.loads((RES / "mutants-diff.json").read_text())
    outdir = RES / "mutant-errors"
    outdir.mkdir(exist_ok=True)
    c = copies(k)
    for i in indices:
        mut = muts[i]
        for d in c.values():
            shutil.copy(d / "lib.rs.pristine", d / "inventory/src/lib.rs")
            subprocess.run(["patch", "--silent", "--no-backup-if-mismatch", "inventory/src/lib.rs"],
                           input=mut["diff"], text=True, cwd=d, capture_output=True, check=True)
        rc, secs, out = sh("./translate.sh", c["D"], T_TRANSLATE)
        for r in "FO":
            for rel in ["lean/Generated/Inventory.lean", "lean/translation.json", "lean/provenance.json"]:
                shutil.copy(c["D"] / rel, c[r] / rel)
            rc, secs, out = sh("lake build", c[r] / "lean", T_BUILD)
            keep = [l for l in out.splitlines() if l.startswith(("error:", "✖"))]
            (outdir / f"{i:03d}-{ARMS[r]}.log").write_text(mut["name"] + "\n" + "\n".join(keep) + "\n")
            print(f"[{i:03d}] {ARMS[r]}: {len(keep)} error lines", flush=True)
        for d in c.values():
            shutil.copy(d / "lib.rs.pristine", d / "inventory/src/lib.rs")


if __name__ == "__main__":
    args = sys.argv[1:]
    w = int(args[args.index("--workers") + 1]) if "--workers" in args else 3
    only = {int(x) for x in args[args.index("--only") + 1].split(",")} if "--only" in args else None
    {"setup": lambda: setup(w), "run": lambda: run(w, only), "table": table,
     "errors": lambda: errors_for(sorted(only or []), int(args[args.index("--worker") + 1]) if "--worker" in args else 1)
     }[args[0]]()
