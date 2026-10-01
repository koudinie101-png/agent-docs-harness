---
id: PLAN-006
title: "Фаза 6: Интеграция этапа исследования (Режим 0: Discovery & Feasibility) и эволюция /kb-research"
status: accepted
type: plan
phase: 6
created: 2026-10-01
updated: 2026-10-01
tags:
  - plan
  - phase6
  - discovery
  - kb-research
  - lifecycle
  - double-diamond
  - roadmap
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 📋 План: PLAN-006 — Фаза 6: Интеграция этапа исследования (Режим 0: Discovery & Feasibility) и эволюция /kb-research

> **ID:** PLAN-006  
> **Статус:** Согласовано (Режим 1)  
> **Теги:** #plan #phase6 #discovery #kb-research #lifecycle #double-diamond #roadmap  
> **Родительская спецификация:** [[../../SPEC|SPEC.md]]  
> **Канбан:** [[../Kanban|Канбан-доска]]  
> **Связанные исследования и ADR:** [[../../04_Research/RESEARCH-007-discovery-mode-and-kb-research-lifecycle-integration|RESEARCH-007: Интеграция этапа исследования (Режим 0) и эволюция /kb-research]], [[../../03_Decisions_ADR/ADR-0012-discovery-mode-and-kb-research-lifecycle-integration|ADR-0012: Интеграция Режима 0 в жизненный цикл]], [[../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009: High-SNR Token Architecture]], [[../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001: Zero Dependencies]]  

---

## 1. Контекст и цели (Problem & Goals)

### Проблема
В методологии Docs-as-Code жестко регламентирован цикл поставки (**Delivery Cycle**: Режимы 1–3: `/kb-plan` -> `/kb-task` -> `/kb-implement` & `/kb-complete`). Однако этап предварительного исследования и валидации (**Discovery Cycle**: «Что имеет смысл делать и какова ценность/риски») не был замкнут в единый формализованный процесс.

В результате возникали два системных антипаттерна:
1. **Захламление бэклога (Icebox Graveyard):** Сырые непроверенные идеи заносились вручную в секцию `Roadmap.md` (Icebox) без критического стресс-теста, фальсификации и оценки рисков, зависая там «мертвым грузом».
2. **Преждевременное планирование (Premature Planning Trap):** При запуске `/kb-plan <идея>` агент сразу формировал план декомпозиции задач (`PLAN-XXX`) для гипотез, чья техническая осуществимость или ценность не были проверены, что приводило к тупикам на стадии кодинга.

### Цель Фазы 6
Реализовать стандарт сквозного жизненного цикла (Double Diamond) согласно [[../../03_Decisions_ADR/ADR-0012-discovery-mode-and-kb-research-lifecycle-integration|ADR-0012]] и [[../../04_Research/RESEARCH-007-discovery-mode-and-kb-research-lifecycle-integration|RESEARCH-007]]:
1. Эволюционировать скилл `.agents/skills/kb-research/SKILL.md` в инструмент валидации продуктовых и архитектурных гипотез с критическим стресс-тестированием (Режим 0).
2. Автоматизировать двухпутевую воронку регистрации результатов исследования в `Roadmap.md`:
   - Одобренные инициативы — автоматическое добавление в `## 🔮 Перспективные направления (Icebox)` с оценкой ценности и связями.
   - Нежизнеспособные идеи — фиксация отказного ADR (`status: rejected`) и автоматическое добавление в `## 🚫 Отклоненные архитектурные идеи`.
3. Внедрить рекомендательный префлайт-чек (Nudge) в `.agents/skills/kb-plan/SKILL.md` для перенаправления непроверенных рискованных идей в `/kb-research`.
4. Обновить онбординг и шаблоны (`TEMPLATE_ROADMAP.md`, `TEMPLATE_ONBOARDING.md`, `Onboarding.md`, `kb-onboard`) с фиксацией 4-этапного жизненного цикла (Режим 0 -> Режимы 1–3).
5. Обеспечить сквозную упаковку обновленных скиллов и шаблонов в `install.py` / `build_installer.py`, поддержку в `--update` и прохождение всех E2E тестов.

---

## 2. Обсуждение и ключевые решения (Q&A / Discussion)

* **Q1: Почему расширяется `/kb-research`, а не создается отдельный скилл `/kb-ideate`?**
  * **Решение (согласно [[../../03_Decisions_ADR/ADR-0012-discovery-mode-and-kb-research-lifecycle-integration|ADR-0012]]):** Создание нового скилла увеличивает Always-On контекст в системном промпте модели, нарушая High-SNR токеномику ([[../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]]). Скилл `/kb-research` семантически охватывает как баги платформ, так и валидацию продуктовых гипотез.
* **Q2: Блокирует ли линтер ручные правки секции Icebox в `Roadmap.md`?**
  * **Решение:** Нет, блокирующий запрет отклонен как враждебный DX. Регулирование осуществляется через ориентирующий комментарий в шапке Icebox, культуру работы и рекомендательный Nudge в `/kb-plan`.
* **Q3: Как работает префлайт-чек в `/kb-plan`?**
  * **Решение:** Если в `/kb-plan <идея>` передана тема с архитектурными рисками (сторонние зависимости, нестабильные платформенные API), агент в роли Senior Partner задает вопрос пользователю: рекомендовать сначала валидацию в Режиме 0 (`/kb-research`) или продолжить прямое планирование.

---

## 3. Архитектурное влияние и риски (Architectural Impact & Risks)

* **Затрагиваемые компоненты:**
  * `.agents/skills/kb-research/SKILL.md` — расширение скоупа, двухпутевая воронка интеграции с `Roadmap.md`.
  * `.agents/skills/kb-plan/SKILL.md` — внедрение префлайт-чека и Nudge для непроверенных идей.
  * `.agents/skills/kb-onboard/SKILL.md` — обновление до 4-этапного цикла (Discovery + Delivery).
  * `docs/00_Templates/TEMPLATE_ROADMAP.md` и `templates/TEMPLATE_ROADMAP.md` — стандартизация структуры Icebox и секции отклоненных альтернатив.
  * `docs/00_Templates/TEMPLATE_ONBOARDING.md` и `templates/TEMPLATE_ONBOARDING.md` — отражение 4 режимов.
  * `docs/Onboarding.md` — актуализация диаграммы жизненного цикла и матрицы команд.
  * `scripts/build_installer.py` и `install.py` — перепаковка шаблонов и скиллов.
  * `tests/test_installer.py` — проверка целостности и обновления через `--update`.
* **Оценка рисков и соблюдение стандартов:**
  * Принцип Zero Dependencies ([[../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]) строго сохраняется (stdlib Python 3).
  * High-SNR лаконичность ([[../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]]) — описания скиллов остаются в пределах ультра-компактных формулировок.
  * Целостность графа базы знаний — `scripts/kb_lint.py` обязан подтверждать 0 битых ссылок.

---

## 4. Высокоуровневая декомпозиция (Task Breakdown)

- [ ] **TASK-021:** Эволюция скилла `.agents/skills/kb-research/SKILL.md` (валидация продуктово-архитектурных гипотез, автоматическая двухпутевая регистрация в `Roadmap.md`: Icebox vs Отклоненные ADR).
- [ ] **TASK-022:** Префлайт-чеки в `.agents/skills/kb-plan/SKILL.md` (Nudge для невалидированных идей) и обновление `.agents/skills/kb-onboard/SKILL.md` (4-этапный цикл).
- [ ] **TASK-023:** Обновление шаблонов `TEMPLATE_ROADMAP.md`, `TEMPLATE_ONBOARDING.md` (в `docs/00_Templates/` и `templates/`) и руководства `docs/Onboarding.md` (Double Diamond: Режимы 0–3).
- [ ] **TASK-024:** Синхронизация инсталлятора `scripts/build_installer.py` / `install.py`, актуализация `tests/test_installer.py` и аудит через `scripts/kb_lint.py`.

---

## 5. Критерии приемки плана (Definition of Done для Режима 1)

- [x] Концепция согласована с пользователем (Режим 1: READ-ONLY, без изменения кода).
- [x] Опирается на завершенное исследование [[../../04_Research/RESEARCH-007-discovery-mode-and-kb-research-lifecycle-integration|RESEARCH-007]] и принятый стандарт [[../../03_Decisions_ADR/ADR-0012-discovery-mode-and-kb-research-lifecycle-integration|ADR-0012]].
- [x] Создан файл плана `docs/02_Tasks/Plans/PLAN-006-discovery-mode-and-kb-research-lifecycle.md`.
- [x] Инициатива промоутирована из Icebox в Фазу 6 в `docs/02_Tasks/Roadmap.md`.
- [x] Задачи `TASK-021` — `TASK-024` добавлены в `docs/02_Tasks/Kanban.md` в колонку `📥 Бэклог`.
- [x] Пройдена проверка целостности базы знаний через `python scripts/kb_lint.py --path docs`.
