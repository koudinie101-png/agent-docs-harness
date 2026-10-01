---
name: docs-as-code
description: >-
  Standard Docs-as-Code knowledge base and task management system for Antigravity projects.
  Use when initializing a new project (/kb-init), onboarding developers or agents (/kb-onboard),
  navigating the 3-mode workflow (Mode 1: /kb-plan, Mode 2: /kb-task, Mode 3: /kb-implement & /kb-complete),
  logging defects (/kb-bug), ADRs (/kb-adr), research (/kb-research), publishing releases (/kb-release), or linting knowledge base integrity (/kb-lint).
---

# Docs-as-Code Knowledge Base & Task Workflow (Antigravity Standard)

This skill provides a complete, standardized **Docs-as-Code** infrastructure for Antigravity projects. It integrates with Obsidian as a knowledge vault, enforces progressive task management, provides rich templates with YAML frontmatter properties, and automates synchronization between plans, specifications, Kanban, Roadmap, and Devlog.

---

## 🚀 Quick Reference: Slash Commands & Workflows

| Command | Operating Mode | Description |
| :--- | :--- | :--- |
| `/kb-init` | All | Scaffolds the complete `docs/` structure, templates, and `.obsidian/graph.json` in a new project. |
| `/kb-onboard` | All | Displays the complete onboarding guide, workflow cheatsheet, and directory index. |
| `/kb-plan <name>` | **Mode 1: Planning (RFC)** | Creates `docs/02_Tasks/Plans/PLAN-XXX-<slug>.md` with Q&A, impact analysis, updates Kanban Backlog, and pushes to Git. |
| `/kb-task <name>` | **Mode 2: Task Specification** | Calculates next `TASK-XXX`, generates spec in `docs/02_Tasks/Specs/<Phase>/`, sets status to In Progress, and pushes to Git. |
| `/kb-implement <TASK-XXX>` | **Mode 3: Implementation** | Guides strict implementation against spec, executes verification commands, and transitions to completion. |
| `/kb-complete <TASK-XXX>` | **Mode 3: Done** | Marks task Done in Kanban with date, checks `[x]` in Roadmap with permalink, updates spec header, writes Devlog entry, runs kb-lint, and pushes commit to Git. |
| `/kb-release <vX.Y.Z>` | **Release Mode** | Pre-flight checks, runs build hook to `dist/`, calculates SHA-256, generates `RELEASE-vX.Y.Z.md`, and publishes via Dual-Mode (GitHub / Local-Only). |
| `/kb-bug <name>` | All | Creates `docs/02_Tasks/Bugs/BUG-XXX-<slug>.md` with RCA, enforces a Regression-First test, and pushes to Git. |
| `/kb-adr <name>` | All | Records an Architectural Decision Record in `docs/03_Decisions_ADR/ADR-XXXX-<slug>.md`, updates index, and pushes to Git. |
| `/kb-research <name>` | All | Creates a research note in `docs/04_Research/RESEARCH-XXX-<slug>.md`, updates index, and pushes to Git. |
| `/kb-lint` | All | Runs `kb_lint.py` to check for broken `[[wikilinks]]`, missing specs, and Kanban/Roadmap desync. |

---

## 🏛️ Standard Directory Structure (`docs/`)

Every project following this standard must have the following layout:

```text
docs/
├── .obsidian/
│   └── graph.json                    # Obsidian Graph Color Palette configuration
├── 00_Index.md                       # Map of Content (MOC) & vault entry point
├── 00_Templates/                     # Central repository of reusable templates
│   ├── TEMPLATE_ONBOARDING.md
│   ├── TEMPLATE_INDEX.md
│   ├── TEMPLATE_KANBAN.md
│   ├── TEMPLATE_ROADMAP.md
│   ├── TEMPLATE_DEVLOG.md
│   ├── TEMPLATE_PLAN.md
│   ├── TEMPLATE_TASK.md
│   ├── TEMPLATE_BUG.md
│   ├── TEMPLATE_ADR.md
│   ├── TEMPLATE_RESEARCH.md
│   ├── TEMPLATE_ARCHITECTURE.md
│   ├── TEMPLATE_TEST.md
│   └── TEMPLATE_RELEASE.md
├── Onboarding.md                     # Comprehensive developer and agent onboarding guide
├── Devlog.md                         # Chronological development journal
├── 01_Architecture/                  # System diagrams, component specs, data flows
├── 02_Tasks/
│   ├── Kanban.md                     # Operational task board (Backlog, In Progress, Done)
│   ├── Roadmap.md                    # Strategic milestones and phase tracking
│   ├── Plans/                        # RFCs & high-level feature plans (Mode 1)
│   ├── Specs/                        # Detailed task specifications grouped by phase (Mode 2)
│   │   ├── 01_<PhaseName>/
│   │   └── ...
│   ├── Bugs/                         # Defect reports with RCA and regression tests (BUG-XXX)
│   └── Releases/                     # Release documents (RELEASE-vX.Y.Z.md, SHA-256 checksums)
├── 03_Decisions_ADR/                 # Architectural Decision Records (ADR-XXXX)
├── 04_Research/                      # Platform quirks, investigation notes (RESEARCH-XXX)
└── 05_Testing/                       # E2E test checklists, QA strategy, test matrices
```

---

## 🧠 Critical Thinking & Constructive Partnership Standard

Antigravity assistants act as senior engineering partners, not passive "yes-men":
1. **Critical Evaluation:** When the user or assistant proposes a feature, architecture shift, protocol change, or implementation technique, evaluate it against industry best practices (.NET/Windows API, Android/Kotlin, Local-First, Security, UX).
2. **Constructive Challenge:** If an idea is suboptimal, violates platform conventions, introduces hidden bugs (e.g., Android Doze/WakeLock issues, memory leaks, UI thread stalls), or creates technical debt:
   - **Highlight the flaw directly:** Do not implement or agree with a bad idea without warning.
   - **Justify with technical reasons:** Explain *why* it is problematic and *where/how* it will negatively impact system performance, stability, or UX.
   - **Offer better alternatives:** Propose 1–2 robust, idiomatic alternatives with their pros and cons.
3. **Respect user decisions:** After risks and trade-offs are clearly explained, if the user still decides on a specific path, proceed while documenting the decision and known trade-offs in the plan or ADR.
4. **Document Rejected Ideas Permanently (Фиксация нежизнеспособных решений):** In both Research notes and ADRs, explicitly document rejected candidate options, failed prototypes, and root causes of unviability. For discarded architectural directions or rejected feature proposals, log a dedicated Rejected ADR (`status: rejected`, e.g. `ADR-XXXX: Отказ от...`) to permanently protect against recurring mistakes.

---

## 🔄 The 3-Mode Development Cycle

### Mode 1: Planning / RFC (`/kb-plan`)
* **Trigger:** Discussing a new feature, architecture shift, or complex refactoring.
* **Hard Constraint:** **NO CODE CHANGES!** Only research, Q&A, critical review, and design discussion.
* **Procedure:**
  1. Determine problem statement, goals, and architectural impact.
  2. Critically evaluate proposals: highlight flaws/anti-patterns, justify negative impacts, suggest better alternatives.
  3. Ask clarifying questions to resolve trade-offs.
  4. Obtain explicit user confirmation.
  5. Generate `docs/02_Tasks/Plans/PLAN-XXX-<slug>.md` using `TEMPLATE_PLAN.md`.
  6. Add task card to `docs/02_Tasks/Kanban.md` under `## 📥 Бэклог (Backlog)`.
  7. **Git Commit & Push (Conditional):** stage plan & Kanban updates, commit `docs(plan): add PLAN-XXX <slug>`, and push to remote if `origin` is configured (skip push if Local-Only).

### Mode 2: Task Specification (`/kb-task`)
* **Trigger:** Transitioning a planned feature or user request into an engineering specification.
* **Hard Constraint:** **NO CODE CHANGES!** Only reading code and creating the spec file.
* **Procedure:**
  1. Find next available `TASK-XXX` ID (inspect existing files in `docs/02_Tasks/Specs/`).
  2. Determine target phase folder: `docs/02_Tasks/Specs/<Phase_Folder>/`.
  3. Create specification file using `TEMPLATE_TASK.md` specifying:
     - Exact affected files: `[NEW]`, `[MODIFY]`, `[DELETE]`.
     - Code contracts, data models, exception handling.
     - Verification Plan: build commands, unit tests, manual checks.
     - Definition of Done (DoD).
  4. Move or add card in `docs/02_Tasks/Kanban.md` to `## ⏳ В работе (In Progress)`.
  5. **Git Commit & Push (Conditional):** stage spec & Kanban updates, commit `docs(spec): add TASK-XXX <slug>`, and push to remote if `origin` is configured (skip push if Local-Only).

### Mode 3: Implementation & Verification (`/kb-implement` & `/kb-complete`)
* **Trigger:** User gives command to code according to approved `TASK-XXX`.
* **Procedure:**
  1. Read approved `TASK-XXX` specification thoroughly.
  2. Write implementation strictly adhering to the spec.
  3. Execute **Verification Plan** (e.g. `dotnet build`, `./gradlew test`, test scripts).
  4. Run `/kb-complete <TASK-XXX>`:
     - In spec file: update header status to `Выполнено`.
     - In `Kanban.md`: move card to `## ✅ Готово (Done)` with current date `(YYYY-MM-DD)`.
     - In `Roadmap.md`: check milestone box `[x]` with permanent link `[[Specs/<Phase>/TASK-XXX-<name>|TASK-XXX]]`.
     - In `Devlog.md`: add chronological entry detailing what was done, tests passed, and next step.
     - Run `kb_lint.py` to ensure knowledge base links integrity.
     - **Git Commit & Push (Conditional):** stage all changes (`git add .`), commit (`git commit -m "feat(...): complete TASK-XXX ..."`), and push to remote if `origin` is configured (skip push if Local-Only).

---

## 🌐 Version Control: Hybrid Model (Trunk-Based Docs + Smart Feature Branching)
1. **Trunk-Based Documentation (`main`):**
   - All knowledge base artifacts (`docs/`), planning (`/kb-plan`), specs (`/kb-task`), ADRs (`/kb-adr`), and Kanban remain strictly in `main` as the Single Source of Truth.
   - Every creation/update runs `git pull --rebase` before writing and pushes to `origin/main` immediately.
2. **Implementation Workflows (`/kb-implement`):**
   - **Small/Standard Tasks:** Work directly on `main` for speed.
   - **Large Features or Peer Review:** Use dedicated feature branches `feat/TASK-XXX-<slug>` or `bug/BUG-XXX-<slug>` to isolate intermediate work.
   - Merge back into `main` via `/kb-complete` (direct merge or GitHub Pull Request).
3. **Remote vs Local-Only:**
   - **Remote Mode:** If `origin` is configured, automatically push commits and pull remote updates.
   - **Local-Only Mode:** If no remote `origin` is configured, all skills create local Git commits to keep revision history, but automatically skip `git push`.
   - **No Git:** Skip Git operations gracefully.

---

## 💡 Capturing Ideas & Hypotheses (Icebox vs Roadmap)

* **🚨 Anti-Pattern:** **NEVER** add raw, unresearched ideas directly as numbered Phases (e.g. `## Фаза 8: ...`) into `Roadmap.md`. Doing so causes premature phase coupling, broken sequential numbering when priorities shift, and roadmap pollution.
* **Quick Capture (5 seconds):**
  - Add the idea to `## 💡 Идеи и гипотезы (Icebox / Future Ideas)` at the bottom of `docs/02_Tasks/Kanban.md` with the tag `#idea`.
* **Strategic Horizons (Thematic vision):**
  - Add to `## 🔮 Перспективные направления (Future Horizons / Ideas)` at the bottom of `docs/02_Tasks/Roadmap.md` as bullet points without phase numbers.
* **Promotion to Active Phase:**
  - When ready to explore an idea, invoke `/kb-plan <name>` (Mode 1). Once the RFC is approved, assign the next sequential Phase number in `Roadmap.md` and scaffold tasks via `/kb-task` (Mode 2).

---

## 🏷️ Standard YAML Frontmatter Properties

All Markdown documents must start with YAML frontmatter to support Obsidian Properties and Dataview:

### Task Specification (`TASK-XXX`):
```yaml
---
id: TASK-026
title: Android Media and Voice Extractor
status: in-progress # planned | in-progress | done | cancelled
type: task
phase: 7
component:
  - android
  - media
parent_plan: "[[PLAN-008-multimedia-preview]]"
created: 2026-09-19
updated: 2026-09-19
tags:
  - task/spec
  - component/android
---
```

### Defect Report (`BUG-XXX`):
```yaml
---
id: BUG-005
title: Windows Toast Tag Length Overflow
severity: major # blocker | critical | major | minor
component:
  - windows
  - toast
status: fixed # new | investigating | confirmed | in-progress | fixed | wontfix
regression_test: "tests/RemoteNotification.Tests/ToastNotificationServiceTests.cs"
created: 2026-09-19
updated: 2026-09-19
tags:
  - bug
  - component/windows
---
```

### Architectural Decision Record (`ADR-XXXX`):
```yaml
---
id: ADR-0004
title: Multimedia Preview Transport and Storage
status: accepted # proposed | accepted | rejected | deprecated | superseded
date: 2026-09-19
tags:
  - adr
  - architecture
---
```

---

## 🔗 Permalinks and Naming Conventions

1. **Permalinks Principle (No Link Rot):** Files are **NEVER** moved to `Done/` or `Archive/` folders when completed. Status is updated in YAML frontmatter, Kanban, and Roadmap.
2. **File Naming Rules:**
   - Tasks: `TASK-XXX-<slug>.md`
   - Plans: `PLAN-XXX-<slug>.md`
   - Bugs: `BUG-XXX-<slug>.md`
   - ADRs: `ADR-XXXX-<slug>.md` (4 digits, uppercase ADR prefix)
   - Research: `RESEARCH-XXX-<slug>.md`
   - Architecture: `<ComponentName>.md`
   - Testing: `<ScenarioName>.md`

---

## 🎨 Obsidian Graph Color Scheme (`.obsidian/graph.json`)

* ⚪ **White / Silver:** Root hubs (`file:00_Index`, `file:Devlog`, `file:SPEC`, `file:Onboarding`).
* 🟣 **Purple:** Architecture (`path:01_Architecture`).
* 🔵 **Cyan / Blue:** ADRs (`path:03_Decisions_ADR`, `#adr`).
* 🟡 **Amber / Yellow:** Research (`path:04_Research`, `#research`).
* 🟠 **Orange:** Tasks, Plans, Roadmap (`path:02_Tasks`, `#task`).
* 🔴 **Red:** Bugs (`path:02_Tasks/Bugs`, `#bug`).
* 🟢 **Green:** Testing & QA (`path:05_Testing`, `#testing`).
