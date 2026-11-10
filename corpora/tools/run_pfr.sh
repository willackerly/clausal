#!/bin/sh
# Export the PFR declaration graph. Run after `lake exe cache get && lake build` in corpora/pfr.
export PATH="$HOME/.elan/bin:$PATH"
cd "$(dirname "$0")/../pfr" || exit 1
OUT=../../out/corpus/pfr
MODS=$(cd .lake/build/lib/lean && find PFR PFRPalomar PFR.olean -name '*.olean' | sed 's/\.olean$//; s#/#.#g' | grep -v '^PFRPalomar.Challenge$' | sort | paste -sd, -)
python3 -I ../tools/parse_blueprint.py blueprint/src web.tex $OUT || exit 1
EXPORT_CHECK_NAMES=$OUT/blueprint_lean_names.txt lake env lean --run ../tools/ExportDecls.lean $OUT PFR,PFRPalomar "$MODS" \
  Marton.pfr_conjecture Marton.pfr_conjecture_nine Marton.torsion_pfr_conjecture \
  Marton.weak_pfr_int Marton.homomorphism_pfr Marton.approx_hom_pfr \
  PFR_conjecture PFR_conjecture_improv torsion_PFR weak_PFR_int homomorphism_pfr approx_hom_pfr
python3 -I ../tools/parse_blueprint.py blueprint/src web.tex $OUT --resolve
