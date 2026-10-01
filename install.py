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

_RULES_BODY = ("## Docs-as-Code (12 Disciplines)\n"
    "Language: {lang}\n"
    "1. Read `SPEC.md`, `docs/00_Index.md`, `docs/Onboarding.md` at session start.\n"
    "2. Kanban: move cards with date `(YYYY-MM-DD)`.\n"
    "3. Roadmap: mark `[x]` + link `[[Specs/.../TASK-XXX|TASK-XXX]]`.\n"
    "4. ADR & Rejected-ADR: log all decisions incl. rejected (`status: rejected`).\n"
    "5. Research: worst-case tests; record discarded prototypes in `RESEARCH-XXX`.\n"
    "6. Devlog: write entry at task/session end.\n"
    "7. Obsidian: wikilinks `[[...]]` + tags.\n"
    "8. Permalinks: NEVER move `TASK-XXX`/`BUG-XXX` to Done/Archive.\n"
    "9. Regression-First: failing test BEFORE fixing any bug.\n"
    "10. QA: checklists `- [ ]` in `docs/05_Testing/`, separate from Plans.\n"
    "11. Graph: 7 Obsidian color groups (White/Purple/Cyan/Yellow/Orange/Red/Green).\n"
    "12. Git: Remote/Local/None + Trunk-Based docs + Feature Branching.\n")


def _rules(doc_lang: str) -> str:
    lang = "Documentation/Devlog **Russian**, code/commits **English**." if doc_lang == "ru" else "All documentation **English**."
    return _RULES_BODY.format(lang=lang)




def generate_gemini_md(project_name: str, stack_key: str, doc_lang: str = "ru") -> str:
    stack = STACK_PRESETS.get(stack_key, STACK_PRESETS["generic"])
    rules = _rules(doc_lang)
    return f"""# GEMINI.md -- Google Antigravity & Gemini CLI Rules for {project_name}

> **Stack:** {stack['name']} | **Full Guidelines:** `AGENTS.md` | **Onboarding:** `docs/Onboarding.md`

{rules}
## 🔄 3-Mode Workflow

**Mode 1 -- Planning (`/kb-plan`) STRICTLY NO CODE CHANGES.** User approval before any plan doc.
**Mode 2 -- Task Spec (`/kb-task`) STRICTLY NO CODE CHANGES.** `[NEW]`/`[MODIFY]`/`[DELETE]` contracts + DoD.
**Mode 3 -- Implementation (`/kb-implement`):**
```bash
{stack['test_cmd']}
python3 scripts/kb_lint.py --path docs
```
Auto-complete: spec->done · Kanban+date · Roadmap `[x]` · Devlog · kb_lint · git push.

Skills: `/kb-plan` `/kb-task` `/kb-implement` `/kb-complete` `/kb-bug` `/kb-adr` `/kb-research` `/kb-lint`
"""


def generate_windsurfrules(project_name: str, stack_key: str, doc_lang: str = "ru") -> str:
    stack = STACK_PRESETS.get(stack_key, STACK_PRESETS["generic"])
    rules = _rules(doc_lang)
    return f"""# .windsurfrules -- Windsurf Cascade AI Rules for {project_name}

Stack: **{stack['name']}** | Build: `{stack['build_cmd']}` | Test: `{stack['test_cmd']}`

{rules}
## 3-Mode Discipline

**Mode 1 (Planning):** STRICTLY NO CODE CHANGES -> `docs/02_Tasks/Plans/PLAN-XXX.md` after user approval.
**Mode 2 (Spec):** STRICTLY NO CODE CHANGES -> `docs/02_Tasks/Specs/<Phase>/TASK-XXX.md` with `[NEW]`/`[MODIFY]`/`[DELETE]`.
**Mode 3 (Implementation):** Code per spec -> `{stack['test_cmd']}` -> `python3 scripts/kb_lint.py --path docs` -> DoD checklist.

Senior Partner: flag risks. Rejected ADRs: `docs/03_Decisions_ADR/` (`status: rejected`).
"""


def generate_clinerules(project_name: str, stack_key: str, doc_lang: str = "ru") -> str:
    stack = STACK_PRESETS.get(stack_key, STACK_PRESETS["generic"])
    rules = _rules(doc_lang)
    return f"""# Cline / Roo Code AI Rules for {project_name}

Stack: **{stack['name']}** | Read `AGENTS.md` and `docs/Onboarding.md` first.

{rules}
## Mode Rules

1. **Mode 1 (Planning):** STRICTLY NO CODE CHANGES. Output: `docs/02_Tasks/Plans/PLAN-XXX.md` after user approval.
2. **Mode 2 (Spec):** STRICTLY NO CODE CHANGES. Output: `docs/02_Tasks/Specs/<Phase>/TASK-XXX.md` with file contracts.
3. **Mode 3 (Implementation):** Code per spec -> `{stack['test_cmd']}` -> `python3 scripts/kb_lint.py --path docs` -> full DoD checklist.

Senior Partner: flag flaws, propose alternatives, document rejected ADRs.
"""


def generate_claude_md(project_name: str, stack_key: str, doc_lang: str = "ru") -> str:
    stack = STACK_PRESETS.get(stack_key, STACK_PRESETS["generic"])
    rules = _rules(doc_lang)
    return f"""# CLAUDE.md -- Claude Code Guidelines for {project_name}

Stack: **{stack['name']}** | Build: `{stack['build_cmd']}` | Test: `{stack['test_cmd']}` | Lint: `python3 scripts/kb_lint.py --path docs`
Read: `AGENTS.md` · `docs/Onboarding.md` · `docs/02_Tasks/Kanban.md` · `docs/02_Tasks/Roadmap.md`

{rules}
## 3-Mode Discipline

- **Mode 1 (Planning):** STRICTLY NO CODE CHANGES. User approval required before writing plan docs.
- **Mode 2 (Spec):** STRICTLY NO CODE CHANGES. `[NEW]`/`[MODIFY]`/`[DELETE]` contracts + DoD + verification plan.
- **Mode 3 (Implementation):** Code per spec -> verify -> DoD (spec+date, Kanban, Roadmap `[x]`, Devlog, kb_lint, git push).

Senior Partner: flag risks and anti-patterns. Document rejected approaches in `docs/03_Decisions_ADR/`.
"""


def generate_cursorrules(project_name: str, stack_key: str, doc_lang: str = "ru") -> str:
    stack = STACK_PRESETS.get(stack_key, STACK_PRESETS["generic"])
    rules = _rules(doc_lang)
    return f"""# Cursor Rules for {project_name}

You are a **Senior Engineering Partner**. Stack: **{stack['name']}**
Read `AGENTS.md` and `docs/Onboarding.md` before any architectural decisions.

{rules}
## 3 Strict Modes

- **Mode 1 (`/kb-plan`):** STRICTLY NO CODE CHANGES -> `docs/02_Tasks/Plans/` (after user approval).
- **Mode 2 (`/kb-task`):** STRICTLY NO CODE CHANGES -> `docs/02_Tasks/Specs/` with `[NEW]`/`[MODIFY]`/`[DELETE]`.
- **Mode 3 (`/kb-implement`):** Code per spec -> `{stack['test_cmd']}` -> `python3 scripts/kb_lint.py --path docs` -> `/kb-complete` (spec, Kanban+date, Roadmap `[x]`, Devlog, git push).

Flag risks, propose alternatives, rejected ADRs: `docs/03_Decisions_ADR/` (`status: rejected`).
"""


def generate_copilot_instructions(project_name: str, stack_key: str, doc_lang: str = "ru") -> str:
    stack = STACK_PRESETS.get(stack_key, STACK_PRESETS["generic"])
    rules = _rules(doc_lang)
    return f"""# GitHub Copilot Instructions for {project_name}

Stack: **{stack['name']}** | Read `AGENTS.md` for full guidelines.

{rules}
## 3-Mode Discipline

- **Mode 1 (Planning):** STRICTLY NO CODE CHANGES. Research/discussion only. Output: `docs/02_Tasks/Plans/PLAN-XXX.md`.
- **Mode 2 (Spec):** STRICTLY NO CODE CHANGES. `[NEW]`/`[MODIFY]`/`[DELETE]` contracts + DoD.
- **Mode 3 (Implementation):** Code per spec -> `{stack['test_cmd']}` -> `python3 scripts/kb_lint.py --path docs` -> DoD checklist.

Permalinks: never move specs/bugs to archive. Regression-First: failing test first. Rejected ADRs: `docs/03_Decisions_ADR/`.
"""


def generate_agents_md(project_name: str, stack_key: str, doc_lang: str = "ru") -> str:
    stack = STACK_PRESETS.get(stack_key, STACK_PRESETS["generic"])
    rules = _rules(doc_lang)
    return f"""# 🤖 AGENTS.md -- AI Agent Guidelines & Operating Modes

> **Project:** {project_name} | **Stack:** {stack['name']}
> **Spec:** [[SPEC|SPEC.md]] | **KB:** [[docs/00_Index|00_Index]] | **Onboarding:** [[docs/Onboarding|Onboarding Guide]]

---

{rules}
---

## 🧠 Senior Engineering Partner Standard

You are a **Senior Engineering Partner**, not a passive assistant:
1. **Critical Review:** Evaluate against best practices ({stack['language']}, Clean Architecture, Zero Dependencies).
2. **Constructive Challenge:** Flag flaws -> justify consequences -> offer 1--2 robust alternatives.
3. **User Confirmation Required (Mode 1 & 2):** NEVER write plan/spec docs without explicit user approval.
4. **Rejected ADRs:** Document discarded directions (`status: rejected`) in `docs/03_Decisions_ADR/`.

---

## 🔄 The 3-Mode Development Cycle

### 🟡 Mode 1 -- Planning (`/kb-plan`)
**🚨 STRICTLY NO CODE CHANGES.** Research, Q&A, critical review. User confirmation before any plan doc.
Output: `docs/02_Tasks/Plans/PLAN-XXX-<slug>.md` + Kanban Backlog card.

### 🟠 Mode 2 -- Task Spec (`/kb-task`)
**🚨 STRICTLY NO CODE CHANGES.** File contracts + verification plan.
Contracts: `[NEW] path/to/file{stack['file_ext']}` / `[MODIFY]` / `[DELETE]` with signatures and DoD.
Output: `docs/02_Tasks/Specs/<Phase>/TASK-XXX-<slug>.md` + Kanban In Progress.

### 🟢 Mode 3 -- Implementation (`/kb-implement` -> `/kb-complete`)
Code strictly per approved spec. Run:
```bash
{stack['build_cmd']}
{stack['test_cmd']}
python3 scripts/kb_lint.py --path docs
```
Completion checklist: spec->done · Kanban->Done(date) · Roadmap `[x]` · Devlog · kb_lint 0 errors · git push.
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
* **Фаза 1: Инициализация и MVP** -- Базовый каркас и проверка сборки.
* **Фаза 2: Основная функциональность** -- Ключевые пользовательские сценарии.
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
1. 🟡 **Режим 1: Планирование** (`/kb-plan`) -- запрет на изменение кода.
2. 🟠 **Режим 2: Спецификация** (`/kb-task`) -- запрет на изменение кода.
3. 🟢 **Режим 3: Реализация** (`/kb-implement`) -- код, тесты, сдача задачи.
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

### [{today_str}] -- Инициализация базы знаний Docs-as-Code
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

<!-- Начните с создания первого плана через команду агента /kb-plan <название> -->

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

## Фаза 1: Первичный MVP и проверка сборки
**Цель:** Создание базового каркаса проекта и проверка сборки/тестов.  
*Сформируйте концептуальный план первой фазы через команду `/kb-plan`.*

---

## 🔮 Перспективные направления (Future Horizons / Later)
*Идеи и гипотезы, находящиеся на стадии осмысления. Прорабатываются через Режим 1 (`/kb-plan`).*

* 💡 **[Идея 1]:** Краткое описание проблемы и ценности.
"""
    roadmap_path.write_text(roadmap_content, encoding="utf-8")



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
        docs_dir / "02_Tasks" / "Specs",
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
    agents_md = generate_agents_md(project_name, stack_key, doc_lang)
    (target_dir / "AGENTS.md").write_text(agents_md, encoding="utf-8")
    print("✅ Created root AGENTS.md (Universal Agent Standard).")

    if agent_choice in ["all", "gemini"]:
        (target_dir / "GEMINI.md").write_text(generate_gemini_md(project_name, stack_key, doc_lang), encoding="utf-8")
        print("✅ Created GEMINI.md (Google Antigravity & Gemini CLI).")

    if agent_choice in ["all", "cline"]:
        (target_dir / ".clinerules").write_text(generate_clinerules(project_name, stack_key, doc_lang), encoding="utf-8")
        print("✅ Created .clinerules (VS Code Cline & Roo Code).")

    if agent_choice in ["all", "claude"]:
        (target_dir / "CLAUDE.md").write_text(generate_claude_md(project_name, stack_key, doc_lang), encoding="utf-8")
        print("✅ Created CLAUDE.md (Claude Code CLI).")

    if agent_choice in ["all", "cursor"]:
        (target_dir / ".cursorrules").write_text(generate_cursorrules(project_name, stack_key, doc_lang), encoding="utf-8")
        print("✅ Created .cursorrules (Cursor IDE).")

    if agent_choice in ["all", "copilot"]:
        copilot_dir = target_dir / ".github"
        copilot_dir.mkdir(parents=True, exist_ok=True)
        (copilot_dir / "copilot-instructions.md").write_text(generate_copilot_instructions(project_name, stack_key, doc_lang), encoding="utf-8")
        print("✅ Created .github/copilot-instructions.md (GitHub Copilot).")

    if agent_choice in ["all", "windsurf"]:
        (target_dir / ".windsurfrules").write_text(generate_windsurfrules(project_name, stack_key, doc_lang), encoding="utf-8")
        print("✅ Created .windsurfrules (Windsurf Cascade).")


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
    print("  [1] All AI Agents (AGENTS.md, GEMINI.md, Cline, Claude, Cursor, Copilot, Windsurf) [Recommended]")
    print("  [2] VS Code Cline & Roo Code (.clinerules)")
    print("  [3] Claude Code CLI (CLAUDE.md)")
    print("  [4] Cursor IDE (.cursorrules)")
    print("  [5] GitHub Copilot (.github/copilot-instructions.md)")
    print("  [6] Google Antigravity & Gemini CLI (GEMINI.md)")
    print("  [7] Windsurf Cascade (.windsurfrules)")
    print("  [8] Universal AGENTS.md only")
    agent_choice_input = prompt_user_input("Select [1-8]", default="1")
    agent_map = {"1": "all", "2": "cline", "3": "claude", "4": "cursor", "5": "copilot", "6": "gemini", "7": "windsurf", "8": "generic"}
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
        choices=["all", "cline", "claude", "cursor", "copilot", "gemini", "windsurf", "generic"],
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
