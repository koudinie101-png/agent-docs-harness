---
id: TASK-052
title: "Шаблон Micro-Spec TEMPLATE_TASK_MICRO.md и поддержка Fast-Track в kb-task / kb-plan"
status: done
type: task
phase: 14
component:
  - skills
  - templates
parent_plan: "[[../../Plans/PLAN-014-agile-docs-as-code-and-chat-first-dx|PLAN-014]]"
created: 2026-10-12
updated: 2026-10-12
tags:
  - task/spec
  - phase14
  - fast-track
  - templates
  - skills
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-052 — Шаблон Micro-Spec TEMPLATE_TASK_MICRO.md и поддержка Fast-Track в kb-task / kb-plan

> **ID:** TASK-052 | **Статус:** Выполнено (Режим 3)  
> **План:** [[../../Plans/PLAN-014-agile-docs-as-code-and-chat-first-dx|PLAN-014]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0023-fast-track-protocol-for-micro-tasks|ADR-0023]], [[../../../04_Research/RESEARCH-018-fast-track-protocol-for-micro-tasks|RESEARCH-018]]

---

## 1. Цель задачи
Устранить избыточное бюрократическое трение при оформлении локальных задач ($\le 30$ строк кода) через создание ультра-компактного шаблона микро-спецификации `TEMPLATE_TASK_MICRO.md` (25–35 строк вместо 80+), интеграцию флага `--fast` в скилл `.agents/skills/kb-task/SKILL.md` и внедрение эвристического Soft Nudge в `.agents/skills/kb-plan/SKILL.md` для перенаправления микро-задач в Fast-Track без создания `PLAN-XXX`.

---

## 2. Затрагиваемые файлы
* `[NEW]` `docs/00_Templates/TEMPLATE_TASK_MICRO.md` — эталонный каркас микро-спецификации для базы знаний.
* `[NEW]` `templates/TEMPLATE_TASK_MICRO.md` — дистрибутивная копия шаблона для инсталлятора.
* `[MODIFY]` `.agents/skills/kb-task/SKILL.md` — поддержка флага `--fast`, генерация Micro-Spec, регистрация в Канбане.
* `[MODIFY]` `.agents/skills/kb-plan/SKILL.md` — эвристический префлайт-чек для выявления микро-задач и рекомендация Fast-Track.

---

## 3. Детали реализации

### 3.1. Структура `TEMPLATE_TASK_MICRO.md`
Компактный High-SNR шаблон:
```markdown
---
id: TASK-XXX
title: "[Краткое действие: 3-7 слов]"
status: planned # planned | in-progress | done | cancelled
type: fast-track
phase: 14 # Номер текущей фазы
component:
  - core
parent_plan: "[[../../Plans/PLAN-XXX|PLAN-XXX]]" # Опционально или ссылка на фазовый план
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - task/spec
  - fast-track
kanban: "[[../../Kanban|Канбан-доска]]"
---

# ⚡ Спецификация (Fast-Track): TASK-XXX — [Краткое название]

> **Тип:** Fast-Track (≤ 30 LOC) | **Статус:** К реализации  
> **Канбан:** [[../../Kanban|Канбан-доска]]

---

## 1. Цель и контекст
<!-- 1-2 предложения: что конкретно меняется и зачем -->

## 2. Контракт файлов
* `[MODIFY]` `path/to/file` — <!-- конкретная функция, строка или блок -->

## 3. План верификации (Verification Plan)
- [ ] Верификация: `python -m unittest discover -s tests`
- [ ] Линтер: `python scripts/kb_lint.py --path docs`

## 4. Критерии готовности (DoD)
- [ ] Изменения внесены строго в рамках скоупа (≤ 30 строк кода, ≤ 2 файлов).
- [ ] Все пункты Плана верификации пройдены без ошибок (Exit code 0).
- [ ] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Devlog.
```

### 3.2. Обновление `.agents/skills/kb-task/SKILL.md`
* Добавить поддержку вызова `/kb-task --fast <название>` или распознавание микро-скоупа.
* При флаге `--fast` использовать каркас `TEMPLATE_TASK_MICRO.md` вместо тяжелого `TEMPLATE_TASK.md`.
* Контролировать лимиты: предупреждать, если пользователь запрашивает комплексную переделку архитектуры через `--fast`.

### 3.3. Обновление `.agents/skills/kb-plan/SKILL.md`
* В процедуре `1. Source Discovery & Intent Routing` добавить проверку: если запрос пользователя (`/kb-plan <idea>`) описывает тривиальную правку ($\le 30$ строк кода, 1–2 файла, правка опечатки, параметра или конфига), агент обязан выдать Soft Nudge:
  > 💡 *Данная задача квалифицирована как Fast-Track (≤ 30 LOC). Рекомендуется перейти напрямую к `/kb-task --fast <описание>`, минуя стадию RFC-плана.*

---

## 4. План верификации (Verification Plan)
- [ ] Целостность: `python scripts/kb_lint.py --path docs` (Exit code 0, 0 broken links).
- [ ] Синтаксис скиллов: проверка размера `.agents/skills/kb-task/SKILL.md` и `.agents/skills/kb-plan/SKILL.md` ($\le 3000$ байт).
- [ ] Проверка шаблонов: проверка валидности YAML frontmatter в `TEMPLATE_TASK_MICRO.md`.

---

## 5. Критерии готовности (DoD)
- [ ] Созданы эталонный `docs/00_Templates/TEMPLATE_TASK_MICRO.md` и дистрибутивный `templates/TEMPLATE_TASK_MICRO.md`.
- [ ] В `.agents/skills/kb-task/SKILL.md` добавлена поддержка Fast-Track режима.
- [ ] В `.agents/skills/kb-plan/SKILL.md` добавлен префлайт Soft Nudge для микро-задач.
- [ ] Все пункты Плана верификации пройдены.
