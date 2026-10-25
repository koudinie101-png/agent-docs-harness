---
id: TASK-102
title: "Контрактные тесты машинно-читаемого вывода линтера (json/sarif)"
status: in-progress
type: task
phase: 27
component:
  - lint
  - tests
parent_plan: "[[../../Plans/PLAN-025-docs-integrity-gate-kb-lint-productization|PLAN-025]]"
created: 2026-10-25
updated: 2026-10-25
tags:
  - task/spec
  - phase27
  - lint
  - tests
  - contracts
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-102 — Контрактные тесты машинно-читаемого вывода

> **ID:** TASK-102 | **Статус:** К реализации (Режим 2)  
> **Фаза:** 27 | **План:** [[../../Plans/PLAN-025-docs-integrity-gate-kb-lint-productization|PLAN-025]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Предыдущая задача:** [[27_DocsIntegrity/TASK-101-finding-model-rule-registry-and-formats|TASK-101]] — реализовала `Finding`, реестр и рендереры  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0032-machine-readable-lint-contract-and-rule-registry|ADR-0032]], [[../../../04_Research/RESEARCH-027-competitor-best-practices-and-adoption-backlog|RESEARCH-027]]  
> **Техдолг фазы:** `DEBT-004` (SARIF без `region.startLine`), `DEBT-005` (sandbox-обёртка тестов)

---

## 1. Цель задачи

Закрепить машинно-читаемый контракт линтера Tier 1-тестами: реестр правил, схема JSON (`version: 1`), структура SARIF 2.1.0 и перекрёстные ссылки `ruleId → rules[]`, неизменность exit-кодов, «чистый stdout» в машинных режимах, no-op `--verbose`, `--version`.

Задача **не меняет продакшн-код**: `scripts/kb_lint.py` зафиксирован в TASK-101. Если контрактный тест вскроет дефект — он оформляется как `BUG-XXX` (Режим 2B → Режим 3, TDD), а не правится молча в этой задаче.

### 1.1. Что именно проверяется (и что нет)

| Слой | Проверяется механически | Не проверяется |
| :--- | :--- | :--- |
| Реестр | 15 ID, уникальность, `RULE_SEVERITY ⊆ RULES`, `KB-010` без severity и с запретом эмиссии | Семантика описаний правил |
| JSON | Точный набор ключей верхнего уровня, `version == 1`, типы `summary`, `file` = `null` для глобальных находок | Стабильность **порядка** находок между версиями (сортировка внутри — деталь реализации, но проверяется как детерминизм двух прогонов) |
| SARIF | `2.1.0`, `$schema`, `runs[0].tool.driver.{name,version,rules}`, `ruleId ∈ rules[]`, `level`, `locations` при наличии файла | Соответствие официальной JSON-схеме OASIS (нет `jsonschema` в Zero-Deps — см. §1.2) |
| CLI | Exit-коды `0/1` во всех трёх форматах, «stdout = один документ», `--version` | Совместимость с `curl | python` и прочие сценарии установки |

### 1.2. Про приёмку SARIF в GitHub Code Scanning

План Фазы 27 (PLAN-025 §4, TASK-102) упоминал «ручную проверку SARIF в Code Scanning». **В этой задаче она невозможна**: в репозитории нет ни `action.yml`, ни workflow, загружающего SARIF, а Code Scanning принимает результат только через `upload-sarif`. Отсюда решение:

* сейчас — **структурные** тесты SARIF + документ проверяется на инварианты «своими руками» (`runs/results/rules`, отсутствие `region` с фиктивной строкой);
* приёмка в Code Scanning переносится в фазу CI-упаковки (Icebox, Волна 1: `action.yml`/pre-commit) и **не заявляется** в DoD этой задачи;
* валидация официальной JSON-схемой не выполняется ([[../../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]), о чём честно сказано в ADR-0032 §2 и §4.

Это не сокращение объёма, а перенос точки проверки в фазу, где появится потребитель.

## 2. Затрагиваемые файлы и скоуп символов

* `[MODIFY]` `tests/test_kb_lint.py`:
  - `TestLintOutputContract.setUp()` — минимальное хранилище с одним валидным документом (переиспользовать паттерн `TestKbLint.setUp`, без копирования 30 строк: вынести общий хелпер внутрь нового класса).
  - `TestLintOutputContract._run_cli(*args)` — хелпер subprocess-запуска `scripts/kb_lint.py` с `sys.executable`, `encoding="utf-8"`, возвращает `(returncode, stdout)`.
  - `TestLintOutputContract.test_rule_registry_is_complete_and_unique()` — инвентарь реестра.
  - `TestLintOutputContract.test_make_finding_rejects_unknown_rule()` — `ValueError`.
  - `TestLintOutputContract.test_make_finding_rejects_reserved_rule()` — `KB-010` → `ValueError`.
  - `TestLintOutputContract.test_finding_keeps_message_string_contract()` — `isinstance(f, str)`, `f == f.message`, атрибуты `rule_id`/`severity`/`file`.
  - `TestLintOutputContract.test_json_contract_on_clean_vault()` — ключи, `version`, типы `summary`, пустые массивы.
  - `TestLintOutputContract.test_json_reports_broken_link_as_kb_001()` — `errors[0]` полностью: `rule_id`, `severity`, `file`, `message`.
  - `TestLintOutputContract.test_json_stdout_contains_only_document()` — subprocess, `json.loads(stdout)` без предварительной очистки.
  - `TestLintOutputContract.test_json_verbose_flag_is_noop()` — `--format json --verbose` парсится, строки `Auditing`/`OK:` отсутствуют.
  - `TestLintOutputContract.test_sarif_contract_structure()` — версия, `$schema`, driver, `ruleId ∈ rules[]`, `level`, `locations`.
  - `TestLintOutputContract.test_sarif_empty_results_on_clean_vault()` — `runs[0].results == []`, `rules` может быть пустым списком.
  - `TestLintOutputContract.test_exit_codes_consistent_across_formats()` — warning-only хранилище → `0` во всех трёх форматах; error-хранилище → `1` во всех трёх.
  - `TestLintOutputContract.test_version_flag()` — `kb_lint 1`, Exit 0.
* `[MODIFY]` `docs/02_Tasks/TechDebt.md`:
  - `DEBT-004`: дополнить ссылкой на тест-политику (SARIF проверяется структурно, `region` отсутствует намеренно).
* Продакшн-код (`scripts/kb_lint.py`, `install.py`, `dist/install.py`) **не изменяется**.

## 3. Детали реализации

### 3.1. Инвентарь реестра

```python
EXPECTED_RULES = ["KB-%03d" % i for i in range(1, 16)]   # KB-001 … KB-015
assert list(kb_lint.RULES) == EXPECTED_RULES             # порядок и полнота
assert set(kb_lint.RULE_SEVERITY) == set(EXPECTED_RULES) - {"KB-010"}
assert set(kb_lint.RULE_SEVERITY.values()) <= {"error", "warning"}
assert all(kb_lint.RULES[r].strip() for r in EXPECTED_RULES)
```

`KB-010` обязан присутствовать в `RULES` (резерв под `depends_on`) и отсутствовать в `RULE_SEVERITY`.

### 3.2. Хелперы нового класса

```python
class TestLintOutputContract(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.docs_dir = self.temp_dir / "docs"
        self.docs_dir.mkdir(parents=True)
        (self.docs_dir / "00_Index.md").write_text("# Index\n", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _run_cli(self, *args):
        res = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "kb_lint.py"), *args],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        return res.returncode, res.stdout
```

* `tempfile.mkdtemp()` под DSH Windows sandbox создаёт непроходимый для дочерних файлов каталог (TRG-03/INC-003) — тесты запускаются через обёртку `tmp/run_tests.py`; её промоушен в `scripts/` — `DEBT-005`, вне scope этой задачи.
* Хранилище для JSON-тестов должно быть **предсказуемым**: без `SPEC.md`/`Roadmap.md`/`Devlog.md` в родителе (иначе `check_spec_drift`/`check_devlog_semantic_guard` добавят `WARN`). Для warning-хранилища дорожная карта с двумя завершёнными фазами добавляется осознанно (§3.4).

### 3.3. JSON-контракт

```python
payload = json.loads(stdout)
assert sorted(payload) == ["errors", "summary", "version", "warnings"]
assert payload["version"] == 1
assert sorted(payload["summary"]) == ["errors", "files", "warnings", "wikilinks"]
assert isinstance(payload["summary"]["files"], int)
finding = payload["errors"][0]
assert sorted(finding) == ["file", "message", "rule_id", "severity"]
assert finding["severity"] == "error"           # severity совпадает с массивом
assert finding["file"] is None or isinstance(finding["file"], str)
```

Дополнительно: два прогона подряд дают **идентичный** stdout (детерминизм сортировки).

### 3.4. Exit-коды и warning-only сценарий

Warning-only хранилище: `SPEC.md` + `Roadmap.md` с двумя завершёнными фазами (как в `TestKbLint.test_spec_drift_detection_warns_when_drifted`) → `check_spec_drift` даёт `KB-011`.

```python
for fmt in ("text", "json", "sarif"):
    rc_warn, _ = self._run_cli("--path", str(self.docs_dir), "--format", fmt)
    assert rc_warn == 0                      # предупреждения не блокируют
```

Error-хранилище: файл с `[[MissingTarget]]` → `1` во всех трёх форматах.

### 3.5. SARIF-контракт

```python
doc = json.loads(stdout)
assert doc["version"] == "2.1.0"
assert doc["$schema"].endswith("sarif-2.1.0.json")
driver = doc["runs"][0]["tool"]["driver"]
assert driver["name"] == "kb_lint"
rule_ids = [r["id"] for r in driver["rules"]]
assert len(rule_ids) == len(set(rule_ids))              # без дублей
results = doc["runs"][0]["results"]
assert all(r["ruleId"] in rule_ids for r in results)   # перекрёстная ссылка
assert all(r["level"] in ("error", "warning") for r in results)
assert "informationUri" not in driver                  # не светим происхождение проекта
assert all("region" not in loc["physicalLocation"] for r in results for loc in r.get("locations", []))
```

### 3.6. Политика при обнаружении дефекта

Если любой из новых тестов падает на текущем `kb_lint.py` — это дефект реализации TASK-101: оформляется `BUG-XXX` по `/kb-bug`, исправляется через `/kb-implement BUG-XXX` (TDD). В рамках TASK-102 тест **не ослабляется** под поведение кода.

## 4. План верификации (Verification Plan)

- [ ] Компиляция: `python -m py_compile tests/test_kb_lint.py scripts/kb_lint.py` → Exit 0.
- [ ] Только контрактные тесты: `python tmp/run_tests.py tests.test_kb_lint` (или `python -m unittest tests.test_kb_lint -v` вне sandbox) → все новые тесты зелёные.
- [ ] Полный набор: `python tmp/run_tests.py` → **166 + N тестов OK**, 0 failures/errors.
- [ ] Паритет с TASK-101: `git diff scripts/kb_lint.py` пуст (продакшн-код не тронут).
- [ ] Ручная структурная проверка SARIF: `python scripts/kb_lint.py --path docs --format sarif > tmp/kb_lint.sarif` + разбор ключей (`runs[0].tool.driver.rules`, `results[].ruleId`, отсутствие `region`/`informationUri`).
- [ ] Детерминизм JSON: два прогона `--format json` дают побайтово одинаковый stdout.
- [ ] `python scripts/kb_lint.py --path docs` → одна строка `OK: …`, Exit 0 (регресс text-вывода).
- [ ] `python scripts/kb_lint.py --path docs` после правок документации → 0 битых ссылок.

* **Замеры $\ge 3$ прогонов:** не требуются (производительность не заявляется); если фиксируется время, то 3 прогона и среднее в Devlog (правило 16 `AGENTS.md`).

### Visual DoD (для задач с GUI/TUI):

Не применимо: задача добавляет автотесты, пользовательская поверхность не меняется. Скриншот-слот не требуется.

## 5. Критерии готовности (DoD)

- [ ] Добавлено не менее **13** контрактных тестов (§2), каждый падает при регрессии соответствующего инварианта (проверено мысленным мутационным тестом: удаление `KB-010` из `RULES`, смена `version`, удаление `locations`).
- [ ] `scripts/kb_lint.py`, `install.py`, `dist/install.py` не изменены (`git diff` пуст).
- [ ] Полный набор тестов зелёный; регрессов в существующих 166 тестах нет.
- [ ] SARIF проверен структурно; приёмка Code Scanning явно отложена до фазы CI-упаковки (не заявляется).
- [ ] `DEBT-004` дополнен ссылкой на тест-политику.
- [ ] `kb_lint --path docs` — 0 битых ссылок; статусы обновлены (ТЗ/Канбан/Roadmap), запись в `Devlog.md` — на шаге `/kb-complete`.
