---
id: RELEASE-v[X.Y.Z]
title: "Релиз v[X.Y.Z]: [Название релиза]"
version: "[X.Y.Z]"
phase: 1
status: completed # completed | draft
date: YYYY-MM-DD
git_tag: "v[X.Y.Z]"
github_release_url: ""
mode: "github" # github | local-only
artifacts:
  - name: "[artifact.ext]"
    path: "dist/[artifact.ext]"
    size: "[Размер]"
    sha256: "[SHA-256]"
tags:
  - release
  - changelog
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v[X.Y.Z]: [Название]

> **Версия:** v[X.Y.Z] | **Фаза:** [N] | **Дата:** YYYY-MM-DD | **Tag:** `v[X.Y.Z]`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза
<!-- Краткое резюме ключевой ценности выпуска -->

## 🚀 Что нового (Changelog)
* **Фичи:** [[Specs/0N_Phase/TASK-XXX-slug|TASK-XXX]]: <!-- Описание -->
* **Багфиксы:** [[Bugs/BUG-XXX-slug|BUG-XXX]]: <!-- Описание -->
* **ADR:** [[../../03_Decisions_ADR/ADR-XXXX-slug|ADR-XXXX]]: <!-- Описание -->

## 📦 Артефакты (SHA-256)

| Файл | Размер | SHA-256 | Путь |
| :--- | :--- | :--- | :--- |
| `[artifact.ext]` | [Размер] | `[SHA-256]` | `dist/[artifact.ext]` |

## 🔍 Проверка контрольной суммы
```bash
# PowerShell: Get-FileHash -Algorithm SHA256 dist/[artifact.ext]
# Linux/macOS: sha256sum dist/[artifact.ext]
```
