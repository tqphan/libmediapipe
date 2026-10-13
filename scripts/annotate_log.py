"""Turns the end of a failed step's log into GitHub annotations.

    python scripts/annotate_log.py path/to/log [more logs...]

Workflow logs need a GitHub login to read, but a run's annotations are public,
so the workflow runs this after a failure: each log gets one error annotation
with its error lines and its last lines.
"""

import re
import sys

ERRORS = re.compile(r"error|fatal|failed", re.IGNORECASE)
MAX_ERRORS = 40
TAIL = 40


def escape(s):
    # Workflow command escaping (data part).
    return s.replace("%", "%25").replace("\r", "").replace("\n", "%0A")


def main():
    for path in sys.argv[1:]:
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                lines = [line.rstrip() for line in f]
        except OSError as e:
            print(f"{path}: {e}")
            continue
        errors = [line for line in lines if ERRORS.search(line)][:MAX_ERRORS]
        body = "\n".join(["Error lines:"] + errors + ["", f"Last {TAIL} lines:"] + lines[-TAIL:])
        print(f"::error title={escape(path.replace(chr(92), '/').split('/')[-1])}::{escape(body)}")


if __name__ == "__main__":
    main()
