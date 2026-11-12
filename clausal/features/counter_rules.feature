Feature: Counter rules
  The third project (plan node X7): a bounded counter (counter/src/lib.rs), declared in projects.yaml. Three Rule lines,
  each compiled from the pieces of core and of the counter's local book (clausebook/local/counter.yaml) alone. The
  expected verdict of each was written down before the pipeline was run on them (counter/expected.json).

  # true for every input: a bump that is rejected returns before it writes
  @id:rejected_bump_unchanged
  Rule: A rejected bump never changes the counter's count

  # false: a bump that would pass 100 is rejected (a counter at 0 bumped by 101)
  @id:bump_always_accepted @expect-refuted
  Rule: A bump is always accepted

  # not a composition of pieces: no book this project lists has the word "resets"
  @id:bump_resets @expect-unbound
  Rule: A bump resets the counter
