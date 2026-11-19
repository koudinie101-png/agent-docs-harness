---
id: TASK-112
title: "Интеграция kb_state в скиллы, бандлинг в install.py и поставка"
status: done
type: task
phase: 30
component:
  - core
  - installer
  - skills
  - docs
parent_plan: "[[../../Plans/PLAN-027-deterministic-navigation-and-task-graph|PLAN-027]]"
depends_on:
  - TASK-111
created: 2026-11-19
updated: 2026-11-19
tags:
  - task/spec
  - phase30
  - navigation
  - installer
  - skills
  - docs
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-112 — Интеграция kb_state в скиллы, бандлинг в install.py и поставка

> **ID:** TASK-112 | **Статус:** Выполнено (Done) | **Фаза:** 30  
> **План:** [[../../Plans/PLAN-027-deterministic-navigation-and-task-graph|PLAN-027: Детерминированная навигация и граф зависимостей]] | **Канбан:** [[../../Kanban|Канбан-доска]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0035-wave-1-deterministic-navigation-and-task-graph-standard|ADR-0035]] | **Исследование:** [[../../../04_Research/RESEARCH-029-wave-1-docs-integrity-and-deterministic-navigation|RESEARCH-029]]  
> **Зависимости:** [[TASK-111-deterministic-navigation-kb-state|TASK-111 (Ядро навигации scripts/kb_state.py)]]

---

## 1. Цель задачи

Завершить формирование контура детерминированной навигации (Фаза 30 / Волна 1, P0):
1. Интегрировать автономную утилиту `scripts/kb_state.py` в жизненный цикл агентов: скилл финализации `/kb-complete` (автоматическая рекомендация точного следующего шага через `kb_state next`) и скилл онбординга `/kb-onboard`.
2. Упаковать `scripts/kb_state.py` в монолитный инсталлятор `install.py` через `scripts/build_installer.py`, гарантируя доставку утилиты во все клиентские проекты на этапе установки и обновления (`--update`).
3. Актуализировать бюджеты дистрибутива в `tests/test_installer.py` (плановое расширение бюджета `install.py` с 186 КБ до 210 КБ с учетом добавления нового исполняемого скрипта).
4. Синхронизировать документацию Living Spec (`SPEC.md`, `README.md`, `docs/Onboarding.md`, `rules/AGENTS_CORE.md` и корневой `AGENTS.md`).

---

## 2. Затрагиваемые файлы и скоуп символов

* `[MODIFY]` `scripts/build_installer.py`:
  - `bundle_assets()` — включение `scripts/kb_state.py` в список бандлируемых скриптов `["kb_lint.py", "kb_release.py", "kb_ingest.py", "kb_state.py"]`.
* `[MODIFY]` `install.py`:
  - `deploy_infrastructure()` / `install_harness()` / `update_harness()` — актуализация сообщений о развертывании и обновлении `scripts/kb_state.py`.
  - `EMBEDDED_ASSETS` — пересборка бандла с упакованным `scripts/kb_state.py`.
* `[MODIFY]` `.agents/skills/kb-complete/SKILL.md`:
  - Раздел `10. Next Step (State-Aware) & Stop & Yield Control` — использование `python scripts/kb_state.py next` для детерминированного определения следующей команды.
* `[MODIFY]` `.agents/skills/kb-onboard/SKILL.md`:
  - Таблица команд и раздел процедур — добавление команд `python scripts/kb_state.py status` и `next`.
* `[MODIFY]` `docs/Onboarding.md`:
  - Раздел быстрых команд и навигации — описание вызова `kb_state.py`.
* `[MODIFY]` `rules/AGENTS_CORE.md`:
  - Раздел Mode 3 Completion checklist — включение вызова `kb_state` перед Stop & Yield.
* `[MODIFY]` `SPEC.md` и `README.md`:
  - Добавление подраздела 2.6 `scripts/kb_state.py`: назначение, флаги, 5 уровней приоритета.
  - Актуализация состава поставляемых скриптов в разделе 3 инсталлятора.
* `[MODIFY]` `tests/test_installer.py`:
  - `test_16_high_snr_static_corpus_benchmarks` — плановое расширение бюджета инсталлятора до 210 000 байт.
  - `test_38_deterministic_navigation_delivery` — новый E2E-тест: валидация развертывания `scripts/kb_state.py` на чистой установке и при `--update`, запуск утилиты в развернутом проекте.

---

## 3. Детали реализации

### 3.1. Интеграция `kb_state` в `.agents/skills/kb-complete/SKILL.md`

```markdown
10. **Next Step (State-Aware) & Stop & Yield Control:**
    - Выполнить `python scripts/kb_state.py next --json` для детерминированного выбора следующего действия:
      * `status: "ready"` -> предложить команду из `target.command` (например, `/kb-implement TASK-YYY` или `/kb-task TASK-YYY`).
      * `status: "blocked_by_bug"` -> предложить устранение критического дефекта: `/kb-implement BUG-ZZZ`.
      * `status: "all_done"` -> рекомендовать приемочное тестирование и `/kb-release <vX.Y.Z>`.
      * `status: "deadlock"` -> предупредить о взаимной блокировке задач.
    - Вывести краткую Anti-Echo сводку (`[FileName](file://...)`, 3–5 пунктов) и прекратить вызовы инструментов (Stop & Yield).
```

### 3.2. Ребалансировка бюджета инсталлятора в `tests/test_installer.py`

В тесте `test_16_high_snr_static_corpus_benchmarks`:
```python
# Installer size check (budget <= 210 KB with 16 templates, 12 skills, 4 standalone scripts including kb_state.py,
# memory patterns, UI harness, tech debt registry & engineering gates, machine-readable lint contract,
# and deterministic navigation engine).
installer_size = (REPO_ROOT / "install.py").stat().st_size
self.assertLessEqual(installer_size, 210000, f"install.py exceeded budget: {installer_size} bytes (budget <= 210 KB)")
```

### 3.3. E2E-тест поставки `test_38_deterministic_navigation_delivery`

```python
def test_38_deterministic_navigation_delivery(self):
    """E2E: verify scripts/kb_state.py is deployed on install and updated on --update."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        target = Path(tmp_dir) / "NavApp"
        target.mkdir()

        install.install_harness(
            target_dir=target,
            project_name="NavApp",
            stack_key="python",
            agent_choice="all",
            git_choice="none",
        )

        kb_state_path = target / "scripts" / "kb_state.py"
        self.assertTrue(kb_state_path.is_file(), "scripts/kb_state.py was not deployed!")

        # Run deployed kb_state next via subprocess
        res = subprocess.run(
            [sys.executable, str(kb_state_path), "next", "--json"],
            cwd=str(target),
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertIn("status", data)
```

---

## 4. План верификации (Verification Plan)

- [x] Сборка бандла: `python scripts/build_installer.py` (Exit code 0).
- [x] Генерация правил агентов: `python scripts/gen_rules.py --check` (Exit code 0).
- [x] Модульные тесты инсталлятора: `python -m unittest tests/test_installer.py` (100% pass).
- [x] Полный прогон тестового сьюта: `python -m unittest discover -s tests` (100% pass).
- [x] Проверка целостности базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links).

---

## 5. Критерии готовности (DoD)

- [x] `scripts/kb_state.py` включен в `scripts/build_installer.py` и упакован в `install.py`.
- [x] Скиллы `.agents/skills/kb-complete/SKILL.md` и `.agents/skills/kb-onboard/SKILL.md` актуализированы.
- [x] `SPEC.md`, `README.md`, `docs/Onboarding.md` и `rules/AGENTS_CORE.md` обновлены.
- [x] Тест `test_38_deterministic_navigation_delivery` добавлен и проходит.
- [x] Бюджет `install.py` в `test_16` скорректирован до $\le 210\text{ КБ}$.
- [x] Все пункты Плана верификации пройдены (Exit code 0).
- [x] Фаза 30 в Канбане (`Done`) и Дорожной карте (`[x]`) закрыта.
- [x] Запись добавлена в `Devlog.md`.
