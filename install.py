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
        "build_cmd": "swift build",
        "test_cmd": "swift test",
        "lint_cmd": "swiftlint",
        "file_ext": ".swift",
        "sample_contract": "```swift\npublic protocol ExampleServiceProtocol: Sendable {\n    func execute() async throws -> String\n}\n```",
        "bug_env": "  - OS: iOS 18.x / macOS 15.x\n  - Toolchain: Xcode 16.x / Swift 6.0",
        "research_quirks": "* **Concurrency & Memory:** ARC weak/unowned, Task isolation, Sendable, BGAppRefresh.",
    },
    "ts": {
        "name": "Web / Node (TypeScript, JavaScript)",
        "language": "TypeScript",
        "build_cmd": "npm run build",
        "test_cmd": "npm test",
        "lint_cmd": "npm run lint",
        "file_ext": ".ts",
        "sample_contract": "```typescript\nexport interface ExampleService {\n  execute(signal?: AbortSignal): Promise<string>;\n}\n```",
        "bug_env": "  - OS: macOS / Linux / Windows\n  - Runtime: Node.js 20.x / 22.x",
        "research_quirks": "* **Event Loop & Memory:** Microtasks, uncleaned event listeners, SSR hydration.",
    },
    "python": {
        "name": "Python (Standard / Pytest / FastAPI)",
        "language": "Python",
        "build_cmd": "python -m py_compile scripts/*.py",
        "test_cmd": "pytest",
        "lint_cmd": "ruff check .",
        "file_ext": ".py",
        "sample_contract": "```python\nclass ExampleService:\n    def execute(self) -> str:\n        return \"OK\"\n```",
        "bug_env": "  - OS: macOS / Linux / Windows\n  - Python: 3.10+ / 3.12+",
        "research_quirks": "* **Async & Types:** Asyncio event loop blocking, GIL limitations, type hinting.",
    },
    "dotnet": {
        "name": ".NET / C# (ASP.NET, MAUI, Console)",
        "language": "C#",
        "build_cmd": "dotnet build",
        "test_cmd": "dotnet test",
        "lint_cmd": "dotnet format",
        "file_ext": ".cs",
        "sample_contract": "```csharp\npublic interface IExampleService {\n    Task<string> ExecuteAsync(CancellationToken ct = default);\n}\n```",
        "bug_env": "  - OS: Windows 11 / macOS / Linux\n  - SDK: .NET 8.0 / 9.0",
        "research_quirks": "* **Async & GC:** ConfigureAwait(false), ThreadPool starvation, IDisposable pattern.",
    },
    "generic": {
        "name": "Generic / Other Technology Stack",
        "language": "Source Code",
        "build_cmd": "make build",
        "test_cmd": "make test",
        "lint_cmd": "make lint",
        "file_ext": ".src",
        "sample_contract": "```text\nfunction execute(): Result\n```",
        "bug_env": "  - OS: macOS / Linux / Windows\n  - Runtime: Project runtime",
        "research_quirks": "* **Concurrency & Resources:** Thread safety, race conditions, memory lifecycle.",
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
        for sname in ["kb_lint.py", "kb_release.py"]:
            sfile = scripts_dir / sname
            if sfile.is_file():
                assets[f"scripts/{sname}"] = sfile.read_text(encoding="utf-8")
        if skills_dir.is_dir():
            for sdir in sorted([d for d in skills_dir.iterdir() if d.is_dir()]):
                skill_md = sdir / "SKILL.md"
                if skill_md.is_file():
                    assets[f".agents/skills/{sdir.name}/SKILL.md"] = skill_md.read_text(encoding="utf-8")
        workflows_dir = repo_root / ".github" / "workflows"
        if workflows_dir.is_dir():
            for wf in workflows_dir.glob("*.yml"):
                assets[f".github/workflows/{wf.name}"] = wf.read_text(encoding="utf-8")
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




_3MODES = (
    "## 🔄 3-Mode Discipline & Workflow\n\n"
    "**Mode 1 -- Planning (`/kb-plan`):** STRICTLY NO CODE CHANGES. User approval before writing plan docs.\n"
    "**Mode 2 -- Task Spec (`/kb-task`):** STRICTLY NO CODE CHANGES. `[NEW]`/`[MODIFY]`/`[DELETE]` contracts + DoD.\n"
    "**Mode 3 -- Implementation (`/kb-implement`):\n"
    "```bash\n{test_cmd}\npython3 scripts/kb_lint.py --path docs\n```\n"
    "Auto-complete: spec->done · Kanban+date · Roadmap `[x]` · Devlog · kb_lint · git push.\n\n"
    "Anti-Echo: NEVER reprint entire files in chat; emit link + 3-5 bullets + next step.\n"
    "Senior Partner: flag risks, propose alternatives. Rejected ADRs: `docs/03_Decisions_ADR/` (`status: rejected`).\n"
)


def _gen_rule(title: str, p: str, s: str, l: str, extra: str = "", tail: str = "") -> str:
    st = STACK_PRESETS.get(s, STACK_PRESETS["generic"])
    return f"# {title} for {p}\n\nStack: **{st['name']}**{extra}\n\n{_rules(l)}\n{_3MODES.format(test_cmd=st['test_cmd'])}{tail}"


def generate_gemini_md(p: str, s: str, l: str = "ru") -> str:
    return _gen_rule("GEMINI.md -- Google Antigravity & Gemini CLI Rules", p, s, l, " | Full Guidelines: `AGENTS.md`", "\nSkills: `/kb-plan` `/kb-task` `/kb-implement` `/kb-complete` `/kb-bug` `/kb-adr` `/kb-research` `/kb-release` `/kb-lint`\n")


def generate_windsurfrules(p: str, s: str, l: str = "ru") -> str:
    st = STACK_PRESETS.get(s, STACK_PRESETS["generic"])
    return _gen_rule(".windsurfrules -- Windsurf Cascade AI Rules", p, s, l, f" | Build: `{st['build_cmd']}` | Test: `{st['test_cmd']}`")


def generate_clinerules(p: str, s: str, l: str = "ru") -> str:
    return _gen_rule("Cline / Roo Code AI Rules", p, s, l, " | Read `AGENTS.md` and `docs/Onboarding.md` first.")


def generate_claude_md(p: str, s: str, l: str = "ru") -> str:
    st = STACK_PRESETS.get(s, STACK_PRESETS["generic"])
    return _gen_rule("CLAUDE.md -- Claude Code Guidelines", p, s, l, f" | Build: `{st['build_cmd']}` | Test: `{st['test_cmd']}` | Lint: `python3 scripts/kb_lint.py --path docs`")


def generate_cursorrules(p: str, s: str, l: str = "ru") -> str:
    return _gen_rule("Cursor Rules", p, s, l, "\nYou are a **Senior Engineering Partner**. Read `AGENTS.md`.")


def generate_copilot_instructions(p: str, s: str, l: str = "ru") -> str:
    return _gen_rule("GitHub Copilot Instructions", p, s, l, " | Read `AGENTS.md` for full guidelines.")


def generate_agents_md(project_name: str, stack_key: str, doc_lang: str = "ru") -> str:
    stack = STACK_PRESETS.get(stack_key, STACK_PRESETS["generic"])
    rules = _rules(doc_lang)
    return f"""# 🤖 AGENTS.md -- AI Agent Guidelines & Operating Modes

> **Project:** {project_name} | **Stack:** {stack['name']}
> **Spec:** [[SPEC|SPEC.md]] | **KB:** [[docs/00_Index|00_Index]] | **Onboarding:** [[docs/Onboarding|Onboarding Guide]]

---

{rules}
### 🎨 Obsidian Graph Color Scheme & Tagging
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
   - Clickable file link: `[FileName](file:///absolute/path/to/file)`
   - Concise 3–5 bullet summary of what changed and key architectural decisions
   - Next actionable step or prompt for confirmation

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
        contract_marker = "```python\n# Ключевой контракт\n```"
        if contract_marker in content:
            content = content.replace(contract_marker, stack["sample_contract"])
        contract_target = "```csharp\n// Пример ключевого интерфейса или фрагмента контракта\npublic interface IExampleService\n{\n    Task ExecuteAsync(CancellationToken ct);\n}\n```"
        if contract_target in content:
            content = content.replace(contract_target, stack["sample_contract"])
        # Replace build & test command
        content = content.replace("<!-- команда сборки, Exit code 0 -->", stack["build_cmd"])
        content = content.replace("<!-- команда запуска тестов, 100% pass -->", stack["test_cmd"])
        content = content.replace("`dotnet build` или `./gradlew test`", f"`{stack['build_cmd']}`")
        content = content.replace("`dotnet test`", f"`{stack['test_cmd']}`")
        content = content.replace("path/to/file.ext", f"path/to/file{stack['file_ext']}")
        content = content.replace("Path/To/NewFile.cs", f"Path/To/NewFile{stack['file_ext']}")
        content = content.replace("Path/To/ExistingFile.kt", f"Path/To/ExistingFile{stack['file_ext']}")
        content = content.replace("Path/To/OldFile.cs", f"Path/To/OldFile{stack['file_ext']}")

    elif template_name == "TEMPLATE_BUG.md":
        # Replace bug environment and test paths
        env_marker = "* **Окружение:** <!-- ОС, версия, стек -->"
        if env_marker in content:
            content = content.replace(env_marker, f"* **Окружение:**\n{stack['bug_env']}")
        legacy_env = "  - ОС: Windows 11 Build / Android Version\n  - Стек: .NET SDK / Gradle Version / Runtime\n  - Сеть/Конфигурация: Localhost / Wi-Fi / VPN"
        if legacy_env in content:
            content = content.replace(legacy_env, stack["bug_env"])
        content = content.replace("tests/path/to/test_regression.ext", f"tests/path/to/test_regression{stack['file_ext']}")
        content = content.replace("path/to/file.ext", f"path/to/file{stack['file_ext']}")
        content = content.replace("path/to/file.cs", f"path/to/file{stack['file_ext']}")
        content = content.replace("tests/Path/To/RegressionTest.cs", f"tests/Path/To/RegressionTest{stack['file_ext']}")

    elif template_name == "TEMPLATE_RESEARCH.md":
        # Replace sample research code and platform quirks
        quirks_marker = "<!-- Поведение подсистемы в фоне, энергопотребление, жизненный цикл, лимиты -->"
        if quirks_marker in content:
            content = content.replace(quirks_marker, stack["research_quirks"])
        legacy_quirks = "* **Поведение в фоне и энергопотребление (Doze / WakeLock):** ...\n* **Поведение при сбоях сети и роуминге:** ...\n* **Потокобезопасность и нагрузка на память/CPU:** ...\n* **Ограничения прав и безопасности ОС:** ..."
        if legacy_quirks in content:
            content = content.replace(legacy_quirks, stack["research_quirks"])
        content = content.replace("```python\n# Экспериментальный код или бенчмарк\n```", stack["sample_contract"])
        content = content.replace("```kotlin\n// Пример проверочного кода или сниппета решения\n```", stack["sample_contract"])

    return content


def detect_project_stack(target_dir: Path) -> str:
    """
    Эвристический детект стека по маркерным файлам в корне проекта.
    Возвращает ключ стека из STACK_PRESETS ('swift', 'ts', 'python', 'dotnet', 'generic').
    """
    if not target_dir.is_dir():
        return "generic"
    if (target_dir / "Package.swift").is_file():
        return "swift"
    if (target_dir / "package.json").is_file():
        return "ts"
    if any((target_dir / f).is_file() for f in ["pyproject.toml", "requirements.txt", "Pipfile", "setup.py"]):
        return "python"
    try:
        if list(target_dir.glob("*.sln")) or list(target_dir.glob("*.csproj")):
            return "dotnet"
    except Exception:
        pass
    return "generic"


def handle_readme(target_dir: Path, project_name: str, doc_lang: str = "ru"):
    readme_path = target_dir / "README.md"
    if doc_lang == "en":
        docs_block = """

---

## 🧠 AI Agent Documentation & Discipline (Docs-as-Code)
This project uses the Docs-as-Code knowledge base and strict 3-mode workflow for AI agents:
* **Documentation Vault:** `docs/` (open as Obsidian Vault).
* **Universal Agent Rules:** [AGENTS.md](AGENTS.md).
* **Knowledge Map (MOC):** [docs/00_Index.md](docs/00_Index.md).
* **Integrity Linter:** `python scripts/kb_lint.py --path docs`.
"""
    else:
        docs_block = """

---

## 🧠 Документация и дисциплина AI-агентов (Docs-as-Code)
В проекте развернута база знаний Docs-as-Code и строгий 3-режимный регламент работы с AI-агентами:
* **Каталог документации:** `docs/` (открывается как Vault в Obsidian).
* **Главный регламент агентов:** [AGENTS.md](AGENTS.md).
* **Карта заметок:** [docs/00_Index.md](docs/00_Index.md).
* **Проверка базы знаний:** `python scripts/kb_lint.py --path docs`.
"""
    if readme_path.is_file():
        content = readme_path.read_text(encoding="utf-8")
        if "AGENTS.md" not in content and "Docs-as-Code" not in content:
            readme_path.write_text(content.rstrip() + "\n" + docs_block, encoding="utf-8")
            print("📝 Appended Docs-as-Code section to existing README.md.")
    else:
        new_content = f"# {project_name}\n\nProject repository.\n{docs_block}"
        readme_path.write_text(new_content, encoding="utf-8")
        print("📝 Created root README.md with Docs-as-Code section.")


def handle_gitignore(target_dir: Path):
    gitignore_path = target_dir / ".gitignore"
    obsidian_rules = """
# Obsidian Workspace (preserve graph.json)
.obsidian/*
!.obsidian/graph.json
"""
    if not gitignore_path.exists():
        gitignore_content = """# System & IDE
.DS_Store
Thumbs.db
.idea/
.vscode/*
!.vscode/settings.json
""" + obsidian_rules
        gitignore_path.write_text(gitignore_content.strip() + "\n", encoding="utf-8")
        print("📁 Created .gitignore (with Obsidian graph retention rules).")
    else:
        content = gitignore_path.read_text(encoding="utf-8")
        if ".obsidian" not in content:
            gitignore_path.write_text(content.rstrip() + "\n" + obsidian_rules, encoding="utf-8")
            print("📁 Appended Obsidian retention rules to existing .gitignore.")


def create_starter_docs(target_dir: Path, project_name: str, stack_key: str, assets: dict = None, force: bool = False):
    stack = STACK_PRESETS.get(stack_key, STACK_PRESETS["generic"])
    today_str = date.today().isoformat()
    docs_dir = target_dir / "docs"

    # 1. SPEC.md (Root)
    spec_path = target_dir / "SPEC.md"
    if not spec_path.exists() or force:
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
    if not index_path.exists() or force:
        tpl = (assets or {}).get("00_Templates/TEMPLATE_INDEX.md", "")
        index_content = tpl.replace("[Название Проекта]", project_name).replace("2026-09-19", today_str) if tpl else f"# {project_name}\n"
        index_path.write_text(index_content, encoding="utf-8")

    # 3. docs/Onboarding.md
    onboarding_path = docs_dir / "Onboarding.md"
    if not onboarding_path.exists() or force:
        tpl = (assets or {}).get("00_Templates/TEMPLATE_ONBOARDING.md", "")
        onboarding_content = (
            tpl.replace("[Название Проекта]", project_name)
            .replace("2026-09-19", today_str)
            .replace("dotnet build", stack["build_cmd"])
            .replace("dotnet test", stack["test_cmd"])
        ) if tpl else f"# Onboarding: {project_name}\n"
        onboarding_path.write_text(onboarding_content, encoding="utf-8")

    # 4. docs/Devlog.md
    devlog_path = docs_dir / "Devlog.md"
    if not devlog_path.exists() or force:
        tpl = (assets or {}).get("00_Templates/TEMPLATE_DEVLOG.md", "")
        devlog_content = tpl.replace("2026-09-19", today_str) if tpl else f"# Devlog: {project_name}\n"
        devlog_path.write_text(devlog_content, encoding="utf-8")

    # 5. docs/02_Tasks/Kanban.md
    kanban_path = docs_dir / "02_Tasks" / "Kanban.md"
    if not kanban_path.exists() or force:
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
    if not roadmap_path.exists() or force:
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
    handle_gitignore(target_dir)

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


def deploy_ci_workflow(target_dir: Path, ci_provider: str = "none", assets: dict = None):
    if ci_provider == "github":
        wf_dir = target_dir / ".github" / "workflows"
        wf_dir.mkdir(parents=True, exist_ok=True)

        # 1. kb-lint.yml
        wf_lint = wf_dir / "kb-lint.yml"
        if assets and ".github/workflows/kb-lint.yml" in assets:
            wf_lint.write_text(assets[".github/workflows/kb-lint.yml"], encoding="utf-8")
        else:
            wf_lint_content = (
                "name: Docs-as-Code Knowledge Base Audit\n\n"
                "on:\n"
                "  push:\n"
                "    branches: [ main, master ]\n"
                "  pull_request:\n"
                "    branches: [ main, master ]\n\n"
                "jobs:\n"
                "  kb-lint:\n"
                "    runs-on: ubuntu-latest\n"
                "    steps:\n"
                "      - name: Checkout repository\n"
                "        uses: actions/checkout@v4\n\n"
                "      - name: Set up Python\n"
                "        uses: actions/setup-python@v5\n"
                "        with:\n"
                "          python-version: '3.11'\n\n"
                "      - name: Run Knowledge Base Linter\n"
                "        run: |\n"
                "          python scripts/kb_lint.py --path docs\n"
            )
            wf_lint.write_text(wf_lint_content, encoding="utf-8")

        # 2. release.yml
        wf_release = wf_dir / "release.yml"
        if assets and ".github/workflows/release.yml" in assets:
            wf_release.write_text(assets[".github/workflows/release.yml"], encoding="utf-8")
        else:
            wf_release_content = (
                "name: Release Automation\n\n"
                "on:\n"
                "  push:\n"
                "    tags:\n"
                "      - 'v*'\n\n"
                "permissions:\n"
                "  contents: write\n\n"
                "jobs:\n"
                "  build-and-release:\n"
                "    name: Build & Publish Release\n"
                "    runs-on: ubuntu-latest\n"
                "    steps:\n"
                "      - name: Checkout Repository\n"
                "        uses: actions/checkout@v4\n"
                "        with:\n"
                "          fetch-depth: 0\n\n"
                "      - name: Set up Python\n"
                "        uses: actions/setup-python@v5\n"
                "        with:\n"
                "          python-version: '3.11'\n\n"
                "      - name: Verify Knowledge Base Integrity\n"
                "        run: |\n"
                "          python scripts/kb_lint.py --path docs\n\n"
                "      - name: Execute Project Build Hook\n"
                "        run: |\n"
                "          if [ -f \"scripts/build_release.sh\" ]; then\n"
                "            bash scripts/build_release.sh\n"
                "          elif [ -f \"scripts/build_release.py\" ]; then\n"
                "            python scripts/build_release.py\n"
                "          elif [ -f \"package.json\" ]; then\n"
                "            npm ci && npm run build\n"
                "          fi\n\n"
                "      - name: Inspect Artifacts & Verify Checksums\n"
                "        id: release_meta\n"
                "        run: |\n"
                "          mkdir -p dist\n"
                "          python scripts/kb_release.py --version ${{ github.ref_name }} --ci-mode\n\n"
                "      - name: Publish GitHub Release\n"
                "        uses: softprops/action-gh-release@v2\n"
                "        if: startsWith(github.ref, 'refs/tags/')\n"
                "        with:\n"
                "          name: Release ${{ github.ref_name }}\n"
                "          draft: false\n"
                "          prerelease: false\n"
                "          body_path: dist/RELEASE_NOTES.md\n"
                "          files: |\n"
                "            dist/*\n"
            )
            wf_release.write_text(wf_release_content, encoding="utf-8")
        print("✅ Deployed GitHub Actions CI workflows (.github/workflows/kb-lint.yml, release.yml).")


# --- INSTALLATION ORCHESTRATOR & INFRASTRUCTURE HELPERS ---

def get_agent_rule_specs(target_dir: Path, project_name: str, stack_key: str, doc_lang: str):
    return [
        ("all", target_dir / "AGENTS.md", generate_agents_md(project_name, stack_key, doc_lang), "root AGENTS.md (Universal Agent Standard)"),
        ("gemini", target_dir / "GEMINI.md", generate_gemini_md(project_name, stack_key, doc_lang), "GEMINI.md (Google Antigravity & Gemini CLI)"),
        ("cline", target_dir / ".clinerules", generate_clinerules(project_name, stack_key, doc_lang), ".clinerules (VS Code Cline & Roo Code)"),
        ("claude", target_dir / "CLAUDE.md", generate_claude_md(project_name, stack_key, doc_lang), "CLAUDE.md (Claude Code CLI)"),
        ("cursor", target_dir / ".cursorrules", generate_cursorrules(project_name, stack_key, doc_lang), ".cursorrules (Cursor IDE)"),
        ("copilot", target_dir / ".github" / "copilot-instructions.md", generate_copilot_instructions(project_name, stack_key, doc_lang), ".github/copilot-instructions.md (GitHub Copilot)"),
        ("windsurf", target_dir / ".windsurfrules", generate_windsurfrules(project_name, stack_key, doc_lang), ".windsurfrules (Windsurf Cascade)"),
    ]


def deploy_infrastructure(target_dir: Path, assets: dict, stack_key: str, today_str: str) -> tuple:
    docs_dir = target_dir / "docs"
    tpl_dir = docs_dir / "00_Templates"
    tpl_dir.mkdir(parents=True, exist_ok=True)
    tpl_count = skills_count = 0

    for rel_path, content in assets.items():
        if rel_path.startswith("00_Templates/"):
            tpl_name = Path(rel_path).name
            customized = customize_templates_for_stack(tpl_name, content, stack_key, today_str)
            (tpl_dir / tpl_name).write_text(customized, encoding="utf-8")
            tpl_count += 1
        elif rel_path.startswith(".agents/skills/"):
            target_file = target_dir / rel_path
            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_text(content, encoding="utf-8")
            skills_count += 1
        elif rel_path == ".obsidian/graph.json":
            target_file = docs_dir / ".obsidian" / "graph.json"
            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_text(content, encoding="utf-8")
        elif rel_path.startswith("scripts/"):
            target_file = target_dir / rel_path
            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_text(content, encoding="utf-8")
            try:
                target_file.chmod(0o755)
            except Exception:
                pass
    return tpl_count, skills_count


def run_linter_audit(target_dir: Path, docs_dir: Path):
    kb_lint_path = target_dir / "scripts" / "kb_lint.py"
    if kb_lint_path.is_file():
        print("\n🔍 Running knowledge base audit with kb_lint.py...")
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


def install_harness(
    target_dir: Path,
    project_name: str,
    stack_key: str,
    agent_choice: str,
    git_choice: str,
    doc_lang: str = "ru",
    force: bool = False,
    ci_choice: str = "none",
):
    print(f"\n🚀 Installing Agent Docs-as-Code Harness into: {target_dir.resolve()}")
    print(f"   • Project Name: {project_name}")
    print(f"   • Stack: {STACK_PRESETS.get(stack_key, STACK_PRESETS['generic'])['name']}")
    print(f"   • AI Agent configs: {agent_choice}")
    print(f"   • Documentation language: {doc_lang}")
    print(f"   • Git mode: {git_choice}")
    if ci_choice != "none":
        print(f"   • CI mode: {ci_choice}")
    print()

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
        docs_dir / "02_Tasks" / "Releases",
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
    tpl_count, skills_count = deploy_infrastructure(target_dir, assets, stack_key, today_str)
    print(f"✅ Deployed {tpl_count} templates and Obsidian graph configuration.")
    print("✅ Deployed scripts/kb_lint.py and scripts/kb_release.py.")
    if skills_count > 0:
        print(f"✅ Deployed {skills_count} AI agent skills (.agents/skills/).")

    # 4. Generate starter knowledge base documents
    create_starter_docs(target_dir, project_name, stack_key, assets=assets, force=force)
    print("✅ Created starter knowledge base docs (SPEC.md, 00_Index.md, Onboarding.md, Kanban.md, Roadmap.md, Devlog.md).")

    # 4.1. Handle README.md and .gitignore (non-destructive)
    handle_readme(target_dir, project_name, doc_lang)
    handle_gitignore(target_dir)

    # 5. Generate Agent rule files
    for agent_key, rule_path, content, desc in get_agent_rule_specs(target_dir, project_name, stack_key, doc_lang):
        if agent_choice == "all" or agent_choice == agent_key or agent_key == "all":
            rule_path.parent.mkdir(parents=True, exist_ok=True)
            rule_path.write_text(content, encoding="utf-8")
            print(f"✅ Created {desc}.")

    # 6. Verify knowledge base integrity with kb_lint.py
    run_linter_audit(target_dir, docs_dir)

    # 6.1. CI setup
    deploy_ci_workflow(target_dir, ci_choice, assets=assets)

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


# --- SAFE HARNESS UPDATE ---

def record_devlog_update(docs_dir: Path, today_str: str, doc_lang: str = "ru"):
    devlog_path = docs_dir / "Devlog.md"
    if not devlog_path.is_file():
        return
    content = devlog_path.read_text(encoding="utf-8")
    if doc_lang == "en":
        entry = (
            f"### [{today_str}] — Docs-as-Code Harness Components Update (`install.py --update`)\n"
            "- **What was updated:**\n"
            "  - Note templates in `docs/00_Templates/` refreshed to latest version.\n"
            "  - Standalone utilities (`scripts/kb_lint.py`, `scripts/kb_release.py`) updated.\n"
            "  - AI agent skills in `.agents/skills/` synchronized.\n"
            "  - Obsidian graph configuration `docs/.obsidian/graph.json` refreshed.\n"
            "- **Integrity verification:**\n"
            "  - Link integrity audit performed with `kb_lint.py`.\n\n---\n\n"
        )
    else:
        entry = (
            f"### [{today_str}] — Обновление компонентов Docs-as-Code Harness (`install.py --update`)\n"
            "- **Что обновлено:**\n"
            "  - Шаблоны заметок в `docs/00_Templates/` обновлены до актуальной версии.\n"
            "  - Автономный линтер и утилиты релизов в `scripts/` обновлены.\n"
            "  - Скиллы AI-агентов в `.agents/skills/` актуализированы.\n"
            "  - Конфигурация графа `docs/.obsidian/graph.json` актуализирована.\n"
            "- **Проверка:**\n"
            "  - Проведен контрольный аудит целостности ссылок через `kb_lint.py`.\n\n---\n\n"
        )
    if "### [" in content:
        idx = content.find("### [")
        new_content = content[:idx] + entry + content[idx:]
    else:
        new_content = content.rstrip() + "\n\n---\n\n" + entry
    devlog_path.write_text(new_content, encoding="utf-8")
    print("📝 Appended update record to docs/Devlog.md.")


def update_agent_rules_safe(target_dir: Path, project_name: str, stack_key: str, doc_lang: str, backup: bool = True):
    for _, rule_path, new_content, _ in get_agent_rule_specs(target_dir, project_name, stack_key, doc_lang):
        if rule_path.is_file():
            existing = rule_path.read_text(encoding="utf-8")
            if existing.strip() != new_content.strip():
                if backup:
                    bak = rule_path.with_name(rule_path.name + ".bak")
                    bak.write_text(existing, encoding="utf-8")
                    print(f"⚠️ Backed up modified {rule_path.name} to {bak.name} and updated to latest version.")
                rule_path.write_text(new_content, encoding="utf-8")
            else:
                print(f"ℹ️ {rule_path.name} is already up to date.")


def update_harness(
    target_dir: Path,
    assets: dict = None,
    stack_key: str = None,
    doc_lang: str = None,
    project_name: str = None,
    ci_provider: str = None,
    backup: bool = True,
) -> int:
    docs_dir = target_dir / "docs"
    if not (docs_dir / "00_Index.md").is_file():
        print(f"❌ Error: 'docs/00_Index.md' not found in {target_dir.resolve()}.")
        print("   This directory does not appear to be an initialized Agent Docs-as-Code project.")
        return 1

    print(f"\n🔄 Updating Agent Docs-as-Code Harness components in: {target_dir.resolve()}")

    if assets is None:
        assets = unpack_assets()

    today_str = date.today().isoformat()

    # Detect project attributes if not specified
    if not project_name:
        spec_path = target_dir / "SPEC.md"
        if spec_path.is_file():
            spec_txt = spec_path.read_text(encoding="utf-8")
            m = re.search(r'title:\s*["\']?(?:Мастер-спецификация:\s*)?([^"\'\n]+)', spec_txt)
            if m:
                project_name = m.group(1).strip()
        if not project_name:
            project_name = target_dir.name or "Project"

    if not stack_key or stack_key == "auto":
        stack_key = detect_project_stack(target_dir)

    if not doc_lang:
        agents_path = target_dir / "AGENTS.md"
        if agents_path.is_file() and ("Russian" in agents_path.read_text(encoding="utf-8") or "Русский" in agents_path.read_text(encoding="utf-8")):
            doc_lang = "ru"
        else:
            doc_lang = "en"

    print(f"   • Project: {project_name}")
    print(f"   • Stack: {STACK_PRESETS.get(stack_key, STACK_PRESETS['generic'])['name']}")
    print(f"   • Language: {doc_lang}\n")

    # Ensure Releases directory exists (safely preserving any existing releases)
    releases_dir = docs_dir / "02_Tasks" / "Releases"
    releases_dir.mkdir(parents=True, exist_ok=True)
    if not list(releases_dir.glob("*")):
        (releases_dir / ".gitkeep").touch()

    # Refresh templates, skills, linter, graph
    tpl_count, skills_count = deploy_infrastructure(target_dir, assets, stack_key, today_str)
    print(f"✅ Refreshed {tpl_count} templates and Obsidian graph configuration.")
    print("✅ Refreshed scripts/kb_lint.py and scripts/kb_release.py.")
    if skills_count > 0:
        print(f"✅ Refreshed {skills_count} skills in .agents/skills/.")

    # Safe update of agent rules with .bak
    update_agent_rules_safe(target_dir, project_name, stack_key, doc_lang, backup=backup)

    # Record update in docs/Devlog.md
    record_devlog_update(docs_dir, today_str, doc_lang)

    # Refresh CI workflow if requested or already existing
    if ci_provider == "github" or (target_dir / ".github" / "workflows" / "kb-lint.yml").is_file():
        deploy_ci_workflow(target_dir, "github", assets=assets)

    # Run kb_lint audit
    run_linter_audit(target_dir, docs_dir)

    print("\n" + "=" * 70)
    print("🎉 Docs-as-Code Harness components successfully updated to latest version!")
    print("=" * 70 + "\n")
    return 0


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
    detected_stack = detect_project_stack(target_dir)
    if args.stack and args.stack != "auto":
        detected_stack = args.stack
    stack_choice_map = {"swift": "1", "ts": "2", "python": "3", "dotnet": "4", "generic": "5"}
    detected_num = stack_choice_map.get(detected_stack, "1")

    print("\n? Select Technology Stack:")
    print(f"  [1] iOS / macOS (Swift, SwiftUI, Xcode) [Target Apple Stack]{' (Detected)' if detected_stack == 'swift' else ''}")
    print(f"  [2] Web / Node (TypeScript, JavaScript, Next.js){' (Detected)' if detected_stack == 'ts' else ''}")
    print(f"  [3] Python (Pytest, FastAPI, CLI){' (Detected)' if detected_stack == 'python' else ''}")
    print(f"  [4] .NET / C# (MAUI, ASP.NET, CoreCLR){' (Detected)' if detected_stack == 'dotnet' else ''}")
    print(f"  [5] Generic / Other{' (Detected)' if detected_stack == 'generic' else ''}")
    stack_choice = prompt_user_input("Select [1-5]", default=detected_num)
    stack_map = {"1": "swift", "2": "ts", "3": "python", "4": "dotnet", "5": "generic"}
    stack_key = stack_map.get(stack_choice, detected_stack)

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

    # 6. CI Setup
    print("\n? Continuous Integration (CI) Workflow:")
    print("  [1] None (Local-Only / Skip CI) [Default]")
    print("  [2] GitHub Actions (.github/workflows/kb-lint.yml)")
    ci_choice_input = prompt_user_input("Select [1-2]", default="1")
    ci_map = {"1": "none", "2": "github"}
    ci_choice = ci_map.get(ci_choice_input, "none")

    return project_name, stack_key, agent_choice, git_choice, doc_lang, ci_choice


# --- MAIN ENTRY POINT ---

def main():
    parser = argparse.ArgumentParser(
        description="Agent Docs-as-Code Harness Installer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 install.py
  python3 install.py -y -n MyApp -s swift -a all -g local
  python3 install.py -y -d ../project -s ts -l en --ci github
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
        choices=["auto", "swift", "ts", "python", "dotnet", "generic"],
        default=None,
        help="Target technology stack preset (default: auto)",
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
        "--ci",
        choices=["github", "none"],
        default=None,
        help="Continuous Integration workflow to deploy (default: none)",
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
    parser.add_argument(
        "--update", "-u",
        action="store_true",
        help="Update harness infrastructure (templates, linter, skills, graph) safely in existing project",
    )

    args = parser.parse_args()
    target_dir = Path(args.target_dir).resolve()

    # Handle --update mode directly
    if args.update:
        exit_code = update_harness(
            target_dir=target_dir,
            stack_key=args.stack,
            doc_lang=args.doc_lang,
            project_name=args.name,
            ci_provider=args.ci,
        )
        sys.exit(exit_code)

    # Determine whether to run interactively
    is_interactive = not args.non_interactive and (sys.stdin.isatty() or os.name == "nt" or os.path.exists("/dev/tty"))

    # If flags were all explicitly passed, run directly
    if args.stack and args.agent and args.git and args.name:
        is_interactive = False

    if is_interactive:
        project_name, stack_key, agent_choice, git_choice, doc_lang, ci_choice = run_interactive_wizard(args)
    else:
        project_name = args.name or target_dir.name or "MyProject"
        stack_key = detect_project_stack(target_dir) if (not args.stack or args.stack == "auto") else args.stack
        agent_choice = args.agent or "all"
        git_choice = args.git or "local"
        doc_lang = args.doc_lang or "ru"
        ci_choice = args.ci or "none"

    install_harness(
        target_dir=target_dir,
        project_name=project_name,
        stack_key=stack_key,
        agent_choice=agent_choice,
        git_choice=git_choice,
        doc_lang=doc_lang,
        force=args.force,
        ci_choice=ci_choice,
    )


if __name__ == "__main__":
    main()
