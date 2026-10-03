---
id: TASK-038
title: "Синхронизация инсталлятора, сквозные E2E тесты и актуализация документации"
status: done
type: task
phase: 10
component:
  - installer
  - bundling
  - e2e
  - docs
parent_plan: "[[../../Plans/PLAN-010-spec-genesis-and-high-snr-release-notes|PLAN-010]]"
created: 2026-10-03
updated: 2026-10-03
tags:
  - task/spec
  - phase10
  - installer
  - bundling
  - e2e
  - docs
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-038 — Синхронизация инсталлятора, сквозные E2E тесты и документация

> **ID:** TASK-038  
> **Статус:** Выполнено (Режим 3)  
> **Теги:** #task/spec #phase10 #installer #bundling #e2e #docs  
> **Родительский план:** [[../../Plans/PLAN-010-spec-genesis-and-high-snr-release-notes|PLAN-010]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-011-spec-genesis-protocol-and-zero-state-handling|RESEARCH-011]], [[../../../04_Research/RESEARCH-013-release-notes-adr-exclusion-and-high-snr|RESEARCH-013]], [[../../../03_Decisions_ADR/ADR-0018-spec-genesis-protocol-and-zero-state-handling|ADR-0018]], [[../../../03_Decisions_ADR/ADR-0017-release-notes-adr-exclusion-and-high-snr-standard|ADR-0017]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Завершить реализацию Фазы 10: синхронизировать ресурсы автономного инсталлятора `install.py` через `scripts/build_installer.py`, обеспечить сквозную верификацию в `tests/test_installer.py` и актуализировать публичную витрину [README.md](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/README.md) и онбординг [docs/Onboarding.md](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/docs/Onboarding.md):
1. **Пересборка инсталлятора:** упаковать обновленные скиллы (`kb-init`, `kb-plan`, `kb-task`, `kb-release`), скрипт `scripts/kb_release.py`, обновленные шаблоны и генераторы правил.
2. **E2E регрессионное тестирование:** проверить развертывание с нуля (`status: discovery` в `SPEC.md`), бесшовное обновление через `install.py --update` и корректность релизных заметок в изолированной песочнице.
3. **Обновление документации:** отразить инвариант Spec Genesis и стандарт High-SNR Release Notes в документации проекта.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `install.py` и `scripts/build_installer.py` — синхронизация бандла и генераторов правил агентов.
* `[MODIFY]` `tests/test_installer.py` — новый сквозной тест `test_21_spec_genesis_and_high_snr_release_notes`.
* `[MODIFY]` `README.md` — актуализация витрины и описания возможностей Фазы 10.
* `[MODIFY]` `docs/Onboarding.md` — обновление руководства разработчика.

---

## 3. Детали реализации

### 3.1. Сборка и упаковка в `scripts/build_installer.py`
- Пересобрать `install.py` с упаковкой обновленных скиллов и утилит.
- Убедиться, что генератор правил `generate_agents_md()` в `install.py` включает правило `6. Zero-State Anti-Hallucination & Spec Genesis`.

### 3.2. E2E тестирование в `tests/test_installer.py`
- Тест проверяет:
  1. Создание нового проекта с пресетом undecided или вызов `install.py` без флагов развертывает `SPEC.md` со статусом `discovery`.
  2. Вызов `install.py --update` в существующем проекте обновляет скиллы `kb-init`, `kb-plan`, `kb-task`, `kb-release` и утилиту `kb_release.py`.
  3. Экспорт релизных заметок не содержит кумулятивной секции ADR.

### 3.3. Документация в `README.md` и `docs/Onboarding.md`
- Описать концепцию трех состояний зрелости спецификации (`Missing` -> `Discovery` -> `Active`).
- Описать High-SNR стандарт заметок на GitHub.

---

## 4. План верификации (Verification Plan)

- [x] Сборка: `python scripts/build_installer.py` (Exit code 0).
- [x] E2E тесты: `python -m unittest tests/test_installer.py` (100% Pass, Exit code 0).
- [x] Полный тестовый сьют: `python -m unittest discover -s tests` (100% Pass, Exit code 0).
- [x] Линтер базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links, 0 warnings, Exit code 0).
- [x] Проверка CLI: `python install.py --help` (Exit code 0).

---

## 5. Критерии готовности (DoD)

- [x] Дистрибутив `install.py` пересобран и содержит все артефакты Фазы 10.
- [x] Все тесты `tests/` проходят успешно (100% Pass).
- [x] `kb_lint.py` не выдает ошибок и предупреждений.
- [x] Документация (`README.md`, `Onboarding.md`) актуализирована.
- [x] Статус обновлен в ТЗ, Канбане, Дорожной карте и Devlog.
