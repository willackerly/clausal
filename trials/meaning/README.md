# Meaning trial (plan node K1)

Does a reader catch a wrong formal reading of an English rule when the reading is echoed back in plain English? Each item shows two texts. The reader says whether the second says exactly the same thing as the first, how sure they are, and why. Some second texts are faithful and some are subtly wrong; the answer key says which.

The same items, brief and question are used for model readers ("proxy") and for people ("human"). The two are always reported separately.

## What is here

| file | what it is | gives the key away? |
|---|---|---|
| `brief.md` | the half page a reader gets first | no |
| `items.json` | the items as a reader sees them, and the question asked | no |
| `take_trial.py` | terminal runner for a person | no |
| `trial.html` | the same trial as one self-contained web page | no |
| `trial.template.html`, `build_html.py` | source of `trial.html`; also makes a reader kit | no |
| `SUMMARY.md` | headline rates, no item named | no |
| `score.py`, `run_tests.py` | scoring and tests, for the organiser | no (they read the key, they do not contain it) |
| `key.json` | the answer key, with a disagreeing input for each wrong item | **yes** |
| `responses/<reader>.json` | one answers file per reader | **yes** (reasons name the defects) |
| `REPORT.md`, `results.json` | full results, written by `score.py` | **yes** |
| `analyst_notes.md`, `item_flags.json` | hand-written notes and item flags, copied into the report | **yes** |

Everything marked **yes** is listed in `.gitignore` here, so it exists on the organiser's machine and not in the public repository. See "Keeping the key away from readers".

## Item banks

| bank | directory | what the second text is | run so far |
|---|---|---|---|
| `wallet-ledger-k1` (plan node K1) | this directory | echoes and glossary entries written by hand | 8 proxy readers, 2026-11-10 |
| `wallet-ledger-generated-echoes-v1` (plan node V5) | `banks/generated-echoes-v1/` | echoes printed by the tool; the unfaithful ones are the tool's echo of a mutated rule | 4 proxy readers, 2026-11-11 |

Every command below takes `--bank banks/generated-echoes-v1` to use the second bank: `build_html.py`, `take_trial.py`, `score.py` and `run_tests.py`. Each bank's `REPORT.md`, `SUMMARY.md` and `results.json` are written into the bank's own directory. `../sentences/RESULTS.md` reads the V5 run together with the sentences trial (V4).

## Giving the trial to a person

1. Make a reader kit: `python3 build_html.py --kit /some/folder`. The folder then holds `take_trial.py`, `items.json`, `brief.md` and `trial.html`, and nothing else.
2. Send the folder, or only `trial.html` for someone who will not use a terminal.
3. The reader runs one of:
   - `python3 take_trial.py --reader NAME` (Python 3.8 or later, nothing to install), or
   - opens `trial.html` in a browser. It works offline and sends nothing anywhere.
4. The reader sends back one file, `NAME.json`: the terminal runner writes it to `responses/NAME.json` next to the script, and the web page offers it as a download.
5. Put that file in `responses/` here and run `python3 score.py`.

What the reader gets, in both versions: the brief, then one item at a time. Parts stay in order (Part A, then Part B) and items are shuffled within each part with a seed chosen for that reader; the seed and the order are written into the answers file. For each item the reader gives a judgement (faithful or not faithful), a confidence from 50 to 100, and a reason (required when the judgement is not faithful). The time on each item is recorded. There is no feedback and no going back to an earlier item.

Stopping and resuming: in the terminal, `q`, Ctrl-C or closing the window keeps every finished item; running the same command again carries on. In the browser, progress is kept in that browser, and "Save and stop" also offers a partial file that can be loaded on the start page later. A finished answers file is never overwritten; to take the trial again use another name.

`NAME` may be a pseudonym. It becomes the file name and appears in the report.

## Adding a reader

- **A person:** as above. The answers file is marked `"reader_type": "human"` by the runner.
- **A model:** write `responses/<reader>.json` in the same shape as the existing proxy files: `"reader_type": "proxy"`, `"model"` and `"model_id"` naming the model, `"material_sha256"` copied from an existing file, and `"answers"` as a list of `{"id", "judgement", "confidence", "reason", "seconds"}` with `judgement` either `faithful` or `not-faithful`. Send the model only `brief.md` and `items.json`. Say in `"presentation"` how the items were shown, and in `"caveat"` anything odd about the run; a reader with a caveat is scored, and the report also gives the pooled rates without it.
- Then `python3 score.py`. It refuses a file that names an unknown item, answers an item twice, or has no reader type, and it warns when a file was answered against a different version of the items.

## Scoring

`python3 score.py` reads `items.json`, `key.json`, `responses/`, `item_flags.json` and `analyst_notes.md` and writes:

- `REPORT.md`: for proxy readers and for human readers separately, per reader and pooled: share of unfaithful items caught and false-alarm rate on faithful items, with 95% Wilson intervals, an interval from resampling items and one from resampling items and readers together; the same split by part (echo, glossary), by structure (wrong in a single piece, wrong only through composition) and by error kind; rates by model; agreement between readers; the items the readers split on; the unfaithful items most often missed and the faithful items most often flagged, with the readers' reasons; confidence and time; and a table of every item. `analyst_notes.md` is copied in after the headline.
- `SUMMARY.md`: the same rates with nothing that names an item. This one can be made public.
- `results.json`: the numbers, for other scripts.

Options: `--bank DIR` for another item bank, `--out DIR` to write somewhere else, `--exclude-reader NAME` to leave a reader out (the report says so).

`item_flags.json` lists items the analyst thinks the author should look at again. Flagged items stay in every table. Items flagged `key-debatable` are also left out of one row of the report's sensitivity table, so the effect of a doubtful key is visible without the item being dropped.

`python3 run_tests.py` (or `python3 run_tests.py --bank DIR` for another bank) checks the whole chain in a temporary directory: the reader kit holds no key text; the terminal runner, fed piped answers in a folder with no key, is interrupted, resumed and finished, and opens no file other than its script, the items, the brief and its own answers file; `trial.html` passes its self-test in headless Chrome if Chrome is installed (`trial.html#selftest` drives the page's own controls through a stop, a reload and a resume); and `score.py` gives the expected rates for a reader who answers exactly as the key and one who flags everything.

## Keeping the key away from readers

- **Separate files.** `items.json` holds only an id, a part and the two texts for each item. `build_html.py` refuses to build if an item carries any other field. Item ids were assigned after shuffling and say nothing about the answer.
- **The reader's programs cannot show it.** `take_trial.py`, `build_html.py` and `trial.html` contain no code that reads `key.json`, and the kit made by `build_html.py --kit` does not include it. `run_tests.py` checks both, the first with an audit hook that logs every file the runner opens.
- **No feedback.** Neither runner tells the reader whether an answer is right.
- **Not in the public repository.** `key.json`, `responses/`, `REPORT.md`, `results.json`, `analyst_notes.md` and `item_flags.json` are git-ignored in this directory. The reasons in other readers' answers and the item lists in the report give the key away as surely as the key does. To publish them once people have taken the trial, delete the lines in `.gitignore`.
- **What this does not do.** A reader with access to the organiser's machine, or to a copy of the full directory, can read the key. The ignored files have no backup in git; keep a copy somewhere private. And anyone who has read `REPORT.md` or the key should not be counted as a reader.

## Adding an item bank for another domain

A bank is a directory with its own `items.json`, brief, `key.json` and `responses/`. The scripts take `--bank DIR`; the default is this directory, which holds the wallet and ledger bank. Put further banks in `banks/<name>/` (the `.gitignore` already covers the key files there).

1. Write `banks/<name>/brief.md`: what a reader needs to know and how rules are to be read. Any convention the key relies on must be stated here.
2. Write `banks/<name>/items.json`:

   ```json
   {
     "schema": "meaning-trial-items-v1",
     "bank": "<name>-v1",
     "title": "shown to the reader",
     "brief_file": "brief.md",
     "instructions": "shown after the brief",
     "judgements": ["faithful", "not-faithful"],
     "parts": [
       {"kind": "echo", "title": "Part A", "first_label": "RULE", "second_label": "ECHO", "question": "shown above every item of this part"}
     ],
     "items": [
       {"id": "E01", "kind": "echo", "first": "the rule", "second": "the echo"}
     ]
   }
   ```

   A bank may have one part or several. Text between backticks is shown as code in the browser. Shuffle the items before numbering them so that ids do not reveal the answer.
3. Write `banks/<name>/key.json`:

   ```json
   {
     "schema": "meaning-trial-key-v1",
     "bank": "<name>-v1",
     "material_sha256": "printed by build_html.py",
     "targets": {"catch_rate_min": 0.9, "false_alarm_rate_max": 0.1, "source": "where the targets come from"},
     "items": {
       "E01": {"faithful": false, "error_kind": "strictness", "structure": "single-piece", "explanation": "what differs, with an input on which the two texts disagree"}
     }
   }
   ```

   `structure` is `single-piece` or `composition` for an unfaithful item and `null` for a faithful one. `error_kind` is free text (`none` for a faithful item); the report groups by it.
4. `python3 build_html.py --bank banks/<name>` writes that bank's `trial.html` and prints the hash to put in `key.json`. `python3 take_trial.py --bank banks/<name> --reader NAME` runs it in a terminal, and `python3 score.py --bank banks/<name>` scores it.
5. Per the plan: the items should be written by someone other than whoever reviews or builds the thing under test, and `items.json`, the brief and the hash should be committed before any reader answers.

**Changing an existing bank.** The hash covers `items.json` and the brief. Any edit to either changes it, the existing answers files then no longer match, and `score.py` says so. To fix an item, copy the bank to a new directory with a new `bank` name and edit there; the old bank stays as the record of what its readers answered. Rebuild `trial.html` after any change.

## Formats

An answers file:

```json
{
  "schema": "meaning-trial-response-v1",
  "bank": "wallet-ledger-k1",
  "material_sha256": "…",
  "reader": "NAME",
  "reader_type": "human",
  "model": null,
  "background": "one line from the reader",
  "presentation": "terminal (take_trial.py), one item at a time",
  "shuffle": "python-random-shuffle-per-part-v1",
  "seed": 123456789,
  "order": ["E22", "E06", "…"],
  "started": "2026-11-10T07:37:20Z",
  "finished": "2026-11-10T08:30:02Z",
  "complete": true,
  "resumed": 0,
  "answers": [
    {"id": "E22", "judgement": "faithful", "confidence": 0.8, "reason": "…", "seconds": 41.2, "seconds_to_judgement": 30.5, "brief_views": 0}
  ]
}
```

`confidence` is stored from 0 to 1 (the reader types 50 to 100). `seconds` runs from the item appearing to the reason being entered; in the browser it leaves out time while the tab was hidden, and `wall_seconds` has the full span. The terminal and browser versions shuffle with different generators, so the same seed gives a different order in each; the order itself is always recorded.

## Provenance of the wallet and ledger bank

The items, key and brief were written by a model (`claude-opus-5-5`) acting as item author in the workflow run of 2026-11-10 and passed straight to eight model readers. The files here were extracted byte for byte from what that workflow passed on; nothing was retyped. The author's own notes are in `DECISIONS.md` under "K1 item bank". What the proxy run does and does not show is in `REPORT.md`.
