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
#
# Do not edit a line to make a check pass: if a refusal stops being provable, or a line that must compile is refused,
# that is the finding.
Feature: Narrowing controls

  # ---- Q1: the four sentences of the readability critique, section 2.1. Each reads like a rule the fixtures expect to be
  #      refuted (features/ledger_rules.feature), and each holds of any code at all.
  @says-nothing:monotone_holds @id:q1_never_loses_acceptance
  Rule: A successful transfer never loses acceptance when the amount is larger

  @says-nothing:independentOf @id:q1_same_answer_successful
  Rule: A successful transfer gives the same answer when the amount is larger

  @says-nothing:independentOf @id:q1_same_answer_rejected
  Rule: A rejected transfer gives the same answer when only the amount differs

  @says-nothing:monotone_fails @id:q1_never_loses_rejection
  Rule: A successful transfer never loses that it is rejected when the amount is smaller

  # ---- Q1: one line for each remaining reason the compiler can give
  @says-nothing:covers_no_call @id:q1_no_rejected_batch
  Rule: For a batch, if it is rejected, the number of transfers applied is zero

  @says-nothing:alwaysAnswers @id:q1_always_answers
  Rule: A successful lookup always answers

  @says-nothing:always @id:q1_always
  Rule: For a successful lookup, there is a result

  @says-nothing:never @id:q1_never
  Rule: For a rejected lookup, there is no result

  @says-nothing:ifThen @id:q1_if_then
  Rule: A successful withdrawal is accepted whenever the amount is not more than the wallet's balance

  @says-nothing:onlyIf @id:q1_only_if
  Rule: A rejected withdrawal is accepted only if the amount is not more than the wallet's balance

  @says-nothing:independentGiven_fails @id:q1_same_answer_if_fails
  Rule: A successful transfer gives the same answer when the amount is larger, if it is rejected

  @says-nothing:independentGiven_view @id:q1_same_answer_if_view
  Rule: A successful transfer gives the same answer when the amount is larger, if it is accepted

  # ---- Q2: the two shapes of the critique, section 2.2, whose printed coverage contradicted the Lean.
  #      First shape: the narrowing is written on the claim ("if it is ..."), not on the subject.
  @covers:accepted @id:q2_claim_narrowed_accepted
  Rule: For a lookup, if it is accepted, the result is the balance of the account in the ledger

  @covers:rejected @id:q2_claim_narrowed_rejected
  Rule: For a transfer, if it is rejected, the ledger is unchanged

  #      Second shape: a narrowed rule that compares two calls (and says something: two lookups that both find a balance
  #      need not find the same one). It must not print that both calls must give an answer.
  @covers:accepted @id:q2_two_calls_narrowed
  Rule: A successful lookup gives the same answer when the ledger is extended

  # ---- Q1, the other direction: narrowed lines that SAY SOMETHING must still compile
  @covers:accepted @id:q1_keeps_exactly_when
  Rule: A successful withdrawal is accepted exactly when the amount is not more than the wallet's balance

  @covers:rejected @id:q1_keeps_state_claim
  Rule: A rejected withdrawal never changes the wallet's balance
