---
id: TASK-028
title: "Сборка инсталлятора, регрессионные E2E тесты и аудит целостности дистрибутива"
status: done
type: task
phase: 7
component:
  - installer
  - bundling
  - testing
  - verification
parent_plan: "[[../../Plans/PLAN-007-github-release-notes-and-distribution-standard|PLAN-007]]"
created: 2026-10-01
updated: 2026-10-01
tags:
  - task/spec
  - phase7
  - component/installer
  - component/testing
  - release
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-028 — Сборка инсталлятора и сквозная E2E верификация

> **ID:** TASK-028  
> **Статус:** Выполнено (Режим 3)  
> **Теги:** #task/spec #phase7 #component/installer #component/testing #release  
> **Родительский план:** [[../../Plans/PLAN-007-github-release-notes-and-distribution-standard|PLAN-007]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-005-github-release-notes-and-distribution-best-practices|RESEARCH-005]], [[../../../03_Decisions_ADR/ADR-0010-github-release-notes-and-public-distribution-standard|ADR-0010]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Завершить цикл поставки Фазы 7:
1. **Сборка дистрибутива:** Пересобрать самодостаточный инсталлятор `install.py` через `scripts/build_installer.py`, упаковав обновленные `scripts/kb_release.py`, `.github/workflows/release.yml`, скилл `kb-release` и шаблоны.
2. **Сквозное E2E тестирование:** Дополнить `tests/test_installer.py` тестами развертывания релизного воркфлоу (проверка наличия `body_path: dist/RELEASE_NOTES.md` в генерируемом `.github/workflows/release.yml` и обновляемости через `install.py --update`).
3. **Регрессионная верификация:** Обеспечить 100% успешное прохождение всех тестов проекта и аудит базы знаний.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `install.py` — обновление бандла через сборщик `scripts/build_installer.py`.
* `[MODIFY]` `tests/test_installer.py` — проверка развертывания и обновления релизного пайплайна.

---

## 3. Детали реализации

### Проверка в `tests/test_installer.py`:
- Проверить, что при развертывании в чистый каталог файл `.github/workflows/release.yml` содержит строку `body_path: dist/RELEASE_NOTES.md`.
- Проверить, что при вызове `install.py --update` в существующий проект скрипт `scripts/kb_release.py` и воркфлоу `release.yml` корректно обновляются.

---

## 4. План верификации (Verification Plan)

- [x] Сборка инсталлятора: `python scripts/build_installer.py` (Exit code 0).
- [x] Полный прогон тестов: `python -m unittest discover -s tests` (100% Pass).
- [x] Линтер базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links).

---

## 5. Критерии готовности (DoD)

- [x] Инсталлятор `install.py` пересобран и содержит все актуальные компоненты.
- [x] Все тесты проходят без ошибок.
- [x] Все задачи Фазы 7 завершены и согласованы.
- [x] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [x] Итоговая запись внесена в `docs/Devlog.md`.
