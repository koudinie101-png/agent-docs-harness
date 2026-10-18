---
id: BUG-010
title: "Утечка credentials из Git remote (PAT) в релизные артефакты и публичные Release Notes"
status: fixed
severity: critical
type: bug
target_release: "v0.21.0"
target_phase: 21
release_blocker: false
fixed_in: "v0.21.0"
regression_test: "tests/test_kb_release.py"
created: 2026-10-18
updated: 2026-10-18
tags:
  - bug
  - defect
  - release
  - security
  - credentials
  - phase21
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 🐞 Дефект: BUG-010 — Утечка credentials из Git remote (PAT) в релизные артефакты

> **ID:** BUG-010 | **Критичность:** Critical | **Статус:** fixed  
> **Релиз:** v0.21.0 | **Блокер:** Нет (устранён до создания тега)  
> **Канбан:** [[../Kanban|Канбан-доска]] | **Спецификация:** [[../../SPEC|SPEC.md]]  

> ⚠️ **Правило раскрытия:** детали не публикуются в GitHub Issues до подтверждения ротации токена. В отчёте не хранятся значения токенов.

---

## 1. Симптомы и окружение
* **Симптом:** Если Git remote настроен с встроенными credentials (например, `https://<user>:<token>@github.com/<owner>/<repo>.git` — типичный артефакт `git remote set-url` с PAT), то `scripts/kb_release.py` переносит этот URL «как есть» во frontmatter `docs/02_Tasks/Releases/RELEASE-vX.Y.Z.md` и в **публичный** `dist/RELEASE_NOTES.md` (ссылки TASK-ссылок, Full Changelog, Quick Install).
* **Окружение:** Кроссплатформенно; Python 3.8+, любой проект, установленный через `install.py`. Проявляется только при credentialed remote, поэтому легко проходит незамеченным в CI (там remote обычно чистый).

## 2. Шаги воспроизведения (Repro Steps)
1. Настроить remote с токеном: `git remote set-url origin https://owner:gho_***REDACTED***@github.com/owner/repo.git`.
2. Выполнить `python scripts/kb_release.py --version 0.21.0 --phase 21`.
3. Открыть `docs/02_Tasks/Releases/RELEASE-v0.21.0.md` -> в `github_release_url` присутствует токен.
4. Открыть `dist/RELEASE_NOTES.md` -> все ссылки вида `https://owner:gho_***@github.com/owner/repo/...`.
5. Опубликовать релиз -> токен попадает в публичные Release Notes на GitHub.

**Ожидаемое:** во всех артефактах используется публичный URL `https://github.com/owner/repo`.
**Фактическое:** credentials попадали в коммитимый документ и в публикуемый текст релиза.

## 3. Диагностика (Логи, Стек-трейс)
```text
# docs/02_Tasks/Releases/RELEASE-v0.21.0.md (до исправления)
github_release_url: "https://<user>:gho_***REDACTED***@github.com/<owner>/<repo>/releases/tag/v0.21.0"

# dist/RELEASE_NOTES.md (до исправления)
- ✨ Фича: [TASK-082](https://<user>:gho_***REDACTED***@github.com/<owner>/<repo>/blob/main/...)
**Полный список изменений (Full Changelog):** https://<user>:gho_***REDACTED***@github.com/<owner>/<repo>/compare/...
```

## 4. Первопричина (Root Cause Analysis — RCA)
1. `detect_release_environment()` сохранял `git remote get-url origin` без санитайзинга (`status["remote_url"] = res_remote.stdout.strip()`), поэтому credentials становились частью «окружения релиза» и попадали даже в `--detect-only` JSON-вывод/логи.
2. Нормализация URL была продублирована в четырёх местах (`generate_release_markdown`, `generate_public_release_notes`, `convert_wikilinks_to_github_markdown`) и обрабатывала **только** scp-форму `git@github.com:` -> `https://github.com/`. Встроенный userinfo (`user:token@`) не вырезался вовсе.
3. Отсутствовал Tier 1-барьер: ни один тест не проверял, что релизные артефакты не содержат credentials, поэтому дефект прошёл все прежние релизы незамеченным.

**Системная причина:** нормализация внешнего недоверенного ввода (URL remote) выполнялась ad-hoc на местах использования вместо единого санитайзера на границе (environment detection).

## 5. План исправления
* `[MODIFY]` `scripts/kb_release.py` — добавить `sanitize_repo_url()` (стриппинг userinfo `https://user:pass@host`, конвертация scp-ssh -> https, снятие `.git` и хвостового `/`), применённый в `detect_release_environment()`, `generate_release_markdown()`, `generate_public_release_notes()` и `convert_wikilinks_to_github_markdown()`.
* `[NEW]` `tests/test_kb_release.py` — регрессионный тест `test_regression_remote_credentials_not_leaked_into_release_outputs`: генерирует оба артефакта из credentialed remote и утверждает отсутствие токена при наличии чистого `https://github.com/...`.
* `[MODIFY]` `install.py` — пересобрать бандл (`scripts/build_release.py`), чтобы патч доехал до пользователей через `install.py --update`.

## 6. Верификация (Regression-First)
- [x] Падающий регрессионный тест воспроизводит дефект (RED) — *отклонение: тест написан одновременно с фиксом в одном проходе (дефект найден в pre-flight релиза, не мог быть отложен); тест валидирован на чистом `sanitize_repo_url` и на реальных артефактах.*
- [x] Исправление применено в коде `scripts/kb_release.py` (GREEN).
- [x] Регрессионный тест и весь сьют проходят успешно (REFACTOR): 120/120 тестов, `kb_lint` — 0 битых ссылок.
- [x] Дефект закрыт: `fixed_in: "v0.21.0"`; опубликованные артефакты и тело GitHub Release проверены на отсутствие credentials (`gh release view --json body` -> clean).
- [x] Рекомендованная реакция на компрометацию: ротация токена владельцем remote, очистка `.git/config` (`git remote set-url`), `gh auth setup-git`.

## 7. Влияние на пользователей и рекомендации
* Все пользователи, установившие харнесс до `v0.21.0`, несут риск при выпуске релиза с credentialed remote. Обновление: `python install.py --update`.
* Секреты никогда не должны храниться в URL remote; используйте credential helper (`gh auth setup-git`) или `GITHUB_TOKEN` в окружении.
