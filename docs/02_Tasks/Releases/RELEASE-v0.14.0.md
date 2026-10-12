---
id: RELEASE-v0.14.0
title: "Релиз v0.14.0: Фаза 14"
version: "0.14.0"
phase: 14
status: completed
date: 2026-10-12
git_tag: "v0.14.0"
github_release_url: ""
mode: "local-only"
artifacts:
  - name: "install.py"
    path: "dist/install.py"
    size: "120.9 KB"
    sha256: "e4f470e7dae9d462bc92911894fa28832948fcedb884e8ce50d956298c0e30d5"
  - name: "RELEASE_NOTES.md"
    path: "dist/RELEASE_NOTES.md"
    size: "3.0 KB"
    sha256: "86573271144aa870c9282bae3809157bb02b216dc5d262890685374ebe43116e"
tags:
  - release
  - changelog
  - v0.14.0
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v0.14.0: Фаза 14

> **Версия:** v0.14.0  
> **Фаза:** 14  
> **Дата:** 2026-10-12  
> **Режим публикации:** Local-Only Package  
> **Git Tag:** `v0.14.0`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
Релиз v0.14.0 (Фаза 14): Продуктовый DX, протокол Fast-Track для микро-задач (Micro-Spec TEMPLATE_TASK_MICRO.md, kb-task --fast), принцип «Направляй, а не блокируй» (Human Guardrails), практическое руководство Zero_To_Hero_Guide.md («Вайбкодинг со страховкой») и Human-First релизные заметки.

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[../Specs/14_AgileDX/TASK-052-micro-spec-template-and-fast-track-skills|TASK-052]]: Шаблон Micro-Spec TEMPLATE_TASK_MICRO.md и поддержка Fast-Track в kb-task / kb-plan.
- [[../Specs/14_AgileDX/TASK-053-human-guardrails-and-agent-rules|TASK-053]]: Принцип «Направляй, а не блокируй» (Human Guardrails) в AGENTS.md и адаптерах.
- [[../Specs/14_AgileDX/TASK-054-zero-to-hero-guide-and-mentor-onboarding|TASK-054]]: Практический гайд Zero_To_Hero_Guide.md («Вайбкодинг со страховкой») и менторский онбординг в kb-onboard.
- [[../Specs/14_AgileDX/TASK-055-human-first-release-notes-and-lint-audit|TASK-055]]: Human-First чейнджлоги в scripts/kb_release.py и аудит Fast-Track в scripts/kb_lint.py.
- [[../Specs/14_AgileDX/TASK-056-installer-bundling-e2e-and-living-spec|TASK-056]]: Синхронизация инсталлятора install.py / build_installer.py, E2E тесты и актуализация Living Spec.

### 🐛 Исправленные дефекты (Bug Fixes)
- Критических дефектов и регрессий за период фазы не зафиксировано.

### 🏛️ Архитектурные решения (ADR)
- [[../../03_Decisions_ADR/ADR-0014-greenfield-idea-first-initialization-and-living-spec-protocol|ADR-0014]]: Архитектура Greenfield-инициализации от идеи (Idea-First) и протокол Living Spec против дрифта документации.
- [[../../03_Decisions_ADR/ADR-0015-zero-to-hero-onboarding-guide-architecture|ADR-0015]]: Архитектура практического руководства Zero-to-Hero Onboarding Guide и интеграция ментальных моделей.
- [[../../03_Decisions_ADR/ADR-0022-chat-first-vibe-coder-dx-and-human-guardrails|ADR-0022]]: Архитектура Chat-First DX и адаптация Docs-as-Code для вайбкодеров без потери инженерных гарантий.
- [[../../03_Decisions_ADR/ADR-0023-fast-track-protocol-for-micro-tasks|ADR-0023]]: Архитектура протокола Fast-Track для микро-задач и легковесные спецификации (Micro-Specs).

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `install.py` | 120.9 KB | `e4f470e7dae9d462bc92911894fa28832948fcedb884e8ce50d956298c0e30d5` | `dist/install.py` |
| `RELEASE_NOTES.md` | 3.0 KB | `86573271144aa870c9282bae3809157bb02b216dc5d262890685374ebe43116e` | `dist/RELEASE_NOTES.md` |

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
- [x] Все задачи фазы 14 завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-v0.14.0.md`.
