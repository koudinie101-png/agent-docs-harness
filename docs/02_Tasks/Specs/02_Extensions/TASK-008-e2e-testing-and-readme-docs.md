---
id: TASK-008
title: "Сквозное E2E тестирование в tests/test_installer.py и документация README.md"
status: planned
type: task
phase: 2
component:
  - tests
  - documentation
parent_plan: "[[../../Plans/PLAN-002-full-skills-and-agent-rules-integration|PLAN-002]]"
created: 2026-09-30
updated: 2026-09-30
tags:
  - task/spec
  - phase2
  - component/tests
  - component/documentation
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-008 — Сквозное E2E тестирование в test_installer.py и документация README.md

> **ID:** TASK-008  
> **Статус:** К реализации (Режим 2)  
> **Теги:** #task/spec #component/tests #component/documentation  
> **Родительский план:** [[../../Plans/PLAN-002-full-skills-and-agent-rules-integration|PLAN-002]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

1. Расширить тестовый набор `tests/test_installer.py` новыми автоматическими сквозными E2E тестами для проверки всех нововведений Фазы 2:
   - Развертывание каталога `.agents/skills/` со всеми 11 скиллами и их валидность.
   - Корректность генерации `GEMINI.md` и `.windsurfrules`.
   - Проверка языковой параметризации `--doc-lang`.
   - Проверка запуска встроенного линтера `kb_lint.py` в созданных проектах.
2. Актуализировать документацию `README.md`:
   - Описание развертывания 11 скиллов.
   - Описание поддержки Antigravity (`GEMINI.md`), Windsurf (`.windsurfrules`) и открытых моделей (Qwen 2.5 Coder, DeepSeek).
   - Описание флага `--doc-lang` и мультиязычного мастера.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `tests/test_installer.py` — добавление новых модульных и интеграционных E2E тестов.
* `[MODIFY]` `README.md` — актуализация документации репозитория.

---

## 3. Детали технической реализации

### 3.1. Тесты в `tests/test_installer.py`:
* `test_install_deploys_all_11_skills`:
  - Установка в изолированный `tempfile.TemporaryDirectory`.
  - Проверка существования каталога `.agents/skills/`.
  - Проверка наличия всех 11 скиллов (`docs-as-code`, `kb-plan`, `kb-task`, `kb-implement`, `kb-complete`, `kb-bug`, `kb-adr`, `kb-research`, `kb-lint`, `kb-onboard`, `kb-init`) и непустых файлов `SKILL.md`.
* `test_install_gemini_and_windsurf_rules`:
  - Проверка создания `GEMINI.md` при `--agent all` и `--agent gemini`.
  - Проверка создания `.windsurfrules` при `--agent all` и `--agent windsurf`.
* `test_install_doc_lang_parameter`:
  - Проверка установки с `--doc-lang ru` и `--doc-lang en`.
  - Проверка наличия соответствующих языковых директив в `AGENTS.md` и `GEMINI.md`.

### 3.2. Документация `README.md`:
* Обновление схемы каталогов с отображением `.agents/skills/` и `GEMINI.md`.
* Таблица скиллов и команд `/kb-*`.
* Описание флага `--doc-lang`.
* Рекомендации по использованию с Google Antigravity, VS Code Cline, Cursor и локальным Qwen 2.5 Coder.

---

## 4. План верификации (Verification Plan)

### Сборка и тесты:
- [ ] Запуск полного набора автотестов: `python -m unittest discover -s tests` (все тесты зеленые, 100% pass).
- [ ] Проверка базы знаний линтером: `python scripts/kb_lint.py --path docs` (0 битых ссылок).
- [ ] Проверка целостности ссылок в `README.md`.

---

## 5. Критерии готовности (Definition of Done)

- [ ] Все новые тесты добавлены в `tests/test_installer.py` и успешно выполняются.
- [ ] `README.md` полностью отражает возможности инсталлятора Фазы 2.
- [ ] `kb_lint.py` подтверждает 0 ошибок и битых ссылок.
- [ ] Карточка задачи переведена в `Kanban.md` в Done, отмечен Roadmap, сделана запись в `Devlog.md`.
