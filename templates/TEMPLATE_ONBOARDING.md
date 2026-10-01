---
id: ONBOARDING
title: Руководство по онбордингу (Onboarding Guide)
status: active
type: hub
created: 2026-09-19
updated: 2026-09-19
tags:
  - onboarding
  - guide
  - docs-as-code
---

# 🚀 Руководство по онбордингу (Onboarding)

> **Назначение:** Точка входа для разработчиков и агентов: архитектура `docs/`, 4 режима и команды.  
> **Связи:** [[00_Index|00_Index]], [[02_Tasks/Kanban|Канбан]], [[02_Tasks/Roadmap|Дорожная карта]], [[Devlog|Журнал]].

---

## 1. Docs-as-Code Vault
* База живет в папке `docs/` репозитория (Obsidian Vault).
* Все документы имеют YAML frontmatter и связаны ссылками [[00_Index|wikilinks]].
* **Permalinks:** Файлы ТЗ, планов и багов не перемещаются при закрытии.
* **Anti-Echo:** Агенты возвращают ссылку и 3–5 пунктов резюме вместо дампа файлов.

---

## 2. 4 режима разработки (Discovery + Delivery)

| Режим | Триггер | Ограничение | Выход |
| :--- | :--- | :--- | :--- |
| **🔬 Режим 0: Исследование** | `/kb-research` | **READ-ONLY (Без кода)** | `RESEARCH-XXX`, `ADR`, Icebox / Отклонено |
| **🟡 Режим 1: План** | `/kb-plan` | **READ-ONLY (Без кода)** | `PLAN-XXX.md`, Канбан `📥 Бэклог` |
| **🟠 Режим 2: ТЗ** | `/kb-task` | **READ-ONLY (Без кода)** | `TASK-XXX.md`, Канбан `⏳ В работе` |
| **🟢 Режим 3: Код** | `/kb-implement` | Строго по ТЗ | Код, тесты, автозакрытие (`kb-complete`) |

---

## 3. Справочник команд
* `/kb-init` / `/kb-onboard` — Инициализация структуры / Онбординг.
* `/kb-release` — Выпуск релиза (сборка dist/, SHA-256, тег).
* `/kb-bug` — Фиксация дефекта (Regression-First TDD, RCA).
* `/kb-lint` — Проверка целостности ссылок и frontmatter.

---

## 4. Архитектура каталогов `docs/`
* `00_Templates/` (шаблоны), `01_Architecture/` (архитектура), `02_Tasks/` (задачи, планы, релизы).
* `03_Decisions_ADR/` (ADR), `04_Research/` (исследования), `05_Testing/` (тестирование UX).
* `Devlog.md` (журнал сессий) и `00_Index.md` (карта заметок).

---

## 5. Ветвление и синхронизация
* **Trunk-Based:** `main`. **Feature Branches:** `feat/TASK-XXX` (слияние через `kb-complete`).
* **Dual-Mode Sync:** Remote origin — push; Local-Only — локальный коммит.

---

## 6. Внедрение в существующий проект (Brownfield Adoption)
* **Шаг 1 (Инвентаризация):** Изучи кодовую базу репозитория и зафиксируй стек в `SPEC.md`.
* **Шаг 2 (План и бэклог):** Создай план внедрения (`/kb-plan`) и внеси карточки в Канбан.
* **Шаг 3 (Дисциплина 4 режимов):** Веди задачи строго по циклу `/kb-research` -> `/kb-plan` -> `/kb-task` -> `/kb-implement`.
