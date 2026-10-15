---
id: TASK-074
title: "Бандлинг инсталлятора build_installer.py, сквозные E2E тесты и актуализация Living Spec"
status: planned
type: task
phase: 18
component:
  - installer
  - tests
  - spec
  - docs
parent_plan: "[[../../Plans/PLAN-018-heterogeneous-ui-ux-and-visual-asset-harness|PLAN-018]]"
created: 2026-10-15
updated: 2026-10-15
tags:
  - task/spec
  - phase18
  - installer
  - e2e
  - spec
  - tests
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-074 — Бандлинг инсталлятора build_installer.py, сквозные E2E тесты и актуализация Living Spec

> **ID:** TASK-074 | **Статус:** К реализации  
> **Фаза:** 18 | **Релиз:** v0.18.0  
> **План:** [[../../Plans/PLAN-018-heterogeneous-ui-ux-and-visual-asset-harness|PLAN-018]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../04_Research/RESEARCH-021-heterogeneous-ui-ux-and-visual-asset-management|RESEARCH-021]], [[../../../03_Decisions_ADR/ADR-0026-heterogeneous-ui-ux-and-visual-asset-management|ADR-0026]]

---

## 1. Цель задачи

Завершить цикл разработки Фазы 18:
1. **Сквозное автоматизированное тестирование:** разработать модульные и E2E тесты для нового функционала в `tests/test_installer.py`, `tests/test_kb_lint.py` и `tests/test_kb_release.py`.
2. **Сборка дистрибутива:** упаковать все обновленные шаблоны, правила и код в автономный монолит `install.py` через `scripts/build_installer.py`.
3. **Living Spec синхронизация:** актуализировать Мастер-Спецификацию (`SPEC.md`), витрину проекта (`README.md`) и руководство онбординга (`docs/Onboarding.md`), зафиксировав описание композитного флага `--ui`, структуру хранения `docs/assets/`, Obsidian DX и дисциплины Visual DoD.
4. **Комплексная валидация:** гарантировать 100% прохождение всех тестов и нулевой уровень ошибок линтинга базы знаний.

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `tests/test_installer.py` — тесты композитного `--ui`, двухступенчатой раскладки каталогов, мержа `docs/.obsidian/app.json` и правил `.gitignore`.
* `[MODIFY]` `tests/test_kb_lint.py` — тесты изолированной индексации медиа, синтаксиса размера Obsidian и предупреждений Asset Weight Gate ($> 2\text{ MB}$).
* `[MODIFY]` `tests/test_kb_release.py` — тесты конвертации медиа-викиссылок без добавления `.md`.
* `[MODIFY]` `scripts/build_installer.py` / `install.py` — сборка монолитного инсталлятора с обновленными ассетами.
* `[MODIFY]` `SPEC.md` — фиксация композитного ключа `--ui`, архитектуры ассетов и правил UI/UX.
* `[MODIFY]` `README.md` — витрина возможностей визуального контура и примеры работы с `--ui`.
* `[MODIFY]` `docs/Onboarding.md` — руководство по работе с визуальными ассетами в Obsidian (Ctrl+V) и матрице состояний.

---

## 3. Детали реализации

### 3.1. Тестовые сценарии в `tests/test_installer.py`
* `test_ui_profiles_scaffolding()`:
  - Проверка `--ui web` $\to$ создание `docs/assets/screenshots/web/`, отсутствие `Protocols/`.
  - Проверка `--ui windows,android` $\to$ создание каталогов для обоих таргетов, `multi-device/`, `Protocols/` и спецификаций в `Targets/`.
  - Проверка `--ui none` $\to$ отсутствие каталога `docs/assets/`.
* `test_obsidian_app_json_safe_merge()`:
  - Создание существующего `docs/.obsidian/app.json` с ключами `{"theme": "obsidian", "legacy": true}`.
  - Запуск `install.py --update` $\to$ проверка сохранения пользовательских ключей и добавления `"attachmentFolderPath": "assets/screenshots"`.
* `test_gitignore_visual_rules()`:
  - Проверка добавления `!.obsidian/app.json` и `tmp/ui_snapshots/`.

### 3.2. Тестовые сценарии в `tests/test_kb_lint.py` и `tests/test_kb_release.py`
* Проверка, что `TASK-001.png` не затеняет спецификацию `TASK-001.md`.
* Проверка, что ссылки `![[image.png|800x600]]` валидируются успешно без ошибок «target not found».
* Проверка генерации `WARN` при весе файла $> 2\text{ MB}`.
* Проверка, что при экспорте заметок релиза ссылка `![[diagram.png]]` преобразуется в `![diagram](diagram.png)`, а не в `diagram.png.md`.

### 3.3. Бандлинг и документация
* Запуск `python scripts/build_installer.py` для обновления монолитного `install.py`.
* Синхронизация разделов CLI, архитектуры и гайдлайнов в `SPEC.md`, `README.md` и `docs/Onboarding.md`.

---

## 4. План верификации (Verification Plan)

- [ ] Запуск модульного сьюта: `python -m unittest discover -s tests` (100% pass, 0 regressions).
- [ ] Сборка инсталлятора: `python scripts/build_installer.py` (Exit code 0).
- [ ] Линтинг базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links).
- [ ] Аудит Living Spec: `SPEC.md` и `README.md` содержат актуальные флаги и описание ассетов.

---

## 5. Критерии готовности (DoD)

- [ ] Все модульные и E2E тесты написаны и проходят успешно.
- [ ] Монолитный `install.py` пересобран и готов к распространению.
- [ ] Документация `SPEC.md`, `README.md` и `docs/Onboarding.md` синхронизирована с кодом.
- [ ] Все пункты Плана верификации пройдены.
- [ ] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [ ] Запись добавлена в `Devlog.md`.
