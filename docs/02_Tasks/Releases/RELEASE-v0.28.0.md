---
id: RELEASE-v0.28.0
title: "Релиз v0.28.0: Фазы 28 и 29 (Кумулятивный)"
version: "0.28.0"
phase: 29
phases: [28, 29]
status: completed
date: 2026-10-25
git_tag: "v0.28.0"
github_release_url: "https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.28.0"
mode: "github"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "176.5 KB"
    sha256: "5d8a2493062d108874aa3a48aef6b3391a76dad8ee8a5735f02e6b5fa8641bad"
tags:
  - release
  - changelog
  - cumulative
  - v0.28.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.28.0: Фазы 28 и 29 (Кумулятивный)

> **Версия:** v0.28.0  
> **Фазы:** 28 и 29 (Кумулятивный)  
> **Дата:** 2026-10-25  
> **Режим публикации:** GitHub Release  
> **Git Tag:** `v0.28.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
CI-доставка линта и правило простого языка: GitHub Action (composite), pre-commit-хук, реальные алерты в Code Scanning с путями от корня репозитория (BUG-013 закрыт), правило PLAIN-LANGUAGE (Tier 2) в корпусе и в установщике, sandbox-раннер тестов в scripts/. DEBT-004 и DEBT-005 погашены; 193 теста, бюджет установщика 182 000 B.

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/28_GateHygiene/TASK-104-sandbox-test-runner-promotion|TASK-104]]: Промоушен sandbox-раннера тестов в scripts/ (DEBT-005).
- [[../Specs/28_GateHygiene/TASK-105-composite-action-and-readme|TASK-105]]: Composite GitHub Action для линта и раздел README.
- [[../Specs/28_GateHygiene/TASK-107-pre-commit-hooks-and-readme|TASK-107]]: pre-commit hook для линта и два рецепта в README.
- [[../Specs/28_GateHygiene/TASK-108-code-scanning-workflow|TASK-108]]: Code Scanning: собственный SARIF-workflow и исключение из бандла.
- [[../Specs/28_GateHygiene/TASK-109-debt004-decision|TASK-109]]: Решение по DEBT-004: проверка аннотаций и закрытие долга.
- [[../Specs/29_PlainLanguage/TASK-106-plain-language-acceptance|TASK-106]]: Принять правило PLAIN-LANGUAGE: ADR, свежесть бандла и бюджет.

### 🐛 Исправленные дефекты (Bug Fixes)
- [[../Bugs/BUG-013-sarif-paths-are-docs-relative|BUG-013]]: SARIF artifactLocation.uri относительный к docs/, а не к корню репозитория.

### 🏛️ Архитектурные решения (ADR)
- [[../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]: Архитектура самообучающегося контура дефектов (Defect Loop), слои надежности Quality Gates (Tier 1–3) и фильтрация инициатив FB-GH-3.
- [[../../03_Decisions_ADR/ADR-0032-machine-readable-lint-contract-and-rule-registry|ADR-0032]]: Машинно-читаемый контракт линтера: модель Finding, реестр KB-XXX и три рендерера.
- [[../../03_Decisions_ADR/ADR-0033-plain-language-contract|ADR-0033]]: Контракт простого языка: пользователь — не разработчик.

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 176.5 KB | `5d8a2493062d108874aa3a48aef6b3391a76dad8ee8a5735f02e6b5fa8641bad` | `dist/install.py` |

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
- [x] Все задачи фаз 28 и 29 завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.28.0.md`.
