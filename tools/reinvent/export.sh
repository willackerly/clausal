#!/bin/zsh
# usage: export.sh <ns|carleson|pfr> <defs|defsproj|thms> [nshards] [names.txt] [extra root] [extra module]
# Compiles Export.lean with the project's own toolchain and reads the project's BUILT environment.
set -e
PROJECT=$1; MODE=$2; N=${3:-6}; NAMES=${4:-}; XROOT=${5:-}; XMOD=${6:-}
source ${0:A:h}/env.sh
if [[ ! -x $B/export || $HERE/Export.lean -nt $B/export ]]; then
  (cd $HERE && lean +$TC -o $B/Export.olean -c $B/Export.c Export.lean && leanc +$TC -O3 -rdynamic -o $B/export $B/Export.c)
fi
MODS=$B/modules.txt
(cd $SRC/.lake/build/lib/lean && for r in ${(s:,:)ROOTS}; do find $r -name '*.olean' | grep -v '\.\(server\|private\)\.olean$'; [[ -f $r.olean ]] && echo $r.olean; done) \
  | sed 's/\.olean$//; s#/#.#g' | grep -v 'Challenge' | sort -u > $MODS

TAG=$MODE
if [[ -n $XMOD ]]; then echo $XMOD >> $MODS; ROOTS=$XROOT; TAG=planted; fi
S=$(date +%s)
for k in $(seq 0 $((N-1))); do
  LEAN_PATH=$LP $B/export $MODS $ROOTS $O/raw/$TAG $k $N $MODE $NAMES 2> $O/raw/$TAG.log.$k &
done; wait
cat $O/raw/$TAG.log.*
cat $O/raw/$TAG.$MODE.*.jsonl > $O/raw/$TAG.jsonl; rm -f $O/raw/$TAG.$MODE.*.jsonl
echo "$PROJECT $MODE: $(( $(date +%s) - S )) s, $(wc -l < $O/raw/$TAG.jsonl) records"
