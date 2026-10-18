---
id: BUG-012
title: "Rules Check: test_render_status_dashboard зависит от GITHUB_REPOSITORY и ходит в живой GitHub API"
status: fixed
severity: high
type: bug
target_release: "v0.23.0"
target_phase: 22
release_blocker: false
fixed_in: "v0.23.0"
regression_test: "tests/test_kb_ingest.py::test_render_status_dashboard, tests/test_kb_ingest.py::test_render_status_dashboard_prefers_env_repository"
created: 2026-10-18
updated: 2026-10-18
tags:
  - bug
  - defect
  - ci
  - tests
  - quality-gates
  - phase22
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 🐞 Дефект: BUG-012 — Rules Check: `test_render_status_dashboard` зависит от `GITHUB_REPOSITORY` и ходит в живой GitHub API

> **ID:** BUG-012 | **Критичность:** High | **Статус:** fixed  
> **Релиз:** v0.23.0 | **Блокер:** Нет (устранён до создания тега)  
> **Канбан:** [[../Kanban|Канбан-доска]] | **Спецификация:** [[../../SPEC|SPEC.md]]  

---

## 1. Симптомы и окружение
* **Симптом:** В CI тест ждёт строку `my-org/my-project (auto-detect)`, но получает `koudinie101-png/agent-docs-harness (env)` → `AssertionError`. Локально проходит, потому что `GITHUB_REPOSITORY` не задан.
* **Окружение:** GitHub Actions, где платформа всегда экспортирует `GITHUB_REPOSITORY`; Python 3.11. Дополнительно тест делает реальный HTTP-запрос к `https://api.github.com/rate_limit` (в логах — `59/60` и `60/60 req/h`).
* **Масштаб:** те же 4 прогона, что и у BUG-011; падение стабильное, не флейк по времени, но зависит от сети и квоты GitHub API.

## 2. Шаги воспроизведения (Repro Steps)
1. Задать `GITHUB_REPOSITORY=koudinie101-png/agent-docs-harness` (как на Actions).
2. Выполнить `python -m unittest tests.test_kb_ingest.TestKbIngest.test_render_status_dashboard`.
3. Дашборд выбирает `env`-ветку, тест патчил только `detect_github_repo`, поэтому утверждение `(auto-detect)` падает.

**Ожидаемое:** тест изолирован от ambient-переменных, не обращается к сети и проверяет обе ветки приоритета (`env` и `auto-detect`) явно.
**Фактическое:** тест наследует `GITHUB_REPOSITORY` от CI и выполняет живой запрос к GitHub API.

## 3. Диагностика (Логи, Стек-трейс)
```text
FAIL: test_render_status_dashboard (test_kb_ingest.TestKbIngest.test_render_status_dashboard)
AssertionError: 'my-org/my-project (auto-detect)' not found in
  '... • Репозиторий:        koudinie101-png/agent-docs-harness (env)
       • Авторизация:        Anonymous (rate-limited)
       • Квота API:          60/60 req/h ...'
```

## 4. Первопричина (Root Cause Analysis — RCA)
1. `render_status_dashboard()` корректно отдаёт приоритет `os.environ["GITHUB_REPOSITORY"]`, и только затем вызывает `detect_github_repo()` (`scripts/kb_ingest.py:278–289`). Это правильное поведение для Actions.
2. Тест патчит `kb_ingest.detect_github_repo`, но не очищает `GITHUB_REPOSITORY` (`tests/test_kb_ingest.py:316`), поэтому env-ветка выигрывает, а мок detect не используется.
3. Actions всегда задаёт `GITHUB_REPOSITORY` → тест падает только в CI. Локально переменная отсутствует → зелёный.
4. Дополнительно тест вызывает реальный `urllib.request.urlopen("https://api.github.com/rate_limit")` (`scripts/kb_ingest.py:302`): unit-тест зависит от сети, квоты и задержек, а при исчерпании квоты (`60/60`) ведёт себя иначе.
5. **Системная причина:** отсутствие hermetic-профиля тестов и мока внешней границы (HTTP); тест не описывает предусловия окружения.

## 5. План исправления
* `[MODIFY]` `tests/test_kb_ingest.py::test_render_status_dashboard` — в `patch.dict(os.environ, {"GITHUB_REPOSITORY": ""})`; `patch("kb_ingest.urllib.request.urlopen", side_effect=OSError("network disabled"))`; сохранить проверки счётчиков Inbox и `(auto-detect)`.
* `[NEW]` `tests/test_kb_ingest.py::test_render_status_dashboard_prefers_env_repository` — задать `GITHUB_REPOSITORY`, замокать `urlopen`, проверить `(env)` и что `detect_github_repo` не вызывается (явный контракт приоритета).
* **Реализовано:** оба теста работают в hermetic-профиле; HTTP-граница всегда замокана (`urlopen` → `OSError`), добавлены утверждения `mock_urlopen.assert_called_once()`, `mock_detect.assert_not_called()` и fallback-строка `unknown/unknown req/h` — тест доказывает отсутствие реального сетевого вызова и корректную деградацию квоты.
* **Отклонено:** убрать env-ветку из продукта — сломает реальный сценарий GitHub Actions, где репозиторий известен только из переменной.

## 6. Верификация (Regression-First)
- [x] RED: с `GITHUB_REPOSITORY=koudinie101-png/agent-docs-harness` `test_render_status_dashboard` падает с `AssertionError: 'my-org/my-project (auto-detect)' not found` (воспроизведено локально 2026-10-18 и в 4 прогонах CI).
- [x] GREEN: после фикса оба теста проходят и с переменной, и без неё; реальных сетевых вызовов нет (`urlopen` замокан, тесты выполняются за ~0.01 с).
- [x] Новый тест фиксирует приоритет `env` → `auto-detect` и отсутствие вызова `detect_github_repo` при наличии переменной.
- [x] Полный сьют и линтер — 0 ошибок: 138 тестов OK (sandbox-safe обёртка `tmp/run_tests.py`, TRG-03); `kb_lint` — 232 файла, 2183 ссылки, 0 битых.
- [x] Прогон `Rules Check` на GitHub Actions зелёный (run [39113878440](https://github.com/koudinie101-png/agent-docs-harness/actions/runs/39113878440), коммит `6949cca`): шаг `Unit tests` успешен, 138 тестов на чистом `ubuntu-latest`.

## 7. Влияние и принятые решения
* Продуктовое поведение дашборда менять не нужно: приоритет `env` корректен и нужен в CI/форках.
* Дефект чисто тестовый, но блокирует Tier 1-гейт наравне с BUG-011: пока он открыт, `Rules Check` остаётся красным даже после починки git-теста.
