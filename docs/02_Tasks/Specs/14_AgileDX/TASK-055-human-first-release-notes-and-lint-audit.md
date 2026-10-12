---
id: TASK-055
title: "Human-First чейнджлоги в scripts/kb_release.py и аудит Fast-Track в scripts/kb_lint.py"
status: done
type: task
phase: 14
component:
  - scripts
  - release
  - lint
parent_plan: "[[../../Plans/PLAN-014-agile-docs-as-code-and-chat-first-dx|PLAN-014]]"
created: 2026-10-12
updated: 2026-10-12
tags:
  - task/spec
  - phase14
  - scripts
  - release
  - lint
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-055 — Human-First чейнджлоги в scripts/kb_release.py и аудит Fast-Track в scripts/kb_lint.py

> **ID:** TASK-055 | **Статус:** Выполнено (Режим 3)  
> **План:** [[../../Plans/PLAN-014-agile-docs-as-code-and-chat-first-dx|PLAN-014]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0022-chat-first-vibe-coder-dx-and-human-guardrails|ADR-0022]], [[../../../03_Decisions_ADR/ADR-0023-fast-track-protocol-for-micro-tasks|ADR-0023]]

---

## 1. Цель задачи
Обеспечить дружелюбный и прозрачный вывод релизных заметок для внешних пользователей на GitHub и автоматизировать инструментальный контроль рамок Fast-Track спецификаций в скриптах харнесса на базе стандартной библиотеки Python 3 (Zero-Dependencies).

---

## 2. Затрагиваемые файлы
* `[MODIFY]` `scripts/kb_release.py` — генерация секции «Главное для пользователей» на понятном языке в `generate_public_release_notes`.
* `[MODIFY]` `scripts/kb_lint.py` — добавление функции аудита `check_fast_track_specs` (контроль лимита $\le 2$ файлов и наличия команды верификации).
* `[MODIFY]` `tests/test_kb_release.py` — модульные тесты для Human-First генерации заметок.
* `[MODIFY]` `tests/test_kb_lint.py` — модульные тесты аудита Fast-Track микро-спецификаций.

---

## 3. Детали реализации

### 3.1. Модернизация `scripts/kb_release.py`
* В генераторе внешних заметок релиза `generate_public_release_notes(release_file, dist_dir)`:
  - Сформировать вводный блок `### 🌟 Главное в этом релизе (Highlights)` на основе выжимки целей фазы или плана, ориентированный на человека без избыточного технического шума.
  - Сгруппировать список задач с понятными маркерами (`⚡ Fast-Track:`, `✨ Фича:`, `🐛 Исправление:`) вместо сухого перечисления номеров тикетов.

### 3.2. Аудит Fast-Track в `scripts/kb_lint.py`
* Реализовать функцию `check_fast_track_specs(docs_dir: Path) -> List[str]`:
  - Находит все спецификации с полем `type: fast-track` в `docs/02_Tasks/Specs/`.
  - Проверяет блок `## 2. Контракт файлов`: подсчитывает количество файлов `[NEW]`, `[MODIFY]`, `[DELETE]`. Если файлов $> 2$, формирует предупреждение:
    `WARNING: Fast-Track spec <file> touches N files (limit: <= 2). Consider full RFC.`
  - Проверяет наличие секции `## 3. План верификации` или команды верификации (`Verification Plan`). При отсутствии — формирует ошибку/предупреждение.

---

## 4. План верификации (Verification Plan)
- [ ] Синтаксис: `python -m py_compile scripts/kb_release.py scripts/kb_lint.py` (Exit code 0).
- [ ] Тесты релиз-менеджера: `python -m unittest tests/test_kb_release.py` (100% Pass).
- [ ] Тесты линтера: `python -m unittest tests/test_kb_lint.py` (100% Pass).
- [ ] Полный аудит: `python scripts/kb_lint.py --path docs` (0 broken links).

---

## 5. Критерии готовности (DoD)
- [ ] Функция `generate_public_release_notes` формирует Human-First чейнджлоги.
- [ ] В `scripts/kb_lint.py` работает валидация лимитов Fast-Track задач.
- [ ] Модульные тесты в `tests/test_kb_release.py` и `tests/test_kb_lint.py` успешно проходят.
- [ ] Все пункты Плана верификации пройдены.
