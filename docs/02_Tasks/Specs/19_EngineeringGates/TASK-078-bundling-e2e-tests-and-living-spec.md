---
id: TASK-078
title: "Синхронизация install.py, сборка монолита через build_installer.py, E2E тесты и актуализация Living Spec"
status: planned # planned | in-progress | done | cancelled
type: task
phase: 19
component:
  - installer
  - bundling
  - e2e
  - spec
  - docs
parent_plan: "[[../../Plans/PLAN-019-engineering-gates-and-tech-debt-governance|PLAN-019]]"
created: 2026-10-15
updated: 2026-10-15
tags:
  - task/spec
  - phase19
  - installer
  - bundling
  - e2e
  - living-spec
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-078 — Синхронизация install.py, сборка монолита через build_installer.py, E2E тесты и актуализация Living Spec

> **ID:** TASK-078 | **Статус:** К реализации  
> **Фаза:** 19 | **План:** [[../../Plans/PLAN-019-engineering-gates-and-tech-debt-governance|PLAN-019]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../04_Research/RESEARCH-020-self-improving-defect-loop-and-quality-gates|RESEARCH-020]], [[../../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]

---

## 1. Цель задачи

Завершить Фазу 19 комплексным контуром сборки, регрессионного E2E тестирования и актуализации мастер-документации:
1. Синхронизировать генераторы правил и шаблонов в `install.py` с новыми инвариантами и шаблонами Фазы 19.
2. Обеспечить упаковку монолитного дистрибутива `install.py` через `scripts/build_installer.py`.
3. Разработать сквозные E2E тесты в `tests/test_installer.py`, проверяющие создание `TechDebt.md`, корректное обновление без перезаписи и наличие инженерных барьеров.
4. Выполнить требования протокола Living Spec (Living Spec Invariant): обновить `SPEC.md`, `README.md` и руководство разработчика `docs/Onboarding.md`.

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `install.py` — интеграция актуальных правил `AGENTS.md` и шаблонов.
* `[MODIFY]` `scripts/build_installer.py` — сборка монолитного установщика с внедрением ресурсов.
* `[MODIFY]` `tests/test_installer.py` — E2E тесты скаффолдинга техдолга и правил.
* `[MODIFY]` `SPEC.md` — актуализация мастер-спецификации (контур управления техдолгом и инженерные барьеры).
* `[MODIFY]` `README.md` — витрина проекта с описанием новых Quality Gates.
* `[MODIFY]` `docs/Onboarding.md` — онбординг с регламентом триажа $P1/P2$ vs $P3$ и Prior-Art Gate.

---

## 3. Детали реализации

### 3.1. Синхронизация `install.py` и сборщика `build_installer.py`

* Синхронизировать генератор `generate_agents_md()` в `install.py` со свежими инвариантами `AGENTS.md` (правила 13–16).
* Запустить `python scripts/build_installer.py` для перепаковки шаблонов `docs/00_Templates/` и вспомогательных модулей в автономный `install.py`.

### 3.2. Сквозные тесты в `tests/test_installer.py`

Добавить тестовые методы:
* `test_clean_slate_includes_tech_debt()`: проверяет, что при инициализации нового проекта создается валидный `docs/02_Tasks/TechDebt.md`.
* `test_update_preserves_tech_debt()`: проверяет, что при запуске `install.py --update` существующие записи в `TechDebt.md` не стираются и не перезаписываются.
* `test_agents_md_has_quality_gates_and_prior_art()`: проверяет присутствие инвариантов Prior-Art Gate, `ROADMAP-<ID>` и «Замер = артефакт» в развернутом `AGENTS.md`.

### 3.3. Актуализация Living Spec

* **`SPEC.md`:** внести описание реестра `TechDebt.md`, архитектуру Prior-Art Gate, протокол маркировки `ROADMAP-<ID>`, серийные замеры $\ge 3$ и чеклист GUI Acceptance.
* **`README.md`:** отразить инженерные барьеры качества в архитектурных принципах харнесса.
* **`docs/Onboarding.md`:** обновить навигацию по 16 шаблонам и регламент триажа $P1/P2$ vs $P3$.

---

## 4. План верификации (Verification Plan)

- [ ] Сборка инсталлятора: `python scripts/build_installer.py` (Exit code 0).
- [ ] Полный запуск тестового сьюта: `pytest tests/` (Exit code 0, 100% pass).
- [ ] Линт базы знаний: `python scripts/kb_lint.py --path docs` (Exit code 0, 0 broken links).
- [ ] Контроль дрифта спецификации: отсутствие несинхронизированных публичных параметров.

---

## 5. Критерии готовности (DoD)

- [ ] Сборщик `build_installer.py` успешно генерирует монолитный `install.py`.
- [ ] Все E2E тесты в `tests/test_installer.py` зеленые.
- [ ] `SPEC.md`, `README.md` и `docs/Onboarding.md` полностью актуализированы.
- [ ] Аудит целостности `kb_lint.py` не выдает ошибок.
