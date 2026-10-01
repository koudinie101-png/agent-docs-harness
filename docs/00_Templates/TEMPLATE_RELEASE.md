---
id: RELEASE-v[X.Y.Z]
title: "Релиз v[X.Y.Z]: [Название релиза / Фазы]"
version: "[X.Y.Z]"
phase: [N]
status: completed # completed | draft
date: YYYY-MM-DD
git_tag: "v[X.Y.Z]"
github_release_url: "" # Заполняется при публикации на GitHub (например, https://github.com/org/repo/releases/tag/vX.Y.Z)
mode: "github" # github | local-only
artifacts:
  - name: "[artifact.ext]"
    path: "dist/[artifact.ext]"
    size: "[Размер]"
    sha256: "[SHA-256]"
tags:
  - release
  - changelog
  - v[X.Y.Z]
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v[X.Y.Z]: [Название релиза / Фазы]

> **Версия:** v[X.Y.Z]  
> **Фаза:** [N]  
> **Дата:** YYYY-MM-DD  
> **Режим публикации:** [GitHub Release | Local-Only Package]  
> **Git Tag:** `v[X.Y.Z]`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
[Краткое резюме ключевой ценности и изменений, вошедших в данный выпуск]

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[Specs/0N_Phase/TASK-XXX-slug|TASK-XXX]]: Краткое описание реализованной функциональности.

### 🐛 Исправленные дефекты (Bug Fixes)
- [[Bugs/BUG-XXX-slug|BUG-XXX]]: Описание устраненной проблемы и RCA.

### 🏛️ Архитектурные решения (ADR)
- [[../../03_Decisions_ADR/ADR-XXXX-slug|ADR-XXXX]]: Архитектурное новшество или стандарт.

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `[artifact.ext]` | [Размер] | `[SHA-256]` | `dist/[artifact.ext]` |

---

## 🔍 Инструкция по проверке целостности артефактов

```bash
# Проверка в PowerShell (Windows)
Get-FileHash -Path dist/[artifact.ext] -Algorithm SHA256

# Проверка в Bash / macOS / Linux
sha256sum dist/[artifact.ext]
# или
shasum -a 256 dist/[artifact.ext]
```

---

## 📋 Чеклист верификации и приемки релиза
- [ ] Все задачи фазы завершены и проверены в `Roadmap.md`.
- [ ] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [ ] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [ ] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [ ] Git-тег создан и запушен в удаленный репозиторий (при наличии).
