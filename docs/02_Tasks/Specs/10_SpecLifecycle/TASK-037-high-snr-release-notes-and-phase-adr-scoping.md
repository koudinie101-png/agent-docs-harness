---
id: TASK-037
title: "High-SNR Release Notes Generator & Phase ADR Scoping (scripts/kb_release.py, kb-release, тесты)"
status: done
type: task
phase: 10
component:
  - release
  - tooling
  - high-snr
parent_plan: "[[../../Plans/PLAN-010-spec-genesis-and-high-snr-release-notes|PLAN-010]]"
created: 2026-10-03
updated: 2026-10-03
tags:
  - task/spec
  - phase10
  - release-notes
  - high-snr
  - distribution
  - clean-changelog
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-037 — High-SNR Release Notes Generator & Phase ADR Scoping

> **ID:** TASK-037  
> **Статус:** Выполнено (Режим 3)  
> **Теги:** #task/spec #phase10 #release-notes #high-snr #distribution #clean-changelog  
> **Родительский план:** [[../../Plans/PLAN-010-spec-genesis-and-high-snr-release-notes|PLAN-010]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-013-release-notes-adr-exclusion-and-high-snr|RESEARCH-013]], [[../../../03_Decisions_ADR/ADR-0017-release-notes-adr-exclusion-and-high-snr-standard|ADR-0017]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Реализовать выходной шлюз методологии Docs-as-Code — **Стандарт высокой плотности полезного сигнала в релизных заметках (High-SNR Release Notes)** согласно [[../../../03_Decisions_ADR/ADR-0017-release-notes-adr-exclusion-and-high-snr-standard|ADR-0017]] и [[../../../04_Research/RESEARCH-013-release-notes-adr-exclusion-and-high-snr|RESEARCH-013]]:
1. **Исключение секции ADR из публичного чейнджлога:** в функции `generate_public_release_notes()` утилиты `scripts/kb_release.py` полностью упразднить секцию `### 🏛️ Архитектурные решения (ADR)`, исключая кумулятивное раздувание публичных заметок на GitHub.
2. **Фазовый скоупинг во внутреннем чейнджлоге:** во внутреннем документе `docs/02_Tasks/Releases/RELEASE-vX.Y.Z.md` собирать только ADR текущей фазы (`phase: N`), устраняя $O(N)$ разрастание списков в архиве.
3. **Актуализация скилла и шаблонов:** синхронизировать `.agents/skills/kb-release/SKILL.md`, `TEMPLATE_RELEASE.md` и покрыть изменения модульными тестами в `tests/test_kb_release.py`.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `scripts/kb_release.py` — модификация `generate_public_release_notes()` (удаление секции ADR) и `generate_release_note()` (фазовая фильтрация ADR).
* `[MODIFY]` `.agents/skills/kb-release/SKILL.md` — обновление High-SNR описания формата публичных заметок.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_RELEASE.md` и `templates/TEMPLATE_RELEASE.md` — уточнение фазового скоупинга ADR.
* `[MODIFY]` `tests/test_kb_release.py` — новые модульные тесты проверки отсутствия секции ADR в публичном чейнджлоге и фильтрации по текущей фазе.

---

## 3. Детали реализации

### 3.1. Модификация `scripts/kb_release.py`
1. В функции `generate_public_release_notes(raw_content: str, repo_slug: str, tag: str) -> str`:
   - Упразднить парсинг и включение секции ADR (`### 🏛️ Архитектурные решения (ADR)`).
   - Публичный экспорт `dist/RELEASE_NOTES.md` содержит строго:
     - Заголовок релиза
     - `### 🚀 Ключевые изменения (Highlights)`
     - `### 📦 Реализованные задачи (Deliverables)`
     - `### ⚡ Быстрый старт (Installation)`
     - `### 🛡️ Контрольные суммы и целостность (Integrity & SHA-256)`
2. В функции `generate_release_note(...)`:
   - При сборе ADR из `docs/03_Decisions_ADR/` анализировать номер фазы (`phase: N` в frontmatter ADR или связях задач текущей фазы) и включать только релевантные текущему релизу решения.

### 3.2. Обновление скилла `.agents/skills/kb-release/SKILL.md`
В шаге `Export Release Notes`:
- Зафиксировать High-SNR стандарт (без ADR).
- Указать, что при необходимости ссылка на ключевой ADR дается инлайн в строке задачи `TASK-XXX`.

### 3.3. Тестирование в `tests/test_kb_release.py`
Добавить тесты:
- `test_generate_public_release_notes_excludes_adrs`: проверяет, что в сгенерированном Markdown отсутствует заголовок `Архитектурные решения` и ссылки на ADR, а размер заметок оптимизирован.
- `test_generate_release_note_filters_adrs_by_phase`: проверяет, что во внутренний документ релиза попадают только ADR текущей фазы.

---

## 4. План верификации (Verification Plan)

- [x] Модульные тесты: `python -m unittest tests/test_kb_release.py` (100% Pass, Exit code 0).
- [x] Все тесты проекта: `python -m unittest discover -s tests` (100% Pass, Exit code 0).
- [x] Линтер базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links, 0 warnings, Exit code 0).

---

## 5. Критерии готовности (DoD)

- [x] В `dist/RELEASE_NOTES.md` отсутствует секция ADR.
- [x] Внутренний архив релиза фильтрует ADR по фазе.
- [x] Тесты в `tests/test_kb_release.py` успешно проходят.
- [x] Статус обновлен в ТЗ, Канбане и Дорожной карте.
