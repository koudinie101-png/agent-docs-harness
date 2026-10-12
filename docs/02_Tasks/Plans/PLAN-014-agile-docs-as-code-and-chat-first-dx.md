---
id: PLAN-014
title: "Фаза 14 — Продуктовый DX, протокол Fast-Track и адаптация для вайбкодеров (Agile Docs-as-Code & Chat-First DX)"
status: accepted
type: plan
phase: 14
created: 2026-10-12
updated: 2026-10-12
tags:
  - plan
  - phase14
  - dx
  - fast-track
  - vibe-coding
  - chat-first
  - agile
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
related_adr:
  - "[[../../03_Decisions_ADR/ADR-0015-zero-to-hero-onboarding-guide-architecture|ADR-0015]]"
  - "[[../../03_Decisions_ADR/ADR-0022-chat-first-vibe-coder-dx-and-human-guardrails|ADR-0022]]"
  - "[[../../03_Decisions_ADR/ADR-0023-fast-track-protocol-for-micro-tasks|ADR-0023]]"
related_research:
  - "[[../../04_Research/RESEARCH-010-zero-to-hero-onboarding-guide-and-developer-mental-models|RESEARCH-010]]"
  - "[[../../04_Research/RESEARCH-017-vibe-coder-dx-and-chat-first-onboarding|RESEARCH-017]]"
  - "[[../../04_Research/RESEARCH-018-fast-track-protocol-for-micro-tasks|RESEARCH-018]]"
---

# 📋 План: PLAN-014 — Продуктовый DX, протокол Fast-Track и адаптация для вайбкодеров

> **ID:** PLAN-014 | **Статус:** Согласовано  
> **Спецификация:** [[../../SPEC|SPEC.md]] | **Канбан:** [[../Kanban|Канбан]]  
> **Обоснование:** [[../../04_Research/RESEARCH-010-zero-to-hero-onboarding-guide-and-developer-mental-models|RESEARCH-010]], [[../../04_Research/RESEARCH-017-vibe-coder-dx-and-chat-first-onboarding|RESEARCH-017]], [[../../04_Research/RESEARCH-018-fast-track-protocol-for-micro-tasks|RESEARCH-018]]  
> **Решения (ADR):** [[../../03_Decisions_ADR/ADR-0015-zero-to-hero-onboarding-guide-architecture|ADR-0015]], [[../../03_Decisions_ADR/ADR-0022-chat-first-vibe-coder-dx-and-human-guardrails|ADR-0022]], [[../../03_Decisions_ADR/ADR-0023-fast-track-protocol-for-micro-tasks|ADR-0023]]

---

## 1. Контекст и цели (Problem & Goals)

### Проблема
1. **Процедурное трение на микро-задачах (Protocol Fatigue):**
   Для локального изменения в $\le 30$ строк кода (правка регулярки, опечатки, параметра конфига) требовался полный цикл: Режим 1 (`PLAN-XXX`, ~100 строк) $\to$ Режим 2 (`TASK-XXX`, ~80 строк) $\to$ Режим 3 (`/kb-implement`). Это приводило к сжиганию 25–40k токенов и провоцировало разработчиков вносить правки вручную в обход Docs-as-Code.
2. **Терминальный шок и когнитивный барьер новичков:**
   Разработчики без опыта системного администрирования («вайбкодеры») пугаются консольных пайпов (`curl | python3`), строгих аббревиатур (RFC, DoD, RCA, TDD) и жестких запретов агента (`🚨 NO CODE EDITS`), воспринимая их как отказ от работы.
3. **Отсутствие дружелюбного онбординга и человечных чейнджлогов:**
   Существующий онбординг ориентирован на классических инженеров. Релизные заметки GitHub содержат технический лог, требующий перевода на простой пользовательский язык.

### Цели
* Внедрить **протокол Fast-Track**: разрешить пропуск Режима 1 (`PLAN-XXX`) для микро-задач ($\le 30$ LOC, $\le 2$ файлов) со стартом сразу через `/kb-task --fast` и компактным шаблоном `TEMPLATE_TASK_MICRO.md` (-70% контекста).
* Закрепить диалоговый принцип **«Направляй, а не блокируй» (Human Guardrails)** в `AGENTS.md`: агент проактивно задает 1–2 понятных вопроса при остановке в Режимах 1/2 вместо сухих отказов.
* Добавить **Chat-First Bootstrapping** в `README.md` (готовый копируемый промпт без терминала).
* Разработать руководство `docs/Zero_To_Hero_Guide.md` («Вайбкодинг со страховкой») и шпаргалку сред разработки.
* Реализовать **Human-First генерацию чейнджлогов** в `scripts/kb_release.py` и аудит Fast-Track в `scripts/kb_lint.py`.

---

## 2. Обсуждение и решения (Q&A)

* **Q1: Не приведет ли Fast-Track к разрушению дисциплины и «вайб-хаосу»?**
  * **Решение:** Нет. Введены строгие Scope Guardrails: лимит $\le 30$ строк кода, $\le 2$ файлов, запрет на изменение нормативных файлов (`SPEC.md`, `AGENTS.md`) и внешних библиотек. Сохраняются Permalinks, карточка в Канбане, команда верификации, тесты и двухстадийный барьер безопасности (`/kb-task --fast` $\to$ Stop & Yield $\to$ подтверждение $\to$ `/kb-implement`).
* **Q2: Зачем объединять Fast-Track и адаптацию для вайбкодеров в одну фазу?**
  * **Решение:** Обе инициативы оптимизируют User Experience (DX) системы. Они одновременно модифицируют правила агентов (`AGENTS.md`), шаблоны (`docs/00_Templates/`), онбординг (`kb-onboard`) и инсталлятор, что делает их объединение архитектурно монолитным и исключает дублирование релизных циклов.
* **Q3: Как сохранить One-Prompt запуск без терминала?**
  * **Решение:** В витрину `README.md` помещается готовый короткий промпт для окна чата AI-среды, содержащий директиву агенту автоматически запустить инсталлятор в фоновом режиме.

---

## 3. Архитектурное влияние и риски

* **Затрагиваемые компоненты:**
  - Шаблоны: `docs/00_Templates/TEMPLATE_TASK_MICRO.md` [NEW], `templates/TEMPLATE_TASK_MICRO.md` [NEW].
  - Скиллы: `.agents/skills/kb-task/SKILL.md`, `.agents/skills/kb-plan/SKILL.md`, `.agents/skills/kb-onboard/SKILL.md`.
  - Правила: `AGENTS.md`, адаптеры в `install.py`.
  - Документация: `docs/Zero_To_Hero_Guide.md` [NEW], `README.md`, `SPEC.md`, `docs/Onboarding.md`.
  - Скрипты: `scripts/kb_lint.py`, `scripts/kb_release.py`, `scripts/build_installer.py`, `install.py`.
  - Тесты: `tests/test_installer.py`, `tests/test_kb_lint.py`, `tests/test_kb_release.py`.
* **Риски и митигация:**
  - *Риск расползания скоупа:* агент может недооценить сложность микро-задачи. *Митигация:* автоматический аудит лимитов файлов и проверка в `kb_lint.py`.
  - *Раздувание инсталлятора:* новые материалы могут увеличить вес монолита. *Митигация:* соблюдение стандартов High-SNR сжатия текста.

---

## 4. Декомпозиция задач (Task Breakdown)

- [ ] `TASK-052`: Шаблон Micro-Spec `TEMPLATE_TASK_MICRO.md` и поддержка Fast-Track в `kb-task` / `kb-plan`
- [ ] `TASK-053`: Принцип «Направляй, а не блокируй» (Human Guardrails) в `AGENTS.md` и адаптерах
- [ ] `TASK-054`: Практический гайд `Zero_To_Hero_Guide.md` («Вайбкодинг со страховкой») и менторский онбординг в `kb-onboard`
- [ ] `TASK-055`: Human-First чейнджлоги в `scripts/kb_release.py` и аудит Fast-Track в `scripts/kb_lint.py`
- [ ] `TASK-056`: Синхронизация инсталлятора `install.py` / `build_installer.py`, E2E тесты и актуализация Living Spec

---

## 5. Критерии приемки плана (DoD Режима 1)

- [x] Концепция согласована и утверждена (READ-ONLY, без изменения кода).
- [ ] Дорожная карта `Roadmap.md` обновлена (Фаза 14 добавлена в активный график, пункты перенесены из Icebox).
- [ ] Карточки добавлены в `Kanban.md` в секцию `📥 Бэклог (Backlog)`.
- [ ] Целостность связей подтверждена запуском `python scripts/kb_lint.py --path docs`.
