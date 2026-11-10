#!/bin/sh
# Export the Carleson declaration graph. Run after `lake exe cache get && lake build Carleson` in corpora/carleson.
export PATH="$HOME/.elan/bin:$PATH"
cd "$(dirname "$0")/../carleson" || exit 1
OUT=../../out/corpus/carleson
MODS=$(cd .lake/build/lib/lean && find Carleson Carleson.olean -name '*.olean' | sed 's/\.olean$//; s#/#.#g' | sort | paste -sd, -)
python3 -I ../tools/parse_blueprint.py blueprint/src web.tex $OUT || exit 1
EXPORT_CHECK_NAMES=$OUT/blueprint_lean_names.txt lake env lean --run ../tools/ExportDecls.lean $OUT Carleson "$MODS" \
  classical_carleson metric_carleson linearized_metric_carleson classical_carleson_check
python3 -I ../tools/parse_blueprint.py blueprint/src web.tex $OUT --resolve
