Feature: Rule probe
  Does cucumber-rs run a Scenario Outline with Examples placed under a Rule?

  Background:
    Given Carol has a balance of 1

  @ruletag
  Rule: A covered withdrawal takes exactly the amount
    Free text under the rule line: the description.
    Second description line.

    @id:probe_outline
    Scenario Outline: covered withdrawal
      Given Alice has a balance of <a>
      And <amount> is not more than Alice's balance
      When Alice withdraws <amount>
      Then the operation succeeds
      And Alice's balance is decreased by <amount>

      Examples:
        | a  | amount |
        | 10 | 4      |
        | 7  | 7      |

    Scenario: literal under the same rule, deliberately failing
      Given Alice has a balance of 10
      When Alice withdraws 11
      Then the operation succeeds

  Rule: Second rule with its own background
    Background:
      Given Bob has a balance of 2

    Example: uses the Example keyword
      Given Alice has a balance of 3
      When Alice withdraws 3
      Then the operation succeeds
      And Bob's balance is unchanged

  # no rule
