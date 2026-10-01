---
name: kb-init
description: "Initialize Docs-as-Code structure, 13 templates, Obsidian graph, and core tracking files."
---

# /kb-init — Initialize Knowledge Base (Docs-as-Code)

Use when the user runs `/kb-init` or requests setting up the knowledge base in a project.

## 🚨 Constraints
* **Safety First:** If `docs/` already exists, prompt the user before modifying to prevent accidental overwrite.
* **Zero Dependencies:** Relies strictly on standard library Python and native Git.

## Procedure
1. **Verify Target:** Check if `docs/` exists in project root.
2. **Scaffold Directory Layout:**
   - Create directories: `docs/.obsidian/`, `docs/00_Templates/`, `docs/01_Architecture/`, `docs/02_Tasks/Plans/`, `docs/02_Tasks/Specs/01_MVP/`, `docs/02_Tasks/Bugs/`, `docs/02_Tasks/Releases/`, `docs/03_Decisions_ADR/`, `docs/04_Research/`, `docs/05_Testing/`.
3. **Deploy Templates & Configs:**
   - Deploy `docs/.obsidian/graph.json` (Obsidian color-coded palette).
   - Deploy all 13 canonical templates to `docs/00_Templates/`.
4. **Deploy Core Tracking Files:**
   - Deploy `docs/Onboarding.md`, `docs/00_Index.md`, `docs/02_Tasks/Kanban.md`, `docs/02_Tasks/Roadmap.md`, and `docs/Devlog.md`.
5. **Verify & Onboard Git:**
   - Run `python scripts/kb_lint.py --path docs` to confirm 0 errors.
   - If Git is not initialized, assist user: `git init`, `git add .`, `git commit -m "feat: initial docs-as-code scaffolding"`.
