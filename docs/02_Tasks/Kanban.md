---
kanban-plugin: basic
---

# 📋 Канбан-доска: agent-docs-harness

> **Теги:** #tasks #kanban #planning  
> **Связанная дорожная карта:** [[Roadmap|Дорожная карта]]  
> *Примечание: этот файл открывается в Obsidian через плагин "Kanban" в виде интерактивной доски.*

## 📥 Бэклог (Backlog)

- [ ] [[Bugs/BUG-013-sarif-paths-are-docs-relative|BUG-013]]: SARIF-путь docs-relative вместо repo-relative (2026-10-25) #bug #code-scanning #sarif

- [ ] [[Plans/PLAN-026-ci-delivery-and-code-scanning|План: Фаза 28 (продолжение) — CI-доставка линта: action.yml, pre-commit, Code Scanning и решение по DEBT-004]] (2026-10-25) #plan #phase28 #ci #distribution #code-scanning

## ⏳ В работе (In Progress)







## ✅ Готово (Done)

- [x] [[Specs/28_GateHygiene/TASK-109-debt004-decision|TASK-109]]: решение по `DEBT-004` — probe-алерт в Code Scanning и закрытие долга (2026-10-25) #task #phase28 #techdebt #code-scanning

- [x] [[Specs/28_GateHygiene/TASK-108-code-scanning-workflow|TASK-108]]: Code Scanning — SARIF-workflow, `uses: ./`, исключение из бандла (2026-10-25) #task #phase28 #ci #code-scanning

- [x] [[Specs/28_GateHygiene/TASK-107-pre-commit-hooks-and-readme|TASK-107]]: `.pre-commit-hooks.yaml` и два рецепта подключения в README (2026-10-25) #task #phase28 #ci #distribution

- [x] [[Specs/29_PlainLanguage/TASK-106-plain-language-acceptance|TASK-106]]: Принять правило `PLAIN-LANGUAGE`: ADR-0033, страж свежести бандла и бюджет (2026-10-25) #task #phase29 #rules #installer

- [x] [[Specs/28_GateHygiene/TASK-105-composite-action-and-readme|TASK-105]]: Composite GitHub Action (`action.yml`) и раздел README (2026-10-25) #task #phase28 #ci #distribution

- [x] [[Specs/28_GateHygiene/TASK-104-sandbox-test-runner-promotion|TASK-104]]: DEBT-005 — промоушен sandbox-раннера тестов в `scripts/` (2026-10-25) #task #fast-track #phase28 #techdebt #tests

- [x] [[Plans/PLAN-025-docs-integrity-gate-kb-lint-productization|План: Фаза 27 — Продуктизация линтера: машинно-читаемая диагностика (Docs Integrity Gate, P0)]] (2026-10-25) #plan #phase27 #docs-integrity-gate #lint #contracts

- [x] [[Specs/27_DocsIntegrity/TASK-103-bundle-e2e-and-living-spec|TASK-103]]: Пересборка бандла, бюджет `test_16`, E2E установленной копии и Living Spec (2026-10-25) #task #phase27 #installer #e2e #spec

- [x] [[Specs/27_DocsIntegrity/TASK-102-output-contract-tests|TASK-102]]: Контрактные тесты машинно-читаемого вывода (реестр, JSON, SARIF, exit-коды) (2026-10-25) #task #phase27 #lint #tests #contracts

- [x] [[Specs/27_DocsIntegrity/TASK-101-finding-model-rule-registry-and-formats|TASK-101]]: Модель `Finding`, реестр `KB-001…KB-015`, рендереры `text/json/sarif`, `--format` и `--version`, ADR-0032 (2026-10-25) #task #phase27 #lint #contracts

- [x] [[Specs/26_TechDebt/TASK-100-align-rules-section-numbering|TASK-100]]: DEBT-001 — выравнивание нумерации разделов корпуса правил (2026-10-18) #task #phase26 #techdebt #rules #tests

- [x] [[Specs/26_TechDebt/TASK-099-roadmap-permalink-at-spec-creation|TASK-099]]: Пермалинк спеки в Roadmap при `/kb-task` (2026-10-18) #task #fast-track #phase26 #process #roadmap

- [x] [[Specs/26_TechDebt/TASK-098-rules-check-ci-hardening|TASK-098]]: DEBT-002 — харденинг CI-гейта Rules Check (2026-10-18) #task #phase26 #techdebt #ci #tests

- [x] [[Specs/26_TechDebt/TASK-097-clean-stale-kanban-icebox|TASK-097]]: DEBT-003 — очистка устаревшего Icebox в Kanban.md (2026-10-18) #task #fast-track #techdebt #phase26

- [x] [[Plans/PLAN-024-symbolic-scope-and-task-contracts|План: Фаза 25 — Символьные контракты скоупа задач (Symbolic Scope)]] (2026-10-18) #plan #phase25 #symbolic-scope #task-spec #templates #lint
- [x] [[Specs/25_SymbolicScope/TASK-096-bundle-e2e-and-living-spec|TASK-096]]: Пересборка бандла, E2E и Living Spec Sync (2026-10-18) #task #phase25 #symbolic-scope #installer #e2e #spec

- [x] [[Specs/25_SymbolicScope/TASK-095-symbolic-behavior-and-advisory-lint|TASK-095]]: Поведение Mode 2/3, `check_symbolic_scope()` и state-aware next step (2026-10-18) #task #phase25 #symbolic-scope #skills #lint #tests

- [x] [[Specs/25_SymbolicScope/TASK-094-symbolic-contract-templates-and-source-guard|TASK-094]]: Символьный контракт в шаблонах, Tier 1 source-guard и замер бюджетов (2026-10-18) #task #phase25 #symbolic-scope #templates #tests

- [x] [[Plans/PLAN-023-research-evidence-gate-and-plan-provenance|План: Фаза 24 — Research-Evidence Gate при промоушене из Icebox (критерий зрелости, Evidence Nudge, `research_basis`, advisory-линт и parity шаблонов)]] (2026-10-18) #plan #phase24 #research-evidence #kb-plan #templates #lint
- [x] [[Specs/24_ResearchEvidence/TASK-093-bundle-rebuild-e2e-and-living-spec-sync|TASK-093]]: Пересборка `install.py` / `dist/install.py` (173 887 байт), E2E установленного скилла и `--update`, нормализация LF в High-SNR бюджете и Living Spec Sync (`SPEC.md`, `README.md`, `docs/Onboarding.md`) (2026-10-18) #task #phase24 #research-evidence #installer #e2e #spec
- [x] [[Specs/24_ResearchEvidence/TASK-092-template-copies-parity-sync-and-test|TASK-092]]: Синхронизация `templates/` ↔ `docs/00_Templates/` (4-State Matrix и multi-target комментарий в `TEMPLATE_PLAN.md`, карта заметок в `TEMPLATE_INDEX.md`) и Tier 1 parity-тест `tests/test_template_parity.py` (2026-10-18) #task #phase24 #templates #tests #quality-gates
- [x] [[Specs/24_ResearchEvidence/TASK-091-plan-research-basis-template-and-advisory-lint|TASK-091]]: `research_basis`/`basis_note` и секция «Research Basis & Unvalidated Assumptions» в `TEMPLATE_PLAN.md` (обе копии), неблокирующий `check_research_basis()` в `scripts/kb_lint.py` и 4 теста (2026-10-18) #task #phase24 #research-evidence #templates #lint
- [x] [[Specs/24_ResearchEvidence/TASK-090-evidence-status-nudge-and-tier2-rule|TASK-090]]: Evidence Status (`🔬`/`🧪`/`⏸`) и `Evidence Nudge` (A/B/C) в `/kb-plan`, Tier 2 правило в корпусе, регенерация `AGENTS.md` и Tier 1 ассерт формулировки (2026-10-18) #task #phase24 #research-evidence #kb-plan #rules #tests
- [x] [[Specs/23_MemoryIntegrity/TASK-089-memory-consistency-lint-and-incident-procedure|TASK-089]]: Целостность процедурной памяти: `check_memory_consistency()`, чистка висячих INC-ссылок и процедура заведения инцидента в `Onboarding.md` §13 (2026-10-18) #task #phase23 #memory #lint

- [x] [[Bugs/BUG-012-dashboard-env-and-live-api-test|BUG-012]]: Rules Check — `test_render_status_dashboard` изолирован от `GITHUB_REPOSITORY` и живого GitHub API (`urlopen` замокан, контракт приоритета `env` → `auto-detect`) — P1, исправлен в v0.23.0 (2026-10-18) #bug #ci #tests #quality-gates #phase22
- [x] [[Bugs/BUG-011-ci-git-identity-hermetic-test|BUG-011]]: Rules Check — `test_05_git_local_setup` изолирован от глобальной Git identity (`hermetic_git_env`, `test_05b` graceful-деградация) — P1, исправлен в v0.23.0 (2026-10-18) #bug #ci #tests #quality-gates #phase22
- [x] [[Plans/PLAN-022-single-source-rule-compiler|План: Фаза 22 — Компилятор правил единого источника и защита от дрейфа SSOT (Single-Source Rule Compiler)]] (2026-10-18) #plan #phase22 #ssot #rules #codegen
- [x] [[Specs/22_RuleCompiler/TASK-088-editorial-consolidation-e2e-and-living-spec|TASK-088]]: Редакционная консолидация правил, E2E-синхронизация, Living Spec и пересборка `dist/install.py` (2026-10-18) #task #phase22 #e2e #spec
- [x] [[Specs/22_RuleCompiler/TASK-087-rules-drift-consistency-tests|TASK-087]]: Tier 1 тесты дрейфа правил (`tests/test_rules_consistency.py`) (2026-10-18) #task #phase22 #tests #quality-gates
- [x] [[Specs/22_RuleCompiler/TASK-086-agents-md-codegen-and-ci-check|TASK-086]]: Генерация корневого `AGENTS.md` через `scripts/gen_rules.py --check`, CI-гейт и exclusion workflow (2026-10-18) #task #phase22 #codegen #ci
- [x] [[Specs/22_RuleCompiler/TASK-085-rules-corpus-renderer-and-bundling|TASK-085]]: Корпус правил `rules/AGENTS_CORE.md`, рендерер в `install.py`, упаковка в бандл и ADR-0030 (2026-10-18) #task #phase22 #ssot #rules #installer
- [x] [[Bugs/BUG-010-release-remote-credentials-leak|BUG-010]]: Утечка credentials из Git remote (PAT) в релизные артефакты и публичные Release Notes — P1, закрыт в v0.21.0 (2026-10-18) #bug #security #release #credentials #phase21
- [x] [[Specs/21_TechDebtLifecycle/TASK-082-kb-lint-tech-debt-cross-check-and-todo-tags|TASK-082]]: Семантический кросс-чек `TechDebt.md` с фазами/задачами `#techdebt` и поддержка кодовых тегов `// DEBT-XXX` в `scripts/kb_lint.py` (2026-10-18) #task #phase21 #techdebt #lint
- [x] [[Specs/21_TechDebtLifecycle/TASK-083-skills-agents-and-templates-tech-debt-lifecycle|TASK-083]]: Сквозной цикл `DEBT-XXX` в скиллах (`kb-plan`, `kb-task`, `kb-triage`, `kb-complete`), правилах `AGENTS.md`, шаблонах и `install.py` (2026-10-18) #task #phase21 #techdebt #skills #agents
- [x] [[Specs/21_TechDebtLifecycle/TASK-084-bundle-rebuild-e2e-tests-and-living-spec-sync|TASK-084]]: Сборка монолита `build_installer.py`, E2E тестирование в `tests/test_installer.py` и синхронизация Living Spec (`SPEC.md`, `README.md`, `Onboarding.md`) (2026-10-18) #task #phase21 #installer #e2e #spec
- [x] [[Plans/PLAN-021-tech-debt-lifecycle-and-cross-mode-sync|План: Фаза 21 — Сквозной жизненный цикл технического долга и кросс-режимная синхронизация]] (2026-10-18) #plan #phase21 #techdebt #lint #skills
- [x] [[Plans/PLAN-020-asset-storage-hardening-and-layout-linting|План: Фаза 20 — Стандартизация хранилища визуальных ассетов, пространства имен TASK-XXX и валидация топологии]] (2026-10-16) #plan #phase20 #assets #ui-ux #lint
  - [x] [[Specs/20_AssetHardening/TASK-081-e2e-verification-bundle-rebuild-and-living-spec-sync|TASK-081]]: Сборка монолита `build_installer.py`, E2E тестирование в `tests/test_installer.py` и синхронизация Living Spec (`SPEC.md`, `README.md`, `docs/Onboarding.md`) (2026-10-16) #task #phase20 #installer #e2e #spec
- [x] [[Specs/20_AssetHardening/TASK-080-mockup-namespace-and-flows-convention-in-installer-and-templates|TASK-080]]: Пространства имен макетов `TASK-XXX/`, жизненный цикл `As-Is / To-Be` и каталог `mockups/flows/` в `install.py`, `TEMPLATE_TASK.md` и `AGENTS.md` (2026-10-16) #task #phase20 #installer #templates #agents
- [x] [[Specs/20_AssetHardening/TASK-079-asset-layout-lint-and-strict-media-resolution|TASK-079]]: Механический контроль топологии `docs/assets/` (`check_asset_layout()`) и строгая резолюция относительных путей медиа-ссылок в `scripts/kb_lint.py` (2026-10-15) #task #phase20 #lint #assets
- [x] [[Plans/PLAN-019-engineering-gates-and-tech-debt-governance|План: Фаза 19 — Инженерные барьеры качества и контроль техдолга]] (2026-10-15) #plan #phase19 #quality-gates #tech-debt
  - [x] [[Specs/19_EngineeringGates/TASK-078-bundling-e2e-tests-and-living-spec|TASK-078]]: Синхронизация `install.py`, сборка монолита через `build_installer.py`, E2E тесты и актуализация Living Spec (2026-10-15) #task #phase19 #installer #e2e #spec
- [x] [[Specs/19_EngineeringGates/TASK-077-gui-acceptance-checklist-and-kb-lint-audit|TASK-077]]: Чеклист приемочного тестирования GUI («UI не лжёт») в TEMPLATE_TEST.md и аудит целостности TechDebt.md в scripts/kb_lint.py (2026-10-15) #task #phase19 #testing #lint
- [x] [[Specs/19_EngineeringGates/TASK-076-prior-art-gate-roadmap-tagging-and-benchmarks|TASK-076]]: Инженерные барьеры в шаблонах и правилах: Prior-Art Gate, трассировка // ROADMAP-<ID> и замеры >= 3 прогонов (2026-10-15) #task #phase19 #prior-art #benchmarks
- [x] [[Specs/19_EngineeringGates/TASK-075-tech-debt-registry-and-triage-rules|TASK-075]]: Инфраструктура реестра техдолга (`docs/02_Tasks/TechDebt.md`, скаффолдинг в `install.py`, правила триажа $P1/P2$ vs $P3$) (2026-10-15) #task #phase19 #tech-debt

- [x] [[Plans/PLAN-018-heterogeneous-ui-ux-and-visual-asset-harness|План: Фаза 18 — Контур UI/UX, управление визуальными ассетами и гетерогенные multi-target системы]] (2026-10-15) #plan #phase18 #ui-ux #multi-target #visual-harness
  - [x] [[Specs/18_VisualHarness/TASK-074-bundling-e2e-tests-and-living-spec|TASK-074]]: Бандлинг инсталлятора `build_installer.py`, сквозные E2E тесты и актуализация Living Spec (2026-10-15) #task #phase18 #installer #e2e #spec
- [x] [[Specs/18_VisualHarness/TASK-073-the-4-state-matrix-visual-dod-and-templates|TASK-073]]: Матрица 4 состояний (The 4-State Matrix), Visual DoD и шаблоны жизненного цикла в `AGENTS.md` (2026-10-15) #task #phase18 #templates #agents #visual-dod
- [x] [[Specs/18_VisualHarness/TASK-072-media-assets-lint-and-release-checks|TASK-072]]: Механический контроль медиа-ассетов в `scripts/kb_lint.py` и `scripts/kb_release.py` (2026-10-15) #task #phase18 #lint #release #assets
- [x] [[Specs/18_VisualHarness/TASK-071-asset-storage-composite-ui-and-obsidian-dx|TASK-071]]: Архитектура хранения ассетов, композитный `--ui` и Obsidian DX в `install.py` (2026-10-15) #task #phase18 #installer #assets #obsidian

- [x] [[Specs/17_HardeningAndSync/TASK-070-skills-templates-and-memory-sync|TASK-070]]: Синхронизация скиллов, шаблонов и контура памяти в AGENTS.md (2026-10-15) #task #skills #templates #memory #phase17
- [x] [[Plans/PLAN-017-core-hardening-and-ssot-sync|План: Фаза 17 — Стабилизация ядра, синхронизация SSOT и защита краевых сценариев]] (2026-10-15) #plan #phase17 #hardening #ssot #quality-gates
- [x] [[Specs/17_HardeningAndSync/TASK-069-ssot-agents-and-docs-sync|TASK-069]]: Синхронизация SSOT: правила агентов, режимы жизненного цикла и таксономия 16 шаблонов (2026-10-15) #task #agents #ssot #docs #phase17
- [x] [[Specs/17_HardeningAndSync/TASK-068-installer-tty-anonymizer-and-build-hook|TASK-068]]: Защита анонимизатора, контейнерный TTY-зонд и интеграция сборщика в install.py и build_release.py (2026-10-15) #task #installer #release #phase17
- [x] [[Specs/17_HardeningAndSync/TASK-067-kb-ingest-yaml-escaping-and-imap-uid|TASK-067]]: Безопасное экранирование YAML, постоянные IMAP UIDs и URL-кодирование в scripts/kb_ingest.py (2026-10-15) #task #ingest #imap #phase17
- [x] [[Bugs/BUG-009-issue-templates-hardcoded-repo-leak|BUG-009]]: Устранение утечки метаданных и ссылок agent-docs-harness в .github/ISSUE_TEMPLATE/ (2026-10-15) #bug #installer #templates #phase17
- [x] [[Specs/17_HardeningAndSync/TASK-066-kb-lint-codeblocks-and-schemas|TASK-066]]: Харденинг парсинга викиссылок и валидация схем frontmatter в scripts/kb_lint.py (2026-10-15) #task #lint #schemas #phase17
- [x] [[Bugs/BUG-008-local-fallback-patterns-and-phase-pad|BUG-008]]: Отсутствие docs/06_Memory/patterns.md в локальном fallback install.py и некорректная маска фаз >= 10 в scripts/kb_release.py (2026-10-15) #bug #installer #release #phase17
- [x] [[Bugs/BUG-007-kb-ingest-paste-inline-arg|BUG-007]]: Падение с ошибкой unrecognized arguments при передаче инлайн-текста в scripts/kb_ingest.py --paste "<text>" (2026-10-15) #bug #ingest #cli #phase17
-  [x] [[Bugs/BUG-006-release-notes-self-artifact|BUG-006]]: dist/RELEASE_NOTES.md попадает в таблицу артефактов SHA-256 при повторном запуске scripts/kb_release.py (2026-10-15) #bug #release #phase17
- [x] [[Bugs/BUG-005-kb-lint-py38-is-relative-to|BUG-005]]: AttributeError при вызове Path.is_relative_to в scripts/kb_lint.py на Python 3.8 (2026-10-15) #bug #lint #python38 #phase17

- [x] [[Specs/16_MemoryAndQualityGates/TASK-065-align-cli-flags-and-sync-readme|TASK-065]]: Выравнивание CLI-флагов (`-i`, `-r`) и синхронизация `README.md` (2026-10-12) #task #fast-track #phase16 #installer #docs
- [x] [[Plans/PLAN-016-self-improving-harness-and-defect-memory|План: Фаза 16 — Самообучающийся харнесс и память дефектов]] (2026-10-12) #plan #phase16 #memory #defect-loop #quality-gates
  - [x] [[Specs/16_MemoryAndQualityGates/TASK-064-kb-lint-memory-audit-bundler-and-e2e|TASK-064]]: Контроль лимита памяти в `scripts/kb_lint.py`, бандлинг `install.py`, E2E тесты и Living Spec sync (2026-10-12) #task #phase16 #lint #installer #e2e
- [x] [[Specs/16_MemoryAndQualityGates/TASK-063-quality-gates-tier-matrix-and-agent-rules|TASK-063]]: Слои надежности Quality Gates (Tier 1–3) в `AGENTS.md` и руководстве `Onboarding.md` (2026-10-12) #task #phase16 #quality-gates #agents #rules
- [x] [[Specs/16_MemoryAndQualityGates/TASK-062-lifecycle-memory-checkpoints-and-promotion|TASK-062]]: Точки чтения памяти в жизненном цикле (`kb-implement`, `kb-complete`) и протокол двухосевого промоушена (2026-10-12) #task #phase16 #memory #lifecycle #skills
- [x] [[Specs/16_MemoryAndQualityGates/TASK-061-memory-infrastructure-and-patterns-index|TASK-061]]: Инфраструктура процедурной памяти (`docs/06_Memory/`, шаблон `TEMPLATE_INCIDENT.md` и агрегированный индекс `patterns.md`) (2026-10-12) #task #phase16 #memory #templates
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

- [ ] Конфигурации для нишевых агентов: Continue.dev (`.continue/config.json`) и Aider (`.aider.conf.yml`) #idea
- [x] Отклонено: Web-визуализатор базы знаний (`install.py --serve`) — [[../03_Decisions_ADR/ADR-0005-rejection-of-embedded-web-visualizer|ADR-0005]] #rejected
- [x] Отклонено: Автогенерация отчетов для руководства (PDF) — [[../03_Decisions_ADR/ADR-0006-rejection-of-standalone-pdf-report-generator|ADR-0006]] #rejected

