# Design probes (2026-11-09)

Throwaway evidence behind `../DESIGN.md`. Not part of the Lake project and not built by `translate.sh`.

- `wallet_lib.rs` - the candidate wallet crate source (enum here is named `Error`; the design renames it `WalletError`).
- `Wallet.generated.lean` - what Aeneas `nightly-2026.11.09-5a392f4` actually produced from it.
- `ProbeHolds.lean`, `ProbeStatement.lean` - self-contained Lean files (the model is pasted in) checking: evaluation of the
  model through `Result.match`, the bridge from Aeneas's `spec` triple to the plain `exists ... = ok ...` form, `step*` proofs of
  a universal scenario statement, a satisfiability witness, and a kernel-checked refutation. All theorems in them report
  axioms `[propext, Classical.choice, Quot.sound]`.

Re-run one (about 3 s, one-off, not for loops): from `clausal/lean`, `lake env lean ../probe/ProbeStatement.lean`.
