#!/usr/bin/env python3
"""
Unit and integration tests for scripts/kb_state.py.
Tests frontmatter parsing, deterministic 5-level next action resolution,
summary aggregation, CLI arguments, and execution performance.
"""

import sys
import io
import json
import time
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Add scripts directory to sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import kb_state


class TestKbStateParser(unittest.TestCase):
    def test_empty_and_no_frontmatter(self):
        self.assertEqual(kb_state.parse_frontmatter(""), {})
        self.assertEqual(kb_state.parse_frontmatter("# Just a title"), {})
        self.assertEqual(kb_state.parse_frontmatter("---\nnot closed"), {})

    def test_full_task_frontmatter(self):
        doc = """---
id: TASK-042
title: "Название задачи" # инлайн комментарий
status: in-progress # planned | in-progress | done | cancelled
type: task
phase: 30
release_blocker: false
target_release: "v0.30.0"
depends_on: [TASK-040, "[[TASK-041|Метка]]"]
---
# TASK-042
"""
        fm = kb_state.parse_frontmatter(doc)
        self.assertEqual(fm["id"], "TASK-042")
        self.assertEqual(fm["title"], "Название задачи")
        self.assertEqual(fm["status"], "in-progress")
        self.assertEqual(fm["type"], "task")
        self.assertEqual(fm["phase"], 30)
        self.assertFalse(fm["release_blocker"])
        self.assertEqual(fm["target_release"], "v0.30.0")
        self.assertEqual(fm["depends_on"], ["TASK-040", "TASK-041"])

    def test_block_depends_on_and_wikilinks(self):
        doc = """---
id: TASK-050
title: Block depends
status: planned
depends_on:
  - TASK-048
  - "[[Specs/30_Phase/TASK-049]]"
---
"""
        fm = kb_state.parse_frontmatter(doc)
        self.assertEqual(fm["depends_on"], ["TASK-048", "TASK-049"])

    def test_status_normalization(self):
        cases = [
            ("done", "done"),
            ("completed", "done"),
            ("fixed", "done"),
            ("closed", "done"),
            ("выполнено", "done"),
            ("done # comment", "done"),
            ("in-progress", "in-progress"),
            ("in_progress", "in-progress"),
            ("planned", "planned"),
            ("cancelled", "cancelled"),
        ]
        for raw, expected in cases:
            doc = f"---\nid: TASK-001\nstatus: {raw}\n---\n"
            fm = kb_state.parse_frontmatter(doc)
            self.assertEqual(fm["status"], expected, f"Failed for {raw}")

    def test_release_blocker_boolean_variants(self):
        true_doc = "---\nid: BUG-001\nrelease_blocker: true\n---\n"
        self.assertTrue(kb_state.parse_frontmatter(true_doc)["release_blocker"])

        false_doc = "---\nid: BUG-001\nrelease_blocker: false\n---\n"
        self.assertFalse(kb_state.parse_frontmatter(false_doc)["release_blocker"])


class TestKbStateResolution(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())
        self.docs_dir = self.tmp_dir / "docs"
        self.specs_dir = self.docs_dir / "02_Tasks" / "Specs" / "01_Phase"
        self.bugs_dir = self.docs_dir / "02_Tasks" / "Bugs"
        self.specs_dir.mkdir(parents=True, exist_ok=True)
        self.bugs_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def _write_task(self, filename: str, task_id: str, status: str = "planned", phase: int = 1, depends_on: list = None):
        deps_yaml = ""
        if depends_on is not None:
            deps_yaml = "depends_on: [" + ", ".join(depends_on) + "]\n"
        content = f"---\nid: {task_id}\ntitle: \"Title of {task_id}\"\nstatus: {status}\ntype: task\nphase: {phase}\n{deps_yaml}---\n# {task_id}\n"
        (self.specs_dir / filename).write_text(content, encoding="utf-8")

    def _write_bug(self, filename: str, bug_id: str, status: str = "open", blocker: bool = False, phase: int = 1):
        content = f"---\nid: {bug_id}\ntitle: \"Title of {bug_id}\"\nstatus: {status}\ntype: bug\ntarget_phase: {phase}\nrelease_blocker: {'true' if blocker else 'false'}\n---\n# {bug_id}\n"
        (self.bugs_dir / filename).write_text(content, encoding="utf-8")

    def test_empty_vault_returns_no_tasks(self):
        # Empty specs and bugs
        res = kb_state.resolve_next_action(self.docs_dir)
        self.assertEqual(res["status"], "empty")
        self.assertEqual(res["action"], "no_tasks")
        self.assertIsNone(res["target"])

    def test_priority_1_in_progress_overrides_everything(self):
        # Write blocker bug, planned ready task, and in-progress task
        self._write_bug("BUG-001.md", "BUG-001", status="open", blocker=True, phase=1)
        self._write_task("TASK-001.md", "TASK-001", status="done", phase=1)
        self._write_task("TASK-002.md", "TASK-002", status="planned", phase=1, depends_on=["TASK-001"])
        self._write_task("TASK-003.md", "TASK-003", status="in-progress", phase=1)

        res = kb_state.resolve_next_action(self.docs_dir)
        self.assertEqual(res["status"], "in-progress")
        self.assertEqual(res["action"], "continue_task")
        self.assertEqual(res["target"]["id"], "TASK-003")
        self.assertEqual(res["target"]["command"], "/kb-implement TASK-003")

    def test_priority_2_release_blocker_bug_overrides_planned_tasks(self):
        # Write blocker bug and ready planned task
        self._write_bug("BUG-001.md", "BUG-001", status="open", blocker=True, phase=1)
        self._write_task("TASK-001.md", "TASK-001", status="planned", phase=1)

        res = kb_state.resolve_next_action(self.docs_dir)
        self.assertEqual(res["status"], "blocked_by_bug")
        self.assertEqual(res["action"], "fix_blocker_bug")
        self.assertEqual(res["target"]["id"], "BUG-001")
        self.assertEqual(res["target"]["command"], "/kb-implement BUG-001")

    def test_priority_2_non_blocker_bug_does_not_override_ready_task(self):
        # Write non-blocker open bug and ready planned task
        self._write_bug("BUG-002.md", "BUG-002", status="open", blocker=False, phase=1)
        self._write_task("TASK-001.md", "TASK-001", status="planned", phase=1)

        res = kb_state.resolve_next_action(self.docs_dir)
        self.assertEqual(res["status"], "ready")
        self.assertEqual(res["action"], "start_task")
        self.assertEqual(res["target"]["id"], "TASK-001")

    def test_priority_3_ready_task_selected_when_dependencies_satisfied(self):
        self._write_task("TASK-001.md", "TASK-001", status="done", phase=1)
        self._write_task("TASK-002.md", "TASK-002", status="planned", phase=1, depends_on=["TASK-001"])
        self._write_task("TASK-003.md", "TASK-003", status="planned", phase=1, depends_on=["TASK-002"])

        res = kb_state.resolve_next_action(self.docs_dir)
        self.assertEqual(res["status"], "ready")
        self.assertEqual(res["action"], "start_task")
        self.assertEqual(res["target"]["id"], "TASK-002")

    def test_priority_3_dependency_on_fixed_bug_is_satisfied(self):
        self._write_bug("BUG-001.md", "BUG-001", status="fixed", blocker=False, phase=1)
        self._write_task("TASK-001.md", "TASK-001", status="planned", phase=1, depends_on=["BUG-001"])

        res = kb_state.resolve_next_action(self.docs_dir)
        self.assertEqual(res["status"], "ready")
        self.assertEqual(res["target"]["id"], "TASK-001")

    def test_priority_4_all_done_triggers_release(self):
        self._write_task("TASK-001.md", "TASK-001", status="done", phase=1)
        self._write_task("TASK-002.md", "TASK-002", status="done", phase=1)

        res = kb_state.resolve_next_action(self.docs_dir)
        self.assertEqual(res["status"], "all_done")
        self.assertEqual(res["action"], "release")
        self.assertIn("/kb-release", res["message"])

    def test_priority_5_deadlock_detected_when_all_planned_blocked(self):
        # TASK-001 depends on TASK-002, TASK-002 depends on TASK-001 (circular or both planned)
        self._write_task("TASK-001.md", "TASK-001", status="planned", phase=1, depends_on=["TASK-002"])
        self._write_task("TASK-002.md", "TASK-002", status="planned", phase=1, depends_on=["TASK-001"])

        res = kb_state.resolve_next_action(self.docs_dir)
        self.assertEqual(res["status"], "deadlock")
        self.assertEqual(res["action"], "deadlock_blocked")
        self.assertGreaterEqual(len(res["blocked_by"]), 2)


class TestKbStateSummary(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())
        self.docs_dir = self.tmp_dir / "docs"
        self.specs_dir = self.docs_dir / "02_Tasks" / "Specs" / "01_Phase"
        self.bugs_dir = self.docs_dir / "02_Tasks" / "Bugs"
        self.specs_dir.mkdir(parents=True, exist_ok=True)
        self.bugs_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_summary_aggregation(self):
        # 1 done, 1 ready, 1 blocked
        (self.specs_dir / "TASK-001.md").write_text("---\nid: TASK-001\ntitle: Done task\nstatus: done\nphase: 1\n---\n", encoding="utf-8")
        (self.specs_dir / "TASK-002.md").write_text("---\nid: TASK-002\ntitle: Ready task\nstatus: planned\nphase: 1\ndepends_on: [TASK-001]\n---\n", encoding="utf-8")
        (self.specs_dir / "TASK-003.md").write_text("---\nid: TASK-003\ntitle: Blocked task\nstatus: planned\nphase: 1\ndepends_on: [TASK-002]\n---\n", encoding="utf-8")

        # 1 fixed bug, 1 open blocker bug
        (self.bugs_dir / "BUG-001.md").write_text("---\nid: BUG-001\ntitle: Fixed\nstatus: fixed\nrelease_blocker: false\n---\n", encoding="utf-8")
        (self.bugs_dir / "BUG-002.md").write_text("---\nid: BUG-002\ntitle: Blocker\nstatus: open\nrelease_blocker: true\n---\n", encoding="utf-8")

        summary = kb_state.compute_status_summary(self.docs_dir)
        self.assertEqual(summary["total_tasks"], 3)
        self.assertEqual(summary["tasks_by_status"]["done"], 1)
        self.assertEqual(summary["tasks_by_status"]["planned"], 2)
        self.assertEqual(summary["total_bugs"], 2)
        self.assertEqual(summary["open_blocker_bugs"], 1)
        self.assertEqual(len(summary["ready_tasks"]), 1)
        self.assertEqual(summary["ready_tasks"][0]["id"], "TASK-002")
        self.assertEqual(len(summary["blocked_tasks"]), 1)
        self.assertEqual(summary["blocked_tasks"][0]["id"], "TASK-003")


class TestKbStateCLI(unittest.TestCase):
    def test_cli_next_json_and_text(self):
        captured_text = io.StringIO()
        with patch("sys.stdout", captured_text):
            code_text = kb_state.main(["next", "--path", "docs"])
        self.assertEqual(code_text, 0)
        out_text = captured_text.getvalue()
        self.assertIn("TASK-111", out_text)

        captured_json = io.StringIO()
        with patch("sys.stdout", captured_json):
            code_json = kb_state.main(["next", "--path", "docs", "--json"])
        self.assertEqual(code_json, 0)
        data = json.loads(captured_json.getvalue())
        self.assertEqual(data["status"], "ready")
        self.assertEqual(data["target"]["id"], "TASK-111")

    def test_cli_status_json_and_text(self):
        captured_text = io.StringIO()
        with patch("sys.stdout", captured_text):
            code_text = kb_state.main(["status", "--path", "docs"])
        self.assertEqual(code_text, 0)
        out_text = captured_text.getvalue()
        self.assertIn("СТАТУС ПРОЕКТА", out_text)
        self.assertIn("TASK-111", out_text)

        captured_json = io.StringIO()
        with patch("sys.stdout", captured_json):
            code_json = kb_state.main(["status", "--path", "docs", "--format", "json"])
        self.assertEqual(code_json, 0)
        data = json.loads(captured_json.getvalue())
        self.assertGreaterEqual(data["total_tasks"], 110)
        self.assertEqual(data["current_phase"], 30)

    def test_cli_invalid_path_returns_exit_1(self):
        captured_err = io.StringIO()
        with patch("sys.stderr", captured_err):
            code = kb_state.main(["next", "--path", "non_existent_directory_xyz"])
        self.assertEqual(code, 1)
        self.assertIn("ERROR:", captured_err.getvalue())


class TestKbStatePerformance(unittest.TestCase):
    def test_benchmark_under_100ms(self):
        """Measures execution speed over >= 3 runs (discarding cold start)."""
        docs_path = Path("docs")
        if not docs_path.is_dir():
            self.skipTest("Real docs directory not available for benchmark")

        # Cold run
        kb_state.resolve_next_action(docs_path)

        runs = []
        for _ in range(5):
            t0 = time.perf_counter()
            kb_state.resolve_next_action(docs_path)
            t1 = time.perf_counter()
            runs.append((t1 - t0) * 1000.0)

        avg_ms = sum(runs) / len(runs)
        # Average run must be well under 100 ms threshold
        self.assertLess(avg_ms, 100.0, f"Average scan latency ({avg_ms:.2f} ms) exceeded 100 ms")


if __name__ == "__main__":
    unittest.main()
