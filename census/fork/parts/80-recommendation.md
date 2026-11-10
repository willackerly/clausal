## Recommendation: fork or upstream, as a trade

**What each route buys and costs.**

| | carry a fork | upstream only |
|:--|:--|:--|
| Gain on this corpus | immediate: {{B_OK}} to {{F_OK}} functions as shipped ({{B_PCT}} to {{F_PCT}}); nine crates {{B9_PCT}} to {{F9_PCT}} | the same, on the day the fixes are merged and released; not before, and the date is not ours |
| Cost to obtain | done: five commits, about 300 lines, `patches/0001…0005` | five issue texts (written, in `upstream/`, not sent), and probably pull requests: the maintainers may want (ii) and (iv) done differently |
| Cost to keep | a rebase each time the pinned Aeneas moves; a source build (opam, OCaml 5.3, 40 s) on every machine and in CI instead of a release tarball; we own the patches' correctness | none |
| Coupling | inherits the release's coupling: one Charon commit, one Rust nightly, one Lean and Mathlib pin per Aeneas commit | same coupling, handled upstream |
| Risk | drift if the fork accumulates; the soundness check behind it is 25 small functions | upstream declines or redesigns a patch and the gain for that part never arrives in this form |

**Facts that bear on it.**

- **The patches are small and local.** (i) is one recursive call. (ii) and (iii) add handlers next to handlers that already exist, in the style of the surrounding code. (iv) is the only one with a design choice in it (when to qualify a builtin name).
- **Rebase cost so far.** Between the two releases the census used (one day apart) the only source change was three lines in a keyword list; the five commits apply to both (checked with `git am`). Aeneas does move fast (a release every night), but the fork only has to follow the releases this project pins, not every night's.
- **Upstream's test outputs do not move**, apart from two line numbers. That makes the patches cheap to review and cheap to carry.
- **The fork does not fix cedar.** As shipped cedar is still 0, because of Charon. With the Charon workarounds the patches turn "no output" into a large Lean file (one measurement, with (i)-(iv); the effect of (v) on cedar was not measured), and what is left is feature work (mixed groups, function items, trait objects), not robustness. A fork that goes after those is a different, much larger commitment than these five commits.
- **Nothing here is private.** All five are defects any user of Aeneas on a real crate will hit; upstream has an interest in them. The issue texts in `upstream/` come with reproductions of 10 to 70 lines, except the formatter one, which has none.

**Recommendation.** Do both, in this order, and keep the fork thin.

1. **Use the fork now** for the census, the profile and plan node S1: it is what makes five of the ten crates usable at all, with no manual peeling. Pin it as "release X plus `patches/`", applied by script, so that the fork is five files and not a diverging repository.
2. **Send issues 1, 2, 3 and 5 first** (mixed-group recursion, method-signature abort, uncaught exceptions, formatter reset). They are bug reports with one-file reproductions and small fixes; if upstream merges them, four of the five commits disappear at the next pin.
3. **Send issue 4 as a question plus a patch** (name capture): upstream may prefer always-qualified builtins or a different renaming rule. Carry our version until they decide.
4. **Do not grow the fork into feature work** (mixed groups proper, function items, `dyn`) without a separate decision. Those are weeks to months, they touch Aeneas's core, and they are where being upstream matters most.

**The trade in one line:** the fork costs a source build and a rebase per pin and buys {{GAIN}} functions today; upstreaming costs five reports, already written, and an unknown wait and removes the carrying cost for good. The two are not alternatives unless upstream declines.

**Sending is the owner's step.** Nothing was posted, no issue or pull request was opened, and nothing was pushed (the clone's push URL is disabled).
