---
id: TASK-004
title: E2E верификация песочницы и документация README
status: planned
type: task
phase: 1
component:
  - testing
  - docs
  - readme
parent_plan: "[[../../Plans/PLAN-001-crossplatform-installer-architecture|PLAN-001]]"
created: 2026-09-30
updated: 2026-09-30
tags:
  - task/spec
  - component/testing
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-004 — E2E верификация песочницы и документация README

> **ID:** TASK-004  
> **Статус:** Запланировано  
> **Теги:** #task/spec #component/testing  
> **Родительский план:** [[../../Plans/PLAN-001-crossplatform-installer-architecture|PLAN-001]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи
Написать автоматизированные E2E тесты (через `unittest`) для проверки установки в изолированном временном каталоге для всех поддерживаемых стеков, убедиться в прохождении `kb_lint.py` с 0 ошибками и подготовить подробный, наглядный `README.md` репозитория.

---

## 2. Затрагиваемые файлы и компоненты
* `[NEW]` `tests/test_installer.py` — сквозные тесты на Python 3 (`unittest`).
* `[NEW]` `README.md` — главное описание проекта, баннер, быстрый старт, архитектура, таблица агентов и стеков.
* `[NEW]` `docs/05_Testing/Acceptance_Checklist.md` — сценарий приемочного тестирования.

---

## 3. Детали технической реализации
1. **Автотесты `tests/test_installer.py`:**
   - Тест распаковки по умолчанию (Generic).
   - Тест параметров для стека `swift` (проверка подстановки Swift-команд в `Onboarding.md` и `AGENTS.md`).
   - Тест генерации зеркальных файлов агентов (`.clinerules`, `CLAUDE.md`, `.cursorrules`, `.github/copilot-instructions.md`).
   - Тест запуска линтера `kb_lint.py` в целевом каталоге.
2. **README.md:**
   - Описание боли ("амнезия контекста", ломка кода, расползание архитектуры).
   - Быстрый старт через `curl | python3`.
   - Описание 3 режимов работы с агентом.
   - Поддерживаемые агенты и редакторы (VS Code Cline, Roo Code, Claude Code, Cursor, Copilot).
   - Интеграция с Obsidian и скриншот/описание графа.

---

## 4. План верификации (Verification Plan)
- [ ] Запуск `python -m unittest discover -s tests` (все тесты проходят).
- [ ] Запуск `python scripts/kb_lint.py --path docs` (0 ошибок).
- [ ] Проверка чистоты временных папок после выполнения тестов.

---

## 5. Критерии готовности (Definition of Done)
- [ ] Все автоматические тесты проходят успешно.
- [ ] `README.md` готов и содержит точные примеры команд.
