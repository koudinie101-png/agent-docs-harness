---
id: RELEASE-v0.10.0
title: "Релиз v0.10.0: Фазы 9 и 10 (Кумулятивный)"
version: "0.10.0"
phase: 10
phases: [9, 10]
status: completed
date: 2026-10-03
git_tag: "v0.10.0"
github_release_url: ""
mode: "local-only"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "95.1 KB"
    sha256: "1e31643af92b5fb3c8347e71c70e02a48c8abe9d764a3c8c2ed09320b7983a19"
  - name: "RELEASE_NOTES.md"
    path: "dist/RELEASE_NOTES.md"
    size: "7.3 KB"
    sha256: "2fdab9236d79856d79c2f66d8b3126c30e15722502a279cbaeb57ce5bb61953e"
  - name: "RELEASE_NOTES_v0.7.0.md"
    path: "dist/RELEASE_NOTES_v0.7.0.md"
    size: "7.5 KB"
    sha256: "e99cb0793368aa4d41212636347e10be833203aea82aef0d00dfc904edeb9e24"
tags:
  - release
  - changelog
  - cumulative
  - v0.10.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.10.0: Фазы 9 и 10 (Кумулятивный)

> **Версия:** v0.10.0  
> **Фазы:** 9 и 10 (Кумулятивный)  
> **Дата:** 2026-10-03  
> **Режим публикации:** Local-Only Package  
> **Git Tag:** `v0.10.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
Кумулятивный релиз v0.10.0: Барьер однозадачного исполнения (Stop-on-Complete Protocol), протокол генезиса спецификаций (Spec Genesis Protocol), стандарт High-SNR Release Notes и устранение регрессии CI release notes (BUG-001).

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/09_Guardrails/TASK-033-single-task-barrier-and-stop-yield-skills|TASK-033]]: Нормативный инвариант барьера единичной задачи в AGENTS.md и терминальный шаг Stop & Yield Control в kb-implement и kb-complete.
- [[../Specs/09_Guardrails/TASK-034-devlog-semantic-guard-and-kb-lint-audit|TASK-034]]: Семантический протокол следующего шага в TEMPLATE_DEVLOG.md, аудит формулировок check_devlog_semantic_guard в scripts/kb_lint.py и тесты в tests/test_kb_lint.py.
- [[../Specs/09_Guardrails/TASK-035-installer-bundling-e2e-and-docs|TASK-035]]: Синхронизация генераторов правил и шаблонов в install.py / build_installer.py (включая --update), сквозные E2E тесты в tests/test_installer.py, обновление README.md и docs/Onboarding.md.
- [[../Specs/10_SpecLifecycle/TASK-036-spec-genesis-and-zero-state-guardrails|TASK-036]]: Spec Genesis Protocol & Zero-State Guardrails (kb-init, kb-plan, kb-task, AGENTS.md).
- [[../Specs/10_SpecLifecycle/TASK-037-high-snr-release-notes-and-phase-adr-scoping|TASK-037]]: High-SNR Release Notes Generator & Phase ADR Scoping (scripts/kb_release.py, kb-release, тесты).
- [[../Specs/10_SpecLifecycle/TASK-038-installer-bundling-e2e-and-docs|TASK-038]]: Синхронизация инсталлятора, сквозные E2E тесты и актуализация документации.

### 🐛 Исправленные дефекты (Bug Fixes)
- [[../Bugs/BUG-001-ci-release-notes-phase-fallback|BUG-001]]: Рассинхронизация номера фазы и описания релиза в CI release.yml (fallback на Фазу 1).

### 🏛️ Архитектурные решения (ADR)
- [[../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]: Архитектура Zero Dependencies на стандартной библиотеке Python 3.
- [[../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]]: Архитектура оптимизации токенов и контекстной эффективности (High-SNR Token Architecture).
- [[../../03_Decisions_ADR/ADR-0010-github-release-notes-and-public-distribution-standard|ADR-0010]]: Стандарт оформления публичных релизов на GitHub и двухформатный экспорт Release Notes.
- [[../../03_Decisions_ADR/ADR-0014-greenfield-idea-first-initialization-and-living-spec-protocol|ADR-0014]]: Архитектура Greenfield-инициализации от идеи (Idea-First) и протокол Living Spec против дрифта документации.
- [[../../03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]]: Барьер единичной задачи и протокол гарантированной остановки (Single-Task Execution Barrier & Stop-on-Complete Protocol).
- [[../../03_Decisions_ADR/ADR-0017-release-notes-adr-exclusion-and-high-snr-standard|ADR-0017]]: Исключение секции архитектурных решений (ADR) из публичных релизных заметок в пользу чистого сигнала (High-SNR Release Notes).
- [[../../03_Decisions_ADR/ADR-0018-spec-genesis-protocol-and-zero-state-handling|ADR-0018]]: Протокол рождения Мастер-Спецификации (Spec Genesis), детект Zero-State и отказ от неконтролируемой автогенерации SPEC.md.

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 95.1 KB | `1e31643af92b5fb3c8347e71c70e02a48c8abe9d764a3c8c2ed09320b7983a19` | `dist/install.py` |
| `RELEASE_NOTES.md` | 7.3 KB | `2fdab9236d79856d79c2f66d8b3126c30e15722502a279cbaeb57ce5bb61953e` | `dist/RELEASE_NOTES.md` |
| `RELEASE_NOTES_v0.7.0.md` | 7.5 KB | `e99cb0793368aa4d41212636347e10be833203aea82aef0d00dfc904edeb9e24` | `dist/RELEASE_NOTES_v0.7.0.md` |

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
- [x] Все задачи фаз 9 и 10 завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.10.0.md`.
