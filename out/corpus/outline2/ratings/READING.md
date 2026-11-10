## Reading (hand-written, 2026-11-10, against six proxy readers and no human)

This section is not regenerated. If reader files are added, check it against the tables above before relying on it.

**What was measured**

- **No more milestones.** Share rated milestone: 8.3% old, 6.7% new; difference -1.7 points, interval -15.0 to +11.7. The new outline did not surface more nameable steps in this sample.
- **Fewer opaque, many more unreadable.** Opaque fell from 83.3% to 17.2% (difference -66.1 points, interval -82.2 to -47.8). Unreadable rose from 1.1% to 48.3% (+47.2, interval +25.0 to +70.0). Both intervals exclude zero.
- **Net change in opaque-or-unreadable is unclear.** 84.4% old, 65.6% new; difference -18.9 points, interval -43.3 to +4.4 when readers and entries are both resampled. It excludes zero only if readers are held fixed (-35.0 to -2.2) or entries are held fixed (-33.9 to -1.1).
- **The gain is in technical steps.** 7.2% old, 27.8% new (+20.6, interval +2.2 to +40.6). Model readers labelled more new entries technical-step; this arm cannot say whether the printed definitions, the corpus docstrings in the context (23 of 30 new entries, 0 of 30 old) or the extra text did it, and none became a milestone.
- **Euler is worse than Navier-Stokes in the new outline.** 61.1% unreadable against 35.6%, consistent with the 0.35% self-contained figure in `METHOD.md`.

**Reader noise**

- **Readers agree on the old outline and not on the new.** Fleiss' kappa 0.78 old, 0.36 new; 26 of 30 old entries unanimous, 9 of 30 new; 18 of 30 new entries had readers on both sides of the readable line, 1 of 30 old.
- **The net result depends on the model.** Opaque-or-unreadable, new minus old: default -38.3, opus -25.0, sonnet +6.7. The two sonnet readers rated 22 and 28 of 30 new entries unreadable; the other four rated 9 or 10.
- **Same-model copies agree more (mean kappa 0.82) than different models (0.59)**, so six readers are closer to three, or to two: the four default-opus pairs agree almost as well (mean kappa 0.76) as copies of one model, and the default model's identity was not recorded.
- **Some sonnet reasons describe the context block, not the statement.** Example: R22 is the Euler headline (`initialDatum_no_global_solution`). Five readers rated it milestone; sonnet-2 rated it unreadable with the reason "a mix of several definitions ... in one block". The same declaration in the old format (R49) was milestone for all six. Whether that is a reading failure or a fair reaction to 2,000 characters of unrelated context before a one-line theorem cannot be settled with model readers.
- **The most contested entries are the Navier-Stokes cone-assembly chapter** (R04, R11, R23, R44, R16, R48, R50, R39): the statement is short, the unfolded structure is printed, and its fields rest on predicates that are not printed. Readers split on whether one level of unfolding is enough.

**Trades**

- The old outline fails in one way (statement cut at 420 characters, names undefined): readers agree it is opaque.
- The new outline trades that for length: median 2,480 characters shown against 498. Where the context is relevant and short, entries become technical steps; where it is long or unrelated, readers who weigh the whole block call it unreadable.
- Format confound: the two effects (definitions shown, more text shown) cannot be separated in this arm, and readers could tell the formats apart.

**Next actions**

1. Run the statement-only arm (`textStatementOnly`, already in `rating_items.json`) with the same readers. It separates "the statement is long" from "the context is long".
2. Get one mathematician's ratings on the 60 entries (or the 18 split ones first) as `ratings/<name>.json` with `"kind": "human"`. The milestone column means little until then.
3. For the outline itself: print only the context a statement uses (R22 and R60 show unrelated context costing a reading), and unfold a second level for the cone-assembly predicates (`IsTrue`, `IsRelaxed`, `ProfileCleanCone`), which is where readers split.
4. Tighten the rubric on one point before the next run: say whether the label is for the target statement given the context, or for the whole block. The sonnet readers appear to have used the second reading.
