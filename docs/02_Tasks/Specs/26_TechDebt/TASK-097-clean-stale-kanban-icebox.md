---
id: TASK-097
title: "Очистка устаревшего Icebox в Kanban.md"
status: planned
type: fast-track
phase: 26
component:
  - docs
parent_plan: "[[../../TechDebt|TechDebt.md]]"
created: 2026-10-18
updated: 2026-10-18
tags:
  - task/spec
  - fast-track
  - phase26
  - techdebt
kanban: "[[../../Kanban|Канбан-доска]]"
---

# ⚡ Спецификация (Fast-Track): TASK-097 — Очистка устаревшего Icebox в Kanban.md

> **Тип:** Fast-Track (≤ 30 LOC) | **Статус:** К реализации  
> **Фаза:** 26 (Tech Debt Hardening) | **Канбан:** [[../../Kanban|Канбан-доска]]  
> **Долг:** [[../../TechDebt|DEBT-003]] — закрывается этой задачей.

---

## 1. Цель и контекст

Закрыть `DEBT-003`: секция «💡 Идеи и гипотезы (Icebox / Future Ideas)» в `docs/02_Tasks/Kanban.md` дублирует Icebox из `Roadmap.md` и содержит два **уже выполненных** пункта, создавая второй источник правды:

* «Семантический контроль фаз в `kb_lint.py`…» — реализовано в TASK-059 (Фаза 15);
* «Адаптация для вайбкодеров и новичков (Chat-First DX…)» — реализовано в Фазе 14 (TASK-052…TASK-056).

Удалить только эти два пункта. Оставить без изменений:

* «Конфигурации для нишевых агентов: Continue.dev и Aider»;
* два отклонённых пункта (`[x] Отклонено: …`).

Отдельного `PLAN-XXX` у Фазы 26 нет: источник работы — реестр `TechDebt.md`, DEBT-003.

## 2. Контракт файлов

* `[MODIFY]` `docs/02_Tasks/Kanban.md` — секция Icebox: удалить два выполненных пункта, остальные записи сохранить.

## 3. План верификации (Verification Plan)

- [ ] `python scripts/kb_lint.py --path docs` → Exit code 0, 0 broken links, 0 fast-track warnings.
- [ ] В Icebox остались ровно три пункта: Continue/Aider и два отклонённых; ссылок на TASK-059 и Фазу 14 как на идеи нет.
- [ ] `git diff -- docs/02_Tasks/Kanban.md` содержит только удаление двух строк (без перестановок и правок соседних пунктов).

## 4. Критерии готовности (DoD)

- [ ] Два устаревших пункта удалены; остальные записи не изменены.
- [ ] `kb_lint` зелёный; рабочее дерево содержит только `Kanban.md` (плюс артефакты завершения).
- [ ] `DEBT-003` переведён в `Resolved Debt` со ссылкой на `TASK-097` на шаге `/kb-complete`.
- [ ] Статус обновлён в Kanban, Roadmap и Devlog.
