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
