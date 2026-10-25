#!/usr/bin/env python3
"""TASK-107: Tier 1 guard for the pre-commit hook manifest (.pre-commit-hooks.yaml).

The manifest is validated structurally because `pre-commit` itself is not a project
dependency (Zero-Deps); the contract is small and fully covered by these assertions.
"""

import base64
import json
import re
import unittest
import zlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = REPO_ROOT / ".pre-commit-hooks.yaml"
INSTALLER = REPO_ROOT / "install.py"


def parse_hooks(text):
    """Minimal parser for the flat hook list this repository owns (no PyYAML)."""
    hooks = []
    current = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("- "):
            current = {}
            hooks.append(current)
            line = line[2:].strip()
        if current is None or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.split("  #", 1)[0].strip().strip("'\"")
        current[key.strip()] = value
    return hooks


class PreCommitManifestTest(unittest.TestCase):
    def _hooks(self):
        return parse_hooks(MANIFEST.read_text(encoding="utf-8"))

    def test_manifest_structure(self):
        hooks = self._hooks()
        self.assertEqual(len(hooks), 1, "the manifest must declare exactly one hook")
        hook = hooks[0]
        self.assertEqual(hook.get("id"), "kb-lint")
        for key in ("name", "description", "entry", "language", "files", "pass_filenames", "require_serial"):
            self.assertTrue(hook.get(key), "hook is missing %s" % key)
        self.assertEqual(hook["language"], "system", "the hook must use the project interpreter, not install a package")
        self.assertEqual(hook["pass_filenames"].lower(), "false", "link resolution is global; per-file runs are false positives")
        self.assertEqual(hook["require_serial"].lower(), "true")

    def test_entry_targets_existing_linter(self):
        hook = self._hooks()[0]
        entry = hook["entry"]
        self.assertIn("scripts/kb_lint.py", entry, "entry must run the shipped linter")
        self.assertIn("--path", entry)
        self.assertIn("docs", entry)
        self.assertTrue((REPO_ROOT / "scripts" / "kb_lint.py").is_file(), "entry points to a missing script")

    def test_files_pattern_matches_markdown(self):
        hook = self._hooks()[0]
        pattern = re.compile(hook["files"])
        self.assertTrue(pattern.search("docs/00_Index.md"), "the hook must run on Markdown")
        self.assertFalse(pattern.search("scripts/kb_lint.py"), "the hook must not run on Python files")

    def test_manifest_is_not_bundled(self):
        text = INSTALLER.read_text(encoding="utf-8")
        match = re.search(r'EMBEDDED_ASSETS_B64 = "([^"]+)"', text)
        self.assertIsNotNone(match, "embedded assets blob not found in install.py")
        assets = json.loads(zlib.decompress(base64.b64decode(match.group(1))).decode("utf-8"))
        self.assertIn("scripts/kb_lint.py", assets, "bundle extraction produced no linter script")
        self.assertNotIn(".pre-commit-hooks.yaml", assets, "the hook manifest must not ship to client projects")


if __name__ == "__main__":
    unittest.main()
