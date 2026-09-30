---
id: TASK-002
title: Мульти-стековые шаблоны и адаптеры агентов
status: planned
type: task
phase: 1
component:
  - templates
  - agents
  - presets
parent_plan: "[[../../Plans/PLAN-001-crossplatform-installer-architecture|PLAN-001]]"
created: 2026-09-30
updated: 2026-09-30
tags:
  - task/spec
  - component/templates
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-002 — Мульти-стековые шаблоны и адаптеры агентов

> **ID:** TASK-002  
> **Статус:** Запланировано  
> **Теги:** #task/spec #component/templates  
> **Родительский план:** [[../../Plans/PLAN-001-crossplatform-installer-architecture|PLAN-001]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи
Реализовать механизм кастомизации сгенерированных шаблонов и файлов базы знаний под стек проекта (Swift/iOS/macOS, Web/TypeScript, Python, .NET, Generic) и сгенерировать правила для различных AI-агентов (`AGENTS.md`, `.clinerules`, `CLAUDE.md`, `.cursorrules`, `.github/copilot-instructions.md`).

---

## 2. Затрагиваемые файлы и компоненты
* `[MODIFY]` `install.py` — интеграция пресетов стеков и генераторов правил агентов.
* `[NEW]` или `[MODIFY]` `templates/` — плейсхолдеры для параметризации сборки и тестов.

---

## 3. Детали технической реализации
1. **Пресеты технологических стеков:**
   - **Swift (iOS/macOS/SwiftUI/Xcode):**
     - Команды сборки: `swift build` / `xcodebuild -scheme <App> build`
     - Команда тестов: `swift test` / `xcodebuild test`
     - Специфика Research & Bugs: ARC/Retain Cycles, Swift Concurrency/MainActor, BackgroundTasks, Keychain, OS limitations.
   - **Web / TypeScript:**
     - Команды сборки: `npm run build` / `pnpm build`
     - Команда тестов: `npm test` / `pnpm test`
   - **Python:**
     - Команды тестов: `pytest` / `python -m unittest`
   - **.NET / C#:**
     - Команды: `dotnet build`, `dotnet test`
   - **Generic:**
     - Настраиваемые плейсхолдеры.
2. **Адаптеры правил для агентов:**
   - `AGENTS.md` (универсальный корневой файл инструкций).
   - `.clinerules` (для Cline и Roo Code).
   - `CLAUDE.md` (для Claude Code).
   - `.cursorrules` (для Cursor).
   - `.github/copilot-instructions.md` (для GitHub Copilot).

---

## 4. План верификации (Verification Plan)
- [ ] Генерация проекта со стеком `swift`: в `Onboarding.md` и `AGENTS.md` подставлены команды `swift test` и специфичные рекомендации.
- [ ] Проверка создания всех зеркальных файлов агентов при опции `--agent all`.
- [ ] Валидация базы знаний сгенерированного проекта через `kb_lint.py`.

---

## 5. Критерии готовности (Definition of Done)
- [ ] Все 5 стеков поддерживаются.
- [ ] Все адаптеры агентов генерируют корректные правила с 3 режимами и запретом на самовольный код.
