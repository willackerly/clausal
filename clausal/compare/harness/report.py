#!/usr/bin/env python3
"""Build TRADES.md from TRADES.template.md by putting the generated tables where `{{table:NAME}}` stands.

    python3 harness/report.py

Tables come from results/tables.md (harness/analyse.py) and results/cost.md (harness/cost.py). The
prose of the template, including the numbers quoted in it, is hand-written: after a rerun with
different results, read it against the tables.
"""
import re
import sys
from pathlib import Path

COMPARE = Path(__file__).resolve().parent.parent


def main():
    tables = {}
    for f in ("results/tables.md", "results/cost.md"):
        for m in re.finditer(r"<!-- table:(\w+) -->\n(.*?)(?=\n\n<!-- table:|\Z)", (COMPARE / f).read_text(), re.S):
            tables[m.group(1)] = m.group(2).strip()
    text = (COMPARE / "TRADES.template.md").read_text()
    # PREREG.md: a run is reported as registered only if the frozen files still have their recorded digests
    sys.path.insert(0, str(COMPARE / "harness"))
    import freeze
    import json
    frozen = json.loads((COMPARE / "results" / "frozen.json").read_text())
    changed = [f for f, h in freeze.digests().items() if frozen["sha256"].get(f) != h]
    text = text.replace("{{frozen_check}}", (f"unchanged since they were frozen at {frozen['frozen_at']} (checked when this file was built)" if not changed
                                             else "**CHANGED since the freeze: " + ", ".join(changed) + ". This run is NOT as registered.**"))
    missing = [n for n in re.findall(r"\{\{table:(\w+)\}\}", text) if n not in tables]
    if missing:
        sys.exit(f"no such table: {missing}")
    text = re.sub(r"\{\{table:(\w+)\}\}", lambda m: tables[m.group(1)], text)
    (COMPARE / "TRADES.md").write_text(text)
    print(f"wrote TRADES.md ({len(text.splitlines())} lines)")


if __name__ == "__main__":
    main()
