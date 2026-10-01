---
name: docs-as-code
description: "Docs-as-Code hub: workspace rules, 3-mode workflow, and artifact standards."
---

# Docs-as-Code Hub

Central router for Docs-as-Code infrastructure. Enforces the 3-mode workflow and directory layout. Detailed rules reside in `AGENTS.md`.

## 🧭 Command Router

| Trigger | Mode | Function | Skill |
| :--- | :--- | :--- | :--- |
| `/kb-init` | Init | Scaffold `docs/`, 13 templates, Obsidian graph | `kb-init` |
| `/kb-onboard` | Help | Developer and agent onboarding cheatsheet | `kb-onboard` |
| `/kb-plan` | Mode 1 | RFC discussion, PLAN-XXX. **No code.** | `kb-plan` |
| `/kb-task` | Mode 2 | Spec TASK-XXX with contracts and DoD. **No code.** | `kb-task` |
| `/kb-implement`| Mode 3 | Implement code strictly adhering to TASK-XXX | `kb-implement` |
| `/kb-complete` | Mode 3 | Mark Done in Kanban/Roadmap, Devlog, git sync | `kb-complete` |
| `/kb-release`  | Release | Dual-Mode release, SHA-256, git tag | `kb-release` |
| `/kb-bug` | Defect | Log BUG-XXX with RCA and regression test | `kb-bug` |
| `/kb-adr` | Decision | ADR-XXXX record with rejected options | `kb-adr` |
| `/kb-research` | Research | RESEARCH-XXX note with benchmarks | `kb-research` |
| `/kb-lint` | Audit | Verify wikilinks and YAML integrity | `kb-lint` |

## 🏛️ Directory Layout (`docs/`)

```text
docs/
├── .obsidian/graph.json   # Graph view palette
├── 00_Index.md            # Map of Content (entry point)
├── 00_Templates/          # 13 skeleton templates
├── 01_Architecture/       # System diagrams & contracts
├── 02_Tasks/              # Kanban, Roadmap, Plans/, Specs/, Bugs/, Releases/
├── 03_Decisions_ADR/      # ADR-XXXX records
├── 04_Research/           # RESEARCH-XXX investigations
├── 05_Testing/            # Acceptance testing checklists
├── Devlog.md              # Chronological dev journal
└── Onboarding.md          # Onboarding guide
```

## 🚨 Invariants
* **Permalinks:** Specs, plans, and bugs are never moved or renamed when closed.
* **Regression-First:** Bugs are closed only after automated test passes.
* **Anti-Echo:** Do not dump file bodies in chat; provide link + 3–5 bullet summary.
* **SSOT:** Behavioral invariants are defined in `AGENTS.md`.
