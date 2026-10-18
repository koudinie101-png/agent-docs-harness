---
id: TASK-085
title: "Корпус правил rules/AGENTS_CORE.md, рендерер в install.py, упаковка в бандл и ADR-0030"
status: planned
type: task
phase: 22
component:
  - installer
  - rules
parent_plan: "[[../../Plans/PLAN-022-single-source-rule-compiler|PLAN-022]]"
created: 2026-10-18
updated: 2026-10-18
tags:
  - task/spec
  - phase22
  - ssot
  - rules
  - installer
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-085 — Корпус правил `rules/AGENTS_CORE.md`, рендерер в `install.py`, упаковка в бандл и ADR-0030

> **ID:** TASK-085 | **Статус:** К реализации  
> **Фаза:** 22 | **План:** [[../../Plans/PLAN-022-single-source-rule-compiler|PLAN-022]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]] (Zero-Deps), [[../../../03_Decisions_ADR/ADR-0021-rules-layering-thin-forwarders-and-obsidian-taxonomy|ADR-0021]] (тонкие адаптеры), [[../../../03_Decisions_ADR/ADR-0029-fine-grained-task-symbol-contracts-and-line-drift-rejection|ADR-0029]] (символьный скоуп), [[../../../03_Decisions_ADR/ADR-0031-research-evidence-gate-for-icebox-promotion|ADR-0031]] (research_basis)

---

## 1. Цель задачи

Извлечь три существующих в коде представления правил агента в один data-файл `rules/AGENTS_CORE.md`, добавить детерминированный рендерер и упаковать корпус в бандл — **без изменения генерируемого вывода**.

Задача сознательно является «извлечением, а не редактированием»: контент правил, порядок, нумерация и формулировки остаются прежними. Это позволяет сменить источник данных под защитой golden-фикстур, а редакционную чистку (числовой литерал, полнота индекса) выполнить отдельно в [[../../Specs/22_RuleCompiler/TASK-088-editorial-consolidation-e2e-and-living-spec|TASK-088]].

**Границы скоупа:**
* Переносится: `install.py` → `_RULES_BODY`, тело `generate_agents_md()`, тело `_gen_rule()` (список из 10 правил).
* Не переносится: `STACK_PRESETS`, заголовки документов, `generate_tech_debt_md()`, README-политика, скиллы.
* Не меняется: публичные сигнатуры генераторов, текст правил, `AGENTS.md` (это [[../../Specs/22_RuleCompiler/TASK-086-agents-md-codegen-and-ci-check|TASK-086]]).

## 2. Затрагиваемые файлы

* `[NEW]` `rules/AGENTS_CORE.md` — единый корпус: документы `client-agents`, `adapters`, `harness-agents` с маркерами `RULE` и плейсхолдерами.
* `[NEW]` `tests/fixtures/rules/` — golden-снимки вывода генераторов, снятые **до** рефакторинга.
* `[NEW]` `tests/test_rules_golden.py` — сравнение рендера с фикстурами.
* `[NEW]` `docs/03_Decisions_ADR/ADR-0030-single-source-rule-compiler.md` — `status: accepted`.
* `[MODIFY]` `install.py`:
  * `_load_rules_corpus()` — новая: загрузка и кэширование корпуса.
  * `_render_rules_document()` — новая: подстановка плейсхолдеров и удаление маркеров.
  * `_rules()` — делегирует рендеру документа `client-agents`.
  * `_gen_rule()` — делегирует рендеру документа `adapters`.
  * `generate_agents_md()` — собирает документ `client-agents` целиком.
  * `_RULES_BODY` — удаляется (текст уезжает в корпус).
  * `unpack_assets()` — добавляет `rules/AGENTS_CORE.md` в local-fallback.
* `[MODIFY]` `scripts/build_installer.py`: `bundle_assets()` — ключ `rules/AGENTS_CORE.md` в бандле.

## 3. Детали реализации

### 3.1. Формат корпуса `rules/AGENTS_CORE.md`

Файл состоит из трёх документов. Документ открывается и закрывается служебными комментариями, внутри — тело с маркерами правил:

```markdown
<!-- DOCUMENT: client-agents -->
## Docs-as-Code (20 Disciplines)
Language: {{lang_instruction}}
<!-- RULE: SESSION-READ -->
1. Read `SPEC.md`, `docs/00_Index.md`, `docs/Onboarding.md` at session start; sync `SPEC.md`/`README.md` (Living Spec).
<!-- /RULE: SESSION-READ -->
...
<!-- /DOCUMENT: client-agents -->
```

* Идентификатор `RULE` — семантический ключ в `UPPER-KEBAB-CASE` (`SESSION-READ`, `SINGLE-TASK`, `FOUR-STATE-UI`, …), а не номер: номера переезжают при вставке правила, ключи — нет.
* Маркеры `<!-- RULE: … -->`, `<!-- /RULE: … -->`, `<!-- DOCUMENT: … -->` **удаляются** при рендере (в выводе остаётся ровно тот текст, который был до рефакторинга).
* Документ `adapters` содержит 10 правил адаптеров; `harness-agents` — весь корневой `AGENTS.md` (RU), включая KB Standard, Anti-Echo, Critical Thinking и Lifecycle.

### 3.2. Плейсхолдеры

Подстановка выполняется **последовательным `str.replace()`**, не `str.format()` (в тексте есть литеральные фигурные скобки и код-фенсы).

| Плейсхолдер | Источник |
| :--- | :--- |
| `{{project}}` | `project_name` |
| `{{stack_name}}` | `STACK_PRESETS[stack_key]["name"]` |
| `{{stack_language}}` | `STACK_PRESETS[stack_key]["language"]` |
| `{{build_cmd}}` / `{{test_cmd}}` | `STACK_PRESETS[stack_key]` |
| `{{file_ext}}` | `STACK_PRESETS[stack_key]["file_ext"]` |
| `{{lang_instruction}}` | `_rules()`: RU/EN-строка про язык докс |
| `{{skills_tail}}` | хвост `generate_gemini_md()` |

Незаполненный плейсхолдер — ошибка рендера (`RuntimeError` с именем плейсхолдера и документа), а не тихий пропуск.

### 3.3. Рендерер

```python
RULES_CORPUS_KEY = "rules/AGENTS_CORE.md"

def _load_rules_corpus() -> dict:
    """Return {document_name: raw_body}. Cached per process; raises RuntimeError if absent."""

def _render_rules_document(name: str, values: dict) -> str:
    """Strip RULE/DOCUMENT markers, substitute {{placeholders}}, raise on leftovers."""
```

* Источник: `unpack_assets()` (бандл → local-fallback). Если ключа нет — `RuntimeError` с указанием `rules/AGENTS_CORE.md` и подсказкой запустить `scripts/build_installer.py`.
* Кэш — модульная переменная; повторный вызов не перечитывает бандл.
* Маркеры удаляются построчно, чтобы не ломать пустые строки вокруг правил.

### 3.4. Golden-фикстуры (обязательный первый шаг)

1. **До** рефакторинга снять текущий вывод и закоммитить:
   * `generate_agents_md("Demo", stack, lang)` для `stack ∈ {python, ts, dotnet, generic, undecided}`, `lang ∈ {ru, en}`;
   * шесть адаптеров через `get_agent_rule_specs()` для `stack=python`, `lang ∈ {ru, en}`.
2. Фикстуры кладутся в `tests/fixtures/rules/<name>.txt` (UTF-8, LF).
3. `tests/test_rules_golden.py` рендерит те же входы после рефакторинга и сравнивает **побайтово** (после нормализации `\r\n` → `\n`).

### 3.5. Упаковка

* `bundle_assets()` читает `rules/AGENTS_CORE.md` и кладёт в словарь под ключом `rules/AGENTS_CORE.md`; при отсутствии файла — `RuntimeError` (сборка не должна выпускать бандл без корпуса).
* `deploy_infrastructure()` **не** должен писать корпус в `docs/` целевого проекта: префикс `rules/` не обслуживается ни одной веткой. Поведение закрепляется тестом в [[../../Specs/22_RuleCompiler/TASK-087-rules-drift-consistency-tests|TASK-087]].

### 3.6. ADR-0030

Зафиксировать: контекст (три инвентаря), решение (корпус + рендерер), отвергнутые варианты (компиляция из корневого `AGENTS.md`, Jinja2/Mako, две билингвальные копии, правила в Python-структуре), последствия (генерируемый `AGENTS.md`, `--check` в CI). Ссылки: [[../../Plans/PLAN-022-single-source-rule-compiler|PLAN-022]], [[../../../03_Decisions_ADR/ADR-0031-research-evidence-gate-for-icebox-promotion|ADR-0031]].

## 4. План верификации (Verification Plan)

- [ ] Компиляция: `python -m py_compile install.py scripts/*.py` (Exit code 0).
- [ ] Golden-тесты: `python -m unittest tests.test_rules_golden -v` (Exit code 0, 0 diff).
- [ ] Полный прогон: `python -m unittest discover -s tests` (Exit code 0 — рефакторинг не меняет поведение).
- [ ] Сборка бандла: `python scripts/build_installer.py` (Exit code 0).
- [ ] Корпус в бандле: `python -c "import install; print('rules/AGENTS_CORE.md' in install.unpack_assets())"` → `True`.
- [ ] Отсутствие корпуса: временно переименовать `rules/AGENTS_CORE.md` → `install.generate_agents_md('D','python')` поднимает `RuntimeError` (проверка вручную, файл вернуть).
- [ ] Линтер базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links, Exit code 0).

## 5. Критерии готовности (DoD)

- [ ] Корпус `rules/AGENTS_CORE.md` содержит три документа и маркеры `RULE` для каждого правила.
- [ ] Golden-фикстуры совпадают побайтово; `_RULES_BODY` удалён из `install.py`.
- [ ] Сигнатуры `generate_agents_md()`, `_gen_rule()`, `_rules()`, `get_agent_rule_specs()` не изменены.
- [ ] Корпус упакован в бандл и доступен в local-fallback; в `docs/` клиента не попадает.
- [ ] `ADR-0030` создан со `status: accepted` и отвергнутыми альтернативами.
- [ ] Статус обновлён в ТЗ, Канбане (`Done`) и Дорожной карте (`[x]`); запись добавлена в `Devlog.md`.
