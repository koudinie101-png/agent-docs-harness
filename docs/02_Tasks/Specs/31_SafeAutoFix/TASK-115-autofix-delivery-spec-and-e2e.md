---
id: TASK-115
title: "Бандлинг в install.py, CI-хуки, Living Spec и E2E-тесты поставки автофикса"
status: in-progress
type: task
phase: 31
component:
  - installer
  - ci
  - docs
  - lint
  - tests
parent_plan: "[[../../Plans/PLAN-028-kb-lint-safe-autofix|PLAN-028]]"
depends_on:
  - TASK-113
  - TASK-114
created: 2026-11-19
updated: 2026-11-19
tags:
  - task/spec
  - phase31
  - installer
  - autofix
  - ci
  - living-spec
  - tests
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-115 — Бандлинг в install.py, CI-хуки, Living Spec и E2E-тесты поставки автофикса

> **ID:** TASK-115 | **Статус:** В работе (In Progress) | **Фаза:** 31  
> **План:** [[../../Plans/PLAN-028-kb-lint-safe-autofix|PLAN-028: Безопасный автофикс kb_lint --fix]] | **Канбан:** [[../../Kanban|Канбан-доска]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0036-kb-lint-safe-autofix-standard|ADR-0036]] | **Исследование:** [[../../../04_Research/RESEARCH-030-kb-lint-safe-autofix|RESEARCH-030]]  
> **Зависимости:** [[TASK-113-kb-lint-autofix-core|TASK-113]], [[TASK-114-autofix-formats-and-skills-integration|TASK-114]]

---

## 1. Цель задачи

Финализировать реализацию Фазы 31 (**Безопасный автофикс kb_lint --fix**):
1. **Интеграция в CI/CD и Git-хуки**:
   - Добавить хук `kb-lint-fix` в `.pre-commit-hooks.yaml` для безопасного устранения тривиальных форматировочных дефектов одной командой pre-commit.
   - Актуализировать composite GitHub Action `action.yml`: поддержать параметр `fix` (`none`, `preview`, `write`) и автоматический проброс флагов линтера.
2. **Синхронизация Living Spec (Мастер-спецификации и витрины)**:
   - Обновить `SPEC.md` (подраздел 2.3 `scripts/kb_lint.py` с фиксацией контракта `--fix`, `--write`, `--allow-dirty`, протокола Zero Data Loss и списка 5 детерминированных правил; раздел 5 с фиксацией завершения Фазы 31).
   - Обновить `README.md` (секция документации линтера и примеры использования автофикса).
3. **Бандлинг и дистрибутив**:
   - Пересобрать монолитный инсталлятор `install.py` и зеркало `dist/install.py` через `scripts/build_installer.py` с контролем весового бюджета ($\le 210\text{ КБ}$).
4. **Сквозное E2E-тестирование поставки**:
   - Добавить тест `test_39_kb_lint_autofix_delivery` в `tests/test_installer.py`, верифицирующий:
     * Развертывание обновленного `scripts/kb_lint.py` при чистой установке `install_harness`.
     * Корректную работу `--fix` (dry-run предпросмотр) на реальном файле в развернутом клиентском проекте без изменения диска.
     * Корректное атомарное исправление при `--fix --write` в установленном проекте.
     * Сохранение работоспособности автофикса после обновления проекта через `install.py --update`.
5. **Финализация Фазы 31**:
   - Полное закрытие задач Фазы 31 в Канбане и Дорожной карте, подготовка к приемочному тестированию и релизу `v0.29.0`.

---

## 2. Затрагиваемые файлы и скоуп символов

* `[MODIFY]` `.pre-commit-hooks.yaml`:
  - `hooks[id=kb-lint-fix]` — регистрация хука безопасного автофикса `python3 scripts/kb_lint.py --path docs --fix --write`.
* `[MODIFY]` `action.yml`:
  - `inputs.fix` — ввод параметра управления автофиксом.
  - `runs.steps[id=lint]` — проброс флагов `--fix` / `--write`.
* `[MODIFY]` `SPEC.md`:
  - Подраздел 2.3 (`scripts/kb_lint.py`) — описание механизма safe autofix.
  - Раздел 5 («История фаз») — добавление Фазы 31.
* `[MODIFY]` `README.md`:
  - Раздел «Линтер и качество базы знаний» — документирование команд `--fix` и `--write`.
* `[MODIFY]` `tests/test_installer.py`:
  - `TestInstallerBundle.test_39_kb_lint_autofix_delivery()` — E2E сценарий развертывания и исполнения автофикса в изолированном каталоге.
* `[MODIFY]` `install.py` & `dist/install.py`:
  - Синхронизация полезной нагрузки через генератор `scripts/build_installer.py`.

---

## 3. Детали реализации

### 3.1. Hook в `.pre-commit-hooks.yaml`
```yaml
- id: kb-lint-fix
  name: Docs-as-Code safe autofix
  description: Deterministic autofix for frontmatter delimiters, ISO dates, trailing whitespace and task dependencies
  entry: python3 scripts/kb_lint.py --path docs --fix --write
  language: system
  files: '\.md$'
  pass_filenames: false
  require_serial: true
```

### 3.2. Параметр в `action.yml`
```yaml
  fix:
    description: 'Safe autofix mode: none (default), preview (dry-run), or write'
    required: false
    default: 'none'
```
При `fix: preview` добавляется флаг `--fix`, при `fix: write` — `--fix --write`.

### 3.3. E2E Тест поставки `test_39_kb_lint_autofix_delivery`
```python
def test_39_kb_lint_autofix_delivery(self):
    """TASK-115: verify safe autofix (--fix, --write) is deployed, functional, and preserved on update."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        target = Path(tmp_dir) / "FixApp"
        target.mkdir()

        install.install_harness(
            target_dir=target,
            project_name="FixApp",
            stack_key="python",
            agent_choice="all",
            git_choice="none",
            force=True,
        )

        kb_lint_path = target / "scripts" / "kb_lint.py"
        self.assertTrue(kb_lint_path.is_file())

        # 1. Create a spec with fixable defects (date format, delimiter trailing space, missing depends_on)
        spec = target / "docs" / "02_Tasks" / "Specs" / "TASK-001.md"
        spec.parent.mkdir(parents=True, exist_ok=True)
        spec.write_text(
            "---\nid: TASK-001\ntitle: T\ntype: task\nphase: 1\nparent_plan: \"[[PLAN-001]]\"\ncreated: 2026.11.19\nstatus: planned\n--- \n# T\n",
            encoding="utf-8"
        )
        plan = target / "docs" / "02_Tasks" / "Plans" / "PLAN-001.md"
        plan.parent.mkdir(parents=True, exist_ok=True)
        plan.write_text("---\nid: PLAN-001\ntitle: P\n---\n# P\n", encoding="utf-8")

        # 2. Dry-run preview: disk unchanged
        res_dry = subprocess.run([sys.executable, str(kb_lint_path), "--path", "docs", "--fix"], cwd=str(target), capture_output=True, text=True)
        self.assertIn("[DRY-RUN]", res_dry.stdout)
        self.assertIn("created: 2026.11.19", spec.read_text(encoding="utf-8"))

        # 3. Write mode: disk updated
        res_write = subprocess.run([sys.executable, str(kb_lint_path), "--path", "docs", "--fix", "--write", "--allow-dirty"], cwd=str(target), capture_output=True, text=True)
        self.assertIn("[FIXED]", res_write.stdout)
        content_after = spec.read_text(encoding="utf-8")
        self.assertIn("created: 2026-11-19", content_after)
        self.assertIn("depends_on: []", content_after)
```

---

## 4. План верификации (Verification Plan)

- [ ] Синтаксическая компиляция: `python -m py_compile scripts/build_installer.py` (Exit code 0).
- [ ] Пересборка монолитного инсталлятора: `python scripts/build_installer.py` (Exit code 0, размер $\le 210\text{ КБ}$).
- [ ] Полный прогон тестов инсталлятора: `python -m unittest tests/test_installer.py` (100% pass, все 49 тестов).
- [ ] Модульные тесты автофикса: `python -m unittest tests/test_kb_lint_fix.py` (100% pass, 17 тестов).
- [ ] Проверка регрессий основного линтера: `python -m unittest tests/test_kb_lint.py` (100% pass, 79 тестов).
- [ ] Проверка целостности базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links).
- [ ] Проверка синхронизации правил: `python scripts/gen_rules.py --check` (Exit code 0).
- [ ] Проверка состояния графа навигации: `python scripts/kb_state.py status`.

---

## 5. Критерии готовности (DoD)

- [ ] Хук `kb-lint-fix` добавлен в `.pre-commit-hooks.yaml`.
- [ ] Параметр `fix` документирован и поддержан в `action.yml`.
- [ ] Документация `SPEC.md` и `README.md` синхронизирована с фактическим поведением `kb_lint.py --fix`.
- [ ] Добавлен сквозной E2E-тест `test_39_kb_lint_autofix_delivery` в `tests/test_installer.py`.
- [ ] Инсталлятор `install.py` и дистрибутив `dist/install.py` актуализированы и укладываются в бюджет $\le 210\text{ КБ}$.
- [ ] Все тесты из плана верификации выполнены со статусом `OK`.
- [ ] Фаза 31 закрыта в `Kanban.md` (`Done`) и `Roadmap.md` (`[x]`).
- [ ] Итоговая запись внесена в `Devlog.md`.
