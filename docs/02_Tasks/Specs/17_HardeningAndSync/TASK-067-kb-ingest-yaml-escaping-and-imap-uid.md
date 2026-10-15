---
id: TASK-067
title: "Безопасное экранирование YAML, постоянные IMAP UIDs и URL-кодирование в scripts/kb_ingest.py"
status: done
type: task
phase: 17
component:
  - ingestion
parent_plan: "[[../../Plans/PLAN-017-core-hardening-and-ssot-sync|PLAN-017]]"
created: 2026-10-14
updated: 2026-10-15
tags:
  - task/spec
  - phase17
  - ingestion
  - imap
  - yaml
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-067 — Безопасное экранирование YAML, постоянные IMAP UIDs и URL-кодирование в scripts/kb_ingest.py

> **ID:** TASK-067 | **Статус:** Выполнено  
> **Фаза:** 17 | **Релиз:** v0.17.0  
> **План:** [[../../Plans/PLAN-017-core-hardening-and-ssot-sync|PLAN-017]] | **Канбан:** [[../../Kanban|Канбан]]  

---

## 1. Цель задачи
Обеспечить отказоустойчивость импорта обратной связи в `scripts/kb_ingest.py`:
1. Защитить генерируемый YAML frontmatter заметок `FB-XXX.md` от синтаксических сбоев при наличии кавычек в заголовках, именах авторов и ссылках.
2. Перевести IMAP-драйвер с эфемеридных номеров последовательности на постоянные `UID` для корректной работы дедупликации в `.inbox_state.json`.
3. Обеспечить корректное URL-кодирование меток GitHub Issues, содержащих пробелы и спецсимволы.

---

## 2. Затрагиваемые файлы
* `[MODIFY]` `scripts/kb_ingest.py` — функции `build_feedback_markdown()`, `EmailIngestDriver.fetch_emails()`, `GitHubIngestDriver.fetch_issues()`.
* `[MODIFY]` `tests/test_kb_ingest.py` — тесты экранирования YAML, мок-тесты `client.uid` и URL-encoding.

---

## 3. Детали реализации

### 3.1. Безопасная сериализация полей frontmatter в `build_feedback_markdown()`
Использовать `json.dumps()` для строковых значений, содержащих пользовательский ввод:
```python
def build_feedback_markdown(
    fb_id: str,
    title: str,
    channel: str,
    body: str,
    author: str = "",
    source_ref: str = "",
    created_date: str = "",
    perceived_severity: str = "s2"
) -> str:
    today = created_date or datetime.date.today().isoformat()
    clean_title = json.dumps(title, ensure_ascii=False)
    clean_author = json.dumps(author, ensure_ascii=False)
    clean_source_ref = json.dumps(source_ref, ensure_ascii=False)

    return f"""---
id: {fb_id}
title: {clean_title}
status: new
type: feedback
channel: {channel}
perceived_severity: {perceived_severity}
target: ""
created: {today}
updated: {today}
author: {clean_author}
source_ref: {clean_source_ref}
tags:
  - feedback
  - inbox
---
...
```

### 3.2. Постоянные IMAP UIDs в `EmailIngestDriver.fetch_emails()`
Заменить вызовы `client.search` и `client.fetch` на интерфейс `UID`:
```python
typ, data = client.uid("search", None, "UNSEEN")
if typ != "OK" or not data or not data[0]:
    client.logout()
    return []

uids = data[0].split()
for uid in uids:
    typ, fetch_data = client.uid("fetch", uid, "(RFC822)")
    if typ != "OK":
        continue
    uid_str = uid.decode("ascii", errors="replace")
    # Использовать uid_str для проверки состояния дедупликации и state_manager
```

### 3.3. URL-кодирование меток GitHub
В `GitHubIngestDriver.fetch_issues()`:
```python
quoted_label = urllib.parse.quote(label)
url = f"https://api.github.com/repos/{self.repo}/issues?state=open&labels={quoted_label}&per_page=100"
```

---

## 4. План верификации (Verification Plan)
- [x] Автотесты: `pytest tests/test_kb_ingest.py` — 100% pass.
- [x] Тест экранирования: запуск `build_feedback_markdown()` с `title='Crash: "Error 404"'` и `author='"John" <j@ex.com>'` — YAML валиден и парсится без ошибок.
- [x] Тест IMAP: проверка мока `mock_client.uid.assert_called()` с UNSEEN и RFC822.
- [x] Тест GitHub: вызов `fetch_issues(label="help wanted")` формирует запрос с `labels=help%20wanted`.

---

## 5. Критерии готовности (DoD)
- [x] Код написан строго по ТЗ без внешних зависимостей (Python `stdlib`).
- [x] Все пункты Плана верификации пройдены.
- [x] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [x] Запись добавлена в `Devlog.md`.
