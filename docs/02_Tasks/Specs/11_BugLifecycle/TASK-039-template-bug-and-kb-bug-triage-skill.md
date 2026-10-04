---
id: TASK-039
title: "Рефакторинг TEMPLATE_BUG.md и скилла kb-bug (строгий триаж Режима 2B и терминальный Stop & Yield)"
status: in-progress
type: task
phase: 11
component:
  - templates
  - skills
  - bug-triage
parent_plan: "[[../../Plans/PLAN-011-bug-lifecycle-triage-and-release-targeting|PLAN-011]]"
created: 2026-10-04
updated: 2026-10-04
tags:
  - task/spec
  - phase11
  - bug-triage
  - templates
  - stop-yield
  - guardrails
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-039 — Рефакторинг TEMPLATE_BUG.md и скилла kb-bug

> **ID:** TASK-039  
> **Статус:** К реализации (Режим 2)  
> **Теги:** #task/spec #phase11 #bug-triage #templates #stop-yield #guardrails  
> **Родительский план:** [[../../Plans/PLAN-011-bug-lifecycle-triage-and-release-targeting|PLAN-011]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-014-bug-lifecycle-triage-and-release-targeting|RESEARCH-014]], [[../../../03_Decisions_ADR/ADR-0019-bug-lifecycle-triage-and-release-targeting|ADR-0019]], [[../../../03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Реализовать изолированный входной шлюз обработки дефектов — **Режим 2B (Defect Logging & Interactive Triage)** согласно [[../../../03_Decisions_ADR/ADR-0019-bug-lifecycle-triage-and-release-targeting|ADR-0019]]:
1. **Релизный контракт в шаблоне дефекта:** Оснастить `TEMPLATE_BUG.md` обязательными метаданными релизного таргетинга (`target_release`, `target_phase`, `release_blocker`, `fixed_in`), исключающими неопределенность судьбы бага.
2. **Изоляция триажа в `kb-bug`:** Исключить из `.agents/skills/kb-bug/SKILL.md` любые инструкции по редактированию рабочего кода проекта и выполнению исправлений. Скилл должен заниматься строго регистрацией дефекта, анализом первопричины (RCA), написанием спецификации регрессионного теста и интерактивным триажем.
3. **Терминальный барьер `Stop & Yield Control`:** Закрепить обязательную остановку агента после фиксации отчета в базе знаний и Git-коммита, предотвращая самовольный переход к кодированию без команды разработчика.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `docs/00_Templates/TEMPLATE_BUG.md` — добавить поля релизного контракта в YAML frontmatter и актуализировать структуру документа.
* `[MODIFY]` `templates/TEMPLATE_BUG.md` — синхронизировать эталонный шаблон для генератора инсталлятора.
* `[MODIFY]` `.agents/skills/kb-bug/SKILL.md` — перевести скилл в строгий Режим 2B (триаж, запись, коммит, Stop & Yield), удалить шаги правки исходного кода.

---

## 3. Детали реализации

### 3.1. Релизный контракт в `TEMPLATE_BUG.md`
В YAML frontmatter шаблона `TEMPLATE_BUG.md` добавляются атрибуты таргетинга:
```yaml
---
id: BUG-XXX
title: "[Краткое описание дефекта]"
status: open # open | in-progress | fixed | rejected
severity: medium # low | medium | high | critical
type: bug
target_release: "" # "vX.Y.Z" | "hotfix" | "backlog"
target_phase: null # Номер целевой фазы (например, 11) или null
release_blocker: false # true | false (блокирует ли релиз target_release)
fixed_in: null # Заполняется при закрытии дефекта: "vX.Y.Z"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - bug
  - defect
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---
```

### 3.2. Рефакторинг скилла `.agents/skills/kb-bug/SKILL.md`
1. **Заголовок и статус:**
   `# /kb-bug — Mode 2B: Defect Logging & Interactive Triage`
2. **Ограничения (Constraints):**
   - **READ-ONLY FOR CODE:** Модификация рабочего кода проекта при заведении дефекта СТРОГО ЗАПРЕЩЕНА.
   - **Triage Isolation:** Скилл отвечает исключительно за заведение отчета дефекта, RCA-анализ, фиксацию регрессионного сценария и триаж.
   - **Terminal Stop:** После коммита отчета агент обязан прекратить вызовы инструментов и вернуть управление человеку.
3. **Процедура (Procedure):**
   - **Шаг 1. Определение ID:** сканирование `docs/02_Tasks/Bugs/` $\to$ вычисление следующего `BUG-XXX`.
   - **Шаг 2. Анализ дефекта:** шаги воспроизведения, ожидаемое vs фактическое поведение, Root Cause Analysis (RCA).
   - **Шаг 3. Интерактивный триаж:** определение `severity`, `target_release`, `target_phase`, `release_blocker`. Если пользователь не указал контекст релиза, запросить подтверждение или выставить безопасный дефолт (`backlog`).
   - **Шаг 4. Фиксация артефакта:** создание `docs/02_Tasks/Bugs/BUG-XXX-<slug>.md` по обновленному `TEMPLATE_BUG.md`.
   - **Шаг 5. Обновление Канбана:** добавление карточки дефекта в `## 📥 Бэклог (Backlog)` или `## ⏳ В работе (In Progress)` в `docs/02_Tasks/Kanban.md`.
   - **Шаг 6. Git Sync:**
     ```bash
     git add docs/02_Tasks/Bugs/ docs/02_Tasks/Kanban.md
     git commit -m "docs(bug): record BUG-XXX <slug>"
     ```
   - **Шаг 7. Stop & Yield Control (Терминальный шаг):**
     Вывод Anti-Echo ответа пользователю с интерактивным меню дальнейших действий:
     - Немедленное исправление по TDD: `/kb-implement BUG-XXX`.
     - Назначение в активную фазу роадмапа: включение в текущий спринт.
     - Оставить в бэклоге до востребования.
     **СТРОГО ОСТАНОВИТЬ ВЫЗОВЫ ИНСТРУМЕНТОВ.**

---

## 4. План верификации (Verification Plan)

- [ ] Проверка синтаксиса frontmatter шаблона `TEMPLATE_BUG.md` и `templates/TEMPLATE_BUG.md`.
- [ ] Аудит целостности базы знаний:
  ```bash
  python scripts/kb_lint.py --path docs
  ```
  *(Ожидаемый результат: 0 broken links, 0 errors)*.
- [ ] Проверка отсутствия директив изменения кода в `kb-bug/SKILL.md`.

---

## 5. Критерии готовности (DoD)

- [ ] Шаблоны `docs/00_Templates/TEMPLATE_BUG.md` и `templates/TEMPLATE_BUG.md` обновлены релизным контрактом.
- [ ] Скилл `.agents/skills/kb-bug/SKILL.md` рефакторен в чистый Режим 2B с шагом Stop & Yield.
- [ ] Все пункты Плана верификации выполнены.
- [ ] Статус задачи обновлен в ТЗ, Канбане и Дорожной карте.
