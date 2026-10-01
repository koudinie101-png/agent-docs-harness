---
id: TASK-010
title: "Бесшовное внедрение в существующие проекты (Brownfield Adoption) и автодетект стека"
status: planned
type: task
phase: 3
component:
  - installer
  - brownfield
  - heuristics
parent_plan: "[[../../Plans/PLAN-003-brownfield-adoption-and-lifecycle|PLAN-003]]"
created: 2026-10-01
updated: 2026-10-01
tags:
  - task/spec
  - phase3
  - component/installer
  - component/brownfield
  - component/heuristics
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-010 — Brownfield Adoption, Smart Stack Autodetection & Legacy Audit Guidance

> **ID:** TASK-010  
> **Статус:** К реализации (Режим 2)  
> **Теги:** #task/spec #phase3 #component/installer #component/brownfield #component/heuristics  
> **Родительский план:** [[../../Plans/PLAN-003-brownfield-adoption-and-lifecycle|PLAN-003]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Обеспечить безопасное и интеллектуальное внедрение харнесса Docs-as-Code в существующие репозитории (Brownfield Projects):
1. Реализовать эвристическое автоопределение технологического стека проекта (`detect_project_stack`).
2. Предотвратить повреждение и перезапись существующих файлов проекта (`README.md`, `.gitignore`, `SPEC.md`).
3. Добавить в `Onboarding.md` подробный сценарий для агента по проведению экспресс-аудита существующей кодовой базы (Brownfield Audit Workflow).
4. Поддержать флаг `--stack auto` (по умолчанию, если стек не передан явно) и автоматический выбор варианта по умолчанию в интерактивном мастере.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `install.py`:
  * Добавление функции `detect_project_stack(target_dir: Path) -> str`.
  * Интеграция автоопределения в CLI аргументы (дефолт `auto`) и интерактивный мастер.
  * Безопасная обработка существующего `README.md` (дописывание раздела с Docs-as-Code вместо слепой перезаписи).
  * Безопасная обработка `.gitignore` (append-only добавление исключений `.obsidian/*`, кроме `graph.json`).
  * Добавление раздела «Brownfield Onboarding: Экспресс-аудит проекта» в генерируемый `Onboarding.md`.
* `[MODIFY]` `tests/test_installer.py`:
  * Тест детекта стеков: Swift (`Package.swift`), Web (`package.json`), Python (`pyproject.toml`), .NET (`*.sln`), Generic (`Cargo.toml`).
  * Тест сохранения содержимого существующего `README.md`.
  * Тест корректного дополнения существующего `.gitignore`.

---

## 3. Детали технической реализации

### 3.1. Функция `detect_project_stack(target_dir: Path) -> str`
```python
def detect_project_stack(target_dir: Path) -> str:
    """
    Эвристический детект стека по маркерным файлам в корне проекта.
    Возвращает ключ стека из STACK_PRESETS ('swift', 'web', 'python', 'dotnet', 'generic').
    """
    if (target_dir / "Package.swift").is_file():
        return "swift"
    if (target_dir / "package.json").is_file():
        return "web"
    if any((target_dir / f).is_file() for f in ["pyproject.toml", "requirements.txt", "Pipfile", "setup.py"]):
        return "python"
    if list(target_dir.glob("*.sln")) or list(target_dir.glob("*.csproj")):
        return "dotnet"
    return "generic"
```

### 3.2. Неразрушающая обработка `README.md`
Если `target_dir / "README.md"` уже существует:
1. Исходное содержимое пользователя сохраняется.
2. Проверяется наличие маркера `## 🧠 База знаний Docs-as-Code` или `AGENTS.md`.
3. Если маркер отсутствует, в конец файла дописывается компактный блок:
```markdown

---

## 🧠 Документация и дисциплина AI-агентов (Docs-as-Code)
В проекте развернута база знаний Docs-as-Code и строгий 3-режимный регламент работы с AI-агентами:
* **Каталог документации:** `docs/` (открывается как Vault в Obsidian).
* **Главный регламент агентов:** [AGENTS.md](AGENTS.md).
* **Карта заметок:** [docs/00_Index.md](docs/00_Index.md).
* **Проверка базы знаний:** `python scripts/kb_lint.py --path docs`.
```

### 3.3. Раздел «Brownfield Audit» в `Onboarding.md`
В шаблон онбординга добавляется инструкция для первого обращения к агенту в существующем проекте:
> **Первый шаг в существующем проекте (Brownfield):**  
> Обратитесь к агенту с запросом:  
> *«Изучи кодовую базу репозитория, составь краткий архитектурный обзор в `docs/01_Architecture/` и заполни мастер-спецификацию `SPEC.md` ключевыми компонентами и целями проекта»*.

---

## 4. План верификации (Verification Plan)

### Сборка и синтаксис:
- [ ] Проверка синтаксиса `install.py`: `python -m py_compile install.py` (Exit code 0).
- [ ] Сборка инсталлятора через `python scripts/build_installer.py` (Exit code 0).

### Автоматические тесты:
- [ ] Тестирование детектора стека на фиктивных директориях с маркерными файлами (все 5 стеков корректно распознаются).
- [ ] Тестирование сохранения существующего `README.md`: в тестовой песочнице создается `README.md` с уникальным текстом пользователя; после запуска `install.py` уникальный текст сохраняется, а в конец файла добавлен блок Docs-as-Code.
- [ ] Тестирование дополнения `.gitignore`: существующие правила пользователя не удаляются, новые правила аккуратно дописываются.

---

## 5. Критерии готовности (Definition of Done)

- [ ] Инсталлятор автоматически распознает технологический стек при установке в существующие каталоги.
- [ ] Существующий `README.md` и `.gitignore` не затираются, данные пользователя защищены от потери.
- [ ] В `Onboarding.md` включен сценарий первичного аудита для агента.
- [ ] Все тесты в `tests/test_installer.py` завершаются успешно.
