---
id: TASK-073
title: "Матрица 4 состояний (The 4-State Matrix), Visual DoD и шаблоны жизненного цикла в AGENTS.md"
status: done
type: task
phase: 18
component:
  - templates
  - agents
  - rules
  - visual-dod
parent_plan: "[[../../Plans/PLAN-018-heterogeneous-ui-ux-and-visual-asset-harness|PLAN-018]]"
created: 2026-10-15
updated: 2026-10-15
tags:
  - task/spec
  - phase18
  - templates
  - agents
  - rules
  - visual-dod
  - ui-ux
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-073 — Матрица 4 состояний (The 4-State Matrix), Visual DoD и шаблоны жизненного цикла в AGENTS.md

> **ID:** TASK-073 | **Статус:** Выполнено  
> **Фаза:** 18 | **Релиз:** v0.18.0  
> **План:** [[../../Plans/PLAN-018-heterogeneous-ui-ux-and-visual-asset-harness|PLAN-018]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../04_Research/RESEARCH-021-heterogeneous-ui-ux-and-visual-asset-management|RESEARCH-021]], [[../../../03_Decisions_ADR/ADR-0026-heterogeneous-ui-ux-and-visual-asset-management|ADR-0026]]

---

## 1. Цель задачи

Закрепить дисциплину визуальной разработки интерфейсов в шаблонах жизненного цикла и правилах агентов:
1. **The 4-State Matrix в шаблонах:** интегрировать обязательное проектирование 4 состояний интерактивных представлений (`Empty`, `Loading`, `Error`, `Populated`) в канонические шаблоны `TEMPLATE_PLAN.md` и `TEMPLATE_TASK.md`.
2. **Multi-Actor Interaction Flow:** предусмотреть блок стейт-машины сопряжения узлов и Mermaid-диаграммы сквозного взаимодействия (`Target A <-> Protocol <-> Target B`) для гетерогенных систем.
3. **Visual DoD и Headless / CLI Fallback:** формализовать в правилах требование подтверждения выполнения UI-задач скриншотом в `docs/assets/screenshots/<target>/TASK-XXX.png`, а для сред без графического дисплея (CI/CD, удаленный SSH, чистый терминал) — подготовку Fallback-слота с ASCII/SVG-вайрфреймом или `generative_ui` предпросмотром.
4. **Актуализация правил агентов:** внедрить дисциплину UI/UX & Visual Verification Invariant в корневой `AGENTS.md` и генераторы правил в `install.py`.
5. **Контроль лимитов контекста:** обеспечить сохранение Skeleton-формата шаблонов с соблюдением лимита `docs/00_Templates/ <= 28 KB`.

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `docs/00_Templates/TEMPLATE_PLAN.md` — компактная секция матрицы 4 состояний и сопряжения узлов.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_TASK.md` — блок The 4-State UI Contract & Visual DoD.
* `[MODIFY]` `AGENTS.md` — добавление дисциплины UI/UX и инварианта Visual Verification.
* `[MODIFY]` `install.py` — обновление `_RULES_BODY` и `generate_agents_md()`.

---

## 3. Детали реализации

### 3.1. Обновление `docs/00_Templates/TEMPLATE_PLAN.md`
Добавить лаконичный блок в раздел проектирования:
```markdown
### The 4-State UI Matrix (если задача затрагивает GUI/TUI):
| Состояние | Поведение и визуализация | Обработка краевых случаев |
| :--- | :--- | :--- |
| **Empty** | Начальный экран без данных | Подсказка к первому действию / кнопка добавления |
| **Loading** | Ожидание ответа сети / узла | Скелетон / спиннер / блокировка повторной отправки |
| **Error** | Сбой транспорта / таймаут / права | Понятное сообщение + кнопка «Повторить» |
| **Populated** | Штатное отображение данных | Адаптивность, скролл, темная/светлая тема |
```

### 3.2. Обновление `docs/00_Templates/TEMPLATE_TASK.md`
В раздел верификации добавить компактный чеклист:
```markdown
### Visual DoD (для задач с GUI/TUI):
- [ ] Фиксация постоянного скриншота: `docs/assets/screenshots/<target>/TASK-XXX.png` (лимит $\le 2\text{ MB}$).
- [ ] *Headless/CLI Fallback (при отсутствии дисплея):* макет в `docs/assets/mockups/` и слот в отчете:  
  `![Скриншот](../../assets/screenshots/TASK-XXX.png) <!-- TODO: Вставьте скриншот через Ctrl+V в Obsidian -->`.
```

### 3.3. Актуализация правил в `AGENTS.md` и `install.py`
В секцию Hot Invariants / Disciplines:
* **The 4-State UI & Visual Verification Invariant:** Задачи, изменяющие графический интерфейс (GUI) или терминальный UI (TUI), обязаны проектировать 4 состояния (`Empty`, `Loading`, `Error`, `Populated`) и сопровождаться скриншотом в `docs/assets/screenshots/<target>/TASK-XXX.png`. В Headless-окружениях формируется ASCII/SVG-макет либо предпросмотр `generative_ui` с сохранением слота в отчете.
* **Git Bloat Prevention:** Запрещено коммитить временные снимки E2E-тестов; они должны изолироваться в `tmp/ui_snapshots/`.

---

## 4. План верификации (Verification Plan)

- [x] Контроль объема каталога шаблонов: суммарный размер файлов в `docs/00_Templates/` $\le 28\text{ KB}$.
- [x] Линтинг базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links).
- [x] Синтаксическая проверка `install.py`: `python -m py_compile install.py` (Exit code 0).
- [x] Проверка синхронизации SSOT: формулировки в `AGENTS.md` и `install.py` идентичны.

---

## 5. Критерии готовности (DoD)

- [x] The 4-State Matrix и Visual DoD интегрированы в шаблоны `TEMPLATE_PLAN.md` и `TEMPLATE_TASK.md`.
- [x] Правила агентов в `AGENTS.md` и `install.py` синхронизированы.
- [x] Жесткий лимит `docs/00_Templates/ <= 28 KB` не превышен.
- [x] Все пункты Плана верификации пройдены.
- [x] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [x] Запись добавлена в `Devlog.md`.
