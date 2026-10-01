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


if __name__ == "__main__":
    unittest.main()
