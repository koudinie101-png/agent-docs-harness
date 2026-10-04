---
id: TASK-041
title: "Релизный таргетинг и фильтрация дефектов в scripts/kb_release.py и тесты"
status: planned
type: task
phase: 11
component:
  - scripts
  - releases
  - release-targeting
  - testing
parent_plan: "[[../../Plans/PLAN-011-bug-lifecycle-triage-and-release-targeting|PLAN-011]]"
created: 2026-10-04
updated: 2026-10-04
tags:
  - task/spec
  - phase11
  - releases
  - bug-lifecycle
  - kb-release
  - blockers
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-041 — Релизный таргетинг и фильтрация дефектов в kb_release.py

> **ID:** TASK-041  
> **Статус:** К реализации (Режим 2)  
> **Теги:** #task/spec #phase11 #releases #bug-lifecycle #kb-release #blockers  
> **Родительский план:** [[../../Plans/PLAN-011-bug-lifecycle-triage-and-release-targeting|PLAN-011]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-014-bug-lifecycle-triage-and-release-targeting|RESEARCH-014]], [[../../../03_Decisions_ADR/ADR-0019-bug-lifecycle-triage-and-release-targeting|ADR-0019]], [[../../../03_Decisions_ADR/ADR-0010-github-release-notes-and-public-distribution-standard|ADR-0010]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Реализовать точный релизный таргетинг дефектов и префлайт-контроль релиз-блокеров в утилите `scripts/kb_release.py` согласно [[../../../03_Decisions_ADR/ADR-0019-bug-lifecycle-triage-and-release-targeting|ADR-0019]]:
1. **Устранение утечки исторических багов:** Модифицировать агрегацию дефектов в чейнджлогах так, чтобы в релиз включались строго те дефекты, которые устранены в текущей версии (`fixed_in == target_version` или `target_release == target_version`), исключая дублирование старых закрытых багов во всех последующих версиях.
2. **Префлайт-проверка релиз-блокеров (`release_blocker`):** Внедрить прерывание релизного пайплайна (Exit code 1) при наличии незакрытых дефектов (`status: open | in-progress`) с атрибутом `release_blocker: true`, нацеленных на выпускаемый релиз.
3. **Бережный Fallback для легаси-отчетов:** Обеспечить обратную совместимость для отчетов дефектов, созданных до внедрения поля `fixed_in` (fallback на `target_phase == current_phase`).
4. **Модульное тестирование:** Покрыть новую логику изолированными тестами в `tests/test_kb_release.py`.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `scripts/kb_release.py` — модифицировать сбор дефектов с фильтрацией по целевой версии и добавить префлайт-проверку открытых релиз-блокеров.
* `[MODIFY]` `tests/test_kb_release.py` — добавить модульные тесты фильтрации багов по `fixed_in`, исключения чужих багов и прерывания при наличии `release_blocker: true`.

---

## 3. Детали реализации

### 3.1. Фильтрация дефектов в `scripts/kb_release.py`
Функция сбора закрытых дефектов для чейнджлогера расширяется сигнатурой и логикой таргетинга:
```python
def collect_fixed_bugs(bugs_dir: Path, target_version: str, current_phase: int = None) -> list[dict]:
    """
    Собирает закрытые дефекты, таргетированные строго на целевую версию релиза.
    
    Критерии включения:
    1. status == 'fixed'
    2. fixed_in == target_version ИЛИ target_release == target_version
    3. Fallback: если fixed_in отсутствует, но target_phase == current_phase
    """
```
Все дефекты других версий или фаз отсекаются.

### 3.2. Префлайт-контроль блокеров
Перед формированием релиза вызывается проверка:
```python
def check_release_blockers(bugs_dir: Path, target_version: str, current_phase: int = None) -> list[str]:
    """
    Проверяет наличие незакрытых дефектов с release_blocker == True.
    Возвращает список сообщений об ошибках. При непустом списке релиз завершается с ошибкой.
    """
```
Если найден незакрытый блокер:
```text
ERROR: Release vX.Y.Z is blocked by open defect BUG-XXX: <Title> (release_blocker=true)
```
Пайплайн аварийно останавливается с `sys.exit(1)`.

### 3.3. Модульные тесты в `tests/test_kb_release.py`
Добавить тестовый класс `TestBugReleaseTargeting`:
1. `test_collect_fixed_bugs_matching_version`: проверяет, что баг с `fixed_in: v0.11.0` включается в чейнджлог `v0.11.0`.
2. `test_collect_fixed_bugs_excludes_prior_versions`: проверяет, что закрытый баг с `fixed_in: v0.10.0` не попадает в чейнджлог `v0.11.0`.
3. `test_check_release_blockers_aborts_on_open_blocker`: проверяет, что открытый баг с `release_blocker: true` вызывает ошибку.
4. `test_check_release_blockers_passes_when_fixed`: проверяет, что закрытый баг с `release_blocker: true` не блокирует сборку.

---

## 4. План верификации (Verification Plan)

- [ ] Запуск модульных тестов релиза:
  ```bash
  python -m unittest tests/test_kb_release.py
  ```
  *(Ожидаемый результат: 100% pass)*.
- [ ] Полный прогон всех существующих тестов:
  ```bash
  python -m unittest discover -s tests
  ```
- [ ] Аудит базы знаний:
  ```bash
  python scripts/kb_lint.py --path docs
  ```

---

## 5. Критерии готовности (DoD)

- [ ] Утилита `scripts/kb_release.py` фильтрует баги строго по целевому релизу.
- [ ] Наличие открытого релиз-блокера блокирует выпуск с Exit code 1.
- [ ] Все модульные тесты в `tests/test_kb_release.py` успешно проходят.
- [ ] Отсутствуют регрессии в существующих сценариях сборки релизов.
