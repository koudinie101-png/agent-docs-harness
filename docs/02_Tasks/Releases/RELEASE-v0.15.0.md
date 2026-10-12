---
id: RELEASE-v0.15.0
title: "Релиз v0.15.0: Фаза 15"
version: "0.15.0"
phase: 15
status: completed
date: 2026-10-12
git_tag: "v0.15.0"
github_release_url: ""
mode: "local-only"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "124.8 KB"
    sha256: "caa5700dde2cb9b349221c07ef0f12ad9b7b0dc1256a294c02e3c903e3ad995d"
  - name: "RELEASE_NOTES.md"
    path: "dist/RELEASE_NOTES.md"
    size: "4.0 KB"
    sha256: "7c5405f42d895d857cfbbe68cf82b21c5df6251c904c3e3c9869f328036472a3"
tags:
  - release
  - changelog
  - v0.15.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.15.0: Фаза 15

> **Версия:** v0.15.0  
> **Фаза:** 15  
> **Дата:** 2026-10-12  
> **Режим публикации:** Local-Only Package  
> **Git Tag:** `v0.15.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
Официальный релиз v0.15.0 по завершении Фазы 15.

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/15_LatencyAndChannels/TASK-057-zero-roundtrip-dispatch-and-hot-invariants|TASK-057]]: Архитектура Zero Round-Trip Dispatch и горячие инварианты в правилах агентов.
- [[../Specs/15_LatencyAndChannels/TASK-058-channel-transparency-git-remote-and-status-dashboard|TASK-058]]: Прозрачный UX инжеста, автодетект Git Remote и дашборд статуса источников в scripts/kb_ingest.py.
- [[../Specs/15_LatencyAndChannels/TASK-059-channel-triage-feedback-and-phase-consistency-lint|TASK-059]]: Прозрачный фидбек источников в /kb-triage и семантический контроль фаз в scripts/kb_lint.py.
- [[../Specs/15_LatencyAndChannels/TASK-060-installer-bundling-e2e-and-living-spec|TASK-060]]: Синхронизация инсталлятора install.py / build_installer.py, регрессионные E2E тесты и актуализация Living Spec.

### 🐛 Исправленные дефекты (Bug Fixes)
- Критических дефектов и регрессий за период фазы не зафиксировано.

### 🏛️ Архитектурные решения (ADR)
- [[../../03_Decisions_ADR/ADR-0013-zero-roundtrip-dispatch-and-hot-invariants-architecture|ADR-0013]]: Архитектура Zero Round-Trip Dispatch и горячие инварианты (Hot Invariants) против латентности скиллов.
- [[../../03_Decisions_ADR/ADR-0024-user-centric-ingestion-and-channel-transparency|ADR-0024]]: Архитектура прозрачности каналов обратной связи, автоопределения репозитория и диагностического статуса (Channel Transparency & Auto-Detection).

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 124.8 KB | `caa5700dde2cb9b349221c07ef0f12ad9b7b0dc1256a294c02e3c903e3ad995d` | `dist/install.py` |
| `RELEASE_NOTES.md` | 4.0 KB | `7c5405f42d895d857cfbbe68cf82b21c5df6251c904c3e3c9869f328036472a3` | `dist/RELEASE_NOTES.md` |

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
- [x] Все задачи фазы 15 завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.15.0.md`.
