---
id: TASK-044
title: "Zero-Dependencies модуль импорта обратной связи (scripts/kb_ingest.py) и тесты"
status: in-progress
type: task
phase: 12
component:
  - ingestion
  - python-stdlib
  - automation
parent_plan: "[[../../Plans/PLAN-012-feedback-ingestion-and-triage-buffer|PLAN-012]]"
created: 2026-10-11
updated: 2026-10-11
tags:
  - task/spec
  - phase12
  - ingestion
  - python-stdlib
  - github
  - email
  - deduplication
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-044 — Zero-Dependencies модуль импорта обратной связи (scripts/kb_ingest.py) и тесты

> **ID:** TASK-044  
> **Статус:** В работе (Режим 2)  
> **Теги:** #task/spec #phase12 #ingestion #python-stdlib #github #email #deduplication  
> **Родительский план:** [[../../Plans/PLAN-012-feedback-ingestion-and-triage-buffer|PLAN-012]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-015-feedback-ingestion-channels-and-triage-heuristics|RESEARCH-015]], [[../../../03_Decisions_ADR/ADR-0020-feedback-ingestion-channels-and-triage-automation|ADR-0020]], [[../../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Разработать автономную, кроссплатформенную утилиту импорта `scripts/kb_ingest.py` на стандартной библиотеке Python 3 (Zero Dependencies):
1. **Многоканальный сбор:** Реализовать драйверы для сбора из GitHub Issues (`gh` CLI или GitHub REST API v3 via `urllib.request`), Email (IMAP via `imaplib` + `email`), и Quick Paste/CLI аргументов.
2. **Детерминированная дедупликация:** Сохранение состояния смещений (offsets/cursors/hashes) в `docs/02_Tasks/Inbox/.inbox_state.json` с гарантией идемпотентности при повторных запусках.
3. **Безопасная работа с секретами:** Поддержка переменных окружения (`FEEDBACK_IMAP_USER`, `FEEDBACK_IMAP_PASS`, `GITHUB_TOKEN`) и локального `.env.local` без риска утечки в Git.
4. **Комплексное тестирование:** Написание изолированных модульных тестов с моками сетевых протоколов (GitHub API, IMAP).

---

## 2. Затрагиваемые файлы и компоненты

* `[NEW]` `scripts/kb_ingest.py` — автономный скрипт импорта обратной связи.
* `[NEW]` `tests/test_kb_ingest.py` — модульные тесты драйверов импорта и дедупликации.
* `[MODIFY]` `.gitignore` — добавление `.env.local` и локальных временных файлов.

---

## 3. Детали реализации

### 3.1. Архитектура и интерфейс `scripts/kb_ingest.py`
CLI-интерфейс утилиты:
```bash
python scripts/kb_ingest.py [--github] [--email] [--paste] [--all] [--dry-run] [--inbox-dir PATH]
```

Ключевые классы и функции:
```python
class InboxStateManager:
    """Управление курсорами и дедупликацией в .inbox_state.json"""
    def __init__(self, state_file: Path): ...
    def is_github_processed(self, issue_num: int) -> bool: ...
    def mark_github_processed(self, issue_num: int): ...
    def is_email_processed(self, message_id: str, uid: int) -> bool: ...
    def mark_email_processed(self, message_id: str, uid: int): ...
    def is_content_processed(self, content_hash: str) -> bool: ...
    def mark_content_processed(self, content_hash: str): ...
    def save(self): ...

class GitHubIngestDriver:
    """Импорт issues с меткой needs-triage через REST API или gh CLI"""
    def fetch_issues(self, repo: str = None, token: str = None) -> list[dict]: ...

class EmailIngestDriver:
    """Чтение непрочитанных сообщений по IMAP через imaplib и email"""
    def fetch_emails(self, host: str, user: str, password: str, folder: str = "INBOX") -> list[dict]: ...

def ingest_paste(text: str, title: str, author: str, inbox_dir: Path, state: InboxStateManager) -> str:
    """Создание файла FB-PASTE-*.md из сырого текста"""
    ...
```

### 3.2. Формат генерируемых файлов в `Inbox/`
- Имена файлов:
  - GitHub: `FB-GH-{number}.md`
  - Email: `FB-MAIL-{YYYYMMDD}-{hash[:8]}.md`
  - Paste: `FB-PASTE-{YYYYMMDD}-{hash[:8]}.md`
- Тело формируется строго по структуре `TEMPLATE_FEEDBACK.md`.

---

## 4. План верификации (Verification Plan)

- [ ] Модульные тесты `tests/test_kb_ingest.py`:
  ```bash
  python -m unittest tests/test_kb_ingest.py
  ```
- [ ] Верификация сухого прогона (Dry Run):
  ```bash
  python scripts/kb_ingest.py --paste --title "Test Feedback" --text "Sample text" --dry-run
  ```
- [ ] Проверка дедупликации: создание файла через `--paste`, повторный вызов без флага `--dry-run` возвращает пропуск уже обработанного хеша (Exit code 0, 0 duplicates created).

---

## 5. Критерии готовности (DoD)

- [ ] `scripts/kb_ingest.py` работает исключительно на стандартной библиотеке Python 3 (Zero Dependencies).
- [ ] Поддерживаются все три канала: GitHub Issues, Email (IMAP), Quick Paste.
- [ ] Механизм дедупликации через `.inbox_state.json` полностью исключает появление повторных записей.
- [ ] Модульные тесты покрывают моки GitHub REST API, IMAP-клиента и парсера почты со 100% успехом.
