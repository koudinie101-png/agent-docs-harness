---
id: TASK-071
title: "Архитектура хранения ассетов, композитный --ui и Obsidian DX в install.py"
status: in-progress # planned | in-progress | done | cancelled
type: task
phase: 18
component:
  - installer
  - assets
  - obsidian
  - cli
parent_plan: "[[../../Plans/PLAN-018-heterogeneous-ui-ux-and-visual-asset-harness|PLAN-018]]"
created: 2026-10-15
updated: 2026-10-15
tags:
  - task/spec
  - phase18
  - installer
  - assets
  - obsidian
  - multi-target
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-071 — Архитектура хранения ассетов, композитный --ui и Obsidian DX в install.py

> **ID:** TASK-071 | **Статус:** В работе  
> **Фаза:** 18 | **Релиз:** v0.18.0  
> **План:** [[../../Plans/PLAN-018-heterogeneous-ui-ux-and-visual-asset-harness|PLAN-018]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../04_Research/RESEARCH-021-heterogeneous-ui-ux-and-visual-asset-management|RESEARCH-021]], [[../../../03_Decisions_ADR/ADR-0026-heterogeneous-ui-ux-and-visual-asset-management|ADR-0026]]

---

## 1. Цель задачи

Реализовать в утилите установки `install.py` поддержку композитных UI-профилей и инфраструктуру хранения визуальных ассетов в соответствии с [ADR-0026](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/docs/03_Decisions_ADR/ADR-0026-heterogeneous-ui-ux-and-visual-asset-management.md):
1. Расширить парсер и логику флага `--ui`: поддерживать как одиночные профили (`auto`, `none`, `web`, `mobile`, `desktop`, `tui`), так и произвольный список узлов через запятую (например, `--ui windows,android`, `--ui macos,ios`, `--ui web,mobile`).
2. Реализовать двухступенчатую раскладку директорий в `docs/assets/`:
   - Single-target (1 узел): `docs/assets/mockups/<target>/`, `docs/assets/screenshots/<target>/`.
   - Multi-target ($\ge 2$ узлов): дополнительно `docs/assets/mockups/flows/`, `docs/assets/screenshots/multi-device/`, а также каталог протоколов `docs/01_Architecture/Protocols/`.
3. Автоматически настраивать маршрутизацию вложений Obsidian через `docs/.obsidian/app.json` (`"attachmentFolderPath": "assets/screenshots"`), обеспечивая безопасный JSON-мерж настроек при `install.py --update`.
4. Включить в `.gitignore` правила: `!.obsidian/app.json` (версионирование настроек вложений) и `tmp/ui_snapshots/` (защита от раздувания Git временными диффами тестов).
5. Динамически генерировать стартовые документы `docs/01_Architecture/UI_Design_System.md` и `docs/01_Architecture/Targets/<Platform>.md` через `create_starter_docs()`, **не добавляя новых файлов в `docs/00_Templates/`** и сохраняя жесткий лимит объема шаблонов ($\le 28\text{ KB}$).

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `install.py` — парсинг аргументов `--ui`, валидация и нормализация профилей, расширение `scaffold_structure()`, безопасный мерж `app.json` в `setup_obsidian()`, обновление `handle_gitignore()`, динамическая генерация дизайн-системы и спецификаций узлов в `create_starter_docs()`.

---

## 3. Детали реализации

### 3.1. Нормализация и парсинг `--ui` в `install.py`

В `parse_args()` и сопутствующих хелперах:
```python
def normalize_ui_targets(ui_arg: Optional[str]) -> List[str]:
    """Разбивает строку --ui по запятым, очищает пробелы и приводит к lowercase.
    
    Примеры:
      'none' -> []
      'web' -> ['web']
      'windows, android' -> ['windows', 'android']
      'auto' -> [результат автодетекта]
    """
```
Если передано `none` — визуальный контур не разворачивается.  
Если передан 1 узел — активируется Single-Target режим.  
Если передано $\ge 2$ узлов — активируется Multi-Target режим.

### 3.2. Раскладка каталогов в `scaffold_structure()`
При наличии UI-таргетов создаются:
```python
# Базовые директории ассетов
assets_dirs = [
    target_dir / "docs" / "assets" / "mockups",
    target_dir / "docs" / "assets" / "screenshots",
]
for t in ui_targets:
    assets_dirs.append(target_dir / "docs" / "assets" / "mockups" / t)
    assets_dirs.append(target_dir / "docs" / "assets" / "screenshots" / t)

# Дополнительно для multi-target:
if len(ui_targets) > 1:
    assets_dirs.append(target_dir / "docs" / "assets" / "mockups" / "flows")
    assets_dirs.append(target_dir / "docs" / "assets" / "screenshots" / "multi-device")
    assets_dirs.append(target_dir / "docs" / "01_Architecture" / "Protocols")
    assets_dirs.append(target_dir / "docs" / "01_Architecture" / "Targets")
```

### 3.3. Настройка Obsidian `docs/.obsidian/app.json`
В функции `setup_obsidian(target_dir, is_update=False)`:
```python
app_json_path = target_dir / "docs" / ".obsidian" / "app.json"
app_data = {}
if app_json_path.exists():
    try:
        app_data = json.loads(app_json_path.read_text(encoding="utf-8"))
    except Exception:
        app_data = {}

# Безопасный мерж настройки роутинга вложений:
app_data["attachmentFolderPath"] = "assets/screenshots"
app_json_path.write_text(json.dumps(app_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
```

### 3.4. Исключения в `handle_gitignore()`
В функции `handle_gitignore(target_dir)` гарантировать наличие:
```text
!.obsidian/app.json
tmp/ui_snapshots/
```

### 3.5. Динамическая генерация в `create_starter_docs()`
При активном UI-контуре генерировать `docs/01_Architecture/UI_Design_System.md` со схемой семантических токенов (`Color.Brand`, `Spacing.Card`, `Action.Primary`).  
Для гетерогенных систем ($\ge 2$ узлов) генерировать шаблоны для каждого узла `docs/01_Architecture/Targets/<Platform>.md` с разделами: фоновые ограничения, энергопотребление, жизненный цикл и платформенные рекомендации.

---

## 4. План верификации (Verification Plan)

- [ ] Синтаксическая проверка: `python -m py_compile install.py` (Exit code 0).
- [ ] Ручной прогон в изолированном временном каталоге:
  ```bash
  python install.py /tmp/test-ui-single --ui web --non-interactive
  python install.py /tmp/test-ui-multi --ui windows,android --non-interactive
  ```
- [ ] Проверка существования `docs/.obsidian/app.json` с `"attachmentFolderPath": "assets/screenshots"`.
- [ ] Проверка `.gitignore` на наличие `!.obsidian/app.json` и `tmp/ui_snapshots/`.
- [ ] Проверка сохранения лимита шаблонов: `docs/00_Templates/` не содержит новых файлов.

---

## 5. Критерии готовности (DoD)

- [ ] Код написан строго по ТЗ без внешних зависимостей (Python 3 stdlib).
- [ ] Флаг `--ui` поддерживает одиночные и композитные значения через запятую.
- [ ] При `--update` существующий `app.json` мержится без потери пользовательских настроек.
- [ ] Все пункты Плана верификации пройдены.
- [ ] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [ ] Запись добавлена в `Devlog.md`.
