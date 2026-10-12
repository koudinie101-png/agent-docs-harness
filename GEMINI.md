# GEMINI.md -- Google Antigravity & Gemini CLI Rules for agent-docs-harness

> **Stack:** Python (Standard / Pytest / FastAPI) | **Language:** Russian (docs), English (code)
> **Canonical Standard (SSOT):** [[AGENTS.md]] | **KB Index:** [[docs/00_Index|00_Index]]

## ⚡ Stack Verification Commands
- **Build:** `python -m py_compile scripts/*.py`
- **Test:** `pytest`
- **Lint:** `python3 scripts/kb_lint.py --path docs`

## 🛡️ Operating Rules & Routing
1. **Single Source of Truth & Zero Round-Trip:** Read `AGENTS.md` at session start. For Modes 0-3, execute directly from hot prefix without reading SKILL.md; co-fetch context in parallel.
2. **Read-Only Invariant & Human Guardrails:** Modes 1 (`/kb-plan`), 2 (`/kb-task`), 2B (`/kb-bug`), 2C (`/kb-triage`): STRICTLY NO CODE CHANGES. Guide user with friendly next steps rather than blocking errors.
3. **Fast-Track Protocol:** Micro-tasks (≤ 30 LOC, ≤ 2 files) bypass Mode 1 planning via `/kb-task --fast` using Micro-Spec.
4. **Mode 3 Implementation:** `/kb-implement <TASK-XXX | BUG-XXX>` authorizes work strictly on ONE target. Execute TDD for bugs (RED -> GREEN -> REFACTOR). Run verification commands before completion.
5. **Anti-Echo & Single-Task Barrier:** Never reprint full files in chat responses. Stop tool calls upon task completion (Stop & Yield).
6. **Quality Gates:** Tier 1 (Enforce: tests/lint) > Tier 2 (Always-On: AGENTS.md) > Tier 3 (Playbook: skills). Never rely on Tier 3 for critical rules.

Skills: `/kb-plan` `/kb-task` `/kb-implement` `/kb-complete` `/kb-bug` `/kb-triage` `/kb-adr` `/kb-research` `/kb-release` `/kb-lint`
