---
id: TASK-083
title: "Сквозной цикл DEBT-XXX в скиллах (kb-plan, kb-task, kb-triage, kb-complete), правилах AGENTS.md, шаблонах и install.py"
status: done # planned | in-progress | done | cancelled
type: task
phase: 21
component:
  - skills
  - agent-rules
  - templates
  - installer
parent_plan: "[[../../Plans/PLAN-021-tech-debt-lifecycle-and-cross-mode-sync|PLAN-021]]"
created: 2026-10-16
updated: 2026-10-18
tags:
  - task/spec
  - phase21
  - techdebt
  - skills
  - agents
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-083 — Сквозной цикл DEBT-XXX в скиллах (kb-plan, kb-task, kb-triage, kb-complete), правилах AGENTS.md, шаблонах и install.py

> **ID:** TASK-083 | **Статус:** Выполнено (Режим 3)  
> **Фаза:** 21 | **План:** [[../../Plans/PLAN-021-tech-debt-lifecycle-and-cross-mode-sync|PLAN-021]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../04_Research/RESEARCH-023-tech-debt-lifecycle-and-cross-mode-sync|RESEARCH-023]], [[../../../03_Decisions_ADR/ADR-0028-end-to-end-tech-debt-lifecycle-and-lint-enforcement|ADR-0028]]

---

## 1. Цель задачи

Замкнуть сквозной жизненный цикл технического долга (`DEBT-XXX`) на уровнях Always-On правил (Tier 2: `AGENTS.md`, IDE-адаптеры, `install.py`) и процедурных скиллов/шаблонов (Tier 3: `.agents/skills/kb-*`, `TEMPLATE_INDEX.md`, `TEMPLATE_ONBOARDING.md`, `.obsidian/graph.json`):
1. **Правила `AGENTS.md` и IDE-адаптеры:**
   - В шапке `docs/02_Tasks/` указать `TechDebt.md` (`TechDebt.md`).
   - В Правиле 4 (`Obsidian Graph & Taxonomy`) добавить канонический тег `#techdebt`.
   - В Правиле 13 (`Tech Debt Governance & End-to-End Lifecycle`) закрепить `docs/02_Tasks/TechDebt.md` как обязательный первичный реестр (SSOT) для любого техдолга `P3` (как побочных находок ревью в Режиме 3, так и плановых фаз/задач рефакторинга в Режимах 1–2 и триажа в Режиме 2C) и обязательный перенос закрытых `DEBT-XXX` в таблицу `Resolved Debt` при завершении задачи.
   - В Правиле 15 (`Traceable Backlog Tags`) разрешить `// DEBT-XXX` наравне с `// ROADMAP-<ID>`.
   - В разделе `Mode 1`, `Mode 2`, `Mode 2C`, `Mode 3` (`AGENTS.md`) кратко отразить точки синхронизации с `TechDebt.md`.
2. **Скиллы `.agents/skills/kb-*`:**
   - `kb-plan/SKILL.md`: проверка `docs/02_Tasks/TechDebt.md` при Source Discovery; при планировании фазы техдолга (`#techdebt`) — первичная регистрация `DEBT-XXX` в `TechDebt.md` и ссылки в `PLAN-XXX`.
   - `kb-task/SKILL.md`: при создании спецификации задачи с `#techdebt` — привязка к `DEBT-XXX` из `TechDebt.md` (с регистрацией записи, если она еще не внесена).
   - `kb-triage/SKILL.md`: четвертый маршрут диспетчеризации для `P3`/рефакторинга — запись `DEBT-XXX` в `docs/02_Tasks/TechDebt.md`.
   - `kb-complete/SKILL.md`: шаг миграции закрытых `DEBT-XXX` из `Active P3 Debt` в `## ✅ Погашенный технический долг (Resolved Debt)` с указанием `[[Specs/.../TASK-XXX|TASK-XXX]]`.
   - `kb-lint/SKILL.md`: упоминание проверки `TechDebt.md` (`DEBT-XXX` и связки `#techdebt`) и тегов `// DEBT-XXX`.
3. **Шаблоны, граф Obsidian и `install.py`:**
   - Добавить группу `tag:#techdebt` в `Docs-As-Code/.obsidian/graph.json` и генератор `graph.json` в `install.py`.
   - Добавить ссылку на `[[02_Tasks/TechDebt|Реестр техдолга (TechDebt.md)]]` в `TEMPLATE_INDEX.md` и `TEMPLATE_ONBOARDING.md` (уложившись в бюджет шаблонов $\le 28\,672$ байт).
   - Синхронизировать генераторы правил в `install.py` (`_RULES_BODY`, `_gen_rule`, `generate_agents_md`) и корневые файлы `GEMINI.md`, `CLAUDE.md`, `.clinerules`, `.cursorrules`, `.windsurfrules`, `.github/copilot-instructions.md`.

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `.clinerules`, `.cursorrules`, `.windsurfrules`, `.github/copilot-instructions.md` — синхронизация правил 4, 13, 15 и этапов жизненного цикла.
* `[MODIFY]` `.agents/skills/kb-plan/SKILL.md`, `.agents/skills/kb-task/SKILL.md`, `.agents/skills/kb-triage/SKILL.md`, `.agents/skills/kb-complete/SKILL.md`, `.agents/skills/kb-lint/SKILL.md` — сквозной цикл `DEBT-XXX`.
* `[MODIFY]` `Docs-As-Code/.obsidian/graph.json` — цветовая группа `tag:#techdebt`.
* `[MODIFY]` `Docs-As-Code/00_Templates/TEMPLATE_INDEX.md`, `Docs-As-Code/00_Templates/TEMPLATE_ONBOARDING.md` — навигационные ссылки на `TechDebt.md`.
* `[MODIFY]` `install.py` — синхронизация генераторов `AGENTS.md`, IDE-правил и `.obsidian/graph.json`.

---

## 3. Детали реализации

### 3.1. Ключевые инварианты в `AGENTS.md` и `install.py`
* **Rule 4:** `(#arch, #adr, #research, #task, #bug, #techdebt, #testing)`.
* **Rule 13:** `TechDebt.md` — SSOT для всех `P3`-элементов и задач рефакторинга (`#techdebt`); при планировании (`/kb-plan`) или постановке задачи (`/kb-task`) по техдолгу запись `DEBT-XXX` создается/линкуется в `Active P3 Debt`, а при завершении (`/kb-complete`) переносится в `Resolved Debt` со ссылкой на `TASK-XXX`.
* **Rule 15:** `// ROADMAP-<ID>` или `// DEBT-XXX`.

### 3.2. Контроль бюджета шаблонов
Суммарный размер `Docs-As-Code/00_Templates/*.md` обязан оставаться строго $\le 28\,672$ байт ($28\text{ KB}$).

---

## 4. План верификации (Verification Plan)

- [x] Сборка: `py -3 -m py_compile install.py scripts/*.py` (Exit code 0).
- [x] Бюджет шаблонов: `py -3 -c "from pathlib import Path; s = sum(p.stat().st_size for p in Path('templates').glob('*.md')); print(s); assert s <= 28672"` (Exit code 0).
- [x] Проверка базы знаний: `py -3 scripts/kb_lint.py --path docs` (0 broken links, Exit code 0).

---

## 5. Критерии готовности (DoD)

- [x] Все скиллы, правила, шаблоны и `install.py` обновлены строго по ТЗ.
- [x] Все пункты Плана верификации пройдены.
- [x] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [x] Запись добавлена в `Devlog.md`.
