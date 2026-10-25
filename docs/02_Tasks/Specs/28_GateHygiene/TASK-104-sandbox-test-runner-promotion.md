---
id: TASK-104
title: "Промоушен sandbox-раннера тестов в scripts/ (DEBT-005)"
status: done
type: fast-track
phase: 28
component:
  - tests
  - tooling
parent_plan: "[[../../Roadmap|Roadmap.md (Фаза 28)]]"
created: 2026-10-25
updated: 2026-10-25
tags:
  - task/spec
  - fast-track
  - phase28
  - techdebt
  - tests
kanban: "[[../../Kanban|Канбан-доска]]"
---

# ⚡ Спецификация (Fast-Track): TASK-104 — Sandbox-раннер тестов в `scripts/`

> **Тип:** Fast-Track (≤ 30 LOC) | **Статус:** Выполнено (Режим 3)  
> **Фаза:** 28 | **Долг:** [[../../TechDebt|DEBT-005]] (закрывается этой задачей) | **Канбан:** [[../../Kanban|Канбан-доска]]  
> **Нормативная база:** [[../../../06_Memory/patterns|TRG-03]] → [[../../../06_Memory/Incidents/INC-003-dsh-sandbox-tempfile-mkdtemp-mode|INC-003]]

---

## 1. Цель и контекст

`TRG-03` (DSH Windows sandbox: `tempfile.mkdtemp()` создаёт каталог с DACL, запрещающей дочерние файлы) сработал уже **дважды**: в INC-003 и в TASK-101. Обёртка, патчащая `mkdtemp` на `os.mkdir(0o777)`, каждый раз пишется заново в `tmp/run_tests.py` — а `tmp/` в `.gitignore`, то есть в чистом клоне и в новой сессии её нет, и первый же прогон падает `PermissionError WinError 5`.

Паттерн при этом зафиксирован в памяти как `Count: 2` — по правилу промоушена он обязан перейти из Tier 3 (знание в заметке) в Tier 1 (закоммиченный исполняемый вход). Эта задача делает ровно это: переносит обёртку в `scripts/run_tests_sandbox.py` и закрывает `DEBT-005`.

## 2. Контракт файлов

* `[NEW]` `scripts/run_tests_sandbox.py`:
  - `main() -> int` — no-op патч `tempfile.mkdtemp` (permissive-режим), redirect `TMP`/`TEMP`/`TMPDIR` в `tmp/sandbox_temp/`, `unittest.discover("tests")`, возврат `0/1` по результату; без аргументов и без вывода сверх unittest.
* `[MODIFY]` `docs/02_Tasks/TechDebt.md`:
  - `DEBT-005` — строка переносится в `Resolved Debt` со ссылкой на эту спеку (на шаге `/kb-complete`).

> **Bookkeeping вне этих двух файлов:** `docs/06_Memory/patterns.md` (TRG-03 → `promoted`, ссылка на `INC-003`) и `docs/Devlog.md` обновляются автоматически на шаге `/kb-complete` по протоколу памяти; они не считаются реализационным скоупом.

## 3. Детали реализации

* Скрипт — копия проверенной обёртки (`tmp/run_tests.py`) без изменений логики: `for _ in range(100)` + `os.urandom(8).hex()`, `os.mkdir(name, 0o777)`, `tempfile.tempdir = str(TEMP_ROOT)`.
* На Linux/CI патч эквивалентен штатному поведению (`0o777` маскируется umask), поэтому отдельной ветки «не Windows» не нужно.
* `tmp/` остаётся gitignored и используется как рабочий каталог песочницы; скрипт создаёт его при необходимости (`mkdir(parents=True, exist_ok=True)`).
* Скрипт **не попадает в бандл**: `scripts/build_installer.py` включает только `["kb_lint.py", "kb_release.py", "kb_ingest.py"]` (whitelist), пересборка `install.py` не требуется.
* Документирование — docstring скрипта (`Usage: python scripts/run_tests_sandbox.py`); отдельная правка `Onboarding.md` не входит в скоуп (иначе выход за ≤ 2 файла).

## 4. План верификации (Verification Plan)

- [x] Синтаксис: `python -m py_compile scripts/run_tests_sandbox.py` → Exit 0.
- [x] Полный прогон через новый вход: `python scripts/run_tests_sandbox.py` → **180 тестов OK**, 0 failures/errors.
- [x] Повторяемость: удалить `tmp/run_tests.py` (локальная копия) и повторить прогон — результат тот же (проверка, что зависимость от untracked-файла устранена).
- [x] Целостность: `python scripts/kb_lint.py --path docs` → Exit 0, 0 битых ссылок.
- [x] Бандл не тронут: `git status --short` не содержит `install.py` / `dist/install.py`.
- [x] 4-State UI / скриншоты: не применимо (dev-tooling, без пользовательской поверхности).

## 5. Критерии готовности (DoD)

- [x] Изменения внесены строго в рамках скоупа (≤ 30 строк кода, ≤ 2 файлов); при выходе за лимит — стоп и переход на стандартную спеку.
- [x] `scripts/run_tests_sandbox.py` закоммичен и даёт зелёный прогон 180 тестов; прогон не зависит от `tmp/run_tests.py`.
- [x] `DEBT-005` переведён в `Resolved Debt`; `patterns.md` (TRG-03) помечен `promoted` с ссылкой на `INC-003`.
- [x] Все пункты Плана верификации пройдены без ошибок (Exit code 0).
- [x] Статус обновлён в ТЗ (`Выполнено`), Канбане (`Done`), Roadmap и Devlog.
