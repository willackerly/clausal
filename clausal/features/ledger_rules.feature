Feature: Ledger rules
  NEW SENTENCES about the ledger. No Rule line and no scenario in this file has an entry in the old
  whole-phrase glossary (glossary.yaml), a hand-written cucumber step or a hand-written Rust predicate.
  Each is compiled from the pieces of the Clausebook (clausebook/), runs on the compiled Rust through the one generic
  step, gets a flat proof obligation generated from the pieces (lean/Wallet/Obligations.lean), and reaches
  a verdict: PROVED-FOR-ALL where a proof of the obligation has been supplied, TESTED-ONLY where none has,
  REFUTED where the search finds an input at which it is false and the kernel confirms it.

  # ------------------------------------------------------------------ the README's own example
  # README.md: "Internal fund transfers never change aggregate account value", with a scenario of a transfer
  # between two accounts. Written here in the singular and with the ledger named, as the grammar asks; a transfer
  # is one value (sender->receiver:amount), so the README's three columns are one.
  @id:readme_internal_transfers
  Rule: An internal fund transfer never changes the total of the ledger's balances

    @id:readme_transfer_keeps_aggregate
    Scenario Outline: a transfer between two accounts of the ledger
      Given ledger Main holds the balances <balances>
      When the transfer <t> is applied to ledger Main
      Then the total of ledger Main's balances is unchanged

      Examples:
        | balances      | t        |
        | [100, 20, 0]  | 0->1:30  |
        | [100, 600]    | 1->0:500 |

  # ------------------------------------------------------------------ the five held-out rules (were heldout/new_rules.feature)
  @id:n1_internal_transfer
  Rule: An internal transfer never changes the total of the ledger's balances

  @id:n2_accepted_only_if_covered
  Rule: A transfer is accepted only if the amount of the transfer is at most the balance of account the sender of the transfer of the ledger

    @id:n2_short_sender_rejected
    Scenario Outline: a transfer of more than the sender holds is rejected and changes nothing
      Given ledger Main holds the balances <balances>
      And the amount of <t> is more than the balance of account the sender of <t> of ledger Main
      When the transfer <t> is applied to ledger Main
      Then it is rejected
      And ledger Main is unchanged

      Examples:
        | balances      | t         |
        | [100, 20, 0]  | 0->1:101  |
        | [5, 5]        | 1->0:6    |
        | [5, 5]        | 3->0:1    |

  @id:n3_lookup_missing_account
  Rule: For a lookup for which the account is not an account of the ledger, there is no result

  @id:n4_total_stays_within_maximum @expect-refuted
  Rule: A batch never leaves the total of the ledger's balances above the maximum
    Deliberately false: a batch conserves the total, and the total of a ledger can exceed the maximum to begin with.

    @id:n4_total_within_maximum_after_batch
    Scenario Outline: after a batch the total of all balances is within the maximum
      Given ledger Main holds the balances <balances>
      When the batch <batch> is applied to ledger Main
      Then the total of ledger Main's balances is afterwards at most the maximum

      Examples:
        | balances      | batch      |
        | [100, 20, 0]  | [0->1:30]  |
        | [5, 5]        | []         |

  @id:n5_stopped_at_invalid
  Rule: For a batch, no transfer at which the batch stopped is valid on the ledger afterwards

  # ------------------------------------------------------------------ the two-run and reference frames, each true once and false once
  # monotone ("more X never loses Q")
  @id:mono_smaller_amount
  Rule: A transfer never loses acceptance when the amount is the same or smaller

  @id:mono_larger_amount @expect-refuted
  Rule: A transfer never loses acceptance when the amount is the same or larger

  @id:mono_extended_ledger @expect-unproved
  Rule: A lookup never loses that there is a result when the ledger is extended
    True, and deliberately left WITHOUT a proof: its generated proof stub is still `sorry`
    (lean/Wallet/RuleProofs/ledger_rules/mono_extended_ledger.lean), so its verdict is TESTED-ONLY.

  # agrees with a reference
  @id:agrees_reference_lookup
  Rule: A lookup agrees with the reference lookup

  @id:agrees_zero_default @expect-refuted
  Rule: A lookup agrees with the zero-default lookup

  # independent of (two runs)
  @id:same_answer_at_account
  Rule: A lookup gives the same answer when the ledger agrees at the account

  @id:same_answer_any_amount @expect-refuted
  Rule: A transfer gives the same answer when only the amount differs

  # independent of, conditioned on the first run's answer
  @id:rejected_stays_rejected
  Rule: A transfer gives the same answer when the amount is the same or larger, if the first call is rejected

  @id:accepted_stays_accepted @expect-refuted
  Rule: A transfer gives the same answer when the amount is the same or larger, if the first call is accepted

  # containment between a collection of the input and a collection of the answer
  @id:stopped_is_of_batch
  Rule: For a batch, every transfer at which the batch stopped is a transfer of the batch

  @id:batch_is_stopped @expect-refuted
  Rule: For a batch, every transfer of the batch is a transfer at which the batch stopped

  # "some X of XS" as a condition
  @id:some_valid_conserves
  Rule: A batch for which some transfer of the batch is valid on the ledger never changes the total of the ledger's balances

  @id:some_invalid_rejected @expect-refuted
  Rule: A batch applied as a whole for which some transfer of the batch is not valid on the ledger is always rejected
    Deliberately false, and it sounds right: a transfer that cannot be carried out on the ledger as it starts
    can become possible after an earlier transfer of the same batch.

  # ------------------------------------------------------------------ the two candidate rules of the K2 trade map
  # compare/TRADES.md section 5: four mutants were shown false by no universal rule, and two rules were proposed for
  # them. Both are written here as "agrees with a reference", where the reference is another operation of the same code.
  @id:k2_whole_agrees_with_batch
  Rule: A batch applied as a whole agrees with the same batch applied transfer by transfer and kept only if every transfer is applied

  @id:k2_batch_agrees_with_transfers @expect-unproved
  Rule: A batch agrees with its transfers applied one at a time until one is rejected
    True as far as the property test and the bounded check can tell, and left WITHOUT a proof on purpose: it is the
    rule shown with property-test and bounded evidence only (no proof of its obligation has been supplied).

  # ------------------------------------------------------------------ a false rule the grid search does not find (plan node E1)
  # A negative control for the feed-back from the generated harnesses. The rule is false only of a ledger with at least
  # five accounts, and the reading search's grid of generated inputs has no ledger with more than four. The generated
  # property test finds one on the compiled Rust (and the generated bounded check does at the six-account rung of its
  # ladder, after verifying the rule at two and four accounts); the input is replayed on the Lean model and refuted in
  # the kernel.
  @id:e1_fifth_account_empty @expect-refuted
  Rule: A transfer never leaves the balance of account 4 of the ledger above zero

  # ------------------------------------------------------------------ false rules beyond "every call of one operation"
  @id:successful_changes_nothing @expect-refuted
  Rule: An accepted transfer never changes the ledger

  @id:rejected_empties_ledger @expect-refuted
  Rule: For a rejected transfer, the total of the ledger's balances is now zero

  @id:batch_then_total_always @expect-refuted
  Rule: A batch followed by a computation of the total is always accepted

  # ------------------------------------------------------------------ the remaining frames and pieces (were heldout/frames.feature)
  # Sentences that exercise the frames and pieces no other sentence reaches (if-then, rejected-and-unchanged, at least,
  # none-of, "no X of XS", a successful / rejected pair in one scenario), so that each has a compiled reading that is
  # evaluated on the Lean model and on the compiled Rust.
  @id:f_if_then
  Rule: A transfer is accepted whenever the transfer is valid on the ledger

  @id:f_rejected_unchanged
  Rule: A transfer for which the transfer is not valid on the ledger is rejected and changes nothing

  @id:f_result_at_least @expect-refuted
  Rule: For a batch, the number of transfers applied is at least the length of the batch

  @id:f_at_least
  Rule: A batch never leaves the total of the ledger's balances below zero

  @id:f_none_of
  Rule: For a batch, no transfer at which the batch stopped is valid on the ledger afterwards

  @id:f_no_valid_none_applied
  Rule: For a batch for which no transfer of the batch is valid on the ledger, the number of transfers applied is zero

  @id:f_scenario_level
  Rule: An accepted transfer never changes the total of the ledger's balances

    # a composition at scenario level that no old glossary phrase says: "the balance of account <k> ... is unchanged"
    @id:f_other_account_untouched
    Scenario Outline: A rejected transfer leaves every single balance as it was
      Given ledger Main holds the balances <balances>
      When the transfer <t> is applied to ledger Main
      Then if it is rejected, the balance of account <k> of ledger Main is unchanged
      And if it is accepted, the total of ledger Main's balances is unchanged

      Examples:
        | balances      | t        | k |
        | [100, 20, 0]  | 0->3:1   | 1 |
        | [100, 20, 0]  | 0->1:5   | 2 |

  # ------------------------------------------------------------------ plan node L2: three pieces the book lacked
  # Each piece has a sentence here that is true and one that is deliberately false (clausebook/l2/README.md).
  # (1) `equals`: a comparison of two values known before the call; its negation is "differs from"
  @id:l2_same_account_rejected
  Rule: A transfer for which the sender of the transfer equals the receiver of the transfer is rejected and changes nothing

  @id:l2_zero_amount_rejected @expect-refuted
  Rule: A transfer for which the amount of the transfer equals zero is always rejected
    Deliberately false: a transfer of nothing between two different accounts of the ledger is accepted.

  @id:l2_distinct_accounts_accepted @expect-refuted
  Rule: A transfer for which the sender of the transfer differs from the receiver of the transfer is always accepted
    Deliberately false: two different account numbers need not be accounts of the ledger, and the sender need
    not cover the amount.

  # (2) `each_at_most`: a bound on every number of a collection of the state, read after the call
  @id:l2_each_within_maximum
  Rule: For a transfer, each of the ledger's balances is afterwards at most the maximum
    True, and it says little beyond "a transfer always answers": a balance is a u64 and the maximum is the
    largest u64. It is here because it is the sentence the piece was asked for.

  @id:l2_each_within_total_bound
  Rule: For a transfer for which the total of the ledger's balances is at most the amount of the transfer, each of the ledger's balances is afterwards at most the amount of the transfer
    True, and it needs the code to conserve the total: no balance can pass a bound that the whole ledger was within.

  @id:l2_each_within_amount @expect-refuted
  Rule: For a transfer, each of the ledger's balances is afterwards at most the amount of the transfer
    Deliberately false: the same claim without its condition.

  # (3) `tied`: a sequence of two calls in which the second is given the first call's input ("with the same input")
  @id:l2_twice_conserves
  Rule: A transfer followed by a transfer with the same input never changes the total of the ledger's balances

  @id:l2_twice_changes_nothing @expect-refuted
  Rule: A transfer followed by a transfer with the same input never changes the ledger
    Deliberately false: the first of the two can be accepted.
