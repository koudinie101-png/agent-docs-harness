---
id: BUG-002
title: "Хардкод установки harness-а (install.py) в публичных релизных записках scripts/kb_release.py"
status: fixed
severity: medium
type: bug
target_release: "v0.16.0"
target_phase: 16
release_blocker: false
fixed_in: "v0.16.0"
resolved: 2026-10-12
regression_test: "tests/test_kb_release.py"
created: 2026-10-12
updated: 2026-10-12
tags:
  - bug
  - defect
  - release
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
feedback_source: "[[../Inbox/FB-GH-1|FB-GH-1]]"
---

# 🐞 Дефект: BUG-002 — Хардкод установки harness-а (`install.py`) в публичных релизных записках `scripts/kb_release.py`

> **ID:** BUG-002 | **Критичность:** Medium | **Статус:** fixed  
> **Релиз:** v0.12.0 | **Блокер:** Нет  
> **Канбан:** [[../Kanban|Канбан-доска]] | **Спецификация:** [[../../SPEC|SPEC.md]]  
> **Источник фидбека:** [[../Inbox/FB-GH-1|FB-GH-1 (GitHub Issue #1)]]  

---

## 1. Симптомы и окружение
* **Симптом:** В генераторе публичных релизных заметок (`scripts/kb_release.py`, строки 754–762) в секцию `Quick Install` жестко зашит вызов `install.py` самого фреймворка Docs-as-Code (`curl -fsSL {raw_install_url} | python3` и `python install.py --update`). В сторонних проектах (C#, Go, Rust, Web и т.д.), использующих harness как документационную обвязку, файла `install.py` нет, и команда завершается ошибкой `HTTP 404 Not Found`. Также конечные пользователи сторонних приложений видят призыв установить Docs-as-Code.
* **Окружение:** `scripts/kb_release.py`, CLI `/kb-release`.

## 2. Шаги воспроизведения (Repro Steps)
1. Выполнить генерацию релизных заметок в проекте, где отсутствует `install.py`, либо запустить команду формирования заметок:
   ```bash
   python scripts/kb_release.py --version v1.0.0 --dry-run
   ```
2. Открыть сгенерированный файл `dist/RELEASE_NOTES.md`.
3. **Фактическое поведение:** В секции `Быстрый старт / Обновление (Quick Install)` присутствует ссылка на `curl .../install.py` и команда `python install.py --update`.
4. **Ожидаемое поведение:** Генератор адаптивно определяет контекст (проверяет наличие `install.py` в корне проекта или принадлежность к `agent-docs-harness`), либо при наличии артефактов в `dist/` генерирует инструкции скачивания артефактов релиза.

## 3. Диагностика (Логи, Стек-трейс)
Фрагмент кода `scripts/kb_release.py`:
```python
# Строки 754-762:
### ⚡ Быстрый старт / Обновление (Quick Install)
```bash
# Новая установка Docs-as-Code
curl -fsSL {raw_install_url} | python3

# Обновление существующего проекта
python install.py --update
```
При попытке выполнения в стороннем репозитории: `curl: (22) The requested URL returned error: 404 Not Found`.

## 4. Первопричина (Root Cause Analysis — RCA)
В шаблоне публичных заметок в методе генерации отсутствует контекстная проверка типа проекта и наличия `install.py`. Переменная `first_art_name` на строке 742 объявлена, но не используется, а шаблон захардкожен на установку Docs-as-Code.

## 5. План исправления
* `[MODIFY]` `scripts/kb_release.py` — проверять наличие `install.py` на диске и генерировать блок `Quick Install` на основе реальных артефактов релиза или кастомных инструкций.
* `[NEW]` `tests/test_kb_release.py` — добавить тест, проверяющий, что для проекта без `install.py` не генерируется ссылка на 404 `install.py`.

## 6. Верификация (Regression-First)
- [x] Падающий регрессионный тест воспроизводит дефект (RED).
- [x] Исправление применено в коде (GREEN).
- [x] Регрессионный тест и весь сьют проходят успешно (REFACTOR).
- [x] Дефект закрыт через `/kb-implement BUG-002`.
