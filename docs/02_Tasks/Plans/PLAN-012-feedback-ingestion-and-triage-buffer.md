---
id: PLAN-012
title: "Фаза 12: Воронка каналов обратной связи, автоматизация импорта и буфер триажа (Feedback Ingestion & Triage Buffer)"
status: accepted
type: plan
phase: 12
created: 2026-10-11
updated: 2026-10-11
tags:
  - plan
  - phase12
  - feedback-loops
  - ingestion
  - triage
  - docs-as-code
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 📋 План: PLAN-012 — Фаза 12: Воронка каналов обратной связи, автоматизация импорта и буфер триажа

> **ID:** PLAN-012  
> **Статус:** Согласовано (Режим 1)  
> **Теги:** #plan #phase12 #feedback-loops #ingestion #triage #docs-as-code  
> **Родительская спецификация:** [[../../SPEC|SPEC.md]]  
> **Канбан:** [[../Kanban|Канбан-доска]]  
> **Связанные исследования и ADR:** [[../../04_Research/RESEARCH-015-feedback-ingestion-channels-and-triage-heuristics|RESEARCH-015: Архитектура сбора обратной связи]], [[../../03_Decisions_ADR/ADR-0020-feedback-ingestion-channels-and-triage-automation|ADR-0020: Архитектура сбора обратной связи, каналы, периодичность и двухстадийный триаж]], [[../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001: Zero Dependencies]], [[../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009: High-SNR]], [[../../03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016: Single-Task Barrier]], [[../../03_Decisions_ADR/ADR-0019-bug-lifecycle-triage-and-release-targeting|ADR-0019: Жизненный цикл дефектов]]

---

## 1. Контекст и цели (Problem & Goals)

### Проблема
1. **Засорение трекера задач неструктурированным фидбеком:**  
   Прямое создание задач Канбана или `BUG-XXX` из каждого сообщения внешних пользователей ведет к деградации базы знаний: 70–80% тикетов содержат невоспроизводимые сбои, вызваны ошибками окружения или являются дубликатами.
2. **Высокий барьер ручного импорта (Friction):**  
   Ручное создание markdown-файлов для писем и GitHub issues отнимает много времени, а отсутствие централизованного учета смещений (offset/cursor) порождает риск дубликатов при повторных синхронизациях.
3. **Отсутствие кросс-агентной автоматизации сбора:**  
   Пользователи разных сред разработки (Cursor, Windsurf, Cline, Claude Code, Antigravity) не имеют единого автоматизированного контура доставки обращений в базу знаний.
4. **Нарушение инварианта неизменяемости ссылок (Permalinks):**  
   Физическое перемещение файлов входящих обращений в архивные подпапки приводит к поломке викиссылок (`Link Rot`).
5. **Преждевременная оценка тяжести:**  
   Определение тяжести дефекта до попытки воспроизведения и написания падающего автотеста нарушает инженерный TDD-контракт.

### Цели Фазы 12
1. **Буфер триажа (Triage Buffer) и строгий Permalinks Invariant:**  
   Создать каталог `docs/02_Tasks/Inbox/` и шаблон `TEMPLATE_FEEDBACK.md`. При разборе обращений статус меняется строго в frontmatter (`status: processed` со ссылкой на результирующий артефакт `target: "[[...]]"`) без физического переноса файлов.
2. **Zero-Dependencies модуль импорта (`scripts/kb_ingest.py`):**  
   Разработать автономную утилиту на стандартной библиотеке Python 3 со встроенными драйверами: GitHub Issues (REST API / `gh`), Email (IMAP via `imaplib`/`email`) и Quick Paste для мессенджеров, с детерминированной дедупликацией через `docs/02_Tasks/Inbox/.inbox_state.json`.
3. **Декларативные формы GitHub и кросс-агентный Cloud Cron:**  
   Внедрить `.github/ISSUE_TEMPLATE/bug_report.yml` и `config.yml`, а также шаблон периодического облачного workflow `.github/workflows/feedback-sync.yml`, обеспечивающего фоновый сбор обращений независимо от открытой IDE.
4. **Исполняемый скилл `/kb-triage` и кросс-агентные правила:**  
   Создать скилл `.agents/skills/kb-triage/SKILL.md` с двухстадийным триажем (входной скрининг $\to$ конвертация в `BUG-XXX` / `Roadmap.md Icebox` / FAQ) и терминальным шагом Stop & Yield. Актуализировать адаптеры правил агентов (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`).
5. **Оффлайн-диагностика и синхронизация инсталлятора:**  
   Реализовать безопасный CLI-флаг `--report` в `install.py` для оффлайн-сбора системных данных, пересобрать монолит через `scripts/build_installer.py`, покрыть E2E тестами и актуализировать документацию.

---

## 2. Обсуждение и решения (Q&A / Discussion)

* **Q1: Почему в качестве основного механизма дедупликации выбран `.inbox_state.json`, а не хранение метаданных в Git-тегах?**  
  * **Решение (согласно [[../../03_Decisions_ADR/ADR-0020-feedback-ingestion-channels-and-triage-automation|ADR-0020]]):** Файл состояния в каталоге `Inbox/` автономен, не требует прав на манипуляцию с Git-тегами, работает одинаково стабильно как в Local-Only режиме, так и в облачном GitHub Actions.
* **Q2: Как соблюдается принцип неизменяемости ссылок (Permalinks)?**  
  * **Решение:** Файлы `FB-*.md` никогда не перемещаются в архивные подпапки. По завершении триажа скилл обновляет `status: processed` (или `status: rejected`) и проставляет `target: "[[../Bugs/BUG-XXX]]"`. Ссылки на обращения в Devlog и Roadmap остаются вечными.
* **Q3: Как обеспечивается безопасность почтовых паролей и токенов?**  
  * **Решение:** Утилита `scripts/kb_ingest.py` считывает пароли строго из переменных окружения (`FEEDBACK_IMAP_PASS`) либо локального `.env.local`, который автоматически игнорируется Git. Никакие секреты не коммитятся в репозиторий.

---

## 3. Архитектурное влияние и риски

* **Затрагиваемые файлы и модули:**
  - `docs/00_Templates/TEMPLATE_FEEDBACK.md` — новый канонический шаблон входящих обращений.
  - `docs/02_Tasks/Inbox/` — буфер триажа и служебный файл состояния `.inbox_state.json`.
  - `scripts/kb_ingest.py` — автономный скрипт импорта обратной связи (Zero-Deps: GitHub, Email, Quick Paste).
  - `tests/test_kb_ingest.py` — юнит-тесты драйверов импорта и механизма дедупликации.
  - `.github/ISSUE_TEMPLATE/` — веб-формы `bug_report.yml` и `config.yml`.
  - `.github/workflows/feedback-sync.yml` — кросс-агентный шедулер импорта в GitHub Actions.
  - `.agents/skills/kb-triage/SKILL.md` — новый исполняемый скилл двухстадийного триажа.
  - `scripts/kb_lint.py` — валидация обязательного YAML frontmatter для каталога `02_Tasks/Inbox`.
  - `AGENTS.md` и адаптеры (`GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`) — регистрация скилла `/kb-triage` и правил триажа.
  - `install.py`, `scripts/build_installer.py` — поддержка флага `--report`, упаковка шаблонов `Inbox` и новых скриптов.
  - `tests/test_installer.py` — E2E регрессионные тесты инсталлятора с новым функционалом.
  - `SPEC.md`, `README.md`, `docs/Onboarding.md` — актуализация витрины и документации онбординга.
* **Риски:**
  - *Риск сбоев сети при IMAP-опросе:*  
    *Митигация:* Изоляция сетевых вызовов в `try-except`, детерминированные таймауты (10с) и сохранение целостности `.inbox_state.json` только при успешном завершении транзакции.

---

## 4. Декомпозиция задач (Task Breakdown)

- [ ] **TASK-043:** Буфер триажа, шаблон TEMPLATE_FEEDBACK и аудит в kb_lint.py
- [ ] **TASK-044:** Zero-Dependencies модуль импорта обратной связи (`scripts/kb_ingest.py`) и тесты
- [ ] **TASK-045:** GitHub Issue Forms и облачный workflow кросс-агентной синхронизации
- [ ] **TASK-046:** Исполняемый скилл `/kb-triage` и интеграция в правила агентов
- [ ] **TASK-047:** Диагностический модуль `install.py --report`, синхронизация сборщика и E2E тесты

---

## 5. Критерии приемки плана (DoD Режима 1)

- [x] Концепция согласована с пользователем (READ-ONLY, без изменения кода).
- [ ] Дорожная карта `Roadmap.md` обновлена (Фаза 12 перенесена из Icebox в активный трек).
- [ ] Карточки добавлены в `Kanban.md` в `📥 Бэклог`.
- [ ] Целостность подтверждена через `python scripts/kb_lint.py --path docs`.
