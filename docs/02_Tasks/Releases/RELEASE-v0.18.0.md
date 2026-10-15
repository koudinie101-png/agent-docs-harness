---
id: RELEASE-v0.18.0
title: "Релиз v0.18.0: Фаза 18"
version: "0.18.0"
phase: 18
status: completed
date: 2026-10-15
git_tag: "v0.18.0"
github_release_url: "https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.18.0"
mode: "github"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "150.4 KB"
    sha256: "8449faf8e61fc8f5d494c387d96ed38107c12744c3807a66c637f6aa9c4a6ea1"
tags:
  - release
  - changelog
  - v0.18.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.18.0: Фаза 18

> **Версия:** v0.18.0  
> **Фаза:** 18  
> **Дата:** 2026-10-15  
> **Режим публикации:** GitHub Release  
> **Git Tag:** `v0.18.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
Официальный релиз v0.18.0 по завершении Фазы 18.

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/18_VisualHarness/TASK-071-asset-storage-composite-ui-and-obsidian-dx|TASK-071]]: Архитектура хранения ассетов, композитный --ui и Obsidian DX в install.py.
- [[../Specs/18_VisualHarness/TASK-072-media-assets-lint-and-release-checks|TASK-072]]: Механический контроль медиа-ассетов в scripts/kb_lint.py и scripts/kb_release.py.
- [[../Specs/18_VisualHarness/TASK-073-the-4-state-matrix-visual-dod-and-templates|TASK-073]]: Матрица 4 состояний (The 4-State Matrix), Visual DoD и шаблоны жизненного цикла в AGENTS.md.
- [[../Specs/18_VisualHarness/TASK-074-bundling-e2e-tests-and-living-spec|TASK-074]]: Бандлинг инсталлятора build_installer.py, сквозные E2E тесты и актуализация Living Spec.

### 🐛 Исправленные дефекты (Bug Fixes)
- Критических дефектов и регрессий за период фазы не зафиксировано.

### 🏛️ Архитектурные решения (ADR)
- [[../../03_Decisions_ADR/ADR-0026-heterogeneous-ui-ux-and-visual-asset-management|ADR-0026]]: Контур UI/UX, управление визуальными ассетами и архитектура гетерогенных multi-target систем.

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 150.4 KB | `8449faf8e61fc8f5d494c387d96ed38107c12744c3807a66c637f6aa9c4a6ea1` | `dist/install.py` |

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
- [x] Все задачи фазы 18 завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.18.0.md`.
