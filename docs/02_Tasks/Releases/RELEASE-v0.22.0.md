---
id: RELEASE-v0.22.0
title: "Релиз v0.22.0: Фаза 22"
version: "0.22.0"
phase: 22
status: completed
date: 2026-10-18
git_tag: "v0.22.0"
github_release_url: "https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.22.0"
mode: "github"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "165.6 KB"
    sha256: "8fac0aa7beeb40ab2a6665263267f0ebf4d64b720661f999922443771b8c2ccb"
tags:
  - release
  - changelog
  - v0.22.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.22.0: Фаза 22

> **Версия:** v0.22.0  
> **Фаза:** 22  
> **Дата:** 2026-10-18  
> **Режим публикации:** GitHub Release  
> **Git Tag:** `v0.22.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
Официальный релиз v0.22.0 по завершении Фазы 22: правила агента стали компилируемым артефактом — единый корпус rules/AGENTS_CORE.md, детерминированный рендерер в install.py, генерация корневого AGENTS.md с CI-гейтом --check, 13 Tier 1 тестов дрейфа и редакционная консолидация индекса до 24 правил; монолит install.py пересобран.

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/22_RuleCompiler/TASK-085-rules-corpus-renderer-and-bundling|TASK-085]]: Корпус правил rules/AGENTS_CORE.md, рендерер в install.py, упаковка в бандл и ADR-0030.
- [[../Specs/22_RuleCompiler/TASK-086-agents-md-codegen-and-ci-check|TASK-086]]: Генерация корневого AGENTS.md через scripts/gen_rules.py --check, CI-гейт и exclusion workflow в бандле.
- [[../Specs/22_RuleCompiler/TASK-087-rules-drift-consistency-tests|TASK-087]]: Tier 1 тесты дрейфа правил (tests/test_rules_consistency.py): инвентарь, выводимость адаптеров и hard-proof.
- [[../Specs/22_RuleCompiler/TASK-088-editorial-consolidation-e2e-and-living-spec|TASK-088]]: Редакционная консолидация правил, E2E-синхронизация инсталлятора, Living Spec и пересборка dist/install.py.

### 🐛 Исправленные дефекты (Bug Fixes)
- Критических дефектов и регрессий за период фазы не зафиксировано.

### 🏛️ Архитектурные решения (ADR)
- [[../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]: Архитектура Zero Dependencies на стандартной библиотеке Python 3.
- [[../../03_Decisions_ADR/ADR-0021-rules-layering-thin-forwarders-and-obsidian-taxonomy|ADR-0021]]: Архитектура распределения правил (Thin Forwarders), декуплинг графа Obsidian и консолидация онбординга.
- [[../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]: Архитектура самообучающегося контура дефектов (Defect Loop), слои надежности Quality Gates (Tier 1–3) и фильтрация инициатив FB-GH-3.
- [[../../03_Decisions_ADR/ADR-0029-fine-grained-task-symbol-contracts-and-line-drift-rejection|ADR-0029]]: Символьные контракты скоупа задач (Symbolic Scope) и отказ от фиксации номеров строк (Line Drift Prevention).
- [[../../03_Decisions_ADR/ADR-0030-single-source-rule-compiler|ADR-0030]]: Single-Source Rule Compiler: корпус rules/AGENTS_CORE.md и детерминированный рендер правил агента.
- [[../../03_Decisions_ADR/ADR-0031-research-evidence-gate-for-icebox-promotion|ADR-0031]]: Research-Evidence Gate при промоушене из Icebox: критерий зрелости в /kb-plan, поле research_basis в PLAN-XXX и неблокирующий контроль.

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 165.6 KB | `8fac0aa7beeb40ab2a6665263267f0ebf4d64b720661f999922443771b8c2ccb` | `dist/install.py` |

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
- [x] Все задачи фазы 22 завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.22.0.md`.
