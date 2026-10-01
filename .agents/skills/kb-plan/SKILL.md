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
1. **Source Discovery & Intent Routing:**
   - **Explicit Idea:** If user specified a topic (`/kb-plan <idea>`), proceed immediately with that topic.
   - **No Argument (`/kb-plan`):** Inspect `## 🔮 Перспективные направления (Future Horizons / Icebox)` in `docs/02_Tasks/Roadmap.md`.
     - *If ideas exist:* Analyze product value impact, rank candidates in prioritized order with a concise 1-line rationale for each, provide a top recommendation, and ask user to confirm, select an alternative, or propose a new idea.
     - *If empty:* Ask user what feature/architecture they plan to design.
2. **Clarify & Challenge:** Identify requirements, edge cases, and trade-offs. Constructively critique flawed approaches.
3. **Draft Plan:** Break down into potential tasks, affected modules, and risks.
4. **User Approval (Mandatory):** Present an executive summary in chat. Obtain explicit confirmation before writing files.
5. **Record Plan:**
   - Scan `docs/02_Tasks/Plans/` for the next available `PLAN-XXX` ID.
   - Create `docs/02_Tasks/Plans/PLAN-XXX-<slug>.md` using `docs/00_Templates/TEMPLATE_PLAN.md`.
   - Add task card to `## 📥 Бэклог (Backlog)` in `docs/02_Tasks/Kanban.md`.
   - If promoted from Icebox: remove item from Icebox, assign sequential Phase number in `docs/02_Tasks/Roadmap.md`, and link relevant ADR/Research notes.
6. **Git Sync (Conditional):**
   - Stage: `git add docs/02_Tasks/Plans/ docs/02_Tasks/Kanban.md docs/02_Tasks/Roadmap.md`
   - Commit: `git commit -m "docs(plan): record PLAN-XXX <slug> and update backlog"`
   - Push if remote origin exists.
