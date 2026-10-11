---
id: BUG-XXX
title: "[Краткое описание дефекта]"
status: open # open | in-progress | fixed | rejected
severity: medium # low | medium | high | critical
type: bug
target_release: "" # "vX.Y.Z" | "hotfix" | "backlog"
target_phase: null # Номер целевой фазы (например, 11) или null
release_blocker: false # true | false (блокирует ли релиз target_release)
fixed_in: null # Заполняется при закрытии дефекта: "vX.Y.Z"
regression_test: "tests/path/to/test_regression.ext"
created: 2026-09-19
updated: 2026-09-19
tags:
  - bug
  - defect
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 🐞 Дефект: BUG-XXX — [Краткое название]

> **ID:** BUG-XXX | **Критичность:** [Low | Medium | High | Critical] | **Статус:** [open | in-progress | fixed | rejected]  
> **Релиз:** [target_release] | **Блокер:** [Да | Нет]  
> **Канбан:** [[../Kanban|Канбан-доска]] | **Спецификация:** [[../../SPEC|SPEC.md]]  

---

## 1. Симптомы и окружение
* **Симптом:** <!-- Что сломалось и как воспроизводится -->
* **Окружение:** <!-- ОС, версия, стек -->

## 2. Шаги воспроизведения (Repro Steps)
1. <!-- Предусловие -->
2. <!-- Действие / команда -->
3. <!-- Ошибка vs Ожидаемое поведение -->

## 3. Диагностика (Логи, Стек-трейс)
```text
<!-- Текст ошибки или лог -->
```

## 4. Первопричина (Root Cause Analysis — RCA)
<!-- Архитектурная или логическая причина дефекта -->

## 5. План исправления
* `[MODIFY]` `path/to/file.ext` — <!-- исправление -->
* `[NEW]` `tests/path/to/test_regression.ext` — <!-- регрессионный тест -->

## 6. Верификация (Regression-First)
- [ ] Падающий регрессионный тест воспроизводит дефект (RED).
- [ ] Исправление применено в коде (GREEN).
- [ ] Регрессионный тест и весь сьют проходят успешно (REFACTOR).
- [ ] Дефект закрыт через `/kb-implement BUG-XXX` или `kb-complete`.
