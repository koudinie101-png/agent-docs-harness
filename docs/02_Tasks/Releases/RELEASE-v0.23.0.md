---
id: RELEASE-v0.23.0
title: "Релиз v0.23.0: Фаза 23"
version: "0.23.0"
phase: 23
status: completed
date: 2026-10-18
git_tag: "v0.23.0"
github_release_url: "https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.23.0"
mode: "github"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "167.6 KB"
    sha256: "985871c5c255719e285b21aad06df20ec13cf6ca12b99e4baf9225a4fcb0c222"
tags:
  - release
  - changelog
  - v0.23.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.23.0: Фаза 23

> **Версия:** v0.23.0  
> **Фаза:** 23  
> **Дата:** 2026-10-18  
> **Режим публикации:** GitHub Release  
> **Git Tag:** `v0.23.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
Официальный релиз v0.23.0 по завершении Фазы 23: контур процедурной памяти получил механический Tier 1-аудит ссылочной целостности check_memory_consistency() в kb_lint.py (4 проверки, неблокирующие WARN), устранены исторические висячие ссылки INC-001/INC-002 и зафиксирована процедура заведения инцидента; кроме того, герметизированы CI-тесты git-identity и dashboard (BUG-011/BUG-012), вернув зелёный гейт Rules Check.

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/23_MemoryIntegrity/TASK-089-memory-consistency-lint-and-incident-procedure|TASK-089]]: Целостность процедурной памяти: check_memory_consistency() в kb_lint, чистка висячих INC-ссылок и процедура заведения инцидента.

### 🐛 Исправленные дефекты (Bug Fixes)
- [[../Bugs/BUG-011-ci-git-identity-hermetic-test|BUG-011]]: Rules Check: test_05_git_local_setup зависит от глобальной Git identity (exit 128 на чистом runner).
- [[../Bugs/BUG-012-dashboard-env-and-live-api-test|BUG-012]]: Rules Check: test_render_status_dashboard зависит от GITHUB_REPOSITORY и ходит в живой GitHub API.

### 🏛️ Архитектурные решения (ADR)
- [[../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]: Архитектура самообучающегося контура дефектов (Defect Loop), слои надежности Quality Gates (Tier 1–3) и фильтрация инициатив FB-GH-3.
- [[../../03_Decisions_ADR/ADR-0029-fine-grained-task-symbol-contracts-and-line-drift-rejection|ADR-0029]]: Символьные контракты скоупа задач (Symbolic Scope) и отказ от фиксации номеров строк (Line Drift Prevention).

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 167.6 KB | `985871c5c255719e285b21aad06df20ec13cf6ca12b99e4baf9225a4fcb0c222` | `dist/install.py` |

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
- [x] Все задачи фазы 23 завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.23.0.md`.
