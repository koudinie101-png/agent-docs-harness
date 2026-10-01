---
id: ROADMAP
title: Дорожная карта разработки (Roadmap)
status: active
type: roadmap
created: 2026-09-30
updated: 2026-10-01
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

## Фаза 2: Расширения и экосистема (Скиллы, мультиязычность и правила агентов) — ✅ Завершена
**Цель:** Интеграция 11 исполняемых скиллов `.agents/skills/`, эталонных правил агентов по канону `remote_notification`, мультиязычности и расширенной матрицы AI-сред.  
**Первоисточник плана:** [[Plans/PLAN-002-full-skills-and-agent-rules-integration|PLAN-002]]

- [x] Исследование экосистемы AI-агентов, IDE и моделей ([[../../04_Research/RESEARCH-001-ai-agent-ecosystem-and-ide-matrix|RESEARCH-001]]) и архитектура мультиязычности — [[Specs/02_Extensions/TASK-005-ai-agent-ecosystem-research-and-multilang|TASK-005]].
- [x] Упаковка всех 11 скиллов `.agents/skills/` в сборщик `build_installer.py` и `install.py` — [[Specs/02_Extensions/TASK-006-skills-packaging-and-deployment|TASK-006]].
- [x] Эталонные правила агентов по канону `remote_notification` (12 дисциплин, языковая параметризация, роль Senior Partner, отказные ADR, `GEMINI.md`, `.windsurfrules` и адаптеры) — [[Specs/02_Extensions/TASK-007-gold-standard-agent-rules-and-gemini-md|TASK-007]].
- [x] Сквозное E2E тестирование в `tests/test_installer.py` и обновление документации `README.md` (включая быстрый старт для новичков) — [[Specs/02_Extensions/TASK-008-e2e-testing-and-readme-docs|TASK-008]].

---

## Фаза 3: Зрелость инсталлятора (Brownfield Adoption, Clean Slate, Обновление и CI) — ✅ Завершена
**Цель:** Обеспечить кристально чистый старт без мусорных задач, безопасную интеграцию в существующие репозитории (Brownfield) с автодетектом стека, бережное обновление компонентов харнесса (`install.py --update`) и CI-контроль в GitHub Actions.  
**Первоисточник плана:** [[Plans/PLAN-003-brownfield-adoption-and-lifecycle|PLAN-003]]

- [x] Чистый старт и устранение фантомных задач при новой установке (Clean Slate Scaffolding) — [[Specs/03_Adoption/TASK-009-clean-slate-scaffolding|TASK-009]].
- [x] Бесшовное внедрение в существующие проекты (Brownfield Adoption) и автодетект стека — [[Specs/03_Adoption/TASK-010-brownfield-adoption-and-stack-autodetect|TASK-010]].
- [x] Механизм бережного обновления инфраструктуры (`install.py --update`) — [[Specs/03_Adoption/TASK-011-safe-update-mechanism|TASK-011]].
- [x] Шаблон GitHub Actions CI (`.github/workflows/kb-lint.yml`) и сквозные E2E тесты — [[Specs/03_Adoption/TASK-012-github-actions-ci-and-e2e|TASK-012]].

---

## Фаза 4: Релиз-менеджмент и автоматизация жизненного цикла (Release Management & Lifecycle Automation)
**Цель:** Создать безопасную инфраструктуру выпуска релизов Docs-as-Code: специализированный скилл `/kb-release`, шаблон `TEMPLATE_RELEASE.md`, каталог `docs/02_Tasks/Releases/`, Zero-Deps утилиту `scripts/kb_release.py` (Dual-Mode: GitHub / Local-Only, SHA-256), контракт сборщика `dist/` и шаблон GitHub Actions CI (`.github/workflows/release.yml`).  
**Первоисточник плана:** [[Plans/PLAN-004-release-management-and-lifecycle-automation|PLAN-004]]

- [ ] Шаблон релиза `TEMPLATE_RELEASE.md`, каталог `docs/02_Tasks/Releases/` и утилита `scripts/kb_release.py` (Zero-Deps: SHA-256, сборка, чейнджлог) — [[Specs/04_Releases/TASK-013-template-release-and-kb-release-utility|TASK-013]].
- [ ] Исполняемый скилл `.agents/skills/kb-release/SKILL.md` (Dual-Mode workflow, префлайт-чеки, напоминания в `kb-complete`) — [[Specs/04_Releases/TASK-014-kb-release-skill-and-complete-nudge|TASK-014]].
- [ ] Шаблон GitHub Actions CI `.github/workflows/release.yml` и упаковка в инсталлятор `install.py` / `build_installer.py` — [[Specs/04_Releases/TASK-015-github-actions-release-ci-and-installer-packaging|TASK-015]].
- [ ] Комплексное E2E тестирование релизного пайплайна и обновление документации — [[Specs/04_Releases/TASK-016-e2e-release-pipeline-verification-and-docs|TASK-016]].

---

## 🔮 Перспективные направления (Future Horizons / Icebox)
*Идеи и гипотезы, находящиеся на стадии осмысления. Номер фазы и декомпозиция на задачи присваиваются при взятии в активную проработку через Режим 1 (`/kb-plan`).*

* 💡 **Архитектура каналов обратной связи и воронка триажа (Feedback Loops & Triage Buffer):** интеграция внешнего фидбека в Docs-as-Code: буфер триажа `docs/02_Tasks/Inbox/`, шаблоны GitHub Issue Forms (`.github/ISSUE_TEMPLATE/`) и Discussions (Ideas), безопасный локальный бандл `install.py --report` для друзей и оффлайн-режима, скилл `/kb-triage` — [[../04_Research/RESEARCH-003-feedback-channels-and-triage-pipeline|RESEARCH-003]], [[../03_Decisions_ADR/ADR-0008-feedback-loops-triage-buffer-and-local-diagnostics|ADR-0008]].
* 💡 **Семантический контроль фаз в kb_lint.py:** валидация соответствия номеров фаз в ТЗ (`phase: N`), структуры папок (`0N_...`) и тегов (`#phaseN`) в виде неблокирующих предупреждений (warnings).
* 💡 **Гайд для начинающих в агентном программировании (Zero-to-Hero Onboarding):** подробный пошаговый туториал с примерами диалогов и сценариев использования для новичков.
* 💡 **Конфигурации для нишевых агентов:** Continue.dev (`.continue/config.json`), Aider (`.aider.conf.yml`).

---

## 🚫 Отклоненные архитектурные идеи (Rejected Alternatives)
*Идеи, проанализированные в Режиме 1 и официально отклоненные во избежание оверинжиниринга, раздувания дистрибутива и дублирования сторонних инструментов:*

* ❌ **Встроенный локальный web-визуализатор базы знаний (`install.py --serve`):** отклонен в пользу нативного Obsidian — [[../../03_Decisions_ADR/ADR-0005-rejection-of-embedded-web-visualizer|ADR-0005]].
* ❌ **Встроенный генератор PDF-отчетов для руководства:** отклонен в пользу нативных возможностей агентов и экспорта Markdown — [[../../03_Decisions_ADR/ADR-0006-rejection-of-standalone-pdf-report-generator|ADR-0006]].
