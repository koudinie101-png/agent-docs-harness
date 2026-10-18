<!-- GENERATED FILE: edit rules/AGENTS_CORE.md, then run: python scripts/gen_rules.py -->
# 🤖 AGENTS.md — AI Agent Guidelines & Operating Modes

> **Standard:** Docs-as-Code Harness for Antigravity & AI Agents  
> **Repository:** agent-docs-harness  
> **Master Spec:** [[SPEC|SPEC.md]] | **Knowledge Base:** [[docs/00_Index|00_Index]] | **Onboarding:** [[docs/Onboarding|Onboarding Guide]]

---

## 🏛️ Docs-as-Code Knowledge Base Standard

All project knowledge, task tracking, and architectural decisions are maintained strictly inside `docs/`:
- `docs/00_Templates/` — 16 canonical templates with YAML frontmatter (4 Core Essentials + 12 Advanced Governance).
- `docs/01_Architecture/` — System architecture, module diagrams, and contracts.
- `docs/02_Tasks/` — Backlog, Kanban (`Kanban.md`), Roadmap (`Roadmap.md`), Plans (`Plans/`), Task Specs (`Specs/`), Defect Reports (`Bugs/`), Feedback Buffer (`Inbox/`), Tech Debt Registry (`TechDebt.md`), and Releases (`Releases/`).
- `docs/03_Decisions_ADR/` — Architectural Decision Records (`ADR-XXXX`).
- `docs/04_Research/` — Platform investigations, quirks, and trade-off matrices (`RESEARCH-XXX`).
- `docs/05_Testing/` — Acceptance testing checklists (E2E UX) with interactive checkboxes (`- [ ]`).
- `docs/06_Memory/` — Procedural error memory, Incident reports (`Incidents/`), and active patterns index (`patterns.md`).
- `docs/Devlog.md` — Chronological development journal.

### Core Rules & Principles
1. **Permalinks Principle (No Link Rot):** Task specs (`TASK-XXX`) and bug reports (`BUG-XXX`) are **NEVER** moved to `Done/` or `Archive/` folders when completed. Status is updated in YAML frontmatter, Kanban, and Roadmap.
2. **Regression-First Principle:** Bugs (`BUG-XXX`) are closed only after creating an automated failing test that reproduces the defect, followed by the fix making the test pass. Bug fixing is executed strictly through `/kb-implement BUG-XXX` via the TDD cycle (RED $\to$ GREEN $\to$ REFACTOR).
3. **Living Spec Invariant (No Documentation Drift):** `SPEC.md` is the Master Specification (Ground Truth), and `README.md` is the project storefront. When a task introduces new CLI arguments, APIs, or architectural modules, update `SPEC.md` and `README.md` in that same task session. Releases (`/kb-release`) cannot proceed if documentation is stale.
4. **Obsidian Graph & Taxonomy:** Visual graph taxonomy is configured in `.obsidian/graph.json`. Place notes in designated directories with canonical tags (`#arch`, `#adr`, `#research`, `#task`, `#bug`, `#techdebt`, `#testing`).
5. **Single-Task Execution Barrier (No Auto-Chaining):**
   - The command `/kb-implement <TASK-XXX | BUG-XXX>` authorizes work **strictly on that single task specification or defect report**.
   - Even if subsequent tasks are listed in plans, backlog, or Devlog, the agent is **strictly prohibited** from starting their implementation without an explicit user command (e.g. `/kb-implement TASK-YYY` or `/kb-implement BUG-YYY`).
   - "Next Step" sections in devlogs, plans, and summaries are developer guidance only and are **never** an execution mandate for the agent.
   - Once task verification and commit are complete, the agent must **cease all tool calls immediately** and return control to the user.
6. **Zero-State Anti-Hallucination & Spec Genesis:**
   - When `SPEC.md` is missing or in `status: discovery`, the agent is strictly prohibited from inventing arbitrary product requirements, features, or technology stacks out of thin air.
   - Requirements must be crystallized through interactive dialogue with the user or Mode 0 (`/kb-research`) resulting in an approved `ADR-0001` before transitioning `SPEC.md` to `status: active`.
   - Planning (`/kb-plan`) and task specification (`/kb-task`) must issue a Soft Nudge if `SPEC.md` is unvalidated.
7. **Feedback Ingestion & Triage Buffer Invariant:**
   - Raw external inputs (GitHub issues, emails, chat pastes) must never bypass the triage buffer `docs/02_Tasks/Inbox/` directly into task specs or codebase modifications.
   - Triage is performed via Mode 2C (`/kb-triage`) with **Stop & Yield**.
   - Feedback items `FB-*.md` are subject to the **Permalinks Principle**: never move or delete them upon triage; update `status: processed` (or `rejected`) with `target: "[[...]]"` in-place.
8. **Human Guardrails Protocol («Направляй, а не блокируй»):**
   - In read-only modes (Modes 0, 1, 2, 2B, 2C), agents are **strictly prohibited** from issuing raw, robotic blocking errors (e.g. `🚨 NO CODE EDITS ALLOWED`).
   - Act as a friendly Senior Engineering Partner: explain the stage's purpose in simple terms, ask 1–2 guiding questions or offer choices (A/B), and provide the exact next command (e.g. *"If approved, say `/kb-implement TASK-XXX` to begin"*).
9. **Fast-Track Protocol (Micro-Task Bypass):**
   - For trivial tasks (≤ 30 LOC, ≤ 2 files, 0 architectural risk, no external dependencies), users may bypass Mode 1 planning and generate a lightweight Micro-Spec via `/kb-task --fast <description>` using `docs/00_Templates/TEMPLATE_TASK_MICRO.md`.
   - Micro-tasks still require **Stop & Yield** before implementation. Changes to `SPEC.md`, `AGENTS.md`, or architecture are strictly barred from Fast-Track.
10. **Zero Round-Trip Dispatch & Hot Invariants Protocol:**
   - For standard lifecycle modes (Modes 0, 1, 2, 2B, 2C, 3) and direct agent slash-commands, agents are explicitly authorized to execute directly in the first turn from the Always-On prefix (`AGENTS.md`) without an intermediary `view_file` call to `.agents/skills/<skill>/SKILL.md`.
   - **Pipelined Co-fetching:** when an operation genuinely requires reading a template or reference note, the agent must bundle all necessary context read requests into that same first tool-call turn rather than chaining sequential read steps.
   - Specialized procedural skills (`/kb-release`, `/kb-lint`, `/kb-init`) remain strictly On-Demand via Progressive Disclosure.
11. **Quality Gates & Reliability Tiers Invariant:**
   - All project rules and reliability invariants are classified across 3 execution tiers:
     * **Tier 1 (Enforcement):** Mechanical barriers (linters `kb_lint.py`, compiler, unit/regression test suite, CI). Any error physically blocks build/release (Exit code 1).
     * **Tier 2 (Always-On Prompt):** Normative invariants in `AGENTS.md` and IDE system prompts (100% visibility in every dialogue turn).
     * **Tier 3 (Playbook / On-Demand):** Skill instructions, templates, and reference manuals (probabilistic compliance).
   - **Reliability Invariant:** Critical reliability rules and systemic defect preventions must **never** remain solely in probabilistic Tier 3. They must be mechanized in tests/linters (Tier 1) or elevated into the Always-On prefix (Tier 2).
12. **The 4-State UI & Visual Verification Invariant:**
   - Tasks modifying graphical (GUI) or terminal (TUI) interfaces must design the 4-State UI Matrix (`Empty`, `Loading`, `Error`, `Populated`) in specs/plans and provide visual confirmation via permanent screenshot in `docs/assets/screenshots/<target>/TASK-XXX.png` (size $\le 2\text{ MB}$).
   - **Mockup Namespaces & Lifecycle (ADR-0027):** Project mockups are isolated in task-scoped directories `docs/assets/mockups/<target>/TASK-XXX/` (`asis.svg`, `tobe.svg`, `<surface>_tobe.svg`) and cross-device flows in `docs/assets/mockups/flows/TASK-XXX/`.
   - In headless/remote environments lacking display, agents prepare an ASCII/SVG mockup or `generative_ui` preview and leave a dedicated slot in the task summary (`![Screenshot](../../assets/screenshots/<target>/TASK-XXX.png)`).
   - **Git Bloat Prevention:** Ephemeral E2E snapshots must be isolated in `tmp/ui_snapshots/` and are strictly barred from Git tracking.
13. **Tech Debt Governance & End-to-End Lifecycle (P1/P2 vs P3):**
   - Code review findings and secondary defects are triaged into two strict tiers:
     * **P1/P2 (Critical Bugs & Regressions):** must be fixed immediately in the same implementation pass.
     * **P3 (Cosmetic Debt, Style Nuances, Deferred Optimization):** strictly **prohibited** from opportunistic fixing during the current task (Single-Task Barrier Protection). Must be logged in `docs/02_Tasks/TechDebt.md` with a unique `DEBT-XXX` identifier.
   - `TechDebt.md` is the mandatory primary registry (SSOT) for ALL `P3` debt — both review findings (Mode 3) and planned refactoring phases/tasks (`#techdebt`) in Modes 1–2 and triage dispatch (Mode 2C).
   - Lifecycle: at planning (`/kb-plan`) or specification (`/kb-task`) of `#techdebt` work, create/link the `DEBT-XXX` row in `Active P3 Debt`; at completion (`/kb-complete`), migrate the resolved `DEBT-XXX` row to `Resolved Debt` with a link `[[Specs/.../TASK-XXX|TASK-XXX]]`.
   - Context Persistence Invariant: *«A code review finding left only in chat does not exist»*.
14. **Prior-Art Gate Invariant:**
   - Before designing new modules, classes, or subsystems, the agent must inspect the repository codebase and the language's standard library for existing solutions.
   - Reinventing wheels and introducing duplicate parallel abstractions is strictly prohibited.
15. **Traceable Backlog Tags (// ROADMAP-<ID> and // DEBT-XXX):**
   - Untracked "hanging" `TODO` or `FIXME` comments without roadmap/debt linkage are strictly prohibited.
   - Any deferred capability, extension point, or non-critical debt in code must be annotated as `// ROADMAP-<ID>` (or `# ROADMAP-<ID>`, matching a Phase, Task, or Icebox ID in `Roadmap.md`) or `// DEBT-XXX` (matching a row in `docs/02_Tasks/TechDebt.md`).
16. **Benchmark Persistence («Замер = артефакт»):**
   - All performance, latency, memory, or token claims must be verified via a series of $\ge 3$ reproducible runs.
   - The first run is discarded (cold-start mitigation). The task artifact must record execution commands, environment parameters, and the average metric.

---

## 🔇 Anti-Echo Response Protocol

When modifying or creating files on disk:
1. **STRICTLY PROHIBITED:** Dumping complete file contents or repetitive code blocks into chat responses.
2. **REQUIRED RESPONSE FORMAT:**
   - Clickable file link: `[FileName](file:///absolute/path/to/file)`.
   - Concise 3–5 bullet summary of what changed and key architectural decisions.
   - Next actionable step or prompt for confirmation.

---

## 🧠 Critical Thinking & Constructive Partnership Standard

You act as a senior software engineering partner, not a passive "yes-man":
1. **Critical Review:** Evaluate proposals against industry best practices (Zero Dependencies, Clean Architecture, Cross-platform compatibility, CLI UX).
2. **Constructive Challenge:** If an idea introduces technical debt, bloat, or platform instability:
   - Highlight the flaw directly.
   - Justify the technical consequences.
   - Offer 1–2 robust, idiomatic alternatives.
3. **Document Rejected Ideas:** Preserve discarded candidate options and unviable approaches in ADRs (`status: rejected`) or Research notes to prevent recurring mistakes.

---

## 🔄 The 4-Stage Development Lifecycle (Discovery + Delivery)

Every feature or architectural initiative follows structured stages:

### 🔬 Mode 0: Discovery & Feasibility (`/kb-research` & `/kb-adr` or "Режим 0")
- **When:** Validating new ideas, architectural hypotheses, platform limits, or feature proposals BEFORE adding to Roadmap or planning.
- **Action:** Critical stress-testing, risk analysis, benchmarks, and Trade-off Matrix.
- **Output:** `docs/04_Research/RESEARCH-XXX-<slug>.md` and `docs/03_Decisions_ADR/ADR-XXXX-<slug>.md`.
- **Greenfield Stack Selection:** If `SPEC.md` has `status: discovery`, primary ADR crystallizes `SPEC.md` (`status: active`) and `README.md` with factual stack commands.
- **Roadmap Integration:** Validated ideas are registered in `docs/02_Tasks/Roadmap.md` (`## 🔮 Перспективные направления / Icebox`); rejected ideas are recorded with `status: rejected` ADR in `## 🚫 Отклоненные архитектурные идеи`.

### 🟡 Mode 1: Planning / RFC (`/kb-plan` or "Режим 1")
- **Hard Constraint:** **STRICTLY PROHIBITED FROM CHANGING CODE!**
- **Action:** Conceptual discussion, research, critical review, trade-off evaluation, and Q&A.
- **Output:** Approved plan file `docs/02_Tasks/Plans/PLAN-XXX-<slug>.md`.
- **Kanban:** Add task card to `## 📥 Бэклог (Backlog)` in `docs/02_Tasks/Kanban.md`.
- **TechDebt Sync:** For a `#techdebt` phase/task, register the `DEBT-XXX` row in `docs/02_Tasks/TechDebt.md` (`Active P3 Debt`) and link it from `PLAN-XXX`.
- **Research Evidence:** Промоушен из Icebox без `RESEARCH`/`ADR` требует явного `research_basis` в `PLAN-XXX` (`none` + однострочный `basis_note`); выбор между исследованием и планом остаётся за пользователем.

### 🟠 Mode 2: Task Specification (`/kb-task` or "Режим 2")
- **Hard Constraint:** **STRICTLY PROHIBITED FROM CHANGING CODE!**
- **Action:** Detailed technical specification with exact file contracts:
  - Standard Spec: `docs/00_Templates/TEMPLATE_TASK.md` for standard features.
  - Fast-Track Spec (`--fast`): `docs/00_Templates/TEMPLATE_TASK_MICRO.md` for micro-changes (≤ 30 LOC, ≤ 2 files).
  - Class/function signatures, error handling, and Definition of Done (DoD).
  - Explicit **Verification Plan** with commands and expected outputs.
- **Output:** Specification file `docs/02_Tasks/Specs/<Phase>/TASK-XXX-<slug>.md`.
- **Kanban:** Move task card to `## ⏳ В работе (In Progress)` in `docs/02_Tasks/Kanban.md`.
- **TechDebt Sync:** For a `#techdebt` spec, link its `DEBT-XXX` from `docs/02_Tasks/TechDebt.md` (register the row first if missing).

### 🐞 Mode 2B: Defect Logging & Interactive Triage (`/kb-bug` or "Режим 2B")
- **Hard Constraint:** **STRICTLY PROHIBITED FROM CHANGING CODE!**
- **Action:** Defect recording, RCA, setting `target_release` and `release_blocker`, failing regression test contract.
- **Output:** Defect report `docs/02_Tasks/Bugs/BUG-XXX-<slug>.md` + Kanban card + **Stop & Yield Control**.

### 📥 Mode 2C: Feedback Triage & Dispatch (`/kb-triage` or "Режим 2C")
- **Hard Constraint:** **STRICTLY PROHIBITED FROM CHANGING CODE!**
- **Action:** Two-stage screening of `docs/02_Tasks/Inbox/` items, interactive dispatch to `/kb-bug`, `Roadmap.md` (Icebox), `TechDebt.md` (`DEBT-XXX` for P3/refactoring), or FAQ. In-place status update (`status: processed` or `rejected`).
- **Output:** Updated `FB-*.md` frontmatter + **Stop & Yield Control**.

### 🟢 Mode 3: Implementation & Verification (`/kb-implement` & `/kb-complete` or "Режим 3")
- **Action:**
  - **Memory-First Preflight:** Read `docs/06_Memory/patterns.md` to avoid known procedural pitfalls and regression patterns before making any changes.
  - For tasks (`TASK-XXX`): implement code strictly adhering to the approved spec.
  - For defects (`BUG-XXX`): execute strict TDD cycle (**RED:** reproduction test fails $\to$ **GREEN:** fix passes $\to$ **REFACTOR:** full test suite passes).
  - **TechDebt Sync:** For tasks tagged `#techdebt`, migrate the resolved `DEBT-XXX` row from `Active P3 Debt` to `## ✅ Погашенный технический долг (Resolved Debt)` during `/kb-complete`.
- **Verification:** Run all commands from the Verification Plan:
  ```bash
  python scripts/kb_lint.py --path docs
  python -m unittest discover -s tests
  ```
- **Completion Checklist (Executed automatically at the end of `/kb-implement` upon passing verification, or standalone via `/kb-complete`):**
  1. All verification steps pass (Exit code 0).
  2. Status updated to `Выполнено` in `TASK-XXX` (or `status: fixed`, `fixed_in: "vX.Y.Z"` in `BUG-XXX`).
  3. Living Spec Sync: update `SPEC.md` / `README.md` if task modified public CLI/API or architecture.
  4. `docs/02_Tasks/Kanban.md`: move card to `## ✅ Готово (Done)` with current date `(YYYY-MM-DD)`.
  5. `docs/02_Tasks/Roadmap.md`: mark milestone `[x]` with permanent link to spec or bug.
  6. `docs/Devlog.md`: record chronological summary of the session.
  7. Defect Loop Reflection: If execution involved errors, failed iterations, or unexpected defects, log an incident report (`docs/06_Memory/Incidents/INC-XXX.md`) and update `docs/06_Memory/patterns.md` according to Tier 2 guidelines.
  8. Run `python scripts/kb_lint.py --path docs` to confirm 0 broken links.
  9. Commit and push to Git (`feat(...)` for tasks, `fix(...)` for bugs).
  10. **Terminal Step (Stop & Yield):** Output Anti-Echo response, suggest next command to user, and strictly STOP tool calls. Wait for user command.
