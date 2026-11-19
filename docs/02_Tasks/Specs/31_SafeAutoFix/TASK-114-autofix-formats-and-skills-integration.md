---
id: TASK-114
title: "Машинно-читаемый контракт (JSON/SARIF fixable) и интеграция автофикса в скиллы"
status: planned
type: task
phase: 31
component:
  - core
  - lint
  - skills
  - docs
parent_plan: "[[../../Plans/PLAN-028-kb-lint-safe-autofix|PLAN-028]]"
depends_on:
  - TASK-113
created: 2026-11-19
updated: 2026-11-19
tags:
  - task/spec
  - phase31
  - lint
  - autofix
  - contracts
  - skills
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-114 — Машинно-читаемый контракт (JSON/SARIF fixable) и интеграция автофикса в скиллы

> **ID:** TASK-114 | **Статус:** К реализации (Planned) | **Фаза:** 31  
> **План:** [[../../Plans/PLAN-028-kb-lint-safe-autofix|PLAN-028: Безопасный автофикс kb_lint --fix]] | **Канбан:** [[../../Kanban|Канбан-доска]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0036-kb-lint-safe-autofix-standard|ADR-0036]] | **Исследование:** [[../../../04_Research/RESEARCH-030-kb-lint-safe-autofix|RESEARCH-030]]  
> **Зависимости:** [[TASK-113-kb-lint-autofix-core|TASK-113 (Ядро автофикса)]]

---

## 1. Цель задачи

Расширить машиночитаемые форматы отчётов и интегрировать безопасный автофикс в рабочий процесс агентов:
1. Добавить в модель находок `Finding` булево поле `fixable: bool` и сериализацию признака исправляемости.
2. Актуализировать рендерер `--format json`: включить поле `fixable` в объекты находок, счётчик `fixable` в секцию `summary` и блок запланированных правок при `--fix`.
3. Актуализировать рендерер `--format sarif`: добавить стандартный массив `fixes` в результаты анализа SARIF 2.1.0 для поддерживаемых правил.
4. Добавить контрактные тесты сериализации автофикса в `tests/test_kb_lint.py` и `tests/test_kb_lint_fix.py`.
5. Интегрировать поддержку и вызов автофикса в скиллы `.agents/skills/kb-lint/SKILL.md` (руководство оператора) и `.agents/skills/kb-complete/SKILL.md` (устранение тривиальных дефектов перед закрытием задачи).
6. Дополнить раздел команд в памятке `docs/Onboarding.md`.

---

## 2. Затрагиваемые файлы и скоуп символов

* `[MODIFY]` `scripts/kb_lint.py`:
  - `Finding.__slots__` — добавление атрибута `fixable`.
  - `Finding.__new__(..., fixable: bool = False)` — инициализация признака исправляемости.
  - `make_finding(..., fixable: bool = False)` — проброс параметра `fixable`.
  - `_finding_payload(finding: Finding) -> dict` — включение `"fixable": bool(finding.fixable)`.
  - `render_json(report: LintReport) -> str` — счётчик `"fixable"` в `summary`.
  - `render_sarif(report: LintReport) -> str` — генерация объекта `fixes` в результатах SARIF 2.1.0.
* `[MODIFY]` `.agents/skills/kb-lint/SKILL.md`:
  - Таблица команд и режимов — добавление документации по `--fix`, `--write`, `--allow-dirty`.
* `[MODIFY]` `.agents/skills/kb-complete/SKILL.md`:
  - Шаг 8 (Верификация базы знаний) — рекомендация применения `python scripts/kb_lint.py --fix --write` при обнаружении исправляемых дефектов.
* `[MODIFY]` `docs/Onboarding.md`:
  - Раздел 18 (Навигация и диагностика) — добавление сценариев применения `--fix`.
* `[MODIFY]` `tests/test_kb_lint_fix.py`:
  - `TestKbLintContractFormats` — тесты схемы JSON (`fixable` в `summary` и `findings`) и SARIF 2.1.0 (`fixes`).

---

## 3. Детали реализации

### 3.1. Расширение модели `Finding` и контракта JSON

```python
class Finding(str):
    __slots__ = ("rule_id", "severity", "file", "location", "fixable")

    def __new__(cls, rule_id: str, message: str, severity: str, file: str = "", location: str = "", fixable: bool = False):
        obj = super().__new__(cls, message)
        obj.rule_id = rule_id
        obj.severity = severity
        obj.file = file or ""
        obj.location = location or ""
        obj.fixable = bool(fixable)
        return obj


def _finding_payload(finding: Finding) -> dict:
    return {
        "rule_id": finding.rule_id,
        "severity": finding.severity,
        "file": finding.file or None,
        "location": finding.location or None,
        "message": finding.message,
        "fixable": getattr(finding, "fixable", False),
    }
```

В `render_json(report)`:
```json
{
  "version": 1,
  "summary": {
    "files": 280,
    "wikilinks": 2762,
    "errors": 0,
    "warnings": 2,
    "fixable": 2
  },
  "errors": [],
  "warnings": [
    {
      "rule_id": "KB-005",
      "severity": "warning",
      "file": "02_Tasks/Specs/TASK-001.md",
      "location": "02_Tasks/Specs/TASK-001.md:4",
      "message": "Invalid date format '2026.11.19'. Expected ISO-8601 YYYY-MM-DD",
      "fixable": true
    }
  ]
}
```

### 3.2. SARIF 2.1.0 Объект `fixes`

В соответствии со спецификацией SARIF 2.1.0 (Section 3.55):
```python
if finding.fixable:
    result["fixes"] = [
        {
            "description": {
                "text": "Deterministic autofix available via 'kb_lint.py --fix --write'"
            }
        }
    ]
```

### 3.3. Обновление скилла `.agents/skills/kb-lint/SKILL.md`

```markdown
### Safe Auto-Fix Mode (--fix, --write)
- `python scripts/kb_lint.py --fix`: Safe Preview (Dry-Run). Shows colorized unified diff without modifying files.
- `python scripts/kb_lint.py --fix --write`: In-place atomic modification of safe rules (KB-004, KB-005, KB-006, KB-007, KB-010).
- `python scripts/kb_lint.py --fix --write --allow-dirty`: Force write even if Git working tree has unstaged edits.
```

### 3.4. Обновление скилла `.agents/skills/kb-complete/SKILL.md`

```markdown
8. **Run Knowledge Base Audit:**
   `python scripts/kb_lint.py --path docs`
   - If fixable frontmatter or whitespace warnings occur, resolve automatically:
     `python scripts/kb_lint.py --path docs --fix --write`
   - Confirm 0 broken links and 0 errors remain.
```

---

## 4. План верификации (Verification Plan)

- [ ] Синтаксическая компиляция: `python -m py_compile scripts/kb_lint.py` (Exit code 0).
- [ ] Контрактные тесты форматов: `python -m unittest tests/test_kb_lint_fix.py` (100% pass).
- [ ] Тесты существующих форматов вывода: `python -m unittest tests/test_kb_lint.py` (100% pass).
- [ ] Проверка бюджета размера скиллов: `python -m unittest tests/test_installer.py` (размер $\le 33000$ байт).
- [ ] Проверка базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links).

---

## 5. Критерии готовности (DoD)

- [ ] В `Finding` добавлено поле `fixable: bool`.
- [ ] В `render_json` и `render_sarif` интегрирован признак исправляемости `fixable` и объект `fixes`.
- [ ] Скиллы `.agents/skills/kb-lint/SKILL.md` и `.agents/skills/kb-complete/SKILL.md` дополнены инструкциями по автофиксу.
- [ ] Руководство `docs/Onboarding.md` обновлено.
- [ ] Все тесты верификационного плана пройдены со статусом `OK`.
- [ ] Статус задачи обновлён в Канбане (`Done`) и Дорожной карте (`[x]`).
- [ ] Запись добавлена в `Devlog.md`.
