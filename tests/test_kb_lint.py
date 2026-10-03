#!/usr/bin/env python3
"""
Unit tests for scripts/kb_lint.py (Docs-as-Code Knowledge Base Linter).
Tests Silent-on-Success mode, verbose mode, error detection, and CLI argument parsing.
"""

import sys
import io
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Add scripts directory to sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import kb_lint


class TestKbLint(unittest.TestCase):

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.docs_dir = self.temp_dir / "docs"
        self.docs_dir.mkdir(parents=True, exist_ok=True)

        # Create basic valid docs structure
        (self.docs_dir / "00_Index.md").write_text("# Index\n[[01_Architecture/arch]]", encoding="utf-8")
        arch_dir = self.docs_dir / "01_Architecture"
        arch_dir.mkdir()
        (arch_dir / "arch.md").write_text("# Architecture\n[[../00_Index]]", encoding="utf-8")

        # Create valid task spec with frontmatter
        tasks_dir = self.docs_dir / "02_Tasks" / "Specs"
        tasks_dir.mkdir(parents=True)
        task_content = "---\nid: TASK-001\ntitle: Test\nstatus: done\n---\n# Task 001\n[[../../00_Index]]"
        (tasks_dir / "TASK-001.md").write_text(task_content, encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_silent_on_success_mode(self):
        """Silent-on-Success should return 0 and output single 'OK: ...' line."""
        captured = io.StringIO()
        with patch("sys.stdout", captured):
            exit_code = kb_lint.run_linter(self.docs_dir, verbose=False)

        self.assertEqual(exit_code, 0)
        output = captured.getvalue().strip()
        lines = output.splitlines()
        self.assertEqual(len(lines), 1)
        self.assertTrue(output.startswith("OK: "))
        self.assertIn("0 broken", output)

    def test_verbose_mode(self):
        """Verbose mode should print full multi-line audit report."""
        captured = io.StringIO()
        with patch("sys.stdout", captured):
            exit_code = kb_lint.run_linter(self.docs_dir, verbose=True)

        self.assertEqual(exit_code, 0)
        output = captured.getvalue()
        self.assertIn("🔍 Auditing Knowledge Base at:", output)
        self.assertIn("Total Markdown Files Scanned:", output)
        self.assertIn("Total Wikilinks Validated:", output)
        self.assertIn("✅ No broken wikilinks found!", output)
        self.assertIn("🎉 Knowledge base is healthy and consistent!", output)

    def test_broken_wikilink_detection(self):
        """Broken wikilink should report ERROR and return exit code 1."""
        broken_file = self.docs_dir / "broken.md"
        broken_file.write_text("# Broken\n[[NonExistentTargetFile]]", encoding="utf-8")

        captured = io.StringIO()
        with patch("sys.stdout", captured):
            exit_code = kb_lint.run_linter(self.docs_dir, verbose=False)

        self.assertEqual(exit_code, 1)
        output = captured.getvalue()
        self.assertIn("ERROR:", output)
        self.assertIn("NonExistentTargetFile", output)

    def test_frontmatter_warning_detection(self):
        """Task spec without YAML frontmatter should fail with exit code 1."""
        bad_task = self.docs_dir / "02_Tasks" / "Specs" / "TASK-999.md"
        bad_task.write_text("# Missing Frontmatter\nJust markdown body.", encoding="utf-8")

        captured = io.StringIO()
        with patch("sys.stdout", captured):
            exit_code = kb_lint.run_linter(self.docs_dir, verbose=False)

        self.assertEqual(exit_code, 1)
        output = captured.getvalue()
        self.assertIn("frontmatter warnings", output)
        self.assertIn("TASK-999.md", output)

    def test_cli_execution_silent_and_verbose(self):
        """Test main() CLI wrapper with --path and --verbose flags."""
        test_argv_silent = [
            "kb_lint.py",
            "--path", str(self.docs_dir),
        ]
        with patch.object(sys, "argv", test_argv_silent):
            with self.assertRaises(SystemExit) as cm:
                kb_lint.run_linter(self.docs_dir, verbose=False)
                sys.exit(0)
            self.assertEqual(cm.exception.code, 0)

    def test_spec_drift_detection_warns_when_drifted(self):
        """Spec drift should emit warning when >= 2 phases completed and SPEC.md not updated."""
        repo_root = self.docs_dir.parent
        spec_content = "---\nid: SPEC\nstatus: active\ncreated: 2026-10-01\nupdated: 2026-10-01\n---\n# Spec"
        (repo_root / "SPEC.md").write_text(spec_content, encoding="utf-8")

        tasks_dir = self.docs_dir / "02_Tasks"
        tasks_dir.mkdir(parents=True, exist_ok=True)
        roadmap_content = (
            "# Roadmap\n\n"
            "## Фаза 1: First Phase — ✅ Завершена\n"
            "- [x] Task 1\n\n"
            "## Фаза 2: Second Phase — ✅ Завершена\n"
            "- [x] Task 2\n"
        )
        (tasks_dir / "Roadmap.md").write_text(roadmap_content, encoding="utf-8")

        warnings = kb_lint.check_spec_drift(self.docs_dir)
        self.assertEqual(len(warnings), 1)
        self.assertIn("Living Spec Drift", warnings[0])
        self.assertIn("2 completed phases", warnings[0])

        captured = io.StringIO()
        with patch("sys.stdout", captured):
            exit_code = kb_lint.run_linter(self.docs_dir, verbose=False)

        # Exit code must remain 0 (non-blocking warning)
        self.assertEqual(exit_code, 0)
        output = captured.getvalue()
        self.assertIn("⚠️  WARN: Living Spec Drift", output)
        self.assertIn("OK:", output)

    def test_spec_drift_no_warning_when_spec_updated(self):
        """No drift warning when SPEC.md updated date differs from created date."""
        repo_root = self.docs_dir.parent
        spec_content = "---\nid: SPEC\nstatus: active\ncreated: 2026-10-01\nupdated: 2026-10-02\n---\n# Spec"
        (repo_root / "SPEC.md").write_text(spec_content, encoding="utf-8")

        tasks_dir = self.docs_dir / "02_Tasks"
        tasks_dir.mkdir(parents=True, exist_ok=True)
        roadmap_content = (
            "# Roadmap\n\n"
            "## Фаза 1: First Phase — ✅ Завершена\n"
            "- [x] Task 1\n\n"
            "## Фаза 2: Second Phase — ✅ Завершена\n"
            "- [x] Task 2\n"
        )
        (tasks_dir / "Roadmap.md").write_text(roadmap_content, encoding="utf-8")

        warnings = kb_lint.check_spec_drift(self.docs_dir)
        self.assertEqual(len(warnings), 0)

        captured = io.StringIO()
        with patch("sys.stdout", captured):
            exit_code = kb_lint.run_linter(self.docs_dir, verbose=False)

        self.assertEqual(exit_code, 0)
        output = captured.getvalue()
        self.assertNotIn("Living Spec Drift", output)

    def test_spec_drift_no_warning_when_single_phase_completed(self):
        """No drift warning when only 1 phase is completed (threshold is >= 2)."""
        repo_root = self.docs_dir.parent
        spec_content = "---\nid: SPEC\nstatus: active\ncreated: 2026-10-01\nupdated: 2026-10-01\n---\n# Spec"
        (repo_root / "SPEC.md").write_text(spec_content, encoding="utf-8")

        tasks_dir = self.docs_dir / "02_Tasks"
        tasks_dir.mkdir(parents=True, exist_ok=True)
        roadmap_content = (
            "# Roadmap\n\n"
            "## Фаза 1: First Phase — ✅ Завершена\n"
            "- [x] Task 1\n\n"
            "## Фаза 2: Second Phase In Progress\n"
            "- [ ] Task 2\n"
        )
        (tasks_dir / "Roadmap.md").write_text(roadmap_content, encoding="utf-8")

        warnings = kb_lint.check_spec_drift(self.docs_dir)
        self.assertEqual(len(warnings), 0)

    def test_spec_drift_missing_spec_or_roadmap(self):
        """No drift warning if SPEC.md or Roadmap.md does not exist."""
        warnings = kb_lint.check_spec_drift(self.docs_dir)
        self.assertEqual(warnings, [])

    def test_spec_drift_verbose_mode(self):
        """Verbose mode should format spec drift warnings in a dedicated section."""
        repo_root = self.docs_dir.parent
        spec_content = "---\nid: SPEC\nstatus: active\ncreated: 2026-10-01\nupdated: 2026-10-01\n---\n# Spec"
        (repo_root / "SPEC.md").write_text(spec_content, encoding="utf-8")

        tasks_dir = self.docs_dir / "02_Tasks"
        tasks_dir.mkdir(parents=True, exist_ok=True)
        roadmap_content = (
            "# Roadmap\n\n"
            "## Phase 1: Alpha (Completed)\n"
            "- [x] Task 1\n\n"
            "## Phase 2: Beta (Completed)\n"
            "- [x] Task 2\n"
        )
        (tasks_dir / "Roadmap.md").write_text(roadmap_content, encoding="utf-8")

        captured = io.StringIO()
        with patch("sys.stdout", captured):
            exit_code = kb_lint.run_linter(self.docs_dir, verbose=True)

        self.assertEqual(exit_code, 0)
        output = captured.getvalue()
        self.assertIn("⚠️ Spec Drift Warnings (1):", output)
        self.assertIn("Living Spec Drift", output)

    def test_devlog_semantic_guard_detects_bare_trigger(self):
        """Bare 'Следующий шаг:' or 'Next Step:' triggers should produce non-blocking warnings."""
        devlog_content = (
            "# Devlog\n\n"
            "### [2026-10-03] — Task 1\n"
            "- **Что сделано:** Some work.\n"
            "- **Следующий шаг:** /kb-implement TASK-002\n\n"
            "### [2026-10-02] — Task 0\n"
            "- **Next Step:** /kb-implement TASK-001\n"
        )
        (self.docs_dir / "Devlog.md").write_text(devlog_content, encoding="utf-8")

        warnings = kb_lint.check_devlog_semantic_guard(self.docs_dir)
        self.assertEqual(len(warnings), 2)
        self.assertIn("line 5: bare step trigger detected", warnings[0])
        self.assertIn("line 8: bare step trigger detected", warnings[1])

    def test_devlog_semantic_guard_passes_with_guardrail(self):
        """Semantic guard with explicit user waiting markers should produce 0 warnings."""
        devlog_content = (
            "# Devlog\n\n"
            "### [2026-10-03] — Task 1\n"
            "- **Что сделано:** Some work.\n"
            "- **Рекомендуемый следующий шаг (Ожидает команды пользователя):** /kb-implement TASK-002\n\n"
            "### [2026-10-02] — Task 0\n"
            "- **Next Step (Awaits user command):** /kb-implement TASK-001\n"
        )
        (self.docs_dir / "Devlog.md").write_text(devlog_content, encoding="utf-8")

        warnings = kb_lint.check_devlog_semantic_guard(self.docs_dir)
        self.assertEqual(warnings, [])

    def test_devlog_semantic_guard_missing_file(self):
        """Returns empty list if Devlog.md does not exist."""
        warnings = kb_lint.check_devlog_semantic_guard(self.docs_dir)
        self.assertEqual(warnings, [])

    def test_devlog_semantic_guard_non_blocking_in_linter(self):
        """Devlog semantic warnings must be non-blocking (exit code 0) in both silent and verbose modes."""
        devlog_content = (
            "# Devlog\n\n"
            "- **Следующий шаг:** /kb-implement TASK-002\n"
        )
        (self.docs_dir / "Devlog.md").write_text(devlog_content, encoding="utf-8")

        # Silent mode
        captured_silent = io.StringIO()
        with patch("sys.stdout", captured_silent):
            exit_code = kb_lint.run_linter(self.docs_dir, verbose=False)
        self.assertEqual(exit_code, 0)
        self.assertIn("⚠️  WARN:", captured_silent.getvalue())

        # Verbose mode
        captured_verbose = io.StringIO()
        with patch("sys.stdout", captured_verbose):
            exit_code = kb_lint.run_linter(self.docs_dir, verbose=True)
        self.assertEqual(exit_code, 0)
        self.assertIn("⚠️ Devlog Semantic Guard Warnings (1):", captured_verbose.getvalue())


if __name__ == "__main__":
    unittest.main()
