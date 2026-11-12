# Item bank `wallet-ledger-generated-echoes-v1` (plan node V5)

The echo trial of `../../README.md` (K1) on the tool's own output. Every item is a Rule line that `clausal/`'s compiler accepts, shown with an echo printed by the compiler's own echo generator.

- A **faithful** item has the echo of the sentence's own composition tree, exactly as the tool prints it.
- An **unfaithful** item has the echo of that tree after one mechanical mutation, shown against the original sentence. The mutations are in `mutate.py`: drop a Given, swap strict and non-strict, every call becomes successful calls only, a party word becomes the other party, a quantity becomes a neighbouring one. Where the mutated tree is one a sentence can spell, `python3 mutate.py` checks that the mutated echo is character for character the tool's echo of that sentence.
- 45 items, one part, about one third unfaithful. No sentence appears twice and no two items share an echo. Item order is a seeded shuffle and ids were assigned after it.

"Faithful" in the key means *the tool's own echo of the unmutated tree*. It is true by construction, not by a person's judgement, so a reader who flags a faithful item has either raised a false alarm or found something in the tool's reading. `item_flags.json` lists the items where the bank builder expects the second.

The sentences come from two places: the rewordings of the V4 proxy authors' rules (`../../../sentences/`) and the Rule lines of `clausal/features/`. The bank builder is a model; the explanations and the disagreeing cases in the key were written by it.

| file | gives the key away? |
|---|---|
| `items.json`, `brief.md`, `trial.html` | no |
| `mutate.py`, `pool.py`, `make_bank.py` | no (the scripts read the selection, they do not contain it) |
| `selection.json`, `key.json`, `item_flags.json`, `responses/` | **yes**; git-ignored |

To rebuild (needs the scratch copy of `clausal/`, see `../../../sentences/README.md`): `python3 make_bank.py`. It writes `items.json`, `key.json`, `item_flags.json` and `trial.html` and prints the material hash. The build is deterministic: the same vocabulary and the same `selection.json` give the same hash. To give the trial and score it: `python3 ../../take_trial.py --bank . --reader NAME`, `python3 ../../score.py --bank .`.
