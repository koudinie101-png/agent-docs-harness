---
id: TASK-089
title: "Целостность процедурной памяти: check_memory_consistency() в kb_lint, чистка висячих INC-ссылок и процедура заведения инцидента"
status: done
type: task
phase: 23
component:
  - lint
  - memory
  - docs
parent_plan: "[[../../Roadmap|Roadmap (Фаза 23)]]"
created: 2026-10-18
updated: 2026-10-18
tags:
  - task/spec
  - phase23
  - memory
  - lint
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-089 — Целостность процедурной памяти

> **ID:** TASK-089 | **Статус:** Выполнено (Режим 3)  
> **Фаза:** 23 | **План:** нет (одна задача, обоснование в `Roadmap.md`) | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]] (Tier 1–3), [[../../../03_Decisions_ADR/ADR-0029-fine-grained-task-symbol-contracts-and-line-drift-rejection|ADR-0029]] (символьный скоуп)

---

## 1. Цель задачи

Замкнуть Tier 1-контроль контура `docs/06_Memory/`, устранив разрыв, обнаруженный при аудите 2026-10-18:

1. `scripts/kb_lint.py` проверяет только лимит 15 записей (`check_memory_limits`), но **не проверяет ссылочную целостность**: `patterns.md` может ссылаться на несуществующий `INC-XXX`, а инцидент — на несуществующий `TRG-XX`.
2. В репозитории уже реализован этот дрейф: `TRG-01` → `INC-001` и `TRG-02` → `INC-002`, при том что отчёты `INC-001`/`INC-002` **никогда не существовали в Git** (контур памяти появился позже, в TASK-061; индекс был заполнен «посевными» паттернами без архива).
3. Процедура заведения инцидента рассыпана по трём документам и не имеет единого описания «когда, какой ID, какие поля, как связать, когда архивировать».

**Вне скоупа:** изменение лимита 15, ротация/архивация паттернов (Icebox: «Автоматизированная ротация»), ретроспективное восстановление `INC-001`/`INC-002` (фабрикация истории запрещена).

## 2. Затрагиваемые файлы

* `[MODIFY]` `scripts/kb_lint.py`:
  * `check_memory_consistency(docs_dir)` — новая функция проверки ссылок памяти.
  * `run_linter()` — вызов новой функции, вывод `WARN` в verbose и silent-on-success режимах (exit code не меняется).
* `[MODIFY]` `tests/test_kb_lint.py` — модульные тесты новой функции и интеграции в `run_linter`.
* `[MODIFY]` `docs/06_Memory/patterns.md` — снятие висячих ссылок `TRG-01`/`TRG-02`.
* `[MODIFY]` `docs/Onboarding.md` — подраздел «Как завести инцидент» в §13.
* `[MODIFY]` `SPEC.md` — описание новой проверки в перечне возможностей `scripts/kb_lint.py` (§2.3).

## 3. Детали реализации

### 3.1. `check_memory_consistency(docs_dir: Path) -> List[str]`

Возвращает список неблокирующих предупреждений (строки начинаются с `WARN:`) либо `[]`.

```python
WARN: patterns.md references missing incident report 'INC-001'
WARN: incident 'INC-005' id does not match filename 'INC-004-...'
WARN: incident 'INC-004' targets 'TRG-99' which is absent from patterns.md
WARN: pattern 'TRG-01' links 'INC-001' whose target_pattern is 'TRG-02'
```

Проверки:
1. **Ссылки индекса:** каждое вхождение `INC-\d{3}` в `patterns.md` имеет файл `06_Memory/Incidents/<INC-...>-*.md`.
2. **Идентичность:** `id` во frontmatter инцидента совпадает с `INC-\d{3}`-префиксом имени файла.
3. **Обратная ссылка:** `target_pattern` инцидента присутствует в `patterns.md` в виде `[TRG-XX]`.
4. **Согласованность пары:** если паттерн `[TRG-XX]` ссылается на `INC-YYY`, то `target_pattern` этого инцидента равен `TRG-XX`.

Устойчивость:
* Нет `06_Memory/` или `patterns.md` — `[]` (проверка не применима).
* Отсутствие `target_pattern` у инцидента — `WARN` (поле обязательно по шаблону).
* Пропуск «посевных» паттернов без архива: строка паттерна, помеченная `seeded pattern (no archived report)`, **не считается ссылкой** и не порождает предупреждений.
* Windows-совместимость: пути только через `pathlib.Path`, `read_text(encoding="utf-8", errors="replace")`.

### 3.2. Интеграция в `run_linter()`

* Рядом с `memory_errors = check_memory_limits(docs_dir)` добавить `memory_warnings = check_memory_consistency(docs_dir)`.
* Verbose: блок `⚠️ Memory Consistency Warnings (N):` после Memory Limit Errors.
* Silent-on-Success: каждая строка печатается как `⚠️  WARN: ...` (аналогично `debt_warnings`).
* `has_errors` **не включает** `memory_warnings`: проверка неблокирующая (прецедент — `debt_warnings`, ADR-0025 Tier 1 advisory).

### 3.3. Чистка висячих ссылок

В `patterns.md` заменить у `TRG-01` и `TRG-02` суффикс `-> INC-00X` на `seeded pattern (no archived report)`:

```markdown
- [TRG-01] Windows Path Compatibility | ... | (Count: 3, Sev: High) seeded pattern (no archived report)
```

Смысл: паттерн сохранён (он валиден и полезен), но не выдаёт несуществующий отчёт за доказательство.

### 3.4. Процедура в `docs/Onboarding.md` §13

Добавить подраздел «Как завести инцидент» (≤ 12 строк):
* **Когда:** процедурная ошибка, сорванная итерация или систематический near-miss в Режиме 3.
* **ID:** следующий свободный `INC-XXX` (не переиспользовать).
* **Файл:** `docs/06_Memory/Incidents/INC-XXX-<slug>.md` по `TEMPLATE_INCIDENT.md`; обязательные поля: `id`, `title`, `status`, `severity`, `tag`, `root_cause`, `target_pattern`.
* **Связи:** `target_pattern` обязателен и должен существовать в `patterns.md`; в отчёте указывается `TASK-XXX`/`BUG-XXX`-источник.
* **Промоушен:** две оси — частота/тяжесть (в индекс) и охват (Tier 1 тест/линтер или Tier 2 `AGENTS.md`).
* **Лимит:** ≤ 15 активных паттернов; при переполнении — слияние или архивация.
* **Контроль:** `check_memory_consistency` предупреждает о разрывах ссылок; `check_memory_limits` блокирует превышение лимита.

### 3.5. `SPEC.md`

В перечне возможностей `scripts/kb_lint.py` (§2.3) добавить пункт: «Контроль целостности процедурной памяти (`check_memory_consistency`): ссылки `patterns.md` → `Incidents/`, совпадение `id` с именем файла, наличие `target_pattern` в индексе (неблокирующие `WARN`).»

## 4. План верификации (Verification Plan)

- [x] Модульные тесты: `python -m unittest tests.test_kb_lint -v` (Exit code 0; 8 новых тестов: 4 сценария ссылочной целостности, seeded-паттерны, чистая пара, интеграция в `run_linter`; модуль — 50 тестов OK через sandbox-safe обёртку INC-003).
- [x] Полный прогон: 146 тестов OK (Exit code 0; в песочнице DSH — через обёртку INC-003 `tmp/run_tests.py`).
- [x] Чистый репозиторий не даёт предупреждений: `python scripts/kb_lint.py --path docs --verbose` — блок `Memory Consistency Warnings` отсутствует, `🎉 Knowledge base is healthy and consistent!`.
- [x] Негативная проверка (вручную): временно дописана ссылка `-> INC-999` → `--verbose` печатает `Memory Consistency Warnings (1)` и `WARN: patterns.md references missing incident report 'INC-999'`, Exit code остался 0; файл восстановлен копией из `tmp/` с совпадением SHA-256 (`7492dd60…f272d2`, TRG-05).
- [x] Компиляция: `python -m compileall -q scripts` (Exit code 0).
- [x] Целостность базы знаний: `python scripts/kb_lint.py --path docs` (232 файла, 2185 wikilinks, 0 broken; Exit code 0).

## 5. Критерии готовности (DoD)

- [x] `check_memory_consistency()` реализована и интегрирована в `run_linter()` без изменения exit code.
- [x] Покрыты 4 сценария: отсутствующий отчёт, несовпадение `id`/имени, отсутствующий `target_pattern`, рассогласованная пара `TRG↔INC`.
- [x] Висячие ссылки `INC-001`/`INC-002` устранены; репозиторий даёт 0 memory-предупреждений.
- [x] Процедура «Как завести инцидент» зафиксирована в `Onboarding.md` §13.
- [x] `SPEC.md` синхронизирован (Living Spec).
- [x] Статус обновлён в ТЗ, Канбане (`Done`) и Дорожной карте (`[x]`); запись добавлена в `Devlog.md`.
