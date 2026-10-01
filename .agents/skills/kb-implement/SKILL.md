---
name: kb-implement
description: "Mode 3: Implement code strictly adhering to TASK-XXX spec with automated verification."
---

# /kb-implement — Mode 3: Implementation & Verification

Use when the user runs `/kb-implement <TASK-XXX>` or begins writing code for an approved specification.

## 🚨 Constraints
* **Spec Adherence:** Implement strictly what is defined in the approved `TASK-XXX` spec. Avoid scope creep.
* **Verification First:** Never conclude implementation without executing all checks in the Verification Plan.

## Procedure
1. **Sync & Review:**
   - Read `docs/02_Tasks/Specs/<Phase>/TASK-XXX-<slug>.md`. Confirm affected files and Verification Plan.
   - Sync base branch: `git pull --rebase` (if remote exists).
2. **Branching Strategy:**
   - **Trunk-Based (Default / Small Task):** Work directly on `main`.
   - **Feature Branch (Complex Task / Review):** `git checkout -b feat/TASK-XXX-<slug>`.
3. **Execute Implementation:**
   - Modify and create only the files listed in section 2 of the specification (`[NEW]`, `[MODIFY]`, `[DELETE]`).
   - Adhere to project architecture, Zero Dependencies, and platform conventions.
4. **Execute Verification Plan:**
   - Run compilation command (e.g. `dotnet build`, `python build.py`).
   - Run test suites (e.g. `python -m unittest discover -s tests`).
   - Verify exit code 0 for all commands.
5. **Transition:**
   - Recommend or trigger `/kb-complete <TASK-XXX>` to update knowledge base tracking and Git.
