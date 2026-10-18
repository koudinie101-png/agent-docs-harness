---
id: TASK-087
title: "Tier 1 тесты дрейфа правил (tests/test_rules_consistency.py): инвентарь, выводимость адаптеров и hard-proof"
status: planned
type: task
phase: 22
component:
  - tests
  - rules
  - quality-gates
parent_plan: "[[../../Plans/PLAN-022-single-source-rule-compiler|PLAN-022]]"
created: 2026-10-18
updated: 2026-10-18
tags:
  - task/spec
  - phase22
  - ssot
  - tests
  - quality-gates
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-087 — Tier 1 тесты дрейфа правил

> **ID:** TASK-087 | **Статус:** К реализации  
> **Фаза:** 22 | **План:** [[../../Plans/PLAN-022-single-source-rule-compiler|PLAN-022]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Предшественники:** [[../../Specs/22_RuleCompiler/TASK-085-rules-corpus-renderer-and-bundling|TASK-085]], [[../../Specs/22_RuleCompiler/TASK-086-agents-md-codegen-and-ci-check|TASK-086]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]] (критичное правило не живёт только в Tier 3)

---

## 1. Цель задачи

Закрепить инварианты корпуса механически (Tier 1), чтобы дрейф правил ловился тестом, а не следующей фазой ремонтных задач.

Проверяется не текст правил (это дело golden-фикстур из TASK-085), а **структурная целостность**: идентификаторы, полнота инвентаря, выводимость адаптеров, отсутствие служебных маркеров и плейсхолдеров в артефактах, детерминизм и честное падение без корпуса.

## 2. Затрагиваемые файлы

* `[NEW]` `tests/test_rules_consistency.py` — набор инвариантов (структура ниже).
* `[MODIFY]` `docs/06_Memory/patterns.md` — **только если** в ходе реализации обнаружатся повторяющиеся процедурные ошибки (по протоколу памяти); иначе файл не трогается.

## 3. Детали реализации

### 3.1. Канонический инвентарь (пин)

В тесте фиксируется список `CANONICAL_RULES` — 20 дисциплин + 4 governance-правила + 4 документных блока:

| Группа | Идентификаторы |
| :--- | :--- |
| Дисциплины (20) | `SESSION-READ`, `KANBAN`, `ROADMAP`, `ADR`, `RESEARCH`, `DEVLOG`, `OBSIDIAN`, `PERMALINKS`, `REGRESSION-FIRST`, `QA-CHECKLISTS`, `GRAPH-COLORS`, `GIT-FLOW`, `SINGLE-TASK`, `ZERO-STATE`, `FEEDBACK-TRIAGE`, `HUMAN-GUARDRAILS`, `FAST-TRACK`, `ZERO-ROUNDTRIP`, `QUALITY-GATES`, `FOUR-STATE-UI` |
| Governance (4) | `TECH-DEBT`, `PRIOR-ART`, `TRACEABLE-TAGS`, `BENCHMARKS` |
| Документные блоки (4) | `KB-STANDARD`, `ANTI-ECHO`, `SENIOR-PARTNER`, `LIFECYCLE` |

Список — контракт: добавление правила меняет и корпус, и пин в одном коммите, иначе тест краснеет.

### 3.2. Инварианты

1. **Документы:** `corpus` содержит ровно `client-agents`, `adapters`, `harness-agents`.
2. **Уникальность:** внутри каждого документа каждый `RULE`-ID встречается один раз (дубль маркера — `AssertionError` с именем ID и документа).
3. **Полнота клиента:** множество ID документа `client-agents` == `CANONICAL_RULES`.
4. **Выводимость адаптеров:** документ `adapters` содержит ровно 10 правил, и каждый его ID ∈ `CANONICAL_RULES` (третьего инвентаря нет).
5. **Полнота харнесса:** `harness-agents` содержит 16 принципов + `KB-STANDARD`, `ANTI-ECHO`, `SENIOR-PARTNER`, `LIFECYCLE`; все ID ∈ `CANONICAL_RULES`.
6. **Чистота вывода:** в отрендеренных `client-agents`, `adapters`, `harness-agents` нет подстрок `<!-- RULE`, `<!-- /RULE`, `<!-- DOCUMENT`.
7. **Подстановка:** в отрендеренном выводе нет `{{` и `}}`.
8. **Детерминизм:** два последовательных рендера одного документа равны побайтово.
9. **Honest failure:** при пустом корпусе `_load_rules_corpus()` поднимает `RuntimeError`, текст содержит `rules/AGENTS_CORE.md` (подмена источника через monkeypatch, без правки файлов).
10. **Нет утечки корпуса:** `deploy_infrastructure()` во временном каталоге не создаёт файл `AGENTS_CORE.md` ни в `docs/`, ни в `docs/00_Templates/`; при этом шаблонов ровно 16.
11. **Гейт:** `gen_rules.check_current(rendered=...)` возвращает `(True, "")` для корректного рендера и `(False, diff)` для испорченного — без чтения/записи `AGENTS.md` (чистая функция, введена в TASK-086).

### 3.3. Требования к тестам

* `unittest`, без внешних зависимостей; временные каталоги — через `tempfile` и `addCleanup`.
* Каждый инвариант — отдельный `test_*` с сообщением, называющим нарушенный ID/документ.
* Тест не должен зависеть от текущего каталога (`REPO_ROOT` от `__file__`).
* Windows-совместимость: сравнение текстов после нормализации `\r\n` → `\n`.

## 4. План верификации (Verification Plan)

- [ ] Новый набор: `python -m unittest tests.test_rules_consistency -v` (Exit code 0, ≥ 11 тестов).
- [ ] Красный сценарий (вручную): удалить маркер `RULE: SINGLE-TASK` из `client-agents` во временной копии корпуса → тест полноты падает с понятным сообщением (файл восстановить).
- [ ] Полный прогон: `python -m unittest discover -s tests` (Exit code 0).
- [ ] Компиляция: `python -m py_compile install.py scripts/*.py` (Exit code 0).
- [ ] Линтер: `python scripts/kb_lint.py --path docs` (0 broken links, Exit code 0).

## 5. Критерии готовности (DoD)

- [ ] `tests/test_rules_consistency.py` покрывает 11 инвариантов раздела 3.2.
- [ ] Канонический инвентарь запинен и падает при добавлении правила без обновления пина.
- [ ] Тесты не пишут в репозиторий и не зависят от текущего каталога.
- [ ] Полный прогон зелёный; дрейф любого из трёх артефактов ловится тестом.
- [ ] Статус обновлён в ТЗ, Канбане (`Done`) и Дорожной карте (`[x]`); запись добавлена в `Devlog.md`.
