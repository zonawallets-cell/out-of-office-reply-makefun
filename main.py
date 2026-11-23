#!/usr/bin/env python3
"""The Funniest AI Out-of-Office Reply entry (make.fun, program/v1).

Writes one original out-of-office auto-reply to /output/entry.txt
(or $MAKEFUN_OUTPUT_DIR). Pure stdlib only (os). The reply is a single
line of at most 160 characters, byte-identical on every run.
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
    print("wrote %d chars to %s" % (len(REPLY), path))


if __name__ == "__main__":
    main()
