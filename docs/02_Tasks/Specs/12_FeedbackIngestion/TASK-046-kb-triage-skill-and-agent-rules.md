---
id: TASK-046
title: "Исполняемый скилл /kb-triage и интеграция в правила агентов"
status: in-progress
type: task
phase: 12
component:
  - skills
  - triage
  - agent-rules
parent_plan: "[[../../Plans/PLAN-012-feedback-ingestion-and-triage-buffer|PLAN-012]]"
created: 2026-10-11
updated: 2026-10-11
tags:
  - task/spec
  - phase12
  - skills
  - triage
  - heuristics
  - agent-rules
  - stop-yield
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-046 — Исполняемый скилл /kb-triage и интеграция в правила агентов

> **ID:** TASK-046  
> **Статус:** В работе (Режим 2)  
> **Теги:** #task/spec #phase12 #skills #triage #heuristics #agent-rules #stop-yield  
> **Родительский план:** [[../../Plans/PLAN-012-feedback-ingestion-and-triage-buffer|PLAN-012]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-015-feedback-ingestion-channels-and-triage-heuristics|RESEARCH-015]], [[../../../03_Decisions_ADR/ADR-0020-feedback-ingestion-channels-and-triage-automation|ADR-0020]], [[../../../03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]], [[../../../03_Decisions_ADR/ADR-0019-bug-lifecycle-triage-and-release-targeting|ADR-0019]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Создать специализированный интерактивный инструмент триажа входящей обратной связи:
1. **Исполняемый скилл `.agents/skills/kb-triage/SKILL.md`:** Реализовать двухстадийную процедуру обработки:
   - Входной скрининг обращений в `docs/02_Tasks/Inbox/` (сортировка по типу, оценка воспринимаемой критичности).
   - Интерактивная конвертация в целевой артефакт: дефекты $\to$ `/kb-bug` (`BUG-XXX`), идеи $\to$ `Roadmap.md (Icebox)`, вопросы $\to$ обновление FAQ/Onboarding.
   - Обновление статуса в исходном файле (`status: processed` / `status: rejected`) без удаления или перемещения файла (Permalinks Invariant).
   - Терминальный шаг **Stop & Yield Control** для предотвращения несанкционированного кодирования.
2. **Кросс-агентные правила и адаптеры:** Актуализировать матрицу правил в `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`, включив скилл `/kb-triage` и дисциплину буфера триажа.

---

## 2. Затрагиваемые файлы и компоненты

* `[NEW]` `.agents/skills/kb-triage/SKILL.md` — новый скилл триажа входящих сообщений.
* `[MODIFY]` `AGENTS.md` — регистрация скилла `/kb-triage`, регламент обработки буфера `Inbox/` и Permalinks Invariant.
* `[MODIFY]` `GEMINI.md` — синхронизация правил для Google Antigravity / Gemini.
* `[MODIFY]` `CLAUDE.md` — синхронизация правил для Claude Code CLI.
* `[MODIFY]` `.cursorrules`, `.windsurfrules`, `.clinerules` — обновление правил целевых редакторов.

---

## 3. Детали реализации

### 3.1. Спецификация скилла `kb-triage/SKILL.md`
```markdown
---
name: kb-triage
description: "Interactive triage of incoming feedback from Inbox/ with Stop & Yield. Prohibits code changes."
---

# /kb-triage — Mode 2C: Feedback Triage & Dispatch

## Constraints
* READ-ONLY: Direct modification of codebase is STRICTLY PROHIBITED.
* Permalinks Invariant: Never delete or move FB-*.md files. Update status and target in-place.
* Stop & Yield: Stop tool execution immediately after triage.

## Workflow
1. Ingest / Check:
   - Run `python scripts/kb_ingest.py` (or parse pasted text).
   - Scan `docs/02_Tasks/Inbox/` for files with `status: new`.
2. Interactive Screening (per item):
   - Categorize: Defect | Feature Request | Question | Invalid.
   - If Defect: Trigger or advise `/kb-bug` to create `BUG-XXX`.
   - If Feature: Register in `docs/02_Tasks/Roadmap.md` (Icebox) with permanent link to `FB-*.md`.
   - If Question: Prepare answer or suggest update to `docs/Onboarding.md`.
3. Update Frontmatter:
   - Set `status: processed`, `updated: <date>`, `target: "[[../Bugs/BUG-XXX]]"` (или `target: "[[../Roadmap#Icebox]]"`).
4. Git Commit & Stop:
   - `git add docs/02_Tasks/Inbox/ docs/02_Tasks/Roadmap.md`
   - `git commit -m "docs(inbox): triage feedback FB-XXX to <target>"`
   - Stop and yield control to user.
```

### 3.2. Обновление правил в `AGENTS.md`
Добавить раздел «Регламент входящей обратной связи и буфера триажа»:
- Запрет создания задач и багов напрямую из неструктурированных входящих сообщений без прохождения `Inbox/` или `/kb-triage`.
- Правило неизменяемости файлов `FB-*.md`.

---

## 4. План верификации (Verification Plan)

- [ ] Проверка синтаксиса и структуры скилла `kb-triage`:
  ```bash
  python scripts/kb_lint.py --path docs
  ```
- [ ] Ручная проверка правил в `AGENTS.md` и адаптерах на соответствие принципам High-SNR и Single-Task Barrier.

---

## 5. Критерии готовности (DoD)

- [ ] Скилл `.agents/skills/kb-triage/SKILL.md` создан в строгом соответствии с High-SNR стандартом.
- [ ] Во всех файлах правил (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`) зарегистрирован `/kb-triage`.
- [ ] Закреплены терминальный шаг Stop & Yield и Permalinks Invariant для обращений.
