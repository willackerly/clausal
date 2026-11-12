#!/usr/bin/env python3
"""V4, proxy version: rules written by model authors who never saw the vocabulary, put through `clausal compile`.

    python3 run_v4.py            everything, in the scratch copy work/clausal (made by clausal/mutation/workcopy.sh); writes results.json
    python3 run_v4.py --kani     also the generated bounded checks (Kani) for the compiled readings
    python3 run_v4.py --print    print the report tables from results.json (nothing is run)

Reads clausal/ through the scratch copy only; changes nothing in clausal/. One Lean invocation (the reading search), one
cargo build, one property-test run, one replay of the authors' cases.
"""
from __future__ import annotations

import json
import os
import re
import statistics
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE / "work" / "clausal"
sys.path.insert(0, str(HERE))
ENV = dict(os.environ, PATH=f"{Path.home()}/.elan/bin:{Path.home()}/.cargo/bin:" + os.environ["PATH"])
M = 18446744073709551615


def sh(cmd, cwd=WORK, timeout=1800):
    t0 = time.time()
    p = subprocess.run(cmd, shell=True, cwd=cwd, env=ENV, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout + p.stderr, round(time.time() - t0, 1)


def words(s):
    return re.findall(r"[a-z0-9'<>\-]+", s.lower())


def edit_distance(a, b):
    """Word-level Levenshtein distance (insert, delete, substitute one word), case and punctuation ignored."""
    a, b = words(a), words(b)
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


# ------------------------------------------------------------------ the runner's reference model (outcomes only)
def parse_tr(s):
    m = re.fullmatch(r"(\d+)->(\d+):(\d+)", s.strip())
    return int(m[1]), int(m[2]), int(m[3])


def parse_list(s):
    s = s.strip()[1:-1].strip()
    return [x.strip() for x in s.split(",")] if s else []


def apply(bal, t):
    f, to, a = t
    n = len(bal)
    if f >= n or to >= n or f == to or bal[f] < a or bal[to] + a > M:
        return False
    bal[f] -= a
    bal[to] += a
    return True


def outcome(values):
    """What the ledger does at an input, by a 20-line Python transcription of ledger/src/lib.rs written by the runner.
    NOT the compiled Rust: used only to print the outcome beside each case and compare it with what the author states."""
    if "the_ledger" not in values:
        s, r, a = int(values["the_sender"]), int(values["the_receiver"]), int(values["the_amount"])
        ok = s >= a and r + a <= M
        return {"ans": ok, "after": [s - a, r + a] if ok else [s, r]}
    bal = [int(x) for x in parse_list(values["the_ledger"])]
    if "the_transfer" in values:
        ok = apply(bal, parse_tr(values["the_transfer"]))
        return {"ans": ok, "after": bal}
    if "the_batch" in values:
        b = [parse_tr(x) for x in parse_list(values["the_batch"])]
        step = list(bal)
        n = 0
        for t in b:
            if not apply(step, t):
                break
            n += 1
        return {"ans": n, "after": step, "whole": n == len(b), "whole_after": step if n == len(b) else bal}
    if "the_account" in values:
        i = int(values["the_account"])
        return {"ans": bal[i] if i < len(bal) else "none", "after": bal}
    t = sum(bal)
    return {"ans": t if t <= M else "none", "after": bal}


def stated_matches(case, unit):
    """Does the outcome the author states agree with the reference model? None when nothing checkable is stated."""
    o = outcome(case["values"])
    whole = unit.startswith("B_WHOLE")
    ans = o.get("whole") if whole else o["ans"]
    after = o.get("whole_after") if whole else o["after"]
    checks = []
    if case["ans"] is not None:
        checks.append(case["ans"] == ans)
    if case["after"] is not None and not case["scaled"]:
        checks.append(case["after"] == after)
    shown = {"answer": ("accepted" if ans is True else "rejected" if ans is False else ans), "after": after}
    return (all(checks) if checks else None), shown


# the scoping modifier of a reading: the replay reports such a call as "holds" (the claim is vacuous there), so the
# runner's reference model is asked whether the call is in the modifier's scope
UNIT_MOD = {"T_TOTAL_OK": True, "T_MOVED": True, "T_ONLY": True, "B_WHOLE_OK": True, "W_TOTAL_OK": True, "T_REJ": False}


def in_modifier_scope(case):
    want = UNIT_MOD.get(case["unit"])
    if want is None or not case["values"]:
        return True
    o = outcome(case["values"])
    return (o.get("whole") if case["unit"].startswith("B_WHOLE") else o["ans"]) is want


def judge(expect, status):
    """The author's word about the rule at a case against the compiled reading's value there."""
    if status == "mismatch":
        return "READING MISMATCH"
    if status not in ("holds", "fails", "out-of-scope"):
        return "NOT EVALUATED"
    if expect == "holds":
        return {"holds": "agrees", "out-of-scope": "silent", "fails": "CONTRADICTS"}[status]
    if expect == "fails":
        return {"fails": "agrees", "holds": "CONTRADICTS", "out-of-scope": "CONTRADICTS"}[status]
    return {"out-of-scope": "agrees", "holds": "says more", "fails": "CONTRADICTS"}[status]


def run() -> dict:
    import cases as cs
    import rewordings as rw
    import try_compile as tc
    import units as un

    authors = json.loads((HERE / "authors.json").read_text())["authors"]
    flat = [(a["author"], a["model"], r) for a in authors for r in a["rules"]]
    key = lambda a, r: f"{a}/{r['id']}"

    # 1. exactly as written
    _, _, res = tc.compile_lines([r["rule"] for _, _, r in flat], ids=[f"x{n}" for n in range(len(flat))], name="as_written")
    as_written = {key(a, r): x for (a, _, r), x in zip(flat, res)}

    # 2. the rewordings, one by one (so that each rule has its own echo), and the probes
    todo = [(k, v["text"]) for k, v in rw.R.items() if v["text"]]
    _, _, res = tc.compile_lines([t for _, t in todo], ids=[f"y{n}" for n in range(len(todo))], name="reworded_each")
    reworded = {k: x for (k, _), x in zip(todo, res)}
    _, _, res = tc.compile_lines([v["text"] for v in rw.PROBES.values()], name="probes")
    probes = {k: x for k, x in zip(rw.PROBES, res)}

    # 3. the unique readings as a feature of the scratch copy: generated predicate, property test, replay; and the search
    (WORK / "features" / "v4_authored.feature").write_text(un.feature())
    (WORK / "v4" / "reworded.feature").write_text(un.feature())
    log = {}
    rc, out, secs = sh("python3 -m clausal gen")
    log["gen"] = {"rc": rc, "secs": secs, "tail": out[-300:]}
    assert rc == 0, out[-2000:]
    sh("python3 -m clausal compile v4/reworded.feature")
    (WORK / "out").mkdir(exist_ok=True)
    rc, out, secs = sh("cd lean && lake env lean Run/NewReadings.lean > ../out/new_sentences.log 2>&1")
    log["search"] = {"rc": rc, "secs": secs}
    rc, out, _ = sh("python3 -m clausal compile v4/reworded.feature --collect")
    search = {x["id"]: x for x in json.loads((WORK / "out" / "new_sentences.json").read_text())["items"]}
    gen = json.loads((WORK / "build" / "evidence_gen.json").read_text())
    ids = [un.rid(u) for u in un.UNITS if un.rid(u) in gen["readings"]]
    kani = "--kani" in sys.argv
    rc, out, secs = sh(f"python3 -m clausal evidence {'--kani-timeout 30 --jobs 4' if kani else '--quick'} --only '{','.join(ids)}'", timeout=3600)
    log["evidence"] = {"rc": rc, "secs": secs, "line": out.strip().splitlines()[-1] if out.strip() else ""}
    ev = json.loads((WORK / "out" / "evidence.json").read_text())

    # 4. the authors' cases, replayed on the compiled Rust through the generated predicate of each reading
    reqs = []
    for group, table in (("case", cs.CASES), ("extra", cs.EXTRA), ("probe", cs.PROBE_CASES)):
        for k, lst in table.items():
            for n, c in enumerate(lst):
                if c["values"]:
                    reqs.append({"rule": un.rid(c["unit"]), "values": c["values"], "tag": f"{group}|{k}|{n}"})
    f = WORK / "evidence" / "target" / "v4_replay.jsonl"
    f.write_text("\n".join(json.dumps(r) for r in reqs) + "\n")
    rc, out, secs = sh(f"./target/debug/rule-evidence --replay '{f}' --timeout-secs 20 --trees '{WORK / 'build' / 'trees.json'}'", cwd=WORK / "evidence")
    back = {r["tag"]: r for r in (json.loads(l) for l in out.splitlines() if l.startswith("{"))}
    log["replay"] = {"requests": len(reqs), "answers": len(back), "secs": secs}

    def cases_of(group, table, k):
        outl = []
        for n, c in enumerate(table.get(k, [])):
            rec = dict(c)
            if c["values"] is None:
                rec.update(status="not encodable", judgement="NOT ENCODABLE")
            else:
                b = back.get(f"{group}|{k}|{n}", {})
                rec["status"] = b.get("status", "no answer")
                if rec["status"] == "holds" and not in_modifier_scope(c):
                    rec["status"], rec["replay_status"] = "out-of-scope", "holds (vacuously: the call is outside 'successful' / 'rejected')"
                rec["judgement"] = judge(c["expect"], rec["status"])
                ok, shown = stated_matches(c, c["unit"])
                rec["code_does"], rec["stated_outcome_matches"] = shown, ok
            outl.append(rec)
        return outl

    def unit_evidence(u):
        i = un.rid(u)
        s = search.get(i, {})
        e = ev["readings"].get(i)
        sr = s.get("search") or {}
        out = {"unit": u, "id": i, "text": un.UNITS[u], "search_status": s.get("status"),
               "search": {k: sr.get(k) for k in ("tried", "in_scope", "bad", "skipped") if k in sr},
               "property": (e or {}).get("property"), "bounded": (e or {}).get("bounded")}
        false_by = []
        if s.get("status") == "COUNTEREXAMPLE":
            false_by.append("search")
        if (e or {}).get("property", {}).get("status") in ("fail", "hang"):
            false_by.append("property test")
        if any(r["status"] == "failed" for r in ((e or {}).get("bounded") or {}).get("rungs", [])):
            false_by.append("bounded check")
        out["found"] = "false" if false_by else ("true-as-far-as-tested" if e and s.get("status") == "NO-COUNTEREXAMPLE" else "not-tested")
        out["false_by"] = false_by
        return out

    unit_ev = {u: unit_evidence(u) for u in un.UNITS}
    rules = []
    for a, model, r in flat:
        k = key(a, r)
        aw = as_written[k]
        rec = {"key": k, "author": a, "model": model, "id": r["id"], "rule": r["rule"], "meantToBeTrue": r["meantToBeTrue"],
               "intentExamples": r["intentExamples"],
               "as_written": {"status": "COMPILED" if aw["compiled"] else aw["status"], "message": aw.get("message"), "nearest_forms": aw.get("hint"),
                              "echo": aw.get("echo")}}
        h = aw.get("hint") or ""
        forms = [l.strip("- ").strip() for l in h.splitlines() if l.strip().startswith("- ")]
        rec["as_written"]["hint_kind"] = "list of operation nouns" if h.startswith("operations of") else "three nearest forms" if forms else "none"
        rec["as_written"]["hint_names_other_fixture_only"] = h.startswith("operations of") and "lookup" not in h
        w = rw.R[k]
        rec["as_written"]["a_nearest_form_begins_like_the_rewording"] = bool(forms) and any(
            f.split("{")[0].strip() and f.split("{")[0].strip() in (w["text"] or "") for f in forms)
        rec["rewording"] = {"text": w["text"], "fit": w.get("fit"), "note": w.get("note", ""), "missing": w.get("missing", [])}
        if w["text"]:
            x = reworded[k]
            assert x["compiled"], (k, x)
            us = un.units_of(w["text"])
            rec["rewording"].update(edit_distance_words=edit_distance(r["rule"], w["text"]), words_original=len(words(r["rule"])),
                                    words_reworded=len(words(w["text"])), echo=x["echo"], lean=x["lean"], pieces=x["pieces"], frames=x["frames"],
                                    units=us)
            rec["cases"] = cases_of("case", cs.CASES, k)
            rec["extra_cases"] = cases_of("extra", cs.EXTRA, k)
            fs = [unit_ev[u]["found"] for u in us]
            rec["found"] = "false" if "false" in fs else "not-tested" if "not-tested" in fs else "true-as-far-as-tested"
            rec["false_by"] = sorted({b for u in us for b in unit_ev[u]["false_by"]})
            rec["label_agrees"] = (rec["found"] == "false") == (not r["meantToBeTrue"]) if rec["found"] != "not-tested" else None
            rec["wrong_reading"] = any(c["judgement"] == "CONTRADICTS" for c in rec["cases"] + rec["extra_cases"])
        if k in rw.PROBES:
            x = probes[k]
            u = un.BY_TEXT[rw.PROBES[k]["text"]]
            rec["probe"] = {"text": rw.PROBES[k]["text"], "note": rw.PROBES[k]["note"], "edit_distance_words": edit_distance(r["rule"], rw.PROBES[k]["text"]),
                            "echo": x["echo"], "pieces": x["pieces"], "unit": u, "cases": cases_of("probe", cs.PROBE_CASES, k),
                            "found": unit_ev[u]["found"]}
        rules.append(rec)
    return {"schema": "v4-proxy-sentences-v1", "date": time.strftime("%Y-%m-%d"),
            "authors_are": "language models (proxy authors), not people; the rewordings and the case encodings were made by the trial runner, also a model",
            "log": log, "kani": kani, "units": unit_ev, "rules": rules,
            "tools": ev.get("tools"), "cases_wanted": ev.get("cases_wanted"), "seed": ev.get("seed")}


# ---------------------------------------------------------------------------------------------- report (stdout)
def pct(n, d):
    return f"{n} of {d}" + (f" ({100 * n / d:.0f}%)" if d else "")


def report(d: dict) -> str:
    R = d["rules"]
    o = []
    groups = [("pooled", R)] + [(a, [r for r in R if r["author"] == a]) for a in dict.fromkeys(r["author"] for r in R)]
    o.append("V4 (proxy): AUTHORS ARE MODELS, not people. Rewordings and case encodings by the trial runner (a model).")
    o.append("")
    o.append("| | " + " | ".join(g for g, _ in groups) + " |")
    o.append("|---|" + "---|" * len(groups))

    def row(name, f):
        o.append(f"| {name} | " + " | ".join(f(rs) for _, rs in groups) + " |")
    comp = lambda rs: [r for r in rs if r["rewording"]["text"]]
    full = lambda rs: [r for r in comp(rs) if r["rewording"]["fit"] in ("exact", "more")]
    row("rules", lambda rs: str(len(rs)))
    row("compile as written", lambda rs: pct(sum(r["as_written"]["status"] == "COMPILED" for r in rs), len(rs)))
    row("refused as written: UNBOUND / ILL-TYPED / AMBIGUOUS", lambda rs: " / ".join(str(sum(r["as_written"]["status"] == s for r in rs)) for s in ("UNBOUND", "ILL-TYPED", "AMBIGUOUS")))
    row("compile after rewording, whole sentence (fit exact or more)", lambda rs: pct(len(full(rs)), len(rs)))
    row("... of which the reading says more than the sentence", lambda rs: str(sum(r["rewording"]["fit"] == "more" for r in rs)))
    row("compile after rewording, part of the sentence only (fit less)", lambda rs: pct(sum(r["rewording"]["fit"] == "less" for r in rs), len(rs)))
    row("no rewording keeps the meaning: a new piece is needed", lambda rs: pct(sum(not r["rewording"]["text"] for r in rs), len(rs)))
    row("need a new piece for all or part of the sentence", lambda rs: pct(sum(bool(r["rewording"]["missing"]) for r in rs), len(rs)))
    row("median rewording size, words changed (min to max)", lambda rs: (lambda e: f"{statistics.median(e):g} ({min(e)} to {max(e)})" if e else "-")([r["rewording"]["edit_distance_words"] for r in comp(rs)]))
    row("median words in the original / in the rewording", lambda rs: (lambda c: f"{statistics.median([r['rewording']['words_original'] for r in c]):g} / {statistics.median([r['rewording']['words_reworded'] for r in c]):g}" if c else "-")(comp(rs)))
    cases = lambda rs: [c for r in comp(rs) for c in r["cases"]]
    for j in ("agrees", "silent", "says more", "CONTRADICTS", "NOT ENCODABLE", "READING MISMATCH", "NOT EVALUATED"):
        row(f"authors' cases: {j}", lambda rs, j=j: pct(sum(c["judgement"] == j for c in cases(rs)), len(cases(rs))))
    row("cases whose stated outcome differs from what the code does", lambda rs: str(sum(c.get("stated_outcome_matches") is False for c in cases(rs))))
    row("WRONG READINGS (a compiled reading contradicted by a case)", lambda rs: str(sum(bool(r.get("wrong_reading")) for r in rs)))
    row("meant true: compiled / found true as far as tested / found false", lambda rs: (lambda c: f"{len(c)} / {sum(r['found'].startswith('true') for r in c)} / {sum(r['found'] == 'false' for r in c)}")([r for r in comp(rs) if r["meantToBeTrue"]]))
    row("meant false: compiled / found false / found true as far as tested", lambda rs: (lambda c: f"{len(c)} / {sum(r['found'] == 'false' for r in c)} / {sum(r['found'].startswith('true') for r in c)}")([r for r in comp(rs) if not r["meantToBeTrue"]]))
    row("meant true / meant false, all rules", lambda rs: f"{sum(r['meantToBeTrue'] for r in rs)} / {sum(not r['meantToBeTrue'] for r in rs)}")
    row("found agrees with the author's label (compiled rules)", lambda rs: pct(sum(r.get("label_agrees") is True for r in comp(rs)), len(comp(rs))))

    row("hint as written: operation nouns only / three nearest forms", lambda rs: f"{sum(r['as_written']['hint_kind'] == 'list of operation nouns' for r in rs)} / {sum(r['as_written']['hint_kind'] == 'three nearest forms' for r in rs)}")
    row("... operation list names only the OTHER fixture's operations", lambda rs: str(sum(r["as_written"]["hint_names_other_fixture_only"] for r in rs)))
    row("... a nearest form begins like the rewording used", lambda rs: str(sum(r["as_written"]["a_nearest_form_begins_like_the_rewording"] for r in rs)))
    o += ["", "Missing pieces, by how many rules need them (generic names):", ""]
    need = {}
    for r in R:
        for m in r["rewording"]["missing"]:
            need.setdefault(m, []).append(r["key"] + ("" if not r["rewording"]["text"] else " (part)"))
    for m, ks in sorted(need.items(), key=lambda kv: -len(kv[1])):
        o.append(f"- {len(ks)}  {m}: {', '.join(ks)}")

    o += ["", "Per rule:", "", "| rule | label | as written | rewording (words changed) | fit | cases a/s/c/n | found |", "|---|---|---|---|---|---|---|"]
    for r in R:
        w = r["rewording"]
        if w["text"]:
            cc = r["cases"]
            cnt = "/".join(str(sum(c["judgement"] == j for c in cc)) for j in ("agrees", "silent", "CONTRADICTS", "NOT ENCODABLE"))
            o.append(f"| {r['key']} | {'true' if r['meantToBeTrue'] else 'false'} | {r['as_written']['status']} | {w['text']} ({w['edit_distance_words']}) | {w['fit']} | {cnt} | {r['found']}{' by ' + ', '.join(r['false_by']) if r['false_by'] else ''} |")
        else:
            o.append(f"| {r['key']} | {'true' if r['meantToBeTrue'] else 'false'} | {r['as_written']['status']} | none: {'; '.join(m.split(':')[0] + ':' + m.split(':')[1][:60] for m in w['missing'])} | - | - | - |")
    o += ["", "Cases that are not plain agreement:", ""]
    for r in R:
        for n, c in enumerate(r.get("cases", []) + r.get("extra_cases", [])):
            if c["judgement"] != "agrees" or c.get("stated_outcome_matches") is False:
                o.append(f"- {r['key']} case {n + 1}: {c['judgement']} (author: rule {c['expect']}; reading: {c['status']}; input {json.dumps(c['values'])}; code does {json.dumps(c.get('code_does'))}"
                         + ("; STATED OUTCOME DIFFERS" if c.get("stated_outcome_matches") is False else "") + (f"; {c['note']}" if c["note"] else "") + ")")
    o += ["", "Probes (smallest compiling rewordings that do NOT keep the meaning; not counted above):", ""]
    for r in R:
        if "probe" in r:
            p = r["probe"]
            o.append(f"- {r['key']}: \"{p['text']}\" ({p['edit_distance_words']} words changed). {p['note']}. Cases: " + ", ".join(c["judgement"] for c in p["cases"]) + f". Found: {p['found']}.")
            o.append("  echo: " + " / ".join(f"{a} {b}".strip() for a, b in p["echo"][:5]))
    o += ["", "Unique readings and what the pipeline found:", ""]
    for u, e in d["units"].items():
        p = e.get("property") or {}
        b = e.get("bounded") or {}
        rungs = "; ".join(f"{x['label']}: {x['status']}" for x in b.get("rungs", [])) if b.get("ran") else "not run"
        o.append(f"- {u}: search {e['search_status']} ({(e['search'] or {}).get('in_scope', '-')} of {(e['search'] or {}).get('tried', '-')} grid points in scope); property test {p.get('status', 'none')}"
                 f" ({p.get('cases', '-')} cases in scope{', witness ' + json.dumps(p['witness']) if p.get('witness') else ''}); bounded: {rungs}; FOUND {e['found']}")
    return "\n".join(o)


if __name__ == "__main__":
    if "--print" not in sys.argv:
        d = run()
        (HERE / "results.json").write_text(json.dumps(d, indent=1, ensure_ascii=False))
    print(report(json.loads((HERE / "results.json").read_text())))
