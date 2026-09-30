---
id: TASK-001
title: Ядро инсталлятора install.py и упаковка ресурсов
status: in-progress
type: task
phase: 1
component:
  - installer
  - bundling
parent_plan: "[[../../Plans/PLAN-001-crossplatform-installer-architecture|PLAN-001]]"
created: 2026-09-30
updated: 2026-09-30
tags:
  - task/spec
  - component/installer
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-001 — Ядро инсталлятора install.py и упаковка ресурсов

> **ID:** TASK-001  
> **Статус:** В работе  
> **Теги:** #task/spec #component/installer  
> **Родительский план:** [[../../Plans/PLAN-001-crossplatform-installer-architecture|PLAN-001]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи
Реализовать основу автономного скрипта `install.py` и утилиту сборки `scripts/build_installer.py`, которая упаковывает 12 шаблонов, `.obsidian/graph.json` и `scripts/kb_lint.py` в компактное строковое или сжатое представление внутри `install.py`. Скрипт распаковывает полную структуру `docs/` при установке.

---

## 2. Затрагиваемые файлы и компоненты
* `[NEW]` `scripts/build_installer.py` — утилита компиляции ассетов из `templates/` и `scripts/kb_lint.py` в тело `install.py`.
* `[NEW]` `install.py` — автономный установщик, генерирующий полную структуру `docs/`.
* `[MODIFY]` `docs/02_Tasks/Kanban.md` — обновление статуса задачи.

---

## 3. Детали технической реализации
1. `scripts/build_installer.py`:
   - Считывает файлы из `templates/*.md`, `templates/graph.json` и `scripts/kb_lint.py`.
   - Сериализует их в словарь в Python-синтаксисе (raw strings или base64/zlib для надежной транспортировки без конфликтов спецсимволов).
   - Внедряет в шаблон `install.py`.
2. `install.py`:
   - Проверяет директорию назначения (по умолчанию текущая).
   - Создает каталоги `docs/`, `docs/00_Templates/`, `docs/.obsidian/`, `docs/01_Architecture/`, `docs/02_Tasks/` (`Plans/`, `Specs/01_MVP/`, `Bugs/`), `docs/03_Decisions_ADR/`, `docs/04_Research/`, `docs/05_Testing/`, `scripts/`.
   - Записывает распакованные шаблоны и скрипты.
   - Поддерживает безопасное сохранение существующей директории (проверка `docs/` на перезапись).

---

## 4. План верификации (Verification Plan)
- [ ] Запуск сборщика `python scripts/build_installer.py` (завершается без ошибок, генерирует валидный синтаксис `install.py`).
- [ ] Проверка запуска `python install.py --help`.
- [ ] Тестовая распаковка в пустую временную папку `test_sandbox`.
- [ ] Прогон `python scripts/kb_lint.py --path test_sandbox/docs` — 0 битых ссылок.

---

## 5. Критерии готовности (Definition of Done)
- [ ] Код сборщика и инсталлятора написан без внешних библиотек (Zero Dependencies).
- [ ] Запуск `install.py` генерирует полную структуру базы знаний.
- [ ] Все пункты плана верификации пройдены.
