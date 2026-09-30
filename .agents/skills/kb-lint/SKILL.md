---
name: kb-lint
description: >-
  Validate the integrity of the Docs-as-Code knowledge base, scanning all wikilinks, detecting broken links,
  and checking YAML frontmatter validity using kb_lint.py.
---

# /kb-lint — Knowledge Base Linter

Use this skill when the user runs `/kb-lint` or wants to check the consistency of the documentation vault.

## Procedure

1. **Run Linter Script:**
   - Execute:
     ```powershell
     python ~/.gemini/config/skills/docs-as-code/scripts/kb_lint.py --path docs
     ```
2. **Interpret Results:**
   - **Broken Wikilinks:** If any target file does not exist, pinpoint the exact source file and link.
   - **Frontmatter Warnings:** If any task, plan, bug, or ADR is missing standard YAML frontmatter (`---`).
3. **Resolve or Advise:**
   - If broken links exist, propose fixes or create missing placeholder specs.
   - If 0 errors, confirm healthy state.
