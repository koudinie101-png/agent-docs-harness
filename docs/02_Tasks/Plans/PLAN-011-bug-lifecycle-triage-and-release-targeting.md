---
id: PLAN-011
title: "Фаза 11: Жизненный цикл дефектов, прозрачный триаж и релизный таргетинг (Bug Lifecycle & Release Targeting)"
status: accepted
type: plan
phase: 11
created: 2026-10-04
updated: 2026-10-04
tags:
  - plan
  - phase11
  - bug-lifecycle
  - triage
  - release-targeting
  - tdd
  - docs-as-code
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 📋 План: PLAN-011 — Фаза 11: Жизненный цикл дефектов, прозрачный триаж и релизный таргетинг

> **ID:** PLAN-011  
> **Статус:** Согласовано (Режим 1)  
> **Теги:** #plan #phase11 #bug-lifecycle #triage #release-targeting #tdd #docs-as-code  
> **Родительская спецификация:** [[../../SPEC|SPEC.md]]  
> **Канбан:** [[../Kanban|Канбан-доска]]  
> **Связанные исследования и ADR:** [[../../04_Research/RESEARCH-014-bug-lifecycle-triage-and-release-targeting|RESEARCH-014: Архитектура жизненного цикла дефектов]], [[../../03_Decisions_ADR/ADR-0019-bug-lifecycle-triage-and-release-targeting|ADR-0019: Архитектура ЖЦ дефектов, изолированный триаж и релизный таргетинг]], [[../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001: Zero Dependencies]], [[../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009: High-SNR]], [[../../03_Decisions_ADR/ADR-0010-github-release-notes-and-public-distribution-standard|ADR-0010: GitHub Release Standard]], [[../../03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016: Single-Task Execution Barrier]]

---

## 1. Контекст и цели (Problem & Goals)

### Проблема
1. **Самовольный фикс дефектов без контроля разработчика (Eager Auto-Fixing Runaway):**  
   В текущей реализации скилл `.agents/skills/kb-bug/SKILL.md` совмещает в себе и процедуру заведения бага, и немедленное исполнение исправлений в коде. При вызове `/kb-bug` агент срывает барьер единичной задачи ([[../../03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]]) и бросается переписывать кодовую базу без явного решения человека о приоритете бага (горячий багфикс vs планирование в спринт).
2. **Отсутствие релизного контракта в дефектах:**  
   В шаблоне `TEMPLATE_BUG.md` отсутствуют метаданные привязки к релизам (`target_release`, `target_phase`, `release_blocker`, `fixed_in`). Невозможно отследить, блокирует ли баг текущий релиз и в какую версию должно войти исправление.
3. **Хроническая утечка исторических дефектов в Release Notes:**  
   Генератор релизов `scripts/kb_release.py` агрегирует все когда-либо закрытые баги из каталога `docs/02_Tasks/Bugs/` без фильтрации по версии релиза. В результате закрытые дефекты предыдущих фаз снова и снова дублируются в публичных чейнджлогах новых версий на GitHub.
4. **Блокировка интеграции внешнего фидбека:**  
   Реализация буфера входящих сообщений и GitHub Issue Forms ([[../../04_Research/RESEARCH-003-feedback-channels-and-triage-pipeline|RESEARCH-003]]) невозможна без четкого изолированного триажа и конвертации обратной связи в `BUG-XXX`.

### Цели Фазы 11
1. **Изоляция триажа в Режиме 2B (`kb-bug`):**  
   Превратить `/kb-bug` в чистый инструмент фиксации дефекта, RCA-анализа и интерактивного триажа без права изменения исходного кода проекта. Внедрить обязательный терминальный шаг `Stop & Yield Control`.
2. **Унификация исполнения в Режиме 3 (`kb-implement BUG-XXX`):**  
   Обучить скилл `/kb-implement` принимать идентификаторы дефектов `BUG-XXX` и исполнять строгий TDD-цикл (RED $\to$ GREEN $\to$ REFACTOR $\to$ `kb-complete`). Автоматически проставлять `fixed_in` в метаданных бага при закрытии.
3. **Релизный контракт и точная фильтрация в `kb_release.py`:**  
   Расширить `TEMPLATE_BUG.md` обязательными полями релизного таргетинга. В `scripts/kb_release.py` фильтровать дефекты строго по целевой версии (`fixed_in == target_version` или fallback по фазе), а также блокировать релиз при наличии открытых дефектов с флагом `release_blocker: true`.
4. **Синхронизация инсталлятора и сквозная верификация:**  
   Обновить `install.py` через `scripts/build_installer.py`, покрыть E2E и юнит-тестами, обновить `SPEC.md`, `README.md` и документацию онбординга.

---

## 2. Обсуждение и решения (Q&A / Discussion)

* **Q1: Почему выбран запуск `/kb-implement BUG-XXX`, а не создание отдельного скилла `/kb-fix`?**  
  * **Решение (согласно [[../../03_Decisions_ADR/ADR-0019-bug-lifecycle-triage-and-release-targeting|ADR-0019]]):** Создание отдельного скилла привело бы к 100% дублированию шагов Режима 3 (верификация тестами, kb_lint, обновление канбана/роадмапа, devlog, git-коммит). Унификация в `/kb-implement` сберегает токеномику (High-SNR) и обеспечивает единый прозрачный вход в Режим 3.
* **Q2: Как предотвратить случайный выпуск релиза с критическими багами?**  
  * **Решение:** Поле `release_blocker: true` в frontmatter `BUG-XXX`. В утилите `scripts/kb_release.py` добавляется префлайт-проверка: если для текущего релиза/фазы обнаружен незакрытый блокер (`status: open/in-progress`), релиз завершается с ошибкой Exit Code 1.
* **Q3: Как заполняется поле `fixed_in`?**  
  * **Решение:** Автоматически на шаге завершения задачи (`kb-complete` / финальный этап `kb-implement`), извлекая номер текущей активной версии или фазы из `SPEC.md` / `Roadmap.md`.

---

## 3. Архитектурное влияние и риски

* **Затрагиваемые файлы и модули:**
  - `docs/00_Templates/TEMPLATE_BUG.md` — внедрение полей `target_release`, `target_phase`, `release_blocker`, `fixed_in`.
  - `.agents/skills/kb-bug/SKILL.md` — удаление права правок кода, превращение в Режим 2B, добавление терминального шага Stop & Yield.
  - `.agents/skills/kb-implement/SKILL.md` — маршрутизация `BUG-XXX` по TDD-контракту, интеграция с `kb-complete`.
  - `.agents/skills/kb-complete/SKILL.md` — закрытие дефекта с автозаполнением `fixed_in`.
  - `scripts/kb_release.py` — фильтрация дефектов по версии, проверка release_blocker, обновление чейнджлога.
  - `tests/test_kb_release.py` — юнит-тесты фильтрации багов и проверки блокеров.
  - `scripts/build_installer.py`, `install.py` — синхронизация шаблонов и скиллов.
  - `tests/test_installer.py` — регрессионный E2E тест инсталлятора.
  - `SPEC.md`, `README.md`, `docs/Onboarding.md` — актуализация витрины и спецификации жизненного цикла дефектов.
* **Риски:**
  - *Риск обратной совместимости:* Старые баги в существующих проектах не содержат полей `fixed_in`.  
    *Митигация:* Реализовать бережный fallback в `scripts/kb_release.py` (если `fixed_in` отсутствует, проверять `target_phase` или дату/теги, исключая дублирование).

---

## 4. Декомпозиция задач (Task Breakdown)

- [ ] [[../Specs/11_BugLifecycle/TASK-039-template-bug-and-kb-bug-triage-skill|TASK-039: Рефакторинг TEMPLATE_BUG.md и скилла kb-bug (строгий триаж Режима 2B и терминальный Stop & Yield)]]
- [ ] [[../Specs/11_BugLifecycle/TASK-040-kb-implement-bug-lifecycle-and-tdd|TASK-040: Нативная поддержка дефектов в kb-implement (/kb-implement BUG-XXX и строгий TDD-цикл)]]
- [ ] [[../Specs/11_BugLifecycle/TASK-041-kb-release-defect-filtering-and-blockers|TASK-041: Релизный таргетинг и фильтрация дефектов в scripts/kb_release.py и тесты]]
- [ ] [[../Specs/11_BugLifecycle/TASK-042-installer-bundling-e2e-and-docs|TASK-042: Синхронизация инсталлятора, сквозные E2E тесты и документация]]

---

## 5. Критерии приемки плана (DoD Режима 1)

- [x] Концепция согласована с пользователем (READ-ONLY, без кода).
- [ ] Дорожная карта `Roadmap.md` обновлена (Фаза 11 перенесена из Icebox в активный трек).
- [ ] Карточки добавлены в `Kanban.md` в `📥 Бэклог`.
- [ ] Целостность базы знаний подтверждена через `python scripts/kb_lint.py --path docs`.
