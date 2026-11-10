# NOT among the five new rules. These sentences exist to exercise the frames that no fixture sentence
# reaches (if-then, rejected-and-unchanged, at least, none-of, and a successful / rejected pair in a scenario),
# so that the definition of each is compared with its executable reading on generated inputs. They use
# existing pieces only; some are deliberately false.
Feature: Sentences that exercise the remaining frames

  @id:f_if_then
  Rule: A transfer is accepted whenever the transfer is valid on the ledger

  @id:f_rejected_unchanged
  Rule: A transfer for which the transfer is not valid on the ledger is rejected and changes nothing

  @id:f_result_at_least @expect-refuted
  Rule: For a batch, the number of transfers applied is at least the length of the batch

  @id:f_at_least
  Rule: A batch never leaves the total of all balances of the ledger below zero

  @id:f_none_of
  Rule: For a batch, no transfer at which the batch stopped is valid on the ledger afterwards

  @id:f_scenario_level
  Rule: A successful transfer never changes the total of all balances of the ledger

    # a NEW composition at scenario level: no old glossary phrase says "the balance of account <k> ... is unchanged"
    @id:f_other_account_untouched
    Scenario Outline: A rejected transfer leaves every single balance as it was
      Given ledger Main holds the balances <balances>
      When the transfer <t> is applied to ledger Main
      Then if it is rejected, the balance of account <k> of ledger Main is unchanged
      And if it is accepted, the total of ledger Main's balances is unchanged

      Examples:
        | balances      | t        | k |
        | [100, 20, 0]  | 0->3:1   | 1 |
