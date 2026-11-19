---
id: TASK-116
title: "Матрица Right-Sizing, поле track и правило линтера KB-020 (Deep-Risk Guard)"
status: planned
type: task
phase: 32
track: standard
component:
  - core
  - lint
  - templates
parent_plan: "[[../../Plans/PLAN-029-right-sizing-and-spec-quality-gate|PLAN-029]]"
depends_on: []
created: 2026-11-19
updated: 2026-11-19
tags:
  - task/spec
  - phase32
  - right-sizing
  - lint
  - templates
  - quality-gates
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-116 — Матрица Right-Sizing, поле track и правило линтера KB-020 (Deep-Risk Guard)

> **ID:** TASK-116 | **Статус:** К реализации (Planned) | **Фаза:** 32 | **Трек:** Standard  
> **План:** [[../../Plans/PLAN-029-right-sizing-and-spec-quality-gate|PLAN-029: Right-Sizing процесса и Spec Quality Gate]] | **Канбан:** [[../../Kanban|Канбан-доска]]  
> **Нормативная база:** [[../../../03_Decisions_ADR/ADR-0037-wave-2-quality-and-evidence-standard|ADR-0037]] | **Исследование:** [[../../../04_Research/RESEARCH-031-wave-2-quality-and-evidence-architecture|RESEARCH-031]]  
> **Зависимости:** `[]` (первая задача Фазы 32)

---

## 1. Цель задачи

Внедрить первый уровень калибровки процесса разработки — **Right-Sizing матрицу (`micro / standard / deep`)** в шаблоны задач и планов, а также реализовать механический контроль в `scripts/kb_lint.py` в виде правила **`KB-020` (Deep-Risk Tag Guard)**:
1. Зафиксировать поле `track` в канонических шаблонах `docs/00_Templates/` и синхронных копиях `templates/` с соблюдением контракта паритета (TASK-092).
2. Реализовать правило `KB-020` в монолитном линтере `scripts/kb_lint.py`: выдавать неблокирующее предупреждение (SEVERITY_WARNING), если задача или план имеют теги повышенного риска (`architecture`, `security`, `migration`, `public-api`), но не имеют привязки к родительскому плану (`parent_plan`) или исследовательской базе (`research_basis`).
3. Зарегистрировать правило `KB-020` в реестре `RULES`, интегрировать во все форматы вывода (`text`, `json`, `sarif`).
4. Покрыть логику правила модульными тестами в `tests/test_kb_lint.py` и подтвердить 100% паритет шаблонов в `tests/test_template_parity.py`.

---

## 2. Затрагиваемые файлы и скоуп символов

* `[MODIFY]` `docs/00_Templates/TEMPLATE_TASK.md`:
  - Frontmatter: добавление поля `track: standard # micro | standard | deep`
* `[MODIFY]` `templates/TEMPLATE_TASK.md`:
  - Frontmatter: синхронное добавление поля `track: standard`
* `[MODIFY]` `docs/00_Templates/TEMPLATE_TASK_MICRO.md`:
  - Frontmatter: добавление поля `track: micro # micro | standard | deep`
* `[MODIFY]` `templates/TEMPLATE_TASK_MICRO.md`:
  - Frontmatter: синхронное добавление поля `track: micro`
* `[MODIFY]` `docs/00_Templates/TEMPLATE_PLAN.md`:
  - Frontmatter: добавление поля `track: standard # standard | deep`
* `[MODIFY]` `templates/TEMPLATE_PLAN.md`:
  - Frontmatter: синхронное добавление поля `track: standard`
* `[MODIFY]` `scripts/kb_lint.py`:
  - `RULES` — добавление записи `"KB-020": "Deep-risk tag requires parent plan or research basis"`
  - `RULE_SEVERITY_DEFAULT` — добавление `"KB-020": SEVERITY_WARNING`
  - `DEEP_RISK_TAGS` — константа `{"architecture", "security", "migration", "public-api"}`
  - `check_deep_risk_tags(files: List[Path]) -> List[Finding]` — функция аудита задач и планов на наличие deep-тегов без плана/исследования
  - `run_linter(...)` — вызов `check_deep_risk_tags` в общем контуре проверки
* `[MODIFY]` `tests/test_kb_lint.py`:
  - `test_kb020_deep_risk_tags_warn()` — тест генерации предупреждения `KB-020` при отсутствии parent_plan у задачи с deep-тегом
  - `test_kb020_deep_risk_tags_pass()` — тест успешного прохождения при наличии parent_plan или research_basis
  - `test_kb020_rule_registry()` — тест присутствия `KB-020` в реестре правил линтера

---

## 3. Детали реализации

### 3.1. Структура поля `track` в шаблонах
В шаблонах `TEMPLATE_TASK.md` и `TEMPLATE_TASK_MICRO.md` поле помещается в блок YAML frontmatter:
```yaml
track: standard # micro | standard | deep
```
Для задач обратная совместимость сохраняется: если поле `track` отсутствует, линтер и агент по умолчанию трактуют задачу как `standard` (или `micro`, если `parent_plan` отсутствует и размер $\le 30$ строк).

### 3.2. Алгоритм правила `KB-020` в `scripts/kb_lint.py`

```python
DEEP_RISK_TAGS: Set[str] = {"architecture", "security", "migration", "public-api"}

def check_deep_risk_tags(files: List[Path]) -> List[Finding]:
    """Проверяет задачи и планы с тегами deep-риска на наличие родительского плана или исследовательской базы.
    
    Правило KB-020 (SEVERITY_WARNING):
    1. Для задач в Specs/: если есть deep-тег, но parent_plan отсутствует, пуст или равен 'none'.
    2. Для планов в Plans/: если есть deep-тег, но research_basis отсутствует или пуст (без basis_note).
    """
    findings: List[Finding] = []
    for f in files:
        # Проверяем только Specs и Plans
        p_str = f.as_posix()
        is_spec = "02_Tasks/Specs/" in p_str
        is_plan = "02_Tasks/Plans/" in p_str
        if not (is_spec or is_plan):
            continue
            
        content = f.read_text(encoding="utf-8", errors="replace")
        fm = extract_frontmatter(content)
        if not fm:
            continue
            
        raw_tags = fm.get("tags", [])
        if isinstance(raw_tags, str):
            raw_tags = [raw_tags]
        tags = {str(t).strip().lower().lstrip("#") for t in raw_tags}
        
        matched_deep = tags & DEEP_RISK_TAGS
        if not matched_deep:
            continue
            
        tag_list_str = ", ".join(sorted(matched_deep))
        if is_spec:
            parent_plan = fm.get("parent_plan")
            if not parent_plan or str(parent_plan).strip().lower() in {"", "none", "null"}:
                findings.append(Finding(
                    rule_id="KB-020",
                    file_path=f,
                    line_number=1,
                    severity=SEVERITY_WARNING,
                    message=f"Task has deep-risk tag(s) [{tag_list_str}] but lacks parent_plan reference",
                    fixable=False,
                ))
        elif is_plan:
            research_basis = fm.get("research_basis")
            basis_note = fm.get("basis_note")
            if not research_basis or (str(research_basis).strip().lower() == "none" and not basis_note):
                findings.append(Finding(
                    rule_id="KB-020",
                    file_path=f,
                    line_number=1,
                    severity=SEVERITY_WARNING,
                    message=f"Plan has deep-risk tag(s) [{tag_list_str}] but lacks verified research_basis or basis_note",
                    fixable=False,
                ))
                
    return findings
```

---

## 4. План верификации (Verification Plan)

- [ ] **Компиляция Python:**
  ```bash
  python -m py_compile scripts/kb_lint.py
  ```
  *Ожидаемый результат:* Exit code 0, отсутствие синтаксических ошибок.
- [ ] **Юнит-тесты правила KB-020:**
  ```bash
  python -m unittest tests/test_kb_lint.py
  ```
  *Ожидаемый результат:* 100% прохождение всех тестов, включая `test_kb020_*`.
- [ ] **Тесты паритета шаблонов:**
  ```bash
  python -m unittest tests/test_template_parity.py
  ```
  *Ожидаемый результат:* 100% паритет файлов `docs/00_Templates/` и `templates/`.
- [ ] **Аудит целостности базы знаний:**
  ```bash
  python scripts/kb_lint.py --path docs
  ```
  *Ожидаемый результат:* 0 broken links, 0 errors, 0 ложных срабатываний `KB-020`.
- [ ] **Проверка контрактов машинного вывода:**
  ```bash
  python scripts/kb_lint.py --path docs --format json
  python scripts/kb_lint.py --path docs --format sarif
  ```
  *Ожидаемый результат:* Валидный JSON и SARIF с присутствием правила `KB-020` в реестре.

---

## 5. Критерии готовности (DoD)

- [ ] Поле `track` добавлено в `TEMPLATE_TASK.md`, `TEMPLATE_TASK_MICRO.md`, `TEMPLATE_PLAN.md` в обеих директориях (`docs/00_Templates/` и `templates/`).
- [ ] Правило `KB-020` реализовано в `scripts/kb_lint.py` и зарегистрировано в `RULES`.
- [ ] Написаны и успешно проходят модульные тесты для `KB-020` в `tests/test_kb_lint.py`.
- [ ] Тесты паритета `test_template_parity.py` и полный аудит `kb_lint.py` завершаются без ошибок.
- [ ] Статус задачи обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [ ] Сессия зафиксирована в `docs/Devlog.md`.
