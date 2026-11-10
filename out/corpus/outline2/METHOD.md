# Definition-centred outline: method and measurements (plan node M2, 2026-11-10)

Status: built and measured; **not rated**. No person or model has rated a single entry yet. All figures below are computed from the Lean export and from text printed by Lean. The paper ground truth it is scored against is a model proxy's work (see `out/corpus/papers/TRUTH.md`).

Files: `OUTLINE2.md` (the outline), `outline2.json` (same, with full untruncated text), `metrics.json` (every number here), `rating_items.json` (60 entries for the blind rating), `lean/` (what Lean was asked and what it printed). Code: `bench/outline2.py`, `corpora/outline2/Outline2.lean`, `corpora/outline2/run.sh`.

## Result in brief

| | Navier-Stokes (`ns_r3`) | Euler (`euler_compact`) |
|---|---|---|
| chapters / statements / definitions printed | 14 + goal + closing / 58 / 103 | 14 + goal / 57 / 70 |
| paper items reached exactly, whole list (old outline) | 12 of 85 at 159 listed (8 at 69) | 7 of 31 at 125 listed (4 at 65) |
| ... at comparable length: concepts + statements only | 10 at 72 | 5 at 71 |
| ... at depth 50 (old outline at 50) | 8 (8) | 4 (4) |
| proof mass beneath the outline's statements (old, level 1) | 47.0% (56.5%) | 30.0% (32.5%) |
| ... beneath statements self-contained as printed | **28.0%** (12 statements) | **0.35%** (3 statements) |
| ... if nothing had been cut for display | 44.0% (19) | 7.0% (8) |
| ... self-contained and closed inside the outline | 4.8% (3) | 0% |
| old outline, same mechanical test / hand rating | 0% / about 10% | 0% / 0% |
| statement length, median characters (old outline) | 299 (982) | 863 (1,047) |
| definitions to read for the top level: unfolded + further named | 17 + 93 | 19 + 150 |

- **Navier-Stokes: by the builder's own (model, unrated) reading the chapter table reads as a strategy; mechanically, about a quarter of the proof sits behind statements whose named definitions are all printed on the page.** Six proxy readers later rated no more milestones than in the old outline (`RATINGS.md`). The chapter table gives a dependency chain read from the graph: profile (4) and clean cone (5) give the prepared profile (6); the moment patch (2) gives the prepared witness (7) and the assembly (8); these give the nominal witness (9), the profile data (10), the correction context and choice (11, 12), the stage estimates (13), the candidate witness (14) and the headline.
- **Euler: the chapter concepts are found, the statements stay unreadable.** Median statement 863 characters, 27 of 57 over 1,000, and almost every statement names definitions the outline does not print.
- **Against the paper, a small gain that the longer list explains in part.** At equal depth (50) the two outlines tie; at about 70 entries the new one is ahead by 2 items (Navier-Stokes) and 1 (Euler).
- **Unfolding one level does not close.** The concepts' own fields name 93 (Navier-Stokes) and 150 (Euler) further definitions; fully unfolding the top level still needs 2,688 and 1,550 definitions (old level 1: 2,880 and 2,024).

## Method, and what each step contributed

Graph, mass, dominators and spine are those of `bench/outline.py`. Parameters are at the top of `bench/outline2.py` and in `metrics.json`.

**Step 1. Chapters are concepts.**
- Candidates: structures, inductive types and Prop-valued definitions below the headline (595 in Navier-Stokes, 159 in Euler). Type-valued definitions such as `Plane := ℝ × ℝ` are notation: printed once in a glossary, never a chapter.
- From Lean, for every declaration: the head of each hypothesis, and what the conclusion produces, looking through `Nonempty`, `∃`, `∧`, subtypes and products (`lean/heads.jsonl`).
- A concept's region is everything dominated by a statement that produces it, plus the statements that take it as a hypothesis or use its chosen object.
- 14 concepts are chosen greedily. The proof is kept as a partition into cells; a candidate's gain is the unattributed mass it covers plus, for each existing cell, the smaller side of the cut it makes. A duplicate region gains nothing; a region nested in a chosen one is credited with the split.
- Each concept is printed by Lean one level deep: structure fields with their docstrings, constructors, or the defining clause.
- Contributed: 14 chapters whose regions hold 60.1% (Navier-Stokes) and 40.4% (Euler) of the proof mass. 11 and 7 of the 14 concepts have a docstring. Field docstrings are nearly absent: 0 of 103 fields in Navier-Stokes, 15 of 141 in Euler. Printing the concepts alone moves the self-contained share from 0% to 23.2% (Navier-Stokes) and 0.04% (Euler).

**Step 2. Construction and consumers, printed relative to the concept.**
- Construction: the producer with the most proof beneath it; if that is a definition, also the heaviest theorem producer.
- Consumers: statements with the concept as a hypothesis, or using its chosen object, by proof mass beneath them. A statement is shown once, under the later chapter.
- Four statements per chapter. Binders that two or more statements of a chapter share are declared once; each statement prints only what it adds. Lean prints every name relative to the chapter's namespace.
- Up to three definitions named by a chapter's statements are also unfolded (six for the goal), chosen by how many of the chapter's statements name them; notation named anywhere is printed in the glossary.
- Contributed: 15 construction and 38 consumer statements (Navier-Stokes), 15 and 41 (Euler). Sharing binders removes 14.4% and 21.9% of statement characters; relative names and shared binders together take the median from 490 to 299 characters (Navier-Stokes) and 1,422 to 863 (Euler) on the same statements. Notation adds 4.8 points of self-contained mass in Navier-Stokes; the 47 supporting definitions add 2 statements and no mass there, and take Euler from 0.04% to 0.35%.

**Step 3. Order and labels.**
- Chapters are ordered by the dependency height of their constructing statement, so no chapter's construction depends on a later one. "Builds on" is the transitive reduction of reachability between constructing statements.
- Labels are the first sentence of the declaration's docstring, read from the environment; otherwise "undocumented". 34 of 58 statements have one in Navier-Stokes, 21 of 57 in Euler.
- Contributed: the strategy table at the top of each outline. In Euler the order is flatter: eight of the 14 chapters build on no other (five in Navier-Stokes).

**Step 4. Size.** 14 concept chapters plus the goal and, for Navier-Stokes, the closing chain of four statements; 58 and 57 statements. The file is long (234 KB) because 173 definitions are printed with it.

## Measurements

**Paper ground truth** (`bench/paper_truth.py`; cell = exact / near; any confidence; "probable or better" gives the same exact counts, 12 of 79 and 7 of 31).

| Navier-Stokes, 85 items (53 have a target below the headline) | listed | k=20 | k=50 | k=100 | all |
|---|---|---|---|---|---|
| definition-centred outline | 159 | 6 / 27 | 8 / 44 | 11 / 51 | 12 / 64 |
| ... concepts, construction, other statements (cumulative) | 14, 29, 72 | | | | 2 / 42, 3 / 42, 10 / 46 |
| dominator outline | 69 | 6 / 20 | 8 / 49 | | 8 / 56 |
| random declarations, same length (mean of 200) | 159 | | | | 1.0 / 23.25 |

| Euler, 31 items (29 below the headline) | listed | k=20 | k=50 | k=100 | all |
|---|---|---|---|---|---|
| definition-centred outline | 125 | 3 / 16 | 4 / 18 | 7 / 24 | 7 / 26 |
| ... concepts, construction, other statements (cumulative) | 14, 29, 71 | | | | 3 / 22, 3 / 23, 5 / 24 |
| dominator outline | 65 | 1 / 14 | 4 / 27 | | 4 / 27 |
| random declarations, same length (mean of 200) | 125 | | | | 0.7 / 15.8 |

- Items only the new outline reaches: Navier-Stokes 4.6, 4.9, 4.10, 8.1, 9.4, B.9, C.2; Euler (1.2), (2.2), (2.8), (3.11), 3.1. Only the old one: Navier-Stokes 9.6, 10.5, A.4; Euler 4.1, 4.1(1).
- **Two cuts that remove the gain.** Counting only `states` and `part` mappings (dropping the 60 `defines` mappings, which only an outline that prints definitions can reach): Navier-Stokes 10 of 79 (dominator outline 8), Euler 2 of 27 (dominator outline 3); four of the five Euler items only the new outline reaches are definitions. At `--min-confidence certain` both outlines reach 1 item in each paper.
- The other baselines in `out/corpus/papers/BASELINES.md` at k=100: own proof size 10 (Navier-Stokes) and 4 (Euler); docstring ordered by mass beneath 9 and 3. The outline's 11 and 7 at k=100 are at or above those.

**Self-contained after one level of unfolding.** A statement counts when every project definition visible in its printed text is printed in full somewhere in the outline, and the statement itself is not cut. "Beneath" is the union of what the counted statements dominate; the headline and closing chain are left out, since everything is beneath them.
- Navier-Stokes 28.0%, of which 23.2 points sit beneath one construction, `profileData_nonempty` and the object chosen from it. `selected_witness` (13.8%) does not count because its concept's 2,600-character defining clause is cut at 700.
- "Closed" asks in addition that the printed definitions name only printed definitions: 3 statements, 4.8%.
- The old outline prints no definitions, so by the same test it scores 0%. Its "about 10%" was a hand rating of readability, a different yardstick; the two are shown side by side, not as a like-for-like gain.

**Definitions to follow the top level** (headline, 14 concepts unfolded, first construction statement of each chapter): 17 unfolded and 93 further named, 24 of them printed elsewhere in the outline (Navier-Stokes); 19 and 150, 34 printed (Euler). The old outline's statements named 369 and 252 project declarations directly.

## Rating items

`rating_items.json`: 60 entries, 15 per outline per paper, drawn by `random.Random(20261110)` from all eligible entries and shuffled by the same generator; the rule is recorded in the file. `text` is what a rater sees; `hidden` names the source and must be stripped. `textStatementOnly` is the same entry without chapter context, for a second arm.

The two outlines are shown as each displays itself, so trimming differs: old entries show the statement with whitespace collapsed, cut at 420 characters, with no docstring (166 to 530 characters); new entries keep Lean's layout, cut the statement at 900 characters, add chapter context with no cap (723 to 7,338 characters) and carry corpus docstrings in 23 of 30 entries. `textStatementOnly` keeps the 900 and 420 caps, so it isolates the context within the new outline but is not like-for-like across outlines.

## Limits

- **Not blind to format.** New entries carry a context block and are mostly several times longer than old ones (up to 7,300 characters against about 500); a rater can tell the outlines apart.
- **The self-contained figure depends on display cuts** (fields 300, clauses 700, statements 900 characters) and on one heavy statement. The uncut figure is given beside it.
- **"Visible" is a token test**: a constant of the printed expression counts when its last name component appears in the printed text. A binder named like a definition would be miscounted.
- **Parameters were fixed before the scorer was first run**, with no version control to prove it; after the scores were seen only reporting fields were added, and `--no-lean` refuses to run if the selection differs from the one Lean printed.
- **Consumers are ranked by proof mass beneath them**, which favours long technical statements; 15 of 58 and 28 of 57 statements are cut for display.
- **Three near-coincident regions are all chapters** in Navier-Stokes (profile, nominal witness, profile data: about 27% each); the greedy rule credits their distinct consumers.
- Inductive indices print with Lean's anonymous binder name (`a`), and a cut constructor loses its indentation.
- Euler was built from the compact-support headline to match the baselines; the earlier outline's printed Euler section used the other root.

## Reproduce

```sh
export PATH="$HOME/.elan/bin:$PATH"
corpora/outline2/run.sh heads out/corpus/outline2/lean/names_all.txt out/corpus/outline2/lean/heads.jsonl   # 16 s
python3 bench/outline2.py --test
python3 bench/outline2.py             # 7 Lean cold starts, about 2 minutes; --no-lean reuses lean/printed_*.jsonl
python3 bench/paper_truth.py --outline out/corpus/outline2/outline2.json --key ns_r3
```

## Next actions

1. Run the blind rating on `rating_items.json` with at least two readers, and the statement-only arm, with a rubric written first.
2. Euler: choose consumers by statement length as well as mass, or print the paper's sentence beside the three heaviest, and re-measure.
3. Print long defining clauses (the candidate `Witness`) as a list of conjuncts so they are not cut; this alone would add 13.8 points to the Navier-Stokes self-contained share.
4. Unfold a second level for the 24 to 34 definitions already printed elsewhere and report how fast the closure shrinks.
