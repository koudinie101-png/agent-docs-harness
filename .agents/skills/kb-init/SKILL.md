---
name: kb-init
description: >-
  Initialize the standard Docs-as-Code knowledge base in a new project (docs/ directory,
  full template suite, colored Obsidian graph, Onboarding.md, 00_Index.md, Kanban.md, Roadmap.md, Devlog.md).
---

# /kb-init — Initialize Knowledge Base (Docs-as-Code)

Use this skill when the user runs `/kb-init` or asks to set up the knowledge base in a new repository.

## Procedure

1. **Verify Target Directory:**
   - Check if `docs/` already exists in the project root. If it does, inform the user to prevent accidental overwrite.
2. **Scaffold Directory Layout:**
   - Create directories:
     - `docs/.obsidian/`
     - `docs/00_Templates/`
     - `docs/01_Architecture/`
     - `docs/02_Tasks/Plans/`
     - `docs/02_Tasks/Specs/01_MVP/`
     - `docs/02_Tasks/Bugs/`
     - `docs/03_Decisions_ADR/`
     - `docs/04_Research/`
     - `docs/05_Testing/`
3. **Deploy Resources & Templates:**
   - Copy or generate from `~/.gemini/config/skills/docs-as-code/resources/`:
     - `docs/.obsidian/graph.json`
     - `docs/00_Templates/` (all 12 templates with YAML frontmatter)
4. **Deploy Starter Artifacts:**
   - `docs/Onboarding.md` (project onboarding and workflow guide)
   - `docs/00_Index.md` (Map of Content)
   - `docs/02_Tasks/Kanban.md` (starter board)
   - `docs/02_Tasks/Roadmap.md` (starter milestones)
   - `docs/Devlog.md` (initial entry)
5. **Verify:**
   - Run `python ~/.gemini/config/skills/docs-as-code/scripts/kb_lint.py --path docs`.
   - Confirm 0 errors and report readiness.
6. **Git & Remote Onboarding (Интерактивная настройка контроля версий):**
   - Check if Git is initialized in the workspace (`Test-Path .git`).
   - If Git is not yet set up or remote origin is not connected, provide the user with clear options:
     - **Option 1: Connect to GitHub (Рекомендуется):**
       - Explain the exact steps:
         1. Open [github.com/new](https://github.com/new) and choose repository name and visibility (Private/Public).
         2. **Important:** Do NOT check "Add a README", "Add .gitignore", or "Choose a license" (files already exist locally).
         3. Copy the repository URL (`https://github.com/<user>/<repo>.git`).
       - Run or provide commands:
         ```bash
         git init
         git add .
         git commit -m "feat: initial project scaffolding with docs-as-code"
         git branch -M main
         git remote add origin <REPO_URL>
         git push -u origin main
         ```
       - Confirm `git config --global user.name` and `user.email` are configured if Git was installed freshly.
     - **Option 2: Local-Only (Только локальный Git):**
       - Initialize local repository for version history without a remote:
         ```bash
         git init
         git add .
         git commit -m "feat: initial project scaffolding (local-only)"
         git branch -M main
         ```
       - Explain: all Docs-as-Code workflows (`/kb-plan`, `/kb-task`, `/kb-complete`, etc.) will record local commits, but will automatically skip `git push`. Remote can be connected anytime via `git remote add origin <URL>`.
     - **Option 3: No Git (Без контроля версий):**
       - Skip all Git operations entirely. Knowledge base files will be maintained as plain local files.
