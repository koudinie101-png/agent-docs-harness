---
id: TASK-047
title: "Диагностический модуль install.py --report, синхронизация сборщика и E2E тесты"
status: done
type: task
phase: 12
component:
  - installer
  - bundling
  - diagnostics
  - e2e
parent_plan: "[[../../Plans/PLAN-012-feedback-ingestion-and-triage-buffer|PLAN-012]]"
created: 2026-10-11
updated: 2026-10-11
tags:
  - task/spec
  - phase12
  - installer
  - bundling
  - diagnostics
  - e2e
  - documentation
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-047 — Диагностический модуль install.py --report, синхронизация сборщика и E2E тесты

> **ID:** TASK-047  
> **Статус:** Выполнено (Режим 3)  
> **Теги:** #task/spec #phase12 #installer #bundling #diagnostics #e2e #documentation  
> **Родительский план:** [[../../Plans/PLAN-012-feedback-ingestion-and-triage-buffer|PLAN-012]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-015-feedback-ingestion-channels-and-triage-heuristics|RESEARCH-015]], [[../../../03_Decisions_ADR/ADR-0020-feedback-ingestion-channels-and-triage-automation|ADR-0020]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Завершить реализацию контура Фазы 12, интегрировав локальную диагностику и упаковав весь новый функционал в монолит инсталлятора:
1. **Диагностический CLI-модуль `install.py --report`:** Реализовать безопасный оффлайн-сборщик окружения (ОС, версия Python, статус git, наличие активных IDE-конфигов, проверка целостности `kb_lint.py`), генерирующий анонимизированный отчет в формате Markdown или JSON для приложения к обращению.
2. **Синхронизация сборщика `scripts/build_installer.py`:** Упаковать новый шаблон `TEMPLATE_FEEDBACK.md`, каталог `docs/02_Tasks/Inbox/`, скрипт `scripts/kb_ingest.py`, скилл `kb-triage` и формы issues в монолит `install.py`.
3. **Обновление механизма `install.py --update`:** Обеспечить безопасную доставку структуры `Inbox/` и новых утилит при накатывании обновлений на существующие проекты.
4. **Сквозное E2E тестирование:** Добавить тесты в `tests/test_installer.py` для верификации флага `--report`, деплоя буфера `Inbox/` и работы `kb_ingest.py`.
5. **Актуализация витрины и онбординга:** Обновить `SPEC.md`, `README.md` и `docs/Onboarding.md` с описанием контура обратной связи, флага `--report` и команды `/kb-triage`.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `install.py` — поддержка флага `--report`, распаковка `Inbox/` и шаблона обратной связи при установке/обновлении.
* `[MODIFY]` `scripts/build_installer.py` — упаковка новых скиллов, шаблонов и скриптов в монолит.
* `[MODIFY]` `tests/test_installer.py` — сквозные E2E тесты нового функционала инсталлятора.
* `[MODIFY]` `SPEC.md` — синхронизация Мастер-спецификации по правилу Living Spec Invariant.
* `[MODIFY]` `README.md` — актуализация витрины проекта (добавление описания сбора фидбека и флага `--report`).
* `[MODIFY]` `docs/Onboarding.md` — включение сценария триажа обращений в руководство онбординга.

---

## 3. Детали реализации

### 3.1. Локальный диагностический модуль `install.py --report`
```python
def generate_diagnostic_report(project_dir: Path) -> str:
    """Генерация анонимизированного диагностического бандла"""
    # 1. Платформа: sys.platform, platform.platform(), sys.version
    # 2. Git: ветка, хеш коммита, статус рабочей директории (git status -s)
    # 3. База знаний: результат быстрого вызова kb_lint
    # 4. Обнаруженные конфигурации агентов (.cursorrules, GEMINI.md и т.д.)
    # 5. Возврат Markdown строки без персональных путей (замена username на <user>)
```

### 3.2. Синхронизация `build_installer.py`
- Добавление `TEMPLATE_FEEDBACK.md` в секцию упаковываемых шаблонов.
- Добавление `scripts/kb_ingest.py` в перечень поставляемых утилит.
- Добавление скилла `kb-triage` в набор упаковываемых скиллов `.agents/skills/`.

---

## 4. План верификации (Verification Plan)

- [x] Генерация монолита инсталлятора:
  ```bash
  python scripts/build_installer.py
  ```
- [x] Верификация флага `--report`:
  ```bash
  python install.py --report
  ```
- [x] Запуск сквозного E2E тестирования:
  ```bash
  python -m unittest tests/test_installer.py
  ```
- [x] Финальный аудит ссылок базы знаний:
  ```bash
  python scripts/kb_lint.py --path docs
  ```

---

## 5. Критерии готовности (DoD)

- [x] `install.py --report` безопасно генерирует диагностический отчет окружения.
- [x] Инсталлятор `install.py` успешно пересобран через `build_installer.py` и все ресурсы актуализированы.
- [x] Все модульные и E2E тесты завершаются со 100% успехом.
- [x] Документация (`SPEC.md`, `README.md`, `docs/Onboarding.md`) полностью синхронизирована.
