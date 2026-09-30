---
kanban-plugin: basic
---

# 📋 Канбан-доска: agent-docs-harness

> **Теги:** #tasks #kanban #planning  
> **Связанная дорожная карта:** [[Roadmap|Дорожная карта]]  
> *Примечание: этот файл открывается в Obsidian через плагин "Kanban" в виде интерактивной доски.*

## 📥 Бэклог (Backlog)

- [ ] [[Plans/PLAN-002-full-skills-and-agent-rules-integration|План: Интеграция полного набора скиллов, мультиязычности и правил агентов]] #plan #skills #phase2
  - [ ] TASK-005: Исследование экосистемы AI-агентов (RESEARCH-001) и мультиязычность (--doc-lang) #task
  - [ ] TASK-006: Упаковка всех 11 скиллов .agents/skills/ в сборщик и install.py #task
  - [ ] TASK-007: Эталонные правила агентов по канону remote-notification и генерация GEMINI.md #task
  - [ ] TASK-008: Обновление E2E тестов и документации README #task

## ⏳ В работе (In Progress)


## ✅ Готово (Done)

- [x] Инициализация Git-репозитория и структуры базы знаний Docs-as-Code (2026-09-30) #docs
- [x] [[Plans/PLAN-001-crossplatform-installer-architecture|План: Фаза 1 — Архитектура автономного инсталлятора]] (2026-09-30) #plan #phase1
- [x] [[Specs/01_MVP/TASK-001-installer-core-and-bundling|TASK-001]]: Ядро инсталлятора install.py и упаковка ресурсов (2026-09-30) #task
- [x] [[Specs/01_MVP/TASK-002-multi-stack-templates-and-agent-configs|TASK-002]]: Мульти-стековые шаблоны и адаптеры агентов (2026-09-30) #task
- [x] [[Specs/01_MVP/TASK-003-cli-wizard-and-options|TASK-003]]: Интерактивный терминальный мастер и CLI флаги (2026-09-30) #task
- [x] [[Specs/01_MVP/TASK-004-e2e-testing-and-readme|TASK-004]]: E2E верификация песочницы и документация README (2026-09-30) #task

## 💡 Идеи и гипотезы (Icebox / Future Ideas)

- [ ] Команда синхронизации и обновления базы знаний (`install.py --update`) для существующих проектов #idea
- [ ] Готовый workflow GitHub Actions (`.github/workflows/kb-lint.yml`) для автоматической проверки целостности базы знаний в CI #idea
- [ ] Поддержка дополнительных агентов: Windsurf (`.windsurfrules`), Continue.dev (`.continue/config.json`), Aider (`.aider.conf.yml`) #idea
