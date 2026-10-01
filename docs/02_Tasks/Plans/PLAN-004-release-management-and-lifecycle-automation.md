---
id: PLAN-004
title: "Фаза 4: Релиз-менеджмент и автоматизация жизненного цикла (Dual-Mode Release, /kb-release, SHA-256 & CI)"
status: accepted
type: plan
phase: 4
created: 2026-10-01
updated: 2026-10-01
tags:
  - plan
  - phase4
  - release-management
  - dual-mode
  - github-releases
  - build-hook
  - skills
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 📋 План: PLAN-004 — Фаза 4: Релиз-менеджмент и автоматизация жизненного цикла (Release Management & Lifecycle Automation)

> **ID:** PLAN-004  
> **Статус:** Согласовано (Режим 1)  
> **Теги:** #plan #phase4 #release-management #dual-mode #github-releases #build-hook #skills  
> **Родительская спецификация:** [[../../SPEC|SPEC.md]]  
> **Канбан:** [[../Kanban|Канбан-доска]]  
> **Связанные исследования и ADR:** [[../../04_Research/RESEARCH-002-release-management-and-github-automation|RESEARCH-002: Архитектура подготовки релиза]], [[../../03_Decisions_ADR/ADR-0007-release-management-dual-mode-and-build-hook|ADR-0007: Архитектура релиз-менеджмента]], [[../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001: Zero Dependencies]]  

---

## 1. Контекст и цели (Problem & Goals)

### Проблема
В текущем жизненном цикле Docs-as-Code задачи переходят через 3 режима: `/kb-plan` (Режим 1) $\to$ `/kb-task` (Режим 2) $\to$ `/kb-implement` и `/kb-complete` (Режим 3). Задачи логически сгруппированы в фазы в [[../Roadmap|Дорожной карте]].

Однако в момент закрытия всех задач фазы образуется системный разрыв:
1. **Отсутствие формализованного релизного перехода:** Когда закрывается последняя задача фазы, фаза завершается, но процесс не создает релизный артефакт, не фиксирует Git-тег, не генерирует Release Notes и не формирует дистрибутив.
2. **Дилемма среды (GitHub vs Local-Only):** Проекты с открытым кодом требуют публикации GitHub Release с вложениями (Assets), а локальные или изолированные корпоративные проекты (Local-Only / Offline) не имеют доступа к GitHub, но критически нуждаются в локальной сборке дистрибутива в `dist/` с фиксацией путей и контрольных сумм SHA-256.
3. **Гетерогенность стеков:** Проекты на Swift, Python, TypeScript, .NET собираются разными компиляторами; хардкодить их команды в ядро инсталлятора — анти-паттерн.
4. **Недопустимость неявного авторелиза:** Автоматический триггер релиза внутри `kb-complete` нарушает принцип наименьшего удивления (POLA), блокирует приемочное тестирование (`05_Testing/`) и несет высокий риск публикации дефектов.

### Цель Фазы 4
Создать полноценную, безопасную и управляемую инфраструктуру релиз-менеджмента для проектов Docs-as-Code:
1. Внедрить 12-й исполняемый скилл `/kb-release` с явным вызовом и предварительными проверками (Pre-flight checks).
2. Разработать канонический шаблон `docs/00_Templates/TEMPLATE_RELEASE.md` и постоянный каталог `docs/02_Tasks/Releases/`.
3. Создать легковесную утилиту `scripts/kb_release.py` (Zero Dependencies на Python stdlib) для проверки окружения, сборки артефактов в `dist/`, вычисления SHA-256 и семантической агрегации чейнджлога из `TASK-XXX`, `BUG-XXX` и `ADR-XXXX`.
4. Реализовать контракт сборочного хука (Build Hook Contract: `scripts/build_release.py` или конфиг проекта) и шаблон GitHub Actions CI (`.github/workflows/release.yml`).
5. Интегрировать новый скилл и шаблоны в `install.py` (включая режим `--update`) и провести сквозные E2E тесты.

---

## 2. Обсуждение и ключевые решения (Q&A / Discussion)

* **Q1: Как именно запускается процесс релиза?**
  * **Решение (согласно [[../../03_Decisions_ADR/ADR-0007-release-management-dual-mode-and-build-hook|ADR-0007]]):** Релиз запускается строго явно вызовом `/kb-release <vX.Y.Z>`. В `kb-complete` при закрытии последней задачи фазы выводится неблокирующая подсказка (Nudge) с рекомендацией провести приемочное E2E UX тестирование и запустить `/kb-release`.
* **Q2: Как релиз работает в Local-Only режиме без GitHub?**
  * **Решение:** Утилита `scripts/kb_release.py` проверяет наличие git remote и `gh`. Если проект оффлайн или без remote, активируется `Local-Only Mode`: вызывается локальный сборочный хук, артефакты собираются в `dist/`, вычисляются размеры и SHA-256 хэши, создается постоянный документ `docs/02_Tasks/Releases/RELEASE-vX.Y.Z.md` с точными локальными путями, обновляется `Roadmap.md` и `Devlog.md`.
* **Q3: Как формируются Release Notes без мусорных коммитов Git?**
  * **Решение:** Чейнджлог агрегируется напрямую из семантической базы знаний Docs-as-Code текущей фазы:
    * Новые возможности $\to$ завершенные `TASK-XXX` фазы.
    * Устраненные дефекты $\to$ закрытые `BUG-XXX` фазы.
    * Архитектурные решения $\to$ принятые `ADR-XXXX` фазы.
* **Q4: Как поддерживаются различные сборочные инструменты без раздувания зависимостей?**
  * **Решение:** Принцип *Convention over Configuration*. Все скомпилированные бинарники и пакеты складываются в каталог `dist/`. Утилита релиза ищет сборочный хук (`scripts/build_release.py`, `npm run build`, `dotnet publish -c Release -o ./dist`, `swift build -c release`, `python -m build`). Если хук не найден, создается Source Release с чистым чейнджлогом.

---

## 3. Архитектурное влияние и критический анализ (Architectural Impact & Critical Review)

* **Затрагиваемые компоненты:**
  * `docs/00_Templates/TEMPLATE_RELEASE.md` — новый канонический шаблон релиза с таблицей артефактов и контрольными суммами.
  * `docs/02_Tasks/Releases/` — новая постоянная директория базы знаний.
  * `.agents/skills/kb-release/SKILL.md` — 12-й скилл агентного харнесса.
  * `.agents/skills/kb-complete/SKILL.md` — добавление подсказки о завершении фазы (Nudge).
  * `scripts/kb_release.py` — утилита релиз-менеджмента на стандартной библиотеке Python 3.
  * `.github/workflows/release.yml` — шаблон GitHub Actions для облачной публикации по тегам `v*`.
  * `scripts/build_installer.py` и `install.py` — упаковка нового скилла, шаблона и поддержка в механизме обновления `--update`.
  * `tests/test_installer.py` — E2E тесты нового скилла и релизных компонентов.
* **Оценка рисков и соблюдение стандартов:**
  * Соблюдение [[../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001: Zero Dependencies]] — никаких внешних утилит (Node/Go), только Python stdlib и нативный Git/`gh`.
  * Принцип неизменяемости ссылок (Permalinks) — файлы `RELEASE-vX.Y.Z.md` не перемещаются и не удаляются.
  * Изоляция сбоев (Blast Radius) — сбой сборщика или отсутствие сети не ломает состояние завершенных задач.

---

## 4. Высокоуровневая декомпозиция (Task Breakdown)

- [ ] **TASK-013:** Канонический шаблон `TEMPLATE_RELEASE.md`, каталог `docs/02_Tasks/Releases/` и утилита `scripts/kb_release.py` (Zero-Deps: инспекция артефактов `dist/`, SHA-256, автогенерация чейнджлога).
- [ ] **TASK-014:** Исполняемый скилл `.agents/skills/kb-release/SKILL.md` (Dual-Mode workflow, префлайт-чеки, интеграция навигационных подсказок в `kb-complete`).
- [ ] **TASK-015:** Шаблон GitHub Actions CI `.github/workflows/release.yml` и упаковка в инсталлятор `install.py` / `build_installer.py` (включая режим `--update`).
- [ ] **TASK-016:** Комплексное E2E тестирование релизного пайплайна (Local-Only и GitHub имитация), обновление документации (`README.md`, `Onboarding.md`, `00_Index.md`).

---

## 5. Критерии приемки плана (Definition of Done для Режима 1)

- [x] Концепция согласована с пользователем.
- [x] Опирается на проведенное исследование [[../../04_Research/RESEARCH-002-release-management-and-github-automation|RESEARCH-002]] и утвержденный стандарт [[../../03_Decisions_ADR/ADR-0007-release-management-dual-mode-and-build-hook|ADR-0007]].
- [x] Составлена декомпозиция задач `TASK-013` — `TASK-016`.
- [x] Дорожная карта `docs/02_Tasks/Roadmap.md` обновлена (добавлена Фаза 4, очищен Icebox).
- [x] Карточки Фазы 4 добавлены в `docs/02_Tasks/Kanban.md` в колонку `📥 Бэклог`.
- [x] Пройдена проверка целостности базы знаний через `python scripts/kb_lint.py --path docs`.
