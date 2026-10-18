---
id: TASK-098
title: "Харденинг CI-гейта Rules Check (DEBT-002)"
status: planned
type: task
phase: 26
component:
  - ci
  - tests
parent_plan: "[[../../TechDebt|TechDebt.md]]"
created: 2026-10-18
updated: 2026-10-18
tags:
  - task/spec
  - phase26
  - techdebt
  - ci
  - tests
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-098 — Харденинг CI-гейта Rules Check

> **ID:** TASK-098 | **Статус:** К реализации  
> **Фаза:** 26 (Tech Debt Hardening) | **Канбан:** [[../../Kanban|Канбан-доска]]  
> **Долг:** [[../../TechDebt|DEBT-002]] — закрывается этой задачей.  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]] (Tier 1), [[../../../03_Decisions_ADR/ADR-0030-single-source-rule-compiler|ADR-0030]] (правила)

---

## 1. Цель задачи

Закрыть `DEBT-002`: `.github/workflows/rules-check.yml` — Tier 1-гейт корпуса правил — имеет четыре дефекта:

1. Нет `permissions: contents: read` (принцип наименьших привилегий) и `concurrency` с `cancel-in-progress` (параллельные прогоны на один ref).
2. `on: push` без фильтра веток: workflow запускается и на тегах, параллельно с `release.yml`.
3. Гейт не запускает `scripts/kb_lint.py`, хотя линтер входит в Verification Plan проекта.
4. Вывод тестов не подавляется — шумные логи CI.

Дополнительно: закрепить контракт workflow Tier 1 тестом, чтобы правки YAML не откатили харденинг незаметно.

**Вне скоупа:** `release.yml` (у него свои `contents: write` и tag-триггер), шаблон `kb-lint.yml` инсталлятора, `install.py` (workflow исключён из бандла: `EXCLUDED_WORKFLOWS = {"rules-check.yml"}` в `scripts/build_installer.py`).

## 2. Затрагиваемые файлы и скоуп символов

* `[MODIFY]` `.github/workflows/rules-check.yml`:
  - `on.push.branches`: `'**'` (все ветки, без тегов); `on.pull_request.branches`: `main`.
  - `permissions.contents`: `read`; `concurrency` с `cancel-in-progress: true`.
  - `jobs.rules.steps`: шаг `Knowledge Base Lint` (`python scripts/kb_lint.py --path docs`) и `Unit tests` с `-q`.
* `[NEW]` `tests/test_ci_workflows.py`:
  - `RulesCheckWorkflowTest.test_rules_check_hardening()`: маркеры харденинга.
  - `RulesCheckWorkflowTest.test_rules_check_does_not_trigger_on_tags()`: отсутствие `tags:`.

## 3. Детали реализации

### 3.1. Целевой `rules-check.yml`

```yaml
name: Rules Check

on:
  push:
    branches:
      - '**'
  pull_request:
    branches:
      - main

permissions:
  contents: read

concurrency:
  group: "rules-check-${{ github.ref }}"
  cancel-in-progress: true

jobs:
  rules:
    name: Rules Corpus Guard
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Verify AGENTS.md is generated from corpus
        run: python scripts/gen_rules.py --check

      - name: Knowledge Base Lint
        run: python scripts/kb_lint.py --path docs

      - name: Unit tests
        run: python -m unittest discover -s tests -q
```

Требования:
* `permissions` — на уровне workflow, только `contents: read`.
* `concurrency.group` — стабильная группа на ref; `cancel-in-progress: true`.
* `push.branches: ['**']` — все ветки, **не** теги (при наличии `branches` фильтр тегов не применяется). `pull_request.branches: [main]`.
* `kb_lint` — отдельный шаг с Exit code 0; тесты — с `-q` (меньше шума, без потери итога).
* Порядок шагов: corpus check → lint → tests. Ошибка любого шага валит гейт.

### 3.2. Tier 1 тест `tests/test_ci_workflows.py`

```python
#!/usr/bin/env python3
"""TASK-098: Tier 1 guard for the harness-only Rules Check workflow (DEBT-002)."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "rules-check.yml"


class RulesCheckWorkflowTest(unittest.TestCase):
    def _workflow(self):
        return WORKFLOW.read_text(encoding="utf-8")

    def test_rules_check_hardening(self):
        text = self._workflow()
        for marker in (
            "permissions:",
            "contents: read",
            "concurrency:",
            "cancel-in-progress: true",
            "branches:",
            "python scripts/kb_lint.py --path docs",
            "discover -s tests -q",
        ):
            self.assertIn(marker, text, "rules-check.yml lost CI hardening marker: %s" % marker)

    def test_rules_check_does_not_trigger_on_tags(self):
        text = self._workflow()
        self.assertNotIn("tags:", text, "rules-check.yml must not run on tag pushes (release.yml owns tags)")
```

Требования:
* Тест читает файл-источник напрямую, без сети и без бандла (workflow в бандл не входит).
* Проверяются именно маркеры контракта, а не побайтовый YAML (форматирование может меняться).
* `tags:` отсутствует во всём файле — это защита от возврата tag-триггера.

### 3.3. Совместимость

* `rules-check.yml` — harness-only: `scripts/build_installer.py` исключает его из `EMBEDDED_ASSETS`; `install.py` не пересобирается.
* `release.yml` не трогаем: у него `contents: write` и `tags: v*` по назначению.
* Клиентские проекты не получают этот workflow (он не входит в дистрибутив).

## 4. План верификации (Verification Plan)

- [ ] Tier 1 тест: `python -m unittest tests.test_ci_workflows` → 2 теста OK.
- [ ] Синтаксис теста: `python -m py_compile tests/test_ci_workflows.py` → Exit code 0.
- [ ] Полный прогон (sandbox-safe, [[../../../06_Memory/Incidents/INC-003-dsh-sandbox-tempfile-mkdtemp-mode|INC-003]] / TRG-03): `python tmp/run_tests.py` → все тесты OK (163 + 2 новых).
- [ ] Целостность: `python scripts/kb_lint.py --path docs` → Exit code 0, 0 битых ссылок, 0 Symbolic Scope Warnings.
- [ ] `git diff --check` → нет trailing whitespace; YAML-отступы проверены вручную (Zero-Deps: PyYAML не используется).
- [ ] 4-State UI / скриншоты: не применимо (CI-конфигурация).
- [ ] Замеры $\ge 3$ прогонов: не применимо.

## 5. Критерии готовности (DoD)

- [ ] `rules-check.yml` содержит `permissions: contents: read`, `concurrency`/`cancel-in-progress`, branch-фильтр без тегов, шаг `kb_lint` и `-q` для тестов.
- [ ] Tier 1 `tests/test_ci_workflows.py` добавлен и зелёный; полный suite и `kb_lint` зелёные.
- [ ] `DEBT-002` переведён в `Resolved Debt` со ссылкой на `TASK-098` на шаге `/kb-complete`.
- [ ] Статус обновлён в Kanban, Roadmap и Devlog.
