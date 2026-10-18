---
id: RELEASE-v0.24.0
title: "Релиз v0.24.0: Фаза 24"
version: "0.24.0"
phase: 24
status: completed
date: 2026-10-18
git_tag: "v0.24.0"
github_release_url: "https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.24.0"
mode: "github"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "169.8 KB"
    sha256: "27166e7df194476fdafa4993eebf61a85d4c296acf3df04dc1faa69ef44eb4e1"
tags:
  - release
  - changelog
  - v0.24.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.24.0: Фаза 24

> **Версия:** v0.24.0  
> **Фаза:** 24  
> **Дата:** 2026-10-18  
> **Режим публикации:** GitHub Release  
> **Git Tag:** `v0.24.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
Фаза 24 восстанавливает критерий технической зрелости в /kb-plan (Evidence Status), добавляет неблокирующий Evidence Nudge (A/B/C), фиксирует доказательную базу плана полями research_basis/basis_note и секцией Research Basis, вводит advisory-WARN в kb_lint.py и Tier 1 parity-тест копий шаблонов.

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/24_ResearchEvidence/TASK-090-evidence-status-nudge-and-tier2-rule|TASK-090]]: Evidence Status и Evidence Nudge в /kb-plan, Tier 2 правило в корпусе и Tier 1 защита формулировки.
- [[../Specs/24_ResearchEvidence/TASK-091-plan-research-basis-template-and-advisory-lint|TASK-091]]: research_basis/basis_note и секция Research Basis в TEMPLATE_PLAN.md, неблокирующий check_research_basis() в kb_lint.
- [[../Specs/24_ResearchEvidence/TASK-092-template-copies-parity-sync-and-test|TASK-092]]: Синхронизация templates/ ↔ docs/00_Templates/ и Tier 1 parity-тест копий шаблонов.
- [[../Specs/24_ResearchEvidence/TASK-093-bundle-rebuild-e2e-and-living-spec-sync|TASK-093]]: Пересборка install.py/dist/install.py, E2E установленного Evidence Gate и Living Spec Sync.

### 🐛 Исправленные дефекты (Bug Fixes)
- Критических дефектов и регрессий за период фазы не зафиксировано.

### 🏛️ Архитектурные решения (ADR)
- [[../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]: Архитектура Zero Dependencies на стандартной библиотеке Python 3.
- [[../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]]: Архитектура оптимизации токенов и контекстной эффективности (High-SNR Token Architecture).
- [[../../03_Decisions_ADR/ADR-0011-intent-routing-and-icebox-prioritization-in-kb-plan|ADR-0011]]: Маршрутизация намерений и приоритизация бэклога идей по ценности продукта в /kb-plan.
- [[../../03_Decisions_ADR/ADR-0022-chat-first-vibe-coder-dx-and-human-guardrails|ADR-0022]]: Архитектура Chat-First DX и адаптация Docs-as-Code для вайбкодеров без потери инженерных гарантий.
- [[../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]: Архитектура самообучающегося контура дефектов (Defect Loop), слои надежности Quality Gates (Tier 1–3) и фильтрация инициатив FB-GH-3.
- [[../../03_Decisions_ADR/ADR-0029-fine-grained-task-symbol-contracts-and-line-drift-rejection|ADR-0029]]: Символьные контракты скоупа задач (Symbolic Scope) и отказ от фиксации номеров строк (Line Drift Prevention).
- [[../../03_Decisions_ADR/ADR-0030-single-source-rule-compiler|ADR-0030]]: Single-Source Rule Compiler: корпус rules/AGENTS_CORE.md и детерминированный рендер правил агента.
- [[../../03_Decisions_ADR/ADR-0031-research-evidence-gate-for-icebox-promotion|ADR-0031]]: Research-Evidence Gate при промоушене из Icebox: критерий зрелости в /kb-plan, поле research_basis в PLAN-XXX и неблокирующий контроль.

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 169.8 KB | `27166e7df194476fdafa4993eebf61a85d4c296acf3df04dc1faa69ef44eb4e1` | `dist/install.py` |

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
- [x] Все задачи фазы 24 завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.24.0.md`.
