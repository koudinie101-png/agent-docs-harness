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

> **Назначение:** Точка входа для разработчиков и агентов: архитектура `docs/`, 3 режима и команды.  
> **Связи:** [[00_Index|00_Index]], [[02_Tasks/Kanban|Канбан]], [[02_Tasks/Roadmap|Дорожная карта]], [[Devlog|Журнал]].

---

## 1. Docs-as-Code Vault
* База живет в папке `docs/` репозитория (Obsidian Vault).
* Все документы имеют YAML frontmatter и связаны ссылками `[[Заметка]]`.
* **Permalinks:** Файлы ТЗ, планов и багов не перемещаются при закрытии.
* **Anti-Echo:** Агенты возвращают ссылку и 3–5 пунктов резюме вместо дампа файлов.

---

## 2. 3 режима разработки

| Режим | Триггер | Ограничение | Выход |
| :--- | :--- | :--- | :--- |
| **🟡 Режим 1: План** | `/kb-plan` | **READ-ONLY (Без кода)** | `PLAN-XXX.md`, Канбан `📥 Бэклог` |
| **🟠 Режим 2: ТЗ** | `/kb-task` | **READ-ONLY (Без кода)** | `TASK-XXX.md`, Канбан `⏳ В работе` |
| **🟢 Режим 3: Код** | `/kb-implement` | Строго по ТЗ | Код, тесты, автозакрытие (`kb-complete`) |

---

## 3. Справочник команд

| Команда | Назначение |
| :--- | :--- |
| `/kb-init` / `/kb-onboard` | Инициализация структуры `docs/` / Онбординг |
| `/kb-plan` / `/kb-task` | Режим 1 (План) / Режим 2 (ТЗ с контрактами) |
| `/kb-implement` / `/kb-complete` | Режим 3 (Код + автозакрытие) / Ручная финализация |
| `/kb-release` | Релиз: сборка `dist/`, SHA-256, чейнджлог, тег |
| `/kb-bug` / `/kb-adr` / `/kb-research` | Дефект (TDD) / Решение ADR / Исследование |
| `/kb-lint` | Аудит целостности ссылок и валидности frontmatter |

---

## 4. Архитектура каталогов `docs/`

```text
docs/
├── 00_Templates/     # 13 каркасных шаблонов
├── 01_Architecture/  # Архитектура и системные контракты
├── 02_Tasks/         # Kanban, Roadmap, Plans/, Specs/, Bugs/, Releases/
├── 03_Decisions_ADR/ # Архитектурные решения ADR-XXXX
├── 04_Research/      # Исследования и бенчмарки RESEARCH-XXX
├── 05_Testing/       # Сценарии приемочного тестирования E2E UX
├── Devlog.md         # Журнал сессий разработки
└── 00_Index.md       # Карта заметок (MOC)
```

---

## 5. Ветвление и синхронизация
* **Trunk-Based Docs:** `docs/` коммитится в `main`. Старт: `git pull --rebase`.
* **Feature Branches:** Крупные фичи изолируются в `feat/TASK-XXX` и сливаются через `kb-complete`.
* **Dual-Mode Sync:** При наличии remote origin изменения пушатся; в Local-Only режиме push пропускается.
