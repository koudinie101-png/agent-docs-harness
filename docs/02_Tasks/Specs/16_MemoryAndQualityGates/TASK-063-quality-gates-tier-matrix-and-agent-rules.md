---
id: TASK-063
title: "Слои надежности Quality Gates (Tier 1–3) в AGENTS.md и руководстве Onboarding.md"
status: done
type: task
phase: 16
component:
  - rules
  - agents
  - onboarding
  - adapters
parent_plan: "[[../../Plans/PLAN-016-self-improving-harness-and-defect-memory|PLAN-016]]"
created: 2026-10-12
updated: 2026-10-12
tags:
  - task/spec
  - phase16
  - quality-gates
  - agents
  - rules
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-063 — Слои надежности Quality Gates (Tier 1–3) в AGENTS.md и руководстве Onboarding.md

> **ID:** TASK-063 | **Статус:** Выполнено (Режим 3)  
> **План:** [[../../Plans/PLAN-016-self-improving-harness-and-defect-memory|PLAN-016]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Обоснование:** [[../../../04_Research/RESEARCH-020-self-improving-defect-loop-and-quality-gates|RESEARCH-020]], [[../../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]  
> **Первоисточник фидбека:** [[../../Inbox/FB-GH-3|Обращение FB-GH-3 (madpanther)]]

---

## 1. Цель задачи

Устранить иллюзию достаточной регламентации («правило написано в тексте скилла — значит агент его соблюдает») за счет внедрения матрицы слоев надежности **Quality Gates (Tier 1–3)**:
* Закрепить фундаментальный инвариант Quality Gates в каноническом файле правил `AGENTS.md`: критические правила надежности и защиты от дефектов обязаны подниматься в слои принуждения (Tier 1) или Always-On контекста (Tier 2).
* Добавить раздел по слоям надежности и контуру памяти в руководство разработчика и агента `docs/Onboarding.md`.
* Синхронизировать генераторы правил и адаптеров в `install.py` (`_RULES_BODY`, тонкие адаптеры $\le 35$ строк).

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `AGENTS.md` — добавление правила 11 («Quality Gates & Reliability Tiers Invariant») в `Core Rules & Principles`.
* `[MODIFY]` `docs/Onboarding.md` — раздел «Слои надежности Quality Gates (Tier 1–3) и процедурная память».
* `[MODIFY]` `install.py` — обновление правила в `_RULES_BODY` и генерации тонких адаптеров.
* `[MODIFY]` `GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`, `.github/copilot-instructions.md` — синхронизация инварианта Quality Gates в Always-On префиксе.
* `[MODIFY]` `docs/02_Tasks/Kanban.md` — обновление карточки `TASK-063` до постоянной викиссылки на ТЗ.
* `[MODIFY]` `docs/02_Tasks/Roadmap.md` — обновление ссылки `TASK-063` на ТЗ.

---

## 3. Детали реализации

### 3.1. Нормативное правило 11 в `AGENTS.md`
В раздел `### Core Rules & Principles` файла `AGENTS.md` добавляется пункт:
```markdown
11. **Quality Gates & Reliability Tiers Invariant:**
    - Все проектные правила и требования надежности классифицируются по 3 слоям исполнения:
      * **Tier 1 (Enforcement / Принуждение):** Механические барьеры (линтеры `kb_lint.py`, компилятор, юнит/регресс-тесты, CI). Ошибка физически блокирует сборку (Exit code 1).
      * **Tier 2 (Always-On Prompt):** Нормативные инварианты в `AGENTS.md` и системных промптах IDE (100% видимость в каждом диалоговом такте).
      * **Tier 3 (Playbook / On-Demand):** Инструкции скиллов, шаблонов и справочников (вероятностное следование).
    - **Инвариант надежности:** Критическое правило надежности или выявленный систематический дефект категорически запрещено оставлять исключительно в вероятностном слое Tier 3. Правило обязано быть автоматизировано в тесте/линтере (Tier 1) либо вынесено в Always-On префикс (Tier 2).
```

### 3.2. Руководство разработчика `docs/Onboarding.md`
В `Onboarding.md` добавляется наглядная таблица:
```markdown
### 🛡️ Слои надежности Quality Gates (Tier 1–3)

| Слой | Механизм исполнения | Где живет | Надежность |
| :--- | :--- | :--- | :--- |
| **Tier 1 (Enforcement)** | Автоматическая блокировка (Exit code 1) | `scripts/kb_lint.py`, тесты, CI | 🟢 100% (Механическая) |
| **Tier 2 (Always-On)** | Системный контекст (Hot Invariants) | `AGENTS.md`, промпты IDE | 🟡 Высокая (Кэш промпта) |
| **Tier 3 (Playbook)** | Справочные инструкции по требованию | `.agents/skills/`, гайды | 🔴 Вероятностная |
```

### 3.3. Тонкие адаптеры IDE
Адаптеры (`GEMINI.md`, `CLAUDE.md`, `.cursorrules` и др.) дополняются компактной строкой:
```markdown
- **Quality Gates:** Tier 1 (Enforce: tests/lint) > Tier 2 (Always-On: AGENTS.md) > Tier 3 (Playbook: skills). Never rely on Tier 3 for critical rules.
```
Строго контролируется лимит $\le 35$ строк на каждый файл адаптера.

---

## 4. План верификации (Verification Plan)

- [x] Проверка объема адаптеров: ни один файл правил в корне репозитория не превышает 35 строк.
- [x] Линтер базы знаний: `python scripts/kb_lint.py --path docs` возвращает 0 ошибок.
- [x] Юнит-тесты: `python -m unittest tests/test_installer.py` подтверждает корректность генерации адаптеров.

---

## 5. Критерии готовности (DoD)

- [x] Правило 11 зафиксировано в `AGENTS.md`.
- [x] Таблица Quality Gates добавлена в `Onboarding.md`.
- [x] Адаптеры IDE синхронизированы в пределах лимита $\le 35$ строк.
- [x] Все проверки верификации успешно пройдены.
