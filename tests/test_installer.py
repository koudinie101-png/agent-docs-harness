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

    def test_06_install_deploys_all_11_skills(self):
        """E2E test: Verify that all 11 AI agent skills (.agents/skills/) are deployed."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "SkillsApp"
            target.mkdir()

            install.install_harness(
                target_dir=target,
                project_name="SkillsApp",
                stack_key="generic",
                agent_choice="generic",
                git_choice="none",
                force=True,
            )

            skills_dir = target / ".agents" / "skills"
            self.assertTrue(skills_dir.is_dir(), ".agents/skills directory not found")

            expected_skills = [
                "docs-as-code",
                "kb-adr",
                "kb-bug",
                "kb-complete",
                "kb-implement",
                "kb-init",
                "kb-lint",
                "kb-onboard",
                "kb-plan",
                "kb-research",
                "kb-task",
            ]
            for skill_name in expected_skills:
                skill_file = skills_dir / skill_name / "SKILL.md"
                self.assertTrue(skill_file.is_file(), f"Missing skill file: {skill_file}")
                content = skill_file.read_text(encoding="utf-8")
                self.assertGreater(len(content), 100, f"Skill file {skill_file} is suspiciously empty")
                self.assertIn("name:", content)
                self.assertIn("description:", content)

    def test_07_install_gemini_and_windsurf_rules(self):
        """E2E test: Verify generation of GEMINI.md and .windsurfrules configurations."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # 1. Test agent_choice="all"
            target_all = Path(tmp_dir) / "AllAgentsApp"
            target_all.mkdir()
            install.install_harness(
                target_dir=target_all,
                project_name="AllAgentsApp",
                stack_key="python",
                agent_choice="all",
                git_choice="none",
                force=True,
            )

            gemini_md = target_all / "GEMINI.md"
            windsurf_rules = target_all / ".windsurfrules"
            self.assertTrue(gemini_md.is_file(), "GEMINI.md was not created under agent_choice='all'")
            self.assertTrue(windsurf_rules.is_file(), ".windsurfrules was not created under agent_choice='all'")

            gemini_content = gemini_md.read_text(encoding="utf-8")
            self.assertIn("Google Antigravity & Gemini CLI", gemini_content)
            self.assertIn("STRICTLY NO CODE CHANGES", gemini_content)
            self.assertIn("/kb-plan", gemini_content)

            windsurf_content = windsurf_rules.read_text(encoding="utf-8")
            self.assertIn("Windsurf Cascade", windsurf_content)
            self.assertIn("STRICTLY NO CODE CHANGES", windsurf_content)

            # 2. Test agent_choice="gemini"
            target_gemini = Path(tmp_dir) / "GeminiApp"
            target_gemini.mkdir()
            install.install_harness(
                target_dir=target_gemini,
                project_name="GeminiApp",
                stack_key="generic",
                agent_choice="gemini",
                git_choice="none",
                force=True,
            )
            self.assertTrue((target_gemini / "GEMINI.md").is_file())
            self.assertFalse((target_gemini / ".windsurfrules").is_file())

            # 3. Test agent_choice="windsurf"
            target_windsurf = Path(tmp_dir) / "WindsurfApp"
            target_windsurf.mkdir()
            install.install_harness(
                target_dir=target_windsurf,
                project_name="WindsurfApp",
                stack_key="generic",
                agent_choice="windsurf",
                git_choice="none",
                force=True,
            )
            self.assertTrue((target_windsurf / ".windsurfrules").is_file())
            self.assertFalse((target_windsurf / "GEMINI.md").is_file())

    def test_08_install_doc_lang_parameter(self):
        """E2E test: Verify --doc-lang parameter controls documentation language directives."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Russian doc language
            target_ru = Path(tmp_dir) / "LangRuApp"
            target_ru.mkdir()
            install.install_harness(
                target_dir=target_ru,
                project_name="LangRuApp",
                stack_key="generic",
                agent_choice="all",
                git_choice="none",
                doc_lang="ru",
                force=True,
            )
            agents_ru = (target_ru / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("Russian", agents_ru)

            # English doc language
            target_en = Path(tmp_dir) / "LangEnApp"
            target_en.mkdir()
            install.install_harness(
                target_dir=target_en,
                project_name="LangEnApp",
                stack_key="generic",
                agent_choice="all",
                git_choice="none",
                doc_lang="en",
                force=True,
            )
            agents_en = (target_en / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("English", agents_en)

            # Both pass kb_lint
            for target in [target_ru, target_en]:
                kb_lint_script = target / "scripts" / "kb_lint.py"
                res = subprocess.run(
                    [sys.executable, str(kb_lint_script), "--path", str(target / "docs")],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                )
                self.assertEqual(res.returncode, 0, f"kb_lint failed on {target.name}:\n{res.stdout}")

    def test_09_clean_slate_scaffolding(self):
        """E2E test: Verify clean slate scaffolding without phantom PLAN-001/TASK-001."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "CleanApp"
            target.mkdir()
            install.install_harness(
                target_dir=target,
                project_name="CleanApp",
                stack_key="python",
                agent_choice="all",
                git_choice="none",
                force=True,
            )

            # Check Kanban.md has clean backlog and no phantom tasks
            kanban_text = (target / "docs" / "02_Tasks" / "Kanban.md").read_text(encoding="utf-8")
            self.assertNotIn("PLAN-001-initial-mvp-setup", kanban_text)
            self.assertNotIn("TASK-001-project-scaffolding", kanban_text)
            self.assertIn("/kb-plan", kanban_text)

            # Check Roadmap.md has no phantom links
            roadmap_text = (target / "docs" / "02_Tasks" / "Roadmap.md").read_text(encoding="utf-8")
            self.assertNotIn("TASK-001-project-scaffolding", roadmap_text)

            # Check Plans and Specs dirs do not contain dummy files
            plans_dir = target / "docs" / "02_Tasks" / "Plans"
            self.assertFalse((plans_dir / "PLAN-001-initial-mvp-setup.md").exists())
            specs_dir = target / "docs" / "02_Tasks" / "Specs"
            self.assertFalse((specs_dir / "01_MVP" / "TASK-001-project-scaffolding.md").exists())

            # Check kb_lint passes with 0 broken links
            kb_lint_script = target / "scripts" / "kb_lint.py"
            res = subprocess.run(
                [sys.executable, str(kb_lint_script), "--path", str(target / "docs")],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(res.returncode, 0, f"kb_lint failed on clean slate installation:\n{res.stdout}")
            self.assertIn("No broken wikilinks found", res.stdout)

    def test_10_brownfield_adoption_and_stack_autodetect(self):
        """E2E test: Verify stack autodetect and non-destructive brownfield adoption."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            base = Path(tmp_dir)

            # 1. Test heuristic stack detection
            swift_dir = base / "swift_project"
            swift_dir.mkdir()
            (swift_dir / "Package.swift").write_text("// swift-tools-version:5.9", encoding="utf-8")
            self.assertEqual(install.detect_project_stack(swift_dir), "swift")

            ts_dir = base / "web_project"
            ts_dir.mkdir()
            (ts_dir / "package.json").write_text('{"name": "web-app"}', encoding="utf-8")
            self.assertEqual(install.detect_project_stack(ts_dir), "ts")

            py_dir = base / "python_project"
            py_dir.mkdir()
            (py_dir / "pyproject.toml").write_text('[project]\nname = "py-app"', encoding="utf-8")
            self.assertEqual(install.detect_project_stack(py_dir), "python")

            dotnet_dir = base / "dotnet_project"
            dotnet_dir.mkdir()
            (dotnet_dir / "App.csproj").write_text("<Project Sdk=\"Microsoft.NET.Sdk\" />", encoding="utf-8")
            self.assertEqual(install.detect_project_stack(dotnet_dir), "dotnet")

            generic_dir = base / "rust_project"
            generic_dir.mkdir()
            (generic_dir / "Cargo.toml").write_text('[package]\nname = "rust-app"', encoding="utf-8")
            self.assertEqual(install.detect_project_stack(generic_dir), "generic")

            # 2. Test brownfield adoption with existing README.md, .gitignore, and custom SPEC.md
            target = base / "brownfield_app"
            target.mkdir()
            (target / "package.json").write_text('{"name": "legacy-web"}', encoding="utf-8")

            custom_readme = "# My Legacy Web App\n\nExisting custom project documentation."
            (target / "README.md").write_text(custom_readme, encoding="utf-8")

            custom_gitignore = "node_modules/\n.env\ndist/\n"
            (target / ".gitignore").write_text(custom_gitignore, encoding="utf-8")

            custom_spec = "---\nid: SPEC\ntitle: Custom Legacy Spec\n---\n# Custom Legacy Spec\nExisting specification."
            (target / "SPEC.md").write_text(custom_spec, encoding="utf-8")

            # Run installation with auto-detected stack
            detected_stack = install.detect_project_stack(target)
            self.assertEqual(detected_stack, "ts")

            install.install_harness(
                target_dir=target,
                project_name="LegacyWebApp",
                stack_key=detected_stack,
                agent_choice="all",
                git_choice="none",
                doc_lang="ru",
                force=False,
            )

            # Check README.md: original text preserved, Docs-as-Code appended
            readme_after = (target / "README.md").read_text(encoding="utf-8")
            self.assertIn("My Legacy Web App", readme_after)
            self.assertIn("Existing custom project documentation.", readme_after)
            self.assertIn("Документация и дисциплина AI-агентов (Docs-as-Code)", readme_after)
            self.assertIn("AGENTS.md", readme_after)

            # Check .gitignore: original rules preserved, Obsidian rules appended
            gitignore_after = (target / ".gitignore").read_text(encoding="utf-8")
            self.assertIn("node_modules/", gitignore_after)
            self.assertIn(".obsidian/*", gitignore_after)
            self.assertIn("!.obsidian/graph.json", gitignore_after)

            # Check SPEC.md: custom user spec was NOT overwritten
            spec_after = (target / "SPEC.md").read_text(encoding="utf-8")
            self.assertEqual(spec_after, custom_spec)

            # Check Onboarding.md contains Section 7 (Brownfield Adoption)
            onboarding_after = (target / "docs" / "Onboarding.md").read_text(encoding="utf-8")
            self.assertIn("Внедрение в существующий проект (Brownfield Adoption)", onboarding_after)
            self.assertIn("Изучи кодовую базу репозитория", onboarding_after)

            # Test idempotency: re-running installation does not duplicate README or .gitignore blocks
            install.handle_readme(target, "LegacyWebApp", doc_lang="ru")
            install.handle_gitignore(target)
            readme_twice = (target / "README.md").read_text(encoding="utf-8")
            gitignore_twice = (target / ".gitignore").read_text(encoding="utf-8")
            self.assertEqual(readme_after, readme_twice)
            self.assertEqual(gitignore_after, gitignore_twice)

            # Check kb_lint passes
            kb_lint_script = target / "scripts" / "kb_lint.py"
            res = subprocess.run(
                [sys.executable, str(kb_lint_script), "--path", str(target / "docs")],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(res.returncode, 0, f"kb_lint failed on brownfield installation:\n{res.stdout}")
            self.assertIn("No broken wikilinks found", res.stdout)


if __name__ == "__main__":
    unittest.main()


