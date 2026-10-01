---
id: TASK-021
title: "Эволюция скилла kb-research: валидация продуктово-архитектурных гипотез и двухпутевая воронка регистрации в Roadmap"
status: in-progress
type: task
phase: 6
component:
  - skills
  - discovery
  - kb-research
  - roadmap
parent_plan: "[[../../Plans/PLAN-006-discovery-mode-and-kb-research-lifecycle|PLAN-006]]"
created: 2026-10-01
updated: 2026-10-01
tags:
  - task/spec
  - phase6
  - component/skills
  - component/discovery
  - component/kb-research
  - component/roadmap
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-021 — Эволюция скилла kb-research

> **ID:** TASK-021  
> **Статус:** В работе (Режим 2)  
> **Теги:** #task/spec #phase6 #component/skills #component/discovery #component/kb-research #component/roadmap  
> **Родительский план:** [[../../Plans/PLAN-006-discovery-mode-and-kb-research-lifecycle|PLAN-006]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-007-discovery-mode-and-kb-research-lifecycle-integration|RESEARCH-007]], [[../../../03_Decisions_ADR/ADR-0012-discovery-mode-and-kb-research-lifecycle-integration|ADR-0012]], [[../../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Трансформировать скилл `.agents/skills/kb-research/SKILL.md` в основной инструмент **Режима 0 (Discovery & Feasibility)** жизненного цикла Docs-as-Code согласно стандарту [[../../../03_Decisions_ADR/ADR-0012-discovery-mode-and-kb-research-lifecycle-integration|ADR-0012]]:
1. **Расширение области применения:** Сделать скилл точкой входа для валидации любых пользовательских продуктовых идей, архитектурных гипотез и предложений фичей (а не только узких дефектов платформ).
2. **Критическое стресс-тестирование:** Закрепить за агентом роль Senior Partner — обязательную фальсификацию гипотез, анализ компромиссов (Trade-off Matrix) и рисков (Zero-Deps, токеномика, кроссплатформенность).
3. **Двухпутевая автоматическая воронка интеграции с `Roadmap.md` (Outcome Routing):**
   - *При валидации идеи:* Оформление `RESEARCH-XXX` (+ `ADR-XXXX` при архитектурном влиянии) и автоматическая регистрация в `Roadmap.md` в секции `## 🔮 Перспективные направления (Future Horizons / Icebox)` с оценкой ценности (Value Impact).
   - *При отклонении идеи:* Оформление отказного ADR (`status: rejected`) через `/kb-adr` и автоматическая регистрация в секции `## 🚫 Отклоненные архитектурные идеи (Rejected Alternatives)` с фиксацией обоснования.
4. **Соблюдение High-SNR токеномики:** Сохранить лаконичность frontmatter (`description` $\le$ 15 слов) и четкую императивную структуру согласно [[../../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]].

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `.agents/skills/kb-research/SKILL.md` — обновление frontmatter, расширение назначений, внедрение процедур критического партнерства и двухпутевой маршрутизации в `Roadmap.md`.

---

## 3. Детали реализации

### Контракт файла `.agents/skills/kb-research/SKILL.md`

Обновленная структура скилла должна строго соответствовать High-SNR стандарту:

```markdown
---
name: kb-research
description: "Mode 0: Validate ideas & hypotheses (RESEARCH-XXX), stress-test risks, register in Roadmap Icebox or reject."
---

# /kb-research — Mode 0: Discovery & Feasibility Research

Use when validating new ideas, testing technical hypotheses, exploring architectural trade-offs, or investigating platform pitfalls.

## 🚨 Constraints
* **Critical Partner & Falsification:** Stress-test proposals against platform limits: OS lifecycle, Zero-Deps (ADR-0001), token economy (ADR-0009), performance, and security. Actively try to falsify assumptions.
* **Preserve Dead Ends:** Explicitly document unviable alternatives and rejected prototypes to prevent recurring mistakes.

## Procedure
1. **Calculate ID:** Scan `docs/04_Research/` for the next available `RESEARCH-XXX`.
2. **Stress-Test & Measure:** Prototype minimally, measure limits, identify trade-offs, evaluate Value vs Effort.
3. **Draft Research Note:** Create `docs/04_Research/RESEARCH-XXX-<slug>.md` using `docs/00_Templates/TEMPLATE_RESEARCH.md` (Context, Hypotheses, Trade-off Matrix, Discarded Options, Conclusions).
4. **Automated Outcome Routing:**
   - **Validated & Approved:**
     - If architectural impact: invoke `/kb-adr` to record accepted `ADR-XXXX`.
     - Register validated initiative in `## 🔮 Перспективные направления (Future Horizons / Icebox)` in `docs/02_Tasks/Roadmap.md` with wikilinks and Value Impact rating.
   - **Unviable / Overengineered (Rejected):**
     - Invoke `/kb-adr` to record rejected ADR (`status: rejected`).
     - Register entry in `## 🚫 Отклоненные архитектурные идеи (Rejected Alternatives)` in `docs/02_Tasks/Roadmap.md` with link to ADR.
5. **Index & Git Sync:**
   - Link research note in `docs/00_Index.md` (section 4: Исследования).
   - Git commit: `git add docs/04_Research/ docs/02_Tasks/Roadmap.md docs/03_Decisions_ADR/ docs/00_Index.md && git commit -m "docs(research): add RESEARCH-XXX <slug>"`. Push if remote origin exists.
```

---

## 4. План верификации (Verification Plan)

- [ ] Frontmatter Check: поле `description` содержит не более 15 слов и четко указывает на Режим 0 (Discovery) и регистрацию в Icebox / отказные ADR.
- [ ] Procedure Validation: в процедуре четко описаны обе ветки воронки (валидированная идея $\to$ Icebox; отклоненная $\to$ отказной ADR в Rejected Alternatives).
- [ ] Аудит базы знаний: запуск `python scripts/kb_lint.py --path docs` завершается с `Exit code 0` и 0 битых ссылок.

---

## 5. Критерии готовности (DoD)

- [ ] Текст `.agents/skills/kb-research/SKILL.md` обновлен в строгом соответствии с контрактом.
- [ ] Все пункты Плана верификации успешно выполнены.
- [ ] Статус задачи обновлен в `TASK-021.md` (`done`), Канбане (`## ✅ Готово`) и Дорожной карте (`[x]`).
- [ ] Запись о завершении добавлена в `docs/Devlog.md`.
