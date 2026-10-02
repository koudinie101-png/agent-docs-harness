---
id: TASK-031
title: "Эвристический контроль дрифта спецификации в scripts/kb_lint.py и модульные тесты"
status: planned
type: task
phase: 8
component:
  - scripts
  - linter
  - audit
parent_plan: "[[../../Plans/PLAN-008-greenfield-idea-first-and-living-spec|PLAN-008]]"
created: 2026-10-02
updated: 2026-10-02
tags:
  - task/spec
  - phase8
  - component/scripts
  - component/linter
  - living-spec
  - documentation-drift
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-031 — Эвристический контроль дрифта спецификации в scripts/kb_lint.py

> **ID:** TASK-031  
> **Статус:** К реализации (Режим 2)  
> **Теги:** #task/spec #phase8 #component/scripts #component/linter #living-spec #documentation-drift  
> **Родительский план:** [[../../Plans/PLAN-008-greenfield-idea-first-and-living-spec|PLAN-008]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-009-greenfield-initialization-and-living-spec-drift|RESEARCH-009]], [[../../../03_Decisions_ADR/ADR-0014-greenfield-idea-first-initialization-and-living-spec-protocol|ADR-0014]], [[../../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Реализовать эвристический аудит устаревания мастер-спецификации в линтере `scripts/kb_lint.py` согласно [[../../../03_Decisions_ADR/ADR-0014-greenfield-idea-first-initialization-and-living-spec-protocol|ADR-0014]] и [[../../../04_Research/RESEARCH-009-greenfield-initialization-and-living-spec-drift|RESEARCH-009]]:
1. **Функция проверки дрифта `check_spec_drift`:** Анализировать состояние `Roadmap.md` (или `Kanban.md`) на предмет количества завершенных фаз разработки (`## Фаза X: ... - [x]`).
2. **Анализ даты обновления `SPEC.md`:** Считывать поле `updated` из YAML frontmatter `SPEC.md` (или корневого `SPEC.md`).
3. **Неблокирующий Warning:** Если в репозитории завершено $\ge 2$ фаз, а `SPEC.md` не обновлялся со времени ранних фаз, линтер выводит информационное предупреждение (Warning):  
   `⚠️ WARN: Living Spec Drift detected! SPEC.md (last updated: YYYY-MM-DD) was not updated despite multiple completed phases.`
4. **Безопасный код выхода (Zero Exit Code Impact):** Предупреждения о дрифте носят рекомендательный характер и не должны приводить к аварийному завершению скрипта (`sys.exit(0)`), предотвращая блокировку CI и локальной разработки.
5. **Модульное тестирование:** Покрыть логику детекции тестами в `tests/test_kb_lint.py`.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `scripts/kb_lint.py` — функция `check_spec_drift`, интеграция в `run_linter()`, вывод предупреждений.
* `[MODIFY]` `tests/test_kb_lint.py` — модульные тесты проверки функции `check_spec_drift` на актуальных и устаревших состояниях хранилища.

---

## 3. Детали реализации

### 3.1. Сигнатура и логика `check_spec_drift` в `scripts/kb_lint.py`

```python
def check_spec_drift(docs_dir: Path) -> list[str]:
    """
    Эвристический анализ дрифта спецификации.
    Возвращает список неблокирующих предупреждений (warnings).
    """
    warnings = []
    repo_root = docs_dir.parent if docs_dir.name == "docs" else docs_dir
    roadmap_path = docs_dir / "02_Tasks" / "Roadmap.md"
    spec_path = repo_root / "SPEC.md"
    if not spec_path.is_file():
        spec_path = docs_dir / "SPEC.md"

    if not roadmap_path.is_file() or not spec_path.is_file():
        return warnings

    # Подсчет завершенных фаз
    roadmap_content = roadmap_path.read_text(encoding="utf-8")
    completed_phases = len(re.findall(r'##\s+Фаза\s+\d+:.*?Завершена|##\s+Phase\s+\d+:.*?Completed', roadmap_content, re.IGNORECASE))
    
    # Извлечение даты updated из SPEC.md
    spec_content = spec_path.read_text(encoding="utf-8")
    updated_match = re.search(r'^updated:\s*(\d{4}-\d{2}-\d{2})', spec_content, re.MULTILINE)
    created_match = re.search(r'^created:\s*(\d{4}-\d{2}-\d{2})', spec_content, re.MULTILINE)

    if completed_phases >= 2 and updated_match:
        updated_date = updated_match.group(1)
        created_date = created_match.group(1) if created_match else None
        if created_date and updated_date == created_date:
            warnings.append(
                f"Living Spec Drift: SPEC.md was never updated since creation ({created_date}), "
                f"despite {completed_phases} completed phases in Roadmap.md. Consider syncing Master Spec."
            )

    return warnings
```

### 3.2. Интеграция в `run_linter`

Предупреждения выводятся в консоль, но `return 0` сохраняется, если нет ошибок целостности wikilinks или frontmatter:
```python
drift_warnings = check_spec_drift(docs_dir)
for dw in drift_warnings:
    print(f"⚠️  WARN: {dw}")
```

---

## 4. План верификации (Verification Plan)

- [ ] Модульные тесты: `python -m unittest tests/test_kb_lint.py` (100% pass).
- [ ] Проверка на текущем репозитории: `python scripts/kb_lint.py --path docs` (должен завершиться успешно с кодом 0).
- [ ] Тестирование на синтетическом репозитории с устаревшим `SPEC.md` и подтверждение вывода `⚠️ WARN: Living Spec Drift`.

---

## 5. Критерии готовности (DoD)

- [ ] Функция `check_spec_drift` реализована без внешних зависимостей (только Python stdlib `re`, `pathlib`).
- [ ] Предупреждения о дрифте не влияют на код возврата линтера (`exit code 0`).
- [ ] Все тесты в `tests/test_kb_lint.py` успешно проходят.
- [ ] Статус задачи обновлен в Канбане и Дорожной карте.
