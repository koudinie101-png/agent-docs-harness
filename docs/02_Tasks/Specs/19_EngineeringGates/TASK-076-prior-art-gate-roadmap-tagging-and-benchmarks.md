---
id: TASK-076
title: "Инженерные барьеры в шаблонах и правилах: Prior-Art Gate, трассировка // ROADMAP-<ID> и замеры >= 3 прогонов"
status: done # planned | in-progress | done | cancelled
type: task
phase: 19
component:
  - templates
  - agents
  - quality-gates
parent_plan: "[[../../Plans/PLAN-019-engineering-gates-and-tech-debt-governance|PLAN-019]]"
created: 2026-10-15
updated: 2026-10-15
tags:
  - task/spec
  - phase19
  - prior-art
  - roadmap-tagging
  - benchmarks
  - templates
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-076 — Инженерные барьеры в шаблонах и правилах: Prior-Art Gate, трассировка // ROADMAP-<ID> и замеры >= 3 прогонов

> **ID:** TASK-076 | **Статус:** Выполнено  
> **Фаза:** 19 | **План:** [[../../Plans/PLAN-019-engineering-gates-and-tech-debt-governance|PLAN-019]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../04_Research/RESEARCH-020-self-improving-defect-loop-and-quality-gates|RESEARCH-020]], [[../../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]

---

## 1. Цель задачи

Внедрить три ключевых инженерных барьера качества в шаблоны жизненного цикла и правила агентов в соответствии с [RESEARCH-020](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/docs/04_Research/RESEARCH-020-self-improving-defect-loop-and-quality-gates.md) и [ADR-0025](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/docs/03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates.md):
1. **Prior-Art Gate:** обязать агента перед созданием новых модулей исследовать существующие решения проекта и стандартной библиотеки во избежание «изобретения велосипедов» и дублирования кода. Добавить секцию в `TEMPLATE_PLAN.md` и `TEMPLATE_RESEARCH.md`.
2. **Трассировка отложенных возможностей (`// ROADMAP-<ID>`):** запретить висячие комментарии `TODO` без контекста. Любая отложенная доработка или точка расширения обязана связываться с идентификатором дорожной карты (`ROADMAP-<ID>`).
3. **Принцип «Замер = артефакт» (Benchmark Persistence):** зафиксировать обязательное проведение любых замеров (скорость, задержка, потребление токенов, память) сериями $\ge 3$ прогонов с отсечением холодного старта в `AGENTS.md` и шаблоне `TEMPLATE_TASK.md`.

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `docs/00_Templates/TEMPLATE_PLAN.md` — внедрение секции `### Prior-Art Gate`.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_RESEARCH.md` — внедрение секции `### Prior-Art Gate`.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_TASK.md` — внедрение секции `### Замеры и бенчмарки (Benchmark Persistence)`.
* `[MODIFY]` `AGENTS.md` — добавление инвариантов Prior-Art Gate, Traceable Backlog Tags (`ROADMAP-<ID>`) и Benchmark Persistence.

---

## 3. Детали реализации

### 3.1. Prior-Art Gate в `TEMPLATE_PLAN.md` и `TEMPLATE_RESEARCH.md`

В секцию 3 планов и исследований добавляется явный блок:
```markdown
### Prior-Art Gate (Существующие решения и платформенные аналоги):
* **Внутренний аудит:** какие существующие модули, утилиты или структуры проекта решают схожие задачи? (Не дублировать существующий код).
* **Внешний / Платформенный аудит:** какие стандартные библиотеки или проверенные отраслевые решения существуют? Почему пишется собственная реализация?
```

### 3.2. Принцип «Замер = артефакт» в `TEMPLATE_TASK.md`

В `TEMPLATE_TASK.md` в секцию 4 (План верификации) добавляется блок:
```markdown
### Замеры и бенчмарки (при оптимизациях / изменениях производительности):
* Замеры производятся сериями не менее 3 прогонов ($\ge 3$).
* Первый «холодный» прогон отбрасывается для исключения шума инициализации кэшей.
* В отчете фиксируются: команда воспроизведения, условия окружения, единицы измерения и среднее значение ($\bar{X}$).
```

### 3.3. Нормативные инварианты в `AGENTS.md` (Tier 2 Always-On)

В `AGENTS.md` в раздел «Core Rules & Principles» добавляются инварианты:
```markdown
14. **Prior-Art Gate Invariant:**
    - Перед созданием новых модулей, классов или подсистем агент обязан проверить кодовую базу репозитория и стандартную библиотеку языка на наличие готовых аналогов.
    - Изобретение велосипедов и создание параллельных сущностей с дублирующей функциональностью категорически запрещено.

15. **Traceable Backlog Tags (// ROADMAP-<ID>):**
    - В кодовой базе запрещены бессистемные «висячие» комментарии `TODO` / `FIXME` без явной привязки к дорожной карте.
    - Любая отложенная возможность или точка расширения оформляется строго в формате `// ROADMAP-<ID>` (или `# ROADMAP-<ID>`, где `<ID>` — идентификатор фазы, задачи или пункта Icebox в `Roadmap.md`).

16. **Benchmark Persistence («Замер = артефакт»):**
    - Любые утверждения об ускорении, потреблении памяти или экономии токенов подтверждаются серией из $\ge 3$ воспроизводимых прогонов.
    - Первый замер отбрасывается (защита от холодного старта). В артефакте задачи обязательно сохраняются точные команды и числовые результаты.
```

---

## 4. План верификации (Verification Plan)

- [ ] Линт базы знаний: `python scripts/kb_lint.py --path docs` (Exit code 0, 0 broken links).
- [ ] Контроль объема шаблонов: суммарный объем 16 шаблонов в `docs/00_Templates/` не должен превышать лимит $28\text{ KB}$ (High-SNR Token Budget).
- [ ] Семантическая проверка: убедиться в наличии секций Prior-Art в обоих шаблонах и инвариантов в `AGENTS.md`.

---

## 5. Критерии готовности (DoD)

- [ ] Шаблоны `TEMPLATE_PLAN.md` и `TEMPLATE_RESEARCH.md` содержат секцию `Prior-Art Gate`.
- [ ] Шаблон `TEMPLATE_TASK.md` содержит протокол серийных замеров.
- [ ] Правила `Prior-Art Gate`, `ROADMAP-<ID>` и «Замер = артефакт» зафиксированы в `AGENTS.md`.
- [ ] Все пункты Плана верификации пройдены.
