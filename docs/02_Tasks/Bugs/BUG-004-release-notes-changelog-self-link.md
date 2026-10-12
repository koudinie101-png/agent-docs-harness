---
id: BUG-004
title: "Циклическая ссылка на саму себя в блоке Full Changelog релизных записок"
status: open
severity: medium
type: bug
target_release: "backlog"
target_phase: null
release_blocker: false
fixed_in: null
regression_test: "tests/test_kb_release.py"
created: 2026-10-12
updated: 2026-10-12
tags:
  - bug
  - defect
  - release
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
feedback_source: "[[../Inbox/FB-GH-4|FB-GH-4]]"
---

# 🐞 Дефект: BUG-004 — Циклическая ссылка на саму себя в блоке Full Changelog релизных записок

> **ID:** BUG-004 | **Критичность:** Medium | **Статус:** open  
> **Релиз:** backlog | **Блокер:** Нет  
> **Канбан:** [[../Kanban|Канбан-доска]] | **Спецификация:** [[../../SPEC|SPEC.md]]  
> **Источник фидбека:** [[../Inbox/FB-GH-4|FB-GH-4 (GitHub Issue #4)]]  

---

## 1. Симптомы и окружение
* **Симптом:** В сгенерированных `Release Notes` на странице GitHub в нижней части отображается пункт «Полный список изменений (Full Changelog)», ссылка в котором ведет на тот же самый тег релиза (`https://github.com/{owner}/{repo}/releases/tag/vX.Y.Z`). Вместо диффа изменений между релизами или ссылки на полный лог пользователь переходит на ту же самую страницу.
* **Окружение:** `scripts/kb_release.py`, генерация заметок релизов.

## 2. Шаги воспроизведения (Repro Steps)
1. Выполнить генерацию публичных заметок релиза для версии `v0.11.0`:
   ```bash
   python scripts/kb_release.py --version v0.11.0 --dry-run
   ```
2. Открыть `dist/RELEASE_NOTES.md` и просмотреть ссылку в секции `Full Changelog`:
   ```markdown
   **Полный список изменений (Full Changelog)**: https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.11.0
   ```
3. **Фактическое поведение:** Ссылка ведет на текущий релиз `releases/tag/v0.11.0`.
4. **Ожидаемое поведение:** Ссылка должна вести на сравнение версий на GitHub (`compare/v{previous}...v{current}`) либо на соответствующий артефакт в базе знаний/историю коммитов.

## 3. Диагностика (Логи, Стек-трейс)
В `scripts/kb_release.py` шаблон формирования строки `Full Changelog` использует URL текущего релиза вместо URL сравнения веток/тегов.

## 4. Первопричина (Root Cause Analysis — RCA)
В коде формирования релизных заметок переменная или ссылка `full_changelog_url` подставляется как `f"https://github.com/{repo}/releases/tag/{tag}"` вместо `f"https://github.com/{repo}/compare/{prev_tag}...{tag}"`.

## 5. План исправления
* `[MODIFY]` `scripts/kb_release.py` — определять предыдущий релизный тег и генерировать URL сравнения (`compare/{prev_tag}...{tag}`). Если предыдущего тега нет, ссылаться на коммиты или ветку.
* `[NEW]` `tests/test_kb_release.py` — добавить тест проверки корректности URL в строке `Full Changelog`.

## 6. Верификация (Regression-First)
- [ ] Падающий регрессионный тест воспроизводит дефект (RED).
- [ ] Исправление применено в коде (GREEN).
- [ ] Регрессионный тест и весь сьют проходят успешно (REFACTOR).
- [ ] Дефект закрыт через `/kb-implement BUG-004`.
