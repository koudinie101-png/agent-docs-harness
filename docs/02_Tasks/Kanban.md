---
kanban-plugin: basic
---

# 📋 Канбан-доска: agent-docs-harness

> **Теги:** #tasks #kanban #planning  
> **Связанная дорожная карта:** [[Roadmap|Дорожная карта]]  
> *Примечание: этот файл открывается в Obsidian через плагин "Kanban" в виде интерактивной доски.*

## 📥 Бэклог (Backlog)

- [ ] [[Plans/PLAN-002-full-skills-and-agent-rules-integration|План: Фаза 2 — Интеграция полного набора скиллов, мультиязычности и правил агентов]] #plan #phase2 #skills
  - [ ] [[Specs/02_Extensions/TASK-006-skills-packaging-and-deployment|TASK-006]]: Упаковка всех 11 скиллов .agents/skills/ в сборщик и install.py #task #phase2
  - [ ] [[Specs/02_Extensions/TASK-007-gold-standard-agent-rules-and-gemini-md|TASK-007]]: Эталонные правила агентов по канону remote-notification и генерация GEMINI.md #task #phase2
  - [ ] [[Specs/02_Extensions/TASK-008-e2e-testing-and-readme-docs|TASK-008]]: Обновление E2E тестов и документации README #task #phase2

## ⏳ В работе (In Progress)


## ✅ Готово (Done)

- [x] [[Specs/02_Extensions/TASK-005-ai-agent-ecosystem-research-and-multilang|TASK-005]]: Исследование экосистемы AI-агентов (RESEARCH-001) и мультиязычность (--doc-lang) (2026-09-30) #task #phase2
- [x] Инициализация Git-репозитория и структуры базы знаний Docs-as-Code (2026-09-30) #docs
- [x] [[Plans/PLAN-001-crossplatform-installer-architecture|План: Фаза 1 — Архитектура автономного инсталлятора]] (2026-09-30) #plan #phase1
- [x] [[Specs/01_MVP/TASK-001-installer-core-and-bundling|TASK-001]]: Ядро инсталлятора install.py и упаковка ресурсов (2026-09-30) #task #phase1
- [x] [[Specs/01_MVP/TASK-002-multi-stack-templates-and-agent-configs|TASK-002]]: Мульти-стековые шаблоны и адаптеры агентов (2026-09-30) #task #phase1
- [x] [[Specs/01_MVP/TASK-003-cli-wizard-and-options|TASK-003]]: Интерактивный терминальный мастер и CLI флаги (2026-09-30) #task #phase1
- [x] [[Specs/01_MVP/TASK-004-e2e-testing-and-readme|TASK-004]]: E2E верификация песочницы и документация README (2026-09-30) #task #phase1

## 💡 Идеи и гипотезы (Icebox / Future Ideas)

- [ ] Команда синхронизации и обновления базы знаний (`install.py --update`) для существующих проектов #idea
- [ ] Готовый workflow GitHub Actions (`.github/workflows/kb-lint.yml`) для автоматической проверки целостности базы знаний в CI #idea
- [ ] Конфигурации для нишевых агентов: Continue.dev (`.continue/config.json`) и Aider (`.aider.conf.yml`) *(Windsurf и Antigravity уже взяты в TASK-007)* #idea
- [ ] Простой и понятный гайд для новичков в агентном программировании: пошаговое руководство, как запустить и использовать `install.py` (Zero-to-Hero Onboarding) #idea #docs #onboarding
