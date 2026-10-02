---
kanban-plugin: basic
---

# 📋 Канбан-доска: agent-docs-harness

> **Теги:** #tasks #kanban #planning  
> **Связанная дорожная карта:** [[Roadmap|Дорожная карта]]  
> *Примечание: этот файл открывается в Obsidian через плагин "Kanban" в виде интерактивной доски.*

## 📥 Бэклог (Backlog)

- [ ] [[Plans/PLAN-008-greenfield-idea-first-and-living-spec|План: Фаза 8 — Greenfield-инициализация от идеи (Idea-First) и протокол Living Spec]] #plan #phase8 #greenfield #living-spec
  - [ ] [[Specs/08_Greenfield/TASK-032-installer-bundling-and-e2e-verification|TASK-032]]: Сборка инсталлятора `build_installer.py`, сквозные E2E тесты нового пресета, обновление `README.md` и `docs/Onboarding.md` #task #phase8

## ⏳ В работе (In Progress)

- [ ] [[Specs/08_Greenfield/TASK-031-kb-lint-spec-drift-audit|TASK-031]]: Эвристический контроль дрифта спецификации в `scripts/kb_lint.py` и модульные тесты в `tests/test_kb_lint.py` #task #phase8

## ✅ Готово (Done)

- [x] [[Specs/08_Greenfield/TASK-030-living-spec-protocol-and-skill-sync|TASK-030]]: Протокол Living Spec и синхронизация документации в скиллах `kb-research`, `kb-complete`, `kb-release` и `AGENTS.md` (2026-10-02) #task #phase8
- [x] [[Specs/08_Greenfield/TASK-029-undecided-preset-and-idea-flag|TASK-029]]: Пресет `undecided`, интерактивная опция меню и CLI-флаг `--idea` в `install.py` / `build_installer.py`, генерация `SPEC.md` со статусом `discovery` (2026-10-02) #task #phase8

- [x] [[Plans/PLAN-007-github-release-notes-and-distribution-standard|План: Фаза 7 — Стандарт оформления публичных релизов на GitHub и экспорт Release Notes]] (2026-10-01) #plan #phase7 #release
  - [x] [[Specs/07_Distribution/TASK-028-installer-bundling-and-e2e-verification|TASK-028]]: Сборка инсталлятора `build_installer.py`, регрессионные E2E тесты (`test_installer.py`, `test_kb_release.py`) и аудит `kb_lint.py` (2026-10-01) #task #phase7
  - [x] [[Specs/07_Distribution/TASK-027-kb-release-skill-and-notes-file|TASK-027]]: Актуализация скилла `.agents/skills/kb-release/SKILL.md` (флаг `--notes-file dist/RELEASE_NOTES.md` и Dual-Export шаги) (2026-10-01) #task #phase7
  - [x] [[Specs/07_Distribution/TASK-026-github-actions-release-body-and-installer-template|TASK-026]]: Автоматизация передачи заметок в `.github/workflows/release.yml` (`body_path: dist/RELEASE_NOTES.md`) и синхронизация встроенного шаблона в `install.py` (2026-10-01) #task #phase7
  - [x] [[Specs/07_Distribution/TASK-025-dual-export-and-wikilinks-converter|TASK-025]]: Двухформатный экспорт и автоконвертер викиссылок в `scripts/kb_release.py`, модульные тесты в `tests/test_kb_release.py` (2026-10-01) #task #phase7

- [x] [[Plans/PLAN-006-discovery-mode-and-kb-research-lifecycle|План: Фаза 6 — Интеграция этапа исследования (Режим 0: Discovery & Feasibility) и эволюция /kb-research]] (2026-10-01) #plan #phase6 #discovery
  - [x] [[Specs/06_Discovery/TASK-024-installer-sync-and-e2e-verification|TASK-024]]: Синхронизация инсталлятора `install.py` / `build_installer.py`, регрессионные E2E тесты и аудит целостности (2026-10-01) #task #phase6
  - [x] [[Specs/06_Discovery/TASK-023-roadmap-onboarding-templates-update|TASK-023]]: Обновление шаблонов `TEMPLATE_ROADMAP.md`, `TEMPLATE_ONBOARDING.md` и руководства `Onboarding.md` (2026-10-01) #task #phase6
  - [x] [[Specs/06_Discovery/TASK-022-kb-plan-preflight-nudges-and-onboard|TASK-022]]: Префлайт-чеки в `/kb-plan` (Nudge для невалидированных идей) и обновление `/kb-onboard` (4-этапный цикл) (2026-10-01) #task #phase6
  - [x] [[Specs/06_Discovery/TASK-021-kb-research-evolution-and-roadmap-routing|TASK-021]]: Эволюция скилла `.agents/skills/kb-research/SKILL.md` (двухпутевая воронка: Icebox vs Отклоненные ADR) (2026-10-01) #task #phase6

- [x] [[Plans/PLAN-005-high-snr-token-optimization|План: Фаза 5 — Оптимизация токенов и High-SNR архитектура контекста]] (2026-10-01) #plan #phase5 #token-optimization
  - [x] [[Specs/05_TokenOptimization/TASK-020-bundler-update-and-e2e-benchmarks|TASK-020]]: Синхронизация сборщика `scripts/build_installer.py`, `install.py` (`--update`) и E2E тесты (2026-10-01) #task #phase5
  - [x] [[Specs/05_TokenOptimization/TASK-019-anti-echo-and-silent-cli|TASK-019]]: Внедрение правил High-SNR, Anti-Echo и Silent-CLI в `AGENTS.md`, `scripts/kb_lint.py` и `scripts/kb_release.py` (2026-10-01) #task #phase5
  - [x] [[Specs/05_TokenOptimization/TASK-018-skeleton-templates-refactoring|TASK-018]]: Рефакторинг 13 шаблонов `docs/00_Templates/` в компактные каркасы (Skeleton Templates) (2026-10-01) #task #phase5
  - [x] [[Specs/05_TokenOptimization/TASK-017-skills-high-snr-refactoring|TASK-017]]: High-SNR рефакторинг реестра и 12 скиллов `.agents/skills/` (микро-описания, легкий роутер) (2026-10-01) #task #phase5
- [x] [[Plans/PLAN-004-release-management-and-lifecycle-automation|План: Фаза 4 — Релиз-менеджмент и автоматизация жизненного цикла]] (2026-10-01) #plan #phase4 #release
  - [x] [[Specs/04_Releases/TASK-016-e2e-release-pipeline-verification-and-docs|TASK-016]]: Комплексное E2E тестирование релизного пайплайна (Local-Only и GitHub) и обновление документации (2026-10-01) #task #phase4
  - [x] [[Specs/04_Releases/TASK-015-github-actions-release-ci-and-installer-packaging|TASK-015]]: Шаблон GitHub Actions CI `.github/workflows/release.yml` и упаковка в инсталлятор `install.py` / `build_installer.py` (включая `--update`) (2026-10-01) #task #phase4
  - [x] [[Specs/04_Releases/TASK-014-kb-release-skill-and-complete-nudge|TASK-014]]: Исполняемый скилл `.agents/skills/kb-release/SKILL.md` (Dual-Mode workflow, префлайт-чеки, подсказка в `kb-complete`) (2026-10-01) #task #phase4
  - [x] [[Specs/04_Releases/TASK-013-template-release-and-kb-release-utility|TASK-013]]: Канонический шаблон `TEMPLATE_RELEASE.md`, каталог `docs/02_Tasks/Releases/` и утилита `scripts/kb_release.py` (2026-10-01) #task #phase4
- [x] [[Plans/PLAN-003-brownfield-adoption-and-lifecycle|План: Фаза 3 — Зрелость инсталлятора (Brownfield Adoption, Clean Slate, Обновление и CI)]] (2026-10-01) #plan #phase3
  - [x] [[Specs/03_Adoption/TASK-012-github-actions-ci-and-e2e|TASK-012]]: Шаблон GitHub Actions CI (`.github/workflows/kb-lint.yml`) и E2E тесты (2026-10-01) #task #phase3
  - [x] [[Specs/03_Adoption/TASK-011-safe-update-mechanism|TASK-011]]: Механизм бережного обновления инфраструктуры (`install.py --update`) (2026-10-01) #task #phase3
  - [x] [[Specs/03_Adoption/TASK-010-brownfield-adoption-and-stack-autodetect|TASK-010]]: Бесшовное внедрение в существующие проекты (Brownfield Adoption) и автодетект стека (2026-10-01) #task #phase3
  - [x] [[Specs/03_Adoption/TASK-009-clean-slate-scaffolding|TASK-009]]: Чистый старт и устранение фантомных задач при новой установке (Clean Slate Scaffolding) (2026-10-01) #task #phase3

- [x] [[Plans/PLAN-002-full-skills-and-agent-rules-integration|План: Фаза 2 — Интеграция полного набора скиллов, мультиязычности и правил агентов]] (2026-09-30) #plan #phase2 #skills
  - [x] [[Specs/02_Extensions/TASK-008-e2e-testing-and-readme-docs|TASK-008]]: Обновление E2E тестов и документации README (2026-09-30) #task #phase2
  - [x] [[Specs/02_Extensions/TASK-007-gold-standard-agent-rules-and-gemini-md|TASK-007]]: Эталонные правила агентов по канону remote-notification и генерация GEMINI.md (2026-09-30) #task #phase2
  - [x] [[Specs/02_Extensions/TASK-006-skills-packaging-and-deployment|TASK-006]]: Упаковка всех 11 скиллов .agents/skills/ в сборщик и install.py (2026-09-30) #task #phase2
  - [x] [[Specs/02_Extensions/TASK-005-ai-agent-ecosystem-research-and-multilang|TASK-005]]: Исследование экосистемы AI-агентов (RESEARCH-001) и мультиязычность (--doc-lang) (2026-09-30) #task #phase2
- [x] Инициализация Git-репозитория и структуры базы знаний Docs-as-Code (2026-09-30) #docs
- [x] [[Plans/PLAN-001-crossplatform-installer-architecture|План: Фаза 1 — Архитектура автономного инсталлятора]] (2026-09-30) #plan #phase1
- [x] [[Specs/01_MVP/TASK-001-installer-core-and-bundling|TASK-001]]: Ядро инсталлятора install.py и упаковка ресурсов (2026-09-30) #task #phase1
- [x] [[Specs/01_MVP/TASK-002-multi-stack-templates-and-agent-configs|TASK-002]]: Мульти-стековые шаблоны и адаптеры агентов (2026-09-30) #task #phase1
- [x] [[Specs/01_MVP/TASK-003-cli-wizard-and-options|TASK-003]]: Интерактивный терминальный мастер и CLI флаги (2026-09-30) #task #phase1
- [x] [[Specs/01_MVP/TASK-004-e2e-testing-and-readme|TASK-004]]: E2E верификация песочницы и документация README (2026-09-30) #task #phase1

## 💡 Идеи и гипотезы (Icebox / Future Ideas)

- [ ] Семантический контроль фаз в kb_lint.py: валидация соответствия phase: N, структуры папок 0N_... и тегов #phaseN в frontmatter и Kanban.md (неблокирующие предупреждения) #idea #tooling
- [ ] Простой и понятный гайд для новичков в агентном программировании: пошаговое руководство, как запустить и использовать `install.py` (Zero-to-Hero Onboarding) #idea #docs #onboarding
- [ ] Конфигурации для нишевых агентов: Continue.dev (`.continue/config.json`) и Aider (`.aider.conf.yml`) #idea
- [x] Отклонено: Web-визуализатор базы знаний (`install.py --serve`) — [[../03_Decisions_ADR/ADR-0005-rejection-of-embedded-web-visualizer|ADR-0005]] #rejected
- [x] Отклонено: Автогенерация отчетов для руководства (PDF) — [[../03_Decisions_ADR/ADR-0006-rejection-of-standalone-pdf-report-generator|ADR-0006]] #rejected

