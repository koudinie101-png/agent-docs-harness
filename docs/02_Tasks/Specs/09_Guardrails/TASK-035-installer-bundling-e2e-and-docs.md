---
id: TASK-035
title: "Синхронизация генераторов правил и шаблонов в install.py / build_installer.py (включая --update), сквозные E2E тесты в tests/test_installer.py, обновление README.md и docs/Onboarding.md"
status: done
type: task
phase: 9
component:
  - installer
  - packaging
  - tests
  - documentation
parent_plan: "[[../../Plans/PLAN-009-single-task-barrier-and-stop-on-complete|PLAN-009]]"
created: 2026-10-02
updated: 2026-10-03
tags:
  - task/spec
  - phase9
  - installer
  - packaging
  - tests
  - documentation
  - guardrails
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-035 — Синхронизация инсталлятора, E2E тесты и документация

> **ID:** TASK-035  
> **Статус:** Выполнено (Режим 3)  
> **Теги:** #task/spec #phase9 #installer #packaging #tests #documentation #guardrails  
> **Родительский план:** [[../../Plans/PLAN-009-single-task-barrier-and-stop-on-complete|PLAN-009]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-012-single-task-execution-barrier-and-autonomous-pipeline-containment|RESEARCH-012]], [[../../../03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Завершить интеграцию Фазы 9 в дистрибутив харнесса Docs-as-Code:
1. **Генераторы правил в `install.py`:** Синхронизировать генератор `generate_agents_md` и строковые константы правил (`_RULES_BODY`, `_3MODES`), включив инвариант барьера единичной задачи и терминальный шаг Stop & Yield Control в базовую конфигурацию новых проектов.
2. **Сборка дистрибутива:** Пересобрать автономный инсталлятор `install.py` с помощью `scripts/build_installer.py`, упаковав обновленные шаблоны (`TEMPLATE_DEVLOG.md`), скиллы (`kb-implement`, `kb-complete`) и скрипт `scripts/kb_lint.py`.
3. **Безопасное обновление (`install.py --update`):** Гарантировать доставку обновленных защитных правил и скиллов в существующие проекты без повреждения пользовательских файлов.
4. **Сквозные E2E тесты:** Добавить и обновить проверочные сценарии в `tests/test_installer.py`.
5. **Документация:** Отразить архитектурные гарантии барьера единичной задачи в `README.md` и руководстве `docs/Onboarding.md`.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `install.py` — обновление встроенного генератора `generate_agents_md`, констант `_RULES_BODY`, `_3MODES` и ребандлинг ресурсов.
* `[MODIFY]` `scripts/build_installer.py` — проверка и синхронизация упаковки ресурсов Фазы 9.
* `[MODIFY]` `tests/test_installer.py` — тесты генерации правил Single-Task Barrier и обновления через `--update`.
* `[MODIFY]` `README.md` — описание механизма защиты от авто-чейнинга в витрине проекта.
* `[MODIFY]` `docs/Onboarding.md` — актуализация онбординг-гида (раздел правил и завершения задач).

---

## 3. Детали реализации

### 3.1. Обновление `generate_agents_md` и правил в `install.py`
В `generate_agents_md` и адаптеры IDE добавляется формулировка правила:
```markdown
## Single-Task Execution Barrier (No Auto-Chaining)
The command `/kb-implement <TASK-XXX>` authorizes work strictly on ONE task.
Even if subsequent tasks are listed in plans or Devlog, the agent is strictly
prohibited from auto-chaining without an explicit user command. Stop tool calls on completion.
```
В `_3MODES`:
```markdown
**Mode 3 -- Implementation (`/kb-implement`):**
Code strictly per approved spec. Once complete, strictly STOP tool calls; never auto-chain next tasks.
```

### 3.2. Пересборка дистрибутива
Запуск `python scripts/build_installer.py` с пересборкой embedded bundle словаря `_EMBEDDED_ASSETS` в `install.py`:
- `00_Templates/TEMPLATE_DEVLOG.md`
- `.agents/skills/kb-implement/SKILL.md`
- `.agents/skills/kb-complete/SKILL.md`
- `scripts/kb_lint.py`

### 3.3. E2E Тесты в `tests/test_installer.py`
Проверка:
- Тест `test_single_task_barrier_in_generated_agents_md`: проверка наличия строк `Single-Task Execution Barrier` в сгенерированном файле `AGENTS.md`.
- Тест `test_update_delivers_stop_yield_skills`: запуск `install.py --update` в тестовой песочнице и верификация обновления скиллов `kb-implement` и `kb-complete`.

### 3.4. Актуализация документации
- В `README.md` в секцию архитектурных гарантий и дисциплин вносится описание барьера единичной задачи.
- В `docs/Onboarding.md` в шаге Режима 3 подчеркивается обязательность ожидания команды пользователя между задачами.

---

## 4. План верификации (Verification Plan)

- [x] Сборка дистрибутива: `python scripts/build_installer.py` (Exit code 0, успешное обновление `install.py`).
- [x] Полный прогон всех тестов проекта: `python -m unittest discover -s tests` (100% pass, Exit code 0).
- [x] Аудит базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links, Exit code 0).
- [x] Проверка автономности инсталлятора: `python install.py --help` (Exit code 0).

---

## 5. Критерии готовности (DoD)

- [x] Генератор правил `generate_agents_md` и константы в `install.py` обновлены.
- [x] Инсталлятор пересобран через `build_installer.py` и протестирован.
- [x] Сквозные тесты в `tests/test_installer.py` успешно проходят.
- [x] Витрина `README.md` и руководство `docs/Onboarding.md` актуализированы.
- [x] Все пункты Плана верификации выполнены.
- [x] Статус обновлен в ТЗ, Канбане и Roadmap.
- [x] Запись сессии внесена в `Devlog.md`.
