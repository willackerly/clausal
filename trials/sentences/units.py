"""The unique compiled readings of the V4 trial (several authors' rules reword to the same line)."""
import rewordings as rw
UNITS = {
 "T_TOTAL": rw.T_TOTAL, "T_TOTAL_OK": rw.T_TOTAL_OK, "T_MOVED": rw.T_MOVED, "T_REJ": rw.T_REJ, "T_VALID": rw.T_VALID,
 "T_SHORT": rw.R["opus-1/r4"]["text"], "T_ONLY": rw.R["haiku-1/R09"]["text"], "T_OVER": rw.R["haiku-1/R10"]["text"],
 "B_STEP": rw.B_STEP, "B_WHOLE": rw.B_WHOLE, "B_WHOLE_OK": rw.B_WHOLE_OK, "B_COUNT": rw.B_COUNT, "B_COUNT_STEP": rw.R["opus-1/r6"]["text"],
 "L_BOTH": rw.L_BOTH, "L_ZERO": rw.R["haiku-1/R12"]["text"],
 "TOTAL_ALWAYS": rw.R["opus-1/r11"]["text"], "TOTAL_FITS": rw.TOTAL_FITS[0].upper() + rw.TOTAL_FITS[1:],
 "L_BOTH_TOTAL_FITS": rw.R["sonnet-1/R9"]["text"],          # two operations in one rule: compiled, but not searched or tested as one
 "W_TOTAL": rw.PROBES["opus-1/r1"]["text"], "W_TOTAL_OK": rw.PROBES["haiku-1/R01"]["text"],   # probes
}
BY_TEXT = {t: u for u, t in UNITS.items()}
# the unit(s) a reworded rule is searched and tested through
def units_of(text):
    u = BY_TEXT[text]
    return ["L_BOTH", "TOTAL_FITS"] if u == "L_BOTH_TOTAL_FITS" else [u]
def rid(u): return f"Rule.v4_authored.{u.lower()}"
def feature():
    lines = ["Feature: V4 authored", "  Rules written by proxy authors (models), reworded by the trial runner so that they compile. Scratch copy only.", ""]
    for u, t in UNITS.items():
        lines += [f"  @id:{u.lower()}", f"  Rule: {t}", ""]
    return "\n".join(lines)
