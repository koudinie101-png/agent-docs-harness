---
id: TASK-099
title: "Пермалинк спеки в Roadmap при /kb-task"
status: planned
type: fast-track
phase: 26
component:
  - skills
  - tests
parent_plan: "[[../../Roadmap|Roadmap.md (Фаза 26)]]"
created: 2026-10-18
updated: 2026-10-18
tags:
  - task/spec
  - fast-track
  - phase26
  - process
  - roadmap
kanban: "[[../../Kanban|Канбан-доска]]"
---

# ⚡ Спецификация (Fast-Track): TASK-099 — Пермалинк спеки в Roadmap

> **Тип:** Fast-Track (≤ 30 LOC) | **Статус:** К реализации  
> **Фаза:** 26 | **Канбан:** [[../../Kanban|Канбан-доска]]

---

## 1. Цель и контекст

При создании TASK-098 обнаружился системный gap: `/kb-task` обновляет Kanban, но **не** вставляет пермалинк новой спеки в `Roadmap.md`. Ссылка появляется только на `/kb-complete`, поэтому всё время реализации задача не видна из дорожной карты (TASK-098 пришлось линковать вручную).

Исправить в `/kb-task`:
* при создании спеки заменять plain `TASK-XXX` в строке целевой фазы на `[[Specs/<Phase_Folder>/TASK-XXX-<slug>|TASK-XXX]]`, сохраняя `[ ]`;
* `/kb-complete` по-прежнему меняет `[ ]` на `[x]` и не дублирует ссылку.

Если строки фазы в Roadmap нет — не выдумывать фазу, а сообщить пользователю (Human Guardrails).

## 2. Контракт файлов

* `[MODIFY]` `.agents/skills/kb-task/SKILL.md` — шаг 5 (Kanban + Roadmap) и шаг 6 (staging Roadmap).
* `[MODIFY]` `tests/test_installer.py`:
  - `TestAgentDocsHarness.test_symbolic_scope_and_state_aware_skill_guards()`: + маркеры `Roadmap.md` и формата ссылки.

## 3. Детали реализации

### 3.1. `/kb-task` — шаги 5–6

Заменить шаг 5 и staging в шаге 6 на:

```markdown
5. **Update Kanban & Roadmap:**
   - Move or add task card in `docs/02_Tasks/Kanban.md` to `## ⏳ В работе (In Progress)`.
   - In `docs/02_Tasks/Roadmap.md`, replace the plain `TASK-XXX` item in the target phase with `[[Specs/<Phase_Folder>/TASK-XXX-<slug>|TASK-XXX]]`, keeping `[ ]`; `/kb-complete` flips it to `[x]`. If no phase line exists, do not invent a phase — report it.
6. **Git Sync (Conditional):**
   - Stage: `git add docs/02_Tasks/Specs/ docs/02_Tasks/Kanban.md docs/02_Tasks/Roadmap.md`
```

Требования: ссылка добавляется один раз; при повторном `/kb-task` для той же спеки не дублируется. `/kb-complete` не должен создавать вторую ссылку.

### 3.2. Tier 1 source-guard

В существующий `test_symbolic_scope_and_state_aware_skill_guards` (файл `tests/test_installer.py`, читает `.agents/skills/...` напрямую) добавить:

```python
        self.assertIn("Roadmap.md", task_skill)
        self.assertIn("[[Specs/<Phase_Folder>/TASK-XXX-<slug>|TASK-XXX]]", task_skill)
```

Тест не увеличивает их количество: это расширение существующего метода (полный suite остаётся 165 тестов).

### 3.3. Пересборка бандла

Скилл входит в `EMBEDDED_ASSETS`, поэтому после правки:

```bash
python scripts/build_installer.py
```

`install.py` и `dist/install.py` — generated artifacts, вручную не редактируются. Ожидаемый размер ~175.2–175.4 KB; лимит 176 000 B. Бюджет скиллов: 30 610 + ~300 → ≤ 31 000.

## 4. План верификации (Verification Plan)

- [ ] Tier 1 source-guard: `python -m unittest tests.test_installer.TestAgentDocsHarness.test_symbolic_scope_and_state_aware_skill_guards` → OK.
- [ ] Синтаксис: `python -m py_compile tests/test_installer.py` → Exit code 0.
- [ ] Пересборка: `python scripts/build_installer.py` → Exit code 0; `install.py` ≡ `dist/install.py`; размер ≤ 176 000 B.
- [ ] Полный прогон (sandbox-safe, [[../../../06_Memory/Incidents/INC-003-dsh-sandbox-tempfile-mkdtemp-mode|INC-003]] / TRG-03): `python tmp/run_tests.py` → **165 тестов OK**; бюджеты `test_16` зелёные.
- [ ] Целостность: `python scripts/kb_lint.py --path docs` → Exit code 0, 0 битых ссылок.
- [ ] `git diff --check` → без trailing whitespace.
- [ ] 4-State UI / скриншоты: не применимо.
- [ ] Замеры $\ge 3$ прогонов: не применимо (статические байтовые бюджеты).

## 5. Критерии готовности (DoD)

- [ ] `/kb-task` содержит правило пермалинка и staging Roadmap; повторный запуск не дублирует ссылку.
- [ ] Tier 1 source-guard расширен и зелёный; полный suite (165) и `kb_lint` зелёные.
- [ ] Бандл пересобран, `install.py` ≡ `dist/install.py`, бюджет ≤ 176 000 B; скиллы ≤ 31 000 B.
- [ ] Статус обновлён в Kanban, Roadmap и Devlog.
