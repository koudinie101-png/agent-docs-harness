---
name: kb-research
description: "Mode 0: Validate ideas & hypotheses (RESEARCH-XXX), stress-test risks, register in Roadmap Icebox or reject."
---

# /kb-research — Mode 0: Discovery & Feasibility Research

Use when validating new ideas, testing technical hypotheses, exploring architectural trade-offs, or investigating platform pitfalls.

## 🚨 Constraints
* **Falsification & Stress Testing:** Stress-test against platform limits: OS lifecycle, background killers, leaks, latency, security.
* **Preserve Dead Ends:** Explicitly record failed prototypes and unviable candidate options.

## Procedure
1. **Calculate ID:** Scan `docs/04_Research/` for the next `RESEARCH-XXX`.
2. **Stress-Test & Measure:** Benchmark candidates, measure resources, identify failure modes.
3. **Draft Research Note:** Create `docs/04_Research/RESEARCH-XXX-<slug>.md` using `TEMPLATE_RESEARCH.md` (Problem, Hypotheses, Benchmarks, Trade-off Matrix, Discarded Options).
4. **Outcome Routing & Roadmap Registration:**
   - *Validated:* Create `ADR-XXXX` (if needed) and add to `## 🔮 Перспективные направления (Future Horizons / Icebox)` in `docs/02_Tasks/Roadmap.md` with links and value impact.
   - *Rejected:* Trigger `/kb-adr` (`status: rejected`) and add to `## 🚫 Отклоненные архитектурные идеи` in `docs/02_Tasks/Roadmap.md`.
5. **Index & Git Sync:**
   - Reference in `docs/00_Index.md` (section 4).
   - Stage and commit: `git add docs/04_Research/ docs/02_Tasks/Roadmap.md docs/00_Index.md && git commit -m "docs(research): add RESEARCH-XXX <slug>"`. Push if remote exists.
