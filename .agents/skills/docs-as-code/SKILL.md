---
name: docs-as-code
description: "Docs-as-Code hub: workspace rules, 4-stage lifecycle, and artifact standards."
---

# Docs-as-Code Hub

Central router for Docs-as-Code infrastructure. Enforces the 4-stage lifecycle (Discovery + Delivery) and directory layout. Detailed rules reside in `AGENTS.md`.

## 🧭 Command Router

| Trigger | Mode | Function | Skill |
| :--- | :--- | :--- | :--- |
| `/kb-init` | Init | Scaffold `docs/`, 13 templates, Obsidian graph | `kb-init` |
| `/kb-onboard` | Help | Developer and agent onboarding cheatsheet | `kb-onboard` |
| `/kb-research` | Mode 0 | Discovery & feasibility (RESEARCH-XXX, Icebox sync) | `kb-research` |
| `/kb-adr` | Mode 0 / ADR | ADR-XXXX record with rejected options | `kb-adr` |
| `/kb-plan` | Mode 1 | RFC discussion, PLAN-XXX. **No code.** | `kb-plan` |
| `/kb-task` | Mode 2 | Spec TASK-XXX with contracts and DoD. **No code.** | `kb-task` |
| `/kb-implement`| Mode 3 | Implement TASK-XXX with auto-complete | `kb-implement` |
| `/kb-complete` | Mode 3 | Standalone sync: Done, Devlog, git | `kb-complete` |
| `/kb-release`  | Release | Dual-Mode release, SHA-256, git tag | `kb-release` |
| `/kb-bug` | Defect | Log BUG-XXX with RCA and regression test | `kb-bug` |
| `/kb-lint` | Audit | Verify wikilinks and YAML integrity | `kb-lint` |

## 🏛️ Directory Layout (`docs/`)
`00_Templates/` (13 templates), `01_Architecture/`, `02_Tasks/` (Kanban, Roadmap, Plans, Specs, Bugs, Releases), `03_Decisions_ADR/`, `04_Research/`, `05_Testing/`, `Devlog.md`, `Onboarding.md`.

## 🚨 Invariants
* **Permalinks:** Specs, plans, and bugs are never moved or renamed when closed.
* **Regression-First:** Bugs are closed only after automated test passes.
* **Anti-Echo:** Link + 3–5 bullet summary instead of dumping file contents.
* **SSOT:** Behavioral rules are defined in `AGENTS.md`.
