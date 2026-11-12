Feature: Ledger
  A ledger holds unsigned 64-bit balances, one per account; accounts are numbered
  from 0. A transfer "0->1:30" moves 30 from account 0 to account 1. A batch is a
  list of transfers applied in order; it stops at the first transfer that cannot
  be carried out exactly. Balances are written account 0 first: [100, 20, 0].

  # THE loop-invariant property: whatever the ledger and whatever the batch.
  @id:batch_conserves
  Scenario Outline: Applying any batch of transfers conserves the total of all balances
    Given ledger Main holds the balances <balances>
    When the batch <batch> is applied to ledger Main
    Then the total of ledger Main's balances is unchanged

    Examples:
      | balances        | batch                       |
      | [100, 20, 0]    | [0->1:30, 1->2:50]          |
      | [5, 5]          | [0->1:6]                    |
      | [1, 0]          | [0->1:1, 0->1:1, 1->0:2]    |
      | []              | []                          |
      | [100, 20, 0]    | [0->1:30, 1->2:50, 2->0:5]  |
      | [9, 0, 0, 0]    | [0->1:4, 1->2:3, 2->3:2, 3->0:1] |

  @id:batch_first_invalid
  Scenario Outline: A batch whose first transfer is invalid changes nothing
    Given ledger Main holds the balances <balances>
    And the first transfer of <batch> is not valid on ledger Main
    When the batch <batch> is applied to ledger Main
    Then no transfer is applied
    And ledger Main is unchanged

    Examples:
      | balances      | batch                  |
      | [5, 5]        | [0->1:6, 1->0:1]       |
      | [5, 5]        | [0->0:1]               |
      | [5, 5]        | [0->2:1, 0->1:1]       |

  @id:batch_count_bounded
  Scenario Outline: The number of transfers applied is at most the length of the batch
    Given ledger Main holds the balances <balances>
    When the batch <batch> is applied to ledger Main
    Then the number of transfers applied is at most the length of <batch>

    Examples:
      | balances      | batch                       |
      | [100, 20, 0]  | [0->1:30, 1->2:50]          |
      | [5, 5]        | [0->1:6]                    |
      | [7]           | []                          |

  # PROGRESS, added after the review. The three scenarios above are all true of a batch function that
  # does nothing at all. This one says the loop goes on as long as it can: if it stopped early, the
  # transfer it stopped at cannot be carried out on the ledger as the batch left it. It is stated
  # without describing the intermediate ledgers.
  @id:batch_stops_at_invalid
  Scenario Outline: A batch stops only at a transfer that cannot be carried out
    Given ledger Main holds the balances <balances>
    When the batch <batch> is applied to ledger Main
    Then the batch <batch> has stopped only at a transfer that is not valid on ledger Main as it now stands

    Examples:
      | balances        | batch                              |
      | [100, 20, 0]    | [0->1:30, 1->2:50]                 |
      | [100, 20, 0]    | [0->1:30, 2->1:5, 0->1:1]          |
      | [9, 0, 0, 0]    | [0->1:4, 1->2:3, 2->3:2, 3->0:1]   |
      | [9, 0, 0, 0]    | [0->1:4, 1->2:3, 2->3:2, 3->0:5]   |
      | [5, 5]          | [0->1:6, 1->0:1]                   |

  # Literal values: the whole batch goes through.
  @id:batch_example_all
  Scenario: A batch of two valid transfers is applied in full
    Given ledger Main holds the balances [100, 20, 0]
    When the batch [0->1:30, 1->2:50] is applied to ledger Main
    Then exactly 2 transfers are applied
    And ledger Main now holds the balances [70, 0, 50]

  # Literal values: the batch stops at the second transfer and keeps the first.
  @id:batch_example_stop
  Scenario: A batch stops at its first invalid transfer and keeps what it has applied
    Given ledger Main holds the balances [100, 20, 0]
    When the batch [0->1:30, 2->1:5, 0->1:1] is applied to ledger Main
    Then exactly 1 transfers are applied
    And ledger Main now holds the balances [70, 50, 0]

  # Deliberately FALSE. It sounds right, and every example row passes as a test:
  # each transfer is fine against the ledger as it stands BEFORE the batch, but an
  # earlier transfer can spend what a later one needs.
  @id:batch_all_valid_all_applied @expect-refuted
  Scenario Outline: A batch of transfers that are each valid on the starting ledger is applied in full
    Given ledger Main holds the balances <balances>
    And every transfer of <batch> is valid on ledger Main
    When the batch <batch> is applied to ledger Main
    Then every transfer of <batch> is applied

    Examples:
      | balances      | batch                  |
      | [100, 20, 0]  | [0->1:30, 1->2:20]     |
      | [5, 5]        | [0->1:5]               |

  @id:transfer_valid_moves
  Scenario Outline: A valid transfer is accepted and moves exactly its amount
    Given ledger Main holds the balances <balances>
    And the transfer <t> is valid on ledger Main
    When the transfer <t> is applied to ledger Main
    Then it is accepted
    And the amount of <t> has moved between its accounts in ledger Main and no other balance changed
    And the total of ledger Main's balances is unchanged

    Examples:
      | balances        | t         |
      | [100, 20, 0]    | 0->2:100  |
      | [1, 2, 3]       | 2->0:1    |
      | [0, 0]          | 1->0:0    |

  @id:transfer_invalid_rejected
  Scenario Outline: An invalid transfer is rejected and changes nothing
    Given ledger Main holds the balances <balances>
    And the transfer <t> is not valid on ledger Main
    When the transfer <t> is applied to ledger Main
    Then it is rejected
    And ledger Main is unchanged

    Examples:
      | balances                        | t         |
      | [100, 20, 0]                    | 0->2:101  |
      | [100, 20, 0]                    | 0->3:1    |
      | [100, 20, 0]                    | 3->0:1    |
      | [100, 20, 0]                    | 1->1:5    |
      | [1, 18446744073709551615]       | 0->1:1    |

  @id:total_is_sum
  Scenario Outline: The total is the sum of the balances when that fits
    Given ledger Main holds the balances <balances>
    And the balances of ledger Main add up to <sum>
    When the total of ledger Main is computed
    Then the result is <sum>

    Examples:
      | balances                    | sum                  |
      | [100, 20, 0]                | 120                  |
      | []                          | 0                    |
      | [18446744073709551615, 0]   | 18446744073709551615 |
      | [1, 2, 3, 4]                | 10                   |
      | [1, 2, 3, 4, 5]             | 15                   |

  @id:total_overflow
  Scenario Outline: The total of balances that do not fit is reported as absent
    Given ledger Main holds the balances <balances>
    And the balances of ledger Main add up to more than the maximum
    When the total of ledger Main is computed
    Then there is no result

    Examples:
      | balances                                       |
      | [18446744073709551615, 1]                      |
      | [9223372036854775808, 5, 9223372036854775808]  |
      | [18446744073709551615, 0, 0, 1]                |

  # Deliberately FALSE: the sum of u64 balances need not fit in a u64.
  @id:total_always_available @expect-refuted
  Scenario Outline: The total of a ledger can always be computed
    Given ledger Main holds the balances <balances>
    When the total of ledger Main is computed
    Then there is a result

    Examples:
      | balances        |
      | [100, 20, 0]    |
      | []              |

  @id:balance_of_account
  Scenario Outline: Looking up an existing account gives its balance
    Given ledger Main holds the balances <balances>
    And <i> is an account of ledger Main
    When the balance of account <i> of ledger Main is looked up
    Then the result is the balance of account <i> of ledger Main

    Examples:
      | balances      | i |
      | [100, 20, 0]  | 0 |
      | [100, 20, 0]  | 2 |

  @id:balance_no_account
  Scenario Outline: Looking up an account that does not exist gives nothing
    Given ledger Main holds the balances <balances>
    And <i> is not an account of ledger Main
    When the balance of account <i> of ledger Main is looked up
    Then there is no result

    Examples:
      | balances      | i |
      | [100, 20, 0]  | 3 |
      | []            | 0 |

  @id:whole_conserves
  Scenario Outline: Applying a batch as a whole conserves the total of all balances
    Given ledger Main holds the balances <balances>
    When the batch <batch> is applied to ledger Main as a whole
    Then the total of ledger Main's balances is unchanged

    Examples:
      | balances        | batch                  |
      | [100, 20, 0]    | [0->1:30, 1->2:50]     |
      | [100, 20, 0]    | [0->1:30, 1->2:51]     |

  @id:whole_first_invalid
  Scenario Outline: A batch applied as a whole whose first transfer is invalid is rejected and changes nothing
    Given ledger Main holds the balances <balances>
    And the first transfer of <batch> is not valid on ledger Main
    When the batch <batch> is applied to ledger Main as a whole
    Then it is rejected
    And ledger Main is unchanged

    Examples:
      | balances      | batch                  |
      | [5, 5]        | [0->1:6, 1->0:1]       |

  # ATOMICITY, added after the review: the defining property of applying a batch as a whole. Before
  # this scenario it was stated only for a batch whose FIRST transfer is invalid and for one literal case.
  @id:whole_rejected_unchanged
  Scenario Outline: A batch applied as a whole that is rejected leaves the ledger unchanged
    Given ledger Main holds the balances <balances>
    When the batch <batch> is applied to ledger Main as a whole
    Then if it is rejected, ledger Main is unchanged

    Examples:
      | balances        | batch                              |
      | [100, 20, 0]    | [0->1:30, 2->1:5]                  |
      | [100, 20, 0]    | [0->1:30, 1->2:50, 2->0:60]        |
      | [9, 0, 0, 0]    | [0->1:4, 1->2:3, 2->3:2, 3->0:5]   |
      | [100, 20, 0]    | [0->1:30, 1->2:50]                 |

  # Literal values: all or nothing. Every transfer goes through, so the batch is accepted.
  @id:whole_example_accept
  Scenario: A batch of valid transfers applied as a whole is accepted and applied
    Given ledger Main holds the balances [100, 20, 0]
    When the batch [0->1:30, 1->2:50] is applied to ledger Main as a whole
    Then it is accepted
    And ledger Main now holds the balances [70, 0, 50]

  # Literal values: all or nothing, three transfers deep. Two transfers go through, the third fails,
  # and both are undone.
  @id:whole_example_rollback_late
  Scenario: A batch applied as a whole is rolled back when its third transfer is invalid
    Given ledger Main holds the balances [100, 20, 0]
    When the batch [0->1:30, 1->2:50, 2->0:60] is applied to ledger Main as a whole
    Then it is rejected
    And ledger Main now holds the balances [100, 20, 0]

  # Literal values: all or nothing. The second transfer fails, so the first is undone.
  @id:whole_example_rollback
  Scenario: A batch applied as a whole is rolled back when a later transfer is invalid
    Given ledger Main holds the balances [100, 20, 0]
    When the batch [0->1:30, 2->1:5] is applied to ledger Main as a whole
    Then it is rejected
    And ledger Main now holds the balances [100, 20, 0]

  # MULTI-STEP: two Whens in sequence, through both loops. Whatever batch is applied
  # first, the total computed afterwards is the sum the ledger started with.
  # The Given "add up to <sum>" restricts this to ledgers whose total fits in a u64 (the review's third
  # finding: the old title claimed more). The ledgers it leaves out are the next scenario.
  @id:batch_then_total
  Scenario Outline: The total computed after any batch is the total before it, when that total fits
    Given ledger Main holds the balances <balances>
    And the balances of ledger Main add up to <sum>
    When the batch <batch> is applied to ledger Main
    And the total of ledger Main is computed
    Then the result is <sum>

    Examples:
      | balances        | sum | batch                    |
      | [100, 20, 0]    | 120 | [0->1:30, 1->2:50]       |
      | [5, 5]          | 10  | [0->1:6]                 |
      | [1, 2, 3, 4]    | 10  | [3->0:4, 2->0:3, 1->0:2] |

  # MULTI-STEP, the other half: a total that does not fit before a batch does not fit after it.
  @id:batch_then_total_overflow
  Scenario Outline: The total computed after any batch is still absent when it did not fit before
    Given ledger Main holds the balances <balances>
    And the balances of ledger Main add up to more than the maximum
    When the batch <batch> is applied to ledger Main
    And the total of ledger Main is computed
    Then there is no result

    Examples:
      | balances                          | batch                |
      | [18446744073709551615, 1]         | [0->1:5]             |
      | [18446744073709551615, 0, 0, 1]   | [0->1:5, 0->2:7]     |
      | [14614687983979785864, 530155800626645669, 3301900289103120083] | [2->1:3301900289103120084] |

  # MULTI-STEP: two batches one after the other.
  @id:two_batches_conserve
  Scenario Outline: Two batches applied one after the other conserve the total
    Given ledger Main holds the balances <balances>
    When the batch <first> is applied to ledger Main
    And the batch <second> is applied to ledger Main
    Then the total of ledger Main's balances is unchanged
    And the number of transfers applied is at most the length of <second>

    Examples:
      | balances        | first                | second              |
      | [100, 20, 0]    | [0->1:30, 1->2:50]   | [2->0:50, 0->1:1]   |
