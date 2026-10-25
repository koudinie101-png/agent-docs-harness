---
id: TECHDEBT
title: "Реестр технического долга (Tech Debt Registry)"
type: techdebt
status: active
created: 2026-10-15
updated: 2026-10-25
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
| DEBT-004 | P3 | `scripts/kb_lint.py` (`--format sarif`) | SARIF без `region.startLine`: Code Scanning принимает документ и показывает правило, файл и сообщение с именем битой ссылки (probe в TASK-109); строка 1 — дефолт GitHub, не наше значение. Трекинг строк потребовал бы переработки 15 проверок без соразмерного выигрыша | [[Specs/28_GateHygiene/TASK-109-debt004-decision\|TASK-109]] | 2026-10-25 |
| DEBT-005 | P3 | `tests/` (DSH Windows sandbox) | Sandbox-обёртка (`TRG-03`) жила только в untracked `tmp/`: без неё `unittest` падал `PermissionError WinError 5`. Промоушен в Tier 1 — `scripts/run_tests_sandbox.py` | [[Specs/28_GateHygiene/TASK-104-sandbox-test-runner-promotion\|TASK-104]] | 2026-10-25 |
| DEBT-003 | P3 | `docs/02_Tasks/Kanban.md` | Секция «Идеи и гипотезы (Icebox / Future Ideas)» дублировала Icebox из `Roadmap.md` и содержала выполненные пункты (TASK-059, Фаза 14); два пункта удалены, оставлены Continue/Aider и отклонённые ADR | [[Specs/26_TechDebt/TASK-097-clean-stale-kanban-icebox\|TASK-097]] | 2026-10-18 |
| DEBT-002 | P3 | `.github/workflows/rules-check.yml` | Не было `permissions: contents: read` и `concurrency`; `on: push` запускался на тегах параллельно с релизом; гейт не запускал `kb_lint`; тесты шумели в логах. Исправлено: read-only permissions, `concurrency`/`cancel-in-progress`, branch-фильтр без тегов, шаг `kb_lint`, `-q` | [[Specs/26_TechDebt/TASK-098-rules-check-ci-hardening\|TASK-098]] | 2026-10-18 |
| DEBT-001 | P3 | `rules/AGENTS_CORE.md` (`client-agents`) | Устаревшая нумерация заголовков 6–11 не совпадала с индексом 1–24. Исправлено: шесть заголовков без числовых префиксов, 12 golden-фикстур перегенерированы, Tier 1 guard против возврата номеров | [[Specs/26_TechDebt/TASK-100-align-rules-section-numbering\|TASK-100]] | 2026-10-18 |
