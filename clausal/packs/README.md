# Rule packs (plan node K1)

Design note for `clausal/clausal/pack.py`, `clausal/packs/` and the first target `clausal/kvparse/`. Source of the
design: `docs/studies/2026-11-12/packs.md`. Results of the first measurement: `validated-input/RESULTS.md`.

## What a rule pack is

A **rule pack** is a parameterised suite of ordinary Clausal sentences with holes for a project's operation and nouns.

| | Clausebook word pack (`clausebook/ledger.yaml`) | Rule pack (`packs/validated-input/`) |
|---|---|---|
| Supplies | words, each with a Lean definition | sentences with `{slot}` holes; no Lean |
| Trusted | yes, piece by piece | no: its output is plain Rule lines the ordinary compiler reads |
| Read by the pipeline | yes (`clausebook/project.yaml`) | **never** |

A pack carries no meaning of its own. Everything a pack rule says comes from the frames of core and from the words
the project puts in the slots. The test of that claim is the strip test below.

## Files

    packs/<name>/pack.yaml                    slots, members (template sentences), axes and variants, the adequacy
                                              expectation, the seeded bug list. Versioned: a change is a new version.
    packs/<name>/FREEZE.md                    what was frozen before a target was looked at; how results are counted
    packs/<name>/SECOND_TARGET.md             the predicted slot fills of the next target, written before the first existed
    features/<feature>.pack.<name>.yaml       BINDINGS of one instantiation: slots, variants, waivers, expected-verdict
                                              tags, and what came of each member. Beside the feature file.
    features/<feature>.feature                the instantiated lines, between two marker comments, each tagged
                                              @pack:<name>@<version> @pack-rule:<member id>

## The command

    python3 -m clausal pack instantiate <pack> --project P --slots name="words" ... --variants axis=choice ...
            [--waive MEMBER="reason"] [--expect MEMBER=unproved|refuted] [--bindings FILE] [--feature F] [--prefix X] [--dry-run]
    python3 -m clausal pack check
    python3 -m clausal pack strip <file.feature> [--out FILE]

`instantiate` is text expansion and nothing else:

1. Each `{slot}` of each member's sentence (for the chosen variant) is replaced by the words given.
2. Each resulting line is handed to the ordinary compiler with the project's books. A line that is refused is **not
   written**; the member is reported as *cannot be stated* with the refusal.
3. The lines that compile are written into the project's feature file between `# >>> pack <name>@<v>` and
   `# <<< pack <name>@<v>` (a second run replaces the block), and the bindings file is written beside it.
4. The **completeness line** is printed. It always counts what is not stated:
   `pack validated-input@1 on kvparse: INCOMPLETE: 11 members: 10 stated (3 of them through a workaround word: ...), 0 waived, 0 not applicable, 1 CANNOT BE STATED (VI-7a: ...). STATED means only that the sentence compiles ...`.
   It reads COMPLETE only when every member is stated.

**What "stated" does not mean** (fix round; the line now says so itself). A stated member is a sentence that compiles
with the project's words. It is not a rule that was examined: what examines it is the project's search, on the
project's inputs. It is not a rule that says what the member's `says:` reads either: that depends on the project's
word meaning what the slot's `means:` asks, which nothing checks (on kvparse the first encoder did not, see
`validated-input/RESULTS.md`). And the count moves with the variants and with how the project's words are built.

`check` re-expands every bindings file and compares the text with the tagged lines of the feature (**drift**: exit 1),
and prints the completeness line again. `strip` removes the pack's tags and empties its marker comments; every line
keeps its number, because the term lock of the book records line numbers.

Per slot the command also prints whether the words, on their own, read as a piece of the category the pack names in
the project's books. That is informational: a slot is words, and the only check with authority is the compilation of
each whole sentence.

## Invariants

- **The pipeline does not read packs.** `run.sh`, `clausal gen` and the report import nothing from `pack.py` and open
  no file under `packs/` and no bindings file. `pack.py` is reached only through `python3 -m clausal pack`.
- **Tags are inert.** `@pack:` and `@pack-rule:` are carried into `out/graph.json` as tags of the rule node, like any
  tag, and are read by nothing.
- **A pack adds no grammar, no piece and no synonym.** No edit of `clausebook/core.yaml` or `lean/Frames` was made.
- **Variants are whole sentences.** A policy axis chooses among sentences; no sentence has a parameter that changes
  its meaning. A choice the pack has no sentence for is printed as *cannot be stated*.
- **A draft is never written.** A member the pack marks `stated: no` has a `draft` (what one would write). The command
  hands the draft to the compiler to record the refusal and never writes it into a feature file.
- **Expected verdicts are the project's.** `--expect` only writes an ordinary `@expect-...` tag on the line.

## What is not built

- **No lemmas over the abstract operation.** The study's fifth part of a pack (derivations between rules, such as
  "VI-2 and VI-3 give exactly-when") is not here. Per-target proofs stay per target.
- **No applicability conditions.** The study's third part (kernel-checkable facts about the bindings, such as "the
  well-formed word is both satisfiable and refutable") is not built. On kvparse the grid shows both happen; nothing
  checks it for a new target.
- **The adequacy expectation is run as mutants of the target**, not as trivial Lean models. The suite adequacy note of
  the pipeline is computed from proved scenarios of the old glossary and does not look at Rule lines, so it says
  nothing about a pack suite.
- **No completeness line in the report.** `out/report.md` does not know about packs (by design: the pipeline does not
  read them). The line is printed by `pack instantiate` and `pack check` only. A reader of the report alone sees ten
  rules and no sign that an eleventh member is missing.
- **One operation per instantiation.** A second `parse` in the same project needs `--prefix` and its own bindings.

## The first target: `kvparse`

A toy byte-level parser (`kvparse/src/lib.rs`, 85 lines with comments): one or two `key=digit` fields separated by `;`,
keys `a` and `b`, each at most once and `a` first, with a size limit held by the parser. Declared in `projects.yaml`
like the counter. What it took outside its own files is listed in `validated-input/RESULTS.md`, section "Cost".

The words the slots are filled with are the project's own (`clausebook/local/kvparse.yaml`, `lean/Kvparse/Pieces.lean`).
Five of them hide a function written in the specification: `well-formed` (a second parser), `field of`, `key of` (a
tokeniser), `the encoding of the result` (an encoder), `the reference parse` (the whole answer). Every pack rule that
catches a seeded bug does so through one of these words. The pack supplies the sentence; the project supplies what
the sentence is about.

**The search is the project's too.** The pipeline examines a kvparse rule on 240 inputs written by the builder with
the pack's bug list in hand. Two mutants a reviewer wrote without that list leave the pipeline green. A wider search
on the compiled Rust (`wallet-bdd/tests/kv_wide.rs`, inputs taken from the format) is run beside the pipeline by
`validated-input/kvparse_mutants.py`; it gives no verdict. See `validated-input/RESULTS.md`, section 1.
