---
id: TASK-110
title: "Граф зависимостей задач (depends_on) и правило линтера KB-010"
status: planned
type: task
phase: 30
component:
  - core
  - lint
  - templates
parent_plan: "[[../../Plans/PLAN-027-deterministic-navigation-and-task-graph|PLAN-027]]"
created: 2026-11-19
updated: 2026-11-19
tags:
  - task/spec
  - phase30
  - navigation
  - task-graph
  - lint
  - kb010
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-110 — Граф зависимостей задач (depends_on) и правило линтера KB-010

> **ID:** TASK-110 | **Статус:** К реализации (Planned) | **Фаза:** 30  
> **План:** [[../../Plans/PLAN-027-deterministic-navigation-and-task-graph|PLAN-027: Детерминированная навигация и граф зависимостей]] | **Канбан:** [[../../Kanban|Канбан-доска]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0035-wave-1-deterministic-navigation-and-task-graph-standard|ADR-0035]] | **Исследование:** [[../../../04_Research/RESEARCH-029-wave-1-docs-integrity-and-deterministic-navigation|RESEARCH-029]]

---

## 1. Цель задачи

Предотвратить преждевременный запуск задач и хаотичную очередность разработки за счет введения явного машинного контроля графа зависимостей (`depends_on`). 

Задача реализует зарезервированное в [[../../../03_Decisions_ADR/ADR-0032-machine-readable-lint-contract-and-rule-registry|ADR-0032]] правило линтера **`KB-010`**:
1. Валидация отсутствия циклических зависимостей в графе задач (алгоритм DFS).
2. Валидация отсутствия ссылок на неизвестные (висячие) задачи.
3. Расширение эталонного шаблона `TEMPLATE_TASK.md` полем `depends_on`.

---

## 2. Затрагиваемые файлы и скоуп символов

* `[MODIFY]` `scripts/kb_lint.py`:
  - `RULE_SEVERITY` — регистрация активной строгости `"KB-010": "error"`.
  - `parse_task_dependencies(content: str) -> List[str]` — извлечение списка идентификаторов из YAML frontmatter поля `depends_on`.
  - `find_dependency_cycles(graph: Dict[str, List[str]]) -> Optional[List[str]]` — детекция циклов в ориентированном графе с возвратом цепочки замыкания.
  - `check_task_dependencies(docs_root: Path) -> List[Finding]` — сбор графа спецификаций, проверка висячих идентификаторов и запуск детектора циклов.
  - `main(argv: Optional[List[str]]) -> int` — интеграция проверки `check_task_dependencies` в конвейер `kb_lint.py`.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_TASK.md`:
  - frontmatter — добавление опционального поля `# depends_on: []`.
* `[MODIFY]` `templates/TEMPLATE_TASK.md`:
  - frontmatter — синхронное добавление `# depends_on: []` для сохранения побайтового паритета (`test_template_parity.py`).
* `[MODIFY]` `tests/test_kb_lint.py`:
  - `TestRuleRegistry.test_01_registry_and_severity_contract` — обновление ассерта (все правила KB-001..KB-015 теперь имеют активную severity).
  - `TestRuleRegistry.test_03_kb_010_cannot_be_emitted_yet` — замена на тест легальной эмиссии `KB-010`.
  - `TestTaskDependencies` — новый тестовый класс:
    - `test_valid_dag_passes` — линейные и разветвленные ациклические зависимости проходят без ошибок.
    - `test_missing_dependency_emits_kb010` — ссылка на несуществующий ID генерирует Finding KB-010.
    - `test_direct_cycle_emits_kb010` — цикл `A -> B -> A` генерирует Finding KB-010 с путем цикла.
    - `test_transitive_cycle_emits_kb010` — цикл `A -> B -> C -> A` генерирует Finding KB-010 с путем цикла.

---

## 3. Детали реализации

### 3.1. Регистрация правила KB-010 в `scripts/kb_lint.py`

```python
RULE_REGISTRY: Dict[str, str] = {
    ...
    "KB-010": "Task dependency cycle or unknown dependency",
    ...
}

RULE_SEVERITY: Dict[str, str] = {
    ...
    "KB-009": "warning",
    "KB-010": "error",
    "KB-011": "error",
    ...
}
```

### 3.2. Парсинг `depends_on` из YAML frontmatter
Парсер извлекает список строковых ID, очищая возможные викиссылки или кавычки:
```python
def parse_task_dependencies(content: str) -> List[str]:
    """Extracts list of task IDs from YAML frontmatter 'depends_on' field."""
    # Поддержка инлайн [TASK-001, TASK-002] и блочного списка:
    # depends_on:
    #   - TASK-001
    #   - "[[TASK-002]]"
```

### 3.3. Детекция циклов и валидация графа
```python
def find_dependency_cycles(graph: Dict[str, List[str]]) -> Optional[List[str]]:
    """Detects cycles in directed graph using DFS coloring. Returns cycle path or None."""
    color: Dict[str, int] = {}  # 0=unvisited, 1=visiting, 2=visited

    def dfs(node: str, path: List[str]) -> Optional[List[str]]:
        color[node] = 1
        for dep in graph.get(node, []):
            if color.get(dep, 0) == 1:
                idx = path.index(dep) if dep in path else 0
                return path[idx:] + [dep]
            if color.get(dep, 0) == 0:
                cycle = dfs(dep, path + [dep])
                if cycle:
                    return cycle
        color[node] = 2
        return None

    for n in sorted(graph.keys()):
        if color.get(n, 0) == 0:
            c = dfs(n, [n])
            if c:
                return c
    return None
```

### 3.4. Сообщения об ошибках Finding KB-010
1. При обнаружении цикла:  
   `make_finding("KB-010", f"Task dependency cycle detected: {' -> '.join(cycle)}", file=rel_path, severity="error")`
2. При ссылке на неизвестную задачу:  
   `make_finding("KB-010", f"Task '{task_id}' depends on unknown task '{dep}'", file=rel_path, severity="error")`

---

## 4. План верификации (Verification Plan)

- [ ] Контрактные и юнит-тесты:
  ```bash
  python -m unittest tests/test_kb_lint.py
  ```
  *Ожидаемый результат:* 100% тестов проходят, включая новый класс `TestTaskDependencies` и обновленный контракт `TestRuleRegistry`.
- [ ] Паритет шаблонов:
  ```bash
  python -m unittest tests/test_template_parity.py
  ```
  *Ожидаемый результат:* 16 шаблонов идентичны, побайтовый паритет сохранен.
- [ ] Аудит целостности базы знаний:
  ```bash
  python scripts/kb_lint.py --path docs
  ```
  *Ожидаемый результат:* Exit code 0, 0 broken links, 0 нарушений KB-010 на существующей кодовой базе.

---

## 5. Критерии готовности (DoD)

- [ ] Код в `scripts/kb_lint.py` написан строго без сторонних зависимостей (Python 3 stdlib).
- [ ] Правило `KB-010` активировано в `RULE_SEVERITY` и включено в общий pipeline проверок.
- [ ] Все пункты Плана верификации пройдены с кодом возврата 0.
- [ ] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [ ] Запись добавлена в `Devlog.md`.
