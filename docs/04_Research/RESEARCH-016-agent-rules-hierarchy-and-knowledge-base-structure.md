---
id: RESEARCH-016
title: "Архитектура распределения правил AI-агентов, слоистая конфигурация (Layering) и таксономия базы знаний Docs-as-Code"
status: completed
created: 2026-10-11
updated: 2026-10-11
tags:
  - research
  - agent-rules
  - token-optimization
  - obsidian-graph
  - context-efficiency
  - knowledge-base
  - developer-experience
related_tasks: []
related_adrs:
  - "[[../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001: Zero Dependencies]]"
  - "[[../03_Decisions_ADR/ADR-0003-multi-agent-adapter-strategy|ADR-0003: Стратегия конфигурации AI-агентов]]"
  - "[[../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009: Оптимизация токенов и High-SNR]]"
  - "[[../03_Decisions_ADR/ADR-0013-zero-roundtrip-dispatch-and-hot-invariants-architecture|ADR-0013: Zero Round-Trip Dispatch]]"
---

# 🔬 Исследование: Архитектура распределения правил AI-агентов и таксономия базы знаний

> **Теги:** #research #agent-rules #token-optimization #obsidian-graph #context-efficiency #knowledge-base #developer-experience  
> **Канбан:** [[../02_Tasks/Kanban|Канбан-доска]] | **Дорожная карта:** [[../02_Tasks/Roadmap|Дорожная карта]]  
> **Связанные ADR:** [[../03_Decisions_ADR/ADR-0003-multi-agent-adapter-strategy|ADR-0003]], [[../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]], [[../03_Decisions_ADR/ADR-0013-zero-roundtrip-dispatch-and-hot-invariants-architecture|ADR-0013]]

---

## 1. Проблема, контекст и проверяемые гипотезы

### 1.1. Проблема: Контекстное дублирование, дрифт правил и размытие ролей
В процессе эволюции харнесса `agent-docs-harness` объем правил, инструкций и вспомогательных файлов существенно увеличился. Анализ текущего состояния выявил четыре системные проблемы:

1. **Двойная инжекция контекста (Double Prompt Injection) и дрифт правил (Rule Drift):**
   * Инсталлятор `install.py` генерирует для адаптеров сред разработки (`GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`, `.github/copilot-instructions.md`) практически полный дубликат `_RULES_BODY` (14 дисциплин) и `_3MODES`.
   * В современных IDE (Cursor, Windsurf, Antigravity/Gemini), где агент автоматически считывает как свой rules-файл, так и корневой `AGENTS.md`, агент получает **удвоенный объем одинаковых правил** на каждом шаге диалога.
   * При ручной корректировке разработчиком файла `AGENTS.md` остальные адаптеры не обновляются, порождая расхождение требований (Rule Drift).
2. **Токеновый налог визуальной конфигурации Obsidian Graph в системном промпте:**
   * В `AGENTS.md` (и генераторе `generate_agents_md`) зашита Markdown-таблица цветов Obsidian Graph на 10 строк с RGB-кодами, путями и описаниями цветовой гаммы.
   * Агент LLM не отображает визуальный интерфейс графа — его рендерит клиент Obsidian на основе файла `docs/.obsidian/graph.json`.
   * Знание модели о том, что папка `01_Architecture` окрашена в «фиолетовый» цвет, не несет никакой операционной пользы и является чистым «токеновым шумом» (Low-SNR Context).
3. **Размытие ответственности между `docs-as-code/SKILL.md`, `kb-onboard` и специализированными скиллами:**
   * Скилл `docs-as-code` содержит таблицу роутера из 11 команд. Но в среде Antigravity/Gemini каждый скилл (`kb-plan`, `kb-task`, `kb-implement` и т.д.) уже зарегистрирован автономно со своим триггером и описанием.
   * Наличие скилла `kb-onboard`, выводящего руководство по онбордингу, конкурирует со скиллом `docs-as-code`, создавая дублирование точек входа для ознакомления с системой.
4. **Когнитивная нагрузка на разработчика (Cognitive Overload & Friction):**
   * Пользователь при развертывании харнесса получает 13 шаблонов, 5 корневых документов в `docs/`, файл мастер-спецификации `SPEC.md`, скрипты и CI.
   * Для новичков отсутствие четкого разделения между «системными файлами агента» и «файлами для человека» создает ощущение избыточной бюрократии.

---

### 1.2. Проверяемые гипотезы

* **Гипотеза 1 (Паттерн «Тонких форвардеров» / Thin Forwarder Pattern):**  
  Сокращение специализированных файлов адаптеров (`GEMINI.md`, `CLAUDE.md`, `.cursorrules` и др.) до компактных указателей (20–30 строк) с командами сборки/тестов и явной ссылкой на Single Source of Truth (`AGENTS.md`) исключит дублирование правил, снизит постоянный контекстный налог на 70% и предотвратит Rule Drift.
* **Гипотеза 2 (Изоляция визуальной таксономии Obsidian Graph):**  
  Полное исключение таблицы цветов из `AGENTS.md` и перенос настроек исключительно в конфигурационный файл `docs/.obsidian/graph.json` сэкономит ~150 токенов на каждом запросе агента без потери целостности структуры графа. Агенту достаточно знать только пути к каталогам и целевые теги.
* **Гипотеза 3 (Трехуровневая слоистая иерархия ответственности — L0..L3):**  
  Четкое разграничение ответственности между слоями:
  * **L0: Глобальные правила пользователя/IDE** (язык, критическое мышление, anti-echo).
  * **L1: AGENTS.md (SSOT)** (конституция проекта, 4 режима, барьеры и инварианты).
  * **L2: Тонкие адаптеры вендоров** (`GEMINI.md`, `CLAUDE.md`, `.cursorrules` — только команды CLI и ссылки на SSOT).
  * **L3: Исполняемые скиллы On-Demand** (`.agents/skills/kb-*` — строго пошаговые алгоритмы действий без повторения философии).
* **Гипотеза 4 (Уточнение роли мета-скилла docs-as-code):**  
  Скилл `docs-as-code` должен стать интерактивным навигатором по методологии (MOC для агента), либо быть объединен с `kb-onboard`, чтобы устранить дублирование в реестре скиллов Always-On.

---

## 2. Анализ архитектурных слоев и стресс-тест

### 2.1. Анатомия текущего распределения инструкций

```
┌────────────────────────────────────────────────────────────────────────┐
│ L0: Глобальные правила пользователя (System / IDE Level)                │
│ • Языковой режим (RU диалог, EN код/термины)                           │
│ • Роль ведущего инженерного партнера (Senior Pair Programmer)          │
│ • Протокол Anti-Echo (запрет простыней кода, формат [Link] + Bullets)  │
│ • Не выходить за рамки проекта                                         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ L1: Адаптеры сред (GEMINI.md, CLAUDE.md, .cursorrules, etc.)           │
│ СЕЙЧАС: Дублируют 14 правил + 4 режима + команды тестов (~1 500 слов) │
│ ЦЕЛЬ (Thin Forwarder): 20 строк: стек, команды CLI + ссылка на AGENTS │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ L2: Канонический стандарт проекта — AGENTS.md (SSOT)                   │
│ • 4-этапный жизненный цикл (Modes 0–3)                                 │
│ • Инварианты: Permalinks, Regression-First, Single-Task Barrier        │
│ • Living Spec Invariant & Spec Genesis Protocol                        │
│ • СЕЙЧАС ЛИШНЕЕ: Таблица цветов Obsidian Graph (10 строк с RGB)        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ L3: Исполняемые скиллы On-Demand (.agents/skills/kb-*)                 │
│ • Вызываются строго по требованию (/kb-plan, /kb-task, /kb-implement) │
│ • Содержат: входные условия, пошаговый алгоритм, выходные артефакты   │
│ • Терминальный шаг: Stop & Yield Control                               │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 2.2. Анализ проблемы Obsidian Graph: почему таблица цветов в промпте вредна

В текущей версии `AGENTS.md` содержится блок:
```markdown
### 🎨 Obsidian Graph Color Scheme & Tagging
| Color / Category | Obsidian Path / Query | Tags | Description |
| :--- | :--- | :--- | :--- |
| ⚪ White / Light | `file:00_Index`, `file:Devlog`, `file:SPEC` | — | Entry points & root navigation hubs |
| 🟣 Purple | `path:01_Architecture` | `#arch` | System architecture, contracts & modules |
| 🔵 Blue / Cyan | `path:03_Decisions_ADR` | `#adr` | Architecture Decision Records |
| 🟡 Yellow / Amber | `path:04_Research` | `#research` | Platform research, benchmarks & quirks |
| 🟠 Orange | `path:02_Tasks` | `#task` | Backlog, Roadmap, Plans & Task Specs |
| 🔴 Red | `path:02_Tasks/Bugs` | `#bug` | Defects, bugs, RCA & regression tests |
| 🟢 Green | `path:05_Testing` | `#testing` | Acceptance testing & E2E UX checklists |
```

#### Критический разбор:
1. **Кто потребитель цветовой дифференциации?**  
   Потребитель — **человек**, открывающий Obsidian. Цвета отображаются в окне интерактивного графа благодаря файлу `docs/.obsidian/graph.json`.
2. **Что нужно модели LLM для поддержания графа?**  
   Модели нужны только два фактора:
   * **Куда сохранить файл** (`path:01_Architecture`, `path:02_Tasks/Specs`, `path:03_Decisions_ADR`, `path:04_Research`, `path:05_Testing`).
   * **Какие теги прописать в frontmatter** (`#arch`, `#adr`, `#research`, `#task`, `#bug`, `#testing`).
3. **Последствия нахождения таблицы в `AGENTS.md`:**
   * Модель тратит токены внимания на распознавание названий цветов («White», «Purple», «Cyan»), которые никак не влияют на генерацию кода или Markdown.
   * При желании пользователя изменить цветовую схему в Obsidian (например, настроить кастомную тему), таблица в `AGENTS.md` становится неактуальной, порождая рассинхронизацию.

#### Решение:
Удалить таблицу цветов из `AGENTS.md` и оставить одну лаконичную директиву:
> `Obsidian Graph: visual taxonomy is defined in .obsidian/graph.json. Ensure files are placed in designated paths with canonical tags (#arch, #adr, #research, #task, #bug, #testing).`

---

### 2.3. Паттерн «Тонких форвардеров» (Thin Forwarders) для адаптеров IDE

Сравнение текущей генерации `GEMINI.md` / `CLAUDE.md` / `.cursorrules` с предлагаемой:

#### Текущее состояние (Heavy Duplication):
* Размер: ~140–180 строк.
* Содержит: полный пересказ 14 дисциплин Docs-as-Code, подробные описания всех 4 режимов, Anti-Echo, Single-Task Barrier, Senior Partner манифест.
* Результат: дублирует `AGENTS.md` на 85%.

#### Предлагаемый Thin Forwarder (High-SNR):
```markdown
# GEMINI.md -- Google Antigravity & Gemini CLI Rules

> Project: agent-docs-harness | Stack: Python (FastAPI / Pytest)
> Universal Guidelines: read [[AGENTS.md]] (Single Source of Truth)

## Project Verification Commands
- Build: `python -m py_compile scripts/*.py`
- Test:  `pytest`
- Lint:  `python3 scripts/kb_lint.py --path docs`

## Execution Protocol
1. Follow the 4-Stage Lifecycle and invariants defined in `AGENTS.md`.
2. Prohibited: modifying code during Mode 1 (/kb-plan), Mode 2 (/kb-task), or Mode 2B (/kb-bug).
3. Implementation (Mode 3): strictly via `/kb-implement <TASK-XXX | BUG-XXX>`.
4. Response format: strictly adhere to Anti-Echo (link + 3-5 bullets + next step).
```
*Экономия:* сокращение размера адаптера с ~5 200 байт до ~800 байт (-84% объема).

---

## 3. Сравнительный анализ (Trade-off Matrix)

| Архитектурный подход | Достоинства | Недостатки и риски | Вердикт |
| :--- | :--- | :--- | :--- |
| **Вариант А: Статус-кво (Heavy Adapters + Цвета в AGENTS)** | Все правила видны в любом отдельном файле без переходов | Раздутый контекст (Double Injection), Rule Drift при редактировании, шум цветов в промпте | ❌ Устарел |
| **Вариант Б: Полная ликвидация адаптеров (Только AGENTS.md)** | Минимальное число файлов, абсолютный SSOT | Часть сред (Cursor, Windsurf, Claude Code) игнорируют `AGENTS.md`, если нет их нативного конфигуратора | ❌ Несовместимо с экосистемой |
| **Вариант В: Слоистая архитектура (Thin Forwarders + Clean AGENTS + Decoupled Graph)** | 1) Четкий SSOT в `AGENTS.md`<br>2) Совместимость со всеми IDE<br>3) Экономия 60–80% токенов адаптеров<br>4) Изоляция UI-настроек графа | Требуется обновить логику генерации в `install.py` и сборщике | ✅ **Рекомендовано** |

---

## 4. Отвергнутые варианты

* **Отказ от файла `.obsidian/graph.json` в пользу генерации тегов «на лету»:**  
  *Причина отказа:* Готовый `graph.json` дает пользователю «вау-эффект» сразу при открытии хранилища в Obsidian. Настроенные цветовые группы и физика графа показывают целостность системы без ручной возни с настройками. Конфиг должен оставаться в репозитории.
* **Удаление скилла `docs-as-code` в пользу одной команды `kb-onboard`:**  
  *Причина отказа:* `docs-as-code` служит мета-именем всего харнесса. Однако его содержание должно быть трансформировано из дублирующей таблицы в лаконичный системный индекс-навигатор (Meta-Hub).

---

## 5. Выводы и дорожная карта улучшений

### 5.1. Ключевые архитектурные выводы
1. **Граф Obsidian:** Удалить цветовую Markdown-таблицу из `AGENTS.md` и шаблонов генератора. Оставить только указание на `docs/.obsidian/graph.json` и перечень канонических тегов.
2. **Адаптеры сред (L1):** Перевести генераторы в `install.py` (`generate_gemini_md`, `generate_clinerules`, `generate_claude_md`, `generate_cursorrules`, etc.) на паттерн **Thin Forwarder** (до 30 строк, ссылки на `AGENTS.md`, команды верификации стека).
3. **Канонический `AGENTS.md` (L2):** Очистить от дублирования и деталей интерфейса, закрепив его статус как неизменного ядра правил (SSOT).
4. **Скиллы On-Demand (L3):** Сохранить строгий процедурный формат с терминальным шагом `Stop & Yield Control`.

---

## 6. Зоны уточнения и открытые вопросы для обсуждения

Для окончательного утверждения плана работ выделим ключевые развилки:

1. **Судьба скилла `docs-as-code`:**
   * *Вариант 1:* Оставить его как ультра-компактный навигатор по всем скиллам харнесса.
   * *Вариант 2:* Объединить со скиллом `kb-onboard` (онбординг и навигация в одной точке), убрав лишний скилл из реестра.
2. **Глубина сжатия `AGENTS.md`:**
   * Следует ли оставить в `AGENTS.md` краткие выжимки по каждому из 4 режимов (Modes 0–3) или сократить их до 1 строки с отсылкой к соответствующим скиллам? (Учитывая, что в Antigravity агент может выполнять Hot Invariants без подгрузки скилла — см. [RESEARCH-008](RESEARCH-008-latency-prompt-caching-and-skill-chaining.md)).
3. **Организация 13 шаблонов в `docs/00_Templates/`:**
   * Стоит ли в `Onboarding.md` явно выделить «Базовый набор» (ADR, Task, Plan, Bug) и «Расширенный набор» (Release, Feedback, Research, Test), чтобы снизить порог входа для новых разработчиков?
