---
id: TASK-072
title: "Механический контроль медиа-ассетов в scripts/kb_lint.py и scripts/kb_release.py"
status: planned
type: task
phase: 18
component:
  - lint
  - release
  - assets
  - quality-gates
parent_plan: "[[../../Plans/PLAN-018-heterogeneous-ui-ux-and-visual-asset-harness|PLAN-018]]"
created: 2026-10-15
updated: 2026-10-15
tags:
  - task/spec
  - phase18
  - lint
  - release
  - assets
  - quality-gates
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-072 — Механический контроль медиа-ассетов в scripts/kb_lint.py и scripts/kb_release.py

> **ID:** TASK-072 | **Статус:** К реализации  
> **Фаза:** 18 | **Релиз:** v0.18.0  
> **План:** [[../../Plans/PLAN-018-heterogeneous-ui-ux-and-visual-asset-harness|PLAN-018]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../04_Research/RESEARCH-021-heterogeneous-ui-ux-and-visual-asset-management|RESEARCH-021]], [[../../../03_Decisions_ADR/ADR-0026-heterogeneous-ui-ux-and-visual-asset-management|ADR-0026]]

---

## 1. Цель задачи

Внедрить механический контроль качества Tier 1 для визуальных ассетов и медиа-ссылок в скриптах линтинга (`scripts/kb_lint.py`) и экспорта релизов (`scripts/kb_release.py`):
1. **Изолированная индексация медиафайлов в `kb_lint.py`:** поддержка расширений `(.png, .jpg, .jpeg, .webp, .svg, .gif, .canvas, .excalidraw)` с регистрацией в `file_map` **строго с расширением**, исключая перезапись и затенение `.md`-файлов с аналогичным стемом (например, скриншот `TASK-001.png` не должен заменять спецификацию `TASK-001.md`).
2. **Очистка параметров размера в `parse_wikilinks()`:** парсинг синтаксиса вставок Obsidian (`![[image.png|600x400]]` или `![[diagram.svg|300]]`) с корректным отсечением параметров размера до обращения к реестру файлов.
3. **Проверка стандартных изображений:** валидация локальных относительных путей в синтаксисе `![alt](relative/path)`.
4. **Asset Weight Gate:** автоматический контроль веса файлов в каталоге `docs/assets/` с выдачей неблокирующего предупреждения (`WARN`) при превышении лимита $2\text{ MB}$.
5. **Адаптация `convert_wikilinks_to_github_markdown()` в `scripts/kb_release.py`:** предотвращение ошибочного добавления суффикса `.md` к медиафайлам и корректная трансляция ссылок на изображения в публичных заметках GitHub.

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `scripts/kb_lint.py` — функции `build_file_map()`, `parse_wikilinks()`, `check_broken_links()`, добавление проверки `check_asset_weights()`.
* `[MODIFY]` `scripts/kb_release.py` — функция `convert_wikilinks_to_github_markdown()`.

---

## 3. Детали реализации

### 3.1. Индексация медиафайлов в `build_file_map()` (`kb_lint.py`)
```python
MEDIA_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".canvas", ".excalidraw"}

def build_file_map(root: Path):
    file_map = {}
    for p in root.rglob("*"):
        if not p.is_file() or p.name.startswith("."):
            continue
        ext = p.suffix.lower()
        if ext == ".md":
            # Регистрация по имени, стэму и относительному пути
            file_map[p.name] = p
            file_map[p.name.lower()] = p
            file_map[p.stem] = p
            file_map[p.stem.lower()] = p
        elif ext in MEDIA_EXTENSIONS:
            # Защита от коллизий: медиа регистрируются ТОЛЬКО с расширением!
            file_map[p.name] = p
            file_map[p.name.lower()] = p
            # Относительный путь от docs/
            rel = p.relative_to(root).as_posix()
            file_map[rel] = p
            file_map[rel.lower()] = p
    return file_map
```

### 3.2. Очистка параметров размера в `parse_wikilinks()`
При извлечении викиссылок:
```python
# Если ссылка содержит пайп размера: ![[image.png|600x400]]
raw_target = match.group(1).strip()
# Если начинается с ! — это эмбеддинг изображения
is_embed = raw_target.startswith("!")
if is_embed:
    raw_target = raw_target[1:].strip()

# Отсекаем параметры отображения/размера: image.png|600 -> image.png
if "|" in raw_target:
    clean_target = raw_target.split("|", 1)[0].strip()
```

### 3.3. Asset Weight Gate в `kb_lint.py`
```python
def check_asset_weights(root: Path, max_bytes: int = 2 * 1024 * 1024) -> List[str]:
    warnings = []
    assets_dir = root / "assets"
    if not assets_dir.exists():
        return warnings
    for p in assets_dir.rglob("*"):
        if p.is_file() and p.suffix.lower() in MEDIA_EXTENSIONS:
            size = p.stat().st_size
            if size > max_bytes:
                mb = size / (1024 * 1024)
                warnings.append(f"WARN: Asset '{p.relative_to(root).as_posix()}' exceeds size limit ({mb:.1f} MB > 2.0 MB)")
    return warnings
```

### 3.4. Адаптация `convert_wikilinks_to_github_markdown()` в `scripts/kb_release.py`
При автоконвертации ссылок:
* Определять, является ли целевой файл медиа-ассетом (`target.suffix.lower() in MEDIA_EXTENSIONS`).
* Для медиафайлов генерировать стандартный Markdown-синтаксис `![alt](url)` без принудительного аппенда `.md`.
* Очищать параметры размера Obsidian (`|600x400`).

---

## 4. План верификации (Verification Plan)

- [ ] Синтаксическая проверка: `python -m py_compile scripts/kb_lint.py scripts/kb_release.py` (Exit code 0).
- [ ] Тестирование линтера на базе знаний: `python scripts/kb_lint.py --path docs` (0 broken links).
- [ ] Проверка индексации медиа и синтаксиса размера: тест на викиссылку `![[test.png|600x400]]`.
- [ ] Проверка Asset Weight Gate: генерация временного тестового файла $> 2\text{ MB}$ в `docs/assets/` и проверка появления предупреждения `WARN: Asset ... exceeds size limit`.
- [ ] Проверка конвертации в `kb_release.py`: запуск тестов `tests/test_kb_release.py`.

---

## 5. Критерии готовности (DoD)

- [ ] Код написан строго по ТЗ без внешних зависимостей (Python 3 stdlib).
- [ ] Медиафайлы не затеняют одноименные `.md`-файлы задач.
- [ ] Параметры размера Obsidian корректно отсекаются в `kb_lint.py` и `kb_release.py`.
- [ ] Файлы $> 2\text{ MB}$ в `docs/assets/` детектируются с понятным предупреждением.
- [ ] Все пункты Плана верификации пройдены.
- [ ] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [ ] Запись добавлена в `Devlog.md`.
