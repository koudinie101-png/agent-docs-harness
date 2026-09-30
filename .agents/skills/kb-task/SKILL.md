---
name: kb-task
description: >-
  Mode 2 (Task Specification): Create detailed engineering specification TASK-XXX with file contracts and verification plan.
  STRICTLY PROHIBITS CHANGING CODE. Updates Kanban to In Progress.
---

# /kb-task — Mode 2: Task Specification

Use this skill when the user runs `/kb-task <name>`, asks to create a specification/ТЗ, or starts Mode 2.

## 🚨 Hard Constraint: NO CODE CHANGES
* **DO NOT** modify, create, or delete any source code files (`.cs`, `.kt`, `.py`, build scripts, etc.).
* Only read tools and file creation for the specification are allowed.

## Procedure

1. **Scan Existing Tasks:**
   - Inspect files in `docs/02_Tasks/Specs/` to calculate the next available `TASK-XXX` ID (e.g. `TASK-029`).
2. **Determine Target Phase:**
   - Identify the appropriate phase folder (e.g. `docs/02_Tasks/Specs/07_Multimedia_Preview/`). If a new phase is starting, create its subfolder.
3. **Draft the Specification:**
   - Critically evaluate proposed contracts, APIs, and data models against platform best practices to prevent architectural debt or subtle bugs.
   - Create `docs/02_Tasks/Specs/<Phase_Folder>/TASK-XXX-<slug>.md` using `docs/00_Templates/TEMPLATE_TASK.md` with standard YAML frontmatter.
   - Specify:
     - Exact affected files: `[NEW]`, `[MODIFY]`, `[DELETE]`.
     - Key class/method signatures, data models, exception handling.
     - **Verification Plan:** exact build commands (`dotnet build`, `./gradlew test`), automated unit tests, and manual verification steps.
     - **Definition of Done (DoD).**
4. **Update Kanban:**
   - Move or add the task card in `docs/02_Tasks/Kanban.md` to `## ⏳ В работе (In Progress)`.
5. **Git Commit & Push (Conditional):**
   - If Git is enabled:
     - Stage the specification and updated Kanban: `git add docs/02_Tasks/Specs/ docs/02_Tasks/Kanban.md`
     - Commit: `git commit -m "docs(spec): add TASK-XXX <slug> and set in-progress"`
     - If remote `origin` is configured, push: `git push`. If in Local-Only mode (no remote), skip push.
