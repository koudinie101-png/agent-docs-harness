#!/usr/bin/env python3
"""Render and verify the root AGENTS.md from rules/AGENTS_CORE.md.

The corpus is the single hand-edited source of agent rules (ADR-0030). The root
AGENTS.md is a generated artifact: manual edits are detected by `--check`.
"""

import argparse
import difflib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import install  # noqa: E402

DEFAULT_OUTPUT = REPO_ROOT / "AGENTS.md"


def normalize(text):
    """Normalize line endings so Windows autocrlf never fakes a drift."""
    return text.replace("\r\n", "\n")


def render_harness_agents():
    return install._render_rules_document("harness-agents", {})


def check_current(output_path=DEFAULT_OUTPUT, rendered=None):
    """Return (ok, unified_diff) for the generated artifact vs the corpus."""
    if rendered is None:
        rendered = render_harness_agents()
    target = Path(output_path)
    actual = normalize(target.read_text(encoding="utf-8")) if target.is_file() else ""
    expected = normalize(rendered)
    if actual == expected:
        return True, ""
    diff = list(difflib.unified_diff(
        actual.splitlines(), expected.splitlines(),
        fromfile=str(target), tofile="rules/AGENTS_CORE.md", lineterm="",
    ))
    return False, "\n".join(diff[:40])


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Render root AGENTS.md from the rules corpus.")
    parser.add_argument("--check", action="store_true",
                        help="verify AGENTS.md is up to date (exit 1 on drift)")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT),
                        help="target path (default: ./AGENTS.md)")
    args = parser.parse_args(argv)

    output = Path(args.output)
    try:
        rendered = render_harness_agents()
    except RuntimeError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 2

    if args.check:
        ok, diff = check_current(output, rendered)
        if ok:
            print("OK: AGENTS.md matches rules/AGENTS_CORE.md")
            return 0
        print("ERROR: AGENTS.md is stale. Run: python scripts/gen_rules.py")
        if diff:
            print(diff)
        return 1

    output.write_bytes(normalize(rendered).encode("utf-8"))
    print("OK: rendered %s from rules/AGENTS_CORE.md" % output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
