---
id: TASK-034
title: "Семантический протокол следующего шага в TEMPLATE_DEVLOG.md, аудит формулировок check_devlog_semantic_guard в scripts/kb_lint.py и тесты в tests/test_kb_lint.py"
status: planned
type: task
phase: 9
component:
  - templates
  - tooling
  - guardrails
parent_plan: "[[../../Plans/PLAN-009-single-task-barrier-and-stop-on-complete|PLAN-009]]"
created: 2026-10-02
updated: 2026-10-02
tags:
  - task/spec
  - phase9
  - templates
  - tooling
  - guardrails
  - devlog
  - kb-lint
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-034 — Семантический протокол журнала разработки и аудит в kb_lint.py

> **ID:** TASK-034  
> **Статус:** К реализации (Режим 2)  
> **Теги:** #task/spec #phase9 #templates #tooling #guardrails #devlog #kb-lint  
> **Родительский план:** [[../../Plans/PLAN-009-single-task-barrier-and-stop-on-complete|PLAN-009]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-012-single-task-execution-barrier-and-autonomous-pipeline-containment|RESEARCH-012]], [[../../../03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Реализовать уровни 3 и 4 эшелонированной защиты против своевольного авто-чейнинга (Eager Task Chaining) согласно [[../../../03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]] и [[../../../04_Research/RESEARCH-012-single-task-execution-barrier-and-autonomous-pipeline-containment|RESEARCH-012]]:
1. **Семантический шаблон журнала разработки:** Заменить нейтрально-побудительный заголовок `- **Следующий шаг:**` в `docs/00_Templates/TEMPLATE_DEVLOG.md` и `templates/TEMPLATE_DEVLOG.md` на эксплицитный маркер ожидания команды пользователя: `- **Рекомендуемый следующий шаг (Ожидает команды пользователя):** \`/kb-implement TASK-YYY\`.`
2. **Эвристический аудит в `scripts/kb_lint.py`:** Реализовать функцию `check_devlog_semantic_guard(docs_dir: Path) -> list`, выявляющую формулировки в `Devlog.md`, провоцирующие модель на несанкционированное продолжение работы. Аудит генерирует неблокирующие предупреждения (Warning, Exit code 0).
3. **Модульные тесты:** Покрыть новый аудит тестами в `tests/test_kb_lint.py` (проверка обнаружения опасных паттернов, игнорирование безопасных маркеров и неблокирующий статус).

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `docs/00_Templates/TEMPLATE_DEVLOG.md` — замена строки «Следующий шаг» на безопасный семантический маркер.
* `[MODIFY]` `templates/TEMPLATE_DEVLOG.md` — синхронизация канонического шаблона для сборщика инсталлятора.
* `[MODIFY]` `scripts/kb_lint.py` — добавление функции `check_devlog_semantic_guard`, интеграция предупреждений в итоговый вывод линтера.
* `[MODIFY]` `tests/test_kb_lint.py` — модульные тесты для `check_devlog_semantic_guard`.

---

## 3. Детали реализации

### 3.1. Изменения в шаблонах `TEMPLATE_DEVLOG.md`
В строках 27–28:
```markdown
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - <!-- Например: `/kb-implement TASK-YYY` или `/kb-release` -->
```

### 3.2. Эвристический аудит в `scripts/kb_lint.py`
Функция проверяет файл `Devlog.md` (в каталоге `docs/` или корне хранилища):
```python
def check_devlog_semantic_guard(docs_dir: Path) -> list:
    """
    Scans Devlog.md for bare 'Следующий шаг:' or 'Next Step:' triggers
    that lack explicit human-waiting markers, provoking eager auto-chaining.
    Returns a list of non-blocking warning strings.
    """
    warnings = []
    devlog_path = docs_dir / "Devlog.md"
    if not devlog_path.is_file():
        devlog_path = docs_dir.parent / "Devlog.md" if docs_dir.name == "docs" else devlog_path
    if not devlog_path.is_file():
        return warnings

    try:
        content = devlog_path.read_text(encoding="utf-8")
    except Exception:
        return warnings

    # Matches bare trigger without awaiting user confirmation guard
    pattern = re.compile(
        r'^\s*-\s*\*\*(?:Следующий шаг|Next Step)\*\*\s*:\s*(?!.*(?:ожидает команды пользователя|awaits user command|awaiting user input))',
        re.IGNORECASE | re.MULTILINE
    )

    for i, line in enumerate(content.splitlines(), start=1):
        if pattern.search(line):
            warnings.append(
                f"In 'Devlog.md' line {i}: bare step trigger detected without user guardrail. "
                f"Prefer '- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**' to prevent auto-chaining."
            )
    return warnings
```

В функции `run_linter` warnings объединяются с предупреждениями спецификации (`check_spec_drift`) и выводятся в секции предупреждений без изменения кода возврата.

### 3.3. Модульные тесты в `tests/test_kb_lint.py`
Добавляются тестовые методы:
- `test_devlog_semantic_guard_detects_bare_trigger`: Devlog с `- **Следующий шаг:** /kb-implement TASK-002` генерирует warning.
- `test_devlog_semantic_guard_passes_with_guardrail`: Devlog с `- **Рекомендуемый следующий шаг (Ожидает команды пользователя):** /kb-implement TASK-002` возвращает 0 warnings.
- `test_devlog_semantic_guard_non_blocking`: Проверка, что при наличии предупреждения `run_linter` возвращает код 0.

---

## 4. План верификации (Verification Plan)

- [ ] Модульные тесты: `python -m unittest tests/test_kb_lint.py` (100% pass, Exit code 0).
- [ ] Аудит базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links, 0 warnings в чистом репозитории).
- [ ] Ручная проверка шаблонов: проверка совпадения `docs/00_Templates/TEMPLATE_DEVLOG.md` и `templates/TEMPLATE_DEVLOG.md`.

---

## 5. Критерии готовности (DoD)

- [ ] Шаблоны `docs/00_Templates/TEMPLATE_DEVLOG.md` и `templates/TEMPLATE_DEVLOG.md` обновлены.
- [ ] Функция `check_devlog_semantic_guard` реализована в `scripts/kb_lint.py` с сохранением Zero Dependencies.
- [ ] Модульные тесты в `tests/test_kb_lint.py` успешно проходят.
- [ ] Все пункты Плана верификации выполнены.
- [ ] Статус обновлен в ТЗ, Канбане и Roadmap.
- [ ] Запись сессии внесена в `Devlog.md`.
