# source this (bash or zsh): toolchain environment for the fork spike (local opam root, no ~/.opam)
FORK="$(cd "$(dirname "${BASH_SOURCE[0]:-${(%):-%x}}")" && pwd)"
export FORK
export OPAMROOT=$FORK/.opam
eval $(opam env --switch=aeneas --set-switch)
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
