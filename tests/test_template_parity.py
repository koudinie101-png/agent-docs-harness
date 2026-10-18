"""TASK-092: Tier 1 parity guard for the two template stores.

`templates/` feeds the installer bundle; `docs/00_Templates/` is the knowledge
base copy. They must stay byte-identical (after CRLF normalisation) so clients
never receive a degraded template.
"""

import difflib
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_DIR = REPO_ROOT / "templates"
DOCS_DIR = REPO_ROOT / "docs" / "00_Templates"


def normalize(text):
    return text.replace("\r\n", "\n")


class TemplateParityTest(unittest.TestCase):
    def test_markdown_file_sets_match(self):
        bundle = {p.name for p in BUNDLE_DIR.glob("*.md")}
        docs = {p.name for p in DOCS_DIR.glob("*.md")}
        self.assertEqual(bundle - docs, set(), "templates missing from docs/00_Templates")
        self.assertEqual(docs - bundle, set(), "docs/00_Templates missing from templates")
        self.assertEqual(len(bundle), 16, "expected exactly 16 canonical templates")

    def test_markdown_contents_match(self):
        for name in sorted(p.name for p in BUNDLE_DIR.glob("*.md")):
            with self.subTest(template=name):
                expected = normalize((BUNDLE_DIR / name).read_text(encoding="utf-8"))
                actual = normalize((DOCS_DIR / name).read_text(encoding="utf-8"))
                if actual != expected:
                    diff = "\n".join(list(difflib.unified_diff(
                        expected.splitlines(), actual.splitlines(),
                        fromfile="templates/" + name,
                        tofile="docs/00_Templates/" + name,
                        lineterm="",
                    ))[:25])
                    self.fail("template copies drifted: %s\n%s" % (name, diff))


if __name__ == "__main__":
    unittest.main()
