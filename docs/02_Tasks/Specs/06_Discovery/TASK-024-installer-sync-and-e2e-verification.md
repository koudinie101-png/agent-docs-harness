---
id: TASK-024
title: "Синхронизация инсталлятора install.py, E2E тесты и аудит целостности"
status: done
type: task
phase: 6
component:
  - installer
  - bundling
  - testing
parent_plan: "[[../../Plans/PLAN-006-discovery-mode-and-kb-research-lifecycle|PLAN-006]]"
created: 2026-10-01
updated: 2026-10-01
tags:
  - task/spec
  - phase6
  - component/installer
  - component/bundling
  - component/testing
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-024 — Синхронизация инсталлятора и E2E тесты

> **ID:** TASK-024  
> **Статус:** Выполнено (Режим 3)  
> **Теги:** #task/spec #phase6 #component/installer #component/bundling #component/testing  
> **Родительский план:** [[../../Plans/PLAN-006-discovery-mode-and-kb-research-lifecycle|PLAN-006]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-007-discovery-mode-and-kb-research-lifecycle-integration|RESEARCH-007]], [[../../../03_Decisions_ADR/ADR-0012-discovery-mode-and-kb-research-lifecycle-integration|ADR-0012]], [[../../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Завершить интеграцию Фазы 6 в дистрибутив харнесса Docs-as-Code:
1. **Пересборка дистрибутива `install.py`:** Запустить `scripts/build_installer.py` для упаковки обновленных шаблонов (`TEMPLATE_ROADMAP.md`, `TEMPLATE_ONBOARDING.md`) и скиллов (`kb-research`, `kb-plan`, `kb-onboard`) в самодостаточный скрипт `install.py`.
2. **Расширение набора автотестов `tests/test_installer.py`:**
   - Добавить тест, верифицирующий распаковку обновленных скиллов и наличие контрактов Режима 0 (Discovery & Feasibility).
   - Проверить наличие секций Режима 0 и отклоненных альтернатив в сгенерированных шаблонах.
   - Проверить сценарий обновления (`install.py --update`), подтверждающий актуализацию шаблонов и скиллов без затирания пользовательских данных.
3. **Финальный сквозной аудит:** Убедиться в прохождении всех 30+ тестов и отсутствии битых ссылок в базе знаний (`kb_lint.py`).

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `install.py` — обновление встроенного base64/zlib бандла через сборщик.
* `[MODIFY]` `tests/test_installer.py` — добавление проверок Режима 0, обновленных скиллов и шаблонов.

---

## 3. Детали реализации

### Контракт сборщика
Запуск сборщика производит перепаковку без изменения архитектуры Zero-Dependencies:
```bash
python scripts/build_installer.py
```

### Дополнения в тестовый набор `tests/test_installer.py`
Добавление тестового метода:
```python
    def test_31_discovery_mode_and_phase6_assets(self):
        """Verify Mode 0 (Discovery) rules in unpacked skills, roadmap template, and onboarding."""
        assets = install.unpack_assets(REPO_ROOT)
        
        # Check kb-research skill contains Mode 0 and outcome routing
        kb_research_skill = assets.get(".agents/skills/kb-research/SKILL.md", "")
        self.assertIn("Mode 0: Discovery & Feasibility Research", kb_research_skill)
        self.assertIn("Automated Outcome Routing", kb_research_skill)
        
        # Check TEMPLATE_ROADMAP contains rejected alternatives section
        roadmap_tpl = assets.get("00_Templates/TEMPLATE_ROADMAP.md", "")
        self.assertIn("Отклоненные архитектурные идеи", roadmap_tpl)
        
        # Check TEMPLATE_ONBOARDING contains Mode 0
        onboarding_tpl = assets.get("00_Templates/TEMPLATE_ONBOARDING.md", "")
        self.assertIn("Режим 0: Исследование", onboarding_tpl)
```

---

## 4. План верификации (Verification Plan)

- [x] Сборка бандла: `python scripts/build_installer.py` выполняется успешно (Exit code 0).
- [x] Запуск автотестов: `python -m unittest discover -s tests` проходит со 100% успехом (все тесты OK).
- [x] Линтер базы знаний: `python scripts/kb_lint.py --path docs` подтверждает 0 битых ссылок (Exit code 0).

---

## 5. Критерии готовности (DoD)

- [x] `install.py` синхронизирован со всеми обновленными ассетами.
- [x] Все автотесты проходят успешно.
- [x] База знаний валидна и не содержит битых ссылок.
- [x] Статус обновлен в ТЗ (`done`), Канбане (`## ✅ Готово`) и Дорожной карте (`[x]`).
- [x] Запись сессии добавлена в `docs/Devlog.md`.
