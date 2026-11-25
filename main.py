#!/usr/bin/env python3
"""Tell a Whole Story in 32 Characters -- make.fun entry.

Writes one original Wi-Fi network name (at most 32 characters) to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output) and prints it to stdout:
a joke that implies a whole story in the few words a passer-by sees in
a phone's network list.

The name: a toddler changed the household Wi-Fi password, so the adults
are locked out of their own network by a two-year-old. The twist lands
on the first read -- the smallest person in the house outsmarted everyone
-- and the story is complete: the password is changed, the family is
locked out, and only the toddler knows it.

Deterministic: no input, no network, no randomness, no clock. Every run
writes byte-identical output. The program checks the gate itself before
writing: exactly one line, 1-32 characters, not blank.
"""

import os
import sys

NAME = "My Toddler Changed the Password"


def main():
    text = NAME
    if not text or not text.strip():
        print("gate failed: name is blank", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("gate failed: name must be a single line", file=sys.stderr)
        return 1
    if len(text) < 1 or len(text) > 32:
        print(
            "gate failed: %d characters, must be 1-32" % len(text),
            file=sys.stderr,
        )
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    # Read the file back and verify what was written is exactly the gated
    # name plus one trailing newline; refuse to report success otherwise.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text + "\n":
        print("gate failed: written file does not match the gated name",
              file=sys.stderr)
        return 1
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
