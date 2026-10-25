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
| DEBT-004 | P3 | `scripts/kb_lint.py` (`--format sarif`) | SARIF-результаты без `region.startLine`: находки привязываются к файлу, а не к строке, поэтому аннотации в GitHub Code Scanning не указывают место. Закрывается трекингом строк в `check_*`-функциях | [[Plans/PLAN-025-docs-integrity-gate-kb-lint-productization\|PLAN-025]] | 2026-10-25 | Открыт |

---

## ✅ Погашенный технический долг (Resolved Debt)

| ID | Приоритет | Модуль / Файл | Описание техдолга | Задача погашения | Дата закрытия |
| :--- | :--- | :--- | :--- | :--- | :--- |
| DEBT-003 | P3 | `docs/02_Tasks/Kanban.md` | Секция «Идеи и гипотезы (Icebox / Future Ideas)» дублировала Icebox из `Roadmap.md` и содержала выполненные пункты (TASK-059, Фаза 14); два пункта удалены, оставлены Continue/Aider и отклонённые ADR | [[Specs/26_TechDebt/TASK-097-clean-stale-kanban-icebox\|TASK-097]] | 2026-10-18 |
| DEBT-002 | P3 | `.github/workflows/rules-check.yml` | Не было `permissions: contents: read` и `concurrency`; `on: push` запускался на тегах параллельно с релизом; гейт не запускал `kb_lint`; тесты шумели в логах. Исправлено: read-only permissions, `concurrency`/`cancel-in-progress`, branch-фильтр без тегов, шаг `kb_lint`, `-q` | [[Specs/26_TechDebt/TASK-098-rules-check-ci-hardening\|TASK-098]] | 2026-10-18 |
| DEBT-001 | P3 | `rules/AGENTS_CORE.md` (`client-agents`) | Устаревшая нумерация заголовков 6–11 не совпадала с индексом 1–24. Исправлено: шесть заголовков без числовых префиксов, 12 golden-фикстур перегенерированы, Tier 1 guard против возврата номеров | [[Specs/26_TechDebt/TASK-100-align-rules-section-numbering\|TASK-100]] | 2026-10-18 |
