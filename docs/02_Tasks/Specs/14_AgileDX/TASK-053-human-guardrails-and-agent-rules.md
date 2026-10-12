---
id: TASK-053
title: "Принцип «Направляй, а не блокируй» (Human Guardrails) в AGENTS.md и адаптерах"
status: done
type: task
phase: 14
component:
  - rules
  - agents
  - installer
parent_plan: "[[../../Plans/PLAN-014-agile-docs-as-code-and-chat-first-dx|PLAN-014]]"
created: 2026-10-12
updated: 2026-10-12
tags:
  - task/spec
  - phase14
  - rules
  - human-guardrails
  - agents
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-053 — Принцип «Направляй, а не блокируй» (Human Guardrails) в AGENTS.md и адаптерах

> **ID:** TASK-053 | **Статус:** Выполнено (Режим 3)  
> **План:** [[../../Plans/PLAN-014-agile-docs-as-code-and-chat-first-dx|PLAN-014]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0022-chat-first-vibe-coder-dx-and-human-guardrails|ADR-0022]], [[../../../03_Decisions_ADR/ADR-0023-fast-track-protocol-for-micro-tasks|ADR-0023]]

---

## 1. Цель задачи
Устранить эффект «диалогового шлагбаума», когда агент блокирует нетехнического пользователя сухими системными запретами (`🚨 NO CODE EDITS`). Закрепить в [AGENTS.md](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/AGENTS.md) и тонких адаптерах инсталлятора [install.py](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/install.py) принцип **«Направляй, а не блокируй» (Human Guardrails)**, нормативные рамки протокола **Fast-Track** и директивы **Chat-First Bootstrapping**.

---

## 2. Затрагиваемые файлы
* `[MODIFY]` `AGENTS.md` — включение принципа Human Guardrails, регламента Fast-Track Protocol и руководства по диалоговому менторству.
* `[MODIFY]` `install.py` — обновление функций генерации тонких адаптеров (`generate_gemini_md`, `generate_windsurfrules`, `generate_clinerules`, `generate_claude_md`, `generate_cursorrules`, `generate_copilot_instructions`).
* `[MODIFY]` `tests/test_installer.py` — проверка наличия ссылок на Human Guardrails и Fast-Track в сгенерированных адаптерах.

---

## 3. Детали реализации

### 3.1. Обновление `AGENTS.md`
1. **Принцип «Направляй, а не блокируй» (Human Guardrails Protocol):**
   * При остановке в Режимах 1 (`/kb-plan`), 2 (`/kb-task`), 2B (`/kb-bug`), 2C (`/kb-triage`) агенту **запрещено** выдавать сухие машинные отказы («Редактирование кода запрещено, утвердите спеку»).
   * Агент обязан действовать как дружелюбный Senior Partner:
     - Кратко объяснить суть текущего этапа на понятном языке;
     - Сформулировать 1–2 понятных уточняющих вопроса или предложить готовые варианты выбора (A / B);
     - Предложить точную следующую команду (например: *«Если всё верно, напиши `/kb-implement TASK-XXX`, и я приступлю к коду»*).
2. **Нормативный протокол Fast-Track (Micro-Task Bypass):**
   * Разрешить старт задачи напрямую с Режима 2 (`/kb-task --fast` или по подтверждению пользователя) при соблюдении лимитов:
     - Объем изменений: $\le 30$ строк кода;
     - Количество файлов: $\le 2$;
     - Нулевой архитектурный риск (запрет правок `SPEC.md`, `AGENTS.md`, запрет внешних зависимостей).
   * Сохранить обязательный шаг **Stop & Yield Control** после формирования Micro-Spec.

### 3.2. Обновление тонких адаптеров в `install.py`
В блоке ключевых инвариантов каждого адаптера зафиксировать лаконичную директиву:
```text
- Guided Guardrails: In read-only modes (1, 2, 2B, 2C), guide the user with clear next-step options instead of raw blocking errors.
- Fast-Track Protocol: Tasks <= 30 LOC and <= 2 files bypass Mode 1 via /kb-task --fast with Micro-Spec.
```

---

## 4. План верификации (Verification Plan)
- [ ] Синтаксис Python: `python -m py_compile install.py` (Exit code 0).
- [ ] Тесты инсталлятора: `python -m unittest tests/test_installer.py` (100% Pass).
- [ ] Аудит базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links).

---

## 5. Критерии готовности (DoD)
- [ ] В `AGENTS.md` закреплены протокол Human Guardrails и правила Fast-Track.
- [ ] Все 6 адаптеров IDE в `install.py` содержат обновленные директивы.
- [ ] Тесты `tests/test_installer.py` адаптированы и успешно проходят.
- [ ] Все проверки верификации завершены с кодом 0.
