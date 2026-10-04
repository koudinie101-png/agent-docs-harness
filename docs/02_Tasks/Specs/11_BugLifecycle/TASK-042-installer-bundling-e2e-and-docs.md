---
id: TASK-042
title: "Синхронизация инсталлятора, сквозные E2E тесты и документация"
status: planned
type: task
phase: 11
component:
  - installer
  - tests
  - docs
parent_plan: "[[../../Plans/PLAN-011-bug-lifecycle-triage-and-release-targeting|PLAN-011]]"
created: 2026-10-04
updated: 2026-10-04
tags:
  - task/spec
  - phase11
  - installer
  - bundling
  - e2e
  - documentation
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-042 — Синхронизация инсталлятора, E2E тесты и документация

> **ID:** TASK-042  
> **Статус:** К реализации (Режим 2)  
> **Теги:** #task/spec #phase11 #installer #bundling #e2e #documentation  
> **Родительский план:** [[../../Plans/PLAN-011-bug-lifecycle-triage-and-release-targeting|PLAN-011]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-014-bug-lifecycle-triage-and-release-targeting|RESEARCH-014]], [[../../../03_Decisions_ADR/ADR-0019-bug-lifecycle-triage-and-release-targeting|ADR-0019]], [[../../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Финализировать интеграцию Фазы 11 в дистрибутив и пользовательскую документацию:
1. **Сборка автономного инсталлятора:** Пересобрать `install.py` с помощью `scripts/build_installer.py`, гарантируя упаковку обновленного шаблона `TEMPLATE_BUG.md` и модифицированных скиллов `kb-bug`, `kb-implement`, `kb-complete`.
2. **Сквозное E2E тестирование:** Расширить тестовый набор `tests/test_installer.py` для валидации чистого развертывания новой структуры и бережного обновления существующего харнесса (`install.py --update`).
3. **Синхронизация Living Spec и документации:** Актуализировать мастер-спецификацию `SPEC.md`, витрину `README.md` и руководство онбординга `docs/Onboarding.md` (а также его шаблон), закрепив правила изолированного триажа и исправления дефектов по TDD.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `scripts/build_installer.py` — проверить упаковку обновленных шаблонов и скиллов.
* `[MODIFY]` `install.py` — автономный дистрибутив, пересобранный сборщиком.
* `[MODIFY]` `tests/test_installer.py` — регрессионные и E2E тесты инсталлятора и процедуры обновления.
* `[MODIFY]` `SPEC.md` — актуализация раздела архитектуры дефектов и скиллов.
* `[MODIFY]` `README.md` — актуализация описания скиллов `/kb-bug` и `/kb-implement`.
* `[MODIFY]` `docs/Onboarding.md` и `templates/TEMPLATE_ONBOARDING.md` — обновление пошагового руководства работы с багами.

---

## 3. Детали реализации

### 3.1. Сборка и верификация инсталлятора
Запуск пересборки:
```bash
python scripts/build_installer.py
```
Проверка размера и целостности собранного файла `install.py`.

### 3.2. Тестирование инсталлятора в `tests/test_installer.py`
Добавить проверки:
- Проверка наличия атрибутов `target_release`, `target_phase`, `release_blocker`, `fixed_in` в развернутом `docs/00_Templates/TEMPLATE_BUG.md`.
- Проверка корректности обновления через `python install.py --update` в изолированном временном каталоге.

### 3.3. Актуализация документации
- **`SPEC.md`:** Отразить переход скилла `kb-bug` в Режим 2B (Defect Logging & Triage) и унификацию Режима 3 в `kb-implement` для багов.
- **`README.md`:** Обновить сводную таблицу скиллов и примеры запуска `/kb-implement BUG-XXX`.
- **`docs/Onboarding.md`:** Добавить наглядную схему двухэтапной обработки дефектов (Триаж $\to$ TDD-исправление).

---

## 4. План верификации (Verification Plan)

- [ ] Сборка дистрибутива:
  ```bash
  python scripts/build_installer.py
  ```
  *(Ожидаемый результат: Exit code 0, install.py обновлен)*.
- [ ] Запуск сквозных тестов инсталлятора:
  ```bash
  python -m unittest tests/test_installer.py
  ```
  *(Ожидаемый результат: 100% pass)*.
- [ ] Полный прогон тестового набора репозитория:
  ```bash
  python -m unittest discover -s tests
  ```
- [ ] Аудит базы знаний:
  ```bash
  python scripts/kb_lint.py --path docs
  ```

---

## 5. Критерии готовности (DoD)

- [ ] Инсталлятор `install.py` успешно пересобран и упаковывает все компоненты Фазы 11.
- [ ] Сквозные тесты `test_installer.py` подтверждают корректность развертывания и обновления.
- [ ] Документация (`SPEC.md`, `README.md`, `Onboarding.md`) полностью синхронизирована без дрифта.
- [ ] Все пункты Плана верификации пройдены.
