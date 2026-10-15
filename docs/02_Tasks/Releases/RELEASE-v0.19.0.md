---
id: RELEASE-v0.19.0
title: "Релиз v0.19.0: Фаза 19"
version: "0.19.0"
phase: 19
status: completed
date: 2026-10-15
git_tag: "v0.19.0"
github_release_url: "https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.19.0"
mode: "github"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "157.7 KB"
    sha256: "3360889dbaf7fb1b23829022ef0191cdbdf04a743752b080e9b1a34183442601"
tags:
  - release
  - changelog
  - v0.19.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.19.0: Фаза 19

> **Версия:** v0.19.0  
> **Фаза:** 19  
> **Дата:** 2026-10-15  
> **Режим публикации:** GitHub Release  
> **Git Tag:** `v0.19.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
Официальный релиз v0.19.0 по завершении Фазы 19.

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/19_EngineeringGates/TASK-075-tech-debt-registry-and-triage-rules|TASK-075]]: Инфраструктура реестра техдолга, скаффолдинг в install.py и правила триажа P1/P2 vs P3.
- [[../Specs/19_EngineeringGates/TASK-076-prior-art-gate-roadmap-tagging-and-benchmarks|TASK-076]]: Инженерные барьеры в шаблонах и правилах: Prior-Art Gate, трассировка // ROADMAP-<ID> и замеры >= 3 прогонов.
- [[../Specs/19_EngineeringGates/TASK-077-gui-acceptance-checklist-and-kb-lint-audit|TASK-077]]: Чеклист приемочного тестирования GUI («UI не лжёт») в TEMPLATE_TEST.md и аудит целостности TechDebt.md в scripts/kb_lint.py.
- [[../Specs/19_EngineeringGates/TASK-078-bundling-e2e-tests-and-living-spec|TASK-078]]: Синхронизация install.py, сборка монолита через build_installer.py, E2E тесты и актуализация Living Spec.

### 🐛 Исправленные дефекты (Bug Fixes)
- Критических дефектов и регрессий за период фазы не зафиксировано.

### 🏛️ Архитектурные решения (ADR)
- [[../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]: Архитектура самообучающегося контура дефектов (Defect Loop), слои надежности Quality Gates (Tier 1–3) и фильтрация инициатив FB-GH-3.

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 157.7 KB | `3360889dbaf7fb1b23829022ef0191cdbdf04a743752b080e9b1a34183442601` | `dist/install.py` |

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
- [x] Все задачи фазы 19 завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.19.0.md`.
