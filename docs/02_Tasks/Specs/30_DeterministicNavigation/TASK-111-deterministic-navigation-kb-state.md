---
id: TASK-111
title: "Ядро навигации scripts/kb_state.py"
status: planned
type: task
phase: 30
component:
  - core
  - cli
  - navigation
parent_plan: "[[../../Plans/PLAN-027-deterministic-navigation-and-task-graph|PLAN-027]]"
depends_on:
  - TASK-110
created: 2026-11-19
updated: 2026-11-19
tags:
  - task/spec
  - phase30
  - navigation
  - cli
  - kb-state
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-111 — Ядро навигации scripts/kb_state.py

> **ID:** TASK-111 | **Статус:** К реализации (Planned) | **Фаза:** 30  
> **План:** [[../../Plans/PLAN-027-deterministic-navigation-and-task-graph|PLAN-027: Детерминированная навигация и граф зависимостей]] | **Канбан:** [[../../Kanban|Канбан-доска]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0035-wave-1-deterministic-navigation-and-task-graph-standard|ADR-0035]] | **Исследование:** [[../../../04_Research/RESEARCH-029-wave-1-docs-integrity-and-deterministic-navigation|RESEARCH-029]]  
> **Зависимости:** [[TASK-110-task-dependency-graph-and-kb010|TASK-110 (Граф зависимостей depends_on)]]

---

## 1. Цель задачи

Реализовать автономную Zero-Dependency CLI-утилиту `scripts/kb_state.py`, предоставляющую однозначный, детерминированный ответ на вопрос «что делать дальше?» (`next`) и текущий срез прогресса проекта (`status`).

Утилита устраняет проблему «потери контекста» и ветвления логики AI-агентов после завершения задач, опираясь на правила приоритетов из [[../../../03_Decisions_ADR/ADR-0035-wave-1-deterministic-navigation-and-task-graph-standard|ADR-0035]]:
1. Задача в статусе `in-progress` (продолжение начатой работы).
2. Критический дефект с флагом `release_blocker: true` в `docs/02_Tasks/Bugs/`.
3. Первая готовая к запуску задача со статусом `planned`, все зависимости (`depends_on`) которой имеют статус `done`.
4. Рекомендация к релизу (`/kb-release`), если все задачи текущей фазы/проекта завершены.
5. Детекция тупика (deadlock), если все оставшиеся задачи заблокированы невыполненными зависимостями.

---

## 2. Затрагиваемые файлы и скоуп символов

* `[NEW]` `scripts/kb_state.py`:
  - `parse_frontmatter(content: str) -> Dict[str, Any]` — извлечение метаданных (`id`, `title`, `status`, `type`, `phase`, `depends_on`, `release_blocker`, `target_release`).
  - `scan_tasks_and_bugs(docs_root: Path) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]]]` — сбор всех задач из `Specs/` и дефектов из `Bugs/`.
  - `is_task_ready(task: Dict[str, Any], all_tasks: Dict[str, Dict[str, Any]], all_bugs: Dict[str, Dict[str, Any]]) -> Tuple[bool, List[str]]` — проверка готовности задачи к взятию в работу с возвратом списка незакрытых блокираторов.
  - `resolve_next_action(docs_root: Path) -> Dict[str, Any]` — 5-ступенчатая детерминированная резолюция следующего шага.
  - `compute_status_summary(docs_root: Path) -> Dict[str, Any]` — формирование сводки статуса проекта (фазы, счетчики статусов, готовые и заблокированные задачи).
  - `render_text_next(action_data: Dict[str, Any]) -> str` — человекочитаемый plain-text вывод следующего действия.
  - `render_text_status(summary_data: Dict[str, Any]) -> str` — человекочитаемый plain-text вывод статуса.
  - `main(argv: Optional[List[str]] = None) -> int` — CLI-диспетчер (`status`, `next`, `--path`, `--json`, `--format {text,json}`).
* `[NEW]` `tests/test_kb_state.py`:
  - `TestKbStateParser` — тестирование парсинга frontmatter (строчные и многострочные списки, булевы флаги).
  - `TestKbStateNextAction` — изолированное тестирование каждого уровня приоритета:
    - `test_priority_1_in_progress_task` — задача `in-progress` имеет наивысший приоритет.
    - `test_priority_2_release_blocker_bug` — критический баг блокирует запуск новых плановых задач.
    - `test_priority_2_non_blocker_bug_ignored` — некритический баг не блокирует готовые задачи.
    - `test_priority_3_ready_task_selected` — выбирается плановая задача с удовлетворенными `depends_on`.
    - `test_priority_3_blocked_task_skipped` — задача с незавершенными `depends_on` пропускается.
    - `test_priority_4_all_done_triggers_release` — завершение всех задач выдает рекомендацию релиза.
    - `test_priority_5_deadlock_detected` — взаимная блокировка или висячие зависимости выдают deadlock warning.
    - `test_empty_repository_state` — пустой каталог задач корректно обрабатывается (`no_tasks`).
  - `TestKbStateCLI` — тестирование аргументов командной строки, флагов `--json` / `--format`, кодов возврата (Exit 0 при успехе, Exit 1 при ошибках).
  - `TestKbStatePerformance` — замер времени сканирования на реальной базе знаний проекта ($\le 100\text{ мс}$).

---

## 3. Детали реализации

### 3.1. Архитектура резолюции `resolve_next_action`

```python
def resolve_next_action(docs_root: Path) -> Dict[str, Any]:
    """
    Детерминированная резолюция следующего действия согласно ADR-0035:
    1. in-progress task -> {"action": "continue_task", "status": "in-progress", ...}
    2. release_blocker bug -> {"action": "fix_blocker_bug", "status": "blocked_by_bug", ...}
    3. ready planned task -> {"action": "start_task", "status": "ready", ...}
    4. all tasks done -> {"action": "release", "status": "all_done", ...}
    5. all remaining blocked -> {"action": "deadlock_blocked", "status": "deadlock", ...}
    6. no tasks found -> {"action": "no_tasks", "status": "empty", ...}
    """
```

### 3.2. Контракт JSON-вывода (`--json` / `--format json`)

При вызове `python scripts/kb_state.py next --json`:

```json
{
  "status": "ready",
  "action": "start_task",
  "target": {
    "id": "TASK-111",
    "title": "Ядро навигации scripts/kb_state.py",
    "path": "docs/02_Tasks/Specs/30_DeterministicNavigation/TASK-111-deterministic-navigation-kb-state.md",
    "command": "/kb-implement TASK-111",
    "phase": 30
  },
  "blocked_by": [],
  "message": "Следующая готовая задача: TASK-111. Запустите: /kb-implement TASK-111"
}
```

При обнаружении блокировки или дедлока:

```json
{
  "status": "deadlock",
  "action": "deadlock_blocked",
  "target": null,
  "blocked_by": [
    {"task_id": "TASK-112", "missing_dependencies": ["TASK-111"]}
  ],
  "message": "Все оставшиеся плановые задачи заблокированы невыполненными зависимостями."
}
```

### 3.3. The 4-State UI Matrix для CLI-интерфейса

| Состояние | Поведение и визуализация | Обработка краевых случаев |
| :--- | :--- | :--- |
| **Empty** | В проекте нет задач в `Specs/` и `Bugs/` | Человечный текст: «Задачи не найдены. Создайте первую через `/kb-plan` или `/kb-task`» (JSON: `"status": "empty"`) |
| **Loading** | Сканирование каталогов `docs/` | Время выполнения $< 50\text{ мс}$, спиннер не требуется |
| **Error** | Невалидный путь к `docs` или критическая ошибка парсинга | Сообщение об ошибке в stderr, код возврата `1` |
| **Populated** | Штатный вывод `status` или `next` | Компактный структурированный текст для CLI или чистый JSON при `--json` |

---

## 4. План верификации (Verification Plan)

- [ ] Синтаксическая валидация: `python -m py_compile scripts/kb_state.py tests/test_kb_state.py` (Exit code 0).
- [ ] Модульные тесты: `python -m unittest tests/test_kb_state.py` (100% pass).
- [ ] Комплексный прогон тестов проекта: `python -m unittest discover -s tests` (100% pass).
- [ ] Интеграционная проверка CLI:
  - `python scripts/kb_state.py next` — возвращает рекомендацию по `TASK-111`.
  - `python scripts/kb_state.py next --json` — возвращает валидный JSON.
  - `python scripts/kb_state.py status` — выводит корректную сводку фаз и задач.
- [ ] Проверка целостности базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links).

### Visual DoD (CLI UX)
- Зафиксировать вывод команд `python scripts/kb_state.py status` и `python scripts/kb_state.py next` в отчете завершения задачи.

### Замеры производительности ($\ge 3$ прогонов):
- Замерить среднее время выполнения команды `python scripts/kb_state.py next --path docs` на боевом репозитории (целевой порог: $\le 100\text{ мс}$).

---

## 5. Критерии готовности (DoD)

- [ ] Код `scripts/kb_state.py` написан строго по ТЗ без внешних зависимостей (Zero-Deps: stdlib only).
- [ ] Реализованы команды `status` и `next`, флаги `--path`, `--json`, `--format`.
- [ ] Тестовый набор `tests/test_kb_state.py` покрывает все 5 уровней приоритетов и краевые состояния.
- [ ] Все пункты Плана верификации пройдены (Exit code 0).
- [ ] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [ ] Запись добавлена в `Devlog.md`.
