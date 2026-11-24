#!/usr/bin/env python3
"""Fortune Cookie Wisdom for Developers.

Writes one original fortune-cookie line for a software developer to
$MAKEFUN_OUTPUT_DIR/entry.txt (falling back to /output), then reads it
back to confirm the file holds exactly that line.

Runs with no arguments, uses only the standard library, makes no
network calls, and produces byte-identical output on every run.
"""

import os
import sys

# One original line of fortune-cookie wisdom for a software developer.
FORTUNE = "The function you named temporary will outlive every promise you made about it."


def main() -> int:
    # The gate allows 1 to 120 characters and rejects whitespace-only text.
    if not 1 <= len(FORTUNE) <= 120:
        print(f"error: line is {len(FORTUNE)} characters, must be 1-120", file=sys.stderr)
        return 1
    if not FORTUNE.strip():
        print("error: line must not be only whitespace", file=sys.stderr)
        return 1
    if "\n" in FORTUNE or "\r" in FORTUNE:
        print("error: line must be a single line", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(FORTUNE + "\n")

    # Read back and verify the file holds exactly the intended line, and
    # that the file as a whole still satisfies the gate (1-120 characters).
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != FORTUNE + "\n":
        print("error: read-back verification failed", file=sys.stderr)
        return 1
    if not 1 <= len(written) <= 120:
        print(f"error: entry.txt is {len(written)} characters, must be 1-120", file=sys.stderr)
        return 1

    print(f"Wrote {len(FORTUNE)}-character fortune to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
