---
id: BUG-014
title: "Несоответствие количества хуков в test_pre_commit_hooks после добавления kb-lint-fix"
status: fixed
severity: medium
type: bug
target_release: "v0.30.0"
target_phase: 32
release_blocker: false
fixed_in: "v0.30.0"
regression_test: "tests/test_pre_commit_hooks.py::PreCommitManifestTest.test_manifest_structure"
created: 2026-11-19
updated: 2026-11-19
tags:
  - bug
  - defect
  - pre-commit
  - ci
  - tests
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 🐞 Дефект: BUG-014 — Несоответствие количества хуков в test_pre_commit_hooks

> **ID:** BUG-014 | **Критичность:** Medium | **Статус:** fixed  
> **Релиз:** v0.30.0 | **Целевая фаза:** 32 | **Блокер:** Нет  
> **Канбан:** [[../Kanban|Канбан-доска]] | **Спецификация:** [[../../SPEC|SPEC.md]]  
> **Обнаружен:** GitHub Actions Run [44479510040](https://github.com/koudinie101-png/agent-docs-harness/actions/runs/44479510040) (2026-11-19)

---

## 1. Симптомы и окружение

* **Симптом:** GitHub Actions workflow `Rules Check` на ветке `main` падает на шаге `Unit tests` с ошибкой `AssertionError: 2 != 1 : the manifest must declare exactly one hook`. GitHub рассылает уведомления о падении сборки при каждом push в репозиторий.
* **Окружение:** Python 3.8+, GitHub Actions Ubuntu runner / Windows local, репозиторий `agent-docs-harness` начиная с коммита `15a8072` (TASK-115).

## 2. Шаги воспроизведения (Repro Steps)

1. Открыть терминал в корне репозитория.
2. Выполнить команду запуска теста манифеста:
   ```bash
   python -m unittest tests/test_pre_commit_hooks.py
   ```
3. **Фактически:** Тест падает с `AssertionError: 2 != 1 : the manifest must declare exactly one hook`.
4. **Ожидаемо:** Все тесты манифеста проходят успешно, валидируя оба объявленных хука (`kb-lint` и `kb-lint-fix`).

## 3. Диагностика (Логи, Стек-трейс)

```text
FAIL: test_manifest_structure (tests.test_pre_commit_hooks.PreCommitManifestTest.test_manifest_structure)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "tests/test_pre_commit_hooks.py", line 46, in test_manifest_structure
    self.assertEqual(len(hooks), 1, "the manifest must declare exactly one hook")
AssertionError: 2 != 1 : the manifest must declare exactly one hook
```

## 4. Первопричина (Root Cause Analysis — RCA)

В рамках [[../Specs/31_SafeAutoFix/TASK-115-autofix-delivery-spec-and-e2e|TASK-115]] (Фаза 31) в файл `.pre-commit-hooks.yaml` был добавлен второй хук `kb-lint-fix`.
Однако тестовый файл `tests/test_pre_commit_hooks.py`, созданный ранее в рамках [[../Specs/28_GateHygiene/TASK-107-pre-commit-hooks-and-readme|TASK-107]], содержал жесткую проверку на единственность хука:
```python
self.assertEqual(len(hooks), 1, "the manifest must declare exactly one hook")
```
и все последующие проверки структуры адресовались только к `hooks[0]`. При расширении манифеста тест не был обновлен, что привело к нарушению регрессионного контура Tier 1.

## 5. План исправления

* `[MODIFY]` `tests/test_pre_commit_hooks.py`:
  - Обновить `test_manifest_structure`: ожидать ровно 2 хука с идентификаторами `kb-lint` и `kb-lint-fix`.
  - Проверять наличие обязательных ключей (`name`, `description`, `entry`, `language`, `files`, `pass_filenames`, `require_serial`) для обоих хуков.
  - Добавить проверку `entry` для `kb-lint-fix` (содержит `--fix --write` и путь `scripts/kb_lint.py`).
  - Убедиться, что оба хука имеют `language: system`, `pass_filenames: false` и `require_serial: true`.

## 6. Верификация (Regression-First)

1. **RED:** `python -m unittest tests/test_pre_commit_hooks.py` падает на текущем коде (подтверждено).
2. **GREEN:** Применение правок к `tests/test_pre_commit_hooks.py` приводит к успешному прохождению `python -m unittest tests/test_pre_commit_hooks.py`.
3. **REFACTOR / FULL SUITE:** Запуск полного набора тестов:
   ```bash
   python -m unittest discover -s tests -q
   ```
4. **Docs Lint:**
   ```bash
   python scripts/kb_lint.py --path docs
   ```
