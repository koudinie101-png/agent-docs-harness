---
name: kb-complete
description: "Mode 3: Finalize TASK-XXX, update Kanban/Roadmap/Devlog, run kb_lint, and git commit."
---

# /kb-complete — Mode 3: Task Finalization & Knowledge Base Sync

Use when the user runs `/kb-complete <TASK-XXX>` after all verification steps have passed.

## 🚨 Constraints
* **Passing Tests Required:** Do not mark complete if any verification step failed.
* **Permalinks Invariant:** Never move or archive spec files. Update status in-place.

## Procedure
1. **Update Task Spec:**
   - In `docs/02_Tasks/Specs/<Phase>/TASK-XXX-<slug>.md`: set frontmatter `status: done`, `updated: <YYYY-MM-DD>`, and header `> **Статус:** Выполнено (Режим 3)`.
2. **Update Kanban:**
   - Move task card from `## ⏳ В работе (In Progress)` to `## ✅ Готово (Done)` in `docs/02_Tasks/Kanban.md` with completion date `(YYYY-MM-DD)`.
3. **Update Roadmap:**
   - In `docs/02_Tasks/Roadmap.md`: check milestone `[x]` with permanent link `[[Specs/<Phase>/TASK-XXX-<slug>|TASK-XXX]]`.
4. **Append Devlog:**
   - In `docs/Devlog.md`: record summary of changes, test verification results, and next step.
5. **Lint Verification:**
   - Run `python scripts/kb_lint.py --path docs` to confirm 0 broken links.
6. **Git Commit & Sync:**
   - **Feature Branch:** commit changes, checkout `main`, pull rebase, merge branch, push, delete local feature branch.
   - **Trunk-Based (`main`):** `git add .`, `git commit -m "feat(<scope>): complete TASK-XXX <summary> and sync docs"`, `git push` (if remote exists).
7. **Phase Completion Nudge:**
   - If all tasks in the current phase are now `[x]`, recommend running acceptance testing in `docs/05_Testing/` and executing `/kb-release <vX.Y.Z>`.
