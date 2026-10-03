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
   - **Spec Genesis Check (Zero-State Guard):** If `SPEC.md` is missing or has `status: discovery`, issue a Soft Nudge: suggest running `/kb-research <topic>` (Mode 0) to validate the architectural stack and crystallize `SPEC.md` (`status: active`) before deep planning, or confirm to proceed directly.
   - **Explicit Idea:** If specified (`/kb-plan <idea>`), check feasibility maturity:
     - *Pre-flight Nudge:* If proposal introduces new external dependencies (violating ADR-0001), platform uncertainties, or high risk, suggest running `/kb-research <idea>` (Mode 0) first to validate trade-offs and record ADR. If user confirms direct planning or idea is low-risk, proceed immediately.
   - **No Argument (`/kb-plan`):** Inspect Icebox in `docs/02_Tasks/Roadmap.md`. Rank candidates by value impact with 1-line rationale and top recommendation. If empty, ask user.
2. **Clarify & Challenge:** Identify requirements, edge cases, trade-offs. Critique flawed approaches.
3. **Draft Plan:** Break down into potential tasks, affected modules, and risks.
4. **User Approval (Mandatory):** Executive summary in chat; obtain explicit confirmation before writing files.
5. **Record Plan:**
   - Scan `docs/02_Tasks/Plans/` for next `PLAN-XXX`.
   - Create `docs/02_Tasks/Plans/PLAN-XXX-<slug>.md` using `TEMPLATE_PLAN.md`.
   - Add card to `## 📥 Бэклог (Backlog)` in `docs/02_Tasks/Kanban.md`.
   - If from Icebox: promote to sequential Phase in `Roadmap.md` and link relevant ADR/Research notes.
6. **Git Sync (Conditional):**
   - Stage: `git add docs/02_Tasks/Plans/ docs/02_Tasks/Kanban.md docs/02_Tasks/Roadmap.md`
   - Commit: `git commit -m "docs(plan): record PLAN-XXX <slug> and update backlog"`
   - Push if remote origin exists.
