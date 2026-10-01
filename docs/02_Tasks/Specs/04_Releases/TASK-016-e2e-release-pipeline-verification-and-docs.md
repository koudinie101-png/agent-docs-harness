---
id: TASK-016
title: "Комплексное E2E тестирование релизного пайплайна и обновление документации"
status: planned
type: task
phase: 4
component:
  - testing
  - e2e
  - documentation
  - onboarding
parent_plan: "[[../../Plans/PLAN-004-release-management-and-lifecycle-automation|PLAN-004]]"
created: 2026-10-01
updated: 2026-10-01
tags:
  - task/spec
  - phase4
  - component/testing
  - component/e2e
  - component/documentation
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-016 — Комплексное E2E тестирование релизного пайплайна и документация

> **ID:** TASK-016  
> **Статус:** К реализации (Режим 2)  
> **Теги:** #task/spec #phase4 #component/testing #component/e2e #component/documentation  
> **Родительский план:** [[../../Plans/PLAN-004-release-management-and-lifecycle-automation|PLAN-004]]  
> **Связанные ADR:** [[../../../03_Decisions_ADR/ADR-0007-release-management-dual-mode-and-build-hook|ADR-0007]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

1. Написать сквозные E2E тесты в `tests/test_installer.py`, верифицирующие корректность работы всех компонентов Фазы 4:
   - Развертывание каталога `docs/02_Tasks/Releases/` и шаблона `TEMPLATE_RELEASE.md` в чистых проектах.
   - Развертывание 12-го скилла `.agents/skills/kb-release/`.
   - Развертывание утилиты `scripts/kb_release.py`.
   - Проверка процедуры обновления (`install.py --update`): проверка обновления скиллов и сохранения пользовательских релизных заметок.
   - Интеграционный тест утилиты `scripts/kb_release.py` в изолированной песочнице: генерация релиза, расчет SHA-256 артефакта в `dist/` и аудит через `kb_lint.py`.
2. Обновить документацию проекта:
   - `README.md`: документирование команды `/kb-release`, структуры релизов и принципа Dual-Mode.
   - `docs/Onboarding.md`: добавление раздела о релиз-менеджменте, Build Hook Contract и актуализация списка 12 скиллов.
   - `docs/00_Index.md`: добавление ссылок на раздел `02_Tasks/Releases/`, `TEMPLATE_RELEASE.md`, `RESEARCH-002` и `ADR-0007`.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `tests/test_installer.py` — новые тесты на развертывание, обновление и сквозную работу релизных утилит.
* `[MODIFY]` `README.md` — актуализация таблицы скиллов и сценария публикации релизов.
* `[MODIFY]` `docs/Onboarding.md` — раздел «Релиз-менеджмент» и обновленная карта скиллов.
* `[MODIFY]` `docs/00_Index.md` — актуализация карты разделов (MOC) и списка шаблонов.

---

## 3. Детали технической реализации

### 3.1. E2E Тесты в `tests/test_installer.py`

```python
def test_release_components_deployed_on_fresh_install(self):
    """Проверяет развертывание TEMPLATE_RELEASE.md, Releases/ и kb-release."""
    pass

def test_kb_release_utility_execution_in_sandbox(self):
    """Создает фиктивный dist/test.zip, вызывает kb_release.py и проверяет генерацию RELEASE-v1.0.0.md."""
    pass

def test_update_preserves_existing_releases(self):
    """Проверяет, что install.py --update не перезаписывает существующие релизные файлы."""
    pass
```

### 3.2. Обновление документации

1. **`README.md`:**
   - Добавление команды `/kb-release` в сводную таблицу скиллов.
   - Описание архитектуры Dual-Mode (GitHub vs Local-Only).
2. **`docs/Onboarding.md`:**
   - Новый раздел: `### 🚀 Релиз-менеджмент (/kb-release)`.
   - Описание Pre-flight проверок, контракта сборщика и формата релизного файла.
3. **`docs/00_Index.md`:**
   - Добавление ссылки на `02_Tasks/Releases/` и `TEMPLATE_RELEASE.md`.

---

## 4. План верификации (Verification Plan)

### Автоматические тесты:
- [ ] Полный прогон тестового набора:
  ```bash
  python -m unittest discover -s tests
  ```
  *(Ожидаемый результат: все тесты зеленые, 100% pass)*

### Целостность базы знаний:
- [ ] Запуск линтера Docs-as-Code:
  ```bash
  python scripts/kb_lint.py --path docs
  ```
  *(Ожидаемый результат: 0 broken wikilinks, 100% валидный frontmatter)*

---

## 5. Критерии готовности (Definition of Done)

- [ ] Все E2E сценарии в `tests/test_installer.py` успешно выполняются.
- [ ] Документация `README.md`, `docs/Onboarding.md` и `docs/00_Index.md` синхронизирована с новым функционалом.
- [ ] Линтер `kb_lint.py` не обнаруживает ни одной битой ссылки.
- [ ] В `Kanban.md` и `Roadmap.md` все задачи Фазы 4 полностью связаны с ТЗ.
