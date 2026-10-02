---
id: PLAN-008
title: "Фаза 8: Greenfield-инициализация от идеи (Idea-First) и протокол Living Spec"
status: accepted
type: plan
phase: 8
created: 2026-10-02
updated: 2026-10-02
tags:
  - plan
  - phase8
  - greenfield
  - install
  - idea-first
  - living-spec
  - readme-sync
  - docs-as-code
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 📋 План: PLAN-008 — Фаза 8: Greenfield-инициализация от идеи (Idea-First) и протокол Living Spec

> **ID:** PLAN-008  
> **Статус:** Согласовано (Режим 1)  
> **Теги:** #plan #phase8 #greenfield #install #idea-first #living-spec #readme-sync #docs-as-code  
> **Родительская спецификация:** [[../../SPEC|SPEC.md]]  
> **Канбан:** [[../Kanban|Канбан-доска]]  
> **Связанные исследования и ADR:** [[../../04_Research/RESEARCH-009-greenfield-initialization-and-living-spec-drift|RESEARCH-009: Greenfield-инициализация от идеи и Living Spec]], [[../../03_Decisions_ADR/ADR-0014-greenfield-idea-first-initialization-and-living-spec-protocol|ADR-0014: Архитектура Greenfield-инициализации и Living Spec]], [[../../03_Decisions_ADR/ADR-0012-discovery-mode-and-kb-research-lifecycle-integration|ADR-0012: Режим 0 Discovery]], [[../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001: Zero Dependencies]], [[../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009: High-SNR Token Architecture]]  

---

## 1. Контекст и цели (Problem & Goals)

### Проблема
1. **Разрыв старта с нуля (Idea-First Greenfield):** В ситуации, когда разработчик начинает в пустой директории лишь с концептуальной идеи приложения, целевой стек технологий (Rust, Swift, Go, Python, TypeScript) объективно неизвестен. Текущий мастер `install.py` вынуждает пользователя указывать конкретный язык, создавая ложные заглушки сборщиков и тестов, которые приходится вручную вычищать.
2. **Дрифт спецификации (Documentation Drift / Rotten Spec):** В ходе реализации задач (Фазы 1–7+) фокус агентов сосредоточен на локальных файловых контрактах `TASK-XXX`. Корневые файлы `SPEC.md` и `README.md` остаются застывшими в первоначальном виде, теряя актуальность и переставая быть Единым Источником Истины (Single Source of Truth).

### Цели Фазы 8
В соответствии с [[../../03_Decisions_ADR/ADR-0014-greenfield-idea-first-initialization-and-living-spec-protocol|ADR-0014]] и [[../../04_Research/RESEARCH-009-greenfield-initialization-and-living-spec-drift|RESEARCH-009]]:
1. Реализовать пресет `undecided` (*"Undecided / Idea-First Research"*) и CLI-флаг `--idea "<описание>"` в `install.py` / `build_installer.py`.
2. Создавать стартовый `SPEC.md` со статусом `status: discovery` при выборе пресета `undecided`, направляя агента сразу в Режим 0 (`/kb-research <идея-и-стек>`).
3. Внедрить механизм кристаллизации `SPEC.md` и `README.md` в скилл `kb-research` при закрытии архитектурного решения по стеку (`ADR-0001`).
4. Закрепить **Инвариант Живой Спецификации (Living Spec Invariant)**: синхронизационные напоминания в `kb-complete`, обязательный префлайт-чек в `kb-release` и эвристический неблокирующий warning в `scripts/kb_lint.py`.
5. Покрыть новые возможности тестами в `tests/test_installer.py` и `tests/test_kb_lint.py`, пересобрать инсталлятор и обновить онбординг.

---

## 2. Обсуждение и ключевые решения (Q&A / Discussion)

* **Q1: Как сочетаются флаги `--idea` и `--stack`?**
  * **Решение:** Если передан `--idea "<текст>"` без флага `--stack`, инсталлятор автоматически активирует пресет `undecided` без интерактивного диалога. Если флаг `--stack` передан явно вместе с `--idea`, используется указанный стек, а переданное описание идеи всё равно заносится в концептуальный раздел `SPEC.md`.
* **Q2: В какой момент `SPEC.md` кристаллизуется и переходит в статус `status: active`?**
  * **Решение:** При завершении первичного исследования в Режиме 0 (`RESEARCH-001` + `ADR-0001` по выбору стека). Агент актуализирует `SPEC.md` (архитектурные слои, команды сборки/тестирования) и витрину `README.md`, переводя проект в фазу готовности к планированию (Mode 1).
* **Q3: Должен ли `kb_lint.py` блокировать пайплайн при дрифте спецификации?**
  * **Решение:** Нет. Чтобы исключить враждебный DX (Hostile Tooling), линтер выдает **неблокирующее предупреждение (Warning)**, если в `Roadmap.md` закрыты 2+ фазы, а поле `updated` в `SPEC.md` не менялось со дня создания проекта. Код выхода остается `0`.

---

## 3. Архитектурное влияние и риски (Architectural Impact & Risks)

* **Затрагиваемые компоненты:**
  * `install.py` и `scripts/build_installer.py` — пресет `undecided`, аргумент командной строки `--idea`, шаблон `SPEC.md` со статусом `discovery`.
  * `.agents/skills/kb-research/SKILL.md` — процедура кристаллизации `SPEC.md` и `README.md` при первичном выборе стека.
  * `.agents/skills/kb-complete/SKILL.md` — шаг синхронизации `SPEC.md` / `README.md` при изменении публичных API или архитектуры.
  * `.agents/skills/kb-release/SKILL.md` — префлайт-чеки актуальности `README.md` и `SPEC.md`.
  * `AGENTS.md` — Living Spec Invariant в блоке правил.
  * `scripts/kb_lint.py` — эвристический аудит актуальности `SPEC.md` (warning).
  * `tests/test_installer.py`, `tests/test_kb_lint.py` — автоматические тесты.
  * `README.md`, `docs/Onboarding.md` — документация сценария Idea-First.

* **Оценка рисков:**
  * Сохраняется принцип Zero Dependencies (стандартная библиотека Python 3).
  * Режим обновления `install.py --update` изолирован: существующие `SPEC.md` и `README.md` никогда не перезаписываются при обновлении.

---

## 4. Высокоуровневая декомпозиция (Task Breakdown)

- [ ] **TASK-029:** Пресет `undecided`, интерактивная опция меню и CLI-флаг `--idea` в `install.py` / `build_installer.py`, генерация `SPEC.md` со статусом `discovery`.
- [ ] **TASK-030:** Протокол Living Spec и синхронизация документации в скиллах `kb-research`, `kb-complete`, `kb-release` и `AGENTS.md` (Living Spec Invariant).
- [ ] **TASK-031:** Эвристический контроль дрифта спецификации в `scripts/kb_lint.py` (неблокирующий warning при отставании `SPEC.md` / `README.md` от фаз Roadmap) и модульные тесты в `tests/test_kb_lint.py`.
- [ ] **TASK-032:** Сборка инсталлятора `build_installer.py`, сквозные E2E тесты нового пресета (`tests/test_installer.py`, `tests/test_kb_lint.py`), обновление `README.md` и `docs/Onboarding.md`.

---

## 5. Критерии приемки плана (Definition of Done для Режима 1)

- [x] Концепция согласована с пользователем (Режим 1: READ-ONLY, без изменения кода проекта).
- [x] Опирается на завершенное исследование [[../../04_Research/RESEARCH-009-greenfield-initialization-and-living-spec-drift|RESEARCH-009]] и принятый стандарт [[../../03_Decisions_ADR/ADR-0014-greenfield-idea-first-initialization-and-living-spec-protocol|ADR-0014]].
- [x] Создан файл плана `docs/02_Tasks/Plans/PLAN-008-greenfield-idea-first-and-living-spec.md`.
- [x] Инициатива промоутирована из Icebox в Фазу 8 в `docs/02_Tasks/Roadmap.md`.
- [x] Задачи `TASK-029` — `TASK-032` добавлены в `docs/02_Tasks/Kanban.md` в колонку `📥 Бэклог`.
- [x] Пройдена проверка целостности базы знаний через `python scripts/kb_lint.py --path docs`.
