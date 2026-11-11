The score orders the reading list. It is not a measure of whether a family is one idea, and it is not used to decide anything.

    score = conceptReductionHigh / penalty

- `conceptReductionLow` = (members − 1) + lemma statements with an identical shape held by two or more members, minus the largest member's share (the statements one parameterised version would replace, counted strictly).
- `conceptReductionHigh` = (members − 1) + the larger of that and the role count: for each lemma role shared by two or more members and held by at most max(40, 3·members + 20) definitions in the corpus, one lemma per further member. For a family of types the role count is set to 0.
- Statements that mention two or more members are left out of both counts.
- `penalty` = 1 + effective parameters + 0.5 × (holes that depend on a bound variable) + 0.5 × (compound holes) when the members share a body; 2 for a specialisation family (the general form exists); 5 when there is no common body (similarity below 0.5), because the replacement would be an interface and not a parameter.
- Printed beside it and not in the score: users, statements mentioning a member, co-occurrence, skeleton size, instance and type arguments per member.

Known distortions. A family of verbatim copies scores highest (no holes, penalty 1) although merging it changes no proof. A two-member family of large structures with many shared roles scores high on the role count alone. The role count is an optimistic bound: two lemmas with the same role need not be instances of one statement, and earlier work here found 18 of the 20 largest statement-shape clusters had a false common generalisation.
