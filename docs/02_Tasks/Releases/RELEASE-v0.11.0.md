---
id: RELEASE-v0.11.0
title: "Релиз v0.11.0: Фаза 11"
version: "0.11.0"
phase: 11
status: completed
date: 2026-10-11
git_tag: "v0.11.0"
github_release_url: ""
mode: "local-only"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "99.0 KB"
    sha256: "c6b877a95817af8a9156666f4decaaceb498593a9ea130e2145a5734a4a105c7"
  - name: "RELEASE_NOTES.md"
    path: "dist/RELEASE_NOTES.md"
    size: "3.0 KB"
    sha256: "4e0bf47abf6519f2fca53dd31e4805519e3d309a30702340667f4e32e694d1b5"
tags:
  - release
  - changelog
  - v0.11.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.11.0: Фаза 11

> **Версия:** v0.11.0  
> **Фаза:** 11  
> **Дата:** 2026-10-11  
> **Режим публикации:** Local-Only Package  
> **Git Tag:** `v0.11.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
Официальный релиз v0.11.0: Жизненный цикл дефектов, изолированный триаж (Режим 2B kb-bug), TDD-исправление (/kb-implement BUG-XXX), строгий релизный таргетинг и префлайт-контроль блокеров.

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/11_BugLifecycle/TASK-039-template-bug-and-kb-bug-triage-skill|TASK-039]]: Рефакторинг TEMPLATE_BUG.md и скилла kb-bug (строгий триаж Режима 2B и терминальный Stop & Yield).
- [[../Specs/11_BugLifecycle/TASK-040-kb-implement-bug-lifecycle-and-tdd|TASK-040]]: Нативная поддержка дефектов в kb-implement (/kb-implement BUG-XXX и строгий TDD-цикл).
- [[../Specs/11_BugLifecycle/TASK-041-kb-release-defect-filtering-and-blockers|TASK-041]]: Релизный таргетинг и фильтрация дефектов в scripts/kb_release.py и тесты.
- [[../Specs/11_BugLifecycle/TASK-042-installer-bundling-e2e-and-docs|TASK-042]]: Синхронизация инсталлятора, сквозные E2E тесты и документация.

### 🐛 Исправленные дефекты (Bug Fixes)
- Критических дефектов и регрессий за период фазы не зафиксировано.

### 🏛️ Архитектурные решения (ADR)
- [[../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]: Архитектура Zero Dependencies на стандартной библиотеке Python 3.
- [[../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]]: Архитектура оптимизации токенов и контекстной эффективности (High-SNR Token Architecture).
- [[../../03_Decisions_ADR/ADR-0010-github-release-notes-and-public-distribution-standard|ADR-0010]]: Стандарт оформления публичных релизов на GitHub и двухформатный экспорт Release Notes.
- [[../../03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]]: Барьер единичной задачи и протокол гарантированной остановки (Single-Task Execution Barrier & Stop-on-Complete Protocol).
- [[../../03_Decisions_ADR/ADR-0019-bug-lifecycle-triage-and-release-targeting|ADR-0019]]: Архитектура жизненного цикла дефектов: изолированный триаж, релизный таргетинг и унификация Режима 3.

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 99.0 KB | `c6b877a95817af8a9156666f4decaaceb498593a9ea130e2145a5734a4a105c7` | `dist/install.py` |
| `RELEASE_NOTES.md` | 3.0 KB | `4e0bf47abf6519f2fca53dd31e4805519e3d309a30702340667f4e32e694d1b5` | `dist/RELEASE_NOTES.md` |

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
- [x] Все задачи фазы 11 завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.11.0.md`.
