---
id: BUG-007
title: "Падение с ошибкой unrecognized arguments при передаче инлайн-текста в scripts/kb_ingest.py --paste \"<text>\""
status: fixed
severity: medium
type: bug
target_release: "v0.17.0"
target_phase: 17
release_blocker: true
fixed_in: "v0.17.0"
regression_test: "tests/test_kb_ingest.py"
created: 2026-10-14
updated: 2026-10-15
tags:
  - bug
  - defect
  - ingest
  - cli
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 🐞 Дефект: BUG-007 — Падение с ошибкой unrecognized arguments при передаче инлайн-текста в scripts/kb_ingest.py --paste "<text>"

> **ID:** BUG-007 | **Критичность:** Medium | **Статус:** fixed  
> **Релиз:** v0.17.0 | **Блокер:** Да  
> **Канбан:** [[../Kanban|Канбан-доска]] | **Спецификация:** [[../../SPEC|SPEC.md]]  

---

## 1. Симптомы и окружение
* **Симптом:** При попытке импорта фидбека по команде, документированной в `CHANGELOG.md` (`scripts/kb_ingest.py --paste "<text>"`), утилита аварийно завершается с ошибкой парсера аргументов: `scripts/kb_ingest.py: error: unrecognized arguments: <text>`.
* **Окружение:** `scripts/kb_ingest.py` (`argparse`).

## 2. Шаги воспроизведения (Repro Steps)
1. Выполнить команду быстрого импорта:
   ```bash
   python scripts/kb_ingest.py --paste "Пользователь пожаловался на сбой авторизации"
   ```
2. **Фактическое поведение:**
   ```text
   usage: kb_ingest.py [-h] [--github] [--email] [--paste] ...
   kb_ingest.py: error: unrecognized arguments: Пользователь пожаловался на сбой авторизации
   ```
3. **Ожидаемое поведение:** Утилита распознает инлайн-текст после `--paste`, создает `FB-XXX.md` в `docs/02_Tasks/Inbox/` и сохраняет текст в теле заметки.

## 3. Диагностика (Логи, Стек-трейс)
В `scripts/kb_ingest.py`:
```python
parser.add_argument("--paste", action="store_true", help="Ingest quick snippet/paste from arguments or stdin")
```
Флаг с `action="store_true"` является булевым и не принимает значение аргумента из командной строки.

## 4. Первопричина (Root Cause Analysis — RCA)
В релизе v0.16.0 возникла несогласованность интерфейса CLI: `CHANGELOG.md` описал вызов `scripts/kb_ingest.py --paste "<text>"`, в то время как `README.md` указывал `--paste --text "<text>"`, а сам аргумент `--paste` остался сконфигурирован как булев флаг без аргументов.

## 5. План исправления
* `[MODIFY]` `scripts/kb_ingest.py` — переконфигурировать аргумент `--paste`:
  ```python
  parser.add_argument("--paste", nargs="?", const=True, default=None, help="...")
  ```
  Если передана строка, трактовать ее как текст обращения (если `--text` не задан явно). Поддержать оба варианта вызова: `--paste "текст"`, `--paste --text "текст"` и передачу через `stdin`.
* `[NEW]` `tests/test_kb_ingest.py` — добавить тест парсинга и обработки аргументов CLI для вызова `--paste "inline text"`.

## 6. Верификация (Regression-First)
- [x] Падающий регрессионный тест воспроизводит дефект (RED).
- [x] Исправление применено в коде (GREEN).
- [x] Регрессионный тест и весь сьют проходят успешно (REFACTOR).
- [x] Дефект закрыт через `/kb-implement BUG-007`.
