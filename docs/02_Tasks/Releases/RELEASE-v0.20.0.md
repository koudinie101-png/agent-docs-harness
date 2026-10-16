---
id: RELEASE-v0.20.0
title: "Релиз v0.20.0: Фаза 20"
version: "0.20.0"
phase: 20
status: completed
date: 2026-10-16
git_tag: "v0.20.0"
github_release_url: "https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.20.0"
mode: "github"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "159.9 KB"
    sha256: "76737116ad8b896a1c16e43938005e96eb15315e4b6ce9e7f0bf709b4b9caca2"
tags:
  - release
  - changelog
  - v0.20.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.20.0: Фаза 20

> **Версия:** v0.20.0  
> **Фаза:** 20  
> **Дата:** 2026-10-16  
> **Режим публикации:** GitHub Release  
> **Git Tag:** `v0.20.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
Официальный релиз v0.20.0 по завершении Фазы 20.

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/20_AssetHardening/TASK-079-asset-layout-lint-and-strict-media-resolution|TASK-079]]: Строгая резолюция медиа-путей и проверка топологии check_asset_layout() в scripts/kb_lint.py.
- [[../Specs/20_AssetHardening/TASK-080-mockup-namespace-and-flows-convention-in-installer-and-templates|TASK-080]]: Стандартизация TASK-XXX/ для макетов и конвенции mockups/flows/ в install.py, шаблонах и правилах агентов.
- [[../Specs/20_AssetHardening/TASK-081-e2e-verification-bundle-rebuild-and-living-spec-sync|TASK-081]]: Сквозные E2E-тесты в tests/test_installer.py, пересборка бандла install.py и синхронизация Living Spec.

### 🐛 Исправленные дефекты (Bug Fixes)
- Критических дефектов и регрессий за период фазы не зафиксировано.

### 🏛️ Архитектурные решения (ADR)
- [[../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]: Архитектура Zero Dependencies на стандартной библиотеке Python 3.
- [[../../03_Decisions_ADR/ADR-0027-task-scoped-asset-namespaces-and-layout-linting|ADR-0027]]: Task-Scoped пространства имен визуальных макетов (TASK-XXX/), жизненный цикл As-Is/To-Be и валидация топологии docs/assets/ в kb_lint.py.

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 159.9 KB | `76737116ad8b896a1c16e43938005e96eb15315e4b6ce9e7f0bf709b4b9caca2` | `dist/install.py` |

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
- [x] Все задачи фазы 20 завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.20.0.md`.
