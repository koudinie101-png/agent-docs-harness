---
name: kb-onboard
description: "Display developer onboarding guide, 3-mode workflow cheatsheet, and quick start."
---

# /kb-onboard — Developer & Agent Onboarding

Use when the user runs `/kb-onboard` or asks how to interact with the project and knowledge base.

## 🚨 Constraints
* **Adherence to Core Rules:** All work strictly adheres to the 3 operating modes defined in `AGENTS.md`.

## Procedure
1. **Present Onboarding Cheatsheet:**
   - Display reference table of `/kb-*` slash commands and 3-mode development cycle.
2. **Review Invariants:**
   - **Mode 1 (`/kb-plan`):** Discussion & RFC. Modifying code is prohibited.
   - **Mode 2 (`/kb-task`):** Engineering specification. Modifying code is prohibited.
   - **Mode 3 (`/kb-implement` & `/kb-complete`):** Strict implementation, automated tests, and git sync.
   - **Permalinks:** Specs and bugs are never moved or deleted upon completion.
   - **Regression-First:** Bugs require an automated failing test before fix.
   - **Anti-Echo:** Response summaries with links instead of dumping full file bodies into chat.
3. **Reference Full Guide:**
   - Direct developer to `docs/Onboarding.md` and `docs/00_Index.md` for full onboarding guide.
