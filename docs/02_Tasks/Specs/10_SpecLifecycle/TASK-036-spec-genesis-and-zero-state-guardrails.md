---
id: TASK-036
title: "Spec Genesis Protocol & Zero-State Guardrails (kb-init, kb-plan, kb-task, AGENTS.md)"
status: in-progress
type: task
phase: 10
component:
  - agents
  - skills
  - spec-genesis
parent_plan: "[[../../Plans/PLAN-010-spec-genesis-and-high-snr-release-notes|PLAN-010]]"
created: 2026-10-03
updated: 2026-10-03
tags:
  - task/spec
  - phase10
  - spec-genesis
  - master-spec
  - zero-state
  - guardrails
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-036 — Spec Genesis Protocol & Zero-State Guardrails

> **ID:** TASK-036  
> **Статус:** В работе (Режим 2)  
> **Теги:** #task/spec #phase10 #spec-genesis #master-spec #zero-state #guardrails  
> **Родительский план:** [[../../Plans/PLAN-010-spec-genesis-and-high-snr-release-notes|PLAN-010]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-011-spec-genesis-protocol-and-zero-state-handling|RESEARCH-011]], [[../../../03_Decisions_ADR/ADR-0018-spec-genesis-protocol-and-zero-state-handling|ADR-0018]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Реализовать входной шлюз методологии Docs-as-Code — **Протокол рождения Мастер-Спецификации (Spec Genesis)** и защиту от галлюцинаций в пустом состоянии (**Zero-State Anti-Hallucination Guardrails**) согласно [[../../../03_Decisions_ADR/ADR-0018-spec-genesis-protocol-and-zero-state-handling|ADR-0018]] и [[../../../04_Research/RESEARCH-011-spec-genesis-protocol-and-zero-state-handling|RESEARCH-011]]:
1. **Устранение пробела в `kb-init`:** при инициализации через скилл `.agents/skills/kb-init/SKILL.md` гарантировать развертывание каркаса `SPEC.md` со статусом `status: discovery` (паритет с `install.py`).
2. **Префлайт-чеки в `kb-plan` и `kb-task`:** внедрить мягкое предупреждение (Soft Nudge), если `SPEC.md` отсутствует или находится в `status: discovery`, предлагая провести Режим 0 (`/kb-research`) для выбора стека и кристаллизации спецификации (`status: active`).
3. **Нормативный инвариант в `AGENTS.md`:** зафиксировать запрет на директивное выдумывание функционала и стека агентом при отсутствии явного диалога с пользователем.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `.agents/skills/kb-init/SKILL.md` — добавить создание стартового `SPEC.md` (`status: discovery`) из шаблона `TEMPLATE_SPEC.md`.
* `[MODIFY]` `.agents/skills/kb-plan/SKILL.md` — добавить префлайт-проверку статуса `SPEC.md` (Zero-State / discovery guard) в Procedure (шаг 1).
* `[MODIFY]` `.agents/skills/kb-task/SKILL.md` — добавить валидацию зрелости спецификации перед нарезкой ТЗ.
* `[MODIFY]` `AGENTS.md` — зафиксировать инвариант `6. Zero-State Anti-Hallucination & Spec Genesis Protocol` в `Core Rules & Principles`.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_SPEC.md` и `templates/TEMPLATE_SPEC.md` — уточнить инструкции перехода `discovery` -> `active`.

---

## 3. Детали реализации

### 3.1. Генерация `SPEC.md` в `.agents/skills/kb-init/SKILL.md`
В шаги инициализации добавляется создание корневого файла спецификации `SPEC.md`:
```markdown
- Create root `SPEC.md` using `docs/00_Templates/TEMPLATE_SPEC.md` with frontmatter `status: discovery` if it does not already exist.
```

### 3.2. Префлайт-чеки в `.agents/skills/kb-plan/SKILL.md`
В раздел `Procedure -> 1. Source Discovery & Intent Routing`:
```markdown
- **Spec Genesis Check (Zero-State Guard):** If `SPEC.md` is missing or has `status: discovery`, display a Soft Nudge:
  "⚠️ Master Specification (SPEC.md) is currently in 'discovery' status. Recommended: run `/kb-research <topic>` (Mode 0) to validate the architectural stack and crystallize SPEC.md before deep planning, or confirm to proceed directly."
```

### 3.3. Валидация в `.agents/skills/kb-task/SKILL.md`
В раздел `Procedure`:
```markdown
- **Spec Status Check:** Verify `SPEC.md` is not in `status: discovery`. If it is, issue a warning that task specs should align with an active Master Spec.
```

### 3.4. Инвариант в `AGENTS.md`
В раздел `Core Rules & Principles`:
```markdown
6. **Zero-State Anti-Hallucination & Spec Genesis:** When `SPEC.md` is missing or in `status: discovery`, the agent is strictly prohibited from inventing arbitrary product requirements or technology stacks out of thin air. Requirements must be discovered through interactive dialogue or Mode 0 (`/kb-research`).
```

---

## 4. План верификации (Verification Plan)

- [ ] Статический аудит: проверить наличие префлайт-чеков в `kb-init`, `kb-plan`, `kb-task` и `AGENTS.md`.
- [ ] Линтер базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links, 0 warnings, Exit code 0).
- [ ] Юнит-тесты: `python -m unittest discover -s tests` (100% Pass, Exit code 0).

---

## 5. Критерии готовности (DoD)

- [ ] Скилл `kb-init` создает `SPEC.md` (`status: discovery`).
- [ ] Скиллы `kb-plan` и `kb-task` содержат правила Zero-State гейткипинга.
- [ ] `AGENTS.md` содержит инвариант Zero-State Anti-Hallucination.
- [ ] Линтер `kb_lint.py` проходит без ошибок.
- [ ] Статус обновлен в ТЗ, Канбане и Дорожной карте.
