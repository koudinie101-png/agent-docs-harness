# 🚀 Agent Docs-as-Code Harness

> **Autonomous, zero-dependency toolkit for bringing engineering discipline, Docs-as-Code knowledge vaults, and strict 4-stage AI agent guardrails to any software project.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-success.svg)](#-zero-external-dependencies)
[![Obsidian Ready](https://img.shields.io/badge/Obsidian-Vault%20Ready-purple.svg)](https://obsidian.md/)

---

## 🎯 The Problem: Why AI Agents Fail in Real Projects

When developing with modern AI coding agents (**Google Antigravity, VS Code Cline, Roo Code, Claude Code, Cursor, GitHub Copilot, Windsurf**), developers consistently hit four roadblocks:

1. 🧠 **"Context Amnesia":** After 15–20 chat turns, the model forgets constraints, platform quirks, and previous architectural decisions.
2. 🔨 **"Wild Code Breaking":** Without strict guardrails, agents immediately rush to edit existing files, inventing suboptimal patterns, breaking public interfaces, and introducing subtle regressions.
3. 🕸️ **"Architecture Drift & Link Rot":** Project notes, plans, and task lists get scattered, outdated, and broken, leading to lost time and confusion.
4. 💸 **"Token Bloat & Echo Chatter":** Agents wastefully dump full code dumps and verbatim file copies into the prompt, exhausting context windows and driving up costs.

---

## 💡 The Solution: Docs-as-Code + 4-Stage Lifecycle (Discovery + Delivery)

**Agent Docs-as-Code Harness** turns your project repository into a self-documenting, disciplined environment that guides AI agents like a senior software engineering partner:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   4 OPERATING MODES                                    │
├────────────────────┬────────────────────┬─────────────────────────────┬────────────────┤
│ 🔬 Mode 0: Research│ 🟡 Mode 1: Plan    │ 🟠 Mode 2: Specification    │ 🟢 Mode 3: Code│
│ (/kb-research)     │ (/kb-plan)         │ (/kb-task)                  │ (/kb-implement)│
│                    │                    │                             │                │
│ • Idea validation  │ • Conceptual RFC   │ • File contracts:           │ • Strict coding│
│ • Trade-off matrix │ • Critical review  │   [NEW] / [MODIFY]          │ • Run tests    │
│ • Icebox / Reject  │ • Risk analysis    │ • Definition of Done (DoD)  │ • Living Spec  │
│ • Stack selection  │ • PLAN-XXX file    │ • Verification commands     │ • Devlog/Kanban│
│ 🚨 NO CODE EDITS!  │ 🚨 NO CODE EDITS!  │ 🚨 NO CODE EDITS!           │ • kb_lint.py   │
└────────────────────┴────────────────────┴─────────────────────────────┴────────────────┘
```

---

## ⚡ Quick Start: 1-Line Installation

Deploy the complete harness into your current project in **one command**:

### Linux & macOS
```bash
curl -sSL https://raw.githubusercontent.com/koudinie101-png/agent-docs-harness/main/install.py | python3
```

### Windows (PowerShell)
```powershell
irm https://raw.githubusercontent.com/koudinie101-png/agent-docs-harness/main/install.py | python3 -
```

### Local / Cloned Usage
```bash
git clone https://github.com/koudinie101-png/agent-docs-harness.git
python3 agent-docs-harness/install.py
```

### 💡 Greenfield Idea-First (Start from a Raw Idea)
Start in an empty folder with just your product concept:
```bash
python3 install.py --idea "AI-powered personal finance assistant"
```
Initializes with the `undecided` preset, generates `SPEC.md` in `status: discovery`, and prepares your AI Agent to conduct tech stack research via `/kb-research` (Mode 0: Discovery). The harness enforces the **Spec Genesis Protocol** with three maturity stages:
* **Missing (Zero-State):** `SPEC.md` is absent; agents are barred from inventing architectures out of thin air.
* **Discovery (Stub):** `SPEC.md` contains raw ideas; agents guide tech stack validation via Mode 0 (`/kb-research`).
* **Active (Ground Truth):** Architectural stack is crystallized through `ADR-0001`, enabling full planning and implementation.

The installer features an **interactive terminal wizard** that asks for your project name, stack, and agent environment, or can be run completely hands-free with CLI flags!

### 💬 Быстрый старт прямо из чата (One-Prompt Quickstart)
Вам даже не нужно открывать терминал! Если вы используете AI-редактор или чат-агент (VS Code Cline/Roo, Cursor, Windsurf, Claude Code, Antigravity), скопируйте и отправьте этот один промпт в окно чата:

> *«Инициализируй в этом проекте harness Docs-as-Code и покажи мне гайд по безопасной разработке».*

Агент самостоятельно скачает установщик, развернет базу знаний и откроет интерактивное руководство `docs/Zero_To_Hero_Guide.md`.

---

## 📦 What Gets Installed in Your Project?

### 1. The Standard `docs/` Knowledge Base (Obsidian Vault)
```text
docs/
├── .obsidian/
│   └── graph.json            # 7-color category palette for Obsidian Graph
├── 00_Index.md               # Map of Content (MOC) entry point
├── Zero_To_Hero_Guide.md     # Interactive visual guide for developers and vibe coders
├── 00_Templates/             # 16 canonical templates with YAML frontmatter
│   ├── TEMPLATE_TASK.md      # Engineering task spec with file contracts
│   ├── TEMPLATE_TASK_MICRO.md# Fast-Track micro-task spec (≤ 30 LOC, ≤ 2 files)
│   ├── TEMPLATE_PLAN.md      # RFC & conceptual feature plan (Mode 1)
│   ├── TEMPLATE_BUG.md       # Defect report with RCA & Regression-First test
│   ├── TEMPLATE_ADR.md       # Architecture Decision Record (+ rejected alternatives)
│   ├── TEMPLATE_RESEARCH.md  # OS quirks, battery/memory limits, trade-off matrix
│   ├── TEMPLATE_TEST.md      # E2E UX acceptance test checklist
│   ├── TEMPLATE_RELEASE.md   # Phased release note with SHA-256 artifact table
│   ├── TEMPLATE_FEEDBACK.md  # Raw feedback item (FB-XXX) with signal metadata
│   ├── TEMPLATE_INCIDENT.md  # Incident report for procedural memory (INC-XXX)
│   ├── TEMPLATE_ARCHITECTURE.md
│   ├── TEMPLATE_ONBOARDING.md
│   ├── TEMPLATE_KANBAN.md
│   ├── TEMPLATE_ROADMAP.md
│   ├── TEMPLATE_DEVLOG.md
│   └── TEMPLATE_INDEX.md
├── Onboarding.md             # Developer & AI Agent onboarding guide
├── Devlog.md                 # Chronological development journal
├── 01_Architecture/          # Component diagrams, data flows, contracts
├── 02_Tasks/
│   ├── Kanban.md             # Operational board (Backlog, In Progress, Done, Ideas)
│   ├── Roadmap.md            # Strategic milestones and phased goals
│   ├── Inbox/                # External feedback triage buffer (.inbox_state.json)
│   ├── Plans/                # RFCs (Mode 1)
│   ├── Specs/01_MVP/         # Detailed task specifications (Mode 2)
│   ├── Bugs/                 # Bug tracker with RCA
│   └── Releases/             # Phased release notes & checksum tables
├── 03_Decisions_ADR/         # Accepted & Rejected Architectural Decisions
├── 04_Research/              # Platform quirks and investigation notes
├── 05_Testing/               # E2E acceptance test scenarios
└── 06_Memory/                # Agent procedural memory: patterns.md & Incidents/
```

### 2. 12 Executable AI Agent Skills (`.agents/skills/`)
The harness bundles and automatically deploys 12 canonical AI agent skills into `.agents/skills/`:

| Slash Command / Skill | Mode / Category | Purpose & Guardrails |
| :--- | :--- | :--- |
| **`/kb-plan`** | 🟡 Mode 1 (RFC) | Conceptual discussion, trade-off analysis, user confirmation. **🚨 STRICTLY NO CODE EDITS!** |
| **`/kb-task`** | 🟠 Mode 2 (Spec) | Detailed file contracts (`[NEW]`/`[MODIFY]`/`[DELETE]`), DoD, verification plan. **🚨 NO CODE EDITS!** |
| **`/kb-implement`** | 🟢 Mode 3 (Code) | Strict execution of ONE task spec (TASK-XXX) or defect fix (BUG-XXX via TDD), verification, auto-completion, and Stop & Yield Control. |
| **`/kb-complete`** | 🟢 Mode 3 (DoD) | Updates spec to `done` (or bug to `fixed`), moves Kanban card (with date), checks Roadmap, appends Devlog, verifies with `kb_lint.py`. |
| **`/kb-release`** | 🚀 Release Mgmt | Pre-flight checks, build hook execution to `dist/`, SHA-256 calculation, `RELEASE-vX.Y.Z.md` notes, defect release targeting, blocker validation, Roadmap sync, Dual-Mode publishing (GitHub / Local-Only). |
| **`/kb-bug`** | 🐞 Mode 2B (Triage) | Isolated defect logging, root cause analysis (RCA), release targeting & blocker triage. **🚨 STRICTLY NO CODE EDITS!** Enforces Stop & Yield Control. |
| **`/kb-triage`** | 📥 Mode 2C (Triage) | Two-stage screening of `docs/02_Tasks/Inbox/` items, dispatch to `/kb-bug`, Roadmap (Icebox), or FAQ with in-place status updates. **🚨 STRICTLY NO CODE EDITS!** Enforces Stop & Yield Control. |
| **`/kb-adr`** | Architecture | Records Architectural Decisions including **explicitly rejected alternatives** (`status: rejected`) to prevent anti-patterns. |
| **`/kb-research`** | Platform Research | Documents OS quirks, worst-case stress tests, thread safety, memory limits, and discarded prototypes. |
| **`/kb-lint`** | Health Audit | Scans internal wikilinks, YAML frontmatter, detects link rot, and ensures knowledge base consistency. |
| **`/kb-onboard`** | Developer Guide & Hub | Displays onboarding cheatsheet, 4-stage lifecycle, command router, directory layout, and core disciplines. |
| **`/kb-init`** | Initialization | Deploys standard Docs-as-Code folder tree, template suite (Core Essentials vs Advanced Governance), and Obsidian graph. |

### 3. Autonomous Knowledge Base Linter, Release & Ingest Utilities (`scripts/`)
* **Zero external dependencies** (standard Python 3 stdlib only).
* **Linter (`scripts/kb_lint.py`):** Scans all markdown documents, cross-validates internal wiki-style links, verifies YAML frontmatter (tasks, bugs, ADRs, feedback items), and detects link rot instantly:
  ```bash
  python3 scripts/kb_lint.py --path docs
  ```
* **Release Manager (`scripts/kb_release.py`):** Inspects `dist/` directory, computes streaming SHA-256 checksums, extracts phase tasks/bugs/ADRs from knowledge base, and writes canonical release notes:
  ```bash
  python3 scripts/kb_release.py --version v1.0.0 --phase 1
  ```
* **Feedback Ingest Utility (`scripts/kb_ingest.py`):** Ingests signals from GitHub Issues, Email/IMAP, or raw clipboard paste into `docs/02_Tasks/Inbox/FB-*.md` with zero-deps Git remote auto-detection, channel status dashboard, and state deduplication:
  ```bash
  # Diagnostic status dashboard & API quota check
  python3 scripts/kb_ingest.py --status

  # Ingest issues with auto-detected remote or custom filters
  python3 scripts/kb_ingest.py --github --label needs-triage
  # Quick paste feedback from clipboard or arguments
  python3 scripts/kb_ingest.py --paste "App crashes when clicking save"
  ```

### 4. Agent Configuration & Rule Files (Thin Forwarders Pattern)
Depending on your preference, the installer configures:
* **`AGENTS.md`** — Universal root standard (Single Source of Truth) governing all 4 operating modes, skills, and disciplines.
* **Thin Forwarder Adapters ($\le 25$ lines, -80% token bloat):**
  * **`GEMINI.md`** — Google Antigravity & Gemini CLI integration.
  * **`.windsurfrules`** — Windsurf Cascade IDE rules.
  * **`.clinerules`** — VS Code Cline & Roo Code integration.
  * **`CLAUDE.md`** — Claude Code CLI in terminal.
  * **`.cursorrules`** — Cursor IDE rules.
  * **`.github/copilot-instructions.md`** — GitHub Copilot chat & completions.
  * *Each adapter links directly to `AGENTS.md` as SSOT, specifies stack verification commands (`Build`, `Test`, `Lint`), and enforces core Read-Only & TDD invariants without double prompt injection.*

---

## 🌐 Documentation Language Support (`--doc-lang`)

The harness supports bilingual development environments out of the box:
* **`--doc-lang ru` (Default):** Documentation, planning (`/kb-plan`), specs (`/kb-task`), and Devlog entries are maintained in Russian. Source code, types, and git commits remain strictly in English.
* **`--doc-lang en`:** All documentation, planning, and agent communications are in English.
* Custom languages can be selected via the interactive wizard.

---

## 🧠 Open Models & Enterprise Privacy (Qwen 2.5 Coder & DeepSeek)

Through platform research ([RESEARCH-001](docs/04_Research/RESEARCH-001-ai-agent-ecosystem-and-ide-matrix.md)), this harness is proven to be exceptionally effective with open-weights models:
* **Qwen 2.5 Coder (32B / 14B / 7B):** Run completely offline via Ollama, LM Studio, or vLLM. The strict 4-stage boundaries and structured templates eliminate context hallucinations and keep open models focused on clean, modular code.
* **DeepSeek R1 / V3:** Ideal for Mode 1 conceptual planning, mathematical verification, and architectural trade-off analysis.

---

## 🎨 Obsidian Graph Integration (7 Color Groups)

Open the `docs/` folder in [Obsidian](https://obsidian.md/) to see your architecture visualized:

| Color | Node Type | Purpose |
| :--- | :--- | :--- |
| ⚪ **White / Silver** | Hubs & Indices | `00_Index`, `Devlog`, `SPEC`, `Onboarding` |
| 🟣 **Purple** | Architecture | `01_Architecture/` subcomponents & data schemas |
| 🔵 **Cyan / Blue** | ADRs | `03_Decisions_ADR/` architectural decisions |
| 🟡 **Yellow / Amber** | Research | `04_Research/` platform quirks, memory/battery limits |
| 🟠 **Orange** | Tasks & Plans | `02_Tasks/` plans, specifications, Kanban, Roadmap |
| 🔴 **Red** | Defects & Bugs | `02_Tasks/Bugs/` defect reports with root cause analysis |
| 🟢 **Green** | Testing & QA | `05_Testing/` acceptance testing scenarios |

---

## 🛠️ Supported Technology Stacks

The installer tailors templates, build commands, and agent prompts to your stack:

| Stack | Identifier | Target Ecosystem & Tailored Guardrails |
| :--- | :--- | :--- |
| **Apple Swift** | `swift` | **iOS, macOS, SwiftUI, Xcode**: ARC memory management, Swift Concurrency (`@MainActor`, `Sendable`), BackgroundTasks framework, Keychain. |
| **Web / Fullstack** | `ts` | **TypeScript, JavaScript, Next.js, Node**: async event loop, memory leaks, SSR hydration, bundling. |
| **Python** | `python` | **Pytest, FastAPI, CLI**: type hinting, asyncio, packaging, cross-platform UTF-8. |
| **.NET / C#** | `dotnet` | **ASP.NET, MAUI, CoreCLR**: async/await, IDisposable, LOH allocations. |
| **Generic** | `generic` | Universal templates for any language or toolchain. |
| **Undecided / Idea-First** | `undecided` | **Research & Discovery**: Stack postponed to Mode 0 (`/kb-research`). Creates `SPEC.md` in `status: discovery`. |

---

## 💻 CLI Options & Non-Interactive Usage

```bash
# Greenfield installation starting from a raw verbal idea:
python3 install.py --idea "AI note taking service"

# Non-interactive installation with autodetection, all agent rules, and GitHub Actions CI:
python3 install.py --non-interactive --name "MySwiftApp" --stack auto --agent all --ci github --git local

# Safe update of harness components (templates, linter, skills, graph) in existing project:
python3 install.py --update

# Generate anonymized environment diagnostic report:
python3 install.py --report

# CLI Options summary:
python3 install.py --help
  --name, -n        Project name (default: directory name)
  --stack, -s       {auto, swift, ts, python, dotnet, generic, undecided} (default: auto)
  --idea, -i        Verbal product idea prompt for Greenfield initialization (undecided preset)
  --agent, -a       {all, cline, claude, cursor, copilot, gemini, windsurf, generic}
  --doc-lang, -l    {ru, en, custom} (default: ru)
  --git, -g         {local, github, none} (default: local)
  --ci              {github, none} Continuous Integration workflow (default: none)
  --target-dir, -d  Destination directory (default: .)
  --non-interactive Run without interactive prompts (-y, --yes)
  --force, -f       Overwrite configurations if present
  --update, -u      Safely update harness infrastructure preserving user tasks & notes
  --report, -r      Generate anonymized Markdown diagnostic report of local environment
```

### 🩺 Offline Diagnostic Report (`install.py --report`)
Generates an anonymized diagnostic report covering OS/Platform, Python runtime, Git status, knowledge base health (`kb_lint.py`), and detected AI agent configs. Sensitive user home directory paths are sanitized to `<user>`.

### 📥 Feedback Ingestion & Triage Buffer (`/kb-triage`, `scripts/kb_ingest.py`)
Isolates external feedback in `docs/02_Tasks/Inbox/` before converting to tasks or code:
* **`scripts/kb_ingest.py`**: Auto-detects GitHub repository remote from `git config`, fetches issues via GitHub API (with `--status` dashboard, `--label`, and `--all-open` filters), parses IMAP feedback, or ingests pasted text with state tracking in `.inbox_state.json`.
* **`/kb-triage` (Mode 2C)**: Interactive two-stage screening (Noise vs Signal) and dispatch to `/kb-bug`, Roadmap (Icebox), or FAQ with strict Stop & Yield control.

### 🔄 Safe Lifecycle Updates (`install.py --update`)
Upgrades templates, `kb_lint.py`, `.agents/skills/*`, and Obsidian graph settings to latest releases while guaranteeing **100% preservation** of user data (`02_Tasks/*`, `03_Decisions_ADR/*`, `04_Research/*`, `05_Testing/*`, `SPEC.md`, `README.md`). User-customized agent rules are automatically backed up as `*.bak`.

### 🛡️ Continuous Integration & Release Automation (GitHub Actions)
Passing `--ci github` generates:
* `.github/workflows/kb-lint.yml`: automated knowledge base link integrity audit on every Pull Request and Push to `main`/`master`.
* `.github/workflows/release.yml`: automated build, verification, and publication of GitHub Releases with `dist/*` assets upon pushing `v*` tags.

### 🚀 Release Management & Dual-Mode Publishing (`/kb-release`)
The harness provides a built-in release automation lifecycle:
* **Dual-Mode Publishing:** Supports both online releases (GitHub Releases via `gh` CLI) and offline/local packages (cataloging build artifacts with SHA-256 in `RELEASE-vX.Y.Z.md`).
* **High-SNR Dual-Export Standard:** Public release notes (`dist/RELEASE_NOTES.md`) exclude internal ADR logs for high-signal user changelogs ([ADR-0017](docs/03_Decisions_ADR/ADR-0017-release-notes-adr-exclusion-and-high-snr-standard.md)), while internal vault notes (`docs/02_Tasks/Releases/`) scope architectural decisions strictly to the current phase.
* **Build Hook Contract:** Automatically invokes your project's build hook (`scripts/build_release.sh`, `scripts/build_release.py`, `package.json`, etc.) outputting artifacts to `dist/`.
* **Zero-Dependencies Checksums:** Calculates streaming SHA-256 hashes and formats Markdown tables for customer verification.

### ⚡ High-SNR Token Architecture & Context Compression (55–65% Savings)
To prevent LLM context exhaustion across long pair-programming sessions, the harness implements the **High-SNR Token Architecture** ([ADR-0009](docs/03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency.md), [RESEARCH-004](docs/04_Research/RESEARCH-004-token-efficiency-and-context-compression.md)):
* **Micro-Descriptions (-53% System Overhead):** All 12 AI skills use compact 10–13 word YAML descriptions, dramatically shrinking the always-on system prompt penalty.
* **Progressive Disclosure Router:** `kb-onboard` acts as a consolidated onboarding hub and lightweight router (~2.2 KB), loading deep instructions on demand.
* **Skeleton Templates (-49% Template Overhead):** 16 canonical templates refactored into compact skeletal scaffolds with single-line `<!-- prompt -->` directives.
* **Anti-Echo Protocol:** Prohibits dumping modified file contents into chat; mandates concise 3–5 bullet summaries with direct file permalinks.
* **Silent-on-Success CLI:** `scripts/kb_lint.py` and `scripts/kb_release.py` output a single status line on success (`OK: ...`), saving up to 80% tokens in terminal output history.

### 🔍 Smart Stack Autodetection (Brownfield Adoption)
When run in existing repositories (`--stack auto`), the harness heuristically inspects root marker files (`Package.swift`, `package.json`, `pyproject.toml`, `*.sln`) to select the appropriate toolchain preset and non-destructively appends Docs-as-Code sections to existing `README.md` and `.gitignore`.

---

## 🚦 Zero-to-Hero Quickstart (What to do after installation)

Once installed, your workflow is seamless:
1. **Open Obsidian:** Click *Open folder as vault* and select the `docs/` folder. Open the **Graph view** to see the 7-color architectural map.
2. **Start with your AI Agent:** In VS Code, Cursor, Antigravity, or Windsurf, prompt your agent:
   > *"Please read `AGENTS.md` and `docs/Onboarding.md`. Let's use `/kb-plan` (Mode 1) to discuss our first feature."*
3. **Verify Documentation Health:** At any time, run:
   ```bash
   python3 scripts/kb_lint.py --path docs
   ```

---

## 🔒 Key Disciplines Enforced by the Harness

1. **Permalinks Principle (No Link Rot):**
   * Task specs (`TASK-XXX`) and bug reports (`BUG-XXX`) are **never moved** to `Done/` or `Archive/` folders when closed. Status is updated in YAML frontmatter, Kanban, and Roadmap.
2. **Regression-First Principle:**
   * Bugs are closed **only** after creating a failing automated regression test and resolving the defect via `/kb-implement BUG-XXX` following the strict TDD cycle (**RED** -> **GREEN** -> **REFACTOR**).
3. **Фиксация нежизнеспособных решений (Documenting Rejected Ideas):**
   * Rejected architectural proposals and failed prototypes are logged as Rejected ADRs (`status: rejected`) or in Research notes to permanently protect against recurring mistakes.
4. **Single-Task Execution Barrier & Stop-on-Complete Protocol:**
   * The command `/kb-implement <TASK-XXX | BUG-XXX>` authorizes work strictly on a single task specification or defect report. Auto-chaining next tasks is prohibited.
   * Upon completing verification and the completion checklist, the agent immediately ceases tool calls (`Stop & Yield Control`) and awaits user commands.
   * Devlog next steps use non-executable semantic markers (`- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**`), preventing runaway autonomous loops.
5. **Spec Genesis & Zero-State Anti-Hallucination Guardrails:**
   * When `SPEC.md` is in `status: discovery` or missing, AI agents are strictly barred from hallucinating arbitrary product architectures or inventing features ([ADR-0018](docs/03_Decisions_ADR/ADR-0018-spec-genesis-protocol-and-zero-state-handling.md)). Requirements must crystallize through interactive dialogue or Mode 0 (`/kb-research`) resulting in an approved `ADR-0001` before `SPEC.md` transitions to `status: active`.
   * Planning (`/kb-plan`) and task specification (`/kb-task`) automatically issue a Soft Nudge if the specification is not yet validated.
6. **Human Guardrails Protocol («Направляй, а не блокируй»):**
   * В режимах только для чтения (Modes 0, 1, 2, 2B, 2C) агенты не выдают сухих роботизированных ошибок (`🚨 NO CODE EDITS ALLOWED`), а выступают чуткими техническими партнерами ([ADR-0022](docs/03_Decisions_ADR/ADR-0022-chat-first-vibe-coder-dx-and-human-guardrails.md)): кратко объясняют назначение стадии, задают 1–2 направляющих вопроса и подсказывают точную готовую команду для продолжения.
7. **Fast-Track Protocol (Micro-Task Bypass):**
   * Для очевидных микро-изменений ($\le 30$ строк кода, $\le 2$ файлов, без изменения архитектуры и публичных API) доступен быстрый трек в обход фазы планирования: команда `/kb-task --fast <описание>` сразу генерирует компактное ТЗ `TEMPLATE_TASK_MICRO.md` ([ADR-0023](docs/03_Decisions_ADR/ADR-0023-fast-track-protocol-for-micro-tasks.md)).
8. **Zero Round-Trip Dispatch & Hot Invariants Protocol:**
   * В стандартных режимах (0, 1, 2, 2B, 2C, 3) агент исполняет команды напрямую из Always-On префикса (`AGENTS.md`) в первом же такте без предварительного вызова `view_file` для `SKILL.md` ([ADR-0013](docs/03_Decisions_ADR/ADR-0013-zero-roundtrip-dispatch-and-hot-invariants-architecture.md)), ускоряя отклик в 2.5–3 раза.
9. **Quality Gates & Reliability Tiers Invariant:**
   * Трехуровневая матрица надежности ([ADR-0025](docs/03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates.md)): Tier 1 (Enforcement: тесты/линтеры блокируют билд) > Tier 2 (Always-On: `AGENTS.md`) > Tier 3 (Playbook: скиллы). Критические правила запрещено оставлять в вероятностном слое Tier 3.
10. **Procedural Defect Memory & Patterns Loop:**
    * Двухуровневый контур процедурной памяти (`docs/06_Memory/`): жестко лимитированный индекс систематических ошибок `patterns.md` ($\le 15$ активных записей) и архив инцидентов `Incidents/` с обязательной проверкой `Memory-First` перед реализацией.

---

## 🤝 Dogfooding

This repository (`agent-docs-harness`) is built and maintained strictly using the exact same Docs-as-Code harness and 4-stage lifecycle. Inspect the `docs/` folder to see an active, healthy knowledge base in practice!

---

## 📄 License

MIT License. Free for personal, open-source, and commercial projects.
