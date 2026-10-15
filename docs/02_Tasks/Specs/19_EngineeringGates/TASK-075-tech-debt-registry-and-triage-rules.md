---
id: TASK-075
title: "Инфраструктура реестра техдолга, скаффолдинг в install.py и правила триажа P1/P2 vs P3"
status: done # planned | in-progress | done | cancelled
type: task
phase: 19
component:
  - core
  - tech-debt
  - installer
  - agents
parent_plan: "[[../../Plans/PLAN-019-engineering-gates-and-tech-debt-governance|PLAN-019]]"
created: 2026-10-15
updated: 2026-10-15
tags:
  - task/spec
  - phase19
  - tech-debt
  - governance
  - triage
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-075 — Инфраструктура реестра техдолга, скаффолдинг в install.py и правила триажа P1/P2 vs P3

> **ID:** TASK-075 | **Статус:** Выполнено  
> **Фаза:** 19 | **План:** [[../../Plans/PLAN-019-engineering-gates-and-tech-debt-governance|PLAN-019]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../04_Research/RESEARCH-020-self-improving-defect-loop-and-quality-gates|RESEARCH-020]], [[../../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]

---

## 1. Цель задачи

Создать и формализовать контур управления техническим долгом в соответствии с [RESEARCH-020](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/docs/04_Research/RESEARCH-020-self-improving-defect-loop-and-quality-gates.md) и [ADR-0025](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/docs/03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates.md):
1. Развернуть канонический файл реестра `docs/02_Tasks/TechDebt.md` с разделением находок ревью на критические ($P1/P2$) и мелкие ($P3$).
2. Интегрировать автоматический скаффолдинг `docs/02_Tasks/TechDebt.md` в `install.py` (при чистой установке и при `--update` без перезаписи существующего пользовательского реестра).
3. Закрепить в `AGENTS.md` (уровень Tier 2) нормативный протокол триажа находок ревью и защиты барьера единичной задачи (Single-Task Barrier): мелкий техдолг $P3$ запрещено исправлять попутно в текущей сессии; он подлежит обязательной регистрации в `TechDebt.md`.

---

## 2. Затрагиваемые файлы

* `[NEW]` `docs/02_Tasks/TechDebt.md` — реестр технического долга проекта.
* `[MODIFY]` `install.py` — добавление генерации `TechDebt.md` в `create_starter_docs()` и логику `--update`.
* `[MODIFY]` `AGENTS.md` — внедрение нормативного инварианта «Tech Debt Governance & Review Triage ($P1/P2$ vs $P3$)».

---

## 3. Детали реализации

### 3.1. Структура `docs/02_Tasks/TechDebt.md`

Файл оформляется в соответствии со стандартом Docs-as-Code:
```markdown
---
id: TECHDEBT
title: "Реестр технического долга (Tech Debt Registry)"
type: techdebt
status: active
created: 2026-10-15
updated: 2026-10-15
tags:
  - techdebt
  - governance
  - backlog
parent_roadmap: "[[Roadmap|Дорожная карта]]"
---

# 💳 Реестр технического долга (Tech Debt Registry)

> **Теги:** #techdebt #governance #backlog | **Канбан:** [[Kanban|Канбан-доска]] | **Дорожная карта:** [[Roadmap|Roadmap]]

---

## 🎯 Протокол триажа находок ревью (Review Triage Protocol)

* **P1 / P2 (Блокеры, функциональные ошибки, регрессии):** устраняются **немедленно** в рамках текущей задачи (`TASK-XXX` или `BUG-XXX`).
* **P3 (Мелкий косметический долг, некритичный рефакторинг, отложенная оптимизация):** **запрещено** исправлять посреди текущей задачи во избежание нарушения барьера единичной задачи (Single-Task Barrier). Находка фиксируется в таблице ниже.
* **Принцип фиксации:** *«Находка ревью, оставшаяся только в чате, не существует»*.

---

## 📋 Открытый технический долг (Active P3 Debt)

| ID | Приоритет | Модуль / Файл | Описание техдолга | Задача-источник | Дата обнаружения | Статус |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |

---

## ✅ Погашенный технический долг (Resolved Debt)

| ID | Приоритет | Модуль / Файл | Описание техдолга | Задача погашения | Дата закрытия |
| :--- | :--- | :--- | :--- | :--- | :--- |
```

### 3.2. Скаффолдинг в `install.py`

В `install.py` добавить функцию:
```python
def generate_tech_debt_md() -> str:
    """Генерирует начальный реестр технического долга docs/02_Tasks/TechDebt.md."""
```
И вызывать её в `create_starter_docs()`:
```python
tech_debt_path = docs_dir / "02_Tasks" / "TechDebt.md"
if not tech_debt_path.exists():
    write_file(tech_debt_path, generate_tech_debt_md())
```
При запуске `install.py --update` существующий файл `TechDebt.md` не перезаписывается.

### 3.3. Правило в `AGENTS.md` (Tier 2 Always-On)

В `AGENTS.md` добавить раздел:
```markdown
### 13. Tech Debt Governance & Triage Protocol (P1/P2 vs P3)
- Находки код-ревью и побочные дефекты классифицируются по двум уровням:
  - **P1/P2 (Критические сбои, ошибки логики, регрессии):** устраняются немедленно в том же проходе реализации.
  - **P3 (Косметические замечания, шероховатости стиля, мелкий рефакторинг, отложенная оптимизация):** строго **запрещено** рефакторить попутно посреди текущей задачи. Находка немедленно регистрируется в `docs/02_Tasks/TechDebt.md` с идентификатором `DEBT-XXX`.
- Принцип сохранения контекста: «Находка ревью, оставшаяся только в чате, не существует».
```

---

## 4. План верификации (Verification Plan)

- [ ] Сборка: `python -m py_compile install.py` (Exit code 0).
- [ ] Линт базы знаний: `python scripts/kb_lint.py --path docs` (Exit code 0, 0 broken links).
- [ ] Ручная/модульная проверка: создание чистого каталога через `install.py` и проверка наличия `docs/02_Tasks/TechDebt.md`.
- [ ] Проверка сохранения при обновлении: повторный запуск `install.py --update` не затирает существующие строки в `TechDebt.md`.

---

## 5. Критерии готовности (DoD)

- [ ] Файл `docs/02_Tasks/TechDebt.md` создан и наполнен канонической структурой.
- [ ] Утилита `install.py` создает `TechDebt.md` при новой установке и сохраняет его при `--update`.
- [ ] Правило триажа $P1/P2$ vs $P3$ добавлено в `AGENTS.md`.
- [ ] Все пункты Плана верификации пройдены.
