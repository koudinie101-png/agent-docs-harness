---
id: TASK-108
title: "Code Scanning: собственный SARIF-workflow и исключение из бандла"
status: in-progress
type: task
phase: 28
component:
  - ci
  - installer
  - tests
parent_plan: "[[../../Plans/PLAN-026-ci-delivery-and-code-scanning|PLAN-026]]"
created: 2026-10-25
updated: 2026-10-25
tags:
  - task/spec
  - phase28
  - ci
  - code-scanning
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-108 — Code Scanning в собственном репозитории

> **ID:** TASK-108 | **Статус:** К реализации (Режим 2)  
> **Фаза:** 28 | **План:** [[../../Plans/PLAN-026-ci-delivery-and-code-scanning|PLAN-026]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Зависимость:** [[28_GateHygiene/TASK-105-composite-action-and-readme|TASK-105]] (workflow использует действие через `uses: ./`)  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0032-machine-readable-lint-contract-and-rule-registry|ADR-0032]], [[../../../04_Research/RESEARCH-027-competitor-best-practices-and-adoption-backlog|RESEARCH-027]] (§4 Волна 1 п.2)

---

## 1. Цель задачи

Дать SARIF-контракту **реального потребителя**: собственный workflow запускает линт, загружает отчёт в GitHub Code Scanning, и в Security-панели появляются алерты с `ruleId` (`KB-XXX`). Это одновременно:

* закрывает «ручную приёмку SARIF», отложенную в `TASK-102` (H1 из PLAN-026: примет ли Code Scanning наш минимальный документ без `region`);
* снимает блокер с `TASK-109`: решение по `DEBT-004` (нужны ли номера строк) принимается по фактическим аннотациям, а не по догадке;
* проверяет `action.yml` вживую (`uses: ./`) — до этого действие ни разу не исполнялось.

### 1.1. Аудит перед спецификацией (2026-10-25)

| Проверка | Факт | Следствие |
| :--- | :--- | :--- |
| Видимость репозитория | `PUBLIC` | Code Scanning доступен бесплатно; `gh api …/code-scanning/analyses` доступен с текущей авторизацией |
| `rules-check.yml` | `permissions: contents: read`, push(all)+PR | Расширять его правами `security-events` нельзя — отдельный workflow (least privilege) |
| `release.yml` | Триггер `push: tags: v*` | Новый workflow не должен реагировать на теги (релиз — зона `release.yml`) |
| `scripts/build_installer.py` | Бандлит все workflows, кроме `EXCLUDED_WORKFLOWS = {"rules-check.yml"}` | Без правки клиенты получат workflow с `security-events: write` и нашим контекстом → красный CI |
| `action.yml` | `format: sarif` пишет файл и возвращает exit-код | Workflow может сначала загрузить отчёт, затем упасть по факту ошибок |
| `gh` CLI | Авторизован (`gh auth status` ранее: authenticated) | Верификация приёмки через API, без скриншотов UI |

## 2. Затрагиваемые файлы и скоуп символов

* `[NEW]` `.github/workflows/code-scanning.yml`:
  - `on` — push в `main`, PR в `main`, `workflow_dispatch` (без тегов).
  - `permissions` — `contents: read`, `security-events: write`; `concurrency` с `cancel-in-progress: true`.
  - `jobs.kb-lint.steps` — checkout, `uses: ./` (наше действие, `format: sarif`), `upload-sarif` с `if: always()` и fork-guard, `category: kb-lint`.
* `[MODIFY]` `scripts/build_installer.py`:
  - `EXCLUDED_WORKFLOWS` — добавить `"code-scanning.yml"` (workflow только для этого репозитория).
* `[MODIFY]` `tests/test_ci_workflows.py`:
  - `CodeScanningWorkflowTest.test_workflow_hardening()` — маркеры прав, триггеров, `uses: ./`, `upload-sarif`, fork-guard.
  - `CodeScanningWorkflowTest.test_rules_check_keeps_least_privilege()` — в `rules-check.yml` нет `security-events`.
  - `CodeScanningWorkflowTest.test_harness_only_workflows_are_not_bundled()` — живой вызов `build_installer.bundle_assets()` (с перехватом stdout): `rules-check.yml` и `code-scanning.yml` отсутствуют, `release.yml` присутствует.

## 3. Детали реализации

### 3.1. Workflow

```yaml
name: Code Scanning

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  security-events: write

concurrency:
  group: "code-scanning-${{ github.ref }}"
  cancel-in-progress: true

jobs:
  kb-lint:
    name: Knowledge Base Lint (SARIF)
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Run knowledge base lint
        id: lint
        uses: ./
        with:
          path: docs
          format: sarif
          output-file: kb-lint.sarif

      - name: Upload SARIF to Code Scanning
        if: always() && (github.event_name != 'pull_request' || github.event.pull_request.head.repo.full_name == github.repository)
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: ${{ steps.lint.outputs.output-file || 'kb-lint.sarif' }}
          category: kb-lint
```

Обязательные инварианты (проверяются тестом):

* `uses: ./` — единственная проверка действия вживую; ручной вызов `python scripts/kb_lint.py` здесь запрещён (иначе действие остаётся непроверенным).
* `if: always()` на загрузке — SARIF загружается даже когда линт нашёл ошибки; при этом job остаётся красным, потому что шаг действия упал.
* fork-guard: на PR из форка `security-events: write` недоступен, загрузка была бы ошибкой; такие PR линтуются, но без загрузки.
* нет `tags:` — релизные теги обслуживает `release.yml`.
* `category: kb-lint` — отдельная категория алертов, чтобы не смешиваться с другими анализаторами.

### 3.2. Исключение из бандла

```python
EXCLUDED_WORKFLOWS = {"rules-check.yml", "code-scanning.yml"}
```

Тест вызывает `bundle_assets()` (не читает готовый `install.py`), поэтому ловит регрессию даже если бандл не пересобирали. Вывод функции перехватывается `contextlib.redirect_stdout`, чтобы не засорять лог тестов.

### 3.3. Non-goals

* Изменение `rules-check.yml` (права) — запрещено.
* Загрузка SARIF внутрь `action.yml` — отклонено в PLAN-026 Q1.
* Настройка branch protection / required checks — вне задачи.

## 4. План верификации (Verification Plan)

- [ ] `python -m py_compile scripts/build_installer.py tests/test_ci_workflows.py` → Exit 0.
- [ ] `python -m unittest tests.test_ci_workflows -v` → 8 тестов OK (5 прежних + 3 новых).
- [ ] Полный набор: `python scripts/run_tests_sandbox.py` → **191 тест OK** (188 + 3).
- [ ] `git status --short` не содержит `install.py` / `dist/install.py` (пересборка не требуется: бандл и так не содержит новый workflow).
- [ ] После пуша: `gh run list --workflow=code-scanning.yml -L 1` → последний запуск `completed/success`.
- [ ] Приёмка SARIF: `gh api repos/koudinie101-png/agent-docs-harness/code-scanning/analyses` → есть анализ с `tool.name = kb_lint` и `results_count = 0` (чистая база — алертов нет, но документ принят). Это и есть доказательство H1.
- [ ] Если API отвечает 403/404 (Code Scanning не включён) — зафиксировать в Devlog как блокер и **не** закрывать задачу «на глаз».
- [ ] `python scripts/kb_lint.py --path docs` → 0 битых ссылок, 0 `WARN`.

* **Замеры $\ge 3$ прогонов:** не применимы (конфигурация CI); если фиксируется длительность workflow, то 3 запуска и среднее в Devlog.

### Visual DoD (для задач с GUI/TUI):

Поверхность — Security-панель GitHub. Скриншот `docs/assets/screenshots/code-scanning/TASK-108.png` (≤ 2 MB) желателен; при работе без UI — ASCII-снимок вывода `gh api …/analyses` в Devlog.

## 5. Критерии готовности (DoD)

- [ ] Workflow создан и содержит триггеры push/PR/dispatch, права `contents: read` + `security-events: write`, `uses: ./`, `if: always()` + fork-guard, `category: kb-lint`.
- [ ] `code-scanning.yml` в `EXCLUDED_WORKFLOWS`; живой тест `bundle_assets()` подтверждает отсутствие `rules-check.yml` и `code-scanning.yml`, наличие `release.yml`.
- [ ] В `rules-check.yml` нет `security-events` (least privilege зафиксирован тестом).
- [ ] Запуск workflow зелёный, анализ `tool.name = kb_lint` виден в API Code Scanning (или зафиксирован блокер).
- [ ] Полный набор тестов зелёный; `kb_lint` — 0 битых; статусы обновлены (ТЗ/Канбан/Roadmap), запись в `Devlog.md` — на шаге `/kb-complete`.
