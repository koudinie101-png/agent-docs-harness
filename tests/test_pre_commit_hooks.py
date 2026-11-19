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
        self.assertEqual(len(hooks), 2, "the manifest must declare kb-lint and kb-lint-fix hooks")
        hook_by_id = {h.get("id"): h for h in hooks}
        self.assertIn("kb-lint", hook_by_id)
        self.assertIn("kb-lint-fix", hook_by_id)

        required_keys = ("name", "description", "entry", "language", "files", "pass_filenames", "require_serial")
        for hook_id in ("kb-lint", "kb-lint-fix"):
            hook = hook_by_id[hook_id]
            for key in required_keys:
                self.assertTrue(hook.get(key), "hook %s is missing %s" % (hook_id, key))
            self.assertEqual(hook["language"], "system", "the hook must use the project interpreter, not install a package")
            self.assertEqual(hook["pass_filenames"].lower(), "false", "link resolution is global; per-file runs are false positives")
            self.assertEqual(hook["require_serial"].lower(), "true")

    def test_entry_targets_existing_linter(self):
        hook_by_id = {h.get("id"): h for h in self._hooks()}
        self.assertTrue((REPO_ROOT / "scripts" / "kb_lint.py").is_file(), "entry points to a missing script")

        lint_hook = hook_by_id["kb-lint"]
        fix_hook = hook_by_id["kb-lint-fix"]

        for hook in (lint_hook, fix_hook):
            entry = hook["entry"]
            self.assertIn("scripts/kb_lint.py", entry, "entry must run the shipped linter")
            self.assertIn("--path", entry)
            self.assertIn("docs", entry)

        self.assertIn("--fix", fix_hook["entry"])
        self.assertIn("--write", fix_hook["entry"])
        self.assertNotIn("--fix", lint_hook["entry"])

    def test_files_pattern_matches_markdown(self):
        for hook in self._hooks():
            pattern = re.compile(hook["files"])
            self.assertTrue(pattern.search("docs/00_Index.md"), "hook %s must run on Markdown" % hook.get("id"))
            self.assertFalse(pattern.search("scripts/kb_lint.py"), "hook %s must not run on Python files" % hook.get("id"))

    def test_manifest_is_not_bundled(self):
        text = INSTALLER.read_text(encoding="utf-8")
        match = re.search(r'EMBEDDED_ASSETS_B64 = "([^"]+)"', text)
        self.assertIsNotNone(match, "embedded assets blob not found in install.py")
        assets = json.loads(zlib.decompress(base64.b64decode(match.group(1))).decode("utf-8"))
        self.assertIn("scripts/kb_lint.py", assets, "bundle extraction produced no linter script")
        self.assertNotIn(".pre-commit-hooks.yaml", assets, "the hook manifest must not ship to client projects")


if __name__ == "__main__":
    unittest.main()
