---
name: kb-research
description: "Mode 0: Validate ideas & hypotheses (RESEARCH-XXX), stress-test risks, register in Roadmap Icebox or reject."
---

# /kb-research — Mode 0: Discovery & Feasibility Research

Use when validating new ideas, testing technical hypotheses, exploring architectural trade-offs, or investigating platform pitfalls.

## 🚨 Constraints
* **Critical Partner & Falsification:** Stress-test proposals against platform limits: OS lifecycle, Zero-Deps (ADR-0001), token economy (ADR-0009), performance, and security. Actively try to falsify assumptions.
* **Preserve Dead Ends:** Explicitly document unviable alternatives and rejected prototypes to prevent recurring mistakes.

## Procedure
1. **Calculate ID:** Scan `docs/04_Research/` for the next available `RESEARCH-XXX`.
2. **Stress-Test & Measure:** Prototype minimally, measure limits, identify trade-offs, evaluate Value vs Effort.
3. **Draft Research Note:** Create `docs/04_Research/RESEARCH-XXX-<slug>.md` using `docs/00_Templates/TEMPLATE_RESEARCH.md` (Context, Hypotheses, Trade-off Matrix, Discarded Options, Conclusions).
4. **Automated Outcome Routing:**
   - **Primary Stack Selection (Greenfield):** If `SPEC.md` has `status: discovery` and this research selects the foundational stack (ADR-0001):
     - Update `SPEC.md` status to `status: active`.
     - Populate Section 2 of `SPEC.md` with chosen tech stack, build/test commands, and architectural layers.
     - Synchronize `README.md` with factual quickstart commands.
   - **Validated & Approved:**
     - If architectural impact: invoke `/kb-adr` to record accepted `ADR-XXXX`.
     - Register validated initiative in `## 🔮 Перспективные направления (Future Horizons / Icebox)` in `docs/02_Tasks/Roadmap.md` with wikilinks and Value Impact rating.
   - **Unviable / Overengineered (Rejected):**
     - Invoke `/kb-adr` to record rejected ADR (`status: rejected`).
     - Register entry in `## 🚫 Отклоненные архитектурные идеи (Rejected Alternatives)` in `docs/02_Tasks/Roadmap.md` with link to ADR.
5. **Index & Git Sync:**
   - Link research note in `docs/00_Index.md` (section 4: Исследования).
   - Git commit: `git add docs/04_Research/ docs/02_Tasks/Roadmap.md docs/03_Decisions_ADR/ docs/00_Index.md && git commit -m "docs(research): add RESEARCH-XXX <slug>"`. Push if remote origin exists.
