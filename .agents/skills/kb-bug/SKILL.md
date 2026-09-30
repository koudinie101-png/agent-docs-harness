---
name: kb-bug
description: >-
  Record a defect or bug report BUG-XXX using TEMPLATE_BUG.md with RCA (Root Cause Analysis)
  and enforce the Regression-First test principle.
---

# /kb-bug — Defect Logging & Bug Tracking

Use this skill when the user runs `/kb-bug <name>` or reports a bug/defect.

## 🚨 Principle: Regression-First
Every bug must be reproduced with an automated test (unit or integration) that FAILS before the fix and PASSES after the fix. A bug cannot be marked as fixed without a regression test.

## Procedure

1. **Calculate ID:**
   - Scan `docs/02_Tasks/Bugs/` to find the next available `BUG-XXX` ID (e.g. `BUG-006`).
2. **Draft the Bug Report:**
   - Create `docs/02_Tasks/Bugs/BUG-XXX-<slug>.md` using `docs/00_Templates/TEMPLATE_BUG.md` with standard YAML frontmatter.
   - Fill in:
     - Symptoms & environment.
     - Steps to Reproduce (STR).
     - Expected vs Actual behavior.
     - Logs / stack trace.
     - Root Cause Analysis (RCA).
     - Fix plan and path to regression test file.
3. **Update Kanban:**
   - Add card `🐞 [[Bugs/BUG-XXX-<slug>|BUG-XXX: <title>]] #bug` to `## 📥 Бэклог (Backlog)` or `## ⏳ В работе (In Progress)` in `docs/02_Tasks/Kanban.md`.
4. **Git Commit & Push (Logging, Conditional):**
   - If Git is enabled:
     - Stage the new defect report and updated Kanban: `git add docs/02_Tasks/Bugs/ docs/02_Tasks/Kanban.md`
     - Commit: `git commit -m "docs(bug): log BUG-XXX <slug>"`
     - If remote `origin` is configured, push: `git push`. If in Local-Only mode (no remote), skip push.

## Resolution & Closing a Defect

When a bug is fixed and verified with a regression test:
1. Update `BUG-XXX` frontmatter to `status: fixed` and set `resolved: <YYYY-MM-DD>`.
2. Move card in `docs/02_Tasks/Kanban.md` to `## ✅ Готово (Done)` with date.
3. Add entry to `docs/Devlog.md` referencing `BUG-XXX` and the regression test path.
4. **Git Commit & Push (Resolution, Conditional):**
   - If Git is enabled:
     - Stage all changes: `git add .`
     - Commit: `git commit -m "fix(<component>): resolve BUG-XXX <title> and add regression test"`
     - If remote `origin` is configured, push: `git push`. If in Local-Only mode (no remote), skip push.
