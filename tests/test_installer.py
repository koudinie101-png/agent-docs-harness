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
from unittest.mock import patch
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
        """Verify embedded assets unpack all 13 templates, graph.json, scripts, skills, and workflows."""
        assets = install.unpack_assets(REPO_ROOT)
        self.assertIn(".obsidian/graph.json", assets)
        self.assertIn("scripts/kb_lint.py", assets)
        self.assertIn("scripts/kb_release.py", assets)
        self.assertIn("scripts/kb_ingest.py", assets)
        self.assertIn(".agents/skills/kb-release/SKILL.md", assets)
        self.assertIn(".github/workflows/release.yml", assets)

        expected_templates = [
            "TEMPLATE_ADR.md",
            "TEMPLATE_ARCHITECTURE.md",
            "TEMPLATE_BUG.md",
            "TEMPLATE_DEVLOG.md",
            "TEMPLATE_FEEDBACK.md",
            "TEMPLATE_INDEX.md",
            "TEMPLATE_KANBAN.md",
            "TEMPLATE_ONBOARDING.md",
            "TEMPLATE_PLAN.md",
            "TEMPLATE_RELEASE.md",
            "TEMPLATE_RESEARCH.md",
            "TEMPLATE_ROADMAP.md",
            "TEMPLATE_TASK.md",
            "TEMPLATE_TASK_MICRO.md",
            "TEMPLATE_TEST.md",
        ]
        for tpl in expected_templates:
            self.assertIn(f"00_Templates/{tpl}", assets, f"Missing template in bundle: {tpl}")
        self.assertIn("docs/Zero_To_Hero_Guide.md", assets)

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
            self.assertIn("0 broken", res.stdout)

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
                "kb-adr",
                "kb-bug",
                "kb-complete",
                "kb-implement",
                "kb-init",
                "kb-lint",
                "kb-onboard",
                "kb-plan",
                "kb-release",
                "kb-research",
                "kb-task",
                "kb-triage",
            ]
            self.assertFalse((skills_dir / "docs-as-code").exists(), "docs-as-code should be consolidated into kb-onboard")
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
            self.assertIn("0 broken", res.stdout)

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
            self.assertIn("0 broken", res.stdout)

    def test_11_safe_update_mechanism(self):
        """E2E test: Verify safe update mechanism (--update) preserves user work and backs up modified rules."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            base = Path(tmp_dir)

            # 1. Non-project directory fails validation
            empty_dir = base / "empty_dir"
            empty_dir.mkdir()
            self.assertEqual(install.update_harness(empty_dir), 1)

            # 2. Initialize a valid project
            target = base / "UpdateApp"
            target.mkdir()
            install.install_harness(
                target_dir=target,
                project_name="UpdateApp",
                stack_key="python",
                agent_choice="all",
                git_choice="none",
                doc_lang="ru",
                force=True,
            )

            # 3. Simulate user data in tasks, Kanban, Roadmap, ADR, SPEC
            user_task = target / "docs" / "02_Tasks" / "Specs" / "01_MVP" / "TASK-099-user-feature.md"
            user_task.parent.mkdir(parents=True, exist_ok=True)
            user_task_content = "---\nid: TASK-099\ntitle: Custom User Task\nstatus: in-progress\ntype: task\nphase: 1\nparent_plan: PLAN-001\ncreated: 2026-10-15\n---\n# Custom User Feature"
            user_task.write_text(user_task_content, encoding="utf-8")

            kanban_path = target / "docs" / "02_Tasks" / "Kanban.md"
            kanban_orig = kanban_path.read_text(encoding="utf-8")
            kanban_custom = kanban_orig.replace("## ⏳ В работе (In Progress)", "## ⏳ В работе (In Progress)\n\n- [ ] [[Specs/01_MVP/TASK-099-user-feature|TASK-099]]: Custom User Task")
            kanban_path.write_text(kanban_custom, encoding="utf-8")

            adr_path = target / "docs" / "03_Decisions_ADR" / "ADR-0001-custom-db.md"
            adr_content = "---\nid: ADR-0001\ntitle: Custom DB Choice\nstatus: accepted\ncreated: 2026-10-15\n---\n# ADR-0001: Custom DB Choice"
            adr_path.write_text(adr_content, encoding="utf-8")

            # 4. Simulate outdated template and linter
            tpl_task_path = target / "docs" / "00_Templates" / "TEMPLATE_TASK.md"
            tpl_task_path.write_text("OUTDATED_TEMPLATE_CONTENT", encoding="utf-8")

            lint_path = target / "scripts" / "kb_lint.py"
            lint_path.write_text("# OUTDATED_LINTER_CONTENT", encoding="utf-8")

            # 5. Simulate modified AGENTS.md by user
            agents_path = target / "AGENTS.md"
            agents_orig = agents_path.read_text(encoding="utf-8")
            agents_modified = agents_orig + "\n## Custom Team Rule: Always wear hats\n"
            agents_path.write_text(agents_modified, encoding="utf-8")

            # 6. Execute update_harness (also testing CLI --update flag via subprocess)
            res = subprocess.run(
                [sys.executable, str(REPO_ROOT / "install.py"), "--update", "--target-dir", str(target)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(res.returncode, 0, f"install.py --update CLI failed:\n{res.stdout}\n{res.stderr}")
            self.assertIn("Harness components successfully updated", res.stdout)

            # 7. Verify templates and linter were refreshed
            self.assertNotEqual(tpl_task_path.read_text(encoding="utf-8"), "OUTDATED_TEMPLATE_CONTENT")
            self.assertIn("TASK-XXX", tpl_task_path.read_text(encoding="utf-8"))
            self.assertNotEqual(lint_path.read_text(encoding="utf-8"), "# OUTDATED_LINTER_CONTENT")
            self.assertIn("run_linter", lint_path.read_text(encoding="utf-8"))

            # 8. Verify user tasks, Kanban, and ADR were preserved untouched
            self.assertEqual(user_task.read_text(encoding="utf-8"), user_task_content)
            self.assertIn("TASK-099", kanban_path.read_text(encoding="utf-8"))
            self.assertEqual(adr_path.read_text(encoding="utf-8"), adr_content)

            # 9. Verify AGENTS.md was updated and AGENTS.md.bak was created with user customization
            bak_path = target / "AGENTS.md.bak"
            self.assertTrue(bak_path.is_file(), "AGENTS.md.bak was not created on update of modified rules!")
            self.assertIn("Custom Team Rule: Always wear hats", bak_path.read_text(encoding="utf-8"))

            # 10. Verify Devlog.md received update record
            devlog_content = (target / "docs" / "Devlog.md").read_text(encoding="utf-8")
            self.assertIn("install.py --update", devlog_content)
            self.assertIn("Обновление компонентов Docs-as-Code Harness", devlog_content)

            # 11. Verify kb_lint audit passes
            kb_lint_res = subprocess.run(
                [sys.executable, str(lint_path), "--path", str(target / "docs")],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(kb_lint_res.returncode, 0, f"kb_lint failed after update:\n{kb_lint_res.stdout}")
            self.assertIn("0 broken", kb_lint_res.stdout)

    def test_12_ci_workflow_generation_and_e2e(self):
        """E2E test: Verify GitHub Actions CI workflow generation (--ci github) and absence by default."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # 1. Test default: no CI workflow generated
            target_no_ci = Path(tmp_dir) / "NoCIApp"
            target_no_ci.mkdir()
            install.install_harness(
                target_dir=target_no_ci,
                project_name="NoCIApp",
                stack_key="python",
                agent_choice="generic",
                git_choice="none",
                ci_choice="none",
            )
            self.assertFalse((target_no_ci / ".github" / "workflows" / "kb-lint.yml").exists())

            # 2. Test with ci_choice="github" via install_harness
            target_ci = Path(tmp_dir) / "CIApp"
            target_ci.mkdir()
            install.install_harness(
                target_dir=target_ci,
                project_name="CIApp",
                stack_key="ts",
                agent_choice="all",
                git_choice="none",
                ci_choice="github",
            )
            ci_file = target_ci / ".github" / "workflows" / "kb-lint.yml"
            self.assertTrue(ci_file.is_file(), "kb-lint.yml was not created when ci_choice='github'!")
            ci_content = ci_file.read_text(encoding="utf-8")
            self.assertIn("Docs-as-Code Knowledge Base Audit", ci_content)
            self.assertIn("actions/checkout", ci_content)
            self.assertIn("actions/setup-python", ci_content)
            self.assertIn("python scripts/kb_lint.py --path docs", ci_content)

            # 3. Test CLI invocation with --ci github flag
            target_cli = Path(tmp_dir) / "CliCIApp"
            res = subprocess.run(
                [sys.executable, str(REPO_ROOT / "install.py"), "-y", "--target-dir", str(target_cli), "--ci", "github", "--stack", "generic", "--git", "none"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(res.returncode, 0, f"install.py --ci github failed:\n{res.stdout}\n{res.stderr}")
            self.assertTrue((target_cli / ".github" / "workflows" / "kb-lint.yml").is_file())
            self.assertIn("Deployed GitHub Actions CI workflow", res.stdout)

            # 4. Test update_harness refreshes existing CI workflow
            ci_cli_file = target_cli / ".github" / "workflows" / "kb-lint.yml"
            ci_cli_file.write_text("# OUTDATED_CI_WORKFLOW", encoding="utf-8")
            res_update = subprocess.run(
                [sys.executable, str(REPO_ROOT / "install.py"), "--update", "--target-dir", str(target_cli)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(res_update.returncode, 0, f"install.py --update failed on CI app:\n{res_update.stdout}")
            self.assertIn("actions/checkout", ci_cli_file.read_text(encoding="utf-8"))

    def test_13_release_components_deployed_on_fresh_install(self):
        """E2E test: Verify release infrastructure deployment (TEMPLATE_RELEASE.md, Releases/, kb_release.py, kb-release skill, release.yml)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "ReleaseApp"
            target.mkdir()

            install.install_harness(
                target_dir=target,
                project_name="ReleaseApp",
                stack_key="python",
                agent_choice="all",
                git_choice="none",
                ci_choice="github",
            )

            # 1. Verify docs/02_Tasks/Releases/ directory exists
            releases_dir = target / "docs" / "02_Tasks" / "Releases"
            self.assertTrue(releases_dir.is_dir(), "docs/02_Tasks/Releases directory was not created!")
            self.assertTrue((releases_dir / ".gitkeep").is_file(), ".gitkeep was not created in Releases/")

            # 2. Verify TEMPLATE_RELEASE.md template deployed
            tpl_release = target / "docs" / "00_Templates" / "TEMPLATE_RELEASE.md"
            self.assertTrue(tpl_release.is_file(), "TEMPLATE_RELEASE.md was not deployed to 00_Templates!")
            content_tpl = tpl_release.read_text(encoding="utf-8")
            self.assertIn("RELEASE-v[X.Y.Z]", content_tpl)
            self.assertIn("github_release_url", content_tpl)
            self.assertIn("sha256", content_tpl)

            # 3. Verify scripts/kb_release.py deployed
            kb_release = target / "scripts" / "kb_release.py"
            self.assertTrue(kb_release.is_file(), "scripts/kb_release.py was not deployed!")

            # 4. Verify kb-release skill deployed
            skill_md = target / ".agents" / "skills" / "kb-release" / "SKILL.md"
            self.assertTrue(skill_md.is_file(), ".agents/skills/kb-release/SKILL.md was not deployed!")
            content_skill = skill_md.read_text(encoding="utf-8")
            self.assertIn("/kb-release", content_skill)
            self.assertIn("Pre-flight Checks", content_skill)
            self.assertIn("--notes-file dist/RELEASE_NOTES.md", content_skill)

            # 5. Verify GitHub Actions release.yml deployed
            workflow_rel = target / ".github" / "workflows" / "release.yml"
            self.assertTrue(workflow_rel.is_file(), ".github/workflows/release.yml was not deployed with --ci github!")
            content_wf = workflow_rel.read_text(encoding="utf-8")
            self.assertIn("Release Automation", content_wf)
            self.assertIn("kb_release.py", content_wf)
            self.assertIn("body_path: dist/RELEASE_NOTES.md", content_wf)

            # 6. Verify GEMINI.md references /kb-release
            gemini_md = target / "GEMINI.md"
            self.assertTrue(gemini_md.is_file())
            self.assertIn("/kb-release", gemini_md.read_text(encoding="utf-8"))

            # 7. Audit with kb_lint.py
            lint_script = target / "scripts" / "kb_lint.py"
            res = subprocess.run(
                [sys.executable, str(lint_script), "--path", str(target / "docs")],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(res.returncode, 0, f"kb_lint failed on release components:\n{res.stdout}\n{res.stderr}")

    def test_14_kb_release_utility_execution_in_sandbox(self):
        """E2E test: Execute scripts/kb_release.py in deployed sandbox and verify generated release note and SHA-256."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "SandboxApp"
            target.mkdir()

            install.install_harness(
                target_dir=target,
                project_name="SandboxApp",
                stack_key="python",
                agent_choice="generic",
                git_choice="none",
                ci_choice="none",
            )

            # 1. Create a dummy artifact in dist/
            dist_dir = target / "dist"
            dist_dir.mkdir(parents=True, exist_ok=True)
            dummy_pkg = dist_dir / "sandboxapp-1.0.0.tar.gz"
            dummy_pkg.write_bytes(b"TEST_BINARY_PAYLOAD_FOR_HASHING_12345")

            # 2. Create a mock completed task in docs/02_Tasks/Specs/01_MVP/
            spec_dir = target / "docs" / "02_Tasks" / "Specs" / "01_MVP"
            spec_dir.mkdir(parents=True, exist_ok=True)
            mock_task = spec_dir / "TASK-001-init.md"
            mock_task.write_text(
                "---\n"
                "id: TASK-001\n"
                "title: \"Project Initialization\"\n"
                "status: done\n"
                "type: task\n"
                "phase: 1\n"
                "parent_plan: PLAN-001\n"
                "created: 2026-10-15\n"
                "---\n\n"
                "# TASK-001: Project Initialization\n",
                encoding="utf-8"
            )

            # 3. Execute deployed scripts/kb_release.py via subprocess
            release_script = target / "scripts" / "kb_release.py"
            res = subprocess.run(
                [
                    sys.executable,
                    str(release_script),
                    "--version", "v1.0.0",
                    "--phase", "1",
                    "--dist-dir", str(dist_dir),
                    "--docs-dir", str(target / "docs"),
                ],
                cwd=str(target),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(res.returncode, 0, f"kb_release.py execution failed:\n{res.stdout}\n{res.stderr}")
            self.assertIn("Release v1.0.0 generated at", res.stdout)

            # 4. Verify release file generated in docs/02_Tasks/Releases/
            release_file = target / "docs" / "02_Tasks" / "Releases" / "RELEASE-v1.0.0.md"
            self.assertTrue(release_file.is_file(), "RELEASE-v1.0.0.md was not generated!")
            release_text = release_file.read_text(encoding="utf-8")
            self.assertIn("id: RELEASE-v1.0.0", release_text)
            self.assertIn("version: \"1.0.0\"", release_text)
            self.assertIn("sandboxapp-1.0.0.tar.gz", release_text)
            self.assertIn("TASK-001", release_text)

            # Calculate expected SHA-256
            import hashlib
            expected_hash = hashlib.sha256(b"TEST_BINARY_PAYLOAD_FOR_HASHING_12345").hexdigest()
            self.assertIn(expected_hash, release_text, "Calculated SHA-256 hash not found in release note table!")

            # 4.1. Verify public release notes generated in dist/
            notes_file = dist_dir / "RELEASE_NOTES.md"
            self.assertTrue(notes_file.is_file(), "dist/RELEASE_NOTES.md was not generated!")
            notes_text = notes_file.read_text(encoding="utf-8")
            self.assertIn("# 🚀 Release v1.0.0", notes_text)
            self.assertIn(expected_hash, notes_text)
            self.assertFalse(notes_text.strip().startswith("---"))

            # 5. Verify knowledge base integrity with kb_lint
            lint_script = target / "scripts" / "kb_lint.py"
            lint_res = subprocess.run(
                [sys.executable, str(lint_script), "--path", str(target / "docs")],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(lint_res.returncode, 0, f"kb_lint failed on generated release doc:\n{lint_res.stdout}\n{lint_res.stderr}")

    def test_15_update_preserves_existing_releases(self):
        """E2E test: Verify that install.py --update refreshes templates/skills while preserving user releases in docs/02_Tasks/Releases/."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "UpdateReleaseApp"
            target.mkdir()

            install.install_harness(
                target_dir=target,
                project_name="UpdateReleaseApp",
                stack_key="python",
                agent_choice="all",
                git_choice="none",
            )

            # 1. Create custom user release document
            user_rel = target / "docs" / "02_Tasks" / "Releases" / "RELEASE-v0.1.0.md"
            user_rel_content = (
                "---\n"
                "id: RELEASE-v0.1.0\n"
                "title: \"Custom User Release v0.1.0\"\n"
                "version: \"0.1.0\"\n"
                "phase: 1\n"
                "status: completed\n"
                "---\n\n"
                "# Custom User Release Document\n\n"
                "DO_NOT_OVERWRITE_THIS_USER_RELEASE_NOTE_12345\n"
            )
            user_rel.write_text(user_rel_content, encoding="utf-8")

            # 2. Simulate outdated TEMPLATE_RELEASE.md and outdated scripts/kb_release.py
            tpl_rel = target / "docs" / "00_Templates" / "TEMPLATE_RELEASE.md"
            tpl_rel.write_text("# OUTDATED_TEMPLATE_RELEASE", encoding="utf-8")

            script_rel = target / "scripts" / "kb_release.py"
            script_rel.write_text("# OUTDATED_KB_RELEASE_SCRIPT", encoding="utf-8")

            # 3. Run install.py --update via CLI
            res = subprocess.run(
                [sys.executable, str(REPO_ROOT / "install.py"), "--update", "--target-dir", str(target)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(res.returncode, 0, f"install.py --update failed:\n{res.stdout}\n{res.stderr}")

            # 4. Verify user release note was preserved untouched!
            self.assertTrue(user_rel.is_file())
            self.assertEqual(user_rel.read_text(encoding="utf-8"), user_rel_content)
            self.assertIn("DO_NOT_OVERWRITE_THIS_USER_RELEASE_NOTE_12345", user_rel.read_text(encoding="utf-8"))

            # 5. Verify TEMPLATE_RELEASE.md and scripts/kb_release.py were updated
            self.assertNotEqual(tpl_rel.read_text(encoding="utf-8"), "# OUTDATED_TEMPLATE_RELEASE")
            self.assertIn("RELEASE-v[X.Y.Z]", tpl_rel.read_text(encoding="utf-8"))
            self.assertNotEqual(script_rel.read_text(encoding="utf-8"), "# OUTDATED_KB_RELEASE_SCRIPT")
            self.assertIn("inspect_release_artifacts", script_rel.read_text(encoding="utf-8"))
            self.assertIn("convert_wikilinks_to_github_markdown", script_rel.read_text(encoding="utf-8"))
            self.assertIn("generate_public_release_notes", script_rel.read_text(encoding="utf-8"))

            # 6. Verify kb_lint check passes
            lint_script = target / "scripts" / "kb_lint.py"
            lint_res = subprocess.run(
                [sys.executable, str(lint_script), "--path", str(target / "docs")],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(lint_res.returncode, 0, f"kb_lint failed after update:\n{lint_res.stdout}\n{lint_res.stderr}")

    def test_16_high_snr_static_corpus_benchmarks(self):
        """E2E benchmark test: Verify deployed skills and templates stay strictly within High-SNR token budget (ADR-0009)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "BenchmarkApp"
            target.mkdir()

            install.install_harness(
                target_dir=target,
                project_name="BenchmarkApp",
                stack_key="python",
                agent_choice="all",
                git_choice="none",
                force=True,
            )

            skills_dir = target / ".agents" / "skills"
            templates_dir = target / "docs" / "00_Templates"

            total_skills_size = sum(f.stat().st_size for f in skills_dir.rglob("*.md"))
            total_templates_size = sum(f.stat().st_size for f in templates_dir.glob("*.md"))

            # Benchmark assertions (ADR-0009 constraints for 12 skills + 16 templates + Living Spec + Guardrails + Spec Genesis + Bug Lifecycle + Feedback Ingestion + Fast-Track + Memory Checkpoints)
            self.assertLessEqual(total_skills_size, 30000, f"Skills size exceeded budget: {total_skills_size} bytes (budget <= 30000)")
            self.assertLessEqual(total_templates_size, 28000, f"Templates size exceeded budget: {total_templates_size} bytes (budget <= 28000)")

            # Micro-benchmarks for critical files
            onboarding_size = (templates_dir / "TEMPLATE_ONBOARDING.md").stat().st_size
            self.assertLessEqual(onboarding_size, 5000, f"TEMPLATE_ONBOARDING.md exceeded budget: {onboarding_size} bytes (budget <= 5000)")

            router_size = (skills_dir / "kb-onboard" / "SKILL.md").stat().st_size
            self.assertLessEqual(router_size, 3000, f"kb-onboard hub exceeded budget: {router_size} bytes (budget <= 3000)")

            # Installer size check (budget <= 160 KB for Phase 18 with 16 templates, 12 skills, 3 standalone scripts, memory patterns, UI harness)
            installer_size = (REPO_ROOT / "install.py").stat().st_size
            self.assertLessEqual(installer_size, 160000, f"install.py exceeded budget: {installer_size} bytes (budget <= 160 KB)")

    def test_17_update_migrates_to_skeleton_templates_and_high_snr_skills(self):
        """E2E test: Verify install.py --update updates old bloated templates/skills to compact High-SNR versions."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "BloatedLegacyApp"
            target.mkdir()

            install.install_harness(
                target_dir=target,
                project_name="BloatedLegacyApp",
                stack_key="python",
                agent_choice="all",
                git_choice="none",
                force=True,
            )

            # Simulate bloated old template (> 10 KB) and bloated router skill (> 10 KB)
            bloated_tpl = target / "docs" / "00_Templates" / "TEMPLATE_ONBOARDING.md"
            bloated_tpl.write_text("# Bloated Onboarding Essay\n" + ("Lots of tokens here...\n" * 500), encoding="utf-8")
            self.assertGreater(bloated_tpl.stat().st_size, 10000)

            bloated_router = target / ".agents" / "skills" / "kb-onboard" / "SKILL.md"
            bloated_router.write_text("# Bloated Router\n" + ("Lots of documentation text...\n" * 500), encoding="utf-8")
            self.assertGreater(bloated_router.stat().st_size, 10000)

            # Run update
            res = install.update_harness(target, backup=False)
            self.assertEqual(res, 0)

            # Verify both files shrunk to compact High-SNR sizes
            self.assertLessEqual(bloated_tpl.stat().st_size, 5000)
            self.assertLessEqual(bloated_router.stat().st_size, 3000)

    def test_18_discovery_mode_and_phase6_assets(self):
        """Verify Mode 0 (Discovery) rules in unpacked skills, roadmap template, and onboarding."""
        assets = install.unpack_assets(REPO_ROOT)

        # Check kb-research skill contains Mode 0 and outcome routing
        kb_research_skill = assets.get(".agents/skills/kb-research/SKILL.md", "")
        self.assertIn("Mode 0: Discovery & Feasibility Research", kb_research_skill)
        self.assertIn("Automated Outcome Routing", kb_research_skill)
        self.assertIn("Critical Partner & Falsification", kb_research_skill)

        # Check kb-plan skill contains pre-flight nudge
        kb_plan_skill = assets.get(".agents/skills/kb-plan/SKILL.md", "")
        self.assertIn("Pre-flight Nudge", kb_plan_skill)

        # Check kb-onboard skill contains Mode 0
        kb_onboard_skill = assets.get(".agents/skills/kb-onboard/SKILL.md", "")
        self.assertIn("Mode 0", kb_onboard_skill)

        # Check TEMPLATE_ROADMAP contains rejected alternatives section and icebox tip
        roadmap_tpl = assets.get("00_Templates/TEMPLATE_ROADMAP.md", "")
        self.assertIn("Отклоненные архитектурные идеи", roadmap_tpl)
        self.assertIn("kb-research", roadmap_tpl)

        # Check TEMPLATE_ONBOARDING contains Mode 0
        onboarding_tpl = assets.get("00_Templates/TEMPLATE_ONBOARDING.md", "")
        self.assertIn("Режим 0: Исследование", onboarding_tpl)

        # Verify fresh installation in temp directory deploys all updated Mode 0 assets
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "DiscoveryTestApp"
            target.mkdir()

            install.install_harness(
                target_dir=target,
                project_name="DiscoveryTestApp",
                stack_key="generic",
                agent_choice="all",
                git_choice="none",
                force=True,
            )

            # Check installed files
            inst_research = (target / ".agents" / "skills" / "kb-research" / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("Mode 0: Discovery & Feasibility Research", inst_research)

            inst_onboard = (target / "docs" / "Onboarding.md").read_text(encoding="utf-8")
            self.assertIn("Режим 0", inst_onboard)

            inst_roadmap_tpl = (target / "docs" / "00_Templates" / "TEMPLATE_ROADMAP.md").read_text(encoding="utf-8")
            self.assertIn("Отклоненные архитектурные идеи", inst_roadmap_tpl)

    def test_19_undecided_preset_and_idea_flag(self):
        """Verify undecided preset, --idea CLI flag, SPEC.md discovery status, and kb_lint verification."""
        self.assertIn("undecided", install.STACK_PRESETS)
        undecided_info = install.STACK_PRESETS["undecided"]
        self.assertEqual(undecided_info["name"], "Undecided / Idea-First Research")

        # 1. Direct Python call to install_harness with stack_key="undecided" and idea
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "IdeaProject"
            target.mkdir()

            install.install_harness(
                target_dir=target,
                project_name="IdeaProject",
                stack_key="undecided",
                agent_choice="all",
                git_choice="none",
                force=True,
                idea="Smart Battery Monitoring Daemon for Desktop",
            )

            # Check SPEC.md
            spec_path = target / "SPEC.md"
            self.assertTrue(spec_path.is_file())
            spec_content = spec_path.read_text(encoding="utf-8")
            self.assertIn("status: discovery", spec_content)
            self.assertIn("Smart Battery Monitoring Daemon for Desktop", spec_content)
            self.assertIn("Не определен. Требуется провести первичное исследование", spec_content)
            self.assertIn("/kb-research", spec_content)

            # Check AGENTS.md
            agents_path = target / "AGENTS.md"
            self.assertTrue(agents_path.is_file())
            agents_content = agents_path.read_text(encoding="utf-8")
            self.assertIn("Undecided / Idea-First Research", agents_content)

            # Run kb_lint
            kb_lint_script = target / "scripts" / "kb_lint.py"
            res = subprocess.run(
                [sys.executable, str(kb_lint_script), "--path", str(target / "docs")],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(res.returncode, 0, f"kb_lint failed: {res.stdout}\n{res.stderr}")

        # 2. CLI subprocess execution with --idea flag without --stack
        with tempfile.TemporaryDirectory() as tmp_dir2:
            target2 = Path(tmp_dir2) / "CliIdeaProject"
            target2.mkdir()

            cli_res = subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "install.py"),
                    "-y",
                    "-d",
                    str(target2),
                    "--idea",
                    "Offline Local-First Encrypted Vault",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(cli_res.returncode, 0, f"CLI install failed: {cli_res.stdout}\n{cli_res.stderr}")
            self.assertIn("Undecided / Idea-First Research", cli_res.stdout)
            self.assertIn("Mode 0: /kb-research", cli_res.stdout)

            spec_path2 = target2 / "SPEC.md"
            self.assertTrue(spec_path2.is_file())
            spec_content2 = spec_path2.read_text(encoding="utf-8")
            self.assertIn("status: discovery", spec_content2)
            self.assertIn("Offline Local-First Encrypted Vault", spec_content2)

            # Check all 12 skills deployed
            skills_dir2 = target2 / ".agents" / "skills"
            self.assertTrue(skills_dir2.is_dir())
            skill_subdirs = [d for d in skills_dir2.iterdir() if d.is_dir()]
            self.assertEqual(len(skill_subdirs), 12)

            # Run kb_lint on installed project
            kb_lint_res = subprocess.run(
                [sys.executable, str(target2 / "scripts" / "kb_lint.py"), "--path", str(target2 / "docs")],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(kb_lint_res.returncode, 0, f"kb_lint failed: {kb_lint_res.stdout}\n{kb_lint_res.stderr}")
            self.assertIn("OK:", kb_lint_res.stdout)

    def test_20_single_task_barrier_and_stop_on_complete(self):
        """Verify Single-Task Execution Barrier and Stop & Yield protocol across rule generators, skills, and --update."""
        # 1. Rule generators checks
        agents_content = install.generate_agents_md("TestApp", "generic", "ru")
        self.assertIn("13. Single-Task Barrier", agents_content)
        self.assertIn("Single-Task Execution Barrier (No Auto-Chaining)", agents_content)
        self.assertIn("STOP tool calls (Stop & Yield)", agents_content)

        for gen_fn in [
            install.generate_gemini_md,
            install.generate_windsurfrules,
            install.generate_clinerules,
            install.generate_claude_md,
            install.generate_cursorrules,
            install.generate_copilot_instructions,
        ]:
            out = gen_fn("TestApp", "generic", "ru")
            self.assertIn("Anti-Echo & Single-Task Barrier", out)
            self.assertIn("Stop & Yield", out)
            self.assertIn("AGENTS.md", out)

        # 2. Fresh installation check: skill contents and Devlog template
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "BarrierApp"
            target.mkdir()

            install.install_harness(
                target_dir=target,
                project_name="BarrierApp",
                stack_key="python",
                agent_choice="all",
                git_choice="none",
                force=True,
            )

            # Check skills
            kb_impl = (target / ".agents" / "skills" / "kb-implement" / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("Single-Task Barrier", kb_impl)
            self.assertIn("Never auto-chain", kb_impl)
            self.assertIn("STOP calling tools and yield control", kb_impl)

            kb_comp = (target / ".agents" / "skills" / "kb-complete" / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("Single-Task Barrier", kb_comp)
            self.assertIn("Stop & Yield Control", kb_comp)
            self.assertIn("Рекомендуемый следующий шаг (Ожидает команды пользователя)", kb_comp)

            # Check devlog template
            devlog_tpl = (target / "docs" / "00_Templates" / "TEMPLATE_DEVLOG.md").read_text(encoding="utf-8")
            self.assertIn("Рекомендуемый следующий шаг (Ожидает команды пользователя)", devlog_tpl)

            # 3. Simulate existing outdated project and test --update
            # Overwrite skills and AGENTS.md with dummy legacy versions
            (target / "AGENTS.md").write_text("Legacy AGENTS content without barrier", encoding="utf-8")
            (target / ".agents" / "skills" / "kb-implement" / "SKILL.md").write_text("Legacy kb-implement", encoding="utf-8")

            # Run install.py --update via CLI
            update_res = subprocess.run(
                [sys.executable, str(REPO_ROOT / "install.py"), "--update", "-d", str(target)],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(update_res.returncode, 0, f"Update failed: {update_res.stdout}\n{update_res.stderr}")

            # Verify backup created and AGENTS.md updated
            self.assertTrue((target / "AGENTS.md.bak").is_file())
            self.assertEqual((target / "AGENTS.md.bak").read_text(encoding="utf-8"), "Legacy AGENTS content without barrier")
            updated_agents = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("Single-Task Execution Barrier (No Auto-Chaining)", updated_agents)

            # Verify skill was refreshed
            updated_kb_impl = (target / ".agents" / "skills" / "kb-implement" / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("Single-Task Barrier", updated_kb_impl)

            # Verify Devlog updated with semantic marker
            devlog_content = (target / "docs" / "Devlog.md").read_text(encoding="utf-8")
            self.assertIn("Рекомендуемый следующий шаг (Ожидает команды пользователя)", devlog_content)

            # Verify kb_lint passes with 0 warnings
            kb_lint_res = subprocess.run(
                [sys.executable, str(target / "scripts" / "kb_lint.py"), "--path", str(target / "docs")],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(kb_lint_res.returncode, 0, f"kb_lint failed: {kb_lint_res.stdout}\n{kb_lint_res.stderr}")
            self.assertIn("OK:", kb_lint_res.stdout)
            self.assertNotIn("WARN: Devlog Semantic Guard", kb_lint_res.stdout)

    def test_21_spec_genesis_and_high_snr_release_notes(self):
        """Verify Spec Genesis guardrails, Zero-State rules, High-SNR release notes, and phase ADR scoping in installer & --update."""
        # 1. Rule generators verification
        agents_content = install.generate_agents_md("TestApp", "generic", "ru")
        self.assertIn("14. Zero-State & Spec Genesis", agents_content)
        self.assertIn("Zero-State Anti-Hallucination & Spec Genesis", agents_content)
        self.assertIn("6. Zero-State Anti-Hallucination & Spec Genesis", agents_content)
        self.assertIn("## Docs-as-Code (19 Disciplines)", agents_content)
        self.assertIn("Mode 0: Discovery & Feasibility", agents_content)
        self.assertIn("Mode 2C: Feedback Triage & Dispatch", agents_content)

        for gen_fn in [
            install.generate_gemini_md,
            install.generate_windsurfrules,
            install.generate_clinerules,
            install.generate_claude_md,
            install.generate_cursorrules,
            install.generate_copilot_instructions,
        ]:
            out = gen_fn("TestApp", "generic", "ru")
            self.assertIn("AGENTS.md", out)
            self.assertIn("Read `AGENTS.md`", out)

        # 2. Fresh installation check (preset undecided / --idea)
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "GenesisApp"
            target.mkdir()

            install.install_harness(
                target_dir=target,
                project_name="GenesisApp",
                stack_key="undecided",
                agent_choice="all",
                git_choice="none",
                force=True,
                idea="Cloud AI Video Editor",
            )

            # Check SPEC.md created with discovery status
            spec_path = target / "SPEC.md"
            self.assertTrue(spec_path.is_file())
            spec_content = spec_path.read_text(encoding="utf-8")
            self.assertIn("status: discovery", spec_content)
            self.assertIn("Cloud AI Video Editor", spec_content)

            # 3. Simulate existing outdated project and test --update
            # Overwrite skills, templates, scripts, AGENTS.md with dummy legacy versions
            (target / "AGENTS.md").write_text("Legacy AGENTS content without spec genesis", encoding="utf-8")
            (target / ".agents" / "skills" / "kb-init" / "SKILL.md").write_text("Legacy kb-init", encoding="utf-8")
            (target / ".agents" / "skills" / "kb-plan" / "SKILL.md").write_text("Legacy kb-plan", encoding="utf-8")
            (target / ".agents" / "skills" / "kb-task" / "SKILL.md").write_text("Legacy kb-task", encoding="utf-8")
            (target / ".agents" / "skills" / "kb-release" / "SKILL.md").write_text("Legacy kb-release", encoding="utf-8")
            (target / "scripts" / "kb_release.py").write_text("# Legacy kb_release", encoding="utf-8")

            # Run install.py --update via CLI
            update_res = subprocess.run(
                [sys.executable, str(REPO_ROOT / "install.py"), "--update", "-d", str(target)],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(update_res.returncode, 0, f"Update failed: {update_res.stdout}\n{update_res.stderr}")

            # Verify backup created and AGENTS.md updated with Spec Genesis
            self.assertTrue((target / "AGENTS.md.bak").is_file())
            updated_agents = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("Zero-State Anti-Hallucination & Spec Genesis", updated_agents)

            # Verify skills refreshed
            updated_kb_init = (target / ".agents" / "skills" / "kb-init" / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("SPEC.md", updated_kb_init)
            self.assertIn("status: discovery", updated_kb_init)

            updated_kb_plan = (target / ".agents" / "skills" / "kb-plan" / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("Zero-State Guard", updated_kb_plan)

            updated_kb_task = (target / ".agents" / "skills" / "kb-task" / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("Zero-State", updated_kb_task)

            updated_kb_release_skill = (target / ".agents" / "skills" / "kb-release" / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("High-SNR", updated_kb_release_skill)

            # Verify scripts/kb_release.py refreshed
            updated_kb_release_py = (target / "scripts" / "kb_release.py").read_text(encoding="utf-8")
            self.assertIn("is_adr_for_phase", updated_kb_release_py)

            # 4. Test release note generation in updated sandbox
            # Create a mock phase task and an ADR
            task_dir = target / "docs" / "02_Tasks" / "Specs" / "01_MVP"
            task_dir.mkdir(parents=True, exist_ok=True)
            (task_dir / "TASK-001-setup.md").write_text(
                "---\nid: TASK-001\ntitle: MVP Setup\nstatus: done\ntype: task\nphase: 1\nparent_plan: PLAN-001\ncreated: 2026-10-15\n---\n# TASK-001: MVP Setup\n",
                encoding="utf-8"
            )
            adr_dir = target / "docs" / "03_Decisions_ADR"
            adr_dir.mkdir(parents=True, exist_ok=True)
            (adr_dir / "ADR-0001-init.md").write_text(
                "---\nid: ADR-0001\ntitle: Initial Stack\nstatus: accepted\nphase: 1\ncreated: 2026-10-15\n---\n# ADR-0001: Initial Stack\n",
                encoding="utf-8"
            )

            # Run kb_release.py in target sandbox
            rel_res = subprocess.run(
                [sys.executable, str(target / "scripts" / "kb_release.py"), "--version", "v0.1.0", "--phase", "1"],
                cwd=str(target),
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(rel_res.returncode, 0, f"kb_release failed: {rel_res.stdout}\n{rel_res.stderr}")

            # Verify dist/RELEASE_NOTES.md exists and EXCLUDES ADR section (High-SNR)
            dist_notes = target / "dist" / "RELEASE_NOTES.md"
            self.assertTrue(dist_notes.is_file())
            dist_notes_txt = dist_notes.read_text(encoding="utf-8")
            self.assertNotIn("Архитектурные решения (ADR)", dist_notes_txt)
            self.assertNotIn("ADR-0001", dist_notes_txt)
            self.assertIn("MVP Setup", dist_notes_txt)

            # Verify docs/02_Tasks/Releases/RELEASE-v0.1.0.md exists and INCLUDES phase ADR
            internal_notes = target / "docs" / "02_Tasks" / "Releases" / "RELEASE-v0.1.0.md"
            self.assertTrue(internal_notes.is_file())
            internal_notes_txt = internal_notes.read_text(encoding="utf-8")
            self.assertIn("Архитектурные решения (ADR)", internal_notes_txt)
            self.assertIn("ADR-0001", internal_notes_txt)

            # 5. Verify kb_lint passes
            kb_lint_res = subprocess.run(
                [sys.executable, str(target / "scripts" / "kb_lint.py"), "--path", str(target / "docs")],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(kb_lint_res.returncode, 0, f"kb_lint failed: {kb_lint_res.stdout}\n{kb_lint_res.stderr}")
            self.assertIn("OK:", kb_lint_res.stdout)


    def test_22_bug_lifecycle_and_phase11_assets(self):
        """E2E test: Verify Phase 11 Bug Lifecycle, TDD implementation, triage Mode 2B, and release targeting."""
        # 1. Rule generators verification
        agents_content = install.generate_agents_md("BugTestApp", "generic", "ru")
        self.assertIn("Mode 2B -- Defect Triage (`/kb-bug`)", agents_content)
        self.assertIn("/kb-implement <TASK-XXX | BUG-XXX>", agents_content)
        self.assertIn("RED -> GREEN -> REFACTOR", agents_content)

        for gen_fn in [
            install.generate_gemini_md,
            install.generate_windsurfrules,
            install.generate_clinerules,
            install.generate_claude_md,
            install.generate_cursorrules,
            install.generate_copilot_instructions,
        ]:
            out = gen_fn("BugTestApp", "generic", "ru")
            self.assertIn("2B (`/kb-bug`)", out)
            self.assertIn("/kb-implement <TASK-XXX | BUG-XXX>", out)

        # 2. Fresh installation check
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "BugLifecycleApp"
            target.mkdir()

            install.install_harness(
                target_dir=target,
                project_name="BugLifecycleApp",
                stack_key="python",
                agent_choice="all",
                git_choice="none",
                force=True,
            )

            # Check TEMPLATE_BUG.md frontmatter attributes
            bug_tpl = (target / "docs" / "00_Templates" / "TEMPLATE_BUG.md").read_text(encoding="utf-8")
            self.assertIn("target_release:", bug_tpl)
            self.assertIn("target_phase:", bug_tpl)
            self.assertIn("release_blocker:", bug_tpl)
            self.assertIn("fixed_in:", bug_tpl)
            self.assertIn("regression_test:", bug_tpl)

            # Check skills deployed
            kb_bug_skill = (target / ".agents" / "skills" / "kb-bug" / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("target_release", kb_bug_skill)
            self.assertIn("release_blocker", kb_bug_skill)
            self.assertIn("Stop & Yield Control", kb_bug_skill)

            kb_implement_skill = (target / ".agents" / "skills" / "kb-implement" / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("BUG-XXX", kb_implement_skill)
            self.assertIn("TDD Pipeline", kb_implement_skill)

            kb_complete_skill = (target / ".agents" / "skills" / "kb-complete" / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("fixed_in", kb_complete_skill)

            # Check scripts/kb_release.py deployed
            kb_release_script = (target / "scripts" / "kb_release.py").read_text(encoding="utf-8")
            self.assertIn("collect_fixed_bugs", kb_release_script)
            self.assertIn("check_release_blockers", kb_release_script)

            # 3. Test install.py --update refreshes bug lifecycle assets
            # Overwrite files with legacy dummy content
            (target / "docs" / "00_Templates" / "TEMPLATE_BUG.md").write_text("Legacy bug template", encoding="utf-8")
            (target / ".agents" / "skills" / "kb-bug" / "SKILL.md").write_text("Legacy kb-bug", encoding="utf-8")
            (target / ".agents" / "skills" / "kb-implement" / "SKILL.md").write_text("Legacy kb-implement", encoding="utf-8")
            (target / "scripts" / "kb_release.py").write_text("# Legacy kb_release", encoding="utf-8")

            update_res = subprocess.run(
                [sys.executable, str(REPO_ROOT / "install.py"), "--update", "-d", str(target)],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(update_res.returncode, 0, f"Update failed: {update_res.stdout}\n{update_res.stderr}")

            # Verify files restored to modern versions
            updated_bug_tpl = (target / "docs" / "00_Templates" / "TEMPLATE_BUG.md").read_text(encoding="utf-8")
            self.assertIn("target_release:", updated_bug_tpl)
            self.assertIn("release_blocker:", updated_bug_tpl)

            updated_kb_release = (target / "scripts" / "kb_release.py").read_text(encoding="utf-8")
            self.assertIn("collect_fixed_bugs", updated_kb_release)

            # 4. Test release targeting & blocker in the sandbox
            # Create a mock task and bugs
            task_dir = target / "docs" / "02_Tasks" / "Specs" / "01_MVP"
            task_dir.mkdir(parents=True, exist_ok=True)
            (task_dir / "TASK-001.md").write_text(
                "---\nid: TASK-001\ntitle: MVP\nstatus: done\ntype: task\nphase: 1\nparent_plan: PLAN-001\ncreated: 2026-10-15\n---\n# TASK-001\n",
                encoding="utf-8"
            )

            bugs_dir = target / "docs" / "02_Tasks" / "Bugs"
            bugs_dir.mkdir(parents=True, exist_ok=True)
            (bugs_dir / "BUG-001-fixed.md").write_text(
                "---\nid: BUG-001\ntitle: Fixed Bug\nstatus: fixed\nseverity: medium\ntype: bug\ntarget_release: v0.1.0\nfixed_in: v0.1.0\nphase: 1\ncreated: 2026-10-15\n---\n# BUG-001\n",
                encoding="utf-8"
            )
            (bugs_dir / "BUG-002-future.md").write_text(
                "---\nid: BUG-002\ntitle: Future Bug\nstatus: fixed\nseverity: low\ntype: bug\ntarget_release: v0.2.0\nfixed_in: v0.2.0\nphase: 1\ncreated: 2026-10-15\n---\n# BUG-002\n",
                encoding="utf-8"
            )
            blocker_file = bugs_dir / "BUG-003-blocker.md"
            blocker_file.write_text(
                "---\nid: BUG-003\ntitle: Blocker Bug\nstatus: open\nseverity: high\ntype: bug\ntarget_release: v0.1.0\nrelease_blocker: true\nphase: 1\ncreated: 2026-10-15\n---\n# BUG-003\n",
                encoding="utf-8"
            )

            # Run kb_release.py expecting abort on open blocker
            rel_fail = subprocess.run(
                [sys.executable, str(target / "scripts" / "kb_release.py"), "--version", "v0.1.0", "--phase", "1"],
                cwd=str(target),
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertNotEqual(rel_fail.returncode, 0, "Release should have failed due to open blocker!")
            self.assertIn("blocked by open defect BUG-003", rel_fail.stderr)

            # Clear blocker flag and re-run release
            blocker_file.write_text(
                "---\nid: BUG-003\ntitle: Blocker Bug\nstatus: open\nseverity: high\ntype: bug\ntarget_release: v0.1.0\nrelease_blocker: false\nphase: 1\ncreated: 2026-10-15\n---\n# BUG-003\n",
                encoding="utf-8"
            )
            rel_ok = subprocess.run(
                [sys.executable, str(target / "scripts" / "kb_release.py"), "--version", "v0.1.0", "--phase", "1"],
                cwd=str(target),
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(rel_ok.returncode, 0, f"Release failed unexpectedly: {rel_ok.stdout}\n{rel_ok.stderr}")

            # Verify public release notes in dist/
            dist_notes = (target / "dist" / "RELEASE_NOTES.md").read_text(encoding="utf-8")
            self.assertIn("BUG-001", dist_notes)
            self.assertNotIn("BUG-002", dist_notes)  # Target release was v0.2.0, so excluded from v0.1.0

            # 5. Verify kb_lint check passes
            lint_res = subprocess.run(
                [sys.executable, str(target / "scripts" / "kb_lint.py"), "--path", str(target / "docs")],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(lint_res.returncode, 0, f"kb_lint failed: {lint_res.stdout}\n{lint_res.stderr}")

    def test_23_feedback_ingestion_and_diagnostic_report(self):
        """Phase 12: Verify feedback buffer, templates, ingest script, and diagnostic report."""
        import getpass
        current_user = getpass.getuser()

        with tempfile.TemporaryDirectory() as tmp_dir:
            base = Path(tmp_dir)

            # 1. Test diagnostic report on REPO_ROOT via subprocess
            res_report = subprocess.run(
                [sys.executable, str(REPO_ROOT / "install.py"), "--report"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(res_report.returncode, 0, f"--report failed:\n{res_report.stderr}")
            report_text = res_report.stdout
            self.assertIn("# 🩺 Diagnostic Report: Agent Docs-as-Code Harness", report_text)
            self.assertIn("## 1. System & Runtime Environment", report_text)
            self.assertIn("## 2. Git Repository Status", report_text)
            self.assertIn("## 3. Knowledge Base Health (kb_lint)", report_text)
            self.assertIn("## 4. Detected AI Agent Configurations", report_text)
            if current_user:
                self.assertNotIn(f"\\Users\\{current_user}\\", report_text)
                self.assertNotIn(f"/home/{current_user}/", report_text)

            # 2. Test fresh harness installation
            target = base / "FeedbackApp"
            target.mkdir()
            install.install_harness(
                target_dir=target,
                project_name="FeedbackApp",
                stack_key="python",
                agent_choice="all",
                git_choice="none",
                doc_lang="ru",
                force=True,
            )

            # Verify Phase 12 artifacts exist
            inbox_dir = target / "docs" / "02_Tasks" / "Inbox"
            self.assertTrue(inbox_dir.is_dir(), "Inbox/ directory missing")
            inbox_state = inbox_dir / ".inbox_state.json"
            self.assertTrue(inbox_state.is_file(), ".inbox_state.json missing")
            self.assertIn('"last_issue_number": 0', inbox_state.read_text(encoding="utf-8"))

            feedback_tpl = target / "docs" / "00_Templates" / "TEMPLATE_FEEDBACK.md"
            self.assertTrue(feedback_tpl.is_file(), "TEMPLATE_FEEDBACK.md missing")
            self.assertIn("FB-XXX", feedback_tpl.read_text(encoding="utf-8"))

            kb_ingest_script = target / "scripts" / "kb_ingest.py"
            self.assertTrue(kb_ingest_script.is_file(), "scripts/kb_ingest.py missing")

            triage_skill = target / ".agents" / "skills" / "kb-triage" / "SKILL.md"
            self.assertTrue(triage_skill.is_file(), ".agents/skills/kb-triage/SKILL.md missing")

            bug_issue_tpl = target / ".github" / "ISSUE_TEMPLATE" / "bug_report.yml"
            self.assertTrue(bug_issue_tpl.is_file(), ".github/ISSUE_TEMPLATE/bug_report.yml missing")
            feature_issue_tpl = target / ".github" / "ISSUE_TEMPLATE" / "feature_request.yml"
            self.assertTrue(feature_issue_tpl.is_file(), ".github/ISSUE_TEMPLATE/feature_request.yml missing")

            # 3. Test update on legacy structure (missing Inbox)
            legacy = base / "LegacyApp"
            legacy.mkdir()
            install.install_harness(
                target_dir=legacy,
                project_name="LegacyApp",
                stack_key="python",
                agent_choice="all",
                git_choice="none",
                doc_lang="ru",
                force=True,
            )
            # Remove Inbox to simulate legacy project
            import shutil
            shutil.rmtree(legacy / "docs" / "02_Tasks" / "Inbox")
            self.assertFalse((legacy / "docs" / "02_Tasks" / "Inbox").exists())

            # Run update
            res_up = subprocess.run(
                [sys.executable, str(REPO_ROOT / "install.py"), "--update", "--target-dir", str(legacy)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(res_up.returncode, 0, f"Update legacy failed: {res_up.stderr}")
            self.assertTrue((legacy / "docs" / "02_Tasks" / "Inbox").is_dir())
            self.assertTrue((legacy / "docs" / "02_Tasks" / "Inbox" / ".inbox_state.json").is_file())

            # 4. Verify existing inbox items and state are preserved during update
            custom_fb = legacy / "docs" / "02_Tasks" / "Inbox" / "FB-001-custom.md"
            custom_fb.write_text("---\nid: FB-001\ntitle: Custom Feedback\nstatus: new\n---\n# FB-001", encoding="utf-8")
            legacy_state = legacy / "docs" / "02_Tasks" / "Inbox" / ".inbox_state.json"
            legacy_state.write_text('{"version": 1, "github": {"last_issue_number": 42}}', encoding="utf-8")

            res_up2 = subprocess.run(
                [sys.executable, str(REPO_ROOT / "install.py"), "--update", "--target-dir", str(legacy)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(res_up2.returncode, 0)
            self.assertTrue(custom_fb.is_file())
            self.assertIn('"last_issue_number": 42', legacy_state.read_text(encoding="utf-8"))

            # 5. Verify diagnostic report on target directory
            res_rep_target = subprocess.run(
                [sys.executable, str(REPO_ROOT / "install.py"), "--report", "--target-dir", str(target)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(res_rep_target.returncode, 0)
            self.assertIn("FeedbackApp", res_rep_target.stdout)

            # 6. Verify kb_lint audit passes on fresh installation
            kb_lint_res = subprocess.run(
                [sys.executable, str(target / "scripts" / "kb_lint.py"), "--path", str(target / "docs")],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(kb_lint_res.returncode, 0, f"kb_lint failed on fresh target:\n{kb_lint_res.stdout}\n{kb_lint_res.stderr}")

    def test_24_obsidian_taxonomy_decoupling(self):
        """Verify Obsidian Graph color table is removed from AGENTS.md generator and compact taxonomy directive is present."""
        # 1. Generator check
        agents_content = install.generate_agents_md("TaxonomyApp", "generic", "ru")
        self.assertIn("### 🎨 Obsidian Graph & Taxonomy", agents_content)
        self.assertIn("Visual graph taxonomy is configured in `.obsidian/graph.json`", agents_content)
        self.assertIn("`#arch`, `#adr`, `#research`, `#task`, `#bug`, `#testing`", agents_content)
        self.assertNotIn("⚪ White / Light", agents_content)
        self.assertNotIn("🟣 Purple", agents_content)
        self.assertNotIn("Color / Category", agents_content)

        # 2. Root AGENTS.md check
        root_agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Visual graph taxonomy is configured in `.obsidian/graph.json`", root_agents)
        self.assertNotIn("⚪ White / Light", root_agents)
        self.assertNotIn("🟣 Purple", root_agents)
        self.assertNotIn("Color / Category", root_agents)

        # 3. Fresh installation check
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "TaxonomyTestApp"
            target.mkdir()

            install.install_harness(
                target_dir=target,
                project_name="TaxonomyTestApp",
                stack_key="python",
                agent_choice="generic",
                git_choice="none",
                force=True,
            )

            installed_agents = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("### 🎨 Obsidian Graph & Taxonomy", installed_agents)
            self.assertIn("Visual graph taxonomy is configured in `.obsidian/graph.json`", installed_agents)
            self.assertNotIn("⚪ White / Light", installed_agents)
            self.assertNotIn("🟣 Purple", installed_agents)

    def test_25_thin_forwarders_rules_layering(self):
        """Verify Thin Forwarders pattern across all adapter generators, root files, and fresh installation."""
        # 1. Generator functions checks
        for gen_fn in [
            install.generate_gemini_md,
            install.generate_windsurfrules,
            install.generate_clinerules,
            install.generate_claude_md,
            install.generate_cursorrules,
            install.generate_copilot_instructions,
        ]:
            out = gen_fn("ForwarderApp", "python", "ru")
            lines = out.strip().splitlines()
            self.assertLessEqual(len(lines), 35, f"Generator {gen_fn.__name__} exceeds 35 lines ({len(lines)} lines)")
            self.assertIn("[[AGENTS.md]]", out)
            self.assertIn("[[docs/00_Index|00_Index]]", out)
            self.assertIn("## ⚡ Stack Verification Commands", out)
            self.assertIn("## 🛡️ Operating Rules & Routing", out)
            self.assertIn("STRICTLY NO CODE CHANGES", out)
            self.assertIn("Human Guardrails", out)
            self.assertIn("Fast-Track Protocol", out)
            self.assertIn("Zero Round-Trip", out)
            self.assertIn("Anti-Echo & Single-Task Barrier", out)
            self.assertNotIn("## Docs-as-Code (19 Disciplines)", out)
            self.assertNotIn("1. Read `SPEC.md`", out)

        # 2. Project root adapter files check
        root_adapters = [
            REPO_ROOT / "GEMINI.md",
            REPO_ROOT / "CLAUDE.md",
            REPO_ROOT / ".cursorrules",
            REPO_ROOT / ".windsurfrules",
            REPO_ROOT / ".clinerules",
            REPO_ROOT / ".github" / "copilot-instructions.md",
        ]
        for adapter_file in root_adapters:
            self.assertTrue(adapter_file.is_file(), f"Root adapter missing: {adapter_file}")
            content = adapter_file.read_text(encoding="utf-8")
            lines = content.strip().splitlines()
            self.assertLessEqual(len(lines), 35, f"Root adapter {adapter_file.name} exceeds 35 lines ({len(lines)} lines)")
            self.assertIn("[[AGENTS.md]]", content)
            self.assertIn("## ⚡ Stack Verification Commands", content)
            self.assertIn("STRICTLY NO CODE CHANGES", content)
            self.assertIn("Human Guardrails", content)
            self.assertIn("Fast-Track Protocol", content)
            self.assertIn("Zero Round-Trip", content)
            self.assertNotIn("## Docs-as-Code (19 Disciplines)", content)

        # 3. Fresh installation with all adapters check
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "ThinForwarderApp"
            target.mkdir()

            install.install_harness(
                target_dir=target,
                project_name="ThinForwarderApp",
                stack_key="ts",
                agent_choice="all",
                git_choice="none",
                force=True,
            )

            for path in [
                target / "GEMINI.md",
                target / "CLAUDE.md",
                target / ".cursorrules",
                target / ".windsurfrules",
                target / ".clinerules",
                target / ".github" / "copilot-instructions.md",
            ]:
                self.assertTrue(path.is_file(), f"Target adapter missing: {path}")
                content = path.read_text(encoding="utf-8")
                lines = content.strip().splitlines()
                self.assertLessEqual(len(lines), 35, f"{path.name} exceeds 35 lines")
                self.assertIn("[[AGENTS.md]]", content)
                self.assertIn("npm test", content)
                self.assertIn("Human Guardrails", content)
                self.assertIn("Fast-Track Protocol", content)
                self.assertIn("Zero Round-Trip", content)
                self.assertNotIn("## Docs-as-Code (19 Disciplines)", content)


    def test_26_skills_consolidation_and_template_taxonomy(self):
        """E2E test: Verify consolidation of docs-as-code into kb-onboard (12 skills total) and two-tier template taxonomy."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "ConsolidatedApp"
            target.mkdir()

            install.install_harness(
                target_dir=target,
                project_name="ConsolidatedApp",
                stack_key="python",
                agent_choice="all",
                git_choice="none",
                force=True,
            )

            # 1. Exactly 12 skills deployed
            skills_dir = target / ".agents" / "skills"
            self.assertTrue(skills_dir.is_dir())
            skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
            self.assertEqual(len(skill_dirs), 12, f"Expected 12 skills, got: {[d.name for d in skill_dirs]}")

            # 2. docs-as-code must NOT exist, kb-onboard must exist and contain command router
            self.assertFalse((skills_dir / "docs-as-code").exists(), "docs-as-code must be consolidated and removed")
            onboard_skill = skills_dir / "kb-onboard" / "SKILL.md"
            self.assertTrue(onboard_skill.is_file())
            onboard_text = onboard_skill.read_text(encoding="utf-8")
            self.assertIn("Command Router", onboard_text)
            self.assertIn("/kb-init", onboard_text)
            self.assertIn("/kb-implement", onboard_text)
            self.assertIn("16 templates: 4 Core, 12 Advanced", onboard_text)

            # 3. Two-tier template taxonomy documented in TEMPLATE_ONBOARDING.md and repo Onboarding.md
            template_onboarding = target / "docs" / "00_Templates" / "TEMPLATE_ONBOARDING.md"
            self.assertTrue(template_onboarding.is_file())
            template_content = template_onboarding.read_text(encoding="utf-8")
            self.assertIn("Core Essentials (4)", template_content)
            self.assertIn("Advanced Governance (12)", template_content)

            repo_onboarding = REPO_ROOT / "docs" / "Onboarding.md"
            repo_content = repo_onboarding.read_text(encoding="utf-8")
            self.assertIn("Двухуровневая таксономия шаблонов", repo_content)
            self.assertIn("Core Essentials — 4 шаблона", repo_content)
            self.assertIn("Advanced Governance — 12 шаблонов", repo_content)

    def test_27_dist_monolith_e2e_fresh_install_and_update(self):
        """E2E test: Verify dist/install.py compiled monolith behavior on fresh install and safe update."""
        dist_installer = REPO_ROOT / "dist" / "install.py"
        self.assertTrue(dist_installer.is_file(), "dist/install.py must exist")

        # 1. Fresh install using dist/install.py via subprocess
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "MonolithApp"
            target.mkdir()

            res = subprocess.run(
                [
                    sys.executable,
                    str(dist_installer),
                    "--non-interactive",
                    "--name",
                    "MonolithApp",
                    "--stack",
                    "python",
                    "--agent",
                    "all",
                    "--git",
                    "none",
                    "--target-dir",
                    str(target),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(res.returncode, 0, f"dist/install.py failed: {res.stdout}\n{res.stderr}")
            self.assertIn("Agent Docs-as-Code Harness installed successfully", res.stdout)

            # Check deployed skills = 12
            skills_dir = target / ".agents" / "skills"
            self.assertTrue(skills_dir.is_dir())
            skill_subdirs = [d for d in skills_dir.iterdir() if d.is_dir()]
            self.assertEqual(len(skill_subdirs), 12)
            self.assertFalse((skills_dir / "docs-as-code").exists())
            self.assertTrue((skills_dir / "kb-onboard").exists())

            # Check adapters are thin forwarders
            gemini_md = target / "GEMINI.md"
            self.assertTrue(gemini_md.is_file())
            gemini_lines = gemini_md.read_text(encoding="utf-8").strip().splitlines()
            self.assertLessEqual(len(gemini_lines), 35)
            self.assertIn("[[AGENTS.md]]", "\n".join(gemini_lines))

            # 2. Safe update test via dist/install.py --update
            res_up = subprocess.run(
                [
                    sys.executable,
                    str(dist_installer),
                    "--update",
                    "--target-dir",
                    str(target),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(res_up.returncode, 0, f"dist/install.py --update failed: {res_up.stdout}\n{res_up.stderr}")
            self.assertIn("Refreshed 12 skills", res_up.stdout)


    def test_28_fast_track_template_and_zero_to_hero_guide_deployment(self):
        """E2E test: Verify TEMPLATE_TASK_MICRO.md and Zero_To_Hero_Guide.md deployment in fresh install and --update."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "FastTrackApp"
            target.mkdir()

            # 1. Fresh installation
            install.install_harness(
                target_dir=target,
                project_name="FastTrackApp",
                stack_key="python",
                agent_choice="all",
                git_choice="none",
                force=True,
            )

            # Check fresh deployment
            micro_template = target / "docs" / "00_Templates" / "TEMPLATE_TASK_MICRO.md"
            self.assertTrue(micro_template.is_file(), "TEMPLATE_TASK_MICRO.md should be deployed in fresh install")
            micro_content = micro_template.read_text(encoding="utf-8")
            self.assertIn("type: fast-track", micro_content)
            self.assertIn("Fast-Track (≤ 30 LOC)", micro_content)

            zero_to_hero = target / "docs" / "Zero_To_Hero_Guide.md"
            self.assertTrue(zero_to_hero.is_file(), "Zero_To_Hero_Guide.md should be deployed in fresh install")
            guide_content = zero_to_hero.read_text(encoding="utf-8")
            self.assertIn("Zero to Hero", guide_content)
            self.assertIn("Fast-Track", guide_content)

            # Check 16 templates total in docs/00_Templates/ (Phase 16 added TEMPLATE_INCIDENT.md)
            templates = list((target / "docs" / "00_Templates").glob("*.md"))
            self.assertEqual(len(templates), 16, f"Expected 16 templates, found {len(templates)}")

            # 2. Modify files to verify update behavior
            # Zero_To_Hero_Guide.md is core documentation refreshed on --update
            zero_to_hero.write_text("# Outdated Guide\n", encoding="utf-8")
            # TEMPLATE_TASK_MICRO.md is refreshed on --update
            micro_template.write_text("# Outdated Template\n", encoding="utf-8")

            # Run safe update
            install.update_harness(target)

            refreshed_guide = zero_to_hero.read_text(encoding="utf-8")
            self.assertIn("Zero to Hero", refreshed_guide)
            self.assertNotIn("# Outdated Guide", refreshed_guide)

            refreshed_template = micro_template.read_text(encoding="utf-8")
            self.assertIn("type: fast-track", refreshed_template)
            self.assertNotIn("# Outdated Template", refreshed_template)

    def test_29_channel_transparency_and_phase_consistency_deployment(self):
        """E2E test verifying deployment and --update for channel transparency and phase consistency."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "ChannelApp"
            target.mkdir()

            # 1. Fresh installation
            install.install_harness(
                target_dir=target,
                project_name="ChannelApp",
                stack_key="python",
                agent_choice="generic",
                git_choice="none",
                ci_choice="none",
            )

            # 2. Check deployed scripts
            ingest_script = target / "scripts" / "kb_ingest.py"
            self.assertTrue(ingest_script.is_file(), "kb_ingest.py should be deployed in fresh install")
            ingest_content = ingest_script.read_text(encoding="utf-8")
            self.assertIn("detect_github_repo", ingest_content)
            self.assertIn("render_status_dashboard", ingest_content)
            self.assertIn("--status", ingest_content)

            lint_script = target / "scripts" / "kb_lint.py"
            self.assertTrue(lint_script.is_file(), "kb_lint.py should be deployed in fresh install")
            lint_content = lint_script.read_text(encoding="utf-8")
            self.assertIn("check_phase_consistency", lint_content)

            triage_skill = target / ".agents" / "skills" / "kb-triage" / "SKILL.md"
            self.assertTrue(triage_skill.is_file(), "kb-triage skill should be deployed")
            triage_content = triage_skill.read_text(encoding="utf-8")
            self.assertIn("Diagnostic Source Feedback", triage_content)
            self.assertIn("kb_ingest.py --status", triage_content)

            # 3. Test running kb_ingest.py --status
            res_ingest = subprocess.run(
                [sys.executable, str(ingest_script), "--status"],
                cwd=str(target),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=10,
            )
            self.assertEqual(res_ingest.returncode, 0, f"kb_ingest.py --status failed:\n{res_ingest.stdout}\n{res_ingest.stderr}")
            self.assertIn("Feedback Ingestion Status Dashboard", res_ingest.stdout)
            self.assertIn("[Канал: GitHub Issues]", res_ingest.stdout)
            self.assertIn("[Буфер обращений: docs/02_Tasks/Inbox/]", res_ingest.stdout)

            # 4. Test running kb_lint.py on fresh docs
            res_lint = subprocess.run(
                [sys.executable, str(lint_script), "--path", str(target / "docs")],
                cwd=str(target),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=10,
            )
            self.assertEqual(res_lint.returncode, 0, f"kb_lint.py failed:\n{res_lint.stdout}\n{res_lint.stderr}")
            self.assertIn("0 broken", res_lint.stdout)

            # 5. Test update behavior: corrupt scripts and run update_harness
            ingest_script.write_text("# OUTDATED_INGEST_SCRIPT\n", encoding="utf-8")
            lint_script.write_text("# OUTDATED_LINT_SCRIPT\n", encoding="utf-8")

            install.update_harness(target)

            refreshed_ingest = ingest_script.read_text(encoding="utf-8")
            self.assertIn("detect_github_repo", refreshed_ingest)
            self.assertNotIn("# OUTDATED_INGEST_SCRIPT", refreshed_ingest)

            refreshed_lint = lint_script.read_text(encoding="utf-8")
            self.assertIn("check_phase_consistency", refreshed_lint)
            self.assertNotIn("# OUTDATED_LINT_SCRIPT", refreshed_lint)

    def test_30_memory_infrastructure_and_safe_update(self):
        """E2E test: Deployment of docs/06_Memory/ and safe retention of patterns.md across updates."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "MemoryApp"
            target.mkdir()

            # 1. Clean installation
            install.install_harness(
                target_dir=target,
                project_name="MemoryApp",
                stack_key="python",
                agent_choice="generic",
                git_choice="none",
                force=True,
            )

            mem_dir = target / "docs" / "06_Memory"
            incidents_dir = mem_dir / "Incidents"
            patterns_file = mem_dir / "patterns.md"
            tpl_incident = target / "docs" / "00_Templates" / "TEMPLATE_INCIDENT.md"

            self.assertTrue(mem_dir.is_dir(), "docs/06_Memory/ should exist after install")
            self.assertTrue(incidents_dir.is_dir(), "docs/06_Memory/Incidents/ should exist after install")
            self.assertTrue(patterns_file.is_file(), "patterns.md should exist after install")
            self.assertTrue(tpl_incident.is_file(), "TEMPLATE_INCIDENT.md should exist after install")

            # Verify initial content of patterns.md
            content = patterns_file.read_text(encoding="utf-8")
            self.assertIn("Память процедурных ошибок: Активные паттерны", content)
            self.assertIn("[TRG-01]", content)

            # 2. Modify patterns.md with user-accumulated pattern
            custom_pattern = "- [TRG-99] Custom Error | Description | Fix | (Count: 5, Sev: High) -> INC-099\n"
            patterns_file.write_text(content + custom_pattern, encoding="utf-8")

            # 3. Run safe update
            install.update_harness(target)

            # Verify patterns.md was NOT overwritten
            updated_content = patterns_file.read_text(encoding="utf-8")
            self.assertIn("[TRG-99]", updated_content, "Custom patterns must be preserved across updates!")

            # Verify kb_lint passes on the updated repository
            lint_script = target / "scripts" / "kb_lint.py"
            res_lint = subprocess.run(
                [sys.executable, str(lint_script), "--path", str(target / "docs")],
                cwd=str(target),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=10,
            )
            self.assertEqual(res_lint.returncode, 0, f"kb_lint failed on MemoryApp:\n{res_lint.stdout}\n{res_lint.stderr}")
            self.assertIn("0 broken", res_lint.stdout)

    def test_31_bug_008_local_fallback_memory_patterns(self):
        """Verify local development fallback in unpack_assets includes docs/06_Memory/patterns.md (BUG-008)."""
        with patch.object(install, "EMBEDDED_ASSETS_B64", ""):
            assets = install.unpack_assets(REPO_ROOT)
            self.assertIn("docs/06_Memory/patterns.md", assets)
            content = assets["docs/06_Memory/patterns.md"]
            self.assertIn("Память процедурных ошибок: Активные паттерны", content)

    def test_32_bug_009_issue_templates_no_repo_leak(self):
        """Verify .github/ISSUE_TEMPLATE in installed project does not leak harness repo metadata (BUG-009)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            target = base / "ClientApp"
            target.mkdir()

            install.install_harness(
                target_dir=target,
                project_name="ClientApp",
                stack_key="python",
                agent_choice="generic",
                git_choice="none",
                doc_lang="ru",
                force=True,
            )

            issue_tpl_dir = target / ".github" / "ISSUE_TEMPLATE"
            self.assertTrue(issue_tpl_dir.is_dir(), ".github/ISSUE_TEMPLATE/ should exist")

            # 1. config.yml must NOT be deployed to client projects (leaks harness repo links)
            config_file = issue_tpl_dir / "config.yml"
            self.assertFalse(config_file.exists(), ".github/ISSUE_TEMPLATE/config.yml should not be deployed to client projects")

            # 2. bug_report.yml must be parameterized with project_name or neutral (no agent-docs-harness leak)
            bug_file = issue_tpl_dir / "bug_report.yml"
            self.assertTrue(bug_file.is_file(), "bug_report.yml must exist")
            bug_content = bug_file.read_text(encoding="utf-8")
            self.assertNotIn("koudinie101-png", bug_content)
            self.assertNotIn("agent-docs-harness", bug_content)
            self.assertIn("ClientApp", bug_content)

            # 3. feature_request.yml must not leak harness repo metadata
            feat_file = issue_tpl_dir / "feature_request.yml"
            self.assertTrue(feat_file.is_file(), "feature_request.yml must exist")
            feat_content = feat_file.read_text(encoding="utf-8")
            self.assertNotIn("koudinie101-png", feat_content)
            self.assertNotIn("agent-docs-harness", feat_content)

        # 4. Verify local development fallback in unpack_assets also skips config.yml
        with patch.object(install, "EMBEDDED_ASSETS_B64", ""):
            local_assets = install.unpack_assets(REPO_ROOT)
            self.assertNotIn(".github/ISSUE_TEMPLATE/config.yml", local_assets)
            self.assertIn(".github/ISSUE_TEMPLATE/bug_report.yml", local_assets)
            self.assertIn(".github/ISSUE_TEMPLATE/feature_request.yml", local_assets)

    def test_33_task_068_installer_tty_anonymizer_and_build_hook(self):
        """Verify anonymizer boundary protection, can_open_tty probe, and build_release hook (TASK-068)."""
        import getpass
        import io

        # 1. Anonymizer boundary protection
        with tempfile.TemporaryDirectory() as tmpdir:
            test_target = Path(tmpdir) / "TestApp"
            test_target.mkdir()
            (test_target / "docs").mkdir()
            (test_target / "docs" / "Devlog.md").write_text("# Devlog", encoding="utf-8")

            with patch("getpass.getuser", return_value="dev"), \
                 patch.object(Path, "home", return_value=Path("C:/Users/dev")):
                rep = install.generate_diagnostic_report(test_target)
                # Ensure Devlog is preserved and not corrupted into <user>log
                self.assertNotIn("<user>log", rep)
                # Ensure home_dir or user in path is masked
                self.assertNotIn("Users/dev/", rep.replace("\\", "/"))

        # 2. can_open_tty probe tests
        # Case A: sys.stdin.isatty() is True
        with patch.object(sys.stdin, "isatty", return_value=True):
            self.assertTrue(install.can_open_tty())

        # Case B: sys.stdin.isatty() is False on Windows (os.name == 'nt')
        with patch.object(sys.stdin, "isatty", return_value=False), patch("os.name", "nt"):
            self.assertFalse(install.can_open_tty())

        # Case C: sys.stdin.isatty() is False on posix, /dev/tty does not exist
        with patch.object(sys.stdin, "isatty", return_value=False), \
             patch("os.name", "posix"), \
             patch("os.path.exists", return_value=False):
            self.assertFalse(install.can_open_tty())

        # Case D: sys.stdin.isatty() is False on posix, /dev/tty exists but raises OSError on open
        with patch.object(sys.stdin, "isatty", return_value=False), \
             patch("os.name", "posix"), \
             patch("os.path.exists", return_value=True), \
             patch("builtins.open", side_effect=OSError("No such device or address")):
            self.assertFalse(install.can_open_tty())

        # 3. setup_git() diagnostics on commit failure
        with tempfile.TemporaryDirectory() as tmpdir:
            git_target = Path(tmpdir) / "GitApp"
            git_target.mkdir()
            (git_target / ".git" / "HEAD").parent.mkdir(parents=True)
            (git_target / ".git" / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")

            mock_commit_res = subprocess.CompletedProcess(
                args=["git", "commit"],
                returncode=128,
                stdout="",
                stderr="fatal: empty ident name (for <user@domain>) not allowed\n*** Please tell me who you are.\nRun\n  git config --global user.email 'you@example.com'\n  git config --global user.name 'Your Name'\n"
            )

            with patch("subprocess.run") as mock_run, patch("sys.stdout", new=io.StringIO()) as fake_out:
                mock_run.side_effect = [
                    subprocess.CompletedProcess(args=["git", "add"], returncode=0),
                    mock_commit_res,
                    subprocess.CompletedProcess(args=["git", "branch"], returncode=0),
                ]
                install.setup_git(git_target, "local")
                out_str = fake_out.getvalue()
                self.assertIn("Initial commit could not be created automatically (exit code 128)", out_str)
                self.assertIn("Configure Git identity: git config --global user.name", out_str)

        # 4. scripts/build_release.py calls build_installer.build()
        import scripts.build_release as build_release
        with patch("scripts.build_installer.build") as mock_build, \
             patch("shutil.copy2") as mock_copy:
            res_code = build_release.main()
            self.assertEqual(res_code, 0)
            mock_build.assert_called_once()
            mock_copy.assert_called_once()


if __name__ == "__main__":
    unittest.main()




