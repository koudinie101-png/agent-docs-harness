---
kanban-plugin: basic
---

# 📋 Канбан-доска: agent-docs-harness

> **Теги:** #tasks #kanban #planning  
> **Связанная дорожная карта:** [[Roadmap|Дорожная карта]]  
> *Примечание: этот файл открывается в Obsidian через плагин "Kanban" в виде интерактивной доски.*

## 📥 Бэклог (Backlog)

- [ ] [[Plans/PLAN-016-self-improving-harness-and-defect-memory|План: Фаза 16 — Самообучающийся харнесс и память дефектов]] #plan #phase16 #memory #defect-loop #quality-gates
  - [ ] [[Specs/16_MemoryAndQualityGates/TASK-061-memory-infrastructure-and-patterns-index|TASK-061]]: Инфраструктура процедурной памяти (`docs/06_Memory/`, шаблон `TEMPLATE_INCIDENT.md` и агрегированный индекс `patterns.md`) #task #phase16 #memory #templates
  - [ ] [[Specs/16_MemoryAndQualityGates/TASK-062-lifecycle-memory-checkpoints-and-promotion|TASK-062]]: Точки чтения памяти в жизненном цикле (`kb-implement`, `kb-complete`) и протокол двухосевого промоушена #task #phase16 #memory #lifecycle #skills
  - [ ] [[Specs/16_MemoryAndQualityGates/TASK-063-quality-gates-tier-matrix-and-agent-rules|TASK-063]]: Слои надежности Quality Gates (Tier 1–3) в `AGENTS.md` и руководстве `Onboarding.md` #task #phase16 #quality-gates #agents #rules
  - [ ] [[Specs/16_MemoryAndQualityGates/TASK-064-kb-lint-memory-audit-bundler-and-e2e|TASK-064]]: Контроль лимита памяти в `scripts/kb_lint.py`, бандлинг `install.py`, E2E тесты и Living Spec sync #task #phase16 #lint #installer #e2e
 
 
## ✅ Готово (Done)

- [x] [[Bugs/BUG-003-release-silent-local-fallback-missing-gh|BUG-003]]: Бесшумный откат в локальный режим при отсутствии GitHub CLI (gh) в kb-release (2026-10-12) #bug #release #cli
- [x] [[Bugs/BUG-004-release-notes-changelog-self-link|BUG-004]]: Циклическая ссылка на саму себя в блоке Full Changelog релизных записок (2026-10-12) #bug #release
- [x] [[Bugs/BUG-002-release-notes-hardcoded-install-script|BUG-002]]: Хардкод установки harness-а (install.py) в публичных релизных записках scripts/kb_release.py (2026-10-12) #bug #release
- [x] [[Plans/PLAN-015-response-latency-and-channel-transparency|План: Фаза 15 — Устранение задержек отклика и прозрачность каналов]] (2026-10-12) #plan #phase15 #latency #dispatch #channel-transparency #kb-lint
  - [x] [[Specs/15_LatencyAndChannels/TASK-060-installer-bundling-e2e-and-living-spec|TASK-060]]: Синхронизация инсталлятора install.py / build_installer.py, регрессионные E2E тесты и актуализация Living Spec (2026-10-12) #task #phase15 #installer #e2e #spec

- [x] [[Specs/15_LatencyAndChannels/TASK-059-channel-triage-feedback-and-phase-consistency-lint|TASK-059]]: Прозрачный фидбек источников в /kb-triage и семантический контроль фаз в scripts/kb_lint.py (2026-10-12) #task #phase15 #triage #lint #semantics
- [x] [[Specs/15_LatencyAndChannels/TASK-058-channel-transparency-git-remote-and-status-dashboard|TASK-058]]: Прозрачный UX инжеста, автодетект Git Remote и дашборд статуса источников в scripts/kb_ingest.py (2026-10-12) #task #phase15 #ingestion #git-remote #transparency
- [x] [[Specs/15_LatencyAndChannels/TASK-057-zero-roundtrip-dispatch-and-hot-invariants|TASK-057]]: Архитектура Zero Round-Trip Dispatch и горячие инварианты в правилах агентов (2026-10-12) #task #phase15 #latency #dispatch #rules
- [x] [[Plans/PLAN-014-agile-docs-as-code-and-chat-first-dx|План: Фаза 14 — Продуктовый DX, протокол Fast-Track и адаптация для вайбкодеров]] (2026-10-12) #plan #phase14 #dx #fast-track #vibe-coding
  - [x] [[Specs/14_AgileDX/TASK-056-installer-bundling-e2e-and-living-spec|TASK-056]]: Синхронизация инсталлятора install.py / build_installer.py, E2E тесты и актуализация Living Spec (2026-10-12) #task #phase14 #installer #e2e
  - [x] [[Specs/14_AgileDX/TASK-055-human-first-release-notes-and-lint-audit|TASK-055]]: Human-First чейнджлоги в scripts/kb_release.py и аудит Fast-Track в scripts/kb_lint.py (2026-10-12) #task #phase14 #release #lint
  - [x] [[Specs/14_AgileDX/TASK-054-zero-to-hero-guide-and-mentor-onboarding|TASK-054]]: Практический гайд Zero_To_Hero_Guide.md («Вайбкодинг со страховкой») и менторский онбординг в kb-onboard (2026-10-12) #task #phase14 #onboarding #vibe-coding
  - [x] [[Specs/14_AgileDX/TASK-053-human-guardrails-and-agent-rules|TASK-053]]: Принцип «Направляй, а не блокируй» (Human Guardrails) в AGENTS.md и адаптерах (2026-10-12) #task #phase14 #agents #guardrails
  - [x] [[Specs/14_AgileDX/TASK-052-micro-spec-template-and-fast-track-skills|TASK-052]]: Шаблон Micro-Spec TEMPLATE_TASK_MICRO.md и поддержка Fast-Track в kb-task / kb-plan (2026-10-12) #task #phase14 #templates #fast-track

- [x] [[Plans/PLAN-013-rules-layering-thin-forwarders-and-obsidian-taxonomy|План: Фаза 13 — Слоистая архитектура правил, тонкие адаптеры и таксономия базы знаний]] (2026-10-11) #plan #phase13 #rules #adapters #obsidian-graph
  - [x] [[Specs/13_RulesLayering/TASK-051-bundling-e2e-tests-and-living-spec|TASK-051]]: Сборка инсталлятора build_installer.py, сквозные E2E тесты и актуализация Living Spec (2026-10-11) #task #phase13 #installer #e2e #spec
  - [x] [[Specs/13_RulesLayering/TASK-050-consolidate-onboard-and-template-taxonomy|TASK-050]]: Консолидация docs-as-code и kb-onboard, двухуровневая таксономия шаблонов в Onboarding.md (2026-10-11) #task #phase13 #skills #onboarding #templates
  - [x] [[Specs/13_RulesLayering/TASK-049-thin-forwarders-adapters-generator|TASK-049]]: Реализация паттерна Thin Forwarders в генераторах адаптеров install.py (2026-10-11) #task #phase13 #installer #adapters #thin-forwarders
  - [x] [[Specs/13_RulesLayering/TASK-048-clean-agents-md-and-obsidian-taxonomy|TASK-048]]: Очистка AGENTS.md от графового шума и изоляция таксономии Obsidian Graph в .obsidian/graph.json (2026-10-11) #task #phase13 #agents #obsidian-graph

- [x] [[Plans/PLAN-012-feedback-ingestion-and-triage-buffer|План: Фаза 12 — Воронка каналов обратной связи, автоматизация импорта и буфер триажа]] (2026-10-11) #plan #phase12 #feedback #triage #ingestion
  - [x] [[Specs/12_FeedbackIngestion/TASK-047-installer-diagnostics-bundling-and-e2e|TASK-047]]: Диагностический модуль install.py --report, синхронизация сборщика и E2E тесты (2026-10-11) #task #phase12 #diagnostics #installer #e2e
  - [x] [[Specs/12_FeedbackIngestion/TASK-046-kb-triage-skill-and-agent-rules|TASK-046]]: Исполняемый скилл /kb-triage и интеграция в правила агентов (2026-10-11) #task #phase12 #skill #triage
  - [x] [[Specs/12_FeedbackIngestion/TASK-045-github-issue-forms-and-cloud-sync-workflow|TASK-045]]: GitHub Issue Forms и облачный workflow кросс-агентной синхронизации (2026-10-11) #task #phase12 #github #actions
  - [x] [[Specs/12_FeedbackIngestion/TASK-044-zero-deps-kb-ingest-script-and-tests|TASK-044]]: Zero-Dependencies модуль импорта обратной связи (scripts/kb_ingest.py) и тесты (2026-10-11) #task #phase12 #ingestion #python-stdlib
  - [x] [[Specs/12_FeedbackIngestion/TASK-043-triage-buffer-template-feedback-and-kb-lint|TASK-043]]: Буфер триажа, шаблон TEMPLATE_FEEDBACK и аудит в kb_lint.py (2026-10-11) #task #phase12 #templates #lint

- [x] [[Plans/PLAN-011-bug-lifecycle-triage-and-release-targeting|План: Фаза 11 — Жизненный цикл дефектов, прозрачный триаж и релизный таргетинг]] (2026-10-11) #plan #phase11 #bug-lifecycle #triage #release-targeting
  - [x] [[Specs/11_BugLifecycle/TASK-042-installer-bundling-e2e-and-docs|TASK-042]]: Синхронизация инсталлятора, сквозные E2E тесты и документация (2026-10-11) #task #phase11
  - [x] [[Specs/11_BugLifecycle/TASK-041-kb-release-defect-filtering-and-blockers|TASK-041]]: Релизный таргетинг и фильтрация дефектов в scripts/kb_release.py и тесты (2026-10-11) #task #phase11 #bug-lifecycle #release-targeting #blockers
  - [x] [[Specs/11_BugLifecycle/TASK-040-kb-implement-bug-lifecycle-and-tdd|TASK-040]]: Нативная поддержка дефектов в kb-implement (/kb-implement BUG-XXX и строгий TDD-цикл) (2026-10-11) #task #phase11 #bug-lifecycle #tdd #implementation
  - [x] [[Specs/11_BugLifecycle/TASK-039-template-bug-and-kb-bug-triage-skill|TASK-039]]: Рефакторинг TEMPLATE_BUG.md и скилла kb-bug (строгий триаж Режима 2B и терминальный Stop & Yield) (2026-10-11) #task #phase11 #bug-triage #templates #stop-yield

- [x] [[Plans/PLAN-010-spec-genesis-and-high-snr-release-notes|План: Фаза 10 — Рождение Мастер-Спецификации (Spec Genesis) и High-SNR релизные заметки]] (2026-10-03) #plan #phase10 #spec-genesis #release-notes
  - [x] [[Specs/10_SpecLifecycle/TASK-038-installer-bundling-e2e-and-docs|TASK-038]]: Синхронизация инсталлятора, сквозные E2E тесты и документация (install.py, README.md, Onboarding.md) (2026-10-03) #task #phase10
  - [x] [[Specs/10_SpecLifecycle/TASK-037-high-snr-release-notes-and-phase-adr-scoping|TASK-037]]: High-SNR Release Notes Generator & Phase ADR Scoping (scripts/kb_release.py, kb-release, TEMPLATE_RELEASE.md) (2026-10-03) #task #phase10 #release-notes #high-snr
  - [x] [[Specs/10_SpecLifecycle/TASK-036-spec-genesis-and-zero-state-guardrails|TASK-036]]: Spec Genesis Protocol & Zero-State Guardrails (kb-init, kb-plan, kb-task, AGENTS.md) (2026-10-03) #task #phase10 #spec-genesis #guardrails

- [x] [[Plans/PLAN-009-single-task-barrier-and-stop-on-complete|План: Фаза 9 — Барьер единичной задачи и протокол гарантированной остановки]] (2026-10-03) #plan #phase9 #agent-governance #guardrails
  - [x] [[Specs/09_Guardrails/TASK-035-installer-bundling-e2e-and-docs|TASK-035]]: Синхронизация инсталлятора `install.py` / `build_installer.py` (включая `--update`), сквозные E2E тесты в `tests/test_installer.py`, обновление `README.md` и `docs/Onboarding.md` (2026-10-03) #task #phase9
  - [x] [[Specs/09_Guardrails/TASK-034-devlog-semantic-guard-and-kb-lint-audit|TASK-034]]: Семантический протокол следующего шага в `TEMPLATE_DEVLOG.md`, аудит формулировок `check_devlog_semantic_guard` в `scripts/kb_lint.py` и тесты в `tests/test_kb_lint.py` (2026-10-03) #task #phase9
  - [x] [[Specs/09_Guardrails/TASK-033-single-task-barrier-and-stop-yield-skills|TASK-033]]: Нормативный инвариант барьера единичной задачи в `AGENTS.md` и терминальный шаг `Stop & Yield Control` в `kb-implement` и `kb-complete` (2026-10-03) #task #phase9

- [x] [[Bugs/BUG-001-ci-release-notes-phase-fallback|BUG-001]]: Рассинхронизация номера фазы и описания релиза в CI release.yml (fallback на Фазу 1) (2026-10-02) #bug #release #ci

- [x] [[Plans/PLAN-008-greenfield-idea-first-and-living-spec|План: Фаза 8 — Greenfield-инициализация от идеи (Idea-First) и протокол Living Spec]] (2026-10-02) #plan #phase8 #greenfield #living-spec
  - [x] [[Specs/08_Greenfield/TASK-032-installer-bundling-and-e2e-verification|TASK-032]]: Сборка инсталлятора `build_installer.py`, сквозные E2E тесты нового пресета, обновление `README.md` и `docs/Onboarding.md` (2026-10-02) #task #phase8
  - [x] [[Specs/08_Greenfield/TASK-031-kb-lint-spec-drift-audit|TASK-031]]: Эвристический контроль дрифта спецификации в `scripts/kb_lint.py` и модульные тесты в `tests/test_kb_lint.py` (2026-10-02) #task #phase8
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
- [ ] Адаптация для вайбкодеров и новичков (Chat-First DX & Protected Vibe Coding): устранение барьеров отпугивания пользователей, One-Prompt старт в чате, гайд и диалоговый ментор — [[../04_Research/RESEARCH-017-vibe-coder-dx-and-chat-first-onboarding|RESEARCH-017]], [[../03_Decisions_ADR/ADR-0022-chat-first-vibe-coder-dx-and-human-guardrails|ADR-0022]] #idea #dx #onboarding #vibe-coding
- [ ] Конфигурации для нишевых агентов: Continue.dev (`.continue/config.json`) и Aider (`.aider.conf.yml`) #idea
- [x] Отклонено: Web-визуализатор базы знаний (`install.py --serve`) — [[../03_Decisions_ADR/ADR-0005-rejection-of-embedded-web-visualizer|ADR-0005]] #rejected
- [x] Отклонено: Автогенерация отчетов для руководства (PDF) — [[../03_Decisions_ADR/ADR-0006-rejection-of-standalone-pdf-report-generator|ADR-0006]] #rejected

