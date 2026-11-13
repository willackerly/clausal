# Arm A0: composer version 1 on the merged book, on the 48 frozen sentences (CONTAMINATED)

One run, 2026-11-12, of the repaired `../l4b.py` at commit `2f2cb46` (composer `clausal/compose.py` as merged, book as
merged), in a private copy of `trials/sentences`. It is the baseline for composer version 2 (plan node L4r, arm A0).

**Contaminated.** Version 1 was measured on these 48 sentences before, its report was read, and the version-2 design
(`docs/studies/2026-11-12/composer-v2.md`) was derived from the failures on them. No number here is a clean
measurement and none is to be used in a decision. Nothing was tuned on this run; the builder of version 2 read the
count table and the first entry of `REPORT.md` and nothing below it.

`REPORT.md` and `results.json` are the script's output, unedited (the title "first measurement" is the script's).

| outcome | first run, book before the merge (`../l4b/`) | A0, merged book (this directory) |
|---|---|---|
| TOP-RIGHT | 5 | 7 |
| RIGHT-IN-TOP-3 | 5 | 2 |
| WRONG-READING | 20 | 21 |
| NO-CANDIDATE | 0 | 0 |
| NOT-SCORABLE | 18 | 18 |

"RIGHT" is agreement with the author on at most five recorded inputs (see `../l4b.py`), and version 1 never declines.

Reproduce (about 2 minutes warm):

```sh
S=<a private directory>
cp -R trials/sentences $S/sentences
bash clausal/mutation/workcopy.sh $S/sentences/work/clausal
tools/sem.sh 3 -- python3 clausal/compose_tests/l4b.py $S/sentences --out $PWD/clausal/compose_tests/l4b_a0
```
