Feature: Wallet
  Wallets hold an unsigned 64-bit balance. Money can be deposited, withdrawn
  and transferred; an operation that cannot be carried out exactly is rejected
  and leaves every balance as it was.

  Each Rule line is one claim, written with the words of vocabulary.yaml, and is compiled
  to one Lean statement that covers every input. The scenarios beneath it are its tested
  instances and, where they are outlines, its parts: the rule statement is proved from them.
  The free text under a rule line is carried into the report as written.

  @id:transfer_total
  Rule: A transfer never changes the total of all balances
    Every transfer falls under one of three cases. Covered, and the receiver has room: it must
    succeed and move exactly the amount (the progress scenario). The sender is short, or the
    receiver has no room: it is rejected and neither balance moves.

    @id:transfer_conserves
    Scenario Outline: A covered transfer moves the money and conserves the total
      Given Alice has a balance of <a>
      And Bob has a balance of <b>
      And <amount> is not more than Alice's balance
      And Bob's balance plus <amount> does not exceed the maximum
      When Alice transfers <amount> to Bob
      Then the operation succeeds
      And Alice's balance is decreased by <amount>
      And Bob's balance is increased by <amount>
      And the total of all balances is unchanged

      Examples:
        | a   | b  | amount |
        | 100 | 20 | 30     |
        | 5   | 0  | 5      |

    @id:transfer_short
    Scenario Outline: Transferring more than the sender has is rejected and changes nothing
      Given Alice has a balance of <a>
      And Bob has a balance of <b>
      And <amount> is more than Alice's balance
      When Alice transfers <amount> to Bob
      Then the operation is rejected with insufficient funds
      And Alice's balance is unchanged
      And Bob's balance is unchanged

      Examples:
        | a  | b | amount |
        | 10 | 7 | 11     |
        | 0  | 0 | 1      |

    @id:transfer_no_room
    Scenario Outline: A transfer the receiver has no room for is rejected and changes nothing
      Given Alice has a balance of <a>
      And Bob has a balance of <b>
      And <amount> is not more than Alice's balance
      And Bob's balance plus <amount> exceeds the maximum
      When Alice transfers <amount> to Bob
      Then the operation is rejected with overflow
      And Alice's balance is unchanged
      And Bob's balance is unchanged

      Examples:
        | a | b                    | amount |
        | 1 | 18446744073709551615 | 1      |
        | 9 | 18446744073709551610 | 6      |

    @id:transfer_short_example
    Scenario: Transferring more than you have is rejected and changes nothing
      Given Alice has a balance of 10
      And Bob has a balance of 7
      When Alice transfers 11 to Bob
      Then the operation is rejected with insufficient funds
      And Alice's balance is unchanged
      And Bob's balance is unchanged

  @id:withdrawal
  Rule: A withdrawal always answers, and a successful withdrawal decreases the wallet's balance by exactly the amount, and a rejected withdrawal never changes the wallet's balance

    @id:withdraw_covered
    Scenario Outline: A covered withdrawal succeeds and takes exactly the amount
      Given Alice has a balance of <a>
      And <amount> is not more than Alice's balance
      When Alice withdraws <amount>
      Then the operation succeeds
      And Alice's balance is decreased by <amount>

      Examples:
        | a  | amount |
        | 10 | 4      |
        | 7  | 7      |
        | 0  | 0      |

    @id:withdraw_too_much
    Scenario Outline: Withdrawing more than the balance is rejected and changes nothing
      Given Alice has a balance of <a>
      And <amount> is more than Alice's balance
      When Alice withdraws <amount>
      Then the operation is rejected with insufficient funds
      And Alice's balance is unchanged

      Examples:
        | a  | amount |
        | 10 | 11     |
        | 0  | 1      |

  @id:deposit
  Rule: A deposit always answers, and a successful deposit increases the wallet's balance by exactly the amount, and a rejected deposit never changes the wallet's balance

    @id:deposit_with_room
    Scenario Outline: A deposit with room succeeds and adds exactly the amount
      Given Alice has a balance of <a>
      And Alice's balance plus <amount> does not exceed the maximum
      When Alice deposits <amount>
      Then the operation succeeds
      And Alice's balance is increased by <amount>

      Examples:
        | a                    | amount               |
        | 1                    | 2                    |
        | 18446744073709551615 | 0                    |
        | 0                    | 18446744073709551615 |

    @id:deposit_overflow
    Scenario Outline: A deposit that would overflow is rejected and changes nothing
      Given Alice has a balance of <a>
      And Alice's balance plus <amount> exceeds the maximum
      When Alice deposits <amount>
      Then the operation is rejected with overflow
      And Alice's balance is unchanged

      Examples:
        | a                    | amount |
        | 18446744073709551615 | 1      |
        | 18446744073709551000 | 616    |

  @expect-refuted @id:transfer_affordable
  Rule: A transfer for which the amount is not more than the sender's balance is always accepted
    Deliberately false, and tagged on the rule: the tag applies to every scenario beneath it.

    # Deliberately FALSE. It sounds right, and both example rows pass as tests,
    # but the receiving wallet can overflow.
    @id:transfer_always_succeeds
    Scenario Outline: A transfer the sender can afford always succeeds
      Given Alice has a balance of <a>
      And Bob has a balance of <b>
      And <amount> is not more than Alice's balance
      When Alice transfers <amount> to Bob
      Then the operation succeeds
      And Alice's balance is decreased by <amount>
      And the total of all balances is unchanged

      Examples:
        | a   | b  | amount |
        | 100 | 20 | 30     |
        | 5   | 0  | 5      |

  @expect-unbound @id:interest
  Rule: A deposit earns interest
    Not a claim about this wallet: the rule line and its scenario use words the vocabulary does not define.

    # Uses a phrase the glossary does not define.
    @id:deposit_earns_interest @expect-unbound
    Scenario: A deposit earns interest
      Given Alice has a balance of 100
      When Alice deposits 5
      Then Alice earns interest on her balance
