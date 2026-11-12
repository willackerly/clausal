# Rule packs (plan node K1)

A **rule pack** is a parameterised suite of ordinary Clausal sentences with holes for a project's operation and nouns.
It is not a Clausebook word pack (`clausebook/ledger.yaml` supplies *words* with Lean definitions and is trusted); a
rule pack supplies *sentences*, has no Lean, and is trusted for nothing: its output is plain Rule lines that the ordinary
compiler reads like any hand-written line.

    packs/<name>/pack.yaml     slots, members (template sentences), variants, adequacy expectation, seeded bugs
    packs/<name>/FREEZE.md     what was frozen before a target was looked at, and how results are counted

Design note and command: section "The command" below is filled in by the step that builds it.
