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

    def test_bug_006_inspect_release_artifacts_excludes_release_notes(self):
        """Verifies that RELEASE_NOTES.md is excluded from release artifacts table (BUG-006)."""
        dist_dir = self.test_root / "dist"
        dist_dir.mkdir(parents=True, exist_ok=True)

        app_bin = dist_dir / "app-v1.0.0.zip"
        app_bin.write_bytes(b"binary content")

        notes_file = dist_dir / "RELEASE_NOTES.md"
        notes_file.write_text("# Release Notes\n\nContent", encoding="utf-8")

        custom_notes = dist_dir / "CUSTOM_NOTES.md"
        custom_notes.write_text("# Custom Notes\n\nContent", encoding="utf-8")

        # By default, RELEASE_NOTES.md must be ignored
        artifacts = kb_release.inspect_release_artifacts(dist_dir)
        artifact_names = [a["name"] for a in artifacts]
        self.assertNotIn("RELEASE_NOTES.md", artifact_names)
        self.assertIn("app-v1.0.0.zip", artifact_names)
        self.assertIn("CUSTOM_NOTES.md", artifact_names)

        # When custom excluded_names are passed, both should be ignored
        artifacts_custom = kb_release.inspect_release_artifacts(dist_dir, excluded_names={"CUSTOM_NOTES.md"})
        custom_artifact_names = [a["name"] for a in artifacts_custom]
        self.assertNotIn("RELEASE_NOTES.md", custom_artifact_names)
        self.assertNotIn("CUSTOM_NOTES.md", custom_artifact_names)
        self.assertEqual(custom_artifact_names, ["app-v1.0.0.zip"])

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
        # ADR (accepted, phase 4)
        (adrs_dir / "ADR-0010-arch.md").write_text(
            "---\nid: ADR-0010\ntitle: Cool Architecture\nphase: 4\nstatus: accepted\n---\n# ADR",
            encoding="utf-8"
        )
        # ADR (accepted, phase 3 - should not match phase 4)
        (adrs_dir / "ADR-0005-other.md").write_text(
            "---\nid: ADR-0005\ntitle: Other Architecture\nphase: 3\nstatus: accepted\n---\n# ADR",
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

    def test_find_phase_artifacts_double_digit_fallback(self):
        """Verifies phase artifacts matching for double-digit phases (>= 10) without phase frontmatter (BUG-008)."""
        docs_dir = self.test_root / "docs"
        specs_dir = docs_dir / "02_Tasks" / "Specs" / "15_LatencyAndChannels"
        specs_dir.mkdir(parents=True, exist_ok=True)

        # Spec file in folder 15_LatencyAndChannels WITHOUT phase field in frontmatter
        (specs_dir / "TASK-057-zero-roundtrip.md").write_text(
            "---\nid: TASK-057\ntitle: Zero Round-Trip Dispatch\nstatus: done\n---\n# TASK-057",
            encoding="utf-8"
        )
        found = kb_release.find_phase_artifacts(docs_dir, phase_num=15)
        self.assertEqual(len(found["tasks"]), 1)
        self.assertEqual(found["tasks"][0]["id"], "TASK-057")

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

    def test_detect_release_environment_regression_bug_003(self):
        """BUG-003: Verifies that missing gh CLI in a GitHub repo is explicitly reported with warning and guidance."""
        def mock_which(cmd):
            if cmd == "git":
                return "/usr/bin/git"
            if cmd == "gh":
                return None
            return None

        def mock_run(cmd, *args, **kwargs):
            m = MagicMock()
            m.returncode = 0
            if "rev-parse" in cmd and "--is-inside-work-tree" in cmd:
                m.stdout = "true\n"
            elif "rev-parse" in cmd and "--abbrev-ref" in cmd:
                m.stdout = "main\n"
            elif "status" in cmd:
                m.stdout = ""
            elif "remote" in cmd:
                m.stdout = "git@github.com:myorg/myproject.git\n"
            else:
                m.stdout = ""
            return m

        with patch("shutil.which", side_effect=mock_which), \
             patch("subprocess.run", side_effect=mock_run), \
             patch.dict(os.environ, {}, clear=True):
            status = kb_release.detect_release_environment(self.test_root)
            self.assertTrue(status["is_github"])
            self.assertFalse(status["has_gh_cli"])
            self.assertEqual(status["mode"], "local-only")
            self.assertIn("warning", status)
            self.assertIn("winget install GitHub.cli", status["warning"])
            self.assertEqual(status.get("gh_missing_reason"), "gh_cli_not_installed")

            # With GITHUB_TOKEN set: should resolve to github mode via REST API
            with patch.dict(os.environ, {"GITHUB_TOKEN": "ghp_secret_token_123"}):
                status_token = kb_release.detect_release_environment(self.test_root)
                self.assertEqual(status_token["mode"], "github")
                self.assertEqual(status_token.get("publish_provider"), "rest_api")

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
        # Verify public notes also generated in dist/
        notes_file = dist_dir / "RELEASE_NOTES.md"
        self.assertTrue(notes_file.exists())
        notes_content = notes_file.read_text(encoding="utf-8")
        self.assertIn("# 🚀 Release v0.5.0", notes_content)
        self.assertNotIn("---", notes_content.splitlines()[0])  # No YAML frontmatter at top

    def test_convert_wikilinks_to_github_markdown_with_repo_url(self):
        repo_url = "https://github.com/myorg/myproject.git"
        text = "- [[../Specs/07_Distribution/TASK-025-foo|TASK-025]]: Title.\n- [[../../03_Decisions_ADR/ADR-0010-arch|ADR-0010]]: Arch title.\n- [[TASK-025]]"
        converted = kb_release.convert_wikilinks_to_github_markdown(text, repo_url=repo_url, branch="main")
        self.assertIn("[TASK-025](https://github.com/myorg/myproject/blob/main/docs/02_Tasks/Specs/07_Distribution/TASK-025-foo.md)", converted)
        self.assertIn("[ADR-0010](https://github.com/myorg/myproject/blob/main/docs/03_Decisions_ADR/ADR-0010-arch.md)", converted)
        self.assertIn("[TASK-025](https://github.com/myorg/myproject/blob/main/docs/TASK-025.md)", converted)

    def test_convert_wikilinks_to_github_markdown_ssh_url(self):
        repo_url = "git@github.com:myorg/myproject.git"
        text = "Check [[../Roadmap|Дорожная карта]]."
        converted = kb_release.convert_wikilinks_to_github_markdown(text, repo_url=repo_url, branch="dev")
        self.assertIn("[Дорожная карта](https://github.com/myorg/myproject/blob/dev/docs/02_Tasks/Roadmap.md)", converted)

    def test_convert_wikilinks_to_github_markdown_without_repo_url(self):
        text = "- [[../Specs/TASK-025|TASK-025]]: Title.\n- [[TASK-025]]"
        converted = kb_release.convert_wikilinks_to_github_markdown(text, repo_url="", branch="main")
        self.assertIn("**TASK-025**: Title.", converted)
        self.assertIn("**TASK-025**", converted)
        self.assertNotIn("[[", converted)

    def test_convert_wikilinks_media_assets_and_embeds(self):
        repo_url = "https://github.com/myorg/myproject.git"
        text = (
            "Embed: ![[image.png|600x400]]\n"
            "Asset link: [[assets/schema.svg|Архитектура]]\n"
            "Relative asset: ![[../assets/ui.webp|300]]"
        )
        converted = kb_release.convert_wikilinks_to_github_markdown(text, repo_url=repo_url, branch="main")
        self.assertIn("![image.png](https://github.com/myorg/myproject/blob/main/docs/image.png)", converted)
        self.assertIn("[Архитектура](https://github.com/myorg/myproject/blob/main/docs/assets/schema.svg)", converted)
        self.assertIn("![ui.webp](https://github.com/myorg/myproject/blob/main/docs/02_Tasks/assets/ui.webp)", converted)
        self.assertNotIn(".md", converted)

        # Local mode without repo_url
        local_text = "![[screenshot.png|800]]"
        local_conv = kb_release.convert_wikilinks_to_github_markdown(local_text, repo_url="", branch="main")
        self.assertEqual("![screenshot.png](screenshot.png)", local_conv)

    def test_generate_public_release_notes(self):
        env_info = {
            "has_git": True,
            "mode": "github",
            "branch": "main",
            "remote_url": "https://github.com/myorg/myproject.git",
        }
        artifacts = [{
            "name": "package.zip",
            "path": "dist/package.zip",
            "size": "1.20 MB",
            "sha256": "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
        }]
        phase_data = {
            "tasks": [{"id": "TASK-025", "title": "Dual Export", "link": "../Specs/07_Distribution/TASK-025"}],
            "bugs": [{"id": "BUG-002", "title": "Windows Path Bug", "link": "../Bugs/BUG-002"}],
            "adrs": [{"id": "ADR-0010", "title": "Release Standard", "link": "../../03_Decisions_ADR/ADR-0010"}],
        }

        notes = kb_release.generate_public_release_notes(
            version="0.7.0",
            phase_num=7,
            env_info=env_info,
            artifacts=artifacts,
            phase_data=phase_data,
            summary="Public release notes summary test.",
        )

        # No YAML frontmatter
        self.assertFalse(notes.strip().startswith("---"))
        self.assertIn("# 🚀 Release v0.7.0 — Фаза 7", notes)
        self.assertIn("Public release notes summary test.", notes)
        self.assertIn("### 🌟 Главное в этом релизе (Highlights)", notes)
        self.assertIn("✨ Фича: [TASK-025](https://github.com/myorg/myproject/blob/main/docs/02_Tasks/Specs/07_Distribution/TASK-025.md)", notes)
        self.assertIn("🐛 Исправление: [BUG-002](https://github.com/myorg/myproject/blob/main/docs/02_Tasks/Bugs/BUG-002.md)", notes)
        self.assertNotIn("install.py", notes)
        self.assertIn("curl -LO https://github.com/myorg/myproject/releases/download/v0.7.0/package.zip", notes)
        self.assertNotIn("Новая установка Docs-as-Code", notes)
        self.assertNotIn("Архитектурные решения", notes)
        self.assertNotIn("ADR-0010", notes)
        self.assertIn("package.zip", notes)
        self.assertIn("abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890", notes)
        self.assertIn("Get-FileHash -Path ./dist/package.zip -Algorithm SHA256", notes)
        self.assertNotIn("https://github.com/myorg/myproject/releases/tag/v0.7.0", notes)
        self.assertIn("https://github.com/myorg/myproject/compare/v0.6.0...v0.7.0", notes)

    def test_generate_public_release_notes_excludes_adrs(self):
        """Verifies dist/RELEASE_NOTES.md strictly excludes the ADR section (High-SNR)."""
        env_info = {
            "has_git": True,
            "mode": "github",
            "branch": "main",
            "remote_url": "https://github.com/myorg/myproject.git",
        }
        artifacts = [{"name": "app.zip", "path": "dist/app.zip", "size": "100 KB", "sha256": "123456"}]
        phase_data = {
            "tasks": [{"id": "TASK-037", "title": "High-SNR Notes", "link": "../Specs/TASK-037"}],
            "bugs": [],
            "adrs": [{"id": "ADR-0017", "title": "Release Notes ADR Exclusion", "link": "../../03_Decisions_ADR/ADR-0017"}],
        }
        notes = kb_release.generate_public_release_notes(
            version="0.10.0",
            phase_num=10,
            env_info=env_info,
            artifacts=artifacts,
            phase_data=phase_data,
            summary="High-SNR summary",
        )
        self.assertNotIn("Архитектурные решения", notes)
        self.assertNotIn("ADR-0017", notes)
        self.assertIn("TASK-037", notes)

    def test_generate_public_release_notes_regression_bug_002(self):
        """BUG-002: Verifies that public release notes in external projects do not hardcode Docs-as-Code install.py."""
        env_info = {
            "has_git": True,
            "mode": "github",
            "branch": "main",
            "remote_url": "https://github.com/someuser/coolproject.git",
        }
        artifacts = [{
            "name": "coolapp.tar.gz",
            "path": "dist/coolapp.tar.gz",
            "size": "500 KB",
            "sha256": "112233445566778899aabbccddeeff00112233445566778899aabbccddeeff00",
        }]
        phase_data = {
            "tasks": [{"id": "TASK-100", "title": "Cool Feature", "link": "../Specs/TASK-100"}],
            "bugs": [],
        }

        # 1. External project with artifacts: should offer artifact download, not install.py
        external_root = self.test_root / "external_project"
        external_root.mkdir()
        notes = kb_release.generate_public_release_notes(
            version="1.0.0",
            phase_num=1,
            env_info=env_info,
            artifacts=artifacts,
            phase_data=phase_data,
            summary="Release 1.0.0",
            repo_root=external_root,
        )
        self.assertNotIn("install.py", notes)
        self.assertNotIn("Новая установка Docs-as-Code", notes)
        self.assertIn("curl -LO https://github.com/someuser/coolproject/releases/download/v1.0.0/coolapp.tar.gz", notes)

        # 2. External project with custom quick_install
        notes_custom = kb_release.generate_public_release_notes(
            version="1.0.0",
            phase_num=1,
            env_info=env_info,
            artifacts=artifacts,
            phase_data=phase_data,
            summary="Release 1.0.0",
            quick_install="pip install coolproject",
            repo_root=external_root,
        )
        self.assertIn("pip install coolproject", notes_custom)
        self.assertNotIn("install.py", notes_custom)

        # 3. External project with no artifacts: should not have Quick Install or dummy install.py checksum
        notes_empty = kb_release.generate_public_release_notes(
            version="1.0.0",
            phase_num=1,
            env_info=env_info,
            artifacts=[],
            phase_data=phase_data,
            summary="Release 1.0.0",
            repo_root=external_root,
        )
        self.assertNotIn("install.py", notes_empty)
        self.assertNotIn("Quick Install", notes_empty)
        self.assertNotIn("Get-FileHash", notes_empty)

        # 4. Harness repo (has install.py and build_installer.py): should keep harness install instructions
        harness_root = self.test_root / "harness_repo"
        harness_root.mkdir()
        (harness_root / "install.py").write_text("# install script", encoding="utf-8")
        (harness_root / "build_installer.py").write_text("# build installer", encoding="utf-8")
        harness_env = {
            "has_git": True,
            "mode": "github",
            "branch": "main",
            "remote_url": "https://github.com/koudinie101-png/agent-docs-harness.git",
        }
        notes_harness = kb_release.generate_public_release_notes(
            version="0.12.0",
            phase_num=15,
            env_info=harness_env,
            artifacts=[],
            phase_data=phase_data,
            summary="Harness release",
            repo_root=harness_root,
        )
        self.assertIn("Новая установка Docs-as-Code", notes_harness)
        self.assertIn("curl -fsSL https://raw.githubusercontent.com/koudinie101-png/agent-docs-harness/main/install.py | python3", notes_harness)
        self.assertIn("python install.py --update", notes_harness)

    def test_generate_public_release_notes_regression_bug_004(self):
        """BUG-004: Verifies Full Changelog link points to compare URL instead of self-linking to current release."""
        env_info = {
            "has_git": True,
            "mode": "github",
            "branch": "main",
            "remote_url": "https://github.com/myorg/coolapp.git",
        }
        phase_data = {
            "tasks": [{"id": "TASK-101", "title": "Some Task", "link": "../Specs/TASK-101"}],
            "bugs": [],
        }

        # 1. Explicit prev_tag provided: must generate compare/prev_tag...tag
        notes = kb_release.generate_public_release_notes(
            version="0.11.0",
            phase_num=11,
            env_info=env_info,
            artifacts=[],
            phase_data=phase_data,
            summary="Release 0.11.0",
            prev_tag="v0.10.0",
        )
        self.assertIn("**Полный список изменений (Full Changelog):** https://github.com/myorg/coolapp/compare/v0.10.0...v0.11.0", notes)
        self.assertNotIn("https://github.com/myorg/coolapp/releases/tag/v0.11.0", notes)

        # 2. Auto-detection via existing release docs in docs/02_Tasks/Releases/
        test_project = self.test_root / "autodetect_project"
        releases_dir = test_project / "docs" / "02_Tasks" / "Releases"
        releases_dir.mkdir(parents=True)
        (releases_dir / "RELEASE-v0.9.0.md").write_text("---\nid: RELEASE-v0.9.0\n---\n", encoding="utf-8")
        (releases_dir / "RELEASE-v0.10.0.md").write_text("---\nid: RELEASE-v0.10.0\n---\n", encoding="utf-8")

        notes_auto = kb_release.generate_public_release_notes(
            version="0.11.0",
            phase_num=11,
            env_info=env_info,
            artifacts=[],
            phase_data=phase_data,
            summary="Release 0.11.0",
            repo_root=test_project,
        )
        self.assertIn("**Полный список изменений (Full Changelog):** https://github.com/myorg/coolapp/compare/v0.10.0...v0.11.0", notes_auto)
        self.assertNotIn("https://github.com/myorg/coolapp/releases/tag/v0.11.0", notes_auto)

        # 3. First release (no previous releases): must link to commits/tag, not releases/tag
        empty_project = self.test_root / "empty_project"
        empty_project.mkdir()
        notes_first = kb_release.generate_public_release_notes(
            version="0.1.0",
            phase_num=1,
            env_info=env_info,
            artifacts=[],
            phase_data=phase_data,
            summary="First release",
            repo_root=empty_project,
        )
        self.assertIn("**Полный список изменений (Full Changelog):** https://github.com/myorg/coolapp/commits/v0.1.0", notes_first)
        self.assertNotIn("https://github.com/myorg/coolapp/releases/tag/v0.1.0", notes_first)

    def test_generate_release_note_filters_adrs_by_phase(self):
        """Verifies internal RELEASE-vX.Y.Z.md filters ADRs to only those relevant to the target phase."""
        docs_dir = self.test_root / "docs"
        adrs_dir = docs_dir / "03_Decisions_ADR"
        specs_dir = docs_dir / "02_Tasks" / "Specs" / "10_SpecLifecycle"
        adrs_dir.mkdir(parents=True)
        specs_dir.mkdir(parents=True)

        (adrs_dir / "ADR-0017-high-snr.md").write_text(
            "---\nid: ADR-0017\ntitle: High-SNR Release Notes\nphase: 10\nstatus: accepted\n---\n# ADR-0017",
            encoding="utf-8"
        )
        (adrs_dir / "ADR-0016-barrier.md").write_text(
            "---\nid: ADR-0016\ntitle: Barrier\nphase: 9\nstatus: accepted\n---\n# ADR-0016",
            encoding="utf-8"
        )
        (specs_dir / "TASK-037-notes.md").write_text(
            "---\nid: TASK-037\ntitle: Release Notes\nphase: 10\nstatus: done\n---\nSee [[ADR-0017]]",
            encoding="utf-8"
        )

        found = kb_release.find_phase_artifacts(docs_dir, phase_num=10)
        adr_ids = [a["id"] for a in found["adrs"]]
        self.assertIn("ADR-0017", adr_ids)
        self.assertNotIn("ADR-0016", adr_ids)

    def test_ci_mode_infers_phase_and_summary_from_existing_release_doc(self):
        """
        REGRESSION TEST for BUG-001:
        In CI mode (e.g. GitHub Actions), kb_release.py is called with:
        `python scripts/kb_release.py --version ${{ github.ref_name }} --ci-mode`
        without `--phase` or `--summary`.
        If docs/02_Tasks/Releases/RELEASE-vX.Y.Z.md already exists with phase: 8 and custom summary,
        kb_release.py MUST infer the phase and summary from that file instead of falling back to Phase 1.
        """
        dist_dir = self.test_root / "dist"
        dist_dir.mkdir()
        (dist_dir / "install.py").write_bytes(b"print('installer')")

        docs_dir = self.test_root / "docs"
        releases_dir = docs_dir / "02_Tasks" / "Releases"
        specs_dir = docs_dir / "02_Tasks" / "Specs" / "08_Greenfield"
        releases_dir.mkdir(parents=True)
        specs_dir.mkdir(parents=True)

        # Create phase 8 task spec
        (specs_dir / "TASK-029-foo.md").write_text(
            "---\nid: TASK-029\ntitle: Undecided Preset\nphase: 8\nstatus: done\n---\n# TASK-029",
            encoding="utf-8"
        )

        # Existing RELEASE-v0.8.0.md created during Mode 3 release cut
        existing_release_doc = (
            "---\n"
            "id: RELEASE-v0.8.0\n"
            "title: \"Релиз v0.8.0: Фаза 8\"\n"
            "version: \"0.8.0\"\n"
            "phase: 8\n"
            "status: completed\n"
            "---\n\n"
            "# 🚀 Релиз v0.8.0: Фаза 8\n\n"
            "## 📋 Обзор релиза (Executive Summary)\n"
            "Greenfield-инициализация от идеи и Living Spec протокол.\n"
        )
        (releases_dir / "RELEASE-v0.8.0.md").write_text(existing_release_doc, encoding="utf-8")

        # Simulate GitHub Actions call: NO --phase, NO --summary
        test_argv = [
            "kb_release.py",
            "--version", "v0.8.0",
            "--ci-mode",
            "--docs-dir", str(docs_dir),
            "--dist-dir", str(dist_dir),
        ]
        with patch.object(sys, "argv", test_argv):
            exit_code = kb_release.main()
            self.assertEqual(exit_code, 0)

        notes_file = dist_dir / "RELEASE_NOTES.md"
        self.assertTrue(notes_file.exists())
        notes_content = notes_file.read_text(encoding="utf-8")

        # Must NOT fallback to Phase 1!
        self.assertNotIn("Фаза 1", notes_content)
        self.assertIn("Фаза 8", notes_content)
        self.assertIn("Greenfield-инициализация от идеи и Living Spec протокол.", notes_content)
        self.assertIn("TASK-029", notes_content)

    def test_cumulative_release_phases_notes_and_doc(self):
        """
        Tests cumulative release cutting across multiple phases (e.g. 9 and 10),
        verifying that tasks from both phases and bugs are bundled,
        ADRs are not dumped into public notes (High-SNR),
        and CI mode can infer cumulative phases from existing release doc.
        """
        dist_dir = self.test_root / "dist"
        dist_dir.mkdir()
        (dist_dir / "install.py").write_bytes(b"print('installer-payload')")

        docs_dir = self.test_root / "docs"
        releases_dir = docs_dir / "02_Tasks" / "Releases"
        specs_p9 = docs_dir / "02_Tasks" / "Specs" / "09_Phase9"
        specs_p10 = docs_dir / "02_Tasks" / "Specs" / "10_Phase10"
        bugs_dir = docs_dir / "02_Tasks" / "Bugs"
        adrs_dir = docs_dir / "03_Decisions_ADR"

        releases_dir.mkdir(parents=True)
        specs_p9.mkdir(parents=True)
        specs_p10.mkdir(parents=True)
        bugs_dir.mkdir(parents=True)
        adrs_dir.mkdir(parents=True)

        (specs_p9 / "TASK-033-barrier.md").write_text(
            "---\nid: TASK-033\ntitle: Single-Task Execution Barrier\nphase: 9\nstatus: done\n---\n# TASK-033",
            encoding="utf-8"
        )
        (specs_p10 / "TASK-036-genesis.md").write_text(
            "---\nid: TASK-036\ntitle: Spec Genesis Protocol\nphase: 10\nstatus: done\n---\n# TASK-036",
            encoding="utf-8"
        )
        (bugs_dir / "BUG-001-fallback.md").write_text(
            "---\nid: BUG-001\ntitle: Release Fallback Defect\nstatus: fixed\n---\n# BUG-001",
            encoding="utf-8"
        )
        (adrs_dir / "ADR-0021-genesis.md").write_text(
            "---\nid: ADR-0021\ntitle: Spec Genesis\nphase: 10\nstatus: accepted\n---\n# ADR-0021",
            encoding="utf-8"
        )

        test_argv = [
            "kb_release.py",
            "--version", "v0.10.0",
            "--phases", "9,10",
            "--docs-dir", str(docs_dir),
            "--dist-dir", str(dist_dir),
            "--summary", "Кумулятивный релиз с барьером выполнения и генезисом спецификации.",
        ]
        with patch.object(sys, "argv", test_argv):
            exit_code = kb_release.main()
            self.assertEqual(exit_code, 0)

        # Verify RELEASE-v0.10.0.md
        release_doc = releases_dir / "RELEASE-v0.10.0.md"
        self.assertTrue(release_doc.exists())
        doc_content = release_doc.read_text(encoding="utf-8")
        self.assertIn("phases: [9, 10]", doc_content)
        self.assertIn("TASK-033", doc_content)
        self.assertIn("TASK-036", doc_content)
        self.assertIn("BUG-001", doc_content)
        self.assertIn("ADR-0021", doc_content)
        self.assertIn("Кумулятивный", doc_content)

        # Verify public dist/RELEASE_NOTES.md
        notes_file = dist_dir / "RELEASE_NOTES.md"
        self.assertTrue(notes_file.exists())
        notes_content = notes_file.read_text(encoding="utf-8")
        self.assertIn("TASK-033", notes_content)
        self.assertIn("TASK-036", notes_content)
        self.assertIn("BUG-001", notes_content)
        self.assertNotIn("ADR-0021", notes_content)  # High-SNR: ADRs excluded from public notes
        self.assertNotIn("Архитектурные решения", notes_content)
        self.assertIn("Кумулятивный", notes_content)

        # Now simulate CI running on git tag without --phase or --phases
        ci_argv = [
            "kb_release.py",
            "--version", "v0.10.0",
            "--ci-mode",
            "--docs-dir", str(docs_dir),
            "--dist-dir", str(dist_dir),
        ]
        with patch.object(sys, "argv", ci_argv):
            exit_code_ci = kb_release.main()
            self.assertEqual(exit_code_ci, 0)

        ci_notes = notes_file.read_text(encoding="utf-8")
        self.assertIn("TASK-033", ci_notes)
        self.assertIn("TASK-036", ci_notes)
        self.assertIn("BUG-001", ci_notes)
        self.assertNotIn("ADR-0021", ci_notes)
        self.assertIn("Кумулятивный", ci_notes)


class TestBugReleaseTargeting(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.test_root = Path(self.tmp_dir.name)
        self.bugs_dir = self.test_root / "docs" / "02_Tasks" / "Bugs"
        self.bugs_dir.mkdir(parents=True)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_collect_fixed_bugs_matching_version(self):
        """Verifies bugs targeted for v0.11.0 via fixed_in or target_release are included."""
        (self.bugs_dir / "BUG-101-crash.md").write_text(
            "---\nid: BUG-101\ntitle: Memory Leak\nstatus: fixed\nfixed_in: v0.11.0\n---\n# BUG-101",
            encoding="utf-8"
        )
        (self.bugs_dir / "BUG-102-ui.md").write_text(
            "---\nid: BUG-102\ntitle: UI Glitch\nstatus: fixed\ntarget_release: v0.11.0\n---\n# BUG-102",
            encoding="utf-8"
        )
        found = kb_release.collect_fixed_bugs(self.bugs_dir, target_version="v0.11.0")
        found_ids = [b["id"] for b in found]
        self.assertIn("BUG-101", found_ids)
        self.assertIn("BUG-102", found_ids)
        self.assertEqual(len(found), 2)

    def test_collect_fixed_bugs_excludes_prior_versions(self):
        """Verifies bugs from prior or future versions are excluded from release notes."""
        (self.bugs_dir / "BUG-001-old.md").write_text(
            "---\nid: BUG-001\ntitle: Old Bug\nstatus: fixed\nfixed_in: v0.10.0\n---\n# BUG-001",
            encoding="utf-8"
        )
        (self.bugs_dir / "BUG-002-past.md").write_text(
            "---\nid: BUG-002\ntitle: Past Issue\nstatus: closed\ntarget_release: v0.09.0\n---\n# BUG-002",
            encoding="utf-8"
        )
        (self.bugs_dir / "BUG-003-current.md").write_text(
            "---\nid: BUG-003\ntitle: Current Bug\nstatus: fixed\nfixed_in: v0.11.0\n---\n# BUG-003",
            encoding="utf-8"
        )
        found = kb_release.collect_fixed_bugs(self.bugs_dir, target_version="v0.11.0")
        found_ids = [b["id"] for b in found]
        self.assertEqual(found_ids, ["BUG-003"])
        self.assertNotIn("BUG-001", found_ids)
        self.assertNotIn("BUG-002", found_ids)

    def test_check_release_blockers_aborts_on_open_blocker(self):
        """Verifies open defects with release_blocker: true return errors and abort release."""
        (self.bugs_dir / "BUG-099-blocker.md").write_text(
            "---\nid: BUG-099\ntitle: Fatal Crash On Start\nstatus: open\nrelease_blocker: true\ntarget_release: v0.11.0\n---\n# BUG-099",
            encoding="utf-8"
        )
        errors = kb_release.check_release_blockers(self.bugs_dir, target_version="v0.11.0")
        self.assertEqual(len(errors), 1)
        self.assertIn("BUG-099", errors[0])
        self.assertIn("release_blocker=true", errors[0])

        # Test CLI abort
        dist_dir = self.test_root / "dist"
        dist_dir.mkdir(parents=True)
        (dist_dir / "app.tar.gz").write_bytes(b"payload")
        argv = [
            "kb_release.py",
            "--version", "v0.11.0",
            "--phase", "11",
            "--docs-dir", str(self.test_root / "docs"),
            "--dist-dir", str(dist_dir),
        ]
        with patch.object(sys, "argv", argv):
            exit_code = kb_release.main()
            self.assertEqual(exit_code, 1)

    def test_check_release_blockers_passes_when_fixed(self):
        """Verifies resolved defects with release_blocker: true do not block release."""
        (self.bugs_dir / "BUG-099-blocker.md").write_text(
            "---\nid: BUG-099\ntitle: Fatal Crash On Start\nstatus: fixed\nrelease_blocker: true\nfixed_in: v0.11.0\n---\n# BUG-099",
            encoding="utf-8"
        )
        errors = kb_release.check_release_blockers(self.bugs_dir, target_version="v0.11.0")
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()

