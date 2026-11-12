# CONTROLS for narrowed Rule lines (plan nodes Q1 and Q2). NOT part of the regression set (features/): these lines get no
# verdict, no proof and no Rust run. `clausal gen` compiles each one twice, with and without the refusal of plan node Q1,
# and lean/Run/Narrowing.lean puts the questions below to the kernel on every run; `clausal narrowing` reads the answers
# and fails the run if one is wrong. The same lines are checked without Lean by `python3 -m clausal.selftest`.
#
#   @says-nothing:<theorem>   the compiler must REFUSE the line (status SAYS-NOTHING) and name that theorem of
#                             lean/Frames/Narrowing.lean. Compiled without the refusal, the statement "for every `run`,
#                             the claim holds" must be kernel-checked through that theorem, and found by the fixed tactic.
#   @covers:<calls>           the line must COMPILE; every claim of it must be about those calls according to Lean, and the
#                             coverage it prints must be the coverage the book gives for them. The fixed tactic must FAIL
#                             to prove its narrowed claims for every `run` (they say something).
#   @narrowed-twice           the line narrows or scopes ONE clause with more than one word (two of accepted / rejected on the
#                             subject, or `internal` BEFORE one of them; a narrowed subject and "if it is ..." on its claim; two
#                             "if it is ...").
#                             The compiler must REFUSE it (code NARROWED-TWICE), with the Q1 refusal on and off: a word is
#                             never dropped and never overrides another.
#
# Do not edit a line to make a check pass: if a refusal stops being provable, or a line that must compile is refused,
# that is the finding.
#
# REWORDED by plan node Q4 (clausebook/q4/FREEZE.md), form for form: "successful" is "accepted", "is not more than" is
# "is at most", "the amount is larger" is "the amount is the same or larger", ", if it is rejected" of frame 16 is
# ", if the first call is rejected", "the total of all balances of the ledger" is "the total of the ledger's balances".
# Every line compiles to the Lean statement it compiled to before, or is refused with the status and code it was refused
# with (clausebook/terms.lock.json was NOT rewritten for these lines; `clausal book check` compares). Four lines changed
# SHAPE, because a Rule line now narrows on its subject only and says each frame in one voice:
#   q1_no_rejected_batch, q2_claim_narrowed_accepted, q2_claim_narrowed_rejected   "for X, if it is ..., C" is "for a ... X, C"
#       (or "a ... X <verb phrase>"). The shape these lines were written for, a narrowing before the claim, is now
#       refused in a Rule line (RETIRED-FORM); the selftest holds its controls. It is still read before a Then step.
#   q2_internal_narrowed_on_claim   "for an internal transfer, if it is accepted, C" is "an accepted internal transfer ...":
#       the one pair of words a subject takes, in that order. The two lines above it (q2_twice_successful_internal,
#       q2_twice_rejected_internal) are now written in the OTHER order, which is refused as before.
Feature: Narrowing controls

  # ---- Q1: the four sentences of the readability critique, section 2.1. Each reads like a rule the fixtures expect to be
  #      refuted (features/ledger_rules.feature), and each holds of any code at all.
  @says-nothing:monotone_holds @id:q1_never_loses_acceptance
  Rule: An accepted transfer never loses acceptance when the amount is the same or larger

  @says-nothing:independentOf @id:q1_same_answer_successful
  Rule: An accepted transfer gives the same answer when the amount is the same or larger

  @says-nothing:independentOf @id:q1_same_answer_rejected
  Rule: A rejected transfer gives the same answer when only the amount differs

  @says-nothing:monotone_fails @id:q1_never_loses_rejection
  Rule: An accepted transfer never loses that it is rejected when the amount is the same or smaller

  # ---- Q1: one line for each remaining reason the compiler can give
  @says-nothing:covers_no_call @id:q1_no_rejected_batch
  Rule: For a rejected batch, the number of transfers applied is zero

  @says-nothing:alwaysAnswers @id:q1_always_answers
  Rule: An accepted lookup always answers

  @says-nothing:always @id:q1_always
  Rule: For an accepted lookup, there is a result

  @says-nothing:never @id:q1_never
  Rule: For a rejected lookup, there is no result

  @says-nothing:ifThen @id:q1_if_then
  Rule: An accepted withdrawal is accepted whenever the amount is at most the wallet's balance

  @says-nothing:onlyIf @id:q1_only_if
  Rule: A rejected withdrawal is accepted only if the amount is at most the wallet's balance

  @says-nothing:independentGiven_fails @id:q1_same_answer_if_fails
  Rule: An accepted transfer gives the same answer when the amount is the same or larger, if the first call is rejected

  @says-nothing:independentGiven_view @id:q1_same_answer_if_view
  Rule: An accepted transfer gives the same answer when the amount is the same or larger, if the first call is accepted

  # ---- Q2: the two shapes of the critique, section 2.2, whose printed coverage contradicted the Lean.
  #      First shape: the narrowing was written on the claim ("for a lookup, if it is accepted, ..."), not on the subject.
  #      After Q4 a Rule line cannot be written that way; the two lines are the same statements, narrowed on the subject.
  @covers:accepted @id:q2_claim_narrowed_accepted
  Rule: For an accepted lookup, the result is the balance of the account in the ledger

  @covers:rejected @id:q2_claim_narrowed_rejected
  Rule: A rejected transfer never changes the ledger

  #      Second shape: a narrowed rule that compares two calls (and says something: two lookups that both find a balance
  #      need not find the same one). It must not print that both calls must give an answer.
  @covers:accepted @id:q2_two_calls_narrowed
  Rule: An accepted lookup gives the same answer when the ledger is extended

  # ---- Q1, the other direction: narrowed lines that SAY SOMETHING must still compile
  @covers:accepted @id:q1_keeps_exactly_when
  Rule: An accepted withdrawal is accepted exactly when the amount is at most the wallet's balance

  @covers:rejected @id:q1_keeps_state_claim
  Rule: A rejected withdrawal never changes the wallet's balance

  # ---- Q2, third shape (review of Q1/Q2): a narrowed clause about a SEQUENCE. It must not print that every call in the
  #      sequence must answer: under a narrowing no call has to, and a sequence in which one gives no answer is not covered.
  @covers:accepted @id:q2_sequence_narrowed_accepted
  Rule: An accepted batch followed by a computation of the total is accepted exactly when the total of the ledger's balances is at most the maximum

  @covers:rejected @id:q2_sequence_narrowed_rejected
  Rule: A rejected batch followed by a computation of the total is accepted exactly when the total of the ledger's balances is at most the maximum

  # ---- Q2 (review of Q1/Q2): a clause narrowed or scoped by more than one word. Before, the second word silently replaced
  #      the first ("a successful internal transfer" was compiled as every internal transfer) or the last narrowing won
  #      ("for a successful transfer, if it is rejected" was compiled as rejected calls). Each is refused.
  #      (After Q4: `internal` after ONE narrowing word is read, and compiles to both; before it, it is refused.)
  @narrowed-twice @id:q2_twice_successful_internal
  Rule: An internal accepted transfer never changes the total of the ledger's balances

  @narrowed-twice @id:q2_twice_rejected_internal
  Rule: An internal rejected transfer never changes the total of the ledger's balances

  @narrowed-twice @id:q2_twice_successful_rejected
  Rule: An accepted rejected transfer never changes the total of the ledger's balances

  @narrowed-twice @id:q2_twice_subject_and_claim
  Rule: For an accepted transfer, if it is rejected, the ledger is unchanged

  @narrowed-twice @id:q2_twice_subject_and_claim_same
  Rule: For a rejected transfer, if it is rejected, the ledger is unchanged

  @narrowed-twice @id:q2_twice_on_the_claim
  Rule: For a transfer, if it is rejected, if it is accepted, the ledger is unchanged

  #      ... and the one way to say it that the book has: one narrowing word, then `internal`, on the subject
  @covers:accepted @id:q2_internal_narrowed_on_claim
  Rule: An accepted internal transfer never changes the total of the ledger's balances
