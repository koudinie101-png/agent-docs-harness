---
id: RELEASE-v0.7.0
title: "Релиз v0.7.0: Фаза 7"
version: "0.7.0"
phase: 7
status: completed
date: 2026-10-01
git_tag: "v0.7.0"
github_release_url: ""
mode: "local-only"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "83.3 KB"
    sha256: "1e386242736e166e836fe5116ccbdad64dfcab48e97781f302b40e8764d68d4b"
tags:
  - release
  - changelog
  - v0.7.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.7.0: Фаза 7

> **Версия:** v0.7.0  
> **Фаза:** 7  
> **Дата:** 2026-10-01  
> **Режим публикации:** Local-Only Package  
> **Git Tag:** `v0.7.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
Стандарт оформления публичных релизов на GitHub и экспорт Release Notes: двухформатный экспорт в kb_release.py (RELEASE-vX.Y.Z.md для базы знаний и dist/RELEASE_NOTES.md для GitHub), автоконвертер викиссылок в чистый Markdown, автоматизация передачи body_path в GitHub Actions release.yml, актуализация скилла /kb-release и упаковка в автономный инсталлятор install.py (83.3 КБ).

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/07_Distribution/TASK-025-dual-export-and-wikilinks-converter|TASK-025]]: Двухформатный экспорт и автоконвертер викиссылок в scripts/kb_release.py.
- [[../Specs/07_Distribution/TASK-026-github-actions-release-body-and-installer-template|TASK-026]]: Автоматизация передачи заметок в CI release.yml и синхронизация встроенного шаблона.
- [[../Specs/07_Distribution/TASK-027-kb-release-skill-and-notes-file|TASK-027]]: Актуализация скилла kb-release и шаблона TEMPLATE_RELEASE.md.
- [[../Specs/07_Distribution/TASK-028-installer-bundling-and-e2e-verification|TASK-028]]: Сборка инсталлятора, регрессионные E2E тесты и аудит целостности дистрибутива.

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

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 83.3 KB | `1e386242736e166e836fe5116ccbdad64dfcab48e97781f302b40e8764d68d4b` | `dist/install.py` |

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
- [x] Все задачи фазы 7 завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.7.0.md`.
