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
    "undecided": {
        "name": "Undecided / Idea-First Research",
        "language": "TBD (Determined in Mode 0 via /kb-research)",
        "build_cmd": "echo 'No build command configured yet (run /kb-research)'",
        "test_cmd": "echo 'No test command configured yet (run /kb-research)'",
        "lint_cmd": "echo 'No lint command configured yet (run /kb-research)'",
        "file_ext": ".txt",
        "sample_contract": "# Архитектурный контракт и интерфейсы будут определены по итогам RESEARCH-001\n",
        "bug_env": "  - ОС: TBD\n  - Стек: TBD (в процессе исследования)\n",
        "research_quirks": "* **Архитектурные ограничения и критерии выбора стека:** будут зафиксированы в ADR-0001.",
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
    "1. Read `SPEC.md`, `docs/00_Index.md`, `docs/Onboarding.md` at session start; sync `SPEC.md`/`README.md` (Living Spec).\n"
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
    "Auto-complete: spec->done · Living Spec sync · Kanban+date · Roadmap `[x]` · Devlog · kb_lint · git push.\n\n"
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


def create_starter_docs(target_dir: Path, project_name: str, stack_key: str, assets: dict = None, force: bool = False, idea: str = None):
    stack = STACK_PRESETS.get(stack_key, STACK_PRESETS["generic"])
    today_str = date.today().isoformat()
    docs_dir = target_dir / "docs"

    # 1. SPEC.md (Root)
    spec_path = target_dir / "SPEC.md"
    if not spec_path.exists() or force:
        is_undecided = (stack_key == "undecided")
        spec_status = "discovery" if is_undecided else "active"
        if is_undecided:
            concept_text = idea.strip() if idea else "*Краткое описание продуктовой идеи, решаемой проблемы и целевой аудитории (зафиксировано для исследования в Режиме 0).*"
            arch_text = (
                "* **Статус стека:** Не определен. Требуется провести первичное исследование через команду агента: `/kb-research выбор-стека-и-архитектуры`.\n"
                "* **Сборка проекта:** `TBD (после завершения RESEARCH-001)`\n"
                "* **Запуск тестов:** `TBD (после завершения RESEARCH-001)`\n"
                "* **Проверка базы знаний:** `python3 scripts/kb_lint.py --path docs`"
            )
        else:
            concept_text = idea.strip() if idea else "*Краткое описание назначения проекта, решаемой проблемы и целевой аудитории.*"
            arch_text = (
                f"* **Платформа и технологии:** {stack['name']} ({stack['language']})\n"
                f"* **Сборка проекта:** `{stack['build_cmd']}`\n"
                f"* **Запуск тестов:** `{stack['test_cmd']}`\n"
                f"* **Проверка базы знаний:** `python3 scripts/kb_lint.py --path docs`"
            )

        spec_content = f"""---
id: SPEC
title: "Мастер-спецификация: {project_name}"
status: {spec_status}
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
{concept_text}

---

## 2. Архитектура и стек технологий
{arch_text}

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
    idea: str = None,
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
    create_starter_docs(target_dir, project_name, stack_key, assets=assets, force=force, idea=idea)
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
    if stack_key == "undecided":
        print("  3. Ask your AI Agent (Start with Mode 0 Discovery & Tech Stack Research):")
        print("     \"Please read AGENTS.md and start Mode 0: /kb-research <исследование идеи и выбор стека>\"")
    else:
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
    if getattr(args, "idea", None) and not args.stack:
        detected_stack = "undecided"
    else:
        detected_stack = detect_project_stack(target_dir)
        if args.stack and args.stack != "auto":
            detected_stack = args.stack
    stack_choice_map = {"swift": "1", "ts": "2", "python": "3", "dotnet": "4", "generic": "5", "undecided": "6"}
    detected_num = stack_choice_map.get(detected_stack, "1")

    print("\n? Select Technology Stack:")
    print(f"  [1] iOS / macOS (Swift, SwiftUI, Xcode) [Target Apple Stack]{' (Detected)' if detected_stack == 'swift' else ''}")
    print(f"  [2] Web / Node (TypeScript, JavaScript, Next.js){' (Detected)' if detected_stack == 'ts' else ''}")
    print(f"  [3] Python (Pytest, FastAPI, CLI){' (Detected)' if detected_stack == 'python' else ''}")
    print(f"  [4] .NET / C# (MAUI, ASP.NET, CoreCLR){' (Detected)' if detected_stack == 'dotnet' else ''}")
    print(f"  [5] Generic / Other{' (Detected)' if detected_stack == 'generic' else ''}")
    print(f"  [6] 💡 Undecided / Idea-First (Стек будет определен через /kb-research){' (Detected)' if detected_stack == 'undecided' else ''}")
    stack_choice = prompt_user_input("Select [1-6]", default=detected_num)
    stack_map = {"1": "swift", "2": "ts", "3": "python", "4": "dotnet", "5": "generic", "6": "undecided"}
    stack_key = stack_map.get(stack_choice, detected_stack)

    # If stack is undecided and no idea provided via flag, ask for idea
    if stack_key == "undecided" and not getattr(args, "idea", None):
        user_idea = prompt_user_input("? Enter your project idea / concept (or press Enter to describe later)", default="")
        if user_idea:
            args.idea = user_idea

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
        "--idea",
        type=str,
        default=None,
        help="Краткое описание продуктовой идеи для Greenfield-инициализации (автоматически активирует пресет undecided, если --stack не указан)",
    )
    parser.add_argument(
        "--doc-lang", "-l",
        type=str,
        default=None,
        help="Preferred documentation & agent communication language (e.g. ru, en, custom; default: ru)",
    )
    parser.add_argument(
        "--stack", "-s",
        choices=["auto", "swift", "ts", "python", "dotnet", "generic", "undecided"],
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
        if args.idea and not args.stack:
            stack_key = "undecided"
        else:
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
        idea=args.idea,
    )


if __name__ == "__main__":
    main()
