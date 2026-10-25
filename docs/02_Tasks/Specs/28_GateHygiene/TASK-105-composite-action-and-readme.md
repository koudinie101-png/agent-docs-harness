---
id: TASK-105
title: "Composite GitHub Action для линта и раздел README"
status: done
type: task
phase: 28
component:
  - ci
  - distribution
  - docs
parent_plan: "[[../../Plans/PLAN-026-ci-delivery-and-code-scanning|PLAN-026]]"
created: 2026-10-25
updated: 2026-10-25
tags:
  - task/spec
  - phase28
  - ci
  - distribution
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-105 — Composite GitHub Action и README

> **ID:** TASK-105 | **Статус:** Выполнено (Режим 3)  
> **Фаза:** 28 | **План:** [[../../Plans/PLAN-026-ci-delivery-and-code-scanning|PLAN-026]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0032-machine-readable-lint-contract-and-rule-registry|ADR-0032]], [[../../../04_Research/RESEARCH-027-competitor-best-practices-and-adoption-backlog|RESEARCH-027]] (§4 Волна 1 п.2)  
> **Следующая задача:** `TASK-107` потребляет это действие через `uses: ./` (смоук + Code Scanning)

---

## 1. Цель задачи

Дать внешний вход в линт без установки харнесса: `uses: koudinie101-png/agent-docs-harness@v0.27.0` с входами `path`, `format`, `output-file`, `python-version`, `extra-args`. Действие — **тонкая обёртка** над `scripts/kb_lint.py`: своей логики проверок не содержит, только запускает скрипт из `$GITHUB_ACTION_PATH` и возвращает его exit-код.

Действие **производит** SARIF/JSON-файл и не загружает его: права `security-events: write` объявляет только workflow вызывающего, composite-действие выдать их себе не может (PLAN-026 Q1). В `action.yml` не должно быть ни `upload-sarif`, ни `security-events` — это закрепляется Tier 1-тестом.

### 1.1. Аудит перед спецификацией (2026-10-25)

| Проверка | Факт | Следствие |
| :--- | :--- | :--- |
| `action.yml` в корне | Отсутствует | GitHub пока не считает репозиторий действием; файл добавляется впервые |
| `scripts/build_installer.py` | Бандл — whitelist (`templates/`, 3 скрипта, скиллы, workflows, `rules/`, `patterns.md`) | `action.yml` в бандл не попадёт; клиентские проекты не затрагиваются |
| `scripts/kb_lint.py` | `--format {text,json,sarif}`, `--version`, exit `0/1`, `--path` резолвит `docs`/корень | Действию достаточно одной команды; `--version` не нужен |
| `rules-check.yml` / `release.yml` | `actions/setup-python@v5`, `python scripts/kb_lint.py --path docs` | Тот же паттерн Python внутри composite |
| `tests/test_ci_workflows.py` | Guard по строковым маркерам, без YAML-парсера (Zero-Deps) | Тот же приём для `action.yml`; настоящая валидация YAML — прогон workflow в TASK-107 |
| `install.py::deploy_ci_workflow` | Клиентам генерируется `kb-lint.yml` из inline-шаблона (`run: python scripts/kb_lint.py`) | Переводить клиентский шаблон на `uses:` — **не** эта задача (см. §3, non-goal) |

## 2. Затрагиваемые файлы и скоуп символов

* `[NEW]` `action.yml`:
  - `name`, `description`, `author`, `branding` — метаданные действия (обязательны для маркетплейса/валидности).
  - `inputs` — `path`, `format`, `output-file`, `python-version`, `extra-args`.
  - `outputs` — `output-file` (`steps.lint.outputs.output-file`).
  - `runs` — `using: composite`; шаги `setup-python` и `lint` (id `lint`, `shell: bash`).
* `[MODIFY]` `README.md`:
  - §«🛡️ Continuous Integration & Release Automation (GitHub Actions)» — подраздел «Use as a GitHub Action» с примером workflow (lint + `upload-sarif`) и перечнем прав.
* `[MODIFY]` `tests/test_ci_workflows.py`:
  - `ActionYmlContractTest.test_action_metadata_and_composite_contract()` — маркеры контракта.
  - `ActionYmlContractTest.test_action_does_not_upload_sarif_or_request_permissions()` — запрет `upload-sarif`/`security-events` внутри действия.

## 3. Детали реализации

### 3.1. Контракт `action.yml`

```yaml
name: 'Docs-as-Code Knowledge Base Lint'
description: 'Zero-dependency Docs-as-Code audit: broken wikilinks, YAML frontmatter, phases, tech debt, memory and assets'
author: 'agent-docs-harness'
branding:
  icon: 'check-circle'
  color: 'purple'
inputs:
  path:          { description: 'Knowledge base directory or project root', required: false, default: 'docs' }
  format:        { description: 'Output format: text, json or sarif',      required: false, default: 'text' }
  output-file:   { description: 'File written when format is json or sarif', required: false, default: 'kb-lint.sarif' }
  python-version:{ description: 'Python version for the linter',           required: false, default: '3.11' }
  extra-args:    { description: 'Additional kb_lint.py arguments',         required: false, default: '' }
outputs:
  output-file:
    description: 'Path to the machine-readable report (json/sarif)'
    value: ${{ steps.lint.outputs.output-file }}
runs:
  using: composite
  steps:
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ inputs.python-version }}
    - name: Run knowledge base lint
      id: lint
      shell: bash
      env:
        KB_PATH: ${{ inputs.path }}
        KB_FORMAT: ${{ inputs.format }}
        KB_OUTPUT: ${{ inputs.output-file }}
        KB_EXTRA: ${{ inputs.extra-args }}
      run: |
        set -u
        python_bin="$(command -v python3 || command -v python)"
        lint="$GITHUB_ACTION_PATH/scripts/kb_lint.py"
        if [ "${KB_FORMAT}" = "text" ]; then
          # shellcheck disable=SC2086
          exec "${python_bin}" "${lint}" --path "${KB_PATH}" --format text ${KB_EXTRA}
        fi
        mkdir -p "$(dirname "${KB_OUTPUT}")"
        rc=0
        # shellcheck disable=SC2086
        "${python_bin}" "${lint}" --path "${KB_PATH}" --format "${KB_FORMAT}" ${KB_EXTRA} > "${KB_OUTPUT}" || rc=$?
        echo "output-file=${KB_OUTPUT}" >> "${GITHUB_OUTPUT}"
        if [ "${rc}" -ne 0 ]; then
          echo "::error::kb_lint reported errors (exit ${rc}); see ${KB_OUTPUT}"
        fi
        exit "${rc}"
```

Обязательные инварианты (проверяются тестом):

* `using: composite`, `shell: bash` (bash есть на ubuntu/macos/windows-раннерах).
* путь к линтеру — `$GITHUB_ACTION_PATH/scripts/kb_lint.py`, **не** `scripts/…` относительно workspace (иначе действие сломается в проекте без установленного харнесса).
* вывод в `GITHUB_OUTPUT` только при `format != text`.
* `set -u` (не `-e`): exit-код линта пробрасывается, а не теряется в пайпе.
* `mkdir -p "$(dirname …)"` — защита от вложенного `output-file`.
* Ни `upload-sarif`, ни `security-events`, ни `permissions` внутри действия.

### 3.2. README: «Use as a GitHub Action»

```markdown
#### Use as a GitHub Action
```yaml
permissions:
  contents: read
  security-events: write   # only needed for the SARIF upload step
jobs:
  kb-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: koudinie101-png/agent-docs-harness@v0.27.0
        with:
          path: docs
          format: sarif
      - uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: kb-lint.sarif
```

* Действие не загружает SARIF: загрузка — отдельный шаг потребителя (права выдаёт вызывающий workflow).
* `format: text` пишет находки в лог и падает на `error`; `json`/`sarif` пишут файл и тоже падают на `error` (exit-код общий для всех форматов).
* Ограничение SARIF: локации на уровне файла, без `region.startLine` (`DEBT-004`).
```

### 3.3. Non-goals

* Не менять inline-шаблон `install.py::deploy_ci_workflow` (клиентский `kb-lint.yml` остаётся `run: python scripts/kb_lint.py`) — иначе ломается офлайн-сценарий установленных проектов, где действие недоступно.
* Не добавлять `uses: ./`-смоук здесь — это TASK-107 (там же Code Scanning).
* Не публиковать действие в Marketplace (отдельное решение, вне фазы).

## 4. План верификации (Verification Plan)

- [x] `python -m unittest tests.test_ci_workflows -v` → все тесты OK, включая 2 новых.
- [x] Полный набор: `python scripts/run_tests_sandbox.py` → **182+ теста OK**.
- [x] Локальная эмуляция тела действия: `python scripts/kb_lint.py --path docs --format sarif > tmp/kb-lint.sarif` → Exit 0, файл парсится `json.loads` (та же команда, что в `run:`).
- [x] Error-путь: во временном хранилище с битой ссылкой `--format sarif` → Exit 1 (действие пробросит код).
- [x] `git status --short` не содержит `install.py` / `dist/install.py` (действие не бандлится).
- [x] `python scripts/kb_lint.py --path docs --verbose` → 0 битых ссылок, 0 `WARN`.
- [x] README: раздел присутствует, пример валиден по маркерам, ссылка на `DEBT-004` на месте.

* **Замеры $\ge 3$ прогонов:** не применимы (YAML-контракт, производительность не заявляется).
* **Ограничение проверки:** синтаксис YAML и поведение composite локально не исполняются — первая настоящая проверка будет в TASK-107 (`uses: ./`); если действие окажется невалидным, дефект оформляется `BUG-XXX`.

### Visual DoD (для задач с GUI/TUI):

Не применимо: изменений пользовательского интерфейса нет; поверхность — YAML-контракт и лог CI (скриншот Security-панели появляется в TASK-107).

## 5. Критерии готовности (DoD)

- [x] `action.yml` создан, содержит composite-шаг, `$GITHUB_ACTION_PATH`, `shell: bash`, все пять входов и один выход.
- [x] В `action.yml` нет `upload-sarif`, `security-events`, `permissions` (Tier 1-тест).
- [x] README-раздел «Use as a GitHub Action» с примером и оговоркой про `DEBT-004`.
- [x] Полный набор тестов зелёный; `kb_lint` — 0 битых.
- [x] Бандл не тронут (`install.py` / `dist/install.py` отсутствуют в диффе); статусы обновлены (ТЗ/Канбан/Roadmap), запись в `Devlog.md` — на шаге `/kb-complete`.
