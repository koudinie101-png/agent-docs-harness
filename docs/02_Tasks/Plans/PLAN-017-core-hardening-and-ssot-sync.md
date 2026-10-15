---
id: PLAN-017
title: "Фаза 17: Стабилизация ядра, синхронизация SSOT и защита краевых сценариев (Core Hardening & SSOT Sync)"
status: proposed
type: plan
phase: 17
created: 2026-10-14
updated: 2026-10-15
tags:
  - plan
  - phase17
  - hardening
  - ssot
  - quality-gates
  - tdd
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 📋 План: PLAN-017 — Фаза 17: Стабилизация ядра, синхронизация SSOT и защита краевых сценариев

> **ID:** PLAN-017 | **Статус:** Обсуждение / Согласовано  
> **Фаза:** 17 | **Релиз:** v0.17.0  
> **Спецификация:** [[../../SPEC|SPEC.md]] | **Канбан:** [[../Kanban|Канбан]]  
> **Дорожная карта:** [[../Roadmap|Дорожная карта (Фаза 17)]]  

---

## 1. Контекст и цели (Problem & Goals)

После масштабного расширения возможностей харнесса в фазах 14–16 (протокол Fast-Track, Zero Round-Trip Dispatch, буфер обратной связи Inbox и процедурная память дефектов) аудит кодовой базы выявил ряд скрытых расхождений между спецификацией, документацией и реализацией:
1. **Регрессионные сбои совместимости:** вызовы `Path.is_relative_to` в `scripts/kb_lint.py` ломают декларированную поддержку Python 3.8 (`AttributeError`).
2. **Артефакты релизного цикла:** повторный запуск `scripts/kb_release.py` каталогизирует `dist/RELEASE_NOTES.md` внутрь собственной таблицы SHA-256 артефактов.
3. **Несогласованность CLI:** флаг `--paste` в `scripts/kb_ingest.py` падает при передаче инлайн-текста из-за конфигурации `store_true`.
4. **Утечки в сборщике и fallback-режимах:** в `install.py` локальный режим распаковки без бандла пропускает `docs/06_Memory/patterns.md`, а в `scripts/kb_release.py` жесткая маска `f"0{p}_"` теряет спеки двузначных фаз ($\ge 10$).
5. **Рассинхронизация SSOT (Rule Drift):** генератор `generate_agents_md()` в `install.py` не содержит Режима 0 и Режима 2C, использует устаревшие роботизированные предупреждения вместо Human Guardrails, а документация онбординга указывает 14 шаблонов вместо актуальных 16.

**Цель фазы:** устранить все накопленные дефекты, обеспечить абсолютную стабильность и чистоту SSOT (Single Source of Truth), защитить скрипты от краевых сценариев в контейнерах и CI, подготовив надежную базу для Фазы 18.

---

## 2. Обсуждение и ключевые решения (Q&A)

* **Q1: Какова последовательность выполнения работ в Фазе 17?**
  * **Решение:** Строгое разделение на два этапа в соответствии с инвариантом единичной задачи (Single-Task Barrier):
    1. **Этап 1 (Defect Resolution):** последовательное устранение зарегистрированных дефектов `BUG-005` $\to$ `BUG-006` $\to$ `BUG-007` $\to$ `BUG-008` $\to$ `BUG-009` по строгому TDD-циклу (**RED** $\to$ **GREEN** $\to$ **REFACTOR**).
    2. **Этап 2 (Engineering Hardening):** поочередная спецификация и реализация задач `TASK-066` $\to$ `TASK-067` $\to$ `TASK-068` $\to$ `TASK-069` $\to$ `TASK-070`.

* **Q2: Как обеспечить совместимость с Python 3.8 в `kb_lint.py`?**
  * **Решение:** Внедрить легковесную вспомогательную функцию `_is_relative_to(path, base)` на базе `try: path.resolve().relative_to(base.resolve()); return True except ValueError: return False`. Это сохраняет Zero-Dependencies и на 100% совместимо со стандартом Python 3.8.

* **Q3: Как защитить `kb_release.py` от каталогизации собственных заметок?**
  * **Решение:** В функции `inspect_release_artifacts(dist_dir)` добавить явный фильтр `if item.name == "RELEASE_NOTES.md": continue`, а также регрессионный ассерт `assertNotIn("RELEASE_NOTES.md", ci_notes)` в тестах.

* **Q4: Как унифицировать UX инжеста `--paste` в `kb_ingest.py`?**
  * **Решение:** Сконфигурировать `parser.add_argument("--paste", nargs="?", const=True, default=None)`. Это позволит бесшовно принимать как `scripts/kb_ingest.py --paste "текст"`, так и `scripts/kb_ingest.py --paste --text "текст"`, а также пайпинг `cat error.log | python scripts/kb_ingest.py --paste`.

* **Q5: Как исключить ложные срабатывания линтера на примерах викиссылок в документации?**
  * **Решение:** В `scripts/kb_lint.py` функция `parse_wikilinks(content)` перед применением регулярного выражения должна вырезать все fenced code blocks (```...```) и инлайн-код (`` `...` ``), а также очищать экранирующие обратные слэши от пайпов таблиц Markdown (`\|`).

* **Q6: Какова актуальная таксономия шаблонов базы знаний?**
  * **Решение:** Зафиксировать 16 канонических шаблонов (4 Core Essentials + 12 Advanced Governance):
    - **Core (4):** `SPEC.md`, `Roadmap.md`, `Kanban.md`, `Devlog.md`.
    - **Advanced (12):** `TEMPLATE_PLAN`, `TEMPLATE_TASK`, `TEMPLATE_TASK_MICRO`, `TEMPLATE_BUG`, `TEMPLATE_INCIDENT`, `TEMPLATE_FEEDBACK`, `TEMPLATE_ADR`, `TEMPLATE_RESEARCH`, `TEMPLATE_TEST`, `TEMPLATE_RELEASE`, `TEMPLATE_ROADMAP`, `TEMPLATE_ONBOARDING`.
    Синхронизировать это число в `AGENTS.md`, `install.py`, `kb-onboard/SKILL.md`, `TEMPLATE_ONBOARDING.md`, `docs/Onboarding.md` и ассертах `tests/test_installer.py`.

---

## 3. Архитектурное влияние и риски

* **Принцип Zero-Dependencies:** все изменения в `scripts/*.py` и `install.py` сохраняют опору исключительно на стандартную библиотеку Python 3.8+.
* **Контейнерная безопасность в `install.py`:** проверка открытия `/dev/tty` защищает CI-раннеры и Docker-контейнеры от падений с `EOFError` при установке харнесса через `curl | python3`.
* **Безопасность анонимизации `--report`:** замена `Path.home()` и привязка к границам путей гарантируют, что короткие системные логины (`dev`, `git`, `py`) не повредят произвольный текст отчета (например, `Devlog.md`).
* **Отказ от оверинжиниринга:** предложения о создании отдельного CLI-инструмента `kb_memory.py` отклонены в пользу сохранения компактности ядра (ротация памяти будет реализована процедурно или флагом линтера).

---

## 4. Декомпозиция задач (Task Breakdown)

### 🐞 Дефекты (Mode 2B -> Mode 3 TDD):
- [x] [[Bugs/BUG-005-kb-lint-py38-is-relative-to|BUG-005]]: Замена `Path.is_relative_to()` в `scripts/kb_lint.py` для совместимости с Python 3.8.
- [x] [[Bugs/BUG-006-release-notes-self-artifact|BUG-006]]: Исключение `dist/RELEASE_NOTES.md` из таблицы SHA-256 артефактов при повторном запуске `scripts/kb_release.py`.
- [x] [[Bugs/BUG-007-kb-ingest-paste-inline-arg|BUG-007]]: Поддержка позиционного текста в `scripts/kb_ingest.py --paste "<text>"` и синхронизация с `--text`.
- [x] [[Bugs/BUG-008-local-fallback-patterns-and-phase-pad|BUG-008]]: Добавление `docs/06_Memory/patterns.md` в локальный fallback `unpack_assets()` (`install.py`) и фикс маски фаз `f"{p:02d}_"` в `scripts/kb_release.py`.
- [x] [[Bugs/BUG-009-issue-templates-hardcoded-repo-leak|BUG-009]]: Устранение утечки метаданных и ссылок agent-docs-harness в `.github/ISSUE_TEMPLATE/` при деплое инсталлятора.

### 🛠️ Инженерные задачи фазы (Mode 2 -> Mode 3):
- [x] [[Specs/17_HardeningAndSync/TASK-066-kb-lint-codeblocks-and-schemas|TASK-066]]: Игнорирование кодовых блоков и экранированных пайпов `\|` в `kb_lint.py`, строгая проверка относительных путей и валидация YAML-схем для `06_Memory/Incidents/`.
- [x] [[Specs/17_HardeningAndSync/TASK-067-kb-ingest-yaml-escaping-and-imap-uid|TASK-067]]: Безопасное экранирование кавычек в YAML frontmatter (`FB-*.md`), переход на постоянные IMAP UID (`client.uid`) и URL-кодирование меток GitHub в `kb_ingest.py`.
- [x] [[Specs/17_HardeningAndSync/TASK-068-installer-tty-anonymizer-and-build-hook|TASK-068]]: Защита анонимизатора `--report` по границам путей, проверка открытия `/dev/tty` в контейнерах, диагностика `git commit` и вызов `build_installer.build()` внутри `scripts/build_release.py`.
- [x] [[Specs/17_HardeningAndSync/TASK-069-ssot-agents-and-docs-sync|TASK-069]]: Полная синхронизация `generate_agents_md()` (`install.py`) с корневым `AGENTS.md` (добавление Mode 0 и Mode 2C, Human Guardrails, таксономия 16 шаблонов в `Onboarding` и тестах, ссылки в `CHANGELOG.md`).
- [x] [[Specs/17_HardeningAndSync/TASK-070-skills-templates-and-memory-sync|TASK-070]]: Синхронизация скиллов, шаблонов и контура памяти в `AGENTS.md` (Zero Round-Trip Memory Sync, Stop & Yield в Read-Only скиллах, кастомизация `TEMPLATE_TASK_MICRO.md`, пути `TEMPLATE_RELEASE.md`, таксономия 16 шаблонов и граф).

---

## 5. Критерии приемки плана (DoD Режима 1)

- [x] Концепция и архитектурные решения согласованы (Режим 1: READ-ONLY, без изменения кода).
- [x] Дорожная карта `Roadmap.md` актуализирована (Фаза 17 сформирована, Icebox расширен).
- [x] Дефекты `BUG-005`–`BUG-008` зарегистрированы в `docs/02_Tasks/Bugs/`.
- [x] Карточки добавлены в `docs/02_Tasks/Kanban.md` в секцию `📥 Бэклог`.
- [x] Целостность базы знаний подтверждена через `python scripts/kb_lint.py --path docs` (0 broken links).
- [x] Пользователь подтвердил план для перехода к реализации (`/kb-implement BUG-005`).
