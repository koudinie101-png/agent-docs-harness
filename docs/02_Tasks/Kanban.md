---
kanban-plugin: basic
---

# 📋 Канбан-доска: agent-docs-harness

> **Теги:** #tasks #kanban #planning  
> **Связанная дорожная карта:** [[Roadmap|Дорожная карта]]  
> *Примечание: этот файл открывается в Obsidian через плагин "Kanban" в виде интерактивной доски.*

## 📥 Бэклог (Backlog)

- [ ] [[Plans/PLAN-004-release-management-and-lifecycle-automation|План: Фаза 4 — Релиз-менеджмент и автоматизация жизненного цикла]] #plan #phase4 #release
  - [ ] [[Specs/04_Releases/TASK-014-kb-release-skill-and-complete-nudge|TASK-014]]: Исполняемый скилл `.agents/skills/kb-release/SKILL.md` (Dual-Mode workflow, префлайт-чеки, подсказка в `kb-complete`) #task #phase4
  - [ ] [[Specs/04_Releases/TASK-015-github-actions-release-ci-and-installer-packaging|TASK-015]]: Шаблон GitHub Actions CI `.github/workflows/release.yml` и упаковка в инсталлятор `install.py` / `build_installer.py` (включая `--update`) #task #phase4
  - [ ] [[Specs/04_Releases/TASK-016-e2e-release-pipeline-verification-and-docs|TASK-016]]: Комплексное E2E тестирование релизного пайплайна (Local-Only и GitHub) и обновление документации #task #phase4

## ⏳ В работе (In Progress)

- [ ] [[Specs/04_Releases/TASK-013-template-release-and-kb-release-utility|TASK-013]]: Канонический шаблон `TEMPLATE_RELEASE.md`, каталог `docs/02_Tasks/Releases/` и утилита `scripts/kb_release.py` (Zero-Deps: сборка, SHA-256, чейнджлог) #task #phase4


## ✅ Готово (Done)

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

