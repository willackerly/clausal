#!/usr/bin/env python3
"""Build the two mutant sets from the frozen snapshot and write them to mutants/.

    python3 harness/mutants.py

  mutants/cargo-mutants.json   EVERY mutant `cargo mutants --list` generates for wallet/ and ledger/
                               (cargo-mutants picks them; nobody here does). Each has the unified diff
                               cargo-mutants prints, which is what gets applied.
  mutants/hand-written.json    the 45 hand-written mutants of slice/mutation/run_mutants.py at the snapshot
                               commit (18 wallet, 22 ledger by the builder, 5 ledger by the reviewer),
                               as (old text, new text) pairs. A separately labelled set.
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import sys

from common import MUTANTS, SNAPSHOT, WORK, sh


def tool_mutants():
    gen = WORK / "mutgen"
    shutil.rmtree(gen, ignore_errors=True)
    gen.mkdir(parents=True)
    out = []
    _, version, _ = sh("cargo mutants --version", WORK)
    for crate in ("wallet", "ledger"):
        shutil.copytree(SNAPSHOT / crate, gen / crate, ignore=shutil.ignore_patterns("target"))
        rc, txt, _ = sh("cargo mutants --list --json --diff 2>/dev/null", gen / crate)
        assert rc == 0, txt
        for k, m in enumerate(json.loads(txt), 1):
            out.append({"id": f"cm-{crate[0]}{k:02d}", "set": "cargo-mutants", "crate": crate,
                        "fn": m["function"]["function_name"] if m.get("function") else None,
                        "description": m["name"], "genre": m["genre"], "replacement": m["replacement"],
                        "line": m["span"]["start"]["line"], "diff": m["diff"]})
    return version.strip(), out


def hand_mutants():
    spec = importlib.util.spec_from_file_location("run_mutants", SNAPSHOT / "mutation" / "run_mutants.py")
    sys.path.insert(0, str(SNAPSHOT))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = []
    for id_, fn, what, old, new in mod.MUTANTS + mod.LEDGER_MUTANTS:
        crate = "ledger" if fn.startswith("ledger::") else "wallet"
        author = "reviewer" if id_.startswith("r") else "builder"
        out.append({"id": f"hand-{id_}", "set": "hand-written", "author": author, "crate": crate, "fn": fn.rsplit("::", 1)[-1],
                    "description": what, "old": old, "new": new})
    return out


def apply(mutant: dict, root):
    """Apply a mutant to <root>/<crate>/src/lib.rs."""
    lib = root / mutant["crate"] / "src" / "lib.rs"
    if mutant["set"] == "cargo-mutants":
        d = root / "build" / "mutant.diff"
        d.parent.mkdir(exist_ok=True)
        d.write_text(mutant["diff"])
        rc, out, _ = sh(f"patch -s '{lib}' < '{d}'", root)
        assert rc == 0, f"{mutant['id']}: patch failed: {out}"
    else:
        s = lib.read_text()
        assert s.count(mutant["old"]) == 1, f"{mutant['id']}: pattern occurs {s.count(mutant['old'])} times"
        lib.write_text(s.replace(mutant["old"], mutant["new"]))


def load():
    return json.loads((MUTANTS / "cargo-mutants.json").read_text())["mutants"] + json.loads((MUTANTS / "hand-written.json").read_text())["mutants"]


if __name__ == "__main__":
    MUTANTS.mkdir(exist_ok=True)
    version, tool = tool_mutants()
    commit = (SNAPSHOT / "compare" / "SLICE_COMMIT").read_text().strip()
    (MUTANTS / "cargo-mutants.json").write_text(json.dumps(
        {"tool": version, "command": "cargo mutants --list --json --diff (in wallet/ and in ledger/)", "slice_commit": commit,
         "mutants": tool}, indent=1) + "\n")
    hand = hand_mutants()
    (MUTANTS / "hand-written.json").write_text(json.dumps(
        {"source": "slice/mutation/run_mutants.py (MUTANTS + LEDGER_MUTANTS)", "slice_commit": commit, "mutants": hand}, indent=1) + "\n")
    print(f"{version}: {len(tool)} mutants ({sum(m['crate'] == 'wallet' for m in tool)} wallet, {sum(m['crate'] == 'ledger' for m in tool)} ledger); "
          f"hand-written: {len(hand)} ({sum(m['crate'] == 'wallet' for m in hand)} wallet, {sum(m['crate'] == 'ledger' for m in hand)} ledger)")
