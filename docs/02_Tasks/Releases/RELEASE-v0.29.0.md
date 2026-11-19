---
id: RELEASE-v0.29.0
title: "Релиз v0.29.0: Фазы 30 и 31 (Кумулятивный)"
version: "0.29.0"
phase: 31
phases: [30, 31]
status: completed
date: 2026-11-19
git_tag: "v0.29.0"
github_release_url: "https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.29.0"
mode: "github"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "191.4 KB"
    sha256: "b060d04ef4870d593d5900c7e55345d20a9cf505a41b7cc25f4b628e99fe24bb"
tags:
  - release
  - changelog
  - cumulative
  - v0.29.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.29.0: Фазы 30 и 31 (Кумулятивный)

> **Версия:** v0.29.0  
> **Фазы:** 30 и 31 (Кумулятивный)  
> **Дата:** 2026-11-19  
> **Режим публикации:** GitHub Release  
> **Git Tag:** `v0.29.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
Завершение Волны 1: детерминированная навигация и граф задач (kb_state, depends_on, KB-010) и безопасный детерминированный автофикс (kb_lint --fix, --write, Zero Data Loss, JSON/SARIF fixes, pre-commit hook).

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/30_DeterministicNavigation/TASK-110-task-dependency-graph-and-kb010|TASK-110]]: Граф зависимостей задач (depends_on) и правило линтера KB-010.
- [[../Specs/30_DeterministicNavigation/TASK-111-deterministic-navigation-kb-state|TASK-111]]: Ядро навигации scripts/kb_state.py.
- [[../Specs/30_DeterministicNavigation/TASK-112-kb-state-integration-and-delivery|TASK-112]]: Интеграция kb_state в скиллы, бандлинг в install.py и поставка.
- [[../Specs/31_SafeAutoFix/TASK-113-kb-lint-autofix-core|TASK-113]]: Ядро хирургического автофикса в scripts/kb_lint.py.
- [[../Specs/31_SafeAutoFix/TASK-114-autofix-formats-and-skills-integration|TASK-114]]: Машинно-читаемый контракт (JSON/SARIF fixable) и интеграция автофикса в скиллы.
- [[../Specs/31_SafeAutoFix/TASK-115-autofix-delivery-spec-and-e2e|TASK-115]]: Бандлинг в install.py, CI-хуки, Living Spec и E2E-тесты поставки автофикса.

### 🐛 Исправленные дефекты (Bug Fixes)
- Критических дефектов и регрессий за период фазы не зафиксировано.

### 🏛️ Архитектурные решения (ADR)
- [[../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]: Архитектура Zero Dependencies на стандартной библиотеке Python 3.
- [[../../03_Decisions_ADR/ADR-0032-machine-readable-lint-contract-and-rule-registry|ADR-0032]]: Машинно-читаемый контракт линтера: модель Finding, реестр KB-XXX и три рендерера.
- [[../../03_Decisions_ADR/ADR-0035-wave-1-deterministic-navigation-and-task-graph-standard|ADR-0035]]: Архитектурный стандарт Волны 1: детерминированная навигация (kb_state), граф зависимостей (depends_on) и консервативный автофикс.
- [[../../03_Decisions_ADR/ADR-0036-kb-lint-safe-autofix-standard|ADR-0036]]: Архитектурный стандарт безопасного автофикса в kb_lint.py (--fix, --write, Zero Data Loss).

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 191.4 KB | `b060d04ef4870d593d5900c7e55345d20a9cf505a41b7cc25f4b628e99fe24bb` | `dist/install.py` |

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
- [x] Все задачи фаз 30 и 31 завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.29.0.md`.
