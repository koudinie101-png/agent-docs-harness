---
id: TASK-005
title: Исследование экосистемы AI-агентов (RESEARCH-001) и мультиязычность (--doc-lang)
status: done
type: task
phase: 2
component:
  - research
  - cli
  - wizard
parent_plan: "[[../../Plans/PLAN-002-full-skills-and-agent-rules-integration|PLAN-002]]"
created: 2026-09-30
updated: 2026-09-30
tags:
  - task/spec
  - component/research
  - component/cli
  - multilang
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-005 — Исследование экосистемы AI-агентов (RESEARCH-001) и мультиязычность (--doc-lang)

> **ID:** TASK-005  
> **Статус:** Выполнено (Режим 3)  
> **Теги:** #task/spec #component/research #component/cli #multilang  
> **Родительский план:** [[../../Plans/PLAN-002-full-skills-and-agent-rules-integration|PLAN-002]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

1. Сформировать глубокую исследовательскую заметку `docs/04_Research/RESEARCH-001-ai-agent-ecosystem-and-ide-matrix.md` с анализом популярных сред разработки (Antigravity/Gemini CLI, VS Code Cline/Roo Code, Claude Code CLI, Cursor IDE, Windsurf, GitHub Copilot, Continue.dev, Aider) и семейств моделей (Claude, Gemini, GPT, DeepSeek, Qwen 2.5 Coder), их файлов конфигураций, механизмов системных промптов и работы со скиллами.
2. Реализовать поддержку языковой параметризации в `install.py`:
   - Добавить интерактивный вопрос на английском языке в TUI визарде с выбором предпочитаемого языка документации (`ru`, `en`, custom).
   - Добавить CLI-параметр `--doc-lang` в парсер аргументов командной строки `argparse`.
   - Пробросить выбранный параметр `doc_lang` в оркестратор `install_harness`.

---

## 2. Затрагиваемые файлы и компоненты

* `[NEW]` `docs/04_Research/RESEARCH-001-ai-agent-ecosystem-and-ide-matrix.md` — детальное платформенное исследование экосистемы сред, IDE и моделей.
* `[MODIFY]` `install.py` — добавление CLI флага `--doc-lang`, вопроса в интерактивном мастере и передача `doc_lang` в `install_harness`.

---

## 3. Детали технической реализации

### 3.1. Исследование `RESEARCH-001`:
Документ в `docs/04_Research/` оформляется по стандарту `TEMPLATE_RESEARCH.md`:
* Обзор сред и файлов правил:
  * Google Antigravity / Gemini CLI -> `GEMINI.md`, `AGENTS.md`, `.gemini/`
  * VS Code Cline / Roo Code -> `.clinerules`, MCP tools
  * Claude Code CLI -> `CLAUDE.md`, terminal integration
  * Cursor IDE -> `.cursorrules`
  * Windsurf (Codeium) -> `.windsurfrules`
  * GitHub Copilot -> `.github/copilot-instructions.md`
  * Continue.dev / Aider -> `.continue/config.json`, `.aider.conf.yml`
* Модели:
  * Claude 3.5 Sonnet / 3.7 Sonnet (лидерство в tool use и code refactoring).
  * Gemini 1.5 Pro / 2.0 Pro / Flash (огромное контекстное окно до 2M токенов, нативная интеграция в Antigravity).
  * GPT-4o / o1 / o3-mini (рассуждения и общая логика).
  * DeepSeek R1 / V3 (доступная reasoning модель для локального и API использования).
  * Qwen 2.5 Coder (32B / 7B / 14B) — ведущая открытая модель для локального кодинга через Ollama/vLLM.
* Матрица компромиссов, ограничений платформ и отвергнутых альтернатив.

### 3.2. CLI-флаг и интерактивный мастер в `install.py`:
```python
# argparse
parser.add_argument(
    "--doc-lang", "-l",
    type=str,
    default="ru",
    help="Preferred documentation & agent communication language (e.g. ru, en, custom; default: ru)",
)

# TUI Wizard prompt (English by default):
print("\n? Preferred documentation & agent communication language:")
print("  [1] Russian (Русский) [Recommended for RU teams]")
print("  [2] English")
print("  [3] Custom language (type name)")
```

---

## 4. План верификации (Verification Plan)

### Сборка и тесты:
- [x] Проверка синтаксиса Python: `python -m py_compile install.py` (код 0).
- [x] Запуск автоматических тестов: `python -m unittest discover -s tests` (5 тестов пройдены, 100% pass).
- [x] Проверка базы знаний линтером: `python scripts/kb_lint.py --path docs` (0 битых ссылок).

### Интеграционная проверка CLI:
- [x] Запуск `python install.py --help` — проверка наличия `--doc-lang` (подтверждено).
- [x] Тестовый неинтерактивный запуск: `python install.py -y --target-dir test_verify_lang --doc-lang en --stack generic --agent generic --git none` (пройдено).
- [x] Проверка успешного завершения и очистка временного каталога `test_verify_lang` (пройдено).

---

## 5. Критерии готовности (Definition of Done)

- [x] Исследование `RESEARCH-001` полностью заполнено и содержит матрицу сред и моделей (включая Qwen).
- [x] `install.py` поддерживает `--doc-lang` и интерактивный вопрос выбора языка.
- [x] `kb_lint.py` не выдает ошибок и битых ссылок.
- [x] Существующие unit-тесты проходят без регрессий (100% pass).
- [x] Карточка задачи переведена в `Kanban.md` в Done, отмечен Roadmap, сделана запись в `Devlog.md`.
