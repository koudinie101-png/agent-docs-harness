---
id: TASK-011
title: "Механизм бережного обновления инфраструктуры базы знаний (install.py --update)"
status: done
type: task
phase: 3
component:
  - installer
  - lifecycle
  - update
parent_plan: "[[../../Plans/PLAN-003-brownfield-adoption-and-lifecycle|PLAN-003]]"
created: 2026-10-01
updated: 2026-10-01
tags:
  - task/spec
  - phase3
  - component/installer
  - component/lifecycle
  - component/update
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-011 — Механизм бережного обновления инфраструктуры (`install.py --update`)

> **ID:** TASK-011  
> **Статус:** Выполнено (Режим 3)  
> **Теги:** #task/spec #phase3 #component/installer #component/lifecycle #component/update  
> **Родительский план:** [[../../Plans/PLAN-003-brownfield-adoption-and-lifecycle|PLAN-003]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Реализовать команду безопасного обновления инфраструктуры Docs-as-Code в существующих проектах (`install.py --update` или `python install.py -u`):
1. Обеспечить обновление статических шаблонов (`docs/00_Templates/*`), линтера (`scripts/kb_lint.py`), исполняемых скиллов (`.agents/skills/*`) и цветовой схемы графа (`.obsidian/graph.json`) до актуальных версий дистрибутива.
2. Гарантировать полную неприкосновенность пользовательских данных: `02_Tasks/*` (Kanban, Roadmap, планы, ТЗ, баги), `03_Decisions_ADR/*`, `04_Research/*`, `05_Testing/*`, `Devlog.md`, `SPEC.md`, `00_Index.md`.
3. При обновлении файлов правил (`AGENTS.md`, `GEMINI.md`, `.clinerules` и др.) создавать резервную копию `*.bak`, если файл был модифицирован пользователем.
4. Автоматически регистрировать факт обновления в `docs/Devlog.md` и запускать контрольную валидацию через `kb_lint.py`.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `install.py`:
  * Добавление аргумента командной строки `--update` / `-u`.
  * Реализация функции `update_harness(target_dir: Path, assets: dict, doc_lang: str)`.
  * Проверка валидности проекта перед обновлением (наличие `docs/` и `docs/00_Index.md`).
  * Резервное копирование правил в `*.bak`.
  * Добавление автоматической записи в `docs/Devlog.md` об успешном обновлении версии.
* `[MODIFY]` `tests/test_installer.py`:
  * Тест обновления устаревших шаблонов и линтера в существующем проекте.
  * Тест сохранения пользовательских задач, записей в Kanban и Devlog при вызове `--update`.
  * Тест создания `.bak` для кастомизированного `AGENTS.md`.

---

## 3. Детали технической реализации

### 3.1. Разделение файлов при обновлении
| Категория | Путь | Действие при `--update` |
|---|---|---|
| **Шаблоны** | `docs/00_Templates/*` | Перезапись актуальными версиями из бандла |
| **Скрипты** | `scripts/kb_lint.py` | Перезапись актуальной версией линтера |
| **Скиллы** | `.agents/skills/*` | Перезапись актуальными `SKILL.md` |
| **Граф Obsidian** | `docs/.obsidian/graph.json` | Обновление цветовой палитры |
| **Правила агентов** | `AGENTS.md`, `GEMINI.md`, etc. | Создание `.bak`, если файл отличается от эталона, затем обновление |
| **Пользовательские данные** | `02_Tasks/`, `03_Decisions_ADR/`, `04_Research/`, `05_Testing/`, `SPEC.md`, `00_Index.md` | **СТРОГИЙ ЗАПРЕТ НА ИЗМЕНЕНИЕ** |
| **Журнал Devlog** | `docs/Devlog.md` | Добавление новой записи в начало истории (append) |

### 3.2. Сигнатура и логика `update_harness`
```python
def update_harness(target_dir: Path, assets: dict, doc_lang: str = "ru") -> int:
    docs_dir = target_dir / "docs"
    if not (docs_dir / "00_Index.md").is_file():
        print(f"❌ docs/00_Index.md not found in {target_dir}. Is this an Agent Docs-as-Code project?")
        return 1

    print(f"🔄 Updating Agent Docs-as-Code Harness components in: {target_dir}")
    
    # 1. Update templates
    deploy_templates(target_dir, assets)
    # 2. Update linter
    deploy_linter(target_dir, assets)
    # 3. Update skills
    deploy_skills(target_dir, assets)
    # 4. Update agent rules with .bak protection
    update_agent_rules_safe(target_dir, doc_lang)
    # 5. Append update record to Devlog.md
    record_devlog_update(docs_dir)
    # 6. Run verification
    run_linter_audit(docs_dir)
    return 0
```

---

## 4. План верификации (Verification Plan)

### Сборка и синтаксис:
- [x] Проверка синтаксиса: `python -m py_compile install.py` (Exit code 0).
- [x] Сборка через `python scripts/build_installer.py` (Exit code 0, размер < 82 КБ).

### Автоматические тесты:
- [x] Развертывание тестового проекта с кастомными задачами и пользовательскими изменениями в `AGENTS.md`.
- [x] Запуск `python install.py --update --dir <test_dir>`.
- [x] Проверка:
  - Шаблоны `00_Templates` и линтер `kb_lint.py` обновлены.
  - Пользовательские задачи `TASK-999` и записи в `Kanban.md` остались нетронутыми.
  - Создан файл `AGENTS.md.bak` с оригинальными правками пользователя.
  - В `Devlog.md` появилась отметка об обновлении компонентов.
  - `kb_lint.py` завершился с кодом 0.

---

## 5. Критерии готовности (Definition of Done)

- [x] Флаг `--update` доступен в CLI и корректно валидирует целевой каталог.
- [x] Шаблоны, линтер и скиллы обновляются до актуальных версий.
- [x] Пользовательские задачи, решения, исследования и журнал защищены от затирания.
- [x] Резервная копия правил создается автоматически при обнаружении модификаций.
- [x] Все тесты в `tests/test_installer.py` зеленые.
