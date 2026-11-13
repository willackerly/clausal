"""clausal CLI.

  python3 -m clausal gen      parse features, bind steps, write Statements/Checks/Search/Adequacy, append proof stubs
  python3 -m clausal derive   read out/search.log, write Run/Audit.lean (sat / unsat / refuted / trivial-Then + audit)
  python3 -m clausal adequacy read out/adequacy.log, write Run/AdequacyAudit.lean (suite adequacy note; informational)
  python3 -m clausal report [--strict] [--trust-policy F]
                              write out/graph.json, out/report.md and out/trust.json, print the per-scenario and per-Rule report
  python3 -m clausal rules [graph.json]   print the per-Rule blocks of a stored graph (reads the graph only)
  python3 -m clausal steps    print the cucumber regex of every glossary entry; check wallet-bdd/tests/steps.rs
  python3 -m clausal attest <id|all|glossary:<id>|policy:<project>> --act ACT --as <human:|model:|tool:|org:>ID --scope TEXT [--on-behalf-of ID]
                               write an attestation record (who did what to which entry, as it is now): stored beside the entry's
                               book (clausebook/<book>.attest.json), in glossary.attest.json, or in trust/<project>.attest.json.
                               A model's record is its own kind and never counts as a person's. `attest check` checks every store.
                               `all` attests every entry but the separations: a separation is attested by its own id, and a
                               review or approval of it is written only if `clausal separate`, run now, confirms it.
                               (Replaces `review … --reviewer NAME` and both sign-off files; format: trust/FREEZE.md)
  python3 -m clausal trust [--graph F] [--policy F] [--strict] [--json]
                               strict mode, computed from a stored graph and each project's trust policy (projects.yaml `trust:`)
  python3 -m clausal compile <file.feature>... [--collect]   NEW sentences compiled from the Clausebook alone (heldout/):
                               writes lean/Run/NewReadings.lean; --collect reads out/new_sentences.log back
  python3 -m clausal separate "<sentence A>" ["<sentence B>"] [--json]   an input on which two candidate readings differ, or
                               "none found" with the bounds, or "same term" / "different operations" (clausal/separate.py)
  python3 -m clausal compose "<rough English>" [--domain D] [--json] [--top N] [--choose K] [--write F.feature]   candidate
                               sentences of the Clausebook close to a rough one, each compiled, best first (clausal/compose.py)

  python3 -m clausal show "<sentence>" [--json] [--no-refusal] [--no-separate]   the computed display of a Rule line: which calls it
                               covers, the outcome table of a rule that compares two calls, an allowed and a forbidden case, the
                               nearest neighbouring sentence that allows the forbidden case (clausal/display.py, DISPLAY.md)
  python3 -m clausal display   after lean/Run/Display.lean ran: out/display.json and its checks (a step of run.sh)

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
