---
id: TASK-080
title: "Стандартизация TASK-XXX/ для макетов и конвенции mockups/flows/ в install.py, шаблонах и правилах агентов"
status: done # planned | in-progress | done | cancelled
type: task
phase: 20
component:
  - installer
  - templates
  - agent-rules
parent_plan: "[[../../Plans/PLAN-020-asset-storage-hardening-and-layout-linting|PLAN-020]]"
created: 2026-10-15
updated: 2026-10-16
tags:
  - task/spec
  - phase20
  - installer
  - templates
  - ui-ux
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-080 — Стандартизация TASK-XXX/ для макетов и конвенции mockups/flows/ в install.py, шаблонах и правилах агентов

> **ID:** TASK-080 | **Статус:** Выполнено (Режим 3)  
> **Фаза:** 20 | **План:** [[../../Plans/PLAN-020-asset-storage-hardening-and-layout-linting|PLAN-020]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../04_Research/RESEARCH-022-asset-storage-hardening-and-task-scoped-namespaces|RESEARCH-022]], [[../../../03_Decisions_ADR/ADR-0027-task-scoped-asset-namespaces-and-layout-linting|ADR-0027]]

---

## 1. Цель задачи

Закрепить каноническую таксономию пространств имен задач (`docs/assets/mockups/<target>/TASK-XXX/`, `docs/assets/mockups/flows/TASK-XXX/`, жизненный цикл `asis.svg` / `tobe.svg` / `<surface>_tobe.svg`) на уровнях генератора `install.py`, шаблона `TEMPLATE_TASK.md` и правил ИИ-агентов (Tier 2 & Tier 3):
1. Обновить генератор дизайн-системы в `install.py` (`create_starter_docs()` $\to$ `docs/01_Architecture/UI_Design_System.md`), добавив секцию `## 4. Организация макетов и визуальных артефактов (Asset Taxonomy)`.
2. Обновить генераторы правил агентов в `install.py` (`_RULES_BODY`, `_gen_rule`, `generate_agents_md`), зафиксировав симметрию `mockups/<target>/TASK-XXX/` и `screenshots/<target>/TASK-XXX.png`.
3. Обновить секцию `Visual DoD` в `docs/00_Templates/TEMPLATE_TASK.md` с указанием путей `docs/assets/mockups/<target>/TASK-XXX/tobe.svg` (`asis.svg`), строго соблюдая общий бюджет шаблонов `docs/00_Templates/` $\le 28\text{ KB}$ ($28\,672$ байт).
4. Синхронизировать корневой `AGENTS.md` (Правило 12) и тонкие IDE-адаптеры (`GEMINI.md`, `CLAUDE.md`, `.clinerules`, `.cursorrules`, `.windsurfrules`, `.github/copilot-instructions.md`).

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `install.py` — обновление `UI_Design_System.md` в `create_starter_docs()`, а также `_RULES_BODY`, `_gen_rule()` и `generate_agents_md()`.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_TASK.md` — уточнение путей макетов `docs/assets/mockups/<target>/TASK-XXX/tobe.svg` (`asis.svg`) в секции `Visual DoD`.
* `[MODIFY]` `AGENTS.md` — обновление Правила 12 (`The 4-State UI & Visual Verification Invariant`) с фиксацией `TASK-XXX/` для макетов и конвенции `asis.svg` / `tobe.svg`.
* `[MODIFY]` `GEMINI.md`, `CLAUDE.md`, `.clinerules`, `.cursorrules`, `.windsurfrules`, `.github/copilot-instructions.md` — синхронизация тонких адаптеров с `install.py`.

---

## 3. Детали реализации

### 3.1. Обновление `UI_Design_System.md` в `install.py` (`create_starter_docs`)

В `install.py` (строки ~884–891) дополнить шаблон `UI_Design_System.md` секцией 4:
```markdown
---

## 4. Организация макетов и визуальных артефактов (Asset Taxonomy)
* **Пространства имен задач (`TASK-XXX/`):** все проектные макеты группируются в подкаталоги задач:
  * Платформенные макеты: `docs/assets/mockups/<target>/TASK-XXX/` (`asis.svg`, `tobe.svg`, `<surface>_tobe.svg`).
  * Кросс-девайсные сценарии (для multi-target): `docs/assets/mockups/flows/TASK-XXX/`.
* **Финальные скриншоты верификации (Visual DoD):** `docs/assets/screenshots/<target>/TASK-XXX.png` (и `docs/assets/screenshots/multi-device/TASK-XXX.png`).
```

### 3.2. Обновление генераторов правил в `install.py` и корневых адаптеров

1. В `_RULES_BODY` (`install.py`, дисциплина 20) и `_gen_rule` (правило 7): указать хранение макетов в `docs/assets/mockups/<target>/TASK-XXX/` (`asis.svg`/`tobe.svg`, или `mockups/flows/TASK-XXX/`) и скриншотов в `docs/assets/screenshots/<target>/TASK-XXX.png`.
2. В `generate_agents_md` (`install.py`, секция 7) и корневом `AGENTS.md` (Правило 12): зафиксировать изоляцию макетов в `docs/assets/mockups/<target>/TASK-XXX/` (`asis.svg`, `tobe.svg`, `<surface>_tobe.svg`) и кросс-девайсных сценариев в `docs/assets/mockups/flows/TASK-XXX/`.
3. Синхронизировать `GEMINI.md`, `CLAUDE.md`, `.clinerules`, `.cursorrules`, `.windsurfrules`, `.github/copilot-instructions.md` с генераторами `install.py`.

### 3.3. Обновление `docs/00_Templates/TEMPLATE_TASK.md`

В `docs/00_Templates/TEMPLATE_TASK.md` (строки 45–49):
```markdown
### Visual DoD (для задач с GUI/TUI):
- [ ] Фиксация скриншота: `docs/assets/screenshots/<target>/TASK-XXX.png` (лимит $\le 2\text{ MB}$).
- [ ] *Headless/CLI Fallback (при отсутствии дисплея):* макет в `docs/assets/mockups/<target>/TASK-XXX/tobe.svg` (`asis.svg`) и слот в отчете:  
  `![Скриншот](../../assets/screenshots/<target>/TASK-XXX.png) <!-- Вставьте скриншот через Ctrl+V в Obsidian -->`
```

---

## 4. План верификации (Verification Plan)

- [x] Сборка: `python -m py_compile install.py scripts/*.py` (Exit code 0).
- [x] Контроль бюджета шаблонов: `python -c "from pathlib import Path; s = sum(p.stat().st_size for p in Path('docs/00_Templates').glob('*.md')); print(s); assert s <= 28672"` (Exit code 0).
- [x] Автотесты: `pytest` (Exit code 0, 100% pass).
- [x] Проверка базы знаний: `python scripts/kb_lint.py --path docs` (Exit code 0).

---

## 5. Критерии готовности (DoD)

- [x] Код и шаблоны обновлены строго по ТЗ без заглушек.
- [x] Все пункты Плана верификации пройдены.
- [x] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [x] Запись добавлена в `Devlog.md`.
