---
id: TASK-056
title: "Синхронизация инсталлятора install.py / build_installer.py, E2E тесты и актуализация Living Spec"
status: done
type: task
phase: 14
component:
  - installer
  - tests
  - spec
  - readme
parent_plan: "[[../../Plans/PLAN-014-agile-docs-as-code-and-chat-first-dx|PLAN-014]]"
created: 2026-10-12
updated: 2026-10-12
tags:
  - task/spec
  - phase14
  - installer
  - e2e
  - spec
  - readme
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-056 — Синхронизация инсталлятора install.py / build_installer.py, E2E тесты и актуализация Living Spec

> **ID:** TASK-056 | **Статус:** Выполнено  
> **План:** [[../../Plans/PLAN-014-agile-docs-as-code-and-chat-first-dx|PLAN-014]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0014-greenfield-idea-first-initialization-and-living-spec-protocol|ADR-0014]], [[../../../03_Decisions_ADR/ADR-0022-chat-first-vibe-coder-dx-and-human-guardrails|ADR-0022]], [[../../../03_Decisions_ADR/ADR-0023-fast-track-protocol-for-micro-tasks|ADR-0023]]

---

## 1. Цель задачи
Собрать все наработки Фазы 14 в единый дистрибутив: упаковать новый шаблон `TEMPLATE_TASK_MICRO.md` и руководство `Zero_To_Hero_Guide.md` в монолитный сборщик [scripts/build_installer.py](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/scripts/build_installer.py), обеспечить развертывание и бережное обновление в [install.py](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/install.py), покрыть сквозными E2E тестами в [tests/test_installer.py](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/tests/test_installer.py), оформить витрину [README.md](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/README.md) с блоком Chat-First Quickstart и синхронизировать Master Specification [SPEC.md](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/SPEC.md).

---

## 2. Затрагиваемые файлы
* `[MODIFY]` `scripts/build_installer.py` — упаковка `TEMPLATE_TASK_MICRO.md` и `Zero_To_Hero_Guide.md` в монолитный дистрибутив `dist/install.py` и `install.py`.
* `[MODIFY]` `install.py` — поддержка развертывания 15 шаблонов и гайда `Zero_To_Hero_Guide.md` (включая режим `--update`).
* `[MODIFY]` `tests/test_installer.py` — комплексный E2E тест развертывания Fast-Track шаблона и гайда.
* `[MODIFY]` `README.md` — блок One-Prompt Quickstart (Chat-First запуск без терминала) и обновленная таблица ресурсов.
* `[MODIFY]` `SPEC.md` — актуализация Мастер-Спецификации (15 шаблонов, протокол Fast-Track, Human Guardrails).

---

## 3. Детали реализации

### 3.1. Синхронизация сборщика `scripts/build_installer.py` и `install.py`
* В словарь встроенных шаблонов `TEMPLATES` сборщика добавить:
  - `TEMPLATE_TASK_MICRO.md` (чтение из `docs/00_Templates/` или `templates/`).
  - `Zero_To_Hero_Guide.md` (чтение из `docs/Zero_To_Hero_Guide.md`).
* При выполнении `install.py --update` гарантировать, что `TEMPLATE_TASK_MICRO.md` и `Zero_To_Hero_Guide.md` бережно обновляются без перезаписи пользовательских заметок в `docs/`.

### 3.2. E2E тестирование в `tests/test_installer.py`
* Реализовать тест `test_28_fast_track_template_and_zero_to_hero_guide_deployment`:
  - Проверка чистой установки: в `docs/00_Templates/` создан `TEMPLATE_TASK_MICRO.md`, в `docs/` создан `Zero_To_Hero_Guide.md`.
  - Проверка обновления существующего проекта (`--update`): новые файлы успешно доставляются.

### 3.3. Актуализация Living Spec и витрины
* В `README.md` добавить раздел:
  ```markdown
  ### 💬 Быстрый старт прямо из чата (One-Prompt Quickstart)
  Скопируйте и отправьте этот промпт в окно чата вашего AI-редактора:
  > «Инициализируй в этом проекте harness Docs-as-Code и покажи мне гайд по безопасной разработке».
  ```
* В `SPEC.md` зафиксировать реестр 15 шаблонов базы знаний и протокол Fast-Track.

---

## 4. План верификации (Verification Plan)
- [x] Сборка дистрибутива: `python scripts/build_installer.py` (Exit code 0, обновлены `install.py` и `dist/install.py`).
- [x] Синтаксис дистрибутива: `python -m py_compile dist/install.py` (Exit code 0).
- [x] Сквозные тесты: `python -m unittest tests/test_installer.py` (100% Pass).
- [x] Полный тестовый сьют: `python -m unittest discover -s tests` (100% Pass).
- [x] Аудит базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links).

---

## 5. Критерии готовности (DoD)
- [x] Инсталлятор и сборщик обновлены и синхронизированы.
- [x] E2E тест проверяет доставку `TEMPLATE_TASK_MICRO.md` и `Zero_To_Hero_Guide.md`.
- [x] Витрина `README.md` и Master Spec `SPEC.md` актуализированы.
- [x] Все пункты Плана верификации пройдены без ошибок.
