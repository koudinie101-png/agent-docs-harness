---
id: TASK-040
title: "Нативная поддержка дефектов в kb-implement (/kb-implement BUG-XXX и строгий TDD-цикл)"
status: planned
type: task
phase: 11
component:
  - skills
  - bug-lifecycle
  - tdd
  - implementation
parent_plan: "[[../../Plans/PLAN-011-bug-lifecycle-triage-and-release-targeting|PLAN-011]]"
created: 2026-10-04
updated: 2026-10-04
tags:
  - task/spec
  - phase11
  - bug-lifecycle
  - tdd
  - implementation
  - kb-complete
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-040 — Нативная поддержка дефектов в kb-implement

> **ID:** TASK-040  
> **Статус:** К реализации (Режим 2)  
> **Теги:** #task/spec #phase11 #bug-lifecycle #tdd #implementation #kb-complete  
> **Родительский план:** [[../../Plans/PLAN-011-bug-lifecycle-triage-and-release-targeting|PLAN-011]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-014-bug-lifecycle-triage-and-release-targeting|RESEARCH-014]], [[../../../03_Decisions_ADR/ADR-0019-bug-lifecycle-triage-and-release-targeting|ADR-0019]], [[../../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]], [[../../../03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Унифицировать исполнение дефектов в рамках **Режима 3 (Implementation & Verification)** согласно [[../../../03_Decisions_ADR/ADR-0019-bug-lifecycle-triage-and-release-targeting|ADR-0019]]:
1. **Поддержка аргумента `BUG-XXX` в `kb-implement`:** Расширить скилл `.agents/skills/kb-implement/SKILL.md` для приема дефекта в качестве цели исполнения (`/kb-implement BUG-XXX`).
2. **Строгий TDD-пайплайн (Regression-First):** Закрепить непреложный цикл устранения дефекта: **RED** (создание воспроизводящего теста и подтверждение его падения) $\to$ **GREEN** (минимальный фикс кода) $\to$ **REFACTOR** (прогон полного набора тестов).
3. **Бесшовная передача в `kb-complete`:** Обучить скилл `.agents/skills/kb-complete/SKILL.md` финализации дефектов с автозаполнением атрибутов frontmatter (`status: fixed`, `fixed_in: "vX.Y.Z"`), перемещением карточки в Канбане, записью в `Devlog.md` и коммитом `fix(...)`.
4. **Актуализация руководства `AGENTS.md`:** Зафиксировать поддержку `/kb-implement <TASK-XXX | BUG-XXX>` в канонических правилах агентов.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `.agents/skills/kb-implement/SKILL.md` — расширить входную маршрутизацию (поддержка `BUG-XXX`), добавить TDD-протокол исправления дефектов.
* `[MODIFY]` `.agents/skills/kb-complete/SKILL.md` — добавить логику завершения дефектов (`status: fixed`, заполнение `fixed_in`, канбан и devlog).
* `[MODIFY]` `AGENTS.md` — обновить описание Режима 3 и принцип Regression-First для поддержки вызова `/kb-implement BUG-XXX`.

---

## 3. Детали реализации

### 3.1. Маршрутизация в `.agents/skills/kb-implement/SKILL.md`
Команда поддерживает полиморфный аргумент:
```text
/kb-implement <TASK-XXX | BUG-XXX>
```
Если передан идентификатор дефекта `BUG-XXX`:
1. **Загрузка контекста:** прочитать `docs/02_Tasks/Bugs/BUG-XXX-*.md`.
2. **Фаза RED:**
   - Найти или создать автоматизированный регрессионный тест (например, в `tests/test_...py`) согласно разделу `## Сценарий воспроизведения` отчета дефекта.
   - Запустить тест и зафиксировать факт падения (Exit Code $\neq$ 0).
3. **Фаза GREEN:**
   - Реализовать минимально достаточные изменения в кодовой базе для исправления дефекта.
   - Повторно запустить регрессионный тест и убедиться в успешном прохождении (Exit Code 0).
4. **Фаза REFACTOR & Verification:**
   - Запустить полный набор тестов проекта: `python -m unittest discover -s tests`.
   - Запустить проверку целостности: `python scripts/kb_lint.py --path docs`.
5. **Финализация:** Автоматически вызвать процедуру завершения дефекта (`kb-complete`).

### 3.2. Логика закрытия дефекта в `.agents/skills/kb-complete/SKILL.md`
При завершении дефекта:
1. **Обновление метаданных:**
   В файле `docs/02_Tasks/Bugs/BUG-XXX-*.md`:
   - `status: fixed`
   - `fixed_in: "<target_release>"` (если `target_release` не пуст, иначе текущая версия из `SPEC.md` / `Roadmap.md`).
   - `updated: YYYY-MM-DD`.
2. **Обновление Канбана:** переместить карточку бага в `## ✅ Готово (Done)` с датой закрытия.
3. **Запись в `Devlog.md`:** зафиксировать факт исправления с сылкой на баг и подтвержденный регрессионный тест.
4. **Git Sync:**
   ```bash
   git add docs/02_Tasks/Bugs/ docs/02_Tasks/Kanban.md docs/Devlog.md <исправленные файлы кода>
   git commit -m "fix(<scope>): resolve BUG-XXX <краткое описание>"
   ```
5. **Stop & Yield Control:** вывести Anti-Echo ответ и завершить работу.

---

## 4. План верификации (Verification Plan)

- [ ] Проверка текста скиллов на соблюдение High-SNR бюджета токенов.
- [ ] Аудит целостности базы знаний:
  ```bash
  python scripts/kb_lint.py --path docs
  ```
  *(Ожидаемый результат: 0 broken links, 0 errors)*.
- [ ] Проверка формулировок терминального шага Stop & Yield в `kb-implement` и `kb-complete`.

---

## 5. Критерии готовности (DoD)

- [ ] Скилл `kb-implement` нативно поддерживает запуск исправления дефекта по TDD.
- [ ] Скилл `kb-complete` корректно проставляет `status: fixed` и `fixed_in`.
- [ ] Руководство `AGENTS.md` синхронизировано.
- [ ] Все пункты Плана верификации пройдены.
