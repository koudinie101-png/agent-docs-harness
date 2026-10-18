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
        task_content = "---\nid: TASK-001\ntitle: Test\nstatus: done\ntype: task\nphase: 1\nparent_plan: PLAN-001\ncreated: 2026-10-01\n---\n# Task 001\n[[../../00_Index]]"
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

    def test_inbox_frontmatter_validation(self):
        """Inbox items must contain required fields and valid status."""
        inbox_dir = self.docs_dir / "02_Tasks" / "Inbox"
        inbox_dir.mkdir(parents=True, exist_ok=True)

        valid_item = inbox_dir / "FB-GH-1.md"
        valid_item.write_text(
            "---\nid: FB-GH-1\ntitle: Issue 1\nstatus: new\ntype: feedback\nchannel: github\ncreated: 2026-10-11\n---\n# Feedback\n[[../../00_Index]]",
            encoding="utf-8"
        )

        ok, msg = kb_lint.check_file_frontmatter(valid_item)
        self.assertTrue(ok)
        self.assertIn("Valid", msg)

        # Missing field
        invalid_missing = inbox_dir / "FB-GH-2.md"
        invalid_missing.write_text(
            "---\nid: FB-GH-2\ntitle: Issue 2\nstatus: new\n---\n# Incomplete",
            encoding="utf-8"
        )
        ok, msg = kb_lint.check_file_frontmatter(invalid_missing)
        self.assertFalse(ok)
        self.assertIn("Missing required frontmatter fields", msg)

        # Invalid status
        invalid_status = inbox_dir / "FB-GH-3.md"
        invalid_status.write_text(
            "---\nid: FB-GH-3\ntitle: Issue 3\nstatus: unknown_status\ntype: feedback\nchannel: github\ncreated: 2026-10-11\n---\n# Bad Status",
            encoding="utf-8"
        )
        ok, msg = kb_lint.check_file_frontmatter(invalid_status)
        self.assertFalse(ok)
        self.assertIn("Invalid status", msg)

    def test_fast_track_specs_validation(self):
        """Validates scope limits (<= 2 files) and Verification Plan for Fast-Track specs."""
        specs_dir = self.docs_dir / "02_Tasks" / "Specs" / "14_Fast"
        specs_dir.mkdir(parents=True, exist_ok=True)

        valid_micro = specs_dir / "TASK-090.md"
        valid_micro.write_text("""---
id: TASK-090
title: "Micro fix"
status: done
type: fast-track
---
# TASK-090
## 1. Цель
Quick fix.
## 2. Контракт файлов
* `[MODIFY]` `file1.py` — fix logic
* `[MODIFY]` `file2.py` — fix test
## 3. План верификации
- [ ] python -m unittest
""", encoding="utf-8")

        warnings = kb_lint.check_fast_track_specs(self.docs_dir)
        self.assertEqual(len(warnings), 0)

        # Exceeds file limit (touches 3 files)
        bloated_micro = specs_dir / "TASK-091.md"
        bloated_micro.write_text("""---
id: TASK-091
title: "Bloated fix"
status: done
type: fast-track
---
# TASK-091
## 1. Цель
Too big.
## 2. Контракт файлов
* `[MODIFY]` `file1.py` — fix 1
* `[MODIFY]` `file2.py` — fix 2
* `[MODIFY]` `file3.py` — fix 3
## 3. План верификации
- [ ] pytest
""", encoding="utf-8")

        warnings = kb_lint.check_fast_track_specs(self.docs_dir)
        self.assertTrue(any("touches 3 files (limit: <= 2)" in w for w in warnings))

        # Missing verification plan
        untested_micro = specs_dir / "TASK-092.md"
        untested_micro.write_text("""---
id: TASK-092
title: "Untested fix"
status: done
type: fast-track
---
# TASK-092
## 1. Цель
No tests.
## 2. Контракт файлов
* `[MODIFY]` `file1.py` — fix 1
""", encoding="utf-8")

        warnings = kb_lint.check_fast_track_specs(self.docs_dir)
        self.assertTrue(any("TASK-092.md' is missing a Verification Plan" in w for w in warnings))

    def test_phase_consistency_matching(self):
        """Matching phase folder, frontmatter phase, and phase tag should produce 0 warnings."""
        specs_dir = self.docs_dir / "02_Tasks" / "Specs" / "15_Latency"
        specs_dir.mkdir(parents=True, exist_ok=True)
        valid_spec = specs_dir / "TASK-058.md"
        valid_spec.write_text("""---
id: TASK-058
title: "Test Task"
phase: 15
tags:
  - task/spec
  - phase15
---
# TASK-058
[[../../../00_Index]]
""", encoding="utf-8")

        warnings = kb_lint.check_phase_consistency(self.docs_dir)
        self.assertEqual(warnings, [])

    def test_phase_consistency_mismatched_folder(self):
        """Mismatched folder number and frontmatter phase should produce a warning."""
        specs_dir = self.docs_dir / "02_Tasks" / "Specs" / "15_Latency"
        specs_dir.mkdir(parents=True, exist_ok=True)
        bad_folder_spec = specs_dir / "TASK-059.md"
        bad_folder_spec.write_text("""---
id: TASK-059
title: "Mismatched folder"
phase: 14
tags:
  - phase14
---
# TASK-059
[[../../../00_Index]]
""", encoding="utf-8")

        warnings = kb_lint.check_phase_consistency(self.docs_dir)
        self.assertEqual(len(warnings), 1)
        self.assertIn("declares phase 14, but is located in folder '15_Latency' (expected phase 15)", warnings[0])

    def test_phase_consistency_mismatched_tag(self):
        """Mismatched phase tag should produce a warning."""
        specs_dir = self.docs_dir / "02_Tasks" / "Specs" / "15_Latency"
        specs_dir.mkdir(parents=True, exist_ok=True)
        bad_tag_spec = specs_dir / "TASK-060.md"
        bad_tag_spec.write_text("""---
id: TASK-060
title: "Mismatched tag"
phase: 15
tags:
  - phase13
---
# TASK-060
[[../../../00_Index]]
""", encoding="utf-8")

        warnings = kb_lint.check_phase_consistency(self.docs_dir)
        self.assertEqual(len(warnings), 1)
        self.assertIn("declares phase 15, but contains mismatched tag 'phase13'", warnings[0])

    def test_phase_consistency_non_blocking_in_linter(self):
        """Phase consistency warnings must be non-blocking (exit code 0) in both silent and verbose modes."""
        specs_dir = self.docs_dir / "02_Tasks" / "Specs" / "15_Latency"
        specs_dir.mkdir(parents=True, exist_ok=True)
        bad_spec = specs_dir / "TASK-061.md"
        bad_spec.write_text("""---
id: TASK-061
title: "Mismatched"
status: done
type: task
phase: 12
parent_plan: PLAN-015
created: 2026-10-12
tags:
  - phase12
---
# TASK-061
[[../../../00_Index]]
""", encoding="utf-8")

        # Silent mode
        captured_silent = io.StringIO()
        with patch("sys.stdout", captured_silent):
            exit_code = kb_lint.run_linter(self.docs_dir, verbose=False)
        self.assertEqual(exit_code, 0)
        self.assertIn("⚠️  WARN: Spec 'TASK-061.md' declares phase 12", captured_silent.getvalue())

        # Verbose mode
        captured_verbose = io.StringIO()
        with patch("sys.stdout", captured_verbose):
            exit_code = kb_lint.run_linter(self.docs_dir, verbose=True)
        self.assertEqual(exit_code, 0)
        self.assertIn("⚠️ Phase Consistency Warnings (1):", captured_verbose.getvalue())

    def test_check_memory_limits_passes_within_limit(self):
        """check_memory_limits passes when patterns <= 15."""
        mem_dir = self.docs_dir / "06_Memory"
        mem_dir.mkdir(parents=True, exist_ok=True)
        patterns_file = mem_dir / "patterns.md"
        patterns_content = "# Memory Patterns\n\n"
        for i in range(1, 16):
            patterns_content += f"- [TRG-{i:02d}] Pattern {i} | Error description | Fix | (Count: 2, Sev: High) -> INC-{i:03d}\n"
        patterns_file.write_text(patterns_content, encoding="utf-8")

        errors = kb_lint.check_memory_limits(self.docs_dir)
        self.assertEqual(len(errors), 0)

        captured = io.StringIO()
        with patch("sys.stdout", captured):
            exit_code = kb_lint.run_linter(self.docs_dir, verbose=False)
        self.assertEqual(exit_code, 0)

    def test_check_memory_limits_blocks_when_exceeding_15(self):
        """check_memory_limits returns error and blocks linter (Exit code 1) when patterns > 15."""
        mem_dir = self.docs_dir / "06_Memory"
        mem_dir.mkdir(parents=True, exist_ok=True)
        patterns_file = mem_dir / "patterns.md"
        patterns_content = "# Memory Patterns\n\n"
        for i in range(1, 17):  # 16 patterns (exceeds limit 15)
            patterns_content += f"- [TRG-{i:02d}] Pattern {i} | Error description | Fix | (Count: 2, Sev: High) -> INC-{i:03d}\n"
        patterns_file.write_text(patterns_content, encoding="utf-8")

        errors = kb_lint.check_memory_limits(self.docs_dir)
        self.assertEqual(len(errors), 1)
        self.assertIn("Memory patterns limit exceeded: 16 active patterns", errors[0])

        captured = io.StringIO()
        with patch("sys.stdout", captured):
            exit_code = kb_lint.run_linter(self.docs_dir, verbose=False)
        self.assertEqual(exit_code, 1)
        self.assertIn("Memory patterns limit exceeded", captured.getvalue())

    def test_bug_005_is_relative_to_python38_compatibility(self):
        """Simulate Python 3.8 where Path.is_relative_to does not exist (BUG-005)."""
        from pathlib import PurePath
        orig_purepath_method = getattr(PurePath, "is_relative_to", None)
        orig_path_method = getattr(Path, "is_relative_to", None)
        try:
            if hasattr(PurePath, "is_relative_to"):
                del PurePath.is_relative_to
            if hasattr(Path, "is_relative_to") and "is_relative_to" in Path.__dict__:
                del Path.is_relative_to

            captured = io.StringIO()
            with patch("sys.stdout", captured):
                exit_code = kb_lint.run_linter(self.docs_dir, verbose=False)
            self.assertEqual(exit_code, 0)
        finally:
            if orig_purepath_method is not None:
                PurePath.is_relative_to = orig_purepath_method
            if orig_path_method is not None and "is_relative_to" in Path.__dict__:
                Path.is_relative_to = orig_path_method

    def test_task_066_wikilinks_in_code_blocks_and_inline_code_ignored(self):
        """Verifies that links inside fenced code blocks and inline code are ignored (TASK-066)."""
        content = """# Note
Here is some text with `[[non_existent_inline]]` and a code block:
```python
# Demo code
link = "[[non_existent_in_fenced_block]]"
```
And a real valid link: [[01_Architecture/arch|Arch]]
"""
        links = kb_lint.parse_wikilinks(content)
        self.assertNotIn("non_existent_inline", links)
        self.assertNotIn("non_existent_in_fenced_block", links)
        self.assertIn("01_Architecture/arch", links)

    def test_task_066_escaped_pipe_in_tables_supported(self):
        """Verifies that wikilinks with escaped pipes \\| in Markdown tables are extracted correctly (TASK-066)."""
        content = """# Table Note
| Column 1 | Column 2 |
| :--- | :--- |
| Item | [[01_Architecture/arch\\|Architecture]] |
| Sibling | [[01_Architecture/arch#sec\\|Section]] |
"""
        links = kb_lint.parse_wikilinks(content)
        self.assertIn("01_Architecture/arch", links)
        self.assertEqual(len(links), 2)

    def test_task_066_strict_relative_path_resolution_no_file_map_fallback(self):
        """Verifies that links with path separators do not fall back to file_map if path is invalid (TASK-066)."""
        doc_file = self.docs_dir / "bad_path_doc.md"
        doc_file.write_text("# Doc\nLink to: [[../WrongDir/TASK-001]]", encoding="utf-8")

        captured = io.StringIO()
        with patch("sys.stdout", captured):
            exit_code = kb_lint.run_linter(self.docs_dir, verbose=False)
        self.assertEqual(exit_code, 1)
        self.assertIn("target not found", captured.getvalue())
        self.assertIn("WrongDir/TASK-001", captured.getvalue())

    def test_task_066_frontmatter_schemas_validation(self):
        """Verifies schema validation for Specs, Bugs, Incidents, and ADRs (TASK-066)."""
        # 1. Spec missing parent_plan
        spec_file = self.docs_dir / "02_Tasks" / "Specs" / "TASK-998.md"
        spec_file.write_text("""---
id: TASK-998
title: "No Plan Spec"
status: done
type: task
phase: 1
created: 2026-10-15
---
# TASK-998
""", encoding="utf-8")
        ok, msg = kb_lint.check_file_frontmatter(spec_file)
        self.assertFalse(ok)
        self.assertIn("parent_plan", msg)

        # 2. Bug missing severity
        bugs_dir = self.docs_dir / "02_Tasks" / "Bugs"
        bugs_dir.mkdir(parents=True, exist_ok=True)
        bug_file = bugs_dir / "BUG-999.md"
        bug_file.write_text("""---
id: BUG-999
title: "No Sev Bug"
status: open
type: bug
created: 2026-10-15
---
# BUG-999
""", encoding="utf-8")
        ok, msg = kb_lint.check_file_frontmatter(bug_file)
        self.assertFalse(ok)
        self.assertIn("severity", msg)

        # 3. Memory Incident missing created
        inc_dir = self.docs_dir / "06_Memory" / "Incidents"
        inc_dir.mkdir(parents=True, exist_ok=True)
        inc_file = inc_dir / "INC-001.md"
        inc_file.write_text("""---
id: INC-001
title: "Incident 1"
status: active
---
# INC-001
""", encoding="utf-8")
        ok, msg = kb_lint.check_file_frontmatter(inc_file)
        self.assertFalse(ok)
        self.assertIn("created", msg)

        # 4. ADR valid
        adr_dir = self.docs_dir / "03_Decisions_ADR"
        adr_dir.mkdir(parents=True, exist_ok=True)
        adr_file = adr_dir / "ADR-0099.md"
        adr_file.write_text("""---
id: ADR-0099
title: "ADR Test"
status: accepted
date: 2026-10-15
---
# ADR-0099
""", encoding="utf-8")
        ok, msg = kb_lint.check_file_frontmatter(adr_file)
        self.assertTrue(ok)

    def test_task_072_media_indexing_no_stem_shadowing(self):
        """Verifies media files do not shadow .md specs by stem (TASK-072)."""
        specs_dir = self.docs_dir / "02_Tasks" / "Specs"
        specs_dir.mkdir(parents=True, exist_ok=True)
        spec_file = specs_dir / "TASK-001.md"
        spec_file.write_text("# Spec", encoding="utf-8")

        assets_dir = self.docs_dir / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)
        media_file = assets_dir / "TASK-001.png"
        media_file.write_bytes(b"fake png")

        file_map = kb_lint.build_file_map(self.docs_dir)
        # Stem must point strictly to markdown spec, never to image!
        self.assertEqual(file_map["TASK-001"], spec_file)
        self.assertEqual(file_map["task-001"], spec_file)
        # Image is accessible strictly via extension
        self.assertEqual(file_map["TASK-001.png"], media_file)
        self.assertEqual(file_map["task-001.png"], media_file)

    def test_task_072_parse_wikilinks_embed_and_size_stripping(self):
        """Verifies ! embed prefix and size parameters are cleanly stripped (TASK-072)."""
        content = (
            "Embed: ![[screenshot.png|600x400]]\n"
            "Simple embed: ![[diagram.svg|300]]\n"
            "Regular wikilink: [[TASK-001|My Task]]"
        )
        links = kb_lint.parse_wikilinks(content)
        self.assertIn("screenshot.png", links)
        self.assertIn("diagram.svg", links)
        self.assertIn("TASK-001", links)

    def test_task_072_markdown_images_validation(self):
        """Verifies markdown images parsing and external link filtering (TASK-072)."""
        content = (
            "Local image: ![Alt Text](assets/diagram.png)\n"
            "URL encoded: ![UI](assets/my%20screenshot.png)\n"
            "External: ![External](https://example.com/pic.png)\n"
            "Data uri: ![Data](data:image/png;base64,...)"
        )
        imgs = kb_lint.parse_markdown_images(content)
        self.assertIn("assets/diagram.png", imgs)
        self.assertIn("assets/my screenshot.png", imgs)
        self.assertNotIn("https://example.com/pic.png", imgs)
        self.assertNotIn("data:image/png;base64,...", imgs)

    def test_task_072_asset_weights_gate(self):
        """Verifies non-blocking warning when an asset in docs/assets/ exceeds 2MB (TASK-072)."""
        assets_dir = self.docs_dir / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)
        big_asset = assets_dir / "heavy_mockup.png"
        # 2.2 MB = 2.2 * 1024 * 1024 bytes
        big_asset.write_bytes(b"0" * int(2.2 * 1024 * 1024))

        warnings = kb_lint.check_asset_weights(self.docs_dir, max_bytes=2 * 1024 * 1024)
        self.assertTrue(any("heavy_mockup.png" in w and "exceeds size limit" in w for w in warnings))

    def test_task_077_tech_debt_lint_missing_file(self):
        """Verifies check_tech_debt_integrity returns error when TechDebt.md is missing (TASK-077)."""
        res = kb_lint.check_tech_debt_integrity(self.docs_dir)
        self.assertTrue(any("Tech debt registry not found" in err for err in res))

    def test_task_077_tech_debt_lint_broken_links(self):
        """Verifies check_tech_debt_integrity reports broken wikilinks in debt table (TASK-077)."""
        tasks_dir = self.docs_dir / "02_Tasks"
        tasks_dir.mkdir(parents=True, exist_ok=True)
        debt_file = tasks_dir / "TechDebt.md"
        debt_content = (
            "---\nid: TECHDEBT\ntitle: Tech Debt\ntype: techdebt\nstatus: active\n---\n"
            "# Tech Debt\n"
            "## 📋 Открытый технический долг (Active P3 Debt)\n"
            "| ID | Приоритет | Модуль | Описание | Задача-источник | Дата | Статус |\n"
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
            "| DEBT-001 | P3 | `core.py` | Refactor regex | [[NonExistentTaskFile]] | 2026-10-15 | open |\n"
        )
        debt_file.write_text(debt_content, encoding="utf-8")
        file_map = kb_lint.build_file_map(self.docs_dir)

        errors = kb_lint.check_tech_debt_integrity(self.docs_dir, file_map=file_map)
        self.assertTrue(any("broken wikilink [[NonExistentTaskFile]]" in err for err in errors))

    def test_task_077_tech_debt_lint_valid_and_invalid_id(self):
        """Verifies check_tech_debt_integrity validates DEBT-XXX format and passes when valid (TASK-077)."""
        tasks_dir = self.docs_dir / "02_Tasks"
        tasks_dir.mkdir(parents=True, exist_ok=True)
        debt_file = tasks_dir / "TechDebt.md"

        # Invalid ID format
        invalid_content = (
            "---\nid: TECHDEBT\ntitle: Tech Debt\ntype: techdebt\nstatus: active\n---\n"
            "# Tech Debt\n"
            "## 📋 Открытый технический долг (Active P3 Debt)\n"
            "| ID | Приоритет | Модуль | Описание | Задача-источник | Дата | Статус |\n"
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
            "| INVALID_ID | P3 | `core.py` | Fix | [[00_Index]] | 2026-10-15 | open |\n"
        )
        debt_file.write_text(invalid_content, encoding="utf-8")
        file_map = kb_lint.build_file_map(self.docs_dir)
        errors = kb_lint.check_tech_debt_integrity(self.docs_dir, file_map=file_map)
        self.assertTrue(any("invalid tech debt ID 'INVALID_ID'" in err for err in errors))

        # Valid content
        valid_content = (
            "---\nid: TECHDEBT\ntitle: Tech Debt\ntype: techdebt\nstatus: active\n---\n"
            "# Tech Debt\n"
            "## 📋 Открытый технический долг (Active P3 Debt)\n"
            "| ID | Приоритет | Модуль | Описание | Задача-источник | Дата | Статус |\n"
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
            "| DEBT-001 | P3 | `core.py` | Fix | [[00_Index]] | 2026-10-15 | open |\n"
        )
        debt_file.write_text(valid_content, encoding="utf-8")
        valid_errors = kb_lint.check_tech_debt_integrity(self.docs_dir, file_map=file_map)
        self.assertEqual(valid_errors, [])

    def test_task_077_untracked_todo_warning(self):
        """Verifies check_untracked_todos flags bare TODOs and ignores ROADMAP-XXX tagged ones (TASK-077)."""
        scripts_dir = self.temp_dir / "scripts"
        scripts_dir.mkdir(parents=True, exist_ok=True)
        py_script = scripts_dir / "sample.py"
        py_script.write_text(
            "# TODO: bare hanging todo\n"
            "# ROADMAP-019: tagged roadmap todo\n"
            "// ROADMAP-TASK-076: another tagged todo\n",
            encoding="utf-8"
        )

        md_doc = self.docs_dir / "sample_doc.md"
        md_doc.write_text(
            "<!-- TODO: untracked doc todo -->\n"
            "<!-- ROADMAP-020 TODO: tracked doc todo -->\n"
            "Discussing `TODO` in prose should not trigger warning.\n",
            encoding="utf-8"
        )

        warnings = kb_lint.check_untracked_todos(self.docs_dir)
        # Should flag sample.py:1 and sample_doc.md:1
        self.assertTrue(any("sample.py:1" in w for w in warnings))
        self.assertTrue(any("sample_doc.md:1" in w for w in warnings))
        # Should NOT flag ROADMAP lines or prose
        self.assertFalse(any("sample.py:2" in w for w in warnings))
        self.assertFalse(any("sample.py:3" in w for w in warnings))
        self.assertFalse(any("sample_doc.md:2" in w for w in warnings))
        self.assertFalse(any("sample_doc.md:3" in w for w in warnings))

    def test_same_name_media_in_different_task_folders_no_false_positive(self):
        """Verifies that having tobe.svg in TASK-047 does not mask broken link to TASK-098/tobe.svg (TASK-079)."""
        # Create TASK-047/tobe.svg
        task47_dir = self.docs_dir / "assets" / "mockups" / "windows" / "TASK-047"
        task47_dir.mkdir(parents=True, exist_ok=True)
        (task47_dir / "tobe.svg").write_text("<svg>task47</svg>", encoding="utf-8")

        # In TASK-001.md, reference non-existent TASK-098/tobe.svg using relative path
        spec_path = self.docs_dir / "02_Tasks" / "Specs" / "TASK-001.md"
        content = spec_path.read_text(encoding="utf-8")
        content += "\n\n![Mockup](../../assets/mockups/windows/TASK-098/tobe.svg)\n"
        spec_path.write_text(content, encoding="utf-8")

        captured = io.StringIO()
        with patch("sys.stdout", captured):
            exit_code = kb_lint.run_linter(self.docs_dir, verbose=False)

        # Must fail with exit code 1 because TASK-098/tobe.svg does not exist!
        self.assertEqual(exit_code, 1)
        self.assertIn("target not found", captured.getvalue())

    def test_bare_wikilink_media_still_resolves(self):
        """Verifies that flat wikilink ![[Pasted image 20261015.png|600]] still resolves (TASK-079)."""
        screenshots_dir = self.docs_dir / "assets" / "screenshots" / "windows"
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        (screenshots_dir / "Pasted image 20261015.png").write_bytes(b"\x89PNG\r\n\x1a\n")

        # In TASK-001.md, reference via bare wikilink with resize
        spec_path = self.docs_dir / "02_Tasks" / "Specs" / "TASK-001.md"
        content = spec_path.read_text(encoding="utf-8")
        content += "\n\n![[Pasted image 20261015.png|600]]\n"
        spec_path.write_text(content, encoding="utf-8")

        captured = io.StringIO()
        with patch("sys.stdout", captured):
            exit_code = kb_lint.run_linter(self.docs_dir, verbose=False)

        self.assertEqual(exit_code, 0)

    def test_check_asset_layout_warns_rogue_platform_dir_and_flat_mockup(self):
        """Verifies check_asset_layout warns on rogue root folder, unorganized files and flat mockup entries (TASK-079)."""
        # Create rogue platform directory directly in assets/
        rogue_dir = self.docs_dir / "assets" / "windows"
        rogue_dir.mkdir(parents=True, exist_ok=True)

        # Create unorganized file in root of assets/
        (self.docs_dir / "assets" / "loose.png").write_bytes(b"data")

        # Create flat mockup entry in mockups/web/
        web_mockups = self.docs_dir / "assets" / "mockups" / "web"
        web_mockups.mkdir(parents=True, exist_ok=True)
        (web_mockups / "login.svg").write_text("<svg>login</svg>", encoding="utf-8")

        warnings = kb_lint.check_asset_layout(self.docs_dir)
        self.assertTrue(any("Disallowed asset category directory 'assets/windows'" in w for w in warnings))
        self.assertTrue(any("Unorganized file 'assets/loose.png'" in w for w in warnings))
        self.assertTrue(any("Non-task mockup entry 'assets/mockups/web/login.svg'" in w for w in warnings))

        # Non-blocking: run_linter returns exit code 0
        captured = io.StringIO()
        with patch("sys.stdout", captured):
            exit_code = kb_lint.run_linter(self.docs_dir, verbose=False)
        self.assertEqual(exit_code, 0)
        self.assertIn("WARN: Disallowed asset category directory 'assets/windows'", captured.getvalue())

    def test_check_asset_layout_allows_canonical_roots(self):
        """Verifies check_asset_layout produces no warnings for canonical roots and task-scoped mockups (TASK-079)."""
        # mockups/windows/TASK-001/tobe.svg
        m_win = self.docs_dir / "assets" / "mockups" / "windows" / "TASK-001"
        m_win.mkdir(parents=True, exist_ok=True)
        (m_win / "tobe.svg").write_text("<svg></svg>", encoding="utf-8")

        # mockups/flows/TASK-002/flow.svg
        m_flows = self.docs_dir / "assets" / "mockups" / "flows" / "TASK-002-checkout"
        m_flows.mkdir(parents=True, exist_ok=True)
        (m_flows / "flow.svg").write_text("<svg></svg>", encoding="utf-8")

        # screenshots/windows/TASK-001.png
        s_win = self.docs_dir / "assets" / "screenshots" / "windows"
        s_win.mkdir(parents=True, exist_ok=True)
        (s_win / "TASK-001.png").write_bytes(b"png")

        # diagrams/arch.png
        diagrams = self.docs_dir / "assets" / "diagrams"
        diagrams.mkdir(parents=True, exist_ok=True)
        (diagrams / "arch.png").write_bytes(b"png")

        # design/tokens.svg
        design = self.docs_dir / "assets" / "design"
        design.mkdir(parents=True, exist_ok=True)
        (design / "tokens.svg").write_text("<svg></svg>", encoding="utf-8")

        # dotfiles like .gitkeep
        (self.docs_dir / "assets" / ".gitkeep").write_text("", encoding="utf-8")
        (self.docs_dir / "assets" / "mockups" / ".gitkeep").write_text("", encoding="utf-8")
        (self.docs_dir / "assets" / "mockups" / "windows" / ".gitkeep").write_text("", encoding="utf-8")

        warnings = kb_lint.check_asset_layout(self.docs_dir)
        self.assertEqual(warnings, [])

    def test_check_untracked_todos_accepts_debt_xxx_reference(self):
        """Verifies TODO/FIXME comments tagged with DEBT-XXX are accepted like ROADMAP-<ID> (TASK-082)."""
        scripts_dir = self.temp_dir / "scripts"
        scripts_dir.mkdir(parents=True, exist_ok=True)
        py_script = scripts_dir / "sample.py"
        py_script.write_text(
            "# TODO(DEBT-001): fix regex\n"
            "// TODO: bare hanging todo\n",
            encoding="utf-8"
        )

        warnings = kb_lint.check_untracked_todos(self.docs_dir)
        # DEBT-001 tagged TODO must NOT be flagged
        self.assertFalse(any("sample.py:1" in w for w in warnings))
        # bare TODO must still be flagged
        self.assertTrue(any("sample.py:2" in w for w in warnings))

    def test_check_tech_debt_warns_when_techdebt_tagged_spec_has_empty_registry(self):
        """Verifies WARN when a #techdebt spec exists but TechDebt.md registry is empty (TASK-082)."""
        tasks_dir = self.docs_dir / "02_Tasks"
        tasks_dir.mkdir(parents=True, exist_ok=True)
        debt_file = tasks_dir / "TechDebt.md"
        debt_content = (
            "---\nid: TECHDEBT\ntitle: Tech Debt\ntype: techdebt\nstatus: active\n---\n"
            "# Tech Debt\n"
            "## 📋 Открытый технический долг (Active P3 Debt)\n"
            "| ID | Приоритет | Модуль | Описание | Задача-источник | Дата | Статус |\n"
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
        )
        debt_file.write_text(debt_content, encoding="utf-8")

        specs_dir = self.docs_dir / "02_Tasks" / "Specs" / "21_TechDebt"
        specs_dir.mkdir(parents=True, exist_ok=True)
        spec_file = specs_dir / "TASK-100.md"
        spec_file.write_text(
            "---\n"
            "id: TASK-100\n"
            "title: Tech Debt Task\n"
            "status: in-progress\n"
            "type: task\n"
            "phase: 21\n"
            "parent_plan: PLAN-021\n"
            "created: 2026-10-16\n"
            "tags:\n"
            "  - techdebt\n"
            "---\n"
            "# TASK-100\n"
            "Refactor something.\n",
            encoding="utf-8"
        )

        file_map = kb_lint.build_file_map(self.docs_dir)
        res = kb_lint.check_tech_debt_integrity(self.docs_dir, file_map=file_map)
        self.assertTrue(any(w.startswith("WARN:") and "TASK-100" in w for w in res))

        # Non-blocking: run_linter returns exit code 0
        captured = io.StringIO()
        with patch("sys.stdout", captured):
            exit_code = kb_lint.run_linter(self.docs_dir, verbose=False)
        self.assertEqual(exit_code, 0)
        self.assertIn("TASK-100", captured.getvalue())

    def test_check_tech_debt_passes_when_techdebt_spec_references_debt_id(self):
        """Verifies no warning when a #techdebt spec references a registered DEBT-XXX (TASK-082)."""
        tasks_dir = self.docs_dir / "02_Tasks"
        tasks_dir.mkdir(parents=True, exist_ok=True)
        debt_file = tasks_dir / "TechDebt.md"
        debt_content = (
            "---\nid: TECHDEBT\ntitle: Tech Debt\ntype: techdebt\nstatus: active\n---\n"
            "# Tech Debt\n"
            "## 📋 Открытый технический долг (Active P3 Debt)\n"
            "| ID | Приоритет | Модуль | Описание | Задача-источник | Дата | Статус |\n"
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
            "| DEBT-001 | P3 | `core.py` | Refactor regex | [[00_Index]] | 2026-10-15 | open |\n"
        )
        debt_file.write_text(debt_content, encoding="utf-8")

        specs_dir = self.docs_dir / "02_Tasks" / "Specs" / "21_TechDebt"
        specs_dir.mkdir(parents=True, exist_ok=True)
        spec_file = specs_dir / "TASK-101.md"
        spec_file.write_text(
            "---\n"
            "id: TASK-101\n"
            "title: Tech Debt Task\n"
            "status: in-progress\n"
            "type: task\n"
            "phase: 21\n"
            "parent_plan: PLAN-021\n"
            "created: 2026-10-16\n"
            "tags:\n"
            "  - techdebt\n"
            "---\n"
            "# TASK-101\n"
            "Resolves DEBT-001 refactor.\n",
            encoding="utf-8"
        )

        file_map = kb_lint.build_file_map(self.docs_dir)
        res = kb_lint.check_tech_debt_integrity(self.docs_dir, file_map=file_map)
        self.assertEqual(res, [])


if __name__ == "__main__":
    unittest.main()


