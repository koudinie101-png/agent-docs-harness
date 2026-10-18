---
id: TASK-084
title: "Сборка монолита build_installer.py, E2E тестирование в tests/test_installer.py и синхронизация Living Spec (SPEC.md, README.md, Onboarding.md)"
status: done # planned | in-progress | done | cancelled
type: task
phase: 21
component:
  - installer
  - tests
  - docs
parent_plan: "[[../../Plans/PLAN-021-tech-debt-lifecycle-and-cross-mode-sync|PLAN-021]]"
created: 2026-10-16
updated: 2026-10-18
tags:
  - task/spec
  - phase21
  - installer
  - e2e
  - spec
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-084 — Сборка монолита build_installer.py, E2E тестирование в tests/test_installer.py и синхронизация Living Spec

> **ID:** TASK-084 | **Статус:** Выполнено (Режим 3)  
> **Фаза:** 21 | **План:** [[../../Plans/PLAN-021-tech-debt-lifecycle-and-cross-mode-sync|PLAN-021]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../04_Research/RESEARCH-023-tech-debt-lifecycle-and-cross-mode-sync|RESEARCH-023]], [[../../../03_Decisions_ADR/ADR-0028-end-to-end-tech-debt-lifecycle-and-lint-enforcement|ADR-0028]]

---

## 1. Цель задачи

Завершить Фазу 21 пересборкой автономного инсталлятора `install.py`, сквозным E2E-тестированием развернутой инфраструктуры и актуализацией Living Spec (`SPEC.md`, `README.md`, `Onboarding.md`):
1. **Пересборка бандла `install.py`:** упаковать в `EMBEDDED_ASSETS_B64` обновленные `scripts/kb_lint.py`, скиллы `.agents/skills/kb-*` и шаблоны `00_Templates/` через `scripts/build_installer.py`.
2. **Сквозные E2E-тесты в `tests/test_installer.py`:** проверить, что в развернутом проекте:
   - `AGENTS.md` и IDE-адаптеры содержат сквозной цикл `DEBT-XXX`, тег `#techdebt` и `// DEBT-XXX`;
   - `.obsidian/graph.json` содержит цветовую группу `tag:#techdebt`;
   - развернутые скиллы (`kb-plan`, `kb-task`, `kb-triage`, `kb-complete`) и шаблоны (`TEMPLATE_INDEX.md`, `TEMPLATE_ONBOARDING.md`) ссылаются на `TechDebt.md`;
   - развернутый `scripts/kb_lint.py` поддерживает `// DEBT-XXX` и выдает `WARN` при наличии `#techdebt`-задачи и пустом `TechDebt.md`.
3. **Синхронизация Living Spec:** отразить Фазу 21 и `ADR-0028` в `SPEC.md`, `README.md` и `Docs-As-Code/Onboarding.md`.

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `install.py` — обновление `EMBEDDED_ASSETS_B64` через `scripts/build_installer.py`.
* `[MODIFY]` `scripts/build_installer.py` — при необходимости поддержка чтения шаблонов из `docs/` или `Docs-As-Code/`.
* `[MODIFY]` `tests/test_installer.py` — добавление E2E-теста `test_tech_debt_end_to_end_lifecycle_and_lint_cross_check`.
* `[MODIFY]` `SPEC.md` — описание сквозного цикла `TechDebt.md` (`ADR-0028`) и Фазы 21.
* `[MODIFY]` `README.md` — актуализация правил управления техдолгом (`DEBT-XXX`, `// DEBT-XXX`, `#techdebt`).
* `[MODIFY]` `Docs-As-Code/Onboarding.md` — описание полного цикла `Active P3 Debt -> Plan/Task -> Resolved Debt` в `TechDebt.md`.

---

## 3. Детали реализации

### 3.1. Пересборка автономного инсталлятора
```bash
py -3 scripts/build_installer.py
```

### 3.2. Сквозной E2E-тест в `tests/test_installer.py`
```python
def test_tech_debt_end_to_end_lifecycle_and_lint_cross_check(self):
    """Verifies Phase 21 (ADR-0028): TechDebt.md SSOT rules, skills, graph.json #techdebt, and kb_lint cross-check."""
```
Проверяемые инварианты:
1. В сгенерированном `AGENTS.md` присутствуют `DEBT-XXX`, `#techdebt` и `Resolved Debt`.
2. В `docs/.obsidian/graph.json` присутствует `tag:#techdebt`.
3. В `.agents/skills/kb-plan/SKILL.md` и `.agents/skills/kb-complete/SKILL.md` присутствует `TechDebt.md`.
4. В `docs/00_Templates/TEMPLATE_INDEX.md` и `TEMPLATE_ONBOARDING.md` присутствует ссылка на `TechDebt`.
5. Развернутый `scripts/kb_lint.py` выдает `WARN:` при создании задачи с `tags: [task/spec, techdebt]` и пустом `TechDebt.md` (Exit code 0), и не выдает предупреждений после добавления `DEBT-001` в `TechDebt.md` и текст задачи.

### 3.3. Синхронизация `SPEC.md`, `README.md`, `Onboarding.md`
* В `SPEC.md`: обновить инвариант `Tech Debt Governance & Review Triage` (Правило 13) и `Traceable Backlog Tags` (`// ROADMAP-<ID>` и `// DEBT-XXX`), добавить раздел **Фаза 21**.
* В `README.md` и `Onboarding.md`: отразить сквозной цикл `DEBT-XXX` и семантическую сверку в `kb_lint.py`.

---

## 4. План верификации (Verification Plan)

- [x] Пересборка бандла: `py -3 scripts/build_installer.py` (Exit code 0).
- [x] Компиляция: `py -3 -m py_compile install.py scripts/*.py` (Exit code 0).
- [x] Полный прогон тестов: `py -3 -m unittest discover -s tests` (Exit code 0, 100% pass).
- [x] Проверка базы знаний: `py -3 scripts/kb_lint.py --path docs` (0 broken links, Exit code 0).

---

## 5. Критерии готовности (DoD)

- [x] Автономный бандл `install.py` пересобран и проверен E2E-тестами.
- [x] Документация `SPEC.md`, `README.md`, `Onboarding.md` синхронизирована (Living Spec).
- [x] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`), Плане (`PLAN-021`) и Дорожной карте (`[x]`).
- [x] Запись добавлена в `Devlog.md`.
