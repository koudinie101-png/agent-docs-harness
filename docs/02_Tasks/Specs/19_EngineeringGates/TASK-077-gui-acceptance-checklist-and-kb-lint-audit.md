---
id: TASK-077
title: "Чеклист приемочного тестирования GUI («UI не лжёт») в TEMPLATE_TEST.md и аудит целостности TechDebt.md в scripts/kb_lint.py"
status: done # planned | in-progress | done | cancelled
type: task
phase: 19
component:
  - testing
  - lint
  - templates
parent_plan: "[[../../Plans/PLAN-019-engineering-gates-and-tech-debt-governance|PLAN-019]]"
created: 2026-10-15
updated: 2026-10-15
tags:
  - task/spec
  - phase19
  - gui-testing
  - lint
  - quality-gates
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-077 — Чеклист приемочного тестирования GUI («UI не лжёт») в TEMPLATE_TEST.md и аудит целостности TechDebt.md в scripts/kb_lint.py

> **ID:** TASK-077 | **Статус:** К реализации  
> **Фаза:** 19 | **План:** [[../../Plans/PLAN-019-engineering-gates-and-tech-debt-governance|PLAN-019]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../04_Research/RESEARCH-020-self-improving-defect-loop-and-quality-gates|RESEARCH-020]], [[../../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]

---

## 1. Цель задачи

Реализовать инструменты проверки качества на уровнях Tier 1 (механический контроль) и Tier 3 (шаблоны тестирования):
1. Внедрить в шаблон `docs/00_Templates/TEMPLATE_TEST.md` структурированный чеклист приемочного тестирования пользовательских интерфейсов («UI не лжёт» / GUI Acceptance), фиксирующий, что успешные юнит-тесты и компиляция недостаточны без интерактивной проверки поведения интерфейса.
2. Реализовать в утилите `scripts/kb_lint.py` аудит целостности реестра техдолга `docs/02_Tasks/TechDebt.md` (валидация структуры таблицы, ссылок, формата `DEBT-XXX`).
3. Добавить в `scripts/kb_lint.py` неблокирующий эвристический аудит комментариев (предупреждение `WARN` при обнаружении висячих `TODO` без привязки к `ROADMAP-<ID>`).
4. Покрыть новые проверки модульными тестами в `tests/test_kb_lint.py`.

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `docs/00_Templates/TEMPLATE_TEST.md` — добавление чеклиста GUI Acceptance.
* `[MODIFY]` `scripts/kb_lint.py` — проверка существования `TechDebt.md`, валидация ссылок и идентификаторов `DEBT-XXX`, эвристический поиск висячих `TODO`.
* `[MODIFY]` `tests/test_kb_lint.py` — модульные тесты для новых проверок линтера.

---

## 3. Детали реализации

### 3.1. Чеклист приемочного тестирования GUI в `TEMPLATE_TEST.md`

В `TEMPLATE_TEST.md` добавляется секция:
```markdown
## 🎨 Чеклист приемочного тестирования GUI («UI не лжёт»)

> **Принцип:** Прохождение юнит-тестов и успешная компиляция не доказывают работоспособность визуального интерфейса. Требуется интерактивная верификация.

- [ ] **The 4-State Matrix:** проверены все 4 состояния (`Empty`, `Loading`, `Error`, `Populated`).
- [ ] **Отклик элементов (Interactive Response):** кнопки нажимаются, поля ввода принимают текст, фокус перемещается корректно.
- [ ] **Геометрия и верстка (No Clipping):** нет наложения текста, обрезания контейнеров, артефактов скролла.
- [ ] **Непрерывность потока (Main Thread):** операции ввода-вывода не блокируют UI-поток (отсутствуют «залипания» анимаций и спиннеров).
- [ ] **Фиксация скриншота:** визуальное подтверждение сохранено в `docs/assets/screenshots/<target>/TASK-XXX.png`.
```

### 3.2. Аудит `TechDebt.md` и висячих `TODO` в `scripts/kb_lint.py`

В `scripts/kb_lint.py`:
1. Функция `check_tech_debt_integrity(docs_path: Path) -> List[str]`:
   - Проверяет наличие `docs/02_Tasks/TechDebt.md`.
   - Парсит строки таблицы открытого долга, извлекает идентификаторы `DEBT-XXX` (регекс `^DEBT-\d{3,}$`).
   - Проверяет все викиссылки внутри таблицы на существование целей в `file_map`.
2. Функция `check_untracked_todos(docs_path: Path) -> List[str]`:
   - Сканирует файлы документации и скрипты на наличие паттерна `TODO` / `FIXME`, не сопровождаемого префиксом `ROADMAP-`.
   - Формирует неблокирующее предупреждение `[WARN] Untracked TODO without ROADMAP-<ID> reference in file:line`.

### 3.3. Модульные тесты в `tests/test_kb_lint.py`

Добавить тестовые сценарии:
* `test_tech_debt_lint_missing_file()`: проверка предупреждения/ошибки при отсутствии `TechDebt.md`.
* `test_tech_debt_lint_broken_links()`: обнаружение битых викиссылок в таблице долга.
* `test_tech_debt_lint_valid()`: успешное прохождение при корректном `TechDebt.md`.
* `test_untracked_todo_warning()`: фиксация предупреждения `WARN` для обычного `TODO` и отсутствие предупреждения для `ROADMAP-XXX`.

---

## 4. План верификации (Verification Plan)

- [ ] Модульные тесты: `pytest tests/test_kb_lint.py` (Exit code 0, 100% pass).
- [ ] Линт базы знаний: `python scripts/kb_lint.py --path docs` (Exit code 0, 0 broken links).
- [ ] Контроль лимита шаблонов: суммарный объем файлов `docs/00_Templates/` $\le 28\text{ KB}$.

---

## 5. Критерии готовности (DoD)

- [ ] В `TEMPLATE_TEST.md` внедрен чеклист GUI Acceptance («UI не лжёт»).
- [ ] В `scripts/kb_lint.py` реализован аудит `TechDebt.md` и предупреждение о висячих `TODO`.
- [ ] Тесты в `tests/test_kb_lint.py` успешно проходят.
