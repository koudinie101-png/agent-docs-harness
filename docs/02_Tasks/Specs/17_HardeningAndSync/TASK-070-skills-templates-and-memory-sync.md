---
id: TASK-070
title: "Синхронизация скиллов, шаблонов и контура памяти в AGENTS.md"
status: planned
type: task
phase: 17
component:
  - skills
  - templates
  - agents
  - memory
  - graph
parent_plan: "[[../../Plans/PLAN-017-core-hardening-and-ssot-sync|PLAN-017]]"
created: 2026-10-15
updated: 2026-10-15
tags:
  - task/spec
  - phase17
  - skills
  - templates
  - memory
  - stop-yield
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-070 — Синхронизация скиллов, шаблонов и контура памяти в AGENTS.md

> **ID:** TASK-070 | **Статус:** К реализации  
> **Фаза:** 17 | **Релиз:** v0.17.0  
> **План:** [[../../Plans/PLAN-017-core-hardening-and-ssot-sync|PLAN-017]] | **Канбан:** [[../../Kanban|Канбан]]  

---

## 1. Цель задачи
Устранить скрытые архитектурные швы и рассинхронизацию между протоколом прямого вызова (Zero Round-Trip Dispatch из Фазы 15), контуром памяти дефектов (Фаза 16), каноническими скиллами (`.agents/skills/`), шаблонами (`templates/`, `docs/00_Templates/`) и графом Obsidian (`templates/graph.json`):
1. **Zero Round-Trip Memory Sync:** Восстановить обязательный префлайт-шаг чтения процедурной памяти (`docs/06_Memory/patterns.md`) и шаг фиксации инцидентов (`INC-XXX`) при ошибках в Режиме 3 в корневом `AGENTS.md` и `generate_agents_md()` в `install.py`.
2. **Terminal Stop & Yield в Read-Only скиллах:** Добавить явный терминальный шаг `Stop & Yield Control` в конец `kb-plan/SKILL.md`, `kb-task/SKILL.md`, `kb-research/SKILL.md` и `kb-adr/SKILL.md` для исключения несанкционированного авто-чейнинга задач (Single-Task Barrier).
3. **Кастомизация `TEMPLATE_TASK_MICRO.md`:** Исправить в шаблоне хардкод `phase: 14` на `phase: 1`, а в `install.py` (`customize_templates_for_stack`) реализовать адаптацию тестовой команды стека (`stack["test_cmd"]`) и замену устаревших дат на текущую `today_str`.
4. **Относительные пути в `TEMPLATE_RELEASE.md`:** Заменить примеры ссылок на релизные задачи на относительные с выходом из каталога `Releases/`: `[[../Specs/0N_Phase/TASK-XXX-slug|TASK-XXX]]` и `[[../Bugs/BUG-XXX-slug|BUG-XXX]]`.
5. **Актуализация таксономии 16 шаблонов, графа и полировка Zero_To_Hero_Guide:** Синхронизировать число шаблонов (16), каталоги `02_Tasks/Inbox/` и `06_Memory/Incidents/` в `kb-init`, `kb-onboard`, `TEMPLATE_ONBOARDING.md`, `docs/Onboarding.md`, `tests/test_installer.py` (`test_26`), раскраску узлов `#memory`, `Inbox/` и `Zero_To_Hero_Guide` в `TEMPLATE_INDEX.md` и `templates/graph.json` с соблюдением лимитов размеров файлов (`test_16`), а также устранить пробелы в руководстве `Zero_To_Hero_Guide.md` (добавить URL скачивания `install.py` и флаг `-y` в Раздел 4, подраздел `/kb-bug` в Раздел 2, исправить синтаксис команды `/kb-task`).

---

## 2. Затрагиваемые файлы
* `[MODIFY]` `AGENTS.md` — префлайт памяти и рефлексия инцидентов в Режиме 3.
* `[MODIFY]` `install.py` — функция `generate_agents_md()`, кастомизация `customize_templates_for_stack()`.
* `[MODIFY]` `.agents/skills/kb-plan/SKILL.md` — терминальный шаг `Stop & Yield Control`.
* `[MODIFY]` `.agents/skills/kb-task/SKILL.md` — терминальный шаг `Stop & Yield Control`.
* `[MODIFY]` `.agents/skills/kb-research/SKILL.md` — терминальный шаг `Stop & Yield Control`.
* `[MODIFY]` `.agents/skills/kb-adr/SKILL.md` — терминальный шаг `Stop & Yield Control`.
* `[MODIFY]` `.agents/skills/kb-init/SKILL.md` — 16 шаблонов, каталоги `Inbox/` и `06_Memory/Incidents/`.
* `[MODIFY]` `.agents/skills/kb-onboard/SKILL.md` — актуализация таксономии 16 шаблонов (лимит $\le 3000$ байт).
* `[MODIFY]` `templates/TEMPLATE_TASK_MICRO.md` и `docs/00_Templates/TEMPLATE_TASK_MICRO.md` — `phase: 1`.
* `[MODIFY]` `templates/TEMPLATE_RELEASE.md` и `docs/02_Tasks/Releases/` шаблоны — относительные пути `[[../Specs/...]]` и `[[../Bugs/...]]`.
* `[MODIFY]` `templates/TEMPLATE_ONBOARDING.md` и `docs/00_Templates/TEMPLATE_ONBOARDING.md` — 16 шаблонов (лимит $\le 5000$ байт).
* `[MODIFY]` `templates/TEMPLATE_INDEX.md` и `docs/00_Index.md` — узлы `Zero_To_Hero_Guide`, `Inbox/`, `06_Memory/`.
* `[MODIFY]` `templates/graph.json` и `docs/.obsidian/graph.json` — теги и цвета `#memory`, `02_Tasks/Inbox`, `Zero_To_Hero_Guide`.
* `[MODIFY]` `docs/Onboarding.md` — таксономия 16 шаблонов (4 Core, 12 Advanced).
* `[MODIFY]` `docs/Zero_To_Hero_Guide.md` — URL скачивания `install.py` и флаг `-y`, секция `/kb-bug`, фикс команды `/kb-task`.
* `[MODIFY]` `tests/test_installer.py` — проверка таксономии 16 шаблонов в `test_26` и лимитов в `test_16`.

---

## 3. Детали реализации

### 3.1. Zero Round-Trip Memory Sync (`AGENTS.md` & `install.py`)
В секцию `### 🟢 Mode 3: Implementation & Verification` файла `AGENTS.md` и строку `generate_agents_md()` в `install.py`:
1. В начало перечня действий добавить обязательный префлайт-шаг:
   ```markdown
   - **0. Memory-First Preflight:** Read `docs/06_Memory/patterns.md` to avoid known procedural pitfalls and regression patterns before making any changes.
   ```
2. В чеклист завершения (Completion Checklist) добавить шаг рефлексии:
   ```markdown
   - Defect Loop Reflection: If execution involved errors, failed iterations, or unexpected defects, log an incident report (`docs/06_Memory/Incidents/INC-XXX.md`) and update `docs/06_Memory/patterns.md` according to Tier 2 guidelines.
   ```

### 3.2. Terminal Stop & Yield в Read-Only скиллах
В конец файлов `.agents/skills/kb-plan/SKILL.md`, `kb-task/SKILL.md`, `kb-research/SKILL.md` и `kb-adr/SKILL.md` добавить финальный шаг:
```markdown
7. **Terminal Step (Stop & Yield Control):**
   - Output concise Anti-Echo summary with clickable file links.
   - Suggest the exact next command (e.g. *"If approved, say `/kb-task <name>` to begin specification"*).
   - **STRICTLY STOP ALL TOOL CALLS.** Yield control to user and wait for explicit command.
```

### 3.3. Кастомизация `TEMPLATE_TASK_MICRO.md`
1. В `templates/TEMPLATE_TASK_MICRO.md` и `docs/00_Templates/TEMPLATE_TASK_MICRO.md`:
   - Заменить `phase: 14` на `phase: 1`.
2. В `install.py` (`customize_templates_for_stack`):
   - Добавить обработку `template_name == "TEMPLATE_TASK_MICRO.md"`.
   - Заменять `python -m unittest discover -s tests` на `stack["test_cmd"]`.
   - Заменять даты `2026-10-03`, `2026-10-12` на `today_str`.

### 3.4. Относительные пути в `TEMPLATE_RELEASE.md`
В `templates/TEMPLATE_RELEASE.md` и `docs/00_Templates/TEMPLATE_RELEASE.md` скорректировать примеры ссылок секции `## 🚀 Что нового`:
```markdown
* **Фичи:** [[../Specs/0N_Phase/TASK-XXX-slug|TASK-XXX]]: <!-- Описание -->
* **Багфиксы:** [[../Bugs/BUG-XXX-slug|BUG-XXX]]: <!-- Описание -->
```

### 3.5. Таксономия 16 шаблонов и граф Obsidian
1. **`kb-init/SKILL.md`:** обновить счетчик шаблонов (16), добавить создание каталогов `docs/02_Tasks/Inbox/` и `docs/06_Memory/Incidents/`.
2. **`kb-onboard/SKILL.md` & `TEMPLATE_ONBOARDING.md`:** зафиксировать формулировку `16 templates: 4 Core, 12 Advanced`, добавить упоминание `TEMPLATE_TASK_MICRO.md`, `TEMPLATE_INCIDENT.md`, команды `/kb-triage` и флага `--fast`. Проверить размеры: `kb-onboard <= 3000` байт, `TEMPLATE_ONBOARDING <= 5000` байт.
3. **`TEMPLATE_INDEX.md` & `docs/00_Index.md`:** добавить в карту и разделы ссылки на `[[Zero_To_Hero_Guide|Вайбкодинг со страховкой]]`, `02_Tasks/Inbox/` и `06_Memory/`.
4. **`templates/graph.json` & `docs/.obsidian/graph.json`:**
   - Добавить узел `Zero_To_Hero_Guide` в группу хабов.
   - Добавить цветную группу для `path:06_Memory OR tag:#memory` (фиолетовый/сиреневый).
   - Добавить `path:02_Tasks/Inbox` в группу задач.
5. **`tests/test_installer.py` (`test_26`):** обновить ассерты на проверку 16 шаблонов (4 Core, 12 Advanced).
6. **Полировка `docs/Zero_To_Hero_Guide.md`:**
   - **Раздел 4 («Запуск без терминала»):** в промпт для агента добавить прямую инструкцию скачивания скрипта (`curl -sSL https://raw.githubusercontent.com/koudinie101-png/agent-docs-harness/main/install.py -o install.py`) и запуск с неинтерактивным флагом по умолчанию (`python install.py -y`), чтобы агент в пустой папке не зависал на интерактивном опроснике.
   - **Раздел 2:** добавить подраздел `### 🐞 Если что-то сломалось (/kb-bug)` (аналогия: «диагностическая карта в автосервисе») как процедурный ответ на проблему «галлюцинаторного штопора» из Раздела 1.
   - **Раздел 2:** исправить пример команды с `/kb-task TASK-001 Профиль пользователя` на `/kb-task Профиль пользователя` (номер задачи генерируется агентом автоматически).

---

## 4. План верификации (Verification Plan)
- [ ] Линтер базы знаний: `python scripts/kb_lint.py --path docs` — Exit code 0, 0 broken links.
- [ ] Модульные тесты инсталлятора: `pytest tests/test_installer.py -k "test_16 or test_26"` — 100% pass (соблюдение лимитов байт и таксономии).
- [ ] Полный тестовый сьют: `pytest tests/` — 100% pass.
- [ ] Проверка компиляции скриптов: `python -m py_compile scripts/*.py install.py`.
- [ ] Сборка дистрибутива: `python scripts/build_installer.py` без предупреждений.

---

## 5. Критерии готовности (DoD)
- [ ] Спецификация согласована и зарегистрирована в плане `PLAN-017`, `Roadmap.md` и `Kanban.md`.
- [ ] Все адаптеры, шаблоны, скиллы и тесты приведены к единому стандарту таксономии и контура памяти.
- [ ] Все пункты Плана верификации выполнены.
- [ ] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [ ] Запись добавлена в `Devlog.md`.
