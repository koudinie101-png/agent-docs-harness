---
name: kb-adr
description: "Record Architecture Decision Record ADR-XXXX, capturing context, trade-offs, and rejected options."
---

# /kb-adr — Architectural Decision Record (ADR)

Use when the user runs `/kb-adr <name>`, decides on an architectural trade-off, or formally rejects an unviable architectural direction.

## 🚨 Constraints
* **Mandatory Rejected Alternatives:** Document discarded options and disqualified flaws.
* **Dedicated Rejected ADRs:** For unviable proposals, log `Отказ от <название>` with `status: rejected`.

## Procedure
1. **Calculate ID:** Scan `docs/03_Decisions_ADR/` for the next `ADR-XXXX`.
2. **Draft the ADR:** Create `docs/03_Decisions_ADR/ADR-XXXX-<slug>.md` using `TEMPLATE_ADR.md` (Context, Decision, Rejected Options, Consequences).
3. **Roadmap & Index Sync:**
   - *Accepted:* register in `docs/02_Tasks/Roadmap.md` (Icebox or active phase).
   - *Rejected:* add to `## 🚫 Отклоненные архитектурные идеи` in `docs/02_Tasks/Roadmap.md`.
   - Add reference in `docs/00_Index.md` (section 3).
4. **Git Sync (Conditional):**
   - Stage and commit: `git add docs/03_Decisions_ADR/ docs/02_Tasks/Roadmap.md docs/00_Index.md && git commit -m "docs(adr): record ADR-XXXX <slug>"`. Push if remote exists.
