#!/usr/bin/env python3
"""The Funniest AI Out-of-Office Reply entry (make.fun, program/v1).

Writes one original out-of-office auto-reply to /output/entry.txt
(or $MAKEFUN_OUTPUT_DIR). Pure stdlib only (os). The reply is a single
line of at most 160 characters, byte-identical on every run.

The line: the AI goes on vacation and asks the reader to be kind to
the human covering for it — the inversion is the joke (the machine is
the competent one leaving; the human stand-in has never done this
before). No beach / inbox / back-soon cliche, and no frozen-weights
or token-count angle (the two visible entries' lanes).
"""

import os

REPLY = "A human is covering for me this week. Please be kind, they've never done this before."


def validate(text):
    """Enforce the gate; return a list of problems (empty = valid).

    Gate: UTF-8, 1-160 chars, no line breaks, not only whitespace.
    """
    problems = []
    if not isinstance(text, str):
        return ["not a string"]
    if not 1 <= len(text) <= 160:
        problems.append("length %d outside 1-160" % len(text))
    if not text.strip():
        problems.append("only whitespace")
    if "\n" in text or "\r" in text:
        problems.append("contains a line break")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append("not UTF-8 encodable: %s" % exc)
    return problems


def main():
    problems = validate(REPLY)
    if problems:
        raise SystemExit("reply failed validation: " + "; ".join(problems))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(REPLY)
    # Read back and verify: the grader runs the program twice and both
    # runs must write the same bytes, so a short/partial write must fail
    # loudly here instead of silently shipping a wrong file.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != REPLY:
        raise SystemExit("read-back mismatch: entry.txt differs from REPLY")
    print("wrote %d chars to %s" % (len(REPLY), path))


if __name__ == "__main__":
    main()
