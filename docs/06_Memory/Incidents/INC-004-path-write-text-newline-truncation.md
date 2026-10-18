---
id: INC-004
title: "Path.write_text с невалидным newline усекает целевой файл до выброса ValueError"
status: active
type: incident
severity: high
tag: tooling
root_cause: "io.open truncates before TextIOWrapper validates newline"
target_pattern: "TRG-04"
created: 2026-10-18
updated: 2026-10-18
tags:
  - memory
  - incident
---

# ⚠️ Инцидент: INC-004 — Path.write_text с невалидным newline усекает целевой файл до выброса ValueError

> **Тег:** #memory #incident | **Тяжесть:** high | **Статус:** active  
> **Паттерн в базе:** `TRG-04` | **Задача:** `TASK-085`

---

## 1. Контекст и симптом
При скриптовом рефакторинге `install.py` (TASK-085) временный патч-скрипт завершал работу вызовом `Path.write_text(src, newline="\\n")`. Скрипт упал с `ValueError: illegal newline value: \n`, но к этому моменту `install.py` уже был **обрезан до 0 байт**: последующие проверки (`grep` по маркерам, `py_compile`) показали пустой файл, а восстановление потребовалось из Git.

## 2. Корневая причина (Root Cause)
`pathlib.Path.write_text()` открывает файл в режиме `"w"` (что усекает его) и только затем создаёт `TextIOWrapper`, который валидирует аргумент `newline` и поднимает `ValueError`. Валидация происходит **после** деструктивного открытия, поэтому исключение не защищает целевой файл.

## 3. Защитное действие (Corrective Action)
1. Для скриптовых перезаписей использовать `Path.write_bytes(text.encode("utf-8"))` — без текстового слоя и без риска усечения при невалидном аргументе.
2. Если нужен именно `write_text`, передавать `newline="\n"` (одна пара слэшей в исходнике) и **никогда** не собирать аргумент динамически.
3. После любой скриптовой перезаписи файла проверять `Get-Item <file>.Length`/`git status` до запуска компиляции: пустой или подозрительно малый размер — сигнал восстановить файл из Git.
4. Паттерн промотирован в `patterns.md` как `TRG-04`.
