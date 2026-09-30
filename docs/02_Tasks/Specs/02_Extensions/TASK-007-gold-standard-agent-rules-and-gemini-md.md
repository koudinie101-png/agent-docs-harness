---
id: TASK-007
title: "Эталонные правила агентов по канону remote-notification и генерация GEMINI.md"
status: planned
type: task
phase: 2
component:
  - installer
  - agent-rules
  - gemini
parent_plan: "[[../../Plans/PLAN-002-full-skills-and-agent-rules-integration|PLAN-002]]"
created: 2026-09-30
updated: 2026-09-30
tags:
  - task/spec
  - phase2
  - component/installer
  - component/agent-rules
  - component/gemini
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-007 — Эталонные правила агентов по канону remote-notification и генерация GEMINI.md

> **ID:** TASK-007  
> **Статус:** К реализации (Режим 2)  
> **Теги:** #task/spec #component/installer #component/agent-rules #component/gemini  
> **Родительский план:** [[../../Plans/PLAN-002-full-skills-and-agent-rules-integration|PLAN-002]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  
> **Эталон:** Регламент `remote_notification/GEMINI.md`  

---

## 1. Цель задачи

Перенести полный канонический регламент из эталонного проекта `remote_notification` (все 12 правил ведения базы знаний, строгая защита 3 режимов, роль Senior Engineering Partner, отказные ADR и настраиваемый язык документации) во все генераторы правил инсталлятора `install.py`:
1. Добавить генерацию корневого файла `GEMINI.md` для поддержки Google Antigravity и Gemini CLI.
2. Обновить и унифицировать генераторы правил:
   - `generate_agents_md(project_name, stack_key, doc_lang)`
   - `generate_gemini_md(project_name, stack_key, doc_lang)`
   - `generate_clinerules(project_name, stack_key, doc_lang)`
   - `generate_claude_md(project_name, stack_key, doc_lang)`
   - `generate_cursorrules(project_name, stack_key, doc_lang)`
   - `generate_copilot_instructions(project_name, stack_key, doc_lang)`
   - `generate_windsurfrules(project_name, stack_key, doc_lang)` (.windsurfrules для Windsurf Cascade).
3. Добавить `gemini` и `windsurf` в опции `--agent` CLI и интерактивного визарда.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `install.py` — добавление генератора `generate_gemini_md`, генератора `generate_windsurfrules`, обновление существующих генераторов с интеграцией `doc_lang`, 12 дисциплин и расширение опций `--agent`.

---

## 3. Детали технической реализации

### 3.1. 12 Канонических дисциплин Docs-as-Code (включаются во все правила):
1. **Онбординг и сверка контекста:** проверка `SPEC.md`, `00_Index.md` и `Onboarding.md` перед стартом.
2. **Актуализация Kanban:** перемещение карточек с датой `(YYYY-MM-DD)`.
3. **Синхронизация Roadmap:** отметка вехи `[x]` с ссылкой `[[Specs/.../TASK-XXX|TASK-XXX]]`.
4. **Архитектурные решения (ADR) и Отказные ADR:** обязательная фиксация отклоненных подходов (`status: rejected`, префикс «Отказ от...»).
5. **Исследования платформы (Research):** стресс-тесты от противного, оценка Doze/Memory/Thread, фиксация отброшенных прототипов.
6. **Журнал разработки (Devlog):** запись хроники при завершении сессии или задачи.
7. **Obsidian-совместимость:** внутренние вики-ссылки `[[...]]` и релевантные теги.
8. **Пермалинки (Permalinks):** запрет перемещения файлов ТЗ и багов в `Done`/`Archive`.
9. **Regression-First для дефектов:** закрытие бага строго после добавления воспроизводящего автотеста.
10. **Реестр QA & Testing (`05_Testing/`):** приемочные чек-листы с `- [ ]`, отдельно от `Plans/`.
11. **Граф связей Obsidian Graph:** 7 фиксированных цветовых групп.
12. **Git-интеграция:** условный push (Remote / Local-Only / No Git) и гибридное ветвление (Trunk-Based Docs + Smart Feature Branching).

### 3.2. Строгость 3 режимов:
* **Режим 1 (Planning / RFC):** ЖЕСТКИЙ ЗАПРЕТ НА КОД. Роль Senior Engineering Partner. ОБЯЗАТЕЛЬНОЕ ПОДТВЕРЖДЕНИЕ ПОЛЬЗОВАТЕЛЯ перед внесением изменений в базу знаний.
* **Режим 2 (Task Spec):** ЖЕСТКИЙ ЗАПРЕТ НА КОД. Перечень файлов `[NEW]`/`[MODIFY]`/`[DELETE]`, сигнатуры/интерфейсы, DoD и детальный Verification Plan.
* **Режим 3 (Implementation):** реализация строго по ТЗ, прогон Verification Plan, закрытие через сквозной чек-лист (DoD, Kanban, Roadmap, Devlog, kb_lint, Git commit & push).

### 3.3. Языковой регламент (`doc_lang`):
* Если `doc_lang == "ru"`: диалог, CoT рассуждения, планы, ТЗ, баг-репорты, записи Devlog и документация ведутся на русском языке. Исходный код, сигнатуры, имена типов и git-коммиты — на английском.
* Если `doc_lang == "en"`: документация и диалог ведутся на английском.

---

## 4. План верификации (Verification Plan)

### Сборка и синтаксис:
- [ ] Проверка синтаксиса: `python -m py_compile install.py` (код 0).
- [ ] Проверка базы знаний линтером: `python scripts/kb_lint.py --path docs`.

### Интеграционная проверка генерации правил:
- [ ] Тестовая установка: `python install.py -y --target-dir test_rules --agent all --doc-lang ru --stack generic --git none`.
- [ ] Проверка наличия файлов:
  - `test_rules/AGENTS.md`
  - `test_rules/GEMINI.md`
  - `test_rules/.clinerules`
  - `test_rules/CLAUDE.md`
  - `test_rules/.cursorrules`
  - `test_rules/.windsurfrules`
  - `test_rules/.github/copilot-instructions.md`
- [ ] Проверка содержания: наличие маркеров 12 дисциплин, языкового регламента, отказных ADR и запретов Режима 1/2.
- [ ] Очистка временного каталога `test_rules`.

---

## 5. Критерии готовности (Definition of Done)

- [ ] Все генераторы правил (`GEMINI.md`, `AGENTS.md`, адаптеры) обновлены в `install.py`.
- [ ] В `install.py` поддерживаются опции `gemini` и `windsurf`.
- [ ] Все пункты Плана верификации пройдены успешно.
