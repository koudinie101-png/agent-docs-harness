---
id: TASK-061
title: "Инфраструктура процедурной памяти (docs/06_Memory/, шаблон TEMPLATE_INCIDENT.md и агрегированный индекс patterns.md)"
status: done
type: task
phase: 16
component:
  - memory
  - templates
  - hub
parent_plan: "[[../../Plans/PLAN-016-self-improving-harness-and-defect-memory|PLAN-016]]"
created: 2026-10-12
updated: 2026-10-12
tags:
  - task/spec
  - phase16
  - memory
  - templates
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-061 — Инфраструктура процедурной памяти (docs/06_Memory/, шаблон TEMPLATE_INCIDENT.md и агрегированный индекс patterns.md)

> **ID:** TASK-061 | **Статус:** Выполнено (Режим 3)  
> **План:** [[../../Plans/PLAN-016-self-improving-harness-and-defect-memory|PLAN-016]] | **Канбан:** [[../../Kanban|Канбан]]  
> **Обоснование:** [[../../../04_Research/RESEARCH-020-self-improving-defect-loop-and-quality-gates|RESEARCH-020]], [[../../../03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]  
> **Первоисточник фидбека:** [[../../Inbox/FB-GH-3|Обращение FB-GH-3 (madpanther)]]

---

## 1. Цель задачи

Создать базовую файловую структуру и артефакты для накапливания процедурной памяти агента и команды:
* Развернуть подсистему `docs/06_Memory/` с архивным каталогом `Incidents/` для детального разбора ошибок.
* Создать эталонный шаблон `docs/00_Templates/TEMPLATE_INCIDENT.md` с валидным YAML frontmatter для регистрации процедурных инцидентов (`INC-XXX`).
* Сформировать корневой High-SNR индекс `docs/06_Memory/patterns.md` с жестким ограничением токеномики ($\le 15$ активных записей, ~350 токенов), однострочным синтаксисом и правилами ротации.
* Зарегистрировать раздел процедурной памяти в карте базы знаний `docs/00_Index.md`.

---

## 2. Затрагиваемые файлы

* `[NEW]` `docs/00_Templates/TEMPLATE_INCIDENT.md` — канонический шаблон инцидента процедурной памяти.
* `[NEW]` `docs/06_Memory/patterns.md` — компактный агрегированный индекс систематических паттернов ошибок.
* `[NEW]` `docs/06_Memory/Incidents/.gitkeep` — инициализация подкаталога архива инцидентов.
* `[MODIFY]` `docs/00_Index.md` — добавление раздела «6. Процедурная память (`docs/06_Memory/`)» в карту базы знаний.
* `[MODIFY]` `docs/02_Tasks/Kanban.md` — обновление карточки `TASK-061` до постоянной викиссылки на ТЗ.
* `[MODIFY]` `docs/02_Tasks/Roadmap.md` — обновление ссылки `TASK-061` на ТЗ.

---

## 3. Детали реализации

### 3.1. Эталонный шаблон `TEMPLATE_INCIDENT.md`
Файл размещается в `docs/00_Templates/TEMPLATE_INCIDENT.md` со структурой:
```markdown
---
id: INC-XXX
title: "[Краткая формулировка ошибки или инцидента]"
status: active # active | resolved | promoted | archived
type: incident
severity: high # low | medium | high
tag: platform # platform | cognitive | testing | contract | tooling
root_cause: "[Корневая причина в 3-5 словах]"
target_pattern: "TRG-XX"
created: 2026-10-12
updated: 2026-10-12
tags:
  - memory
  - incident
---

# ⚠️ Инцидент: INC-XXX — [Краткая формулировка]

> **Тег:** #memory #incident | **Тяжесть:** high | **Статус:** active  
> **Паттерн в базе:** `TRG-XX` | **Задача:** `TASK-XXX`

---

## 1. Контекст и симптом
<!-- Что произошло? Симптом сбоя, лог ошибки или неожиданное поведение -->

## 2. Корневая причина (Root Cause)
<!-- Почему агент/разработчик ошибся? Ложное допущение, галлюцинация API, спешка -->

## 3. Защитное действие (Corrective Action)
<!-- Какое правило или автотест предотвращает повторение ошибки в будущем? -->
```

### 3.2. Компактный индекс `docs/06_Memory/patterns.md`
Файл размещается в корне каталога `docs/06_Memory/` со строгим High-SNR форматом:
```markdown
# 🧠 Память процедурных ошибок: Активные паттерны

> **Инвариант токеномики:** Строго $\le 15$ активных записей. При превышении — слияние или архивация.  
> **Точки обязательного чтения:** перед началом реализации (Режим 3) и перед закрытием задачи (/kb-complete).

---

## ⚡ Активные паттерны (Active Patterns)

- [TRG-01] Windows Path Compatibility | Сырые прямые/обратные слеши в регулярных выражениях ломают поиск на Windows | Использовать pathlib.Path или нормализацию .replace('\\', '/') | (Count: 3, Sev: High) -> INC-001
- [TRG-02] Mock False Confidence | Мок-тест проверяет аргументы вызова вместо реального контракта CLI | Для внешних утилит обязателен живой smoke-тест без моков | (Count: 2, Sev: High) -> INC-002

---

## 📖 Правила промоушена
1. **Уровень (Частота/Тяжесть):** Добавление в индекс при $\text{count} \ge 2$ или $\text{severity} = \text{high}$.
2. **Охват:** При воспроизведении на всем стеке — перенос в автотест (Tier 1) или норматив `AGENTS.md` (Tier 2).
3. **Лимит:** При достижении 15 записей наименее частотные паттерны архивируются в `Incidents/`.
```

### 3.3. Обновление карты знаний `docs/00_Index.md`
В раздел `## 📂 Структура разделов` добавляется подраздел:
```markdown
### 6. Процедурная память (`docs/06_Memory/`)
* `06_Memory/patterns` — компактная база систематических ошибок агента ($\le 15$ записей).
* `Incidents/` — архив детальных отчетов об инцидентах (`INC-XXX`).
```

---

## 4. План верификации (Verification Plan)

- [x] Наличие файлов: проверка создания `TEMPLATE_INCIDENT.md`, `patterns.md` и `docs/06_Memory/Incidents/.gitkeep`.
- [x] Линтер базы знаний: `python scripts/kb_lint.py --path docs` завершается с `0 broken links` и валидным YAML frontmatter.
- [x] Аудит связности: ссылка на `patterns.md` открывается из `00_Index.md`.

---

## 5. Критерии готовности (DoD)

- [x] Каталог `docs/06_Memory/` развернут с `patterns.md` и подкаталогом `Incidents/`.
- [x] Шаблон `TEMPLATE_INCIDENT.md` создан и соответствует стандарту.
- [x] `docs/00_Index.md` обновлен.
- [x] `python scripts/kb_lint.py --path docs` возвращает Exit code 0.

