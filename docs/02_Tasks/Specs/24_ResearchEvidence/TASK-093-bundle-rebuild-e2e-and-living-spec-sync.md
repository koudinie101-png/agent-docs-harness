---
id: TASK-093
title: "Пересборка install.py/dist/install.py, E2E установленного Evidence Gate и Living Spec Sync"
status: done
type: task
phase: 24
component:
  - installer
  - e2e
  - docs
parent_plan: "[[../../Plans/PLAN-023-research-evidence-gate-and-plan-provenance|PLAN-023]]"
created: 2026-10-18
updated: 2026-10-18
tags:
  - task/spec
  - phase24
  - research-evidence
  - installer
  - e2e
  - spec
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-093 — Пересборка бандла, E2E и Living Spec Sync

> **ID:** TASK-093 | **Статус:** Выполнено (Режим 3)  
> **Фаза:** 24 | **План:** [[../../Plans/PLAN-023-research-evidence-gate-and-plan-provenance|PLAN-023]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0031-research-evidence-gate-for-icebox-promotion|ADR-0031]] §5 (критерии приёмки), [[../../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]] (бюджеты), `AGENTS.md` Правило 3 (Living Spec Invariant)  
> **Предшествующие задачи:** [[TASK-090-evidence-status-nudge-and-tier2-rule|TASK-090]], [[TASK-091-plan-research-basis-template-and-advisory-lint|TASK-091]], [[TASK-092-template-copies-parity-sync-and-test|TASK-092]]

---

## 1. Цель задачи

Замкнуть фазу на **установленном** артефакте и устранить документационный дрейф:

1. Пересобрать монолит: `EMBEDDED_ASSETS_B64` (шаблоны, скиллы, `scripts/kb_lint.py`, корпус правил) → `install.py` **и** `dist/install.py` одной командой.
2. E2E: в свежей установке скилл `/kb-plan` содержит `Evidence Nudge`, шаблон плана — `research_basis` и секцию Research Basis, установленный линтер — `check_research_basis`; `install.py --update` обновляет устаревший шаблон плана.
3. Living Spec Sync: `SPEC.md` (§2.3 — перечень возможностей `scripts/kb_lint.py`, §2.4 — Mode 1), `README.md` (§2, §3), `docs/Onboarding.md` (Режим 1) отражают Evidence Status, Nudge, `research_basis` и advisory-`WARN`.

**Вне скоупа:** изменение логики скилла/линтера (задачи 090–092); релизная сборка `scripts/kb_release.py`; повышение бюджетов High-SNR.

## 2. Затрагиваемые файлы

* `[MODIFY]` `install.py`, `dist/install.py` — **только** результат `python scripts/build_installer.py` (генерируемые артефакты; ручное редактирование `EMBEDDED_ASSETS_B64` запрещено).
* `[MODIFY]` `tests/test_installer.py` — E2E-метод `test_phase24_research_basis_deploy_and_update` в классе `TestAgentDocsHarness`.
* `[MODIFY]` `SPEC.md` — §2.3 (advisory-проверка линтера) и §2.4 (Mode 1: Evidence Status/Nudge/`research_basis`), поле `updated`.
* `[MODIFY]` `README.md` — таблица скиллов (`/kb-plan`) и описание линтера (`scripts/kb_lint.py`).
* `[MODIFY]` `docs/Onboarding.md` — раздел «🟡 Режим 1: Планирование»: абзац о доказательной базе.

## 3. Детали реализации

### 3.1. Пересборка бандла

```bash
python scripts/build_installer.py
```

Команда обновляет `install.py` и зеркалит его в `dist/install.py` (маркеры `# --- BEGIN_EMBEDDED_ASSETS ---` / `# --- END_EMBEDDED_ASSETS ---`). Контроль:

* оба файла побайтово идентичны: `python -c "from pathlib import Path; assert Path('install.py').read_bytes()==Path('dist/install.py').read_bytes()"`;
* `install.py` ≤ 175 000 байт (текущий замер 171 639; ожидаемая дельта ≈ +2.1 КБ сырого текста шаблонов/скилла после сжатия и base64 → ориентир ≈ 173.7 КБ, запас ≈ 1.3 КБ);
* в бандл попали обновлённые `00_Templates/TEMPLATE_PLAN.md`, `00_Templates/TEMPLATE_INDEX.md`, `.agents/skills/kb-plan/SKILL.md`, `scripts/kb_lint.py`, `rules/AGENTS_CORE.md`.

### 3.2. E2E-тест установленного Evidence Gate

```python
def test_phase24_research_basis_deploy_and_update(self):
    """TASK-093: Evidence Gate ships in the bundle and survives --update."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        target = Path(tmp_dir) / "EvidenceApp"
        target.mkdir()

        install.install_harness(
            target_dir=target,
            project_name="EvidenceApp",
            stack_key="python",
            agent_choice="all",
            git_choice="none",
            force=True,
        )

        skill = (target / ".agents" / "skills" / "kb-plan" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Evidence Nudge", skill)
        self.assertIn("🧪", skill)

        plan_tpl_path = target / "docs" / "00_Templates" / "TEMPLATE_PLAN.md"
        plan_tpl = plan_tpl_path.read_text(encoding="utf-8")
        self.assertIn("research_basis", plan_tpl)
        self.assertIn("Research Basis & Unvalidated Assumptions", plan_tpl)

        index_tpl = (target / "docs" / "00_Templates" / "TEMPLATE_INDEX.md").read_text(encoding="utf-8")
        self.assertIn("06_Memory", index_tpl)
        self.assertIn("Zero_To_Hero_Guide", index_tpl)

        deployed_lint = (target / "scripts" / "kb_lint.py").read_text(encoding="utf-8")
        self.assertIn("def check_research_basis", deployed_lint)

        # Simulate a stale plan template from an earlier harness version, then update.
        plan_tpl_path.write_text("# Legacy plan template\n", encoding="utf-8")
        self.assertEqual(install.update_harness(target, backup=False), 0)
        refreshed = plan_tpl_path.read_text(encoding="utf-8")
        self.assertIn("Research Basis & Unvalidated Assumptions", refreshed)
        self.assertIn("research_basis", refreshed)
```

Требования:
* Проверяется **установленный** артефакт (после пересборки), а не файл-источник — в паре с Tier 1 ассертом из [[TASK-090-evidence-status-nudge-and-tier2-rule|TASK-090]] это закрывает обе точки (источник и дистрибутив).
* `--update` не должен затирать пользовательские заметки: тест правит только шаблон (инфраструктурный файл), пользовательские `docs/02_Tasks/*` не затрагиваются (инвариант `--update` сохраняется, см. `test_11`/`test_15`).
* Тест обязан быть герметичным: только `tempfile`, без сети и Git identity (см. [[../../../06_Memory/patterns.md|TRG-02]]).

### 3.3. `SPEC.md`

1. §2.3 — после пункта про `check_memory_consistency`:

```markdown
  * Неблокирующий контроль доказательной базы плана (`check_research_basis`): `research_basis: none` без `basis_note` → `WARN:` (Exit code 0); при отсутствии поля предупреждение не выдаётся.
```

2. §2.4 — в строку Режима 1 добавить после Prior-Art Gate:

```markdown
Evidence Status (`🔬`/`🧪`/`⏸`) с неблокирующим Evidence Nudge (A/B/C) при промоушене из Icebox и фиксация `research_basis`/`basis_note` в `PLAN-XXX`.
```

3. Поле `updated` в frontmatter — дата коммита задачи (2026-10-18).

### 3.4. `README.md`

* В таблице «12 Executable AI Agent Skills» строка `/kb-plan`:

```markdown
| **`/kb-plan`** | 🟡 Mode 1 (RFC) | Conceptual discussion, trade-off analysis, user confirmation. Ranks Icebox by value impact **and evidence status** (`🔬`/`🧪`/`⏸`), emits a non-blocking Evidence Nudge (A/B/C) for unvalidated items, and records `research_basis` provenance in the plan. Read-only planning; guides user with clear options and next steps. |
```

* В §3 «Autonomous Knowledge Base Linter…» — абзац `Linter (scripts/kb_lint.py)`: добавить предложение: *"It also performs an advisory plan-provenance check: a plan declaring `research_basis: none` without `basis_note` prints a `WARN:` without failing the build."*

### 3.5. `docs/Onboarding.md`

В разделе «🟡 Режим 1: Планирование (Planning / RFC)» добавить пункт:

```markdown
* **Доказательная база (Evidence Gate):** при выборе пункта Icebox без `RESEARCH`/`ADR` агент показывает статус каждого кандидата (`🔬` валидировано, `🧪` гипотеза, `⏸` parked) и выдаёт один неблокирующий Nudge: **(A)** узкий `/kb-research`, **(B)** план с разделом «Research Basis & Unvalidated Assumptions», **(C)** сразу план. Выбор остаётся за пользователем и фиксируется в `PLAN-XXX` полем `research_basis` (ссылка на исследование либо `none` + `basis_note`); `scripts/kb_lint.py` предупреждает (`WARN:`), если `none` указан без причины.
```

### 3.6. Находка при верификации: платформенная инфляция байтового бюджета (P2)

Первый прогон полного suite на Windows упал в `test_16_high_snr_static_corpus_benchmarks`: установленные скиллы заняли **31 056** байт при лимите 31 000, хотя те же файлы в репозитории — 30 654 байта. Причина: `deploy_infrastructure()` пишет Markdown через `Path.write_text()`, и на Windows перевод LF → CRLF добавляет по байту на строку (12 скиллов → +402 байта). Это платформенный артефакт, а не рост токенов: на Linux CI тот же контент даёт 30 654 байта и гейт зелёный.

Исправление (P2 — устраняется в том же проходе по протоколу TechDebt): измерение бюджета в `test_16` переведено на канонический LF-размер через локальный хелпер `canonical_size()` (`read_text` → `\r\n`→`\n` → UTF-8 `encode`). Лимиты 31 000 / 30 000 / 175 000 **не менялись**, текст скиллов не сокращался. Гейт стал детерминированным на Windows и Linux и больше не даёт ложного красного срабатывания.

## 4. План верификации (Verification Plan)

- [x] Пересборка: `python scripts/build_installer.py` → Exit code 0; `install.py` = `dist/install.py` = **173 887 байт** (raw bundle 236 008 → 91 580 b64).
- [x] Идентичность монолитов: `assert Path('install.py').read_bytes()==Path('dist/install.py').read_bytes()` → Exit code 0.
- [x] Новый E2E: `test_phase24_research_basis_deploy_and_update` → **OK** (установленный скилл, шаблон, `TEMPLATE_INDEX.md`, `check_research_basis`, обновление через `--update`).
- [x] Полный прогон (sandbox-safe, [[../../../06_Memory/Incidents/INC-003-dsh-sandbox-tempfile-mkdtemp-mode|INC-003]] / TRG-03): `python tmp/run_tests.py` → **154 теста OK**, Exit code 0 (после P2-фикса §3.6).
- [x] Дрейф корпуса: `python scripts/gen_rules.py --check` → `OK: AGENTS.md matches rules/AGENTS_CORE.md`.
- [x] Бюджеты High-SNR: `install.py` **173 887** ≤ 175 000; скиллы **30 654** ≤ 31 000; шаблоны **29 579** ≤ 30 000; лимиты в тестах не менялись (измерение нормализовано по LF, §3.6).
- [x] Целостность базы знаний: `python scripts/kb_lint.py --path docs` → Exit code 0, 0 broken links.
- [x] `dist/install.py` smoke: `python dist/install.py --yes --stack python --target-dir tmp/smoke_task093` → Exit code 0; скилл содержит `Evidence Nudge`, шаблон — `research_basis` и секцию Research Basis; каталог удалён.
- [x] 4-State UI / скриншоты: не применимо (GUI/TUI отсутствует).
- [x] Замеры $\ge 3$ прогонов: не применимо (фиксируются только статические байтовые бюджеты).

## 5. Критерии готовности (DoD)

- [x] `install.py` и `dist/install.py` пересобраны, идентичны и укладываются в бюджет ≤ 175 000 байт.
- [x] В свежей установке присутствуют `Evidence Nudge`, `research_basis`, секция Research Basis, `check_research_basis`, обновлённый `TEMPLATE_INDEX.md`.
- [x] `install.py --update` обновляет устаревший `TEMPLATE_PLAN.md`, не затрагивая пользовательские заметки.
- [x] `SPEC.md`, `README.md`, `docs/Onboarding.md` синхронизированы (Living Spec).
- [x] Бюджеты скиллов ≤ 31 000 и шаблонов ≤ 30 000 байт не нарушены; лимиты в тестах не поднимались.
- [x] Полный suite и `kb_lint` зелёные; статус задачи обновлён в [[../../Kanban|Kanban]] и [[../../Roadmap|Roadmap]] на шаге `/kb-complete`.
