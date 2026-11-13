"""clausal evidence: run the GENERATED property tests and bounded checks, and feed what they find back (plan node E1).

    python3 -m clausal evidence [--quick] [--cases 10000] [--seed 20261111] [--jobs 6] [--kani-timeout 30] [--only id,id]

  1. property test   evidence/ (proptest, generated from build/trees.json by clausal/evgen.py): every compiled reading on
                     `--cases` generated inputs IN ITS SCOPE, edge-weighted, with shrinking, on the compiled Rust. A test
                     that does not finish in its time names the input it was evaluating; that input is evaluated again
                     alone, and is reported against the compiled Rust unless the call answers there with the reading
                     holding or not applying (then the test ran out of time, not the call: `property_witness`).
  2. bounded check   evidence/kani/ (Kani, generated from the same trees): every reading at every rung of the size ladder
                     (evgen.LADDER), every integer symbolic. Skipped by --quick. A harness that fails is run again for its
                     concrete input, and that input is replayed on the compiled Rust through the generated predicate.
  3. out/evidence.json   per reading: the property test (cases, seed, result, shrunk input), the bounded check (per rung:
                     verified / failed / no answer in time), and the falsifying inputs found, each with its source.

FEED-BACK (the rest of this module, called from `clausal witness` and `clausal derive`): every falsifying input is
evaluated on the LEAN MODEL through the reading itself (lean/Run/Witness.lean, generated). If the reading is false there
too, the input becomes the counterexample of the reading (when the grid search found none) and the usual scripts turn it
into a kernel-checked refutation. If the model does NOT fail where the compiled Rust did, that is a MODEL MISMATCH: a
finding about the translation link, reported as such.
"""
from __future__ import annotations

import json
import re
import subprocess
import time
from pathlib import Path

from . import evgen, projects

ROOT = Path(__file__).resolve().parent.parent
EV = ROOT / "evidence"
OUT = ROOT / "out"
SEED, CASES = 20261111, 10000
SIZE = 6      # the runner's --size: a freely drawn collection has at most this many items. The second call of a two-call rule
              # can be longer (the first call's collection plus a few items); the runner records the limit per reading
              # (`limit` in its row), and clausal/sizes.py reports that, not this number.


def sh(cmd: str, cwd: Path, timeout: float):
    """(exit status or None on timeout, output, seconds). The command runs in its own process group, killed on timeout."""
    import os
    import signal
    t0 = time.time()
    p = subprocess.Popen(cmd, cwd=str(cwd), shell=True, executable="/bin/bash", stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, start_new_session=True)
    try:
        out, _ = p.communicate(timeout=timeout)
        return p.returncode, out, round(time.time() - t0, 2)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        try:
            out, _ = p.communicate(timeout=20)
        except Exception:      # noqa: BLE001
            out = ""
        return None, out or "", round(time.time() - t0, 2)


# ---------------------------------------------------------------------------------------------- property tests

def build_runner(ev: Path = EV):
    rc, out, secs = sh("cargo build --offline --quiet 2>&1 || cargo build --quiet 2>&1", ev, 900)
    return rc == 0, out[-2000:], secs


def run_proptest(ev: Path = EV, cases: int = CASES, seed: int = SEED, timeout: int = 60, only=None, trees: Path | None = None, ids=None) -> tuple:
    """({reading id: row}, seconds). The runner stops at a rule that does not finish (the hung thread cannot be stopped);
    the rules after it are then run in a fresh process, which is why `ids` (all reading ids, in order) is needed."""
    base = f"--cases {cases} --seed {seed} --size {SIZE} --timeout-secs {timeout}" + (f" --trees '{trees}'" if trees else "")
    rows, total = {}, 0.0
    todo = list(only) if only else (list(ids) if ids else None)
    while True:
        args = base + (" --only '" + ",".join(todo) + "'" if todo is not None else "")
        n = len(todo) if todo is not None else 100
        rc, out, secs = sh(f"./target/debug/rule-evidence {args}", ev, (timeout + 5) * n + 300)
        total += secs
        got = [json.loads(l) for l in out.splitlines() if l.startswith("{")]
        for r in got:
            rows[r["rule"]] = r
        if todo is None or not got or got[-1]["status"] != "hang":
            break
        todo = [i for i in todo if i not in rows]
        if not todo:
            break
    return rows, round(total, 2)


def replay(requests: list, ev: Path = EV, timeout: int = 20, trees: Path | None = None) -> list:
    """Evaluate readings at given inputs on the compiled Rust: [{rule, status, bits, values, tag}]."""
    if not requests:
        return []
    f = ev / "target" / "replay.jsonl"
    f.write_text("\n".join(json.dumps(r) for r in requests) + "\n")
    rc, out, _ = sh(f"./target/debug/rule-evidence --replay '{f}' --timeout-secs {timeout}" + (f" --trees '{trees}'" if trees else ""), ev,
                    timeout * len(requests) + 120)
    return [json.loads(l) for l in out.splitlines() if l.startswith("{")]


# ---------------------------------------------------------------------------------------------- Kani

def parse_kani(out: str) -> dict:
    """{harness: {status, verification_secs, failed_checks}} from `cargo kani --output-format terse` (with or without -j)."""
    res, cur, block, who = {}, {}, {}, None
    for line in out.splitlines():
        m = re.match(r"^(?:Thread (\d+): )?Checking harness (\S+?)\.\.\.$", line)
        if m:
            t = m.group(1) or "0"
            cur[t] = m.group(2).split("::")[-1]
            who = t if m.group(1) is None else None
            if m.group(1) is None:
                block[cur[t]] = []
            continue
        m = re.match(r"^Thread (\d+): ?$", line)
        if m:
            who = m.group(1)
            block[cur.get(who, "?")] = []
            continue
        if line.startswith("Thread ") or line.startswith("Manual Harness Summary") or line.startswith("Complete - "):
            who = None
            continue
        if who is not None and cur.get(who) in block:
            block[cur[who]].append(line)
    for name, lines in block.items():
        text = "\n".join(lines)
        failed = sorted(set(re.findall(r"^Failed Checks: (.*)$", text, re.M)))
        vt = re.search(r"Verification Time: ([0-9.]+)s", text)
        if "CBMC timed out" in text:
            status = "timeout"
        elif "VERIFICATION:- SUCCESSFUL" in text:
            status = "verified"
        elif "VERIFICATION:- FAILED" in text and failed:
            status = "failed"
        else:
            status = "error"
        res[name] = {"status": status, "verification_secs": float(vt.group(1)) if vt else None,
                     "failed_checks": [f.strip().strip('"') for f in failed], "tail": "" if status in ("verified", "failed", "timeout") else text[-400:]}
    return res


def run_kani(names: list, jobs: int, timeout: int, kd: Path | None = None) -> tuple:
    """({harness: result}, seconds) for the named harnesses, `jobs` at a time, each with `timeout` seconds."""
    kd = kd or EV / "kani"
    if not names:
        return {}, 0.0
    res, total = {}, 0.0
    for k in range(0, len(names), 120):         # keep the command line short
        chunk = names[k:k + 120]
        sel = " ".join(f"--harness harnesses::{n}" for n in chunk)
        rc, out, secs = sh(f"cargo kani {sel} --exact -j {max(jobs, 2)} --output-format terse -Z unstable-options --harness-timeout {timeout}s 2>&1",
                           kd, (timeout + 30) * (len(chunk) / max(jobs, 1) + 2) + 900)
        total += secs
        got = parse_kani(out)
        for n in chunk:
            res[n] = got.get(n) or {"status": "error", "verification_secs": None, "failed_checks": [], "tail": out[-600:]}
    return res, round(total, 1)


def kani_playback(names: list, meta: dict, timeout: int, kd: Path | None = None) -> dict:
    """{harness: {variable: literal} | None}: the concrete input of each failing harness (Kani's concrete playback)."""
    kd = kd or EV / "kani"
    out = {}
    for n in names:
        rc, text, _ = sh(f"cargo kani --harness harnesses::{n} --exact -Z concrete-playback --concrete-playback=print --output-format terse "
                         f"-Z unstable-options --harness-timeout {timeout}s 2>&1", kd, timeout + 300)
        out[n] = evgen.decode_playback(text, meta[n]["layout"]) if "concrete_vals" in text else None
    return out


# ---------------------------------------------------------------------------------------------- the whole step

def collect(quick: bool, cases: int = CASES, seed: int = SEED, jobs: int = 6, kani_timeout: int = 30, only=None, root: Path = ROOT,
            rungs=None, stop_at_failure: bool = False, prop_timeout: int = 20, kani_only=None) -> dict:
    """Run both generated harness sets on the compiled Rust of `root`; returns (and does not write) the evidence."""
    ev = root / "evidence"
    gen = json.loads((root / "build" / "evidence_gen.json").read_text())
    ids = [i for i in gen["readings"] if only is None or i in only]
    res = {"seed": seed, "cases_wanted": cases, "ladder": gen["ladder"], "quick": quick, "skipped": gen["skipped"], "readings": {},
           "cost": {}, "kani_timeout": kani_timeout, "jobs": jobs, "size": SIZE,
           "tools": {"proptest": "1.12.0", "kani": None if quick else " / ".join(sh("cargo kani --version", root, 60)[1].split("\n")[:2]).strip(" /")}}
    ok, tail, bsecs = build_runner(ev)
    res["cost"]["property_build_secs"] = bsecs
    if not ok:
        res["error"] = "the generated property tests do not build: " + tail
        return res
    rows, secs = run_proptest(ev, cases, seed, timeout=prop_timeout, only=only, trees=root / "build" / "trees.json", ids=ids)
    res["cost"]["property_secs"] = secs
    # A property test that did not finish names the input it was evaluating when its time ran out. That input is evaluated
    # again, alone, on the compiled Rust (as the input of a failing bounded check is, below): only if the call gives no
    # answer there either is it an input at which the compiled Rust gives no answer.
    hung = [i for i in ids if (rows.get(i) or {}).get("status") == "hang" and rows[i].get("witness")]
    alone = {r.get("tag"): r.get("status") for r in replay([{"rule": i, "values": rows[i]["witness"], "tag": i} for i in hung], ev,
                                                           timeout=prop_timeout, trees=root / "build" / "trees.json")}
    for i in hung:
        rows[i]["alone"] = alone.get(i, "not replayed")
    for i in ids:
        res["readings"][i] = {"property": rows.get(i) or {"status": "not run"}, "bounded": {"ran": False, "rungs": []}, "witnesses": []}
        w = property_witness(rows.get(i) or {})
        if w:
            res["readings"][i]["witnesses"].append(w)
    if quick:
        return res
    meta = gen["harnesses"]
    by_id = {}
    for name, m in meta.items():
        if m["id"] in ids and (rungs is None or m["rung"] in rungs) and (kani_only is None or m["id"] in kani_only):
            by_id.setdefault(m["id"], []).append(name)
    t0 = time.time()
    results = {}
    if stop_at_failure:
        # in two stages: the first rung of every reading; then the other rungs of the readings the first did not show
        # false (used on mutants, to save time: most falsified rules fail at the first rung)
        nr = max((len(v) for v in by_id.values()), default=0)
        for stage in ([0], list(range(1, nr))):
            todo = [v[r] for i, v in by_id.items() for r in stage if r < len(v) and not any(results.get(n, {}).get("status") == "failed" for n in v)]
            got, _ = run_kani(todo, jobs, kani_timeout, ev / "kani")
            results.update(got)
    else:
        results, _ = run_kani([n for v in by_id.values() for n in v], jobs, kani_timeout, ev / "kani")
    res["cost"]["bounded_secs"] = round(time.time() - t0, 1)
    failing = {}
    for i, names in by_id.items():
        b = res["readings"][i]["bounded"]
        b["ran"] = True
        for n in names:
            m, r = meta[n], results.get(n)
            b["rungs"].append({"harness": n, "label": m["label"], "accounts": m["accounts"], "transfers": m["transfers"],
                               "status": r["status"] if r else "not run", "secs": r.get("verification_secs") if r else None,
                               "failed_checks": r.get("failed_checks", []) if r else []})
            if r and r["status"] == "failed" and i not in failing:
                failing[i] = n
    t0 = time.time()
    plays = kani_playback(list(failing.values()), meta, max(kani_timeout, 60), ev / "kani")
    reqs = [{"rule": i, "values": plays[n], "tag": n} for i, n in failing.items() if plays.get(n)]
    back = {r.get("tag"): r for r in replay(reqs, ev, trees=root / "build" / "trees.json")}
    res["cost"]["bounded_witness_secs"] = round(time.time() - t0, 1)
    for i, n in failing.items():
        b = res["readings"][i]["bounded"]
        rp = back.get(n)
        b["witness_harness"], b["witness_rung"] = n, meta[n]["label"]
        if not plays.get(n):
            b["witness"] = None
            b["replay"] = "Kani gave no concrete input"
            continue
        b["witness"] = (rp or {}).get("values") or plays[n]
        b["replay"] = (rp or {}).get("status", "not replayed")
        res["readings"][i]["witnesses"].append({"source": "bounded check", "values": b["witness"],
                                                "rust": {"fails": "fails", "hang": "gives no answer in time"}.get(b["replay"], f"NOT reproduced ({b['replay']})"),
                                                "note": f"Kani at {meta[n]['label']}; replayed on the compiled Rust through the generated predicate"})
    return res


def property_witness(r: dict) -> dict | None:
    """The falsifying input a property-test row gives, or None. A test that FAILED gives its shrunk input. A test that DID
    NOT FINISH gives the input it was evaluating only when that input, evaluated alone on the compiled Rust (`alone`, the
    status of the replay), does not come back with an answer under which the reading holds or does not apply. When it does,
    it was the test that ran out of time (a slow search for inputs in scope, a loaded machine),
    not the call: the row keeps its status "hang" and says so, and no input is reported against the compiled Rust."""
    if not r.get("witness"):
        return None
    if r.get("status") == "fail":
        return {"source": "property test", "values": r["witness"], "rust": "fails", "note": f"case {r.get('calls_to_first_failure')} of the run, shrunk"}
    if r.get("status") != "hang":
        return None
    alone = r.get("alone", "not replayed")
    if alone in ("holds", "out-of-scope"):
        return None
    # anything else (the replay hangs too, errors, or was not made) leaves the finding as it was before the replay existed
    return {"source": "property test", "values": r["witness"], "rust": "fails" if alone == "fails" else "gives no answer in time",
            "note": "the input being evaluated when the test stopped; evaluated again alone: "
                    + {"hang": "no answer in time", "fails": "the reading is false there"}.get(alone, alone)}


def overview(ev: dict | None) -> list:
    """Markdown lines for the report: what the generated harnesses did in this run, as a whole."""
    if not ev or not ev.get("readings"):
        return ["The generated property tests and bounded checks did not run in this run (`./run.sh --no-rust`, or the step failed"
                + (f": {ev['error'][:300]}" if ev and ev.get("error") else "") + ").", ""]
    rd = ev["readings"]
    st = [r["property"].get("status") for r in rd.values()]
    ws = [w for _, _, w in witness_list(ev)]
    o = ["| | |", "|---|---|",
         f"| Readings with a generated property test and Kani harness | {len(rd)} (every compiled scenario and Rule line"
         + (f"; {len(ev['skipped'])} have no typed reading: {', '.join(ev['skipped'])}" if ev.get("skipped") else "") + ") |",
         f"| Property test | proptest {ev['tools'].get('proptest')}, seed {ev['seed']}, {ev['cases_wanted']} cases IN SCOPE per reading, collections up to "
         f"{ev.get('size', 6)} items{longer_note(ev)}, shrinking: {st.count('pass')} not falsified, {st.count('fail')} shown false, {st.count('hang')} did not finish, "
         f"{st.count('abort')} had no input in scope, {st.count('mismatch')} READING MISMATCH |",
         f"| Generated predicate against the tree evaluator | compared at every generated case ({sum(r['property'].get('calls') or 0 for r in rd.values())} cases): "
         f"{st.count('mismatch')} readings differ |",
         f"| Cost of the property tests | {ev['cost'].get('property_secs')} s for all readings (build {ev['cost'].get('property_build_secs')} s) |"]
    if ev["quick"]:
        o.append("| Bounded check | SKIPPED (`./run.sh --quick`) |")
    else:
        rungs = [g for r in rd.values() for g in r["bounded"]["rungs"]]
        c = {s: sum(g["status"] == s for g in rungs) for s in ("verified", "failed", "timeout", "error")}
        full = sum(1 for r in rd.values() if r["bounded"]["rungs"] and all(g["status"] == "verified" for g in r["bounded"]["rungs"]))
        some = sum(1 for r in rd.values() if any(g["status"] == "verified" for g in r["bounded"]["rungs"]) and not all(g["status"] == "verified" for g in r["bounded"]["rungs"])
                   and not any(g["status"] == "failed" for g in r["bounded"]["rungs"]))
        fl = sum(1 for r in rd.values() if any(g["status"] == "failed" for g in r["bounded"]["rungs"]))
        none = len(rd) - full - some - fl
        o += [f"| Bounded check | {ev['tools'].get('kani')}; size ladder (accounts, transfers) = {', '.join(f'({a}, {b})' for a, b in ev['ladder'])}, the same for every "
              f"rule; {ev['kani_timeout']} s per harness, {ev['jobs']} at a time: {len(rungs)} harnesses, {c['verified']} verified, {c['failed']} failed, "
              f"{c['timeout']} no answer in time, {c['error']} error |",
              f"| Bounded check, per reading | {full} hold at every rung; {some} hold at some rungs and give no answer at others; {fl} shown false; {none} no answer at any rung |",
              f"| Cost of the bounded checks | {ev['cost'].get('bounded_secs')} s wall-clock; {round(sum(g['secs'] or 0 for g in rungs))} s of solver time in the harnesses that answered; "
              f"{ev['cost'].get('bounded_witness_secs')} s more to get and replay the failing inputs |"]
    o += [f"| Falsifying inputs found (property test + bounded check) | {len(ws)}: {sum(w.get('model') == 'fails' for w in ws)} fail on the Lean model too, "
          f"{sum(bool(w.get('mismatch')) for w in ws)} MODEL MISMATCH, {sum(w.get('model') == 'not evaluated' for w in ws)} not evaluated on the model |", ""]
    return o


def cmd_evidence(argv) -> int:
    def opt(name, default):
        return type(default)(argv[argv.index(name) + 1]) if name in argv else default
    quick = "--quick" in argv
    only = argv[argv.index("--only") + 1].split(",") if "--only" in argv else None
    res = collect(quick, opt("--cases", CASES), opt("--seed", SEED), opt("--jobs", 6), opt("--kani-timeout", 30), only)
    OUT.mkdir(exist_ok=True)
    (OUT / "evidence.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    if res.get("error"):
        print("  " + res["error"])
        return 1
    print("  " + summary_line(res))
    return 0


def summary_line(res: dict) -> str:
    rd = res["readings"]
    st = [r["property"].get("status") for r in rd.values()]
    line = (f"property tests (generated, proptest, seed {res['seed']}): {len(rd)} readings, {res['cases_wanted']} cases in scope each; "
            f"{st.count('pass')} found nothing, {st.count('fail')} shown false, {st.count('hang')} did not finish, "
            f"{st.count('abort')} had no input in scope, {st.count('mismatch')} READING MISMATCH; {res['cost'].get('property_secs')} s")
    if res["quick"]:
        return line + "; bounded check SKIPPED (--quick)"
    rungs = [g for r in rd.values() for g in r["bounded"]["rungs"]]
    c = {s: sum(g["status"] == s for g in rungs) for s in ("verified", "failed", "timeout", "error")}
    return line + (f"\n  bounded check (generated, Kani, ladder {res['ladder']} as accounts x transfers, {res['kani_timeout']} s per harness): "
                   f"{len(rungs)} harnesses; {c['verified']} verified, {c['failed']} failed, {c['timeout']} no answer in time, {c['error']} error; "
                   f"{res['cost'].get('bounded_secs')} s")


# ---------------------------------------------------------------------------------------------- feed-back on the Lean model

def load(out: Path = OUT) -> dict | None:
    p = out / "evidence.json"
    return json.loads(p.read_text()) if p.exists() else None


def witness_list(ev: dict | None) -> list:
    """[(reading id, k, witness)]: every falsifying input found, in a fixed order."""
    out = []
    for i, r in ((ev or {}).get("readings") or {}).items():
        for k, w in enumerate(r["witnesses"]):
            out.append((i, k, w))
    return out


def terms_at(voc, side_entry: dict, values: dict) -> dict:
    """Lean terms of the state and the input of a reading at given values (the counterpart of rsearch.point_terms)."""
    from .rsearch import lit
    types = side_entry["rust"]["types"]
    out = {k: side_entry.get(k) for k in ("st", "inp", "st2", "inp2")}
    terms = {n: lit(voc, types[n], values[n]) for n, _ in side_entry["vars"] if n in values}
    for n, t in terms.items():
        for k in out:
            if out[k] is not None:
                out[k] = re.sub(rf"\b{re.escape(n)}\b(?!')", lambda _m, t=t: t, out[k])
    out["outer"] = terms
    return out


def witness_file(st, ev: dict | None, side: dict) -> tuple:
    """(lean/Run/Witness.lean, sidecar): every falsifying input the generated harnesses found, evaluated on the Lean model
    through the reading itself; for a scenario with a flat statement also as an extra Examples row of that statement."""
    from . import emit
    from .rsearch import HEADER
    by_id = {rd.id: (rd, b) for rd, b in st.compiled}
    out = [HEADER + "-- Run once per pipeline run with `lake env lean Run/Witness.lean` (interpreter).\n"
           "-- Every falsifying input found by the generated property tests and bounded checks (out/evidence.json), on the MODEL.\n"
           "import Wallet.Readings\nimport Wallet.Checks\n" + "".join(f"import {m}\n" for m in projects.load().search_imports())
           + "open Aeneas Aeneas.Std Result\n"
           "set_option linter.unusedVariables false\n\n"
           "def wbits (l : List Bool) : String := String.ofList (l.map fun b => if b then '1' else '0')\n"]
    meta = []
    for i, k, w in witness_list(ev):
        if i not in by_id or i not in side or "skipped" in side[i]:
            continue
        rd, b = by_id[i]
        s = side[i]
        if any(n not in w["values"] for n, _ in s["vars"]):
            continue
        # the model leaves the width of usize open (at least 32 bits), so an account number above 2^32 - 1 has no literal there
        big = [n for n, _ in s["vars"] if s["rust"]["types"].get(n) in ("index", "transfer", "batch")
               and any(int(x) > 4294967295 for x in re.findall(r"\d+(?=->)|(?<=->)\d+(?=:)|^\d+$", w["values"][n]))]
        if big:
            w["model_note"] = ("an account number above 4294967295 has no literal in the Lean model, which leaves the width of usize open: "
                               + ", ".join(big))
            continue
        p = terms_at(st.voc, s, w["values"])
        two = bool(s.get("st2"))
        lets = "".join(f"  let {name} : {typ} := {p['outer'][name]}\n" for name, typ in rd.outer if name in p["outer"])
        lets += f"  let st : {rd.state_type} := {p['st']}\n  let inp : {rd.input_type} := {p['inp']}\n"
        if two:
            lets += f"  let st2 : {rd.state_type} := {p['st2']}\n  let inp2 : {rd.input_type} := {p['inp2']}\n"

        def pt(c):
            return "st inp st2 inp2" if c.runs == 2 else "st inp"
        from .rsearch import rel_of
        scopes = ", ".join((f"decide (({c.op}).scope st inp ∧ ({c.op}).scope st2 inp2 ∧ {rel_of(st.voc, c)} st inp st2 inp2)" if c.runs == 2
                            else f"decide (({c.op}).scope st inp)") for c in rd.claims)
        ats = ", ".join(f"decide ({c.at} {pt(c)})" for c in rd.claims)
        n = len(meta)
        chunk = f"#eval show IO Unit from do\n  -- {i}: {w['source']}\n" + lets + f"  IO.println s!\"WITNESS\\t{n}\\t{{wbits [{scopes}]}}\\t{{wbits [{ats}]}}\"\n"
        row = False
        if b is not None and not b.hidden and all(h in w["values"] for h in b.sc.header):
            args = emit.concrete_args(b, {h: w["values"][h] for h in b.sc.header})
            chunk += (f"#eval show IO Unit from do\n  IO.println \"WITROW\\t{n}\"\n"
                      f"  IO.println (Bdd.rowLine \"{b.id}\" 0 ({b.id}.check {args}) ({b.id}.givens {args}) ({b.id}.thens {args}) ({b.id}.returned {args}))\n")
            row = True
        out.append(chunk)
        meta.append({"n": n, "id": i, "k": k, "row": row, "flat": b.id if b is not None else None, "terms": p})
    return "\n".join(out), meta


def parse_witness(log: str, meta: list, ev: dict) -> dict:
    """Fill each witness of `ev` with what the model said: `model` = "fails" | "holds" | "out of scope" | "not evaluated",
    its claim bits, the Lean terms of the point, and for a scenario with a flat statement the row line of that statement."""
    lines = log.splitlines()
    got, rows = {}, {}
    for k, line in enumerate(lines):
        p = line.split("\t")
        if p[0] == "WITNESS" and len(p) >= 4:
            got[int(p[1])] = (p[2], p[3])
        elif p[0] == "WITROW" and k + 1 < len(lines) and lines[k + 1].startswith("ROW\t"):
            q = lines[k + 1].split("\t")
            rows[int(p[1])] = {"check": q[3], "givens": q[4], "thens": q[5], "returned": q[6] if len(q) > 6 else ""}
    for m in meta:
        w = ev["readings"][m["id"]]["witnesses"][m["k"]]
        w["terms"] = m["terms"]
        if m["n"] not in got:
            w["model"] = "not evaluated"
            w.setdefault("model_note", "the Lean script for this input gave no result (out/witness.log)")
            continue
        scope, ats = got[m["n"]]
        w["model_bits"] = ats
        about = [a for s, a in zip(scope, ats) if s == "1"]
        w["model"] = "out of scope" if not about else "fails" if "0" in about else "holds"
        if m["n"] in rows:
            w["flat_row"] = rows[m["n"]]
    for r in ev["readings"].values():
        for w in r["witnesses"]:
            w.setdefault("model", "not evaluated")
            # the compiled Rust fails (or gives no answer) and the model does not: the translation link is in question
            w["mismatch"] = w["rust"] in ("fails", "gives no answer in time") and w["model"] in ("holds", "out of scope")
    return ev


def feed_back(ev: dict | None, rs: dict) -> list:
    """Make each falsifying input that also fails on the model the counterexample of its reading where the grid search
    found none (the reading search result `rs`: Rule lines, NEW sentences, and the reading of every scenario). Returns what
    was fed back, for the log."""
    done = []
    for i, k, w in witness_list(ev):
        if w.get("model") != "fails":
            continue
        r = rs.get(i)
        if r is not None and "skipped" not in r and not r.get("bad"):
            r["bad"] = {"values": w["values"], "bits": w["model_bits"], "index": None, "terms": w["terms"], "source": w["source"]}
            done.append((i, w["source"]))
    return done


def feed_back_flat(ev: dict | None, search: dict, st) -> list:
    """The same for a scenario with a FLAT statement of the old glossary: the input, evaluated as one more row of that
    statement, becomes the counterexample of the old search where its grid found none. Called from `parse_search`, so that
    `derive` (which writes the refutation) and `report` see the same thing."""
    done = []
    flat = {rd.id: b for rd, b in st.compiled if b is not None}
    for i, k, w in witness_list(ev):
        b = flat.get(i)
        fr = w.get("flat_row")
        if w.get("model") != "fails" or b is None or not fr or b.id not in search or search[b.id]["bad"]:
            continue
        if fr["check"] in ("pass", "givenFalse"):
            continue
        search[b.id]["bad"] = {"values": {h: w["values"][h] for h in b.sc.header}, "check": fr["check"], "thens": fr["thens"],
                               "returned": fr["returned"], "source": w["source"]}
        done.append((i, w["source"]))
    return done


# ---------------------------------------------------------------------------------------------- the evidence ladder of one reading

def longer_note(ev: dict) -> str:
    """What the runner recorded beyond --size: the second call of a two-call rule can have a longer collection."""
    size, top = ev.get("size", 6), {}
    for r in ev.get("readings", {}).values():
        for w, n in ((r.get("property") or {}).get("limit") or {}).items():
            if n is not None and n > size:
                top[w] = max(top.get(w, 0), n)
    return (" (up to " + " and ".join(f"{n} {w}" for w, n in top.items()) + " in the second call of a two-call rule)") if top else ""


def ladder(ev: dict | None, rid: str) -> dict | None:
    """What the generated harnesses say about one reading, in the words of the report."""
    r = ((ev or {}).get("readings") or {}).get(rid)
    if r is None:
        return None
    p = r["property"]
    out = {"seed": ev["seed"], "property": None, "bounded": None, "witnesses": [], "tools": ev.get("tools", {}), "size": ev.get("size", 6),
           "kani_timeout": ev.get("kani_timeout"), "quick": ev.get("quick"),
           "limit": {w: n for w, n in (p.get("limit") or {}).items() if n is not None}}
    st = p.get("status")
    if st == "pass":
        text = f"{p['cases']} generated inputs in scope ({p['calls']} generated), none falsifies it"
    elif st == "fail":
        text = f"FALSE at an input found at generated input {p['calls_to_first_failure']} and shrunk: {json.dumps(p['witness'], ensure_ascii=False)}"
    elif st == "hang":
        text = f"NO ANSWER in time (the test did not finish); it was evaluating {json.dumps(p.get('witness'), ensure_ascii=False)}"
        if p.get("alone") in ("holds", "out-of-scope"):
            text += (f"; evaluated again alone, the call answers there and the reading {'holds' if p['alone'] == 'holds' else 'does not apply (out of scope)'}: "
                     "the test ran out of time, not the call")
    elif st == "abort":
        text = f"no result: {p['cases']} inputs in scope among {p['calls']} generated (the scope is hardly ever or never met)"
    elif st == "mismatch":
        text = f"READING MISMATCH (generated predicate against the tree evaluator): {p.get('message', '')}"
    else:
        text = "not run"
    out["property"] = {"status": st, "text": text, "cases": p.get("cases"), "calls": p.get("calls"), "ms": p.get("elapsed_ms")}
    b = r["bounded"]
    if b["ran"]:
        ver = [g["label"] for g in b["rungs"] if g["status"] == "verified"]
        fail = [g for g in b["rungs"] if g["status"] == "failed"]
        tmo = [g["label"] for g in b["rungs"] if g["status"] == "timeout"]
        err = [g["label"] for g in b["rungs"] if g["status"] not in ("verified", "failed", "timeout")]
        bits = []
        unreproduced = bool(fail) and b.get("replay") in ("holds", "out-of-scope", "mismatch")
        if unreproduced:
            g = fail[0]
            bits.append(f"Kani reports a failure with {g['label']}, but its input {json.dumps(b.get('witness'), ensure_ascii=False)} does NOT fail on the "
                        f"compiled Rust ({b.get('replay')}): NOT REPRODUCED, not counted as a counterexample")
            fail = []
        if fail:
            g = fail[0]
            why = "the rule's assertion" if "RULE" in g["failed_checks"] else "the call gives no answer (" + "; ".join(g["failed_checks"]) + ")"
            bits.append(f"FALSE with {g['label']} ({why}"
                        + (f"; input {json.dumps(b.get('witness'), ensure_ascii=False)}; on the compiled Rust it {b.get('replay')}" if b.get("witness") else "") + ")")
        if ver == ["no size bound"]:
            bits.append("holds for every input (no size bound: the rule speaks of no collection)")
        elif ver:
            bits.append("holds for every input with " + "; with ".join(ver))
        if tmo:
            bits.append(f"NO ANSWER in {ev['kani_timeout']} s with " + "; with ".join(tmo))
        if err:
            bits.append("error with " + "; with ".join(err))
        out["bounded"] = {"status": "unreproduced" if unreproduced else "failed" if fail else "verified" if ver and not tmo and not err else "partial" if ver else "none",
                          "text": "; ".join(bits), "verified": ver, "timeout": tmo,
                          "secs": round(sum(g["secs"] or 0 for g in b["rungs"]), 1)}
    for w in r["witnesses"]:
        out["witnesses"].append({k: w.get(k) for k in ("source", "values", "rust", "model", "mismatch", "note", "model_note")})
    return out
