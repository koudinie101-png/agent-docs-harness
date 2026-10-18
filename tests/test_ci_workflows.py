#!/usr/bin/env python3
"""TASK-098: Tier 1 guard for the harness-only Rules Check workflow (DEBT-002)."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "rules-check.yml"


class RulesCheckWorkflowTest(unittest.TestCase):
    def _workflow(self):
        return WORKFLOW.read_text(encoding="utf-8")

    def test_rules_check_hardening(self):
        text = self._workflow()
        for marker in (
            "permissions:",
            "contents: read",
            "concurrency:",
            "cancel-in-progress: true",
            "branches:",
            "python scripts/kb_lint.py --path docs",
            "discover -s tests -q",
        ):
            self.assertIn(marker, text, "rules-check.yml lost CI hardening marker: %s" % marker)

    def test_rules_check_does_not_trigger_on_tags(self):
        text = self._workflow()
        self.assertNotIn("tags:", text, "rules-check.yml must not run on tag pushes (release.yml owns tags)")


if __name__ == "__main__":
    unittest.main()
