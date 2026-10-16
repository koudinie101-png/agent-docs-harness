---
id: TASK-079
title: "Строгая резолюция медиа-путей и проверка топологии check_asset_layout() в scripts/kb_lint.py"
status: done # planned | in-progress | done | cancelled
type: task
phase: 20
component:
  - lint
  - assets
  - quality-gates
parent_plan: "[[../../Plans/PLAN-020-asset-storage-hardening-and-layout-linting|PLAN-020]]"
created: 2026-10-15
updated: 2026-10-15
tags:
  - task/spec
  - phase20
  - lint
  - assets
  - quality-gates
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-079 — Строгая резолюция медиа-путей и проверка топологии check_asset_layout() в scripts/kb_lint.py

> **ID:** TASK-079 | **Статус:** Выполнено (Режим 3)  
> **Фаза:** 20 | **План:** [[../../Plans/PLAN-020-asset-storage-hardening-and-layout-linting|PLAN-020]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../04_Research/RESEARCH-022-asset-storage-hardening-and-task-scoped-namespaces|RESEARCH-022]], [[../../../03_Decisions_ADR/ADR-0027-task-scoped-asset-namespaces-and-layout-linting|ADR-0027]]

---

## 1. Цель задачи

Устранить ложноположительное разрешение одноименных медиафайлов (`tobe.svg`, `asis.svg`, `empty_tobe.svg`) и внедрить механический барьер (Tier 1 Quality Gate) для защиты корневой топологии `docs/assets/`:
1. **Запрет bare-filename fallback для ссылок с разделителями путей (`/` или `\`):** в `scripts/kb_lint.py` исключить срабатывание `link_name in file_map`, если ссылка содержит относительный путь (`../../assets/mockups/windows/TASK-098/tobe.svg`). Fallback по голому имени разрешен только для плоских викиссылок Obsidian без слешей (`![[Pasted image 20261015.png]]`).
2. **Проверка топологии `check_asset_layout(docs_dir: Path) -> List[str]`:** неблокирующая проверка (Tier 1 Non-blocking Quality Gate, выдает `WARN` без падения с Exit code 1 по аналогии с `check_asset_weights()`), контролирующая:
   - все подкаталоги первого уровня внутри `docs/assets/` принадлежат строго каноническому множеству `VALID_ASSET_ROOTS = {"mockups", "screenshots", "diagrams", "design"}` (и в корне `docs/assets/` нет неразмеченных файлов);
   - элементы внутри `docs/assets/mockups/<target>/` и `docs/assets/mockups/flows/` (кроме системных dotfiles вроде `.gitkeep`) являются папками, соответствующими шаблону `^(TASK|BUG)-\d{3,}(?:-[a-zA-Z0-9_-]+)?$`.
3. **Покрытие модульными тестами в `tests/test_kb_lint.py`:** проверка перехвата коллизий одноименных `tobe.svg` в разных `TASK-XXX/` (Exit code 1), сохранения обратной совместимости плоских викиссылок `![[Pasted image.png]]` и выдачи предупреждений `WARN` в `check_asset_layout()` при неразрешенных папках в `docs/assets/` или плоских файлах в `mockups/<target>/`.

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `scripts/kb_lint.py` — константа `VALID_ASSET_ROOTS`, функция `check_asset_layout(docs_dir: Path) -> List[str]`, интеграция в `run_linter()` и сужение условия `file_map` fallback для медиа-ссылок.
* `[MODIFY]` `tests/test_kb_lint.py` — модульные тесты для `check_asset_layout()` и защиты от ложноположительного разрешения одноименных медиафайлов (`tobe.svg`).

---

## 3. Детали реализации

### 3.1. Константа и функция `check_asset_layout()` в `scripts/kb_lint.py`

```python
VALID_ASSET_ROOTS = {"mockups", "screenshots", "diagrams", "design"}
TASK_NAMESPACE_PATTERN = re.compile(r"^(?:TASK|BUG)-\d{3,}(?:-[a-zA-Z0-9_-]+)?$")


def check_asset_layout(docs_dir: Path) -> List[str]:
    warnings: List[str] = []
    assets_dir = docs_dir / "assets"
    if not assets_dir.is_dir() and (docs_dir / "docs" / "assets").is_dir():
        assets_dir = docs_dir / "docs" / "assets"
    if not assets_dir.is_dir():
        return warnings

    for item in sorted(assets_dir.iterdir()):
        if item.name.startswith("."):
            continue
        if item.is_dir():
            if item.name not in VALID_ASSET_ROOTS:
                allowed_str = ", ".join(sorted(VALID_ASSET_ROOTS))
                warnings.append(
                    f"WARN: Invalid top-level asset directory 'assets/{item.name}/'. "
                    f"Allowed roots in docs/assets/: {allowed_str}. "
                    f"Move platform folders inside 'assets/mockups/{item.name}/' or 'assets/screenshots/{item.name}/'."
                )
        elif item.is_file():
            warnings.append(
                f"WARN: Unorganized file 'assets/{item.name}' in root of docs/assets/. "
                f"Place assets inside mockups/, screenshots/, diagrams/, or design/."
            )

    mockups_dir = assets_dir / "mockups"
    if mockups_dir.is_dir():
        for target_dir in sorted(mockups_dir.iterdir()):
            if not target_dir.is_dir() or target_dir.name.startswith("."):
                continue
            for entry in sorted(target_dir.iterdir()):
                if entry.name.startswith("."):
                    continue
                if not entry.is_dir() or not TASK_NAMESPACE_PATTERN.match(entry.name):
                    rel_entry = f"assets/mockups/{target_dir.name}/{entry.name}"
                    warnings.append(
                        f"WARN: Non-task mockup entry '{rel_entry}'. "
                        f"Expected task-scoped directory 'assets/mockups/{target_dir.name}/TASK-XXX/' (ADR-0027)."
                    )
    return warnings
```

### 3.2. Исправление резолюции медиа-путей и интеграция в `run_linter()`

В `run_linter()` (`scripts/kb_lint.py`, строки ~723–751):
```python
            if not found:
                has_path_sep = ("/" in link or "\\" in link)
                if link_ext in MEDIA_EXTENSIONS or "." in link_name:
                    if not has_path_sep and (link_name in file_map or link_name_lower in file_map):
                        found = True
                    elif (
                        link in file_map
                        or link.lower() in file_map
                        or stripped_link in file_map
                        or stripped_link.lower() in file_map
                    ):
                        found = True
                else:
                    if not has_path_sep and (link_stem in file_map or link_stem_lower in file_map):
                        found = True
```
Вызвать `asset_layout_warnings = check_asset_layout(docs_dir)` и вывести блок предупреждений `⚠️ Asset Layout Warnings (Non-blocking)` при наличии элементов.

### 3.3. Модульные тесты в `tests/test_kb_lint.py`

* `test_same_name_media_in_different_task_folders_no_false_positive`: наличие `TASK-047/tobe.svg` не маскирует битую ссылку на `TASK-098/tobe.svg` (Exit code 1).
* `test_bare_wikilink_media_still_resolves`: плоская ссылка `![[Pasted image 20261015.png|600]]` продолжает резолвиться (Exit code 0).
* `test_check_asset_layout_warns_rogue_platform_dir_and_flat_mockup`: папка `docs/assets/windows/` и плоский файл `docs/assets/mockups/web/login.svg` вызывают `WARN` в `check_asset_layout()`, не роняя `run_linter()` (Exit code 0).
* `test_check_asset_layout_allows_canonical_roots`: папки `mockups/windows/TASK-001/tobe.svg`, `screenshots`, `diagrams`, `design` проходят с пустым списком предупреждений `[]`.

---

## 4. План верификации (Verification Plan)

- [x] Сборка: `python -m py_compile scripts/kb_lint.py tests/test_kb_lint.py` (Exit code 0).
- [x] Автотесты линтера: `pytest tests/test_kb_lint.py` (Exit code 0, 100% pass).
- [x] Проверка базы знаний: `python scripts/kb_lint.py --path docs` (Exit code 0).

---

## 5. Критерии готовности (DoD)

- [x] Код написан строго по ТЗ без заглушек.
- [x] Все пункты Плана верификации пройдены.
- [x] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [x] Запись добавлена в `Devlog.md`.
