---
id: TASK-117
title: "Spec Quality Gate: маркеры [NEEDS CLARIFICATION], чек-лист ТЗ и правило KB-016"
status: done
type: task
phase: 32
track: standard
component:
  - core
  - lint
  - templates
parent_plan: "[[../../Plans/PLAN-029-right-sizing-and-spec-quality-gate|PLAN-029]]"
depends_on:
  - "TASK-116"
created: 2026-11-20
updated: 2026-11-20
tags:
  - task/spec
  - phase32
  - spec-quality
  - lint
  - quality-gates
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-117 — Spec Quality Gate: маркеры `[NEEDS CLARIFICATION]`, чек-лист ТЗ и правило KB-016

> **ID:** TASK-117 | **Статус:** Выполнено (Done) | **Фаза:** 32 | **Трек:** Standard  
> **План:** [[../../Plans/PLAN-029-right-sizing-and-spec-quality-gate|PLAN-029: Right-Sizing процесса и Spec Quality Gate]] | **Канбан:** [[../../Kanban|Канбан-доска]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0037-wave-2-quality-and-evidence-standard|ADR-0037]] | **Исследование:** [[../../../04_Research/RESEARCH-031-wave-2-quality-and-evidence-architecture|RESEARCH-031]]  
> **Зависимости:** [[TASK-116-right-sizing-matrix-and-kb020|TASK-116]]

---

## 1. Цель задачи

Искоренить «синдром уверенного угадывания» (спекулятивные домыслы агента при составлении ТЗ) и создать механический барьер качества требований в соответствии со стандартом [[../../../03_Decisions_ADR/ADR-0037-wave-2-quality-and-evidence-standard|ADR-0037]]:
1. Ввести обязательный раздел `## 0. Чек-лист качества ТЗ (Spec Quality Checklist)` и канонический синтаксический маркер `[NEEDS CLARIFICATION: ...]` в `TEMPLATE_TASK.md` в обеих директориях (`docs/00_Templates/` и `templates/`) с обеспечением 100% паритета.
2. Реализовать правило линтера **`KB-016` (Spec Quality Guard)** в `scripts/kb_lint.py`:
   - Для спецификаций со статусом `planned`: обнаружение маркеров выдаёт предупреждение (SEVERITY_WARNING).
   - Для спецификаций со статусом `in-progress` и `done`: обнаружение неразрешённых маркеров выдаёт блокирующую ошибку (SEVERITY_ERROR, Exit code 1). Запрещено брать в работу или закрывать задачи с неразрешёнными развилками!
3. Зарегистрировать правило в форматах вывода (`text`, `json`, `sarif`).
4. Покрыть логику правила модульными тестами в `tests/test_kb_lint.py` и подтвердить паритет шаблонов в `tests/test_template_parity.py`.

---

## 2. Затрагиваемые файлы и скоуп символов

* `[MODIFY]` `docs/00_Templates/TEMPLATE_TASK.md`:
  - Добавление раздела `## 0. Чек-лист качества ТЗ (Spec Quality Checklist)`
  - Синтаксический образец маркера `[NEEDS CLARIFICATION: ...]` в комментариях к шаблону
* `[MODIFY]` `templates/TEMPLATE_TASK.md`:
  - Синхронное добавление раздела `## 0. Чек-лист качества ТЗ (Spec Quality Checklist)`
* `[MODIFY]` `scripts/kb_lint.py`:
  - `CLARIFICATION_MARKER_RE` — регулярное выражение `re.compile(r"\[NEEDS CLARIFICATION(?::\s*([^\]]+))?\]", re.IGNORECASE)`
  - `check_spec_quality_markers(docs_dir: Path) -> List[Finding]` — функция сканирования файлов `Specs/` и `Bugs/` на незакрытые маркеры с дифференциацией строгости по статусу (`planned` $\to$ WARN, `in-progress`/`done` $\to$ ERROR)
  - `run_linter(...)` — интеграция `check_spec_quality_markers` в основной контур проверок
* `[MODIFY]` `tests/test_kb_lint.py`:
  - `TestSpecQualityGate(unittest.TestCase)` — модульные тесты правила `KB-016`:
    * `test_kb016_planned_task_with_marker_emits_warning()`
    * `test_kb016_in_progress_task_with_marker_emits_error()`
    * `test_kb016_done_task_with_marker_emits_error()`
    * `test_kb016_clean_task_passes()`
    * `test_kb016_cancelled_task_ignored()`

---

## 3. Детали реализации

### 3.1. Раздел качества ТЗ в TEMPLATE_TASK.md
В шаблоне `TEMPLATE_TASK.md` сразу после разделителя frontmatter размещается секция:
```markdown
## 0. Чек-лист качества ТЗ (Spec Quality Checklist)
- [ ] Требования однозначны и не содержат недосказанностей
- [ ] Нет неразрешённых маркеров `[NEEDS CLARIFICATION: ...]`
- [ ] Скоуп символов локализован (`[MODIFY]`/`[NEW]`/`[DELETE]`) без номеров строк (ADR-0029)
- [ ] Критерии приёмки (DoD) проверяемы автоматизированно
<!-- При наличии неясностей запрещено угадывать — ставьте маркер: [NEEDS CLARIFICATION: вопрос A vs B] -->
```

### 3.2. Алгоритм правила `KB-016` в `scripts/kb_lint.py`

```python
CLARIFICATION_MARKER_RE = re.compile(r"\[NEEDS CLARIFICATION(?::\s*([^\]]+))?\]", re.IGNORECASE)


def check_spec_quality_markers(docs_dir: Path) -> List[Finding]:
    """
    Tier 1 Quality Gate: audit clarification markers in tasks and bugs.

    Rule KB-016:
    - Status 'planned': SEVERITY_WARNING (reminder that task needs user refinement).
    - Status 'in-progress' or 'done': SEVERITY_ERROR (hard block: cannot implement or complete with open ambiguities).
    - Status 'cancelled': ignored.
    """
    findings: List[Finding] = []
    scan_dirs = [
        docs_dir / "02_Tasks" / "Specs",
        docs_dir / "02_Tasks" / "Bugs",
    ]
    # Fallback for nested docs/docs
    for i, d in enumerate(scan_dirs):
        if not d.is_dir() and (docs_dir / "docs" / d.relative_to(docs_dir)).is_dir():
            scan_dirs[i] = docs_dir / "docs" / d.relative_to(docs_dir)

    for target_dir in scan_dirs:
        if not target_dir.is_dir():
            continue
        for md_file in sorted(target_dir.rglob("*.md")):
            if md_file.name.startswith("TEMPLATE_"):
                continue
            try:
                content = md_file.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue

            matches = list(CLARIFICATION_MARKER_RE.finditer(content))
            if not matches:
                continue

            # Extract status from frontmatter
            status = "planned"
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    st_m = re.search(r"^status:\s*([^\s#]+)", parts[1], re.MULTILINE)
                    if st_m:
                        status = st_m.group(1).strip().lower()

            if status in ("cancelled", "rejected"):
                continue

            for match in matches:
                marker_detail = match.group(1).strip() if match.group(1) else "unspecified question"
                line_no = content[:match.start()].count("\n") + 1
                
                if status in ("in-progress", "done", "fixed"):
                    findings.append(make_finding(
                        "KB-016",
                        f"ERROR: file '{md_file.name}' with status '{status}' contains unresolved marker [NEEDS CLARIFICATION: {marker_detail}]",
                        file=_docs_rel(md_file, docs_dir),
                        severity="error",
                        location=f"{_docs_rel(md_file, docs_dir)}:L{line_no}",
                    ))
                else:  # planned / draft / proposed
                    findings.append(make_finding(
                        "KB-016",
                        f"WARN: file '{md_file.name}' contains open marker [NEEDS CLARIFICATION: {marker_detail}]",
                        file=_docs_rel(md_file, docs_dir),
                        severity="warning",
                        location=f"{_docs_rel(md_file, docs_dir)}:L{line_no}",
                    ))

    return findings
```

---

## 4. План верификации (Verification Plan)

- [x] **Синтаксический контроль Python:**
  ```bash
  python -m py_compile scripts/kb_lint.py
  ```
  *Ожидаемый результат:* Exit code 0, компиляция без ошибок.
- [x] **Юнит-тесты правила KB-016:**
  ```bash
  python -m unittest tests/test_kb_lint.py
  ```
  *Ожидаемый результат:* 100% прохождение всех тестов, включая класс `TestSpecQualityGate`.
- [x] **Тесты паритета шаблонов:**
  ```bash
  python -m unittest tests/test_template_parity.py
  ```
  *Ожидаемый результат:* 100% паритет `docs/00_Templates/` и `templates/`.
- [x] **Аудит целостности базы знаний:**
  ```bash
  python scripts/kb_lint.py --path docs
  ```
  *Ожидаемый результат:* 0 broken links, 0 errors, 0 ложных срабатываний `KB-016`.
- [x] **Проверка контрактов машинного вывода (JSON и SARIF):**
  ```bash
  python scripts/kb_lint.py --path docs --format json
  python scripts/kb_lint.py --path docs --format sarif
  ```
  *Ожидаемый результат:* Валидный машиночитаемый вывод с нулевыми ошибками.

---

## 5. Критерии готовности (DoD)

- [x] Раздел `## 0. Чек-лист качества ТЗ` добавлен в `TEMPLATE_TASK.md` в обеих директориях (`docs/00_Templates/` и `templates/`).
- [x] Правило `KB-016` реализовано в `scripts/kb_lint.py` с градацией `planned` $\to$ WARN, `in-progress/done` $\to$ ERROR.
- [x] Написаны и проходят модульные тесты для `KB-016` в `tests/test_kb_lint.py`.
- [x] Паритет шаблонов и полный аудит документации завершаются с кодом 0.
- [x] Статус задачи обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [x] Сессия зафиксирована в `docs/Devlog.md`.
