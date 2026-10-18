---
id: TASK-086
title: "Генерация корневого AGENTS.md через scripts/gen_rules.py --check, CI-гейт и exclusion workflow в бандле"
status: done
type: task
phase: 22
component:
  - rules
  - codegen
  - ci
parent_plan: "[[../../Plans/PLAN-022-single-source-rule-compiler|PLAN-022]]"
created: 2026-10-18
updated: 2026-10-18
tags:
  - task/spec
  - phase22
  - ssot
  - codegen
  - ci
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-086 — Генерация корневого `AGENTS.md` через `scripts/gen_rules.py --check`, CI-гейт и exclusion workflow

> **ID:** TASK-086 | **Статус:** Выполнено (Режим 3)  
> **Фаза:** 22 | **План:** [[../../Plans/PLAN-022-single-source-rule-compiler|PLAN-022]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Предшественник:** [[../../Specs/22_RuleCompiler/TASK-085-rules-corpus-renderer-and-bundling|TASK-085]] (корпус и рендерер)  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]] (Tier 1), [[../../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]

---

## 1. Цель задачи

Сделать корневой `AGENTS.md` **генерируемым артефактом**: единственный источник — документ `harness-agents` в `rules/AGENTS_CORE.md` (TASK-085), а любая ручная правка `AGENTS.md` ловится механически в CI (`--check`, Exit code 1).

Задача не меняет содержание правил. Единственное ожидаемое изменение самого файла — служебная шапка `GENERATED`, поэтому дифф `AGENTS.md` в этой задаче должен состоять ровно из одной добавленной строки.

Дополнительно закрывается риск утечки: `.github/workflows/rules-check.yml` — внутренний workflow харнесса, в клиентские проекты он уезжать не должен (там нет `rules/`).

## 2. Затрагиваемые файлы

* `[NEW]` `scripts/gen_rules.py` — CLI: рендер и `--check`.
* `[NEW]` `.github/workflows/rules-check.yml` — гейт на `push` и `pull_request`.
* `[MODIFY]` `AGENTS.md` — регенерирован из корпуса (+1 строка шапки), далее только генерация.
* `[MODIFY]` `rules/AGENTS_CORE.md` — шапка `GENERATED` внутри документа `harness-agents`.
* `[MODIFY]` `scripts/build_installer.py` — `EXCLUDED_WORKFLOWS` в `bundle_assets()`.
* `[MODIFY]` `.github/workflows/release.yml` — шаг `--check` в префлайт.
* `[MODIFY]` `tests/test_installer.py` — ассерт: `rules-check.yml` отсутствует в бандле, `release.yml` присутствует.
* `[MODIFY]` `docs/Onboarding.md` — абзац «правила редактируются в `rules/AGENTS_CORE.md`, `AGENTS.md` руками не правится».

## 3. Детали реализации

### 3.1. `scripts/gen_rules.py`

```python
REPO_ROOT = Path(__file__).resolve().parent.parent   # sys.path.insert(0, str(REPO_ROOT)); import install

def render_harness_agents() -> str:
    """install._render_rules_document("harness-agents", {})"""

def normalize(text: str) -> str:
    """\r\n -> \n (Windows autocrlf не должен давать ложный diff)."""

def check_current(output_path: Path = REPO_ROOT / "AGENTS.md",
                  rendered: str | None = None) -> tuple[bool, str]:
    """(ok, unified_diff) — сравнение нормализованных строк."""

def main(argv: list[str]) -> int:
    """--check -> 0 | 1; иначе запись файла. Ошибка рендера -> 2."""
```

Требования:
* `--check` печатает первые 40 строк unified-diff и возвращает 1; при совпадении — `OK`.
* Запись выполняется с `newline="\n"`, UTF-8, без BOM.
* Импорт `install` не должен запускать `main()` (в `install.py` уже есть guard `if __name__ == "__main__"` — проверить и сохранить).
* Скрипт не зависит от текущего каталога: все пути от `REPO_ROOT`.

### 3.2. Шапка GENERATED

В документе `harness-agents` первой строкой:

```markdown
<!-- GENERATED FILE: edit rules/AGENTS_CORE.md, then run: python scripts/gen_rules.py -->
```

Шапка — часть корпуса (рендерер остаётся «глупым»), поэтому `render_harness_agents()` возвращает её вместе с телом.

### 3.3. Workflow `rules-check.yml`

```yaml
name: Rules Check
on:
  push:
  pull_request:
jobs:
  rules:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: '3.11'}
      - name: Verify AGENTS.md is generated from corpus
        run: python scripts/gen_rules.py --check
      - name: Unit tests
        run: python -m unittest discover -s tests
```

### 3.4. Exclusion в `scripts/build_installer.py`

```python
EXCLUDED_WORKFLOWS = {"rules-check.yml"}
```

Пропуск выполняется в цикле по `workflows_dir.glob("*.yml")`. Бандл не должен содержать `.github/workflows/rules-check.yml`; `release.yml` и `feedback-sync.yml` остаются.

### 3.5. Префлайт `.github/workflows/release.yml`

Шаг добавляется после «Verify Knowledge Base Integrity»:

```yaml
      - name: Verify Rules Corpus Consistency
        run: python scripts/gen_rules.py --check
```

## 4. План верификации (Verification Plan)

- [x] Генерация идемпотентна: `python scripts/gen_rules.py --check` (Exit code 0, вывод `OK`).
- [x] Дрейф ловится: `Add-Content AGENTS.md "<!-- test -->"` → `--check` возвращает 1 и печатает diff; затем `git checkout -- AGENTS.md`.
- [x] Diff миграции: `git diff --stat AGENTS.md` → ровно 1 вставка (шапка GENERATED).
- [x] Компиляция: `python -m py_compile install.py scripts/*.py` (Exit code 0).
- [x] Полный прогон: `python -m unittest discover -s tests` (Exit code 0).
- [x] Сборка: `python scripts/build_installer.py` (Exit code 0).
- [x] Exclusion: `python -c "import install; a=install.unpack_assets(); print('.github/workflows/rules-check.yml' in a, '.github/workflows/release.yml' in a)"` → `False True`.
- [x] Линтер: `python scripts/kb_lint.py --path docs` (0 broken links, Exit code 0).

## 5. Критерии готовности (DoD)

- [x] `AGENTS.md` воспроизводится из корпуса побайтово (после нормализации переводов строк).
- [x] `--check` возвращает 0 на чистом дереве и 1 при любой ручной правке.
- [x] `rules-check.yml` работает на `push`/`pull_request` и **не** попадает в бандл.
- [x] `release.yml` падает на рассинхронизированном `AGENTS.md` до публикации.
- [x] `docs/Onboarding.md` объясняет новый порядок правки правил.
- [x] Статус обновлён в ТЗ, Канбане (`Done`) и Дорожной карте (`[x]`); запись добавлена в `Devlog.md`.
