---
name: kb-lint
description: "Audit knowledge base integrity: scan wikilinks, broken targets, and YAML frontmatter."
---

# /kb-lint — Knowledge Base Linter

Use when the user runs `/kb-lint` or asks to check the integrity of the documentation vault.

## 🚨 Constraints
* **Zero Dependencies:** Runs on standard library Python 3 via `scripts/kb_lint.py`.
* **Zero Broken Links:** All `[[wikilinks]]` in active files must resolve to existing markdown files or anchors.

## Procedure
1. **Run Linter Script:**
   - Execute:
     ```powershell
     python scripts/kb_lint.py --path docs
     ```
2. **Interpret Output:**
   - **Broken Wikilinks:** Identifies exact source file and missing target file.
   - **Frontmatter Errors:** Validates mandatory YAML properties (`id`, `title`, `status`, `type`, `tags`).
3. **Resolve Findings:**
   - If broken links are detected, fix typos, create missing placeholder specs, or adjust relative paths.
   - Exit code 0 confirms a healthy and consistent knowledge base.
