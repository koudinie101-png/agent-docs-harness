---
id: PLAN-010
title: "Фаза 10: Рождение Мастер-Спецификации (Spec Genesis) и High-SNR релизные заметки (Spec Genesis Protocol & High-SNR Release Notes)"
status: accepted
type: plan
phase: 10
created: 2026-10-03
updated: 2026-10-03
tags:
  - plan
  - phase10
  - spec-genesis
  - master-spec
  - zero-state
  - release-notes
  - high-snr
  - docs-as-code
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 📋 План: PLAN-010 — Фаза 10: Рождение Мастер-Спецификации (Spec Genesis) и High-SNR релизные заметки

> **ID:** PLAN-010  
> **Статус:** Согласовано (Режим 1)  
> **Теги:** #plan #phase10 #spec-genesis #master-spec #zero-state #release-notes #high-snr #docs-as-code  
> **Родительская спецификация:** [[../../SPEC|SPEC.md]]  
> **Канбан:** [[../Kanban|Канбан-доска]]  
> **Связанные исследования и ADR:** [[../../04_Research/RESEARCH-011-spec-genesis-protocol-and-zero-state-handling|RESEARCH-011: Протокол рождения Мастер-Спецификации]], [[../../03_Decisions_ADR/ADR-0018-spec-genesis-protocol-and-zero-state-handling|ADR-0018: Протокол Spec Genesis и контроль Zero-State]], [[../../04_Research/RESEARCH-013-release-notes-adr-exclusion-and-high-snr|RESEARCH-013: Оптимизация публичных релизных заметок]], [[../../03_Decisions_ADR/ADR-0017-release-notes-adr-exclusion-and-high-snr-standard|ADR-0017: Исключение секции ADR из релизных заметок]], [[../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001: Zero Dependencies]], [[../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009: High-SNR]], [[../../03_Decisions_ADR/ADR-0010-github-release-notes-and-public-distribution-standard|ADR-0010: GitHub Release Standard]], [[../../03_Decisions_ADR/ADR-0014-greenfield-idea-first-initialization-and-living-spec-protocol|ADR-0014: Living Spec]]

---

## 1. Контекст и цели (Problem & Goals)

### Проблема
1. **Разрыв тулинга и риск Zero-State галлюцинаций (Входной шлюз):**
   При инициализации через скилл `.agents/skills/kb-init/SKILL.md` файл `SPEC.md` не создается вовсе, тогда как инсталлятор `install.py` генерирует каркас со статусом `discovery`. При отсутствии спецификации или ее пустом состоянии агент в последующих сессиях рискует директивно выдумать («галлюцинировать») произвольный стек и функционал без диалога с пользователем.
2. **Кумулятивное раздувание публичных заметок релиза (Выходной шлюз):**
   В утилите `scripts/kb_release.py` функция `generate_public_release_notes()` автоматически включает кумулятивный реестр всех исторических ADR проекта (до 16+ записей), занимающий до 45% текста заметок на GitHub. Это размывает полезный сигнал (Highlights, Installation, SHA-256) и смешивает аудитории пользователей дистрибутива и внутренних разработчиков архитектуры.

### Цели Фазы 10
Объединить два комплементарных стандарта чистоты жизненного цикла в единую систему:
1. **Spec Genesis & Zero-State Protocol ([[../../03_Decisions_ADR/ADR-0018-spec-genesis-protocol-and-zero-state-handling|ADR-0018]], [[../../04_Research/RESEARCH-011-spec-genesis-protocol-and-zero-state-handling|RESEARCH-011]]):**
   - Добавить создание каркаса `SPEC.md` (`status: discovery`) в скилл `kb-init`.
   - Внедрить предупреждающие проверки (Nudge) в скиллы `kb-plan` и `kb-task` при статусе спецификации `discovery` или ее отсутствии.
   - Зафиксировать в `AGENTS.md` нормативный инвариант запрета директивной автогенерации бизнес-требований и стека без ведома человека.
2. **High-SNR Release Notes Standard ([[../../03_Decisions_ADR/ADR-0017-release-notes-adr-exclusion-and-high-snr-standard|ADR-0017]], [[../../04_Research/RESEARCH-013-release-notes-adr-exclusion-and-high-snr|RESEARCH-013]]):**
   - Упразднить секцию `### 🏛️ Архитектурные решения (ADR)` в публичном генераторе заметок `generate_public_release_notes()` в `scripts/kb_release.py`.
   - Ограничить включение ADR во внутреннем архивном чейнджлоге `docs/02_Tasks/Releases/RELEASE-vX.Y.Z.md` только решениями текущей фазы (`phase: N`).
   - Актуализировать шаблон `TEMPLATE_RELEASE.md` и скилл `kb-release`.
3. **Синхронизация и E2E верификация:**
   - Обновить дистрибутив `install.py` через `scripts/build_installer.py` (с поддержкой `install.py --update`).
   - Добавить регрессионные тесты в `tests/test_installer.py` и `tests/test_kb_release.py`.
   - Актуализировать витрину `README.md` и руководство `docs/Onboarding.md`.

---

## 2. Обсуждение и решения (Q&A / Discussion)

* **Q1: Почему объединение ADR-0018 и ADR-0017 архитектурно оправдано?**
  * **Решение:** Оба решения устраняют размытие сигналов и структурные дефекты на противоположных полюсах жизненного цикла Docs-as-Code: Spec Genesis защищает начальную точку входа проекта от ложного Ground Truth, а High-SNR Release Notes защищает финальную точку выхода от кумулятивного шума. Оба решения имеют зрелую нормативную базу и соотношение High Value / Low Effort.
* **Q2: Блокирует ли Zero-State гейткипинг выполнение команд пользователя?**
  * **Решение:** Нет. В соответствии с Friendly DX агент не блокирует точечные команды или утилитарные задачи, а выдает мягкое предупреждение (Soft Nudge) перед планированием новой крупной функциональности (`/kb-plan`), если спецификация еще не кристаллизована.
* **Q3: Где теперь отражаются архитектурные решения в релизах?**
  * **Решение:** В публичных заметках на GitHub ADR опускаются, так как внешнему пользователю важны пользовательские изменения и контрольные суммы SHA-256. В случае необходимости ссылки на ключевые ADR даются инлайн в задачах (`TASK-XXX`). Во внутреннем архиве `docs/02_Tasks/Releases/` сохраняются ADR текущей фазы.

---

## 3. Архитектурное влияние и риски (Architectural Impact & Risks)

* **Затрагиваемые компоненты:**
  * `.agents/skills/kb-init/SKILL.md` — генерация начального каркаса `SPEC.md` (`status: discovery`).
  * `.agents/skills/kb-plan/SKILL.md` — префлайт-чеки статуса спецификации и Zero-State Nudge.
  * `.agents/skills/kb-task/SKILL.md` — проверка готовности спецификации перед нарезкой ТЗ.
  * `AGENTS.md` — инвариант защиты от слепой автогенерации спецификации.
  * `scripts/kb_release.py` — удаление секции ADR из публичного чейнджлога и скоупинг ADR по текущей фазе во внутреннем архиве.
  * `.agents/skills/kb-release/SKILL.md` — обновление инструкций экспорта заметок.
  * `docs/00_Templates/TEMPLATE_RELEASE.md` и `templates/TEMPLATE_RELEASE.md` — синхронизация шаблона.
  * `tests/test_kb_release.py` — модульные тесты чистоты заметок и фазовой фильтрации.
  * `install.py` и `scripts/build_installer.py` — сборка автономного инсталлятора и доставка обновлений.
  * `tests/test_installer.py` — сквозные E2E тесты.
  * `README.md` и `docs/Onboarding.md` — актуализация документации.

* **Оценка рисков:**
  * Стандартная библиотека Python (Zero Dependencies preserved).
  * 100% обратная совместимость: существующие проекты продолжают работать, а при `install.py --update` получают обновленные скиллы и шаблоны.

---

## 4. Декомпозиция задач (Task Breakdown)

- [ ] [[../Specs/10_SpecLifecycle/TASK-036-spec-genesis-and-zero-state-guardrails|TASK-036]]: Spec Genesis Protocol & Zero-State Guardrails (генерация `SPEC.md` со статусом `discovery` в `kb-init`, префлайт-проверки в `kb-plan` и `kb-task`, инвариант в `AGENTS.md`).
- [ ] [[../Specs/10_SpecLifecycle/TASK-037-high-snr-release-notes-and-phase-adr-scoping|TASK-037]]: High-SNR Release Notes Generator & Phase ADR Scoping (упразднение секции ADR в `generate_public_release_notes` в `scripts/kb_release.py`, фазовый скоупинг во внутреннем чейнджлоге, обновление `TEMPLATE_RELEASE.md` и `kb-release`, модульные тесты в `tests/test_kb_release.py`).
- [ ] [[../Specs/10_SpecLifecycle/TASK-038-installer-bundling-e2e-and-docs|TASK-038]]: Синхронизация инсталлятора, сквозные E2E тесты и документация (сборка `install.py` через `scripts/build_installer.py`, регрессионные E2E тесты в `tests/test_installer.py`, аудит `scripts/kb_lint.py`, обновление `README.md` и `docs/Onboarding.md`).

---

## 5. Критерии приемки плана (Definition of Done для Режима 1)

- [x] Концепция согласована с пользователем (Режим 1: READ-ONLY, без изменения проектного кода).
- [x] Опирается на завершенные исследования [[../../04_Research/RESEARCH-011-spec-genesis-protocol-and-zero-state-handling|RESEARCH-011]], [[../../04_Research/RESEARCH-013-release-notes-adr-exclusion-and-high-snr|RESEARCH-013]] и стандарты [[../../03_Decisions_ADR/ADR-0018-spec-genesis-protocol-and-zero-state-handling|ADR-0018]], [[../../03_Decisions_ADR/ADR-0017-release-notes-adr-exclusion-and-high-snr-standard|ADR-0017]].
- [x] Создан файл плана `docs/02_Tasks/Plans/PLAN-010-spec-genesis-and-high-snr-release-notes.md`.
- [x] Инициативы промоутированы из Icebox в Фазу 10 в `docs/02_Tasks/Roadmap.md`.
- [x] Задачи `TASK-036` — `TASK-038` добавлены в `docs/02_Tasks/Kanban.md` в колонку `📥 Бэклог (Backlog)`.
- [x] Целостность базы знаний подтверждена через `python scripts/kb_lint.py --path docs`.
