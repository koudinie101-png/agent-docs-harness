---
id: TASK-019
title: "Внедрение правил High-SNR, Anti-Echo протокола и Silent-CLI в AGENTS.md, kb_lint.py и kb_release.py"
status: done
type: task
phase: 5
component:
  - rules
  - cli
  - tooling
  - anti-echo
parent_plan: "[[../../Plans/PLAN-005-high-snr-token-optimization|PLAN-005]]"
created: 2026-10-01
updated: 2026-10-01
tags:
  - task/spec
  - phase5
  - component/rules
  - component/cli
  - component/tooling
  - component/anti-echo
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-019 — Внедрение правил High-SNR, Anti-Echo и Silent-CLI

> **ID:** TASK-019  
> **Статус:** Выполнено (2026-10-01)  
> **Теги:** #task/spec #phase5 #component/rules #component/cli #component/tooling #component/anti-echo  
> **Родительский план:** [[../../Plans/PLAN-005-high-snr-token-optimization|PLAN-005]]  
> **Связанные ADR и исследования:** [[../../../04_Research/RESEARCH-004-token-efficiency-and-context-compression|RESEARCH-004]], [[../../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]], [[../../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Реализовать Правило 3 (Anti-Echo Response Protocol), Правило 4 (DRY Rules Hierarchy) и Правило 6 (Silent-on-Success CLI) из [[../../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]]:
1. **Протокол Anti-Echo в корневых правилах (`AGENTS.md`):**
   * Внедрить жесткое системное ограничение: запрет на перепечатку содержимого записанных на диск файлов в теле сообщения агента.
   * Установить обязательный компактный стандарт ответа: кликабельная ссылка `[FILE](file://...)` + резюме из 3–5 пунктов + явный вопрос о переходе к следующему шагу.
   * Синхронизировать правило с правилами адаптеров (`GEMINI.md`, `.cursorrules`, `.windsurfrules`).
2. **Очистка `AGENTS.md` от словесной воды:**
   * Сформулировать 3 режима и роль Senior Partner через лаконичные императивные предикаты.
   * Закрепить `AGENTS.md` как единый источник правды (SSOT) для инвариантов поведения.
3. **Схема цветов и тегирование Obsidian Graph в `AGENTS.md`:**
   * Зафиксировать явную таблицу цветовой схемы Obsidian Graph (7 категорий) и тегов `#task`, `#adr`, `#research`, `#bug`, `#testing`.
   * Синхронизировать с правилами в `install.py` (`generate_agents_md`).
4. **Режим Silent-on-Success в CLI-инструментах:**
   * В `scripts/kb_lint.py`:
     - При успехе выводить ровно одну строку: `OK: <N> files scanned, <M> links verified (0 broken).` (сокращение вывода на 80%).
     - Добавить флаг `--verbose` для отображения полного лога сканирования.
     - При ошибках сохранять подробный отчет с точным указанием файлов и сломанных ссылок.
   * В `scripts/kb_release.py`:
     - Поддержать лаконичный однострочный вывод в стандартном режиме и подробный при `--verbose`.
5. **Автоматизированное тестирование CLI:**
   * Создать `tests/test_kb_lint.py` для покрытия лаконичного и подробного режимов, проверки флагов и обнаружения битых ссылок.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `AGENTS.md` — добавление раздела Anti-Echo Protocol, таблицы цветов и тегов Obsidian Graph.
* `[MODIFY]` `install.py` — обновление генератора `generate_agents_md` и правил.
* `[MODIFY]` `scripts/kb_lint.py` — реализация лаконичного режима Silent-on-Success и флага `--verbose`.
* `[MODIFY]` `scripts/kb_release.py` — лаконичный вывод успешной проверки/сборки.
* `[NEW]` `tests/test_kb_lint.py` — unit-тесты режимов работы `kb_lint.py`.

---

## 3. Детали технической реализации

### 3.1. Секция Anti-Echo Protocol в `AGENTS.md`

```markdown
### 🔇 Anti-Echo Response Protocol
When creating or modifying files on disk:
1. **STRICTLY PROHIBITED:** Dumping the complete file contents into the chat message.
2. **REQUIRED FORMAT:**
   - Clickable file permalink: `[FileName](file:///path/to/file)`.
   - Concise 3–5 bullet summary of key changes/decisions.
   - Next actionable step or prompt for user confirmation.
```

### 3.2. Архитектура вывода `scripts/kb_lint.py`

```python
# По умолчанию (Silent-on-Success):
if broken_count == 0 and not frontmatter_errors:
    print(f"OK: {scanned_files} files scanned, {total_links} wikilinks verified (0 broken).")
    return 0
else:
    # Детальный отчет об ошибках
    print(f"ERROR: {broken_count} broken links, {len(frontmatter_errors)} frontmatter errors.")
    ...
    return 1

# При наличии флага --verbose:
# Выводить полный лог аудита, как было раньше.
```

---

## 4. План верификации (Verification Plan)

### Автоматические тесты:
- [x] Запуск `python -m unittest tests/test_kb_lint.py` (все тесты зеленые).
- [x] Запуск `python scripts/kb_lint.py --path docs`:
  * Вывод состоит ровно из 1 строки с префиксом `OK:`.
  * Код завершения 0.
- [x] Запуск `python scripts/kb_lint.py --path docs --verbose`:
  * Вывод содержит полный аудит.

### Инспекция правил:
- [x] Проверить наличие секции Anti-Echo Protocol в `AGENTS.md` и `install.py`.
- [x] Проверить наличие таблицы цветов и тегов Obsidian Graph в `AGENTS.md` и `install.py`.

---

## 5. Критерии готовности (Definition of Done)

- [x] Правило Anti-Echo зафиксировано в `AGENTS.md` и генераторе правил в `install.py`.
- [x] Таблица цветов и тегов Obsidian Graph зафиксирована в `AGENTS.md` и `install.py`.
- [x] Скрипты `kb_lint.py` и `kb_release.py` работают в режиме Silent-on-Success.
- [x] Добавлены тесты `tests/test_kb_lint.py`, подтверждающие корректность кодов возврата и форматирования вывода.
- [x] Все существующие тесты проекта продолжают проходить (Exit code 0).
