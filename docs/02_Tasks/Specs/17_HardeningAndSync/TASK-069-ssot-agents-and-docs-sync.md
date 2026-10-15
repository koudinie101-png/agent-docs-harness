---
id: TASK-069
title: "Синхронизация SSOT: правила агентов, режимы жизненного цикла и таксономия 16 шаблонов"
status: done
type: task
phase: 17
component:
  - agents
  - rules
  - docs
  - onboarding
parent_plan: "[[../../Plans/PLAN-017-core-hardening-and-ssot-sync|PLAN-017]]"
created: 2026-10-14
updated: 2026-10-15
tags:
  - task/spec
  - phase17
  - ssot
  - agents
  - onboarding
  - templates
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-069 — Синхронизация SSOT: правила агентов, режимы жизненного цикла и таксономия 16 шаблонов

> **ID:** TASK-069 | **Статус:** Выполнено  
> **Фаза:** 17 | **Релиз:** v0.17.0  
> **План:** [[../../Plans/PLAN-017-core-hardening-and-ssot-sync|PLAN-017]] | **Канбан:** [[../../Kanban|Канбан]]  

---

## 1. Цель задачи
Устранить рассинхронизацию между корневой спецификацией `AGENTS.md`, генераторами правил в `install.py`, руководством онбординга и историей изменений `CHANGELOG.md`:
1. Добавить пропущенные **Режим 0 (`/kb-research`)** и **Режим 2C (`/kb-triage`)** в `generate_agents_md()` в `install.py`.
2. Заменить устаревшие роботизированные запреты (`🚨 STRICTLY NO CODE CHANGES`) на принципы Human Guardrails («Направляй, а не блокируй»).
3. Зафиксировать каноническую таксономию **16 шаблонов** (4 Core Essentials, 12 Advanced Governance) в `AGENTS.md`, `install.py`, `docs/Onboarding.md`, `docs/00_Templates/TEMPLATE_ONBOARDING.md`, `.agents/skills/kb-onboard/SKILL.md` и тестах `tests/test_installer.py`.
4. Синхронизировать структуру каталогов в `AGENTS.md` (`06_Memory/`, `02_Tasks/Inbox/`, `02_Tasks/Releases/`) и перевести Правило 11 на английский язык для стилистического единообразия.
5. Добавить ссылки на теги релизов с `[0.10.0]` по `[0.16.0]` в `CHANGELOG.md`.

---

## 2. Затрагиваемые файлы
* `[MODIFY]` `install.py` — функция `generate_agents_md()`, константа `_RULES_BODY`.
* `[MODIFY]` `AGENTS.md` — реестр каталогов, счетчик шаблонов (16), перевод Правила 11, выравнивание команды тестов в Режиме 3.
* `[MODIFY]` `README.md` — замена роботизированных фраз на Human Guardrails.
* `[MODIFY]` `docs/Onboarding.md` — таксономия 16 шаблонов (4 Core, 12 Advanced).
* `[MODIFY]` `docs/00_Templates/TEMPLATE_ONBOARDING.md` — таксономия 16 шаблонов.
* `[MODIFY]` `.agents/skills/kb-onboard/SKILL.md` — таксономия 16 шаблонов.
* `[MODIFY]` `CHANGELOG.md` — ссылки на релизы GitHub в конце файла.
* `[MODIFY]` `tests/test_installer.py` — синхронизация ассертов `test_21` и `test_26`.

---

## 3. Детали реализации

### 3.1. Синхронизация `generate_agents_md()` в `install.py`
В секцию жизненного цикла добавить:
* **Mode 0: Discovery & Feasibility (`/kb-research` & `/kb-adr`):** валидация идей до внесения в Roadmap, воронка Icebox vs Отклоненные ADR.
* **Mode 2C: Feedback Triage & Dispatch (`/kb-triage`):** двухстадийный триаж `Inbox/`, пермалинки `FB-*.md`, Stop & Yield Control.
* Заменить роботизированные алерты на фразы в духе: *«Planning phase. Focus on research and architecture; coordinate with user before implementation.»*
* Обновить заголовок `_RULES_BODY`: `## Docs-as-Code (19 Disciplines)`.

### 3.2. Таксономия 16 шаблонов в `Onboarding` и `AGENTS.md`
В корневом `AGENTS.md` и руководствах онбординга:
```markdown
- `docs/00_Templates/` — 16 canonical templates with YAML frontmatter (4 Core Essentials + 12 Advanced Governance).
```
В `tests/test_installer.py`:
Обновить ассерт в `test_26_skills_consolidation_and_template_taxonomy`:
```python
self.assertIn("16 templates: 4 Core, 12 Advanced", onboard_text)
```
И выровнять ассерт `test_21` под обновленные заголовки дисциплин.

### 3.3. Дополнение `CHANGELOG.md`
Добавить ссылки на диффы в подвале:
```markdown
[0.16.0]: https://github.com/koudinie101-png/agent-docs-harness/compare/v0.15.0...v0.16.0
[0.15.0]: https://github.com/koudinie101-png/agent-docs-harness/compare/v0.14.0...v0.15.0
...
[0.10.0]: https://github.com/koudinie101-png/agent-docs-harness/compare/v0.9.0...v0.10.0
```

---

## 4. План верификации (Verification Plan)
- [x] Автотесты: `pytest tests/test_installer.py` — 100% pass (включая `test_21` и `test_26`).
- [x] Проверка генератора: запуск `install.generate_agents_md("TestApp", "generic", "ru")` содержит разделы Режима 0 и Режима 2C.
- [x] Проверка ссылок Changelog: все URL тегов валидны и ведут на существующие версии.
- [x] Линтер: `python scripts/kb_lint.py --path docs` — Exit code 0, 0 broken links.

---

## 5. Критерии готовности (DoD)
- [x] Все адаптеры и документация согласованы с SSOT (`AGENTS.md`).
- [x] Все пункты Плана верификации пройдены.
- [x] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [x] Запись добавлена в `Devlog.md`.
