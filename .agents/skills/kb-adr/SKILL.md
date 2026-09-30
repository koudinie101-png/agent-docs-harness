---
name: kb-adr
description: >-
  Record an Architectural Decision Record ADR-XXXX in docs/03_Decisions_ADR/ documenting problem, choice,
  trade-offs, consequences, and explicitly preserving rejected alternatives to prevent recurring anti-patterns.
---

# /kb-adr — Architectural Decision Record (ADR)

Use this skill when the user runs `/kb-adr <name>`, decides on an architectural trade-off, or formally rejects an unviable architectural direction.

## 🛑 Preserving Rejected Ideas (Фиксация нежизнеспособных решений)
* **Never lose the "Why NOT":** Documenting why an approach was rejected is as vital as documenting the chosen path. It permanently prevents future sessions, agents, or contributors from re-introducing dead-end patterns.
* **Two formats of rejection:**
  1. **Rejected Alternatives inside accepted ADRs:** In every approved ADR, thoroughly detail the discarded candidate options and the deal-breaker flaws that disqualified them.
  2. **Dedicated Rejected ADRs (`status: rejected`):** When an architectural concept, feature, or platform hack is investigated and found fundamentally flawed or rejected (e.g., `ADR-0003: Отказ от кастомных кнопок эмодзи...`), create an ADR titled `Отказ от <название>` with `status: rejected`. Clearly explain the technical roadblocks and recommend safe alternatives.

## Procedure

1. **Calculate ID:**
   - Scan `docs/03_Decisions_ADR/` to find the next available 4-digit ID `ADR-XXXX` (e.g. `ADR-0005`).
2. **Draft the ADR:**
   - Create `docs/03_Decisions_ADR/ADR-XXXX-<slug>.md` using `docs/00_Templates/TEMPLATE_ADR.md` with standard YAML frontmatter.
   - Fill in:
     - **Context & Problem:** The architectural dilemma, drivers, and candidate options.
     - **Decision:** Clear choice or explicit rejection statement (`status: accepted` or `status: rejected`).
     - **Considered & Rejected Alternatives:** Explicit reasons, technical traps, and performance/security risks that disqualified other options.
     - **Consequences:** Concrete pros, cons, and operational guidelines.
3. **Update Index:**
   - Add reference in `docs/00_Index.md` under section 3 (Архитектурные решения).
4. **Git Commit & Push (Conditional):**
   - If Git is enabled:
     - Stage the new ADR and updated index: `git add docs/03_Decisions_ADR/ docs/00_Index.md`
     - Commit: `git commit -m "docs(adr): record ADR-XXXX <slug>"`
     - If remote `origin` is configured, push: `git push`. If in Local-Only mode (no remote), skip push.
