---
name: kb-research
description: "Record platform research note RESEARCH-XXX with stress tests, benchmarks, and trade-off matrix."
---

# /kb-research — Platform Investigation & Research

Use when the user runs `/kb-research <name>`, tests technical hypotheses, or investigates platform/API pitfalls.

## 🚨 Constraints
* **Falsification & Stress Testing:** Actively stress-test approaches against real-world constraints: OS lifecycle limits, background task killers, UI blocking, memory leaks, latency, and platform security.
* **Preserve Dead Ends:** Explicitly record all failed prototypes and unviable candidate options to prevent recurring anti-patterns.

## Procedure
1. **Calculate ID:**
   - Scan `docs/04_Research/` to determine the next available ID `RESEARCH-XXX`.
2. **Stress-Test & Measure:**
   - Benchmark candidate options, measure resource consumption, and identify edge cases and failure modes.
3. **Draft Research Note:**
   - Create `docs/04_Research/RESEARCH-XXX-<slug>.md` using `docs/00_Templates/TEMPLATE_RESEARCH.md`.
   - Include: Problem & Hypotheses, Edge Case Stress-Tests, Benchmarks/Code snippets, Trade-off Matrix, and Discarded Options.
4. **Escalate to Rejected ADR (If applicable):**
   - If an architectural direction is formally rejected, trigger `/kb-adr` to log an ADR with `status: rejected`.
5. **Update Index & Git Sync:**
   - Add reference in `docs/00_Index.md` under section 4 (Исследования).
   - Stage and commit: `git add docs/04_Research/ docs/00_Index.md && git commit -m "docs(research): add RESEARCH-XXX <slug>"`. Push if remote exists.
