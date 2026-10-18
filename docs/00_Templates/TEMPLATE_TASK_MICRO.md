---
id: TASK-XXX
title: "[Краткое действие: 3-7 слов]"
status: planned # planned | in-progress | done | cancelled
type: fast-track
phase: 1 # Номер текущей фазы
component:
  - core
parent_plan: "[[../../Plans/PLAN-XXX|PLAN-XXX]]" # Опционально или ссылка на фазовый план
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - task/spec
  - fast-track
kanban: "[[../../Kanban|Канбан-доска]]"
---

# ⚡ Спецификация (Fast-Track): TASK-XXX — [Краткое название]

> **Тип:** Fast-Track (≤ 30 LOC) | **Статус:** [К реализации | В работе | Выполнено]  
> **Канбан:** [[../../Kanban|Канбан-доска]]

---

## 1. Цель и контекст
<!-- 1-2 предложения: что конкретно меняется и зачем -->

## 2. Контракт файлов
* `[MODIFY]` `path/to/file` — <!-- символ(ы) и суть изменения; без номеров строк (ADR-0029) -->

## 3. План верификации (Verification Plan)
- [ ] Верификация: `python -m unittest discover -s tests`
- [ ] Линтер: `python scripts/kb_lint.py --path docs`

## 4. Критерии готовности (DoD)
- [ ] Изменения внесены строго в рамках скоупа (≤ 30 строк кода, ≤ 2 файлов).
- [ ] Все пункты Плана верификации пройдены без ошибок (Exit code 0).
- [ ] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Devlog.
