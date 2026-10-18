---
name: kb-task
description: "Mode 2: Engineering specification TASK-XXX with file contracts and DoD. Prohibits code changes."
---

# /kb-task — Mode 2: Task Specification

Use when the user runs `/kb-task <name>`, asks to create a specification/ТЗ, or starts Mode 2.

## 🚨 Constraints
* **READ-ONLY:** Modifying or creating project code files is STRICTLY PROHIBITED.
* **Exact Contracts:** Mark changes as `[NEW]`, `[MODIFY]`, or `[DELETE]`; for code, name nested symbols (`Class.method()`), never line numbers (ADR-0029).

## Procedure
1. **Spec Status Check (Zero-State Guard):**
   - Verify `SPEC.md` is present and not in `status: discovery`. If it is in discovery, issue a Soft Nudge warning that engineering task specs should align with an active Master Spec, or confirm user intent before proceeding.
2. **Calculate Task ID:**
   - Scan `docs/02_Tasks/Specs/` to determine the next available `TASK-XXX` ID.
3. **Identify Target Phase:**
   - Locate or create the target phase directory `docs/02_Tasks/Specs/<Phase_Folder>/`.
4. **Draft Specification:**
   - **Fast-Track Mode (`--fast` / micro-scope ≤ 30 LOC):** If called with `--fast` or targeting a trivial micro-task, use `docs/00_Templates/TEMPLATE_TASK_MICRO.md`. Guardrails: if scope exceeds 30 LOC or 2 files, warn user and fallback to standard spec.
   - **Standard Mode:** Create `docs/02_Tasks/Specs/<Phase_Folder>/TASK-XXX-<slug>.md` using `docs/00_Templates/TEMPLATE_TASK.md`.
   - Specify file contracts (`[NEW]`, `[MODIFY]`, `[DELETE]`), data structures, API signatures, and exception handling.
   - Define explicit **Verification Plan** (compilation commands, automated test suites, manual verification).
   - Define **Definition of Done (DoD)**.
   - If the spec carries the `#techdebt` tag: link its `DEBT-XXX` from `docs/02_Tasks/TechDebt.md` (register the row first if missing).
5. **Update Kanban:**
   - Move or add task card in `docs/02_Tasks/Kanban.md` to `## ⏳ В работе (In Progress)`.
6. **Git Sync (Conditional):**
   - Stage: `git add docs/02_Tasks/Specs/ docs/02_Tasks/Kanban.md`
   - Commit: `git commit -m "docs(spec): add TASK-XXX <slug> and set in-progress"`
   - Push if remote origin exists.
7. **Terminal Step (Stop & Yield Control):** Output Anti-Echo response, suggest next command (`/kb-implement TASK-XXX`), and strictly STOP all tool calls. Wait for user command.
