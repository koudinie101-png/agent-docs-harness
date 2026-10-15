---
id: BUG-008
title: "Отсутствие docs/06_Memory/patterns.md в локальном fallback install.py и некорректная маска фаз >= 10 в scripts/kb_release.py"
status: fixed
severity: high
type: bug
target_release: "v0.17.0"
target_phase: 17
release_blocker: true
fixed_in: "v0.17.0"
regression_test: "tests/test_installer.py"
created: 2026-10-14
updated: 2026-10-15
tags:
  - bug
  - defect
  - installer
  - release
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 🐞 Дефект: BUG-008 — Отсутствие docs/06_Memory/patterns.md в локальном fallback install.py и некорректная маска фаз >= 10 в scripts/kb_release.py

> **ID:** BUG-008 | **Критичность:** High | **Статус:** fixed  
> **Релиз:** v0.17.0 | **Блокер:** Да  
> **Канбан:** [[../Kanban|Канбан-доска]] | **Спецификация:** [[../../SPEC|SPEC.md]]  

---

## 1. Симптомы и окружение
* **Симптомы:**
  1. При разработке в локальном репозитории без собранного base64-бандла (`EMBEDDED_ASSETS_B64 = ""`) выполнение `install.py` не создает файл `docs/06_Memory/patterns.md`. В результате новый проект создается без инициализированной процедурной памяти, и `scripts/kb_lint.py` выдает предупреждение об отсутствии индекса памяти.
  2. В `scripts/kb_release.py` при автоматическом поиске спеков фаз без явного поля `phase` во фронтматтере маска поиска для фаз $\ge 10$ вычисляется как `"015_"` вместо `"15_"`, из-за чего задачи двузначных фаз теряются в релизных заметках.
* **Окружение:** `install.py` (`unpack_assets()`), `scripts/kb_release.py` (`find_phase_artifacts()`).

## 2. Шаги воспроизведения (Repro Steps)
1. **Воспроизведение 1 (install.py):**
   - Запустить `python install.py /tmp/test-project` в режиме исходного репозитория, когда `EMBEDDED_ASSETS_B64` пуст или не содержит `patterns.md`.
   - Проверить наличие `/tmp/test-project/docs/06_Memory/patterns.md`. Файл отсутствует.
2. **Воспроизведение 2 (kb_release.py):**
   - Создать спек в папке `docs/02_Tasks/Specs/15_LatencyAndChannels/` без явного `phase: 15` в YAML.
   - Запустить `find_phase_artifacts(docs_dir, 15)`. Спек не находится, так как ищется подстрока `"015_"`.

## 3. Диагностика (Логи, Стек-трейс)
1. В `install.py` (`unpack_assets()`):
   ```python
   # Собираются шаблоны, скрипты, скиллы, workflow, но patterns.md не включен в словарь assets
   ```
2. В `scripts/kb_release.py` (`find_phase_artifacts()`):
   ```python
   for p in target_phases:
       if f"0{p}_" in str(spec_file) or f"phase{p}" in str(spec_file).lower():
   ```
   Для `p = 15` выражение `f"0{p}_"` дает `"015_"`, что не соответствует именованию каталогов `15_LatencyAndChannels`.

## 4. Первопричина (Root Cause Analysis — RCA)
1. В `install.py` логика локального fallback копирует `Zero_To_Hero_Guide.md`, но не включает `docs/06_Memory/patterns.md`.
2. В `scripts/kb_release.py` жестко закодирован префикс `"0"` (`f"0{p}_"`), рассчитанный только на однозначные фазы (`01_`–`09_`).

## 5. План исправления
* `[MODIFY]` `install.py` — добавить чтение `docs/06_Memory/patterns.md` в секцию локального fallback функции `unpack_assets()`.
* `[MODIFY]` `scripts/kb_release.py` — заменить `f"0{p}_"` на `f"{p:02d}_"` (или проверку `f"{p:02d}_" in str(spec_file) or f"{p}_" in str(spec_file)`).
* `[NEW]` `tests/test_installer.py` — тест на распаковку `patterns.md` в локальном режиме.
* `[NEW]` `tests/test_kb_release.py` — тест поиска артефактов для фаз $\ge 10$ без поля `phase`.

## 6. Верификация (Regression-First)
- [x] Падающий регрессионный тест воспроизводит дефект (RED).
- [x] Исправление применено в коде (GREEN).
- [x] Регрессионный тест и весь сьют проходят успешно (REFACTOR).
- [x] Дефект закрыт через `/kb-implement BUG-008`.
