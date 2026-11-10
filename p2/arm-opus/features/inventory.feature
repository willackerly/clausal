Feature: Inventory
  A warehouse is a row of storage bins, bin 0 first. Each bin holds some number of units of one
  product, and several bins may hold the same product. A bin and an order are both written
  product:units, so a warehouse holding the bins [7:10, 3:5] has ten units of product 7 in bin 0
  and five units of product 3 in bin 1, and the order 7:4 asks for four units of product 7.
  Units are unsigned 64-bit numbers; "the maximum" is the largest of them, 18446744073709551615.

  Each Rule is one plain-English claim. The rule line and the text under it are carried
  into the report as written; they are not compiled. What is proved is each scenario
  beneath the rule, and together those scenarios are the rule's suite.

  Rule: Counting the units of a product adds up what all of its bins hold, and gives no count when that sum does not fit

    @id:stock_is_sum
    Scenario Outline: The count of a product's units is the sum over its bins
      Given warehouse Main holds the bins <bins>
      And the units of product <p> in warehouse Main add up to at most the maximum
      When the units of product <p> in warehouse Main are counted
      Then the result is the number of units of product <p> in warehouse Main

      Examples:
        | bins                           | p |
        | [7:10, 3:5, 7:4]               | 7 |
        | [7:10, 3:5, 7:4]               | 3 |
        | [7:10, 3:5, 7:4]               | 9 |
        | []                             | 1 |
        | [1:18446744073709551615, 1:0]  | 1 |

    @id:stock_too_big
    Scenario Outline: No count is given when a product's units add up to more than the maximum
      Given warehouse Main holds the bins <bins>
      And the units of product <p> in warehouse Main add up to more than the maximum
      When the units of product <p> in warehouse Main are counted
      Then no count is given

      Examples:
        | bins                                            | p |
        | [1:18446744073709551615, 2:1, 1:1]              | 1 |
        | [5:9223372036854775808, 6:1, 5:9223372036854775808] | 5 |

  Rule: Looking for a bin finds the first bin of the product that holds enough units, and finds nothing when no bin does

    @id:find_first_bin
    Scenario Outline: The bin found is the first one that holds enough of the product
      Given warehouse Main holds the bins <bins>
      And some bin of warehouse Main holds at least <n> units of product <p>
      When a bin of product <p> with at least <n> units is looked for in warehouse Main
      Then the result is the first bin of warehouse Main that holds at least <n> units of product <p>

      Examples:
        | bins                    | p | n |
        | [7:2, 3:5, 7:6, 7:9]    | 7 | 5 |
        | [7:2, 3:5, 7:6, 7:9]    | 7 | 0 |
        | [7:2, 3:5, 7:6, 7:9]    | 3 | 5 |

    @id:find_no_bin
    Scenario Outline: Nothing is found when no bin holds enough of the product
      Given warehouse Main holds the bins <bins>
      And no bin of warehouse Main holds at least <n> units of product <p>
      When a bin of product <p> with at least <n> units is looked for in warehouse Main
      Then no bin is found

      Examples:
        | bins                    | p | n  |
        | [7:2, 3:5, 7:6, 7:9]    | 7 | 10 |
        | [7:2, 3:5, 7:6, 7:9]    | 8 | 0  |
        | []                      | 1 | 0  |

  Rule: Restocking a product adds the amount to every bin of that product, up to the maximum, and changes no other bin

    @id:restock_adds
    Scenario Outline: Every bin of the product gains the amount, up to the maximum
      Given warehouse Main holds the bins <bins>
      When every bin of product <p> in warehouse Main is restocked with <a> units
      Then every bin of product <p> in warehouse Main has gained <a> units, up to the maximum, and no other bin has changed

      Examples:
        | bins                                 | p | a |
        | [7:2, 3:5, 7:6]                      | 7 | 3 |
        | [7:2, 3:5, 7:18446744073709551614]   | 7 | 3 |
        | [7:2, 3:5]                           | 9 | 3 |

    @id:restock_counts
    Scenario Outline: Restocking reports how many bins it restocked
      Given warehouse Main holds the bins <bins>
      When every bin of product <p> in warehouse Main is restocked with <a> units
      Then the number of bins restocked is the number of bins of product <p> in warehouse Main

      Examples:
        | bins              | p | a |
        | [7:2, 3:5, 7:6]   | 7 | 3 |
        | [7:2, 3:5, 7:6]   | 3 | 0 |
        | []                | 7 | 1 |

  Rule: Taking units of a product empties its earliest bins first, and takes what was asked for or all there is, whichever is less

    @id:take_amount
    Scenario Outline: The amount taken is what was asked for, or all there is if that is less
      Given warehouse Main holds the bins <bins>
      When <n> units of product <p> are taken from warehouse Main
      Then the amount taken is the smaller of <n> and the units of product <p> that warehouse Main held

      Examples:
        | bins                                              | p | n                    |
        | [7:4, 3:5, 7:6, 7:1]                              | 7 | 7                    |
        | [7:4, 3:5, 7:6, 7:1]                              | 7 | 20                   |
        | [7:4, 3:5]                                        | 9 | 1                    |
        | [1:18446744073709551615, 1:18446744073709551615]  | 1 | 18446744073709551615 |

    @id:take_stock_down
    Scenario Outline: The product's units go down by exactly the amount taken
      Given warehouse Main holds the bins <bins>
      When <n> units of product <p> are taken from warehouse Main
      Then the units of product <p> in warehouse Main have gone down by exactly the amount taken

      Examples:
        | bins                   | p | n  |
        | [7:4, 3:5, 7:6, 7:1]   | 7 | 7  |
        | [7:4, 3:5, 7:6, 7:1]   | 3 | 2  |

    @id:take_earliest_first
    Scenario Outline: Units are taken from the earliest bins of the product first
      Given warehouse Main holds the bins <bins>
      When <n> units of product <p> are taken from warehouse Main
      Then warehouse Main now holds what is left after taking <n> units of product <p> from its earliest bins first

      Examples:
        | bins                   | p | n  |
        | [7:4, 3:5, 7:6, 7:1]   | 7 | 7  |
        | [7:4, 3:5, 7:6, 7:1]   | 7 | 0  |
        | [7:4, 3:5, 7:6, 7:1]   | 7 | 20 |

  Rule: Filling orders fills, in turn, each order the warehouse can then cover in full, and skips the others

    @id:fill_count
    Scenario Outline: The number of orders filled is the number that can be covered in full when their turn comes
      Given warehouse Main holds the bins <bins>
      When the orders <orders> are filled from warehouse Main
      Then the number of orders filled is the number of orders of <orders> that can be filled in full, in turn, from warehouse Main

      Examples:
        | bins                           | orders                              |
        | [7:4, 3:5, 7:6]                | [7:8, 3:6, 7:3, 3:5]                |
        | [7:4, 3:5, 7:6]                | []                                  |
        | [1:18446744073709551615, 1:5]  | [1:18446744073709551615, 1:5, 1:1]  |

    @id:fill_state
    Scenario Outline: What is left is what remains after filling, in turn, the orders that can be covered
      Given warehouse Main holds the bins <bins>
      When the orders <orders> are filled from warehouse Main
      Then warehouse Main now holds what is left after filling, in turn, each order of <orders> that can be filled in full

      Examples:
        | bins              | orders                   |
        | [7:4, 3:5, 7:6]   | [7:8, 3:6, 7:3, 3:5]     |
        | [7:4, 3:5, 7:6]   | [9:1, 7:0]               |

    @id:fill_at_most
    Scenario Outline: No more orders are filled than were given
      Given warehouse Main holds the bins <bins>
      When the orders <orders> are filled from warehouse Main
      Then the number of orders filled is at most the number of orders in <orders>

      Examples:
        | bins              | orders                   |
        | [7:4, 3:5, 7:6]   | [7:8, 3:6, 7:3, 3:5]     |
        | []                | [7:0]                    |

  Rule: Counting products counts each different product once, however many bins hold it

    @id:count_products
    Scenario Outline: The count is the number of different products
      Given warehouse Main holds the bins <bins>
      When the different products in warehouse Main are counted
      Then the result is the number of different products in warehouse Main

      Examples:
        | bins                         |
        | [7:1, 3:0, 7:2, 9:1, 3:3]    |
        | []                           |
        | [7:1]                        |

    @id:count_at_most_bins
    Scenario Outline: There are no more products than bins
      Given warehouse Main holds the bins <bins>
      When the different products in warehouse Main are counted
      Then the result is at most the number of bins of warehouse Main

      Examples:
        | bins                         |
        | [7:1, 3:0, 7:2, 9:1, 3:3]    |
        | [7:1, 8:1]                   |

  Rule: The dominant product is the one held by more than half of the bins, and there is none when no product is

    @id:dominant_found
    Scenario Outline: A product in more than half of the bins is the dominant product
      Given warehouse Main holds the bins <bins>
      And product <p> is in more than half of the bins of warehouse Main
      When the dominant product of warehouse Main is looked for
      Then the result is product <p>

      Examples:
        | bins                         | p |
        | [3:1, 7:1, 7:1]              | 7 |
        | [7:1, 3:1, 3:1, 7:1, 7:1]    | 7 |
        | [0:5]                        | 0 |

    @id:dominant_none
    Scenario Outline: There is no dominant product when no product is in more than half of the bins
      Given warehouse Main holds the bins <bins>
      And no product is in more than half of the bins of warehouse Main
      When the dominant product of warehouse Main is looked for
      Then there is no dominant product

      Examples:
        | bins                         |
        | [7:1, 3:1]                   |
        | [7:1, 3:1, 9:1, 7:1]         |
        | []                           |
