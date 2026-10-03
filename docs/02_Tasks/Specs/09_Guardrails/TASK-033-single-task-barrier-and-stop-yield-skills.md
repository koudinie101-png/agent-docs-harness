---
id: TASK-033
title: "Нормативный инвариант барьера единичной задачи в AGENTS.md и терминальный шаг Stop & Yield Control в kb-implement и kb-complete"
status: done
type: task
phase: 9
component:
  - agents
  - skills
  - guardrails
parent_plan: "[[../../Plans/PLAN-009-single-task-barrier-and-stop-on-complete|PLAN-009]]"
created: 2026-10-02
updated: 2026-10-03
tags:
  - task/spec
  - phase9
  - agent-governance
  - guardrails
  - single-task-barrier
  - stop-on-complete
  - anti-runaway
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-033 — Нормативный инвариант барьера единичной задачи и терминальный шаг Stop & Yield Control

> **ID:** TASK-033  
> **Статус:** Выполнено (Режим 3)  
> **Теги:** #task/spec #phase9 #agent-governance #guardrails #single-task-barrier #stop-on-complete #anti-runaway  
> **Родительский план:** [[../../Plans/PLAN-009-single-task-barrier-and-stop-on-complete|PLAN-009]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-012-single-task-execution-barrier-and-autonomous-pipeline-containment|RESEARCH-012]], [[../../../03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Внедрить первые два уровня эшелонированной защиты (Defense-in-Depth) против своевольного авто-чейнинга задач (Eager Task Chaining / Autonomous Pipeline Runaway) согласно [[../../../03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]] и [[../../../04_Research/RESEARCH-012-single-task-execution-barrier-and-autonomous-pipeline-containment|RESEARCH-012]]:
1. **Нормативный инвариант в `AGENTS.md`:** Закрепить жесткий запрет авто-перехода между задачами: команда `/kb-implement <TASK-XXX>` авторизует реализацию строго одной задачи.
2. **Терминальный шаг `Stop & Yield Control` в `kb-implement` и `kb-complete`:** Обязать агента принудительно прекращать любые вызовы инструментов (Tool Calls) сразу после фиксации коммита задачи, выводить Anti-Echo резюме и передавать управление человеку.
3. **Семантический формат в `kb-complete`:** Закрепить формирование записи Devlog в виде `- **Рекомендуемый следующий шаг (Ожидает команды пользователя):** \`/kb-implement TASK-YYY\`.`

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `AGENTS.md` — добавление инварианта `Single-Task Execution Barrier (No Auto-Chaining)` и шага остановки в чеклист Mode 3.
* `[MODIFY]` `.agents/skills/kb-implement/SKILL.md` — ограничение `Single-Task Barrier` и шаг остановки после вызова completion.
* `[MODIFY]` `.agents/skills/kb-complete/SKILL.md` — семантический формат шага Devlog и шаг 9 `Terminal Step: Stop & Yield Control`.

---

## 3. Детали реализации

### 3.1. Инвариант в `AGENTS.md`
В раздел `Core Rules & Principles` добавляется правило 5:
```markdown
5. **Single-Task Execution Barrier (No Auto-Chaining):**
   - The command `/kb-implement <TASK-XXX>` authorizes work **strictly on that single task specification**.
   - Even if subsequent tasks are listed in plans, backlog, or Devlog, the agent is **strictly prohibited** from starting their implementation without an explicit user command (e.g. `/kb-implement TASK-YYY`).
   - "Next Step" sections in devlogs, plans, and summaries are developer guidance only and are **never** an execution mandate for the agent.
   - Once task verification and commit are complete, the agent must **cease all tool calls immediately** and return control to the user.
```

В чеклист `### 🟢 Mode 3: Implementation & Verification` добавляется терминальный шаг:
```markdown
9. **Terminal Step (Stop & Yield):** Output Anti-Echo response, suggest next command to user, and strictly STOP tool calls. Wait for user command.
```

### 3.2. Ограничения и остановка в `.agents/skills/kb-implement/SKILL.md`
В `## 🚨 Constraints`:
```markdown
* **Single-Task Barrier:** Execute strictly ONE approved task. Never auto-chain to subsequent tasks without an explicit user command.
```

В `## Procedure` обновляется шаг 5:
```markdown
5. **Immediate Auto-Completion & Stop:**
   - Upon all checks passing (Exit code 0), immediately execute `/kb-complete <TASK-XXX>` to finalize the task without waiting for user input.
   - Once kb-complete finishes, strictly STOP calling tools and yield control to the user.
```

### 3.3. Терминальный шаг и семантический Devlog в `.agents/skills/kb-complete/SKILL.md`
В `## 🚨 Constraints`:
```markdown
* **Single-Task Barrier:** Finalize only the specified task. Do not begin or execute subsequent tasks.
```

В `## Procedure` шаг 4 обновляется:
```markdown
4. **Append Devlog:**
   - In `docs/Devlog.md`: record summary of changes, test verification results, and recommended next step using semantic format:
     `- **Рекомендуемый следующий шаг (Ожидает команды пользователя):** \`/kb-implement TASK-YYY\`.`
```

Добавляется шаг 9:
```markdown
9. **Terminal Step: Stop & Yield Control:**
   - Render concise Anti-Echo summary (`[FileName](file://...)`, 3–5 bullets).
   - Propose next command to user (e.g. `/kb-implement TASK-YYY` or `/kb-release`).
   - STRICTLY STOP calling tools. Yield control to user and wait for explicit prompt.
```

---

## 4. План верификации (Verification Plan)

- [x] Целостность базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links, Exit code 0).
- [x] Аудит High-SNR компактности: размеры `kb-implement/SKILL.md` (32 строки) и `kb-complete/SKILL.md` (37 строк) остаются компактными (до 35–40 строк).
- [x] Проверка наличия инварианта в `AGENTS.md` и терминов `Stop & Yield Control` в обоих скиллах.

---

## 5. Критерии готовности (DoD)

- [x] Правило Single-Task Execution Barrier внесено в `AGENTS.md`.
- [x] Скилл `kb-implement` содержит ограничение на одну задачу и предписание остановки.
- [x] Скилл `kb-complete` содержит семантический формат записи в Devlog и шаг 9 `Stop & Yield Control`.
- [x] Все пункты Плана верификации пройдены.
- [x] Статус обновлен в ТЗ, Канбане и Roadmap.
- [x] Запись сессии внесена в `Devlog.md`.
