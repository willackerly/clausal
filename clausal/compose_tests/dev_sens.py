#!/usr/bin/env python3
"""CONTROL OF THE SENSITIVITY RUN (fix round of plan node L1c): the development set with the frozen-only cue entries removed.

    bash clausal/mutation/workcopy.sh $S/clausal
    tools/sem.sh 3 -- python3 clausal/compose_tests/dev_sens.py $S/clausal      # writes compose_tests/dev/sens_control.json

No removed entry matches a development sentence (that is how the list is made: compose_tests/cue_audit.py), so the
composer and the dialogue should do on the development set exactly what the committed run records
(compose_tests/dev/results.json). This script composes each of the 60 sentences as dev.py does (A1; A1s with the system
where the system is asked; A1o with the operation where the operation is asked; the dialogue with the oracle author where
there is a gold reading), with the entries removed by compose_tests/ablate.py, and compares, per sentence:
  A1, A1s, A1o   outcome, question kind, and per shown candidate its sentence, dropped words, added pieces, full or not
  A1d            how the dialogue ends, the number of questions, each turn's kind and answer, at gold or not, the sentence
No sentence is replayed on the cases: a row of the development tallies is a function of what is compared here and of the
replay of the same sentences. If every sentence is the same, the development tallies without the entries are the committed
ones. A sentence that differs is listed, and means the removal reaches further than its list says.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEV = HERE / "dev"


def shown(res: dict) -> list:
    return [[x["sentence"], x["coverage"]["dropped"], x["coverage"]["added"], x["coverage"]["full"]] for x in res["candidates"]]


def main() -> int:
    work = Path(sys.argv[1]).resolve()
    assert (work / "clausal" / "compose2.py").exists(), f"no scratch copy of clausal/ at {work} (see the usage)"
    sys.path.insert(0, str(work))
    sys.path.insert(0, str(HERE))
    import os
    os.chdir(work)
    from clausal import compose2, cues2, dialogue
    import ablate
    import dev
    rec = ablate.install(compose2, cues2, json.loads((HERE / "cue_audit.json").read_text())["frozen_only"])
    items = json.loads((DEV / "devset.json").read_text())
    gold = json.loads((DEV / "gold.json").read_text())["gold"]
    old = {r["id"]: r for r in json.loads((DEV / "results.json").read_text())["rows"]}
    t0, rows = time.time(), []
    for it in items:
        o = old[it["id"]]
        a1 = compose2.compose(it["sentence"])
        a1s = compose2.compose(it["sentence"], it["system"]) if a1["outcome"] == "ASK" and a1["ask"] == "system" else a1
        opid = dev.case_op(it["system"], it["cases"])
        a1o = compose2.compose(it["sentence"], None, operation=opid) if a1s["outcome"] == "ASK" and a1s["ask"] == "operation" and opid else a1s
        diff = {}
        for arm, res in (("A1", a1), ("A1s", a1s), ("A1o", a1o)):
            was = [o[arm]["outcome"], o[arm]["ask"], [[x["sentence"], x["dropped"], x["added"], x["full"]] for x in o[arm]["shown"]]]
            now = [res["outcome"], res["ask"], shown(res)]
            if was != now:
                diff[arm] = {"committed": was[:2] + [[x[0] for x in was[2]]], "now": now[:2] + [[x[0] for x in now[2]]]}
        g = (gold.get(it["id"]) or {}).get("sentences")
        if g:
            orc = dialogue.Oracle(g, it["system"])
            d = dialogue.converse(it["sentence"], orc)
            ag = dialogue.at_gold(d, orc)
            x = o["A1d"]
            was = [x["end"], x["questions"], [[t["kind"], t["answer"]] for t in x["turns"]], x["at_gold"], (x["first"] or {}).get("sentence")]
            now = [d["end"], d["questions"], [[t["kind"], t["answer"]] for t in d["turns"]], ag["at_gold"], d["sentence"]]
            if json.loads(json.dumps(was)) != json.loads(json.dumps(now)):
                diff["A1d"] = {"committed": was, "now": now}
        rows.append({"id": it["id"], "same": not diff, "diff": diff})
        print(f"{it['id']} {'same' if not diff else 'DIFFERS: ' + ', '.join(diff)}", file=sys.stderr, flush=True)
    res = {"schema": "dev-sens-control-v1", "date": time.strftime("%Y-%m-%d"),
           "what": "the development set composed with the frozen-only cue entries removed (compose_tests/ablate.py), compared with the committed "
                   "development run (compose_tests/dev/results.json); see compose_tests/dev_sens.py",
           "removed": rec["removed"], "skipped_matches": {k[1]: v for k, v in sorted(ablate.hits.items())},
           "sentences": len(rows), "with_dialogue": sum(1 for it in items if (gold.get(it["id"]) or {}).get("sentences")),
           "same": sum(r["same"] for r in rows), "differ": [r for r in rows if not r["same"]], "seconds": round(time.time() - t0, 1)}
    (DEV / "sens_control.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    print(f"development set without the frozen-only entries: {res['same']} of {res['sentences']} sentences the same as the committed run "
          f"({res['with_dialogue']} with a dialogue); skipped matches: {res['skipped_matches'] or 'none'}")
    for r in res["differ"]:
        print(" ", r["id"], json.dumps(r["diff"], ensure_ascii=False)[:600])
    return 0 if res["same"] == res["sentences"] else 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main())
