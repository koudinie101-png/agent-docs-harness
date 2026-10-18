---
id: TASK-090
title: "Evidence Status и Evidence Nudge в /kb-plan, Tier 2 правило в корпусе и Tier 1 защита формулировки"
status: done
type: task
phase: 24
component:
  - skills
  - rules
  - tests
parent_plan: "[[../../Plans/PLAN-023-research-evidence-gate-and-plan-provenance|PLAN-023]]"
created: 2026-10-18
updated: 2026-10-18
tags:
  - task/spec
  - phase24
  - research-evidence
  - kb-plan
  - rules
  - tests
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-090 — Evidence Status и Evidence Nudge в `/kb-plan`

> **ID:** TASK-090 | **Статус:** Выполнено (Режим 3)  
> **Фаза:** 24 | **План:** [[../../Plans/PLAN-023-research-evidence-gate-and-plan-provenance|PLAN-023]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0031-research-evidence-gate-for-icebox-promotion|ADR-0031]] (R1, R2, R5), [[../../../03_Decisions_ADR/ADR-0011-intent-routing-and-icebox-prioritization-in-kb-plan|ADR-0011]] §2.2 (восстанавливаемый критерий), [[../../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]] (Tier 1/2/3), [[../../../04_Research/RESEARCH-025-research-evidence-gate-for-icebox-promotion|RESEARCH-025]]  
> **Предшествующие задачи:** [[../22_RuleCompiler/TASK-086-agents-md-codegen-and-ci-check|TASK-086]] (генерация `AGENTS.md`), [[../22_RuleCompiler/TASK-087-rules-drift-consistency-tests|TASK-087]] (Tier 1 структура корпуса)

---

## 1. Цель задачи

Восстановить критерий технической зрелости в ветке `No Argument` скилла `/kb-plan` (регресс [[../../../03_Decisions_ADR/ADR-0011-intent-routing-and-icebox-prioritization-in-kb-plan|ADR-0011]] §2.2: при переносе решения в текст скилла остался только `value impact`) и защитить формулировку от повторной потери механически:

1. **R1 — Evidence Status:** ранжирование Icebox ведётся по двум критериям (Value Impact + Evidence Status), каждый кандидат помечается `🔬` / `🧪` / `⏸`; пометки **вычисляются из ссылок** и никогда не вносятся вручную в `Roadmap.md`.
2. **R2 — Evidence Nudge:** для `🧪`-рекомендации агент предлагает ровно один Nudge с тремя опциями (A — узкий `/kb-research`, B — план с разделом Research Basis, C — сразу план) и правилом рекомендации по обратимости; выбор пользователя абсолютен, Nudge не повторяется в рамках сессии.
3. **R5 — Tier 2:** одна содержательная строка в Mode 1 корпуса `rules/AGENTS_CORE.md` в **обоих** документах (`client-agents` — для клиентских проектов, `harness-agents` — для этого репозитория) + регенерация `AGENTS.md`.
4. **Tier 1:** ассерт маркеров Nudge по **файлу-источнику** `.agents/skills/kb-plan/SKILL.md` (не по бандлу) в `tests/test_installer.py`, чтобы suite оставался зелёным до пересборки монолита в [[TASK-093-bundle-rebuild-e2e-and-living-spec-sync|TASK-093]].

**Вне скоупа:** поля `research_basis`/`basis_note` и секция Research Basis в шаблоне плана, `check_research_basis()` в линтере ([[TASK-091-plan-research-basis-template-and-advisory-lint|TASK-091]]); синхронизация копий шаблонов и parity-тест ([[TASK-092-template-copies-parity-sync-and-test|TASK-092]]); пересборка `install.py`/`dist/install.py` и E2E установленного артефакта ([[TASK-093-bundle-rebuild-e2e-and-living-spec-sync|TASK-093]]).

## 2. Затрагиваемые файлы

* `[MODIFY]` `.agents/skills/kb-plan/SKILL.md` — критерий `Evidence Status`, правила классификации `🔬`/`🧪`/`⏸`, блок `Evidence Nudge` (A/B/C).
* `[MODIFY]` `rules/AGENTS_CORE.md` — по одной строке `Research Evidence` в Mode 1 блоков `LIFECYCLE` обоих документов (`client-agents`, `harness-agents`).
* `[MODIFY]` `AGENTS.md` — **только** результат `python scripts/gen_rules.py` (генерируемый артефакт, ручная правка запрещена).
* `[MODIFY]` `tests/test_installer.py` — Tier 1 ассерт маркеров Nudge по файлу-источнику скилла.
* `[MODIFY]` `tests/fixtures/rules/client_agents__*__*.txt` — 12 golden-фикстур клиентского свода (регенерация после правки корпуса; фикстуры адаптеров не меняются).

## 3. Детали реализации

### 3.1. `.agents/skills/kb-plan/SKILL.md` — ветка `No Argument`

Заменить единственную строку ветки (строка 20 текущей версии):

```markdown
- **No Argument (`/kb-plan`):** Inspect Icebox in `docs/02_Tasks/Roadmap.md`. Rank candidates by value impact with 1-line rationale and top recommendation. If empty, ask user.
```

на два пункта (сохранить отступ в 3 пробела перед `-`, как в исходном файле):

```markdown
   - **No Argument (`/kb-plan`):** Inspect Icebox in `docs/02_Tasks/Roadmap.md`. Rank candidates by value impact AND **Evidence Status** (linked `RESEARCH-XXX`/`ADR-XXXX`), 1-line rationale each, then a top recommendation. Derive the badge from links (never hand-edit `Roadmap.md`): `🔬` validated, `🧪` hypothesis (no links), `⏸` parked (explicit "future"/"after Phase N" marker).
   - *Evidence Nudge (once per session, only for a `🧪` top recommendation):* offer **(A)** narrow `/kb-research <topic>`, **(B)** plan with "Research Basis & Unvalidated Assumptions", **(C)** plan now. Recommend **A** for irreversible decisions (new deps per ADR-0001, public contracts, data formats, migrations, security), **B** otherwise. The user's choice is absolute.
```

Требования к тексту:
* Маркеры `Evidence Status`, `Evidence Nudge`, `🔬`, `🧪`, `⏸` присутствуют **дословно** (на них опирается Tier 1 ассерт §3.5).
* Классификация `⏸` — только при явном parking-маркере в тексте пункта («на будущее», «когда наступит X», «после Фазы N») и отсутствии ссылок; иначе `🧪`.
* Nudge не повторяется в рамках сессии; сообщение ≤ 3 строк; при пустом Icebox — вопрос пользователю (не Nudge).
* Бюджет: суммарный размер `.agents/skills/**/*.md` **обязан остаться ≤ 31 000 байт**. Замер 2026-10-18: 30 070 байт; ожидаемая дельта от замены строки (178 → 763 байта) — **+585 байт**, итог ≈ 30 654 байта (запас 346 байт). Если бюджет превышен — сокращать прозу (примеры/скобки), **не** поднимать лимит в `test_16_high_snr_static_corpus_benchmarks`.

### 3.2. Контрольный dry-run на текущем Icebox

До коммита выполнить ручной прогон ранжирования по `docs/02_Tasks/Roadmap.md` (секция Icebox, 8 пунктов) и зафиксировать таблицу в отчёте задачи:

| Ожидание | Значение |
| :--- | :--- |
| `🔬` валидировано | 1 пункт — «Символьные контракты скоупа задач» (`RESEARCH-024` + `ADR-0029`) |
| `🧪` гипотеза | 7 пунктов (в текущем тексте Icebox нет explicit parking-маркеров) |
| `⏸` parked | 0 пунктов |
| Nudge срабатывает | при выборе любого из 7 `🧪`-пунктов, ровно один раз |

Если фактическая классификация отличается — это не ошибка теста, а сигнал уточнить parking-маркеры в тексте скилла; расхождение фиксируется в отчёте.

### 3.3. `rules/AGENTS_CORE.md` — Tier 2 (два документа корпуса)

* В `client-agents` (блок `<!-- RULE: LIFECYCLE -->`, Mode 1, после строки `Output:`):

```markdown
- **Research Evidence:** Promoting an Icebox item without `RESEARCH`/`ADR` requires an explicit `research_basis` in `PLAN-XXX` (`none` + one-line `basis_note`); research-vs-plan choice stays with the user.
```

* В `harness-agents` (Mode 1, после пункта `- **TechDebt Sync:** ...`):

```markdown
- **Research Evidence:** Промоушен из Icebox без `RESEARCH`/`ADR` требует явного `research_basis` в `PLAN-XXX` (`none` + однострочный `basis_note`); выбор между исследованием и планом остаётся за пользователем.
```

Ограничения:
* **Новый блок `<!-- RULE: ... -->` не создаётся** — иначе придётся править три пина инвентаря в `tests/test_rules_consistency.py` (`CLIENT_RULES`, `ADAPTER_RULES`, `HARNESS_RULES`) и subset-проверку адаптеров. Правка идёт внутрь существующего `LIFECYCLE`.
* Правка `AGENTS.md` вручную запрещена: только `python scripts/gen_rules.py`.

### 3.4. Регенерация артефактов

```bash
python scripts/gen_rules.py                      # AGENTS.md из корпуса
python tmp/gen_fixtures.py                       # golden-фикстуры (tmp/ в .gitignore)
```

`tmp/gen_fixtures.py` (уже существует, вне Git) вызывает `install.generate_agents_md("Demo", stack, lang)` для 6 стеков × 2 языка и 6 адаптеров × 2 языка. Если файл отсутствует — создать его с тем же контрактом (импорт `install` из корня репозитория, `REPO_ROOT/tests/fixtures/rules`, запись `newline="\n"`).

Контроль ожидаемого диффа:

```bash
git status --short tests/fixtures/rules
```

Должно измениться **ровно 12** файлов `client_agents__*.txt`; `adapter__*.txt` — без изменений (в адаптерах нет блока `LIFECYCLE`). Если изменились адаптеры — правка корпуса затронула не тот документ, откатить и исправить.

### 3.5. Tier 1 ассерт в `tests/test_installer.py`

Добавить метод в класс `TestAgentDocsHarness` (после `test_18_discovery_mode_and_phase6_assets`):

```python
def test_evidence_nudge_source_guard(self):
    """Tier 1: TASK-090 protects the Evidence Nudge wording from being lost again.

    Reads the source skill file (not the bundled snapshot) so the guard stays
    green until TASK-093 rebuilds the monolithic installer.
    """
    skill = (REPO_ROOT / ".agents" / "skills" / "kb-plan" / "SKILL.md").read_text(encoding="utf-8")
    for marker in (
        "Evidence Status",
        "Evidence Nudge",
        "🔬",
        "🧪",
        "⏸",
        "Research Basis & Unvalidated Assumptions",
    ):
        self.assertIn(marker, skill, "kb-plan skill lost marker: %s" % marker)
```

Почему по файлу-источнику: `install.unpack_assets()` в корневом репозитории читает `EMBEDDED_ASSETS_B64` (снимок бандла), который обновится только в TASK-093. Ассерт по установленному артефакту — в [[TASK-093-bundle-rebuild-e2e-and-living-spec-sync|TASK-093]].

## 4. План верификации (Verification Plan)

- [x] Компиляция: `python -m py_compile install.py scripts/gen_rules.py` (Exit code 0).
- [x] Дрейф корпуса: `python scripts/gen_rules.py --check` → `OK: AGENTS.md matches rules/AGENTS_CORE.md` (Exit code 0).
- [x] Golden-фикстуры: `python -m unittest tests.test_rules_golden -v` → OK (3 теста; 12 client + 12 adapter).
- [x] Структура корпуса: `python -m unittest tests.test_rules_consistency -v` → покрыто полным прогоном (13 тестов модуля OK).
- [x] Новый ассерт: `python -m unittest tests.test_installer.TestAgentDocsHarness.test_evidence_nudge_source_guard -v` → OK.
- [x] Полный прогон (sandbox-safe, [[../../../06_Memory/Incidents/INC-003-dsh-sandbox-tempfile-mkdtemp-mode|INC-003]] / TRG-03): `python tmp/run_tests.py` → **147 тестов OK**, Exit code 0.
- [x] Бюджет скиллов: 30 654 байта ≤ 31 000 (запас 346), лимит теста не менялся.
- [x] Целостность базы знаний: `python scripts/kb_lint.py --path docs` → Exit code 0 (238 файлов, 2283 ссылки, 0 broken).
- [x] Dry-run §3.2 выполнен: 8 пунктов Icebox → **1 `🔬`** («Символьные контракты», `RESEARCH-024`+`ADR-0029`), **7 `🧪`**, **0 `⏸`**; Nudge срабатывает на любом из 7.
- [x] 4-State UI / скриншоты: не применимо (интерфейс — текстовое сообщение Nudge в чате, GUI/TUI не затрагивается).
- [x] Замеры $\ge 3$ прогонов: не применимо (нет изменений производительности/токенов, кроме статического бюджета скиллов).

## 5. Критерии готовности (DoD)

- [x] Ветка `No Argument` ранжирует по Value Impact **+** Evidence Status и печатает `🔬`/`🧪`/`⏸` из ссылок.
- [x] `Evidence Nudge` содержит ровно 3 опции (A/B/C) и правило рекомендации по обратимости; Nudge не повторяется в сессии.
- [x] Строка `Research Evidence` присутствует в Mode 1 обоих документов корпуса; `AGENTS.md` регенерирован, `gen_rules.py --check` зелёный.
- [x] Tier 1 ассерт по файлу-источнику защищает маркеры от повторной потери; полный suite зелёный.
- [x] Бюджет скиллов ≤ 31 000 байт не нарушен; лимит в тесте не поднят.
- [x] Статус задачи обновлён в [[../../Kanban|Kanban]] и [[../../Roadmap|Roadmap]] на шаге `/kb-complete`.
