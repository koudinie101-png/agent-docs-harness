---
id: ROADMAP
title: Дорожная карта разработки (Roadmap)
status: active
type: roadmap
created: 2026-09-30
updated: 2026-10-18
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

- [x] Шаблон релиза `TEMPLATE_RELEASE.md`, каталог `docs/02_Tasks/Releases/` и утилита `scripts/kb_release.py` (Zero-Deps: SHA-256, сборка, чейнджлог) — [[Specs/04_Releases/TASK-013-template-release-and-kb-release-utility|TASK-013]].
- [x] Исполняемый скилл `.agents/skills/kb-release/SKILL.md` (Dual-Mode workflow, префлайт-чеки, напоминания в `kb-complete`) — [[Specs/04_Releases/TASK-014-kb-release-skill-and-complete-nudge|TASK-014]].
- [x] Шаблон GitHub Actions CI `.github/workflows/release.yml` и упаковка в инсталлятор `install.py` / `build_installer.py` — [[Specs/04_Releases/TASK-015-github-actions-release-ci-and-installer-packaging|TASK-015]].
- [x] Комплексное E2E тестирование релизного пайплайна и обновление документации — [[Specs/04_Releases/TASK-016-e2e-release-pipeline-verification-and-docs|TASK-016]].

---

## Фаза 5: Оптимизация токенов и High-SNR архитектура контекста (Token Efficiency & Context Compression) — ✅ Завершена
**Цель:** Сократить контекстную нагрузку на 55–65% за сессию: перевести 12 скиллов и 13 шаблонов на High-SNR императивные примитивы, сжать Always-On реестр описаний скиллов (-53%), внедрить Anti-Echo протокол, рефакторить монолит `docs-as-code` в легковесный роутер и обеспечить лаконичный Silent-on-Success CLI.  
**Первоисточник плана:** [[Plans/PLAN-005-high-snr-token-optimization|PLAN-005]]  
**Официальный релиз:** [[Releases/RELEASE-v0.5.0|RELEASE-v0.5.0]]

- [x] High-SNR рефакторинг реестра и 12 скиллов `.agents/skills/` (микро-описания, устранение дублирования, легкий роутер) — [[Specs/05_TokenOptimization/TASK-017-skills-high-snr-refactoring|TASK-017]].
- [x] Рефакторинг 13 шаблонов `docs/00_Templates/` в компактные каркасы (Skeleton Templates) — [[Specs/05_TokenOptimization/TASK-018-skeleton-templates-refactoring|TASK-018]].
- [x] Внедрение правил High-SNR, Anti-Echo и Silent-CLI в `AGENTS.md`, `scripts/kb_lint.py` и `scripts/kb_release.py` — [[Specs/05_TokenOptimization/TASK-019-anti-echo-and-silent-cli|TASK-019]].
- [x] Синхронизация сборщика `scripts/build_installer.py`, `install.py` (`--update`), E2E тесты и замеры сжатия — [[Specs/05_TokenOptimization/TASK-020-bundler-update-and-e2e-benchmarks|TASK-020]].

---

## Фаза 6: Интеграция этапа исследования (Режим 0: Discovery & Feasibility) и эволюция /kb-research — ✅ Завершена
**Цель:** Замкнуть сквозной жизненный цикл разработки (модель Double Diamond: Discovery + Delivery), эволюционировать скилл `/kb-research` в инструмент стресс-тестирования продуктово-архитектурных гипотез с автоматической воронкой регистрации в `Roadmap.md` (Icebox vs отказные ADR), внедрить префлайт-чеки в `/kb-plan` и актуализировать онбординг.  
**Первоисточник плана:** [[Plans/PLAN-006-discovery-mode-and-kb-research-lifecycle|PLAN-006]]  
**Официальный релиз:** [[Releases/RELEASE-v0.6.0|RELEASE-v0.6.0]]  
**Нормативная база:** [[../04_Research/RESEARCH-007-discovery-mode-and-kb-research-lifecycle-integration|RESEARCH-007]], [[../03_Decisions_ADR/ADR-0012-discovery-mode-and-kb-research-lifecycle-integration|ADR-0012]]

- [x] Эволюция скилла `.agents/skills/kb-research/SKILL.md` (двухпутевая воронка: Icebox vs Отклоненные ADR) — [[Specs/06_Discovery/TASK-021-kb-research-evolution-and-roadmap-routing|TASK-021]].
- [x] Префлайт-чеки в `/kb-plan` (Nudge для невалидированных идей) и обновление `/kb-onboard` (4-этапный цикл) — [[Specs/06_Discovery/TASK-022-kb-plan-preflight-nudges-and-onboard|TASK-022]].
- [x] Обновление шаблонов `TEMPLATE_ROADMAP.md`, `TEMPLATE_ONBOARDING.md` и руководства `Onboarding.md` — [[Specs/06_Discovery/TASK-023-roadmap-onboarding-templates-update|TASK-023]].
- [x] Синхронизация инсталлятора `install.py` / `build_installer.py`, регрессионные E2E тесты и аудит целостности — [[Specs/06_Discovery/TASK-024-installer-sync-and-e2e-verification|TASK-024]].

---

## Фаза 7: Стандарт оформления публичных релизов на GitHub и экспорт Release Notes — ✅ Завершена
**Цель:** Автоматизировать выпуск релизов на GitHub без ручного вмешательства: двухформатный экспорт в `scripts/kb_release.py` (`RELEASE-vX.Y.Z.md` для базы знаний + `dist/RELEASE_NOTES.md` для внешнего мира), автоконвертер викиссылок в чистый Markdown, передача `body_path` в `.github/workflows/release.yml`, актуализация скилла `/kb-release` и упаковка в инсталлятор `install.py`.  
**Первоисточник плана:** [[Plans/PLAN-007-github-release-notes-and-distribution-standard|PLAN-007]]  
**Нормативная база:** [[../04_Research/RESEARCH-005-github-release-notes-and-distribution-best-practices|RESEARCH-005]], [[../03_Decisions_ADR/ADR-0010-github-release-notes-and-public-distribution-standard|ADR-0010]]  
**Официальный релиз:** [[Releases/RELEASE-v0.7.0|RELEASE-v0.7.0]]

- [x] Двухформатный экспорт и автоконвертер викиссылок в `scripts/kb_release.py` и модульные тесты — [[Specs/07_Distribution/TASK-025-dual-export-and-wikilinks-converter|TASK-025]].
- [x] Автоматизация передачи заметок в `.github/workflows/release.yml` (`body_path: dist/RELEASE_NOTES.md`) и шаблонах инсталлятора — [[Specs/07_Distribution/TASK-026-github-actions-release-body-and-installer-template|TASK-026]].
- [x] Актуализация скилла `.agents/skills/kb-release/SKILL.md` (параметр `--notes-file` и Dual-Export шаги) — [[Specs/07_Distribution/TASK-027-kb-release-skill-and-notes-file|TASK-027]].
- [x] Сборка инсталлятора `build_installer.py`, регрессионные E2E тесты и аудит целостности базы знаний — [[Specs/07_Distribution/TASK-028-installer-bundling-and-e2e-verification|TASK-028]].

---

## Фаза 8: Greenfield-инициализация от идеи (Idea-First) и протокол Living Spec — ✅ Завершена
**Цель:** Обеспечить старт проектов с чистого листа от одной вербальной идеи (`install.py --idea "..."` с пресетом `undecided`), сквозную кристаллизацию `SPEC.md` и `README.md` по итогам Режима 0 (`/kb-research`), закрепить Living Spec Invariant в скиллах и эвристический аудит дрифта спецификации в `kb_lint.py`.  
**Первоисточник плана:** [[Plans/PLAN-008-greenfield-idea-first-and-living-spec|PLAN-008]]  
**Нормативная база:** [[../04_Research/RESEARCH-009-greenfield-initialization-and-living-spec-drift|RESEARCH-009]], [[../03_Decisions_ADR/ADR-0014-greenfield-idea-first-initialization-and-living-spec-protocol|ADR-0014]]  
**Официальный релиз:** [[Releases/RELEASE-v0.8.0|RELEASE-v0.8.0]]

- [x] Пресет `undecided`, интерактивная опция меню и CLI-флаг `--idea` в `install.py` / `build_installer.py`, генерация `SPEC.md` со статусом `discovery` — [[Specs/08_Greenfield/TASK-029-undecided-preset-and-idea-flag|TASK-029]].
- [x] Протокол Living Spec и синхронизация документации в скиллах `kb-research`, `kb-complete`, `kb-release` и `AGENTS.md` — [[Specs/08_Greenfield/TASK-030-living-spec-protocol-and-skill-sync|TASK-030]].
- [x] Эвристический контроль дрифта спецификации в `scripts/kb_lint.py` и модульные тесты в `tests/test_kb_lint.py` — [[Specs/08_Greenfield/TASK-031-kb-lint-spec-drift-audit|TASK-031]].
- [x] Сборка инсталлятора `build_installer.py`, сквозные E2E тесты нового пресета, обновление `README.md` и `docs/Onboarding.md` — [[Specs/08_Greenfield/TASK-032-installer-bundling-and-e2e-verification|TASK-032]].

---

## Фаза 9: Барьер единичной задачи и протокол гарантированной остановки (Single-Task Execution Barrier & Stop-on-Complete Protocol) — ✅ Завершена
**Цель:** Исключить своевольный авто-чейнинг задач (Eager Task Chaining) при сжатии контекста с помощью трехуровневой эшелонированной защиты: нормативного инварианта в `AGENTS.md`, терминального шага `Stop & Yield Control` в `kb-implement`/`kb-complete`, семантического разделения субъекта в `Devlog.md` и неблокирующего аудита в `scripts/kb_lint.py`.  
**Первоисточник плана:** [[Plans/PLAN-009-single-task-barrier-and-stop-on-complete|PLAN-009]]  
**Нормативная база:** [[../04_Research/RESEARCH-012-single-task-execution-barrier-and-autonomous-pipeline-containment|RESEARCH-012]], [[../03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]]  
**Официальный релиз:** [[Releases/RELEASE-v0.10.0|RELEASE-v0.10.0 (Кумулятивный)]]

- [x] Нормативный инвариант барьера единичной задачи в `AGENTS.md` и терминальный шаг `Stop & Yield Control` в `kb-implement` и `kb-complete` — [[Specs/09_Guardrails/TASK-033-single-task-barrier-and-stop-yield-skills|TASK-033]].
- [x] Семантический протокол следующего шага в `TEMPLATE_DEVLOG.md`, аудит формулировок `check_devlog_semantic_guard` в `scripts/kb_lint.py` и тесты в `tests/test_kb_lint.py` — [[Specs/09_Guardrails/TASK-034-devlog-semantic-guard-and-kb-lint-audit|TASK-034]].
- [x] Синхронизация инсталлятора `install.py` / `build_installer.py` (включая `--update`), сквозные E2E тесты в `tests/test_installer.py`, обновление `README.md` и `docs/Onboarding.md` — [[Specs/09_Guardrails/TASK-035-installer-bundling-e2e-and-docs|TASK-035]].

---

## Фаза 10: Рождение Мастер-Спецификации (Spec Genesis) и High-SNR релизные заметки (Spec Genesis Protocol & High-SNR Release Notes) — ✅ Завершена
**Цель:** Создать замкнутый контур чистоты спецификаций и релизных артефактов: устранить рассинхронизацию `kb-init` и `install.py` при рождении `SPEC.md`, внедрить префлайт-чеки Zero-State в `kb-plan` и `kb-task`, закрепить инвариант защиты от галлюцинаций в `AGENTS.md` ([[../03_Decisions_ADR/ADR-0018-spec-genesis-protocol-and-zero-state-handling|ADR-0018]]), и исключить кумулятивный шум архитектурных решений (ADR) из публичных заметок на GitHub ([[../03_Decisions_ADR/ADR-0017-release-notes-adr-exclusion-and-high-snr-standard|ADR-0017]]).  
**Первоисточник плана:** [[Plans/PLAN-010-spec-genesis-and-high-snr-release-notes|PLAN-010]]  
**Нормативная база:** [[../04_Research/RESEARCH-011-spec-genesis-protocol-and-zero-state-handling|RESEARCH-011]], [[../03_Decisions_ADR/ADR-0018-spec-genesis-protocol-and-zero-state-handling|ADR-0018]], [[../04_Research/RESEARCH-013-release-notes-adr-exclusion-and-high-snr|RESEARCH-013]], [[../03_Decisions_ADR/ADR-0017-release-notes-adr-exclusion-and-high-snr-standard|ADR-0017]]  
**Официальный релиз:** [[Releases/RELEASE-v0.10.0|RELEASE-v0.10.0 (Кумулятивный)]]

- [x] [[Specs/10_SpecLifecycle/TASK-036-spec-genesis-and-zero-state-guardrails|TASK-036]]: Spec Genesis Protocol & Zero-State Guardrails (генерация `SPEC.md` в `kb-init`, префлайт-чеки в `kb-plan`/`kb-task`, инвариант в `AGENTS.md`).
- [x] [[Specs/10_SpecLifecycle/TASK-037-high-snr-release-notes-and-phase-adr-scoping|TASK-037]]: High-SNR Release Notes Generator & Phase ADR Scoping (упразднение секции ADR в `generate_public_release_notes` в `scripts/kb_release.py`, фазовый скоупинг во внутреннем чейнджлоге, обновление `TEMPLATE_RELEASE.md` и `kb-release`, модульные тесты в `tests/test_kb_release.py`).
- [x] [[Specs/10_SpecLifecycle/TASK-038-installer-bundling-e2e-and-docs|TASK-038]]: Синхронизация инсталлятора, сквозные E2E тесты и документация (сборка `install.py` через `scripts/build_installer.py`, регрессионные E2E тесты в `tests/test_installer.py`, аудит `scripts/kb_lint.py`, обновление `README.md` и `docs/Onboarding.md`).

---

## Фаза 11: Жизненный цикл дефектов, прозрачный триаж и релизный таргетинг (Bug Lifecycle & Release Targeting) — ✅ Завершена
**Цель:** Исключить хаотичный фикс багов агентом (Eager Auto-Fixing) за счет изоляции заведения дефектов от их устранения (Режим 2B `kb-bug` со `Stop & Yield`), унифицировать исполнение дефектов в Режиме 3 (`kb-implement BUG-XXX` по циклу TDD), внедрить строгий релизный контракт дефектов (`target_release`, `target_phase`, `release_blocker`, `fixed_in`), устранить утечку старых багов в чейнджлогах релизов GitHub (`scripts/kb_release.py`) и разблокировать воронку входящего фидбека.  
**Первоисточник плана:** [[Plans/PLAN-011-bug-lifecycle-triage-and-release-targeting|PLAN-011]]  
**Нормативная база:** [[../04_Research/RESEARCH-014-bug-lifecycle-triage-and-release-targeting|RESEARCH-014]], [[../03_Decisions_ADR/ADR-0019-bug-lifecycle-triage-and-release-targeting|ADR-0019]]  
**Официальный релиз:** [[Releases/RELEASE-v0.11.0|RELEASE-v0.11.0]]

- [x] Рефакторинг `TEMPLATE_BUG.md` и скилла `kb-bug` (строгий триаж Режима 2B и терминальный `Stop & Yield`) — [[Specs/11_BugLifecycle/TASK-039-template-bug-and-kb-bug-triage-skill|TASK-039]].
- [x] Нативная поддержка дефектов в `kb-implement` (`/kb-implement BUG-XXX` и строгий TDD-цикл) — [[Specs/11_BugLifecycle/TASK-040-kb-implement-bug-lifecycle-and-tdd|TASK-040]].
- [x] Релизный таргетинг и фильтрация дефектов в `scripts/kb_release.py` и тесты — [[Specs/11_BugLifecycle/TASK-041-kb-release-defect-filtering-and-blockers|TASK-041]].
- [x] Синхронизация инсталлятора, сквозные E2E тесты и документация (`install.py`, `README.md`, `SPEC.md`, `Onboarding.md`) — [[Specs/11_BugLifecycle/TASK-042-installer-bundling-e2e-and-docs|TASK-042]].

---

## Фаза 12: Воронка каналов обратной связи, автоматизация импорта и буфер триажа (Feedback Ingestion & Triage Buffer) — ✅ Завершена
**Цель:** Создать безопасный контур приема внешних обращений без риска засорения базы знаний и нарушения Permalinks Principle: буфер `docs/02_Tasks/Inbox/` с шаблоном `TEMPLATE_FEEDBACK.md`, дедупликацию `.inbox_state.json`, автономную Zero-Deps утилиту `scripts/kb_ingest.py` (GitHub Issues, Email IMAP, Quick Paste), декларативные формы `.github/ISSUE_TEMPLATE/`, кросс-агентный Cloud Cron workflow `.github/workflows/feedback-sync.yml`, исполняемый скилл `/kb-triage` с двухстадийной эвристикой и оффлайн-диагностику `install.py --report`.  
**Первоисточник плана:** [[Plans/PLAN-012-feedback-ingestion-and-triage-buffer|PLAN-012]]  
**Нормативная база:** [[../04_Research/RESEARCH-015-feedback-ingestion-channels-and-triage-heuristics|RESEARCH-015]], [[../03_Decisions_ADR/ADR-0020-feedback-ingestion-channels-and-triage-automation|ADR-0020]]

- [x] Буфер триажа, шаблон TEMPLATE_FEEDBACK и аудит в kb_lint.py — [[Specs/12_FeedbackIngestion/TASK-043-triage-buffer-template-feedback-and-kb-lint|TASK-043]].
- [x] Zero-Dependencies модуль импорта обратной связи (`scripts/kb_ingest.py`) и тесты — [[Specs/12_FeedbackIngestion/TASK-044-zero-deps-kb-ingest-script-and-tests|TASK-044]].
- [x] GitHub Issue Forms и облачный workflow кросс-агентной синхронизации — [[Specs/12_FeedbackIngestion/TASK-045-github-issue-forms-and-cloud-sync-workflow|TASK-045]].
- [x] Исполняемый скилл `/kb-triage` и интеграция в правила агентов — [[Specs/12_FeedbackIngestion/TASK-046-kb-triage-skill-and-agent-rules|TASK-046]].
- [x] Диагностический модуль `install.py --report`, синхронизация сборщика и E2E тесты — [[Specs/12_FeedbackIngestion/TASK-047-installer-diagnostics-bundling-and-e2e|TASK-047]].

---

## Фаза 13: Слоистая архитектура правил (Thin Forwarders), декуплинг графа Obsidian и таксономия базы знаний — ✅ Завершена
**Цель:** Оптимизировать распределение правил по слоям L0–L3, устранить двойную инжекцию инструкций (Double Prompt Injection) и Rule Drift через внедрение паттерна Thin Forwarders в адаптерах IDE (`install.py`), вынести цветовую таблицу Obsidian Graph из `AGENTS.md` в `.obsidian/graph.json` (экономия ~150 токенов на шаг диалога), консолидировать навигацию и онбординг (`docs-as-code` $\to$ `kb-onboard`) и зафиксировать двухуровневую таксономию шаблонов (Core Essentials vs Advanced Governance) в руководстве `docs/Onboarding.md`.  
**Первоисточник плана:** [[Plans/PLAN-013-rules-layering-thin-forwarders-and-obsidian-taxonomy|PLAN-013]]  
**Нормативная база:** [[../04_Research/RESEARCH-016-agent-rules-hierarchy-and-knowledge-base-structure|RESEARCH-016]], [[../03_Decisions_ADR/ADR-0021-rules-layering-thin-forwarders-and-obsidian-taxonomy|ADR-0021]]

- [x] [[Specs/13_RulesLayering/TASK-048-clean-agents-md-and-obsidian-taxonomy|TASK-048]]: Очистка `AGENTS.md` от графового шума и изоляция таксономии Obsidian Graph в `.obsidian/graph.json`.
- [x] [[Specs/13_RulesLayering/TASK-049-thin-forwarders-adapters-generator|TASK-049]]: Реализация паттерна Thin Forwarders в генераторах адаптеров `install.py`.
- [x] [[Specs/13_RulesLayering/TASK-050-consolidate-onboard-and-template-taxonomy|TASK-050]]: Консолидация `docs-as-code` и `kb-onboard`, двухуровневая таксономия шаблонов в `Onboarding.md`.
- [x] [[Specs/13_RulesLayering/TASK-051-bundling-e2e-tests-and-living-spec|TASK-051]]: Сборка инсталлятора `build_installer.py`, сквозные E2E тесты и актуализация Living Spec.

---

## Фаза 14: Продуктовый DX, протокол Fast-Track и адаптация для вайбкодеров (Agile Docs-as-Code & Chat-First DX) — ✅ Завершена
**Цель:** Снизить когнитивное и процедурное трение Docs-as-Code: внедрить протокол Fast-Track для микро-задач (пропуск Режима 1, компактная Micro-Spec `TEMPLATE_TASK_MICRO.md`, экономия 70% токенов), принцип «Направляй, а не блокируй» (Human Guardrails) в правилах агентов, Chat-First Bootstrapping в README (запуск без терминала), практическое руководство `Zero_To_Hero_Guide.md` («Вайбкодинг со страховкой»), понятные чейнджлоги в `kb_release.py` и аудит лимитов в `kb_lint.py`.  
**Первоисточник плана:** [[Plans/PLAN-014-agile-docs-as-code-and-chat-first-dx|PLAN-014]]  
**Официальный релиз:** [[Releases/RELEASE-v0.14.0|RELEASE-v0.14.0]]  
**Нормативная база:** [[../04_Research/RESEARCH-018-fast-track-protocol-for-micro-tasks|RESEARCH-018]], [[../03_Decisions_ADR/ADR-0023-fast-track-protocol-for-micro-tasks|ADR-0023]], [[../04_Research/RESEARCH-010-zero-to-hero-onboarding-guide-and-developer-mental-models|RESEARCH-010]], [[../03_Decisions_ADR/ADR-0015-zero-to-hero-onboarding-guide-architecture|ADR-0015]], [[../04_Research/RESEARCH-017-vibe-coder-dx-and-chat-first-onboarding|RESEARCH-017]], [[../03_Decisions_ADR/ADR-0022-chat-first-vibe-coder-dx-and-human-guardrails|ADR-0022]]

- [x] [[Specs/14_AgileDX/TASK-052-micro-spec-template-and-fast-track-skills|TASK-052]]: Шаблон Micro-Spec `TEMPLATE_TASK_MICRO.md` и поддержка Fast-Track в `kb-task` / `kb-plan`.
- [x] [[Specs/14_AgileDX/TASK-053-human-guardrails-and-agent-rules|TASK-053]]: Принцип «Направляй, а не блокируй» (Human Guardrails) в `AGENTS.md` и адаптерах.
- [x] [[Specs/14_AgileDX/TASK-054-zero-to-hero-guide-and-mentor-onboarding|TASK-054]]: Практический гайд `Zero_To_Hero_Guide.md` («Вайбкодинг со страховкой») и менторский онбординг в `kb-onboard`.
- [x] [[Specs/14_AgileDX/TASK-055-human-first-release-notes-and-lint-audit|TASK-055]]: Human-First чейнджлоги в `scripts/kb_release.py` и аудит Fast-Track в `scripts/kb_lint.py`.
- [x] [[Specs/14_AgileDX/TASK-056-installer-bundling-e2e-and-living-spec|TASK-056]]: Синхронизация инсталлятора `install.py` / `build_installer.py`, E2E тесты и актуализация Living Spec.

---

## Фаза 15: Устранение задержек отклика и прозрачность каналов (Response Latency Elimination & Channel Transparency) — ✅ Завершена
**Цель:** Сократить задержку отклика агента в 2.5–3 раза за счет архитектуры Zero Round-Trip Dispatch (Hot Invariants в Always-On `AGENTS.md` без обязательного `view_file(SKILL.md)` для Режимов 0–3), внедрить User-Centric Ingestion & Channel Transparency в `scripts/kb_ingest.py` (Zero-Deps автодетект репозитория из `git remote origin`, флаг `--status`, гибкая фильтрация `--label` / `--all-open`, запрет немых пропусков), актуализировать скилл `/kb-triage`, реализовать семантический контроль фаз в `scripts/kb_lint.py` и упаковать монолитный дистрибутив `install.py` с E2E тестами.  
**Первоисточник плана:** [[Plans/PLAN-015-response-latency-and-channel-transparency|PLAN-015]]  
**Официальный релиз:** [[Releases/RELEASE-v0.15.0|RELEASE-v0.15.0]]  
**Нормативная база:** [[../04_Research/RESEARCH-008-latency-prompt-caching-and-skill-chaining|RESEARCH-008]], [[../03_Decisions_ADR/ADR-0013-zero-roundtrip-dispatch-and-hot-invariants-architecture|ADR-0013]], [[../04_Research/RESEARCH-019-user-centric-ingestion-and-channel-transparency|RESEARCH-019]], [[../03_Decisions_ADR/ADR-0024-user-centric-ingestion-and-channel-transparency|ADR-0024]]

- [x] [[Specs/15_LatencyAndChannels/TASK-057-zero-roundtrip-dispatch-and-hot-invariants|TASK-057]]: Архитектура Zero Round-Trip Dispatch и горячие инварианты в правилах агентов (Hot Invariants & Direct Dispatch).
- [x] [[Specs/15_LatencyAndChannels/TASK-058-channel-transparency-git-remote-and-status-dashboard|TASK-058]]: Прозрачный UX инжеста, автодетект Git Remote и дашборд статуса источников в `scripts/kb_ingest.py`.
- [x] [[Specs/15_LatencyAndChannels/TASK-059-channel-triage-feedback-and-phase-consistency-lint|TASK-059]]: Прозрачный фидбек источников в `/kb-triage` и семантический контроль фаз в `scripts/kb_lint.py`.
- [x] [[Specs/15_LatencyAndChannels/TASK-060-installer-bundling-e2e-and-living-spec|TASK-060]]: Синхронизация инсталлятора `install.py` / `build_installer.py`, регрессионные E2E тесты и актуализация Living Spec.

---

## Фаза 16: Самообучающийся харнесс и память дефектов (Self-Improving Harness & Defect Memory) — ✅ Завершена
**Цель:** Превратить статический харнесс в самообучающуюся систему: устранить амнезию процедурных ошибок агента через двухуровневую память (`docs/06_Memory/`), внедрить жестко лимитированный индекс `patterns.md` ($\le 15$ записей), формализовать слои надежности Quality Gates (Tier 1–3), закрепить точки проверки памяти в жизненном цикле и интегрировать автоматический аудит лимитов в `scripts/kb_lint.py`.  
**Первоисточник плана:** [[Plans/PLAN-016-self-improving-harness-and-defect-memory|PLAN-016]]  
**Официальный релиз:** [[Releases/RELEASE-v0.16.0|RELEASE-v0.16.0]]  
**Нормативная база:** [[../04_Research/RESEARCH-020-self-improving-defect-loop-and-quality-gates|RESEARCH-020]], [[../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]

- [x] [[Specs/16_MemoryAndQualityGates/TASK-061-memory-infrastructure-and-patterns-index|TASK-061]]: Инфраструктура процедурной памяти (`docs/06_Memory/`, шаблон `TEMPLATE_INCIDENT.md` и агрегированный индекс `patterns.md`).
- [x] [[Specs/16_MemoryAndQualityGates/TASK-062-lifecycle-memory-checkpoints-and-promotion|TASK-062]]: Точки чтения памяти в жизненном цикле (`kb-implement`, `kb-complete`) и протокол двухосевого промоушена.
- [x] [[Specs/16_MemoryAndQualityGates/TASK-063-quality-gates-tier-matrix-and-agent-rules|TASK-063]]: Слои надежности Quality Gates (Tier 1–3) в `AGENTS.md` и руководстве `Onboarding.md`.
- [x] [[Specs/16_MemoryAndQualityGates/TASK-064-kb-lint-memory-audit-bundler-and-e2e|TASK-064]]: Контроль лимита памяти в `scripts/kb_lint.py`, бандлинг `install.py`, E2E тесты и Living Spec sync.
- [x] [[Specs/16_MemoryAndQualityGates/TASK-065-align-cli-flags-and-sync-readme|TASK-065]]: Выравнивание CLI-флагов (`-i`, `-r`) и синхронизация `README.md`.

---

## Фаза 17: Стабилизация ядра, синхронизация SSOT и защита краевых сценариев (Core Hardening & SSOT Sync) — ✅ Завершена
**Цель:** Устранение рассинхронизации между корневым `AGENTS.md` и генераторами `install.py`, исправление краевых дефектов линтера/инжестора/релизера и обеспечение 100% совместимости с Python 3.8+.  
**Первоисточник плана:** [[Plans/PLAN-017-core-hardening-and-ssot-sync|PLAN-017]]

### 🐞 Исправление дефектов (Mode 2B -> Mode 3 TDD)
- [x] [[Bugs/BUG-005-kb-lint-py38-is-relative-to|BUG-005]]: Замена `Path.is_relative_to()` в `scripts/kb_lint.py` для совместимости с Python 3.8.
- [x] [[Bugs/BUG-006-release-notes-self-artifact|BUG-006]]: Исключение `dist/RELEASE_NOTES.md` из таблицы SHA-256 артефактов при повторном запуске `scripts/kb_release.py`.
- [x] [[Bugs/BUG-007-kb-ingest-paste-inline-arg|BUG-007]]: Поддержка позиционного текста в `scripts/kb_ingest.py --paste "<text>"` и синхронизация с `--text`.
- [x] [[Bugs/BUG-008-local-fallback-patterns-and-phase-pad|BUG-008]]: Добавление `docs/06_Memory/patterns.md` в локальный fallback `unpack_assets()` (`install.py`) и фикс маски фаз `f"{p:02d}_"` в `scripts/kb_release.py`.
- [x] [[Bugs/BUG-009-issue-templates-hardcoded-repo-leak|BUG-009]]: Устранение утечки метаданных и ссылок agent-docs-harness в `.github/ISSUE_TEMPLATE/` при деплое инсталлятора.

### 🛠️ Инженерные задачи фазы (Mode 2 -> Mode 3)
- [x] [[Specs/17_HardeningAndSync/TASK-066-kb-lint-codeblocks-and-schemas|TASK-066]]: Игнорирование кодовых блоков и экранированных пайпов `\|` в `kb_lint.py`, строгая проверка относительных путей и валидация YAML-схем для `06_Memory/Incidents/`.
- [x] [[Specs/17_HardeningAndSync/TASK-067-kb-ingest-yaml-escaping-and-imap-uid|TASK-067]]: Безопасное экранирование кавычек в YAML frontmatter (`FB-*.md`), переход на постоянные IMAP UID (`client.uid`) и URL-кодирование меток GitHub в `kb_ingest.py`.
- [x] [[Specs/17_HardeningAndSync/TASK-068-installer-tty-anonymizer-and-build-hook|TASK-068]]: Защита анонимизатора `--report` по границам путей, проверка открытия `/dev/tty` в контейнерах, диагностика `git commit` и вызов `build_installer.build()` внутри `scripts/build_release.py`.
- [x] [[Specs/17_HardeningAndSync/TASK-069-ssot-agents-and-docs-sync|TASK-069]]: Полная синхронизация `generate_agents_md()` (`install.py`) с корневым `AGENTS.md` (добавление Mode 0 и Mode 2C, Human Guardrails, таксономия 16 шаблонов в `Onboarding` и тестах, ссылки в `CHANGELOG.md`).
- [x] [[Specs/17_HardeningAndSync/TASK-070-skills-templates-and-memory-sync|TASK-070]]: Синхронизация скиллов, шаблонов и контура памяти в `AGENTS.md` (Zero Round-Trip Memory Sync, Stop & Yield в Read-Only скиллах, кастомизация `TEMPLATE_TASK_MICRO.md`, пути `TEMPLATE_RELEASE.md`, таксономия 16 шаблонов и граф).

---

## Фаза 18: Контур UI/UX, управление визуальными ассетами и гетерогенные multi-target системы (Heterogeneous UI/UX & Visual Asset Harness) — ✅ Завершена
**Цель:** Создать надежный, масштабируемый контур управления UI/UX, изолированное хранилище ассетов с Obsidian DX (`docs/assets/`, `docs/.obsidian/app.json`), механический контроль медиа в `kb_lint.py`/`kb_release.py` и поддержку гетерогенных multi-target комплексов (`--ui <targets>`).  
**Первоисточник плана:** [[Plans/PLAN-018-heterogeneous-ui-ux-and-visual-asset-harness|PLAN-018]]  
**Нормативная база:** [[../04_Research/RESEARCH-021-heterogeneous-ui-ux-and-visual-asset-management|RESEARCH-021]], [[../03_Decisions_ADR/ADR-0026-heterogeneous-ui-ux-and-visual-asset-management|ADR-0026]]

- [x] [[Specs/18_VisualHarness/TASK-071-asset-storage-composite-ui-and-obsidian-dx|TASK-071]]: Архитектура хранения ассетов, композитный `--ui` и Obsidian DX в `install.py` (2026-10-15).
- [x] [[Specs/18_VisualHarness/TASK-072-media-assets-lint-and-release-checks|TASK-072]]: Механический контроль медиа-ассетов в `scripts/kb_lint.py` и `scripts/kb_release.py` (2026-10-15).
- [x] [[Specs/18_VisualHarness/TASK-073-the-4-state-matrix-visual-dod-and-templates|TASK-073]]: Матрица 4 состояний (The 4-State Matrix), Visual DoD и шаблоны жизненного цикла в `AGENTS.md` (2026-10-15).
- [x] [[Specs/18_VisualHarness/TASK-074-bundling-e2e-tests-and-living-spec|TASK-074]]: Бандлинг инсталлятора `build_installer.py`, сквозные E2E тесты и актуализация Living Spec (2026-10-15).

---

## Фаза 19: Инженерные барьеры качества и контроль техдолга (Engineering Gates & Tech Debt Governance) — ✅ Завершена
**Цель:** Создать реестр техдолга `docs/02_Tasks/TechDebt.md` (P1/P2 vs P3), внедрить Prior-Art Gate в `TEMPLATE_PLAN.md` и `TEMPLATE_RESEARCH.md`, запретить висячие `TODO` в пользу `// ROADMAP-<ID>`, закрепить замеры $\ge 3$ прогонов («Замер = артефакт»), добавить чеклист приемочного тестирования GUI («UI не лжёт») в `TEMPLATE_TEST.md` и механический аудит в `scripts/kb_lint.py`.  
**Первоисточник плана:** [[Plans/PLAN-019-engineering-gates-and-tech-debt-governance|PLAN-019]]  
**Нормативная база:** [[../04_Research/RESEARCH-020-self-improving-defect-loop-and-quality-gates|RESEARCH-020]], [[../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]

- [x] [[Specs/19_EngineeringGates/TASK-075-tech-debt-registry-and-triage-rules|TASK-075]]: Инфраструктура реестра техдолга (`docs/02_Tasks/TechDebt.md`, скаффолдинг в `install.py`, правила триажа $P1/P2$ vs $P3$) (2026-10-15).
- [x] [[Specs/19_EngineeringGates/TASK-076-prior-art-gate-roadmap-tagging-and-benchmarks|TASK-076]]: Инженерные барьеры в шаблонах и правилах: Prior-Art Gate (`TEMPLATE_PLAN.md`, `TEMPLATE_RESEARCH.md`), трассировка `// ROADMAP-<ID>` и замеры $\ge 3$ прогонов в `AGENTS.md` и `TEMPLATE_TASK.md` (2026-10-15).
- [x] [[Specs/19_EngineeringGates/TASK-077-gui-acceptance-checklist-and-kb-lint-audit|TASK-077]]: Чеклист приемочного тестирования GUI («UI не лжёт») в `TEMPLATE_TEST.md` и аудит целостности `TechDebt.md` в `scripts/kb_lint.py` (2026-10-15).
- [x] [[Specs/19_EngineeringGates/TASK-078-bundling-e2e-tests-and-living-spec|TASK-078]]: Синхронизация `install.py`, сборка монолита через `scripts/build_installer.py`, E2E тесты и актуализация Living Spec (2026-10-15).

---

## Фаза 20: Стандартизация хранилища визуальных ассетов, пространства имен TASK-XXX и валидация топологии (Asset Storage Hardening & Layout Linting) — ✅ Завершена
**Цель:** Устранить «дрифт редизайнов» (To-Be Drift) и перезапись макетов за счет пространств имен `docs/assets/mockups/<target>/TASK-XXX/` и сквозных сценариев `docs/assets/mockups/flows/TASK-XXX/`, стандартизировать жизненный цикл `As-Is / To-Be` (`asis.svg`, `tobe.svg`), исправить ложноположительное разрешение путей одноименных медиафайлов в `scripts/kb_lint.py` и внедрить механическую проверку топологии `check_asset_layout()`.  
**Первоисточник плана:** [[Plans/PLAN-020-asset-storage-hardening-and-layout-linting|PLAN-020]]  
**Нормативная база:** [[../04_Research/RESEARCH-022-asset-storage-hardening-and-task-scoped-namespaces|RESEARCH-022]], [[../03_Decisions_ADR/ADR-0027-task-scoped-asset-namespaces-and-layout-linting|ADR-0027]] | **Источник:** [[Inbox/FB-GH-5|FB-GH-5]]  
**Официальный релиз:** [[Releases/RELEASE-v0.20.0|RELEASE-v0.20.0]]

- [x] [[Specs/20_AssetHardening/TASK-079-asset-layout-lint-and-strict-media-resolution|TASK-079]]: Механический контроль топологии `docs/assets/` (`check_asset_layout()`) и строгая резолюция относительных путей медиа-ссылок в `scripts/kb_lint.py` (2026-10-15).
- [x] [[Specs/20_AssetHardening/TASK-080-mockup-namespace-and-flows-convention-in-installer-and-templates|TASK-080]]: Пространства имен макетов `TASK-XXX/`, жизненный цикл `As-Is / To-Be` и каталог `mockups/flows/` в `install.py`, `TEMPLATE_TASK.md` и `AGENTS.md` (2026-10-16).
- [x] [[Specs/20_AssetHardening/TASK-081-e2e-verification-bundle-rebuild-and-living-spec-sync|TASK-081]]: Сборка монолита `build_installer.py`, E2E тестирование в `tests/test_installer.py` и синхронизация Living Spec (`SPEC.md`, `README.md`, `docs/Onboarding.md`) (2026-10-16).

---

## Фаза 21: Сквозной жизненный цикл технического долга и кросс-режимная синхронизация (Tech Debt Lifecycle & Cross-Mode Sync) — ✅ Завершена
**Цель:** Замкнуть сквозной жизненный цикл технического долга (`DEBT-XXX`) во всех режимах разработки (`/kb-plan`, `/kb-task`, `/kb-triage`, `/kb-complete`), разрешить кодовые комментарии `// DEBT-XXX` наравне с `// ROADMAP-<ID>`, унифицировать канонический тег `#techdebt` в таксономии/шаблонах и добавить семантический кросс-чек `TechDebt.md` с фазами/задачами `#techdebt` в `scripts/kb_lint.py`.  
**Первоисточник плана:** [[Plans/PLAN-021-tech-debt-lifecycle-and-cross-mode-sync|PLAN-021]]  
**Нормативная база:** [[../04_Research/RESEARCH-023-tech-debt-lifecycle-and-cross-mode-sync|RESEARCH-023]], [[../03_Decisions_ADR/ADR-0028-end-to-end-tech-debt-lifecycle-and-lint-enforcement|ADR-0028]]  
**Официальный релиз:** [[Releases/RELEASE-v0.21.0|RELEASE-v0.21.0]]

- [x] [[Specs/21_TechDebtLifecycle/TASK-082-kb-lint-tech-debt-cross-check-and-todo-tags|TASK-082]]: Семантический кросс-чек `TechDebt.md` с фазами/задачами `#techdebt` и поддержка кодовых тегов `// DEBT-XXX` в `scripts/kb_lint.py`.
- [x] [[Specs/21_TechDebtLifecycle/TASK-083-skills-agents-and-templates-tech-debt-lifecycle|TASK-083]]: Сквозной цикл `DEBT-XXX` в скиллах (`kb-plan`, `kb-task`, `kb-triage`, `kb-complete`), правилах `AGENTS.md`, шаблонах и `install.py`.
- [x] [[Specs/21_TechDebtLifecycle/TASK-084-bundle-rebuild-e2e-tests-and-living-spec-sync|TASK-084]]: Сборка монолита `build_installer.py`, E2E тестирование в `tests/test_installer.py` и синхронизация Living Spec (`SPEC.md`, `README.md`, `Onboarding.md`).

---

## Фаза 22: Компилятор правил единого источника и защита от дрейфа SSOT (Single-Source Rule Compiler) — ✅ Завершена
**Цель:** Устранить тройной инвентарь правил агента (корневой `AGENTS.md` — 16 принципов, `_RULES_BODY` — 20 дисциплин + 11 секций, `_gen_rule` — 10 правил для 6 адаптеров) за счёт единого корпуса `rules/AGENTS_CORE.md`, детерминированного рендера и механического Tier 1 контроля дрейфа в CI. Новое правило = одна правка вместо трёх, дрейф ловится на коммите, а не через фазу ремонтной задачи.  
**Первоисточник плана:** [[Plans/PLAN-022-single-source-rule-compiler|PLAN-022]]  
**Нормативная база:** ADR-0030 (оформляется в рамках TASK-085)  
**Официальный релиз:** [[Releases/RELEASE-v0.22.0|RELEASE-v0.22.0]]

- [x] [[Specs/22_RuleCompiler/TASK-085-rules-corpus-renderer-and-bundling|TASK-085]]: Корпус правил `rules/AGENTS_CORE.md`, рендерер в `install.py`, упаковка в бандл и ADR-0030 (2026-10-18).
- [x] [[Specs/22_RuleCompiler/TASK-086-agents-md-codegen-and-ci-check|TASK-086]]: Генерация корневого `AGENTS.md` через `scripts/gen_rules.py --check`, workflow `rules-check.yml` и префлайт релиза (2026-10-18).
- [x] [[Specs/22_RuleCompiler/TASK-087-rules-drift-consistency-tests|TASK-087]]: Tier 1 тесты дрейфа (`tests/test_rules_consistency.py`): канонический инвентарь, уникальность ID, выводимость адаптеров (2026-10-18).
- [x] [[Specs/22_RuleCompiler/TASK-088-editorial-consolidation-e2e-and-living-spec|TASK-088]]: Редакционная консолидация, E2E-синхронизация инсталлятора, Living Spec (`SPEC.md`, `README.md`, `Onboarding.md`) и пересборка `dist/install.py` (2026-10-18).

### 🐞 Исправление дефектов (Mode 2B -> Mode 3 TDD)
- [x] [[Bugs/BUG-011-ci-git-identity-hermetic-test|BUG-011]]: Герметизация `test_05_git_local_setup` (изоляция `GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM`, синтетическая identity через `GIT_AUTHOR_*`/`GIT_COMMITTER_*`) и контрактный тест `test_05b` graceful-деградации без identity — hotfix Tier 1-гейта `Rules Check`, блокер v0.23.0 (2026-10-18).
- [x] [[Bugs/BUG-012-dashboard-env-and-live-api-test|BUG-012]]: Изоляция `test_render_status_dashboard` от `GITHUB_REPOSITORY` и живого GitHub API (замоканный `urlopen`, контракт приоритета `env` → `auto-detect`) — второй блокер Tier 1-гейта `Rules Check`, v0.23.0 (2026-10-18).

---

## Фаза 23: Целостность процедурной памяти и защита от дрейфа ссылок (Memory Integrity Guard) — ✅ Завершена
**Цель:** Замкнуть Tier 1-контроль контура `docs/06_Memory/`: проверять, что каждый `INC-XXX`, на который ссылается `patterns.md`, существует; что `target_pattern` инцидента присутствует в индексе; что `id` совпадает с именем файла. Устранить исторические висячие ссылки (`TRG-01`/`TRG-02` → `INC-001`/`INC-002`, которых никогда не было в Git) и зафиксировать единую процедуру заведения инцидента в `docs/Onboarding.md` §13.  
**Обоснование:** аудит 2026-10-18 показал, что `check_memory_limits()` контролирует только лимит 15 записей, а ссылочная целостность индекса не механизирована — нарушение инварианта Quality Gates (Tier 1), из-за которого дрейф памяти остаётся незамеченным. Выделено в отдельную фазу, чтобы не размывать релизный нарратив Фазы 22 (Single-Source Rule Compiler) и не менять её DoD.  
**Спецификация:** [[Specs/23_MemoryIntegrity/TASK-089-memory-consistency-lint-and-incident-procedure|TASK-089]]  
**Официальный релиз:** [[Releases/RELEASE-v0.23.0|RELEASE-v0.23.0]]

- [x] [[Specs/23_MemoryIntegrity/TASK-089-memory-consistency-lint-and-incident-procedure|TASK-089]]: `check_memory_consistency()` в `scripts/kb_lint.py` (неблокирующий `WARN:`), тесты в `tests/test_kb_lint.py`, чистка висячих ссылок в `patterns.md` и раздел «Как завести инцидент» в `docs/Onboarding.md` (2026-10-18).

---

## Фаза 24: Research-Evidence Gate при промоушене из Icebox (Research-Evidence Gate & Plan Provenance) — ✅ Завершена
**Цель:** Восстановить критерий технической зрелости в ранжировании `/kb-plan` (утерянный при переносе ADR-0011 §2.2 в текст скилла) и сделать доказательную базу плана явной, durable и защищённой от повторной потери: пометки `🔬`/`🧪`/`⏸` в ранжировании, неблокирующий Evidence Nudge с тремя опциями, поля `research_basis`/`basis_note` и секция «Research Basis & Unvalidated Assumptions» в `PLAN-XXX`, advisory-`WARN` в `scripts/kb_lint.py`, правило Tier 2 в корпусе `rules/AGENTS_CORE.md` и Tier 1 тесты против повторной потери формулировки. Попутно устраняется P2-расхождение `templates/` ↔ `docs/00_Templates/` (клиенты получали план-шаблон без матрицы 4 состояний) с parity-тестом.
**Первоисточник плана:** [[Plans/PLAN-023-research-evidence-gate-and-plan-provenance|PLAN-023]]  
**Нормативная база:** [[../04_Research/RESEARCH-025-research-evidence-gate-for-icebox-promotion|RESEARCH-025]], [[../03_Decisions_ADR/ADR-0031-research-evidence-gate-for-icebox-promotion|ADR-0031]], [[../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]  
**Официальный релиз:** [[Releases/RELEASE-v0.24.0|RELEASE-v0.24.0]]

- [x] [[Specs/24_ResearchEvidence/TASK-090-evidence-status-nudge-and-tier2-rule|TASK-090]]: Критерий Evidence Status (`🔬`/`🧪`/`⏸`), `Evidence Nudge` (A/B/C) в `.agents/skills/kb-plan/SKILL.md`, строка правила Mode 1 в `rules/AGENTS_CORE.md` (+ регенерация `AGENTS.md`) и Tier 1 ассерт против повторной потери формулировки (2026-10-18).
- [x] [[Specs/24_ResearchEvidence/TASK-091-plan-research-basis-template-and-advisory-lint|TASK-091]]: `research_basis`/`basis_note` и секция «Research Basis & Unvalidated Assumptions» в `TEMPLATE_PLAN.md` (обе копии), неблокирующий `check_research_basis()` в `scripts/kb_lint.py` и тесты в `tests/test_kb_lint.py` (2026-10-18).
- [x] [[Specs/24_ResearchEvidence/TASK-092-template-copies-parity-sync-and-test|TASK-092]]: Синхронизация `templates/` ↔ `docs/00_Templates/` (4-State Matrix в `TEMPLATE_PLAN.md`, карта заметок в `TEMPLATE_INDEX.md`) и Tier 1 parity-тест копий шаблонов (P2-находка планирования) (2026-10-18).
- [x] [[Specs/24_ResearchEvidence/TASK-093-bundle-rebuild-e2e-and-living-spec-sync|TASK-093]]: Пересборка `install.py` / `dist/install.py`, E2E установленного скилла и `--update`, Living Spec Sync (`SPEC.md`, `README.md`, `docs/Onboarding.md`) (2026-10-18).

---

## Фаза 25: Символьные контракты скоупа задач и защита от дрейфа строк (Symbolic Scope & Line Drift Prevention) — ✅ Завершена
**Цель:** Заменить плоский список файлов в спецификациях задач иерархическим контрактом `Файл → символ/метод → изменение`, запретить номера строк как ориентир, дать Режиму 3 устойчивую локализацию по именам символов и неблокирующий контроль в `scripts/kb_lint.py` без выхода за бюджеты High-SNR.  
**Первоисточник плана:** [[Plans/PLAN-024-symbolic-scope-and-task-contracts|PLAN-024]]  
**Нормативная база:** [[../04_Research/RESEARCH-024-fine-grained-task-scope-and-symbol-contracts|RESEARCH-024]], [[../03_Decisions_ADR/ADR-0029-fine-grained-task-symbol-contracts-and-line-drift-rejection|ADR-0029]]  
**Официальный релиз:** [[Releases/RELEASE-v0.25.0|RELEASE-v0.25.0]]

- [x] [[Specs/25_SymbolicScope/TASK-094-symbolic-contract-templates-and-source-guard|TASK-094]]: Символьный контракт в `TEMPLATE_TASK.md` и `TEMPLATE_TASK_MICRO.md` (обе копии), Tier 1 source-guard тест и замер бюджетов (2026-10-18).
- [x] [[Specs/25_SymbolicScope/TASK-095-symbolic-behavior-and-advisory-lint|TASK-095]]: Поведение `/kb-task` и `/kb-implement`, `check_symbolic_scope()` в `scripts/kb_lint.py`, state-aware next step в `/kb-complete` и unit-тесты (2026-10-18).
- [x] [[Specs/25_SymbolicScope/TASK-096-bundle-e2e-and-living-spec|TASK-096]]: Пересборка `install.py` / `dist/install.py`, E2E свежей установки и `--update`, Living Spec Sync (2026-10-18).

---

## 🔮 Перспективные направления (Future Horizons / Icebox)
*Идеи и гипотезы, находящиеся на стадии осмысления. Номер фазы и декомпозиция на задачи присваиваются при взятии в активную проработку через Режим 1 (`/kb-plan`).*
<!-- 💡 При появлении новой идеи не вносите сырые пункты вручную! Запустите '/kb-research <идея>', чтобы агент исследовал жизнеспособность, риски и ценность идеи (Режим 0: Discovery), оформил RESEARCH/ADR и автоматически занес валидированную инициативу в Icebox либо отклонил её. -->

* 💡 **Детерминированный синтаксический автофикс (kb_lint.py --fix):** опциональный флаг для безопасного автоматического экранирования неэкранированных пайпов `\|` в табличных викиссылках и нормализации пробелов без эвристического вмешательства в семантику ссылок.
* 💡 **Автоматизированная ротация процедурной памяти (Compaction):** процедурный механизм в `kb-complete` или встроенный хелпер для ротации старейших паттернов `[TRG-XX]` из `patterns.md` в архив `docs/06_Memory/Incidents/` при приближении к лимиту 15 записей.
* 💡 **Расширенные пресеты стеков (Go, Rust, JVM):** автодетект стеков (`Cargo.toml`, `go.mod`, `build.gradle.kts`, `pom.xml`) и базовые команды верификации для `install.py`.
* 💡 **Контроль архитектурной преемственности в исследованиях (Codebase Continuity & Invariant Guard в kb-research):** формализация инварианта скилла `/kb-research`: обязательная опора на существующую кодовую базу (скрипты, линтер, инсталлятор, правила), запрет скрытого разрушения ранее принятых архитектурных контрактов (Permalinks, Zero-Deps) и требование явного обоснования рефакторинга через статус `superseded/amended`.
* 💡 **Обязательное Spike-прототипирование в Режиме 0 (Executable Research):** требование создания запускаемого проверочного прототипа в `scratch/` перед фиксацией вердикта в ADR для исключения рисков «бумажной архитектуры».
* 💡 **Пакетный триаж обращений (Batch Triage в kb-triage):** режим `/kb-triage --batch` для массовой дедупликации, кластеризации и классификации потока тикетов в `Inbox/` без поштучной остановки на каждом обращении.
* 💡 **Конфигурации для нишевых агентов:** Continue.dev (`.continue/config.json`), Aider (`.aider.conf.yml`).


---

## 🚫 Отклоненные архитектурные идеи (Rejected Alternatives)
*Идеи, проанализированные в Режиме 1 и официально отклоненные во избежание оверинжиниринга, раздувания дистрибутива и дублирования сторонних инструментов:*

* ❌ **Встроенный локальный web-визуализатор базы знаний (`install.py --serve`):** отклонен в пользу нативного Obsidian — [[../../03_Decisions_ADR/ADR-0005-rejection-of-embedded-web-visualizer|ADR-0005]].
* ❌ **Встроенный генератор PDF-отчетов для руководства:** отклонен в пользу нативных возможностей агентов и экспорта Markdown — [[../../03_Decisions_ADR/ADR-0006-rejection-of-standalone-pdf-report-generator|ADR-0006]].
* ❌ **Монолитный umbrella-скилл вместо модульных скиллов:** отклонен во избежание деградации слэш-команд в IDE и раздувания контекста — [[../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]].
* ❌ **Отказ от автономного инсталлятора install.py и линтера kb_lint.py:** отклонен для сохранения Zero-Dependencies распространения и Tier 1 контроля — [[../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]].
* ❌ **Фиксация диапазонов строк в задачах и микродетализация реализации в планах (Line Drift & Plan Overspecification):** отклонено из-за неизбежного дрейфа строк при коммитах, сбоев диффов у AI-агентов и нарушения уровней абстракции — [[../03_Decisions_ADR/ADR-0029-fine-grained-task-symbol-contracts-and-line-drift-rejection|ADR-0029]].
