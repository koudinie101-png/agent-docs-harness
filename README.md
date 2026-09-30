# 🚀 Agent Docs-as-Code Harness

> **Autonomous, zero-dependency toolkit for bringing engineering discipline, Docs-as-Code knowledge vaults, and strict 3-mode AI agent guardrails to any software project.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-success.svg)](#-zero-external-dependencies)
[![Obsidian Ready](https://img.shields.io/badge/Obsidian-Vault%20Ready-purple.svg)](https://obsidian.md/)

---

## 🎯 The Problem: Why AI Agents Fail in Real Projects

When developing with modern AI coding agents (**VS Code Cline, Roo Code, Claude Code, Cursor, GitHub Copilot**), developers consistently hit three roadblocks:

1. 🧠 **"Context Amnesia":** After 15–20 chat turns, the model forgets constraints, platform quirks, and previous architectural decisions.
2. 🔨 **"Wild Code Breaking":** Without strict guardrails, agents immediately rush to edit existing files, inventing suboptimal patterns, breaking public interfaces, and introducing subtle regressions.
3. 🕸️ **"Architecture Drift & Link Rot":** Project notes, plans, and task lists get scattered, outdated, and broken, leading to lost time and confusion.

---

## 💡 The Solution: Docs-as-Code + 3-Mode Discipline

**Agent Docs-as-Code Harness** turns your project repository into a self-documenting, disciplined environment that guides AI agents like a senior software engineering partner:

```
┌────────────────────────────────────────────────────────────────────────┐
│                          3 OPERATING MODES                             │
├────────────────────┬─────────────────────────────┬─────────────────────┤
│ 🟡 Mode 1: Plan    │ 🟠 Mode 2: Specification    │ 🟢 Mode 3: Code     │
│ (/kb-plan)         │ (/kb-task)                  │ (/kb-implement)     │
│                    │                             │                     │
│ • Critical review  │ • File contracts:           │ • Strict coding per │
│ • Anti-pattern Q&A │   [NEW] / [MODIFY]          │   specification     │
│ • Risk analysis    │ • Definition of Done (DoD)  │ • Run build & tests │
│ • PLAN-XXX file    │ • Verification commands     │ • Devlog & Kanban   │
│                    │ • TASK-XXX file             │ • kb_lint.py check  │
│ 🚨 NO CODE EDITS!  │ 🚨 NO CODE EDITS!           │                     │
└────────────────────┴─────────────────────────────┴─────────────────────┘
```

---

## ⚡ Quick Start: 1-Line Installation

Deploy the complete harness into your current project in **one command**:

### Linux & macOS
```bash
curl -sSL https://raw.githubusercontent.com/<username>/agent-docs-harness/main/install.py | python3
```

### Windows (PowerShell)
```powershell
irm https://raw.githubusercontent.com/<username>/agent-docs-harness/main/install.py | python3 -
```

### Local / Cloned Usage
```bash
git clone https://github.com/<username>/agent-docs-harness.git
python3 agent-docs-harness/install.py
```

The installer features an **interactive terminal wizard** that asks for your project name, stack, and agent environment, or can be run completely hands-free with CLI flags!

---

## 📦 What Gets Installed in Your Project?

### 1. The Standard `docs/` Knowledge Base (Obsidian Vault)
```text
docs/
├── .obsidian/
│   └── graph.json            # 7-color category palette for Obsidian Graph
├── 00_Index.md               # Map of Content (MOC) entry point
├── 00_Templates/             # 12 canonical templates with YAML frontmatter
│   ├── TEMPLATE_TASK.md      # Engineering task spec with file contracts
│   ├── TEMPLATE_PLAN.md      # RFC & conceptual feature plan (Mode 1)
│   ├── TEMPLATE_BUG.md       # Defect report with RCA & Regression-First test
│   ├── TEMPLATE_ADR.md       # Architecture Decision Record (+ rejected alternatives)
│   ├── TEMPLATE_RESEARCH.md  # OS quirks, battery/memory limits, trade-off matrix
│   ├── TEMPLATE_TEST.md      # E2E UX acceptance test checklist
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
│   ├── Plans/                # RFCs (Mode 1)
│   ├── Specs/01_MVP/         # Detailed task specifications (Mode 2)
│   └── Bugs/                 # Bug tracker with RCA
├── 03_Decisions_ADR/         # Accepted & Rejected Architectural Decisions
├── 04_Research/              # Platform quirks and investigation notes
└── 05_Testing/               # E2E acceptance test scenarios
```

### 2. Autonomous Knowledge Base Linter (`scripts/kb_lint.py`)
* **Zero external dependencies** (standard Python 3 stdlib only).
* Scans all markdown documents, cross-validates internal wiki-style links, verifies YAML frontmatter, and detects link rot instantly.
* Run anytime:
  ```bash
  python3 scripts/kb_lint.py --path docs
  ```

### 3. Agent Configuration & Rule Files
Depending on your preference, the installer configures:
* **`AGENTS.md`** — Universal root standard for modern agents.
* **`.clinerules`** — VS Code Cline & Roo Code integration.
* **`CLAUDE.md`** — Claude Code CLI in terminal.
* **`.cursorrules`** — Cursor IDE rules.
* **`.github/copilot-instructions.md`** — GitHub Copilot chat & completions.

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

---

## 💻 CLI Options & Non-Interactive Usage

```bash
# Non-interactive installation for iOS/macOS Swift project with all agent rules:
python3 install.py --non-interactive --name "MySwiftApp" --stack swift --agent all --git local

# Install into a separate directory:
python3 install.py -y --target-dir ../existing-project --stack ts --agent cline

# CLI Options summary:
python3 install.py --help
  --name, -n        Project name (default: directory name)
  --stack, -s       {swift, ts, python, dotnet, generic}
  --agent, -a       {all, cline, claude, cursor, copilot, generic}
  --git, -g         {local, github, none}
  --target-dir, -d  Destination directory (default: .)
  --non-interactive Run without interactive prompts (-y, --yes)
  --force, -f       Overwrite configurations if present
```

---

## 🔒 Key Disciplines Enforced by the Harness

1. **Permalinks Principle (No Link Rot):**
   * Task specs (`TASK-XXX`) and bug reports (`BUG-XXX`) are **never moved** to `Done/` or `Archive/` folders when closed. Status is updated in YAML frontmatter, Kanban, and Roadmap.
2. **Regression-First Principle:**
   * Bugs are closed **only** when an automated regression test reproducing the defect is added to the test suite and passes.
3. **Фиксация нежизнеспособных решений (Documenting Rejected Ideas):**
   * Rejected architectural proposals and failed prototypes are logged as Rejected ADRs (`status: rejected`) or in Research notes to permanently protect against recurring mistakes.

---

## 🤝 Dogfooding

This repository (`agent-docs-harness`) is built and maintained strictly using the exact same Docs-as-Code harness and 3-mode workflow. Inspect the `docs/` folder to see an active, healthy knowledge base in practice!

---

## 📄 License

MIT License. Free for personal, open-source, and commercial projects.
