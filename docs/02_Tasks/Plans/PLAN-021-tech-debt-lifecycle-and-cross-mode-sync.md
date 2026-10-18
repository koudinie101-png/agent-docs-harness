---
id: PLAN-021
title: "Фаза 21: Сквозной жизненный цикл технического долга и кросс-режимная синхронизация (Tech Debt Lifecycle & Cross-Mode Sync)"
status: accepted
type: plan
phase: 21
created: 2026-10-16
updated: 2026-10-16
tags:
  - plan
  - phase21
  - techdebt
  - lint
  - skills
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 📋 План: PLAN-021 — Фаза 21: Сквозной жизненный цикл технического долга и кросс-режимная синхронизация

> **ID:** PLAN-021 | **Статус:** Согласовано (2026-10-16)  
> **Фаза:** 21 | **Целевой релиз:** v0.21.0  
> **Спецификация:** [[../../SPEC|SPEC.md]] | **Канбан:** [[../Kanban|Канбан]] | **Дорожная карта:** [[../Roadmap|Дорожная карта (Фаза 21)]]  
> **Нормативная база:** [[../../04_Research/RESEARCH-023-tech-debt-lifecycle-and-cross-mode-sync|RESEARCH-023]], [[../../03_Decisions_ADR/ADR-0028-end-to-end-tech-debt-lifecycle-and-lint-enforcement|ADR-0028]]

---

## 1. Контекст и цели (Problem & Goals)

В Фазе 19 ([[PLAN-019-engineering-gates-and-tech-debt-governance|PLAN-019]], [[../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]) был внедрен реестр `docs/02_Tasks/TechDebt.md` с проверкой `check_tech_debt_integrity()` в `scripts/kb_lint.py`. Аудит ([[../../04_Research/RESEARCH-023-tech-debt-lifecycle-and-cross-mode-sync|RESEARCH-023]]) показал, что при создании фаз и задач рефакторинга с тегом `#techdebt` реестр `TechDebt.md` остается пустым из-за 6 разрывов:

1. **Узкий триггер в `AGENTS.md` (Правило 13):** запись в `TechDebt.md` предписана только для побочных находок `P3` на ревью в Режиме 3 (`/kb-implement`), игнорируя плановые фазы и задачи рефакторинга в Режимах 1 (`/kb-plan`) и 2 (`/kb-task`).
2. **Отсутствие `TechDebt.md` в скиллах `.agents/skills/kb-*`:** `/kb-plan`, `/kb-task`, `/kb-triage` и `/kb-complete` не интегрированы с `TechDebt.md` и не переносят закрытый долг в `Resolved Debt`.
3. **Конфликт `// ROADMAP-<ID>` и `// DEBT-XXX`:** Правило 15 `AGENTS.md` и `check_untracked_todos()` в `scripts/kb_lint.py` выдают предупреждение на `TODO(DEBT-001)`.
4. **Разнобой таксономии (`#techdebt` vs `#tech-debt`):** пропуск канонического `#techdebt` в Правиле 4 `AGENTS.md` и `.obsidian/graph.json`.
5. **Слепая зона в шаблонах:** `TechDebt.md` отсутствует в `TEMPLATE_INDEX.md`, `TEMPLATE_ONBOARDING.md` и шапке `02_Tasks/` в `AGENTS.md`.
6. **Отсутствие кросс-проверки в `scripts/kb_lint.py`:** `check_tech_debt_integrity()` не предупреждает, когда в проекте есть фазы/планы/задачи с тегом `#techdebt` при пустом реестре `TechDebt.md`.

**Цель Фазы 21:** замкнуть сквозной цикл `DEBT-XXX` (`Active P3 Debt -> Plan/Task -> Resolved Debt`) во всех режимах (`Mode 1`, `Mode 2`, `Mode 2C`, `Mode 3`), разрешить `// DEBT-XXX`, унифицировать `#techdebt` и внедрить семантическую сверку в `scripts/kb_lint.py`.

---

## 2. Обсуждение и решения (Q&A)

* **Q1: Блокировать ли сборку (`ERROR`) или выдавать `WARN`, если есть документ с `#techdebt`, а `TechDebt.md` пуст?**
  * **Решение:** Выдавать **неблокирующее предупреждение (`WARN`)** по аналогии с `check_phase_consistency()`, исключая мета-документы самого харнесса (`PLAN-019`, `PLAN-021`, `TASK-075`..`TASK-084`). Синтаксические нарушения внутри `TechDebt.md` остаются `ERROR` (exit code 1).
* **Q2: Как синхронизировать `TechDebt.md` в `/kb-plan` и `/kb-task`?**
  * **Решение:** `TechDebt.md` закрепляется в Правиле 13 `AGENTS.md` как обязательный первичный реестр (SSOT) для любого техдолга `P3`. При планировании или постановке задач с `#techdebt` агент проверяет наличие записей `DEBT-XXX` в `Active P3 Debt` (регистрируя их при отсутствии) и ссылается на них в `PLAN-XXX` / `TASK-XXX`.
* **Q3: Как закрывается запись `DEBT-XXX`?**
  * **Решение:** В `/kb-complete` (и финализации `/kb-implement`) агент переносит закрытые строки `DEBT-XXX` из `Active P3 Debt` в `## ✅ Погашенный технический долг (Resolved Debt)` с указанием `[[Specs/.../TASK-XXX|TASK-XXX]]`.

---

## 3. Архитектурное влияние и риски

* **Затрагиваемые компоненты:** `scripts/kb_lint.py`, `tests/test_kb_lint.py`, `.agents/skills/kb-{plan,task,triage,complete,lint}/SKILL.md`, `AGENTS.md`, `GEMINI.md`, `.clinerules`, `Docs-As-Code/.obsidian/graph.json`, `TEMPLATE_INDEX.md`, `TEMPLATE_ONBOARDING.md`, `install.py`, `tests/test_installer.py`, `SPEC.md`, `README.md`, `Onboarding.md`.

### Prior-Art Gate (Существующие решения и платформенные аналоги):
* **Внутренний аудит:** расширяются функции `check_tech_debt_integrity()` и `check_untracked_todos()` в `scripts/kb_lint.py` и генераторы `install.py` без создания новых модулей.
* **Внешний аудит:** внешние трекеры техдолга противоречат `ADR-0001` (Zero Dependencies).

---

## 4. Декомпозиция задач (Task Breakdown)

- [ ] [[../Specs/21_TechDebtLifecycle/TASK-082-kb-lint-tech-debt-cross-check-and-todo-tags|TASK-082]]: Семантический кросс-чек `TechDebt.md` с фазами/задачами `#techdebt` и поддержка кодовых тегов `// DEBT-XXX` в `scripts/kb_lint.py`
  * Поддержка `r'(?:ROADMAP-[A-Za-z0-9_-]+|DEBT-\d{3,})'` в `check_untracked_todos()`.
  * Предупреждение (`WARN`) в `check_tech_debt_integrity()` при наличии планов/задач с `#techdebt` без привязки к `DEBT-XXX` или при пустом `TechDebt.md`.
  * Модульные тесты в `tests/test_kb_lint.py`.
- [ ] [[../Specs/21_TechDebtLifecycle/TASK-083-skills-agents-and-templates-tech-debt-lifecycle|TASK-083]]: Сквозной цикл `DEBT-XXX` в скиллах (`kb-plan`, `kb-task`, `kb-triage`, `kb-complete`), правилах `AGENTS.md`, шаблонах и `install.py`
  * Обновление `AGENTS.md` (Правила 4, 13, 15 и шапка `02_Tasks/`), `GEMINI.md`, `.clinerules` и `.obsidian/graph.json` (`tag:#techdebt`).
  * Интеграция `TechDebt.md` в скиллы `kb-plan`, `kb-task`, `kb-triage`, `kb-complete`, `kb-lint`, шаблоны `TEMPLATE_INDEX.md`, `TEMPLATE_ONBOARDING.md` и генераторы `install.py`.
- [ ] [[../Specs/21_TechDebtLifecycle/TASK-084-bundle-rebuild-e2e-tests-and-living-spec-sync|TASK-084]]: Сборка монолита `build_installer.py`, E2E тестирование в `tests/test_installer.py` и синхронизация Living Spec (`SPEC.md`, `README.md`, `Onboarding.md`)
  * Пересборка `install.py` через `scripts/build_installer.py`, E2E тесты в `tests/test_installer.py` и актуализация `SPEC.md`, `README.md`, `Onboarding.md`.

---

## 5. Критерии приемки плана (DoD Режима 1)

- [x] Концепция исследована в Режиме 0 ([[../../04_Research/RESEARCH-023-tech-debt-lifecycle-and-cross-mode-sync|RESEARCH-023]], [[../../03_Decisions_ADR/ADR-0028-end-to-end-tech-debt-lifecycle-and-lint-enforcement|ADR-0028]]) и переведена в план (READ-ONLY, без изменения кода).
- [x] Дорожная карта `Roadmap.md` обновлена (Фаза 21).
- [x] Карточки добавлены в `Kanban.md` в `📥 Бэклог`.
- [x] Целостность подтверждена через `scripts/kb_lint.py`.

