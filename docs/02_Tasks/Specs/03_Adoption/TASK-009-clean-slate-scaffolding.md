---
id: TASK-009
title: "Чистый старт и устранение фантомных задач при новой установке (Clean Slate Scaffolding)"
status: in-progress
type: task
phase: 3
component:
  - installer
  - scaffolding
  - kanban
parent_plan: "[[../../Plans/PLAN-003-brownfield-adoption-and-lifecycle|PLAN-003]]"
created: 2026-10-01
updated: 2026-10-01
tags:
  - task/spec
  - phase3
  - component/installer
  - component/scaffolding
  - component/kanban
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-009 — Clean Slate Scaffolding & Zero-Broken-Links FTUE

> **ID:** TASK-009  
> **Статус:** В работе (Режим 2)  
> **Теги:** #task/spec #phase3 #component/installer #component/scaffolding #component/kanban  
> **Родительский план:** [[../../Plans/PLAN-003-brownfield-adoption-and-lifecycle|PLAN-003]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Устранить генерацию фиктивных ссылок на несуществующие файлы `PLAN-001` и `TASK-001` при первоначальном развертывании харнесса в `install.py`:
1. Обеспечить кристально чистый бэклог в сгенерированном `Kanban.md` без чужих шаблонных задач.
2. В `Roadmap.md` генерировать каркас Фазы 1 без битых вики-ссылок, готовый к наполнению через `/kb-plan`.
3. Гарантировать, что запуск `python scripts/kb_lint.py --path docs` в свежесозданном проекте сразу завершается со статусом 0 (0 broken links, 100% валидный frontmatter).
4. Обновить тесты в `tests/test_installer.py` для фиксации чистого бэклога и отсутствия битых ссылок.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `install.py` — модификация функции `create_starter_docs`:
  * Формирование чистого `Kanban.md` без ссылок на несуществующие `PLAN-001` и `TASK-001`.
  * Формирование `Roadmap.md` с валидной структурой без фантомных ссылок.
  * Добавление информативного комментария/приглашения в колонку `Backlog`.
* `[MODIFY]` `tests/test_installer.py` — добавление проверок содержимого `Kanban.md` и `Roadmap.md` на отсутствие ссылок на несуществующие файлы и прохождение `kb_lint.py`.

---

## 3. Детали технической реализации

### 3.1. Генерация стартового `Kanban.md`
В функции `create_starter_docs` в `install.py`:
```markdown
---
kanban-plugin: basic
---

# 📋 Канбан-доска: {project_name}

> **Теги:** #tasks #kanban #planning  
> **Связанная дорожная карта:** [[Roadmap|Дорожная карта]]  

## 📥 Бэклог (Backlog)

<!-- Создайте ваш первый план через slash-команду агента /kb-plan <название> -->

## ⏳ В работе (In Progress)


## ✅ Готово (Done)

- [x] Инициализация структуры базы знаний Docs-as-Code ({today_str}) #docs

## 💡 Идеи и гипотезы (Icebox / Future Ideas)

- [ ] [Идея 1]: краткая формулировка задумки или гипотезы #idea
```

### 3.2. Генерация стартового `Roadmap.md`
В функции `create_starter_docs` в `install.py`:
```markdown
---
id: ROADMAP
title: Дорожная карта разработки (Roadmap)
status: active
type: roadmap
created: {today_str}
updated: {today_str}
tags:
  - roadmap
  - planning
  - milestones
---

# 🗺️ Дорожная карта разработки (Roadmap): {project_name}

> **Теги:** #roadmap #planning #milestones  
> **Связанный канбан:** [[Kanban|Канбан-доска]]  
> **Первоисточник:** [[../../SPEC|SPEC.md (Мастер-спецификация)]]  

---

## Фаза 1: Первичный MVP и проверка сборки
**Цель:** Развернуть базовую кодовую базу и подтвердить работоспособность окружения.  
*Сформируйте план первой фазы через команду `/kb-plan`.*

---

## 🔮 Перспективные направления (Future Horizons / Icebox)
*Идеи и гипотезы для будущих фаз проекта.*

* 💡 [Идея 1]: первоначальная гипотеза развития продукта.
```

---

## 4. План верификации (Verification Plan)

### Сборка и синтаксис:
- [ ] Проверка синтаксиса `install.py`: `python -m py_compile install.py` (Exit code 0).
- [ ] Сборка инсталлятора через `python scripts/build_installer.py` (Exit code 0, размер < 82 КБ).

### Автоматические тесты:
- [ ] Запуск `python -m unittest discover -s tests` (все тесты зеленые).
- [ ] Проверка `test_installer.py`: убедиться, что свежеразвернутый проект не содержит в `Kanban.md` ссылок на `PLAN-001-initial-mvp-setup` и `TASK-001-project-scaffolding`.
- [ ] Проверка `kb_lint.py`: автоматический аудит развернутого тестового каталога подтверждает 0 broken links.

---

## 5. Критерии готовности (Definition of Done)

- [ ] В `create_starter_docs` полностью исключены фантомные ссылки на несуществующие файлы планов и задач.
- [ ] `Kanban.md` и `Roadmap.md` содержат чистые, интуитивно понятные стартовые разделы.
- [ ] Линтер `kb_lint.py` при первой установке отрабатывает без единого предупреждения.
- [ ] Все существующие и новые unit-тесты успешно проходят.
- [ ] Статус задачи обновлен в `docs/02_Tasks/Kanban.md` и `docs/02_Tasks/Roadmap.md`.
