---
id: PLAN-001
title: Архитектура автономного кроссплатформенного инсталлятора
status: accepted
type: plan
phase: 1
created: 2026-09-30
updated: 2026-09-30
tags:
  - plan
  - feature
  - architecture
  - installer
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 📋 План: PLAN-001 — Архитектура автономного кроссплатформенного инсталлятора

> **ID:** PLAN-001  
> **Статус:** Согласовано  
> **Теги:** #plan #feature #architecture #installer  
> **Родительская спецификация:** [[../../SPEC|SPEC.md]]  
> **Канбан:** [[../Kanban|Канбан-доска]]  

---

## 1. Контекст и цели (Problem & Goals)
Разработчикам, использующим AI-агентов (Cline, Roo Code, Claude Code, Cursor, Copilot), требуется готовый процесс дисциплины Docs-as-Code.
Цель: создать утилиту `install.py`, запускаемую в одну строку без внешних зависимостей:
```bash
curl -sSL https://raw.githubusercontent.com/<username>/agent-docs-harness/main/install.py | python3
```

## 2. Обсуждение и ключевые решения (Q&A / Discussion)
* **Q1: Как обеспечить запуск через `curl | python3` без скачивания zip или git clone?**
  * **Решение:** Инсталлятор упаковывается как самодостаточный (self-contained) монолитный Python 3 скрипт. Все 12 шаблонов, конфиг графа Obsidian и скрипт `kb_lint.py` вшиваются внутрь в виде base64-сжатого или raw-структурированного словаря. При запуске скрипт распаковывает и кастомизирует их на лету под выбранный проект и стек.
* **Q2: Как поддерживать удобство редактирования шаблонов в самом репозитории?**
  * **Решение:** В репозитории шаблоны хранятся как чистые `.md` файлы в `templates/`. Скрипт сборки `scripts/build_installer.py` автоматически компилирует актуальные шаблоны в `install.py`. При этом `install.py` также может определять локальные файлы, если запускается разработчиком внутри клонированного репо.
* **Q3: Поддержка целевых сред (первый фокус — macOS / iOS Swift / Xcode)?**
  * **Решение:** Инсталлятор параметризует сгенерированные файлы (`Onboarding.md`, `TASK.md`, `BUG.md`, `RESEARCH.md`, `AGENTS.md`) специфичными для Swift командами (`swift test`, `xcodebuild test`), путями и характерными платформами (iOS/macOS/watchOS).

## 3. Архитектурное влияние и критический анализ
* **Zero Dependencies:** Использование `pathlib`, `json`, `os`, `sys`, `shutil`, `argparse`, `base64`, `zlib`. Отказ от внешних библиотек гарантирует мгновенный старт на любой чистой macOS / Linux / Windows машине с установленным Python 3.8+.
* **Cross-platform UTF-8:** Корректный перевызов `sys.stdout.reconfigure(encoding="utf-8")` для Windows Console.
* **Non-destructive:** Инсталлятор проверяет наличие существующей папки `docs/` и предупреждает пользователя, предотвращая случайную потерю данных.

## 4. Высокоуровневая декомпозиция (Task Breakdown)
- [x] Инициализация репозитория и базы знаний самого проекта.
- [ ] [[Specs/01_MVP/TASK-001-installer-core-and-bundling|TASK-001]]: Ядро `install.py` и упаковка ассетов через builder.
- [ ] [[Specs/01_MVP/TASK-002-multi-stack-templates-and-agent-configs|TASK-002]]: Мульти-стековые шаблоны (Swift, TS, Python, .NET, Generic) и адаптеры агентов.
- [ ] [[Specs/01_MVP/TASK-003-cli-wizard-and-options|TASK-003]]: Интерактивный терминальный мастер и CLI флаги.
- [ ] [[Specs/01_MVP/TASK-004-e2e-testing-and-readme|TASK-004]]: E2E верификация песочницы и документация README.

## 5. Критерии приемки плана (DoD)
- [x] Концепция согласована и зафиксирована.
- [x] Задачи декомпозированы со спецификациями.
- [x] Карточки добавлены в `Kanban.md`.
