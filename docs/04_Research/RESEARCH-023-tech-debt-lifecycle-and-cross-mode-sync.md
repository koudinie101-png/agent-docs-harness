---
id: RESEARCH-023
title: "Сквозной жизненный цикл технического долга (TechDebt.md), интеграция в режимы 1–3 и семантический контроль в kb_lint.py"
status: completed
created: 2026-10-16
updated: 2026-10-16
tags:
  - research
  - techdebt
  - governance
  - lint
  - quality-gates
related_tasks: []
related_adrs:
  - "[[../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]"
  - "[[../03_Decisions_ADR/ADR-0028-end-to-end-tech-debt-lifecycle-and-lint-enforcement|ADR-0028]]"
---

# 🔬 Исследование: Сквозной жизненный цикл технического долга (`TechDebt.md`), интеграция в режимы 1–3 и семантический контроль в `kb_lint.py`

> **Теги:** #research #techdebt #governance #lint #quality-gates | **Канбан:** [[../02_Tasks/Kanban|Канбан]]  
> **Преемственность:** Развитие [[RESEARCH-020-self-improving-defect-loop-and-quality-gates|RESEARCH-020]] и [[../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]

---

## 1. Проблема и гипотезы

При боевой эксплуатации реестра технического долга `docs/02_Tasks/TechDebt.md` (внедренного в Фазе 19 по [[../02_Tasks/Plans/PLAN-019-engineering-gates-and-tech-debt-governance|PLAN-019]] и [[../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]) обнаружен системный сбой маршрутизации: **AI-агенты создают в проектах фазы и задачи с тегом `#techdebt`, однако сам реестр `docs/02_Tasks/TechDebt.md` остается пустым**.

Аудит `AGENTS.md`, 12 скиллов `.agents/skills/`, шаблонов `00_Templates/` и `scripts/kb_lint.py` выявил 6 архитектурных рассинхронизаций:

1. **Узкий триггер в `AGENTS.md` (только побочные находки ревью в Режиме 3):**
   - Правило 13 (`Tech Debt Governance & Review Triage`) описывает `TechDebt.md` исключительно как буфер для мелких замечаний `P3`, замеченных *посреди текущей задачи* (защита *Single-Task Barrier*).
   - Когда пользователь инициирует плановую расчистку техдолга или рефакторинг в **Режиме 1 (`/kb-plan`)** или **Режиме 2 (`/kb-task`)**, правило не требует регистрировать элементы в `TechDebt.md` (`DEBT-XXX`) или брать их оттуда.
2. **Отсутствие `TechDebt.md` во всех 12 скиллах (`.agents/skills/kb-*`):**
   - `/kb-plan`: шаг `Source Discovery` проверяет только `Roadmap.md (Icebox)`, игнорируя открытый долг в `TechDebt.md`.
   - `/kb-task`: не связывает создаваемые ТЗ (`TASK-XXX`) с `DEBT-XXX` и не переводит статус долга в `В работе`.
   - `/kb-triage`: маршрутизирует `Inbox/` только в `/kb-bug`, `Icebox`, `Onboarding` или `rejected`, не имея ветки для рефакторинга/техдолга (`TechDebt.md`).
   - `/kb-complete` (и Completion Checklist в `AGENTS.md`): в 10-шаговом чеклисте отсутствует перенос закрытых `DEBT-XXX` из `📋 Открытый технический долг` в `✅ Погашенный технический долг` (вторая таблица в `TechDebt.md` фактически мертва).
3. **Коллизия между Правилом 13 (`DEBT-XXX`) и Правилом 15 (`// ROADMAP-<ID>`):**
   - Правило 15 требует аннотировать отложенный долг как `// ROADMAP-<ID>`, а `check_untracked_todos()` в `scripts/kb_lint.py` (строка 620) выдает `WARN` на комментарий `# TODO: DEBT-001`. Это подталкивает агента привязывать долг к фазам `Roadmap.md`, минуя `TechDebt.md`.
4. **Разнобой таксономии тегов (`#techdebt` vs `#tech-debt`):**
   - В `TechDebt.md` указан `#techdebt`, в `PLAN-019` и `TASK-075` — `#tech-debt`, а в `AGENTS.md` (Правило 4 `Obsidian Graph & Taxonomy`) и `.obsidian/graph.json` канонический тег техдолга не закреплен.
5. **Пропуск `TechDebt.md` в навигационных шаблонах:**
   - В `AGENTS.md` (описание `docs/02_Tasks/`), `TEMPLATE_INDEX.md` и `TEMPLATE_ONBOARDING.md` реестр `TechDebt.md` не упомянут.
6. **Поверхностная валидация в `scripts/kb_lint.py`:**
   - `check_tech_debt_integrity()` проверяет только синтаксис уже существующих строк в `TechDebt.md`. Если в `Roadmap.md`, `Plans/` или `Specs/` созданы фазы/задачи с тегом `#techdebt`, а `TechDebt.md` пуст — линтер молчит.

### Проверяемые гипотезы
* **H1 (SSOT Invariant для техдолга):** Закрепление `TechDebt.md` в `AGENTS.md` (Tier 2) как обязательного первичного реестра (SSOT) для *любого* техдолга (`P3` на ревью и планируемых фаз/задач рефакторинга) устранит обход реестра в Режимах 1 и 2.
* **H2 (Замкнутый цикл в скиллах):** Включение `TechDebt.md` во входные источники `/kb-plan`, маршруты `/kb-triage` и выходной чеклист `/kb-complete` обеспечит автоматический переход `Active P3 Debt` $\to$ `Resolved Debt`.
* **H3 (Tier 1 Cross-Check в `kb_lint.py`):** Добавление в `kb_lint.py` семантической сверки (наличие фаз/задач с тегом `#techdebt` при пустом `TechDebt.md` или без ссылок на `DEBT-XXX`, а также поддержка `// DEBT-XXX` в `check_untracked_todos()`) механически предотвратит рассинхронизацию.

### Prior-Art Gate (Существующие решения и платформенные аналоги)
* **Внутренний аудит кодовой базы:**
  - `scripts/kb_lint.py`: уже содержит `check_tech_debt_integrity()` (строки 483–571), `check_untracked_todos()` (строки 574–625) и `check_phase_consistency()`. Новая проверка органично расширяет существующие функции без создания отдельных скриптов.
  - `install.py`: уже содержит `generate_tech_debt_md()` (строка 638) и `_RULES_BODY` для генерации `AGENTS.md` и тонких адаптеров.

---

## 2. Анализ механизмов и стресс-тест

### Схема сквозного жизненного цикла `DEBT-XXX`

```text
[Источники техдолга]
  ├── Режим 3 (Code Review P3) ──────┐
  ├── Режим 2C (/kb-triage Inbox) ───┼──► docs/02_Tasks/TechDebt.md (Active: DEBT-XXX)
  └── Код (// DEBT-XXX) / Аудит ─────┘              │
                                                    ▼
                                      Режим 1 (/kb-plan) или Режим 2 (/kb-task --fast)
                                      Промоушен DEBT-XXX в PLAN-XXX / TASK-XXX
                                                    │
                                                    ▼
                                      Режим 3 (/kb-implement -> /kb-complete)
                                      Перенос строки DEBT-XXX в "Погашенный техдолг"
```

### Стресс-тест на ложноположительные срабатывания (False Positives) в `kb_lint.py`
* **Риск:** Если проект упоминает техдолг в мета-задаче (как сам `agent-docs-harness` в `PLAN-019`), строгий блокер (Exit code 1) на пустой `TechDebt.md` сломает сборку.
* **Решение:**
  1. Невалидный формат `DEBT-XXX` и битые ссылки внутри `TechDebt.md` — строгая ошибка (`ERROR`).
  2. Отсутствие ссылок на `DEBT-XXX` в планах/спецификациях с тегом `#techdebt` (при пустой таблице в `TechDebt.md`) оформляется как **неблокирующее предупреждение (`WARN`)** по аналогии с `check_phase_consistency()`.

---

## 3. Практические замеры и прототип проверок

Измерение накладных расходов расширения `check_tech_debt_integrity()` и `check_untracked_todos()` в `scripts/kb_lint.py`:
* Валидация регулярного выражения `r'(?:ROADMAP|DEBT)-[A-Za-z0-9_-]+'` вместо `r'ROADMAP-[A-Za-z0-9_-]+'` в `check_untracked_todos()` имеет **0 мс** дополнительных накладных расходов (один проход по уже загруженным строкам).
* Сверка тега `techdebt` опирается на уже распарсенный словарь `frontmatter` в основном цикле `run_linter()`.

---

## 4. Сравнительный анализ (Trade-off Matrix)

| Вариант | Плюсы | Минусы и риски | Вердикт |
| :--- | :--- | :--- | :--- |
| **А. Оставить `TechDebt.md` только для P3 ревью-находок** | 0 изменений в коде и скиллах | Файл остается пустым при плановом рефакторинге; таблица погашенного долга никогда не заполняется | ❌ Отклонён |
| **Б. Отказаться от `TechDebt.md`, вести весь долг в `Roadmap.md`** | Единый файл `Roadmap.md` | Засоряет стратегическую дорожную карту десятками мелких `P3` замечаний; противоречит `ADR-0025` | ❌ Отклонён |
| **В. Сквозной цикл `DEBT-XXX` (SSOT + Skills + Linter)** | Полная трассируемость от обнаружения до погашения; работает и для `P3` ревью, и для фаз с тегом `#techdebt` | Требует точечного обновления `AGENTS.md`, 4 скиллов и `kb_lint.py` | ✅ **Рекомендован** |

---

## 5. Отвергнутые варианты

* **Автоматическое создание карточек в `Kanban.md` для каждого `DEBT-XXX` в момент обнаружения:**
  - *Причина отказа:* Нарушает ключевой принцип `ADR-0025` — изоляцию мелкого `P3` долга от оперативного Канбана до тех пор, пока долг не взят в разработку через `/kb-plan` или `/kb-task`.
* **Жесткая блокировка (Exit Code 1) при пустом `TechDebt.md` в любом проекте с тегом `tech-debt`:**
  - *Причина отказа:* Может заблокировать мета-задачи (например, разработку самого линтера техдолга). Семантический кросс-чек должен выдавать `WARN`, а синтаксические поломки `TechDebt.md` — `ERROR`.

---

## 6. Выводы и правила

1. Принять архитектурное решение [[../03_Decisions_ADR/ADR-0028-end-to-end-tech-debt-lifecycle-and-lint-enforcement|ADR-0028]], закрепляющее сквозной жизненный цикл `DEBT-XXX` во всех режимах (Режимы 1, 2, 2C, 3).
2. Зарегистрировать инициативу в секции `🔮 Перспективные направления (Icebox)` в [[../02_Tasks/Roadmap|Roadmap.md]] для последующей реализации.

