---
id: TASK-048
title: "Очистка AGENTS.md от графового шума и изоляция таксономии Obsidian Graph в .obsidian/graph.json"
status: done
type: task
phase: 13
component:
  - rules
  - agents
  - installer
parent_plan: "[[../../Plans/PLAN-013-rules-layering-thin-forwarders-and-obsidian-taxonomy|PLAN-013]]"
created: 2026-10-11
updated: 2026-10-11
tags:
  - task/spec
  - phase13
  - token-optimization
  - obsidian-graph
  - agents-md
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-048 — Очистка AGENTS.md от графового шума и изоляция таксономии Obsidian Graph в .obsidian/graph.json

> **ID:** TASK-048 | **Статус:** Выполнено (Режим 3)  
> **План:** [[../../Plans/PLAN-013-rules-layering-thin-forwarders-and-obsidian-taxonomy|PLAN-013]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Обоснование:** [[../../../04_Research/RESEARCH-016-agent-rules-hierarchy-and-knowledge-base-structure|RESEARCH-016]] | **Решение:** [[../../../03_Decisions_ADR/ADR-0021-rules-layering-thin-forwarders-and-obsidian-taxonomy|ADR-0021]]

---

## 1. Цель задачи

Устранить токеновый шум визуальной конфигурации Obsidian Graph из системного файла инструкций `AGENTS.md` и генератора `generate_agents_md` в `install.py`. 
Визуальная палитра (White, Purple, Cyan, Yellow, Orange, Red, Green) с RGB-кодами предназначается исключительно человеку и рендерится клиентом Obsidian на основе конфигурационного файла `docs/.obsidian/graph.json`. Нахождение 10-строчной Markdown-таблицы в системном промпте не несет операционной пользы для LLM и расходует ~150 токенов контекста на каждом запросе.

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `AGENTS.md` — удаление Markdown-таблицы цветов графа, замена на однострочную директиву канонической таксономии путей и тегов.
* `[MODIFY]` `install.py` — обновление генератора `generate_agents_md` (удаление таблицы цветов из шаблона генерации корневого `AGENTS.md`).
* `[MODIFY]` `tests/test_installer.py` — актуализация проверок содержимого `AGENTS.md` (удаление ассертов на таблицу цветов, проверка наличия директивы таксономии).

---

## 3. Детали реализации

### 3.1. Канонический `AGENTS.md`
Заменить блок:
```markdown
### 🎨 Obsidian Graph Color Scheme & Tagging
| Color / Category | Obsidian Path / Query | Tags | Description |
| :--- | :--- | :--- | :--- |
| ⚪ White / Light | `file:00_Index`, `file:Devlog`, `file:SPEC` | — | Entry points & root navigation hubs |
| 🟣 Purple | `path:01_Architecture` | `#arch` | System architecture, contracts & modules |
| 🔵 Blue / Cyan | `path:03_Decisions_ADR` | `#adr` | Architecture Decision Records |
| 🟡 Yellow / Amber | `path:04_Research` | `#research` | Platform research, benchmarks & quirks |
| 🟠 Orange | `path:02_Tasks` | `#task` | Backlog, Roadmap, Plans & Task Specs |
| 🔴 Red | `path:02_Tasks/Bugs` | `#bug` | Defects, bugs, RCA & regression tests |
| 🟢 Green | `path:05_Testing` | `#testing` | Acceptance testing & E2E UX checklists |
```

На компактную директиву:
```markdown
### 🎨 Obsidian Graph & Taxonomy
Visual graph taxonomy is configured in `.obsidian/graph.json`. Place notes in designated directories with canonical tags (`#arch`, `#adr`, `#research`, `#task`, `#bug`, `#testing`).
```

### 3.2. Генератор `generate_agents_md` в `install.py`
Синхронизировать шаблон генерации в `generate_agents_md`: удалить многострочную Markdown-таблицу цветов, подставив лаконичную директиву таксономии.

### 3.3. Тесты в `tests/test_installer.py`
Обновить тестовые сценарии, проверяющие генерацию `AGENTS.md`, исключив устаревшие проверки наличия названий цветов («White / Light», «Purple») и подтвердив наличие новой директивы таксономии `.obsidian/graph.json`.

---

## 4. План верификации (Verification Plan)

- [x] Синтаксическая проверка: `python -m py_compile install.py` (Exit code 0).
- [x] Проверка базы знаний: `python scripts/kb_lint.py --path docs -v` (0 broken links, Exit code 0).
- [x] Модульные тесты инсталлятора: `python -m unittest tests/test_installer.py` (100% Pass, Exit code 0).
- [x] Полный тестовый сьют: `python -m unittest discover -s tests` (100% Pass, Exit code 0).

---

## 5. Критерии готовности (DoD)

- [x] Цветовая Markdown-таблица полностью удалена из `AGENTS.md` и `install.py`.
- [x] В `AGENTS.md` и `generate_agents_md` зафиксирована лаконичная директива таксономии.
- [x] Все пункты Плана верификации пройдены с кодом 0.
- [x] Статус задачи обновлен в Канбане (`Done`), ТЗ (`Выполнено`), Дорожной карте (`[x]`).
- [x] Результаты зафиксированы в `Devlog.md`.
