# Sentences trial (plan node V4, proxy version)

Do rules written by people who do not know the vocabulary compile from its existing pieces, and does the compiled reading say what the author meant?

**The authors here are language models, not people** (`opus-1`, `sonnet-1`, `haiku-1`, `default-1`). Each saw only a prose description of the ledger and the wallet, never the vocabulary, and recorded five intended cases per rule before any compiled reading existed. The rewordings and the encodings of the cases were made by the trial runner, also a model, who had read the vocabulary. Nothing here is evidence about people.

## What is here

| file | what it is |
|---|---|
| `RESULTS.md` | what the V4 and V5 proxy trials found, what model authors and readers can and cannot show, and how to redo both with people. Not for anyone who will take the echo trial |
| `AUTHOR_BRIEF.md`, `author_template.json` | the one page an author is given, and the file they send back; for people and for model authors alike |
| `check_author.py` | checks an author's file; with `--compile` (needs the scratch copy) compiles every rule exactly as written and prints status and echo |
| `authors.json` | the 48 rules as the authors wrote them, with their label (meant true / meant false) and five cases each |
| `rewordings.py` | per rule: the smallest rewording found that compiles and keeps the meaning shown by the cases, how well it fits (`exact`, `more`, `less`), or `None` with the missing piece named generically; and two probes (the smallest compiling rewordings that do not keep the meaning) |
| `cases.py` | the authors' cases encoded as inputs of the compiled readings, with the outcome the author states |
| `units.py` | the unique compiled readings (several rules reword to the same line) |
| `try_compile.py` | compile candidate Rule lines in the scratch copy and print status, nearest forms and echo; no Lean |
| `run_v4.py` | the whole trial; writes `results.json`; `--print` prints the tables again |
| `results.json` | per rule: status as written with the nearest forms offered, rewording, word edit distance, echo, Lean statement, pieces, each case with the reading's value and the outcome, what the search, the generated property test and the generated bounded check found |
| `raw/` | the pipeline's own outputs for the unique readings: `new_sentences.json` (compile and search), `evidence.json` (property tests, Kani), and the feature file that was put in the scratch copy |

## Running it

```sh
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
bash ../../slice/mutation/workcopy.sh "$PWD/work/slice"   # scratch copy of slice/ (about 4 GB, APFS clones); slice/ itself is only read
python3 run_v4.py            # about 15 s warm: compile, one Lean run (the reading search), property tests, replay of the cases
python3 run_v4.py --kani     # the same with the generated bounded checks (about 2.5 min)
python3 run_v4.py --print    # the tables from results.json, nothing run
python3 check_author.py FILE.json --compile   # any author's file (or authors.json), compiled as written; nothing stored
rm -rf work                  # the scratch copy is not kept
```

How a rule is judged:

- **As written**: `python3 -m slicegen compile` on the author's sentence, unchanged. Compiled, UNBOUND, ILL-TYPED or AMBIGUOUS, with the nearest forms the tool offers.
- **Reworded**: the runner's rewording, with the word-level edit distance (insert, delete or substitute one word; case and punctuation ignored).
- **Cases**: each of the author's five cases is put to the compiled reading on the compiled Rust (`rule-evidence --replay`, the generated predicate of the reading). The reading holds, fails or is out of scope there; the author said the rule holds, fails or does not apply there. A reading that fails where the author says the rule holds, or holds where the author says it is false, CONTRADICTS the case: a wrong reading. A 20-line Python transcription of the ledger, written by the runner, prints what the code does at each case so that the author's stated outcome can be compared; it is not the compiled Rust.
- **Found true / false**: the reading search on the Lean model (a grid), the generated property test (10,000 cases in scope) and, with `--kani`, the generated bounded check. "True as far as tested" is not a proof.

The second trial that uses these rules, the echo trial on real generated echoes (V5), is in `../meaning/banks/generated-echoes-v1/`.
