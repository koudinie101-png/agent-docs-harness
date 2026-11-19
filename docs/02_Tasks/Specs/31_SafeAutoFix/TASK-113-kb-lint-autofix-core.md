---
id: TASK-113
title: "Ядро хирургического автофикса в scripts/kb_lint.py"
status: planned
type: task
phase: 31
component:
  - core
  - lint
parent_plan: "[[../../Plans/PLAN-028-kb-lint-safe-autofix|PLAN-028]]"
depends_on: []
created: 2026-11-19
updated: 2026-11-19
tags:
  - task/spec
  - phase31
  - lint
  - autofix
  - data-integrity
  - safety
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-113 — Ядро хирургического автофикса в scripts/kb_lint.py

> **ID:** TASK-113 | **Статус:** К реализации (Planned) | **Фаза:** 31  
> **План:** [[../../Plans/PLAN-028-kb-lint-safe-autofix|PLAN-028: Безопасный автофикс kb_lint --fix]] | **Канбан:** [[../../Kanban|Канбан-доска]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0036-kb-lint-safe-autofix-standard|ADR-0036]] | **Исследование:** [[../../../04_Research/RESEARCH-030-kb-lint-safe-autofix|RESEARCH-030]]  
> **Зависимости:** `[]` (первая задача Фазы 31)

---

## 1. Цель задачи

Реализовать ядро безопасного хирургического автофикса в монолитном линтере `scripts/kb_lint.py` в соответствии со стандартом [[../../../03_Decisions_ADR/ADR-0036-kb-lint-safe-autofix-standard|ADR-0036]]:
1. Ввести флаги командной строки: `--fix`, `--dry-run`, `--write`, `--allow-dirty`.
2. Реализовать генератор хирургических строковых замен `generate_file_fixes()` для 5 детерминированных безопасных правил (`KB-004`, `KB-005`, `KB-006`, `KB-007`, `KB-010`).
3. Реализовать генерацию унифицированного диффа через стандартную библиотеку `difflib.unified_diff`.
4. Реализовать протокол безопасности Zero Data Loss: безопасный предпросмотр `--dry-run` по умолчанию, атомарная запись через `tempfile.NamedTemporaryFile` + `os.replace` при флаге `--write`, проверка чистоты дерева `git_is_clean()`.
5. Покрыть функционал модульными тестами в `tests/test_kb_lint_fix.py` (100% покрытие всех правил, флагов, диффов, атомарности и Git-Clean Guard).

---

## 2. Затрагиваемые файлы и скоуп символов

* `[MODIFY]` `scripts/kb_lint.py`:
  - `Fix` — датакласс атомарного исправления (`rule_id`, `description`, `file_path`, `line_number`, `original_text`, `replacement_text`).
  - `FixResult` — датакласс результата обработки файла (`file_path`, `original_content`, `modified_content`, `diff_lines`, `fixes`).
  - `generate_file_fixes(content: str, file_path: Path) -> FixResult` — функция генерации хирургических строковых замен без внешних библиотек.
  - `atomic_write_file(file_path: Path, content: str) -> None` — атомарная запись через временный файл в том же каталоге и `os.replace`.
  - `git_check_clean(file_path: Path) -> bool` — проверка отсутствия незакоммиченных изменений в Git для целевого файла с мягкой деградацией при отсутствии Git.
  - `render_diff(diff_lines: List[str], use_color: bool = True) -> str` — форматирование и подсветка унифицированного диффа.
  - `run_linter(...)` — интеграция прохода автофикса, обработка флагов `--fix`, `--write`, `--dry-run`, `--allow-dirty`.
  - CLI parser (`argparse`) — регистрация аргументов `--fix`, `--write`, `--dry-run`, `--allow-dirty`.
* `[NEW]` `tests/test_kb_lint_fix.py`:
  - `TestKbLintAutoFixCore` — тесты детерминированных автофиксов для правил `KB-004`, `KB-005`, `KB-006`, `KB-007`, `KB-010`.
  - `TestKbLintAutoFixCLI` — тесты флагов CLI (`--fix`, `--write`, `--dry-run`, exit codes, вывод диффа).
  - `TestKbLintSafetyProtocol` — тесты атомарной записи, Git-Clean Guard и сохранения пользовательских комментариев.

---

## 3. Детали реализации

### 3.1. Структуры данных и правила автофикса

```python
@dataclass
class Fix:
    rule_id: str
    description: str
    file_path: Path
    line_number: int  # 1-based
    original_text: str
    replacement_text: str


@dataclass
class FixResult:
    file_path: Path
    original_content: str
    modified_content: str
    diff_lines: List[str]
    fixes: List[Fix]

    @property
    def has_changes(self) -> bool:
        return self.original_content != self.modified_content
```

### 3.2. Алгоритм хирургического строкового патчинга `generate_file_fixes`

1. **Разделители frontmatter (`KB-004`):**
   - Устранение пробелов вокруг маркеров `---` на строках разделителей.
2. **Формат дат (`KB-005`):**
   - Во frontmatter поиск полей `created:`, `updated:`, `date:`.
   - Если значение соответствует паттерну `YYYY.MM.DD` или `YYYY/MM/DD` — замена на `YYYY-MM-DD`.
3. **Концевые пробелы (`KB-006`):**
   - Удаление пробельных символов в конце строк: `line.rstrip(" \t")`.
4. **Завершающий перевод строки (`KB-007`):**
   - Гарантия наличия ровно одного `\n` в конце файла: `content.rstrip("\r\n") + "\n"`.
5. **Дефолтное поле `depends_on: []` (`KB-010`):**
   - Если файл находится в `02_Tasks/Specs/` или имя файла начинается с `TASK-`:
   - Если во frontmatter отсутствует ключ `depends_on:`, строка `depends_on: []\n` безопасно вставляется перед закрывающим разделителем `---`.
   - **Инвариант:** Все комментарии пользователей вида `# ...` внутри frontmatter сохраняются в исходных позициях.

### 3.3. Протокол безопасности Zero Data Loss

```python
def git_check_clean(file_path: Path) -> bool:
    """Returns True if the file has no unstaged/staged modifications in Git."""
    try:
        res = subprocess.run(
            ["git", "status", "--porcelain", str(file_path)],
            cwd=str(file_path.parent),
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if res.returncode != 0:
            return True  # Fallback for environments without git
        return len(res.stdout.strip()) == 0
    except Exception:
        return True  # Git not installed or not a git repo


def atomic_write_file(file_path: Path, content: str) -> None:
    """Writes content atomically using a temporary file and os.replace."""
    target_dir = file_path.parent
    target_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=str(target_dir), delete=False, encoding="utf-8", newline="") as tf:
        temp_name = tf.name
        tf.write(content)
    os.replace(temp_name, str(file_path))
```

### 3.4. Логика CLI и режимы работы

* `kb_lint.py --path docs --fix`:
  - Выполняет анализ базы знаний.
  - Генерирует и печатает унифицированные цветные диффы для всех файлов с исправлениями.
  - Файлы на диске **НЕ изменяются** (Safe Preview / Dry-Run).
  - Выводит финальную строку:
    `[DRY-RUN] Found X fixable issues in Y files. Run with '--fix --write' to apply.`
* `kb_lint.py --path docs --fix --write`:
  - Проверяет `git_check_clean` для каждого файла (если грязный и нет `--allow-dirty`, выдаёт `WARNING: Skipping <file> (uncommitted changes)`).
  - Атомарно перезаписывает чистые файлы.
  - Выводит:
    `[FIXED] Successfully applied X fixes in Y files.`

---

## 4. План верификации (Verification Plan)

- [ ] Синтаксическая компиляция: `python -m py_compile scripts/kb_lint.py` (Exit code 0).
- [ ] Запуск модульных тестов ядра автофикса: `python -m unittest tests/test_kb_lint_fix.py` (100% pass).
- [ ] Запуск полного сьюта существующих тестов: `python -m unittest discover -s tests` (100% pass, без регрессий).
- [ ] Прогон автофикса на реальной базе знаний в режиме dry-run: `python scripts/kb_lint.py --path docs --fix` (Exit code 0, 0 непреднамеренных мутаций).
- [ ] Проверка целостности базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links).

---

## 5. Критерии готовности (DoD)

- [ ] В `scripts/kb_lint.py` реализованы флаги `--fix`, `--dry-run`, `--write`, `--allow-dirty`.
- [ ] Реализован алгоритм хирургического строкового патчинга для правил `KB-004`, `KB-005`, `KB-006`, `KB-007`, `KB-010`.
- [ ] Пользовательские комментарии и форматирование frontmatter сохраняются на 100%.
- [ ] Атомарная запись через `tempfile` и Git-Clean Guard защищают от повреждения данных.
- [ ] Набор тестов `tests/test_kb_lint_fix.py` покрывает все правила, флаги и краевые случаи.
- [ ] Все пункты Плана верификации пройдены.
- [ ] Статус обновлён в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [ ] Запись добавлена в `Devlog.md`.
