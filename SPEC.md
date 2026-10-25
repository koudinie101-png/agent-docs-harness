---
id: SPEC
title: "Мастер-спецификация: agent-docs-harness"
status: active
type: specification
created: 2026-09-30
updated: 2026-10-25
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
* `00_Templates/` — 16 эталонных шаблонов (ADR, Research, Task, Micro-Task Fast-Track, Plan, Bug, Test, Onboarding, Index, Kanban, Roadmap, Devlog, Architecture, Release, Feedback, Incident) с поддержкой YAML frontmatter.
* `01_Architecture/` — схемы, архитектурные контракты и протоколы.
* `02_Tasks/` — Канбан-доска (`Kanban.md`), Дорожная карта (`Roadmap.md`), Реестр техдолга (`TechDebt.md`), планы (`Plans/`), спецификации задач (`Specs/`), баг-трекер (`Bugs/`), релизы (`Releases/`) и буфер входящей обратной связи (`Inbox/` с `.inbox_state.json`).
* `03_Decisions_ADR/` — Архитектурные решения (`ADR-XXXX`) с фиксацией контекста и отклоненных альтернатив.
* `04_Research/` — Исследования платформенных ограничений, памяти и гипотез (`RESEARCH-XXX`).
* `05_Testing/` — Сценарии приемочного тестирования (E2E UX) с интерактивными чек-боксами и чеклистом GUI («UI не лжёт»).
* `06_Memory/` — Процедурная память агента: High-SNR компактный индекс систематических ошибок `patterns.md` ($\le 15$ активных записей, лимит ~350 токенов) и архив детальных отчетов об инцидентах `Incidents/` (`INC-XXX`).
* `assets/` — Хранилище визуальных ассетов (`mockups/`, `screenshots/<target>/`, `diagrams/`, `design/UI_Design_System.md`).
* `Devlog.md` — Хронологический журнал сессий разработки.
* `Onboarding.md` — Единое руководство разработчика и агента.
* `Zero_To_Hero_Guide.md` — Интерактивное руководство для начинающих разработчиков и вайбкодеров.
* `00_Index.md` — Карта заметок (Map of Content).

### 2.2. Настройки Obsidian и граф связей (`.obsidian/`)
* **Цветовая дифференциация графа (`.obsidian/graph.json`):** 7 цветовых групп для визуализации архитектурных связей (Белый — хабы, Фиолетовый — архитектура, Циан — ADR, Янтарный — исследования, Оранжевый — задачи, Красный — баги, Зеленый — тестирование).
* **Obsidian DX и вставка ассетов (`.obsidian/app.json`):** автоматическая конфигурация `attachmentFolderPath: "assets/screenshots"`, позволяющая пользователям вставлять скриншоты по Ctrl+V прямо в репозиторий без ручного перекладывания файлов.

### 2.3. Автономные утилиты скриптов (`scripts/`)
* **`scripts/kb_lint.py`:**
  * Zero dependencies (только Python 3 stdlib: `pathlib`, `re`, `argparse`).
  * Валидация всех вики-ссылок `[[...]]`, регистра имен и структуры путей.
  * Аудит целостности реестра техдолга (`check_tech_debt_integrity`): проверка наличия `docs/02_Tasks/TechDebt.md`, формата идентификаторов `DEBT-XXX`, валидности викиссылок в строках открытого и закрытого долга и семантический кросс-чек планов/спецификаций с тегом `#techdebt` (неблокирующее `WARN:` при отсутствии привязки к `DEBT-XXX` или пустом реестре).
  * Неблокирующий контроль отложенных доработок (`check_untracked_todos`): аудит комментариев `TODO`/`FIXME` на обязательное наличие привязки к элементу бэклога `// ROADMAP-<ID>` или `// DEBT-XXX`.
  * Индексация и валидация медиа-ассетов (изображения `![[...]]`, markdown `![...](...)`): поддержка параметров размера/отображения (`![[img.png|300]]`), проверка физического существования файлов и аудит весового лимита ($\le 2\text{ MB}$).
  * Механический контроль топологии визуальных ассетов (`check_asset_layout`): неблокирующий аудит корневых каталогов `docs/assets/` (`VALID_ASSET_ROOTS = {"mockups", "screenshots", "diagrams", "design"}`), отсутствия неразмеченных файлов в корне и контроль пространств имен `docs/assets/mockups/<target>/TASK-XXX/` и `docs/assets/mockups/flows/TASK-XXX/` с запретом невалидного fallback'а по `file_map` для относительных медиа-путей.
  * Проверка наличия и валидности YAML frontmatter в задачах, багах, планах, ADR, элементах обратной связи (`FB-XXX`) и отчетах об инцидентах (`INC-XXX`).
  * Механический Tier 1 контроль лимита процедурной памяти (`check_memory_limits`): строгая проверка лимита активных записей ($\le 15$) в `docs/06_Memory/patterns.md` с блокировкой сборки (Exit code 1).
  * Контроль целостности процедурной памяти (`check_memory_consistency`): ссылки `patterns.md` → `Incidents/`, совпадение `id` с именем файла, наличие `target_pattern` в индексе (неблокирующие `WARN`).
  * Неблокирующий контроль доказательной базы плана (`check_research_basis`): `research_basis: none` без `basis_note` → `WARN:` (Exit code 0); при отсутствии поля предупреждение не выдаётся.
  * Неблокирующий контроль символьного скоупа задач (`check_symbolic_scope`): для активных задач (`planned`/`in-progress`) кодовые `[MODIFY]`/`[NEW]` без вложенного символа и маркеры `:L10-L20` дают `WARN:` (Exit code 0); `done`-спеки и fast-track не аудируются (ADR-0029).
  * Silent-on-Success CLI и кроссплатформенный UTF-8 вывод.
  * Эвристический контроль дрифта спецификации (`check_spec_drift`) с неблокирующими предупреждениями при $\ge 2$ завершенных фазах.
  * Семантический аудит журнала разработки (`check_devlog_semantic_guard`) с неблокирующими предупреждениями при обнаружении триггеров авто-чейнинга без защитного маркера ожидания пользователя.
  * Семантический контроль структуры фаз (`check_phase_consistency`): сопоставление номера фазы в frontmatter (`phase: N`) с папкой размещения (`Specs/NN_<Slug>/`) и тегами (`phaseN`).
  * Единая модель находки (`Finding`: `rule_id`, `severity`, `file`, `message`) и реестр стабильных правил `KB-001…KB-015` (`KB-010` зарезервирован под `depends_on` и не эмитится) — SSOT для машинно-читаемых отчётов и будущих ignore-политик (ADR-0032).
  * CLI-контракт диагностики: `--format {text,json,sarif}` (text — байт-в-байт прежний человекочитаемый вывод), `--version` (версия набора правил, `kb_lint 1`) и неизменные exit-коды `0/1` во всех форматах; SARIF 2.1.0 без `region.startLine` и без метаданных происхождения проекта (`DEBT-004`).
* **`scripts/kb_release.py`:**
  * Zero dependencies (хэширование SHA-256, парсинг артефактов).
  * High-SNR Dual-Export: экспорт `RELEASE-vX.Y.Z.md` во внутреннюю базу знаний с фазово-изолированными решениями ADR (`is_adr_for_phase`) и публичный `dist/RELEASE_NOTES.md` без внутренних технических протоколов ADR, с очищенными от викиссылок Markdown-текстами для потребителей и GitHub Releases.
  * Конвертер медиа-вставок в чистый Markdown: преобразование синтаксиса `![[image.png]]` в стандартные Markdown-изображения `![image.png](...)` в публичных заметках `dist/RELEASE_NOTES.md`.
  * Релизный таргетинг дефектов (`collect_fixed_bugs`): включение в чейнджлог только устраненных багов целевой версии (`fixed_in` или `target_release`).
  * Префлайт-контроль релиз-блокеров (`check_release_blockers`): аварийная остановка сборки релиза (Exit code 1) при наличии открытых багов с флагом `release_blocker: true`.
  * Адаптивный блок установки (Adaptive Quick Install): контекстная генерация инструкций в `dist/RELEASE_NOTES.md` (Docs-as-Code инсталлятор только для репозитория самого harness-а, скачивание скомпилированных артефактов `dist/` для сторонних проектов, либо кастомные команды через аргумент `--quick-install`).
  * Ссылки на полный диф изменений (Full Changelog Compare URL): автоопределение предшествующего релиза через Git-теги или файлы `docs/02_Tasks/Releases/` с формированием ссылки сравнения (`compare/{prev_tag}...{tag}`) без циклического зацикливания на саму себя, с поддержкой ручного переопределения `--prev-tag`.
  * Протокол No Silent Fallback и детекция окружения публикации: явные предупреждения с инструкциями установки (`winget install GitHub.cli` / `brew install gh`) и поддержка REST API токена (`GITHUB_TOKEN`), флаг принудительной валидации `--require-github` и управление режимом через `--mode {auto,github,local}`.
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
  * **Режим 0: Исследование и валидация гипотез (`/kb-research`)** — стресс-тестирование рисков, матрица компромиссов, двухпутевая воронка регистрации (Icebox vs отказные ADR), Prior-Art Gate.
  * **Режим 1: Планирование (Planning / RFC, `/kb-plan`)** — только концептуальное обсуждение, критика, архитектурный план с обязательным барьером Prior-Art Gate, Evidence Status (`🔬`/`🧪`/`⏸`) с неблокирующим Evidence Nudge (A/B/C) при промоушене из Icebox и фиксация `research_basis`/`basis_note` в `PLAN-XXX`. Запрет на редактирование кода!
  * **Режим 2: Формирование ТЗ (Task Spec, `/kb-task`)** — точные контракты `[NEW]`/`[MODIFY]`/`[DELETE]` с иерархическим символьным скоупом (`Class.method()`, без номеров строк, ADR-0029), сигнатуры, DoD, план верификации с протоколом серийных замеров Benchmark Persistence. Запрет на редактирование кода!
  * **Режим 2B: Заведение и триаж дефектов (`/kb-bug`)** — изолированная фиксация дефекта, RCA, назначение `target_release`, `target_phase`, `release_blocker` и падающего теста `regression_test`. Запрет на правку кода! Терминальный шаг Stop & Yield.
  * **Режим 2C: Триаж и маршрутизация обратной связи (`/kb-triage`)** — изоляция внешних сигналов в буфере `docs/02_Tasks/Inbox/`, двухэтапный скрининг, интерактивная маршрутизация в `/kb-bug`, Дорожную карту (Icebox) или FAQ. Запрет на правку кода! Терминальный шаг Stop & Yield.
  * **Режим 3: Реализация (Implementation, `/kb-implement` & `/kb-complete`)** — написание кода задач (`TASK-XXX`) строго по ТЗ с локализацией по именам символов (не по номерам строк), исправление багов (`BUG-XXX`) строго по циклу TDD (**RED** failing test -> **GREEN** fix -> **REFACTOR** full test suite), Living Spec Sync, автоматическое закрытие карточки в Канбане, Дорожной карте и Devlog; state-aware next step: `/kb-implement TASK-YYY` только при существующей спеке, иначе `/kb-task TASK-YYY`.
* **Tech Debt Governance & End-to-End Lifecycle (P1/P2 vs P3):** строгий триаж находок ревью на критические дефекты (P1/P2 — правятся немедленно) и отложенный долг (P3 — запрещено исправлять на лету во избежание срыва скоупа). `docs/02_Tasks/TechDebt.md` — обязательный первичный реестр (SSOT) для любого долга `P3` (находки ревью и плановый рефакторинг `#techdebt` в Режимах 1–2 и триаже 2C); при планировании/постановке задачи запись `DEBT-XXX` создаётся в `Active P3 Debt`, при завершении переносится в `Resolved Debt` со ссылкой на `TASK-XXX`.
* **Prior-Art Gate Invariant:** обязательный аудит существующего кода и стандартных библиотек платформы перед созданием новых модулей во избежание «изобретения велосипедов».
* **Traceable Backlog Tags (`// ROADMAP-<ID>` и `// DEBT-XXX`):** запрет висячих комментариев `TODO`/`FIXME` без явной привязки к бэклогу или реестру техдолга.
* **Benchmark Persistence («Замер = артефакт»):** валидация производительности сериями $\ge 3$ прогонов с отсечением холодного старта.
* **Чеклист приемочного тестирования GUI («UI не лжёт»):** интерактивная верификация матрицы 4 состояний, кликабельности, верстки без обрезания и незаблокированности UI-потока.
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
* **The 4-State UI & Visual Verification Invariant:** обязательное проектирование матрицы 4 состояний (`Empty`, `Loading`, `Error`, `Populated`) в планах (`TEMPLATE_PLAN.md`) и спецификациях (`TEMPLATE_TASK.md`) для графических (GUI) и терминальных (TUI) интерфейсов; фиксация макетов в изолированных пространствах имен задач `docs/assets/mockups/<target>/TASK-XXX/` (`asis.svg`, `tobe.svg`, `<surface>_tobe.svg`) и сквозных сценариев `docs/assets/mockups/flows/TASK-XXX/` (ADR-0027); подтверждение завершения задач постоянным скриншотом в `docs/assets/screenshots/<target>/TASK-XXX.png` ($\le 2\text{ MB}$) или ASCII/SVG превью в Headless окружении; механический контроль топологии `check_asset_layout()` и строгая резолюция относительных путей медиа-ссылок в `scripts/kb_lint.py`; изоляция временных тестовых снапшотов в `tmp/ui_snapshots/` с запретом коммита в Git.

---

### 2.5. Компилятор правил агента (`rules/AGENTS_CORE.md`)
Единый рукописный источник правил поведения агента ([ADR-0030](docs/03_Decisions_ADR/ADR-0030-single-source-rule-compiler.md)): три документа корпуса (`client-agents`, `adapters`, `harness-agents`) с семантическими маркерами `RULE` (устойчивые ключи `UPPER-KEBAB-CASE`) и плейсхолдерами стека (`{{project}}`, `{{build_cmd}}`, `{{lang_instruction}}` и др.).
* Рендерер `install.py` (`_load_rules_corpus`, `_render_rules_document`) собирает `AGENTS.md` клиентского проекта и 6 тонких адаптеров; корпус упаковывается в `EMBEDDED_ASSETS` и **не** разворачивается в `docs/` целевого проекта.
* Источник разрешается каскадом: локальный `rules/AGENTS_CORE.md` (разработка) → бандл (развёрнутый дистрибутив) → `RuntimeError` с actionable-подсказкой; тихий fallback отсутствует.
* Контроль дрейфа: golden-фикстуры (`tests/test_rules_golden.py`), генерация корневого `AGENTS.md` через `scripts/gen_rules.py --check` (TASK-086) и Tier 1 тесты структуры (TASK-087).

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
   * `--update` — бережное обновление шаблонов, скиллов, утилит, реестра техдолга и создание буфера Inbox без перезаписи пользовательских заметок.
   * `--report` — генерация анонимизированного диагностического Markdown-отчета окружения (ОС, Python, Git, статус kb_lint, найденные конфиги агентов).
   * `--ui {auto,none,web,mobile,desktop,tui,<comma-separated>}` — выбор UI-платформ и инициализация каталогов визуальных ассетов (`docs/assets/`).
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
* **Фаза 16: Самообучающийся харнесс и память дефектов (Self-Improving Harness & Defect Memory)** — ликвидация амнезии процедурных ошибок агента через двухуровневый контур памяти (архив инцидентов `docs/06_Memory/Incidents/` и High-SNR агрегированный индекс `patterns.md` с лимитом $\le 15$ записей), контрольные точки Memory-First в Режиме 3 (`kb-implement`) и `/kb-complete`, протокол двухосевого промоушена, матрица слоев надежности Quality Gates (Tier 1–3), аудит лимитов в `scripts/kb_lint.py`, бандлинг инсталлятора `install.py` и сквозные E2E тесты.
* **Фаза 17: Стабилизация ядра, синхронизация SSOT и защита краевых сценариев (Core Hardening & SSOT Sync)** — устранение рассинхронизации между корневым `AGENTS.md` и генераторами `install.py`, исправление краевых дефектов линтера/инжестора/релизера (`BUG-005`–`BUG-009`), обеспечение 100% совместимости с Python 3.8+, защита анонимизатора и синхронизация всех 16 шаблонов.
* **Фаза 18: Контур UI/UX, управление визуальными ассетами и гетерогенные multi-target системы (Heterogeneous UI/UX & Visual Asset Harness)** — изолированное хранилище ассетов с Obsidian DX (`docs/assets/`, `docs/.obsidian/app.json`), композитный CLI-флаг `--ui <targets>`, механический контроль медиа-ассетов в `scripts/kb_lint.py` и `scripts/kb_release.py` (лимит $\le 2\text{ MB}$, очистка размеров, конвертация в Markdown), норматив матрицы 4 состояний (The 4-State UI Matrix) и визуальный DoD в `AGENTS.md`, шаблонах и руководствах.
* **Фаза 19: Инженерные барьеры качества и контроль техдолга (Engineering Gates & Tech Debt Governance)** — реестр технического долга `docs/02_Tasks/TechDebt.md` с разделением на $P1/P2$ (исправляются немедленно) vs $P3$ (фиксируются без срыва скоупа текущей задачи), Prior-Art Gate в планировании (`TEMPLATE_PLAN.md`, `TEMPLATE_RESEARCH.md`) для исключения дублирования готовых решений, сквозная трассировка отложенных доработок `// ROADMAP-<ID>` с запретом висячих `TODO`/`FIXME`, фиксация серийных замеров Benchmark Persistence («Замер = артефакт» на $\ge 3$ прогонах), чеклист приемочного тестирования GUI («UI не лжёт») в `TEMPLATE_TEST.md` и механический аудит в `scripts/kb_lint.py`.
* **Фаза 20: Стандартизация хранилища визуальных ассетов, пространства имен TASK-XXX и валидация топологии (Asset Storage Hardening & Layout Linting)** — ликвидация «дрифта редизайнов» (To-Be Drift) за счет введения пространств имен задач `docs/assets/mockups/<target>/TASK-XXX/` и каталога сквозных кросс-девайсных сценариев `docs/assets/mockups/flows/TASK-XXX/`, закрепление жизненного цикла макетов `As-Is / To-Be` (`asis.svg`, `tobe.svg`, `<surface>_tobe.svg`), устранение дефекта ложноположительного разрешения путей одноименных медиафайлов в `scripts/kb_lint.py`, внедрение механического контроля топологии `check_asset_layout()`, обновление `UI_Design_System.md` и сборка монолитного установщика `install.py`.
* **Фаза 21: Сквозной жизненный цикл технического долга и кросс-режимная синхронизация (Tech Debt Lifecycle & Cross-Mode Sync)** — замкнутый цикл `DEBT-XXX` (`Active P3 Debt` → Plan/Task → `Resolved Debt`) во всех режимах (`/kb-plan`, `/kb-task`, `/kb-triage`, `/kb-complete`), разрешение кодовых тегов `// DEBT-XXX` наравне с `// ROADMAP-<ID>`, унификация канонического тега `#techdebt` (правила агентов и цветовая группа `.obsidian/graph.json`), семантический кросс-чек `TechDebt.md` с планами/задачами `#techdebt` в `scripts/kb_lint.py` и пересборка монолитного установщика `install.py` с E2E-тестами.



