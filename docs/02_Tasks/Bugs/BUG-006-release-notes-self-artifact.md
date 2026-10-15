---
id: BUG-006
title: "dist/RELEASE_NOTES.md попадает в таблицу артефактов SHA-256 при повторном запуске scripts/kb_release.py"
status: fixed
severity: medium
type: bug
target_release: "v0.17.0"
target_phase: 17
release_blocker: true
fixed_in: "v0.17.0"
regression_test: "tests/test_kb_release.py"
created: 2026-10-14
updated: 2026-10-15
tags:
  - bug
  - defect
  - release
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 🐞 Дефект: BUG-006 — dist/RELEASE_NOTES.md попадает в таблицу артефактов SHA-256 при повторном запуске scripts/kb_release.py

> **ID:** BUG-006 | **Критичность:** Medium | **Статус:** fixed  
> **Релиз:** v0.17.0 | **Блокер:** Да  
> **Канбан:** [[../Kanban|Канбан-доска]] | **Спецификация:** [[../../SPEC|SPEC.md]]  

---

## 1. Симптомы и окружение
* **Симптом:** При повторном выполнении `scripts/kb_release.py` (или при наличии предварительно сгенерированного файла `dist/RELEASE_NOTES.md`), файл релизных заметок воспринимается как бинарный дистрибутив и попадает в таблицу контрольных сумм SHA-256 внутри самого себя и внутри `docs/02_Tasks/Releases/RELEASE-vX.Y.Z.md`.
* **Окружение:** `scripts/kb_release.py` (`inspect_release_artifacts()`).

## 2. Шаги воспроизведения (Repro Steps)
1. Выполнить генерацию релиза:
   ```bash
   python scripts/kb_release.py --version v0.16.0 --dry-run
   ```
2. Повторить команду:
   ```bash
   python scripts/kb_release.py --version v0.16.0 --dry-run
   ```
3. Проверить таблицу артефактов в `dist/RELEASE_NOTES.md`:
   ```markdown
   | Файл / Артефакт | Размер | SHA-256 Контрольная сумма |
   | :--- | :--- | :--- |
   | `RELEASE_NOTES.md` | X.X KB | `...` |
   ```
4. **Фактическое поведение:** Заметки релиза каталогизируют сами себя как скачиваемый артефакт релиза.
5. **Ожидаемое поведение:** `RELEASE_NOTES.md` служит описанием релиза и никогда не включается в перечень распространяемых файлов и таблицу хешей.

## 3. Диагностика (Логи, Стек-трейс)
Функция `inspect_release_artifacts(dist_dir)` проверяет только `not item.is_file() or item.name.startswith(".")`, сканируя все остальные файлы без фильтрации служебного файла заметок.

## 4. Первопричина (Root Cause Analysis — RCA)
В `scripts/kb_release.py` процедура `inspect_release_artifacts()` не содержит исключения для имени `RELEASE_NOTES.md` (или кастомного `--notes-output`). При первом прогоне в чистом `dist/` файл заметок пишется после вызова инспектора артефактов, но при любом перезапуске или существовании `dist/` он попадает в список артефактов.

## 5. План исправления
* `[MODIFY]` `scripts/kb_release.py` — в функции `inspect_release_artifacts()` добавить явную проверку:
  ```python
  if item.name == "RELEASE_NOTES.md" or (notes_filename and item.name == notes_filename):
      continue
  ```
* `[NEW]` `tests/test_kb_release.py` — добавить тест, вызывающий `inspect_release_artifacts()` на каталоге `dist/`, содержащем `RELEASE_NOTES.md` и бинарный архив, с проверкой отсутствия `RELEASE_NOTES.md` в результате.

## 6. Верификация (Regression-First)
- [x] Падающий регрессионный тест воспроизводит дефект (RED).
- [x] Исправление применено в коде (GREEN).
- [x] Регрессионный тест и весь сьют проходят успешно (REFACTOR).
- [x] Дефект закрыт через `/kb-implement BUG-006`.
