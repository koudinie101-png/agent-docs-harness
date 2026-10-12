---
name: kb-onboard
description: "Display developer onboarding guide, 4-stage lifecycle cheatsheet, and quick start."
---

# /kb-onboard — Developer & Agent Onboarding

Use when the user runs `/kb-onboard` or asks how to interact with the project and knowledge base.

## 🧭 Command Router

| Trigger | Mode | Function | Skill |
| :--- | :--- | :--- | :--- |
| `/kb-init` | Init | Scaffold `docs/`, 14 templates, Obsidian graph | `kb-init` |
| `/kb-onboard` | Help | Developer and agent onboarding cheatsheet | `kb-onboard` |
| `/kb-research` | Mode 0 | Discovery & feasibility (RESEARCH-XXX, Icebox sync) | `kb-research` |
| `/kb-adr` | Mode 0 / ADR | ADR-XXXX record with rejected options | `kb-adr` |
| `/kb-plan` | Mode 1 | RFC discussion, PLAN-XXX. **No code.** | `kb-plan` |
| `/kb-task` | Mode 2 | Spec TASK-XXX with contracts and DoD. **No code.** | `kb-task` |
| `/kb-bug` | Mode 2B | Triage defect BUG-XXX with RCA. **No code.** | `kb-bug` |
| `/kb-triage` | Mode 2C | Ingestion triage from `docs/02_Tasks/Inbox/`. **No code.** | `kb-triage` |
| `/kb-implement`| Mode 3 | Implement TASK-XXX or resolve BUG-XXX with auto-complete | `kb-implement` |
| `/kb-complete` | Mode 3 | Standalone sync: Done, Devlog, git | `kb-complete` |
| `/kb-release`  | Release | Dual-Mode release, SHA-256, git tag | `kb-release` |
| `/kb-lint` | Audit | Verify wikilinks and YAML integrity | `kb-lint` |

## 🏛️ Directory Layout (`docs/`)
`00_Templates/` (14 templates: 4 Core, 10 Advanced), `01_Architecture/`, `02_Tasks/` (Kanban, Roadmap, Plans, Specs, Bugs, Inbox, Releases), `03_Decisions_ADR/`, `04_Research/`, `05_Testing/`, `Devlog.md`, `Onboarding.md`.

## 🚨 Invariants
* **Permalinks:** Specs, plans, bugs, and feedback are never moved or renamed when closed.
* **Regression-First:** Bugs (`BUG-XXX`) closed strictly after automated failing test reproduces defect and passes.
* **Anti-Echo:** Link + 3–5 bullet summary instead of dumping full file bodies into chat.
* **Single-Task Barrier:** `/kb-implement` executes exactly one spec; never auto-chain.
* **SSOT:** Behavioral standards are defined in `AGENTS.md`.

## Procedure
1. **Present Onboarding Cheatsheet:** Display `/kb-*` command router and 4-stage lifecycle (Discovery $\to$ Planning $\to$ Spec $\to$ Verification/TDD $\to$ Release $\to$ Ingestion).
2. **Review Core Invariants:** Permalinks, Regression-First, Anti-Echo, Single-Task Barrier, Living Spec, Human Guardrails.
3. **Mentor Mode (Beginners & Vibe Coders):** If user requests plain-language guidance or is new to coding, explain steps via everyday analogies and suggest reading `docs/Zero_To_Hero_Guide.md` («Вайбкодинг со страховкой»).
4. **Reference Full Guides:** Direct developer to `docs/Zero_To_Hero_Guide.md`, `docs/Onboarding.md`, and `docs/00_Index.md`.
