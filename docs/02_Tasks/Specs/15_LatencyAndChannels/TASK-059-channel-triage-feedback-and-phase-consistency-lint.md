---
id: TASK-059
title: "Прозрачный фидбек источников в /kb-triage и семантический контроль фаз в scripts/kb_lint.py"
status: completed
type: task
phase: 15
component:
  - triage
  - skill
  - linter
parent_plan: "[[../../Plans/PLAN-015-response-latency-and-channel-transparency|PLAN-015]]"
created: 2026-10-12
updated: 2026-10-12
tags:
  - task/spec
  - phase15
  - triage
  - lint
  - semantics
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-059 — Прозрачный фидбек источников в /kb-triage и семантический контроль фаз в scripts/kb_lint.py

> **ID:** TASK-059 | **Статус:** Выполнено  
> **План:** [[../../Plans/PLAN-015-response-latency-and-channel-transparency|PLAN-015]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Обоснование:** [[../../../04_Research/RESEARCH-019-user-centric-ingestion-and-channel-transparency|RESEARCH-019]], [[../../../03_Decisions_ADR/ADR-0024-user-centric-ingestion-and-channel-transparency|ADR-0024]]  

---

## 1. Цель задачи

1. **Прозрачный диагностический фидбек в Режиме 2C (`/kb-triage`):**  
   Модернизировать исполняемый скилл `.agents/skills/kb-triage/SKILL.md`. При запуске команды `/kb-triage` и отсутствии необработанных обращений (`status: new`) агент не должен ограничиваться сухой фразой «инбокс пуст». Вместо этого агент запрашивает диагностический статус источников через `python scripts/kb_ingest.py --status` и выводит пользователю прозрачную сводку (опрошенные каналы, распознанный репозиторий, статус авторизации и количество ранее обработанных тикетов), подтверждая реальный факт успешной проверки.
2. **Семантический контроль соответствия фаз в `scripts/kb_lint.py`:**  
   Внедрить функцию `check_phase_consistency(docs_dir: Path) -> list`, которая автоматически сопоставляет декларируемый номер фазы в метаданных (`phase: N`) спецификаций задач с директорией размещения (`Specs/NN_<Slug>/...`) и тегами (`phaseN`).
3. **Неблокирующие семантические предупреждения:**  
   Выводить предупреждения линтера как `⚠️ Phase Consistency Warnings` (не срывающие Exit code 0 при отсутствии критических ошибок связности).
4. **Модульные тесты линтера:**  
   Покрыть функцию `check_phase_consistency` модульными тестами в `tests/test_kb_lint.py`.

---

## 2. Затрагиваемые файлы

* `[MODIFY]` `.agents/skills/kb-triage/SKILL.md` — включение шага вызова дашборда источников при пустом инбоксе.
* `[MODIFY]` `scripts/kb_lint.py` — функция `check_phase_consistency`, вывод предупреждений в обоих режимах (Verbose и Silent-on-Success).
* `[MODIFY]` `tests/test_kb_lint.py` — модульные тесты обнаружения несоответствий фаз и структуры папок.
* `[MODIFY]` `docs/02_Tasks/Kanban.md` — связывание пермалинком и актуализация статуса.
* `[MODIFY]` `docs/02_Tasks/Roadmap.md` — связывание пермалинком на спецификацию.

---

## 3. Детали реализации

### 3.1. Обновление процедуры `.agents/skills/kb-triage/SKILL.md`
В разделе `## Procedure` обновляется шаг 1:
```markdown
1. **Ingest / Synchronize & Source Verification:**
   - Запустить инжест: `python scripts/kb_ingest.py` (поддерживаются опциональные аргументы, например `--all-open` или `--label <NAME>`).
   - Просканировать директорию `docs/02_Tasks/Inbox/` на наличие файлов со статусом `status: new`.
   - **Диагностический фидбек источников:** Если обращений со статусом `status: new` не обнаружено:
     * Выполнить: `python scripts/kb_ingest.py --status`.
     * Вывести пользователю компактный диагностический отчет: указать опрошенный репозиторий GitHub, статус каналов и число уже обработанных тикетов.
     * Зафиксировать подтверждение чистоты инбокса и завершить работу по протоколу Stop & Yield.
```

### 3.2. Функция `check_phase_consistency` в `scripts/kb_lint.py`
```python
def check_phase_consistency(docs_dir: Path) -> list:
    """
    Scans docs/02_Tasks/Specs/ for task specifications and validates:
    1. Folder Phase vs Frontmatter Phase:
       e.g., Specs/15_LatencyAndChannels/TASK-*.md must have phase: 15.
    2. Frontmatter Phase vs Tags:
       if tags contains 'phase15', frontmatter phase must be 15.
    Returns a list of non-blocking warning strings.
    """
```
- Путь к спецификациям: `docs_dir / "02_Tasks" / "Specs"`.
- Ищет папки формата `(\d+)_[\w-]+`.
- Для каждого `.md` файла спецификации проверяет:
  - `phase:\s*(\d+)` в YAML frontmatter.
  - Если номер фазы в frontmatter не совпадает с числовым префиксом папки:
    `warning = f"Spec '{rel_path}' declares phase {fm_phase}, but is located in folder '{folder.name}' (expected phase {folder_phase})."`
  - Если в тегах присутствует `phase(\d+)`, отличный от `fm_phase`:
    `warning = f"Spec '{rel_path}' declares phase {fm_phase}, but contains mismatched tag 'phase{tag_phase}'."`
- Интеграция в `run_linter`:
  - Добавить `phase_warnings = check_phase_consistency(docs_dir)`
  - Выводить блок `⚠️ Phase Consistency Warnings ({len(phase_warnings)}):` в Verbose режиме и `⚠️  WARN: {pw}` в Silent-on-Success режиме.
  - Предупреждения о фазах являются неблокирующими (не влияют на `has_errors`).

### 3.3. Тестирование в `tests/test_kb_lint.py`
- Тест `test_phase_consistency_matching`: валидная структура не генерирует warnings.
- Тест `test_phase_consistency_mismatched_folder`: несовпадение папки и `phase:` генерирует информативный warning.
- Тест `test_phase_consistency_mismatched_tag`: несовпадение тега `phaseX` и `phase: Y` генерирует warning.

---

## 4. План верификации (Verification Plan)

- [x] Синтаксическая корректность: `python -m py_compile scripts/kb_lint.py tests/test_kb_lint.py` (Exit code 0)
- [x] Модульные тесты линтера: `python -m unittest tests/test_kb_lint.py` (100% Pass, Exit code 0)
- [x] Запуск линтера базы знаний: `python scripts/kb_lint.py --path docs -v` (0 broken links, 0 warnings)
- [x] Полный регрессионный сьют проекта: `python -m unittest discover -s tests` (100% Pass, Exit code 0)

---

## 5. Критерии готовности (DoD)

- [x] Скилл `/kb-triage` обновлен и требует диагностического отчета при чистом инбоксе.
- [x] В `scripts/kb_lint.py` внедрена функция `check_phase_consistency`.
- [x] Модульные тесты в `tests/test_kb_lint.py` успешно проверяют семантический аудит фаз.
- [x] Все пункты Плана верификации пройдены (Exit code 0).
- [x] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [x] Запись добавлена в `Devlog.md`.
