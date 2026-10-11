---
id: TASK-051
title: "Сборка монолитного инсталлятора build_installer.py, сквозные E2E тесты и актуализация Living Spec"
status: done
type: task
phase: 13
component:
  - installer
  - packaging
  - tests
  - spec
parent_plan: "[[../../Plans/PLAN-013-rules-layering-thin-forwarders-and-obsidian-taxonomy|PLAN-013]]"
created: 2026-10-11
updated: 2026-10-11
tags:
  - task/spec
  - phase13
  - installer
  - bundler
  - e2e
  - living-spec
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-051 — Сборка монолитного инсталлятора build_installer.py, сквозные E2E тесты и актуализация Living Spec

> **ID:** TASK-051 | **Статус:** Выполнено (Режим 3)  
> **План:** [[../../Plans/PLAN-013-rules-layering-thin-forwarders-and-obsidian-taxonomy|PLAN-013]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Обоснование:** [[../../../04_Research/RESEARCH-016-agent-rules-hierarchy-and-knowledge-base-structure|RESEARCH-016]] | **Решение:** [[../../../03_Decisions_ADR/ADR-0021-rules-layering-thin-forwarders-and-obsidian-taxonomy|ADR-0021]]

---

## 1. Цель задачи

Завершить реализацию Фазы 13, выполнив синхронизацию и упаковку всех оптимизаций (устранение графового шума, тонкие форвардеры адаптеров, консолидация 12 скиллов):
1. **Пересборка монолитного инсталлятора:** Запустить `scripts/build_installer.py` для генерации самодостаточного автономного файла `dist/install.py` с актуализированным embedded bundle (12 скиллов, тонкие адаптеры, директива таксономии).
2. **Сквозное E2E тестирование:** Разработать и прогнать регрессионный сьют тестов в `tests/test_installer.py`, проверяющий поведение автономного скрипта при чистой установке (`fresh install`), бережном обновлении (`--update`) и диагностическом отчете (`--report`).
3. **Living Spec & Storefront Invariant:** Актуализировать Master Specification (`SPEC.md`) и `README.md`, зафиксировав переход адаптеров IDE на паттерн Thin Forwarders, 12 скиллов и замеры экономии контекстных токенов.

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `scripts/build_installer.py` — проверка и адаптация генератора бандла под 12 скиллов и новые адаптеры.
* `[MODIFY]` `dist/install.py` — пересобранный самодостаточный дистрибутив инсталлятора.
* `[MODIFY]` `SPEC.md` — актуализация архитектуры правил (слои L0–L3, Thin Forwarders, 12 скиллов, экономия контекста).
* `[MODIFY]` `README.md` — обновление витрины проекта: перечень адаптеров, 12 скиллов, замеры токеномики.
* `[MODIFY]` `tests/test_installer.py` — добавление комплексного E2E теста сборщика и дистрибутива Фазы 13.

---

## 3. Детали реализации

### 3.1. Синхронизация и сборка монолита
- Запуск `python scripts/build_installer.py`.
- Проверка размера монолита и валидности embedded bundle (`_ASSETS` словарь содержит 12 скиллов, 14 шаблонов, скрипты и конфигурацию `.obsidian/graph.json`).

### 3.2. Регрессионный E2E тест
- Добавить метод `test_25_phase13_thin_forwarders_and_rules_layering` в `tests/test_installer.py`:
  - Проверка чистой установки стеков через автономный инсталлятор.
  - Проверка размера сгенерированных файлов адаптеров ($\le 35$ строк).
  - Проверка отсутствия дублирования 15 дисциплин в адаптерах.
  - Проверка корректного обновления через `--update` (создание бэкапов `.bak` при кастомизации).

### 3.3. Актуализация Living Spec (`SPEC.md` и `README.md`)
- Внести данные о паттерне Thin Forwarders и снижении размера системных промптов на 80–85%.
- Обновить перечень доступных скиллов (12 скиллов, `kb-onboard` как единая точка входа).

---

## 4. План верификации (Verification Plan)

- [x] Сборка дистрибутива: `python scripts/build_installer.py` (Exit code 0).
- [x] Синтаксическая проверка: `python -m py_compile dist/install.py` (Exit code 0).
- [x] Проверка базы знаний: `python scripts/kb_lint.py --path docs -v` (0 broken links, Exit code 0).
- [x] Тесты инсталлятора: `python -m unittest tests/test_installer.py` (100% Pass, Exit code 0).
- [x] Полный тестовый сьют: `python -m unittest discover -s tests` (100% Pass, Exit code 0).

---

## 5. Критерии готовности (DoD)

- [x] Монолит `dist/install.py` успешно собран и верифицирован.
- [x] Все E2E и регрессионные тесты завершились с кодом 0.
- [x] `SPEC.md` и `README.md` полностью синхронизированы с кодовой базой.
- [x] Все задачи Фазы 13 отмечены выполненными в Канбане и Дорожной карте.
- [x] Результаты зафиксированы в `Devlog.md`.
