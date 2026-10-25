#!/usr/bin/env python3
"""Sandbox-safe unittest runner (TRG-03 / INC-003).

DSH Windows sandbox: ``tempfile.mkdtemp()`` creates directories with mode 0o700,
which produces a DACL that denies child file creation, so every test that uses it
fails with ``PermissionError: [WinError 5]``. Patch ``mkdtemp`` to a permissive
mode and keep temporary directories inside the workspace (``tmp/`` is gitignored).

Usage:
    python scripts/run_tests_sandbox.py
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = REPO_ROOT / "tests"
TEMP_ROOT = REPO_ROOT / "tmp" / "sandbox_temp"
TEMP_ROOT.mkdir(parents=True, exist_ok=True)

for _var in ("TMP", "TEMP", "TMPDIR"):
    os.environ[_var] = str(TEMP_ROOT)
tempfile.tempdir = str(TEMP_ROOT)


def _mkdtemp(suffix=None, prefix=None, dir=None):
    suffix = suffix or ""
    prefix = prefix or "tmp"
    dir = dir or tempfile.gettempdir()
    for _ in range(100):
        name = os.path.join(dir, prefix + os.urandom(8).hex() + suffix)
        try:
            os.mkdir(name, 0o777)
            return name
        except FileExistsError:
            continue
    raise FileExistsError("could not create temp directory")


def main() -> int:
    tempfile.mkdtemp = _mkdtemp
    sys.path.insert(0, str(REPO_ROOT))
    suite = unittest.TestLoader().discover(str(TESTS_DIR), top_level_dir=str(TESTS_DIR))
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
