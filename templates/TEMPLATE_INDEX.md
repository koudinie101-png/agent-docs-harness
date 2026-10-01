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

> **Спецификация:** [[../SPEC|SPEC.md]] | **Онбординг:** [[Onboarding|Онбординг]]  

---

## 🗺️ Карта разделов

```mermaid
flowchart TD
    Index["00_Index (Хаб)"] --> Onboarding["[[Onboarding|Онбординг]]"]
    Index --> Arch["01. Архитектура"]
    Index --> Tasks["02. Задачи"]
    Index --> ADR["03. ADR"]
    Index --> Research["04. Исследования"]
    Index --> Testing["05. Тестирование"]
    Index --> Devlog["[[Devlog|Журнал]]"]

    Tasks --> Kanban["[[02_Tasks/Kanban|Канбан]]"]
    Tasks --> Roadmap["[[02_Tasks/Roadmap|Дорожная карта]]"]
```

---

## 📂 Разделы хранилища
* **Хабы:** [[Onboarding|Онбординг]], [[Devlog|Журнал разработки]], [[../SPEC|SPEC.md]].
* **`01_Architecture/`:** Архитектурные схемы и контракты.
* **`02_Tasks/`:** [[02_Tasks/Kanban|Канбан]], [[02_Tasks/Roadmap|Дорожная карта]], `Plans/`, `Specs/`, `Bugs/`, `Releases/`.
* **`03_Decisions_ADR/`:** Реестр решений (`ADR-XXXX`).
* **`04_Research/`:** Исследования и бенчмарки (`RESEARCH-XXX`).
* **`05_Testing/`:** Чек-листы тестирования E2E UX.
* **`00_Templates/`:** Каркасные шаблоны.
