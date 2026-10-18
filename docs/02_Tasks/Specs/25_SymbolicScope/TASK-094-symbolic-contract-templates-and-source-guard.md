---
id: TASK-094
title: "Символьный контракт в шаблонах задач, Tier 1 source-guard и замер бюджетов"
status: planned
type: task
phase: 25
component:
  - templates
  - tests
parent_plan: "[[../../Plans/PLAN-024-symbolic-scope-and-task-contracts|PLAN-024]]"
created: 2026-10-18
updated: 2026-10-18
tags:
  - task/spec
  - phase25
  - symbolic-scope
  - templates
  - tests
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-094 — Символьный контракт в шаблонах и source-guard

> **ID:** TASK-094 | **Статус:** К реализации  
> **Фаза:** 25 | **План:** [[../../Plans/PLAN-024-symbolic-scope-and-task-contracts|PLAN-024]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0029-fine-grained-task-symbol-contracts-and-line-drift-rejection|ADR-0029]], [[../../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]] (бюджеты), [[../24_ResearchEvidence/TASK-092-template-copies-parity-sync-and-test|TASK-092]] (parity)

---

## 1. Цель задачи

Привести шаблоны спецификаций в соответствие с принятым [[../../../03_Decisions_ADR/ADR-0029-fine-grained-task-symbol-contracts-and-line-drift-rejection|ADR-0029]]:

1. Заменить плоский список файлов в `TEMPLATE_TASK.md` иерархическим контрактом «Файл → символ/метод → изменение» и запретить номера строк как ориентир.
2. Убрать из `TEMPLATE_TASK_MICRO.md` подсказку «конкретная функция, **строка** или блок», которая прямо противоречит ADR.
3. Защитить формулировку Tier 1 source-guard тестом, читающим **файл-источник** `templates/`, а не снимок бандла.
4. Замерить бюджеты и уложиться в `≤ +250 B` (шаблоны ≤ 29 829 из 30 000).

**Вне скоупа:** `check_symbolic_scope()` и правки скиллов (TASK-095); пересборка `install.py` / `dist/install.py`, E2E и Living Spec (TASK-096). `install.py` намеренно не пересобирается — `test_16` продолжит измерять прежний снимок бандла до TASK-096.

## 2. Затрагиваемые файлы и скоуп символов

* `[MODIFY]` `docs/00_Templates/TEMPLATE_TASK.md`:
  - Раздел `## 2. Затрагиваемые файлы и скоуп символов`: новый иерархический контракт (§3.1).
* `[MODIFY]` `templates/TEMPLATE_TASK.md`:
  - Раздел `## 2. Затрагиваемые файлы и скоуп символов`: побайтовая копия для бандла.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_TASK_MICRO.md`:
  - Раздел `## 2. Контракт файлов`: символьная подсказка вместо «строка или блок» (§3.2).
* `[MODIFY]` `templates/TEMPLATE_TASK_MICRO.md`:
  - Раздел `## 2. Контракт файлов`: побайтовая копия для бандла.
* `[MODIFY]` `tests/test_installer.py`:
  - `TestAgentDocsHarness.test_symbolic_scope_template_source_guard()`: Tier 1 защита формулировки и отсутствия номеров строк (§3.3).

## 3. Детали реализации

### 3.1. `TEMPLATE_TASK.md` — целевой текст §2

Четыре строки (заголовок + три маркера) заменяются на блок ниже. Заголовок сохраняет префикс `## 2.` — на него опирается разбор секции в `scripts/kb_lint.py` (`check_fast_track_specs`).

```markdown
## 2. Затрагиваемые файлы и скоуп символов
* `[MODIFY]` `path/to/file.ext`:
  - `ClassName.method_name()` — <!-- суть изменения; сигнатура, если меняется -->
* `[NEW]` `path/to/new_file.ext`:
  - `function_name(arg: Type) -> Ret` — <!-- контракт нового символа -->
* `[DELETE]` `path/to/file.ext` — <!-- причина удаления -->
<!-- Символы, без номеров строк (ADR-0029) -->
```

Требования:
* Для `[DELETE]` и не-кодовых файлов (`.md`, `.yml`, `.json`, `.toml`) вложенные символы не требуются — это фиксирует пример и комментарий.
* Никаких `:L42` / `L10-L20` в шаблоне (проверяется тестом §3.3).
* Ожидаемый прирост: ~+150…200 B; верхняя граница — +250 B.

### 3.2. `TEMPLATE_TASK_MICRO.md` — целевой текст §2

Меняется только вторая строка; заголовок `## 2. Контракт файлов` остаётся прежним.

```markdown
* `[MODIFY]` `path/to/file` — <!-- символ(ы) и суть изменения; без номеров строк (ADR-0029) -->
```

Подсказка остаётся HTML-комментарием (как и раньше), но требует символ и запрещает строки. Иерархия в micro **не** вводится: Fast-Track не должен подорожать.

### 3.3. Tier 1 source-guard в `tests/test_installer.py`

Новый метод класса `TestAgentDocsHarness`, сразу после `test_evidence_nudge_source_guard` (≈ строка 1171). Читает `templates/` — источник бандла, поэтому зелёный до пересборки в TASK-096; равенство копий `docs/00_Templates/` уже обеспечивает `tests/test_template_parity.py`.

```python
    def test_symbolic_scope_template_source_guard(self):
        """Tier 1 (TASK-094): the symbol-scope contract must not be lost again.

        Reads the bundle source templates, not the built snapshot, so the guard
        stays green until TASK-096 rebuilds the monolithic installer.
        """
        task_tpl = (REPO_ROOT / "templates" / "TEMPLATE_TASK.md").read_text(encoding="utf-8")
        micro_tpl = (REPO_ROOT / "templates" / "TEMPLATE_TASK_MICRO.md").read_text(encoding="utf-8")

        for marker in (
            "Затрагиваемые файлы и скоуп символов",
            "ClassName.method_name()",
            "function_name(arg: Type) -> Ret",
            "ADR-0029",
        ):
            self.assertIn(marker, task_tpl, "TASK template lost symbol-scope marker: %s" % marker)

        self.assertNotRegex(task_tpl, r":L\d+", "Line-number anchors are prohibited (ADR-0029)")
        self.assertIn("символ(ы)", micro_tpl)
        self.assertNotIn("строка или блок", micro_tpl)
        self.assertIn("ADR-0029", micro_tpl)
```

### 3.4. Синхронизация копий

Правки вносятся **идентично** в `templates/` и `docs/00_Templates/`; расхождение ловится существующим Tier 1 `tests/test_template_parity.py` (TASK-092). Ручная правка только одной копии запрещена.

### 3.5. Замер бюджетов

Базовая линия (2026-10-18, канонический LF-размер): шаблоны **29 579 B**, `TEMPLATE_TASK.md` **2 625 B**, `TEMPLATE_TASK_MICRO.md` **1 614 B**. Команда замера:

```bash
python -c "from pathlib import Path; fs=sorted(Path('templates').glob('*.md')); total=sum(len(p.read_text(encoding='utf-8').replace(chr(13)+chr(10),chr(10)).encode('utf-8')) for p in fs); print('templates', total); print('task', len(Path('templates/TEMPLATE_TASK.md').read_text(encoding='utf-8').replace(chr(13)+chr(10),chr(10)).encode('utf-8'))); print('micro', len(Path('templates/TEMPLATE_TASK_MICRO.md').read_text(encoding='utf-8').replace(chr(13)+chr(10),chr(10)).encode('utf-8')))"
```

Порог: `templates ≤ 29 829` (прирост `≤ +250 B`) и абсолютный лимит `≤ 30 000`. Фактические числа фиксируются в отчёте задачи.

### 3.6. Совместимость

* Бандл не пересобирается: `install.py` / `dist/install.py` остаются прежними; установленные клиенты увидят новый шаблон только после TASK-096.
* `test_16_high_snr_static_corpus_benchmarks` до пересборки измеряет старый снимок — это ожидаемо и не является регрессией.
* Исторические спеки (`status: done`) не трогаются.

## 4. План верификации (Verification Plan)

- [ ] Tier 1 source-guard: `python -m unittest tests.test_installer.TestAgentDocsHarness.test_symbolic_scope_template_source_guard` → OK.
- [ ] Parity копий: `python -m unittest tests.test_template_parity` → 2 теста OK.
- [ ] Синтаксис теста: `python -m py_compile tests/test_installer.py` → Exit code 0.
- [ ] Бюджет (§3.5): `templates ≤ 29 829` и `≤ 30 000`, `TEMPLATE_TASK` / `TEMPLATE_TASK_MICRO` — фактические числа записаны в отчёт.
- [ ] Целостность базы знаний: `python scripts/kb_lint.py --path docs` → Exit code 0, 0 битых ссылок.
- [ ] Полный прогон (sandbox-safe, [[../../../06_Memory/Incidents/INC-003-dsh-sandbox-tempfile-mkdtemp-mode|INC-003]] / TRG-03): `python tmp/run_tests.py` → все тесты OK, Exit code 0.
- [ ] 4-State UI / скриншоты: не применимо (GUI/TUI отсутствует).
- [ ] Замеры $\ge 3$ прогонов: не применимо — статический байтовый бюджет детерминирован; фиксируется один канонический замер.

## 5. Критерии готовности (DoD)

- [ ] Все четыре шаблона обновлены, `tests/test_template_parity.py` зелёный.
- [ ] В `TEMPLATE_TASK.md` есть иерархический контракт, нет номеров строк и есть ссылка на ADR-0029.
- [ ] В `TEMPLATE_TASK_MICRO.md` нет фразы «строка или блок», есть символьная подсказка.
- [ ] Tier 1 source-guard добавлен и зелёный; полный suite и `kb_lint` зелёные.
- [ ] Бюджет замерен: `templates ≤ 29 829` (и `≤ 30 000`), фактические числа зафиксированы.
- [ ] Статус задачи обновлён в [[../../Kanban|Kanban]] и [[../../Roadmap|Roadmap]] на шаге `/kb-complete`.
