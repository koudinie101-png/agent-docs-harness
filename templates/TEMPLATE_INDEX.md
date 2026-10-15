---
id: 00_INDEX
title: "База знаний: [Название Проекта]"
status: active
type: hub
created: 2026-09-19
updated: 2026-09-19
tags:
  - project
  - index
---

# 🧠 База знаний: [Название Проекта]

> **Спецификация:** [[../SPEC|SPEC.md]] | **Онбординг:** [[Onboarding|Онбординг]] | **Вайбкодинг:** [[Zero_To_Hero_Guide|Вайбкодинг]]  

---

## 🗺️ Карта разделов

```mermaid
flowchart TD
    Index["00_Index (Хаб)"] --> Onboarding["[[Onboarding|Онбординг]]"]
    Index --> Zero["[[Zero_To_Hero_Guide|Вайбкодинг]]"]
    Index --> Arch["01. Архитектура"]
    Index --> Tasks["02. Задачи"]
    Index --> ADR["03. ADR"]
    Index --> Research["04. Исследования"]
    Index --> Testing["05. Тестирование"]
    Index --> Memory["06. Память"]
    Index --> Devlog["[[Devlog|Журнал]]"]

    Tasks --> Kanban["[[02_Tasks/Kanban|Канбан]]"]
    Tasks --> Roadmap["[[02_Tasks/Roadmap|Дорожная карта]]"]
```

---

## 📂 Разделы хранилища
* **Хабы:** [[Onboarding|Онбординг]], [[Zero_To_Hero_Guide|Вайбкодинг]], [[Devlog|Журнал разработки]], [[../SPEC|SPEC.md]].
* **`01_Architecture/`:** Архитектурные схемы и контракты.
* **`02_Tasks/`:** [[02_Tasks/Kanban|Канбан]], [[02_Tasks/Roadmap|Дорожная карта]], `Inbox/`, `Plans/`, `Specs/`, `Bugs/`, `Releases/`.
* **`03_Decisions_ADR/`:** Реестр решений (`ADR-XXXX`).
* **`04_Research/`:** Исследования и бенчмарки (`RESEARCH-XXX`).
* **`05_Testing/`:** Чек-листы тестирования E2E UX.
* **`06_Memory/`:** Процедурная память (`patterns.md`) и отчеты об инцидентах (`Incidents/INC-XXX`).
* **`00_Templates/`:** Каркасные шаблоны (16 шаблонов).
