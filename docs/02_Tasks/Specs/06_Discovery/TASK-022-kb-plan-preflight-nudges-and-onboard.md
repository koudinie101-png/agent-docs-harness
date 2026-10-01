---
id: TASK-022
title: "Префлайт-чеки в kb-plan и обновление скилла kb-onboard (4-этапный цикл)"
status: done
type: task
phase: 6
component:
  - skills
  - planning
  - onboarding
parent_plan: "[[../../Plans/PLAN-006-discovery-mode-and-kb-research-lifecycle|PLAN-006]]"
created: 2026-10-01
updated: 2026-10-01
tags:
  - task/spec
  - phase6
  - component/skills
  - component/planning
  - component/onboarding
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-022 — Префлайт-чеки в kb-plan и обновление kb-onboard

> **ID:** TASK-022  
> **Статус:** Выполнено (Режим 3)  
> **Теги:** #task/spec #phase6 #component/skills #component/planning #component/onboarding  
> **Родительский план:** [[../../Plans/PLAN-006-discovery-mode-and-kb-research-lifecycle|PLAN-006]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-007-discovery-mode-and-kb-research-lifecycle-integration|RESEARCH-007]], [[../../../03_Decisions_ADR/ADR-0012-discovery-mode-and-kb-research-lifecycle-integration|ADR-0012]], [[../../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

1. **Внедрение префлайт-чеков (Pre-flight Nudges) в `.agents/skills/kb-plan/SKILL.md`:**
   - Обеспечить защиту от преждевременного планирования сырых идей (Premature Planning Trap).
   - Если пользователь запускает `/kb-plan <идея>` с темой, сопряженной с архитектурными рисками (новые внешние зависимости, неопределенность API платформ), агент обязан предложить предварительную валидацию в Режиме 0 (`/kb-research <идея>`).
   - Сохранить право пользователя продолжить планирование напрямую, если риски минимальны или идея концептуально ясна.
2. **Обновление онбординг-скилла `.agents/skills/kb-onboard/SKILL.md`:**
   - Актуализировать матрицу процессов: переход от 3-режимного процесса к 4-этапному циклу разработки (**Discovery + Delivery**).
   - Добавить описание **Режима 0 (Discovery & Feasibility)**: команды `/kb-research` и `/kb-adr`.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `.agents/skills/kb-plan/SKILL.md` — внедрение шага Pre-flight Nudge в процедуру маршрутизации намерений.
* `[MODIFY]` `.agents/skills/kb-onboard/SKILL.md` — актуализация таблицы режимов, фиксация Режима 0 и правил валидации гипотез.

---

## 3. Детали реализации

### Контракт изменений в `.agents/skills/kb-plan/SKILL.md`
В секцию `## Procedure` шаг 1 дополняется проверкой зрелости идеи:
```markdown
## Procedure
1. **Source Discovery & Intent Routing:**
   - **Explicit Idea:** If specified (`/kb-plan <idea>`), check feasibility maturity:
     - *Pre-flight Nudge:* If proposal introduces new external dependencies (violating ADR-0001), platform uncertainties, or high risk, suggest running `/kb-research <idea>` (Mode 0) first to validate trade-offs and record ADR. If user confirms direct planning or idea is low-risk, proceed immediately.
   - **No Argument (`/kb-plan`):** Inspect Icebox in `docs/02_Tasks/Roadmap.md`. Rank candidates by value impact with 1-line rationale and top recommendation. If empty, ask user.
```

### Контракт изменений в `.agents/skills/kb-onboard/SKILL.md`
Обновление структуры с отражением 4 режимов:
```markdown
---
name: kb-onboard
description: "Display developer onboarding guide, 4-stage lifecycle cheatsheet, and quick start."
---

# /kb-onboard — Developer & Agent Onboarding

Use when the user runs `/kb-onboard` or asks how to interact with the project and knowledge base.

## 🚨 Constraints
* **Adherence to Core Rules:** All work strictly adheres to the 4 operating modes defined in `AGENTS.md`.

## Procedure
1. **Present Onboarding Cheatsheet:**
   - Display reference table of `/kb-*` slash commands and 4-stage development lifecycle:
     - **Mode 0 (`/kb-research` & `/kb-adr`):** Discovery & Feasibility. Falsification, benchmarks, Icebox sync.
     - **Mode 1 (`/kb-plan`):** Conceptual Planning & RFC. Modifying code is prohibited.
     - **Mode 2 (`/kb-task`):** Engineering Specification & Contracts. Modifying code is prohibited.
     - **Mode 3 (`/kb-implement` & `/kb-complete`):** Strict implementation, automated tests, Devlog, and git sync.
2. **Review Invariants:**
   - **Permalinks:** Specs and bugs are never moved or deleted upon completion.
   - **Regression-First:** Bugs require an automated failing test before fix.
   - **Anti-Echo:** Response summaries with links instead of dumping full file bodies into chat.
3. **Reference Full Guide:**
   - Direct developer to `docs/Onboarding.md` and `docs/00_Index.md` for full onboarding guide.
```

---

## 4. План верификации (Verification Plan)

- [ ] Проверка `.agents/skills/kb-plan/SKILL.md`: шаг Pre-flight Nudge присутствует в шаге 1 процедуры, frontmatter сохранен в High-SNR формате.
- [ ] Проверка `.agents/skills/kb-onboard/SKILL.md`: описан 4-этапный цикл, команды Режима 0 зафиксированы, frontmatter обновлен.
- [ ] Аудит базы знаний: запуск `python scripts/kb_lint.py --path docs` завершается с кодом 0 и 0 битых ссылок.

---

## 5. Критерии готовности (DoD)

- [ ] Изменения в обоих скиллах внесены согласно контрактам.
- [ ] Все пункты Плана верификации пройдены.
- [ ] Статус обновлен в ТЗ (`done`), Канбане (`## ✅ Готово`) и Дорожной карте (`[x]`).
- [ ] Запись добавлена в `docs/Devlog.md`.
