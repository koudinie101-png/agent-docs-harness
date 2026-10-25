---
id: TASK-101
title: "Модель Finding, реестр KB-XXX и машинно-читаемые форматы линтера"
status: done
type: task
phase: 27
component:
  - lint
  - contracts
  - adr
parent_plan: "[[../../Plans/PLAN-025-docs-integrity-gate-kb-lint-productization|PLAN-025]]"
created: 2026-10-25
updated: 2026-10-25
tags:
  - task/spec
  - phase27
  - lint
  - contracts
  - ci
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-101 — Модель Finding, реестр KB-XXX и форматы вывода

> **ID:** TASK-101 | **Статус:** Выполнено (Режим 3)  
> **Фаза:** 27 | **План:** [[../../Plans/PLAN-025-docs-integrity-gate-kb-lint-productization|PLAN-025]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../04_Research/RESEARCH-027-competitor-best-practices-and-adoption-backlog|RESEARCH-027]] (§4 Волна 1 п.1, §5.1); ADR-0032 (создаётся этой задачей)  
> **Следующая задача фазы:** `TASK-102` (контрактные тесты) — блокирует релиз Фазы 27, но не эту задачу

---

## 1. Цель задачи

Заменить «печать строк» на «построение находок» в `scripts/kb_lint.py`: 15 `check_*`-функций начинают возвращать `List[Finding]`, из одного и того же набора находок собираются три вывода — `text` (байт-в-байт как сегодня), `json` (контракт `version: 1`) и `sarif` (2.1.0), плюс добавляются флаги `--format {text,json,sarif}` и `--version`.

Задача **не добавляет ни одной новой проверки**: меняется только форма результата и точка рендеринга. Это фундамент для `KB-010` (`depends_on`), right-sizing-предупреждений и CI-упаковки — они все будут эмитить находки через тот же реестр.

Жёсткий инвариант: **60 существующих тестов `tests/test_kb_lint.py` остаются зелёными без правки ассертов.** Если текст разошёлся — чинится рендерер, а не тест.

## 2. Затрагиваемые файлы и скоуп символов

* `[MODIFY]` `scripts/kb_lint.py`:
  - `Finding` — новая неизменяемая структура находки (`NamedTuple`, Python 3.8, Zero-Deps).
  - `RULES`, `RULE_SEVERITY` — новые константы-реестры правил `KB-001…KB-015`.
  - `make_finding(rule_id: str, message: str, file: str = "", severity: Optional[str] = None) -> Finding` — новый конструктор, валидирующий `rule_id` по реестру.
  - `LintReport` — новая структура отчёта (`files`, `wikilinks`, `findings`).
  - `render_text(report: LintReport, verbose: bool) -> str`, `render_json(report: LintReport) -> str`, `render_sarif(report: LintReport) -> str` — новые рендереры; `run_linter` только печатает их результат.
  - `run_linter(docs_dir: Path, verbose: bool = False, output_format: str = "text") -> int` — точка сборки отчёта и выбора рендерера; цикл обхода ссылок эмитит `KB-001`.
  - `check_file_frontmatter(file_path: Path) -> Tuple[bool, str]` — сигнатура **не меняется** (возвращает признак + текст), обёртка в `KB-002` делается вызывающим кодом.
  - `check_spec_drift`, `check_devlog_semantic_guard`, `check_fast_track_specs`, `check_phase_consistency`, `check_memory_limits`, `check_memory_consistency`, `check_research_basis`, `check_symbolic_scope`, `check_asset_weights`, `check_asset_layout`, `check_tech_debt_integrity`, `check_untracked_todos` — все меняют тип возврата `List[str]` → `List[Finding]`.
  - блок `if __name__ == "__main__"` — новые аргументы `--format` и `--version`.
* `[MODIFY]` `tests/test_kb_lint.py`:
  - правок ассертов нет; допускается только добавление недостающего импорта, если сигнатуры вызываются напрямую (проверить перед правкой).
* `[NEW]` `docs/03_Decisions_ADR/ADR-0032-machine-readable-lint-contract-and-rule-registry.md`:
  - `ADR-0032`: контекст (линт отдаёт только текст), решение (Finding + реестр + три рендерера), отклонённые альтернативы (§3.7), последствия (`DEBT-004`).
* `[MODIFY]` `docs/02_Tasks/TechDebt.md`:
  - `DEBT-004`: уточнить формулировку — локации без `region.startLine`, а не «файл вместо строки» (сделано при планировании; при реализации сверить с фактическим поведением).

## 3. Детали реализации

### 3.1. Модель находки и реестр

```python
class Finding(NamedTuple):
    rule_id: str          # "KB-001" … "KB-015"
    severity: str         # "error" | "warning"
    file: str             # docs-relative POSIX или имя корневого дока; "" если находка глобальная
    message: str          # текст ровно как печатается сегодня (legacy-префикс "WARN:" сохраняется)

RULES: Dict[str, str] = {          # rule_id -> короткое описание (SARIF shortDescription)
    "KB-001": "Broken or unresolved wikilink or markdown link",
    "KB-002": "Missing or invalid YAML frontmatter",
    "KB-003": "Procedural memory limit exceeded",
    "KB-004": "Tech debt registry integrity",
    "KB-005": "Asset layout violation",
    "KB-006": "Phase consistency mismatch",
    "KB-007": "Missing research basis for a plan",
    "KB-008": "Devlog next-step semantics",
    "KB-009": "Untracked TODO/FIXME comment",
    "KB-010": "Task dependency cycle or unknown dependency",   # ЗАРЕЗЕРВИРОВАН: не эмитится
    "KB-011": "Living Spec drift",
    "KB-012": "Fast-track scope or budget violation",
    "KB-013": "Memory index consistency",
    "KB-014": "Symbolic scope contract violation",
    "KB-015": "Asset weight budget exceeded",
}
RULE_SEVERITY: Dict[str, str] = {...}   # KB-001/002/003/004 — "error", остальные — "warning"
```

* `make_finding(...)`: `rule_id` отсутствует в `RULES` → `ValueError("Unknown lint rule: <id>")` (ошибка программиста, не пользователя); `severity` не в `{"error", "warning"}` → `ValueError`; при `severity=None` берётся `RULE_SEVERITY[rule_id]`.
* **Нумерация фиксирована** (RESEARCH-027 §5.1 + `Roadmap.md`): `KB-001…KB-010` не перенумеровываются. `KB-010` присутствует в реестре, но ни один `check_*` его не возвращает — иначе линт разойдётся с Roadmap.
* **Сообщения не нормализуются.** `message` остаётся дословно тем, что печатается сегодня (включая legacy-префикс `WARN:` у части проверок). JSON-потребитель опирается на `severity`, а не на текст. Причина: нормализация изменила бы text-вывод и потребовала бы переписать ассерты — это отдельная задача, не эта.

### 3.2. Отчёт и рендеринг

```python
class LintReport(NamedTuple):
    files: int
    wikilinks: int
    findings: List[Finding]
```

* `render_text(report, verbose)` — **единственный** источник text-вывода; воспроизводит текущие секции и их порядок (verbose: файлы → ссылки → frontmatter → память → drift → devlog → fast-track → фазы → research → symbolic → веса ассетов → топология ассетов → долг (warnings) → долг (errors) → TODO; silent: только warnings в текущем порядке, затем `OK:`/`ERROR:`), включая эмодзи, отступы `   • `, пустые строки и условные `✅`-заглушки. Секции строятся из находок фильтром по `rule_id` (+ `severity` для `KB-004`).
* `render_json(report)` — `json.dumps(..., indent=2, ensure_ascii=False)` (стиль как в `kb_release.py`):

```json
{
  "version": 1,
  "summary": {"files": 252, "wikilinks": 2477, "errors": 0, "warnings": 0},
  "errors": [{"rule_id": "KB-001", "severity": "error", "file": "docs/x.md", "message": "..."}],
  "warnings": []
}
```

  * `version` — версия **схемы**, не релиза. `file` — `null`, если находка глобальная.
  * Порядок детерминированный: сначала `errors`, затем `warnings`; внутри — сортировка по `(rule_id, file, message)`.
* `render_sarif(report)` — SARIF 2.1.0, минимально достаточный:

```json
{
  "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
  "version": "2.1.0",
  "runs": [{
    "tool": {"driver": {"name": "kb_lint", "version": "1",
                        "rules": [{"id": "KB-001", "shortDescription": {"text": "..."}}]}},
    "results": [{"ruleId": "KB-001", "level": "error", "message": {"text": "..."},
                 "locations": [{"physicalLocation": {"artifactLocation": {"uri": "docs/x.md"}}}]}]
  }]
}
```

  * `rules[]` — только фактически встреченные правила (не весь реестр); каждый `ruleId` результата обязан присутствовать в `rules[]`.
  * `level`: `error` → `"error"`, `warning` → `"warning"`. Находки без `file` публикуются **без** `locations` (SARIF это допускает).
  * `informationUri` **не заполняется**: установленная копия линта не должна выдавать происхождение проекта (прецедент утечки метаданных — BUG-009).
  * `region.startLine` не заполняется — линтер не считает строки (см. `DEBT-004`); фиктивная строка 1 запрещена.

### 3.3. CLI

* `--format {text,json,sarif}`, default `text`; `--version` — печатает `kb_lint 1` (версия набора правил) и завершается с кодом 0, не выполняя скан.
* При `output_format != "text"` на stdout попадает **только** документ: подавляются `🔍 Auditing…`, `OK:`-строка, `--verbose`-блоки. `--verbose` в машинных режимах — задокументированный no-op (не ошибка парсера).
* Exit-коды неизменны и не зависят от формата: `0` при отсутствии `error`-находок, `1` при их наличии, `1` при несуществующем каталоге (существующее поведение, сообщение остаётся в `stderr`).

### 3.4. Миграция проверок

* Каждая `check_*` заменяет `warnings.append("...")` на `findings.append(make_finding("KB-0XX", "...", file=<rel>))`, сохраняя порядок и текст сообщений.
* `file` заполняется там, где проверка уже знает путь (все проверки, итерирующие файлы); глобальные находки (например, `Tech debt registry not found`) — `file=""`.
* Спецлогика `KB-004` в `run_linter` сохраняется: `debt_errors` = находки с `severity=="error"`, `debt_warnings` = `severity=="warning"` при условии «не `Tech debt registry not found` **или** harness-файлы найдены» (текущее поведение, TASK-075).
* Спецлогика `startswith("WARN:")` в silent-ветке **удаляется**: роль префикса больше не нужна, потому что `severity` известен заранее, а сам префикс уже содержится в `message` там, где он печатался раньше.

### 3.5. ADR-0032

Создать по `TEMPLATE_ADR.md` (`status: accepted`, `date`/`created` по схеме frontmatter ADR): контекст (текстовый вывод, 74 `print()`, нет rule-id), решение (Finding + реестр + три рендерера, `KB-010` зарезервирован), последствия (`--fix`/CI-упаковка отложены, `DEBT-004`), отклонённые альтернативы: парсинг строк регулярками, гибрид «строки + находки», отдельный `kb_lint_json.py`, `line`/`fixable` «на будущее», SARIF с `startLine: 1`, `jsonschema` (ADR-0001), хардкод релизной версии в `--version`.

## 4. План верификации (Verification Plan)

- [x] Компиляция: `python -m py_compile scripts/kb_lint.py` → Exit code 0.
- [x] Полный набор тестов: `python -m unittest discover -s tests` → 0 failures/errors; **`git diff tests/test_kb_lint.py` пуст** (ассерты не правились).
- [x] Паритет text (silent): `python scripts/kb_lint.py --path docs` → ровно одна строка `OK: <N> files scanned, <M> wikilinks verified (0 broken).`, Exit 0.
- [x] Паритет text (verbose): `python scripts/kb_lint.py --path docs --verbose` → те же секции и порядок, что до правки; в выводе нет `WARN`, `❌`, `⚠️`.
- [x] JSON-контракт: `python scripts/kb_lint.py --path docs --format json > tmp/kb_lint.json` → `python -c "import json; d=json.load(open('tmp/kb_lint.json',encoding='utf-8')); print(d['version'], sorted(d), d['summary'])"` → `1 ['errors','summary','version','warnings'] {'files': N, …}`; повторный разбор stdin-вариантом (`| python -c ...`) подтверждает, что stdout не содержит ничего, кроме JSON.
- [x] SARIF-контракт: `python scripts/kb_lint.py --path docs --format sarif > tmp/kb_lint.sarif` → `python -c "import json; d=json.load(open('tmp/kb_lint.sarif',encoding='utf-8')); r=d['runs'][0]; ids={x['id'] for x in r['tool']['driver']['rules']}; assert d['version']=='2.1.0' and all(x['ruleId'] in ids for x in r['results'])"` → без `AssertionError`.
- [x] Error-путь: во временном хранилище `tmp/lint_probe/` (gitignored) с одной битой ссылкой: `--format json` → `summary.errors == 1`, `errors[0].rule_id == "KB-001"`, Exit code 1; `--format text` → прежний блок `ERROR:`.
- [x] Exit-код `--version`: `python scripts/kb_lint.py --version` → `kb_lint 1`, Exit 0.
- [x] Отсутствие регрессий реестра: `python -c "import sys; sys.path.insert(0,'scripts'); import kb_lint as k; assert len(k.RULES)==15; assert 'KB-010' in k.RULES and 'KB-010' not in k.RULE_SEVERITY"` → без `AssertionError` (`KB-010` присутствует в реестре и не имеет severity, потому что не эмитится).
- [x] `python scripts/kb_lint.py --path docs` (после создания ADR-0032 и спеки) → 0 битых ссылок.

* **Замеры $\ge 3$ прогонов (без холодного старта):** производительность не заявляется; если фиксируется время `--format json`, то 3 прогона с командой и средним в Devlog (правило 16 `AGENTS.md`).

### Visual DoD (для задач с GUI/TUI):

Поверхность — терминальный вывод. Макеты не нужны (раскладка не меняется). Скриншот-слот: `![Скриншот](../../assets/screenshots/kb_lint/TASK-101.png) <!-- вывод --format json/sarif; в headless — ASCII-снимок в Devlog -->`

## 5. Критерии готовности (DoD)

- [x] Код написан строго по ТЗ без заглушек; `Finding` — единственная форма результата (в файле не осталось `check_*`, возвращающих строки).
- [x] `git diff tests/test_kb_lint.py` пуст: 60 тестов зелёные **без** правки ассертов.
- [x] Text-вывод совпадает с эталоном до правки (silent и verbose), включая порядок секций и эмодзи.
- [x] `--format json` и `--format sarif` дают по одному валидному документу; stdout не содержит посторонних строк.
- [x] Реестр: 15 правил, `KB-010` зарезервирован и не эмитится.
- [x] `ADR-0032` создан (`status: accepted`) и содержит отклонённые альтернативы §3.5.
- [x] Все пункты Плана верификации пройдены; бюджет `install.py` **не проверяется в этой задаче** (пересборка и `test_16` — `TASK-103`).
- [ ] Living Spec (`SPEC.md`, `README.md`, `Onboarding.md`) — `TASK-103` по плану Фазы 27; в этой задаче публичный контракт фиксируется только в ADR-0032.
- [x] Статус обновлён в ТЗ (`Выполнено`), Канбане (`Done`), Дорожной карте (`[x]`); запись в `Devlog.md` — на шаге `/kb-complete`.

## 6. Отклонения при реализации (2026-10-25)

* **`Finding` реализован как подкласс `str`, а не `NamedTuple`** (отклонение от §3.1). Причина: `check_*` вызываются напрямую в **75** местах `tests/test_kb_lint.py` и сравниваются как строки (`assertIn("...", warnings[0])`, `assertEqual(..., [])`). `NamedTuple` потребовал бы править ассерты — прямое нарушение DoD этой задачи и обратной совместимости вспомогательного API, которым пользуются установленные проекты. Модель: `Finding(str)` с `__slots__ = ("rule_id", "severity", "file")` и свойством `message`; JSON/SARIF читают атрибуты, text-рендерер печатает `str(finding)`. Решение зафиксировано в [[../../../03_Decisions_ADR/ADR-0032-machine-readable-lint-contract-and-rule-registry|ADR-0032]] §2–§3.
* **`file` заполняется для всех 14 эмитящих правил**, а не только для однофайловых: обёртка `make_finding(..., file=...)` применена в 28 точках эмиссии; `KB-013` и `KB-004` дополнительно получают имя своего файла (patterns/incidents/TechDebt/план). Поэтому `DEBT-004` остаётся только про отсутствие `region.startLine`.
* **`by_rule_severity()`** добавлен в `LintReport` как вспомогательный селектор для JSON/SARIF (в §3.2 не перечислялся).
* **Паритет text-вывода подтверждён байт-в-байт:** старый (`git show HEAD:scripts/kb_lint.py`) и новый скрипт дают идентичный stdout в silent и verbose на реальном репозитории; `git diff tests/` пуст, 166 тестов репозитория зелёные.
