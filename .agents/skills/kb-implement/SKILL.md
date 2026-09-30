---
name: kb-implement
description: >-
  Mode 3 (Implementation): Implement code strictly according to approved TASK-XXX specification,
  supports Smart Feature Branching or Trunk-Based workflow, executes verification plan commands, and transitions to /kb-complete.
---

# /kb-implement — Mode 3: Implementation & Verification

Use this skill when the user runs `/kb-implement <TASK-XXX>`, asks to write code for a specified task, or starts Mode 3.

## Procedure

1. **Review Specification & Synchronize:**
   - Locate and read the target specification `docs/02_Tasks/Specs/<Phase>/TASK-XXX-<slug>.md`.
   - Verify that requirements, affected files list, and Verification Plan are clear.
   - If Git is enabled and remote `origin` exists: run `git pull --rebase` to ensure implementation starts on the freshest base.
2. **Branching Strategy (Smart Feature Branching):**
   - **Default / Small Task:** Implement directly on `main` (Trunk-Based) for speed and simplicity.
   - **Feature Branch (Large feature or peer review):**
     - Create and switch to a dedicated branch: `git checkout -b feat/TASK-XXX-<slug>`.
     - Isolates active work until all tests pass, protecting collaborators from intermediate breakages.
3. **Execute Changes:**
   - Modify and create only the files specified in section 2 of the specification (`[NEW]`, `[MODIFY]`, `[DELETE]`).
   - Follow existing project code style and architectural boundaries.
4. **Execute Verification Plan:**
   - Run compilation command (e.g. `dotnet build`, `./gradlew assembleDebug`).
   - Run automated test suites (e.g. `dotnet test`, `./gradlew testDebugUnitTest`).
   - Confirm all tests are green (exit code 0).
5. **Transition to Completion:**
   - Invoke or recommend `/kb-complete <TASK-XXX>` to finalize status across the knowledge base, merge or push the branch, and synchronize with Git.
