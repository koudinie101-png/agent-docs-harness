---
id: TASK-050
title: "Консолидация docs-as-code и kb-onboard, двухуровневая таксономия шаблонов в Onboarding.md"
status: done
type: task
phase: 13
component:
  - skills
  - onboarding
  - templates
  - docs
parent_plan: "[[../../Plans/PLAN-013-rules-layering-thin-forwarders-and-obsidian-taxonomy|PLAN-013]]"
created: 2026-10-11
updated: 2026-10-11
tags:
  - task/spec
  - phase13
  - skills
  - onboarding
  - templates
  - taxonomy
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-050 — Консолидация docs-as-code и kb-onboard, двухуровневая таксономия шаблонов в Onboarding.md

> **ID:** TASK-050 | **Статус:** Выполнено (Режим 3)  
> **План:** [[../../Plans/PLAN-013-rules-layering-thin-forwarders-and-obsidian-taxonomy|PLAN-013]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Обоснование:** [[../../../04_Research/RESEARCH-016-agent-rules-hierarchy-and-knowledge-base-structure|RESEARCH-016]] | **Решение:** [[../../../03_Decisions_ADR/ADR-0021-rules-layering-thin-forwarders-and-obsidian-taxonomy|ADR-0021]]

---

## 1. Цель задачи

1. **Консолидация онбординга и реестра скиллов:** Упразднить избыточный мета-скилл `.agents/skills/docs-as-code/`, дублирующий функции `kb-onboard` и онбординг-гайда `docs/Onboarding.md`. Высвободить постоянный слот в Always-On реестре описаний скиллов модели, перенеся навигацию и справочник жизненного цикла целиком в `kb-onboard`.
2. **Двухуровневая таксономия шаблонов (Core vs Advanced):** Снизить когнитивный барьер 14 шаблонов базы знаний для разработчиков, зафиксировав в `docs/Onboarding.md` и `docs/00_Templates/TEMPLATE_ONBOARDING.md` четкую градацию:
   - **Core Essentials (4 базовых шаблона):** `TEMPLATE_ADR.md`, `TEMPLATE_PLAN.md`, `TEMPLATE_TASK.md`, `TEMPLATE_BUG.md` — основные рабочие инструменты повседневной разработки.
   - **Advanced Governance (10 расширенных шаблонов):** `TEMPLATE_RESEARCH.md`, `TEMPLATE_RELEASE.md`, `TEMPLATE_FEEDBACK.md`, `TEMPLATE_TEST.md`, `TEMPLATE_DEVLOG.md`, `TEMPLATE_INDEX.md`, `TEMPLATE_KANBAN.md`, `TEMPLATE_ROADMAP.md`, `TEMPLATE_ARCHITECTURE.md`, `TEMPLATE_ONBOARDING.md` — системные каркасы для автономных скиллов агента.

---

## 2. Затрагиваемые файлы

* `[DELETE]` `.agents/skills/docs-as-code/SKILL.md` (и директория `.agents/skills/docs-as-code/`) — удаление дублирующего скилла.
* `[MODIFY]` `.agents/skills/kb-onboard/SKILL.md` — расширение руководства: включение полного справочника жизненного цикла Docs-as-Code и навигационной карты.
* `[MODIFY]` `docs/Onboarding.md` — внедрение двухуровневой классификации шаблонов и обновленного перечня 12 скиллов.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_ONBOARDING.md` — синхронизация эталонного шаблона с обновленной двухуровневой таксономией.
* `[MODIFY]` `install.py` — обновление списка развертываемых скиллов (12 скиллов вместо 13) и онбординг-подсказок.
* `[MODIFY]` `tests/test_installer.py` — обновление проверок на развертывание 12 скиллов (проверка отсутствия `docs-as-code`, валидность `kb-onboard`).

---

## 3. Детали реализации

### 3.1. Упразднение `docs-as-code` и обогащение `kb-onboard`
- Скилл `.agents/skills/kb-onboard/SKILL.md` становится единой точкой входа для разработчика и агента при онбординге:
  - 4-этапный жизненный цикл (Discovery $\to$ Planning $\to$ Spec $\to$ Verification/TDD $\to$ Release $\to$ Ingestion).
  - Навигационная карта структуры каталогов `docs/`.
  - Реестр 12 специализированных скиллов (`kb-research`, `kb-adr`, `kb-plan`, `kb-task`, `kb-bug`, `kb-triage`, `kb-implement`, `kb-complete`, `kb-release`, `kb-lint`, `kb-ingest`, `kb-onboard`).

### 3.2. Таксономия шаблонов в `Onboarding.md`
В разделе шаблонов выделяются две четкие категории с объяснением назначения:
- **Базовые шаблоны (Core Essentials):** заполняются разработчиком и агентом в регулярном цикле задач.
- **Расширенные системные шаблоны (Advanced Governance):** используются скиллами и инфраструктурой харнесса, не требуют ручного создания с нуля.

---

## 4. План верификации (Verification Plan)

- [x] Синтаксическая проверка: `python -m py_compile install.py` (Exit code 0).
- [x] Проверка базы знаний: `python scripts/kb_lint.py --path docs -v` (0 broken links, Exit code 0).
- [x] Тесты инсталлятора: `python -m unittest tests/test_installer.py` (100% Pass, Exit code 0).
- [x] Полный тестовый сьют: `python -m unittest discover -s tests` (100% Pass, Exit code 0).

---

## 5. Критерии готовности (DoD)

- [x] Скилл `.agents/skills/docs-as-code/` удален, `kb-onboard` обновлен и содержит полную сводку.
- [x] В `docs/Onboarding.md` и `TEMPLATE_ONBOARDING.md` зафиксирована двухуровневая таксономия шаблонов.
- [x] Инсталлятор `install.py` разворачивает ровно 12 скиллов.
- [x] Все тесты из Плана верификации пройдены с кодом 0.
- [x] Статус задачи обновлен в Канбане (`Done`), ТЗ (`Выполнено`), Дорожной карте (`[x]`).
- [x] Результаты зафиксированы в `Devlog.md`.
