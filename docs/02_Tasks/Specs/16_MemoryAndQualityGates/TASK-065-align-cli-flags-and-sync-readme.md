---
id: TASK-065
title: "Выравнивание CLI-флагов и синхронизация README.md"
status: done
type: fast-track
phase: 16
component:
  - installer
  - docs
parent_plan: "[[../../Plans/PLAN-016-self-improving-harness-and-defect-memory|PLAN-016]]"
created: 2026-10-12
updated: 2026-10-12
tags:
  - task/spec
  - fast-track
  - phase16
  - installer
  - docs
kanban: "[[../../Kanban|Канбан-доска]]"
---

# ⚡ Спецификация (Fast-Track): TASK-065 — Выравнивание CLI-флагов и синхронизация README.md

> **Тип:** Fast-Track (≤ 30 LOC) | **Статус:** Выполнено (Режим 3)  
> **Канбан:** [[../../Kanban|Канбан-доска]]

---

## 1. Цель и контекст
Устранить выявленные расхождения документации в `README.md` и добавить недостающие CLI-флаги в `install.py`:
1. Добавить короткие флаги `-i` (для `--idea`) и `-r` (для `--report`) в `install.py`.
2. Исправить команду-пример вызова `--paste` в `README.md` на `--paste --text "..."`.
3. Заменить абсолютный локальный Windows-путь к `RESEARCH-001` на относительную ссылку.
4. Синхронизировать дерево каталогов `docs/`: отразить 16 шаблонов (включая `TEMPLATE_INCIDENT.md`) и `docs/06_Memory/`.
5. Актуализировать терминологию: переход к 4-этапному циклу (Modes 0–3), замена роутера `docs-as-code` на `kb-onboard`, отражение Quality Gates Tier 1–3 и процедурной памяти.

## 2. Контракт файлов
* `[MODIFY]` `install.py` — объявить короткие флаги `-i` для `--idea` и `-r` для `--report` в `parser.add_argument`.
* `[MODIFY]` `README.md` — устранить расхождения, исправить ссылки, команды, дерево каталогов и реестр шаблонов.

## 3. План верификации (Verification Plan)
- [x] Проверка CLI-флагов: `python install.py -r` и `python install.py -i "TestIdea" -y -n FastApp -d temp_fast` отрабатывают без ошибок.
- [x] Сборка дистрибутива: `python scripts/build_installer.py` успешно компилирует `install.py` и `dist/install.py`.
- [x] Тесты инсталлятора: `python -m unittest tests/test_installer.py` завершается успешно.
- [x] Аудит базы знаний: `python scripts/kb_lint.py --path docs` завершается с успехом (0 broken links, 0 fast-track warnings).
- [x] Проверка отсутствия утечек путей: в `README.md` отсутствуют ссылки `file:///`.

## 4. Критерии готовности (DoD)
- [x] Изменения внесены строго в рамках скоупа Fast-Track (≤ 30 строк кода, ≤ 2 файлов).
- [x] Все пункты Плана верификации пройдены без ошибок (Exit code 0).
- [x] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Devlog.
