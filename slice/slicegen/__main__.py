"""slicegen CLI.

  python3 -m slicegen gen      parse features, bind steps, write Statements/Checks/Search/Adequacy, append proof stubs
  python3 -m slicegen derive   read out/search.log, write Run/Audit.lean (sat / unsat / refuted / trivial-Then + audit)
  python3 -m slicegen adequacy read out/adequacy.log, write Run/AdequacyAudit.lean (suite adequacy note; informational)
  python3 -m slicegen report   write out/graph.json and out/report.md, print the per-scenario and per-Rule report
  python3 -m slicegen rules [graph.json]   print the per-Rule blocks of a stored graph (reads the graph only)
  python3 -m slicegen steps    print the cucumber regex of every glossary entry; check wallet-bdd/tests/steps.rs
  python3 -m slicegen review <id|all> --reviewer NAME    record a sign-off of a vocabulary piece (vocabulary.yaml) or of an entry
                               of the old glossary; `all` signs both
  python3 -m slicegen compile <file.feature>... [--collect]   NEW sentences compiled from the vocabulary alone (heldout/):
                               writes lean/Run/NewReadings.lean; --collect reads out/new_sentences.log back

gen also writes lean/Wallet/Readings.lean (the reading of every scenario and Rule line, compiled from vocabulary.yaml) and
lean/Run/ReadingSearch.lean; derive also writes lean/Run/Links.lean (NEW <-> OLD equivalences, non-vacuity, Rule glue).
"""
import sys

from . import pipeline

if __name__ == "__main__":
    sys.exit(pipeline.main(sys.argv[1:]))
