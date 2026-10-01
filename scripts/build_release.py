#!/usr/bin/env python3
"""
scripts/build_release.py — Build Hook for agent-docs-harness.
Packages standalone install.py into dist/install.py for distribution.
"""

import sys
import shutil
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = REPO_ROOT / "dist"
INSTALL_PY = REPO_ROOT / "install.py"


def main() -> int:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    if not INSTALL_PY.is_file():
        print(f"Error: {INSTALL_PY} not found.", file=sys.stderr)
        return 1

    target = DIST_DIR / "install.py"
    shutil.copy2(INSTALL_PY, target)
    print(f"OK: Release artifact packaged at {target.as_posix()} ({target.stat().st_size} bytes).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
