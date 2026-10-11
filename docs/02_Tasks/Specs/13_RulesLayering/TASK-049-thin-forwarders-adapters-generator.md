---
id: TASK-049
title: "Реализация паттерна Thin Forwarders в генераторах адаптеров install.py"
status: in-progress
type: task
phase: 13
component:
  - rules
  - adapters
  - installer
parent_plan: "[[../../Plans/PLAN-013-rules-layering-thin-forwarders-and-obsidian-taxonomy|PLAN-013]]"
created: 2026-10-11
updated: 2026-10-11
tags:
  - task/spec
  - phase13
  - rules-layering
  - thin-forwarders
  - adapters
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-049 — Реализация паттерна Thin Forwarders в генераторах адаптеров install.py

> **ID:** TASK-049 | **Статус:** В работе  
> **План:** [[../../Plans/PLAN-013-rules-layering-thin-forwarders-and-obsidian-taxonomy|PLAN-013]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Обоснование:** [[../../../04_Research/RESEARCH-016-agent-rules-hierarchy-and-knowledge-base-structure|RESEARCH-016]] | **Решение:** [[../../../03_Decisions_ADR/ADR-0021-rules-layering-thin-forwarders-and-obsidian-taxonomy|ADR-0021]]

---

## 1. Цель задачи

Устранить проблему двойной инжекции инструкций (Double Prompt Injection) и дрейфа правил (Rule Drift) в адаптерах IDE (`GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`, `.github/copilot-instructions.md`). 
В текущей реализации генераторы адаптеров в `install.py` дублируют 15 дисциплин и развернутые описания 4 режимов из `AGENTS.md`. В средах, считывающих как системный файл, так и `AGENTS.md`, это расходует контекст вдвое и создает риск рассинхронизации.
Задача переводит адаптеры на архитектурный паттерн **Thin Forwarders** (до 25–30 строк):
1. Прямая ссылка на канонический `AGENTS.md` как Single Source of Truth (SSOT).
2. Специфичные команды верификации стека (`Build`, `Test`, `Lint`).
3. Компактный перечень скиллов и горячих инвариантов (Anti-Echo, Single-Task Barrier, запрет изменений кода в Режимах 1/2).

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `install.py` — рефакторинг генераторов адаптеров (`_gen_rule`, `generate_gemini_md`, `generate_claude_md`, `generate_cursorrules`, `generate_windsurfrules`, `generate_clinerules`, `generate_copilot_instructions`) под шаблон Thin Forwarders.
* `[MODIFY]` `GEMINI.md` — актуализация корневого адаптера проекта под тонкий формат.
* `[MODIFY]` `CLAUDE.md` — актуализация корневого адаптера под тонкий формат.
* `[MODIFY]` `.cursorrules` — актуализация корневого адаптера под тонкий формат.
* `[MODIFY]` `.windsurfrules` — актуализация корневого адаптера под тонкий формат.
* `[MODIFY]` `.clinerules` — актуализация корневого адаптера под тонкий формат.
* `[MODIFY]` `.github/copilot-instructions.md` — актуализация корневого адаптера под тонкий формат.
* `[MODIFY]` `tests/test_installer.py` — обновление проверок генерации адаптеров (наличие ссылок на `AGENTS.md`, команд стека и отсутствие дублирования полного тела 15 дисциплин).

---

## 3. Детали реализации

### 3.1. Структура Thin Forwarder шаблона в `install.py`

Каждый адаптер формируется по унифицированному компактному каркасу:
```markdown
# {Title} for {Project}

> **Stack:** {Stack Name} | **Language:** {Lang}
> **Canonical Standard (SSOT):** [[AGENTS.md]] | **KB Index:** [[docs/00_Index|00_Index]]

## ⚡ Stack Verification Commands
- **Build:** `{build_cmd}`
- **Test:** `{test_cmd}`
- **Lint:** `python3 scripts/kb_lint.py --path docs`

## 🛡️ Operating Rules & Routing
1. **Single Source of Truth:** Read `AGENTS.md` at session start. All 4 operating modes, skills, and disciplines are governed strictly by `AGENTS.md`.
2. **Read-Only Invariant:** Modes 1 (`/kb-plan`), 2 (`/kb-task`), 2B (`/kb-bug`), 2C (`/kb-triage`) strictly PROHIBIT modifying or creating project code.
3. **Mode 3 Implementation:** `/kb-implement <TASK-XXX | BUG-XXX>` authorizes work strictly on ONE target. Execute TDD for bugs (RED -> GREEN -> REFACTOR). Run verification commands before completion.
4. **Anti-Echo & Single-Task Barrier:** Never reprint full files. Stop tool calls upon task completion (Stop & Yield).
```

### 3.2. Обновление тестов в `tests/test_installer.py`

- Исключить старые ассерты на проверку наличия полной портянки `13. Single-Task Barrier`, `14. Zero-State & Spec Genesis` внутри каждого отдельного адаптера IDE.
- Добавить проверки:
  - Наличие ссылки на `AGENTS.md` в каждом адаптере.
  - Наличие команд сборки, тестирования и линтинга.
  - Наличие ключевых инвариантов (Single-Task Barrier, Read-Only Modes 1/2, Anti-Echo).
  - Сжатие объема адаптеров до $\le 35$ строк.

---

## 4. План верификации (Verification Plan)

- [ ] Синтаксическая проверка: `python -m py_compile install.py` (Exit code 0).
- [ ] Проверка базы знаний: `python scripts/kb_lint.py --path docs -v` (0 broken links, Exit code 0).
- [ ] Тесты инсталлятора: `python -m unittest tests/test_installer.py` (100% Pass, Exit code 0).
- [ ] Полный тестовый сьют: `python -m unittest discover -s tests` (100% Pass, Exit code 0).

---

## 5. Критерии готовности (DoD)

- [ ] Все 6 адаптеров в `install.py` и корне репозитория переведены на паттерн Thin Forwarders.
- [ ] Размер сгенерированных адаптеров составляет не более 35 строк.
- [ ] Отсутствует дублирование 15 дисциплин между `AGENTS.md` и адаптерами.
- [ ] Все тесты из Плана верификации пройдены с кодом 0.
- [ ] Статус задачи обновлен в Канбане (`Done`), ТЗ (`Выполнено`), Дорожной карте (`[x]`).
- [ ] Результаты зафиксированы в `Devlog.md`.
