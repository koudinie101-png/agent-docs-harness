---
id: ADR-0020
title: "Архитектура сбора обратной связи (Feedback Ingestion), каналы, периодичность и двухстадийный триаж"
status: accepted
date: 2026-10-11
superseded_by: ""
tags:
  - adr
  - architecture
  - feedback-loops
  - ingestion
  - triage
  - scheduling
  - deduplication
  - docs-as-code
---

# ADR-0020: Архитектура сбора обратной связи (Feedback Ingestion), каналы, периодичность и двухстадийный триаж

> **Статус:** Принято  
> **Дата:** 2026-10-11  
> **Заменяет (Supersedes):** [[ADR-0008-feedback-loops-triage-buffer-and-local-diagnostics|ADR-0008: Архитектура каналов обратной связи, буфера триажа и локальной диагностики]]  
> **Первоисточник исследования:** [[../../04_Research/RESEARCH-015-feedback-ingestion-channels-and-triage-heuristics|RESEARCH-015: Архитектура сбора обратной связи (Feedback Ingestion)]]  
> **Связанные решения:** [[ADR-0001-zero-dependencies-python-stdlib|ADR-0001: Zero Dependencies]], [[ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009: High-SNR]], [[ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016: Single-Task Barrier]], [[ADR-0019-bug-lifecycle-triage-and-release-targeting|ADR-0019: Жизненный цикл дефектов]]

---

## 1. Контекст и проблема

В предыдущем решении [[ADR-0008-feedback-loops-triage-buffer-and-local-diagnostics|ADR-0008]] была заложена концепция изоляции базы знаний через промежуточный буфер `docs/02_Tasks/Inbox/`. Однако в процессе планирования выявились критические белые пятна реализации:
1. **Отсутствие автоматизации импорта (Ingestion Gap):** Ручное создание markdown-файлов для каждого обращения из внешнего мира (почта, GitHub Issues) создавало высокий барьер входа (friction).
2. **Риск дублирования при повторных запусках:** Отсутствовал стандарт фиксации курсора/смещения (offset/cursor), что приводило к повторному захвату одних и тех же issues и писем.
3. **Неопределенность периодичности (Scheduling Strategy):** Не был определен баланс между автономным периодическим сбором (фоновые демоны vs шедулеры) и On-Demand запуском разработчиком.
4. **Смешение типов и ранняя оценка критичности:** Оценка тяжести бага (Severity) до создания репродуцирующего автотеста приводила к недостоверным приоритетам в бэклоге.

---

## 2. Решение

Принята архитектура **многоканального сбора с дедупликацией и двухстадийным триажем**:

### 2.1. Буфер триажа и детерминированная дедупликация
1. Каталог **`docs/02_Tasks/Inbox/`** является точкой входа для всех внешних сигналов.
2. В соответствии с **Permalinks Principle (No Link Rot)** файлы обращений `FB-*.md` **никогда не перемещаются** физически в архивные подпапки. По завершении триажа обновляется YAML frontmatter: `status: processed` (или `status: rejected`) с фиксацией даты `triaged_date` и ссылкой на целевой артефакт `target: "[[...]]"`.
3. Префикс `02_Tasks/Inbox` добавляется в обязательный аудит frontmatter в `scripts/kb_lint.py`.
4. Файл **`docs/02_Tasks/Inbox/.inbox_state.json`** фиксирует смещения:
   - GitHub: номер последнего обработанного issue (`last_issue_number`) и массив ID.
   - Email: последний UID (`last_uid`) и хеши `Message-ID`.
   - Local Paste: SHA-256 хеши содержимого для отсечения повторов.

### 2.2. Каналы сбора (Ingestion Channels & Drivers)
Реализуется модуль **`scripts/kb_ingest.py`** (Zero Dependencies, Python 3 stdlib):
1. **GitHub Issues Driver:**
   - Интеграция через `gh issue list` либо GitHub REST API (`urllib.request`).
   - Импорт issues с меткой `needs-triage` в файлы `FB-GH-{number}.md`.
2. **Email (IMAP) Driver:**
   - Чтение почты по протоколу IMAP через `imaplib` и парсинг через `email`.
   - Учетные данные считываются строго из переменных окружения (`FEEDBACK_IMAP_USER`, `FEEDBACK_IMAP_PASS`) или локального `.env.local` (включен в `.gitignore`).
   - Конвертация писем в файлы `FB-MAIL-{YYYYMMDD}-{hash}.md`.
3. **Quick Paste Driver (Мессенджеры и буфер обмена):**
   - Возможность прямого добавления сырого текста из Telegram/Discord через CLI:  
     `python scripts/kb_ingest.py --paste --title "..." --text "..."`  
     или интерактивно в чате агента через `/kb-triage paste`.
4. **Local Diagnostic Bundle (`install.py --report`):**
   - Сохраняется возможность создания оффлайн-отчета окружения пользователем с переносом в `Inbox/`.

### 2.3. Периодичность и триггеры запуска (Кросс-агентная матрица)
Принят трехуровневый гибридный подход для всех поддерживаемых сред разработки:
1. **Основной режим (On-Demand — все среды):** Запуск разработчиком по требованию перед сессией планирования (`python scripts/kb_ingest.py` или шаг скилла `/kb-triage`).
2. **Облачный кросс-агентный уровень (GitHub Actions):** Шаблон `.github/workflows/feedback-sync.yml` запускается по расписанию (cron) и стягивает issues/письма в `Inbox/` автономно, не требуя запущенной IDE.
3. **Сессионный уровень целевых сред:**
   - **Antigravity:** нативный скилл `/schedule` для периодического запуска сбора в активной сессии.
   - **VS Code / Cursor / Windsurf / Cline / Roo Code:** задача запуска `python scripts/kb_ingest.py` в `.vscode/tasks.json` по событию открытия каталога (`folderOpen`).
   - **Claude Code CLI / Generic:** pre-flight правило в адаптерах правил (`CLAUDE.md`, `AGENTS.md`) для автоматической проверки `Inbox/` на старте диалога.
4. *Категорический отказ от платформенного фонового демона ОС (`daemon/service`).*

### 2.4. Двухстадийная эвристика триажа
1. **Стадия 1: Входной скрининг (Triage Screening):**
   - Классификация обращения на:
     - **Дефект:** фиксируется *Perceived Severity* (S1: Blocker, S2: Major, S3: Minor).
     - **Идея / Улучшение:** оценка *Value vs Effort*.
     - **Вопрос / Ошибка пользователя:** подготовка разъяснения для автора.
     - **Мусор / Спам:** отклонение.
2. **Стадия 2: Конвертация и исполнение:**
   - Дефект конвертируется в **`BUG-XXX`** (Режим 2B `kb-bug`) без права изменения кода. Окончательная тяжесть и статус валидируются в Режиме 3 (`kb-implement BUG-XXX`) через обязательный failing тест (Regression-First).
   - Идея направляется в **`Roadmap.md` (Icebox)** для дальнейшей проработки в Режиме 0 (`kb-research`) или Режиме 1 (`kb-plan`).
   - Вопрос/UX приводит к формированию ответа и при необходимости доработке **`docs/Onboarding.md`**.
   - В исходном файле `FB-*.md` обновляется статус на `status: processed`, указывается дата и ссылка на созданный артефакт (Permalinks Invariant).
   - Выполняется терминальный шаг **Stop & Yield**.

---

## 3. Отвергнутые варианты (Rejected Alternatives)

* **Фоновый демон в ОС (Background Daemon):** Отклонен из-за риска утечек памяти, зависания процессов и платформозависимости.
* **Прямые боты в мессенджерах (Telegram Bot / Slack Socket Mode):** Отклонены во избежание оверинжиниринга и необходимости аренды выделенного сервера для CLI-инструмента.
* **Назначение Verified Severity до воспроизведения:** Отклонено как нарушающее инженерную дисциплину TDD.

---

## 4. Последствия

### Плюсы:
* **Устранение рутины:** Обращения из GitHub и Email попадают в базу знаний одной командой.
* **Защита от дубликатов:** `.inbox_state.json` гарантирует детерминированность.
* **Чистый бэклог:** Четкое разделение багов (в Канбан/TDD) и идей (в Icebox).
* **Zero Dependencies:** Полная автономность на Python 3 stdlib.

### Минусы и компромиссы:
* Для чтения почты требуется первичная настройка переменных окружения IMAP.
* Появляется дополнительный служебный файл `docs/02_Tasks/Inbox/.inbox_state.json`.
