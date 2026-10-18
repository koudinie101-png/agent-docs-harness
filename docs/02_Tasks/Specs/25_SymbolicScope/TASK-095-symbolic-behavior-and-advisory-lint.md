---
id: TASK-095
title: "Поведение Mode 2/3, advisory-контракт и state-aware next step"
status: done
type: task
phase: 25
component:
  - skills
  - lint
  - tests
parent_plan: "[[../../Plans/PLAN-024-symbolic-scope-and-task-contracts|PLAN-024]]"
created: 2026-10-18
updated: 2026-10-18
tags:
  - task/spec
  - phase25
  - symbolic-scope
  - skills
  - lint
  - tests
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-095 — Поведение Mode 2/3 и advisory-контракт

> **ID:** TASK-095 | **Статус:** Выполнено (Режим 3)  
> **Фаза:** 25 | **План:** [[../../Plans/PLAN-024-symbolic-scope-and-task-contracts|PLAN-024]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0029-fine-grained-task-symbol-contracts-and-line-drift-rejection|ADR-0029]], [[../../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]] (Tier 1 advisory), [[TASK-094-symbolic-contract-templates-and-source-guard|TASK-094]] (P2-находка)

---

## 1. Цель задачи

Замкнуть символьный контракт на уровне поведения агента и добавить механический контроль:

1. `/kb-task` требует вложенные символы для кодовых файлов и запрещает номера строк.
2. `/kb-implement` локализует код по именам символов, а не по номерам строк.
3. `scripts/kb_lint.py` получает неблокирующую `check_symbolic_scope()`: `WARN:` для активных задач с кодовым `[MODIFY]`/`[NEW]` без вложенного символа и для маркеров `:L10-L20`.
4. **P2-фикс `kb-complete`:** следующий шаг вычисляется по состоянию артефакта. `/kb-implement TASK-YYY` предлагается только если спека существует; иначе — `/kb-task TASK-YYY`. Это устраняет системную ошибку, обнаруженную при завершении TASK-094: скилл жёстко подставлял implement без проверки спеки.

**Вне скоупа:** шаблоны (TASK-094), пересборка `install.py` / `dist/install.py` и E2E (TASK-096), `SPEC.md` / `README.md` / `Onboarding.md` (TASK-096). Batch-режим подготовки спек всей фазы не реализуется — это отдельное решение уровня research/plan.

## 2. Затрагиваемые файлы и скоуп символов

* `[MODIFY]` `.agents/skills/kb-task/SKILL.md`:
  - Раздел `## 🚨 Constraints`, пункт `Exact Contracts`: символьный скоуп и запрет строк (§3.1).
* `[MODIFY]` `.agents/skills/kb-implement/SKILL.md`:
  - `Procedure` шаги 1 и 3: подтверждение символов и локализация по имени (§3.2).
* `[MODIFY]` `.agents/skills/kb-complete/SKILL.md`:
  - `Procedure` шаг 4 (Devlog) и объединённый шаг 10 (State-Aware Next Step) (§3.3).
* `[MODIFY]` `scripts/kb_lint.py`:
  - `check_symbolic_scope(docs_dir)`: новая advisory-проверка (§3.4).
  - `run_linter()`: вызов, verbose-блок и silent-строки (§3.4).
* `[MODIFY]` `tests/test_kb_lint.py`:
  - `TestKbLint._write_scope_spec()`: helper.
  - `TestKbLint.test_symbolic_scope_*()`: 6 тестов (§3.5).
* `[MODIFY]` `tests/test_installer.py`:
  - `TestAgentDocsHarness.test_symbolic_scope_and_state_aware_skill_guards()`: Tier 1 source-guard (§3.5).

## 3. Детали реализации

### 3.1. `/kb-task` — Exact Contracts

Заменить пункт `Exact Contracts` в `## 🚨 Constraints` на:

```markdown
* **Exact Contracts:** Mark changes as `[NEW]`, `[MODIFY]`, or `[DELETE]`; for code, name nested symbols (`Class.method()`), never line numbers (ADR-0029).
```

Требование к содержанию: для кодовых `[NEW]`/`[MODIFY]` — вложенный символ; `[DELETE]` и не-кодовые файлы — без символов.

### 3.2. `/kb-implement` — локализация по символу

1. В `Procedure` шаг 1 заменить `Confirm affected files and Verification Plan.` на:

```markdown
   - If `TASK-XXX`: read `docs/02_Tasks/Specs/<Phase>/TASK-XXX-<slug>.md`. Confirm affected files, symbols, and Verification Plan.
```

2. В шаге 3 (`For Tasks`) заменить пункт про файлы на:

```markdown
     * Modify and create only the files and symbols listed in section 2; locate code by symbol names, never by line numbers (ADR-0029).
```

### 3.3. `/kb-complete` — state-aware next step (P2)

1. В шаге 4 (Append Devlog) заменить жёсткий пример на generic:

```markdown
      * For tasks: `- **Рекомендуемый следующий шаг (Ожидает команды пользователя):** \`<next command>\`.`
```

2. Объединить шаги 10–11 в один шаг 10:

```markdown
10. **Next Step (State-Aware) & Stop & Yield:**
    - If all tasks in the current phase are `[x]`: recommend acceptance testing in `docs/05_Testing/` and `/kb-release <vX.Y.Z>`.
    - Else propose `/kb-implement TASK-YYY` only if its spec exists in `docs/02_Tasks/Specs/`; otherwise `/kb-task TASK-YYY`.
    - Render concise Anti-Echo summary (`[FileName](file://...)`, 3–5 bullets) and STOP.
```

Смысл: развилка кодируется не по намерению пользователя («пакет» vs JIT), а по состоянию артефакта. Если спеки всех задач существуют — implement уместен; если нет — task.

### 3.4. `check_symbolic_scope()` в `scripts/kb_lint.py`

Константы (рядом с `MEDIA_EXTENSIONS`):

```python
CODE_FILE_EXTENSIONS = {
    ".py", ".pyi", ".js", ".jsx", ".ts", ".tsx", ".swift", ".cs",
    ".go", ".rs", ".java", ".kt", ".rb", ".php",
    ".c", ".h", ".cpp", ".hpp", ".m", ".mm",
}
ACTIVE_SCOPE_STATUSES = {"planned", "in-progress", "in_progress"}
LINE_ANCHOR_RE = re.compile(
    r"(?:\b[\w./\\-]+\.\w+:L\d{1,5}\b|\bL\d{1,5}\s*[-–]\s*L?\d{1,5}\b)"
)
FILE_CONTRACT_RE = re.compile(r"^\s*[\*\-]\s*`?\[(NEW|MODIFY|DELETE)\]`?\s*`([^`]+)`")
NESTED_SYMBOL_RE = re.compile(r"^\s{2,}[\*\-]\s+\S")
```

Функция:

```python
def check_symbolic_scope(docs_dir: Path) -> List[str]:
    """Tier 1 (non-blocking): active task specs must name nested code symbols (ADR-0029)."""
```

Алгоритм:
* Сканировать `docs/02_Tasks/Specs/**/*.md` (fallback `docs/docs/...`), пропуская `TEMPLATE_*`.
* Разбирать frontmatter: `type` должен быть `task` (fast-track молчит), `status` ∈ `ACTIVE_SCOPE_STATUSES` (иначе `done`/`cancelled` молчат).
* Извлечь секцию 2: `^##\s+2\.[^\n]*\n([\s\S]*?)(?=^##\s|\Z)`; если секции нет — молчать.
* Для каждого `[MODIFY]`/`[NEW]` с расширением из `CODE_FILE_EXTENSIONS`:
  - сканировать последующие строки до следующего `FILE_CONTRACT_RE` или `## `;
  - если ни одна строка не матчит `NESTED_SYMBOL_RE` → `WARN: task '<file>' modifies code '<path>' without a nested symbol (ADR-0029)`.
* Если `LINE_ANCHOR_RE` найден в секции 2 → `WARN: task '<file>' uses line-number anchors (ADR-0029)` (один на файл).
* `[DELETE]`, не-кодовые расширения и вложенные символы не дают предупреждений.

Интеграция в `run_linter()`:
* `symbolic_warnings = check_symbolic_scope(docs_dir)` рядом с `research_warnings`.
* Verbose: блок `⚠️ Symbolic Scope Warnings (N):` со строками `   • {w}`.
* Silent: строки `⚠️  {w}` (как у `research_warnings`).
* В `has_errors` **не** добавлять — Exit code остаётся 0.

### 3.5. Тесты

**`tests/test_kb_lint.py`** — helper и 6 тестов (Silent-on-Success, Exit code 0):

```python
    def _write_scope_spec(self, name, section2, status="planned", spec_type="task"):
        spec = self.docs_dir / "02_Tasks" / "Specs" / f"{name}.md"
        spec.write_text(
            "---\n"
            f"id: {name}\n"
            "title: Scope Test\n"
            f"status: {status}\n"
            f"type: {spec_type}\n"
            "phase: 1\n"
            "parent_plan: PLAN-001\n"
            "created: 2026-10-01\n"
            "---\n"
            f"# {name}\n\n{section2}\n",
            encoding="utf-8",
        )
        return spec
```

| Тест | Вход | Ожидание |
| :--- | :--- | :--- |
| `test_symbolic_scope_missing_nested_symbol_warns` | `planned`, `[MODIFY]` `.py`, нет вложенного | `WARN`, Exit 0; verbose содержит `Symbolic Scope Warnings (1)` |
| `test_symbolic_scope_nested_symbol_passes` | `planned`, `[MODIFY]` `.py` + `  - \`Foo.bar()\`` | нет `without a nested symbol` |
| `test_symbolic_scope_done_task_is_silent` | `done`, без символа | молчит |
| `test_symbolic_scope_fast_track_is_silent` | `type: fast-track`, без символа | молчит |
| `test_symbolic_scope_line_anchor_warns` | `planned`, символ есть, в тексте `:L10-L20` | `line-number anchors`, Exit 0 |
| `test_symbolic_scope_non_code_file_is_silent` | `planned`, `[MODIFY]` `.md`, без символа | молчит |

**`tests/test_installer.py`** — один Tier 1 source-guard (читает файлы-источники, не бандл):

```python
    def test_symbolic_scope_and_state_aware_skill_guards(self):
        """Tier 1 (TASK-095): behavior wording must not be lost again."""
        root = REPO_ROOT / ".agents" / "skills"
        task_skill = (root / "kb-task" / "SKILL.md").read_text(encoding="utf-8")
        impl_skill = (root / "kb-implement" / "SKILL.md").read_text(encoding="utf-8")
        complete_skill = (root / "kb-complete" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("nested symbols", task_skill)
        self.assertIn("ADR-0029", task_skill)
        self.assertIn("symbol names", impl_skill)
        self.assertIn("ADR-0029", impl_skill)
        for marker in ("State-Aware", "only if its spec exists", "/kb-task TASK-YYY", "<next command>"):
            self.assertIn(marker, complete_skill, "kb-complete lost marker: %s" % marker)
```

### 3.6. Бюджет скиллов

Базовая линия: **30 654 B** по `tests/test_installer.py` (канонический LF-размер; мой прямой замер — 30 622 B). Лимит — 31 000 B.

* Фактический итог: **30 610 B** (−12 B к прямому замеру 30 622): `kb-task` +51 B, `kb-implement` +30 B, `kb-complete` −93 B (объединение шагов 10–11 и generic Devlog-шаблон).
* Лимит 31 000 B соблюдён; `test_16_high_snr_static_corpus_benchmarks` зелёный.

### 3.7. Совместимость

* Бандл не пересобирается: `install.py` / `dist/install.py` остаются прежними до TASK-096.
* `kb_lint` в этом репозитории после реализации не должен выдавать symbolic-предупреждений: TASK-095 — единственная активная спека, оформленная в новом формате.
* Исторические `done`-спеки не затрагиваются.

## 4. План верификации (Verification Plan)

- [x] Полный прогон (sandbox-safe, [[../../../06_Memory/Incidents/INC-003-dsh-sandbox-tempfile-mkdtemp-mode|INC-003]] / TRG-03): `python tmp/run_tests.py` → **162 теста OK**, Exit code 0 (6 новых lint + 1 source-guard).
- [x] Точечный source-guard (без tempfile): `python -m unittest tests.test_installer.TestAgentDocsHarness.test_symbolic_scope_and_state_aware_skill_guards` → OK.
- [x] Синтаксис: `python -m py_compile scripts/kb_lint.py tests/test_kb_lint.py tests/test_installer.py` → Exit code 0.
- [x] Бюджет скиллов: прямой канонический замер **30 610 B** (≤ 31 000; −12 B к 30 622); `test_16` зелёный.
- [x] Целостность: `python scripts/kb_lint.py --path docs` → Exit code 0, 0 битых ссылок, 0 `Symbolic Scope Warnings`.
- [x] 4-State UI / скриншоты: не применимо (GUI/TUI отсутствует).
- [x] Замеры $\ge 3$ прогонов: не применимо — статический байтовый бюджет детерминирован.

## 5. Критерии готовности (DoD)

- [x] Три скилла обновлены; Tier 1 source-guard зелёный.
- [x] `check_symbolic_scope()` реализована, интегрирована в `run_linter()` и покрыта 6 тестами.
- [x] `kb-complete` предлагает implement только при существующей спеке; Devlog-шаблон больше не хардкодит `/kb-implement`.
- [x] `kb_lint` в репозитории: 0 битых ссылок и 0 symbolic-предупреждений.
- [x] Полный suite зелёный (162 теста); бюджет скиллов 30 610 B ≤ 31 000 B.
- [x] Статус задачи обновлён в [[../../Kanban|Kanban]] и [[../../Roadmap|Roadmap]] на шаге `/kb-complete`.
