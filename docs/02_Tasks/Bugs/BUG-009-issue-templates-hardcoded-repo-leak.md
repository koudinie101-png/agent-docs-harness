---
id: BUG-009
title: "Утечка метаданных agent-docs-harness в .github/ISSUE_TEMPLATE/"
status: fixed
severity: medium
type: bug
target_release: "v0.17.0"
target_phase: 17
release_blocker: false
fixed_in: "v0.17.0"
regression_test: "tests/test_installer.py"
created: 2026-10-15
updated: 2026-10-15
tags:
  - bug
  - defect
  - installer
  - templates
  - github
  - phase17
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 🐞 Дефект: BUG-009 — Утечка метаданных agent-docs-harness в .github/ISSUE_TEMPLATE/

> **ID:** BUG-009 | **Критичность:** Medium | **Статус:** fixed  
> **Релиз:** v0.17.0 | **Блокер:** Нет  
> **Канбан:** [[../Kanban|Канбан-доска]] | **Спецификация:** [[../../SPEC|SPEC.md]]  

---

## 1. Симптомы и окружение
* **Симптом:** При развертывании харнесса в сторонний проект (`install.py`) копируются файлы `.github/ISSUE_TEMPLATE/` (`bug_report.yml`, `feature_request.yml`, `config.yml`), содержащие жестко зашитые ссылки и упоминания репозитория `koudinie101-png/agent-docs-harness`.
* **Окружение:** Кроссплатформенно (любая ОС, любой стек).

## 2. Шаги воспроизведения (Repro Steps)
1. Установить харнесс в чистый проект: `python install.py --project "ClientApp" -y`.
2. Открыть созданный файл `.github/ISSUE_TEMPLATE/config.yml`.
3. Обнаружить ссылки на `https://github.com/koudinie101-png/agent-docs-harness/...`.
4. Открыть `.github/ISSUE_TEMPLATE/bug_report.yml` и увидеть описание: *"Сообщить об ошибке или сбое в работе agent-docs-harness"*.

## 3. Диагностика (Логи, Стек-трейс)
```yaml
# .github/ISSUE_TEMPLATE/config.yml в пользовательском проекте:
contact_links:
  - name: 📖 Документация и Онбординг
    url: https://github.com/koudinie101-png/agent-docs-harness/blob/main/docs/Onboarding.md
  - name: 💬 Вопросы и обсуждения архитектуры
    url: https://github.com/koudinie101-png/agent-docs-harness/discussions
```

## 4. Первопричина (Root Cause Analysis — RCA)
В `install.py` (строки 164–167 и 915–918) упаковка и деплой файлов каталога `.github/ISSUE_TEMPLATE/` выполняются механически («как есть») без параметризации под целевой проект:
1. `config.yml` предназначен исключительно для репозитория самого харнесса и не должен развертываться в клиентские проекты без предварительной адаптации или должен пропускаться вовсе.
2. `bug_report.yml` и `feature_request.yml` не параметризуются переменной `project_name` или универсальными нейтральными формулировками при распаковке.

## 5. План исправления
* `[MODIFY]` `install.py` — в процессе распаковки ассетов `.github/ISSUE_TEMPLATE/`:
  - Исключить деплой `config.yml` в сторонние проекты (или генерировать относительные/локальные ссылки на документацию проекта).
  - Заменять имя `agent-docs-harness` на `{project_name}` в заголовках и описаниях форм.
* `[MODIFY]` `.github/ISSUE_TEMPLATE/bug_report.yml` и `feature_request.yml` — выверить нейтральные формулировки по умолчанию.
* `[MODIFY]` `tests/test_installer.py` — добавить регрессионный тест, проверяющий отсутствие ссылок на `koudinie101-png/agent-docs-harness` в развернутых issue-формах целевого проекта.

## 6. Верификация (Regression-First)
- [x] Падающий регрессионный тест воспроизводит дефект (RED).
- [x] Исправление применено в коде `install.py` (GREEN).
- [x] Регрессионный тест и весь сьют проходят успешно (REFACTOR).
- [x] Дефект закрыт через `/kb-implement BUG-009`.
