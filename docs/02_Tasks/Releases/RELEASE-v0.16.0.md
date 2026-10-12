---
id: RELEASE-v0.16.0
title: "Релиз v0.16.0: Фаза 16"
version: "0.16.0"
phase: 16
status: completed
date: 2026-10-12
git_tag: "v0.16.0"
github_release_url: ""
mode: "local-only"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "131.5 KB"
    sha256: "c7aa191358f21f7c8096f564e0f68758df4f8e482d590c641bde20679af1eae8"
  - name: "RELEASE_NOTES.md"
    path: "dist/RELEASE_NOTES.md"
    size: "3.6 KB"
    sha256: "2d89a853d8485cf4349f9f97c82d2e4e2356d49c227e8de050d43dc208351a0f"
tags:
  - release
  - changelog
  - v0.16.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.16.0: Фаза 16

> **Версия:** v0.16.0  
> **Фаза:** 16  
> **Дата:** 2026-10-12  
> **Режим публикации:** Local-Only Package  
> **Git Tag:** `v0.16.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
Официальный релиз v0.16.0 по завершении Фазы 16.

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/16_MemoryAndQualityGates/TASK-061-memory-infrastructure-and-patterns-index|TASK-061]]: Инфраструктура процедурной памяти (docs/06_Memory/, шаблон TEMPLATE_INCIDENT.md и агрегированный индекс patterns.md).
- [[../Specs/16_MemoryAndQualityGates/TASK-062-lifecycle-memory-checkpoints-and-promotion|TASK-062]]: Точки чтения памяти в жизненном цикле (kb-implement, kb-complete) и протокол двухосевого промоушена.
- [[../Specs/16_MemoryAndQualityGates/TASK-063-quality-gates-tier-matrix-and-agent-rules|TASK-063]]: Слои надежности Quality Gates (Tier 1–3) в AGENTS.md и руководстве Onboarding.md.
- [[../Specs/16_MemoryAndQualityGates/TASK-064-kb-lint-memory-audit-bundler-and-e2e|TASK-064]]: Контроль лимита памяти в scripts/kb_lint.py, бандлинг install.py, E2E тесты и Living Spec sync.
- [[../Specs/16_MemoryAndQualityGates/TASK-065-align-cli-flags-and-sync-readme|TASK-065]]: Выравнивание CLI-флагов и синхронизация README.md.

### 🐛 Исправленные дефекты (Bug Fixes)
- [[../Bugs/BUG-002-release-notes-hardcoded-install-script|BUG-002]]: Хардкод установки harness-а (install.py) в публичных релизных записках scripts/kb_release.py.
- [[../Bugs/BUG-003-release-silent-local-fallback-missing-gh|BUG-003]]: Бесшумный откат в локальный режим при отсутствии GitHub CLI (gh) в kb-release.
- [[../Bugs/BUG-004-release-notes-changelog-self-link|BUG-004]]: Циклическая ссылка на саму себя в блоке Full Changelog релизных записок.

### 🏛️ Архитектурные решения (ADR)
- [[../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]: Архитектура самообучающегося контура дефектов (Defect Loop), слои надежности Quality Gates (Tier 1–3) и фильтрация инициатив FB-GH-3.

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 131.5 KB | `c7aa191358f21f7c8096f564e0f68758df4f8e482d590c641bde20679af1eae8` | `dist/install.py` |
| `RELEASE_NOTES.md` | 3.6 KB | `2d89a853d8485cf4349f9f97c82d2e4e2356d49c227e8de050d43dc208351a0f` | `dist/RELEASE_NOTES.md` |

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
- [x] Все задачи фазы 16 завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.16.0.md`.
