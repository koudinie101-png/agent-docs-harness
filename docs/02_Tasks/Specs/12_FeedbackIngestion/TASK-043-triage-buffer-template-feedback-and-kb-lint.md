---
id: TASK-043
title: "Буфер триажа, шаблон TEMPLATE_FEEDBACK и аудит в kb_lint.py"
status: in-progress
type: task
phase: 12
component:
  - templates
  - lint
  - feedback-buffer
parent_plan: "[[../../Plans/PLAN-012-feedback-ingestion-and-triage-buffer|PLAN-012]]"
created: 2026-10-11
updated: 2026-10-11
tags:
  - task/spec
  - phase12
  - feedback
  - triage
  - templates
  - lint
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-043 — Буфер триажа, шаблон TEMPLATE_FEEDBACK и аудит в kb_lint.py

> **ID:** TASK-043  
> **Статус:** В работе (Режим 2)  
> **Теги:** #task/spec #phase12 #feedback #triage #templates #lint  
> **Родительский план:** [[../../Plans/PLAN-012-feedback-ingestion-and-triage-buffer|PLAN-012]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-015-feedback-ingestion-channels-and-triage-heuristics|RESEARCH-015]], [[../../../03_Decisions_ADR/ADR-0020-feedback-ingestion-channels-and-triage-automation|ADR-0020]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Создать стандартизированный изоляционный буфер для входящей обратной связи, предотвращающий засорение базы знаний и потерю ссылок (Permalinks Invariant):
1. **Канонический шаблон входящих обращений:** Создать компактный High-SNR шаблон `TEMPLATE_FEEDBACK.md` в каталогах `docs/00_Templates/` и `templates/` с обязательными метаданными источника, воспринимаемой критичности, статуса и результирующего артефакта.
2. **Структура буфера триажа:** Инициализировать директорию `docs/02_Tasks/Inbox/` с заготовкой состояния `.inbox_state.json` и защитным `.gitignore` (для исключения локальных секретов и временных дампов).
3. **Аудит целостности буфера в `scripts/kb_lint.py`:** Добавить проверку обязательных полей YAML frontmatter для всех файлов в `docs/02_Tasks/Inbox/` (`id`, `title`, `status`, `channel`, `created`) и валидацию `status: new | triaged | processed | rejected`.

---

## 2. Затрагиваемые файлы и компоненты

* `[NEW]` `docs/00_Templates/TEMPLATE_FEEDBACK.md` — канонический шаблон входящего обращения в базе знаний.
* `[NEW]` `templates/TEMPLATE_FEEDBACK.md` — эталонный шаблон входящего обращения для упаковки инсталлятора.
* `[NEW]` `docs/02_Tasks/Inbox/.inbox_state.json` — начальное пустое состояние дедупликации с курсорами источников.
* `[NEW]` `docs/02_Tasks/Inbox/.gitignore` — игнорирование локальных дампов `Raw/` и файлов секретов в буфере.
* `[MODIFY]` `scripts/kb_lint.py` — регистрация требований к структуре frontmatter для каталога `02_Tasks/Inbox`.
* `[MODIFY]` `tests/test_kb_lint.py` — модульные тесты валидации файлов обращений в `Inbox/`.

---

## 3. Детали реализации

### 3.1. Структура `TEMPLATE_FEEDBACK.md`
```yaml
---
id: FB-XXX
title: "[Краткая суть обращения]"
status: new # new | triaged | processed | rejected
type: feedback
channel: github # github | email | paste | manual
perceived_severity: s2 # s1 (blocker) | s2 (major) | s3 (minor) | na
target: "" # [[../Bugs/BUG-XXX]] или [[../Roadmap#Icebox]]
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: "[Автор или адрес]"
source_ref: "[ID issue, Message-ID или ссылка]"
tags:
  - feedback
  - inbox
---

# 📥 Обращение: FB-XXX — [Краткая суть]

> **Источник:** [Канал / Ссылка] | **Статус:** [new / processed]  
> **Целевой артефакт:** [Ссылка на BUG-XXX / Roadmap]  

---

## 1. Исходное сообщение
<!-- Дословный текст или цитата обращения -->

## 2. Анализ и предварительный скрининг
<!-- Тип: Дефект / Идея / Вопрос / Спам -->
<!-- Воспринимаемая тяжесть и контекст окружения -->

## 3. Решение по триажу
<!-- Итог разбора: Конвертировано в BUG-XXX / Добавлено в Roadmap Icebox / Ответ пользователю / Отклонено -->
```

### 3.2. Начальное состояние `.inbox_state.json`
```json
{
  "version": 1,
  "github": {
    "last_issue_number": 0,
    "processed_ids": []
  },
  "email": {
    "last_uid": 0,
    "processed_message_ids": []
  },
  "paste": {
    "processed_hashes": []
  }
}
```

### 3.3. Аудит в `scripts/kb_lint.py`
В секцию правил проверки frontmatter добавляется валидация для путей, содержащих `02_Tasks/Inbox`:
- Обязательные поля: `['id', 'title', 'status', 'type', 'channel', 'created']`.
- Валидные статусы `status`: `['new', 'triaged', 'processed', 'rejected']`.

---

## 4. План верификации (Verification Plan)

- [ ] Модульные тесты линтера:
  ```bash
  python -m unittest tests/test_kb_lint.py
  ```
- [ ] Аудит базы знаний:
  ```bash
  python scripts/kb_lint.py --path docs
  ```
- [ ] Проверка синтаксиса шаблонов и `.inbox_state.json`:
  ```bash
  python -c "import json; json.load(open('docs/02_Tasks/Inbox/.inbox_state.json', encoding='utf-8'))"
  ```

---

## 5. Критерии готовности (DoD)

- [ ] Шаблоны `docs/00_Templates/TEMPLATE_FEEDBACK.md` и `templates/TEMPLATE_FEEDBACK.md` созданы и идентичны.
- [ ] Папка `docs/02_Tasks/Inbox/` инициализирована с валидным `.inbox_state.json`.
- [ ] Линтер `scripts/kb_lint.py` валидирует frontmatter файлов `Inbox/`, и тесты в `tests/test_kb_lint.py` проходят на 100%.
- [ ] Выполнен аудит целостности `kb_lint.py` с кодом возврата 0.
