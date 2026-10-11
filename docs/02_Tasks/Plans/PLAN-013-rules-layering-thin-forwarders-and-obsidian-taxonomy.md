---
id: PLAN-013
title: "Фаза 13 — Слоистая архитектура правил (Thin Forwarders), декуплинг графа Obsidian и таксономия базы знаний"
status: proposed
type: plan
phase: 13
created: 2026-10-11
updated: 2026-10-11
tags:
  - plan
  - phase13
  - rules-layering
  - thin-forwarders
  - obsidian-graph
  - token-optimization
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
related_adr: "[[../../03_Decisions_ADR/ADR-0021-rules-layering-thin-forwarders-and-obsidian-taxonomy|ADR-0021]]"
related_research: "[[../../04_Research/RESEARCH-016-agent-rules-hierarchy-and-knowledge-base-structure|RESEARCH-016]]"
---

# 📋 План: PLAN-013 — Слоистая архитектура правил (Thin Forwarders), декуплинг графа Obsidian и таксономия базы знаний

> **ID:** PLAN-013 | **Статус:** Обсуждение / Согласовано  
> **Спецификация:** [[../../SPEC|SPEC.md]] | **Канбан:** [[../Kanban|Канбан]]  
> **Обоснование:** [[../../04_Research/RESEARCH-016-agent-rules-hierarchy-and-knowledge-base-structure|RESEARCH-016]] | **Решение:** [[../../03_Decisions_ADR/ADR-0021-rules-layering-thin-forwarders-and-obsidian-taxonomy|ADR-0021]]

---

## 1. Контекст и цели (Problem & Goals)

### Проблема
1. **Двойная инжекция контекста (Double Prompt Injection) и Rule Drift:** Адаптеры IDE (`GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`, `.github/copilot-instructions.md`) дублируют 85% правил и режимов из `AGENTS.md`. В Cursor/Antigravity агент считывает оба файла, сжигая контекст вдвое. При обновлении `AGENTS.md` адаптеры рассинхронизируются.
2. **Токеновый налог визуальной палитры Obsidian:** Таблица цветов интерфейса графа Obsidian в `AGENTS.md` (10 строк) тратит ~150 токенов контекста модели на каждом запросе, хотя предназначается исключительно человеку.
3. **Размытие ответственности скиллов:** Мета-скилл `docs-as-code` дублирует функции автономных скиллов и онбординга `kb-onboard`.
4. **Когнитивный барьер 14 шаблонов:** Отсутствие градации шаблонов на минимальный базис (Core) и специализированные надстройки (Advanced) усложняет старт для новых разработчиков.

### Цели
* Перевести адаптеры IDE на паттерн **Thin Forwarders** (до 30 строк, ссылки на `AGENTS.md`, команды верификации стека), снизив объем адаптеров на 80–85%.
* Полностью удалить цветовую таблицу из `AGENTS.md` и локализовать визуальные настройки строго в `docs/.obsidian/graph.json` (-150 токенов на шаг диалога).
* Консолидировать навигацию и онбординг, объединив функции `docs-as-code` и `kb-onboard`.
* Выделить двухуровневую структуру шаблонов (Core Essentials vs Advanced Governance) в руководстве `docs/Onboarding.md`.

---

## 2. Обсуждение и решения (Q&A)

* **Q1: Не потеряют ли адаптеры IDE свою эффективность при сжатии до 30 строк?**
  * **Решение:** Нет. В современных средах первой строкой прописывается прямая ссылка на `AGENTS.md` как Single Source of Truth (SSOT). Адаптер сохраняет главное: команды сборки, тестов и линтинга конкретного стека и запрет на изменение кода в режимах 1/2. Это соответствует официальным рекомендациям Anthropic для `CLAUDE.md` и лучшим практикам Cursor.
* **Q2: Что делать с таблицей цветов Obsidian Graph?**
  * **Решение:** Изолировать в `.obsidian/graph.json`. В `AGENTS.md` оставить только одну лаконичную директиву: размещать файлы в канонических папках с каноническими тегами (`#arch`, `#adr`, `#research`, `#task`, `#bug`, `#testing`).
* **Q3: Как поступить со скиллом `docs-as-code`?**
  * **Решение:** Консолидировать его функции в `kb-onboard`. В Always-On реестре описаний скиллов высвобождается слот, устраняя конкуренцию триггеров.

---

## 3. Архитектурное влияние и риски

* **Затрагиваемые компоненты:** `install.py`, `scripts/build_installer.py`, `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`, `.github/copilot-instructions.md`, `.agents/skills/docs-as-code/`, `.agents/skills/kb-onboard/`, `docs/Onboarding.md`, `tests/test_installer.py`.
* **Риски:** Потенциальный слом тестов в `test_installer.py`, проверяющих наличие специфических строк в сгенерированных адаптерах.
* **Митигация:** Обновление тестовых ассертов на проверку наличия команд верификации и ссылок на `AGENTS.md` в тонких форвардерах.

---

## 4. Декомпозиция задач (Task Breakdown)

- [x] [[../Specs/13_RulesLayering/TASK-048-clean-agents-md-and-obsidian-taxonomy|TASK-048]]: Очистка `AGENTS.md` от графового шума и изоляция таксономии Obsidian Graph в `.obsidian/graph.json`
- [x] [[../Specs/13_RulesLayering/TASK-049-thin-forwarders-adapters-generator|TASK-049]]: Реализация паттерна Thin Forwarders в генераторах адаптеров `install.py`
- [x] [[../Specs/13_RulesLayering/TASK-050-consolidate-onboard-and-template-taxonomy|TASK-050]]: Консолидация `docs-as-code` и `kb-onboard`, двухуровневая таксономия шаблонов в `Onboarding.md`
- [ ] [[../Specs/13_RulesLayering/TASK-051-bundling-e2e-tests-and-living-spec|TASK-051]]: Сборка инсталлятора `build_installer.py`, сквозные E2E тесты и актуализация Living Spec

---

## 5. Критерии приемки плана (DoD Режима 1)

- [x] Концепция согласована (RESEARCH-016 и ADR-0021 приняты).
- [ ] Дорожная карта `Roadmap.md` обновлена (Фаза 13 оформлена в активный статус).
- [ ] Карточки задач добавлены в `Kanban.md` в `📥 Бэклог`.
- [ ] Целостность подтверждена через `python scripts/kb_lint.py --path docs`.
