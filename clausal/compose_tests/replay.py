"""Replay of composed sentences on recorded cases, on the COMPILED RUST, through the pipeline's own machinery.

Used by dev.py. Nothing here evaluates a sentence: the sentences are put in feature files of a SCRATCH COPY of clausal/
(made by mutation/workcopy.sh), one file per project, listed in the scratch copy's projects.yaml; `clausal gen` compiles
them, `clausal evidence --quick` builds the generated predicate of each reading, and `rule-evidence --replay` evaluates
each reading at each given input. This is the plumbing of l4b.py (which stays as it is, tied to the frozen trial).
"""
from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path

ENV = dict(os.environ, PATH=f"{Path.home()}/.elan/bin:{Path.home()}/.cargo/bin:" + os.environ["PATH"])
FEATURE = "composed"


def sh(cmd, cwd, timeout=3600):
    t0 = time.time()
    p = subprocess.run(cmd, shell=True, cwd=cwd, env=ENV, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout + p.stderr, round(time.time() - t0, 1)


def list_sentences(work: Path, voc, sentences: dict) -> dict:
    """`sentences`: {sentence: first operation id}. Writes features/composed_<project>.feature in the scratch copy and
    lists each under its project. {sentence: reading id}."""
    import yaml
    from clausal import projects as pj, vocab
    assert work.resolve() != Path(__file__).resolve().parent.parent, "the scratch copy only: the tracked projects.yaml is never edited"
    ids = {s: f"s{n:03d}" for n, s in enumerate(sentences)}
    files = {}
    for s, op in sentences.items():
        book = voc.home[op].rel
        proj = next(p for p in pj.load(work) if any(book == f"{vocab.BOOK_DIR}/{b}" for b in p.books))
        files.setdefault(proj.name, []).append(s)
    path = work / pj.FILE
    raw = yaml.safe_load(path.read_text())
    for d in raw["projects"]:
        rel = f"features/{FEATURE}_{d['name']}.feature"
        d["features"] = [f for f in d["features"] if not Path(f).name.startswith(FEATURE)]
        (work / rel).unlink(missing_ok=True)
        if d["name"] in files:
            lines = [f"Feature: composed {d['name']}", "  Sentences of `clausal compose` under test. Scratch copy only.", ""]
            for s in files[d["name"]]:
                lines += [f"  @id:{ids[s]}", f"  Rule: {s}", ""]
            (work / rel).write_text("\n".join(lines))
            d["features"].append(rel)
    path.write_text(yaml.safe_dump(raw, sort_keys=False))
    return {s: f"Rule.{FEATURE}_{p}.{ids[s]}" for p, v in files.items() for s in v}


def run(work: Path, voc, sentences: dict, requests: list) -> tuple:
    """`requests`: [{sentence, values: {variable: literal}, tag}]. ({tag: status}, {sentence: [variable names]}, log)."""
    rid = list_sentences(work, voc, sentences)
    log = {}
    rc, out, secs = sh("python3 -m clausal gen", work)
    log["gen"] = {"rc": rc, "secs": secs, "tail": out[-300:]}
    assert rc == 0, out[-3000:]
    gen = json.loads((work / "build" / "evidence_gen.json").read_text())["readings"]
    log["without_generated_predicate"] = [s for s, i in rid.items() if i not in gen]
    ids = [i for i in rid.values() if i in gen]
    rc, out, secs = sh(f"python3 -m clausal evidence --quick --only '{','.join(ids)}'", work)
    log["evidence"] = {"rc": rc, "secs": secs, "line": out.strip().splitlines()[-1] if out.strip() else ""}
    vars_of = {s: [v[0] for v in gen[i]["vars"]] for s, i in rid.items() if i in gen}
    reqs = [{"rule": rid[r["sentence"]], "values": r["values"], "tag": r["tag"]} for r in requests if r["sentence"] in vars_of]
    f = work / "evidence" / "target" / "composed_replay.jsonl"
    f.write_text("\n".join(json.dumps(r) for r in reqs) + "\n")
    rc, out, secs = sh(f"./target/debug/rule-evidence --replay '{f}' --timeout-secs 20 --trees '{work / 'build' / 'trees.json'}'", work / "evidence")
    back = {r["tag"]: r.get("status", "no answer") for r in (json.loads(l) for l in out.splitlines() if l.startswith("{")) if "tag" in r}
    log["replay"] = {"rc": rc, "requests": len(reqs), "answers": len(back), "secs": secs}
    return back, vars_of, log
