---
id: TASK-118
title: "Поведение скиллов, онбординг и корпус правил rules/AGENTS_CORE.md"
status: in-progress
type: task
phase: 32
track: standard
component:
  - skills
  - docs
  - rules
parent_plan: "[[../../Plans/PLAN-029-right-sizing-and-spec-quality-gate|PLAN-029]]"
depends_on:
  - "TASK-117"
created: 2026-11-20
updated: 2026-11-20
tags:
  - task/spec
  - phase32
  - skills
  - onboarding
  - rules
  - right-sizing
  - spec-quality
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-118 — Поведение скиллов, онбординг и корпус правил rules/AGENTS_CORE.md

> **ID:** TASK-118 | **Статус:** В работе (In Progress) | **Фаза:** 32 | **Трек:** Standard  
> **План:** [[../../Plans/PLAN-029-right-sizing-and-spec-quality-gate|PLAN-029: Right-Sizing процесса и Spec Quality Gate]] | **Канбан:** [[../../Kanban|Канбан-доска]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0037-wave-2-quality-and-evidence-standard|ADR-0037]] | **Исследование:** [[../../../04_Research/RESEARCH-031-wave-2-quality-and-evidence-architecture|RESEARCH-031]]  
> **Зависимости:** [[TASK-117-spec-quality-gate-and-kb016|TASK-117]]

---

## 0. Чек-лист качества ТЗ (Spec Quality Checklist)

- [x] Требования однозначны и не содержат недосказанностей
- [x] Нет неразрешённых маркеров `[NEEDS CLARIFICATION: ...]`
- [x] Скоуп символов локализован (`[MODIFY]`/`[NEW]`/`[DELETE]`) без номеров строк (ADR-0029)
- [x] Критерии приёмки (DoD) проверяемы автоматизированно

---

## 1. Цель задачи

Интегрировать стандарты матрицы Right-Sizing (`micro | standard | deep`), Spec Quality Gate (синтаксические маркеры `[NEEDS CLARIFICATION]`) и защитные механизмы (`KB-016`, `KB-020`) в операционное поведение скиллов (`/kb-plan`, `/kb-task`, `/kb-implement`), руководство разработчика (`docs/Onboarding.md`) и первоисточник правил (`rules/AGENTS_CORE.md` с синхронной генерацией `AGENTS.md` без дрифта).

---

## 2. Затрагиваемые файлы и скоуп символов

* `[MODIFY]` `.agents/skills/kb-plan/SKILL.md`:
  - `Procedure > Intent Routing` — добавление маршрутизации треков (`micro`, `standard`, `deep`) и префлайта Deep-Risk Guard (`KB-020`).
  - `Procedure > Record Plan` — фиксация поля `track: deep | standard` в создаваемом плане.
* `[MODIFY]` `.agents/skills/kb-task/SKILL.md`:
  - `Procedure > Draft Specification` — обязательное указание поля `track`, префлайт чек-листа ТЗ, запрет домысливания неясных требований и принудительное выставление маркеров `[NEEDS CLARIFICATION: <вопрос>]`.
* `[MODIFY]` `.agents/skills/kb-implement/SKILL.md`:
  - `Procedure > Sync & Context` — блокирующий префлайт при наличии неразрешенных маркеров `[NEEDS CLARIFICATION]` (соответствие правилу `KB-016`).
* `[MODIFY]` `docs/Onboarding.md`:
  - `Раздел 2: Четыре режима взаимодействия` — документация матрицы Right-Sizing (`micro/standard/deep`), Spec Quality Gate и регламента маркеров уточнения.
* `[MODIFY]` `rules/AGENTS_CORE.md`:
  - `Docs-as-Code Disciplines` — добавление нормативных правил `RIGHT-SIZING` и `SPEC-QUALITY-GATE`.
  - `Single-Task Execution Barrier & Invariants` — актуализация Always-On инвариантов Tier 2.
* `[MODIFY]` `AGENTS.md`:
  - Регенерация артефакта через `python scripts/gen_rules.py` с гарантией отсутствия расхождений (`--check`).

---

## 3. Детали реализации

### 3.1. Обновление скилла `/kb-plan`
В `.agents/skills/kb-plan/SKILL.md`:
1. При анализе идеи и формулировании плана определять рекомендуемый трек:
   - **Micro:** тривиальные правки ($\le 30$ LOC, $\le 2$ файлов) $\to$ предложение Fast-Track `/kb-task --fast`.
   - **Standard:** стандартные фичи и рефакторинги без высоких архитектурных рисков.
   - **Deep:** затрагивание ключевых компонентов с тегами `architecture`, `security`, `migration`, `public-api` $\to$ префлайт исследовательской базы (`research_basis` или ADR-0037).
2. Запись поля `track: deep | standard` в `TEMPLATE_PLAN.md`.

### 3.2. Обновление скилла `/kb-task`
В `.agents/skills/kb-task/SKILL.md`:
1. Обязательная валидация поля `track: micro | standard | deep` в создаваемой спецификации.
2. Проверка раздела `## 0. Чек-лист качества ТЗ`:
   - Если пользовательские требования содержат развилки, пробелы или неоднозначности, агенту **категорически запрещено додумывать** детали за пользователя.
   - Агент обязан явно вставить синтаксический маркер `[NEEDS CLARIFICATION: краткая суть развилки/вопроса]`.

### 3.3. Обновление скилла `/kb-implement`
В `.agents/skills/kb-implement/SKILL.md`:
1. В шаге 1 (`Sync & Context`):
   - Просканировать тело спецификации `TASK-XXX` на наличие активных маркеров `[NEEDS CLARIFICATION]`.
   - При обнаружении хотя бы одного маркера — немедленно **остановить реализацию** (Stop & Yield), вывести дружелюбное уведомление в чат с формулировками открытых вопросов и попросить пользователя принять решение перед началом кодовых правок (соответствие блокирующему правилу `KB-016`).

### 3.4. Обновление `docs/Onboarding.md`
1. Добавить подраздел «Матрица Right-Sizing процессов» с описанием критериев выбора треков (`Micro`, `Standard`, `Deep`).
2. Добавить подраздел «Spec Quality Gate и маркеры `[NEEDS CLARIFICATION]`» с описанием синтаксиса и механики защиты от галлюцинаций.

### 3.5. Обновление `rules/AGENTS_CORE.md` и `AGENTS.md`
1. Добавить инвариант **Right-Sizing Matrix**:
   - `micro`: Fast-Track без плана;
   - `standard`: классический цикл Modes 1-3;
   - `deep`: обязательное подтверждение `parent_plan` и `research_basis` (правило `KB-020`).
2. Добавить инвариант **Spec Quality Gate & Clarification Markers**:
   - Запрет спекулятивных домыслов;
   - Маркер `[NEEDS CLARIFICATION: <вопрос>]`;
   - Блокировка `/kb-implement` при наличии неразрешенных маркеров (правило `KB-016`).
3. Запустить `python scripts/gen_rules.py` для синхронизации `AGENTS.md`.

---

## 4. План верификации (Verification Plan)

- [ ] **Контроль генерации правил и отсутствия дрифта:**
  ```bash
  python scripts/gen_rules.py --check
  ```
  *Ожидаемый результат:* Exit code 0, полное соответствие `AGENTS.md` и `rules/AGENTS_CORE.md`.
- [ ] **Модульные тесты правил линтера:**
  ```bash
  python -m unittest tests/test_kb_lint.py
  ```
  *Ожидаемый результат:* 100% успешное прохождение всех тестов (включая `KB-016` и `KB-020`).
- [ ] **Тесты паритета шаблонов:**
  ```bash
  python -m unittest tests/test_template_parity.py
  ```
  *Ожидаемый результат:* 100% паритет шаблонов.
- [ ] **Аудит целостности базы знаний:**
  ```bash
  python scripts/kb_lint.py --path docs
  ```
  *Ожидаемый результат:* 0 broken links, 0 errors, 0 warnings.
- [ ] **Контроль навигации kb_state:**
  ```bash
  python scripts/kb_state.py status
  ```
  *Ожидаемый результат:* Отображение `TASK-118` в статусе in-progress.

---

## 5. Критерии готовности (DoD)

- [ ] Скиллы `/kb-plan`, `/kb-task`, `/kb-implement` обновлены и поддерживают матрицу Right-Sizing и Spec Quality Gate.
- [ ] Руководство `docs/Onboarding.md` дополнено разделами о Right-Sizing и маркерах `[NEEDS CLARIFICATION]`.
- [ ] Первоисточник правил `rules/AGENTS_CORE.md` дополнен Tier 2 инвариантами, `AGENTS.md` синхронизирован без дрифта (`gen_rules.py --check`).
- [ ] Все тесты и аудит базы знаний (`kb_lint.py`) проходят с кодом 0.
- [ ] Статус задачи обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [ ] Сессия зафиксирована в `docs/Devlog.md`.
