---
id: BUG-013
title: "SARIF artifactLocation.uri относительный к docs/, а не к корню репозитория"
status: open
severity: medium
type: bug
target_release: "v0.28.0"
target_phase: 28
release_blocker: true
fixed_in: null
regression_test: "tests/test_kb_lint.py::TestLintOutputContract.test_sarif_paths_are_repo_relative"
created: 2026-10-25
updated: 2026-10-25
tags:
  - bug
  - defect
  - code-scanning
  - sarif
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 🐞 Дефект: BUG-013 — SARIF-путь не совпадает с реальным путём файла

> **ID:** BUG-013 | **Критичность:** Medium | **Статус:** open  
> **Релиз:** v0.28.0 | **Блокер:** Да (Code Scanning — заголовочная функция релиза)  
> **Канбан:** [[../Kanban|Канбан-доска]] | **Спецификация:** [[../../SPEC|SPEC.md]]  
> **Обнаружен:** probe в [[Specs/28_GateHygiene/TASK-109-debt004-decision|TASK-109]] (2026-10-25)

---

## 1. Симптомы и окружение

* **Симптом:** в GitHub Code Scanning алерт показывает путь без префикса хранилища: `99_probe_broken.md` вместо `docs/99_probe_broken.md`. Ссылка «открыть файл» ведёт на несуществующий путь в корне репозитория.
* **Окружение:** `scripts/kb_lint.py --format sarif` (v0.27.0+), GitHub Code Scanning (CodeQL Action v4); воспроизводится локально на любом хранилище с вложенным каталогом `docs/`.

## 2. Шаги воспроизведения (Repro Steps)

1. Создать хранилище `tmp/probe_uri/docs/` с файлом `nested.md`, содержащим `[[MissingNote]]`.
2. Выполнить `python scripts/kb_lint.py --path tmp/probe_uri/docs --format sarif`.
3. **Фактически:** `runs[0].results[0].locations[0].physicalLocation.artifactLocation.uri == "nested.md"`.
4. **Ожидаемо:** `"docs/nested.md"` — путь относительно корня репозитория (так его интерпретирует Code Scanning).

Подтверждено на реальном GitHub: `gh api …/code-scanning/alerts/1` → `{"rule":"KB-001","path":"99_probe_broken.md","start_line":1}` при фактическом файле `docs/99_probe_broken.md`.

## 3. Диагностика (Логи, Стек-трейс)

```text
$ python scripts/kb_lint.py --path tmp/probe_uri/docs --format sarif | jq -r '.runs[0].results[0].locations[0].physicalLocation.artifactLocation.uri'
nested.md

$ gh api repos/koudinie101-png/agent-docs-harness/code-scanning/alerts/1 --jq '.most_recent_instance.location.path'
99_probe_broken.md
```

## 4. Первопричина (Root Cause Analysis — RCA)

`Finding.file` формируется как путь относительно **хранилища** (`_relative_to(file, docs_dir)`), и `render_sarif()` публикует его дословно как `artifactLocation.uri`. SARIF и Code Scanning интерпретируют `uri` относительно **корня репозитория** (или абсолютного URL), поэтому для файлов внутри `docs/` теряется префикс хранилища. JSON-контракт (`file`) намеренно документировал docs-relative значение, то есть дефект локализован в SARIF-рендерере и в семантике поля `Finding.file`.

Дополнительно зафиксировано поведение GitHub: при отсутствии `region` API возвращает `start_line: 1` (дефолт рендеринга, не наше значение).

## 5. План исправления

* `[MODIFY]` `scripts/kb_lint.py`:
  - `_repo_relative(path, docs_dir, repo_root) -> str` — новый хелпер (root-документы остаются как есть, файлы `docs/` получают префикс хранилища).
  - точки эмиссии находок (`check_*`, `KB-001`, `KB-002`) — `file=` заполняется repo-relative значением.
  - `render_sarif()` — публикует `Finding.file` без изменений (контракт SARIF: repo-relative); `render_json()` — то же значение (осознанное изменение контракта `file`, фиксируется в ADR-0032 Amendments).
* `[MODIFY]` `tests/test_kb_lint.py`:
  - `TestLintOutputContract.test_json_reports_broken_link_as_kb_001()` — ожидание `docs/broken.md`.
  - `TestLintOutputContract.test_sarif_paths_are_repo_relative()` — новый регрессионный тест.
  - `PreCommitManifestTest` не затрагивается.

## 6. Верификация (Regression-First)

- [ ] Падающий регрессионный тест воспроизводит дефект (RED).
- [ ] Исправление применено в коде (GREEN).
- [ ] Регрессионный тест и весь сьют проходят успешно (REFACTOR).
- [ ] Дефект закрыт через `/kb-implement BUG-013` или `kb-complete`.
