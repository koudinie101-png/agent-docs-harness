---
id: RELEASE-v0.8.0
title: "Релиз v0.8.0: Фаза 8"
version: "0.8.0"
phase: 8
status: completed
date: 2026-10-02
git_tag: "v0.8.0"
github_release_url: ""
mode: "local-only"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "88.4 KB"
    sha256: "867757bad12d737fa8409fdfea41e63850c9658f8e5fb0cc4a60c62e6351ec26"
  - name: "RELEASE_NOTES.md"
    path: "dist/RELEASE_NOTES.md"
    size: "6.4 KB"
    sha256: "1469cd999b113ab5a8f98ad4eb9c96e996e1c936d865186d8dcf431cecaf421e"
tags:
  - release
  - changelog
  - v0.8.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.8.0: Фаза 8

> **Версия:** v0.8.0  
> **Фаза:** 8  
> **Дата:** 2026-10-02  
> **Режим публикации:** Local-Only Package  
> **Git Tag:** `v0.8.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
Greenfield-инициализация от идеи (Idea-First, пресет undecided, CLI-флаг --idea), сквозная кристаллизация SPEC.md и README.md, протокол Living Spec Invariant в скиллах разработки и эвристический аудит дрифта спецификации в kb_lint.py.

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/08_Greenfield/TASK-029-undecided-preset-and-idea-flag|TASK-029]]: Пресет undecided, интерактивная опция меню и CLI-флаг --idea в install.py.
- [[../Specs/08_Greenfield/TASK-030-living-spec-protocol-and-skill-sync|TASK-030]]: Протокол Living Spec и синхронизация документации в скиллах kb-research, kb-complete, kb-release и AGENTS.md.
- [[../Specs/08_Greenfield/TASK-031-kb-lint-spec-drift-audit|TASK-031]]: Эвристический контроль дрифта спецификации в scripts/kb_lint.py и модульные тесты.
- [[../Specs/08_Greenfield/TASK-032-installer-bundling-and-e2e-verification|TASK-032]]: Сборка инсталлятора build_installer.py, сквозные E2E тесты и документация.

### 🐛 Исправленные дефекты (Bug Fixes)
- Критических дефектов и регрессий за период фазы не зафиксировано.

### 🏛️ Архитектурные решения (ADR)
- [[../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]: Архитектура Zero Dependencies на стандартной библиотеке Python 3.
- [[../../03_Decisions_ADR/ADR-0002-self-contained-installer-bundling|ADR-0002]]: Монолитная сборка инсталлятора через Self-Contained Bundle (zlib + Base64).
- [[../../03_Decisions_ADR/ADR-0003-multi-agent-adapter-strategy|ADR-0003]]: Стратегия конфигурации AI-агентов (Канонический AGENTS.md + Зеркала для редакторов).
- [[../../03_Decisions_ADR/ADR-0004-multi-stack-presets-and-apple-swift-priority|ADR-0004]]: Мульти-стековая параметризация шаблонов с приоритетом Apple Swift / Xcode.
- [[../../03_Decisions_ADR/ADR-0007-release-management-dual-mode-and-build-hook|ADR-0007]]: Архитектура релиз-менеджмента (Dual-Mode: GitHub / Local-Only и Build Hook Contract).
- [[../../03_Decisions_ADR/ADR-0008-feedback-loops-triage-buffer-and-local-diagnostics|ADR-0008]]: Архитектура каналов обратной связи, буфера триажа и локальной диагностики (Feedback Loops & Local Diagnostics).
- [[../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]]: Архитектура оптимизации токенов и контекстной эффективности (High-SNR Token Architecture).
- [[../../03_Decisions_ADR/ADR-0010-github-release-notes-and-public-distribution-standard|ADR-0010]]: Стандарт оформления публичных релизов на GitHub и двухформатный экспорт Release Notes.
- [[../../03_Decisions_ADR/ADR-0011-intent-routing-and-icebox-prioritization-in-kb-plan|ADR-0011]]: Маршрутизация намерений и приоритизация бэклога идей по ценности продукта в /kb-plan.
- [[../../03_Decisions_ADR/ADR-0012-discovery-mode-and-kb-research-lifecycle-integration|ADR-0012]]: Интеграция этапа исследования новых идей (Режим 0: Discovery & Feasibility) в жизненный цикл разработки и эволюция /kb-research.
- [[../../03_Decisions_ADR/ADR-0013-zero-roundtrip-dispatch-and-hot-invariants-architecture|ADR-0013]]: Архитектура Zero Round-Trip Dispatch и горячие инварианты (Hot Invariants) против латентности скиллов.
- [[../../03_Decisions_ADR/ADR-0014-greenfield-idea-first-initialization-and-living-spec-protocol|ADR-0014]]: Архитектура Greenfield-инициализации от идеи (Idea-First) и протокол Living Spec против дрифта документации.
- [[../../03_Decisions_ADR/ADR-0015-zero-to-hero-onboarding-guide-architecture|ADR-0015]]: Архитектура практического руководства Zero-to-Hero Onboarding Guide и интеграция ментальных моделей.
- [[../../03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]]: Барьер единичной задачи и протокол гарантированной остановки (Single-Task Execution Barrier & Stop-on-Complete Protocol).

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 88.4 KB | `867757bad12d737fa8409fdfea41e63850c9658f8e5fb0cc4a60c62e6351ec26` | `dist/install.py` |
| `RELEASE_NOTES.md` | 6.4 KB | `1469cd999b113ab5a8f98ad4eb9c96e996e1c936d865186d8dcf431cecaf421e` | `dist/RELEASE_NOTES.md` |

---

## 🔍 Инструкция по проверке целостности артефактов

```bash
# Проверка в PowerShell (Windows)
Get-FileHash -Path dist/install.py -Algorithm SHA256

# Проверка в Bash / macOS / Linux
sha256sum dist/install.py
# или
shasum -a 256 dist/install.py
```

---

## 📋 Чеклист верификации и приемки релиза
- [x] Все задачи фазы 8 завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.8.0.md`.
