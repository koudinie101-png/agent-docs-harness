---
id: TASK-081
title: "Сквозные E2E-тесты в tests/test_installer.py, пересборка бандла install.py и синхронизация Living Spec"
status: done # planned | in-progress | done | cancelled
type: task
phase: 20
component:
  - installer
  - tests
  - docs
parent_plan: "[[../../Plans/PLAN-020-asset-storage-hardening-and-layout-linting|PLAN-020]]"
created: 2026-10-15
updated: 2026-10-16
tags:
  - task/spec
  - phase20
  - e2e
  - living-spec
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-081 — Сквозные E2E-тесты в tests/test_installer.py, пересборка бандла install.py и синхронизация Living Spec

> **ID:** TASK-081 | **Статус:** Выполнено (Режим 3)  
> **Фаза:** 20 | **План:** [[../../Plans/PLAN-020-asset-storage-hardening-and-layout-linting|PLAN-020]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../04_Research/RESEARCH-022-asset-storage-hardening-and-task-scoped-namespaces|RESEARCH-022]], [[../../../03_Decisions_ADR/ADR-0027-task-scoped-asset-namespaces-and-layout-linting|ADR-0027]]

---

## 1. Цель задачи

Завершить Фазу 20 пересборкой автономного бандла `install.py`, сквозным E2E-тестированием и синхронизацией витринной документации (Living Spec Invariant):
1. Пересобрать `EMBEDDED_ASSETS_B64` в монолитном `install.py` через `python scripts/build_installer.py`, упаковав обновленные в `TASK-079` и `TASK-080` файлы `scripts/kb_lint.py` и `docs/00_Templates/TEMPLATE_TASK.md`.
2. Расширить E2E-тесты в `tests/test_installer.py`, проверив наличие таксономии `TASK-XXX/`, `asis.svg` / `tobe.svg` и `mockups/flows/` в сгенерированных `UI_Design_System.md`, `AGENTS.md`, `GEMINI.md` и `TEMPLATE_TASK.md`, а также валидацию развернутого проекта встроенным `kb_lint.py`.
3. Синхронизировать `SPEC.md`, `README.md` и `docs/Onboarding.md` с архитектурой Фазы 20 (`ADR-0027`).

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `install.py` — обновление `EMBEDDED_ASSETS_B64` через `scripts/build_installer.py`.
* `[MODIFY]` `tests/test_installer.py` — добавление E2E-проверок генерации `UI_Design_System.md`, правил `AGENTS.md`/`GEMINI.md` и встроенного `kb_lint.py` с `check_asset_layout()`.
* `[MODIFY]` `SPEC.md` — отражение Фазы 20, `ADR-0027`, пространств имен `mockups/<target>/TASK-XXX/` и проверки `check_asset_layout()` в `kb_lint.py`.
* `[MODIFY]` `README.md` — обновление описания контура визуальных ассетов и правил `kb_lint.py`.
* `[MODIFY]` `docs/Onboarding.md` — дополнение раздела `🎨 1. Изолированное хранилище ассетов (docs/assets/)` правилами нейминга `TASK-XXX/`, `asis.svg` / `tobe.svg` и `mockups/flows/TASK-XXX/`.

---

## 3. Детали реализации

### 3.1. Пересборка автономного инсталлятора

Запустить сборщик:
```bash
python scripts/build_installer.py
```
Убедиться, что `EMBEDDED_ASSETS_B64` в `install.py` содержит актуальные версии `scripts/kb_lint.py` (с `VALID_ASSET_ROOTS` и `check_asset_layout`) и `docs/00_Templates/TEMPLATE_TASK.md`.

### 3.2. Сквозные E2E-тесты в `tests/test_installer.py`

Дополнить или добавить тест в `tests/test_installer.py`:
```python
def test_ui_harness_task_scoped_mockup_taxonomy_and_asset_layout_lint(self):
    """Verifies Phase 20: UI_Design_System.md, AGENTS.md, TEMPLATE_TASK.md and deployed kb_lint.py."""
```
Проверяемые инварианты:
1. При установке с `--ui windows,android` создаются `docs/assets/mockups/flows/` и `docs/01_Architecture/UI_Design_System.md`.
2. В `docs/01_Architecture/UI_Design_System.md` присутствуют `docs/assets/mockups/<target>/TASK-XXX/`, `asis.svg`, `tobe.svg` и `docs/assets/mockups/flows/TASK-XXX/`.
3. В развернутом `AGENTS.md` и `GEMINI.md` зафиксирован путь `docs/assets/mockups/<target>/TASK-XXX/`.
4. В развернутом `docs/00_Templates/TEMPLATE_TASK.md` указан `docs/assets/mockups/<target>/TASK-XXX/tobe.svg`.
5. Развернутый `scripts/kb_lint.py` проходит с кодом `0` на чистом проекте, выдает предупреждение `WARN` при создании неканонической папки `docs/assets/windows/` и возвращает код `1` при битой относительной ссылке на `TASK-099/tobe.svg` даже при наличии `TASK-001/tobe.svg`.

### 3.3. Синхронизация Living Spec (`SPEC.md`, `README.md`, `docs/Onboarding.md`)

1. **`SPEC.md`:**
   - В разделе `2.3. Ключевые архитектурные инварианты` (`The 4-State UI & Visual Verification Invariant`) указать изоляцию макетов задач в `docs/assets/mockups/<target>/TASK-XXX/` (`asis.svg`, `tobe.svg`, `<surface>_tobe.svg`), кросс-девайсных сценариев в `docs/assets/mockups/flows/TASK-XXX/` и механический контроль топологии `check_asset_layout()` в `scripts/kb_lint.py`.
   - В разделе `3. Этапы разработки (Фазы)` добавить описание **Фазы 20: Стандартизация хранения макетов в пространствах имен задач и линтинг топологии `docs/assets/` (Asset Storage Hardening & Layout Linting)**.
2. **`README.md`:**
   - Обновить пункт 11 (`The 4-State UI & Visual Verification Invariant`), добавив ссылку на `ADR-0027`, структуру `docs/assets/mockups/<target>/TASK-XXX/` (`asis.svg` / `tobe.svg`) и проверку топологии `docs/assets/` в `kb_lint.py`.
3. **`docs/Onboarding.md`:**
   - В разделе `### 🎨 1. Изолированное хранилище ассетов (docs/assets/)` детализировать структуру `docs/assets/mockups/<target>/TASK-XXX/` (`asis.svg`, `tobe.svg`, `<surface>_tobe.svg`) и `docs/assets/mockups/flows/TASK-XXX/`.

---

## 4. План верификации (Verification Plan)

- [x] Пересборка бандла: `python scripts/build_installer.py` (Exit code 0).
- [x] Сборка всех скриптов: `python -m py_compile install.py scripts/*.py` (Exit code 0).
- [x] Полный прогон тестов: `pytest` (Exit code 0, 100% pass).
- [x] Проверка базы знаний: `python scripts/kb_lint.py --path docs` (Exit code 0, 0 broken links).

---

## 5. Критерии готовности (DoD)

- [x] Автономный бандл `install.py` пересобран и синхронизирован с исходниками.
- [x] E2E-тесты в `tests/test_installer.py` проходят успешно.
- [x] Документация `SPEC.md`, `README.md`, `docs/Onboarding.md` синхронизирована (Living Spec).
- [x] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [x] Запись добавлена в `Devlog.md`.
