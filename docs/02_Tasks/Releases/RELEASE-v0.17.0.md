---
id: RELEASE-v0.17.0
title: "Релиз v0.17.0: Фаза 17"
version: "0.17.0"
phase: 17
status: completed
date: 2026-10-15
git_tag: "v0.17.0"
github_release_url: "https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.17.0"
mode: "github"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "135.6 KB"
    sha256: "5163a7629b939f18de76b7ec2a44cc3cc23f6e7db045c9e521ca17b8f5b7fe5c"
tags:
  - release
  - changelog
  - v0.17.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.17.0: Фаза 17

> **Версия:** v0.17.0  
> **Фаза:** 17  
> **Дата:** 2026-10-15  
> **Режим публикации:** GitHub Release  
> **Git Tag:** `v0.17.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
Официальный релиз v0.17.0 по завершении Фазы 17.

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/17_HardeningAndSync/TASK-066-kb-lint-codeblocks-and-schemas|TASK-066]]: Харденинг парсинга викиссылок и валидация схем frontmatter в scripts/kb_lint.py.
- [[../Specs/17_HardeningAndSync/TASK-067-kb-ingest-yaml-escaping-and-imap-uid|TASK-067]]: Безопасное экранирование YAML, постоянные IMAP UIDs и URL-кодирование в scripts/kb_ingest.py.
- [[../Specs/17_HardeningAndSync/TASK-068-installer-tty-anonymizer-and-build-hook|TASK-068]]: Защита анонимизатора, контейнерный TTY-зонд и интеграция сборщика в install.py и build_release.py.
- [[../Specs/17_HardeningAndSync/TASK-069-ssot-agents-and-docs-sync|TASK-069]]: Синхронизация SSOT: правила агентов, режимы жизненного цикла и таксономия 16 шаблонов.
- [[../Specs/17_HardeningAndSync/TASK-070-skills-templates-and-memory-sync|TASK-070]]: Синхронизация скиллов, шаблонов и контура памяти в AGENTS.md.

### 🐛 Исправленные дефекты (Bug Fixes)
- [[../Bugs/BUG-005-kb-lint-py38-is-relative-to|BUG-005]]: AttributeError при вызове Path.is_relative_to в scripts/kb_lint.py на Python 3.8.
- [[../Bugs/BUG-006-release-notes-self-artifact|BUG-006]]: dist/RELEASE_NOTES.md попадает в таблицу артефактов SHA-256 при повторном запуске scripts/kb_release.py.
- [[../Bugs/BUG-007-kb-ingest-paste-inline-arg|BUG-007]]: Падение с ошибкой unrecognized arguments при передаче инлайн-текста в scripts/kb_ingest.py --paste \"<text>\.
- [[../Bugs/BUG-008-local-fallback-patterns-and-phase-pad|BUG-008]]: Отсутствие docs/06_Memory/patterns.md в локальном fallback install.py и некорректная маска фаз >= 10 в scripts/kb_release.py.
- [[../Bugs/BUG-009-issue-templates-hardcoded-repo-leak|BUG-009]]: Утечка метаданных agent-docs-harness в .github/ISSUE_TEMPLATE/.

### 🏛️ Архитектурные решения (ADR)
- Архитектурных изменений в рамках фазы не вводилось.

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 135.6 KB | `5163a7629b939f18de76b7ec2a44cc3cc23f6e7db045c9e521ca17b8f5b7fe5c` | `dist/install.py` |

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
- [x] Все задачи фазы 17 завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.17.0.md`.
