---
id: TASK-060
title: "Синхронизация инсталлятора install.py / build_installer.py, регрессионные E2E тесты и актуализация Living Spec"
status: completed
type: task
phase: 15
component:
  - installer
  - builder
  - e2e-tests
  - living-spec
parent_plan: "[[../../Plans/PLAN-015-response-latency-and-channel-transparency|PLAN-015]]"
created: 2026-10-12
updated: 2026-10-12
tags:
  - task/spec
  - phase15
  - installer
  - e2e
  - living-spec
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-060 — Синхронизация инсталлятора install.py / build_installer.py, регрессионные E2E тесты и актуализация Living Spec

> **ID:** TASK-060 | **Статус:** Выполнено  
> **План:** [[../../Plans/PLAN-015-response-latency-and-channel-transparency|PLAN-015]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Обоснование:** [[../../../04_Research/RESEARCH-008-latency-prompt-caching-and-skill-chaining|RESEARCH-008]], [[../../../04_Research/RESEARCH-019-user-centric-ingestion-and-channel-transparency|RESEARCH-019]]  
> **Решения (ADR):** [[../../../03_Decisions_ADR/ADR-0013-zero-roundtrip-dispatch-and-hot-invariants-architecture|ADR-0013]], [[../../../03_Decisions_ADR/ADR-0024-user-centric-ingestion-and-channel-transparency|ADR-0024]]  

---

## 1. Цель задачи

1. **Сборка монолитных дистрибутивов `install.py` и `dist/install.py`:**  
   Пересобрать и синхронизировать установщик через `scripts/build_installer.py`, упаковав обновленные утилиты `scripts/kb_ingest.py` (автодетект Git Remote, `--status`, `--label`, `--all-open`), `scripts/kb_lint.py` (семантический контроль фаз `check_phase_consistency`) и обновленный скилл `.agents/skills/kb-triage/SKILL.md`.
2. **Сквозные E2E регрессионные тесты (`tests/test_installer.py`):**  
   Разработать интеграционный тест `test_29_channel_transparency_and_phase_consistency_deployment`, проверяющий корректность развертывания новых возможностей инжеста и линтера во временном каталоге, а также работоспособность режима обновления существующей кодовой базы `install.py --update`.
3. **Синхронизация Living Spec (Мастер-Спецификации и витрины):**  
   Актуализировать документацию проекта:
   - `SPEC.md` — зафиксировать архитектуру Zero Round-Trip Dispatch (Правило 10), CLI-контракты `kb_ingest.py` (`--status`, `--label`, `--all-open`, `detect_github_repo`) и функцию `check_phase_consistency` в `kb_lint.py`.
   - `README.md` — обновить витрину новыми возможностями сбора фидбека и дашборда статуса.
   - `docs/Onboarding.md` — актуализировать справочник команд и руководство по настройке каналов обратной связи.
4. **Завершение Фазы 15:**  
   Перевести статус Фазы 15 в Дорожной карте в выполненное состояние после успешного прогона всех проверок.

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `install.py` — монолитный инсталлятор (актуализация запакованных ассетов).
* `[MODIFY]` `dist/install.py` — публичный дистрибутив пакета.
* `[MODIFY]` `tests/test_installer.py` — сквозной тест `test_29_channel_transparency_and_phase_consistency_deployment`.
* `[MODIFY]` `SPEC.md` — обновление Мастер-Спецификации (Ground Truth).
* `[MODIFY]` `README.md` — обновление витрины проекта.
* `[MODIFY]` `docs/Onboarding.md` — актуализация онбординг-руководства.
* `[MODIFY]` `docs/02_Tasks/Kanban.md` — закрытие карточки задачи и всей Фазы 15.
* `[MODIFY]` `docs/02_Tasks/Roadmap.md` — отметка завершения задачи и фазы.

---

## 3. Детали реализации

### 3.1. Сборка через `scripts/build_installer.py`
- Запуск сборщика: `python scripts/build_installer.py`.
- Сборщик упаковывает актуальные версии скриптов (`kb_lint.py`, `kb_release.py`, `kb_ingest.py`), шаблонов и скиллов в сжатый payload внутри `install.py` и `dist/install.py`.
- Проверка размера монолита и валидности синтаксиса `py_compile`.

### 3.2. E2E Тест в `tests/test_installer.py`
Реализация теста `test_29_channel_transparency_and_phase_consistency_deployment`:
```python
def test_29_channel_transparency_and_phase_consistency_deployment(self):
    """E2E test verifying deployment and --update for channel transparency and phase consistency."""
    # 1. Запуск install.py в изолированной temp-директории
    # 2. Проверка распаковки scripts/kb_ingest.py с функцией detect_github_repo и аргументом --status
    # 3. Проверка запуска python scripts/kb_ingest.py --status в развернутом каталоге
    # 4. Проверка распаковки scripts/kb_lint.py с функцией check_phase_consistency
    # 5. Проверка успешного обновления существующего хранилища через install.py --update
```

### 3.3. Актуализация Living Spec (`SPEC.md`, `README.md`, `docs/Onboarding.md`)
- В `SPEC.md`:
  - Добавить пункт в раздел архитектурных правил о Zero Round-Trip Dispatch (Hot Invariants Protocol).
  - Описать сигнатуры `detect_github_repo`, параметры `--status`, `--label`, `--all-open` утилиты `scripts/kb_ingest.py`.
  - Описать алгоритм семантической проверки `check_phase_consistency` в `scripts/kb_lint.py`.
- В `README.md`:
  - Добавить описание команды `python scripts/kb_ingest.py --status` в раздел каналов обратной связи.
- В `docs/Onboarding.md`:
  - Актуализировать таблицу утилит и регламент триажа `/kb-triage`.

---

## 4. План верификации (Verification Plan)

- [x] Сборка инсталлятора: `python scripts/build_installer.py` (Exit code 0)
- [x] Синтаксическая корректность: `python -m py_compile install.py dist/install.py` (Exit code 0)
- [x] E2E тесты инсталлятора: `python -m unittest tests/test_installer.py` (100% Pass, Exit code 0)
- [x] Полный регрессионный сьют проекта: `python -m unittest discover -s tests` (100% Pass, Exit code 0)
- [x] Аудит базы знаний: `python scripts/kb_lint.py --path docs` (Exit code 0, 0 broken links, 0 warnings)

---

## 5. Критерии готовности (DoD)

- [x] Артефакты `install.py` и `dist/install.py` пересобраны и содержат весь функционал Фазы 15.
- [x] Разработан и успешно проходит сквозной тест `test_29`.
- [x] Файлы `SPEC.md`, `README.md` и `docs/Onboarding.md` полностью синхронизированы без документационного дрифта.
- [x] Все пункты Плана верификации пройдены.
- [x] Статус задачи обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`). Завершена Фаза 15!
- [x] Запись добавлена в `Devlog.md`.
