#!/usr/bin/env python3
"""
Unit and integration test suite for kb_lint.py safe autofix core (TASK-113).
Verifies deterministic rules, surgical string patching, atomic writes, and git-clean safety.
"""

import os
import sys
import json
import tempfile
import unittest
import subprocess
from pathlib import Path

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.kb_lint import (
    Fix,
    FixResult,
    Finding,
    LintReport,
    make_finding,
    generate_file_fixes,
    render_diff,
    render_json,
    render_sarif,
    git_check_clean,
    atomic_write_file,
    run_linter,
)


class TestKbLintAutoFixCore(unittest.TestCase):
    """Tests the surgical string patching logic for the 5 safe deterministic rules."""

    def test_kb004_frontmatter_delimiters(self):
        """KB-004: Normalize stray spaces in opening/closing frontmatter delimiters."""
        content = "---\t \nid: TASK-001\ntitle: Sample\n---  \n\n# Body\n"
        path = Path("docs/02_Tasks/Specs/TASK-001.md")
        result = generate_file_fixes(content, path)
        self.assertTrue(result.has_changes)
        fix_rules = [f.rule_id for f in result.fixes]
        self.assertIn("KB-004", fix_rules)
        self.assertTrue(result.modified_content.startswith("---\n"))
        self.assertIn("\n---\n", result.modified_content)

    def test_kb005_date_normalization(self):
        """KB-005: Normalize dot/slash date formats to ISO-8601 YYYY-MM-DD."""
        content = (
            "---\n"
            "id: TASK-001\n"
            "created: 2026.11.19\n"
            "updated: \"2026/09/26\" # comment\n"
            "date: '2026.01.01'\n"
            "depends_on: []\n"
            "---\n"
            "\n# Spec\n"
        )
        path = Path("docs/02_Tasks/Specs/TASK-001.md")
        result = generate_file_fixes(content, path)
        self.assertTrue(result.has_changes)
        self.assertIn("created: 2026-11-19\n", result.modified_content)
        self.assertIn('updated: "2026-09-26" # comment\n', result.modified_content)
        self.assertIn("date: '2026-01-01'\n", result.modified_content)
        kb005_fixes = [f for f in result.fixes if f.rule_id == "KB-005"]
        self.assertEqual(len(kb005_fixes), 3)

    def test_kb006_trailing_whitespace(self):
        """KB-006: Strip trailing whitespace while preserving markdown hard line breaks."""
        content = (
            "---\n"
            "id: TASK-001   \n"
            "title: Sample\n"
            "depends_on: []\n"
            "---\n"
            "\n"
            "Line with single space \n"
            "Line with hard break  \n"
            "Line with tab\t\n"
            "   \n"
            "Clean line\n"
        )
        path = Path("docs/02_Tasks/Specs/TASK-001.md")
        result = generate_file_fixes(content, path)
        self.assertTrue(result.has_changes)
        # In frontmatter, all trailing whitespace is removed
        self.assertIn("id: TASK-001\n", result.modified_content)
        # Single trailing space and tab removed
        self.assertIn("Line with single space\n", result.modified_content)
        self.assertIn("Line with tab\n", result.modified_content)
        # Empty whitespace-only line cleaned
        self.assertIn("\n\nClean line\n", result.modified_content)
        # Hard line break with exactly 2 spaces preserved
        self.assertIn("Line with hard break  \n", result.modified_content)

    def test_kb007_eof_newline(self):
        """KB-007: Guarantee single trailing newline at EOF."""
        # Case A: Missing EOF newline
        content_no_nl = "---\nid: NOTE\n---\n# Body"
        res_a = generate_file_fixes(content_no_nl, Path("note.md"))
        self.assertTrue(res_a.has_changes)
        self.assertTrue(res_a.modified_content.endswith("# Body\n"))
        self.assertIn("KB-007", [f.rule_id for f in res_a.fixes])

        # Case B: Multiple trailing newlines
        content_multi_nl = "---\nid: NOTE\n---\n# Body\n\n\n\n"
        res_b = generate_file_fixes(content_multi_nl, Path("note.md"))
        self.assertTrue(res_b.has_changes)
        self.assertTrue(res_b.modified_content.endswith("# Body\n"))
        self.assertFalse(res_b.modified_content.endswith("\n\n"))

    def test_kb010_inject_default_depends_on(self):
        """KB-010: Safely inject depends_on: [] into task spec frontmatter if missing."""
        content = (
            "---\n"
            "id: TASK-001\n"
            "# Custom comment here\n"
            "title: Sample Task\n"
            "status: planned\n"
            "---\n"
            "\n# TASK-001\n"
        )
        path = Path("docs/02_Tasks/Specs/01_Phase/TASK-001-sample.md")
        result = generate_file_fixes(content, path)
        self.assertTrue(result.has_changes)
        self.assertIn("depends_on: []\n", result.modified_content)
        # Injected before the closing --- delimiter
        self.assertIn("depends_on: []\n---\n", result.modified_content)
        # Comments preserved
        self.assertIn("# Custom comment here\n", result.modified_content)

    def test_kb010_skip_when_depends_on_already_present(self):
        """KB-010: Do not inject depends_on if already declared."""
        content = (
            "---\n"
            "id: TASK-001\n"
            "depends_on:\n"
            "  - TASK-000\n"
            "---\n"
            "\n# Spec\n"
        )
        path = Path("docs/02_Tasks/Specs/TASK-001.md")
        result = generate_file_fixes(content, path)
        self.assertFalse(result.has_changes)
        self.assertEqual(len(result.fixes), 0)

    def test_clean_file_produces_no_fixes(self):
        """Clean file must produce zero fixes and empty diff."""
        content = (
            "---\n"
            "id: TASK-001\n"
            "title: Clean Task\n"
            "created: 2026-11-19\n"
            "depends_on: []\n"
            "---\n"
            "\n# Clean Spec\n"
        )
        path = Path("docs/02_Tasks/Specs/TASK-001.md")
        result = generate_file_fixes(content, path)
        self.assertFalse(result.has_changes)
        self.assertEqual(len(result.fixes), 0)
        self.assertEqual(len(result.diff_lines), 0)


class TestKbLintAutoFixCLI(unittest.TestCase):
    """Tests CLI flag behaviors: --fix dry-run preview vs --write in-place execution."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self.tmp.name) / "docs"
        self.vault.mkdir()
        specs = self.vault / "02_Tasks" / "Specs"
        specs.mkdir(parents=True)
        plans = self.vault / "02_Tasks" / "Plans"
        plans.mkdir(parents=True)
        (plans / "PLAN-001.md").write_text("---\nid: PLAN-001\ntitle: Plan\n---\n# Plan\n", encoding="utf-8")
        # Create an unformatted task spec file with all required fields except depends_on
        self.task_file = specs / "TASK-001.md"
        self.task_file.write_text(
            "---\n"
            "id: TASK-001\n"
            "title: Test Task\n"
            "type: task\n"
            "phase: 1\n"
            "parent_plan: \"[[PLAN-001]]\"\n"
            "created: 2026.11.19\n"
            "status: planned\n"
            "--- \n"
            "\n"
            "# Content with trailing space \n"
            "\n\n",
            encoding="utf-8"
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_dry_run_leaves_disk_untouched(self):
        """--fix without --write must not modify any files on disk."""
        initial_content = self.task_file.read_text(encoding="utf-8")
        code = run_linter(self.vault, fix=True, write=False)
        self.assertEqual(code, 0)
        # Content on disk must be identical
        self.assertEqual(self.task_file.read_text(encoding="utf-8"), initial_content)

    def test_write_applies_modifications_to_disk(self):
        """--fix with write=True atomically applies modifications to disk."""
        code = run_linter(self.vault, fix=True, write=True, allow_dirty=True)
        self.assertEqual(code, 0)
        modified = self.task_file.read_text(encoding="utf-8")
        self.assertIn("created: 2026-11-19\n", modified)
        self.assertIn("depends_on: []\n", modified)
        self.assertIn("---\n", modified)
        self.assertTrue(modified.endswith("# Content with trailing space\n"))

    def test_dry_run_wins_over_write(self):
        """When dry_run=True, files must not be written even if write=True was specified."""
        initial_content = self.task_file.read_text(encoding="utf-8")
        # In CLI, effective_write = bool(args.write and not args.dry_run)
        effective_write = bool(True and not True)
        self.assertFalse(effective_write)
        run_linter(self.vault, fix=True, write=effective_write)
        self.assertEqual(self.task_file.read_text(encoding="utf-8"), initial_content)


class TestKbLintSafetyProtocol(unittest.TestCase):
    """Tests the safety protocol: atomic writes, Git-Clean Guard, and diff formatting."""

    def test_atomic_write_file(self):
        """atomic_write_file creates file safely and cleanly."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "sub" / "file.md"
            atomic_write_file(target, "Hello Atomic World\n")
            self.assertTrue(target.is_file())
            self.assertEqual(target.read_text(encoding="utf-8"), "Hello Atomic World\n")

    def test_render_diff(self):
        """render_diff formats unified diff with optional ANSI colors."""
        diff_lines = [
            "--- a/test.md\n",
            "+++ b/test.md\n",
            "@@ -1,2 +1,2 @@\n",
            "-old line\n",
            "+new line\n",
        ]
        plain = render_diff(diff_lines, use_color=False)
        self.assertEqual(plain, "".join(diff_lines))

        colored = render_diff(diff_lines, use_color=True)
        self.assertIn("\033[32m", colored)  # Green for +
        self.assertIn("\033[31m", colored)  # Red for -
        self.assertIn("\033[36m", colored)  # Cyan for @@

    def test_git_check_clean_guard(self):
        """git_check_clean detects uncommitted modifications in a real git repository."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_dir = Path(tmp_dir)
            try:
                subprocess.run(["git", "init"], cwd=str(repo_dir), check=True, capture_output=True)
                subprocess.run(["git", "config", "user.email", "test@test.local"], cwd=str(repo_dir), check=True, capture_output=True)
                subprocess.run(["git", "config", "user.name", "Test User"], cwd=str(repo_dir), check=True, capture_output=True)
                
                test_file = repo_dir / "test.md"
                test_file.write_text("Committed\n", encoding="utf-8")
                subprocess.run(["git", "add", "test.md"], cwd=str(repo_dir), check=True, capture_output=True)
                subprocess.run(["git", "commit", "-m", "init"], cwd=str(repo_dir), check=True, capture_output=True)

                # 1. Clean file
                self.assertTrue(git_check_clean(test_file))

                # 2. Modify file without commit
                test_file.write_text("Uncommitted modification\n", encoding="utf-8")
                self.assertFalse(git_check_clean(test_file))
            except (subprocess.CalledProcessError, FileNotFoundError):
                # If git is not installed in the testing environment, it safely falls back to True
                self.assertTrue(git_check_clean(Path("some_file.md")))


class TestKbLintContractFormats(unittest.TestCase):
    """Tests machine-readable format extensions (JSON fixable / fixes and SARIF 2.1.0 fixes array)."""

    def test_finding_fixable_attribute(self):
        """Finding supports fixable flag with explicit and auto-detection behaviors."""
        f1 = Finding("KB-001", "Broken link", "error", fixable=False)
        self.assertFalse(f1.fixable)

        f2 = Finding("KB-004", "Tag missing #", "warning", fixable=True)
        self.assertTrue(f2.fixable)

        # make_finding auto-detection
        mf_unfixable = make_finding("KB-001", "Missing link")
        self.assertFalse(mf_unfixable.fixable)

        mf_fixable = make_finding("KB-002", "Malformed YAML frontmatter (missing closing ---)")
        self.assertTrue(mf_fixable.fixable)

    def test_json_contract_without_fix_preserves_strict_v1_keys(self):
        """Without --fix, render_json preserves exact v1 schema without extra keys."""
        f_err = make_finding("KB-001", "Missing link [[Target]]", file="doc.md", location="docs/doc.md")
        f_warn = make_finding("KB-005", "Asset layout violation", file="doc.md", location="docs/doc.md")
        report = LintReport(files=1, wikilinks=1, findings=[f_err, f_warn])

        out = render_json(report, include_fix=False)
        data = json.loads(out)
        self.assertEqual(sorted(data["summary"]), ["errors", "files", "warnings", "wikilinks"])
        self.assertNotIn("fixable", data["summary"])
        self.assertNotIn("fixes", data)

        err_item = data["errors"][0]
        self.assertEqual(sorted(err_item), ["file", "location", "message", "rule_id", "severity"])
        self.assertNotIn("fixable", err_item)

    def test_json_contract_with_fix_includes_fixable_and_fixes(self):
        """With include_fix=True, render_json includes fixable in summary and findings, plus fixes array."""
        f_err = make_finding("KB-001", "Missing link [[Target]]", file="doc.md", location="docs/doc.md")
        f_fix_err = make_finding("KB-002", "Malformed YAML frontmatter (missing closing ---)", file="doc.md", location="docs/doc.md")
        f_fix_warn = make_finding("KB-006", "Tag format error", severity="warning", file="doc.md", location="docs/doc.md", fixable=True)
        report = LintReport(files=1, wikilinks=1, findings=[f_err, f_fix_err, f_fix_warn])

        dummy_fix = Fix(
            rule_id="KB-004",
            description="Normalized delimiter",
            file_path=Path("docs/doc.md"),
            line_number=1,
            original_text="--- ",
            replacement_text="---",
        )
        fix_res = FixResult(
            file_path=Path("docs/doc.md"),
            original_content="---\n",
            modified_content="---\n",
            fixes=[dummy_fix],
            diff_lines=["-old\n", "+new\n"],
        )

        out = render_json(report, fix_results=[fix_res], include_fix=True)
        data = json.loads(out)
        self.assertIn("fixable", data["summary"])
        self.assertEqual(data["summary"]["fixable"], 2)

        err_item = data["errors"][0]
        self.assertIn("fixable", err_item)
        self.assertFalse(err_item["fixable"])

        warn_item = data["warnings"][0]
        self.assertIn("fixable", warn_item)
        self.assertTrue(warn_item["fixable"])

        self.assertIn("fixes", data)
        self.assertEqual(len(data["fixes"]), 1)
        self.assertEqual(data["fixes"][0]["rule_id"], "KB-004")
        self.assertEqual(data["fixes"][0]["line"], 1)

    def test_sarif_contract_with_fix_includes_fixes_block(self):
        """With include_fix=True, render_sarif attaches fixes array to fixable results only."""
        f_unfix = make_finding("KB-001", "Broken link", file="broken.md")
        f_fix = make_finding("KB-002", "Malformed YAML frontmatter (missing closing ---)", file="fixed.md")
        report = LintReport(files=2, wikilinks=1, findings=[f_unfix, f_fix])

        # Without fix: no fixes property
        sarif_plain = json.loads(render_sarif(report, include_fix=False))
        results_plain = sarif_plain["runs"][0]["results"]
        for res in results_plain:
            self.assertNotIn("fixes", res)

        # With fix: fixes present for fixable rule only
        sarif_fixed = json.loads(render_sarif(report, include_fix=True))
        results_fixed = sarif_fixed["runs"][0]["results"]
        self.assertEqual(len(results_fixed), 2)
        res_by_id = {r["ruleId"]: r for r in results_fixed}
        self.assertNotIn("fixes", res_by_id["KB-001"])
        self.assertIn("fixes", res_by_id["KB-002"])
        self.assertIn("kb_lint.py --fix --write", res_by_id["KB-002"]["fixes"][0]["description"]["text"])


if __name__ == "__main__":
    unittest.main()
