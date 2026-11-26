#!/usr/bin/env python3
"""The Comment Above the Code.

Writes one funny, painfully honest comment -- the kind a developer leaves
above fragile production code -- to /output/entry.txt (or $ENTRY_OUTPUT).

Three candidate lines were scored by hand against the judge's brief, in
order of importance: (1) funny comment about fragile legacy code,
(2) honesty that stings by naming a real, recognisable failure,
(3) economical, punchline landing on the last few words,
(4) fresh angle, no off-by-one / who-wrote-this / no-comments cliche,
(5) reads like a comment actually left in a codebase.

Scores (each criterion 0-5):

  A  "If you change anything in this file, the invoice module starts
      charging customers twice and the logs will insist everything
      is fine."
      (5, 4, 4, 4, 5) = 22
      Double-charging plus lying logs is a real failure, and the
      punchline lands at the end, but "don't touch this file" is a
      well-worn angle.

  B  "This function works only because of a bug in the database
      driver that was fixed upstream in 2019. We pinned the driver
      instead."
      (5, 5, 5, 5, 4) = 24
      The sting is specific and instantly recognisable: the code is
      correct only by accident, and the team chose to freeze the bug
      in place rather than fix the code. "instead" sharpens that
      choice into the punchline. Winner.

  C  "The retry loop below fires exactly once per deployment, which
      is why the dashboard says 100% uptime and the customers say
      otherwise."
      (5, 4, 4, 4, 4) = 21
      A good observation about lying dashboards, but the punchline
      softens at the end and the angle is more familiar than B's.

The program is fully deterministic: no randomness, no clock, no network,
no file reads. It re-scores the candidates from the table below, picks
the highest total score (ties broken by shorter text, then by order),
and writes the winner to the output file.
"""

import os

# (text, scores per criterion 1..5, in judge order)
CANDIDATES = [
    (
        "// If you change anything in this file, the invoice module "
        "starts charging customers twice and the logs will insist "
        "everything is fine.",
        (5, 4, 4, 4, 5),
    ),
    (
        "// This function works only because of a bug in the database "
        "driver that was fixed upstream in 2019. We pinned the driver "
        "instead.",
        (5, 5, 5, 5, 4),
    ),
    (
        "// The retry loop below fires exactly once per deployment, "
        "which is why the dashboard says 100% uptime and the customers "
        "say otherwise.",
        (5, 4, 4, 4, 4),
    ),
]

MAX_CHARS = 200


def pick_winner(candidates):
    """Highest total score; ties broken by shorter text, then by order."""
    best = None
    best_key = None
    for index, (text, scores) in enumerate(candidates):
        total = sum(scores)
        # Negate total so the smallest key wins; shorter text wins ties.
        key = (-total, len(text), index)
        if best_key is None or key < best_key:
            best_key = key
            best = text
    return best


def main():
    winner = pick_winner(CANDIDATES)

    # The gate requires 1-200 characters of UTF-8 text, not only spaces.
    if not (1 <= len(winner) <= MAX_CHARS):
        raise SystemExit(
            "winner is %d chars, outside the 1-%d range" % (len(winner), MAX_CHARS)
        )
    if not winner.strip():
        raise SystemExit("winner is only whitespace")

    # Output path: $ENTRY_OUTPUT wins, else $MAKEFUN_OUTPUT_DIR/entry.txt,
    # else /output/entry.txt. Never chmod anything here: in the grader
    # sandbox the output directory may be owned by another user (e.g.
    # root, mode 777), and chmod on a directory or file we do not own
    # raises PermissionError and kills the run before anything is written.
    out_path = os.environ.get("ENTRY_OUTPUT")
    if not out_path:
        makefun_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
        if makefun_dir:
            out_path = os.path.join(makefun_dir, "entry.txt")
        else:
            out_path = "/output/entry.txt"
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(winner + "\n")


if __name__ == "__main__":
    main()
