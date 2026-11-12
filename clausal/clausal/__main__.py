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

  python3 -m clausal book check [--lean] [--quiet] [--json] [--update-expected] [--update-terms]
                               the Clausebook itself: core stands alone, and the registration lint over every surface form
                               (clausebook/check.expected.json, clausebook/terms.lock.json); `book core` runs the first part only

gen also writes lean/Wallet/Readings.lean (the reading of every scenario and Rule line, compiled from the books of clausebook/) and
lean/Run/ReadingSearch.lean; derive also writes lean/Run/Links.lean (NEW <-> OLD equivalences, non-vacuity, Rule glue).
"""
import sys

from . import pipeline

if __name__ == "__main__":
    sys.exit(pipeline.main(sys.argv[1:]))
