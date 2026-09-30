---
name: kb-research
description: >-
  Record a platform research note RESEARCH-XXX in docs/04_Research/ documenting OS quirks,
  background limitations, failure modes, trade-off matrices, and rejected unviable approaches.
---

# /kb-research — Platform Investigation & Research

Use this skill when the user runs `/kb-research <name>`, tests technical hypotheses, or investigates platform/API pitfalls.

## 🧠 Critical Thinking in Research (Стресс-тестирование гипотез)
* **Devil's Advocate & Falsification:** Don't just search for proofs that an idea works on the happy path. Actively stress-test it against real-world constraints: Android Doze mode / OEM background killers, Windows thread safety / UI freezes, network roaming / packet loss, memory leaks on media files, and security risks.
* **Trade-off Evaluation:** Compare competing approaches in an explicit Trade-off Matrix (stability, battery drain, latency, code maintainability).
* **Document Rejected Hypotheses:** Every rejected idea, non-viable prototype, or dead-end must be explicitly recorded with the technical reasons why it failed, preventing future sessions from repeating the same mistakes.
* **Escalate to Rejected ADR:** If an architectural concept is formally discarded as unviable, record an Architectural Decision Record with `status: rejected` (`/kb-adr`) to permanently lock the decision.

## Procedure

1. **Calculate ID:**
   - Scan `docs/04_Research/` to find the next ID `RESEARCH-XXX` (e.g. `RESEARCH-005`).
2. **Formulate & Stress-Test Hypotheses:**
   - Define candidate approaches and test edge cases (battery, memory, background lifecycle, OS limits).
   - Identify drawbacks, anti-patterns, and failure modes.
3. **Draft the Research Document:**
   - Create `docs/04_Research/RESEARCH-XXX-<slug>.md` using `docs/00_Templates/TEMPLATE_RESEARCH.md` with standard YAML frontmatter.
   - Detail:
     - Context, problem statement, and investigated hypotheses.
     - Critical analysis: failure modes, background behavior, edge cases.
     - Practical experiments, benchmark numbers, and test code.
     - Trade-off matrix comparing options.
     - Rejected alternatives and root causes of unviability.
     - Developer rules to prevent future regressions.
4. **Log Rejected ADR if Architecture-Level Decision:**
   - If an architectural approach or proposed feature is rejected, create `ADR-XXXX` with `status: rejected` via `/kb-adr`.
5. **Update Index:**
   - Add reference in `docs/00_Index.md` under section 4 (Исследования).
6. **Git Commit & Push (Conditional):**
   - If Git is enabled:
     - Stage the new research note and updated index: `git add docs/04_Research/ docs/00_Index.md`
     - Commit: `git commit -m "docs(research): add RESEARCH-XXX <slug>"`
     - If remote `origin` is configured, push: `git push`. If in Local-Only mode (no remote), skip push.
