---
id: TECHDEBT
title: "Реестр технического долга (Tech Debt Registry)"
type: techdebt
status: active
created: 2026-10-15
updated: 2026-10-18
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
| DEBT-001 | P3 | `rules/AGENTS_CORE.md` (`client-agents`) | Устаревшая нумерация развёрнутых секций (`## 🛡️ 6. Zero-State`, `## 🎨 7. The 4-State UI`, `## 💳 8. Tech Debt`, `## 🏛️ 9. Prior-Art`, `## 🏷️ 10. Traceable`, `## ⏱️ 11. Benchmark`) не совпадает с индексом 1–24 после редакционной консолидации; числа в заголовках вводят в заблуждение | [[Specs/22_RuleCompiler/TASK-088-editorial-consolidation-e2e-and-living-spec\|TASK-088]] | 2026-10-18 | Открыт |
| DEBT-002 | P3 | `.github/workflows/rules-check.yml` | Нет `permissions: contents: read` и `concurrency` (`cancel-in-progress`); триггер `on: push` без фильтра веток (запускается и на тегах параллельно с релизом); гейт не запускает `scripts/kb_lint.py`, хотя он входит в Verification Plan; вывод тестов не подавляется (шумные логи CI) | [[Bugs/BUG-011-ci-git-identity-hermetic-test\|BUG-011]], [[Bugs/BUG-012-dashboard-env-and-live-api-test\|BUG-012]] | 2026-10-18 | Открыт |
| DEBT-003 | P3 | `docs/02_Tasks/Kanban.md` | Секция «Идеи и гипотезы (Icebox / Future Ideas)» дублирует Icebox из `Roadmap.md` и содержит уже выполненные пункты (семантический контроль фаз — TASK-059; адаптация для вайбкодеров — Фаза 14), создавая второй источник правды | [[Plans/PLAN-024-symbolic-scope-and-task-contracts\|PLAN-024]] | 2026-10-18 | Открыт |

---

## ✅ Погашенный технический долг (Resolved Debt)

| ID | Приоритет | Модуль / Файл | Описание техдолга | Задача погашения | Дата закрытия |
| :--- | :--- | :--- | :--- | :--- | :--- |
