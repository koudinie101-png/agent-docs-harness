---
name: kb-onboard
description: "Display developer onboarding guide, 4-stage lifecycle cheatsheet, and quick start."
---

# /kb-onboard — Developer & Agent Onboarding

Use when the user runs `/kb-onboard` or asks how to interact with the project and knowledge base.

## 🚨 Constraints
* **Adherence to Core Rules:** All work strictly adheres to the 4 operating modes defined in `AGENTS.md`.

## Procedure
1. **Present Onboarding Cheatsheet:**
   - Display reference table of `/kb-*` slash commands and 4-stage development lifecycle:
     - **Mode 0 (`/kb-research` & `/kb-adr`):** Discovery & Feasibility. Falsification, benchmarks, Icebox sync.
     - **Mode 1 (`/kb-plan`):** Conceptual Planning & RFC. Modifying code is prohibited.
     - **Mode 2 (`/kb-task`):** Engineering Specification & Contracts. Modifying code is prohibited.
     - **Mode 3 (`/kb-implement` & `/kb-complete`):** Strict implementation, automated tests, Devlog, and git sync.
2. **Review Invariants:**
   - **Permalinks:** Specs and bugs are never moved or deleted upon completion.
   - **Regression-First:** Bugs require an automated failing test before fix.
   - **Anti-Echo:** Response summaries with links instead of dumping full file bodies into chat.
3. **Reference Full Guide:**
   - Direct developer to `docs/Onboarding.md` and `docs/00_Index.md` for full onboarding guide.
