#!/usr/bin/env python3
"""
Automated unit & E2E tests for agent-docs-harness.
Zero external dependencies (uses standard library unittest, tempfile, pathlib).
"""

import sys
import os
import shutil
import tempfile
import unittest
import subprocess
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import install


class TestAgentDocsHarness(unittest.TestCase):
    def test_01_assets_unpacking(self):
        """Verify embedded assets unpack all 12 templates, graph.json, and kb_lint.py."""
        assets = install.unpack_assets(REPO_ROOT)
        self.assertIn(".obsidian/graph.json", assets)
        self.assertIn("scripts/kb_lint.py", assets)

        expected_templates = [
            "TEMPLATE_ADR.md",
            "TEMPLATE_ARCHITECTURE.md",
            "TEMPLATE_BUG.md",
            "TEMPLATE_DEVLOG.md",
            "TEMPLATE_INDEX.md",
            "TEMPLATE_KANBAN.md",
            "TEMPLATE_ONBOARDING.md",
            "TEMPLATE_PLAN.md",
            "TEMPLATE_RESEARCH.md",
            "TEMPLATE_ROADMAP.md",
            "TEMPLATE_TASK.md",
            "TEMPLATE_TEST.md",
        ]
        for tpl in expected_templates:
            self.assertIn(f"00_Templates/{tpl}", assets, f"Missing template in bundle: {tpl}")

    def test_02_swift_stack_installation(self):
        """E2E test: Install Swift stack with all agent configs and verify with kb_lint."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "SwiftApp"
            target.mkdir()

            install.install_harness(
                target_dir=target,
                project_name="SwiftApp",
                stack_key="swift",
                agent_choice="all",
                git_choice="none",
                force=True,
            )

            # Check core files exist
            self.assertTrue((target / "SPEC.md").is_file())
            self.assertTrue((target / "AGENTS.md").is_file())
            self.assertTrue((target / ".clinerules").is_file())
            self.assertTrue((target / "CLAUDE.md").is_file())
            self.assertTrue((target / ".cursorrules").is_file())
            self.assertTrue((target / ".github" / "copilot-instructions.md").is_file())
            self.assertTrue((target / "scripts" / "kb_lint.py").is_file())
            self.assertTrue((target / "docs" / ".obsidian" / "graph.json").is_file())

            # Check Swift specific customizations
            agents_text = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("swift test", agents_text)
            self.assertIn("path/to/file.swift", agents_text)

            task_tpl = (target / "docs" / "00_Templates" / "TEMPLATE_TASK.md").read_text(encoding="utf-8")
            self.assertIn("ExampleServiceProtocol: Sendable", task_tpl)
            self.assertIn(".swift", task_tpl)

            # Run kb_lint.py on the generated docs
            kb_lint_script = target / "scripts" / "kb_lint.py"
            res = subprocess.run(
                [sys.executable, str(kb_lint_script), "--path", str(target / "docs")],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(res.returncode, 0, f"kb_lint failed on Swift installation:\n{res.stdout}\n{res.stderr}")
            self.assertIn("No broken wikilinks found", res.stdout)

    def test_03_typescript_stack_installation(self):
        """E2E test: Install TypeScript stack and verify kb_lint passes."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "WebProject"
            target.mkdir()

            install.install_harness(
                target_dir=target,
                project_name="WebProject",
                stack_key="ts",
                agent_choice="generic",
                git_choice="none",
                force=True,
            )

            agents_text = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("npm test", agents_text)
            self.assertIn(".ts", agents_text)

            kb_lint_script = target / "scripts" / "kb_lint.py"
            res = subprocess.run(
                [sys.executable, str(kb_lint_script), "--path", str(target / "docs")],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(res.returncode, 0, f"kb_lint failed on TS installation:\n{res.stdout}")

    def test_04_python_stack_installation(self):
        """E2E test: Install Python stack and verify kb_lint passes."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "PyProject"
            target.mkdir()

            install.install_harness(
                target_dir=target,
                project_name="PyProject",
                stack_key="python",
                agent_choice="claude",
                git_choice="none",
                force=True,
            )

            agents_text = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("pytest", agents_text)
            self.assertIn(".py", agents_text)

            kb_lint_script = target / "scripts" / "kb_lint.py"
            res = subprocess.run(
                [sys.executable, str(kb_lint_script), "--path", str(target / "docs")],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(res.returncode, 0, f"kb_lint failed on Python installation:\n{res.stdout}")

    def test_05_git_local_setup(self):
        """Verify local Git initialization and initial commit generation."""
        # Check if git is available
        git_cmd = shutil.which("git")
        if not git_cmd and sys.platform == "win32":
            win_path = r"C:\Program Files\Git\cmd\git.exe"
            if os.path.isfile(win_path):
                git_cmd = win_path

        if not git_cmd:
            self.skipTest("Git executable not found in test environment.")

        # Use a directory outside the current repo to avoid nested git ignore rules
        temp_base = tempfile.mkdtemp()
        try:
            target = Path(temp_base) / "GitApp"
            target.mkdir()

            install.install_harness(
                target_dir=target,
                project_name="GitApp",
                stack_key="generic",
                agent_choice="generic",
                git_choice="local",
                force=True,
            )

            self.assertTrue((target / ".git").is_dir(), ".git folder was not created")
            self.assertTrue((target / ".git" / "HEAD").is_file(), ".git/HEAD does not exist")

            git_env = os.environ.copy()
            git_env["GIT_DIR"] = str((target / ".git").resolve())
            git_env["GIT_WORK_TREE"] = str(target.resolve())

            # Verify commit was created
            res = subprocess.run(
                [git_cmd, "log", "-n", "1", "--oneline"],
                cwd=str(target),
                env=git_env,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(res.returncode, 0)
            self.assertIn("feat: initialize docs-as-code harness", res.stdout)
        finally:
            # Clean up read-only files on Windows
            for root, dirs, files in os.walk(temp_base, topdown=False):
                for f in files:
                    fp = os.path.join(root, f)
                    try:
                        os.chmod(fp, 0o777)
                        os.remove(fp)
                    except Exception:
                        pass
                for d in dirs:
                    dp = os.path.join(root, d)
                    try:
                        os.rmdir(dp)
                    except Exception:
                        pass
            try:
                os.rmdir(temp_base)
            except Exception:
                pass


if __name__ == "__main__":
    unittest.main()
