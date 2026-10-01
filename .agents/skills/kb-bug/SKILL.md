---
name: kb-bug
description: "Record defect BUG-XXX with Root Cause Analysis (RCA) and Regression-First TDD test."
---

# /kb-bug — Defect Logging & Bug Tracking

Use when the user runs `/kb-bug <name>` or reports a software defect.

## 🚨 Constraints
* **Regression-First Principle:** Every defect MUST be reproduced with an automated test that FAILS before the fix and PASSES after the fix. Closing a bug without a regression test is strictly prohibited.
* **Permalinks Invariant:** Defect reports are never moved or deleted upon resolution.

## Procedure: Logging a Bug
1. **Calculate Bug ID:** Scan `docs/02_Tasks/Bugs/` to determine next `BUG-XXX` ID.
2. **Draft Report:** Create `docs/02_Tasks/Bugs/BUG-XXX-<slug>.md` using `docs/00_Templates/TEMPLATE_BUG.md`. Include STR, expected vs actual behavior, stack trace, and Root Cause Analysis (RCA).
3. **Update Kanban:** Add card to `## 📥 Бэклог (Backlog)` or `## ⏳ В работе (In Progress)` in `docs/02_Tasks/Kanban.md`.
4. **Git Sync (Conditional):** Stage report and Kanban, commit `docs(bug): log BUG-XXX <slug>`, push if remote exists.

## Procedure: Resolving a Bug
1. **Write Regression Test:** Create automated test reproducing defect (must fail).
2. **Apply Fix:** Implement fix in source code until the regression test passes.
3. **Update Report:** Set frontmatter `status: fixed`, `resolved: <YYYY-MM-DD>`.
4. **Update Kanban & Devlog:** Move card to `## ✅ Готово (Done)` in `docs/02_Tasks/Kanban.md`. Add entry to `docs/Devlog.md` with link to regression test.
5. **Git Sync (Conditional):** Commit `fix(<scope>): resolve BUG-XXX <title> with regression test`, push if remote exists.
