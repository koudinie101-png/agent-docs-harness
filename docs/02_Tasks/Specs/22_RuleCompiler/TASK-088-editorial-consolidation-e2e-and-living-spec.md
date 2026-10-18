---
id: TASK-088
title: "Редакционная консолидация правил, E2E-синхронизация инсталлятора, Living Spec и пересборка dist/install.py"
status: done
type: task
phase: 22
component:
  - rules
  - installer
  - tests
  - docs
parent_plan: "[[../../Plans/PLAN-022-single-source-rule-compiler|PLAN-022]]"
created: 2026-10-18
updated: 2026-10-18
tags:
  - task/spec
  - phase22
  - rules
  - e2e
  - spec
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-088 — Редакционная консолидация правил, E2E, Living Spec и пересборка `dist/install.py`

> **ID:** TASK-088 | **Статус:** Выполнено (Режим 3)  
> **Фаза:** 22 | **План:** [[../../Plans/PLAN-022-single-source-rule-compiler|PLAN-022]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Предшественники:** [[../../Specs/22_RuleCompiler/TASK-085-rules-corpus-renderer-and-bundling|TASK-085]], [[../../Specs/22_RuleCompiler/TASK-086-agents-md-codegen-and-ci-check|TASK-086]], [[../../Specs/22_RuleCompiler/TASK-087-rules-drift-consistency-tests|TASK-087]]  
> **Нормативная база:** ADR-0030 (создаётся в [[../../Specs/22_RuleCompiler/TASK-085-rules-corpus-renderer-and-bundling|TASK-085]]), [[../../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]

---

## 1. Цель задачи

Закрыть Фазу 22 содержательной чисткой контента, которая стала возможной только после появления корпуса и Tier 1-защиты:

1. **Убрать числовой литерал из заголовка.** `## Docs-as-Code (20 Disciplines)` → `## Docs-as-Code Disciplines`. Число перестаёт быть данными, которые надо синхронизировать с содержимым.
2. **Достроить нумерованный индекс до полного.** Governance-правила (`TECH-DEBT`, `PRIOR-ART`, `TRACEABLE-TAGS`, `BENCHMARKS`) существуют только развёрнутыми секциями — в индексе их нет. Индекс становится полным (24 пункта), а секции остаются развёрнутой редакцией **без** собственных маркеров (ID живёт ровно в одном месте).
3. **Синхронизировать E2E и Living Spec** и пересобрать монолит `dist/install.py`.

## 2. Затрагиваемые файлы

* `[MODIFY]` `rules/AGENTS_CORE.md` — документ `client-agents`: заголовок без числа, индекс 1–24, перенос маркеров ID на пункты индекса.
* `[MODIFY]` `AGENTS.md` — регенерируется (`python scripts/gen_rules.py`), руками не правится.
* `[MODIFY]` `tests/test_installer.py` — ассерты заголовка и полноты индекса.
* `[MODIFY]` `SPEC.md` — раздел «Компилятор правил агентов» (`rules/AGENTS_CORE.md` → артефакты, `--check`).
* `[MODIFY]` `README.md` — как добавить правило (3 шага) и что `AGENTS.md` генерируется.
* `[MODIFY]` `docs/Onboarding.md` — рецепт «добавить правило» и место правки.
* `[MODIFY]` `install.py` — новый `EMBEDDED_ASSETS_B64` (результат сборки).
* `[MODIFY]` `dist/install.py` — зеркало бандла (результат сборки).

## 3. Детали реализации

### 3.1. Заголовок и индекс

* Заголовок: `## Docs-as-Code Disciplines` (без числа в любой форме).
* Индекс: пункты 1–20 сохраняют текущие тексты и порядок; после них добавляются 4 пункта:

```markdown
<!-- RULE: TECH-DEBT -->
21. **Tech Debt Governance:** Fix P1/P2 immediately; log every P3 finding and planned `#techdebt` refactoring as `DEBT-XXX` in `docs/02_Tasks/TechDebt.md`; migrate resolved rows to Resolved Debt in `/kb-complete`.
<!-- /RULE: TECH-DEBT -->
```

Аналогично: `PRIOR-ART` (22), `TRACEABLE-TAGS` (23), `BENCHMARKS` (24).

* Маркеры `RULE` для этих четырёх правил **переносятся** с развёрнутых секций на пункты индекса. Секции остаются, но теряют маркеры (текст сохраняется без изменений). Дубликат маркера — красный тест TASK-087.
* Пункт 20 (`FOUR-STATE-UI`) сохраняет свой ID; секция `## 🎨 7. The 4-State UI …` маркер не несёт (как и сейчас — проверить).

### 3.2. Синхронизация `AGENTS.md`

```bash
python scripts/gen_rules.py          # перезапись AGENTS.md из корпуса
python scripts/gen_rules.py --check  # Exit code 0
```

Ожидаемый дифф `AGENTS.md`: заголовок, +4 пункта индекса, перенос строк-маркеров. Текст развёрнутых секций не меняется.

### 3.3. Обновление `tests/test_installer.py`

* Найти ассерт `## Docs-as-Code (20 Disciplines)` и заменить на `## Docs-as-Code Disciplines`.
* Добавить проверки: `assertNotIn("(20 Disciplines)", generated)`; наличие `21.`…`24.` с `DEBT-XXX`, `Prior-Art`, `ROADMAP-`, `>= 3` соответственно.
* Сохранить существующие проверки `DEBT-XXX`, `#techdebt`, `Prior-Art Gate`, `ROADMAP-` в сгенерированных `AGENTS.md` и `GEMINI.md` (они не должны сломаться).

### 3.4. Living Spec

* `SPEC.md`: подраздел в §2 «Ключевые компоненты» — «Компилятор правил агентов»: `rules/AGENTS_CORE.md` как SSOT, артефакты (`AGENTS.md`, 6 адаптеров), `--check` в CI, запрет ручной правки.
* `README.md`: короткий блок «Как добавить правило» (1) правка корпуса, (2) `python scripts/gen_rules.py`, (3) `--check` / тесты.
* `docs/Onboarding.md`: тот же рецепт + пояснение, почему `AGENTS.md` помечен как GENERATED.

### 3.5. Пересборка

```bash
python scripts/build_installer.py
python -c "import install; a=install.unpack_assets(); print('rules/AGENTS_CORE.md' in a, len(a))"
```

Бандл обязан содержать корпус; `dist/install.py` — побайтово совпадать с обновлённым `install.py`.

## 4. План верификации (Verification Plan)

- [x] Гейт корпуса: `python scripts/gen_rules.py --check` (Exit code 0).
- [x] Полный прогон: `python -m unittest discover -s tests` (Exit code 0; включая `tests.test_rules_consistency` и `tests.test_rules_golden`).
- [x] E2E-установка: `python install.py --name Demo --stack python --agents all --no-git` во временном каталоге → `AGENTS.md` содержит `## Docs-as-Code Disciplines`, 24 пункта, `DEBT-XXX`; адаптеры ≤ 35 строк.
- [x] Сборка: `python scripts/build_installer.py` (Exit code 0), затем `python -c "print(open('dist/install.py',encoding='utf-8').read()==open('install.py',encoding='utf-8').read())"` → `True`.
- [x] Компиляция: `python -m py_compile install.py scripts/*.py` (Exit code 0).
- [x] Линтер: `python scripts/kb_lint.py --path docs` (0 broken links, Exit code 0).

## 5. Критерии готовности (DoD)

- [x] Заголовок без числового литерала; индекс содержит 24 пункта, ID каждого правила встречается ровно один раз.
- [x] `tests/test_installer.py` обновлён и зелёный; полный прогон — 100% pass.
- [x] `SPEC.md`, `README.md`, `docs/Onboarding.md` описывают новый порядок правки правил (Living Spec).
- [x] `install.py` и `dist/install.py` пересобраны и идентичны; бандл содержит корпус.
- [x] Статус обновлён в ТЗ, Канбане (`Done`), Плане (`PLAN-022`) и Дорожной карте (`[x]`); запись добавлена в `Devlog.md`.
