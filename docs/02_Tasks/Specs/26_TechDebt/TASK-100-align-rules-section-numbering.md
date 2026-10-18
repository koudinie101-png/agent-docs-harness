---
id: TASK-100
title: "Выравнивание нумерации разделов корпуса правил (DEBT-001)"
status: planned
type: task
phase: 26
component:
  - rules
  - tests
  - installer
parent_plan: "[[../../TechDebt|TechDebt.md]]"
created: 2026-10-18
updated: 2026-10-18
tags:
  - task/spec
  - phase26
  - techdebt
  - rules
  - tests
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-100 — Выравнивание нумерации разделов корпуса правил

> **ID:** TASK-100 | **Статус:** К реализации  
> **Фаза:** 26 (Tech Debt Hardening) | **Канбан:** [[../../Kanban|Канбан-доска]]  
> **Долг:** [[../../TechDebt|DEBT-001]] — закрывается этой задачей.  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0030-single-source-rule-compiler|ADR-0030]] (единый корпус), [[../../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]] (Tier 1)

---

## 1. Цель задачи

Закрыть `DEBT-001`: в документе `client-agents` корпуса `rules/AGENTS_CORE.md` шесть развёрнутых секций сохранили нумерацию **6–11** от старой редакции, хотя индекс дисциплин давно 1–24. Числа в заголовках дублируют дисциплины 14/20/21/22/23/24 и создают ложное впечатление, что после списка идёт продолжение с шестого пункта.

Исправление: убрать числовые префиксы у шести заголовков, не меняя текст, эмодзи и `RULE`-маркеры. Затем перегенерировать 12 golden-фикстур `client_agents` и пересобрать бандл. `AGENTS.md` в корне рендерится из документа `harness-agents` и этих заголовков не содержит — проверяется `gen_rules.py --check` (ожидается отсутствие диффа).

Дополнительно: Tier 1 тест против повторного появления нумерованных `##`-заголовков в `client-agents`.

## 2. Затрагиваемые файлы и скоуп символов

* `[MODIFY]` `rules/AGENTS_CORE.md`:
  - `## 🛡️ 6. Zero-State…` → `## 🛡️ Zero-State…` (и ещё пять заголовков, §3.1).
* `[MODIFY]` `tests/fixtures/rules/client_agents__*.txt`:
  - 12 golden-фикстур перегенерируются из `install.generate_agents_md("Demo", <stack>, <lang>)`.
* `[MODIFY]` `tests/test_rules_consistency.py`:
  - `RulesConsistencyTest.test_client_agents_sections_are_unnumbered()`: Tier 1 guard.
* `[MODIFY]` `install.py`, `dist/install.py`:
  - Generated artifacts: `python scripts/build_installer.py` (manual symbols not applicable).

## 3. Детали реализации

### 3.1. Шесть заголовков `client-agents`

Убрать только числовой префикс (`6. `, `7. `, …); остальной текст не менять:

```markdown
## 🛡️ 6. Zero-State Anti-Hallucination & Spec Genesis        → ## 🛡️ Zero-State Anti-Hallucination & Spec Genesis
## 🎨 7. The 4-State UI & Visual Verification Invariant      → ## 🎨 The 4-State UI & Visual Verification Invariant
## 💳 8. Tech Debt Governance & End-to-End Lifecycle (P1/P2 vs P3) → ## 💳 Tech Debt Governance & End-to-End Lifecycle (P1/P2 vs P3)
## 🏛️ 9. Prior-Art Gate Invariant                            → ## 🏛️ Prior-Art Gate Invariant
## 🏷️ 10. Traceable Backlog Tags (// ROADMAP-<ID> and // DEBT-XXX) → ## 🏷️ Traceable Backlog Tags (// ROADMAP-<ID> and // DEBT-XXX)
## ⏱️ 11. Benchmark Persistence («Замер = артефакт»)          → ## ⏱️ Benchmark Persistence («Замер = артефакт»)
```

Не трогать нумерованный список дисциплин 1–24, `RULE`-маркеры, `DOCUMENT`-границы и `harness-agents`.

### 3.2. Перегенерация golden-фикстур

После правки корпуса выполнить (из корня репозитория; `tmp/` gitignored):

```bash
python -c "import sys; from pathlib import Path; sys.path.insert(0,'.'); import install; f=Path('tests/fixtures/rules'); [ (f/('client_agents__%s__%s.txt'%(s,l))).write_text(install.generate_agents_md('Demo',s,l),encoding='utf-8') for s in ['swift','ts','python','dotnet','generic','undecided'] for l in ['ru','en'] ]"
```

Проверить, что изменились только 12 `client_agents__*.txt`; `adapter__*.txt` не должны затрагиваться.

### 3.3. Tier 1 guard

Добавить в `RulesConsistencyTest` (`tests/test_rules_consistency.py`):

```python
    def test_client_agents_sections_are_unnumbered(self):
        body = self.corpus["client-agents"]
        numbered = re.findall(r"^##\s+[^\n]*\b\d{1,2}\.\s", body, re.MULTILINE)
        self.assertEqual(numbered, [], "client-agents section headings must not carry stale numbers")
```

Тест читает корпус через уже существующий `self.corpus` (setUp сбрасывает кэш `install._RULES_CORPUS_CACHE`).

### 3.4. `AGENTS.md` и бандл

* `python scripts/gen_rules.py --check` → OK; при неожиданном диффе выполнить `python scripts/gen_rules.py` и включить `AGENTS.md` в задачу.
* `python scripts/build_installer.py` → пересборка `install.py` / `dist/install.py`; оба файла идентичны. Ожидаемый размер ~175.1 KB (лимит 176 000 B); удаление префиксов немного уменьшает бандл.

## 4. План верификации (Verification Plan)

- [ ] Golden: `python -m unittest tests.test_rules_golden` → 3 теста OK (12 клиентских подтестов).
- [ ] Структура: `python -m unittest tests.test_rules_consistency` → все тесты OK (+1 новый guard).
- [ ] Дрейф корпуса: `python scripts/gen_rules.py --check` → Exit code 0.
- [ ] Пересборка: `python scripts/build_installer.py` → Exit code 0; `install.py` ≡ `dist/install.py`; размер ≤ 176 000 B.
- [ ] Полный прогон (sandbox-safe, [[../../../06_Memory/Incidents/INC-003-dsh-sandbox-tempfile-mkdtemp-mode|INC-003]] / TRG-03): `python tmp/run_tests.py` → **166 тестов OK** (165 + 1), Exit code 0.
- [ ] Целостность: `python scripts/kb_lint.py --path docs` → Exit code 0, 0 битых ссылок.
- [ ] `git diff --check` → без trailing whitespace.
- [ ] 4-State UI / скриншоты: не применимо.
- [ ] Замеры $\ge 3$ прогонов: не применимо (статические байтовые бюджеты).

## 5. Критерии готовности (DoD)

- [ ] Шесть заголовков `client-agents` без числовых префиксов; дисциплины 1–24 и `RULE`-маркеры не изменены.
- [ ] 12 golden-фикстур перегенерированы; `test_rules_golden` и новый Tier 1 guard зелёные.
- [ ] `AGENTS.md` без дрейфа (`gen_rules.py --check`); `install.py` ≡ `dist/install.py` ≤ 176 000 B.
- [ ] Полный suite (166) и `kb_lint` зелёные.
- [ ] `DEBT-001` переведён в `Resolved Debt` со ссылкой на `TASK-100` на шаге `/kb-complete`.
- [ ] Статус обновлён в Kanban, Roadmap и Devlog.
