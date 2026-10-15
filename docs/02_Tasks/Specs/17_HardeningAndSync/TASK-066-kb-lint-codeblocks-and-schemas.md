---
id: TASK-066
title: "Харденинг парсинга викиссылок и валидация схем frontmatter в scripts/kb_lint.py"
status: done
type: task
phase: 17
component:
  - lint
parent_plan: "[[../../Plans/PLAN-017-core-hardening-and-ssot-sync|PLAN-017]]"
created: 2026-10-14
updated: 2026-10-15
tags:
  - task/spec
  - phase17
  - lint
  - schemas
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-066 — Харденинг парсинга викиссылок и валидация схем frontmatter в scripts/kb_lint.py

> **ID:** TASK-066 | **Статус:** Выполнено  
> **Фаза:** 17 | **Релиз:** v0.17.0  
> **План:** [[../../Plans/PLAN-017-core-hardening-and-ssot-sync|PLAN-017]] | **Канбан:** [[../../Kanban|Канбан]]  

---

## 1. Цель задачи
Устранить ложные срабатывания и слепые зоны в линтере базы знаний `scripts/kb_lint.py`:
1. Исключить распознавание демонстрационных ссылок внутри fenced code blocks (```...```) и инлайн-кода (`` `...` ``).
2. Поддержать корректное извлечение ссылок из Markdown-таблиц Obsidian с экранированными пайпами (`[[path/to/XXX_note\|Label]]`).
3. Запретить невалидный fallback на `file_map` для ссылок с явным путем (`/`), маскирующий битые относительные ссылки на GitHub.
4. Расширить валидацию обязательных полей frontmatter на каталоги `06_Memory/Incidents/`, `02_Tasks/Specs/`, `02_Tasks/Bugs/` и `03_Decisions_ADR/`.

---

## 2. Затрагиваемые файлы
* `[MODIFY]` `scripts/kb_lint.py` — функции `parse_wikilinks()`, `check_file_frontmatter()`, `run_linter()`.
* `[MODIFY]` `tests/test_kb_lint.py` — тесты экранирования, код-блоков, относительных путей и схем frontmatter.

---

## 3. Детали реализации

### 3.1. Очистка кода перед извлечением викиссылок в `parse_wikilinks()`
```python
def parse_wikilinks(content: str) -> list:
    # 1. Вырезать блоки кода ```...``` и инлайн-код `...`
    stripped = re.sub(r'```[\s\S]*?```', '', content)
    stripped = re.sub(r'`[^`\n]*`', '', stripped)
    
    # 2. Поиск викиссылок: [[target|label]], [[target#heading|label]], [[target]]
    pattern = re.compile(r'\[\[([^\]\|#]+)(?:#[^\]\|]*)?(?:\\?\|[^\]]*)?\]\]')
    matches = pattern.findall(stripped)
    
    # 3. Нормализация ссылок с очисткой от экранирующих слэшей
    cleaned = []
    for m in matches:
        target = m.rstrip("\\").strip()
        if target:
            cleaned.append(target)
    return cleaned
```

### 3.2. Строгий резолв относительных путей в `run_linter()`
```python
# Если ссылка содержит '/' (относительный путь), fallback по голому имени файла запрещен!
if not found:
    if "/" not in link and (link_name_no_ext in file_map or link_name_lower in file_map):
        found = True

if not found:
    broken_links.append((rel, link))
```

### 3.3. Валидация frontmatter для инцидентов памяти и заметок жизненного цикла
В `check_file_frontmatter()` добавить проверку схем:
* `06_Memory/Incidents/`: `["id", "title", "status", "created"]`
* `02_Tasks/Specs/`: `["id", "title", "status", "type", "phase", "parent_plan", "created"]`
* `02_Tasks/Bugs/`: `["id", "title", "status", "severity", "type", "created"]`
* `03_Decisions_ADR/`: `["id", "title", "status", "type", "created"]`

---

## 4. План верификации (Verification Plan)
- [x] Автотесты: `pytest tests/test_kb_lint.py` — 100% pass.
- [x] Проверка экранированных пайпов: запуск теста с `[[path/to/XXX_note\|Title]]` в таблице — ссылка успешно находится.
- [x] Проверка код-блоков: запуск теста с `[[XXX-non-existent-doc]]` внутри ``` — ошибка не генерируется.
- [x] Проверка битого пути: `[[../XXX_WrongDir/TASK-001]]` при существующем `TASK-001` в другой папке — линтер регистрирует broken link.
- [x] Проверка базы знаний: `python scripts/kb_lint.py --path docs` — Exit code 0, 0 broken links.

---

## 5. Критерии готовности (DoD)
- [x] Код написан строго по ТЗ с сохранением Zero-Dependencies (только `stdlib` Python).
- [x] Все пункты Плана верификации пройдены.
- [x] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [x] Запись добавлена в `Devlog.md`.
