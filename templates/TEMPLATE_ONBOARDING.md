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
* База в папке `docs/` репозитория (Obsidian Vault).
* Документы имеют YAML frontmatter и связаны [[00_Index|wikilinks]].
* **Permalinks:** Файлы ТЗ, планов и багов не перемещаются при закрытии.
* **Anti-Echo:** Ссылка и 3–5 пунктов резюме вместо дампа файлов.
* **Living Spec:** Синхронизация `SPEC.md` и `README.md` при смене контрактов и релизах.
* **Single-Task Barrier:** /kb-implement выполняет ровно 1 задачу/баг, остановка вызовов при завершении.

---

## 2. 4 режима разработки (Discovery + Delivery)

| Режим | Триггер | Ограничение | Выход |
| :--- | :--- | :--- | :--- |
| **🔬 Режим 0: Исследование** | `/kb-research` | **READ-ONLY (Без кода)** | `RESEARCH-XXX`, `ADR`, Icebox / Отклонено |
| **🟡 Режим 1: План** | `/kb-plan` | **READ-ONLY (Без кода)** | `PLAN-XXX.md`, Канбан `📥 Бэклог` |
| **🟠 Режим 2: ТЗ** | `/kb-task` | **READ-ONLY (Без кода)** | `TASK-XXX.md`, Канбан `⏳ В работе` |
| **🐞 Режим 2B: Триаж бага** | `/kb-bug` | **READ-ONLY (Без кода)** | `BUG-XXX.md`, Stop & Yield |
| **🟢 Режим 3: Код** | `/kb-implement` | Строго по ТЗ / TDD | Код, тесты, автозакрытие (`kb-complete`) |

---

## 3. Справочник команд
* `/kb-init` / `/kb-onboard` — Инициализация структуры / Онбординг.
* `/kb-release` — Выпуск релиза (сборка dist/, SHA-256, таргетинг дефектов, тег).
* `/kb-bug` — Фиксация дефекта и триаж (Режим 2B, RCA, релизный контракт, Stop & Yield).
* `/kb-implement` — Реализация ТЗ или исправление дефекта по TDD (`/kb-implement BUG-XXX`).
* `/kb-lint` — Проверка целостности ссылок, frontmatter и дрифта `SPEC.md`.

---

## 4. Архитектура каталогов `docs/` и таксономия шаблонов
* `00_Templates/` (16 шаблонов):
  - **Core Essentials (4):** `ADR`, `PLAN`, `TASK`, `BUG` — регулярная разработка.
  - **Advanced Governance (12):** `RESEARCH`, `RELEASE`, `FEEDBACK`, `TEST`, `DEVLOG`, `INDEX`, `KANBAN`, `ROADMAP`, `ARCHITECTURE`, `ONBOARDING`, `INCIDENT`, `TASK_MICRO`.
* `01_Architecture/`, `02_Tasks/` (задачи, планы, баги, инбокс, релизы), `03_Decisions_ADR/`, `04_Research/`, `05_Testing/`, `06_Memory/` (инциденты, паттерны).
* `Devlog.md` (журнал сессий) и `00_Index.md` (карта заметок).

---

## 5. Ветвление и синхронизация
* **Trunk-Based:** `main`. **Feature Branches:** `feat/TASK-XXX` (слияние через `kb-complete`).
* **Dual-Mode Sync:** Remote origin — push; Local-Only — локальный коммит.

---

## 6. Внедрение в существующий проект (Brownfield Adoption)
* **Greenfield Idea-First (`--idea`):** Пресет `undecided`, `SPEC.md` (`status: discovery`), старт с `/kb-research`.
* **Brownfield:** Инвентаризация стека в `SPEC.md` $\to$ план `/kb-plan` $\to$ цикл 4 режимов.
