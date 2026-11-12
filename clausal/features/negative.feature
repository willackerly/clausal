# @control: these scenarios get their verdicts like any other, but they are checks of the pipeline's own
# checks, not claims about the code, so they are left out of the suite adequacy note.
@control
Feature: Negative controls
  These exist to show the checks firing. None of them is a claim anyone
  should want to make about the wallet.

  # The two Givens about <amount> contradict each other, so the statement is
  # true of nothing. A proof of it would be worthless.
  @id:contradictory_givens @expect-vacuous
  Scenario Outline: A withdrawal that is both covered and not covered
    Given Alice's balance is <a>
    And <amount> is more than Alice's balance
    And <amount> is at most Alice's balance
    When Alice withdraws <amount>
    Then it is accepted

    Examples:
      | a | amount |
      | 5 | 6      |

  # True and provable, but the last Then says nothing about the code: Bob is not
  # touched by the call, so "unchanged" compares Bob with himself.
  @id:bystander_unchanged
  Scenario Outline: A deposit does not touch a bystander
    Given Alice's balance is <a>
    And Bob's balance is <b>
    And Alice's balance plus <amount> is at most the maximum
    When Alice deposits <amount>
    Then it is accepted
    And Bob's balance is unchanged

    Examples:
      | a | b | amount |
      | 1 | 2 | 3      |
