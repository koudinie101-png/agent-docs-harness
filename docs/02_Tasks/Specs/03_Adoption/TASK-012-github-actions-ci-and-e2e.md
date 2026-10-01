---
id: TASK-012
title: "Шаблон GitHub Actions CI (.github/workflows/kb-lint.yml) и комплексное E2E тестирование"
status: planned
type: task
phase: 3
component:
  - installer
  - ci
  - testing
  - docs
parent_plan: "[[../../Plans/PLAN-003-brownfield-adoption-and-lifecycle|PLAN-003]]"
created: 2026-10-01
updated: 2026-10-01
tags:
  - task/spec
  - phase3
  - component/installer
  - component/ci
  - component/testing
  - component/docs
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-012 — Шаблон GitHub Actions CI и комплексное E2E тестирование

> **ID:** TASK-012  
> **Статус:** К реализации (Режим 2)  
> **Теги:** #task/spec #phase3 #component/installer #component/ci #component/testing #component/docs  
> **Родительский план:** [[../../Plans/PLAN-003-brownfield-adoption-and-lifecycle|PLAN-003]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

1. Добавить генерацию готового workflow GitHub Actions для автоматического аудита базы знаний при Pull Request и Push (`.github/workflows/kb-lint.yml`).
2. Добавить CLI-флаг `--ci [github|none]` и вопрос в интерактивный мастер инсталлятора `install.py`.
3. Реализовать комплексный набор сквозных E2E тестов в `tests/test_installer.py`, покрывающий все сценарии Фазы 3:
   - Чистый старт (Clean Slate Scaffolding).
   - Автодетект стека и безопасная интеграция в существующие проекты (Brownfield Adoption).
   - Обновление компонентов (`install.py --update`).
   - Генерация CI-конфигурации (`--ci github`).
4. Обновить документацию `README.md`, отразив новые флаги и возможности Фазы 3.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `install.py`:
  * Добавление аргумента `--ci` со значениями `github`, `none` (по умолчанию `none`).
  * Добавление шага выбора CI в интерактивный мастер.
  * Реализация функции `generate_github_actions_workflow(target_dir: Path)`.
* `[MODIFY]` `tests/test_installer.py`:
  * Добавление тестов генерации CI-workflow:
    - Проверка создания `.github/workflows/kb-lint.yml`.
    - Проверка синтаксиса YAML и команд запуска линтера.
  * Сквозные тесты полного цикла установки и обновления.
* `[MODIFY]` `README.md`:
  * Описание флага `--ci github` и сценария защиты базы знаний в командной разработке.
  * Описание флага `--update` для сопровождения проектов.
  * Описание автодетекта технологического стека.

---

## 3. Детали технической реализации

### 3.1. Содержимое `.github/workflows/kb-lint.yml`
```yaml
name: Docs-as-Code Knowledge Base Audit

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  kb-lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Run Knowledge Base Linter
        run: |
          python scripts/kb_lint.py --path docs
```

### 3.2. Генератор в `install.py`
```python
def deploy_ci_workflow(target_dir: Path, ci_provider: str):
    if ci_provider == "github":
        workflow_dir = target_dir / ".github" / "workflows"
        workflow_dir.mkdir(parents=True, exist_ok=True)
        workflow_file = workflow_dir / "kb-lint.yml"
        workflow_file.write_text(GITHUB_ACTIONS_WORKFLOW_TEMPLATE, encoding="utf-8")
        print("✅ Deployed GitHub Actions CI workflow (.github/workflows/kb-lint.yml).")
```

---

## 4. План верификации (Verification Plan)

### Сборка и синтаксис:
- [ ] Проверка синтаксиса: `python -m py_compile install.py` (Exit code 0).
- [ ] Сборка через `python scripts/build_installer.py` (Exit code 0, размер < 82 КБ).

### Автоматические тесты:
- [ ] Запуск `python -m unittest discover -s tests` (все тесты проходят, 100% pass).
- [ ] Тест развертывания проекта с флагом `--ci github`:
  - Файл `.github/workflows/kb-lint.yml` создан.
  - Содержит шаги `actions/checkout` и запуск `scripts/kb_lint.py`.
- [ ] Тест без флага `--ci` (по умолчанию папка `.github/workflows` не создается).

### Документация:
- [ ] Проверка базы знаний через `python scripts/kb_lint.py --path docs` (0 broken links, valid frontmatter).

---

## 5. Критерии готовности (Definition of Done)

- [ ] Флаг `--ci github` генерирует готовый workflow для автоматической валидации базы знаний в GitHub Actions.
- [ ] Интерактивный мастер поддерживает выбор генерации CI.
- [ ] Все новые возможности Фазы 3 покрыты автоматическими тестами в `test_installer.py`.
- [ ] `README.md` актуализирован.
- [ ] `docs/02_Tasks/Kanban.md` и `docs/02_Tasks/Roadmap.md` обновлены, все вехи Фазы 3 закрыты.
