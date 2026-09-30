---
id: ROADMAP
title: Дорожная карта разработки (Roadmap)
status: active
type: roadmap
created: 2026-09-30
updated: 2026-09-30
tags:
  - roadmap
  - planning
  - milestones
---

# 🗺️ Дорожная карта разработки (Roadmap)

> **Теги:** #roadmap #planning #milestones  
> **Связанный канбан:** [[Kanban|Канбан-доска]]  
> **Первоисточник:** [[../../SPEC|SPEC.md (Мастер-спецификация)]]  

---

## Фаза 1: Автономный инсталлятор (MVP)
**Цель:** Создать самодостаточную, кроссплатформенную утилиту `install.py` на стандартной библиотеке Python 3, разворачивающую полный харнесс Docs-as-Code за одну команду.

- [x] Ядро инсталлятора и механизм упаковки ресурсов — [[Specs/01_MVP/TASK-001-installer-core-and-bundling|TASK-001]].
- [x] Мульти-стековые шаблоны (Swift/iOS, TypeScript, Python, .NET, Generic) и адаптеры агентов — [[Specs/01_MVP/TASK-002-multi-stack-templates-and-agent-configs|TASK-002]].
- [x] Интерактивный CLI-мастер с флагами командной строки — [[Specs/01_MVP/TASK-003-cli-wizard-and-options|TASK-003]].
- [x] Сквозное E2E тестирование в изолированных каталогах и документация — [[Specs/01_MVP/TASK-004-e2e-testing-and-readme|TASK-004]].

---

## Фаза 2: Расширения и экосистема (Скиллы, мультиязычность и правила агентов)
**Цель:** Интеграция 11 исполняемых скиллов `.agents/skills/`, эталонных правил агентов по канону `remote_notification`, мультиязычности и расширенной матрицы AI-сред.  
**Первоисточник плана:** [[Plans/PLAN-002-full-skills-and-agent-rules-integration|PLAN-002]]

- [x] Исследование экосистемы AI-агентов, IDE и моделей ([[../../04_Research/RESEARCH-001-ai-agent-ecosystem-and-ide-matrix|RESEARCH-001]]) и архитектура мультиязычности — [[Specs/02_Extensions/TASK-005-ai-agent-ecosystem-research-and-multilang|TASK-005]].
- [x] Упаковка всех 11 скиллов `.agents/skills/` в сборщик `build_installer.py` и `install.py` — [[Specs/02_Extensions/TASK-006-skills-packaging-and-deployment|TASK-006]].
- [x] Эталонные правила агентов по канону `remote_notification` (12 дисциплин, языковая параметризация, роль Senior Partner, отказные ADR, `GEMINI.md`, `.windsurfrules` и адаптеры) — [[Specs/02_Extensions/TASK-007-gold-standard-agent-rules-and-gemini-md|TASK-007]].
- [x] Сквозное E2E тестирование в `tests/test_installer.py` и обновление документации `README.md` (включая быстрый старт для новичков) — [[Specs/02_Extensions/TASK-008-e2e-testing-and-readme-docs|TASK-008]].
- [ ] Шаблон GitHub Actions для автоматического запуска `kb_lint.py` при pull request.
- [ ] Режим обновления (`--update`), аккуратно обновляющий шаблоны без затирания пользовательских задач и планов.

---

## 🔮 Перспективные направления (Future Horizons / Later)
*Идеи и гипотезы, находящиеся на стадии осмысления. Номер фазы и декомпозиция на задачи присваиваются при взятии в активную проработку через Режим 1 (`/kb-plan`).*

* 💡 **Чистая инициализация нового проекта (Clean Slate Scaffolding):** развертывание каркаса харнесса без навязанных фиктивных планов и задач с мгновенным переходом к формулированию реальной идеи пользователя через `/kb-plan`.
* 💡 **Бесшовное подключение к существующим проектам (Brownfield Adoption):** автодетект технологического стека по файлам (`Package.swift`, `package.json`, `pyproject.toml`, `*.sln`), защита существующих файлов от затирания и сценарий экспресс-аудита легаси-архитектуры агентом.
* 💡 **Семантический контроль фаз в kb_lint.py:** автоматический аудит соответствия номеров фаз в ТЗ (`phase: N`), структуры папок (`0N_...`), тегов (`#phaseN`) и карточек Канбана.
* 💡 **Web-визуализатор базы знаний:** встроенный легковесный локальный просмотрщик графа и канбана без Obsidian (`python install.py --serve`).
* 💡 **Автогенерация отчетов для руководства:** утилита сборки статуса Roadmap и Devlog в красивый PDF или Markdown-отчет.
* 💡 **Гайд для начинающих в агентном программировании (Zero-to-Hero Onboarding):** максимально простой и понятный пошаговый туториал по запуску `install.py`, выбору параметров и первым шагам работы с AI-агентами для пользователей без опыта.
* 💡 **Конфигурации для нишевых агентов:** Continue.dev (`.continue/config.json`), Aider (`.aider.conf.yml`).
