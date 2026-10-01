#!/usr/bin/env python3
"""
Unit tests for scripts/kb_release.py (Release Automation Utility).
"""

import os
import sys
import tempfile
import unittest
import hashlib
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add scripts directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import kb_release


class TestKbRelease(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_inspect_release_artifacts_empty_and_nonexistent(self):
        # Non-existent dir
        artifacts = kb_release.inspect_release_artifacts(self.test_root / "dist_missing")
        self.assertEqual(artifacts, [])

        # Empty dir
        dist_dir = self.test_root / "dist"
        dist_dir.mkdir()
        artifacts = kb_release.inspect_release_artifacts(dist_dir)
        self.assertEqual(artifacts, [])

    def test_inspect_release_artifacts_calculation(self):
        dist_dir = self.test_root / "dist"
        dist_dir.mkdir()

        # Create dummy artifacts
        file1 = dist_dir / "app-v1.0.0.zip"
        content1 = b"Hello, this is a test payload for release!"
        file1.write_bytes(content1)
        expected_sha256 = hashlib.sha256(content1).hexdigest()

        # Hidden file (should be ignored)
        hidden_file = dist_dir / ".DS_Store"
        hidden_file.write_bytes(b"garbage")

        artifacts = kb_release.inspect_release_artifacts(dist_dir)
        self.assertEqual(len(artifacts), 1)
        art = artifacts[0]
        self.assertEqual(art["name"], "app-v1.0.0.zip")
        self.assertEqual(art["path"], "dist/app-v1.0.0.zip")
        self.assertEqual(art["sha256"], expected_sha256)
        self.assertTrue("KB" in art["size"] or "MB" in art["size"])

    def test_format_artifacts_markdown_table(self):
        # Empty
        table_empty = kb_release.format_artifacts_markdown_table([])
        self.assertIn("Source Release", table_empty)

        # Non-empty
        sample_artifacts = [{
            "name": "pkg.zip",
            "path": "dist/pkg.zip",
            "size": "1.50 MB",
            "sha256": "abcdef1234567890",
        }]
        table = kb_release.format_artifacts_markdown_table(sample_artifacts)
        self.assertIn("| `pkg.zip` | 1.50 MB | `abcdef1234567890` | `dist/pkg.zip` |", table)
        self.assertIn("Контрольная сумма (SHA-256)", table)

    def test_parse_frontmatter(self):
        content = """---
id: TASK-100
title: "Sample Task"
phase: 4
status: done
---
# Body
"""
        fm = kb_release.parse_frontmatter(content)
        self.assertEqual(fm.get("id"), "TASK-100")
        self.assertEqual(fm.get("title"), "Sample Task")
        self.assertEqual(fm.get("phase"), "4")
        self.assertEqual(fm.get("status"), "done")

    def test_find_phase_artifacts(self):
        docs_dir = self.test_root / "docs"
        specs_dir = docs_dir / "02_Tasks" / "Specs" / "04_TestPhase"
        bugs_dir = docs_dir / "02_Tasks" / "Bugs"
        adrs_dir = docs_dir / "03_Decisions_ADR"
        specs_dir.mkdir(parents=True)
        bugs_dir.mkdir(parents=True)
        adrs_dir.mkdir(parents=True)

        # Spec 1 (phase 4)
        (specs_dir / "TASK-041-feature.md").write_text(
            "---\nid: TASK-041\ntitle: Super Feature\nphase: 4\nstatus: done\n---\n# Feature",
            encoding="utf-8"
        )
        # Spec 2 (phase 3 - should not match)
        (specs_dir / "TASK-031-other.md").write_text(
            "---\nid: TASK-031\ntitle: Old Feature\nphase: 3\nstatus: done\n---\n# Old",
            encoding="utf-8"
        )
        # Bug (resolved)
        (bugs_dir / "BUG-001-fix.md").write_text(
            "---\nid: BUG-001\ntitle: Critical Fix\nstatus: closed\n---\n# Bug",
            encoding="utf-8"
        )
        # ADR (accepted)
        (adrs_dir / "ADR-0010-arch.md").write_text(
            "---\nid: ADR-0010\ntitle: Cool Architecture\nstatus: accepted\n---\n# ADR",
            encoding="utf-8"
        )

        found = kb_release.find_phase_artifacts(docs_dir, phase_num=4)
        self.assertEqual(len(found["tasks"]), 1)
        self.assertEqual(found["tasks"][0]["id"], "TASK-041")
        self.assertEqual(found["tasks"][0]["title"], "Super Feature")

        self.assertEqual(len(found["bugs"]), 1)
        self.assertEqual(found["bugs"][0]["id"], "BUG-001")

        self.assertEqual(len(found["adrs"]), 1)
        self.assertEqual(found["adrs"][0]["id"], "ADR-0010")

    def test_generate_release_markdown(self):
        env_info = {
            "has_git": True,
            "mode": "github",
            "remote_url": "https://github.com/myorg/myproject.git",
        }
        artifacts = [{
            "name": "app.zip",
            "path": "dist/app.zip",
            "size": "500 KB",
            "sha256": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        }]
        phase_data = {
            "tasks": [{"id": "TASK-001", "title": "Cool Task", "link": "../Specs/TASK-001"}],
            "bugs": [],
            "adrs": [],
        }

        md = kb_release.generate_release_markdown(
            version="1.0.0",
            phase_num=4,
            env_info=env_info,
            artifacts=artifacts,
            phase_data=phase_data,
            summary="Custom summary text",
            release_date="2026-10-01",
        )

        self.assertIn("id: RELEASE-v1.0.0", md)
        self.assertIn("version: \"1.0.0\"", md)
        self.assertIn("phase: 4", md)
        self.assertIn("mode: \"github\"", md)
        self.assertIn("github_release_url: \"https://github.com/myorg/myproject/releases/tag/v1.0.0\"", md)
        self.assertIn("Custom summary text", md)
        self.assertIn("[[../Specs/TASK-001|TASK-001]]: Cool Task.", md)
        self.assertIn("1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef", md)

    def test_detect_release_environment_structure(self):
        status = kb_release.detect_release_environment(Path.cwd())
        self.assertIn("has_git", status)
        self.assertIn("is_clean", status)
        self.assertIn("mode", status)
        self.assertIn(status["mode"], ["github", "local-only"])

    def test_cli_execution_with_dry_run_and_output(self):
        dist_dir = self.test_root / "dist"
        dist_dir.mkdir()
        (dist_dir / "dist.tar.gz").write_bytes(b"content")

        docs_dir = self.test_root / "docs"
        docs_dir.mkdir()

        out_file = self.test_root / "RELEASE-v0.5.0.md"

        # Mock sys.argv
        test_argv = [
            "kb_release.py",
            "--version", "0.5.0",
            "--phase", "4",
            "--dist-dir", str(dist_dir),
            "--docs-dir", str(docs_dir),
            "--output", str(out_file),
            "--summary", "Test CLI release summary",
        ]
        with patch.object(sys, "argv", test_argv):
            exit_code = kb_release.main()
            self.assertEqual(exit_code, 0)
            self.assertTrue(out_file.exists())
            content = out_file.read_text(encoding="utf-8")
            self.assertIn("Test CLI release summary", content)
            self.assertIn("dist.tar.gz", content)


if __name__ == "__main__":
    unittest.main()
