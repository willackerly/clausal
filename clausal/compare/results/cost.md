<!-- table:cost_rules -->
| Rule | Kind | Gherkin statement lines | a: + rows lines (rows) | b: property lines | c: harness lines | d: proof lines | d: lemma lines it rests on (share) | b ms plain / edge | c seconds | d seconds to re-check the proof |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_conserves | exact | 11 | 4 (2) | 17 | 13 | 6 | 0 | 14 / 41 | 0 | 5.62 |
| withdraw_too_much | rejection | 7 | 4 (2) | 12 | 10 | 4 | 0 | 10 / 27 | 0 | 5.34 |
| deposit_overflow | rejection | 7 | 4 (2) | 12 | 10 | 4 | 0 | 11 / 27 | 0 | 5.49 |
| withdraw_covered | exact | 7 | 5 (3) | 12 | 10 | 4 | 0 | 12 / 26 | 0 | 5.24 |
| deposit_with_room | exact | 7 | 5 (3) | 12 | 10 | 4 | 0 | 11 / 26 | 0 | 5.63 |
| transfer_short | rejection | 9 | 4 (2) | 15 | 11 | 4 | 0 | 11 / 32 | 0 | 5.21 |
| transfer_no_room | rejection | 10 | 4 (2) | 16 | 12 | 4 | 0 | 13 / 38 | 0 | 5.52 |
| batch_conserves | safety | 5 | 8 (6) | 10 | 11 | 3 | 153 (9.1) | 25 / 100 | 7 | 5.17 |
| batch_first_invalid | rejection | 7 | 5 (3) | 11 | 13 | 4 | 153 (9.1) | 31 / 157 | 6 | 5.44 |
| batch_count_bounded | bound | 5 | 5 (3) | 10 | 11 | 3 | 153 (9.1) | 25 / 114 | 4 | 5.31 |
| batch_stops_at_invalid | progress | 5 | 7 (5) | 12 | 13 | 3 | 153 (9.1) | 25 / 103 | 5 | 5.26 |
| transfer_valid_moves | exact | 8 | 5 (3) | 27 | 23 | 5 | 92 (5.0) | 28 / 56 | 9 | 5.3 |
| transfer_invalid_rejected | rejection | 7 | 7 (5) | 15 | 13 | 5 | 92 (5.0) | 27 / 71 | 3 | 5.42 |
| total_is_sum | exact | 6 | 7 (5) | 9 | 11 | 6 | 90 (10.9) | 14 / 55 | 1 | 5.2 |
| total_overflow | rejection | 6 | 5 (3) | 9 | 10 | 3 | 90 (10.9) | 13 / 39 | 1 | 5.35 |
| balance_of_account | exact | 6 | 4 (2) | 10 | 12 | 4 | 9 (4.5) | 16 / 34 | 1 | 5.42 |
| balance_no_account | rejection | 6 | 4 (2) | 13 | 11 | 4 | 9 (4.5) | 17 / 39 | 1 | 5.09 |
| whole_conserves | safety | 5 | 4 (2) | 10 | 11 | 3 | 187 (14.8) | 29 / 97 | 6 | 5.22 |
| whole_first_invalid | rejection | 7 | 3 (1) | 11 | 13 | 5 | 187 (14.8) | 38 / 141 | 4 | 5.47 |
| whole_rejected_unchanged | safety | 5 | 6 (4) | 10 | 11 | 3 | 187 (14.8) | 34 / 114 | 4 | 5.49 |
| batch_then_total | safety | 7 | 5 (3) | 11 | 13 | 10 | 184 (16.9) | 52 / 172 | 7 | 5.44 |
| batch_then_total_overflow | safety | 7 | 4 (2) | 11 | 12 | 7 | 184 (16.9) | 32 / 133 | 4 | 5.56 |
| two_batches_conserve | safety | 7 | 3 (1) | 13 | 14 | 5 | 153 (9.1) | 44 / 174 | 8 | 5.32 |

<!-- table:cost_kinds -->
| Crate | Kind | Rules | Gherkin statement lines | a: rows lines | b: property lines | c: harness lines | d: proof lines | d: lemma lines, share | d: lemma lines the proof rests on | b: ms plain / edge | c: seconds | d: seconds to re-check the proof |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| wallet (straight-line) | exact | 3 | 8.3 | 4.7 | 13.7 | 11.0 | 4.7 | 0.0 | 0.0 | 12.3 / 31.0 | 0.4 | 5.5 |
| wallet (straight-line) | rejection | 4 | 8.2 | 4.0 | 13.8 | 10.8 | 4.0 | 0.0 | 0.0 | 11.2 / 31.0 | 0.3 | 5.4 |
| ledger (loops, Vec) | safety | 6 | 6.0 | 5.0 | 10.8 | 12.0 | 5.2 | 13.6 | 174.7 | 36.0 / 131.7 | 6.0 | 5.4 |
| ledger (loops, Vec) | exact | 3 | 6.7 | 5.3 | 15.3 | 15.3 | 5.0 | 6.8 | 63.7 | 19.3 / 48.3 | 3.9 | 5.3 |
| ledger (loops, Vec) | rejection | 5 | 6.6 | 4.8 | 11.8 | 12.0 | 4.2 | 8.9 | 106.2 | 25.2 / 89.4 | 3.2 | 5.4 |
| ledger (loops, Vec) | progress | 1 | 5.0 | 7.0 | 12.0 | 13.0 | 3.0 | 9.1 | 153.0 | 25.0 / 103.0 | 5.3 | 5.3 |
| ledger (loops, Vec) | bound | 1 | 5.0 | 5.0 | 10.0 | 11.0 | 3.0 | 9.1 | 153.0 | 25.0 / 114.0 | 3.6 | 5.3 |

<!-- table:cost_whole -->
| Arm | Build | Run | Notes |
|---|---|---|---|
| a. example rows | 5.6 s (61 s) | 0.4 s (2.5 s) | all 35 scenarios of the three feature files |
| b. proptest | 1.4 s (10.9 s) | plain 0.7 s (1.5 s); edge 1.8 s (5.0 s) | 23 properties, 10,000 cases each |
| c. Kani | 7.6 s (44 s) | 75 s (681 s), of which the 16 ledger rules 73 s (663 s) | 23 harnesses run one at a time; per rule in appendix B |
| d. Lean | - | 53 s (273 s) | the whole pipeline: translation, build, search, audit, cucumber, report. Re-checking one proof after an edit: 5 to 6 s; rebuilding the lemma library: 18 s |
