---
id: TASK-XXX
title: "[Краткое название задачи]"
status: planned # planned | in-progress | done | cancelled
type: task
phase: 1
track: standard # micro | standard | deep
component:
  - core
parent_plan: "[[../../Plans/PLAN-XXX|PLAN-XXX]]"
# depends_on: [] # list of TASK-XXX IDs that must be completed first
created: 2026-09-19
updated: 2026-09-19
tags:
  - task/spec
  - phase1
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-XXX — [Краткое название]

> **ID:** TASK-XXX | **Статус:** [К реализации | В работе | Выполнено]  
> **План:** [[../../Plans/PLAN-XXX|PLAN-XXX]] | **Канбан:** [[../../Kanban|Канбан]]  

---

## 0. Чек-лист качества ТЗ (Spec Quality Checklist)
- [ ] Требования однозначны и не содержат недосказанностей
- [ ] Нет неразрешённых маркеров `[NEEDS CLARIFICATION: ...]`
- [ ] Скоуп символов локализован (`[MODIFY]`/`[NEW]`/`[DELETE]`) без номеров строк (ADR-0029)
- [ ] Критерии приёмки (DoD) проверяемы автоматизированно
<!-- При наличии неясностей запрещено угадывать — ставьте маркер: [NEEDS CLARIFICATION: вопрос A vs B] -->

## 1. Цель задачи
<!-- Техническое назначение задачи и решаемая проблема -->

## 2. Затрагиваемые файлы и скоуп символов
* `[MODIFY]` `path/to/file.ext`:
  - `ClassName.method_name()` — <!-- суть изменения и сигнатура -->
* `[NEW]` `path/to/new_file.ext`:
  - `function_name(arg: Type) -> Ret` — <!-- контракт нового символа -->
* `[DELETE]` `path/to/file.ext` — <!-- причина удаления -->
<!-- Символы, без номеров строк (ADR-0029) -->

## 3. Детали реализации
<!-- Сигнатуры интерфейсов, структуры данных, обработка ошибок -->

```python
# Ключевой контракт
```

## 4. План верификации (Verification Plan)
- [ ] Сборка: `<!-- команда сборки, Exit code 0 -->`
- [ ] Автотесты: `<!-- команда запуска тестов, 100% pass -->`
- [ ] Проверка: `<!-- шаг ручной/интеграционной проверки -->`

### Visual DoD (для задач с GUI/TUI):
- [ ] Фиксация скриншота: `docs/assets/screenshots/<target>/TASK-XXX.png` (лимит $\le 2\text{ MB}$).
- [ ] *Headless/CLI Fallback (при отсутствии дисплея):* макет в `docs/assets/mockups/<target>/TASK-XXX/tobe.svg` (`asis.svg`) и слот в отчете:  
  `![Скриншот](../../assets/screenshots/<target>/TASK-XXX.png) <!-- Вставьте скриншот через Ctrl+V в Obsidian -->`

* **Замеры $\ge 3$ прогонов (без холодного старта):** фиксировать команду, среду и среднее ($\bar{X}$).

## 5. Критерии готовности (DoD)
- [ ] Код написан строго по ТЗ без заглушек.
- [ ] Все пункты Плана верификации пройдены.
- [ ] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [ ] Запись добавлена в `Devlog.md`.
