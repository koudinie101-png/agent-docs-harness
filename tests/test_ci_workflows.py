#!/usr/bin/env python3
"""TASK-098: Tier 1 guard for the harness-only Rules Check workflow (DEBT-002)."""

import contextlib
import io
import sys
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


ACTION = REPO_ROOT / "action.yml"


class ActionYmlContractTest(unittest.TestCase):
    """TASK-105: Tier 1 guard for the composite lint action."""

    def _action(self):
        return ACTION.read_text(encoding="utf-8")

    def test_action_metadata_and_composite_contract(self):
        text = self._action()
        for marker in (
            "name:",
            "description:",
            "branding:",
            "icon:",
            "color:",
            "using: composite",
            "shell: bash",
            "actions/setup-python@v5",
            "${GITHUB_ACTION_PATH}/scripts/kb_lint.py",
            "GITHUB_OUTPUT",
            "rc=$?",
            'exit "${rc}"',
        ):
            self.assertIn(marker, text, "action.yml lost composite contract marker: %s" % marker)
        for input_name in ("path:", "format:", "output-file:", "python-version:", "extra-args:"):
            self.assertIn("\n  " + input_name, text, "action.yml lost input: %s" % input_name)

    def test_action_does_not_upload_sarif_or_request_permissions(self):
        text = self._action()
        for marker in ("upload-sarif", "codeql-action", "security-events", "permissions:"):
            self.assertNotIn(
                marker,
                text,
                "action.yml must only produce SARIF: '%s' belongs to the caller workflow" % marker,
            )

    def test_action_uses_action_path_not_workspace_scripts(self):
        text = self._action()
        self.assertNotIn(
            "python scripts/kb_lint.py",
            text,
            "action.yml must resolve the linter from $GITHUB_ACTION_PATH, not from the workspace",
        )


CODE_SCANNING = REPO_ROOT / ".github" / "workflows" / "code-scanning.yml"


class CodeScanningWorkflowTest(unittest.TestCase):
    """TASK-108: Tier 1 guards for the harness-only Code Scanning workflow."""

    def _workflow(self):
        return CODE_SCANNING.read_text(encoding="utf-8")

    def test_workflow_hardening(self):
        text = self._workflow()
        for marker in (
            "permissions:",
            "contents: read",
            "security-events: write",
            "branches:",
            "concurrency:",
            "cancel-in-progress: true",
            "uses: ./",
            "upload-sarif",
            "if: always()",
            "github.event.pull_request.head.repo.full_name == github.repository",
            "category: kb-lint",
        ):
            self.assertIn(marker, text, "code-scanning.yml lost marker: %s" % marker)
        self.assertNotIn("tags:", text, "code-scanning.yml must not run on tag pushes (release.yml owns tags)")

    def test_rules_check_keeps_least_privilege(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertNotIn(
            "security-events",
            text,
            "rules-check.yml must not request Code Scanning permissions: use code-scanning.yml",
        )

    def test_harness_only_workflows_are_not_bundled(self):
        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        import build_installer

        with contextlib.redirect_stdout(io.StringIO()):
            assets = build_installer.bundle_assets()
        self.assertNotIn(".github/workflows/rules-check.yml", assets)
        self.assertNotIn(".github/workflows/code-scanning.yml", assets)
        self.assertIn(".github/workflows/release.yml", assets, "client workflows must still be bundled")


if __name__ == "__main__":
    unittest.main()
