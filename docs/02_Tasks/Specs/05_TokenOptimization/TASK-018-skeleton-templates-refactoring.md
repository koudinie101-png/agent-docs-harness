---
id: TASK-018
title: "Рефакторинг 13 шаблонов docs/00_Templates/ в компактные каркасы (Skeleton Templates)"
status: planned
type: task
phase: 5
component:
  - templates
  - token-optimization
parent_plan: "[[../../Plans/PLAN-005-high-snr-token-optimization|PLAN-005]]"
created: 2026-10-01
updated: 2026-10-01
tags:
  - task/spec
  - phase5
  - component/templates
  - component/token-optimization
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-018 — Рефакторинг 13 шаблонов docs/00_Templates/ в компактные каркасы

> **ID:** TASK-018  
> **Статус:** К реализации (Режим 2)  
> **Теги:** #task/spec #phase5 #component/templates #component/token-optimization  
> **Родительский план:** [[../../Plans/PLAN-005-high-snr-token-optimization|PLAN-005]]  
> **Связанные ADR и исследования:** [[../../../04_Research/RESEARCH-004-token-efficiency-and-context-compression|RESEARCH-004]], [[../../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Реализовать Правило 5 (Skeleton Templates) архитектурного стандарта [[../../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]] для каталога шаблонов `docs/00_Templates/`:
1. **Устранение вербального шума и обучающих эссе:**
   * Очистить шаблоны от пространных теоретических рассуждений, дублирующих документацию, и громоздких примеров кода.
   * Заменить абзацы пояснений на точечные однострочные директивы `<!-- prompt / instruction -->`.
2. **Сжатие перегруженного шаблона онбординга (`TEMPLATE_ONBOARDING.md`):**
   * Сократить `TEMPLATE_ONBOARDING.md` с текущих 11.4 КБ (29% объема всех шаблонов) до $\le$ 4 КБ. Превратить его в лаконичную, высокоэффективную шпаргалку для человека и агента.
3. **Сохранение 100% структурной совместимости и контрактов:**
   * Сохранить валидные схемы YAML frontmatter (обязательные поля `id`, `title`, `status`, `type`, `tags` и др.).
   * Сохранить канонические разделы документов (например, `## 1. Цель`, `## 2. Затрагиваемые файлы`, `## 4. План верификации`, `## 5. DoD` в ТЗ).
   * Сохранить интерактивные чек-боксы (`- [ ]`) для E2E сценариев и планов.
4. **Сокращение статического веса каталога шаблонов:**
   * Уменьшить суммарный объем 13 шаблонов с 38.8 КБ (~9.7k токенов) до $\le$ 21 КБ (~5.2k токенов) — экономия ~45%.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `docs/00_Templates/TEMPLATE_ONBOARDING.md` — сжатие с 11.4 КБ до < 4 КБ (шпаргалка без «воды»).
* `[MODIFY]` `docs/00_Templates/TEMPLATE_TASK.md` — компактный каркас технической спецификации.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_PLAN.md` — лаконичный каркас плана Режима 1.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_ADR.md` — четкий каркас архитектурного решения с обязательной секцией отказных вариантов.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_BUG.md` — компактный шаблон баг-репорта с RCA и TDD регрессионным тестом.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_RESEARCH.md` — лаконичный шаблон платформенного исследования.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_RELEASE.md` — компактный каркас релиза с таблицей SHA-256.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_KANBAN.md` — легковесная структура доски.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_ROADMAP.md` — каркас дорожной карты по фазам.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_DEVLOG.md` — компактный шаблон дневника разработки.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_INDEX.md` — лаконичный входной хаб базы знаний.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_TESTING.md` — структура E2E UX чек-листа тестирования.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_SPEC.md` — канонический скелет мастер-спецификации `SPEC.md`.

---

## 3. Детали технической реализации

### 3.1. Принцип Skeleton Template (Каркас вместо учебника)

Вместо длинных абзацев пояснений в шаблонах используются компактные HTML-комментарии или однострочные плейсхолдеры:

```markdown
<!-- Было в TEMPLATE_BUG.md (18 строк описания):
## 2. Шаги воспроизведения
Пожалуйста, опишите как можно подробнее каждый шаг, который привел к возникновению дефекта. Укажите операционную систему, версию сборки...
-->

<!-- Стало в Skeleton Template (High-SNR): -->
## 2. Шаги воспроизведения
1. <!-- Предусловие / окружение -->
2. <!-- Точное действие пользователя или команды -->
3. <!-- Наблюдаемый ошибочный результат vs Ожидаемый корректный -->
```

### 3.2. Архитектура компактного `TEMPLATE_ONBOARDING.md`

1. **Quick Start:** 3 команды для запуска харнесса (`python install.py`, `agy`, запуск тестов).
2. **3-Mode Cheatsheet:** таблица 3 режимов (`/kb-plan`, `/kb-task`, `/kb-implement`).
3. **Knowledge Base Map:** карта папок `docs/00_...` до `05_...` в 6 строк.
4. **Agent Rules Summary:** 5 ключевых табу (No Code в Mode 1/2, Regression-First, Permalinks, Anti-Echo).
5. Объем: $\le$ 3 800 байт.

---

## 4. План верификации (Verification Plan)

### Автоматическая проверка:
- [ ] Проверка суммарного размера каталога `docs/00_Templates/`:
  ```powershell
  (Get-ChildItem -Path docs/00_Templates -Recurse -Filter *.md | Measure-Object -Property Length -Sum).Sum
  ```
  *Критерий:* суммарный объем $\le$ 21 000 байт (было 38 774 байта).
- [ ] Проверка размера `TEMPLATE_ONBOARDING.md`:
  *Критерий:* $\le$ 4 000 байт (было 11 423 байта).
- [ ] Валидация базы знаний: `python scripts/kb_lint.py --path docs` (Exit code 0, frontmatter валиден во всех 13 шаблонах).

---

## 5. Критерии готовности (Definition of Done)

- [ ] Все 13 шаблонов очищены от теоретических эссе и переведены в формат Skeleton Templates.
- [ ] Шаблон `TEMPLATE_ONBOARDING.md` сокращен до компактной шпаргалки.
- [ ] Сохранены все обязательные поля frontmatter и структура секций.
- [ ] Линтер `kb_lint.py` подтверждает отсутствие сломанных ссылок и корректность frontmatter.
