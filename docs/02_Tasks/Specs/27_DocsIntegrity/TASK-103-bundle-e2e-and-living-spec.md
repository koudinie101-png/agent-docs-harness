---
id: TASK-103
title: "Доставка машинно-читаемого линтера: пересборка бандла, бюджет, E2E и Living Spec"
status: in-progress
type: task
phase: 27
component:
  - installer
  - tests
  - docs
parent_plan: "[[../../Plans/PLAN-025-docs-integrity-gate-kb-lint-productization|PLAN-025]]"
created: 2026-10-25
updated: 2026-10-25
tags:
  - task/spec
  - phase27
  - installer
  - e2e
  - spec
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-103 — Доставка машинно-читаемого линтера

> **ID:** TASK-103 | **Статус:** К реализации (Режим 2)  
> **Фаза:** 27 | **План:** [[../../Plans/PLAN-025-docs-integrity-gate-kb-lint-productization|PLAN-025]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Предыдущие задачи:** [[27_DocsIntegrity/TASK-101-finding-model-rule-registry-and-formats|TASK-101]] (реализация), [[27_DocsIntegrity/TASK-102-output-contract-tests|TASK-102]] (контрактные тесты)  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0032-machine-readable-lint-contract-and-rule-registry|ADR-0032]], [[../../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]], [[../../../03_Decisions_ADR/ADR-0014-greenfield-idea-first-initialization-and-living-spec-protocol|ADR-0014]]  
> **Техдолг фазы:** `DEBT-004` (SARIF без строк) остаётся открытым

---

## 1. Цель задачи

Замкнуть Фазу 27 «до клиента»: пересобрать монолитный `install.py` / `dist/install.py` с новым `kb_lint.py`, пере-базировать бюджет монолита, доказать E2E-тестом, что **установленная** копия линтера отдаёт `--format json` и `--version`, и синхронизировать Living Spec (`SPEC.md`, `README.md`, `docs/Onboarding.md`) с новым публичным контрактом.

Пока задача не сделана, `install.py` содержит **прежний** линтер (без `Finding`/`--format`): публичный контракт существует в репозитории, но не доставляется.

### 1.1. Аудит перед спецификацией (2026-10-25)

| Проверка | Факт | Следствие |
| :--- | :--- | :--- |
| `scripts/kb_lint.py` | 57 903 символа (было 51 329 в v0.26.0, +6 574) | Ожидаемый прирост монолита ≈ **+2 100 B** (коэффициент бандла 3.13 символа/байт) |
| `install.py` / `dist/install.py` | 175 175 B, бюджет `test_16` = **176 000** → запас 825 B | Ожидаемые ~177 300 B не влезают: нужен ре-байзлайн до 178 000 (запас ~700 B на компрессию) |
| `scripts/build_installer.py` | `bundle_assets()` + `compress_bundle()` (zlib-9 + base64), пишет оба файла | Пересборка — одна команда; ручного редактирования артефактов нет |
| `tests/test_installer.py` | 43 теста, `test_16` держит бюджет; установку проверяют через `install.install_harness(...)` в temp-каталоге | E2E нового контракта добавляется тем же паттерном (`test_35_...`) |
| `SPEC.md` §2.3 | 14 буллетов про `kb_lint.py`, ни слова про `Finding`/`KB-XXX`/`--format` | Обязательная правка: публичный контракт изменился (ADR-0014) |
| `README.md` §3 | Команда `python3 scripts/kb_lint.py --path docs` + advisory-проверки | Нужны примеры `--format json/sarif` и `--version` |
| `docs/Onboarding.md` §4 | Блок «Проверка линтером» с одной командой | Добавить машинно-читаемый вариант |
| `docs/06_Memory/patterns.md` | `TRG-03` count=2 (изменён в TASK-101) | Попадёт в бандл при пересборке — ожидаемо |

## 2. Затрагиваемые файлы и скоуп символов

* `[MODIFY]` `tests/test_installer.py`:
  - `TestInstaller.test_16_high_snr_static_corpus_benchmarks()` — бюджет монолита `176000` → `178000` с комментарием-обоснованием (Фаза 27: `Finding` + `KB-XXX` + 3 рендерера).
  - `TestInstaller.test_35_task_101_machine_readable_lint_delivery()` — **новый** E2E: установка в temp-каталог, запуск установленного `scripts/kb_lint.py` с `--format json` и `--version`, проверка схемы и кода возврата; повторный прогон после `--update` (флаг сохраняется).
* `[MODIFY]` `install.py`, `dist/install.py` — только регенерация `python scripts/build_installer.py` (embedded payload; ручных правок нет).
* `[MODIFY]` `SPEC.md`:
  - `SPEC.md` frontmatter `updated:` → `2026-10-25`.
  - §2.3 `scripts/kb_lint.py` — два новых буллета: машинно-читаемый контракт (`Finding`, реестр `KB-001…KB-015`, `KB-010` зарезервирован) и CLI (`--format {text,json,sarif}`, `--version`, неизменные exit-коды).
* `[MODIFY]` `README.md`:
  - §3 «Linter» — примеры `--format json`/`--format sarif`/`--version`, стабильные `KB-XXX`, оговорка про отсутствие `region` в SARIF (`DEBT-004`).
* `[MODIFY]` `docs/Onboarding.md`:
  - §4 «Проверка линтером» — машинно-читаемый вариант команды и правило «text — для человека, json/sarif — для CI».
* `[MODIFY]` `docs/02_Tasks/TechDebt.md`:
  - `DEBT-004` — не закрывается (строки не появились), отметка не требуется.

## 3. Детали реализации

### 3.1. Пересборка и бюджет

```bash
python scripts/build_installer.py
```

Ожидаемый вывод: размер обоих артефактов; `install.py` и `dist/install.py` **побайтово идентичны** (проверяется `fc`/`Compare-Object` или сравнением SHA-256).

Бюджет в `test_16` меняется осознанно:

```python
# Installer size check (budget <= 178 KB ... Phase 27 machine-readable lint contract:
# Finding model + KB-XXX registry + text/json/sarif renderers)
self.assertLessEqual(installer_size, 178000, f"install.py exceeded budget: {installer_size} bytes (budget <= 178 KB)")
```

Обоснование в комментарии: предыдущий бюджет 176 000 держался на фактических 175 175 B; прирост кода линтера — продуктовый (машинно-читаемая диагностика), а не токен-блоат: `kb_lint.py` не инжектится в контекст агента. Токен-бюджеты шаблонов (30 000) и скиллов (31 000) **не трогаются**.

### 3.2. E2E установленной копии

```python
def test_35_task_101_machine_readable_lint_delivery(self):
    """TASK-101/103: installed linter ships machine-readable output contract."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        target = Path(tmp_dir) / "MachineLintApp"
        target.mkdir()
        install.install_harness(target_dir=target, project_name="MachineLintApp",
                                stack_key="python", agent_choice="all",
                                git_choice="none", force=True)
        lint_script = target / "scripts" / "kb_lint.py"
        self.assertTrue(lint_script.is_file())

        res = subprocess.run([sys.executable, str(lint_script), "--path", str(target / "docs"),
                              "--format", "json"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res.returncode, 0, res.stderr)
        payload = json.loads(res.stdout)          # stdout = только документ
        self.assertEqual(payload["version"], 1)
        self.assertEqual(sorted(payload["summary"]), ["errors", "files", "warnings", "wikilinks"])

        version = subprocess.run([sys.executable, str(lint_script), "--version"],
                                 capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(version.returncode, 0)
        self.assertEqual(version.stdout.strip(), "kb_lint 1")
```

* Установка в temp-каталог — существующий паттерн (`test_16`, `test_17`); под DSH sandbox запускается через обёртку (TRG-03, `DEBT-005`).
* Тест обязан падать на старом бандле (там `--format` неизвестен: `argparse` вернёт Exit 2) — это и есть проверка доставки.

### 3.3. Живая спецификация (Living Spec)

Ключевые формулировки (кратко, High-SNR):

* `SPEC.md` §2.3:
  * «Единая модель находки (`Finding`) и реестр стабильных правил `KB-001…KB-015` (`KB-010` зарезервирован под `depends_on`) — SSOT для машинно-читаемых отчётов и ignore-политик.»
  * «CLI-контракт: `--format {text,json,sarif}` (text — байт-в-байт прежний человекочитаемый вывод), `--version` (версия набора правил), неизменные exit-коды `0/1`; SARIF 2.1.0 без `region.startLine` (`DEBT-004`).»
* `README.md` §3: блок примеров команд (`--format json` с разбором через `json.loads`, `--format sarif > kb.sarif`, `--version`) + предложение о стабильных `KB-XXX`.
* `docs/Onboarding.md` §4: одна строка с машинно-читаемым вызовом и указанием, что CI потребляет `json/sarif`, а человек — `text`.

## 4. План верификации (Verification Plan)

- [ ] Пересборка: `python scripts/build_installer.py` → Exit 0; размер объявлен в выводе, `install.py` ≤ 178 000 B.
- [ ] Паритет артефактов: SHA-256 `install.py` == SHA-256 `dist/install.py`.
- [ ] Компиляция: `python -m py_compile scripts/*.py tests/test_installer.py` → Exit 0.
- [ ] Полный набор: `python tmp/run_tests.py` → **180 тестов OK** (179 + 1 новый), 0 failures.
- [ ] Бюджет: новый тест `test_16` зелёный на фактическом размере; в случае выхода за 178 000 — сжать код, а не поднимать бюджет молча.
- [ ] E2E доставки: установить в песочницу (`install.install_harness` или `python install.py --stack python --agent all --git none --force`), затем `python <target>/scripts/kb_lint.py --path <target>/docs --format json` → JSON-документ, Exit 0; `--version` → `kb_lint 1`.
- [ ] `--update`: повторный прогон установки с обновлением не ломает флаги (проверяется в новом тесте).
- [ ] Живая спецификация: `SPEC.md`/`README.md`/`docs/Onboarding.md` содержат `--format`, `KB-XXX` и `--version`; `SPEC.md` `updated: 2026-10-25`.
- [ ] `python scripts/kb_lint.py --path docs --verbose` → 0 битых ссылок, 0 `WARN`.

* **Замеры:** размер монолита — детерминированная величина (`stat`), серия прогонов не требуется; если фиксируется время прогона линтера, то 3 прогона и среднее в Devlog (правило 16 `AGENTS.md`).

### Visual DoD (для задач с GUI/TUI):

Не применимо: меняются артефакты сборки и текст документации. Пользовательская поверхность — вывод `--format`, он уже покрыт контрактными тестами TASK-102.

## 5. Критерии готовности (DoD)

- [ ] `install.py` и `dist/install.py` пересобраны, идентичны и ≤ 178 000 B; фактический размер записан в Devlog.
- [ ] `test_16` содержит новый бюджет и обоснование; бюджет шаблонов/скиллов не менялся.
- [ ] Новый E2E-тест доказывает, что **установленная** копия отдаёт `--format json` и `--version` (на старом бандле тест падает).
- [ ] `SPEC.md`, `README.md`, `docs/Onboarding.md` описывают новый контракт; `SPEC.md.updated` обновлён.
- [ ] Полный набор тестов зелёный (180), `kb_lint` — 0 битых ссылок.
- [ ] `DEBT-004`/`DEBT-005` не закрываются: строки и sandbox-обёртка остаются вне scope.
- [ ] После завершения Фаза 27 готова к релизу: следующий шаг — `/kb-release` (по отдельной команде пользователя).
