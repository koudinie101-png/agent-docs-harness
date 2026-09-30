#!/usr/bin/env python3
"""
🚀 Agent Docs-as-Code Harness Installer
=======================================
Autonomous, zero-dependency installer bringing Docs-as-Code discipline,
Obsidian graph integration, knowledge base linter, and 3-mode AI agent guardrails
to any project in a single command.

Usage:
    curl -sSL https://raw.githubusercontent.com/koudinie101-png/agent-docs-harness/main/install.py | python3
    python3 install.py [options]

Zero external dependencies (requires Python 3.8+ stdlib only).
"""

import sys
import os
import re
import json
import zlib
import base64
import shutil
import argparse
import subprocess
from datetime import date
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Python version check
if sys.version_info < (3, 8):
    print("❌ Error: agent-docs-harness requires Python 3.8 or newer.")
    print(f"Current version is: {sys.version.split()[0]}")
    sys.exit(1)

# --- BEGIN_EMBEDDED_ASSETS ---
EMBEDDED_ASSETS_B64 = "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"
# --- END_EMBEDDED_ASSETS ---


# --- STACK PRESETS & METADATA ---

STACK_PRESETS = {
    "swift": {
        "name": "iOS / macOS (Swift, SwiftUI, Xcode)",
        "language": "Swift",
        "build_cmd": "swift build  # or: xcodebuild -scheme <App> build",
        "test_cmd": "swift test   # or: xcodebuild test",
        "lint_cmd": "swiftlint    # or: swift-format",
        "file_ext": ".swift",
        "sample_contract": (
            "```swift\n"
            "public protocol ExampleServiceProtocol: Sendable {\n"
            "    func execute() async throws -> String\n"
            "}\n"
            "```"
        ),
        "bug_env": (
            "  - OS: iOS 18.x / macOS 15.x\n"
            "  - Toolchain: Xcode 16.x / Swift 6.0\n"
            "  - Device: iPhone 16 Simulator / Physical Device"
        ),
        "research_quirks": (
            "* **Memory & ARC:** Weak/unowned references, retain cycles in closures.\n"
            "* **Swift Concurrency:** `@MainActor` UI updates, `Sendable` crossing actor boundaries, Task isolation.\n"
            "* **Background Execution:** `BackgroundTasks` framework (`BGAppRefreshTask`), `URLSession` background transfers.\n"
            "* **Platform Security:** Keychain Services, App Sandbox, Entitlements."
        ),
    },
    "ts": {
        "name": "Web / Node (TypeScript, JavaScript)",
        "language": "TypeScript",
        "build_cmd": "npm run build  # or: pnpm build / yarn build",
        "test_cmd": "npm test       # or: pnpm test / vitest / jest",
        "lint_cmd": "npm run lint   # or: eslint .",
        "file_ext": ".ts",
        "sample_contract": (
            "```typescript\n"
            "export interface ExampleService {\n"
            "  execute(signal?: AbortSignal): Promise<string>;\n"
            "}\n"
            "```"
        ),
        "bug_env": (
            "  - OS: macOS / Linux / Windows\n"
            "  - Runtime: Node.js 20.x / 22.x (or Browser)\n"
            "  - Framework: TypeScript 5.x / Next.js / React"
        ),
        "research_quirks": (
            "* **Event Loop & Concurrency:** Async/await microtasks, non-blocking I/O.\n"
            "* **Memory Leaks:** Uncleaned event listeners, closures retaining DOM elements.\n"
            "* **SSR & Hydration:** Server/client markup mismatches, local storage access on server.\n"
            "* **Bundling:** Tree-shaking constraints, ESM/CJS interop."
        ),
    },
    "python": {
        "name": "Python (Standard / Pytest / FastAPI)",
        "language": "Python",
        "build_cmd": "python -m py_compile scripts/*.py",
        "test_cmd": "pytest  # or: python -m unittest discover",
        "lint_cmd": "ruff check .  # or: flake8 / mypy",
        "file_ext": ".py",
        "sample_contract": (
            "```python\n"
            "class ExampleService:\n"
            "    def execute(self) -> str:\n"
            "        return \"OK\"\n"
            "```"
        ),
        "bug_env": (
            "  - OS: macOS / Linux / Windows\n"
            "  - Python: 3.10+ / 3.12+\n"
            "  - Environment: Virtualenv / Poetry / Conda"
        ),
        "research_quirks": (
            "* **Concurrency:** Asyncio event loop blocking, GIL limitations, thread safety.\n"
            "* **Type Checking:** Strict type hints with Mypy/Pyright.\n"
            "* **Packaging:** Dependency isolation and zero-dependency discipline.\n"
            "* **OS Differences:** Windows CRLF/UTF-8 console encoding vs Unix LF."
        ),
    },
    "dotnet": {
        "name": ".NET / C# (ASP.NET, MAUI, Console)",
        "language": "C#",
        "build_cmd": "dotnet build",
        "test_cmd": "dotnet test",
        "lint_cmd": "dotnet format --verify-no-changes",
        "file_ext": ".cs",
        "sample_contract": (
            "```csharp\n"
            "public interface IExampleService {\n"
            "    Task<string> ExecuteAsync(CancellationToken ct = default);\n"
            "}\n"
            "```"
        ),
        "bug_env": (
            "  - OS: Windows 11 / macOS / Linux\n"
            "  - SDK: .NET 8.0 / 9.0\n"
            "  - Runtime: CoreCLR"
        ),
        "research_quirks": (
            "* **Async & Threading:** `ConfigureAwait(false)`, ThreadPool starvation, sync-over-async.\n"
            "* **Memory & GC:** IDisposable pattern, LOH allocations, memory leaks with events.\n"
            "* **Platform Interop:** P/Invoke, WinRT, Native AOT limitations."
        ),
    },
    "generic": {
        "name": "Generic / Other Technology Stack",
        "language": "Source Code",
        "build_cmd": "make build  # or project build command",
        "test_cmd": "make test   # or project test command",
        "lint_cmd": "make lint   # or project lint command",
        "file_ext": ".src",
        "sample_contract": (
            "```text\n"
            "// Key interface or component contract\n"
            "function execute(): Result\n"
            "```"
        ),
        "bug_env": (
            "  - OS: macOS / Linux / Windows\n"
            "  - Runtime: Project runtime environment\n"
            "  - Compiler/SDK: Project build toolchain"
        ),
        "research_quirks": (
            "* **Concurrency & Threading:** Thread safety, race conditions, synchronization.\n"
            "* **Resource Management:** Memory lifecycle, handles, leaks.\n"
            "* **OS Constraints:** Platform-specific APIs, permissions, background limits."
        ),
    },
}


# --- ASSET UNPACKING ---

def unpack_assets(source_repo_path: Path = None) -> dict:
    """
    Unpacks embedded assets from base64/zlib.
    Falls back to local filesystem if running in source repo and bundle is empty.
    """
    if EMBEDDED_ASSETS_B64:
        try:
            compressed = base64.b64decode(EMBEDDED_ASSETS_B64.encode("ascii"))
            raw_json = zlib.decompress(compressed).decode("utf-8")
            return json.loads(raw_json)
        except Exception as e:
            print(f"⚠️ Error unpacking embedded bundle: {e}")

    # Fallback for local repository development
    repo_root = source_repo_path or Path(__file__).resolve().parent
    templates_dir = repo_root / "templates"
    scripts_dir = repo_root / "scripts"
    skills_dir = repo_root / ".agents" / "skills"

    if templates_dir.is_dir():
        assets = {}
        for tf in templates_dir.glob("*.md"):
            assets[f"00_Templates/{tf.name}"] = tf.read_text(encoding="utf-8")
        graph_json = templates_dir / "graph.json"
        if graph_json.is_file():
            assets[".obsidian/graph.json"] = graph_json.read_text(encoding="utf-8")
        kb_lint = scripts_dir / "kb_lint.py"
        if kb_lint.is_file():
            assets["scripts/kb_lint.py"] = kb_lint.read_text(encoding="utf-8")
        if skills_dir.is_dir():
            for sdir in sorted([d for d in skills_dir.iterdir() if d.is_dir()]):
                skill_md = sdir / "SKILL.md"
                if skill_md.is_file():
                    assets[f".agents/skills/{sdir.name}/SKILL.md"] = skill_md.read_text(encoding="utf-8")
        if assets:
            return assets

    raise RuntimeError("Cannot find assets. Both embedded bundle and local templates directory are unavailable.")


# --- GENERATORS FOR AGENTS & REPO RULES ---

def generate_agents_md(project_name: str, stack_key: str) -> str:
    stack = STACK_PRESETS.get(stack_key, STACK_PRESETS["generic"])
    return f"""# 🤖 AGENTS.md — AI Agent Guidelines & Operating Modes

> **Project:** {project_name}  
> **Stack:** {stack['name']}  
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
3. **Graph Color Scheme:** Visual categories are preserved via `.obsidian/graph.json`.

---

## 🧠 Critical Thinking & Constructive Partnership Standard

You act as a senior software engineering partner, not a passive "yes-man":
1. **Critical Review:** Evaluate proposals against industry best practices ({stack['language']} conventions, Clean Architecture, Memory Safety, UI responsiveness).
2. **Constructive Challenge:** If an idea introduces technical debt, architectural drift, or hidden runtime crashes:
   - Highlight the flaw directly.
   - Justify the technical consequences.
   - Offer 1–2 robust, idiomatic alternatives.
3. **Document Rejected Ideas:** Preserve discarded candidate options and unviable approaches in ADRs (`status: rejected`) or Research notes to prevent recurring mistakes.

---

## 🔄 The 3-Mode Development Cycle

Every non-trivial task or feature strictly follows three sequential modes:

### 🟡 Mode 1: Planning / RFC (Trigger: "Режим 1", "Планирование", "/kb-plan")
- **Hard Constraint:** **STRICTLY PROHIBITED FROM CHANGING CODE!**
- **Action:** Conceptual discussion, research, critical review, trade-off evaluation, and Q&A.
- **Output:** Approved plan file `docs/02_Tasks/Plans/PLAN-XXX-<slug>.md`.
- **Kanban:** Add task card to `## 📥 Бэклог (Backlog)` in `docs/02_Tasks/Kanban.md`.

### 🟠 Mode 2: Task Specification (Trigger: "Режим 2", "ТЗ", "/kb-task")
- **Hard Constraint:** **STRICTLY PROHIBITED FROM CHANGING CODE!**
- **Action:** Detailed technical specification with exact file contracts:
  - `[NEW] path/to/file{stack['file_ext']}`
  - `[MODIFY] path/to/existing_file{stack['file_ext']}`
  - `[DELETE] path/to/file`
  - Class/protocol signatures, error handling, and Definition of Done (DoD).
  - Explicit **Verification Plan** with commands and expected outputs.
- **Output:** Specification file `docs/02_Tasks/Specs/<Phase>/TASK-XXX-<slug>.md`.
- **Kanban:** Move task card to `## ⏳ В работе (In Progress)` in `docs/02_Tasks/Kanban.md`.

### 🟢 Mode 3: Implementation & Verification (Trigger: "Режим 3", "Реализация", "/kb-implement")
- **Action:** Implement code strictly adhering to the approved `TASK-XXX` spec.
- **Verification Plan Commands:**
  ```bash
  # Verification & Tests:
  {stack['test_cmd']}

  # Knowledge Base Link Integrity:
  python3 scripts/kb_lint.py --path docs
  ```
- **Completion Checklist:**
  1. All verification steps pass (Exit code 0).
  2. Spec status updated to `Выполнено` in `TASK-XXX`.
  3. `docs/02_Tasks/Kanban.md`: move card to `## ✅ Готово (Done)` with current date `(YYYY-MM-DD)`.
  4. `docs/02_Tasks/Roadmap.md`: mark milestone `[x]` with permanent link to spec.
  5. `docs/Devlog.md`: record chronological summary of the session.
  6. Run `python3 scripts/kb_lint.py --path docs` to confirm 0 broken links.
  7. Commit and push to Git.
"""


def generate_clinerules(project_name: str, stack_key: str) -> str:
    return f"""# Cline / Roo Code AI Rules for {project_name}

You are working in a repository governed by the Docs-as-Code standard and a strict 3-mode workflow.
Always read `AGENTS.md` and `docs/Onboarding.md` for full guidance.

## Strict Rules:
1. **Mode 1 (Planning / RFC):** When asked to discuss, plan, or review a feature, YOU ARE STRICTLY PROHIBITED FROM EDITING OR CREATING SOURCE CODE FILES. Only read files and generate `docs/02_Tasks/Plans/PLAN-XXX-<slug>.md`.
2. **Mode 2 (Task Specification):** When asked to write a spec or ТЗ, YOU ARE STRICTLY PROHIBITED FROM EDITING SOURCE CODE. Only produce `docs/02_Tasks/Specs/<Phase>/TASK-XXX-<slug>.md`.
3. **Mode 3 (Implementation):** Implement code ONLY after explicit confirmation of the approved `TASK-XXX`. Run tests and `python3 scripts/kb_lint.py --path docs`.
4. **No Link Rot (Permalinks):** NEVER move completed task specs or bugs to archive or done folders. Update their status in-place.
5. **Regression-First:** Always write a failing test before fixing a bug.
"""


def generate_claude_md(project_name: str, stack_key: str) -> str:
    stack = STACK_PRESETS.get(stack_key, STACK_PRESETS["generic"])
    return f"""# CLAUDE.md — Claude Code Project Guidelines for {project_name}

This project uses the Docs-as-Code knowledge base and strict 3-mode discipline.

## Commands
- Build: `{stack['build_cmd']}`
- Test: `{stack['test_cmd']}`
- Lint KB: `python3 scripts/kb_lint.py --path docs`

## Architecture & Workflows
- Full instructions: `AGENTS.md`
- Onboarding guide: `docs/Onboarding.md`
- Kanban Board: `docs/02_Tasks/Kanban.md`

## 3-Mode Operating Discipline
- **Mode 1 (Planning):** Research & discussion only. No code modifications!
- **Mode 2 (Spec):** File contracts `[NEW]`/`[MODIFY]`, DoD, verification plan. No code modifications!
- **Mode 3 (Implementation):** Strict coding per spec, run tests, update Kanban & Devlog, run `kb_lint.py`.
- **Permalinks:** Never move closed tasks or bugs to archive folders.
"""


def generate_cursorrules(project_name: str, stack_key: str) -> str:
    return f"""# Cursor Rules for {project_name}

You are an expert engineer adhering to Docs-as-Code standards.
Always inspect `AGENTS.md` and `docs/Onboarding.md` before making architectural decisions.

Follow the 3 strict operating modes:
- Mode 1: Planning / RFC (NO CODE CHANGES) -> docs/02_Tasks/Plans/
- Mode 2: Specification (NO CODE CHANGES) -> docs/02_Tasks/Specs/
- Mode 3: Implementation & DoD -> verify tests & python3 scripts/kb_lint.py --path docs

Permalinks: Do not move completed specs or bugs to different folders.
Bugs: Enforce regression-first failing tests before patching defects.
"""


def generate_copilot_instructions(project_name: str, stack_key: str) -> str:
    return f"""# GitHub Copilot Instructions for {project_name}

This repository follows the Docs-as-Code methodology and 3-mode development discipline described in `AGENTS.md`.
- Mode 1: Planning / RFC (Discussion only, no code edits).
- Mode 2: Task Specification (Formal spec with [NEW]/[MODIFY] file list, no code edits).
- Mode 3: Implementation (Code strictly per spec, execute verification commands, record Devlog).
- Knowledge Base: Maintained inside `docs/`. Run `python3 scripts/kb_lint.py --path docs` to check links.
"""


# --- STARTER DOCS CUSTOMIZATION ---

def customize_templates_for_stack(template_name: str, content: str, stack_key: str, today_str: str) -> str:
    stack = STACK_PRESETS.get(stack_key, STACK_PRESETS["generic"])
    content = content.replace("2026-09-19", today_str).replace("2026-09-26", today_str)

    if template_name == "TEMPLATE_TASK.md":
        # Replace sample contract with stack-specific contract
        contract_target = "```csharp\n// Пример ключевого интерфейса или фрагмента контракта\npublic interface IExampleService\n{\n    Task ExecuteAsync(CancellationToken ct);\n}\n```"
        if contract_target in content:
            content = content.replace(contract_target, stack["sample_contract"])
        # Replace build & test command
        content = content.replace("`dotnet build` или `./gradlew test`", f"`{stack['build_cmd']}`")
        content = content.replace("`dotnet test`", f"`{stack['test_cmd']}`")
        content = content.replace("Path/To/NewFile.cs", f"Path/To/NewFile{stack['file_ext']}")
        content = content.replace("Path/To/ExistingFile.kt", f"Path/To/ExistingFile{stack['file_ext']}")
        content = content.replace("Path/To/OldFile.cs", f"Path/To/OldFile{stack['file_ext']}")

    elif template_name == "TEMPLATE_BUG.md":
        # Replace bug environment and test paths
        env_marker = "  - ОС: Windows 11 Build / Android Version\n  - Стек: .NET SDK / Gradle Version / Runtime\n  - Сеть/Конфигурация: Localhost / Wi-Fi / VPN"
        if env_marker in content:
            content = content.replace(env_marker, stack["bug_env"])
        content = content.replace("path/to/file.cs", f"path/to/file{stack['file_ext']}")
        content = content.replace("tests/Path/To/RegressionTest.cs", f"tests/Path/To/RegressionTest{stack['file_ext']}")

    elif template_name == "TEMPLATE_RESEARCH.md":
        # Replace sample research code and platform quirks
        quirks_marker = "* **Поведение в фоне и энергопотребление (Doze / WakeLock):** ...\n* **Поведение при сбоях сети и роуминге:** ...\n* **Потокобезопасность и нагрузка на память/CPU:** ...\n* **Ограничения прав и безопасности ОС:** ..."
        if quirks_marker in content:
            content = content.replace(quirks_marker, stack["research_quirks"])
        content = content.replace("```kotlin\n// Пример проверочного кода или сниппета решения\n```", stack["sample_contract"])

    return content


def create_starter_docs(target_dir: Path, project_name: str, stack_key: str, assets: dict = None):
    stack = STACK_PRESETS.get(stack_key, STACK_PRESETS["generic"])
    today_str = date.today().isoformat()
    docs_dir = target_dir / "docs"

    # 1. SPEC.md (Root)
    spec_path = target_dir / "SPEC.md"
    if not spec_path.exists():
        spec_content = f"""---
id: SPEC
title: "Мастер-спецификация: {project_name}"
status: active
type: specification
created: {today_str}
updated: {today_str}
tags:
  - spec
  - master
  - {project_name.lower().replace(" ", "-")}
---

# 🚀 Мастер-спецификация: {project_name}

> **Проект:** {project_name}  
> **Стек:** {stack['name']}  
> **Связанные документы:** [[docs/00_Index|00_Index]], [[docs/Onboarding|Онбординг]], [[docs/02_Tasks/Kanban|Канбан]], [[docs/02_Tasks/Roadmap|Дорожная карта]].

---

## 1. Концепция и цели проекта
*Краткое описание назначения проекта, решаемой проблемы и целевой аудитории.*

---

## 2. Архитектура и стек технологий
* **Платформа и технологии:** {stack['name']} ({stack['language']})
* **Сборка проекта:** `{stack['build_cmd']}`
* **Запуск тестов:** `{stack['test_cmd']}`
* **Проверка базы знаний:** `python3 scripts/kb_lint.py --path docs`

---

## 3. Этапы разработки
План реализации разбит на фазы в [[docs/02_Tasks/Roadmap|Дорожной карте]]:
* **Фаза 1: Инициализация и MVP** — Базовый каркас и проверка сборки.
* **Фаза 2: Основная функциональность** — Ключевые пользовательские сценарии.
"""
        spec_path.write_text(spec_content, encoding="utf-8")

    # 2. docs/00_Index.md
    index_path = docs_dir / "00_Index.md"
    if not index_path.exists():
        tpl = (assets or {}).get("00_Templates/TEMPLATE_INDEX.md", "")
        if tpl:
            index_content = tpl.replace("[Название Проекта]", project_name).replace("2026-09-19", today_str)
        else:
            index_content = f"""---
id: 00_INDEX
title: "База знаний: {project_name}"
status: active
type: hub
created: {today_str}
updated: {today_str}
tags:
  - project
  - pkm
  - index
---

# 🧠 База знаний: {project_name}

> **Стек:** {stack['name']}  
> **Главная спецификация:** [[../SPEC|SPEC.md (Master Specification)]]  
> **Руководство по онбордингу:** [[Onboarding|Руководство разработчика]]  

## 🗺️ Карта заметок
* [[Onboarding|Руководство по онбордингу]]
* [[02_Tasks/Kanban|Канбан-доска]]
* [[02_Tasks/Roadmap|Дорожная карта]]
* [[Devlog|Журнал разработки]]
* [[00_Templates/TEMPLATE_TASK|Каталог шаблонов]]
"""
        index_path.write_text(index_content, encoding="utf-8")

    # 3. docs/Onboarding.md
    onboarding_path = docs_dir / "Onboarding.md"
    if not onboarding_path.exists():
        tpl = (assets or {}).get("00_Templates/TEMPLATE_ONBOARDING.md", "")
        if tpl:
            onboarding_content = (
                tpl
                .replace("[Название Проекта]", project_name)
                .replace("2026-09-19", today_str)
                .replace("dotnet build", stack["build_cmd"])
                .replace("dotnet test", stack["test_cmd"])
            )
        else:
            onboarding_content = f"""---
id: ONBOARDING
title: Руководство по онбордингу и взаимодействию
status: active
type: hub
created: {today_str}
updated: {today_str}
tags:
  - onboarding
  - guide
  - docs-as-code
  - workflow
---

# 🚀 Руководство по онбордингу: {project_name}

> **Связанные документы:** [[00_Index|00_Index]], [[02_Tasks/Kanban|Канбан-доска]], [[02_Tasks/Roadmap|Дорожная карта]], [[Devlog|Журнал разработки]].

## Режимы взаимодействия:
1. 🟡 **Режим 1: Планирование** (`/kb-plan`) — запрет на изменение кода.
2. 🟠 **Режим 2: Спецификация** (`/kb-task`) — запрет на изменение кода.
3. 🟢 **Режим 3: Реализация** (`/kb-implement`) — код, тесты, сдача задачи.
"""
        onboarding_path.write_text(onboarding_content, encoding="utf-8")

    # 4. docs/Devlog.md
    devlog_path = docs_dir / "Devlog.md"
    if not devlog_path.exists():
        tpl = (assets or {}).get("00_Templates/TEMPLATE_DEVLOG.md", "")
        if tpl:
            devlog_content = tpl.replace("2026-09-19", today_str)
        else:
            devlog_content = f"""---
id: DEVLOG
title: Журнал разработки (Devlog)
status: active
type: devlog
created: {today_str}
updated: {today_str}
tags:
  - devlog
  - journal
---

# 📝 Журнал разработки (Devlog): {project_name}

> **Родительская заметка:** [[00_Index|00_Index]]  

### [{today_str}] — Инициализация базы знаний Docs-as-Code
- **Что сделано:**
  - Развернута инфраструктура базы знаний `docs/` по стандарту Docs-as-Code.
  - Настроена цветовая схема Obsidian Graph (`.obsidian/graph.json`).
  - Развернут автономный линтер базы знаний `scripts/kb_lint.py`.
"""
        devlog_path.write_text(devlog_content, encoding="utf-8")

    # 5. docs/02_Tasks/Kanban.md
    kanban_path = docs_dir / "02_Tasks" / "Kanban.md"
    kanban_content = f"""---
kanban-plugin: basic
---

# 📋 Канбан-доска: {project_name}

> **Теги:** #tasks #kanban #planning  
> **Связанная дорожная карта:** [[Roadmap|Дорожная карта]]  

## 📥 Бэклог (Backlog)

- [ ] [[Plans/PLAN-001-initial-mvp-setup|План: Фаза 1 — Первичный MVP и проверка сборки]] #plan #phase1
  - [ ] [[Specs/01_MVP/TASK-001-project-scaffolding|TASK-001]]: Первичный каркас проекта и базовые тесты #task

## ⏳ В работе (In Progress)


## ✅ Готово (Done)

- [x] Инициализация структуры базы знаний Docs-as-Code ({today_str}) #docs

## 💡 Идеи и гипотезы (Icebox / Future Ideas)

- [ ] [Идея 1]: краткая формулировка задумки или гипотезы #idea
"""
    kanban_path.write_text(kanban_content, encoding="utf-8")

    # 6. docs/02_Tasks/Roadmap.md
    roadmap_path = docs_dir / "02_Tasks" / "Roadmap.md"
    roadmap_content = f"""---
id: ROADMAP
title: Дорожная карта разработки (Roadmap)
status: active
type: roadmap
created: {today_str}
updated: {today_str}
tags:
  - roadmap
  - planning
  - milestones
---

# 🗺️ Дорожная карта разработки (Roadmap): {project_name}

> **Теги:** #roadmap #planning #milestones  
> **Связанный канбан:** [[Kanban|Канбан-доска]]  
> **Первоисточник:** [[../../SPEC|SPEC.md (Мастер-спецификация)]]  

---

## Фаза 1: Инициализация и MVP
**Цель:** Создание базового каркаса проекта и проверка сборки/тестов.

- [ ] Создание каркаса репозитория и базовая конфигурация — [[Specs/01_MVP/TASK-001-project-scaffolding|TASK-001]].
- [ ] Базовые функциональные модули.

---

## Фаза 2: Основная функциональность
**Цель:** Реализация ключевых пользовательских сценариев.

- [ ] Реализация основных сервисов.

---

## 🔮 Перспективные направления (Future Horizons / Later)
*Идеи и гипотезы, находящиеся на стадии осмысления. Прорабатываются через Режим 1 (`/kb-plan`).*

* 💡 **[Идея 1]:** Краткое описание проблемы и ценности.
"""
    roadmap_path.write_text(roadmap_content, encoding="utf-8")

    # 7. Starter Plan & Task to ensure 0 broken links in starter Kanban & Roadmap
    plans_dir = docs_dir / "02_Tasks" / "Plans"
    specs_dir = docs_dir / "02_Tasks" / "Specs" / "01_MVP"

    plan_path = plans_dir / "PLAN-001-initial-mvp-setup.md"
    if not plan_path.exists():
        plan_content = f"""---
id: PLAN-001
title: Инициализация проекта и первичный MVP
status: proposed
type: plan
phase: 1
created: {today_str}
updated: {today_str}
tags:
  - plan
  - feature
  - setup
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 📋 План: PLAN-001 — Инициализация проекта и первичный MVP

> **ID:** PLAN-001  
> **Статус:** Обсуждение  
> **Теги:** #plan #feature #setup  
> **Родительская спецификация:** [[../../SPEC|SPEC.md]]  
> **Канбан:** [[../Kanban|Канбан-доска]]  

---

## 1. Контекст и цели (Problem & Goals)
Развертывание базовой кодовой базы проекта {project_name} на стеке {stack['name']}.

## 2. Задачи плана
- [ ] [[../Specs/01_MVP/TASK-001-project-scaffolding|TASK-001]]: Первичный каркас проекта.
"""
        plan_path.write_text(plan_content, encoding="utf-8")

    task_path = specs_dir / "TASK-001-project-scaffolding.md"
    if not task_path.exists():
        task_content = f"""---
id: TASK-001
title: Первичный каркас проекта и базовые тесты
status: planned
type: task
phase: 1
component:
  - core
parent_plan: "[[../../Plans/PLAN-001-initial-mvp-setup|PLAN-001]]"
created: {today_str}
updated: {today_str}
tags:
  - task/spec
  - component/core
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-001 — Первичный каркас проекта

> **ID:** TASK-001  
> **Статус:** К реализации  
> **Теги:** #task/spec #component/core  
> **Родительский план:** [[../../Plans/PLAN-001-initial-mvp-setup|PLAN-001]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи
Настроить базовую структуру исходных кодов и убедиться, что тесты успешно запускаются.

## 2. Затрагиваемые файлы и компоненты
* `[NEW]` Исходные файлы проекта ({stack['file_ext']})
* `[NEW]` Конфигурационные файлы сборщика

## 3. План верификации (Verification Plan)
- [ ] Запуск сборки: `{stack['build_cmd']}`
- [ ] Запуск тестов: `{stack['test_cmd']}`
- [ ] Проверка базы знаний: `python3 scripts/kb_lint.py --path docs`
"""
        task_path.write_text(task_content, encoding="utf-8")


# --- GIT SETUP ---

def setup_git(target_dir: Path, git_choice: str):
    """
    Handles git initialization according to user choice: 'local', 'github', or 'none'.
    """
    if git_choice == "none":
        print("⏭️ Git setup skipped.")
        return

    # Check if git command exists
    git_cmd = shutil.which("git")
    if not git_cmd and sys.platform == "win32":
        # Check standard Windows paths
        win_candidates = [
            r"C:\Program Files\Git\cmd\git.exe",
            r"C:\Program Files\Git\bin\git.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Git\cmd\git.exe"),
        ]
        for cand in win_candidates:
            if os.path.isfile(cand):
                git_cmd = cand
                break

    if not git_cmd:
        print("⚠️ Warning: 'git' executable not found in PATH. Skipping automated Git operations.")
        print("   You can initialize Git manually later with: git init")
        return

    is_git_repo = (target_dir / ".git" / "HEAD").is_file()

    if not is_git_repo:
        try:
            subprocess.run([git_cmd, "init"], cwd=str(target_dir), check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
            print("📦 Initialized local Git repository.")
        except Exception as e:
            print(f"⚠️ Git init warning: {e}")

    # Prepare .gitignore if not present
    gitignore_path = target_dir / ".gitignore"
    if not gitignore_path.exists():
        gitignore_content = """# System & IDE
.DS_Store
Thumbs.db
.idea/
.vscode/*
!.vscode/settings.json

# Obsidian Workspace (keep graph config, ignore local workspace state)
.obsidian/*
!.obsidian/graph.json
"""
        gitignore_path.write_text(gitignore_content, encoding="utf-8")
        print("📄 Created .gitignore (with Obsidian graph retention rules).")

    # Scope git operations strictly to target_dir
    git_env = os.environ.copy()
    git_env["GIT_DIR"] = str((target_dir / ".git").resolve())
    git_env["GIT_WORK_TREE"] = str(target_dir.resolve())

    # Initial commit
    try:
        subprocess.run([git_cmd, "add", "-A"], cwd=str(target_dir), env=git_env, check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
        res = subprocess.run([git_cmd, "commit", "-m", "feat: initialize docs-as-code harness"], cwd=str(target_dir), env=git_env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        subprocess.run([git_cmd, "branch", "-M", "main"], cwd=str(target_dir), env=git_env, check=False, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if res.returncode == 0:
            print("✅ Created initial Git commit with Docs-as-Code harness (branch: main).")
    except Exception as e:
        print(f"⚠️ Git commit notice: {e}")

    if git_choice == "github":
        print("\n🐙 GitHub Remote Setup Instructions:")
        print("   1. Go to https://github.com/new and create a new repository.")
        print("   2. (Do NOT check README, .gitignore or license options).")
        print("   3. Run the following commands to link your repository:")
        print(f"      cd \"{target_dir.resolve()}\"")
        print("      git remote add origin https://github.com/<your-username>/<repo-name>.git")
        print("      git push -u origin main\n")


# --- INSTALLATION ORCHESTRATOR ---

def install_harness(
    target_dir: Path,
    project_name: str,
    stack_key: str,
    agent_choice: str,
    git_choice: str,
    doc_lang: str = "ru",
    force: bool = False,
):
    print(f"\n🚀 Installing Agent Docs-as-Code Harness into: {target_dir.resolve()}")
    print(f"   • Project Name: {project_name}")
    print(f"   • Stack: {STACK_PRESETS.get(stack_key, STACK_PRESETS['generic'])['name']}")
    print(f"   • AI Agent configs: {agent_choice}")
    print(f"   • Documentation language: {doc_lang}")
    print(f"   • Git mode: {git_choice}\n")

    docs_dir = target_dir / "docs"
    if docs_dir.exists() and not force:
        print(f"⚠️ Warning: Directory '{docs_dir}' already exists.")
        print("   Existing files will be preserved. Only missing templates and directories will be created.")

    # 1. Unpack assets
    assets = unpack_assets()

    # 2. Create directory skeleton
    dirs_to_create = [
        docs_dir / "00_Templates",
        docs_dir / ".obsidian",
        docs_dir / "01_Architecture",
        docs_dir / "02_Tasks" / "Plans",
        docs_dir / "02_Tasks" / "Specs" / "01_MVP",
        docs_dir / "02_Tasks" / "Bugs",
        docs_dir / "03_Decisions_ADR",
        docs_dir / "04_Research",
        docs_dir / "05_Testing",
        target_dir / "scripts",
    ]

    for d in dirs_to_create:
        d.mkdir(parents=True, exist_ok=True)
        # Ensure .gitkeep in empty dirs so Git tracks them
        if not list(d.glob("*")):
            (d / ".gitkeep").touch()

    # 3. Write unpacked templates and scripts
    today_str = date.today().isoformat()
    skills_count = 0
    for rel_path, content in assets.items():
        if rel_path.startswith("00_Templates/"):
            tpl_name = Path(rel_path).name
            customized = customize_templates_for_stack(tpl_name, content, stack_key, today_str)
            target_file = docs_dir / "00_Templates" / tpl_name
            target_file.write_text(customized, encoding="utf-8")
        elif rel_path.startswith(".agents/skills/"):
            target_file = target_dir / rel_path
            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_text(content, encoding="utf-8")
            skills_count += 1
        elif rel_path == ".obsidian/graph.json":
            target_file = docs_dir / ".obsidian" / "graph.json"
            target_file.write_text(content, encoding="utf-8")
        elif rel_path == "scripts/kb_lint.py":
            target_file = target_dir / "scripts" / "kb_lint.py"
            target_file.write_text(content, encoding="utf-8")
            try:
                target_file.chmod(0o755)
            except Exception:
                pass

    print(f"✅ Deployed 12 templates and Obsidian graph configuration.")
    print(f"✅ Deployed scripts/kb_lint.py linter.")
    if skills_count > 0:
        print(f"✅ Deployed {skills_count} AI agent skills (.agents/skills/).")

    # 4. Generate starter knowledge base documents
    create_starter_docs(target_dir, project_name, stack_key, assets=assets)
    print(f"✅ Created starter knowledge base docs (SPEC.md, 00_Index.md, Onboarding.md, Kanban.md, Roadmap.md, Devlog.md).")

    # 5. Generate Agent rule files
    agents_md = generate_agents_md(project_name, stack_key)
    (target_dir / "AGENTS.md").write_text(agents_md, encoding="utf-8")
    print("✅ Created root AGENTS.md (Universal Agent Standard).")

    if agent_choice in ["all", "cline"]:
        (target_dir / ".clinerules").write_text(generate_clinerules(project_name, stack_key), encoding="utf-8")
        print("✅ Created .clinerules (VS Code Cline & Roo Code).")

    if agent_choice in ["all", "claude"]:
        (target_dir / "CLAUDE.md").write_text(generate_claude_md(project_name, stack_key), encoding="utf-8")
        print("✅ Created CLAUDE.md (Claude Code CLI).")

    if agent_choice in ["all", "cursor"]:
        (target_dir / ".cursorrules").write_text(generate_cursorrules(project_name, stack_key), encoding="utf-8")
        print("✅ Created .cursorrules (Cursor IDE).")

    if agent_choice in ["all", "copilot"]:
        copilot_dir = target_dir / ".github"
        copilot_dir.mkdir(parents=True, exist_ok=True)
        (copilot_dir / "copilot-instructions.md").write_text(generate_copilot_instructions(project_name, stack_key), encoding="utf-8")
        print("✅ Created .github/copilot-instructions.md (GitHub Copilot).")

    # 6. Verify knowledge base integrity with kb_lint.py
    kb_lint_path = target_dir / "scripts" / "kb_lint.py"
    if kb_lint_path.is_file():
        print("\n🔍 Running initial knowledge base audit with kb_lint.py...")
        res = subprocess.run(
            [sys.executable, str(kb_lint_path), "--path", str(docs_dir)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if res.returncode == 0:
            print("✅ Linter check passed: 0 broken links, valid YAML frontmatter!")
        else:
            print(f"⚠️ Linter reported warnings:\n{res.stdout}\n{res.stderr}")

    # 7. Git setup
    setup_git(target_dir, git_choice)

    # 8. Success banner and instructions
    print("\n" + "=" * 70)
    print(f"🎉 Agent Docs-as-Code Harness installed successfully in '{project_name}'!")
    print("=" * 70)
    print("\n📚 Next Steps for You & Your AI Agent:")
    print("  1. Open the project folder in VS Code / Cursor / Obsidian:")
    print(f"     code \"{target_dir.resolve()}\"")
    print("  2. In Obsidian: Open Vault -> choose folder 'docs/' to view the colored graph!")
    print("  3. Ask your AI Agent:")
    print("     \"Please read AGENTS.md and let's start Mode 1 (Planning) for our first task.\"")
    print("  4. Verify your documentation anytime:")
    print("     python3 scripts/kb_lint.py --path docs\n")


# --- INTERACTIVE CLI WIZARD ---

def prompt_user_input(prompt_text: str, default: str = "") -> str:
    default_hint = f" [{default}]" if default else ""
    try:
        val = input(f"{prompt_text}{default_hint}: ").strip()
        return val if val else default
    except (EOFError, KeyboardInterrupt):
        return default


def run_interactive_wizard(args) -> tuple:
    print("""
╭──────────────────────────────────────────────────────────╮
│  ✨ Agent Docs-as-Code Harness Installer                 │
│  Zero-Dependency AI Agent Discipline & Obsidian Vault   │
╰──────────────────────────────────────────────────────────╯
""")

    # Try reopening TTY if piped through curl
    if not sys.stdin.isatty():
        try:
            if os.name != "nt" and os.path.exists("/dev/tty"):
                sys.stdin = open("/dev/tty", "r")
            elif os.name == "nt":
                sys.stdin = open("CONIN$", "r")
        except Exception:
            pass

    target_dir = Path(args.target_dir).resolve()
    default_name = args.name or target_dir.name or "MyProject"

    # 1. Project Name
    project_name = prompt_user_input("? Enter Project Name", default=default_name)

    # 2. Documentation & Agent Communication Language
    print("\n? Preferred documentation & agent communication language:")
    print("  [1] Russian (Русский) [Recommended for RU teams]")
    print("  [2] English")
    print("  [3] Custom language (type name)")
    lang_choice_input = prompt_user_input("Select [1-3]", default="1")
    if lang_choice_input == "1":
        doc_lang = "ru"
    elif lang_choice_input == "2":
        doc_lang = "en"
    elif lang_choice_input == "3":
        doc_lang = prompt_user_input("Enter language name", default="ru")
    else:
        doc_lang = "ru"

    # 3. Technology Stack
    print("\n? Select Technology Stack:")
    print("  [1] iOS / macOS (Swift, SwiftUI, Xcode) [Target Apple Stack]")
    print("  [2] Web / Node (TypeScript, JavaScript, Next.js)")
    print("  [3] Python (Pytest, FastAPI, CLI)")
    print("  [4] .NET / C# (MAUI, ASP.NET, CoreCLR)")
    print("  [5] Generic / Other")
    stack_choice = prompt_user_input("Select [1-5]", default="1")
    stack_map = {"1": "swift", "2": "ts", "3": "python", "4": "dotnet", "5": "generic"}
    stack_key = stack_map.get(stack_choice, "swift")

    # 4. AI Agent Setup
    print("\n? Select AI Agent / IDE Setup:")
    print("  [1] All AI Agents (AGENTS.md, Cline, Claude Code, Cursor, Copilot) [Recommended]")
    print("  [2] VS Code Cline & Roo Code (.clinerules)")
    print("  [3] Claude Code CLI (CLAUDE.md)")
    print("  [4] Cursor IDE (.cursorrules)")
    print("  [5] GitHub Copilot (.github/copilot-instructions.md)")
    print("  [6] Universal AGENTS.md only")
    agent_choice_input = prompt_user_input("Select [1-6]", default="1")
    agent_map = {"1": "all", "2": "cline", "3": "claude", "4": "cursor", "5": "copilot", "6": "generic"}
    agent_choice = agent_map.get(agent_choice_input, "all")

    # 5. Git Setup
    print("\n? Git Version Control Setup:")
    print("  [1] Local Git (Initialize repository & commit initial docs) [Recommended]")
    print("  [2] Connect to GitHub (Local commit + setup guidance)")
    print("  [3] Skip Git")
    git_choice_input = prompt_user_input("Select [1-3]", default="1")
    git_map = {"1": "local", "2": "github", "3": "none"}
    git_choice = git_map.get(git_choice_input, "local")

    return project_name, stack_key, agent_choice, git_choice, doc_lang


# --- MAIN ENTRY POINT ---

def main():
    parser = argparse.ArgumentParser(
        description="Agent Docs-as-Code Harness Installer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode:
  python3 install.py

  # Non-interactive mode for Swift/iOS:
  python3 install.py --non-interactive --name "MyApp" --stack swift --agent all --git local

  # Install into specific target directory with English documentation:
  python3 install.py -y --target-dir ../other-project --stack ts --doc-lang en
""",
    )

    parser.add_argument("--name", "-n", type=str, help="Project name (default: current directory name)")
    parser.add_argument(
        "--doc-lang", "-l",
        type=str,
        default=None,
        help="Preferred documentation & agent communication language (e.g. ru, en, custom; default: ru)",
    )
    parser.add_argument(
        "--stack", "-s",
        choices=["swift", "ts", "python", "dotnet", "generic"],
        default=None,
        help="Target technology stack preset (default: swift)",
    )
    parser.add_argument(
        "--agent", "-a",
        choices=["all", "cline", "claude", "cursor", "copilot", "generic"],
        default=None,
        help="AI agent / editor configuration files to generate (default: all)",
    )
    parser.add_argument(
        "--git", "-g",
        choices=["local", "github", "none"],
        default=None,
        help="Git version control strategy (default: local)",
    )
    parser.add_argument(
        "--target-dir", "-d",
        type=str,
        default=".",
        help="Target directory where the harness will be installed (default: current directory)",
    )
    parser.add_argument(
        "--non-interactive", "-y", "--yes",
        action="store_true",
        help="Run without interactive prompts, accepting flags or defaults",
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Overwrite existing configuration files if present",
    )

    args = parser.parse_args()
    target_dir = Path(args.target_dir).resolve()

    # Determine whether to run interactively
    is_interactive = not args.non_interactive and (sys.stdin.isatty() or os.name == "nt" or os.path.exists("/dev/tty"))

    # If flags were all explicitly passed, run directly
    if args.stack and args.agent and args.git and args.name:
        is_interactive = False

    if is_interactive:
        project_name, stack_key, agent_choice, git_choice, doc_lang = run_interactive_wizard(args)
    else:
        project_name = args.name or target_dir.name or "MyProject"
        stack_key = args.stack or "swift"
        agent_choice = args.agent or "all"
        git_choice = args.git or "local"
        doc_lang = args.doc_lang or "ru"

    install_harness(
        target_dir=target_dir,
        project_name=project_name,
        stack_key=stack_key,
        agent_choice=agent_choice,
        git_choice=git_choice,
        doc_lang=doc_lang,
        force=args.force,
    )


if __name__ == "__main__":
    main()
