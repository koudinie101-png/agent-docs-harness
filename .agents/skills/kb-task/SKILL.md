---
name: kb-task
description: "Mode 2: Engineering specification TASK-XXX with file contracts and DoD. Prohibits code changes."
---

# /kb-task — Mode 2: Task Specification

Use when the user runs `/kb-task <name>`, asks to create a specification/ТЗ, or starts Mode 2.

## 🚨 Constraints
* **READ-ONLY:** Modifying or creating project code files is STRICTLY PROHIBITED.
* **Exact Contracts:** All file changes must be explicitly marked as `[NEW]`, `[MODIFY]`, or `[DELETE]`.

## Procedure
1. **Calculate Task ID:**
   - Scan `docs/02_Tasks/Specs/` to determine the next available `TASK-XXX` ID.
2. **Identify Target Phase:**
   - Locate or create the target phase directory `docs/02_Tasks/Specs/<Phase_Folder>/`.
3. **Draft Specification:**
   - Create `docs/02_Tasks/Specs/<Phase_Folder>/TASK-XXX-<slug>.md` using `docs/00_Templates/TEMPLATE_TASK.md`.
   - Specify file contracts (`[NEW]`, `[MODIFY]`, `[DELETE]`), data structures, API signatures, and exception handling.
   - Define explicit **Verification Plan** (compilation commands, automated test suites, manual verification).
   - Define **Definition of Done (DoD)**.
4. **Update Kanban:**
   - Move or add task card in `docs/02_Tasks/Kanban.md` to `## ⏳ В работе (In Progress)`.
5. **Git Sync (Conditional):**
   - Stage: `git add docs/02_Tasks/Specs/ docs/02_Tasks/Kanban.md`
   - Commit: `git commit -m "docs(spec): add TASK-XXX <slug> and set in-progress"`
   - Push if remote origin exists.
