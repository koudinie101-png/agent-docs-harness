---
id: TASK-109
title: "Решение по DEBT-004: проверка аннотаций и закрытие долга"
status: in-progress
type: task
phase: 28
component:
  - docs
  - ci
parent_plan: "[[../../Plans/PLAN-026-ci-delivery-and-code-scanning|PLAN-026]]"
created: 2026-10-25
updated: 2026-10-25
tags:
  - task/spec
  - phase28
  - techdebt
  - code-scanning
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-109 — Решение по `DEBT-004`

> **ID:** TASK-109 | **Статус:** К реализации (Режим 2)  
> **Фаза:** 28 | **План:** [[../../Plans/PLAN-026-ci-delivery-and-code-scanning|PLAN-026]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Долг:** [[../../TechDebt|DEBT-004]] — закрывается или переоформляется этой задачей  
> **База:** [[28_GateHygiene/TASK-108-code-scanning-workflow|TASK-108]] (Code Scanning уже принимает наш SARIF)

---

## 1. Цель задачи

Принять окончательное решение по `DEBT-004` («SARIF без `region.startLine`») **по наблюдаемым данным**, а не по интуиции:

* TASK-108 доказала, что Code Scanning принимает документ (`analyses` → `tool: kb_lint`, `results: 0`), но **реального алерта мы не видели** — база чистая, находок нет;
* значит нельзя честно утверждать ни «файла достаточно», ни «без строк неудобно».

Задача: создать **временную** ветку с одной намеренной находкой, прогнать workflow на ней, посмотреть, как GitHub показывает алерт (файл? сообщение? правило?), затем убрать за собой. По результату — либо закрыть долг как принятое ограничение (с записью обоснования), либо завести отдельную задачу на трекинг строк.

### 1.1. Что известно до проверки (2026-10-25)

| Факт | Источник | Следствие |
| :--- | :--- | :--- |
| SARIF принимается без `region` | `code-scanning/analyses`, TASK-108 | Отсутствие строк — не блокер приёмки |
| `test_sarif_contract_structure` фиксирует отсутствие `region` | `tests/test_kb_lint.py` | Регресс «появилась фиктивная строка 1» будет пойман |
| Трекинг строк потребует переработки 15 `check_*` | `scripts/kb_lint.py` | Дорого: каждая проверка должна считать позицию |
| Сообщение уже содержит имя ссылки/поля | `render_sarif` message | Читаемость алерта не нулевая даже без строк |

## 2. Затрагиваемые файлы и скоуп символов

* `[MODIFY]` `docs/02_Tasks/TechDebt.md`:
  - `DEBT-004` — строка переезжает в `Resolved Debt` с датой, ссылкой на эту задачу и **записанным решением** (наблюдение + почему файла достаточно). При альтернативном исходе — остаётся в `Active P3 Debt` с уточнённой формулировкой и ссылкой на новую задачу.
* `[MODIFY]` `docs/03_Decisions_ADR/ADR-0032-machine-readable-lint-contract-and-rule-registry.md`:
  - раздел «Amendments» (короткий, 3–5 строк): решение по `region.startLine` со ссылкой на наблюдение.
* `[MODIFY]` `README.md`:
  - пункт про SARIF-локации — заменить «see `DEBT-004`» на итоговое решение (файл-level как осознанный выбор, а не открытый долг).
* **Временные артефакты (не попадают в `main`):** ветка `probe/kb-001-alert` с файлом `docs/99_probe_broken.md` (`[[MissingNote]]`), после проверки ветка удаляется, алерт закрывается через API.

## 3. Детали реализации

### 3.1. Процедура наблюдения (probe)

```bash
git checkout -b probe/kb-001-alert
printf -- "---\nid: PROBE\ntitle: Probe\nstatus: active\n---\n\n[[MissingNote]]\n" > docs/99_probe_broken.md
git add docs/99_probe_broken.md
git commit -m "chore(probe): temporary broken link for TASK-109 alert shape"
git push -u origin probe/kb-001-alert
gh workflow run code-scanning.yml --ref probe/kb-001-alert
gh run list --workflow=code-scanning.yml -L 1 --json databaseId,status,conclusion
gh run watch <databaseId> --exit-status || true   # job обязан упасть: линт нашёл ошибку
gh api repos/koudinie101-png/agent-docs-harness/code-scanning/alerts \
  --jq '.[0] | {rule: .rule.id, path: .most_recent_instance.location.path, line: .most_recent_instance.location.start_line, message: .most_recent_instance.message.text, state: .state}'
```

Ожидание (критерий приемлемости A): `rule.id` = `KB-001`, `path` = `docs/99_probe_broken.md`, `line` = `null` (или отсутствует), `message` содержит `MissingNote`, `state` = `open`.

Критерий B (строки действительно нужны): алерт без `path` или сообщение не позволяет найти место.

### 3.2. Уборка (обязательна независимо от исхода)

```bash
gh api -X PATCH repos/koudinie101-png/agent-docs-harness/code-scanning/alerts/<number> \
  -f state=dismissed -f dismissed_reason="won't fix" -f dismissed_comment="TASK-109 probe: temporary broken link"
git checkout main
git branch -D probe/kb-001-alert
git push origin --delete probe/kb-001-alert
```

После уборки `code-scanning/alerts` на `main` не должен содержать открытых алертов; закрытый probe-алерт остаётся в истории как dismissed — это нормально и документируется.

### 3.3. Закрытие долга (при исходе A — ожидаемом)

* `TechDebt.md`: `DEBT-004` → `Resolved Debt`, описание: «file-level локации достаточны: Code Scanning показывает правило, путь и сообщение с именем битой ссылки; трекинг строк потребовал бы переработки 15 проверок без наблюдаемого выигрыша».
* `ADR-0032`: короткий **Amendments**-раздел с датой и ссылкой на TASK-109.
* `README.md`: пункт про SARIF переписывается как решение, без «открытого долга».

### 3.4. При исходе B

* `DEBT-004` остаётся `Открыт`, формулировка уточняется по факту (что именно не хватает).
* В `Roadmap.md` Icebox добавляется пункт «Line-level SARIF locations for KB-001/006/014» со ссылкой на наблюдение; задача на реализацию **не** создаётся в этой фазе (Single-Task Barrier).

## 4. План верификации (Verification Plan)

- [ ] Probe-ветка создана, workflow запущен на ней: `gh run view` показывает `success` для шага «Upload SARIF» и `failure` для шага линта (ожидаемо: битая ссылка).
- [ ] `code-scanning/alerts` содержит алерт с `rule.id = KB-001`, `path = docs/99_probe_broken.md`, `state = open`, `start_line = null` — JSON записан в `Devlog.md`.
- [ ] Алерт закрыт (`state = dismissed`), ветка удалена локально и на remote; `git branch -a` не содержит `probe/`.
- [ ] `code-scanning/alerts` на `main`: 0 открытых.
- [ ] `python -m unittest tests.test_kb_lint tests.test_ci_workflows` → OK (регрессов нет; код не менялся).
- [ ] Полный набор: `python scripts/run_tests_sandbox.py` → **191 тест OK**.
- [ ] `python scripts/kb_lint.py --path docs` → 0 битых ссылок, 0 `WARN`.
- [ ] `git status --porcelain` пуст; `install.py` не менялся.

* **Замеры $\ge 3$ прогонов:** не применимы.

### Visual DoD (для задач с GUI/TUI):

Поверхность — Security-панель. Скриншот `docs/assets/screenshots/code-scanning/TASK-109.png` желателен; при работе без UI — JSON-снимок алерта в `Devlog.md` (основное доказательство).

## 5. Критерии готовности (DoD)

- [ ] Наблюдение выполнено: реальный алерт `KB-001` получен, его форма (правило/путь/сообщение/отсутствие строки) записана в `Devlog.md`.
- [ ] Уборка выполнена: ветка удалена, алерт dismissed, открытых алертов на `main` — 0.
- [ ] `DEBT-004` либо в `Resolved Debt` с обоснованием, либо остаётся открытым с уточнённой формулировкой и записью в Icebox (исход B).
- [ ] `ADR-0032` содержит Amendments-раздел; `README.md` описывает итоговое поведение без ссылки на открытый долг (исход A).
- [ ] Полный набор тестов зелёный; `kb_lint` — 0 битых; статусы обновлены (ТЗ/Канбан/Roadmap), запись в `Devlog.md` — на шаге `/kb-complete`.
