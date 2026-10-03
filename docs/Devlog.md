---
id: DEVLOG
title: Журнал разработки (Devlog)
status: active
type: devlog
created: 2026-09-30
updated: 2026-10-03
tags:
  - devlog
  - journal
  - agent-docs-harness
---

# 📝 Журнал разработки (Devlog): agent-docs-harness

> **Теги:** #devlog #journal #agent-docs-harness  
> **Родительская заметка:** [[00_Index|00_Index]]  

### [2026-10-03] — Завершение TASK-036: Spec Genesis Protocol и Zero-State Guardrails
- **Что сделано:**
  - Реализован входной шлюз методологии Docs-as-Code — Протокол рождения Мастер-Спецификации (Spec Genesis) и защита от галлюцинаций в пустом состоянии (Zero-State) согласно [[03_Decisions_ADR/ADR-0018-spec-genesis-protocol-and-zero-state-handling|ADR-0018]] и [[04_Research/RESEARCH-011-spec-genesis-protocol-and-zero-state-handling|RESEARCH-011]].
  - В скилл `.agents/skills/kb-init/SKILL.md` добавлено гарантированное развертывание каркаса `SPEC.md` со статусом `status: discovery` (Spec Genesis skeleton), устраняя архитектурный пробел тулинга по сравнению с `install.py`.
  - В скилл `.agents/skills/kb-plan/SKILL.md` внедрен префлайт-чек Spec Genesis (Zero-State Guard), выдающий мягкое предупреждение (Soft Nudge) с предложением кристаллизовать концепцию и стек через `/kb-research` (Режим 0) до перехода к детальному планированию.
  - В скилл `.agents/skills/kb-task/SKILL.md` добавлена проверка статуса `SPEC.md`, предотвращающая нарезку ТЗ без согласованной спецификации.
  - В [AGENTS.md](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/AGENTS.md) закреплен инвариант `6. Zero-State Anti-Hallucination & Spec Genesis`: категорический запрет директивного выдумывания архитектуры, стека и бизнес-требований без прямого диалога с пользователем.
  - Спецификация задачи [[02_Tasks/Specs/10_SpecLifecycle/TASK-036-spec-genesis-and-zero-state-guardrails|TASK-036]] переведена в статус `done`, Канбан и Дорожная карта актуализированы.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 105 файлов проверено, 855 связей валидны (0 битых, 0 предупреждений, Exit code 0).
  - `python -m unittest discover -s tests` -> 47/47 тестов успешно пройдено (100% Pass, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация задачи `TASK-037`: `/kb-implement TASK-037`.

---

### [2026-10-03] — Завершение TASK-035: Синхронизация инсталлятора, E2E тесты и документация (Завершение Фазы 9)
- **Что сделано:**
  - Завершена реализация Фазы 9: комплексная интеграция барьера единичной задачи и протокола гарантированной остановки в дистрибутив харнесса Docs-as-Code ([[03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]], [[04_Research/RESEARCH-012-single-task-execution-barrier-and-autonomous-pipeline-containment|RESEARCH-012]]).
  - В `install.py` актуализированы строковые константы правил (`_RULES_BODY`, `_3MODES` с 13-й дисциплиной `Single-Task Barrier`), встроенный генератор `generate_agents_md` и запись обновлений `record_devlog_update` с семантическим маркером.
  - Через `scripts/build_installer.py` пересобран автономный дистрибутив `install.py` с упаковкой обновленных шаблонов (`TEMPLATE_DEVLOG.md`, `TEMPLATE_ONBOARDING.md`), скиллов (`kb-implement`, `kb-complete`) и утилиты `scripts/kb_lint.py`.
  - В `tests/test_installer.py` добавлен сквозной E2E тест `test_20_single_task_barrier_and_stop_on_complete`, проверяющий генерацию правил, доставку обновлений через `install.py --update`, бэкап `AGENTS.md.bak` и чистоту журнала без предупреждений линтера.
  - Витрина проекта `README.md` и руководство `docs/Onboarding.md` дополнены описанием барьера единичной задачи и протокола Stop & Yield Control.
  - Успешно завершены задача [[02_Tasks/Specs/09_Guardrails/TASK-035-installer-bundling-e2e-and-docs|TASK-035]], план [[02_Tasks/Plans/PLAN-009-single-task-barrier-and-stop-on-complete|PLAN-009]] и вся Фаза 9 в [[02_Tasks/Kanban|Канбане]] и [[02_Tasks/Roadmap|Дорожной карте]].
- **Результаты верификации:**
  - `python scripts/build_installer.py` -> Успешная сборка дистрибутива `install.py` (Exit code 0).
  - `python -m unittest discover -s tests` -> 47/47 тестов успешно пройдено (100% Pass, Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 101 файл проверен, 795 связей валидны (0 битых, 0 предупреждений, Exit code 0).
  - `python install.py --help` -> Автономный инсталлятор готов к использованию (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Подготовка и срез официального релиза Фазы 9: `/kb-release v0.9.0 --phase 9`.

---

### [2026-10-03] — Завершение TASK-034: Семантический протокол журнала разработки и аудит в kb_lint.py
- **Что сделано:**
  - Реализованы уровни 3 и 4 эшелонированной защиты против своевольного авто-чейнинга (Eager Task Chaining) согласно [[03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]] и [[04_Research/RESEARCH-012-single-task-execution-barrier-and-autonomous-pipeline-containment|RESEARCH-012]].
  - В шаблонах `docs/00_Templates/TEMPLATE_DEVLOG.md` и `templates/TEMPLATE_DEVLOG.md` строка «Следующий шаг» заменена на семантически безопасный маркер `- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**`.
  - В `scripts/kb_lint.py` реализована функция `check_devlog_semantic_guard(docs_dir)`: неблокирующий эвристический аудит (Exit code 0), выявляющий формулировки, провоцирующие модель на несанкционированное конвейерное продолжение работы.
  - В `tests/test_kb_lint.py` добавлены 4 модульных теста (`test_devlog_semantic_guard_*`), проверяющие детекцию опасных паттернов, пропуск защищенных строк и неблокирующий статус предупреждений.
  - Исторические записи в `docs/Devlog.md` приведены в соответствие новому стандарту (0 предупреждений).
  - Спецификация задачи [[02_Tasks/Specs/09_Guardrails/TASK-034-devlog-semantic-guard-and-kb-lint-audit|TASK-034]] переведена в статус `done`, Канбан-доска и Дорожная карта актуализированы.
- **Результаты верификации:**
  - `python -m unittest tests/test_kb_lint.py` -> 14/14 тестов успешно пройдено (100% Pass).
  - `python -m unittest discover -s tests` -> 46/46 тестов успешно пройдено (100% Pass).
  - `python scripts/kb_lint.py --path docs` -> 100 файлов проверено, 782 связи валидны (0 битых, 0 предупреждений).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация задачи `TASK-035`: `/kb-implement TASK-035`.

---

### [2026-10-03] — Завершение TASK-033: Нормативный инвариант барьера единичной задачи и терминальный шаг Stop & Yield Control
- **Что сделано:**
  - Реализованы уровни 1 и 2 эшелонированной защиты против своевольного авто-чейнинга (Eager Task Chaining) согласно [[03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]] и [[04_Research/RESEARCH-012-single-task-execution-barrier-and-autonomous-pipeline-containment|RESEARCH-012]].
  - В корневые правила [AGENTS.md](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/AGENTS.md) внесен инвариант `5. Single-Task Execution Barrier (No Auto-Chaining)` и шаг 9 `Terminal Step (Stop & Yield)` в чеклист Mode 3.
  - В скилл `.agents/skills/kb-implement/SKILL.md` добавлено ограничение `Single-Task Barrier` и шаг 5 `Immediate Auto-Completion & Stop` с принудительной остановкой вызовов инструментов.
  - В скилл `.agents/skills/kb-complete/SKILL.md` добавлено ограничение `Single-Task Barrier`, шаг 9 `Terminal Step: Stop & Yield Control` и семантический формат записи в Devlog.
  - Синхронизирована мастер-спецификация `SPEC.md` (добавлено описание Single-Task Barrier и Фазы 9).
  - Спецификация задачи [[02_Tasks/Specs/09_Guardrails/TASK-033-single-task-barrier-and-stop-yield-skills|TASK-033]] переведена в статус `done`, Канбан-доска и Дорожная карта актуализированы.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 100 файлов проверено, 775 связей валидны (0 битых).
  - `python -m unittest discover -s tests` -> 42/42 теста успешно пройдено (100% Pass).
  - High-SNR замеры: `kb-implement` (32 строки), `kb-complete` (37 строк) соответствуют лимитам компактности.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация задачи `TASK-034`: `/kb-implement TASK-034`.

---

### [2026-10-02] — Устранение дефекта BUG-001: Рассинхронизация номера фазы и описания релиза в CI release.yml
- **Что сделано:**
  - Локализован и устранен дефект [[02_Tasks/Bugs/BUG-001-ci-release-notes-phase-fallback|BUG-001]]: сброс метаданных в дефолтную Фазу 1 при запуске в GitHub Actions CI без параметров `--phase` и `--summary`.
  - Разработан воспроизводящий регрессионный тест `test_ci_mode_infers_phase_and_summary_from_existing_release_doc` в `tests/test_kb_release.py` (Regression-First, RED -> GREEN).
  - В `scripts/kb_release.py` добавлены функции `extract_release_meta_from_doc` (чтение `phase` и `Executive Summary` из существующего артефакта `docs/02_Tasks/Releases/RELEASE-{tag}.md` как Single Source of Truth) и `detect_latest_phase` (эвристический автодетект фазы по `docs/02_Tasks/Specs/`).
  - Пересобран бандл `install.py` (89.4 KB) через `scripts/build_installer.py`.
  - Карточка дефекта переведена в статус `Done` на Канбан-доске [[02_Tasks/Kanban|Kanban.md]], отчет [[02_Tasks/Bugs/BUG-001-ci-release-notes-phase-fallback|BUG-001]] переведен в статус `fixed`.
- **Результаты верификации:**
  - `python -m unittest discover -s tests` -> 42/42 теста пройдено успешно (100% Pass).
  - `python scripts/kb_release.py --version v0.8.0 --ci-mode` -> сформирован корректный `dist/RELEASE_NOTES.md` с «Фаза 8» и полным Executive Summary.
  - `python scripts/kb_lint.py --path docs` -> 94 файла проверено, 712 викиссылок валидны (0 битых).

---

### [2026-10-02] — Выпуск официального релиза v0.8.0: Greenfield-инициализация от идеи и Living Spec (Фаза 8)
- **Что сделано:**
  - Осуществлен официальный релиз **v0.8.0** по завершении Фазы 8 (План [[02_Tasks/Plans/PLAN-008-greenfield-idea-first-and-living-spec|PLAN-008]]).
  - Сформирован релизный документ [[02_Tasks/Releases/RELEASE-v0.8.0|RELEASE-v0.8.0]] и публичные заметки `dist/RELEASE_NOTES.md` с чистым GitHub Markdown и автоконвертером викиссылок.
  - Собраны релизные артефакты через хук `scripts/build_release.py`:
    - `dist/install.py` (88.4 KB) — SHA-256: `867757bad12d737fa8409fdfea41e63850c9658f8e5fb0cc4a60c62e6351ec26`.
    - `dist/RELEASE_NOTES.md` (6.4 KB) — SHA-256: `1469cd999b113ab5a8f98ad4eb9c96e996e1c936d865186d8dcf431cecaf421e`.
  - Обновлены [[02_Tasks/Roadmap|Roadmap.md]] (ссылка на официальный релиз `RELEASE-v0.8.0`) и корневой `CHANGELOG.md` (секция `[0.8.0]`).
  - Зафиксирован аннотированный Git-тег `v0.8.0`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 93 файла проверено, 683 викиссылки валидны (0 битых).
  - `python -m unittest discover -s tests` -> 41/41 тест успешно пройден (100% Pass).
  - Контрольная сумма SHA-256 `dist/install.py` подтверждена (`867757bad12d737fa8409fdfea41e63850c9658f8e5fb0cc4a60c62e6351ec26`).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Определение приоритета следующей инициативы из Icebox (например, реализация Single-Task Execution Barrier по итогам [[04_Research/RESEARCH-012-single-task-execution-barrier-and-autonomous-pipeline-containment|RESEARCH-012]] и [[03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]]) через `/kb-plan`.

---

### [2026-10-02] — Завершение TASK-032: Сборка инсталлятора, E2E тесты и документация (Завершение Фазы 8)
- **Что сделано:**
  - Запущен сборщик `scripts/build_installer.py`: актуализирован монолит `install.py` с упаковкой обновленных шаблонов (`TEMPLATE_ONBOARDING.md`), скиллов (`kb-research`, `kb-complete`, `kb-release`), скрипта `kb_lint.py` и конфигов (`EMBEDDED_ASSETS_B64`).
  - Расширен тестовый сценарий `test_19_undecided_preset_and_idea_flag` в `tests/test_installer.py`: добавлена валидация развертывания всех 12 скиллов и успешного прогона `kb_lint.py` на созданном проекте.
  - Актуализирован `README.md`: добавлен раздел быстрого старта с опцией `--idea` (Greenfield Idea-First), пресет `undecided` в таблицу поддерживаемых стеков, CLI-флаг `--idea`, и диаграмма 4-этапного жизненного цикла (Discovery + Delivery).
  - Актуализировано руководство `docs/Onboarding.md` и шаблон `templates/TEMPLATE_ONBOARDING.md`: добавлен раздел 7 с регламентом Greenfield Idea-First старта, инварианта Living Spec и эвристического контроля дрифта.
  - Задача [[02_Tasks/Specs/08_Greenfield/TASK-032-installer-bundling-and-e2e-verification|TASK-032]] и весь план [[02_Tasks/Plans/PLAN-008-greenfield-idea-first-and-living-spec|PLAN-008]] переведены в статус `done`, Канбан и Дорожная карта актуализированы (Фаза 8 завершена).
- **Результаты верификации:**
  - `python scripts/build_installer.py` -> успешная сборка монолита `install.py` (88.4 KB).
  - `python -m unittest discover -s tests` -> 41/41 тест пройден (100% Pass).
  - `python scripts/kb_lint.py --path docs` -> 89 файлов проверено, 658 викиссылок валидны (0 битых).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Выпуск официального релиза Фазы 8 через `/kb-release v0.8.0`.

---

### [2026-10-02] — Завершение TASK-031: Эвристический контроль дрифта спецификации в scripts/kb_lint.py
- **Что сделано:**
  - В автономном линтере `scripts/kb_lint.py` реализована функция `check_spec_drift(docs_dir: Path)` для неблокирующего эвристического анализа устаревания мастер-спецификации.
  - Детектор сканирует `Roadmap.md` на предмет завершенных фаз (`## Фаза X: ... — ✅ Завершена` или блоков с закрытыми чекбоксами `- [x]`) и сверяет дату `updated` в `SPEC.md` с датой `created`.
  - При обнаружении $\ge 2$ завершенных фаз без обновления `SPEC.md` линтер выводит неблокирующее предупреждение (`⚠️  WARN: Living Spec Drift...`), сохраняя статус успешного выполнения (`exit code 0`).
  - В `tests/test_kb_lint.py` добавлено 5 новых модульных тестов, проверяющих:
    - генерацию предупреждения при дрифте (с сохранением exit code 0);
    - отсутствие предупреждения при актуализированном `SPEC.md` (`updated != created`);
    - отсутствие ложных срабатываний при одной завершенной фазе (порог $\ge 2$);
    - безопасную работу при отсутствии файлов спецификации или дорожной карты;
    - форматирование секции дрифта в подробном режиме (`--verbose`).
  - Актуализирована мастер-спецификация `SPEC.md`: дата обновлена до `2026-10-02`, разделы дополнены описанием 4 этапов жизненного цикла (Modes 0–3), 13 шаблонов, утилит `kb_release.py` и `kb_lint.py`, пресета `undecided` и протокола Living Spec.
  - Задача [[02_Tasks/Specs/08_Greenfield/TASK-031-kb-lint-spec-drift-audit|TASK-031]] переведена в `status: done`, Канбан и Дорожная карта актуализированы.
- **Результаты верификации:**
  - `python -m unittest tests/test_kb_lint.py` -> 10/10 тестов пройдено (100% Pass).
  - `python -m unittest discover -s tests` -> 41/41 тест пройден (100% Pass).
  - `python scripts/kb_lint.py --path docs` -> 89 файлов проверено, 656 викиссылок валидны (0 битых, 0 предупреждений дрифта).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация задачи [[02_Tasks/Specs/08_Greenfield/TASK-032-installer-bundling-and-e2e-verification|TASK-032]] (Сборка инсталлятора `build_installer.py`, сквозные E2E тесты нового пресета, обновление `README.md` и `docs/Onboarding.md`).

---

### [2026-10-02] — Завершение TASK-030: Протокол Living Spec и синхронизация документации
- **Что сделано:**
  - В скилле `.agents/skills/kb-research/SKILL.md` добавлен шаг первичного выбора стека (Primary Stack Selection): если `SPEC.md` находится в `status: discovery`, принятие `ADR-0001` автоматически переводит спецификацию в `status: active`, наполняет реальными командами сборки/тестирования и синхронизирует `README.md`.
  - В скилле `.agents/skills/kb-complete/SKILL.md` внедрен шаг `Living Spec Sync`: если завершенная задача изменила публичный CLI, интерфейсы или системную архитектуру, агент обязан актуализировать `SPEC.md` и `README.md` в той же сессии.
  - В скилле `.agents/skills/kb-release/SKILL.md` в раздел префлайт-чеков добавлена обязательная верификация актуальности `README.md` (CLI команды/примеры) и `SPEC.md` перед срезом релиза.
  - В `AGENTS.md` закреплено каноническое правило `Living Spec Invariant (No Documentation Drift)` и обновлены чеклисты режимов 0 и 3.
  - В утилите `install.py` синхронизированы шаблоны правил агентов (`_RULES_BODY`, `_3MODES`) с обязательным напоминанием о синхронизации Living Spec.
  - Задача [[02_Tasks/Specs/08_Greenfield/TASK-030-living-spec-protocol-and-skill-sync|TASK-030]] переведена в `status: done`, Канбан и Дорожная карта актуализированы.
- **Результаты верификации:**
  - `python -m unittest discover -s tests` -> 36/36 тестов успешно пройдено (100% Pass).
  - `python scripts/kb_lint.py --path docs` -> 89 файлов проверено, 654 викиссылки валидны (0 битых).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация задачи [[02_Tasks/Specs/08_Greenfield/TASK-031-kb-lint-spec-drift-audit|TASK-031]] (Эвристический контроль дрифта спецификации в `scripts/kb_lint.py` и модульные тесты в `tests/test_kb_lint.py`).

---

### [2026-10-02] — Завершение TASK-029: Пресет undecided и CLI-флаг --idea в install.py
- **Что сделано:**
  - В утилите `install.py` реализован пресет `undecided` (*"Undecided / Idea-First Research"*) с нейтральными заглушками и отложенным выбором стека через Режим 0.
  - Добавлена опция `6) 💡 Undecided / Idea-First` в интерактивное меню выбора стека.
  - Реализован CLI-флаг `--idea "<текст>"` для Greenfield-старта с одной продуктовой идеи; при его указании без флага `--stack` автоматически активируется пресет `undecided`.
  - Модифицирована функция `create_starter_docs`: при выборе пресета `undecided` мастер-спецификация `SPEC.md` создается со статусом `status: discovery`, описание идеи помещается в раздел «Концепция и цели», а в архитектурном разделе фиксируется статус TBD.
  - Обновлен финальный приветственный баннер инсталлятора, подсказывающий первый шаг: `/kb-research <исследование идеи и выбор стека>`.
  - Добавлен сквозной модульный и CLI тест `test_19_undecided_preset_and_idea_flag` в `tests/test_installer.py`.
  - Задача [[02_Tasks/Specs/08_Greenfield/TASK-029-undecided-preset-and-idea-flag|TASK-029]] переведена в `status: done`, Канбан и Дорожная карта актуализированы.
- **Результаты верификации:**
  - `python install.py --help` -> подтверждено наличие опции `--idea` и значения `undecided` в `--stack`.
  - `python -m unittest tests.test_installer.TestAgentDocsHarness.test_19_undecided_preset_and_idea_flag` -> 1/1 Pass (Exit code 0).
  - `python -m unittest discover -s tests` -> 36/36 тестов успешно пройдено (100% Pass).
  - `python scripts/kb_lint.py --path docs` -> 89 файлов проверено, 652 викиссылки валидны (0 битых).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация задачи [[02_Tasks/Specs/08_Greenfield/TASK-030-living-spec-protocol-and-skill-sync|TASK-030]] (Протокол Living Spec и синхронизация документации в скиллах `kb-research`, `kb-complete`, `kb-release` и `AGENTS.md`).

---

### [2026-10-01] — Выпуск официального релиза v0.7.0: GitHub Releases & Distribution Notes Standard (Фаза 7)
- **Что сделано:**
  - Осуществлен официальный релиз **v0.7.0** по завершении Фазы 7 (План [[02_Tasks/Plans/PLAN-007-github-release-notes-and-distribution-standard|PLAN-007]]).
  - Сформирован релизный документ [[02_Tasks/Releases/RELEASE-v0.7.0|RELEASE-v0.7.0]] и публичные заметки `dist/RELEASE_NOTES.md` с чистым GitHub Markdown и автоконвертером викиссылок.
  - Собраны релизные артефакты через хук `scripts/build_release.py`:
    - `dist/install.py` (83.3 KB / 85 310 байт) — SHA-256: `1e386242736e166e836fe5116ccbdad64dfcab48e97781f302b40e8764d68d4b`.
  - Обновлены [[02_Tasks/Roadmap|Roadmap.md]] (ссылка на официальный релиз `RELEASE-v0.7.0`) и корневой `CHANGELOG.md` (секция `[0.7.0]`).
  - Зафиксирован аннотированный Git-тег `v0.7.0`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 0 broken links.
  - `python -m unittest discover -s tests` -> 35/35 тестов успешно пройдено (Exit code 0).
  - Контрольная сумма SHA-256 `dist/install.py` подтверждена (`1e386242736e166e836fe5116ccbdad64dfcab48e97781f302b40e8764d68d4b`).

---

### [2026-10-01] — Завершение TASK-028 и Фазы 7: Сборка инсталлятора и сквозная E2E верификация
- **Что сделано:**
  - Пересобран автономный инсталлятор `install.py` через `scripts/build_installer.py`, упаковав обновленные `scripts/kb_release.py` (двухформатный экспорт заметок и автоконвертер викиссылок), воркфлоу `.github/workflows/release.yml` (`body_path: dist/RELEASE_NOTES.md`), скилл `.agents/skills/kb-release/SKILL.md` и шаблон `TEMPLATE_RELEASE.md`.
  - Дополнен тестовый набор `tests/test_installer.py` проверками наличия `body_path: dist/RELEASE_NOTES.md` в воркфлоу, флага `--notes-file dist/RELEASE_NOTES.md` в скилле `kb-release`, генерации `dist/RELEASE_NOTES.md` и корректного обновления через `install.py --update`.
  - Все задачи Фазы 7 ([[02_Tasks/Plans/PLAN-007-github-release-notes-and-distribution-standard|PLAN-007]]) — TASK-025, TASK-026, TASK-027, TASK-028 — переведены в `status: done` в ТЗ, Дорожная карта и Канбан актуализированы (Фаза 7 перемещена в `Done`).
- **Результаты верификации:**
  - `python scripts/build_installer.py` -> инсталлятор успешно пересобран (размер: 83.3 KB, сжатие: 41.9%).
  - `python -m unittest discover -s tests` -> 35/35 тестов успешно пройдено (100% Pass).
  - `python scripts/kb_lint.py --path docs` -> 77 файлов проверено, 516 викиссылок валидны (0 битых).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Приемочное тестирование Фазы 7 и выпуск публичного релиза `v0.7.0` через скилл `/kb-release`.

---

### [2026-10-01] — Завершение TASK-027: Актуализация скилла kb-release и шаблона TEMPLATE_RELEASE.md
- **Что сделано:**
  - В скилле `.agents/skills/kb-release/SKILL.md` актуализированы шаги 4 и 6:
    - Шаг 4: зафиксирована генерация внутреннего `RELEASE-vX.Y.Z.md` и публичного `dist/RELEASE_NOTES.md`.
    - Шаг 6 (GitHub Mode): команда публикации `gh release create` дополнена параметром `--notes-file dist/RELEASE_NOTES.md`.
    - Сохранена High-SNR токеномика (описание frontmatter $\le$ 15 слов).
  - В шаблонах `TEMPLATE_RELEASE.md` (в `docs/00_Templates/` и корневой `templates/`) добавлено примечание о генерации публичных заметок в `dist/RELEASE_NOTES.md`.
  - Задача [[02_Tasks/Specs/07_Distribution/TASK-027-kb-release-skill-and-notes-file|TASK-027]] переведена в `status: done` в ТЗ, Канбане (`(2026-10-01)`) и Дорожной карте (`[x]`).
- **Результаты верификации:**
  - Подтверждена идентичность файлов шаблонов в `docs/00_Templates/` и `templates/`.
  - Проверена лаконичность описания `SKILL.md` (13 слов).
  - `python scripts/kb_lint.py --path docs` -> 0 broken links.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Переход к `TASK-028`: Сборка инсталлятора `build_installer.py`, регрессионные E2E тесты и аудит целостности дистрибутива.

---

### [2026-10-01] — Завершение TASK-026: Автоматизация передачи заметок в CI release.yml и шаблоне инсталлятора
- **Что сделано:**
  - В файле `.github/workflows/release.yml` добавлен параметр `body_path: dist/RELEASE_NOTES.md` в шаг `Publish GitHub Release` (`softprops/action-gh-release@v2`). Теперь GitHub Release автоматически получает полное описание, команды быстрой установки и таблицу SHA-256 из артефакта, сгенерированного `kb_release.py --ci-mode`.
  - В `install.py` обновлен встроенный fallback-шаблон `wf_release_content` в функции `deploy_ci_workflows()` с включением `body_path: dist/RELEASE_NOTES.md`.
  - Задача [[02_Tasks/Specs/07_Distribution/TASK-026-github-actions-release-body-and-installer-template|TASK-026]] переведена в `status: done` в ТЗ, Канбане (`(2026-10-01)`) и Дорожной карте (`[x]`).
- **Результаты верификации:**
  - Проверена валидность синтаксиса `.github/workflows/release.yml` и наличие `body_path: dist/RELEASE_NOTES.md`.
  - Проверено наличие актуального шаблона воркфлоу в `install.py`.
  - `python -m unittest tests/test_kb_release.py` -> 12/12 тестов успешно пройдено.
  - `python scripts/kb_lint.py --path docs` -> 0 broken links.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Переход к `TASK-027`: Актуализация скилла `.agents/skills/kb-release/SKILL.md` (флаг `--notes-file dist/RELEASE_NOTES.md`) и шаблона `TEMPLATE_RELEASE.md`.

---

### [2026-10-01] — Завершение TASK-025: Двухформатный экспорт и автоконвертер викиссылок в scripts/kb_release.py
- **Что сделано:**
  - В утилите `scripts/kb_release.py` реализована функция `convert_wikilinks_to_github_markdown` (Zero-Dependencies):
    - Относительные викиссылки `[ [ ../Specs/... | TASK-XXX ] ]` и `[ [ ../../03_Decisions_ADR/... | ADR-XXXX ] ]` преобразуются в полноценные кликабельные URL GitHub с учетом `remote.origin.url` и ветки `main`.
    - В Local-Only режиме без удаленного репозитория ссылки безопасно сворачиваются в жирный шрифт `**Alias**`.
  - Добавлена функция `generate_public_release_notes`:
    - Формирует `dist/RELEASE_NOTES.md` в чистом GitHub Flavored Markdown (GFM) без YAML frontmatter.
    - Включает Executive Summary, блок быстрого старта (Quick Install / Upgrade) с автоопределением `raw.githubusercontent.com`, категоризированный чейнджлог (Features, Bug Fixes, ADRs), таблицу артефактов SHA-256 с командами верификации (`Get-FileHash` / `sha256sum`) и ссылку на Release diff.
  - Обновлен CLI интерфейс `main()`:
    - Добавлен аргумент `--notes-output` (по умолчанию `dist/RELEASE_NOTES.md`).
    - При обычном запуске и в `--ci-mode` генерируются оба документа: внутренний `docs/02_Tasks/Releases/RELEASE-{tag}.md` и публичный `dist/RELEASE_NOTES.md`.
    - В режиме `--dry-run` выводятся обе секции с разделителем.
  - Написаны модульные тесты в `tests/test_kb_release.py` (12 тестов, 100% pass):
    - Тестирование конвертации викиссылок (HTTPS, SSH, Local-Only fallback).
    - Тестирование структуры `dist/RELEASE_NOTES.md` и отсутствия YAML frontmatter.
    - Тестирование одновременного создания обоих файлов через CLI.
  - Задача [[02_Tasks/Specs/07_Distribution/TASK-025-dual-export-and-wikilinks-converter|TASK-025]] переведена в `status: done`.
- **Результаты верификации:**
  - `python -m unittest tests/test_kb_release.py` -> 12/12 тестов успешно пройдено.
  - `python scripts/kb_release.py --version 0.7.0 --phase 7 --dry-run` -> чистый и корректный вывод.
  - `python -m unittest discover -s tests` -> 35/35 тестов успешно пройдено.
  - `python scripts/kb_lint.py --path docs` -> 0 broken links.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Переход к `TASK-026`: Автоматизация передачи заметок в CI `release.yml` (`body_path: dist/RELEASE_NOTES.md`) и синхронизация встроенного шаблона в `install.py`.

---

### [2026-10-01] — Выпуск официального релиза v0.6.0: Discovery & Feasibility Lifecycle (Фаза 6)
- **Что сделано:**
  - Осуществлен официальный релиз **v0.6.0** по завершении Фазы 6 (План [[02_Tasks/Plans/PLAN-006-discovery-mode-and-kb-research-lifecycle|PLAN-006]]).
  - Сформирован релизный документ [[02_Tasks/Releases/RELEASE-v0.6.0|RELEASE-v0.6.0]] по каноническому стандарту `TEMPLATE_RELEASE.md`.
  - Собраны релизные артефакты через хук `scripts/build_release.py`:
    - `dist/install.py` (81.5 KB / 83 499 байт) — SHA-256: `132776da84c4820caf3359598ec827594d541927bd6c857b7a8ee16647d03a7f`.
  - Обновлены [[02_Tasks/Roadmap|Roadmap.md]] (ссылка на официальный релиз `RELEASE-v0.6.0`) и корневой `CHANGELOG.md` (секция `[0.6.0]`).
  - Зафиксирован аннотированный Git-тег `v0.6.0`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 0 broken links.
  - `python -m unittest discover -s tests` -> 31/31 тест успешно пройден (Exit code 0).
  - Контрольная сумма SHA-256 `dist/install.py` подтверждена (`132776da84c4820caf3359598ec827594d541927bd6c857b7a8ee16647d03a7f`).

---

### [2026-10-01] — Завершение TASK-024 и Фазы 6: Синхронизация инсталлятора, E2E тесты и аудит целостности
- **Что сделано:**
  - Запущена пересборка автономного инсталлятора `scripts/build_installer.py`:
    - Все обновленные шаблоны (`TEMPLATE_ROADMAP.md`, `TEMPLATE_ONBOARDING.md`) и скиллы (`kb-research`, `kb-plan`, `kb-onboard`) сжаты и упакованы в `install.py` (размер дистрибутива 81.5 KB, полезная нагрузка ассетов 71.4 KB).
  - Актуализирован тестовый набор `tests/test_installer.py`:
    - Добавлен сквозной регрессионный тест `test_18_discovery_mode_and_phase6_assets` для верификации упаковки артефактов Режима 0 (Discovery & Feasibility), двухпутевой воронки в `kb-research`, префлайт-чеков в `kb-plan` и секций отклоненных альтернатив.
    - Адаптированы бенчмарки токеномики High-SNR (`test_16_high_snr_static_corpus_benchmarks`) под обновленные шаблоны с сохранением строгого лимита `total_templates_size <= 21000`.
  - Закрыта задача `TASK-024` в спецификации (`status: done`), Канбане (`## ✅ Готово`) и Дорожной карте (`[x]`).
  - Успешно завершена **Фаза 6: Интеграция этапа исследования (Режим 0: Discovery & Feasibility) и эволюция /kb-research** (`PLAN-006` переведен в `status: completed`).
- **Результаты верификации:**
  - `python scripts/build_installer.py` -> Payload 73 148 bytes, `install.py` 83 490 bytes (Exit code 0).
  - `python -m unittest discover -s tests` -> 31/31 тест успешно пройден (100% pass, Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 0 broken links (71 files scanned, 438 wikilinks verified).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Релиз версии `v0.6.0` через команду `/kb-release v0.6.0` (Dual-Mode: Local-Only / GitHub tag & Release Notes).

---

### [2026-10-01] — Завершение TASK-023: Обновление шаблонов TEMPLATE_ROADMAP, TEMPLATE_ONBOARDING и руководства Onboarding.md
- **Что сделано:**
  - Синхронизированы канонические шаблоны в `docs/00_Templates/` и корневом `templates/`:
    - `TEMPLATE_ROADMAP.md`: внедрен ориентирующий комментарий для секции Icebox (рекомендация использовать `/kb-research <идея>` вместо ручной правки) и добавлена секция `## 🚫 Отклоненные архитектурные идеи (Rejected Alternatives)`.
    - `TEMPLATE_ONBOARDING.md`: матрица режимов обновлена до 4-этапного цикла (Режим 0: Исследование / Discovery, Режимы 1–3: Delivery), команды `/kb-research` и `/kb-adr` добавлены в справочник, процесс Brownfield Adoption расширен до 4 этапов.
  - Обновлено руководство `docs/Onboarding.md`:
    - Mermaid диаграмма жизненного цикла обновлена (модель Double Diamond: Режим 0 $\to$ Режимы 1–3).
    - Добавлен подраздел с описанием **Режима 0: Исследование и валидация гипотез (Discovery & Feasibility)**.
  - Закрыта задача `TASK-023` в спецификации (`status: done`), Канбане (`## ✅ Готово`) и Дорожной карте (`[x]`).
  - В `Kanban.md` задача `TASK-024` переведена в колонку `## ⏳ В работе (In Progress)`.
- **Результаты верификации:**
  - Проверена строгая побайтовая идентичность шаблонов `docs/00_Templates/` и `templates/` (100% совпадение).
  - `python scripts/kb_lint.py --path docs` -> 0 broken links (71 files scanned, 438 wikilinks verified).
  - `python -m unittest discover -s tests` -> 30/30 тестов успешно пройдены (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-024`: пересборка дистрибутива `install.py` через `scripts/build_installer.py`, регрессионные E2E тесты и аудит целостности.

---

### [2026-10-01] — Завершение TASK-022: Префлайт-чеки в kb-plan и 4-этапный цикл в kb-onboard
- **Что сделано:**
  - Обновлен скилл `.agents/skills/kb-plan/SKILL.md`:
    - Внедрен предупреждающий фильтр **Pre-flight Nudge** в шаге 1 процедуры (Intent Routing): при передаче рискованной идеи, затрагивающей внешние зависимости (ADR-0001) или платформенные неопределенности, агент рекомендует сначала выполнить исследование и фальсификацию в Режиме 0 (`/kb-research <idea>`).
  - Обновлен скилл `.agents/skills/kb-onboard/SKILL.md`:
    - Онбординг-шпаргалка актуализирована с 3-режимного до **4-этапного жизненного цикла (Discovery + Delivery)**.
    - В матрицу команд включен **Режим 0 (Discovery & Feasibility)**: `/kb-research` (стресс-тесты, бенчмарки, синхронизация с Icebox) и `/kb-adr` (фиксация архитектурных решений и отказных альтернатив).
  - Закрыта задача `TASK-022` в спецификации (`status: done`), Канбане (`## ✅ Готово`) и Дорожной карте (`[x]`).
  - В `Kanban.md` задача `TASK-023` переведена в колонку `## ⏳ В работе (In Progress)`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 0 broken links (71 files scanned, 437 wikilinks verified).
  - `python -m unittest discover -s tests` -> 30/30 тестов успешно пройдены (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-023`: обновление шаблонов `TEMPLATE_ROADMAP.md`, `TEMPLATE_ONBOARDING.md` и руководства `Onboarding.md`.

---

### [2026-10-01] — Завершение TASK-021: Эволюция скилла kb-research и маршрутизация гипотез в Roadmap
- **Что сделано:**
  - Обновлен исполняемый скилл `.agents/skills/kb-research/SKILL.md` согласно спецификации [[02_Tasks/Specs/06_Discovery/TASK-021-kb-research-evolution-and-roadmap-routing|TASK-021]]:
    - Скилл преобразован в канонический инструмент **Режима 0 (Discovery & Feasibility)** модели Double Diamond (согласно [[03_Decisions_ADR/ADR-0012-discovery-mode-and-kb-research-lifecycle-integration|ADR-0012]] и [[04_Research/RESEARCH-007-discovery-mode-and-kb-research-lifecycle-integration|RESEARCH-007]]).
    - Расширен фокус: от узких платформенных дефектов к полноценной валидации продуктовых и архитектурных гипотез с критическим партнерством агента (Senior Partner: обязательная фальсификация, риски Zero-Deps, токеномика).
    - Внедрена двухпутевая автоматическая воронка интеграции с [[02_Tasks/Roadmap|Roadmap.md]]:
      - Одобренные инициативы $\to$ автоматическая регистрация в `## 🔮 Перспективные направления (Future Horizons / Icebox)` с оценкой ценности (Value Impact).
      - Отклоненные инициативы $\to$ фиксация отказного ADR (`status: rejected`) через `/kb-adr` и регистрация в `## 🚫 Отклоненные архитектурные идеи (Rejected Alternatives)`.
    - Сохранена High-SNR токеномика: микро-описание frontmatter $\le$ 15 слов, компактные императивные формулировки.
  - Закрыта задача `TASK-021` в спецификации (`status: done`), Канбане (`## ✅ Готово`) и Дорожной карте (`[x]`).
  - В `Kanban.md` задача `TASK-022` переведена в колонку `## ⏳ В работе (In Progress)`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 0 broken links (71 files scanned, 433 wikilinks verified).
  - `python -m unittest discover -s tests` -> 30/30 тестов успешно пройдены (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-022`: префлайт-чеки в `/kb-plan` и актуализация онбординг-скилла `/kb-onboard`.

---

### [2026-10-01] — Выпуск официального релиза v0.5.0: High-SNR Token Architecture (Фаза 5)
- **Что сделано:**
  - Осуществлен официальный релиз **v0.5.0** по завершении Фазы 5 (План [[02_Tasks/Plans/PLAN-005-high-snr-token-optimization|PLAN-005]]).
  - Сформирован релизный документ [[02_Tasks/Releases/RELEASE-v0.5.0|RELEASE-v0.5.0]] по каноническому стандарту `TEMPLATE_RELEASE.md`.
  - Собраны релизные артефакты через хук `scripts/build_release.py`:
    - `dist/install.py` (81.2 KB / 83 119 байт) — SHA-256: `04d88c2a1f5c10bb0e2b4bb0f1715d6af377aaffd3cfed3843a6b51183d5707d`.
  - Обновлены [[02_Tasks/Roadmap|Roadmap.md]] (статус Фазы 5 переведен в `✅ Завершена`) и корневой `CHANGELOG.md`.
  - Зафиксирован аннотированный Git-тег `v0.5.0`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 0 broken links (60 files scanned, 331 wikilinks verified).
  - `python -m unittest discover -s tests` -> 30/30 тестов успешно пройдены (Exit code 0).
  - Контрольная сумма SHA-256 `dist/install.py` подтверждена.

---

### [2026-10-01] — Завершение TASK-020: Синхронизация сборщика, install.py (--update) и E2E тесты (Завершение Фазы 5)
- **Что сделано:**
  - Полностью завершена **Фаза 5: Оптимизация токенов и High-SNR архитектура контекста**:
    - Перепакован автономный монолитный инсталлятор `install.py` через `scripts/build_installer.py`:
      - В бандл включены все 13 компактных шаблонов `templates/`, 12 High-SNR скиллов `.agents/skills/`, утилиты `scripts/kb_lint.py` и `scripts/kb_release.py`.
      - Размер итогового дистрибутива `install.py` сократился с 98.6 КБ до **81.2 КБ** (-17.6%).
    - Функция `customize_templates_for_stack` адаптирована для бесшовной параметризации новых компактных Skeleton Templates под все поддерживаемые стеки (Swift, TS, Python, .NET, Generic).
    - В `install.py` расширен механизм бережного обновления (`update_harness`) с поддержкой флага `backup=True/False`.
    - В `tests/test_installer.py` добавлены E2E тесты бенчмаркинга (`test_16_high_snr_static_corpus_benchmarks`) и верификации миграции устаревших проектов (`test_17_update_migrates_to_skeleton_templates_and_high_snr_skills`):
      - Общий размер 12 скиллов: $\le$ 20 000 байт (фактически ~18.9 КБ vs лимит 20 КБ).
      - Общий размер 13 шаблонов: $\le$ 21 000 байт (фактически ~20.0 КБ vs лимит 21 КБ).
      - Размер `TEMPLATE_ONBOARDING.md`: $\le$ 4 000 байт (фактически 3.8 КБ).
      - Размер роутера `docs-as-code/SKILL.md`: $\le$ 3 000 байт (фактически 2.2 КБ).
      - Размер дистрибутива `install.py`: $\le$ 100 000 байт (фактически 81.2 КБ).
    - Актуализирована документация: в `README.md`, `docs/Onboarding.md` и `docs/00_Index.md` отражен стандарт High-SNR Token Architecture.
    - В `scripts/kb_lint.py` расширен список игнорируемых русскоязычных плейсхолдеров (`заметка`, `документ`, `файл`, `slug`).
  - Закрыта задача `TASK-020` и завершен план `PLAN-005` в `Kanban.md`, `Roadmap.md` и спецификации.
- **Результаты верификации:**
  - `python scripts/build_installer.py` -> 13 шаблонов, 12 скиллов, 2 скрипта, 81.2 КБ payload (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> `OK: 59 files scanned, 315 wikilinks verified (0 broken).` (Exit code 0).
  - `python -m unittest discover -s tests` -> 30/30 тестов успешно пройдены (100% pass, Exit code 0).
  - Тестовая установка в изолированную директорию подтвердила работоспособность и чистоту создаваемого проекта.
- **Итог Фазы 5:**
  - Достигнуто радикальное сжатие контекстной нагрузки на 55–65% за сессию при 100% сохранении инженерных гарантий, 3-режимного цикла и интерактивного графа Obsidian.

---

### [2026-10-01] — Завершение TASK-019: Внедрение правил High-SNR, Anti-Echo и Silent-CLI (Фаза 5)
- **Что сделано:**
  - Реализованы Правила 3 (Anti-Echo Response Protocol), 4 (DRY Rules Hierarchy) и 6 (Silent-on-Success CLI) из [[03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]]:
    - В `AGENTS.md` и генератор правил `install.py` внедрен строгий протокол **Anti-Echo Response Protocol**: полный запрет на повторную распечатку содержимого файлов в чате; обязательный компактный формат (кликабельный permalink `[FileName](file:///...)` + резюме из 3–5 пунктов + следующий шаг).
    - В `AGENTS.md` и `install.py` внедрена полная явная таблица 7-цветовой схемы Obsidian Graph (`.obsidian/graph.json`) и тегов (`#arch`, `#adr`, `#research`, `#task`, `#bug`, `#testing`).
    - В утилите `scripts/kb_lint.py` реализован режим Silent-on-Success: при успешной проверке выводится ровно одна строка (`OK: N files scanned, M wikilinks verified (0 broken).`), добавлен флаг `--verbose` (`-v`) для вывода полного аудита; ошибки выводятся развернуто.
    - В утилите `scripts/kb_release.py` реализован лаконичный однострочный вывод успешной генерации релиза и добавлен флаг `--verbose` (`-v`).
    - Создан набор модульных тестов `tests/test_kb_lint.py` (5 тестов: Silent-on-Success, Verbose, обнаружение битых wikilinks, ошибки YAML frontmatter, CLI флаги).
  - Закрыта задача `TASK-019` в `Kanban.md`, `Roadmap.md` и спецификации.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> `OK: 59 files scanned, 313 wikilinks verified (0 broken).` (1 строка, Exit code 0).
  - `python scripts/kb_lint.py --path docs --verbose` -> полный лог аудита, Exit code 0.
  - `python -m unittest tests/test_kb_lint.py` -> 5/5 тестов зеленые.
  - `python -m unittest discover -s tests` -> 28/28 тестов зеленые.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-020`: Синхронизация сборщика `scripts/build_installer.py`, `install.py` (`--update`), E2E тесты и замеры сжатия.

---

### [2026-10-01] — Завершение TASK-018: Рефакторинг 13 шаблонов docs/00_Templates/ в компактные каркасы (Фаза 5)
- **Что сделано:**
  - Реализовано Правило 5 (Skeleton Templates) архитектурного стандарта [[03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]]:
    - Все 13 шаблонов `docs/00_Templates/` очищены от обучающих эссе, вербального шума и пространных рассуждений, замененных на точечные однострочные директивы `<!-- prompt / instruction -->`.
    - Шаблон `TEMPLATE_ONBOARDING.md` радикально сжат с 11 423 байт до 3 567 байт (-68.8%), превратившись в высокоэффективную шпаргалку по онбордингу без «воды».
    - Сохранена 100% структурная целостность: YAML frontmatter, канонические разделы, интерактивные чеклисты `- [ ]` и связность графа Obsidian.
  - Суммарный объем 13 шаблонов сокращен с 38 774 байт до 19 712 байт (-49.2%), что укладывается в бюджет $\le$ 21 000 байт.
  - Закрыта задача `TASK-018` в `Kanban.md` и отмечен пункт в `Roadmap.md`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 59 файлов, 312 ссылок, 0 broken links, 100% валидный YAML frontmatter.
  - `python -m unittest discover -s tests` -> 23/23 тестов зеленые.
  - Замер размера шаблонов: 19 712 байт $\le$ 21 000 байт; `TEMPLATE_ONBOARDING.md`: 3 567 байт $\le$ 4 000 байт.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Переход к `TASK-019`: Внедрение правил High-SNR, Anti-Echo протокола и Silent-CLI в `AGENTS.md`, `scripts/kb_lint.py` и `scripts/kb_release.py`.

---

### [2026-10-01] — Завершение TASK-017: High-SNR рефакторинг реестра и 12 скиллов .agents/skills/ (Фаза 5)
- **Что сделано:**
  - Реализованы Правила 1, 2, 4 и 6 архитектурного стандарта [[03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]]:
    - Сжаты Always-On описания в YAML frontmatter всех 12 скиллов до лаконичных Micro-Descriptions (10–13 слов), что снижает постоянный налог системного реестра на 53% (~194 токена вместо ~410 токенов на каждом шаге диалога).
    - Монолитный скилл `docs-as-code/SKILL.md` рефакторен в компактный высокоуровневый роутер Progressive Disclosure: размер снижен с 13 775 байт до 2 274 байт (-83.5%).
    - Все 11 специализированных скиллов (`kb-plan`, `kb-task`, `kb-implement`, `kb-complete`, `kb-release`, `kb-bug`, `kb-adr`, `kb-research`, `kb-init`, `kb-lint`, `kb-onboard`) очищены от словесного шума, эмоциональной риторики и дублирования `AGENTS.md`. Инструкции переведены в строгий императивный формат (`CONSTRAINT: ...`, `PROCEDURE: ...`).
  - Суммарный объем 12 файлов `SKILL.md` сокращен с 42 445 байт до 18 728 байт (-55.9%), полностью уложившись в бюджет $\le$ 20 000 байт.
  - Закрыта задача `TASK-017` в `Kanban.md` и отмечен пункт в `Roadmap.md`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 59 файлов, 311 ссылок, 0 broken links, 100% валидный YAML.
  - `python -m unittest discover -s tests` -> 23/23 тестов зеленые.
  - Проверка суммарного размера скиллов: 18 728 байт $\le$ 20 000 байт.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Переход к `TASK-018`: Рефакторинг 13 шаблонов `docs/00_Templates/` в компактные каркасы (Skeleton Templates).

---

### [2026-10-01] — Завершение TASK-016: Комплексное E2E тестирование релизного пайплайна и документация (Завершение Фазы 4)
- **Что сделано:**
  - Написаны и интегрированы 3 сквозных E2E теста в `tests/test_installer.py`:
    - `test_13_release_components_deployed_on_fresh_install`: верификация развертывания `docs/02_Tasks/Releases/`, `TEMPLATE_RELEASE.md`, `scripts/kb_release.py`, скилла `kb-release` и воркфлоу `release.yml`.
    - `test_14_kb_release_utility_execution_in_sandbox`: генерация релиза, расчет потокового SHA-256 артефакта в `dist/` и проверка генерации `RELEASE-v1.0.0.md` с аудитом через `kb_lint.py`.
    - `test_15_update_preserves_existing_releases`: верификация бережного обновления через `install.py --update` (обновление шаблонов/скиллов при 100% сохранении существующих заметок `docs/02_Tasks/Releases/RELEASE-*.md`).
  - Синхронизирована пользовательская и агентная документация:
    - `README.md`: добавлена 13-я позиция каталога шаблонов (`TEMPLATE_RELEASE.md`), папка `Releases/`, 12-й скилл `/kb-release`, команды запуска `scripts/kb_release.py` и раздел Dual-Mode автоматизации релизов.
    - `docs/Onboarding.md`: добавлен раздел «3. Релиз-менеджмент и жизненный цикл (`/kb-release`)» с диаграммой каналов выпуска (Dual-Mode: GitHub / Local-Only), Pre-flight чеками и Build Hook Contract.
    - `docs/00_Index.md`: актуализирована карта разделов, добавлен раздел `Releases/` и шаблон `TEMPLATE_RELEASE.md`.
  - Закрыта задача `TASK-016` и полностью завершена **Фаза 4 («Релиз-менеджмент и автоматизация жизненного цикла»)** в `Kanban.md` и `Roadmap.md`.
- **Результаты верификации:**
  - `python -m unittest discover -s tests` -> 23/23 тестов успешно пройдены (100% pass).
  - `python scripts/kb_lint.py --path docs` -> 54 файла, 260 ссылок, 0 broken links, 100% валидный YAML frontmatter.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Выполнение приемочных сценариев в `docs/05_Testing/` и публикация первого официального релиза Фазы 4 через `/kb-release`.

---

### [2026-10-01] — Завершение TASK-015: Шаблон GitHub Actions CI release.yml и упаковка релизных компонентов в инсталлятор
- **Что сделано:**
  - Разработан эталонный GitHub Actions workflow `.github/workflows/release.yml` для автоматической сборки и публикации релизов по push аннотированных тегов `v*`:
    - Проверка целостности базы знаний через `scripts/kb_lint.py --path docs`.
    - Обнаружение и запуск билд-хука (`scripts/build_release.sh`, `scripts/build_release.py`, `package.json`).
    - Инспекция артефактов в `dist/` и валидация контрольных сумм через `scripts/kb_release.py --ci-mode`.
    - Публикация GitHub Release через `softprops/action-gh-release@v2`.
  - Скопирован `TEMPLATE_RELEASE.md` в корень `templates/`.
  - Обновлен сборочный скрипт `scripts/build_installer.py`:
    - Бандлинг всех 13 шаблонов (включая `TEMPLATE_RELEASE.md`).
    - Бандлинг утилит `scripts/kb_lint.py` и `scripts/kb_release.py`.
    - Бандлинг 12 скиллов агентов (включая `kb-release`).
    - Бандлинг CI воркфлоу `.github/workflows/*.yml`.
  - Обновлен автономный инсталлятор `install.py`:
    - Создание каталога `docs/02_Tasks/Releases/` с `.gitkeep`.
    - Развертывание `scripts/kb_release.py` с правами 0o755 в `deploy_infrastructure`.
    - Развертывание `.github/workflows/release.yml` и `kb-lint.yml` в `deploy_ci_workflow`.
    - Безопасное обновление через `install.py --update`: переразвертывание шаблонов, утилит и скиллов при строгом сохранении существующих пользовательских релизов в `docs/02_Tasks/Releases/`.
    - Перекомпилирован монолитный бандл в `install.py`: размер 95.0 КБ (в рамках бюджета < 120 КБ).
  - Закрыта задача `TASK-015` в `Kanban.md`, `Roadmap.md` и спецификации.
- **Результаты верификации:**
  - `python -m py_compile scripts/build_installer.py install.py` -> Код 0.
  - `python scripts/build_installer.py` -> 13 шаблонов, 12 скиллов, 2 скрипта, 95.0 КБ бандл.
  - `python scripts/kb_lint.py --path docs` -> 52 файла, 239 ссылок, 0 broken links, 100% валидный YAML frontmatter.
  - `python -m unittest discover -s tests` -> 20/20 тестов успешно пройдены (100% pass).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-016`: Комплексное E2E тестирование релизного пайплайна (Local-Only и GitHub) и обновление документации (`README.md`, `Onboarding.md`, `00_Index.md`).

---

### [2026-10-01] — Завершение TASK-014: Исполняемый скилл kb-release и фазовые подсказки в kb-complete
- **Что сделано:**
  - Создан 12-й канонический исполняемый скилл `.agents/skills/kb-release/SKILL.md` со строгим 7-шаговым регламентом выпуска релизов фаз:
    1. Pre-flight Checks (проверка чистоты рабочей копии Git, прохождения `kb_lint.py`, тестов и закрытия задач фазы в `Roadmap.md`).
    2. Dual-Mode Detection (`github` через `gh` CLI или `local-only`).
    3. Build Hook Discovery (`scripts/build_release.py`, `package.json`, `pyproject.toml`, `Package.swift`, `*.sln`, `Cargo.toml`).
    4. Artifacts Inspection & SHA-256 (вызов `scripts/kb_release.py` и генерация `RELEASE-vX.Y.Z.md`).
    5. Knowledge Base Sync (`Roadmap.md`, `CHANGELOG.md`, `Devlog.md`).
    6. Publication (Git tag, `gh release create` или отчет о локальных файлах).
    7. Validation (`kb_lint.py`).
  - В скилл `.agents/skills/kb-complete/SKILL.md` добавлен шаг 7 «Phase Completion Nudge»: если при закрытии задачи все тикеты текущей фазы выполнены, выводится рекомендация провести E2E тестирование и вызвать `/kb-release`.
  - В мастер-скилл `.agents/skills/docs-as-code/SKILL.md` добавлена строка `/kb-release` и обновлена карта разделов.
  - Закрыта задача `TASK-014` в `Kanban.md`, `Roadmap.md` и спецификации.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 52 файла, 239 ссылок, 0 broken links, 100% валидный YAML frontmatter.
  - `python -m unittest discover -s tests` -> 20/20 тестов успешно пройдены (100% pass).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-015`: Шаблон GitHub Actions CI `.github/workflows/release.yml` и упаковка в инсталлятор `install.py` / `build_installer.py` (включая `--update`).

---

### [2026-10-01] — Завершение TASK-013: Шаблон релиза, каталог Releases/ и утилита scripts/kb_release.py
- **Что сделано:**
  - Создан канонический 13-й шаблон `docs/00_Templates/TEMPLATE_RELEASE.md` для фиксации релизов фаз с метаданными, чейнджлогом, таблицей артефактов и контрольными суммами SHA-256.
  - Создан постоянный каталог `docs/02_Tasks/Releases/` с правилом неизменяемости ссылок (Permalinks).
  - Разработана автономная Zero-Dependencies CLI-утилита `scripts/kb_release.py` на стандартной библиотеке Python 3:
    - Детекция окружения (`detect_release_environment`): статус git, чистота рабочего дерева, remote origin, `gh` CLI и режим (`github` | `local-only`).
    - Инспекция каталога `dist/` (`inspect_release_artifacts`): расчет размеров и потоковых SHA-256 хэшей блоками по 64 КБ.
    - Семантический сбор артефактов фазы (`find_phase_artifacts`): извлечение выполненных `TASK-XXX`, закрытых `BUG-XXX` и принятых `ADR-XXXX` из базы знаний.
    - Генерация markdown-документа релиза по стандарту `TEMPLATE_RELEASE.md`.
    - CLI интерфейс с флагами `--version`, `--phase`, `--dist-dir`, `--docs-dir`, `--output`, `--summary`, `--dry-run`, `--detect-only`.
  - Создан набор модульных тестов `tests/test_kb_release.py` (8 тестов: SHA-256, Markdown-таблица, парсер frontmatter, сбор артефактов фазы, CLI).
  - Закрыта задача `TASK-013` в `Kanban.md`, `Roadmap.md` и спецификации.
- **Результаты верификации:**
  - `python -m py_compile scripts/kb_release.py` -> Код 0.
  - `python -m unittest tests/test_kb_release.py` -> 8/8 тестов успешно пройдены (100% pass).
  - `python -m unittest discover -s tests` -> 20/20 тестов успешно пройдены (100% pass).
  - `python scripts/kb_lint.py --path docs` -> 52 файла, 239 ссылок, 0 broken links, 100% валидный YAML frontmatter.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-014`: Исполняемый скилл `.agents/skills/kb-release/SKILL.md` (Dual-Mode workflow, префлайт-чеки, подсказка в `kb-complete`).

---

### [2026-10-01] — Завершение TASK-012 и полное закрытие Фазы 3: Зрелость инсталлятора
- **Что сделано:**
  - Реализован генератор workflow для GitHub Actions `deploy_ci_workflow` в `install.py`, создающий `.github/workflows/kb-lint.yml` для автоматического аудита базы знаний через `kb_lint.py` при Push и Pull Request.
  - Добавлен CLI-флаг `--ci` со значениями `github` и `none` (по умолчанию `none`).
  - В интерактивный CLI-мастер добавлен шаг выбора настройки CI.
  - Поддержано автоматическое развертывание и обновление CI-workflow при использовании `install.py --update`.
  - Произведена оптимизация размера `install.py` (компактизация пресетов стека `STACK_PRESETS` и унификация генераторов правил через `_gen_rule`), итоговый размер дистрибутива: **80.4 КБ / 82,334 байта** (с запасом внутри бюджета < 82 КБ).
  - В `tests/test_installer.py` добавлен сквозной тест `test_12_ci_workflow_generation_and_e2e`, верифицирующий отсутствие CI по умолчанию, создание при `--ci github`, работу через CLI и сохранение/обновление при `--update`.
  - Обновлена документация `README.md` (разделы по CLI-флагам, безопасному обновлению, интеграции в существующие проекты и CI).
  - Закрыты все 4 задачи Фазы 3 (`TASK-009`, `TASK-010`, `TASK-011`, `TASK-012`) и родительский план `PLAN-003`.
- **Результаты верификации:**
  - `python -m py_compile install.py` -> Код 0.
  - `python scripts/build_installer.py` -> Код 0 (размер 80.4 КБ / 82,334 байта).
  - `python -m unittest discover -s tests` -> 12/12 тестов успешно пройдены (100% pass).
  - `python scripts/kb_lint.py --path docs` -> 44 файла, 174 ссылки, 0 broken links, 100% валидный YAML frontmatter.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Переход к перспективным идеям из бэклога / Icebox: автоматизация релиз-менеджмента (`/kb-release`, `RESEARCH-002`, `ADR-0007`) или семантический контроль фаз в `kb_lint.py`.

---

### [2026-10-01] — Завершение TASK-011: Safe Infrastructure Update Mechanism (`install.py --update`)
- **Что сделано:**
  - Реализован флаг `--update` (`-u`) в CLI `install.py` для обновления инфраструктуры базы знаний в уже существующих проектах.
  - Разделены зоны ответственности при обновлении:
    - Обновляемые компоненты: шаблоны (`docs/00_Templates/*`), линтер (`scripts/kb_lint.py`), скиллы (`.agents/skills/*`), цветовая схема графа Obsidian (`.obsidian/graph.json`).
    - Неприкосновенные пользовательские данные: `docs/02_Tasks/*` (Kanban, Roadmap, планы, ТЗ, отчеты о багах), `docs/03_Decisions_ADR/*`, `docs/04_Research/*`, `docs/05_Testing/*`, `SPEC.md`, `README.md`, `.gitignore`, `00_Index.md`.
  - Реализован механизм защиты кастомных правил агентов: если пользователь модифицировал `AGENTS.md` (или другие конфигурации агентов), автоматически создается резервная копия `*.bak` перед обновлением.
  - Реализована автоматическая фиксация обновления в `docs/Devlog.md` и последующий запуск контрольного аудита линтером `scripts/kb_lint.py`.
  - Произведен рефакторинг общих модулей в `install.py` (`deploy_infrastructure`, `run_linter_audit`, `get_agent_rule_specs`, сжатие `_3MODES`), позволивший удержать итоговый размер однофайлового дистрибутива в пределах бюджета: 81.8 КБ / 83,770 байт (лимит < 82 КБ).
  - В `tests/test_installer.py` добавлен сквозной E2E тест `test_11_safe_update_mechanism`, проверяющий валидацию директории, обновление шаблонов/линтера, неприкосновенность пользовательских задач, создание `AGENTS.md.bak`, добавление записи в `Devlog.md` и успешный прогон `kb_lint.py`.
- **Результаты верификации:**
  - `python -m py_compile install.py` -> Код 0.
  - `python scripts/build_installer.py` -> Код 0 (размер 81.8 КБ).
  - `python -m unittest discover -s tests` -> 11/11 тестов успешно пройдены (100% pass).
  - `python scripts/kb_lint.py --path docs` -> 44 файла, 174 ссылки, 0 broken links, 100% валидный YAML frontmatter.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-012`: Шаблон GitHub Actions CI (`.github/workflows/kb-lint.yml`) и E2E тесты.

---

### [2026-10-01] — Завершение TASK-010: Brownfield Adoption & Smart Stack Autodetection
- **Что сделано:**
  - Реализован эвристический детектор стека технологий `detect_project_stack` в `install.py`, определяющий Swift (`Package.swift`), Web/TypeScript (`package.json`), Python (`pyproject.toml`, `requirements.txt`, `Pipfile`, `setup.py`), .NET (`*.sln`, `*.csproj`) и fallback на Generic.
  - Реализован неразрушающий механизм внедрения в существующие проекты (Brownfield Adoption):
    - `handle_readme`: сохраняет исходный пользовательский `README.md` и бережно дописывает блок Docs-as-Code (с поддержкой мультиязычности `ru`/`en`), предотвращая дублирование при повторных запусках.
    - `handle_gitignore`: сохраняет пользовательские правила игнорирования и дописывает правила для Obsidian (`.obsidian/*`, `!.obsidian/graph.json`).
    - `create_starter_docs`: защищает существующие `SPEC.md`, `Kanban.md`, `Roadmap.md`, `Devlog.md` и `00_Index.md` от перезаписи, если не указан флаг `--force`.
  - В интерактивный CLI-мастер добавлена подсветка и предвыбор автоопределенного стека по умолчанию. В CLI поддержан параметр `--stack auto`.
  - В шаблон онбординга `TEMPLATE_ONBOARDING.md` добавлен раздел 7 («Внедрение в существующий проект») со сценарием экспресс-аудита легаси-кода для AI-агента.
  - В `tests/test_installer.py` добавлен сквозной E2E тест `test_10_brownfield_adoption_and_stack_autodetect`, верифицирующий детект всех 5 стеков, неразрушающее внедрение и идемпотентность.
  - Сборщик `scripts/build_installer.py` пересобрал бандл (размер `install.py`: 80.3 КБ / 82,204 байта, строго в рамках бюджета < 82 КБ).
- **Результаты верификации:**
  - `python -m py_compile install.py` -> Код 0.
  - `python scripts/build_installer.py` -> Код 0.
  - `python -m unittest discover -s tests` -> 10/10 тестов успешно пройдены (100% pass).
  - `python scripts/kb_lint.py --path docs` -> 44 файла, 174 ссылки, 0 broken links, 100% валидный YAML frontmatter.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-011`: Механизм бережного обновления инфраструктуры (`install.py --update`).

---

### [2026-10-01] — Завершение TASK-009: Clean Slate Scaffolding & Zero-Broken-Links FTUE
- **Что сделано:**
  - В `install.py` (`create_starter_docs`) полностью исключена генерация фантомных ссылок на несуществующие файлы `PLAN-001` и `TASK-001` в `Kanban.md` и `Roadmap.md`.
  - Стартовый бэклог в `Kanban.md` теперь создается чистым, с комментарием-приглашением начать работу с `/kb-plan <название>`.
  - `Roadmap.md` генерирует чистую структуру Фазы 1 без битых ссылок.
  - Удалена паразитная генерация фиктивных файлов планов и ТЗ в каталогах `Plans/` и `Specs/`.
  - Обновлены канонические шаблоны `templates/TEMPLATE_KANBAN.md`, `templates/TEMPLATE_ROADMAP.md` и пересобран бандл через `build_installer.py` (размер дистрибутива `install.py`: 75.9 КБ / 77,684 байта).
  - В тестовый набор `tests/test_installer.py` добавлен сквозной тест `test_09_clean_slate_scaffolding`, проверяющий чистоту бэклога и успешное прохождение аудита `kb_lint.py` с 0 битых ссылок при первой установке.
- **Результаты верификации:**
  - `python -m py_compile install.py` -> Код 0.
  - `python scripts/build_installer.py` -> Код 0.
  - `python -m unittest discover -s tests` -> 9/9 тестов успешно пройдены (100% pass).
  - `python scripts/kb_lint.py --path docs` -> 44 файла, 174 ссылки, 0 broken links, 100% валидный YAML frontmatter.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-010`: Бесшовное внедрение в существующие проекты (Brownfield Adoption) и автодетект стека.

---

### [2026-10-01] — Режим 1: Планирование Фазы 3 и фиксация отказных архитектурных решений (ADR-0005, ADR-0006)
- **Что сделано:**
  - Проведен критический анализ бэклога перспективных идей из `Roadmap.md` и `Kanban.md` с позиции Senior Partner.
  - Идеи категории C официально отклонены как оверинжиниринг и зафиксированы в отказных архитектурных решениях (`status: rejected`):
    - [[03_Decisions_ADR/ADR-0005-rejection-of-embedded-web-visualizer|ADR-0005]]: Отказ от встроенного локального web-визуализатора базы знаний (`install.py --serve`) во избежание раздувания бандла, нарушения Zero Dependencies и дублирования нативного Obsidian.
    - [[03_Decisions_ADR/ADR-0006-rejection-of-standalone-pdf-report-generator|ADR-0006]]: Отказ от встроенного Python-генератора PDF-отчетов в пользу нативных возможностей LLM/агентов и штатного экспорта Markdown.
  - Сформирован и утвержден концептуальный план Фазы 3: [[02_Tasks/Plans/PLAN-003-brownfield-adoption-and-lifecycle|PLAN-003]] («Зрелость инсталлятора — Brownfield Adoption, Clean Slate Scaffolding, безопасное обновление и CI»).
  - Декомпозированы задачи Фазы 3 (`TASK-009` — `TASK-012`), добавлены карточки в бэклог [[02_Tasks/Kanban|Kanban.md]] и вехи в [[02_Tasks/Roadmap|Roadmap.md]].
  - Запущена проверка целостности базы знаний через `python scripts/kb_lint.py --path docs`: 0 broken wikilinks, 100% валидность frontmatter.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Переход к Режиму 2 (Task Specification) для первой задачи `TASK-009` (Clean Slate Scaffolding).

---

### [2026-09-30] — Завершение TASK-008 и успешное закрытие Фазы 2 (Скиллы, правила и экосистема)
- **Что сделано:**
  - В тестовый набор `tests/test_installer.py` добавлены 3 новых сквозных E2E теста:
    - `test_06_install_deploys_all_11_skills`: проверяет корректное развертывание каталога `.agents/skills/`, наличие всех 11 исполняемых скиллов и валидность структуры их файлов `SKILL.md`.
    - `test_07_install_gemini_and_windsurf_rules`: проверяет корректность создания `GEMINI.md` и `.windsurfrules` как в режиме `--agent all`, так и в изолированных режимах `--agent gemini` / `--agent windsurf`, а также наличие директив `STRICTLY NO CODE CHANGES`.
    - `test_08_install_doc_lang_parameter`: проверяет влияние флага `--doc-lang` (`ru` vs `en`) на директивы в сгенерированных правилах и подтверждает успешное прохождение аудита `kb_lint.py` в обоих случаях.
  - Актуализирована документация `README.md`:
    - Добавлено описание структуры каталога `.agents/skills/` и таблица всех 11 скиллов с их slash-командами `/kb-*` и режимами.
    - Отражена поддержка Google Antigravity (`GEMINI.md`) и Windsurf Cascade (`.windsurfrules`).
    - Описан флаг `--doc-lang` и поддержка двуязычной разработки.
    - Включен раздел об открытых моделях (Qwen 2.5 Coder, DeepSeek) со ссылкой на платформенное исследование `RESEARCH-001`.
    - Добавлен раздел «Zero-to-Hero Quickstart» с первыми шагами для пользователей после установки.
  - Проведена полная верификация: все 8 тестов в `tests/test_installer.py` пройдены успешно (100% pass), `kb_lint.py` подтвердил 0 битых ссылок и целостность базы знаний.
  - План Фазы 2 (`PLAN-002`) и все входящие задачи (TASK-005, TASK-006, TASK-007, TASK-008) полностью выполнены и закрыты.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Переход к перспективным направлениям бэклога (Clean Slate Scaffolding, GitHub Actions CI workflow, Brownfield Adoption).

---

### [2026-09-30] — Завершение TASK-007: Эталонные правила агентов по канону remote-notification и генерация GEMINI.md
- **Что сделано:**
  - Во все генераторы правил инсталлятора `install.py` интегрирован полный канонический регламент из эталонного проекта `remote_notification`:
    - 12 канонических дисциплин Docs-as-Code (онбординг, Kanban, Roadmap, ADR и отказные ADR, платформа/Research, Devlog, Obsidian, Permalinks, Regression-First, QA-реестр `05_Testing/`, Obsidian Graph, Git-интеграция).
    - Строгая защита 3 режимов с маркером `STRICTLY NO CODE CHANGES` для Режимов 1 и 2.
    - Роль Senior Engineering Partner с обязательным подтверждением пользователя перед записью планов и ТЗ.
    - Поддержка языкового регламента `doc_lang` (`ru` vs `en`).
  - Добавлен генератор `generate_gemini_md` для создания корневого файла `GEMINI.md` (поддержка Google Antigravity и Gemini CLI с перечислением доступных скиллов).
  - Добавлен генератор `generate_windsurfrules` для поддержки Windsurf Cascade (`.windsurfrules`).
  - Обновлены генераторы `generate_agents_md`, `generate_clinerules`, `generate_claude_md`, `generate_cursorrules`, `generate_copilot_instructions`.
  - В опции `--agent` CLI и интерактивного визарда добавлены варианты `gemini` и `windsurf`.
  - Проведена оптимизация размера: итоговый размер `install.py` составил 79.3 КБ / 81,153 байта (строго в рамках DoD < 80 КБ / 81,920 байт).
  - Успешно пройдены все верификационные тесты: сборка `build_installer.py` (код 0), `py_compile` (код 0), `kb_lint.py` (0 битых ссылок), интеграционный прогон генерации всех 7 файлов правил и проверка наличия ключевых маркеров, полный набор тестов `unittest` (5/5 тестов OK).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-008`: Сквозное E2E тестирование в `tests/test_installer.py` и обновление документации `README.md` (включая гайд для новичков).

---

### [2026-09-30] — Завершение TASK-006: Упаковка 11 скиллов .agents/skills/ в сборщик и install.py
- **Что сделано:**
  - В `scripts/build_installer.py` добавлен сборщик скиллов: обход каталога `.agents/skills/` и упаковка канонических файлов `SKILL.md` для всех 11 скиллов без дублирования лишних файлов.
  - В `install.py` реализован локальный фолбэк для разработки в `unpack_assets()` и автоматическая распаковка скиллов в целевую директорию `.agents/skills/<skill>/SKILL.md`.
  - Оптимизирована генерация стартовых документов в `create_starter_docs` через переиспользование распакованных шаблонов (итоговый размер `install.py` составил 78.1 КБ / 80,024 байта при лимите DoD < 80 КБ).
  - Успешно пройдены все этапы верификации: `build_installer.py` (код 0), `py_compile` (код 0), `kb_lint.py` (0 битых ссылок), интеграционный прогон в песочнице с проверкой всех 11 `SKILL.md`, полный прогон `unittest` (5/5 тестов пройдено).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-007`: Эталонные правила агентов по канону `remote_notification` (12 дисциплин, языковая параметризация, роль Senior Partner, отказные ADR, `GEMINI.md`, `.windsurfrules` и адаптеры).

---

### [2026-09-30] — Завершение TASK-005: Исследование экосистемы AI-агентов (RESEARCH-001) и мультиязычность
- **Что сделано:**
  - Проведено и оформлено глубокое платформенное исследование `docs/04_Research/RESEARCH-001-ai-agent-ecosystem-and-ide-matrix.md` по средам разработки (Antigravity, Cline, Claude Code CLI, Cursor, Windsurf, Copilot, Continue, Aider) и семействам моделей (Qwen 2.5 Coder, DeepSeek R1/V3, Claude, Gemini, GPT).
  - В исследовании детально разобран потенциал ведущей открытой модели **Qwen 2.5 Coder** (32B/14B/7B) для локального enterprise-развертывания (Ollama/vLLM) со 100% приватностью кода под управлением 3-режимного каркаса.
  - Реализована поддержка языковой параметризации в `install.py`: добавлен CLI-флаг `--doc-lang` (по умолчанию `ru`) и интерактивный вопрос на английском языке в TUI визарде.
  - Проведена верификация: `py_compile` (код 0), запуск `install.py --help`, запуск песочницы с `--doc-lang en`, все 5 модульных тестов в `test_installer.py` (100% pass), проверка ссылок `kb_lint.py` (0 битых ссылок).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-006`: упаковка всех 11 исполняемых скиллов `.agents/skills/` в сборщик `build_installer.py` и распаковка в `install.py`.

---

### [2026-09-30] — Завершение Фазы 1 (MVP): Автономный инсталлятор и мульти-стековые пресеты
- **Что сделано:**
  - Реализован автономный установщик `install.py` на стандартной библиотеке Python 3 (Zero Dependencies).
  - Разработан скрипт компиляции ресурсов `scripts/build_installer.py`, который упаковывает 12 шаблонов, `.obsidian/graph.json` и `kb_lint.py` в компактный zlib/base64 бандл внутри `install.py`.
  - Реализованы 5 технологических пресетов (Swift/iOS/macOS с нюансами ARC/Concurrency/BackgroundTasks, TypeScript, Python, .NET, Generic).
  - Сгенерированы адаптеры правил AI-агентов (`AGENTS.md`, `.clinerules`, `CLAUDE.md`, `.cursorrules`, `.github/copilot-instructions.md`).
  - Разработан интерактивный терминальный мастер с поддержкой TTY при pipe через `curl | python3` и полным набором CLI-флагов.
  - Написан набор автоматических тестов `tests/test_installer.py` (5 E2E тестов, 100% pass).
  - Подготовлен исчерпывающий `README.md` с визуальным стилем, инструкцией в 1 команду и описанием преимуществ.
  - Проверена целостность базы знаний через `kb_lint.py` (0 битых ссылок).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Подключение удаленного GitHub репозитория и релиз v1.0.0.

---

### [2026-09-30] — Инициализация проекта agent-docs-harness и базы знаний Docs-as-Code
- **Что сделано:**
  - Инициализирован Git-репозиторий и настроен `.gitignore`.
  - Развернута архитектура базы знаний `docs/` по стандарту Docs-as-Code с соблюдением догфудинга.
  - Настроена цветовая схема Obsidian Graph (`.obsidian/graph.json`) с 7 цветовыми группами.
  - Подготовлены 12 эталонных шаблонов в `templates/` и `docs/00_Templates/`.
  - Реализован автономный линтер базы знаний `scripts/kb_lint.py` с проверкой wikilinks и frontmatter без внешних зависимостей.
  - Сформированы документы `SPEC.md`, `00_Index.md`, `Onboarding.md`, `Kanban.md`, `Roadmap.md`.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация первой задачи фазы MVP: ядро инсталлятора `install.py` с упаковщиком шаблонов и адаптерами стеков.
