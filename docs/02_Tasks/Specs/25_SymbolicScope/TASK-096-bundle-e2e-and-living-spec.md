---
id: TASK-096
title: "Пересборка бандла, E2E и Living Spec Sync для символьного скоупа"
status: planned
type: task
phase: 25
component:
  - installer
  - e2e
  - docs
parent_plan: "[[../../Plans/PLAN-024-symbolic-scope-and-task-contracts|PLAN-024]]"
created: 2026-10-18
updated: 2026-10-18
tags:
  - task/spec
  - phase25
  - symbolic-scope
  - installer
  - e2e
  - spec
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-096 — Бандл, E2E и Living Spec Sync

> **ID:** TASK-096 | **Статус:** К реализации  
> **Фаза:** 25 | **План:** [[../../Plans/PLAN-024-symbolic-scope-and-task-contracts|PLAN-024]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0029-fine-grained-task-symbol-contracts-and-line-drift-rejection|ADR-0029]], [[../../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]] (бюджеты), [[TASK-094-symbolic-contract-templates-and-source-guard|TASK-094]], [[TASK-095-symbolic-behavior-and-advisory-lint|TASK-095]]

---

## 1. Цель задачи

Замкнуть Фазу 25 на **установленном** артефакте:

1. Пересобрать `install.py` / `dist/install.py`, включив новые шаблоны, скиллы и `check_symbolic_scope()`.
2. E2E: свежая установка содержит контракт и state-aware правило; `install.py --update` обновляет устаревшие шаблон/скилл, **не перезаписывая** пользовательские ТЗ.
3. Living Spec Sync: `SPEC.md` (§2.3, §2.4), `README.md` (скиллы и линтер), `docs/Onboarding.md` (Режимы 2 и 3) отражают символьный скоуп и state-aware next step.
4. Зафиксировать бюджеты после пересборки.

**Вне скоупа:** изменение логики шаблонов/скиллов/линтера (TASK-094/095); релиз v0.25.0 (`/kb-release`); техдолг (DEBT-001…003) — после релиза.

## 2. Затрагиваемые файлы и скоуп символов

* `[MODIFY]` `install.py`, `dist/install.py`:
  - Generated artifacts: только результат `python scripts/build_installer.py`; ручное редактирование `EMBEDDED_ASSETS_B64` запрещено.
* `[MODIFY]` `tests/test_installer.py`:
  - `TestAgentDocsHarness.test_phase25_symbolic_scope_bundle_and_update()`: новый E2E (§3.3).
* `[MODIFY]` `SPEC.md`:
  - §2.3: пункт про `check_symbolic_scope`; §2.4: формулировки Режимов 2 и 3 (§3.4).
* `[MODIFY]` `README.md`:
  - Таблица скиллов (`/kb-task`, `/kb-implement`, `/kb-complete`) и абзац про линтер (§3.5).
* `[MODIFY]` `docs/Onboarding.md`:
  - Режим 2 (файлы и символы) и Режим 3 (локализация и state-aware next step) (§3.6).

## 3. Детали реализации

### 3.1. Пересборка бандла

```bash
python scripts/build_installer.py
```

Команда обновляет `install.py` и зеркалит его в `dist/install.py`. Контроль:

* оба файла побайтово идентичны: `python -c "from pathlib import Path; assert Path('install.py').read_bytes()==Path('dist/install.py').read_bytes()"`;
* в бандл вошли: новые `TEMPLATE_TASK.md` / `TEMPLATE_TASK_MICRO.md`, `.agents/skills/kb-task|kb-implement|kb-complete/SKILL.md`, `scripts/kb_lint.py` с `check_symbolic_scope`;
* размер `install.py` — по бюджету §3.2.

### 3.2. Бюджет и риск переполнения

Текущие значения: `install.py` **173 887 B** (лимит 175 000), шаблоны **29 826 B** (лимит 30 000), скиллы **30 610 B** (лимит 31 000).

`check_symbolic_scope()` добавляет к `scripts/kb_lint.py` (52 593 B) ~3.6 KB исходного кода; после zlib/base64 ожидаемый прирост бандла — **~1.5–2.2 KB**. Риск: `install.py` может выйти за 175 000.

Порядок действий:
1. Пересобрать и замерить.
2. Если > 175 000 — сжать docstring/комментарии/константы `check_symbolic_scope()` без изменения поведения и пересобрать.
3. Если всё ещё > 175 000 — **остановиться и согласовать** повышение лимита до 176 000 с записью причины в `Devlog.md` и ADR-0009. Молчаливое повышение запрещено.
4. `test_16` проверяет `install ≤ 175 000`, `templates ≤ 30 000`, `skills ≤ 31 000`.

### 3.3. E2E в `tests/test_installer.py`

Метод класса `TestAgentDocsHarness`:

```python
    def test_phase25_symbolic_scope_bundle_and_update(self):
        """TASK-096: symbol-scope contract and state-aware skill ship in the bundle."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "SymbolicApp"
            target.mkdir()

            install.install_harness(
                target_dir=target,
                project_name="SymbolicApp",
                stack_key="python",
                agent_choice="all",
                git_choice="none",
                force=True,
            )

            task_tpl = (target / "docs" / "00_Templates" / "TEMPLATE_TASK.md").read_text(encoding="utf-8")
            self.assertIn("Затрагиваемые файлы и скоуп символов", task_tpl)
            self.assertIn("ClassName.method_name()", task_tpl)
            micro_tpl = (target / "docs" / "00_Templates" / "TEMPLATE_TASK_MICRO.md").read_text(encoding="utf-8")
            self.assertNotIn("строка или блок", micro_tpl)
            self.assertIn("символ(ы)", micro_tpl)

            task_skill = (target / ".agents" / "skills" / "kb-task" / "SKILL.md").read_text(encoding="utf-8")
            impl_skill = (target / ".agents" / "skills" / "kb-implement" / "SKILL.md").read_text(encoding="utf-8")
            complete_skill = (target / ".agents" / "skills" / "kb-complete" / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("nested symbols", task_skill)
            self.assertIn("symbol names", impl_skill)
            self.assertIn("only if its spec exists", complete_skill)

            deployed_lint = (target / "scripts" / "kb_lint.py").read_text(encoding="utf-8")
            self.assertIn("def check_symbolic_scope", deployed_lint)

            # Simulate stale harness artifacts and a user-owned spec.
            task_tpl_path = target / "docs" / "00_Templates" / "TEMPLATE_TASK.md"
            task_tpl_path.write_text("# Legacy task template\n", encoding="utf-8")
            complete_path = target / ".agents" / "skills" / "kb-complete" / "SKILL.md"
            complete_path.write_text("# Legacy complete skill\n", encoding="utf-8")

            user_spec = target / "docs" / "02_Tasks" / "Specs" / "01_MVP" / "TASK-099-user.md"
            user_spec.parent.mkdir(parents=True, exist_ok=True)
            user_body = (
                "---\nid: TASK-099\ntitle: User Task\nstatus: planned\ntype: task\n"
                "phase: 1\nparent_plan: PLAN-001\ncreated: 2026-10-18\n---\n"
                "# User TASK-099\nCustom content\n"
            )
            user_spec.write_text(user_body, encoding="utf-8")

            self.assertEqual(install.update_harness(target, backup=False), 0)

            refreshed_tpl = task_tpl_path.read_text(encoding="utf-8")
            self.assertIn("Затрагиваемые файлы и скоуп символов", refreshed_tpl)
            refreshed_complete = complete_path.read_text(encoding="utf-8")
            self.assertIn("only if its spec exists", refreshed_complete)
            self.assertEqual(user_spec.read_text(encoding="utf-8"), user_body)
```

Требования: герметичность (только `tempfile`, без сети/Git), проверка **установленного** артефакта, сохранение пользовательского ТЗ.

### 3.4. `SPEC.md`

1. §2.3 — после пункта `check_research_basis`:

```markdown
  * Неблокирующий контроль символьного скоупа задач (`check_symbolic_scope`): для активных задач (`planned`/`in-progress`) кодовые `[MODIFY]`/`[NEW]` без вложенного символа и маркеры `:L10-L20` дают `WARN:` (Exit code 0); `done`-спеки и fast-track не аудируются (ADR-0029).
```

2. §2.4 — Режим 2 заменить на:

```markdown
  * **Режим 2: Формирование ТЗ (Task Spec, `/kb-task`)** — точные контракты `[NEW]`/`[MODIFY]`/`[DELETE]` с иерархическим символьным скоупом (`Class.method()`, без номеров строк, ADR-0029), сигнатуры, DoD, план верификации с протоколом серийных замеров Benchmark Persistence. Запрет на редактирование кода!
```

3. §2.4 — Режим 3 заменить на:

```markdown
  * **Режим 3: Реализация (Implementation, `/kb-implement` & `/kb-complete`)** — написание кода задач (`TASK-XXX`) строго по ТЗ с локализацией по именам символов (не по номерам строк), исправление багов (`BUG-XXX`) строго по циклу TDD (**RED** failing test -> **GREEN** fix -> **REFACTOR** full test suite), Living Spec Sync, автоматическое закрытие карточки в Канбане, Дорожной карте и Devlog; state-aware next step: `/kb-implement TASK-YYY` только при существующей спеке, иначе `/kb-task TASK-YYY`.
```

4. Поле `updated` — 2026-10-18.

### 3.5. `README.md`

1. Строка `/kb-task`:

```markdown
| **`/kb-task`** | 🟠 Mode 2 (Spec) | Detailed file and symbol contracts (`[NEW]`/`[MODIFY]`/`[DELETE]` with nested `Class.method()`, no line numbers), DoD, verification plan. Read-only specification; focuses on contracts before implementation. |
```

2. Строка `/kb-implement`:

```markdown
| **`/kb-implement`** | 🟢 Mode 3 (Code) | Strict execution of ONE task spec (TASK-XXX) or defect fix (BUG-XXX via TDD), locating code by symbol names rather than line numbers, verification, auto-completion, and Stop & Yield Control. |
```

3. Строка `/kb-complete`:

```markdown
| **`/kb-complete`** | 🟢 Mode 3 (DoD) | Updates spec to `done` (or bug to `fixed`), moves Kanban card (with date), checks Roadmap, appends Devlog, verifies with `kb_lint.py`, and derives the next step from artifact state: `/kb-implement` only when the next spec exists, otherwise `/kb-task`. |
```

4. После абзаца про plan-provenance:

```markdown
  It also performs an advisory symbolic-scope check: an active task spec that lists a code file without a nested symbol, or uses `:L10-L20` anchors, prints a `WARN:` without failing the build (ADR-0029).
```

### 3.6. `docs/Onboarding.md`

1. Режим 2, пункт «Точный список файлов»:

```markdown
  - Точный список файлов и символов: `[NEW]`, `[MODIFY]`, `[DELETE]`; для кода — вложенный `Class.method()`, без номеров строк (ADR-0029).
```

2. Режим 3, пункт 1:

```markdown
  1. Код написан строго по спецификации с локализацией по именам символов, а не по номерам строк (ADR-0029); для `BUG-XXX` — цикл TDD: **RED** -> **GREEN** -> **REFACTOR**.
```

3. Режим 3, пункт 6 — добавить в конец:

```markdown
Следующий шаг state-aware: `/kb-implement` предлагается только при существующей спеке, иначе `/kb-task`.
```

### 3.7. Совместимость

* `--update` обновляет шаблоны/скиллы/линтер и **не** перезаписывает `docs/02_Tasks/Specs/*` (проверяется E2E).
* Исторические `done`-спеки и пользовательские ТЗ не мигрируются.
* `install.py` — только сгенерированный артефакт; ручные правки запрещены.

## 4. План верификации (Verification Plan)

- [ ] Пересборка: `python scripts/build_installer.py` → Exit code 0; `install.py` ≡ `dist/install.py`.
- [ ] Бюджеты: `install.py ≤ 175 000`, шаблоны ≤ 30 000, скиллы ≤ 31 000 (или согласованное повышение по §3.2); `test_16` зелёный.
- [ ] Полный прогон (sandbox-safe, [[../../../06_Memory/Incidents/INC-003-dsh-sandbox-tempfile-mkdtemp-mode|INC-003]] / TRG-03): `python tmp/run_tests.py` → **163 теста OK** (162 + 1 E2E), Exit code 0.
- [ ] E2E установленного артефакта: `test_phase25_symbolic_scope_bundle_and_update` → OK (свежая установка + `--update` + сохранение пользовательского ТЗ).
- [ ] Living Spec: `SPEC.md`, `README.md`, `docs/Onboarding.md` синхронизированы (§3.4–§3.6).
- [ ] Целостность: `python scripts/kb_lint.py --path docs` → Exit code 0, 0 битых ссылок, 0 `Symbolic Scope Warnings`.
- [ ] 4-State UI / скриншоты: не применимо (GUI/TUI отсутствует).
- [ ] Замеры $\ge 3$ прогонов: не применимо — статические байтовые бюджеты детерминированы.

## 5. Критерии готовности (DoD)

- [ ] `install.py` и `dist/install.py` пересобраны, идентичны, содержат новые шаблоны, скиллы и `check_symbolic_scope`.
- [ ] Бюджеты зафиксированы; при превышении 175 000 — согласованное решение, а не молчаливый рост.
- [ ] E2E свежей установки и `--update` зелёный; пользовательское ТЗ не перезаписано.
- [ ] `SPEC.md` §2.3/§2.4, `README.md`, `docs/Onboarding.md` синхронизированы.
- [ ] Полный suite и `kb_lint` зелёные.
- [ ] Статус задачи обновлён в [[../../Kanban|Kanban]] и [[../../Roadmap|Roadmap]] на шаге `/kb-complete`.
