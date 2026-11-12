"""clausal CLI.

  python3 -m clausal gen      parse features, bind steps, write Statements/Checks/Search/Adequacy, append proof stubs
  python3 -m clausal derive   read out/search.log, write Run/Audit.lean (sat / unsat / refuted / trivial-Then + audit)
  python3 -m clausal adequacy read out/adequacy.log, write Run/AdequacyAudit.lean (suite adequacy note; informational)
  python3 -m clausal report   write out/graph.json and out/report.md, print the per-scenario and per-Rule report
  python3 -m clausal rules [graph.json]   print the per-Rule blocks of a stored graph (reads the graph only)
  python3 -m clausal steps    print the cucumber regex of every glossary entry; check wallet-bdd/tests/steps.rs
  python3 -m clausal review <id|all> --reviewer NAME    record a sign-off of a Clausebook entry (stored beside its book, clausebook/<book>.signoff.json) or of an entry
                               of the old glossary; `all` signs both
  python3 -m clausal compile <file.feature>... [--collect]   NEW sentences compiled from the Clausebook alone (heldout/):
                               writes lean/Run/NewReadings.lean; --collect reads out/new_sentences.log back
  python3 -m clausal separate "<sentence A>" ["<sentence B>"] [--json]   an input on which two candidate readings differ, or
                               "none found" with the bounds, or "same term" / "different operations" (clausal/separate.py)
  python3 -m clausal compose "<rough English>" [--domain D] [--json] [--top N] [--choose K] [--write F.feature]   candidate
                               sentences of the Clausebook close to a rough one, each compiled, best first (clausal/compose.py)
  python3 -m clausal compose2 "<rough English>" [--domain D] [--json] [--no-l3] [--acknowledge K --by NAME] [--write F.feature]
                               composer version 2, no language model: ANSWER / ASK / DECLINE, every word of the rough sentence
                               accounted for or reported as dropped (clausal/compose2.py, clausal/COMPOSE2.md)
  python3 -m clausal converse "<rough English>" [--gold "<intended reading>"] [--domain D] [--json] [--max N]
                               the dialogue of composer version 2: one question per turn, an answer removes candidates; with --gold an
                               oracle author answers from the intended reading (clausal/dialogue.py)
  python3 -m clausal propose --request "<rough English>" | --check PROPOSAL.json   the interface of a proposer (no model is called; plan node
                               L1f is not built): what a proposer is given, and what the tool makes of the trees it returns (clausal/propose.py)
  python3 -m clausal tree "<rule sentence>" | --from FILE.json | --schema | --check   a Rule line's parse tree as JSON, the sentence
                               a tree spells (compiled, read back as the same tree), the JSON schema generated from the book (clausal/ctree.py)

  python3 -m clausal book check [--lean] [--quiet] [--json] [--update-expected] [--update-terms]
                               the Clausebook itself: core stands alone, and the registration lint over every surface form
                               (clausebook/check.expected.json, clausebook/terms.lock.json); `book core` runs the first part only

  python3 -m clausal duplicates [file.feature ...] [--json]
                               sentences whose compiled statements are the same once the operation's acceptance is unfolded
                               (informational; plan node Q5)

gen also writes lean/Wallet/Readings.lean (the reading of every scenario and Rule line, compiled from the books of clausebook/) and
lean/Run/ReadingSearch.lean; derive also writes lean/Run/Links.lean (NEW <-> OLD equivalences, non-vacuity, Rule glue).
"""
import sys

from . import pipeline

if __name__ == "__main__":
    sys.exit(pipeline.main(sys.argv[1:]))
