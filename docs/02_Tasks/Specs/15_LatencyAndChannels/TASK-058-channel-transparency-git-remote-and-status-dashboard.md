---
id: TASK-058
title: "Прозрачный UX инжеста, автодетект Git Remote и дашборд статуса источников в scripts/kb_ingest.py"
status: planned
type: task
phase: 15
component:
  - ingestion
  - git-remote
  - cli
  - zero-deps
parent_plan: "[[../../Plans/PLAN-015-response-latency-and-channel-transparency|PLAN-015]]"
created: 2026-10-12
updated: 2026-10-12
tags:
  - task/spec
  - phase15
  - ingestion
  - git-remote
  - transparency
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-058 — Прозрачный UX инжеста, автодетект Git Remote и дашборд статуса источников в scripts/kb_ingest.py

> **ID:** TASK-058 | **Статус:** К реализации  
> **План:** [[../../Plans/PLAN-015-response-latency-and-channel-transparency|PLAN-015]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Обоснование:** [[../../../04_Research/RESEARCH-019-user-centric-ingestion-and-channel-transparency|RESEARCH-019]], [[../../../03_Decisions_ADR/ADR-0024-user-centric-ingestion-and-channel-transparency|ADR-0024]]  

---

## 1. Цель задачи

Устранить эффект «черного ящика» и проблему немых пропусков (Silent Skipping) в модуле сбора обратной связи `scripts/kb_ingest.py`:
1. **Zero-Dependencies автоопределение GitHub репозитория:** извлечение имени `owner/repo` из локального `git config --get remote.origin.url` (поддержка HTTPS, SSH, token auth) без необходимости ручного задания `GITHUB_REPOSITORY`. Переменная среды `GITHUB_REPOSITORY` сохраняется как приоритетное ручное переопределение (override).
2. **Инвариант прозрачности каналов (Channel Transparency Invariant):** строгий запрет немых пропусков источников. Если канал активирован, но не настроен, скрипт обязан вывести предупреждение `⚠️ Warning: [Канал] пропущен: [Причина и инструкция по настройке]`. Для анонимных обращений к GitHub API выводить информационную плашку с подсказкой о переходе с лимита 60 req/h на 5000 req/h через токен.
3. **Гибкие фильтры инжеста:** внедрение CLI-флагов `--label <NAME>` (по умолчанию `needs-triage` для обратной совместимости) и `--all-open` (сбор всех открытых issues репозитория за исключением Pull Requests).
4. **Диагностический дашборд источников (`--status`):** команда для мгновенного отображения состояния каналов (GitHub, Email, буфер `docs/02_Tasks/Inbox/`), остатка лимитов API и курсоров смещения дедупликации `.inbox_state.json`.
5. **Информативная обработка HTTP-ошибок:** явные подсказки пользователю при получении кодов 401 (неверный токен), 403 (исчерпание квоты rate limit) и 404 (репозиторий не найден / приватный).
6. **Модульное тестирование:** полное покрытие новых функций в `tests/test_kb_ingest.py` на стандартной библиотеке Python 3.

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `scripts/kb_ingest.py` — функции `detect_github_repo`, `render_status_dashboard`, флаги `--status`, `--label`, `--all-open`, предупреждения о пропуске, обработка HTTP-ошибок.
* `[MODIFY]` `tests/test_kb_ingest.py` — модульные тесты автодетекта URL, флагов фильтрации, дашборда статуса и обработки ошибок.
* `[MODIFY]` `docs/02_Tasks/Kanban.md` — связывание пермалинком и актуализация статуса.
* `[MODIFY]` `docs/02_Tasks/Roadmap.md` — связывание пермалинком на спецификацию.

---

## 3. Детали реализации

### 3.1. Функция `detect_github_repo`
```python
def detect_github_repo(repo_root: Optional[Path] = None) -> Optional[str]:
    """
    Zero-dependencies detection of GitHub owner/repo from git config remote.origin.url.
    Supports HTTPS, SSH, and personal access token URL schemes:
      - https://github.com/owner/repo.git
      - https://github.com/owner/repo
      - git@github.com:owner/repo.git
      - https://x-access-token:...@github.com/owner/repo.git
    Returns 'owner/repo' or None.
    """
```
- Если задана переменная `os.environ.get("GITHUB_REPOSITORY")`, она имеет наивысший приоритет.
- Выполняет `subprocess.run(["git", "config", "--get", "remote.origin.url"], capture_output=True, text=True, check=False, cwd=repo_root)`.
- Парсит URL регулярным выражением:
  `r'(?:git@github\.com:|https://(?:[^@]+@)?github\.com/)([\w.-]+)/([\w.-]+?)(?:\.git)?$'`
- Безопасно перехватывает `FileNotFoundError` (git не установлен) и любые исключения, возвращая `None`.

### 3.2. Инвариант прозрачности каналов и информативные предупреждения
- В `run_ingest`:
  - Если `github=True`, но `repo` не определен ни через env, ни через git:
    Вывести: `⚠️ Warning: Канал GitHub пропущен: репозиторий не найден. Убедитесь, что настроен git remote origin или задана переменная GITHUB_REPOSITORY.`
  - Если `github=True`, `repo` определен, но `token` пуст:
    Вывести: `ℹ️ Info: GitHub опрашивается анонимно (лимит 60 req/h). Для лимита 5000 req/h настройте GITHUB_TOKEN в .env.local или переменных среды.`
  - Если `email_mode=True`, но `FEEDBACK_IMAP_HOST` / `FEEDBACK_IMAP_USER` не заданы:
    Вывести: `⚠️ Warning: Канал Email пропущен: не настроены переменные FEEDBACK_IMAP_HOST / FEEDBACK_IMAP_USER.`
- В `GitHubIngestDriver`:
  - Перехватывать `urllib.error.HTTPError`:
    - 401: `❌ Ошибка GitHub API: Неверный или просроченный GITHUB_TOKEN (HTTP 401 Unauthorized).`
    - 403: `❌ Ошибка GitHub API: Превышен лимит запросов API (HTTP 403 Forbidden). Используйте GITHUB_TOKEN или дождитесь сброса лимита.`
    - 404: `❌ Ошибка GitHub API: Репозиторий '{self.repo}' не найден или является приватным (HTTP 404 Not Found).`
    - Прочие: `❌ Ошибка GitHub API: HTTP {e.code} ({e.reason}).`

### 3.3. Фильтры `--label` и `--all-open`
- В `GitHubIngestDriver.fetch_issues(label: str = "needs-triage", all_open: bool = False) -> list`:
  - Если `all_open=True`:
    `url = f"https://api.github.com/repos/{self.repo}/issues?state=open&per_page=100"`
  - Иначе:
    `url = f"https://api.github.com/repos/{self.repo}/issues?state=open&labels={label}&per_page=100"`
  - Фильтрация Pull Requests:
    Игнорировать элементы с `'pull_request' in issue`.

### 3.4. Диагностический режим `--status`
- Функция `render_status_dashboard(inbox_dir: Path, repo_root: Path) -> int`:
  Выводит структурированный дашборд:
  ```text
  ======================================================================
  📊 Docs-as-Code Feedback Ingestion Status Dashboard
  ======================================================================
  [Канал: GitHub Issues]
    • Репозиторий:        {repo} ({source: auto-detect | env | not-found})
    • Авторизация:        {Token configured | Anonymous (rate-limited)}
    • Квота API:          {remaining}/{limit} req/h (Сброс: {reset_time})
    • Фильтр по умолчанию: --label {default_label}
    • Курсор смещения:    last_issue_number={last_issue}, processed={count}

  [Канал: Email (IMAP)]
    • Хост / Пользователь: {host} / {user} ({configured | not-configured})
    • Курсор смещения:    last_uid={last_uid}, processed={count}

  [Буфер обращений: docs/02_Tasks/Inbox/]
    • Всего тикетов:      {total}
    • Статусы:            new: {new_count} | processed: {proc_count} | rejected: {rej_count}
  ======================================================================
  ```
  При передаче флага `--status` дашборд печатается, и утилита завершает работу с кодом 0 без выполнения инжеста.

---

## 4. План верификации (Verification Plan)

- [ ] Синтаксическая корректность: `python -m py_compile scripts/kb_ingest.py tests/test_kb_ingest.py` (Exit code 0)
- [ ] Модульные тесты инжеста: `python -m unittest tests/test_kb_ingest.py` (100% Pass, Exit code 0)
- [ ] Тестирование CLI дашборда: `python scripts/kb_ingest.py --status` (Exit code 0)
- [ ] Тестирование CLI с флагом `--dry-run`: `python scripts/kb_ingest.py --github --dry-run` (Exit code 0)
- [ ] Полный регрессионный сьют проекта: `python -m unittest discover -s tests` (100% Pass, Exit code 0)
- [ ] Аудит базы знаний: `python scripts/kb_lint.py --path docs` (Exit code 0, 0 broken links)

---

## 5. Критерии готовности (DoD)

- [ ] Реализован автодетект `detect_github_repo` для HTTPS, SSH и токенизированных URL.
- [ ] Внедрены предупреждения при пропуске каналов (Channel Transparency Invariant).
- [ ] Добавлены флаги `--status`, `--label <NAME>` и `--all-open`.
- [ ] Реализован текстовый дашборд статуса источников с проверкой лимитов API и состояния `Inbox/`.
- [ ] Разработаны исчерпывающие модульные тесты в `tests/test_kb_ingest.py`.
- [ ] Все пункты Плана верификации пройдены.
- [ ] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [ ] Запись добавлена в `Devlog.md`.
