---
id: TASK-107
title: "pre-commit hook для линта и два рецепта в README"
status: in-progress
type: task
phase: 28
component:
  - ci
  - distribution
  - docs
parent_plan: "[[../../Plans/PLAN-026-ci-delivery-and-code-scanning|PLAN-026]]"
created: 2026-10-25
updated: 2026-10-25
tags:
  - task/spec
  - phase28
  - ci
  - distribution
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-107 — pre-commit hook и README

> **ID:** TASK-107 | **Статус:** К реализации (Режим 2)  
> **Фаза:** 28 | **План:** [[../../Plans/PLAN-026-ci-delivery-and-code-scanning|PLAN-026]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Предыдущая задача:** [[28_GateHygiene/TASK-105-composite-action-and-readme|TASK-105]] (действие для CI уже есть)  
> **Нормативная база:** [[../../../04_Research/RESEARCH-027-competitor-best-practices-and-adoption-backlog|RESEARCH-027]] (§4 Волна 1 п.2), [[../../../03_Decisions_ADR/ADR-0032-machine-readable-lint-contract-and-rule-registry|ADR-0032]]

---

## 1. Цель задачи

Дать линту **локальный** барьер до коммита: манифест `.pre-commit-hooks.yaml` с хуком `kb-lint`, который в проекте с установленным харнессом запускает `scripts/kb_lint.py` на изменённых Markdown-файлах, и двух рецептов подключения в README (`repo: local` и удалённый `repo:` + `rev:`).

Почему это отдельная задача, а не «ещё один шаг действия»: GitHub Action работает в CI уже **после** пуша, а pre-commit ловит битую ссылку до коммита; у хука другая механика (локальный git-хук, `language: system`), другой контракт (`files`/`pass_filenames`) и другой способ распространения (`rev:` в чужом `.pre-commit-config.yaml`).

### 1.1. Аудит перед спецификацией (2026-10-25)

| Проверка | Факт | Следствие |
| :--- | :--- | :--- |
| `pre-commit` в окружении | **Не установлен** (`shutil.which` → False) | Реальная валидация манифеста инструментом невозможна; Tier 1-тест проверяет структуру и семантику сам, команда для ручной проверки документируется |
| `scripts/kb_lint.py` | `--path docs` (default), text — дефолтный формат, exit `0/1` | Хуку достаточно `entry: python3 scripts/kb_lint.py --path docs` |
| Проверка ссылок | Глобальная (`build_file_map` по всему vault) | `pass_filenames: false` + полный скан (~0.4 с); поштучный режим дал бы ложные «битые ссылки» |
| `scripts/build_installer.py` | Бандл — whitelist (шаблоны, 3 скрипта, скиллы, workflows, `rules/`, `patterns.md`) | `.pre-commit-hooks.yaml` в бандл не попадёт; проверяется Tier 1-тестом на распакованном `EMBEDDED_ASSETS_B64` |
| `action.yml` (TASK-105) | Действие работает без установки харнесса | Разделение: action — для неинсталлированных проектов, hook — для установленных |

## 2. Затрагиваемые файлы и скоуп символов

* `[NEW]` `.pre-commit-hooks.yaml`:
  - единственный хук `id: kb-lint` с полями `name`, `description`, `entry`, `language: system`, `files`, `pass_filenames: false`, `require_serial: true`.
* `[NEW]` `tests/test_pre_commit_hooks.py`:
  - `PreCommitManifestTest._parse_hooks()` — минимальный парсер манифеста (Zero-Deps, без PyYAML).
  - `PreCommitManifestTest.test_manifest_structure()` — один хук, обязательные поля, типы, `language: system`.
  - `PreCommitManifestTest.test_entry_targets_existing_linter()` — `entry` ссылается на существующий `scripts/kb_lint.py`, содержит `--path docs`.
  - `PreCommitManifestTest.test_files_pattern_matches_markdown()` — `files` компилируется и матчит `.md`, но не `.py`.
  * `PreCommitManifestTest.test_manifest_is_not_bundled()` — распаковка `EMBEDDED_ASSETS_B64` из `install.py`: ключа `.pre-commit-hooks.yaml` нет.
* `[MODIFY]` `README.md`:
  - §«🛡️ Continuous Integration & Release Automation» — подраздел «Use as a pre-commit hook» с двумя рецептами и оговорками.

## 3. Детали реализации

### 3.1. Манифест

```yaml
- id: kb-lint
  name: Docs-as-Code knowledge base lint
  description: Broken wikilinks, YAML frontmatter, phase/tech-debt/memory integrity (zero dependencies)
  entry: python3 scripts/kb_lint.py --path docs
  language: system
  files: '\.md$'
  pass_filenames: false
  require_serial: true
```

* `language: system` — хук использует интерпретатор проекта-потребителя, ничего не устанавливает (Zero-Deps; пакет не публикуется).
* `pass_filenames: false` — обязательное условие: проверка ссылок глобальная, поштучный запуск даёт ложные срабатывания.
* `files: '\.md$'` — хук запускается только если в коммите есть Markdown (не на каждый коммит).
* `require_serial: true` — один прогон вместо параллельных копий на большом наборе файлов.
* Переопределение пути: у потребителя `args: ['--path', 'documentation']` (argparse берёт последнее значение `--path`).

### 3.2. README: два рецепта

**A. Проект с установленным харнессом (`repo: local`):**

```yaml
repos:
  - repo: local
    hooks:
      - id: kb-lint
        name: Docs-as-Code knowledge base lint
        entry: python3 scripts/kb_lint.py --path docs
        language: system
        files: '\.md$'
        pass_filenames: false
        require_serial: true
```

**B. Удалённый манифест (`repo:` + `rev:`):**

```yaml
repos:
  - repo: https://github.com/koudinie101-png/agent-docs-harness
    rev: v0.28.0        # первый релиз, содержащий .pre-commit-hooks.yaml; до него — rev: main
    hooks:
      - id: kb-lint
```

Оговорки, которые обязаны быть в README:

* удалённый вариант требует, чтобы `scripts/kb_lint.py` уже был в проекте (установленный харнесс) — pre-commit запускает `entry` в рабочей копии потребителя;
* без установки харнесса используйте GitHub Action (`action.yml`, TASK-105), а не хук;
* `rev` фиксируется на релиз, содержащий манифест; `@main` — временная мера до `v0.28.0`;
* хук не проверяет веса ассетов и SARIF: это делает CI-действие.

### 3.3. Non-goals

* Публикация пакета в PyPI ради `language: python` — против Zero-Deps простоты (PLAN-026 Q3).
* Отдельный скрипт-обёртка для хука — `entry` уже однострочный.
* Изменение бандла установщика: манифест не доставляется клиентам автоматически (они подключают его через `rev:` или копируют рецепт).

## 4. План верификации (Verification Plan)

- [ ] `python -m py_compile tests/test_pre_commit_hooks.py` → Exit 0.
- [ ] `python -m unittest tests.test_pre_commit_hooks -v` → 4 теста OK.
- [ ] Полный набор: `python scripts/run_tests_sandbox.py` → **188 тестов OK** (184 + 4).
- [ ] Ручная проверка манифеста при наличии `pre-commit`: `pre-commit validate-manifest .pre-commit-hooks.yaml` → Exit 0. **В этом окружении `pre-commit` не установлен** — проверка структурная (Tier 1) + документированная команда для пользователя.
- [ ] `git status --short` не содержит `install.py` / `dist/install.py` (манифест не бандлится).
- [ ] `python scripts/kb_lint.py --path docs --verbose` → 0 битых ссылок, 0 `WARN`.
- [ ] README: оба рецепта присутствуют, оговорки на месте, ссылка на действие TASK-105 есть.

* **Замеры $\ge 3$ прогонов:** не применимы (YAML-контракт); если фиксируется время хука — 3 прогона и среднее в Devlog.

### Visual DoD (для задач с GUI/TUI):

Не применимо: поверхности интерфейса нет.

## 5. Критерии готовности (DoD)

- [ ] Манифест создан, структурные и семантические проверки зелёные (4 теста).
- [ ] `files`-регексп матчит Markdown и не матчит код; `pass_filenames: false` зафиксирован тестом.
- [ ] README содержит оба рецепта, оговорку про установленный харнесс, `rev`-пиннинг и `args`-переопределение пути.
- [ ] Манифест отсутствует в бандле (Tier 1-тест на распакованном `EMBEDDED_ASSETS_B64`).
- [ ] Полный набор тестов зелёный; `kb_lint` — 0 битых; статусы обновлены (ТЗ/Канбан/Roadmap), запись в `Devlog.md` — на шаге `/kb-complete`.
