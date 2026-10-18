---
id: RELEASE-v0.26.0
title: "Релиз v0.26.0: Фаза 26"
version: "0.26.0"
phase: 26
status: completed
date: 2026-10-18
git_tag: "v0.26.0"
github_release_url: "https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.26.0"
mode: "github"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "171.1 KB"
    sha256: "6eab6c96aae47a45af5e658560febbeab57c9d6801e1d27cf70a5bf4a6e57d8f"
tags:
  - release
  - changelog
  - v0.26.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.26.0: Фаза 26

> **Версия:** v0.26.0  
> **Фаза:** 26  
> **Дата:** 2026-10-18  
> **Режим публикации:** GitHub Release  
> **Git Tag:** `v0.26.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
Tech Debt Hardening: ужесточён CI-гейт Rules Check, очищен Icebox Kanban, выровнена нумерация разделов корпуса правил; /kb-task теперь автоматически линкует новую спеку в Roadmap.

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/26_TechDebt/TASK-097-clean-stale-kanban-icebox|TASK-097]]: Очистка устаревшего Icebox в Kanban.md.
- [[../Specs/26_TechDebt/TASK-098-rules-check-ci-hardening|TASK-098]]: Харденинг CI-гейта Rules Check (DEBT-002).
- [[../Specs/26_TechDebt/TASK-099-roadmap-permalink-at-spec-creation|TASK-099]]: Пермалинк спеки в Roadmap при /kb-task.
- [[../Specs/26_TechDebt/TASK-100-align-rules-section-numbering|TASK-100]]: Выравнивание нумерации разделов корпуса правил (DEBT-001).

### 🐛 Исправленные дефекты (Bug Fixes)
- Критических дефектов и регрессий за период фазы не зафиксировано.

### 🏛️ Архитектурные решения (ADR)
- [[../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]: Архитектура самообучающегося контура дефектов (Defect Loop), слои надежности Quality Gates (Tier 1–3) и фильтрация инициатив FB-GH-3.
- [[../../03_Decisions_ADR/ADR-0030-single-source-rule-compiler|ADR-0030]]: Single-Source Rule Compiler: корпус rules/AGENTS_CORE.md и детерминированный рендер правил агента.

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 171.1 KB | `6eab6c96aae47a45af5e658560febbeab57c9d6801e1d27cf70a5bf4a6e57d8f` | `dist/install.py` |

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
- [x] Все задачи фазы 26 завершены и проверены в `Roadmap.md`.
- [x] Автоматические тесты (**166**, `python tmp/run_tests.py`) пройдены; отдельных чек-листов в `05_Testing/` нет.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.26.0.md`.
