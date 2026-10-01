---
name: kb-plan
description: "Mode 1: Conceptual analysis, RFC, and PLAN-XXX creation. Prohibits code changes."
---

# /kb-plan — Mode 1: Planning / RFC

Use when the user runs `/kb-plan <name>`, plans a feature, or discusses architecture.

## 🚨 Constraints
* **READ-ONLY:** Modifying or creating project code files is STRICTLY PROHIBITED.
* **Constructive Partner:** Challenge suboptimal ideas, highlight platform flaws, and offer 1–2 idiomatic alternatives.

## Procedure
1. **Clarify & Challenge:** Identify requirements, edge cases, and trade-offs. Constructively critique flawed approaches.
2. **Draft Plan:** Break down into potential tasks, affected modules, and risks.
3. **User Approval (Mandatory):** Present an executive summary in chat. Obtain explicit confirmation before writing files.
4. **Record Plan:**
   - Scan `docs/02_Tasks/Plans/` for the next available `PLAN-XXX` ID.
   - Create `docs/02_Tasks/Plans/PLAN-XXX-<slug>.md` using `docs/00_Templates/TEMPLATE_PLAN.md`.
   - Add task card to `## 📥 Бэклог (Backlog)` in `docs/02_Tasks/Kanban.md`.
   - If promoted from Icebox: assign sequential Phase number in `docs/02_Tasks/Roadmap.md`.
5. **Git Sync (Conditional):**
   - Stage: `git add docs/02_Tasks/Plans/ docs/02_Tasks/Kanban.md docs/02_Tasks/Roadmap.md`
   - Commit: `git commit -m "docs(plan): record PLAN-XXX <slug> and update backlog"`
   - Push if remote origin exists.
