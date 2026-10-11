---
id: RELEASE-v0.13.0
title: "Релиз v0.13.0: Фаза 13"
version: "0.13.0"
phase: 13
status: completed
date: 2026-10-11
git_tag: "v0.13.0"
github_release_url: ""
mode: "local-only"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "114.1 KB"
    sha256: "f472fe4dbcf8e12d8a15249d52475d23890b48ea8e1423f8c7b5f405df3fe633"
  - name: "RELEASE_NOTES.md"
    path: "dist/RELEASE_NOTES.md"
    size: "2.9 KB"
    sha256: "d60a7ba1f4bdaec9570b8595423cab212bd80ed760854b6225a57b6314d9bfae"
tags:
  - release
  - changelog
  - v0.13.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.13.0: Фаза 13

> **Версия:** v0.13.0  
> **Фаза:** 13  
> **Дата:** 2026-10-11  
> **Режим публикации:** Local-Only Package  
> **Git Tag:** `v0.13.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
Релиз v0.13.0 (Фаза 13): Слоистая архитектура правил (Thin Forwarders, -80% токенов), декуплинг Obsidian Graph (-150 токенов на шаг), консолидация навигации в kb-onboard (12 специализированных скиллов) и двухуровневая таксономия шаблонов.

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/13_RulesLayering/TASK-048-clean-agents-md-and-obsidian-taxonomy|TASK-048]]: Очистка AGENTS.md от графового шума и изоляция таксономии Obsidian Graph в .obsidian/graph.json.
- [[../Specs/13_RulesLayering/TASK-049-thin-forwarders-adapters-generator|TASK-049]]: Реализация паттерна Thin Forwarders в генераторах адаптеров install.py.
- [[../Specs/13_RulesLayering/TASK-050-consolidate-onboard-and-template-taxonomy|TASK-050]]: Консолидация docs-as-code и kb-onboard, двухуровневая таксономия шаблонов в Onboarding.md.
- [[../Specs/13_RulesLayering/TASK-051-bundling-e2e-tests-and-living-spec|TASK-051]]: Сборка монолитного инсталлятора build_installer.py, сквозные E2E тесты и актуализация Living Spec.

### 🐛 Исправленные дефекты (Bug Fixes)
- Критических дефектов и регрессий за период фазы не зафиксировано.

### 🏛️ Архитектурные решения (ADR)
- [[../../03_Decisions_ADR/ADR-0021-rules-layering-thin-forwarders-and-obsidian-taxonomy|ADR-0021]]: Архитектура распределения правил (Thin Forwarders), декуплинг графа Obsidian и консолидация онбординга.

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 114.1 KB | `f472fe4dbcf8e12d8a15249d52475d23890b48ea8e1423f8c7b5f405df3fe633` | `dist/install.py` |
| `RELEASE_NOTES.md` | 2.9 KB | `d60a7ba1f4bdaec9570b8595423cab212bd80ed760854b6225a57b6314d9bfae` | `dist/RELEASE_NOTES.md` |

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
- [x] Все задачи фазы 13 завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.13.0.md`.
