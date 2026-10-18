---
id: RELEASE-v0.21.0
title: "Релиз v0.21.0: Фаза 21"
version: "0.21.0"
phase: 21
status: completed
date: 2026-10-18
git_tag: "v0.21.0"
github_release_url: "https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.21.0"
mode: "github"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "162.7 KB"
    sha256: "f40c395e85fe1b17cf4d418def0bfc435fbc8484d3f3a68decd647960d9a66a9"
tags:
  - release
  - changelog
  - v0.21.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.21.0: Фаза 21

> **Версия:** v0.21.0  
> **Фаза:** 21  
> **Дата:** 2026-10-18  
> **Режим публикации:** GitHub Release  
> **Git Tag:** `v0.21.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
Официальный релиз v0.21.0 по завершении Фазы 21: замкнут сквозной жизненный цикл технического долга DEBT-XXX во всех режимах (/kb-plan, /kb-task, /kb-triage, /kb-complete), кодовые теги // DEBT-XXX приравнены к // ROADMAP-<ID>, введён семантический кросс-чек TechDebt.md с фазами #techdebt в scripts/kb_lint.py и пересобран автономный монолит install.py (162.7 KB).

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/21_TechDebtLifecycle/TASK-082-kb-lint-tech-debt-cross-check-and-todo-tags|TASK-082]]: Семантический кросс-чек TechDebt.md с фазами/задачами #techdebt и поддержка кодовых тегов // DEBT-XXX в scripts/kb_lint.py.
- [[../Specs/21_TechDebtLifecycle/TASK-083-skills-agents-and-templates-tech-debt-lifecycle|TASK-083]]: Сквозной цикл DEBT-XXX в скиллах (kb-plan, kb-task, kb-triage, kb-complete), правилах AGENTS.md, шаблонах и install.py.
- [[../Specs/21_TechDebtLifecycle/TASK-084-bundle-rebuild-e2e-tests-and-living-spec-sync|TASK-084]]: Сборка монолита build_installer.py, E2E тестирование в tests/test_installer.py и синхронизация Living Spec (SPEC.md, README.md, Onboarding.md).

### 🐛 Исправленные дефекты (Bug Fixes)
- Критических дефектов и регрессий за период фазы не зафиксировано.

### 🏛️ Архитектурные решения (ADR)
- [[../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]: Архитектура Zero Dependencies на стандартной библиотеке Python 3.
- [[../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]: Архитектура самообучающегося контура дефектов (Defect Loop), слои надежности Quality Gates (Tier 1–3) и фильтрация инициатив FB-GH-3.
- [[../../03_Decisions_ADR/ADR-0028-end-to-end-tech-debt-lifecycle-and-lint-enforcement|ADR-0028]]: Сквозной жизненный цикл технического долга (DEBT-XXX), интеграция в режимы 1–3 и семантический контроль в kb_lint.py.

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 162.7 KB | `f40c395e85fe1b17cf4d418def0bfc435fbc8484d3f3a68decd647960d9a66a9` | `dist/install.py` |

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
- [x] Все задачи фазы 21 завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.21.0.md`.
