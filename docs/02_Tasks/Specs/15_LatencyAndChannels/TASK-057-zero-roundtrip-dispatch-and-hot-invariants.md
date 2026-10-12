---
id: TASK-057
title: "Архитектура Zero Round-Trip Dispatch и горячие инварианты в правилах агентов"
status: done
type: task
phase: 15
component:
  - rules
  - adapters
  - installer
parent_plan: "[[../../Plans/PLAN-015-response-latency-and-channel-transparency|PLAN-015]]"
created: 2026-10-12
updated: 2026-10-12
tags:
  - task/spec
  - phase15
  - latency
  - dispatch
  - rules
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-057 — Архитектура Zero Round-Trip Dispatch и горячие инварианты в правилах агентов

> **ID:** TASK-057 | **Статус:** Выполнено (Режим 3)  
> **План:** [[../../Plans/PLAN-015-response-latency-and-channel-transparency|PLAN-015]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Обоснование:** [[../../../04_Research/RESEARCH-008-latency-prompt-caching-and-skill-chaining|RESEARCH-008]], [[../../../03_Decisions_ADR/ADR-0013-zero-roundtrip-dispatch-and-hot-invariants-architecture|ADR-0013]]  

---

## 1. Цель задачи

Устранить задержку двухтактного исполнения (Two-Turn Latency Penalty, 6–12 с) в Antigravity и других агентных средах за счет формализации архитектуры **Zero Round-Trip Dispatch (Hot Invariants)**:
* Наделить агента нормативным правом выполнять типовые команды жизненного цикла Режимов 0–3 (`/kb-plan`, `/kb-task`, `/kb-implement`, `/kb-bug`, `/kb-triage`) в первом же диалоговом такте без промежуточного tool call `view_file(path/to/SKILL.md)`, опираясь на постоянный Always-On префикс `AGENTS.md` (100% Cache Hit в сервере).
* Закрепить протокол параллельного чтения сопутствующего контекста (**Pipelined Co-fetching**): если агенту объективно требуется прочитать файл шаблона или заметки, он объединяет запросы в один первый такт вместо последовательной цепочки вызовов.
* Сохранить On-Demand Progressive Disclosure для тяжелых процедур (`/kb-release`, `/kb-lint`, `/kb-init`).
* Обновить базовый стандарт `AGENTS.md`, генератор правил `install.py` (`_RULES_BODY`, `generate_agents_md`, `_gen_rule`) и все 6 тонких адаптеров IDE при строгом сохранении лимита $\le 35$ строк.

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `AGENTS.md` — внедрение правила 10 («Zero Round-Trip Dispatch & Hot Invariants Protocol») в базовый стандарт.
* `[MODIFY]` `install.py` — обновление правила 18 в `_RULES_BODY`, генератора `generate_agents_md` и директивы Zero Round-Trip в `_gen_rule`.
* `[MODIFY]` `GEMINI.md` — закрепление директивы прямого исполнения в Always-On префиксе.
* `[MODIFY]` `CLAUDE.md` — синхронизация правил тонкого адаптера.
* `[MODIFY]` `.cursorrules` — синхронизация правил тонкого адаптера.
* `[MODIFY]` `.windsurfrules` — синхронизация правил тонкого адаптера.
* `[MODIFY]` `.clinerules` — синхронизация правил тонкого адаптера.
* `[MODIFY]` `.github/copilot-instructions.md` — синхронизация правил тонкого адаптера.
* `[MODIFY]` `tests/test_installer.py` — расширение теста `test_25_thin_forwarders_rules_layering` для проверки директивы Zero Round-Trip.
* `[MODIFY]` `docs/02_Tasks/Kanban.md` — перевод задачи в `## ⏳ В работе (In Progress)`.
* `[MODIFY]` `docs/02_Tasks/Roadmap.md` — превращение `TASK-057` в постоянную викиссылку на ТЗ.

---

## 3. Детали реализации

### 3.1. Нормативное правило 10 в `AGENTS.md`
В раздел `### Core Rules & Principles` файла `AGENTS.md` добавляется пункт:

```markdown
10. **Zero Round-Trip Dispatch & Hot Invariants Protocol:**
    - For standard lifecycle modes (Modes 0, 1, 2, 2B, 2C, 3) and direct agent slash-commands, agents are explicitly authorized to execute directly in the first turn from the Always-On prefix (`AGENTS.md`) without an intermediary `view_file` call to `.agents/skills/<skill>/SKILL.md`.
    - **Pipelined Co-fetching:** when an operation genuinely requires reading a template or reference note, the agent must bundle all necessary context read requests into that same first tool-call turn rather than chaining sequential read steps.
    - Specialized procedural skills (`/kb-release`, `/kb-lint`, `/kb-init`) remain strictly On-Demand via Progressive Disclosure.
```

### 3.2. Обновление `_RULES_BODY` и тонких адаптеров в `install.py`
В строковую константу `_RULES_BODY` добавляется правило 18:
```python
"18. Zero Round-Trip Dispatch: For standard Modes 0-3, execute directly from Always-On AGENTS.md in the 1st turn without view_file(SKILL.md); co-fetch context in parallel.\n"
```

В генераторе тонких адаптеров `_gen_rule` обновляется пункт 1 операционных правил:
```python
"1. **Single Source of Truth & Zero Round-Trip:** Read AGENTS.md at session start. For Modes 0-3, execute directly from hot prefix without reading SKILL.md; co-fetch context in parallel.\n"
```
*Требование жесткого лимита:* Размер каждого сгенерированного файла адаптера обязан оставаться $\le 35$ строк.

### 3.3. Тестовый контракт в `tests/test_installer.py`
В метод `test_25_thin_forwarders_rules_layering` добавляется проверка:
```python
self.assertIn("Zero Round-Trip", out)
```
И проверка непревышения лимита $\le 35$ строк для всех адаптеров.

---

## 4. План верификации (Verification Plan)

- [ ] Синтаксическая валидация:  
  `python -m py_compile install.py` (Exit code 0).
- [ ] Модульное тестирование тонких адаптеров:  
  `python -m unittest tests/test_installer.py -k test_25` (100% Pass, Exit code 0).
- [ ] Полный регрессионный тест инсталлятора:  
  `python -m unittest tests/test_installer.py` (28/28 Pass, Exit code 0).
- [ ] Аудит целостности базы знаний:  
  `python scripts/kb_lint.py --path docs` (0 broken links, Exit code 0).

---

## 5. Критерии готовности (DoD)

- [ ] Правило 10 зафиксировано в `AGENTS.md`.
- [ ] `install.py` (`_RULES_BODY`, `_gen_rule`) и все 6 адаптеров обновлены и соответствуют лимиту $\le 35$ строк.
- [ ] Тесты `tests/test_installer.py` успешно проходят.
- [ ] `kb_lint.py` подтверждает 0 сломанных ссылок.
- [ ] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [ ] Запись добавлена в `docs/Devlog.md`.
