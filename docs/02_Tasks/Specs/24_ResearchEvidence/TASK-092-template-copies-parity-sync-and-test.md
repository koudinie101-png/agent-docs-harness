---
id: TASK-092
title: "Синхронизация templates/ ↔ docs/00_Templates/ и Tier 1 parity-тест копий шаблонов"
status: done
type: task
phase: 24
component:
  - templates
  - tests
parent_plan: "[[../../Plans/PLAN-023-research-evidence-gate-and-plan-provenance|PLAN-023]]"
created: 2026-10-18
updated: 2026-10-18
tags:
  - task/spec
  - phase24
  - templates
  - tests
  - quality-gates
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-092 — Parity шаблонов `templates/` ↔ `docs/00_Templates/`

> **ID:** TASK-092 | **Статус:** Выполнено (Режим 3)  
> **Фаза:** 24 | **План:** [[../../Plans/PLAN-023-research-evidence-gate-and-plan-provenance|PLAN-023]] §1.4, §4 | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]] (Tier 1 механизация), [[../../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]] (бюджет шаблонов)  
> **Происхождение:** P2-находка планирования Фазы 24 (§1.4 PLAN-023); устраняется в том же проходе по протоколу TechDebt (P1/P2 — немедленно)

---

## 1. Цель задачи

Закрыть **blind spot** двойного хранилища шаблонов: `templates/` — источник бандла (`scripts/build_installer.py`, local-fallback `unpack_assets()`), `docs/00_Templates/` — хранилище базы знаний. Тесты читают `install.unpack_assets(REPO_ROOT)`, то есть **снимок бандла**, поэтому расхождение копий не детектируется и клиенты получают шаблоны без Always-On правил.

Измерено 2026-10-18 (обе директории содержат одинаковые 16 имён `*.md`):

| Файл | `templates/` | `docs/00_Templates/` | Расхождение |
| :--- | ---: | ---: | :--- |
| `TEMPLATE_PLAN.md` | 2 215 байт | 3 195 байт | в `docs/` есть 4-State UI Matrix (TASK-073), в `templates/` — нет |
| `TEMPLATE_INDEX.md` | 2 068 байт | 1 675 байт | в `templates/` есть `Zero_To_Hero_Guide`, `06_Memory/`, `Inbox/`, «16 шаблонов»; в `docs/` — нет |

**Задача:** привести копии к побайтовому паритету (с нормализацией переводов строк) и закрыть blind spot механически — Tier 1 тестом, который упадёт при любом будущем расхождении.

**Вне скоупа:** `templates/graph.json` (источник `.obsidian/graph.json`, в `docs/00_Templates/` копии намеренно нет); пересборка бандла и E2E установленного артефакта ([[TASK-093-bundle-rebuild-e2e-and-living-spec-sync|TASK-093]]).

## 2. Затрагиваемые файлы

* `[MODIFY]` `templates/TEMPLATE_PLAN.md` — добавить блок `### The 4-State UI Matrix` и строку-комментарий про multi-target Mermaid (обе отсутствовали), дословно как в `docs/00_Templates/TEMPLATE_PLAN.md`.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_INDEX.md` — синхронизировать с `templates/TEMPLATE_INDEX.md` (добавить `Zero_To_Hero_Guide`, узел `06_Memory` в Mermaid, `Inbox/`, раздел `06_Memory/`, «16 шаблонов»).
* `[NEW]` `tests/test_template_parity.py` — Tier 1 parity-тест всех `*.md` двух каталогов.

## 3. Детали реализации

### 3.1. Синхронизация `templates/TEMPLATE_PLAN.md`

После блока `### Prior-Art Gate` (перед `## 4. Декомпозиция задач`) вставить таблицу, **идентичную** версии в `docs/00_Templates/TEMPLATE_PLAN.md`:

```markdown
### The 4-State UI Matrix (если задача затрагивает GUI/TUI):
| Состояние | Поведение и визуализация | Обработка краевых случаев |
| :--- | :--- | :--- |
| **Empty** | Начальный экран без данных | Подсказка к первому действию / кнопка добавления |
| **Loading** | Ожидание ответа сети / узла | Скелетон / спиннер / блокировка повторной отправки |
| **Error** | Сбой транспорта / таймаут / права | Понятное сообщение + кнопка «Повторить» |
| **Populated** | Штатное отображение данных | Адаптивность, скролл, темная/светлая тема |
```

Порядок важен: [[TASK-091-plan-research-basis-template-and-advisory-lint|TASK-091]] уже добавил секцию Research Basis в **обе** копии; здесь переносится только оставшийся блок матрицы.

**Находка при реализации:** в том же файле было второе расхождение — в `docs/` присутствует комментарий `<!-- Для multi-target систем: схема взаимодействия (Mermaid) Target A <-> Protocol <-> Target B -->`, отсутствовавший в `templates/`. Он синхронизирован тем же проходом: паритет означает побайтовое совпадение файла, а не только перенос 4-State Matrix.

### 3.2. Синхронизация `docs/00_Templates/TEMPLATE_INDEX.md`

Канонической считается более полная версия из `templates/` (в ней уже есть актуальные хабы и разделы). Заменить содержимое `docs/00_Templates/TEMPLATE_INDEX.md` на содержимое `templates/TEMPLATE_INDEX.md` **побайтово**, сохранив frontmatter. Проверяемый результат — в `docs/` появляются:

* строка шапки `| **Вайбкодинг:** [[Zero_To_Hero_Guide|Вайбкодинг]]`;
* узлы Mermaid `Index --> Zero[...]` и `Index --> Memory["06. Память"]`;
* `Zero_To_Hero_Guide` в перечне хабов;
* `Inbox/` в перечне `02_Tasks/`;
* строка про `06_Memory/` (Процедурная память и `Incidents/INC-XXX`);
* `(16 шаблонов)` в строке `00_Templates/`.

Причина направления: `templates/` — источник бандла, поэтому любая правка обязана происходить в нём; `docs/` догоняет. Обратное направление (обогащать `docs/` и забывать `templates/`) — ровно тот дрейф, который устраняется.

### 3.3. `tests/test_template_parity.py`

```python
"""TASK-092: Tier 1 parity guard for the two template stores.

`templates/` feeds the installer bundle; `docs/00_Templates/` is the knowledge
base copy. They must stay byte-identical (after CRLF normalisation) so clients
never receive a degraded template.
"""

import difflib
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_DIR = REPO_ROOT / "templates"
DOCS_DIR = REPO_ROOT / "docs" / "00_Templates"


def normalize(text):
    return text.replace("\r\n", "\n")


class TemplateParityTest(unittest.TestCase):
    def test_markdown_file_sets_match(self):
        bundle = {p.name for p in BUNDLE_DIR.glob("*.md")}
        docs = {p.name for p in DOCS_DIR.glob("*.md")}
        self.assertEqual(bundle - docs, set(), "templates missing from docs/00_Templates")
        self.assertEqual(docs - bundle, set(), "docs/00_Templates missing from templates")
        self.assertEqual(len(bundle), 16, "expected exactly 16 canonical templates")

    def test_markdown_contents_match(self):
        for name in sorted(p.name for p in BUNDLE_DIR.glob("*.md")):
            with self.subTest(template=name):
                expected = normalize((BUNDLE_DIR / name).read_text(encoding="utf-8"))
                actual = normalize((DOCS_DIR / name).read_text(encoding="utf-8"))
                if actual != expected:
                    diff = "\n".join(list(difflib.unified_diff(
                        expected.splitlines(), actual.splitlines(),
                        fromfile="templates/" + name,
                        tofile="docs/00_Templates/" + name,
                        lineterm="",
                    ))[:25])
                    self.fail("template copies drifted: %s\n%s" % (name, diff))
```

Контракт:
* Сравниваются **только** `*.md`; `graph.json` исключён намеренно (см. §1).
* Нормализация `\r\n` → `\n` обязательна: Windows autocrlf не должен давать ложный красный тест ([[../../../06_Memory/patterns.md|TRG-01]]).
* Сообщение об ошибке содержит имя файла и unified diff — чтобы правка была очевидной без отладки.
* Тест обязан падать при возврате любого из двух известных расхождений (проверяется негативным прогоном §4).

## 4. План верификации (Verification Plan)

- [x] Паритет: `python -m unittest tests.test_template_parity -v` → **2 теста OK**; прямая сверка 16 файлов: `drifted: []`.
- [x] Негативная проверка теста: в `docs/00_Templates/TEMPLATE_INDEX.md` добавлена строка (`tmp/parity_index_backup.md` — резервная копия) → тест **FAILED** с unified diff; файл восстановлен копией, SHA-256 совпал (`hash match: True`), повторный прогон OK (INC-005 / TRG-05).
- [x] Полный прогон (sandbox-safe, [[../../../06_Memory/Incidents/INC-003-dsh-sandbox-tempfile-mkdtemp-mode|INC-003]] / TRG-03): `python tmp/run_tests.py` → **153 теста OK**, Exit code 0.
- [x] Целостность базы знаний: `python scripts/kb_lint.py --path docs` → Exit code 0, 0 broken links.
- [x] Бюджет шаблонов: **29 579 байт** ≤ 30 000 (запас 421); лимит `test_16` не менялся. Фактический прирост выше оценки на 130 байт из-за второго расхождения (multi-target комментарий), найденного при реализации.
- [x] Ожидаемый дифф: `templates/TEMPLATE_PLAN.md`, `docs/00_Templates/TEMPLATE_INDEX.md`, `tests/test_template_parity.py`; скиллы и адаптеры не затронуты.
- [x] 4-State UI / скриншоты: не применимо (правка Markdown-шаблонов, GUI/TUI отсутствует).
- [x] Замеры $\ge 3$ прогонов: не применимо.

## 5. Критерии готовности (DoD)

- [x] 16 `*.md` в `templates/` и `docs/00_Templates/` побайтово совпадают (после нормализации CRLF).
- [x] `templates/TEMPLATE_PLAN.md` содержит 4-State UI Matrix; `docs/00_Templates/TEMPLATE_INDEX.md` содержит `Zero_To_Hero_Guide`, `06_Memory/`, `Inbox/`, «16 шаблонов».
- [x] Tier 1 parity-тест добавлен, зелёный на синхронизированных копиях и красный при искусственном расхождении.
- [x] Бюджет шаблонов ≤ 30 000 байт не нарушен.
- [x] Статус задачи обновлён в [[../../Kanban|Kanban]] и [[../../Roadmap|Roadmap]] на шаге `/kb-complete`.
