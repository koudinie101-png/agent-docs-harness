---
id: BUG-005
title: "AttributeError при вызове Path.is_relative_to в scripts/kb_lint.py на Python 3.8"
status: fixed
severity: high
type: bug
target_release: "v0.17.0"
target_phase: 17
release_blocker: true
fixed_in: "v0.17.0"
regression_test: "tests/test_kb_lint.py"
created: 2026-10-14
updated: 2026-10-15
tags:
  - bug
  - defect
  - lint
  - python38
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 🐞 Дефект: BUG-005 — AttributeError при вызове Path.is_relative_to в scripts/kb_lint.py на Python 3.8

> **ID:** BUG-005 | **Критичность:** High | **Статус:** fixed  
> **Релиз:** v0.17.0 | **Блокер:** Да  
> **Канбан:** [[../Kanban|Канбан-доска]] | **Спецификация:** [[../../SPEC|SPEC.md]]  

---

## 1. Симптомы и окружение
* **Симптом:** При запуске `scripts/kb_lint.py` в среде Python 3.8 скрипт аварийно завершается с исключением `AttributeError: 'WindowsPath'/'PosixPath' object has no attribute 'is_relative_to'`.
* **Окружение:** Python 3.8, `scripts/kb_lint.py` (`run_linter()`).

## 2. Шаги воспроизведения (Repro Steps)
1. Установить интерпретатор Python 3.8.
2. Выполнить проверку базы знаний:
   ```bash
   python3.8 scripts/kb_lint.py --path docs
   ```
3. **Фактическое поведение:** Необработанное исключение `AttributeError` при проверке относительных путей файлов заметок.
4. **Ожидаемое поведение:** Линтер успешно отрабатывает без падений на любой поддерживаемой версии Python (начиная с 3.8+, как декларировано в `README.md` и `install.py`).

## 3. Диагностика (Логи, Стек-трейс)
```text
Traceback (most recent call last):
  File "scripts/kb_lint.py", line 475, in <module>
    sys.exit(run_linter(Path(args.path)))
  File "scripts/kb_lint.py", line 350, in run_linter
    if f.is_relative_to(docs_dir):
AttributeError: 'WindowsPath' object has no attribute 'is_relative_to'
```

## 4. Первопричина (Root Cause Analysis — RCA)
Метод `Path.is_relative_to()` был добавлен в стандартную библиотеку только в Python 3.9 (`PEP 597` / Python 3.9 Standard Library additions). В кодовой базе `scripts/kb_lint.py` метод вызывается дважды (строки 350 и 370). При этом `install.py` (`sys.version_info < (3, 8)`) и документация проекта гарантируют поддержку Python 3.8+.

## 5. План исправления
* `[MODIFY]` `scripts/kb_lint.py` — заменить прямые вызовы `f.is_relative_to(docs_dir)` на совместимую с Python 3.8 вспомогательную функцию/блок:
  ```python
  def _is_relative_to(p: Path, base: Path) -> bool:
      try:
          p.resolve().relative_to(base.resolve())
          return True
      except ValueError:
          return False
  ```
* `[NEW]` `tests/test_kb_lint.py` — добавить регрессионный юнит-тест, эмулирующий окружение без `is_relative_to` либо тестирующий хелпер совместимости.

## 6. Верификация (Regression-First)
- [x] Падающий регрессионный тест воспроизводит дефект (RED).
- [x] Исправление применено в коде (GREEN).
- [x] Регрессионный тест и весь сьют проходят успешно (REFACTOR).
- [x] Дефект закрыт через `/kb-implement BUG-005`.
