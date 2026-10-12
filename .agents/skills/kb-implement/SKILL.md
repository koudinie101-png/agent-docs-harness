---
name: kb-implement
description: "Mode 3: Implement TASK-XXX or resolve BUG-XXX with verification and immediate auto-completion."
---

# /kb-implement — Mode 3: Implementation & Verification

Use when the user runs `/kb-implement <TASK-XXX | BUG-XXX>` or begins implementation.

## 🚨 Constraints
* **Target Adherence:** For tasks, implement strictly what is defined in the approved `TASK-XXX` spec. For bugs, eliminate the root cause identified in `BUG-XXX`. Avoid scope creep.
* **Single-Task Barrier:** Execute strictly ONE target (task or bug). Never auto-chain to subsequent tasks without an explicit user command.
* **Verification First:** Never conclude implementation without executing all checks in the Verification Plan or full test suites.
* **Auto-Complete:** When all verification steps pass, immediately execute completion (`kb-complete`) without waiting for an extra user prompt.

## Procedure
0. **Memory-First Check:**
   - Если существует `docs/06_Memory/patterns.md`, ознакомиться с активными паттернами.
   - Проверить, содержит ли текущая задача риски из списка граблей (Windows paths, ложные моки, несовместимость версий, галлюцинации API).
   - Учесть защитные правила паттернов при проектировании решения.
1. **Sync & Context:**
   - If `TASK-XXX`: read `docs/02_Tasks/Specs/<Phase>/TASK-XXX-<slug>.md`. Confirm affected files and Verification Plan.
   - If `BUG-XXX`: read `docs/02_Tasks/Bugs/BUG-XXX-<slug>.md`. Confirm reproduction steps and Root Cause Analysis (RCA).
   - Sync base branch: `git pull --rebase` (if remote exists).
2. **Branching Strategy:**
   - **Trunk-Based (Default / Small Target):** Work directly on `main`.
   - **Feature Branch (Complex Target / Review):** `git checkout -b feat/<target>-<slug>`.
3. **Execute Implementation:**
   - **For Tasks (`TASK-XXX`):**
     * Modify and create only the files listed in section 2 of the specification (`[NEW]`, `[MODIFY]`, `[DELETE]`).
     * Adhere to project architecture, Zero Dependencies, and platform conventions.
   - **For Defects (`BUG-XXX` — Regression-First TDD Pipeline):**
     * **RED:** Create or run reproduction test (from `regression_test` in bug report). Verify test failure reproducing the defect.
     * **GREEN:** Implement minimal fix in source code to make the reproduction test pass.
     * **REFACTOR:** Run full test suite to guarantee zero regression across the project.
4. **Execute Verification:**
   - Run compilation commands (e.g. `dotnet build`, `python build.py`).
   - Run test suites (e.g. `python -m unittest discover -s tests`).
   - Run KB integrity check (`python scripts/kb_lint.py --path docs`).
   - Verify exit code 0 for all commands.
5. **Immediate Auto-Completion & Stop:**
   - Upon all checks passing (Exit code 0), immediately execute `/kb-complete <TASK-XXX | BUG-XXX>` to finalize without waiting for user input.
   - Once kb-complete finishes, strictly STOP calling tools and yield control to the user.
