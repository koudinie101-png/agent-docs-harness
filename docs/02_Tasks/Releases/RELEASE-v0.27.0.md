---
id: RELEASE-v0.27.0
title: "Релиз v0.27.0: Фаза 27"
version: "0.27.0"
phase: 27
status: completed
date: 2026-10-25
git_tag: "v0.27.0"
github_release_url: "https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.27.0"
mode: "github"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "175.0 KB"
    sha256: "a4961bfe2599a6c0f898816e761ef28adbc4479de0ac9edf033ae405b1655a87"
tags:
  - release
  - changelog
  - v0.27.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.27.0: Фаза 27

> **Версия:** v0.27.0  
> **Фаза:** 27  
> **Дата:** 2026-10-25  
> **Режим публикации:** GitHub Release  
> **Git Tag:** `v0.27.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
Продуктизация линтера: машинно-читаемая диагностика (--format text/json/sarif, реестр стабильных KB-XXX, --version) при неизменном text-выводе и exit-кодах; 13 контрактных тестов вывода; доставка через пересобранный бандл (179 171 B) с E2E установленной копии и синхронизацией Living Spec (SPEC.md, README.md, Onboarding.md).

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/27_DocsIntegrity/TASK-101-finding-model-rule-registry-and-formats|TASK-101]]: Модель Finding, реестр KB-XXX и машинно-читаемые форматы линтера.
- [[../Specs/27_DocsIntegrity/TASK-102-output-contract-tests|TASK-102]]: Контрактные тесты машинно-читаемого вывода линтера (json/sarif).
- [[../Specs/27_DocsIntegrity/TASK-103-bundle-e2e-and-living-spec|TASK-103]]: Доставка машинно-читаемого линтера: пересборка бандла, бюджет, E2E и Living Spec.

### 🐛 Исправленные дефекты (Bug Fixes)
- Критических дефектов и регрессий за период фазы не зафиксировано.

### 🏛️ Архитектурные решения (ADR)
- [[../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]: Архитектура Zero Dependencies на стандартной библиотеке Python 3.
- [[../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]]: Архитектура оптимизации токенов и контекстной эффективности (High-SNR Token Architecture).
- [[../../03_Decisions_ADR/ADR-0014-greenfield-idea-first-initialization-and-living-spec-protocol|ADR-0014]]: Архитектура Greenfield-инициализации от идеи (Idea-First) и протокол Living Spec против дрифта документации.
- [[../../03_Decisions_ADR/ADR-0030-single-source-rule-compiler|ADR-0030]]: Single-Source Rule Compiler: корпус rules/AGENTS_CORE.md и детерминированный рендер правил агента.
- [[../../03_Decisions_ADR/ADR-0032-machine-readable-lint-contract-and-rule-registry|ADR-0032]]: Машинно-читаемый контракт линтера: модель Finding, реестр KB-XXX и три рендерера.

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 175.0 KB | `a4961bfe2599a6c0f898816e761ef28adbc4479de0ac9edf033ae405b1655a87` | `dist/install.py` |

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
- [x] Все задачи фазы 27 завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.27.0.md`.
