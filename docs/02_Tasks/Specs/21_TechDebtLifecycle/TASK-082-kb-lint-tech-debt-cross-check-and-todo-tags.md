---
id: TASK-082
title: "Семантический кросс-чек TechDebt.md с фазами/задачами #techdebt и поддержка кодовых тегов // DEBT-XXX в scripts/kb_lint.py"
status: done # planned | in-progress | done | cancelled
type: task
phase: 21
component:
  - lint
  - techdebt
  - quality-gates
parent_plan: "[[../../Plans/PLAN-021-tech-debt-lifecycle-and-cross-mode-sync|PLAN-021]]"
created: 2026-10-16
updated: 2026-10-18
tags:
  - task/spec
  - phase21
  - lint
  - techdebt
  - quality-gates
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-082 — Семантический кросс-чек TechDebt.md с фазами/задачами #techdebt и поддержка кодовых тегов // DEBT-XXX в scripts/kb_lint.py

> **ID:** TASK-082 | **Статус:** Выполнено (Режим 3)  
> **Фаза:** 21 | **План:** [[../../Plans/PLAN-021-tech-debt-lifecycle-and-cross-mode-sync|PLAN-021]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../04_Research/RESEARCH-023-tech-debt-lifecycle-and-cross-mode-sync|RESEARCH-023]], [[../../../03_Decisions_ADR/ADR-0028-end-to-end-tech-debt-lifecycle-and-lint-enforcement|ADR-0028]]

---

## 1. Цель задачи

Устранить слепую зону механического контроля (Tier 1 Quality Gate) в `scripts/kb_lint.py`, из-за которой в проектах создаются планы и задачи с тегом `#techdebt` при пустом реестре `docs/02_Tasks/TechDebt.md`, а кодовые комментарии `// TODO(DEBT-001)` ошибочно помечаются как неразмеченные:
1. **Поддержка `DEBT-XXX` в `check_untracked_todos(docs_dir: Path) -> List[str]`:** разрешить привязку комментариев `TODO`/`FIXME` как к `ROADMAP-<ID>`, так и к `DEBT-\d{3,}` (`r'(?:ROADMAP-[A-Za-z0-9_-]+|DEBT-\d{3,})'`).
2. **Семантический кросс-чек в `check_tech_debt_integrity(docs_dir: Path, file_map: Optional[Dict[str, Path]] = None) -> List[str]`:**
   - Собирать множество валидных идентификаторов `DEBT-XXX` (активных и погашенных) в `TechDebt.md`.
   - Сканировать документы в `02_Tasks/Plans/` и `02_Tasks/Specs/` на наличие тега `techdebt` или `tech-debt` в YAML frontmatter (исключая мета-документы самого харнесса `PLAN-019`, `PLAN-021`, `TASK-075`..`TASK-084`).
   - Если найден план/спецификация с тегом `techdebt`/`tech-debt`, который не содержит ссылки на `DEBT-\d{3,}` (или если в `TechDebt.md` 0 записей `DEBT-XXX`), добавлять неблокирующее предупреждение `WARN: ...` (без падения с Exit code 1).
3. **Разделение `debt_errors` и `debt_warnings` в `run_linter()`:** строки из `check_tech_debt_integrity()`, начинающиеся с `"WARN:"`, маршрутизировать в `debt_warnings` (неблокирующие), сохраняя синтаксические нарушения `TechDebt.md` в `debt_errors` (Exit code 1).
4. **Покрытие модульными тестами в `tests/test_kb_lint.py`:** проверка `// TODO(DEBT-001)`, предупреждений `WARN` при наличии `#techdebt`-задачи и пустом `TechDebt.md`, и отсутствия предупреждений при наличии валидной связки `DEBT-001`.

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `scripts/kb_lint.py` — обновление `check_untracked_todos()`, `check_tech_debt_integrity()` и фильтрации `debt_errors` / `debt_warnings` в `run_linter()`.
* `[MODIFY]` `tests/test_kb_lint.py` — модульные тесты для `DEBT-XXX` в `check_untracked_todos()` и кросс-проверки `#techdebt` в `check_tech_debt_integrity()`.

---

## 3. Детали реализации

### 3.1. Расширение `check_untracked_todos()` в `scripts/kb_lint.py`

```python
        for line_no, line in enumerate(content.splitlines(), start=1):
            line_to_check = re.sub(r'`[^`]*`', '', line)
            if active_pattern.search(line_to_check):
                if not re.search(r'(?:ROADMAP-[A-Za-z0-9_-]+|DEBT-\d{3,})', line, re.IGNORECASE):
                    warnings.append(
                        f"Untracked TODO without ROADMAP-<ID> or DEBT-XXX reference in {rel_name}:{line_no}"
                    )
```

### 3.2. Кросс-чек `#techdebt` в `check_tech_debt_integrity()` и `run_linter()`

1. В `check_tech_debt_integrity(docs_dir, file_map)` отслеживать `recorded_debt_ids: Set[str]` из строк таблиц `TechDebt.md` с `^DEBT-\d{3,}$`.
2. Обходить `*.md` в `02_Tasks/Plans/` и `02_Tasks/Specs/`, пропуская шаблоны (`TEMPLATE_`) и мета-документы харнесса (`HARNESS_META_TECHDEBT_IDS = {"PLAN-019", "PLAN-021", "TASK-075", "TASK-076", "TASK-077", "TASK-078", "TASK-082", "TASK-083", "TASK-084"}`).
3. При наличии `techdebt` / `tech-debt` во frontmatter и отсутствии `DEBT-\d{3,}` в теле документа (либо при пустом `recorded_debt_ids`) добавлять `WARN: ...`.
4. В `run_linter()` фильтровать `e.startswith("WARN:")` в `debt_warnings` (неблокирующие) и избегать дублирования префикса `WARN: WARN:` в silent-режиме.

### 3.3. Модульные тесты в `tests/test_kb_lint.py`

* `test_check_untracked_todos_accepts_debt_xxx_reference`
* `test_check_tech_debt_warns_when_techdebt_tagged_spec_has_empty_registry`
* `test_check_tech_debt_passes_when_techdebt_spec_references_debt_id`

---

## 4. План верификации (Verification Plan)

- [x] Сборка: `py -3 -m py_compile scripts/kb_lint.py tests/test_kb_lint.py` (Exit code 0).
- [x] Автотесты линтера: `py -3 -m unittest tests/test_kb_lint.py` (Exit code 0, 100% pass).
- [x] Проверка базы знаний: `py -3 scripts/kb_lint.py --path docs` (0 broken links, Exit code 0).

---

## 5. Критерии готовности (DoD)

- [x] Код написан строго по ТЗ без заглушек.
- [x] Все пункты Плана верификации пройдены.
- [x] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [x] Запись добавлена в `Devlog.md`.
