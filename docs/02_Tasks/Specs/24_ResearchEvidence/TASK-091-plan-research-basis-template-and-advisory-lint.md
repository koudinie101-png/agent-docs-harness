---
id: TASK-091
title: "research_basis/basis_note и секция Research Basis в TEMPLATE_PLAN.md, неблокирующий check_research_basis() в kb_lint"
status: done
type: task
phase: 24
component:
  - templates
  - lint
  - tests
parent_plan: "[[../../Plans/PLAN-023-research-evidence-gate-and-plan-provenance|PLAN-023]]"
created: 2026-10-18
updated: 2026-10-18
tags:
  - task/spec
  - phase24
  - research-evidence
  - templates
  - lint
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-091 — Поле `research_basis` и advisory-контроль в `kb_lint.py`

> **ID:** TASK-091 | **Статус:** Выполнено (Режим 3)  
> **Фаза:** 24 | **План:** [[../../Plans/PLAN-023-research-evidence-gate-and-plan-provenance|PLAN-023]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0031-research-evidence-gate-for-icebox-promotion|ADR-0031]] (R3, R4), [[../../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]] (advisory Tier 1), [[../../../04_Research/RESEARCH-025-research-evidence-gate-for-icebox-promotion|RESEARCH-025]] §2.3–2.4  
> **Предшествующая задача:** [[TASK-090-evidence-status-nudge-and-tier2-rule|TASK-090]] (Nudge и Tier 2 правило)

---

## 1. Цель задачи

Сделать доказательную базу плана **явной и durable** в артефакте, а не в чате, и получить дешёвый неблокирующий контроль:

1. **R3:** во frontmatter `TEMPLATE_PLAN.md` — закомментированные подсказки `research_basis` / `basis_note`; в секции Q&A — `### Research Basis & Unvalidated Assumptions` (известно / не проверено / как закрываем). Обе копии шаблона: `docs/00_Templates/TEMPLATE_PLAN.md` и `templates/TEMPLATE_PLAN.md`.
2. **R4:** `check_research_basis(docs_dir)` в `scripts/kb_lint.py` выдаёт `WARN:` (не `ERROR`), если `research_basis` присутствует, нормализуется в `none` и `basis_note` пуст. Поле отсутствует — предупреждения нет (обратная совместимость с 23 существующими планами).
3. 4 модульных теста в `tests/test_kb_lint.py`, включая интеграцию через `run_linter()` с `Exit code 0`.

**Вне скоупа:** обязательность поля (в `schemas` `02_Tasks/Plans` **не добавляется**); ретроактивное заполнение старых планов; синхронизация копий `TEMPLATE_INDEX.md` и parity-тест ([[TASK-092-template-copies-parity-sync-and-test|TASK-092]]); пересборка бандла и E2E установленного артефакта ([[TASK-093-bundle-rebuild-e2e-and-living-spec-sync|TASK-093]]).

## 2. Затрагиваемые файлы

* `[MODIFY]` `docs/00_Templates/TEMPLATE_PLAN.md` — подсказки `research_basis`/`basis_note` + секция `### Research Basis & Unvalidated Assumptions`.
* `[MODIFY]` `templates/TEMPLATE_PLAN.md` — **те же** изменения дословно (это источник бандла; расхождение копий устраняется в [[TASK-092-template-copies-parity-sync-and-test|TASK-092]] для 4-State Matrix, но новую секцию обе копии получают уже здесь).
* `[MODIFY]` `scripts/kb_lint.py` — `check_research_basis()`, хелпер нормализации значения, интеграция в `run_linter()` (verbose + silent-on-success), без изменения `has_errors`.
* `[MODIFY]` `tests/test_kb_lint.py` — 4 теста: `none` без заметки, `none` с заметкой (+ inline-комментарий), ссылка на исследование, отсутствующее поле.

## 3. Детали реализации

### 3.1. Frontmatter шаблона (обе копии)

Сразу после строки `phase: 1` добавить **комментированные** строки (активные значения не выставляются — шаблон не навязывает `none` каждому новому плану):

```yaml
# research_basis: "[[../../04_Research/RESEARCH-XXX-<slug>|RESEARCH-XXX]]"  # or: none
# basis_note: "Почему исследование не требуется и насколько решение обратимо (обязательно при research_basis: none)"
```

Почему комментарии: активный `research_basis: none` навсегда порождал бы `WARN:` у каждого свежего плана (шум, привыкание к предупреждениям — отклонено в PLAN-023 Q3).

### 3.2. Секция плана (обе копии)

Вставить между `## 2. Обсуждение и решения (Q&A)` и `## 3. Архитектурное влияние и риски`:

```markdown
### Research Basis & Unvalidated Assumptions
* **Известно (проверено):** <!-- факты, инспекция кода, замеры -->
* **Не проверено (гипотезы):** <!-- допущения и их влияние на план -->
* **Как закрываем:** <!-- spike / TASK-XXX / метрика; при research_basis: none — строка об обратимости -->
```

### 3.3. `check_research_basis(docs_dir: Path) -> List[str]`

```python
RESEARCH_BASIS_RE = re.compile(r"^research_basis:\s*(.*)$", re.MULTILINE)
BASIS_NOTE_RE = re.compile(r"^basis_note:\s*(.*)$", re.MULTILINE)


def _normalize_plan_value(raw):
    """Strip quotes, inline comments and surrounding whitespace."""
    value = raw.strip().split("#", 1)[0].strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1].strip()
    return value


def check_research_basis(docs_dir: Path) -> List[str]:
    warnings = []
    plans_dir = docs_dir / "02_Tasks" / "Plans"
    if not plans_dir.is_dir() and (docs_dir / "docs" / "02_Tasks" / "Plans").is_dir():
        plans_dir = docs_dir / "docs" / "02_Tasks" / "Plans"
    if not plans_dir.is_dir():
        return warnings

    for plan_file in sorted(plans_dir.rglob("*.md")):
        if plan_file.name.startswith("TEMPLATE_"):
            continue
        try:
            text = plan_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if not text.startswith("---"):
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        frontmatter = parts[1]

        basis_match = RESEARCH_BASIS_RE.search(frontmatter)
        if not basis_match:
            continue  # поле отсутствует -> молчим (обратная совместимость)
        if _normalize_plan_value(basis_match.group(1)).lower() != "none":
            continue  # ссылка на RESEARCH/ADR -> доказательная база объявлена

        note_match = BASIS_NOTE_RE.search(frontmatter)
        note = _normalize_plan_value(note_match.group(1)) if note_match else ""
        if not note:
            warnings.append(
                "WARN: plan '%s' sets research_basis: none without basis_note" % plan_file.name
            )
    return warnings
```

Контракт:
* Сканируются только `02_Tasks/Plans/**/*.md`, файлы `TEMPLATE_*` пропускаются.
* `research_basis` с пустым значением `""` **не** приравнивается к `none` (нет явного утверждения) — предупреждения нет.
* `basis_note` должен быть непустым после нормализации: `""`, `''`, `# comment` → пусто.
* Формат предупреждения фиксирован (проверяется в тестах): `WARN: plan '<file>.md' sets research_basis: none without basis_note`.
* Пути — только `pathlib.Path`; чтение с `encoding="utf-8", errors="replace"` (Windows-совместимость, [[../../../06_Memory/patterns.md|TRG-01]]).

### 3.4. Интеграция в `run_linter()`

* После `phase_warnings = check_phase_consistency(docs_dir)` добавить `research_warnings = check_research_basis(docs_dir)`.
* Verbose: после блока `Phase Consistency Warnings`:

```python
if research_warnings:
    print(f"⚠️ Research Basis Warnings ({len(research_warnings)}):")
    for rw in research_warnings:
        print(f"   • {rw}")
    print()
```

* Silent-on-success: после цикла `phase_warnings` печатать `⚠️  {rw}` (как `memory_warnings`, с обработкой префикса `WARN:`).
* `has_errors` **не** включает `research_warnings`; `ERROR:`-счётчик не меняется → Exit code остаётся 0 (прецедент `debt_warnings`, `check_memory_consistency`).

### 3.5. Тесты в `tests/test_kb_lint.py`

Хелпер в классе `TestKbLint`:

```python
def _write_plan(self, name, frontmatter):
    plans_dir = self.docs_dir / "02_Tasks" / "Plans"
    plans_dir.mkdir(parents=True, exist_ok=True)
    (plans_dir / name).write_text("---\n%s\n---\n# Plan\n" % frontmatter, encoding="utf-8")
```

| Тест | Вход | Ожидание |
| :--- | :--- | :--- |
| `test_check_research_basis_none_without_basis_note` | `research_basis: none` | ровно 1 `WARN`, текст совпадает с §3.3; `run_linter()` → Exit code **0**, `WARN` в выводе |
| `test_check_research_basis_none_with_basis_note` | `research_basis: none  # reversible` + `basis_note: "..."` | `[]`, `run_linter()` без `Research Basis` |
| `test_check_research_basis_research_link_is_clean` | `research_basis` = викиссылка на `RESEARCH-025` в кавычках | `[]` |
| `test_check_research_basis_absent_field_is_silent` | frontmatter без поля | `[]`, `run_linter()` без `WARN` |

Тест 1 обязан проверять именно Exit code 0 (advisory-инвариант), а не только текст функции — иначе регресс в `has_errors` пройдёт незамеченным.

## 4. План верификации (Verification Plan)

- [x] Новые тесты: `tests.test_kb_lint` — **54 теста OK** (50 + 4 новых, регрессий нет; sandbox-safe прогон через `tmp/run_task091_tests.py`).
- [x] Полный прогон (sandbox-safe, [[../../../06_Memory/Incidents/INC-003-dsh-sandbox-tempfile-mkdtemp-mode|INC-003]] / TRG-03): `python tmp/run_tests.py` → **151 тест OK**, Exit code 0.
- [x] Чистый репозиторий: `python scripts/kb_lint.py --path docs --verbose` → Exit code 0, блок `Research Basis Warnings` **отсутствует** (`PLAN-022` имеет `basis_note`, `PLAN-023` — ссылку на `RESEARCH-025`).
- [x] Негативная ручная проверка: временный `PLAN-001-negative.md` (`research_basis: none`) в `tmp/neg091/` → `--verbose` печатает `Research Basis Warnings (1)` и `WARN: plan '...' sets research_basis: none without basis_note`, Exit code **0**; каталог удалён.
- [x] Компиляция: `python -m py_compile scripts/kb_lint.py` → Exit code 0.
- [x] Бюджет шаблонов: **28 599 байт** ≤ 30 000 (запас 1 401); лимит теста не менялся.
- [x] 4-State UI / скриншоты: не применимо (нет GUI/TUI).
- [x] Замеры $\ge 3$ прогонов: не применимо (нет изменений производительности).

## 5. Критерии готовности (DoD)

- [x] `research_basis` и `basis_note` задокументированы (закомментированы) в обеих копиях `TEMPLATE_PLAN.md`.
- [x] Секция `Research Basis & Unvalidated Assumptions` присутствует в обеих копиях шаблона.
- [x] `check_research_basis()` возвращает только строки `WARN:` и не влияет на Exit code.
- [x] Покрыты 4 сценария §3.5, включая интеграцию `run_linter()` с Exit code 0.
- [x] `02_Tasks/Plans` **не** добавлен в `schemas` обязательных полей.
- [x] Существующие 23 плана не порождают предупреждений.
- [x] Статус задачи обновлён в [[../../Kanban|Kanban]] и [[../../Roadmap|Roadmap]] на шаге `/kb-complete`.
