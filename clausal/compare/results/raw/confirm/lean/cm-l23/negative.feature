Feature: Negative controls
  These exist to show the checks firing. None of them is a claim anyone
  should want to make about the wallet.

  # The two Givens about <amount> contradict each other, so the statement is
  # true of nothing. A proof of it would be worthless.
  @id:contradictory_givens @expect-vacuous
  Scenario Outline: A withdrawal that is both covered and not covered
    Given Alice has a balance of <a>
    And <amount> is more than Alice's balance
    And <amount> is not more than Alice's balance
    When Alice withdraws <amount>
    Then the operation succeeds

    Examples:
      | a | amount |
      | 5 | 6      |

  # True and provable, but the last Then says nothing about the code: Bob is not
  # touched by the call, so "unchanged" compares Bob with himself.
  @id:bystander_unchanged
  Scenario Outline: A deposit does not touch a bystander
    Given Alice has a balance of <a>
    And Bob has a balance of <b>
    And Alice's balance plus <amount> does not exceed the maximum
    When Alice deposits <amount>
    Then the operation succeeds
    And Bob's balance is unchanged

    Examples:
      | a | b | amount |
      | 1 | 2 | 3      |
