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
