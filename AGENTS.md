# 🤖 AGENTS.md — AI Agent Guidelines & Operating Modes

> **Standard:** Docs-as-Code Harness for Antigravity & AI Agents  
> **Repository:** agent-docs-harness  
> **Master Spec:** [[SPEC|SPEC.md]] | **Knowledge Base:** [[docs/00_Index|00_Index]] | **Onboarding:** [[docs/Onboarding|Onboarding Guide]]

---

## 🏛️ Docs-as-Code Knowledge Base Standard

All project knowledge, task tracking, and architectural decisions are maintained strictly inside `docs/`:
- `docs/00_Templates/` — 12 canonical templates with YAML frontmatter.
- `docs/01_Architecture/` — System architecture, module diagrams, and contracts.
- `docs/02_Tasks/` — Backlog, Kanban (`Kanban.md`), Roadmap (`Roadmap.md`), Plans (`Plans/`), Task Specs (`Specs/`), and Defect Reports (`Bugs/`).
- `docs/03_Decisions_ADR/` — Architectural Decision Records (`ADR-XXXX`).
- `docs/04_Research/` — Platform investigations, quirks, and trade-off matrices (`RESEARCH-XXX`).
- `docs/05_Testing/` — Acceptance testing checklists (E2E UX) with interactive checkboxes (`- [ ]`).
- `docs/Devlog.md` — Chronological development journal.

### Core Rules & Principles
1. **Permalinks Principle (No Link Rot):** Task specs (`TASK-XXX`) and bug reports (`BUG-XXX`) are **NEVER** moved to `Done/` or `Archive/` folders when completed. Status is updated in YAML frontmatter, Kanban, and Roadmap.
2. **Regression-First Principle:** Bugs (`BUG-XXX`) are closed only after creating an automated failing test that reproduces the defect, followed by the fix making the test pass.
3. **Graph Visual Color Scheme & Tagging:** Preserved in `.obsidian/graph.json`:
   | Color / Category | Obsidian Path / Query | Tags | Description |
   | :--- | :--- | :--- | :--- |
   | ⚪ White / Light | `file:00_Index`, `file:Devlog`, `file:SPEC` | — | Entry points & root navigation hubs |
   | 🟣 Purple | `path:01_Architecture` | `#arch` | System architecture, contracts & modules |
   | 🔵 Blue / Cyan | `path:03_Decisions_ADR` | `#adr` | Architecture Decision Records |
   | 🟡 Yellow / Amber | `path:04_Research` | `#research` | Platform research, benchmarks & quirks |
   | 🟠 Orange | `path:02_Tasks` | `#task` | Backlog, Roadmap, Plans & Task Specs |
   | 🔴 Red | `path:02_Tasks/Bugs` | `#bug` | Defects, bugs, RCA & regression tests |
   | 🟢 Green | `path:05_Testing` | `#testing` | Acceptance testing & E2E UX checklists |

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

## 🔄 The 3-Mode Development Cycle

Every non-trivial task or feature strictly follows three sequential modes:

### 🟡 Mode 1: Planning / RFC (`/kb-plan` or "Режим 1")
- **Hard Constraint:** **STRICTLY PROHIBITED FROM CHANGING CODE!**
- **Action:** Conceptual discussion, research, critical review, trade-off evaluation, and Q&A.
- **Output:** Approved plan file `docs/02_Tasks/Plans/PLAN-XXX-<slug>.md`.
- **Kanban:** Add task card to `## 📥 Бэклог (Backlog)` in `docs/02_Tasks/Kanban.md`.

### 🟠 Mode 2: Task Specification (`/kb-task` or "Режим 2")
- **Hard Constraint:** **STRICTLY PROHIBITED FROM CHANGING CODE!**
- **Action:** Detailed technical specification with exact file contracts:
  - `[NEW] path/to/file`
  - `[MODIFY] path/to/file`
  - `[DELETE] path/to/file`
  - Class/function signatures, error handling, and Definition of Done (DoD).
  - Explicit **Verification Plan** with commands and expected outputs.
- **Output:** Specification file `docs/02_Tasks/Specs/<Phase>/TASK-XXX-<slug>.md`.
- **Kanban:** Move task card to `## ⏳ В работе (In Progress)` in `docs/02_Tasks/Kanban.md`.

### 🟢 Mode 3: Implementation & Verification (`/kb-implement` & `/kb-complete` or "Режим 3")
- **Action:** Implement code strictly adhering to the approved `TASK-XXX` spec.
- **Verification:** Run all commands from the Verification Plan:
  ```bash
  python scripts/kb_lint.py --path docs
  python -m unittest discover -s tests
  ```
- **Completion Checklist (Executed automatically at the end of `/kb-implement` upon passing verification, or standalone via `/kb-complete`):**
  1. All verification steps pass (Exit code 0).
  2. Spec status updated to `Выполнено` in `TASK-XXX`.
  3. `docs/02_Tasks/Kanban.md`: move card to `## ✅ Готово (Done)` with current date `(YYYY-MM-DD)`.
  4. `docs/02_Tasks/Roadmap.md`: mark milestone `[x]` with permanent link to spec.
  5. `docs/Devlog.md`: record chronological summary of the session.
  6. Run `python scripts/kb_lint.py --path docs` to confirm 0 broken links.
  7. Commit and push to Git.
