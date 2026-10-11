---
name: kb-bug
description: "Mode 2B: Defect logging, RCA analysis, and interactive triage. Prohibits code modifications."
---

# /kb-bug — Mode 2B: Defect Logging & Interactive Triage

Use when the user runs `/kb-bug <name>`, reports a software defect, or logs a bug.

## 🚨 Constraints
* **READ-ONLY FOR CODE:** Modifying or creating project code files is STRICTLY PROHIBITED.
* **Triage Isolation:** Focus strictly on defect recording, RCA analysis, regression test specification, and interactive triage. Implementation is performed separately via `/kb-implement BUG-XXX`.
* **Permalinks Invariant:** Defect reports are never moved or deleted upon resolution.
* **Terminal Stop:** Once the bug report is committed, immediately STOP tool calls and yield control.

## Procedure
1. **Calculate Bug ID:**
   - Scan `docs/02_Tasks/Bugs/` to determine the next available `BUG-XXX` ID.
2. **Analyze Defect:**
   - Collect steps to reproduce (STR), environment, expected vs actual behavior, stack trace/logs.
   - Perform Root Cause Analysis (RCA) to document architectural or logical defect cause.
3. **Interactive Triage:**
   - Solicit or clarify `severity` (`low | medium | high | critical`), `target_release` (`vX.Y.Z | hotfix | backlog`), `target_phase` (phase number or `null`), and `release_blocker` (`true | false`).
   - If release context is unspecified by the user, set safe default `target_release: "backlog"` and `release_blocker: false`.
4. **Draft Defect Report:**
   - Create `docs/02_Tasks/Bugs/BUG-XXX-<slug>.md` using `docs/00_Templates/TEMPLATE_BUG.md`.
5. **Update Kanban:**
   - Add card to `## 📥 Бэклог (Backlog)` (or `## ⏳ В работе (In Progress)` if triaged for immediate fix) in `docs/02_Tasks/Kanban.md`.
6. **Git Sync (Conditional):**
   - Stage: `git add docs/02_Tasks/Bugs/ docs/02_Tasks/Kanban.md`
   - Commit: `git commit -m "docs(bug): record BUG-XXX <slug>"`
   - Push if remote origin exists.
7. **Stop & Yield Control (Terminal Step):**
   - Output concise Anti-Echo summary with actionable triage menu:
     * Hotfix immediately via TDD: `/kb-implement BUG-XXX`
     * Schedule into active roadmap phase
     * Retain in backlog
   - **STRICTLY STOP ALL TOOL CALLS.** Yield control to user and wait for explicit command.
