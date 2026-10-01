---
id: TASK-025
title: "Двухформатный экспорт и автоконвертер викиссылок в scripts/kb_release.py"
status: planned
type: task
phase: 7
component:
  - scripts
  - release-management
  - distribution
parent_plan: "[[../../Plans/PLAN-007-github-release-notes-and-distribution-standard|PLAN-007]]"
created: 2026-10-01
updated: 2026-10-01
tags:
  - task/spec
  - phase7
  - component/scripts
  - component/release
  - release-notes
  - supply-chain-security
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-025 — Двухформатный экспорт и автоконвертер викиссылок

> **ID:** TASK-025  
> **Статус:** К реализации (Режим 2)  
> **Теги:** #task/spec #phase7 #component/scripts #component/release #release-notes #supply-chain-security  
> **Родительский план:** [[../../Plans/PLAN-007-github-release-notes-and-distribution-standard|PLAN-007]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-005-github-release-notes-and-distribution-best-practices|RESEARCH-005]], [[../../../03_Decisions_ADR/ADR-0010-github-release-notes-and-public-distribution-standard|ADR-0010]], [[../../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Реализовать механизм двухформатного экспорта релизных заметок в утилите `scripts/kb_release.py` согласно стандарту [[../../../03_Decisions_ADR/ADR-0010-github-release-notes-and-public-distribution-standard|ADR-0010]]:
1. **Автоконвертер викиссылок:** Создать функцию `convert_wikilinks_to_github_markdown`, преобразующую относительные викиссылки Obsidian `[ [ target | alias ] ]` и `[ [ target ] ]` в валидные GFM-ссылки на GitHub на основе `remote.origin.url` и ветки `main`. В оффлайн/local-only режиме ссылки должны преобразовываться в жирный текст без сломанных скобок.
2. **Публичный релизный документ:** Создать функцию `generate_public_release_notes`, генерирующую `dist/RELEASE_NOTES.md` (чистый Markdown без YAML frontmatter, Executive Summary, команды Quick Install / Upgrade, категоризированный чейнджлог, таблица контрольных сумм SHA-256 со сниппетом верификации и ссылка на diff коммитов).
3. **Обновление CLI интерфейса:** Добавить автоматическую генерацию `dist/RELEASE_NOTES.md` при создании релиза и в `--ci-mode`, с поддержкой флага `--notes-output`.
4. **Тестирование:** Покрыть новый функционал модульными тестами в `tests/test_kb_release.py`.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `scripts/kb_release.py` — функции `convert_wikilinks_to_github_markdown`, `generate_public_release_notes`, аргумент `--notes-output`, автогенерация в `main()`.
* `[MODIFY]` `tests/test_kb_release.py` — юнит-тесты на преобразование ссылок, структуру публичных заметок и CLI-вызовы.

---

## 3. Детали реализации

### Сигнатуры и контракты в `scripts/kb_release.py`

```python
def convert_wikilinks_to_github_markdown(text: str, repo_url: str = "", branch: str = "main") -> str:
    """
    Конвертирует внутренние викиссылки Obsidian в чистый Markdown для GitHub:
    - [ [ path/to/spec | Title ] ] -> [Title](repo_url/blob/branch/docs/path/to/spec.md) (если repo_url задан)
    - [ [ path/to/spec | Title ] ] -> **Title** (если repo_url отсутствует)
    - [ [ Title ] ] -> **Title**
    """
    ...

def generate_public_release_notes(
    version: str,
    phase_num: int,
    env_info: Dict[str, Any],
    artifacts: List[Dict[str, Any]],
    phase_data: Dict[str, List[Dict[str, Any]]],
    summary: str = "",
) -> str:
    """
    Генерирует публичный Markdown для dist/RELEASE_NOTES.md:
    - Без YAML frontmatter
    - H1 заголовок с версией и названием фазы
    - Executive Summary
    - Сниппет быстрого старта (Quick Install / Update)
    - Что нового (Features, Bug Fixes, ADRs) с конвертированными ссылками
    - Таблица артефактов и SHA-256 хэшей
    - Инструкция по проверке контрольных сумм (PowerShell / Bash)
    - Ссылка на Full Changelog (git diff)
    """
    ...
```

### CLI Аргументы в `scripts/kb_release.py`:
- `--notes-output` (str, default: `dist/RELEASE_NOTES.md`): целевой путь для публичных заметок.
- При обычном запуске или `--ci-mode`: создавать оба файла — внутренний `docs/02_Tasks/Releases/RELEASE-{tag}.md` и публичный `dist/RELEASE_NOTES.md`.

---

## 4. План верификации (Verification Plan)

- [ ] Модульные тесты: `python -m unittest tests/test_kb_release.py` (100% Pass).
- [ ] Ручная верификация: `python scripts/kb_release.py --version 0.7.0 --phase 7 --dry-run` выводит чистые публичные заметки.
- [ ] Линтер базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links).

---

## 5. Критерии готовности (DoD)

- [ ] Конвертер викиссылок и генератор публичных заметок реализованы на stdlib Python без внешних зависимостей.
- [ ] Все тесты в `tests/test_kb_release.py` завершаются успешно (Exit code 0).
- [ ] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [ ] Запись о задаче добавлена в `docs/Devlog.md`.
