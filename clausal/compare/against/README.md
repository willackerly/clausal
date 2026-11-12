# compare/against: this tree against a commit

Three comparisons that a change to the compiler has to report ("verdicts identical", "the compiled readings are the
same", "which bounded checks answered differently"). Each takes a git revision (default `5e6cfa7`, the tree before plan
nodes Q1 and Q2) and reads that revision's files with `git show` / `git archive`; nothing outside the repository is read.
Run from `clausal/`.

| command | compares | needs |
|---|---|---|
| `python3 compare/against/verdicts.py [rev]` | the outcome code of every verdict (scenario, rule group, function) in `out/graph.json` with the same file at `rev` | a finished `./run.sh` in this tree |
| `python3 compare/against/readings.py [rev]` | every compilation of the fixtures (scenarios and Rule lines): Lean statement, status, defaults, echo text; compiled now by this tree's compiler and by the compiler at `rev` | nothing (no Lean, no run) |
| `python3 compare/against/bounded.py [rev]` | the bounded-check (Kani) rung results of every reading in `out/graph.json` with the same file at `rev` | a finished full `./run.sh` (not `--quick`) in this tree |

`verdicts.py` exits 1 if a code differs. `readings.py` exits 1 if a Lean statement, a status or a list of defaults
differs. An echo that differs is counted (separately: only the name of a slot, or the text of a line), the lines whose
text differs are listed, and it is not a failure: the echo is what Q2 changed.
`bounded.py` always exits 0: rungs answer differently under machine load; it lists each difference.

`verdicts.py` and `bounded.py` also take the path of a stored `graph.json` in place of a revision.
