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
> **Дорожная карта:** [[../Roadmap|Дорожная карта]] | **GitHub Notes:** `dist/RELEASE_NOTES.md`  

---

## 📋 Главное в этом релизе (Highlights & Core Value)
<!-- Краткое резюме одной фразой простыми словами: какую главную пользу выпуск дает пользователю -->

---

## ✨ Новые возможности и их ценность (Features & Value)

### 🌟 [Понятное название новой возможности]
* **Что появилось:** <!-- Краткое описание возможности без внутреннего жаргона -->
* **Зачем это нужно:** <!-- Какую проблему решает и как облегчает жизнь пользователю -->
* **Как попробовать:**
```bash
# Пример команды или сценария использования
```

---

## 🐛 Исправления и улучшения (User-Friendly Fixes)
<!-- Формулируйте исправления простым языком по правилу: симптом (что было не так) -> результат (как теперь работает) -->
* **[Понятное название компонента / сценария]:** <!-- Было: описание проблемы понятными словами. Стало: как теперь работает корректно. Без стек-трейсов и внутренних имен переменных. -->

---

## ⚡ Быстрый старт и обновление (Quick Start & Upgrade)

```bash
# Установка или обновление до актуальной версии
curl -fsSL https://raw.githubusercontent.com/<owner>/<repo>/main/install.py | python3
```

---

<details>
<summary>🔍 <b>Инженерный аудит, трассируемость и артефакты (Technical Details & Audit)</b></summary>

### 📋 Матрица трассируемости задач (Traceability Matrix)

| Идентификатор | Тип | Название и ссылка | Статус |
| :--- | :--- | :--- | :--- |
| `TASK-XXX` | Фича | [[../Specs/0N_Phase/TASK-XXX-slug|TASK-XXX: Название]] | Выполнено |
| `BUG-XXX` | Багфикс | [[../Bugs/BUG-XXX-slug|BUG-XXX: Название]] | Исправлено |
| `ADR-XXXX` | Архитектура | [[../../03_Decisions_ADR/ADR-XXXX-slug|ADR-XXXX: Название]] | Принято |
| `DEBT-XXX` | Техдолг | [[../TechDebt|DEBT-XXX: Название]] | Погашен |

### 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | SHA-256 | Путь |
| :--- | :--- | :--- | :--- |
| `[artifact.ext]` | [Размер] | `[SHA-256]` | `dist/[artifact.ext]` |

### 🔍 Проверка контрольной суммы
```bash
# PowerShell: Get-FileHash -Algorithm SHA256 dist/[artifact.ext]
# Linux/macOS: sha256sum dist/[artifact.ext]
```

### 📋 Чеклист верификации и приемки релиза (DoD)
- [x] Все задачи фазы завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v[X.Y.Z].md`.

</details>
