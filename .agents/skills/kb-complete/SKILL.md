---
name: kb-complete
description: "Mode 3: Finalize TASK-XXX or BUG-XXX, update Kanban/Roadmap/Devlog, run kb_lint, and git commit."
---

# /kb-complete — Mode 3: Finalization & Knowledge Base Sync

Use when the user runs `/kb-complete <TASK-XXX | BUG-XXX>` after all verification steps have passed.

## 🚨 Constraints
* **Single-Task Barrier:** Finalize only the specified task or bug. Do not begin or execute subsequent work.
* **Passing Tests Required:** Do not mark complete if any verification step failed.
* **Permalinks Invariant:** Never move or archive spec or bug files. Update status in-place.

## Procedure
1. **Update Target Status:**
   - **Task (`TASK-XXX`):** In `docs/02_Tasks/Specs/<Phase>/TASK-XXX-<slug>.md`: set frontmatter `status: done`, `updated: <YYYY-MM-DD>`, and header `> **Статус:** Выполнено (Режим 3)`.
   - **Defect (`BUG-XXX`):** In `docs/02_Tasks/Bugs/BUG-XXX-<slug>.md`: set frontmatter `status: fixed`, `fixed_in: "<target_release>"`, `updated: <YYYY-MM-DD>`, and header `> **Статус:** [fixed]`. If `target_release` is empty, use current active version from `SPEC.md` / `Roadmap.md`.
2. **Update Kanban:**
   - Move target card from `## ⏳ В работе (In Progress)` to `## ✅ Готово (Done)` in `docs/02_Tasks/Kanban.md` with completion date `(YYYY-MM-DD)`.
3. **Update Roadmap:**
   - For `TASK-XXX`: check milestone `[x]` with permanent link `[[Specs/<Phase>/TASK-XXX-<slug>|TASK-XXX]]`.
   - For `BUG-XXX`: if tracked in a Roadmap phase, mark milestone `[x]`.
4. **Append Devlog:**
   - In `docs/Devlog.md`: record summary of changes and test verification results using semantic format:
     * For tasks: `- **Рекомендуемый следующий шаг (Ожидает команды пользователя):** \`<next command>\`.`
     * For bugs: note resolution via TDD with link to regression test.
5. **Living Spec Sync:**
   - If task or fix modified public CLI flags, APIs, or system architecture: update `SPEC.md` and `README.md` in that same session.
6. **Tech Debt Migration (DEBT-XXX):**
   - In `docs/02_Tasks/TechDebt.md`, for a task tagged `#techdebt`, move its resolved `DEBT-XXX` row from `## 📋 Открытый технический долг (Active P3 Debt)` to `## ✅ Погашенный технический долг (Resolved Debt)` with a link `[[Specs/.../TASK-XXX|TASK-XXX]]`.
7. **Defect Loop Reflection:**
   - Если возникли процедурные ошибки, падения тестов или сбои:
     * Оформить отчет `docs/06_Memory/Incidents/INC-XXX-<slug>.md` (`TEMPLATE_INCIDENT.md`).
     * **Двухосевой промоушен:**
       1. *Ось 1 (Частота/Тяжесть):* при count $\ge 2$ или high severity обновить `docs/06_Memory/patterns.md` (лимит $\le 15$).
       2. *Ось 2 (Охват):* системный сбой вынести в автотест (Tier 1) или `AGENTS.md` (Tier 2).
   - Если сессия прошла чисто: зафиксировать отсутствие инцидентов.
8. **Lint Verification:**
   - Run `python scripts/kb_lint.py --path docs` to confirm 0 broken links.
9. **Git Commit & Sync:**
   - **Task Commit:** `git commit -m "feat(<scope>): complete TASK-XXX <summary> and sync docs"`.
   - **Bug Commit:** `git commit -m "fix(<scope>): resolve BUG-XXX <summary> with regression test"`.
   - Push to remote if origin exists.
10. **Next Step (State-Aware) & Stop & Yield Control:**
   - If all tasks in the current phase are `[x]`: recommend acceptance testing in `docs/05_Testing/` and `/kb-release <vX.Y.Z>`.
   - Else propose `/kb-implement TASK-YYY` only if its spec exists in `docs/02_Tasks/Specs/`; otherwise `/kb-task TASK-YYY`.
   - Render concise Anti-Echo summary (`[FileName](file://...)`, 3–5 bullets) and STOP.
