---
id: TASK-032
title: "Сборка инсталлятора build_installer.py, сквозные E2E тесты и документация"
status: planned
type: task
phase: 8
component:
  - bundler
  - installer
  - e2e-testing
  - docs
parent_plan: "[[../../Plans/PLAN-008-greenfield-idea-first-and-living-spec|PLAN-008]]"
created: 2026-10-02
updated: 2026-10-02
tags:
  - task/spec
  - phase8
  - component/bundler
  - component/installer
  - e2e-testing
  - documentation
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-032 — Сборка инсталлятора, E2E тесты и документация

> **ID:** TASK-032  
> **Статус:** К реализации (Режим 2)  
> **Теги:** #task/spec #phase8 #component/bundler #component/installer #e2e-testing #documentation  
> **Родительский план:** [[../../Plans/PLAN-008-greenfield-idea-first-and-living-spec|PLAN-008]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-009-greenfield-initialization-and-living-spec-drift|RESEARCH-009]], [[../../../03_Decisions_ADR/ADR-0014-greenfield-idea-first-initialization-and-living-spec-protocol|ADR-0014]], [[../../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Завершить реализацию Фазы 8 согласно [[../../Plans/PLAN-008-greenfield-idea-first-and-living-spec|PLAN-008]]:
1. **Пересборка инсталлятора:** Запустить `scripts/build_installer.py` для запаковки обновленных шаблонов, утилит `kb_lint.py` и скиллов `.agents/skills/` в автономный монолит `install.py` (`EMBEDDED_ASSETS_B64`).
2. **Сквозное E2E тестирование:** Верифицировать корректность работы инсталлятора при чистой установке с `--idea`, обновлении `--update`, проверке пресета `undecided` и детекции дрифта в `test_installer.py`.
3. **Обновление документации:**
   - Внести в `README.md` описание флага `--idea` и сценария старта от идеи (Idea-First Greenfield).
   - Актуализировать `docs/Onboarding.md` и шаблон `templates/TEMPLATE_ONBOARDING.md` с описанием пресета `undecided` и протокола Living Spec.
4. **Аудит целостности:** Запустить `scripts/kb_lint.py` для подтверждения отсутствия битых ссылок во всем репозитории.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `install.py` — обновление упакованного монолита `EMBEDDED_ASSETS_B64`.
* `[MODIFY]` `scripts/build_installer.py` — сборка и верификация контента бандла.
* `[MODIFY]` `tests/test_installer.py` — расширение набора E2E тестов.
* `[MODIFY]` `README.md` — раздел быстрого старта с опцией `--idea`.
* `[MODIFY]` `docs/Onboarding.md` — гайд по Greenfield Idea-First старту и Living Spec.
* `[MODIFY]` `templates/TEMPLATE_ONBOARDING.md` — синхронизация шаблона онбординга.

---

## 3. Детали реализации

### 3.1. Синхронизация ассетов и пересборка
Команда сборки:
```bash
python scripts/build_installer.py
```
Сборщик должен упаковать актуальные версии `.agents/skills/kb-research/SKILL.md`, `.agents/skills/kb-complete/SKILL.md`, `.agents/skills/kb-release/SKILL.md`, `scripts/kb_lint.py` и обновить строку `EMBEDDED_ASSETS_B64` в корневом `install.py`.

### 3.2. E2E верификация в изолированной песочнице
Тест в `tests/test_installer.py`:
1. Создание временного каталога.
2. Выполнение `install.py --target-dir <dir> --idea "AI note taking service" --doc-lang ru`.
3. Проверка:
   - Создан ли `SPEC.md` со статусом `discovery` и переданным описанием идеи.
   - Развернуты ли все 12 скиллов в `.agents/skills/`.
   - Проходит ли `python scripts/kb_lint.py --path <dir>/docs` без ошибок.

---

## 4. План верификации (Verification Plan)

- [ ] Сборка монолита: `python scripts/build_installer.py` (Exit code 0).
- [ ] Полный прогон тестового набора: `python -m unittest discover -s tests` (100% pass).
- [ ] Проверка целостности базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links).

---

## 5. Критерии готовности (DoD)

- [ ] `install.py` пересобран и содержит все обновленные компоненты.
- [ ] Документация `README.md` и `docs/Onboarding.md` актуализирована.
- [ ] Все автотесты (модульные и сквозные E2E) проходят успешно.
- [ ] Финальный аудит линтера завершается без ошибок.
- [ ] Статус всех задач Фазы 8 обновлен в Канбане и Дорожной карте.
