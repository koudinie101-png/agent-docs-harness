---
id: TASK-045
title: "GitHub Issue Forms и облачный workflow кросс-агентной синхронизации"
status: in-progress
type: task
phase: 12
component:
  - github-actions
  - issue-templates
  - workflows
parent_plan: "[[../../Plans/PLAN-012-feedback-ingestion-and-triage-buffer|PLAN-012]]"
created: 2026-10-11
updated: 2026-10-11
tags:
  - task/spec
  - phase12
  - github
  - actions
  - issue-forms
  - automation
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-045 — GitHub Issue Forms и облачный workflow кросс-агентной синхронизации

> **ID:** TASK-045  
> **Статус:** В работе (Режим 2)  
> **Теги:** #task/spec #phase12 #github #actions #issue-forms #automation  
> **Родительский план:** [[../../Plans/PLAN-012-feedback-ingestion-and-triage-buffer|PLAN-012]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-015-feedback-ingestion-channels-and-triage-heuristics|RESEARCH-015]], [[../../../03_Decisions_ADR/ADR-0020-feedback-ingestion-channels-and-triage-automation|ADR-0020]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Построить облачный автоматизированный контур сбора и структурирования внешних обращений:
1. **Декларативные веб-формы обратной связи на GitHub:** Создать `.github/ISSUE_TEMPLATE/bug_report.yml`, `feature_request.yml` и `config.yml`, автоматически навешивающие метку `needs-triage` и структурирующие шаги воспроизведения, ожидаемое поведение и диагностический контекст.
2. **Кросс-агентный Cloud Cron Workflow:** Разработать `.github/workflows/feedback-sync.yml`, который по расписанию (cron раз в 4-6 часов) и ручному триггеру (`workflow_dispatch`) запускает `scripts/kb_ingest.py`, импортирует новые тикеты/письма в `docs/02_Tasks/Inbox/`, обновляет `.inbox_state.json` и создает коммит/PR без необходимости локального участия разработчика.
3. **Синхронизация шаблонов в инсталляторе:** Добавить новые шаблоны issue forms и workflow в ресурсы инсталлятора.

---

## 2. Затрагиваемые файлы и компоненты

* `[NEW]` `.github/ISSUE_TEMPLATE/bug_report.yml` — форма баг-репорта с авто-лейблом `needs-triage`.
* `[NEW]` `.github/ISSUE_TEMPLATE/feature_request.yml` — форма запроса улучшений с авто-лейблом `needs-triage`.
* `[NEW]` `.github/ISSUE_TEMPLATE/config.yml` — конфигурация issue chooser (запрет пустых тикетов, ссылки на документацию).
* `[NEW]` `.github/workflows/feedback-sync.yml` — облачный шедулер синхронизации обращений.

---

## 3. Детали реализации

### 3.1. Формы обратной связи (`.github/ISSUE_TEMPLATE/`)
- `bug_report.yml`:
  - Поля: Описание проблемы, Шаги воспроизведения, Ожидаемое поведение, Фактическое поведение, Окружение (ОС, версия Python, модель агента).
  - Навешиваемые метки: `labels: ["needs-triage", "kind:defect"]`.
- `config.yml`:
  - `blank_issues_enabled: false`
  - Контактные ссылки на документацию проекта и FAQ.

### 3.2. Облачный рабочий процесс (`.github/workflows/feedback-sync.yml`)
```yaml
name: Feedback Ingestion Sync

on:
  schedule:
    - cron: '0 */6 * * *'
  workflow_dispatch:

permissions:
  contents: write
  issues: read

jobs:
  sync-feedback:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Run Ingest Script
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          FEEDBACK_IMAP_USER: ${{ secrets.FEEDBACK_IMAP_USER }}
          FEEDBACK_IMAP_PASS: ${{ secrets.FEEDBACK_IMAP_PASS }}
        run: |
          python scripts/kb_ingest.py --all
      - name: Commit & Push Changes
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add docs/02_Tasks/Inbox/
          if git diff --staged --quiet; then
            echo "No new feedback to commit"
          else
            git commit -m "chore(inbox): ingest new feedback items [skip ci]"
            git push
          fi
```

---

## 4. План верификации (Verification Plan)

- [ ] Синтаксическая валидация YAML файлов:
  ```bash
  python -c "import yaml; yaml.safe_load(open('.github/ISSUE_TEMPLATE/bug_report.yml', encoding='utf-8')); yaml.safe_load(open('.github/workflows/feedback-sync.yml', encoding='utf-8'))"
  ```
- [ ] Проверка схемы GitHub Actions через `actionlint` (если доступен) или сухой запуск синтаксиса YAML.

---

## 5. Критерии готовности (DoD)

- [ ] Формы `.github/ISSUE_TEMPLATE/bug_report.yml`, `feature_request.yml` и `config.yml` созданы с корректной YAML схемой.
- [ ] Workflow `.github/workflows/feedback-sync.yml` готов к выполнению по расписанию и On-Demand.
- [ ] Права `contents: write` и безопасная работа с секретами учтены.
