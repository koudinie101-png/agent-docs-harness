---
id: TASK-064
title: "Контроль лимита памяти в scripts/kb_lint.py, бандлинг install.py, E2E тесты и Living Spec sync"
status: planned
type: task
phase: 16
component:
  - lint
  - installer
  - bundler
  - tests
  - spec
parent_plan: "[[../../Plans/PLAN-016-self-improving-harness-and-defect-memory|PLAN-016]]"
created: 2026-10-12
updated: 2026-10-12
tags:
  - task/spec
  - phase16
  - lint
  - installer
  - e2e
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-064 — Контроль лимита памяти в scripts/kb_lint.py, бандлинг install.py, E2E тесты и Living Spec sync

> **ID:** TASK-064 | **Статус:** К реализации (Режим 2)  
> **План:** [[../../Plans/PLAN-016-self-improving-harness-and-defect-memory|PLAN-016]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Обоснование:** [[../../../04_Research/RESEARCH-020-self-improving-defect-loop-and-quality-gates|RESEARCH-020]], [[../../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]  
> **Первоисточник фидбека:** [[../../Inbox/FB-GH-3|Обращение FB-GH-3 (madpanther)]]

---

## 1. Цель задачи

Завершить интеграцию Фазы 16 механическим Tier 1 контролем и сквозной сборкой дистрибутива:
* Реализовать функцию `check_memory_limits` в утилите `scripts/kb_lint.py`: автоматический аудит лимита активных записей в `docs/06_Memory/patterns.md` ($\le 15$, Exit code 1 при превышении) и валидация frontmatter инцидентов `INC-*.md`.
* Добавить упаковку компонентов процедурной памяти в сборщик `scripts/build_installer.py`.
* Обеспечить бережное обновление (`install.py --update`): развертывание подсистемы памяти при ее отсутствии без перезаписи пользовательских инцидентов и паттернов.
* Написать модульные тесты в `tests/test_kb_lint.py` и сквозные E2E тесты в `tests/test_installer.py`.
* Актуализировать Living Spec (`SPEC.md`), витрину проекта `README.md` и скомпилировать `install.py` / `dist/install.py`.

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `scripts/kb_lint.py` — функция `check_memory_limits` и вызов в главном цикле проверки.
* `[MODIFY]` `tests/test_kb_lint.py` — юнит-тесты контроля лимита паттернов и валидации инцидентов.
* `[MODIFY]` `scripts/build_installer.py` — упаковка шаблона инцидента и стартового файла памяти.
* `[MODIFY]` `install.py` — логика деплоя каталога `docs/06_Memory/` и сохранение памяти в `--update`.
* `[MODIFY]` `tests/test_installer.py` — E2E тесты развертывания подсистемы памяти.
* `[MODIFY]` `SPEC.md`, `README.md` — актуализация документации Living Spec.
* `[MODIFY]` `docs/02_Tasks/Kanban.md` — обновление карточки `TASK-064` до постоянной викиссылки на ТЗ.
* `[MODIFY]` `docs/02_Tasks/Roadmap.md` — обновление ссылки `TASK-064` на ТЗ.

---

## 3. Детали реализации

### 3.1. Функция `check_memory_limits` в `scripts/kb_lint.py`
В утилиту добавляется механическая проверка:
```python
def check_memory_limits(docs_dir: Path) -> List[str]:
    """Tier 1 Quality Gate: проверяет лимит активных паттернов (<= 15) в docs/06_Memory/patterns.md."""
    errors = []
    memory_dir = docs_dir / "06_Memory"
    if not memory_dir.exists():
        return errors

    patterns_file = memory_dir / "patterns.md"
    if patterns_file.exists():
        content = patterns_file.read_text(encoding="utf-8")
        # Парсим строки вида: - [TRG-01] ...
        pattern_matches = re.findall(r"^\s*-\s*\[TRG-\d+\].*", content, flags=re.MULTILINE)
        if len(pattern_matches) > 15:
            errors.append(
                f"Memory patterns limit exceeded: {len(pattern_matches)} active patterns found in "
                f"'{patterns_file.relative_to(docs_dir)}' (maximum allowed: 15). "
                f"Archive or consolidate patterns to preserve token economy!"
            )
    return errors
```

### 3.2. Логика инсталлятора `install.py`
* При чистой установке: создаются `docs/06_Memory/` и `docs/06_Memory/Incidents/.gitkeep`, деплоится чистый стартовый `docs/06_Memory/patterns.md` и `TEMPLATE_INCIDENT.md`.
* При обновлении (`--update`):
  * `TEMPLATE_INCIDENT.md` бережно обновляется в `docs/00_Templates/`.
  * Если `docs/06_Memory/` отсутствует в существующем проекте — каталог создается и инициализируется.
  * Если `patterns.md` уже существует — файл **не перезаписывается**, сохраняя накопленную память пользователя.

---

## 4. План верификации (Verification Plan)

- [ ] Модульные тесты линтера: `python -m unittest tests/test_kb_lint.py` — проверка срабатывания ошибки при 16 паттернах и прохождения при $\le 15$.
- [ ] Сборка дистрибутива: `python scripts/build_installer.py` собирает `install.py` и `dist/install.py` без ошибок (Exit code 0).
- [ ] Сквозные тесты инсталлятора: `python -m unittest tests/test_installer.py` подтверждает создание `docs/06_Memory/` и сохранение данных при `--update`.
- [ ] Полный аудит базы знаний: `python scripts/kb_lint.py --path docs` завершается с успехом.

---

## 5. Критерии готовности (DoD)

- [ ] Механический контроль лимита памяти интегрирован в `scripts/kb_lint.py`.
- [ ] Инсталлятор `install.py` разворачивает подсистему памяти и защищает ее при обновлении.
- [ ] Все модульные и E2E тесты завершаются со 100% успехом.
- [ ] Документация синхронизирована.
