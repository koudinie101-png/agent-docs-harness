---
id: TASK-029
title: "Пресет undecided, интерактивная опция меню и CLI-флаг --idea в install.py"
status: done
type: task
phase: 8
component:
  - installer
  - cli
  - presets
parent_plan: "[[../../Plans/PLAN-008-greenfield-idea-first-and-living-spec|PLAN-008]]"
created: 2026-10-02
updated: 2026-10-02
tags:
  - task/spec
  - phase8
  - component/installer
  - component/cli
  - greenfield
  - idea-first
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-029 — Пресет undecided, интерактивная опция меню и CLI-флаг --idea в install.py

> **ID:** TASK-029  
> **Статус:** Выполнено (Режим 3)  
> **Теги:** #task/spec #phase8 #component/installer #component/cli #greenfield #idea-first  
> **Родительский план:** [[../../Plans/PLAN-008-greenfield-idea-first-and-living-spec|PLAN-008]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-009-greenfield-initialization-and-living-spec-drift|RESEARCH-009]], [[../../../03_Decisions_ADR/ADR-0014-greenfield-idea-first-initialization-and-living-spec-protocol|ADR-0014]], [[../../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Реализовать поддержку старта проекта с чистого листа от сырой идеи (Idea-First Greenfield) в утилите `install.py` согласно [[../../../03_Decisions_ADR/ADR-0014-greenfield-idea-first-initialization-and-living-spec-protocol|ADR-0014]] и [[../../../04_Research/RESEARCH-009-greenfield-initialization-and-living-spec-drift|RESEARCH-009]]:
1. **Пресет `undecided` в `STACK_PRESETS`:** Добавить нейтральный пресет без привязки к конкретному языку программирования или тестовому раннеру, с отложенным выбором стека через Режим 0 (`/kb-research`).
2. **Интерактивное меню CLI:** Добавить пункт меню `6) 💡 Undecided / Idea-First (Стек будет определен через /kb-research)`.
3. **CLI-флаг `--idea "<описание>"`:** Добавить аргумент командной строки для передачи продуктовой идеи. Если передан `--idea` без флага `--stack`, автоматически активируется пресет `undecided`. Если передан и `--stack`, описание идеи все равно заносится в `SPEC.md`.
4. **Формирование `SPEC.md` со статусом `discovery`:** При выборе `undecided` создавать мастер-спецификацию со статусом `status: discovery`, заполненным разделом «Концепция и цели» и пометкой о необходимости проведения исследования стека.
5. **Приветственное сообщение:** Финальный вывод инсталлятора должен явно направлять разработчика: `"Начните работу с команды агента: /kb-research <исследование идеи и выбор стека>"`.
6. **Автотесты:** Добавить юнит-тесты в `tests/test_installer.py`.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `install.py` — добавление пресета `undecided` в `STACK_PRESETS`, опции `6` в интерактивном опросе, флага `--idea`, модификация логики создания `SPEC.md` и приветственного баннера.
* `[MODIFY]` `tests/test_installer.py` — тесты установки с пресетом `undecided`, флагом `--idea` и валидация содержимого `SPEC.md`.

---

## 3. Детали реализации

### 3.1. Структура пресета `undecided` в `STACK_PRESETS` (`install.py`)

```python
"undecided": {
    "name": "Undecided / Idea-First Research",
    "language": "TBD (Determined in Mode 0 via /kb-research)",
    "file_ext": ".txt",
    "build_cmd": "echo 'No build command configured yet (run /kb-research)'",
    "test_cmd": "echo 'No test command configured yet (run /kb-research)'",
    "lint_cmd": "echo 'No lint command configured yet (run /kb-research)'",
    "sample_contract": "# Архитектурный контракт и интерфейсы будут определены по итогам RESEARCH-001\n",
    "bug_env": "  - ОС: TBD\n  - Стек: TBD (в процессе исследования)\n",
    "research_quirks": "* **Архитектурные ограничения и критерии выбора стека:** будут зафиксированы в ADR-0001.",
}
```

### 3.2. Обработка флага `--idea` и автовыбор пресета

```python
parser.add_argument(
    "--idea",
    type=str,
    default=None,
    help="Краткое описание продуктовой идеи для Greenfield-инициализации (автоматически активирует пресет undecided, если --stack не указан)",
)
```

Логика разрешения параметров:
```python
if args.idea and not args.stack:
    chosen_stack = "undecided"
```

### 3.3. Шаблонизация `SPEC.md`

При `chosen_stack == "undecided"`:
- Поле frontmatter: `status: discovery`.
- Раздел «1. Концепция и цели»: заполняется переданным текстом из `args.idea` (или стандартной формулировкой для Idea-First старта).
- Раздел «2. Архитектура и стек технологий»:
  ```markdown
  * **Статус стека:** Не определен. Требуется провести первичное исследование через команду агента: `/kb-research выбор-стека-и-архитектуры`.
  ```

---

## 4. План верификации (Verification Plan)

- [x] Тестирование CLI-флага: `python install.py --help` и запуск установки с `--stack undecided` (Exit code 0).
- [x] Тестирование инициализации с `--idea`: запуск во временной директории с проверкой `status: discovery` в `SPEC.md`.
- [x] Запуск модульных тестов инсталлятора: `python -m unittest tests/test_installer.py` (100% pass).
- [x] Проверка целостности базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links).

---

## 5. Критерии готовности (DoD)

- [x] Пресет `undecided` добавлен в `STACK_PRESETS` и интерактивное меню выбора стека.
- [x] Флаг `--idea` корректно обрабатывается и переносит описание идеи в `SPEC.md`.
- [x] Приветственный экран подсказывает вызов `/kb-research`.
- [x] Автотесты в `tests/test_installer.py` успешно выполняются (`test_19_undecided_preset_and_idea_flag`).
- [x] Статус задачи обновлен в Канбане и Дорожной карте.
