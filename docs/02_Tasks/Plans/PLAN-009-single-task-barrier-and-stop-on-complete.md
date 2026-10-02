---
id: PLAN-009
title: "Фаза 9: Барьер единичной задачи и протокол гарантированной остановки (Single-Task Execution Barrier & Stop-on-Complete Protocol)"
status: accepted
type: plan
phase: 9
created: 2026-10-02
updated: 2026-10-02
tags:
  - plan
  - phase9
  - agent-governance
  - guardrails
  - single-task-barrier
  - stop-on-complete
  - anti-runaway
  - docs-as-code
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 📋 План: PLAN-009 — Фаза 9: Барьер единичной задачи и протокол гарантированной остановки (Single-Task Execution Barrier)

> **ID:** PLAN-009  
> **Статус:** Согласовано (Режим 1)  
> **Теги:** #plan #phase9 #agent-governance #guardrails #single-task-barrier #stop-on-complete #anti-runaway #docs-as-code  
> **Родительская спецификация:** [[../../SPEC|SPEC.md]]  
> **Канбан:** [[../Kanban|Канбан-доска]]  
> **Связанные исследования и ADR:** [[../../04_Research/RESEARCH-012-single-task-execution-barrier-and-autonomous-pipeline-containment|RESEARCH-012: Барьер единичной задачи и сдерживание конвейерного перевыполнения]], [[../../03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016: Барьер единичной задачи и протокол гарантированной остановки]], [[../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009: High-SNR токеномика]], [[../../03_Decisions_ADR/ADR-0014-greenfield-idea-first-initialization-and-living-spec-protocol|ADR-0014: Living Spec]]

---

## 1. Контекст и цели (Problem & Goals)

### Проблема
В ходе разработки с участием AI-агентов выявлен дефект **«Eager Task Chaining / Autonomous Pipeline Runaway»**: при сжатии контекста (`<CONTEXT_SUMMARY>`) директивные ограничения сессии утрачиваются, а блок «Следующие шаги» воспринимается моделью как активная очередь исполнения. Агент завершает одну задачу и неконтролируемо переходит к последующим задачам без ведома и разрешения пользователя, нарушая принцип Human-in-the-Loop.

### Цели Фазы 9
В соответствии с [[../../03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]] и [[../../04_Research/RESEARCH-012-single-task-execution-barrier-and-autonomous-pipeline-containment|RESEARCH-012]]:
1. Закрепить нормативный инвариант **Single-Task Execution Barrier (No Auto-Chaining)** в `AGENTS.md` и генераторах правил агентов в `install.py`.
2. Внедрить терминальный шаг **Stop & Yield Control** в скиллы `kb-implement` и `kb-complete`, предписывающий агенту принудительно прекращать вызовы инструментов (Tool Calls) после коммита текущей задачи.
3. Разрешить семантическую двусмысленность субъекта в `Devlog.md` и шаблоне `TEMPLATE_DEVLOG.md`: заменить триггерный заголовок `- **Следующий шаг:**` на `- **Рекомендуемый следующий шаг (Ожидает команды пользователя):** \`/kb-implement TASK-XXX\`.`
4. Реализовать неблокирующий эвристический аудит в `scripts/kb_lint.py` (`check_devlog_semantic_guard`) и модульные тесты в `tests/test_kb_lint.py`.
5. Синхронизировать ресурсы инсталлятора `build_installer.py` / `install.py` (включая `--update`), покрыть сквозными тестами в `tests/test_installer.py` и актуализировать `README.md` и `docs/Onboarding.md`.

---

## 2. Обсуждение и решения (Q&A / Discussion)

* **Q1: Почему недостаточно просто просить агента в промпте «сделай только задачу N»?**
  * **Решение:** При контекстной суммаризации пользовательский промпт сжимается или замещается блоком `<CONTEXT_SUMMARY>`, в котором следующий шаг описан в нейтрально-побудительном залоге. Необходима эшелонированная защита (правила + скиллы + шаблон Devlog + линтер).
* **Q2: Должен ли линтер `kb_lint.py` блокировать CI при нарушении формулировки в Devlog?**
  * **Решение:** Нет. Согласно принципу Friendly DX, несоответствие семантическому стандарту генерирует **неблокирующее предупреждение (Warning)** с кодом возврата `0`.
* **Q3: Как обновление затронет существующие репозитории при `install.py --update`?**
  * **Решение:** Обновляются только инфраструктурные файлы: `.agents/skills/`, шаблоны `docs/00_Templates/`, `scripts/` и корневые правила `AGENTS.md`. Пользовательский `Devlog.md` не перезаписывается, но начинает проверяться линтером на предупреждения.

---

## 3. Архитектурное влияние и риски (Architectural Impact & Risks)

* **Затрагиваемые компоненты:**
  * `AGENTS.md` — новый инвариант в блоке Core Rules.
  * `.agents/skills/kb-implement/SKILL.md` — терминальный шаг Stop & Yield Control, ограничение на одну задачу.
  * `.agents/skills/kb-complete/SKILL.md` — терминальный шаг Stop & Yield Control, семантический формат записи в Devlog.
  * `docs/00_Templates/TEMPLATE_DEVLOG.md` и `templates/TEMPLATE_DEVLOG.md` — обновленный каркас Devlog.
  * `scripts/kb_lint.py` — функция проверки `check_devlog_semantic_guard`.
  * `tests/test_kb_lint.py` — тесты нового аудита.
  * `install.py` и `scripts/build_installer.py` — обновление встроенных шаблонов, генераторов правил и сборка бандла.
  * `tests/test_installer.py` — E2E регрессионные тесты.
  * `README.md`, `docs/Onboarding.md` — документация протокола гарантированной остановки.

* **Оценка рисков:**
  * Сохраняется принцип Zero Dependencies (стандартная библиотека Python 3).
  * Риск регрессии минимален благодаря сквозным E2E тестам.

---

## 4. Декомпозиция задач (Task Breakdown)

- [ ] [[../Specs/09_Guardrails/TASK-033-single-task-barrier-and-stop-yield-skills|TASK-033]]: Нормативный инвариант барьера единичной задачи в `AGENTS.md` и терминальный шаг `Stop & Yield Control` в `.agents/skills/kb-implement/SKILL.md` и `kb-complete/SKILL.md`.
- [ ] [[../Specs/09_Guardrails/TASK-034-devlog-semantic-guard-and-kb-lint-audit|TASK-034]]: Семантический протокол следующего шага в `TEMPLATE_DEVLOG.md`, аудит формулировок `check_devlog_semantic_guard` в `scripts/kb_lint.py` и модульные тесты в `tests/test_kb_lint.py`.
- [ ] [[../Specs/09_Guardrails/TASK-035-installer-bundling-e2e-and-docs|TASK-035]]: Синхронизация генераторов правил и шаблонов в `install.py` / `build_installer.py` (включая `--update`), сквозные E2E тесты в `tests/test_installer.py`, обновление `README.md` и `docs/Onboarding.md`.

---

## 5. Критерии приемки плана (Definition of Done для Режима 1)

- [x] Концепция согласована с пользователем (Режим 1: READ-ONLY, без изменения кода проекта).
- [x] Опирается на завершенное исследование [[../../04_Research/RESEARCH-012-single-task-execution-barrier-and-autonomous-pipeline-containment|RESEARCH-012]] и принятый стандарт [[../../03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]].
- [x] Создан файл плана `docs/02_Tasks/Plans/PLAN-009-single-task-barrier-and-stop-on-complete.md`.
- [x] Инициатива промоутирована из Icebox в Фазу 9 в `docs/02_Tasks/Roadmap.md`.
- [x] Задачи `TASK-033` — `TASK-035` добавлены в `docs/02_Tasks/Kanban.md` в колонку `📥 Бэклог (Backlog)`.
- [x] Пройдена проверка целостности базы знаний через `python scripts/kb_lint.py --path docs`.
