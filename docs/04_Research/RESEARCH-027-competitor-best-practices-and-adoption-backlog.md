---
id: RESEARCH-027
title: "Что перенять у конкурентов: аудит лучших практик и adoption-бэклог для agent-docs-harness"
status: completed
type: research
created: 2026-10-18
updated: 2026-10-18
tags:
  - research
  - competitive-analysis
  - best-practices
  - adoption-backlog
  - docs-as-code
  - spec-driven-development
  - quality-gates
related_tasks: []
related_adrs:
  - "[[../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001: Zero Dependencies]]"
  - "[[../03_Decisions_ADR/ADR-0005-rejection-of-embedded-web-visualizer|ADR-0005: Отказ от веб-визуализатора]]"
  - "[[../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009: High-SNR Token Architecture]]"
  - "[[../03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016: Single-Task Execution Barrier]]"
  - "[[../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025: Quality Gates Tier 1/2/3]]"
  - "[[../03_Decisions_ADR/ADR-0029-fine-grained-task-symbol-contracts-and-line-drift-rejection|ADR-0029: Символьные контракты]]"
  - "[[../03_Decisions_ADR/ADR-0030-single-source-rule-compiler|ADR-0030: Single-Source Rule Compiler]]"
---

# 🔬 Исследование: что конкуренты делают лучше и что из этого брать

> **Теги:** #research #competitive-analysis #best-practices #adoption-backlog #docs-as-code #spec-driven-development #quality-gates  
> **Продолжение:** [[../04_Research/RESEARCH-026-competitive-landscape-and-differentiation|RESEARCH-026: Конкурентный ландшафт и дифференциация]]  
> **Канбан:** [[../02_Tasks/Kanban|Канбан-доска]] | **Дорожная карта:** [[../02_Tasks/Roadmap|Roadmap.md]]

---

## 1. Вопрос, метод и гипотезы

### 1.1. Вопрос

[[../04_Research/RESEARCH-026-competitive-landscape-and-differentiation|RESEARCH-026]] ответил «сколько конкурентов» и «есть ли уникальная фича». Следующий вопрос: **где именно конкуренты объективно сильнее и какие практики стоит перенести, не потеряв нашу ДНК** (Zero Dependencies, Stop & Yield, аудируемость, High-SNR).

### 1.2. Метод

* Публичные README, docs и CLI-справочники: Spec Kit, Superpowers, OpenSpec, BMAD, Agent OS, Task Master, Backlog.md, Cline Memory Bank, cc-sdd, Disciplined Methodology.
* Сверка с нашими скиллами, шаблонами и `scripts/kb_lint.py` на 2026-10-18.
* Оценка **Value vs Effort** и влияния на позиционирование «governance/audit layer» из RESEARCH-026.
* Это **не** аудит исходного кода конкурентов и не бенчмарк; это перенос паттернов, а не копирование реализации.

### 1.3. Гипотезы

| # | Гипотеза | Критерий фальсификации |
| :--- | :--- | :--- |
| **H1** | Конкуренты сильнее не в «интеллекте» промптов, а в **детерминированной инженерии вокруг агента**: состояние, навигация, проверки, упаковка | Если их преимущество сводится только к шаблонам — гипотеза ложна |
| **H2** | Самые ценные заимствования — CLI-эргономика и машинно-читаемые артефакты, а не новые AI-фичи | Если внедрение `--json`/`next` не меняет UX — гипотеза ложна |
| **H3** | Копирование всех гейтов подряд усилит церемонию и ухудшит adoption; сначала нужен right-sizing процесса | Если добавление гейтов не влияет на время до первой задачи — гипотеза ложна |

---

## 2. Где конкуренты объективно сильнее

### 2.1. Сводка по слоям

| Слой | Кто сильнее | Что именно сделано лучше | Наш разрыв |
| :--- | :--- | :--- | :--- |
| **Состояние и навигация** | BMAD, OpenSpec, Task Master, Backlog.md | `bmad-help` / `bmad status`, `openspec status/doctor/context`, `task-master next`, `backlog` JSON | Нет детерминированных `next/status/doctor`; логика «что дальше» живёт в прозе скиллов |
| **Качество спецификаций** | Spec Kit, OpenSpec, cc-sdd | `[NEEDS CLARIFICATION]`, чек-листы как «unit tests» для спеки, Phase -1 gates, delta-спеки, `_Boundary:_` / `_Depends:_` | Нет маркеров неопределённости, чек-листа качества спеки, delta-секции, трассировки сценарий → тест |
| **Ревью и сходимость** | Superpowers, cc-sdd, OpenSpec (schema `anvil`) | Двухстадийное ревью, независимый reviewer, auto-debug, converge-цикл, verdict-гейт | TDD только для багов; нет обязательного ревью-контракта и convergence-гейта |
| **Граф задач** | Task Master, Backlog.md, cc-sdd | Зависимости, `next`, complexity analysis, blocked-by, milestones | Плоский Kanban без зависимостей и защиты от преждевременного старта |
| **Контекст** | Agent OS, Cline MB, OpenSpec | Discover/inject стандартов, `activeContext`/`progress`, project context в конфиге | Статические `AGENTS.md` и шаблоны; нет per-task манифеста релевантных знаний |
| **Упаковка и интеграции** | Spec Kit, OpenSpec, Superpowers | Extensions/presets/catalogs, 30+ инструментов, JSON/SARIF-подобный вывод, marketplace, air-gapped | Нет `--format json/sarif`, GitHub Action, pre-commit, inventory; 7 адаптеров против 16–30+ |
| **Right-sizing процесса** | BMAD, OpenSpec | «Размер процесса по размеру изменения», profiles/schemas, независимые entry points | Только micro (Fast-Track) vs полный цикл; среднего трека нет |

### 2.2. Главный вывод

**Конкуренты выигрывают не промптами, а инженерией вокруг промптов.** У них есть состояние, машинно-читаемые выходы, проверки и упаковка. Наш харнесс силён философией и линтом, но слаб в детерминированной операционной обвязке. Именно там лежит наибольший ROI заимствований.

---

## 3. Каталог практик: что берём

| # | Практика | Кто делает лучше | Конкретное заимствование | Effort | Влияние на wedge |
| :--- | :--- | :--- | :--- | :---: | :--- |
| 1 | Машинно-читаемая диагностика | OpenSpec `--json`, Backlog `--json`, Spec Kit artifact inventory | `kb_lint --format {text,json,sarif}`, стабильные rule-id | S | **Усиливает** |
| 2 | CI/pre-commit упаковка | Spec Kit, OpenSpec | `action.yml`, `.pre-commit-hooks.yaml`, пример workflow | S–M | **Усиливает** |
| 3 | State/navigation | BMAD, OpenSpec, Task Master | `kb_state.py next/status`, `install.py --doctor` | M | **Усиливает** |
| 4 | Зависимости задач | Task Master, Backlog, cc-sdd | `depends_on`, cycle detection, blocked-by | S–M | Усиливает |
| 5 | Right-sizing | BMAD | 3 трека: micro / standard / deep + матрица риска | S | **Снимает главный барьер** |
| 6 | Маркеры неопределённости | Spec Kit | `[NEEDS CLARIFICATION: ...]` + запрет догадок | S | Усиливает |
| 7 | Чек-лист качества спеки | Spec Kit | «Unit tests» для ТЗ: тестируемость, измеримость, отсутствие спекуляций | S | Усиливает |
| 8 | Сценарий → тест | OpenSpec schema `anvil` | Таблица `Scenario → Test` в ТЗ; `/kb-complete` проверяет покрытие | S–M | **Усиливает** |
| 9 | Двухстадийное ревью | Superpowers, cc-sdd | Stage 1 spec compliance, Stage 2 code quality, verdict + evidence | M | **Усиливает** |
| 10 | Convergence / consistency | Spec Kit | Сверка diff ↔ ТЗ ↔ DoD; deviations; повторная верификация | M | Усиливает |
| 11 | Delta-спеки | OpenSpec | `ADDED/MODIFIED/REMOVED` для brownfield-изменений | M | Усиливает (brownfield) |
| 12 | Контекстный манифест | Agent OS, OpenSpec config | `kb_state.py context TASK-XXX`: релевантные ADR/research/patterns/techdebt | M | Усиливает (токены) |
| 13 | Resumable state | cc-sdd | `## Current State` + `next_action` в задаче; продолжение после сбоя | S–M | Нейтрально |
| 14 | Doctor / upgrade diff | OpenSpec, Spec Kit, BMAD | `--doctor`, `--update --dry-run`, artifact inventory | M | Усиливает |
| 15 | Assess go/clarify/kill | Spec Kit | Решение с критериями в `RESEARCH-XXX` и `/kb-research` | S | Нейтрально |
| 16 | Evals скиллов | Superpowers | Drill-харнесс для проверки поведения скиллов | L | Нейтрально/дорого |
| 17 | Extensions/schemas | Spec Kit, OpenSpec | Локальный реестр расширений/схем | L | Позже |
| 18 | Stores/монорепо | OpenSpec | Кросс-репозиторные спеки | L | Позже |

---

## 4. Приоритизированный adoption-бэклог

### Волна 1 — фундамент (P0)

1. **`kb_lint` как продукт:** `--format json|sarif`, `--fix` (безопасное подмножество), `--version`, стабильные `KB-XXX` rule-id.
2. **CI/pre-commit:** `action.yml` (composite, без зависимостей), `.pre-commit-hooks.yaml`, короткий workflow-пример.
3. **`kb_state.py`:** `next`, `status`, `context TASK-XXX`; `--json`; интеграция в `kb-onboard` и `/kb-complete`.
4. **Зависимости задач:** `depends_on`, проверка циклов/висячих ID, blocked-by в Kanban, учёт в `next`.
5. **Right-sizing:** три трека и матрица риска в `/kb-plan`, `/kb-task`, `Onboarding.md`; линт-предупреждение для deep-изменений без research/plan.

**Почему сначала это:** волна 1 не добавляет обязательных гейтов, а снижает трение и делает наши проверки пригодными для CI. Это прямо усиливает позиционирование «governance/audit layer», не ухудшая порог входа.

### Волна 2 — качество и доказательства (P1)

6. **Spec Quality Gate:** `[NEEDS CLARIFICATION]`, чек-лист качества, запрет спекулятивных требований; блокировка `in-progress/done` при неразрешённых маркерах.
7. **Сценарий → тест:** таблица в `TEMPLATE_TASK`; `/kb-complete` не закрывает задачу с непокрытыми сценариями (WARN → ERROR для deep-трека).
8. **Review & Convergence Gate:** двухстадийное ревью, `review:`-блок, verdict, evidence; self-review vs independent reviewer; convergence-сверка diff ↔ ТЗ.
9. **Delta-спеки:** `ADDED/MODIFIED/REMOVED` для задач, меняющих существующее поведение; `/kb-complete` синхронизирует `SPEC.md`/архитектуру.

**Почему после волны 1:** это дополнительные гейты. Их нужно ставить только на deep-трек и только после того, как появился `next/status` и right-sizing, иначе церемония добьёт adoption.

### Волна 3 — контекст и эксплуатация (P2)

10. **Контекстный манифест:** `kb_state.py context TASK-XXX` с релевантными ADR/research/patterns/techdebt/prior tasks; компактный вывод и «почему включено».
11. **Doctor/upgrade diff:** `install.py --doctor`, `--update --dry-run`, inventory шаблонов/скиллов.
12. **Resumable state:** `## Current State` / `next_action` в задаче; продолжение после сбоя.
13. **Assess go/clarify/kill:** явное решение и критерии в `TEMPLATE_RESEARCH` и `/kb-research`.

### Отложено / отклонено

* **Evals скиллов** — дорого, требует LLM-вызовов, не вписывается в zero-deps CI; вернуться после появления внешнего eval-контура.
* **Extensions/schemas, stores, marketplace** — требуют массовой аудитории и поддержки; преждевременно.
* **Web UI, dashboard, approval-UI** — [[../03_Decisions_ADR/ADR-0005-rejection-of-embedded-web-visualizer|ADR-0005]]; конкуренты закрывают это лучше.
* **Autonomy-first субагенты** — противоречит [[../03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]] и нашей позиции containment.

---

## 5. Deep dive: шесть заимствований с наибольшим ROI

### 5.1. `kb_lint` как самостоятельный продукт

**Проблема:** сегодня линт — это скрипт внутри харнесса с человекочитаемым выводом и двумя флагами (`--path`, `--verbose`). Его нельзя нормально встроить в CI, code scanning или pre-commit без парсинга текста.

**Что берём:** у OpenSpec — `validate`/`status --json`; у Backlog.md — `--json`; у Spec Kit — artifact inventory. Но не копируем их форматы; делаем свой минимальный, стабильный контракт.

**Предлагаемый контракт:**
```bash
python scripts/kb_lint.py --path docs --format sarif > kb.sarif
python scripts/kb_lint.py --path docs --format json
python scripts/kb_lint.py --path docs --fix --dry-run
```
* `KB-001` broken wikilink, `KB-002` frontmatter, `KB-003` memory limit, `KB-004` tech debt, `KB-005` asset layout, `KB-006` phase consistency, `KB-007` research basis, `KB-008` devlog semantics, `KB-009` untracked TODO, `KB-010` dependency cycle.
* JSON: `{ "version": 1, "errors": [...], "warnings": [...], "summary": {...} }`, у каждого элемента `rule_id`, `severity`, `file`, `line`, `message`, `fixable`.
* SARIF: минимальный валидный `runs[].results[]` для GitHub Code Scanning.
* `--fix`: только детерминированные, не семантические правки (регистр wikilink при однозначном совпадении, отсутствующий `updated`, нормализация тега фазы). Всё остальное — suggestion, не auto-fix.

**DoD:** линт работает на Python 3.8 без зависимостей; SARIF валиден; GitHub Action краснеет на битой ссылке; pre-commit блокирует коммит; вывод `text` не меняется (обратная совместимость).

**Риск:** `--fix` может испортить пользовательские ссылки. Поэтому — `--dry-run` по умолчанию, backup и только безопасный класс правок.

---

### 5.2. `kb_state.py`: next / status / context

**Проблема:** «что делать дальше» сейчас вычисляет агент по прозе скилла. Это дорого, недетерминированно и зависит от контекста. У BMAD есть `bmad-help`/`bmad status`, у OpenSpec — `status/doctor/context`, у Task Master — `next`, у Backlog — JSON.

**Что берём:** детерминированную навигацию по состоянию KB, без LLM.

**Предлагаемый контракт:**
```bash
python scripts/kb_state.py next            # одна следующая команда + почему
python scripts/kb_state.py status          # фаза, in-progress, blocked, stale, attention
python scripts/kb_state.py context TASK-096 --max-items 10
python scripts/kb_state.py next --json
```

**Источники:** `Specs/**` (status, phase, depends_on, parent_plan), `Bugs/**` (severity, release_blocker), `Plans/**`, `Kanban.md`, `Inbox/`, `TechDebt.md`, `Roadmap.md`.

**Выход `status`:** текущая фаза; in-progress (и сколько дней stale); blocked (и чем); ready-to-start; новые FB; открытые release-блокеры; расхождения Kanban ↔ frontmatter.

**Выход `next`:** ровно одна рекомендация + команда, например:
```
Next: TASK-097 — Add kb_lint SARIF output
Why: phase 26, status planned, deps satisfied, no open blocker
Command: /kb-implement TASK-097
```

**DoD:** `--json` стабилен; `next` не предлагает задачу с невыполненными зависимостями; `status` находит расхождения; интеграция в `kb-onboard` и `/kb-complete`.

**Риск:** ложные приоритеты. Решение: `next` — advisory, финальное слово за пользователем (Human Guardrails).

---

### 5.3. Зависимости задач и защита от преждевременного старта

**Проблема:** Kanban плоский, `depends_on` нет. Агент может взять задачу, чьи предпосылки не готовы; lint этого не видит.

**Что берём:** Task Master (dependencies/next), Backlog (blocked-by/milestones), cc-sdd (`_Depends:_`).

**Предлагаемый контракт:**
```yaml
depends_on: ["TASK-095", "TASK-096"]
```
* `kb_lint`: `KB-010` — неизвестный ID, цикл, зависимость на `cancelled` (ERROR); `in-progress` при незакрытых зависимостях (WARN).
* `kb_state next`: не предлагает задачу с незакрытыми зависимостями.
* Kanban: суффикс `⛔ blocked by TASK-XXX` (ручной или генерируемый).
* `TEMPLATE_TASK`: поле `depends_on` и раздел «Предпосылки».

**DoD:** цикл из двух задач ловится тестом; `next` обходит blocked; существующие задачи без поля не ломаются (обратная совместимость).

---

### 5.4. Spec Quality Gate: `[NEEDS CLARIFICATION]` + чек-лист + сценарий → тест

**Проблема:** ТЗ может быть «гладким», но неоднозначным: агент догадывается о требованиях, а потом «успешно» реализует не то. У Spec Kit есть `[NEEDS CLARIFICATION]`, чек-листы как unit tests и Phase -1 gates; у OpenSpec schema `anvil` — `Scenario → Test` ledger.

**Что берём (минимально):**
* В `TEMPLATE_TASK` — раздел `## 0. Spec Quality Checklist`:
  - [ ] Нет неразрешённых `[NEEDS CLARIFICATION: ...]`
  - [ ] Требования тестируемы и однозначны
  - [ ] Критерии успеха измеримы
  - [ ] Нет спекулятивных «может пригодиться»
  - [ ] Каждый сценарий отображён на тест/проверку
* В `/kb-task`: при неопределённости — ставить маркер, **не угадывать**.
* В `TEMPLATE_TASK` — таблица:
  ```markdown
  | Сценарий | Тест / проверка | Статус |
  | :--- | :--- | :--- |
  | ... | `tests/test_x.py::test_y` | [ ] |
  ```
* `kb_lint`: `[NEEDS CLARIFICATION]` в `planned` → WARN; в `in-progress/done` → ERROR. Непокрытый сценарий в `done` → WARN (позже ERROR для deep-трека).

**DoD:** маркер в done-задаче валит линт; чек-лист есть в шаблоне и в `/kb-task`; таблица сценариев обязательна для задач с acceptance criteria.

**Риск:** бюрократизация. Решение: чек-лист — только для standard/deep; micro-трек его пропускает.

---

### 5.5. Review & Convergence Gate

**Проблема:** у нас есть верификация (тесты/линт), но нет доказанного ревью «сделано ли то, что просили». Superpowers делает двухстадийное ревью (spec compliance → code quality), cc-sdd — независимого reviewer и auto-debug, OpenSpec `anvil` — verdict-гейт.

**Что берём:**
* `## 6. Review Contract` в `TEMPLATE_TASK`:
  - **Stage 1 — Spec compliance:** все `[NEW]/[MODIFY]` файлы и символы затронуты; DoD выполнен; verification evidence приложен.
  - **Stage 2 — Code quality:** архитектура, Zero-Deps, обработка ошибок, тесты, безопасность.
* Frontmatter:
  ```yaml
  review:
    status: passed        # pending | passed | failed | waived
    reviewer: self        # self | independent | human
    verdict: PASS         # PASS | FAIL
    evidence: ["tests/test_x.py::test_y", "kb_lint OK"]
  ```
* `/kb-implement` step 4.5: self-review по чек-листу; если хост поддерживает субагентов — independent reviewer с diff + ТЗ; иначе честно `reviewer: self`, без имитации независимости.
* `/kb-complete`: `status: done` требует `review.status: passed`; для deep-трека (`architecture|security|migration`) — `reviewer: human` или `independent`.
* **Convergence:** после тестов сравнить `git diff` с ТЗ; зафиксировать deviations; либо исправить, либо обновить ТЗ с одобрения пользователя; повторно прогнать verification.

**DoD:** задача без review-блока не закрывается (WARN → ERROR после миграции); deep-задача без human/independent review не закрывается; deviations не пусты, если были.

**Риск:** имитация ревью. Решение: evidence обязателен (команды + вывод + список файлов), а для deep-трека — человек. Это соответствует нашему аудит-позиционированию, а не «галочке».

---

### 5.6. Right-sizing: три трека вместо «micro vs всё»

**Проблема:** сейчас есть только Fast-Track (≤30 LOC, ≤2 файла) и полный цикл research → plan → spec. Средний размер изменения проваливается в полный цикл, что отпугивает.

**Что берём:** BMAD right-sized process + независимые entry points Spec Kit.

| Трек | Критерии | Обязательные артефакты | Пропускается |
| :--- | :--- | :--- | :--- |
| **Micro** | ≤30 LOC, ≤2 файла, нет публичного API/новых зависимостей | Micro-Spec | Plan, Research |
| **Standard** | 1 модуль, обратимо, нет миграций/новых зависимостей | `TASK-XXX` + `research_basis: none` + `basis_note` | Research; Plan — опционально |
| **Deep** | Архитектура, публичный API, миграция, безопасность, новая зависимость | `RESEARCH-XXX` → `PLAN-XXX` → `TASK-XXX`, review human/independent | Ничего |

**DoD:** матрица опубликована в `/kb-plan`, `/kb-task`, `Onboarding.md`; `kb_lint` предупреждает, если deep-теги (`architecture`, `migration`, `public-api`, `security`) без research/plan; micro-задачи не требуют чек-листа качества.

**Риск:** агент неправильно классифицирует. Решение: классификация — предложение с подтверждением пользователя; линт ловит очевидные пропуски, но не блокирует.

---

## 6. Что не копируем

| Практика | Кто | Почему нет |
| :--- | :--- | :--- |
| Autonomy-first субагенты, часы без человека | Superpowers, cc-sdd | Противоречит Stop & Yield и позиции containment; ресурсоёмко |
| Persona-heavy роли (Analyst/PM/Architect/QA) | BMAD | Токен-оверхед, имитация процессов; наш value — лёгкий аудит |
| Web dashboard / approval UI | Backlog.md, spec-workflow-mcp | [[../03_Decisions_ADR/ADR-0005-rejection-of-embedded-web-visualizer|ADR-0005]]; конкуренты закрывают лучше |
| Plugin marketplace / hosted catalogs | Spec Kit, BMAD, Superpowers | Нужна массовая аудитория; преждевременно |
| Telemetry | OpenSpec | Против privacy-позиционирования |
| 14 языков документации | cc-sdd | Поддержка дороже пользы; ru/en достаточно |
| Stores / монорепо | OpenSpec | Сложность; отложить до реального запроса |
| Полный EARS-формализм | Kiro/cc-sdd | Избыточен; берём только WHEN/THEN для сценариев |
| Evals на LLM в CI | Superpowers | Ломает zero-deps и детерминизм CI |

---

## 7. Последовательность и метрики

### 7.1. Последовательность

1. **Волна 1** — `kb_lint --format/--fix`, CI/pre-commit, `kb_state next/status`, зависимости, right-sizing.
2. **Волна 2** — spec quality gate, сценарий → тест, review/convergence, delta-спеки (только deep/standard).
3. **Волна 3** — контекстный манифест, doctor/upgrade diff, resumable state, assess go/clarify/kill.

**Правило:** ни один новый гейт не добавляется без трека, который его пропускает. Иначе мы проиграем OpenSpec по порогу входа.

### 7.2. Метрики (замерять ≥3 прогонов)

* **Time-to-first-task:** от установки до первой созданной задачи.
* **False-positive rate** линта на реальной KB (цель: <5%).
* **Доля задач с review evidence** (цель: 100% для deep, ≥80% для standard).
* **Доля ТЗ с неразрешёнными `[NEEDS CLARIFICATION]` на момент done** (цель: 0).
* **CI adoption:** число проектов с `kb-lint` workflow / pre-commit.
* **Token overhead** против конкурентов (≥3 прогона, холодный старт отброшен).

### 7.3. Что это даст

* **Wedge:** линт становится самостоятельным продуктом, а не внутренним скриптом.
* **Adoption:** right-sizing и `next` снижают порог входа.
* **Audit:** review/convergence/сценарий→тест дают доказательства, а не «мы проверили».
* **Дифференциация:** мы не соревнуемся в автономии; мы соревнуемся в доказуемости.

### 7.4. Следующий шаг

Если волна 1 одобрена:

* `/kb-plan Wave 1 — Docs Integrity Gate productization` — полный RFC на CLI-контракт, SARIF, GitHub Action и pre-commit.
* или `/kb-task --fast "kb_lint --format json"` — если хотим начать с одного флага и одного теста.

**Не начинать волну 2 до завершения волны 1:** иначе церемония вырастет без фундамента, и мы получим худшее из двух миров — тяжёлый процесс без CI-пригодного линта.

---

## 8. Источники

| Источник | Что взято | URL |
| :--- | :--- | :--- |
| GitHub Spec Kit | `[NEEDS CLARIFICATION]`, чек-листы, Phase -1 gates, `[P]`, converge, extensions | https://github.com/github/spec-kit |
| Spec Kit SDD methodology | Конституция, consistency, test-first, иерархия деталей | https://github.com/github/spec-kit/blob/main/spec-driven.md |
| OpenSpec CLI | `validate`, `status`, `doctor`, `context`, `--json`, schemas | https://openspec.dev/docs/cli |
| OpenSpec customization | Project context/rules, custom schemas, community `anvil` | https://github.com/Fission-AI/OpenSpec/blob/main/docs/customization.md |
| Superpowers | Brainstorming, plans, subagent-driven dev, two-stage review, TDD, worktrees | https://github.com/obra/superpowers |
| BMAD-METHOD | Right-sized process, `bmad-help`/`status`, modules | https://github.com/bmad-code-org/BMAD-METHOD |
| Task Master | Dependencies, `next`, complexity, MCP tool profiles | https://github.com/eyaltoledano/claude-task-master |
| Backlog.md | 3 review checkpoints, DoD defaults, dependencies, JSON/watch, archive | https://github.com/MrLesk/Backlog.md |
| cc-sdd | Discovery routing, `_Boundary:_`, independent reviewer, resumable state | https://github.com/gotalab/cc-sdd |
| Agent OS | Standards discovery/injection | https://github.com/buildermethods/agent-os |
| Cline Memory Bank | `activeContext`/`progress`, hierarchical memory | https://docs.cline.bot/best-practices/memory-bank |
| Disciplined Methodology | Checks over reminders, docs under same checks | https://github.com/Varietyz/Disciplined-AI-Software-Development |
