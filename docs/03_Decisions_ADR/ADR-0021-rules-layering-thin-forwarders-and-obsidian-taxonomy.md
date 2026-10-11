---
id: ADR-0021
title: "Архитектура распределения правил (Thin Forwarders), декуплинг графа Obsidian и консолидация онбординга"
status: accepted
date: 2026-10-11
superseded_by: ""
tags:
  - adr
  - architecture
  - agent-rules
  - token-optimization
  - obsidian-graph
  - skills
related_research:
  - "[[../04_Research/RESEARCH-016-agent-rules-hierarchy-and-knowledge-base-structure|RESEARCH-016]]"
---

# ADR-0021: Архитектура распределения правил (Thin Forwarders), декуплинг графа Obsidian и консолидация онбординга

> **Статус:** Принято | **Дата:** 2026-10-11  
> **Обоснование и замеры:** [[../04_Research/RESEARCH-016-agent-rules-hierarchy-and-knowledge-base-structure|RESEARCH-016: Архитектура распределения правил AI-агентов]]  
> **Связанные ADR:** [[ADR-0003-multi-agent-adapter-strategy|ADR-0003: Мультиагентные адаптеры]], [[ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009: Оптимизация токенов и High-SNR]], [[ADR-0013-zero-roundtrip-dispatch-and-hot-invariants-architecture|ADR-0013: Zero Round-Trip Dispatch]]

---

## 1. Контекст и проблема

В ходе аудита [RESEARCH-016](RESEARCH-016-agent-rules-hierarchy-and-knowledge-base-structure.md) выявлены структурные неэффективности в текущей организации правил и базе знаний:
1. **Двойная инжекция контекста (Double Prompt Injection) и Rule Drift:** Адаптеры сред разработки (`GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`) дублируют 14 дисциплин и 4 режима из `AGENTS.md`. В IDE, считывающих как системный файл, так и `AGENTS.md`, контекст расходуется вдвое. При изменении `AGENTS.md` адаптеры рассинхронизируются.
2. **Токеновый налог визуальной конфигурации Obsidian:** В `AGENTS.md` присутствует 10-строчная таблица цветов интерфейса графа Obsidian. Модель LLM не занимается визуализацией, ее читает клиент Obsidian из `docs/.obsidian/graph.json`. Информация о цветах расходует токены внимания модели вхолостую.
3. **Дублирование скиллов `docs-as-code` и `kb-onboard`:** Скилл `docs-as-code` дублирует список команд реестра и онбординг, создавая избыточную сущность в Always-On реестре описаний скиллов.
4. **Когнитивный барьер 13 шаблонов:** Для новых пользователей наличие 13 файлов в `docs/00_Templates/` создает ощущение тяжеловесной бюрократии.

---

## 2. Решение

Принято комплексное архитектурное решение по оптимизации слоев правил и таксономии базы знаний:

### 2.1. Паттерн «Тонких форвардеров» (Thin Forwarders) для адаптеров IDE
* Генераторы правил в `install.py` (`generate_gemini_md`, `generate_claude_md`, `generate_cursorrules`, `generate_windsurfrules`, `generate_clinerules`, `generate_copilot_instructions`) переводятся на формат тонких указателей (до 25–30 строк).
* Содержание адаптера:
  1. Метаданные проекта и технологический стек.
  2. Команды верификации (`Build`, `Test`, `Lint`).
  3. Прямая ссылка на канонический `AGENTS.md` как Single Source of Truth (SSOT).
  4. Краткий протокол исполнения (4 режима, Anti-Echo, Single-Task Barrier).

### 2.2. Декуплинг визуальной таксономии Obsidian Graph
* Таблица цветов графа с RGB-кодами полностью удаляется из `AGENTS.md` и генератора `generate_agents_md`.
* Конфигурация графа (цвета, фильтры, физика) локализуется строго в `docs/.obsidian/graph.json`.
* В `AGENTS.md` сохраняется лаконичная директива:
  > `Obsidian Graph: visual taxonomy is configured in .obsidian/graph.json. Ensure notes are placed in designated directories with canonical tags (#arch, #adr, #research, #task, #bug, #testing).`

### 2.3. Консолидация мета-скилла и онбординга
* Отдельный скилл `.agents/skills/docs-as-code/` упраздняется.
* Навигация по жизненному циклу, справочник команд и структура папок объединяются в скилле `kb-onboard` и документе `docs/Onboarding.md`.
* Высвобождается постоянный слот в Always-On реестре описаний скиллов модели.

### 2.4. Градация шаблонов в руководстве разработчика
* В `docs/Onboarding.md` шаблоны разделяются на:
  * **Core (Базовые):** `TEMPLATE_ADR.md`, `TEMPLATE_PLAN.md`, `TEMPLATE_TASK.md`, `TEMPLATE_BUG.md`.
  * **Extended (Специализированные):** `TEMPLATE_RESEARCH.md`, `TEMPLATE_RELEASE.md`, `TEMPLATE_FEEDBACK.md`, `TEMPLATE_TEST.md`, `TEMPLATE_DEVLOG.md`, `TEMPLATE_INDEX.md`, `TEMPLATE_KANBAN.md`, `TEMPLATE_ROADMAP.md`, `TEMPLATE_ARCHITECTURE.md`.
* Явно фиксируется назначение шаблонов как системных структур для скиллов агента, снимая ощущение необходимости их ручного заполнения.

---

## 3. Отвергнутые варианты (Rejected Alternatives)

* **Полная ликвидация адаптеров вендоров (только `AGENTS.md`):**  
  *Причина отклонения:* Инструменты вроде Claude Code (`CLAUDE.md`), Cursor (`.cursorrules`) и Windsurf (`.windsurfrules`) требуют наличия нативных файлов для автоматического применения инструкций при инициализации сессии.
* **Сохранение скилла `docs-as-code` параллельно с `kb-onboard`:**  
  *Причина отклонения:* Создает дублирование функционала и расходует квоту внимания в реестре системного промпта.
* **Удаление второстепенных шаблонов из поставки инсталлятора:**  
  *Причина отклонения:* Нарушит автономность скиллов (`/kb-release`, `/kb-research`, `/kb-triage`), которые опираются на эталонные шаблоны при генерации документов.

---

## 4. Последствия

### Плюсы:
1. **Снижение постоянного контекста на 70% в адаптерах IDE:** исключена повторная инжекция 14 дисциплин.
2. **Исключение Rule Drift:** `AGENTS.md` становится фактическим и единственным SSOT; адаптеры лишь ссылаются на него.
3. **Чистый контекст LLM (-150 токенов на шаг):** устранена таблица цветов Obsidian из системных промптов.
4. **Упрощение реестра скиллов:** онбординг и навигация объединены в одной точке.

### Минусы / Компромиссы:
1. В IDE, не поддерживающих рекурсивный переход по ссылкам на файлы в системных промптах, модель должна явно считывать `AGENTS.md` через инструмент чтения файлов при начале сессии (что уже закреплено первой строкой адаптеров).
