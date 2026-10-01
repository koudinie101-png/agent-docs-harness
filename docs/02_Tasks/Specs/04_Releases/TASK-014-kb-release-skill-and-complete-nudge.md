---
id: TASK-014
title: "Исполняемый скилл kb-release и интеграция подсказок в kb-complete"
status: done
type: task
phase: 4
component:
  - skills
  - release
  - workflow
  - nudge
parent_plan: "[[../../Plans/PLAN-004-release-management-and-lifecycle-automation|PLAN-004]]"
created: 2026-10-01
updated: 2026-10-01
tags:
  - task/spec
  - phase4
  - component/skills
  - component/release
  - component/workflow
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-014 — Исполняемый скилл kb-release и подсказки о релизе в kb-complete

> **ID:** TASK-014  
> **Статус:** Выполнено (Режим 3)  
> **Теги:** #task/spec #phase4 #component/skills #component/release #component/workflow  
> **Родительский план:** [[../../Plans/PLAN-004-release-management-and-lifecycle-automation|PLAN-004]]  
> **Связанные ADR и исследования:** [[../../../03_Decisions_ADR/ADR-0007-release-management-dual-mode-and-build-hook|ADR-0007]], [[../../../04_Research/RESEARCH-002-release-management-and-github-automation|RESEARCH-002]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Реализовать интерфейс взаимодействия AI-агентов и разработчиков с релизным процессом:
1. Создать 12-й исполняемый скилл `.agents/skills/kb-release/SKILL.md`, формализующий строгий регламент подготовки и публикации релизов.
2. Внедрить процедуру **Pre-flight Checks** (проверка чистоты рабочего дерева Git, завершенности всех задач текущей фазы в `Roadmap.md`, отсутствия незакрытых багов в `Bugs/` и успешного прохождения `kb_lint.py`).
3. Реализовать цепочку поиска сборочного контракта (**Build Hook Discovery**): поиск скрипта проекта (`scripts/build_release.py` / `scripts/build_release.sh`) либо стандартных манифестов (`package.json`, `pyproject.toml`, `Package.swift`, `*.csproj`, `Cargo.toml`).
4. Поддержать двухуровневую публикацию (**Dual-Mode**):
   - **GitHub Mode:** создание аннотированного тега `vX.Y.Z`, пуш в remote, публикация через `gh release create` или триггер GitHub Actions.
   - **Local-Only Mode:** сборка в `dist/`, вычисление SHA-256, создание локального `RELEASE-vX.Y.Z.md` и вывод итоговых локальных путей в консоль без внешних сетевых запросов.
5. Интегрировать в `.agents/skills/kb-complete/SKILL.md` ненавязчивую подсказку (**Nudge**): если при закрытии задачи все тикеты текущей фазы оказываются выполнены, агент выводит напоминание о проведении приемочного тестирования в `05_Testing/` и вызове `/kb-release`.
6. Актуализировать мастер-скилл `.agents/skills/docs-as-code/SKILL.md`.

---

## 2. Затрагиваемые файлы и компоненты

* `[NEW]` `.agents/skills/kb-release/SKILL.md` — 12-й канонический скилл релиз-менеджмента.
* `[MODIFY]` `.agents/skills/kb-complete/SKILL.md` — внедрение фазовой подсказки (Phase Completion Nudge).
* `[MODIFY]` `.agents/skills/docs-as-code/SKILL.md` — добавление команды `/kb-release` в сводную карту скиллов.

---

## 3. Детали технической реализации

### 3.1. Скилл `.agents/skills/kb-release/SKILL.md`

Скилл должен содержать метаданные и 7 строгих этапов выполнения:

```markdown
---
name: kb-release
description: >-
  Release Management: Execute pre-flight checks, trigger build hook contract to dist/,
  calculate SHA-256 checksums, generate RELEASE-vX.Y.Z.md, synchronize Roadmap/CHANGELOG,
  and publish via Dual-Mode (GitHub Releases with gh CLI or Local-Only package).
---

# /kb-release — Подготовка и публикация релиза фазы

Используйте этот скилл при выполнении команды `/kb-release <vX.Y.Z>`, завершении фазы проекта или подготовке дистрибутива.

## 🚨 Жесткие правила и ограничения
1. **Строго явный запуск:** Релиз НИКОГДА не запускается неявно или автоматически. Только прямой вызов пользователем `/kb-release <версия>`.
2. **Pre-flight блокировки:** Релиз не может быть создан, если в рабочей копии Git есть незакоммиченные файлы, если в фазе остались незавершенные задачи или линтер `kb_lint.py` сообщает об ошибках.
3. **Zero External Dependencies:** Работает исключительно на встроенных инструментах (Git, `gh` при наличии, Python stdlib `scripts/kb_release.py`).

## Пошаговая процедура

### Шаг 1: Pre-flight Checks (Предполетная проверка)
- Запуск `python scripts/kb_lint.py --path docs` -> Ожидается 0 broken links.
- Запуск тестов проекта (например, `python -m unittest discover -s tests`).
- Проверка `git status` -> Рабочее дерево должно быть чистым.
- Проверка `docs/02_Tasks/Roadmap.md` -> Все задачи текущей фазы должны быть отмечены `[x]`.

### Шаг 2: Определение среды и режима (Dual-Mode Detection)
- Вызов `python scripts/kb_release.py --detect-only` или определение через git/gh.
- Режим: `github` (если есть remote origin на github.com и gh CLI) либо `local-only`.

### Шаг 3: Вызов сборочного контракта (Build Hook Discovery)
Поиск и запуск команды сборки с выводом в каталог `dist/`:
1. `scripts/build_release.py` или `scripts/build_release.sh`.
2. Манифест стека (`package.json`, `pyproject.toml`, `Package.swift`, `*.sln`, `Cargo.toml`).
3. Если хук отсутствует: предупреждение в лог, создается Source Release (без бинарников).

### Шаг 4: Расчет хэшей и формирование релизного документа
- Запуск `python scripts/kb_release.py --version X.Y.Z --phase N`
- Создание `docs/02_Tasks/Releases/RELEASE-vX.Y.Z.md` с таблицей SHA-256 и чейнджлогом.

### Шаг 5: Синхронизация базы знаний
- Обновление `docs/02_Tasks/Roadmap.md`: отметка фазы `✅ Завершена (Релиз: Releases/RELEASE-vX.Y.Z)`.
- Обновление `CHANGELOG.md` (добавление секции релиза в начало файла).
- Запись в `docs/Devlog.md` с фиксацией контрольных сумм и ссылки на релиз.

### Шаг 6: Публикация
- **GitHub Mode:**
  1. `git add docs/ CHANGELOG.md`
  2. `git commit -m "chore(release): release vX.Y.Z"`
  3. `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
  4. `git push origin main --tags`
  5. Если `gh` авторизован: `gh release create vX.Y.Z dist/* --title "vX.Y.Z" --notes-file docs/02_Tasks/Releases/RELEASE-vX.Y.Z.md`
- **Local-Only Mode:**
  1. `git add docs/ CHANGELOG.md && git commit -m "chore(release): release vX.Y.Z (local)"`
  2. `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
  3. Вывод в чат блока с локальными путями к артефактам и SHA-256.

### Шаг 7: Финальная валидация
- `python scripts/kb_lint.py --path docs` -> подтверждение целостности всех ссылок на новый релиз.
```

---

### 3.2. Модификация `.agents/skills/kb-complete/SKILL.md`

В конец процедуры завершения задачи добавляется секция:

```markdown
### 💡 Фазовое напоминание (Phase Completion Nudge)
После отметки чекбокса задачи в `docs/02_Tasks/Roadmap.md` агент проверяет текущую фазу:
- Если все задачи текущей фазы теперь отмечены `[x]`:
  Вывести пользователю информационное сообщение:
  > `🎉 Все задачи Фазы N успешно завершены!`  
  > `Рекомендуется выполнить приемочные сценарии в docs/05_Testing/ и запустить команду:`  
  > `👉 /kb-release vX.Y.Z для автоматической сборки дистрибутива и публикации релиза.`
```

---

## 4. План верификации (Verification Plan)

### Валидация формата скиллов:
- [x] Проверить корректность структуры и YAML frontmatter в `.agents/skills/kb-release/SKILL.md`.
- [x] Проверить наличие ссылки на `/kb-release` в `.agents/skills/docs-as-code/SKILL.md`.

### Целостность базы знаний:
- [x] Запуск линтера Docs-as-Code:
  ```bash
  python scripts/kb_lint.py --path docs
  ```
  *(Ожидаемый результат: 0 broken wikilinks)*

---

## 5. Критерии готовности (Definition of Done)

- [x] Создан файл `.agents/skills/kb-release/SKILL.md` с полной документацией шагов.
- [x] В `.agents/skills/kb-complete/SKILL.md` добавлен шаг фазового напоминания (Nudge).
- [x] В `.agents/skills/docs-as-code/SKILL.md` актуализирована сводная таблица скиллов.
- [x] `kb_lint.py` подтверждает отсутствие сломанных ссылок в базе знаний.
