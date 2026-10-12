---
id: SPEC
title: "Мастер-спецификация: agent-docs-harness"
status: active
type: specification
created: 2026-09-30
updated: 2026-10-12
tags:
  - spec
  - master
  - agent-docs-harness
  - living-spec
---

# 🚀 Мастер-спецификация: agent-docs-harness

> **Проект:** `agent-docs-harness`  
> **Тип:** Автономный CLI-инструмент и фреймворк дисциплин AI-агентов  
> **Лицензия:** MIT  
> **Связанные документы:** [[docs/00_Index|00_Index]], [[docs/Onboarding|Онбординг]], [[docs/02_Tasks/Kanban|Канбан]], [[docs/02_Tasks/Roadmap|Дорожная карта]].

---

## 1. Концепция и цель проекта

### Проблема
При разработке с AI-агентами (Google Antigravity, Cline, Roo Code, Claude Code, Cursor, Copilot, Windsurf) разработчики неизбежно сталкиваются с четырьмя критическими проблемами:
1. **«Амнезия контекста»:** агент забывает договоренности, архитектурные ограничения и решения, принятые 20 сообщений назад.
2. **«Самовольная ломка кода»:** агент бросается писать код без предварительного согласования архитектуры, ломая существующие контракты и плодя скрытые баги.
3. **«Расползание архитектуры и дрифт (Link Rot & Rotten Spec)»:** проект обрастает устаревшими markdown-файлами с битыми ссылками, а мастер-спецификация отстает от реального кода.
4. **«Шумовое загрязнение контекста (Token Bloat)»:** агент повторяет чужой код в чате (эхо-ответы), расходуя контекстное окно и увеличивая затраты токенов.

### Решение
`agent-docs-harness` — это автономный кроссплатформенный установщик (Zero Dependencies, Python 3 stdlib), который разворачивает в любом проекте профессиональную инфраструктуру **Docs-as-Code**, сквозной **4-этапный жизненный цикл (Double Diamond: Discovery + Delivery)** и High-SNR токеномику:

```bash
curl -sSL https://raw.githubusercontent.com/koudinie101-png/agent-docs-harness/main/install.py | python3
```

---

## 2. Ключевые компоненты харнесса

### 2.1. База знаний Docs-as-Code (`docs/`)
Структурированное хранилище (Obsidian Vault) внутри репозитория:
* `00_Templates/` — 15 эталонных шаблонов (ADR, Research, Task, Micro-Task Fast-Track, Plan, Bug, Test, Onboarding, Index, Kanban, Roadmap, Devlog, Architecture, Release, Feedback) с поддержкой YAML frontmatter.
* `01_Architecture/` — схемы, архитектурные контракты и протоколы.
* `02_Tasks/` — Канбан-доска (`Kanban.md`), Дорожная карта (`Roadmap.md`), планы (`Plans/`), спецификации задач (`Specs/`), баг-трекер (`Bugs/`), релизы (`Releases/`) и буфер входящей обратной связи (`Inbox/` с `.inbox_state.json`).
* `03_Decisions_ADR/` — Архитектурные решения (`ADR-XXXX`) с фиксацией контекста и отклоненных альтернатив.
* `04_Research/` — Исследования платформенных ограничений, памяти и гипотез (`RESEARCH-XXX`).
* `05_Testing/` — Сценарии приемочного тестирования (E2E UX) с интерактивными чек-боксами.
* `Devlog.md` — Хронологический журнал сессий разработки.
* `Onboarding.md` — Единое руководство разработчика и агента.
* `Zero_To_Hero_Guide.md` — Интерактивное руководство для начинающих разработчиков и вайбкодеров.
* `00_Index.md` — Карта заметок (Map of Content).

### 2.2. Цветовая дифференциация Obsidian Graph (`.obsidian/graph.json`)
7 цветовых групп для визуализации архитектурных связей:
* ⚪ **Белый:** Главные хабы (`00_Index`, `Devlog`, `SPEC`, `Onboarding`).
* 🟣 **Фиолетовый:** Архитектура (`01_Architecture`).
* 🔵 **Голубой/Циан:** Решения (`03_Decisions_ADR`, `#adr`).
* 🟡 **Желтый/Янтарный:** Исследования платформы (`04_Research`, `#research`).
* 🟠 **Оранжевый:** Задачи, планы и roadmap (`02_Tasks`, `#task`).
* 🔴 **Красный:** Баги и дефекты (`02_Tasks/Bugs`, `#bug`).
* 🟢 **Зеленый:** Приемочное тестирование (`05_Testing`, `#testing`).

### 2.3. Автономные утилиты скриптов (`scripts/`)
* **`scripts/kb_lint.py`:**
  * Zero dependencies (только Python 3 stdlib: `pathlib`, `re`, `argparse`).
  * Валидация всех вики-ссылок `[[...]]`, регистра имен и структуры путей.
  * Проверка наличия и валидности YAML frontmatter в задачах, багах, планах, ADR и элементах обратной связи (`FB-XXX`).
  * Silent-on-Success CLI и кроссплатформенный UTF-8 вывод.
  * Эвристический контроль дрифта спецификации (`check_spec_drift`) с неблокирующими предупреждениями при $\ge 2$ завершенных фазах.
  * Семантический аудит журнала разработки (`check_devlog_semantic_guard`) с неблокирующими предупреждениями при обнаружении триггеров авто-чейнинга без защитного маркера ожидания пользователя.
  * Семантический контроль структуры фаз (`check_phase_consistency`): сопоставление номера фазы в frontmatter (`phase: N`) с папкой размещения (`Specs/NN_<Slug>/`) и тегами (`phaseN`).
* **`scripts/kb_release.py`:**
  * Zero dependencies (хэширование SHA-256, парсинг артефактов).
  * High-SNR Dual-Export: экспорт `RELEASE-vX.Y.Z.md` во внутреннюю базу знаний с фазово-изолированными решениями ADR (`is_adr_for_phase`) и публичный `dist/RELEASE_NOTES.md` без внутренних технических протоколов ADR, с очищенными от викиссылок Markdown-текстами для потребителей и GitHub Releases.
  * Релизный таргетинг дефектов (`collect_fixed_bugs`): включение в чейнджлог только устраненных багов целевой версии (`fixed_in` или `target_release`).
  * Префлайт-контроль релиз-блокеров (`check_release_blockers`): аварийная остановка сборки релиза (Exit code 1) при наличии открытых багов с флагом `release_blocker: true`.
  * Адаптивный блок установки (Adaptive Quick Install): контекстная генерация инструкций в `dist/RELEASE_NOTES.md` (Docs-as-Code инсталлятор только для репозитория самого harness-а, скачивание скомпилированных артефактов `dist/` для сторонних проектов, либо кастомные команды через аргумент `--quick-install`).
* **`scripts/kb_ingest.py`:**
  * Zero dependencies (только стандартные модули `urllib`, `email`, `hashlib`, `pathlib`, `argparse`, `subprocess`).
  * Инжест внешних сигналов обратной связи из трех каналов: GitHub Issues API, Email/EML/Mbox и ручного буфера вставки (Raw Clipboard Paste).
  * Zero-deps автоопределение GitHub репозитория (`detect_github_repo`) из `git config --get remote.origin.url` (HTTPS, SSH, token auth) с приоритетом переменной `GITHUB_REPOSITORY`.
  * Инвариант прозрачности каналов (Channel Transparency Invariant): запрет немых пропусков (предупреждения о пропущенных источниках, подсказка по лимитам API 60 req/h -> 5000 req/h).
  * Гибкие фильтры инжеста (`--label <NAME>`, `--all-open`) и диагностический дашборд статуса источников (`--status`).
  * Автоматическая дедупликация сигналов на основе персистентного состояния `docs/02_Tasks/Inbox/.inbox_state.json`.
  * Нормализация сигналов в компактные атомарные артефакты `FB-XXX-<slug>.md` по каноническому шаблону `TEMPLATE_FEEDBACK.md`.

### 2.4. Дисциплина 4 этапов (Modes 0–3) и конфигурация агентов
* Единый канонический файл правил **`AGENTS.md`** и адаптеры (`GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`, `.github/copilot-instructions.md`).
* **Структурированные режимы:**
  * **Режим 0: Исследование и валидация гипотез (`/kb-research`)** — стресс-тестирование рисков, матрица компромиссов, двухпутевая воронка регистрации (Icebox vs отказные ADR).
  * **Режим 1: Планирование (Planning / RFC, `/kb-plan`)** — только концептуальное обсуждение, критика, архитектурный план. Запрет на редактирование кода!
  * **Режим 2: Формирование ТЗ (Task Spec, `/kb-task`)** — точные контракты `[NEW]`/`[MODIFY]`, сигнатуры, DoD, план верификации. Запрет на редактирование кода!
  * **Режим 2B: Заведение и триаж дефектов (`/kb-bug`)** — изолированная фиксация дефекта, RCA, назначение `target_release`, `target_phase`, `release_blocker` и падающего теста `regression_test`. Запрет на правку кода! Терминальный шаг Stop & Yield.
  * **Режим 2C: Триаж и маршрутизация обратной связи (`/kb-triage`)** — изоляция внешних сигналов в буфере `docs/02_Tasks/Inbox/`, двухэтапный скрининг, интерактивная маршрутизация в `/kb-bug`, Дорожную карту (Icebox) или FAQ. Запрет на правку кода! Терминальный шаг Stop & Yield.
  * **Режим 3: Реализация (Implementation, `/kb-implement` & `/kb-complete`)** — написание кода задач (`TASK-XXX`) строго по ТЗ, исправление багов (`BUG-XXX`) строго по циклу TDD (**RED** failing test -> **GREEN** fix -> **REFACTOR** full test suite), Living Spec Sync, автоматическое закрытие карточки в Канбане, Дорожной карте и Devlog.
* **Протокол Living Spec (Anti-Drift):** обязательная синхронизация `SPEC.md` и `README.md` при изменении публичных контрактов и префлайт-проверка перед релизом.
* **Spec Genesis Protocol & Zero-State Guardrails (Anti-Hallucination):** трехстадийная модель зрелости спецификации (`Missing` -> `Discovery` -> `Active`). Категорический запрет на директивное выдумывание требований агентом в Zero-State; кристаллизация через диалог, Режим 0 (`/kb-research`) и `ADR-0001`. Префлайт Soft Nudge в `/kb-plan` и `/kb-task`.
* **Human Guardrails Protocol («Направляй, а не блокируй»):** запрет на грубые роботизированные ошибки в read-only режимах; вежливое партнерское объяснение сути этапа, 1–2 направляющих вопроса и подсказка точной команды для продолжения.
* **Fast-Track Protocol (Micro-Task Bypass):** обход этапа планирования для микро-задач ($\le 30$ LOC, $\le 2$ файлов, без рисков) через `/kb-task --fast <описание>` с использованием компактного шаблона `TEMPLATE_TASK_MICRO.md`.
* **Anti-Echo Protocol:** запрет на вывод полных листингов файлов в чат — только кликабельные ссылки `[File](file:///...)` и 3–5 пунктов резюме.
* **Zero Round-Trip Dispatch & Hot Invariants Protocol:** прямая авторизация агентов на исполнение стандартных жизненных циклов (Режимы 0, 1, 2, 2B, 2C, 3) из Always-On префикса без предварительного раунда чтения `SKILL.md`; параллельное чтение контекста (Pipelined Co-fetching) в первом же раунде вызова инструментов.
* **Single-Task Execution Barrier (Stop & Yield):** команда `/kb-implement <TASK-XXX | BUG-XXX>` авторизует работу строго над одной задачей или багом; после завершения коммита агент обязан прекратить вызовы инструментов (Tool Calls) и передать управление разработчику, предотвращая неконтролируемый авто-чейнинг задач при сжатии контекста.
* **Feedback Ingestion & Triage Buffer Invariant:** внешние сигналы никогда не попадают в код или ТЗ в обход буфера `Inbox/`; триаж выполняется исключительно через `/kb-triage` с соблюдением принципа пермалинков (in-place обновление frontmatter `FB-XXX`).
* **Permalinks Principle:** файлы ТЗ, багов и обратной связи не перемещаются в архивы при закрытии.
* **Regression-First:** баги закрываются только после создания падающего воспроизводящего автотеста и успешного прохождения TDD-цикла через `/kb-implement BUG-XXX`.

---

## 3. Архитектура инсталлятора `install.py`

### 3.1. Требования к рантайму
* Только стандартная библиотека Python 3 (Python 3.8+).
* Никаких внешних пакетов (`no requests`, `no pyyaml`, `no rich`).
* Полная автономность (Self-Contained) — скрипт содержит упакованные base64-ресурсы (шаблоны, скиллы, утилиты, issue templates).
* Кроссплатформенная работа (macOS, Linux, Windows).

### 3.2. Режимы запуска и флаги
1. **Интерактивный мастер (Interactive Wizard):**
   * Определение имени проекта (дефолт — имя текущей папки).
   * Выбор технологического стека (Swift/iOS, Web/TS, Python, .NET, Generic, Undecided / Idea-First).
   * Выбор целевого агента / редактора (All, Cline, Claude Code, Cursor, Copilot, Antigravity/Gemini, Generic).
   * Выбор языка документации (`ru` / `en`).
   * Выбор стратегии Git (GitHub, Local-Only, Skip).
2. **Неинтерактивный CLI (Flags / Automation):**
   * `--name <str>` — название проекта.
   * `--stack {swift,ts,python,dotnet,generic,undecided}` — предустановка стека.
   * `--idea "<текст>"` — вербальное описание идеи для старта с чистого листа (пресет `undecided`).
   * `--agent {all,cline,claude,cursor,copilot,generic}` — конфигурации агентов.
   * `--lang {ru,en}` — язык документации.
   * `--git {github,local,none}` — стратегия контроля версий.
   * `--update` — бережное обновление шаблонов, скиллов, утилит и создание буфера Inbox без перезаписи пользовательских заметок.
   * `--report` — генерация анонимизированного диагностического Markdown-отчета окружения (ОС, Python, Git, статус kb_lint, найденные конфиги агентов).
   * `-y`, `--yes`, `--non-interactive` — авто-подтверждение дефолтов.
   * `--target-dir <path>` — путь назначения (по умолчанию `.`).

---

## 4. Дорожная карта и эволюция проекта

* **Фаза 1: Автономный инсталлятор (MVP)** — `install.py`, шаблоны, CLI-мастер, E2E тесты.
* **Фаза 2: Расширения и экосистема** — 11 скиллов `.agents/skills/`, мультиязычность, канонические правила агентов.
* **Фаза 3: Зрелость инсталлятора** — Brownfield Adoption, Clean Slate, механизм обновления (`--update`), GitHub Actions CI.
* **Фаза 4: Релиз-менеджмент и автоматизация** — скилл `/kb-release`, `scripts/kb_release.py`, SHA-256, пайплайн релизов.
* **Фаза 5: Оптимизация токенов и High-SNR архитектура** — Anti-Echo протокол, Silent-on-Success CLI, сжатие шаблонов и скиллов (-60% контекста).
* **Фаза 6: Интеграция этапа исследования (Режим 0: Discovery)** — Double Diamond цикл, воронка `/kb-research`, префлайты `/kb-plan`.
* **Фаза 7: Стандарт оформления публичных релизов на GitHub** — Dual-Export в `kb_release.py`, очистка викиссылок, автоматизация GitHub Releases.
* **Фаза 8: Greenfield-инициализация от идеи (Idea-First) и Living Spec** — пресет `undecided`, флаг `--idea`, протокол Living Spec и эвристический аудит дрифта в `kb_lint.py`.
* **Фаза 9: Барьер единичной задачи и протокол гарантированной остановки (Single-Task Execution Barrier & Stop-on-Complete)** — трехуровневая защита от Eager Task Chaining: норматив в `AGENTS.md`, терминальный шаг `Stop & Yield` в скиллах, семантический маркер в `Devlog.md` и аудит в `kb_lint.py`.
* **Фаза 10: Рождение Мастер-Спецификации (Spec Genesis) и High-SNR релизные заметки** — протокол кристаллизации спецификации из идеи (`Missing` -> `Discovery` -> `Active`), префлайт-чеки в `kb-init`/`kb-plan`/`kb-task`, исключение кумулятивных ADR из публичных релизов (`dist/RELEASE_NOTES.md`) и фазовая изоляция ADR в `scripts/kb_release.py`.
* **Фаза 11: Жизненный цикл дефектов, прозрачный триаж и релизный таргетинг (Bug Lifecycle & Release Targeting)** — изоляция триажа дефектов (Режим 2B `kb-bug` со Stop & Yield) от их устранения, унификация исполнения дефектов в Режиме 3 (`kb-implement BUG-XXX` по циклу TDD), строгий релизный контракт дефектов (`target_release`, `target_phase`, `release_blocker`, `fixed_in`) и префлайт-фильтрация блокеров в `scripts/kb_release.py`.
* **Фаза 12: Инжест внешней обратной связи, буфер триажа и оффлайн-диагностика (Feedback Ingestion, Triage Buffer & Diagnostic Diagnostics)** — канонический шаблон `TEMPLATE_FEEDBACK.md`, утилита инжеста `scripts/kb_ingest.py` (GitHub/Email/Paste с дедупликацией), буфер `docs/02_Tasks/Inbox/` с состоянием `.inbox_state.json`, Режим 2C (`/kb-triage` со Stop & Yield), формы GitHub Issue Forms (`bug_report.yml`, `feature_request.yml`), диагностический отчет `install.py --report` и E2E верификация.
* **Фаза 13: Слоистая архитектура правил (Thin Forwarders), декуплинг графа Obsidian и таксономия базы знаний** — переход адаптеров IDE на паттерн Thin Forwarders ($\le 25$ строк, -80% контекста) со ссылкой на `AGENTS.md` как SSOT, декуплинг таблицы цветов Obsidian Graph в `.obsidian/graph.json` (-150 токенов на шаг), консолидация навигации и онбординга (`docs-as-code` $\to$ `kb-onboard`, 12 скиллов), двухуровневая таксономия шаблонов (Core Essentials [4] vs Advanced Governance [10]), сборка автономного инсталлятора `dist/install.py` и сквозные E2E тесты.
* **Фаза 14: Продуктовый DX, протокол Fast-Track и адаптация для вайбкодеров (Agile Docs-as-Code & Chat-First DX)** — протокол Fast-Track для микро-задач (пропуск Режима 1, компактная Micro-Spec `TEMPLATE_TASK_MICRO.md`, экономия 70% токенов), принцип «Направляй, а не блокируй» (Human Guardrails) в правилах агентов, Chat-First Bootstrapping в README (запуск без терминала), практическое руководство `Zero_To_Hero_Guide.md` («Вайбкодинг со страховкой»), понятные чейнджлоги в `kb_release.py` и аудит лимитов в `kb_lint.py`.
* **Фаза 15: Устранение задержек отклика и прозрачность каналов (Response Latency Elimination & Channel Transparency)** — архитектура Zero Round-Trip Dispatch (Hot Invariants в Always-On префиксе без предварительного чтения `SKILL.md`), User-Centric Ingestion & Channel Transparency в `scripts/kb_ingest.py` (Zero-Deps автодетект репозитория из `git remote origin`, флаг `--status`, гибкая фильтрация `--label` / `--all-open`, запрет немых пропусков), актуализация скилла `/kb-triage`, семантический контроль фаз в `scripts/kb_lint.py` (`check_phase_consistency`), монолитный дистрибутив `install.py` и сквозные E2E тесты.

