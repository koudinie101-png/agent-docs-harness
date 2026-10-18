---
id: RELEASE-v0.25.0
title: "Релиз v0.25.0: Фаза 25"
version: "0.25.0"
phase: 25
status: completed
date: 2026-10-18
git_tag: "v0.25.0"
github_release_url: "https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.25.0"
mode: "github"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "171.0 KB"
    sha256: "533f279f80e31eb2feb7ec5229c3b7c8ac0900732022b7436fa558b6454f7dac"
tags:
  - release
  - changelog
  - v0.25.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.25.0: Фаза 25

> **Версия:** v0.25.0  
> **Фаза:** 25  
> **Дата:** 2026-10-18  
> **Режим публикации:** GitHub Release  
> **Git Tag:** `v0.25.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
Символьные контракты задач (ADR-0029): иерархический скоуп в шаблонах, поведение Mode 2/3, advisory-линт check_symbolic_scope и state-aware next step; пересборка бандла и Living Spec.

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/25_SymbolicScope/TASK-094-symbolic-contract-templates-and-source-guard|TASK-094]]: Символьный контракт в шаблонах задач, Tier 1 source-guard и замер бюджетов.
- [[../Specs/25_SymbolicScope/TASK-095-symbolic-behavior-and-advisory-lint|TASK-095]]: Поведение Mode 2/3, advisory-контракт и state-aware next step.
- [[../Specs/25_SymbolicScope/TASK-096-bundle-e2e-and-living-spec|TASK-096]]: Пересборка бандла, E2E и Living Spec Sync для символьного скоупа.

### 🐛 Исправленные дефекты (Bug Fixes)
- Критических дефектов не зафиксировано.
- **P2 (TASK-096):** восстановлена фраза `Stop & Yield Control` в `/kb-complete` после регрессии TASK-095; source-guard расширен, чтобы разрыв между источником скилла и бандлом не маскировал потерю.

### 🏛️ Архитектурные решения (ADR)
- [[../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]: Архитектура Zero Dependencies на стандартной библиотеке Python 3.
- [[../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]]: Архитектура оптимизации токенов и контекстной эффективности (High-SNR Token Architecture).
- [[../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]: Архитектура самообучающегося контура дефектов (Defect Loop), слои надежности Quality Gates (Tier 1–3) и фильтрация инициатив FB-GH-3.
- [[../../03_Decisions_ADR/ADR-0029-fine-grained-task-symbol-contracts-and-line-drift-rejection|ADR-0029]]: Символьные контракты скоупа задач (Symbolic Scope) и отказ от фиксации номеров строк (Line Drift Prevention).

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 171.0 KB | `533f279f80e31eb2feb7ec5229c3b7c8ac0900732022b7436fa558b6454f7dac` | `dist/install.py` |

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
- [x] Все задачи фазы 25 завершены и проверены в `Roadmap.md`.
- [x] Автоматические тесты (**163**, `python tmp/run_tests.py`) пройдены; отдельных чек-листов в `05_Testing/` нет.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.25.0.md`.
