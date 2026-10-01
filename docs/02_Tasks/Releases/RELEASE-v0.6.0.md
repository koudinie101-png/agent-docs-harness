---
id: RELEASE-v0.6.0
title: "Релиз v0.6.0: Фаза 6"
version: "0.6.0"
phase: 6
status: completed
date: 2026-10-01
git_tag: "v0.6.0"
github_release_url: ""
mode: "local-only"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "81.5 KB"
    sha256: "132776da84c4820caf3359598ec827594d541927bd6c857b7a8ee16647d03a7f"
tags:
  - release
  - changelog
  - v0.6.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.6.0: Фаза 6

> **Версия:** v0.6.0  
> **Фаза:** 6  
> **Дата:** 2026-10-01  
> **Режим публикации:** Local-Only Package  
> **Git Tag:** `v0.6.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
Discovery & Feasibility Lifecycle Integration: сквозная модель Double Diamond (Режимы 0-3), эволюция скилла /kb-research с двухпутевой воронкой (Icebox vs Отклоненные ADR), префлайт-чеки Pre-flight Nudge в /kb-plan, обновление канонических шаблонов TEMPLATE_ROADMAP и TEMPLATE_ONBOARDING, синхронизация автономного инсталлятора install.py (81.5 КБ).

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/06_Discovery/TASK-021-kb-research-evolution-and-roadmap-routing|TASK-021]]: Эволюция скилла kb-research: валидация продуктово-архитектурных гипотез и двухпутевая воронка регистрации в Roadmap.
- [[../Specs/06_Discovery/TASK-022-kb-plan-preflight-nudges-and-onboard|TASK-022]]: Префлайт-чеки в kb-plan и обновление скилла kb-onboard (4-этапный цикл).
- [[../Specs/06_Discovery/TASK-023-roadmap-onboarding-templates-update|TASK-023]]: Обновление шаблонов TEMPLATE_ROADMAP, TEMPLATE_ONBOARDING и руководства Onboarding.md.
- [[../Specs/06_Discovery/TASK-024-installer-sync-and-e2e-verification|TASK-024]]: Синхронизация инсталлятора install.py, E2E тесты и аудит целостности.

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

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 81.5 KB | `132776da84c4820caf3359598ec827594d541927bd6c857b7a8ee16647d03a7f` | `dist/install.py` |

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
- [x] Все задачи фазы 6 завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.6.0.md`.
