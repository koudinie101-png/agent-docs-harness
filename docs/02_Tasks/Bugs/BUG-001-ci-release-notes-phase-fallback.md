---
id: BUG-001
title: "Рассинхронизация номера фазы и описания релиза в CI release.yml (fallback на Фазу 1)"
severity: major
component:
  - ci
  - automation
  - release
status: fixed
resolved: 2026-10-02
regression_test: "tests/test_kb_release.py"
created: 2026-10-02
updated: 2026-10-02
tags:
  - bug
  - release
  - ci
  - automation
kanban: "[[../Kanban|Канбан-доска]]"
---

# 🐞 Дефект: BUG-001 — Рассинхронизация номера фазы и описания релиза в CI release.yml

> **ID:** BUG-001 | **Критичность:** Major | **Статус:** Исправлен (Режим 3)  
> **Канбан:** [[../Kanban|Канбан-доска]] | **Теги:** #bug #release #ci #automation  

---

## 1. Симптомы и окружение
* **Симптом:** При автоматической публикации релиза на GitHub через GitHub Actions (`release.yml`) в заголовке и теле Release Notes указывается «Фаза 1» и шаблонное описание `Официальный релиз v0.X.0 по завершении Фазы 1.`, независимо от фактической фазы релиза (например, для `v0.8.0` / Фаза 8 и `v0.7.0` / Фаза 7). При этом локально в базе знаний создается корректный артефакт `RELEASE-vX.Y.Z.md`.
* **Окружение:** GitHub Actions Ubuntu runner (`.github/workflows/release.yml`), `scripts/kb_release.py`.

## 2. Шаги воспроизведения (Repro Steps)
1. Создать в базе знаний артефакт релиза `docs/02_Tasks/Releases/RELEASE-v0.8.0.md` с `phase: 8` и подробным `Executive Summary`.
2. Запустить генератор заметок в режиме CI без явного флага `--phase`, как это делает GitHub Actions:
   ```bash
   python scripts/kb_release.py --version v0.8.0 --ci-mode
   ```
3. **Фактическое поведение:** Скрипт генерирует `dist/RELEASE_NOTES.md` с `# 🚀 Release v0.8.0 — Фаза 1` и заглушкой `Executive Summary: Официальный релиз v0.8.0 по завершении Фазы 1.`
4. **Ожидаемое поведение:** Скрипт обнаруживает существующий файл `RELEASE-v0.8.0.md` как источник истины (Single Source of Truth), считывает из него фактическую фазу (8), реальное `Executive Summary`, список фич и формирует корректный `dist/RELEASE_NOTES.md`.

## 3. Диагностика (Логи, Стек-трейс)
Сгенерированный файл `dist/RELEASE_NOTES.md` в GitHub Actions:
```markdown
# 🚀 Release v0.8.0 — Фаза 1

> 💡 **Executive Summary:** Официальный релиз v0.8.0 по завершении Фазы 1.
```
В то время как в репозитории зафиксирован `docs/02_Tasks/Releases/RELEASE-v0.8.0.md`:
```yaml
---
id: RELEASE-v0.8.0
title: "Релиз v0.8.0: Фаза 8"
version: "0.8.0"
phase: 8
...
```

## 4. Первопричина (Root Cause Analysis — RCA)
1. **Жесткий дефолт `--phase` в CLI:** В `scripts/kb_release.py` параметр объявлен с `default=1`. В `.github/workflows/release.yml` скрипт вызывается командой `python scripts/kb_release.py --version ${{ github.ref_name }} --ci-mode` без передачи аргумента `--phase`.
2. **Игнорирование существующего артефакта базы знаний:** Скрипт `kb_release.py` при запуске не проверяет, существует ли уже `docs/02_Tasks/Releases/RELEASE-{tag}.md`. Он перетирает метаданные релизных заметок дефолтной фазой `1` и пустым описанием, вместо того чтобы извлечь `phase` и `summary` из канонического файла релиза.

## 5. План исправления
* `[NEW]` `tests/test_kb_release.py` — регрессионный тест `test_ci_mode_infers_phase_and_summary_from_existing_release_doc`: вызов без `--phase` при наличии `RELEASE-v0.8.0.md` должен сохранять фазу 8 и оригинальное саммари.
* `[MODIFY]` `scripts/kb_release.py` — перед обращением к дефолту `--phase` проверять наличие `docs/02_Tasks/Releases/RELEASE-{tag}.md` и считывать из него `phase` и `summary` (если они не переопределены явно пользователем в CLI).
* `[MODIFY]` `install.py` — синхронизация шаблона `release.yml` и встроенной версии `kb_release.py` при необходимости.
* `[RUN]` Пересборка инсталлятора через `python scripts/build_installer.py`.
* `[MANUAL]` Обновление тела релизов `v0.8.0` и `v0.7.0` на GitHub Releases.

## 6. Верификация (Regression-First)
- [x] Падающий регрессионный тест воспроизводит дефект (RED).
- [x] Исправление применено в коде `scripts/kb_release.py`.
- [x] Регрессионный тест и весь сьют проходят успешно (GREEN).
- [x] Проверка целостности базы знаний через `python scripts/kb_lint.py --path docs`.
- [x] Карточка дефекта перемещена в `Done` на Канбане и записана в `Devlog.md`.
