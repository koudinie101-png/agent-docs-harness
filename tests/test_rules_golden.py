"""TASK-085: golden tests pinning generated rule artifacts to pre-refactor output."""

import difflib
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import install  # noqa: E402

FIXTURES = REPO_ROOT / "tests" / "fixtures" / "rules"

STACKS = ["swift", "ts", "python", "dotnet", "generic", "undecided"]
ADAPTERS = {
    "gemini": install.generate_gemini_md,
    "windsurf": install.generate_windsurfrules,
    "cline": install.generate_clinerules,
    "claude": install.generate_claude_md,
    "cursor": install.generate_cursorrules,
    "copilot": install.generate_copilot_instructions,
}


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n")


class RulesGoldenTest(unittest.TestCase):
    """Byte-level pin: the corpus renderer must reproduce the old generators."""

    def assert_fixture(self, name: str, actual: str) -> None:
        path = FIXTURES / (name + ".txt")
        self.assertTrue(path.is_file(), "missing golden fixture: %s" % path)
        expected = normalize(path.read_text(encoding="utf-8"))
        actual = normalize(actual)
        if actual != expected:
            diff = list(difflib.unified_diff(
                expected.splitlines(), actual.splitlines(),
                fromfile="fixture:" + name, tofile="rendered:" + name, lineterm="",
            ))
            self.fail("golden mismatch for %s:\n%s" % (name, "\n".join(diff[:40])))

    def test_client_agents_golden(self):
        for stack in STACKS:
            for lang in ("ru", "en"):
                with self.subTest(stack=stack, lang=lang):
                    self.assert_fixture(
                        "client_agents__%s__%s" % (stack, lang),
                        install.generate_agents_md("Demo", stack, lang),
                    )

    def test_adapters_golden(self):
        for name, generator in ADAPTERS.items():
            for lang in ("ru", "en"):
                with self.subTest(adapter=name, lang=lang):
                    self.assert_fixture(
                        "adapter__%s__%s" % (name, lang),
                        generator("Demo", "python", lang),
                    )

    def test_golden_fixtures_are_complete(self):
        expected = {"client_agents__%s__%s" % (s, l) for s in STACKS for l in ("ru", "en")}
        expected |= {"adapter__%s__%s" % (a, l) for a in ADAPTERS for l in ("ru", "en")}
        present = {p.stem for p in FIXTURES.glob("*.txt")}
        self.assertEqual(expected - present, set(), "fixtures missing")
        self.assertEqual(present - expected, set(), "unexpected fixtures")


if __name__ == "__main__":
    unittest.main()
