"""TASK-087: Tier 1 structural guards for the single-source rules corpus.

These tests do not pin rule *text* (that is tests/test_rules_golden.py); they pin
the shape of the corpus: document inventory, unique semantic IDs, adapter
derivability, clean rendering, determinism and honest failure without a corpus.
"""

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]
for path in (REPO_ROOT, REPO_ROOT / "scripts"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import install  # noqa: E402
import gen_rules  # noqa: E402

OPEN_MARKER = re.compile(r"<!-- RULE: ([A-Z0-9-]+) -->")
CLOSE_MARKER = "<!-- /RULE:"
DOCUMENTS = {"client-agents", "adapters", "harness-agents"}

CLIENT_RULES = [
    # 20 disciplines
    "SESSION-READ", "KANBAN", "ROADMAP", "ADR", "RESEARCH", "DEVLOG", "OBSIDIAN",
    "PERMALINKS", "REGRESSION-FIRST", "QA-CHECKLISTS", "GRAPH-COLORS", "GIT-FLOW",
    "SINGLE-TASK", "ZERO-STATE", "FEEDBACK-TRIAGE", "HUMAN-GUARDRAILS", "FAST-TRACK",
    "ZERO-ROUNDTRIP", "QUALITY-GATES", "FOUR-STATE-UI",
    # governance
    "TECH-DEBT", "PRIOR-ART", "TRACEABLE-TAGS", "BENCHMARKS",
    # document blocks
    "ANTI-ECHO", "SENIOR-PARTNER", "LIFECYCLE",
]

ADAPTER_RULES = [
    "ZERO-ROUNDTRIP", "HUMAN-GUARDRAILS", "FAST-TRACK", "SINGLE-TASK", "ANTI-ECHO",
    "QUALITY-GATES", "FOUR-STATE-UI", "TECH-DEBT", "PRIOR-ART", "TRACEABLE-TAGS",
]

HARNESS_RULES = [
    "PERMALINKS", "REGRESSION-FIRST", "LIVING-SPEC", "OBSIDIAN", "SINGLE-TASK",
    "ZERO-STATE", "FEEDBACK-TRIAGE", "HUMAN-GUARDRAILS", "FAST-TRACK",
    "ZERO-ROUNDTRIP", "QUALITY-GATES", "FOUR-STATE-UI", "TECH-DEBT", "PRIOR-ART",
    "TRACEABLE-TAGS", "BENCHMARKS", "KB-STANDARD", "ANTI-ECHO", "SENIOR-PARTNER",
    "LIFECYCLE",
]


class RulesConsistencyTest(unittest.TestCase):
    def setUp(self):
        install._RULES_CORPUS_CACHE = None
        self.addCleanup(setattr, install, "_RULES_CORPUS_CACHE", None)
        self.corpus = install._load_rules_corpus()

    def ids(self, document):
        return OPEN_MARKER.findall(self.corpus[document])

    def render(self, document):
        values = install._rules_values("Demo", "python", "ru") if document == "client-agents" else {}
        return install._render_rules_document(document, values)

    # --- inventory ---------------------------------------------------------

    def test_corpus_documents_present(self):
        self.assertEqual(set(self.corpus), DOCUMENTS, "unexpected rules documents")

    def test_rule_ids_unique_within_documents(self):
        for document in sorted(DOCUMENTS):
            body = self.corpus[document]
            found = self.ids(document)
            duplicates = sorted({rid for rid in found if found.count(rid) > 1})
            self.assertEqual(duplicates, [], "duplicate RULE ids in %s" % document)
            self.assertEqual(
                body.count(CLOSE_MARKER), len(found),
                "unbalanced RULE markers in %s" % document,
            )

    def test_client_inventory_matches_pin(self):
        self.assertEqual(set(self.ids("client-agents")), set(CLIENT_RULES))

    def test_adapters_are_derived_subset(self):
        adapters = set(self.ids("adapters"))
        self.assertEqual(adapters, set(ADAPTER_RULES), "adapter inventory drifted")
        self.assertEqual(len(self.ids("adapters")), 10, "adapters must stay at 10 rules")
        self.assertTrue(adapters.issubset(set(CLIENT_RULES)), "adapter rule missing in client document")

    def test_harness_inventory_matches_pin(self):
        harness = set(self.ids("harness-agents"))
        self.assertEqual(harness, set(HARNESS_RULES), "harness inventory drifted")
        self.assertIn("LIVING-SPEC", harness)
        self.assertNotIn("LIVING-SPEC", set(CLIENT_RULES))

    # --- rendering ---------------------------------------------------------

    def test_rendered_outputs_have_no_markers(self):
        for document in sorted(DOCUMENTS):
            rendered = self.render(document)
            for marker in ("<!-- RULE", "<!-- /RULE", "<!-- DOCUMENT"):
                self.assertNotIn(marker, rendered, "marker leaked from %s" % document)

    def test_rendered_outputs_have_no_placeholders(self):
        for document in sorted(DOCUMENTS):
            rendered = self.render(document)
            self.assertNotIn("{{", rendered, "unresolved placeholder in %s" % document)
            self.assertNotIn("}}", rendered, "unresolved placeholder in %s" % document)

    def test_render_is_deterministic(self):
        for document in sorted(DOCUMENTS):
            self.assertEqual(self.render(document), self.render(document), document)

    # --- failure modes -----------------------------------------------------

    def test_missing_corpus_raises_actionable_error(self):
        with mock.patch.object(install, "_rules_corpus_path", return_value=Path("missing/AGENTS_CORE.md")), \
                mock.patch.object(install, "unpack_assets", return_value={}):
            install._RULES_CORPUS_CACHE = None
            with self.assertRaises(RuntimeError) as ctx:
                install.generate_agents_md("Demo", "python", "ru")
        self.assertIn("rules/AGENTS_CORE.md", str(ctx.exception))

    def test_corpus_not_deployed_to_client_docs(self):
        assets = install.unpack_assets()
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Target"
            target.mkdir()
            templates, _skills = install.deploy_infrastructure(
                target, assets, "python", "2026-10-18", project_name="Demo")
            self.assertEqual(templates, 16, "template count changed")
            self.assertFalse((target / "rules").exists(), "corpus directory leaked into client project")
            leaked = [p for p in target.rglob("AGENTS_CORE.md")]
            self.assertEqual(leaked, [], "corpus file leaked into client project")

    # --- gate --------------------------------------------------------------

    def test_check_current_detects_drift(self):
        rendered = gen_rules.render_harness_agents()
        ok, diff = gen_rules.check_current(REPO_ROOT / "AGENTS.md", rendered)
        self.assertTrue(ok, diff)
        ok, diff = gen_rules.check_current(
            REPO_ROOT / "AGENTS.md", rendered + "\n<!-- tampered -->\n")
        self.assertFalse(ok)
        self.assertIn("tampered", diff)

    def test_gate_cli_exits_zero_on_clean_tree(self):
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "gen_rules.py"), "--check"],
            cwd=str(REPO_ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_gate_cli_fails_on_missing_corpus(self):
        with mock.patch.object(install, "_rules_corpus_path", return_value=Path("missing/AGENTS_CORE.md")), \
                mock.patch.object(install, "unpack_assets", return_value={}):
            install._RULES_CORPUS_CACHE = None
            code = gen_rules.main(["--check"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
