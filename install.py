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


# ============================================================================
# STACK PRESETS & METADATA
# ============================================================================

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


# ============================================================================
# ASSET UNPACKING
# ============================================================================

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
        if assets:
            return assets

    raise RuntimeError("Cannot find assets. Both embedded bundle and local templates directory are unavailable.")


# ============================================================================
# GENERATORS FOR AGENTS & REPO RULES
# ============================================================================

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


# ============================================================================
# STARTER DOCS CUSTOMIZATION
# ============================================================================

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


def create_starter_docs(target_dir: Path, project_name: str, stack_key: str):
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

Добро пожаловать в базу знаний проекта. Каталог `docs/` спроектирован по стандарту **Docs-as-Code** и представляет собой локальное хранилище для Obsidian и AI-агентов.

---

## 🗺️ Карта заметок (Map of Content)

```mermaid
flowchart TD
    Index["00_Index (База знаний)"] --> Onboarding["[[Onboarding|Онбординг]]"]
    Index --> Arch["01. Архитектура"]
    Index --> Tasks["02. Задачи и планы"]
    Index --> ADR["03. Решения (ADR)"]
    Index --> Research["04. Исследования"]
    Index --> Testing["05. Тестирование"]
    Index --> Devlog["Журнал разработки"]

    Tasks --> Kanban["[[02_Tasks/Kanban|Канбан-доска]]"]
    Tasks --> Roadmap["[[02_Tasks/Roadmap|Дорожная карта]]"]
```

---

## 📂 Структура разделов

### 0. Вводные материалы
* [[Onboarding|Руководство по онбордингу]] — правила ведения базы знаний, 3 режима и быстрые команды.
* [[00_Templates/TEMPLATE_TASK|Каталог шаблонов]] — эталонные шаблоны (12 шаблонов).

### 1. Архитектура (`01_Architecture/`)
* Системные компоненты, схемы взаимодействия, диаграммы модулей.

### 2. Задачи и трекинг (`02_Tasks/`)
* [[02_Tasks/Kanban|Канбан-доска]] — оперативные задачи (Backlog, In Progress, Done).
* [[02_Tasks/Roadmap|Дорожная карта]] — стратегические фазы от MVP до релиза.
* `Plans/` — концепции и планы фичей (Режим 1).
* `Specs/` — технические задания по фазам (Режим 2).
* `Bugs/` — журнал дефектов и баг-репортов.

### 3. Архитектурные решения (`03_Decisions_ADR/`)
* Реестр принятых архитектурных решений (`ADR-XXXX`).

### 4. Исследования платформы (`04_Research/`)
* Подводные камни API, особенности ОС и платформенные ограничения.

### 5. Тестирование и верификация (`05_Testing/`)
* Чек-листы E2E UX, сценарии приемки, тест-планы.

### 6. Дневник проекта
* [[Devlog|Журнал разработки]] — хроника сессий и результатов.
"""
    index_path.write_text(index_content, encoding="utf-8")

    # 3. docs/Onboarding.md
    onboarding_path = docs_dir / "Onboarding.md"
    onboarding_content = f"""---
id: ONBOARDING
title: Руководство по онбордингу и взаимодействию (Onboarding Guide)
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

> **Назначение:** Единая точка входа для разработчиков и AI-агентов.  
> **Связанные документы:** [[00_Index|00_Index]], [[02_Tasks/Kanban|Канбан-доска]], [[02_Tasks/Roadmap|Дорожная карта]], [[Devlog|Журнал разработки]].

---

## 1. Концепция Docs-as-Code
База знаний проекта спроектирована по методологии **Docs-as-Code**:
* Документация ведется в каталоге `docs/` рядом с кодом.
* Связи оформляются через вики-ссылки `[[Имя_Файла]]`.
* Принцип **Permalinks**: файлы задач и багов **никогда не перемещаются** в архивные директории при закрытии.
* Принцип **Regression-First**: любой баг закрывается только при наличии теста, подтверждающего устранение сбоя.
* Цвета графа Obsidian настроены в `.obsidian/graph.json`.

---

## 2. Три режима взаимодействия (Operating Modes)

```mermaid
flowchart LR
    Mode1["🟡 Режим 1: Планирование\n[Запрет на код]"]
    Mode2["🟠 Режим 2: Спецификация\n[Запрет на код]"]
    Mode3["🟢 Режим 3: Реализация\n[Код + Тесты + Devlog]"]

    Mode1 -->|Согласование| Mode2
    Mode2 -->|Утверждение ТЗ| Mode3
```

* **🟡 Режим 1 (Planning / RFC):** Обсуждение архитектуры, выявление рисков, фиксация `PLAN-XXX`. **Изменение кода запрещено!**
* **🟠 Режим 2 (Task Specification):** Контракты файлов `[NEW]`/`[MODIFY]`, критерии DoD, план проверки `TASK-XXX`. **Изменение кода запрещено!**
* **🟢 Режим 3 (Implementation & Verification):** Написание кода строго по ТЗ, прогон тестов, обновление Канбана и `Devlog.md`.

---

## 3. Стек технологий и ключевые команды
* **Стек проекта:** {stack['name']} ({stack['language']})
* **Сборка:**
  ```bash
  {stack['build_cmd']}
  ```
* **Запуск тестов:**
  ```bash
  {stack['test_cmd']}
  ```
* **Проверка целостности базы знаний:**
  ```bash
  python3 scripts/kb_lint.py --path docs
  ```
"""
    onboarding_path.write_text(onboarding_content, encoding="utf-8")

    # 4. docs/Devlog.md
    devlog_path = docs_dir / "Devlog.md"
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

---

### [{today_str}] — Инициализация базы знаний Docs-as-Code
- **Что сделано:**
  - Развернута инфраструктура базы знаний `docs/` по стандарту Docs-as-Code.
  - Настроена цветовая схема Obsidian Graph (`.obsidian/graph.json`).
  - Развернут автономный линтер базы знаний `scripts/kb_lint.py`.
  - Сконфигурированы правила AI-агентов (`AGENTS.md`) и 3-режимный воркфлоу для стека {stack['name']}.
- **Следующий шаг:**
  - Формирование плана Фазы 1 в [[02_Tasks/Roadmap|Дорожной карте]] и первой задачи на [[02_Tasks/Kanban|Канбан-доске]].
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


# ============================================================================
# GIT SETUP
# ============================================================================

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


# ============================================================================
# INSTALLATION ORCHESTRATOR
# ============================================================================

def install_harness(
    target_dir: Path,
    project_name: str,
    stack_key: str,
    agent_choice: str,
    git_choice: str,
    force: bool = False,
):
    print(f"\n🚀 Installing Agent Docs-as-Code Harness into: {target_dir.resolve()}")
    print(f"   • Project Name: {project_name}")
    print(f"   • Stack: {STACK_PRESETS.get(stack_key, STACK_PRESETS['generic'])['name']}")
    print(f"   • AI Agent configs: {agent_choice}")
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
    for rel_path, content in assets.items():
        if rel_path.startswith("00_Templates/"):
            tpl_name = Path(rel_path).name
            customized = customize_templates_for_stack(tpl_name, content, stack_key, today_str)
            target_file = docs_dir / "00_Templates" / tpl_name
            target_file.write_text(customized, encoding="utf-8")
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

    # 4. Generate starter knowledge base documents
    create_starter_docs(target_dir, project_name, stack_key)
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


# ============================================================================
# INTERACTIVE CLI WIZARD
# ============================================================================

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

    # 2. Technology Stack
    print("\n? Select Technology Stack:")
    print("  [1] iOS / macOS (Swift, SwiftUI, Xcode) [Target Apple Stack]")
    print("  [2] Web / Node (TypeScript, JavaScript, Next.js)")
    print("  [3] Python (Pytest, FastAPI, CLI)")
    print("  [4] .NET / C# (MAUI, ASP.NET, CoreCLR)")
    print("  [5] Generic / Other")
    stack_choice = prompt_user_input("Select [1-5]", default="1")
    stack_map = {"1": "swift", "2": "ts", "3": "python", "4": "dotnet", "5": "generic"}
    stack_key = stack_map.get(stack_choice, "swift")

    # 3. AI Agent Setup
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

    # 4. Git Setup
    print("\n? Git Version Control Setup:")
    print("  [1] Local Git (Initialize repository & commit initial docs) [Recommended]")
    print("  [2] Connect to GitHub (Local commit + setup guidance)")
    print("  [3] Skip Git")
    git_choice_input = prompt_user_input("Select [1-3]", default="1")
    git_map = {"1": "local", "2": "github", "3": "none"}
    git_choice = git_map.get(git_choice_input, "local")

    return project_name, stack_key, agent_choice, git_choice


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

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

  # Install into specific target directory:
  python3 install.py -y --target-dir ../other-project --stack ts
""",
    )

    parser.add_argument("--name", "-n", type=str, help="Project name (default: current directory name)")
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
        project_name, stack_key, agent_choice, git_choice = run_interactive_wizard(args)
    else:
        project_name = args.name or target_dir.name or "MyProject"
        stack_key = args.stack or "swift"
        agent_choice = args.agent or "all"
        git_choice = args.git or "local"

    install_harness(
        target_dir=target_dir,
        project_name=project_name,
        stack_key=stack_key,
        agent_choice=agent_choice,
        git_choice=git_choice,
        force=args.force,
    )


if __name__ == "__main__":
    main()
