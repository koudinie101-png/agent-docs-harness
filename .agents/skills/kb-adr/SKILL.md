---
name: kb-adr
description: "Record Architecture Decision Record ADR-XXXX, capturing context, trade-offs, and rejected options."
---

# /kb-adr — Architectural Decision Record (ADR)

Use when the user runs `/kb-adr <name>`, decides on an architectural trade-off, or formally rejects an unviable architectural direction.

## 🚨 Constraints
* **Mandatory Rejected Alternatives:** Every ADR must explicitly document discarded candidate options and the deal-breaker flaws that disqualified them.
* **Dedicated Rejected ADRs:** When a concept or proposal is investigated and discarded as unviable, create a dedicated ADR titled `Отказ от <название>` with `status: rejected` to permanently protect against recurring mistakes.

## Procedure
1. **Calculate ID:**
   - Scan `docs/03_Decisions_ADR/` for the next available 4-digit ID `ADR-XXXX`.
2. **Draft the ADR:**
   - Create `docs/03_Decisions_ADR/ADR-XXXX-<slug>.md` using `docs/00_Templates/TEMPLATE_ADR.md`.
   - Fill in: Context & Problem, Decision (`status: accepted` or `status: rejected`), Considered & Rejected Alternatives (technical flaws/risks), and Consequences.
3. **Update Index:**
   - Add entry in `docs/00_Index.md` under section 3 (Архитектурные решения).
4. **Git Sync (Conditional):**
   - Stage: `git add docs/03_Decisions_ADR/ docs/00_Index.md`
   - Commit: `git commit -m "docs(adr): record ADR-XXXX <slug>"`
   - Push if remote origin exists.
