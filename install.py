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
