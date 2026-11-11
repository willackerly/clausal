# Reviewer's sentences (step-3 independent check, 2026-11-11), written before reading
# features/ledger_rules.feature. First draft as written; any rewording needed to compile is
# recorded in slice/review/step3/attempts.txt, not made silently here.
Feature: Reviewer sentences
  Three claims about the ledger, written by the reviewer.

  # T: meant TRUE. A batch whose transfers are all invalid on the ledger is stopped at its first
  # transfer (or is empty), so nothing changes.
  @id:rv_no_valid_batch_unchanged
  Rule: A batch for which no transfer of the batch is valid on the ledger never changes the ledger

    @id:rv_no_valid_batch_unchanged_ex
    Scenario Outline: A batch with no valid transfer leaves the ledger as it was
      Given ledger Main holds the balances <balances>
      And no transfer of <batch> is valid on ledger Main
      When the batch <batch> is applied to ledger Main
      Then ledger Main is unchanged
      And the number of transfers applied is zero

      Examples:
        | balances   | batch               |
        | [5, 0]     | [0->1:6, 1->0:1]    |
        | [3, 4]     | []                  |
        | [7]        | [0->0:1]            |
        | [2, 2, 2]  | [0->3:1, 1->1:1]    |

  # F: meant FALSE. Every transfer being valid on the ledger BEFORE the batch does not make the whole
  # batch go through: two transfers that each fit the starting balance can overdraw together.
  @id:rv_all_valid_whole_accepted @expect-refuted
  Rule: A batch applied as a whole for which every transfer of the batch is valid on the ledger is always accepted

    @id:rv_all_valid_whole_accepted_ex @expect-refuted
    Scenario Outline: A batch of valid transfers applied as a whole is accepted
      Given ledger Main holds the balances <balances>
      And every transfer of <batch> is valid on ledger Main
      When the batch <batch> is applied to ledger Main as a whole
      Then it is accepted

      Examples:
        | balances   | batch               |
        | [10, 0]    | [0->1:3, 0->1:4]    |
        | [5, 5]     | [0->1:5, 1->0:2]    |

  # R: two-run, meant TRUE. Adding accounts at the end of a ledger does not change what a lookup
  # of an existing account returns.
  @id:rv_lookup_extended_same
  Rule: A lookup gives the same answer when the ledger is extended, if there is a result
