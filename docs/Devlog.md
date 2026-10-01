---
id: DEVLOG
title: Журнал разработки (Devlog)
status: active
type: devlog
created: 2026-09-30
updated: 2026-10-01
tags:
  - devlog
  - journal
  - agent-docs-harness
---

# 📝 Журнал разработки (Devlog): agent-docs-harness

> **Теги:** #devlog #journal #agent-docs-harness  
> **Родительская заметка:** [[00_Index|00_Index]]  

Здесь фиксируются ключевые события, результаты сессий и важные изменения по проекту в хронологическом порядке.

---

### [2026-10-01] — Завершение TASK-009: Clean Slate Scaffolding & Zero-Broken-Links FTUE
- **Что сделано:**
  - В `install.py` (`create_starter_docs`) полностью исключена генерация фантомных ссылок на несуществующие файлы `PLAN-001` и `TASK-001` в `Kanban.md` и `Roadmap.md`.
  - Стартовый бэклог в `Kanban.md` теперь создается чистым, с комментарием-приглашением начать работу с `/kb-plan <название>`.
  - `Roadmap.md` генерирует чистую структуру Фазы 1 без битых ссылок.
  - Удалена паразитная генерация фиктивных файлов планов и ТЗ в каталогах `Plans/` и `Specs/`.
  - Обновлены канонические шаблоны `templates/TEMPLATE_KANBAN.md`, `templates/TEMPLATE_ROADMAP.md` и пересобран бандл через `build_installer.py` (размер дистрибутива `install.py`: 75.9 КБ / 77,684 байта).
  - В тестовый набор `tests/test_installer.py` добавлен сквозной тест `test_09_clean_slate_scaffolding`, проверяющий чистоту бэклога и успешное прохождение аудита `kb_lint.py` с 0 битых ссылок при первой установке.
- **Результаты верификации:**
  - `python -m py_compile install.py` -> Код 0.
  - `python scripts/build_installer.py` -> Код 0.
  - `python -m unittest discover -s tests` -> 9/9 тестов успешно пройдены (100% pass).
  - `python scripts/kb_lint.py --path docs` -> 44 файла, 174 ссылки, 0 broken links, 100% валидный YAML frontmatter.
- **Следующий шаг:**
  - Реализация `TASK-010`: Бесшовное внедрение в существующие проекты (Brownfield Adoption) и автодетект стека.

---

### [2026-10-01] — Режим 1: Планирование Фазы 3 и фиксация отказных архитектурных решений (ADR-0005, ADR-0006)
- **Что сделано:**
  - Проведен критический анализ бэклога перспективных идей из `Roadmap.md` и `Kanban.md` с позиции Senior Partner.
  - Идеи категории C официально отклонены как оверинжиниринг и зафиксированы в отказных архитектурных решениях (`status: rejected`):
    - [[03_Decisions_ADR/ADR-0005-rejection-of-embedded-web-visualizer|ADR-0005]]: Отказ от встроенного локального web-визуализатора базы знаний (`install.py --serve`) во избежание раздувания бандла, нарушения Zero Dependencies и дублирования нативного Obsidian.
    - [[03_Decisions_ADR/ADR-0006-rejection-of-standalone-pdf-report-generator|ADR-0006]]: Отказ от встроенного Python-генератора PDF-отчетов в пользу нативных возможностей LLM/агентов и штатного экспорта Markdown.
  - Сформирован и утвержден концептуальный план Фазы 3: [[02_Tasks/Plans/PLAN-003-brownfield-adoption-and-lifecycle|PLAN-003]] («Зрелость инсталлятора — Brownfield Adoption, Clean Slate Scaffolding, безопасное обновление и CI»).
  - Декомпозированы задачи Фазы 3 (`TASK-009` — `TASK-012`), добавлены карточки в бэклог [[02_Tasks/Kanban|Kanban.md]] и вехи в [[02_Tasks/Roadmap|Roadmap.md]].
  - Запущена проверка целостности базы знаний через `python scripts/kb_lint.py --path docs`: 0 broken wikilinks, 100% валидность frontmatter.
- **Следующий шаг:**
  - Переход к Режиму 2 (Task Specification) для первой задачи `TASK-009` (Clean Slate Scaffolding).

---

### [2026-09-30] — Завершение TASK-008 и успешное закрытие Фазы 2 (Скиллы, правила и экосистема)
- **Что сделано:**
  - В тестовый набор `tests/test_installer.py` добавлены 3 новых сквозных E2E теста:
    - `test_06_install_deploys_all_11_skills`: проверяет корректное развертывание каталога `.agents/skills/`, наличие всех 11 исполняемых скиллов и валидность структуры их файлов `SKILL.md`.
    - `test_07_install_gemini_and_windsurf_rules`: проверяет корректность создания `GEMINI.md` и `.windsurfrules` как в режиме `--agent all`, так и в изолированных режимах `--agent gemini` / `--agent windsurf`, а также наличие директив `STRICTLY NO CODE CHANGES`.
    - `test_08_install_doc_lang_parameter`: проверяет влияние флага `--doc-lang` (`ru` vs `en`) на директивы в сгенерированных правилах и подтверждает успешное прохождение аудита `kb_lint.py` в обоих случаях.
  - Актуализирована документация `README.md`:
    - Добавлено описание структуры каталога `.agents/skills/` и таблица всех 11 скиллов с их slash-командами `/kb-*` и режимами.
    - Отражена поддержка Google Antigravity (`GEMINI.md`) и Windsurf Cascade (`.windsurfrules`).
    - Описан флаг `--doc-lang` и поддержка двуязычной разработки.
    - Включен раздел об открытых моделях (Qwen 2.5 Coder, DeepSeek) со ссылкой на платформенное исследование `RESEARCH-001`.
    - Добавлен раздел «Zero-to-Hero Quickstart» с первыми шагами для пользователей после установки.
  - Проведена полная верификация: все 8 тестов в `tests/test_installer.py` пройдены успешно (100% pass), `kb_lint.py` подтвердил 0 битых ссылок и целостность базы знаний.
  - План Фазы 2 (`PLAN-002`) и все входящие задачи (TASK-005, TASK-006, TASK-007, TASK-008) полностью выполнены и закрыты.
- **Следующий шаг:**
  - Переход к перспективным направлениям бэклога (Clean Slate Scaffolding, GitHub Actions CI workflow, Brownfield Adoption).

---

### [2026-09-30] — Завершение TASK-007: Эталонные правила агентов по канону remote-notification и генерация GEMINI.md
- **Что сделано:**
  - Во все генераторы правил инсталлятора `install.py` интегрирован полный канонический регламент из эталонного проекта `remote_notification`:
    - 12 канонических дисциплин Docs-as-Code (онбординг, Kanban, Roadmap, ADR и отказные ADR, платформа/Research, Devlog, Obsidian, Permalinks, Regression-First, QA-реестр `05_Testing/`, Obsidian Graph, Git-интеграция).
    - Строгая защита 3 режимов с маркером `STRICTLY NO CODE CHANGES` для Режимов 1 и 2.
    - Роль Senior Engineering Partner с обязательным подтверждением пользователя перед записью планов и ТЗ.
    - Поддержка языкового регламента `doc_lang` (`ru` vs `en`).
  - Добавлен генератор `generate_gemini_md` для создания корневого файла `GEMINI.md` (поддержка Google Antigravity и Gemini CLI с перечислением доступных скиллов).
  - Добавлен генератор `generate_windsurfrules` для поддержки Windsurf Cascade (`.windsurfrules`).
  - Обновлены генераторы `generate_agents_md`, `generate_clinerules`, `generate_claude_md`, `generate_cursorrules`, `generate_copilot_instructions`.
  - В опции `--agent` CLI и интерактивного визарда добавлены варианты `gemini` и `windsurf`.
  - Проведена оптимизация размера: итоговый размер `install.py` составил 79.3 КБ / 81,153 байта (строго в рамках DoD < 80 КБ / 81,920 байт).
  - Успешно пройдены все верификационные тесты: сборка `build_installer.py` (код 0), `py_compile` (код 0), `kb_lint.py` (0 битых ссылок), интеграционный прогон генерации всех 7 файлов правил и проверка наличия ключевых маркеров, полный набор тестов `unittest` (5/5 тестов OK).
- **Следующий шаг:**
  - Реализация `TASK-008`: Сквозное E2E тестирование в `tests/test_installer.py` и обновление документации `README.md` (включая гайд для новичков).

---

### [2026-09-30] — Завершение TASK-006: Упаковка 11 скиллов .agents/skills/ в сборщик и install.py
- **Что сделано:**
  - В `scripts/build_installer.py` добавлен сборщик скиллов: обход каталога `.agents/skills/` и упаковка канонических файлов `SKILL.md` для всех 11 скиллов без дублирования лишних файлов.
  - В `install.py` реализован локальный фолбэк для разработки в `unpack_assets()` и автоматическая распаковка скиллов в целевую директорию `.agents/skills/<skill>/SKILL.md`.
  - Оптимизирована генерация стартовых документов в `create_starter_docs` через переиспользование распакованных шаблонов (итоговый размер `install.py` составил 78.1 КБ / 80,024 байта при лимите DoD < 80 КБ).
  - Успешно пройдены все этапы верификации: `build_installer.py` (код 0), `py_compile` (код 0), `kb_lint.py` (0 битых ссылок), интеграционный прогон в песочнице с проверкой всех 11 `SKILL.md`, полный прогон `unittest` (5/5 тестов пройдено).
- **Следующий шаг:**
  - Реализация `TASK-007`: Эталонные правила агентов по канону `remote_notification` (12 дисциплин, языковая параметризация, роль Senior Partner, отказные ADR, `GEMINI.md`, `.windsurfrules` и адаптеры).

---

### [2026-09-30] — Завершение TASK-005: Исследование экосистемы AI-агентов (RESEARCH-001) и мультиязычность
- **Что сделано:**
  - Проведено и оформлено глубокое платформенное исследование `docs/04_Research/RESEARCH-001-ai-agent-ecosystem-and-ide-matrix.md` по средам разработки (Antigravity, Cline, Claude Code CLI, Cursor, Windsurf, Copilot, Continue, Aider) и семействам моделей (Qwen 2.5 Coder, DeepSeek R1/V3, Claude, Gemini, GPT).
  - В исследовании детально разобран потенциал ведущей открытой модели **Qwen 2.5 Coder** (32B/14B/7B) для локального enterprise-развертывания (Ollama/vLLM) со 100% приватностью кода под управлением 3-режимного каркаса.
  - Реализована поддержка языковой параметризации в `install.py`: добавлен CLI-флаг `--doc-lang` (по умолчанию `ru`) и интерактивный вопрос на английском языке в TUI визарде.
  - Проведена верификация: `py_compile` (код 0), запуск `install.py --help`, запуск песочницы с `--doc-lang en`, все 5 модульных тестов в `test_installer.py` (100% pass), проверка ссылок `kb_lint.py` (0 битых ссылок).
- **Следующий шаг:**
  - Реализация `TASK-006`: упаковка всех 11 исполняемых скиллов `.agents/skills/` в сборщик `build_installer.py` и распаковка в `install.py`.

---

### [2026-09-30] — Завершение Фазы 1 (MVP): Автономный инсталлятор и мульти-стековые пресеты
- **Что сделано:**
  - Реализован автономный установщик `install.py` на стандартной библиотеке Python 3 (Zero Dependencies).
  - Разработан скрипт компиляции ресурсов `scripts/build_installer.py`, который упаковывает 12 шаблонов, `.obsidian/graph.json` и `kb_lint.py` в компактный zlib/base64 бандл внутри `install.py`.
  - Реализованы 5 технологических пресетов (Swift/iOS/macOS с нюансами ARC/Concurrency/BackgroundTasks, TypeScript, Python, .NET, Generic).
  - Сгенерированы адаптеры правил AI-агентов (`AGENTS.md`, `.clinerules`, `CLAUDE.md`, `.cursorrules`, `.github/copilot-instructions.md`).
  - Разработан интерактивный терминальный мастер с поддержкой TTY при pipe через `curl | python3` и полным набором CLI-флагов.
  - Написан набор автоматических тестов `tests/test_installer.py` (5 E2E тестов, 100% pass).
  - Подготовлен исчерпывающий `README.md` с визуальным стилем, инструкцией в 1 команду и описанием преимуществ.
  - Проверена целостность базы знаний через `kb_lint.py` (0 битых ссылок).
- **Следующий шаг:**
  - Подключение удаленного GitHub репозитория и релиз v1.0.0.

---

### [2026-09-30] — Инициализация проекта agent-docs-harness и базы знаний Docs-as-Code
- **Что сделано:**
  - Инициализирован Git-репозиторий и настроен `.gitignore`.
  - Развернута архитектура базы знаний `docs/` по стандарту Docs-as-Code с соблюдением догфудинга.
  - Настроена цветовая схема Obsidian Graph (`.obsidian/graph.json`) с 7 цветовыми группами.
  - Подготовлены 12 эталонных шаблонов в `templates/` и `docs/00_Templates/`.
  - Реализован автономный линтер базы знаний `scripts/kb_lint.py` с проверкой wikilinks и frontmatter без внешних зависимостей.
  - Сформированы документы `SPEC.md`, `00_Index.md`, `Onboarding.md`, `Kanban.md`, `Roadmap.md`.
- **Следующий шаг:**
  - Реализация первой задачи фазы MVP: ядро инсталлятора `install.py` с упаковщиком шаблонов и адаптерами стеков.
