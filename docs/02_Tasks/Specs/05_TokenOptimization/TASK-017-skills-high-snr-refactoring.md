---
id: TASK-017
title: "High-SNR рефакторинг реестра и 12 скиллов .agents/skills/ (микро-описания, легкий роутер docs-as-code)"
status: done
type: task
phase: 5
component:
  - skills
  - registry
  - token-optimization
parent_plan: "[[../../Plans/PLAN-005-high-snr-token-optimization|PLAN-005]]"
created: 2026-10-01
updated: 2026-10-01
tags:
  - task/spec
  - phase5
  - component/skills
  - component/registry
  - component/token-optimization
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-017 — High-SNR рефакторинг реестра и 12 скиллов .agents/skills/

> **ID:** TASK-017  
> **Статус:** Выполнено (Режим 3)  
> **Теги:** #task/spec #phase5 #component/skills #component/registry #component/token-optimization  
> **Родительский план:** [[../../Plans/PLAN-005-high-snr-token-optimization|PLAN-005]]  
> **Связанные ADR и исследования:** [[../../../04_Research/RESEARCH-004-token-efficiency-and-context-compression|RESEARCH-004]], [[../../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Реализовать Правила 1, 2, 4 и 6 архитектурного стандарта [[../../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]] для каталога исполняемых скиллов `.agents/skills/`:
1. **Сжатие Always-On реестра скиллов (-53% токенов на каждом шаге):**
   * Переписать поле `description` в YAML frontmatter всех 12 файлов `SKILL.md` на лаконичные триггерные микро-описания (Micro-Descriptions) объемом 10–13 слов согласно эталонной матрице из [[../../../04_Research/RESEARCH-004-token-efficiency-and-context-compression|RESEARCH-004]].
2. **Рефакторинг монолита `docs-as-code/SKILL.md` (13.8 КБ $\to$ < 2 КБ):**
   * Превратить монолитный скилл в компактный навигационный роутер (Progressive Disclosure Hub), направляющий агента к специализированным скиллам вместо дублирования инструкций всей системы.
3. **Устранение вербального шума и дублирования во всех 11 специализированных скиллах:**
   * Удалить мотивационную риторику («Никогда не будьте соглашателем»), размытые эпитеты и артефакты копипасты (Doze mode, UI thread Windows).
   * Исключить дублирование философии, определенной в `AGENTS.md` (DRY Rules Hierarchy).
   * Сформулировать процедуры в виде четких императивных предикатов (`CONSTRAINT: ...`, `PROCEDURE: 1, 2, 3`).
4. **Сокращение статического веса каталога скиллов:**
   * Уменьшить общий объем файлов скиллов с 42.4 КБ (~10.6k токенов) до $\le$ 19.5 КБ (~4.8k токенов) — экономия более 55%.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `.agents/skills/docs-as-code/SKILL.md` — трансформация из монолита 13.8 КБ в легкий роутер < 2 КБ.
* `[MODIFY]` `.agents/skills/kb-plan/SKILL.md` — сжатие frontmatter, перевод в императивный формат (High-SNR прототип).
* `[MODIFY]` `.agents/skills/kb-task/SKILL.md` — сжатие frontmatter, лаконичные шаги спецификации.
* `[MODIFY]` `.agents/skills/kb-implement/SKILL.md` — сжатие frontmatter, устранение воды при сохранении ветвления Trunk/Branch.
* `[MODIFY]` `.agents/skills/kb-complete/SKILL.md` — сжатие frontmatter, лаконичный чеклист завершения задачи и подсказка релиза.
* `[MODIFY]` `.agents/skills/kb-release/SKILL.md` — сжатие frontmatter, четкие императивные шаги Dual-Mode релиза.
* `[MODIFY]` `.agents/skills/kb-bug/SKILL.md` — сжатие frontmatter, фокус на правиле Regression-First и RCA.
* `[MODIFY]` `.agents/skills/kb-adr/SKILL.md` — сжатие frontmatter, четкий фокус на отклоненных альтернативах.
* `[MODIFY]` `.agents/skills/kb-research/SKILL.md` — сжатие frontmatter, процедура проведения стресс-тестов и замеров.
* `[MODIFY]` `.agents/skills/kb-init/SKILL.md` — сжатие frontmatter, шаги начальной разметки базы знаний.
* `[MODIFY]` `.agents/skills/kb-lint/SKILL.md` — сжатие frontmatter, процедура аудита ссылок и frontmatter.
* `[MODIFY]` `.agents/skills/kb-onboard/SKILL.md` — сжатие frontmatter, компактная навигационная карточка онбординга.

---

## 3. Детали технической реализации

### 3.1. Канонические микро-описания в YAML frontmatter (Micro-Descriptions)

В каждом `SKILL.md` поле `description` заменяется на эталонную строку:

```yaml
# docs-as-code
description: "Docs-as-Code hub: workspace rules, 3-mode workflow, and artifact standards."

# kb-plan
description: "Mode 1: Conceptual analysis, RFC, and PLAN-XXX creation. Prohibits code changes."

# kb-task
description: "Mode 2: Engineering specification TASK-XXX with file contracts and DoD. Prohibits code changes."

# kb-implement
description: "Mode 3: Implement code strictly adhering to TASK-XXX spec with automated verification."

# kb-complete
description: "Mode 3: Finalize TASK-XXX, update Kanban/Roadmap/Devlog, run kb_lint, and git commit."

# kb-release
description: "Release cut: pre-flight checks, dist/ build hook, SHA-256, RELEASE notes, git tag."

# kb-bug
description: "Record defect BUG-XXX with Root Cause Analysis (RCA) and Regression-First TDD test."

# kb-adr
description: "Record Architecture Decision Record ADR-XXXX, capturing context, trade-offs, and rejected options."

# kb-research
description: "Record platform research note RESEARCH-XXX with stress tests, benchmarks, and trade-off matrix."

# kb-init
description: "Initialize Docs-as-Code structure, 13 templates, Obsidian graph, and core tracking files."

# kb-lint
description: "Audit knowledge base integrity: scan wikilinks, broken targets, and YAML frontmatter."

# kb-onboard
description: "Display developer onboarding guide, 3-mode workflow cheatsheet, and quick start."
```

### 3.2. Архитектура легкого роутера `docs-as-code/SKILL.md`

Вместо дублирования 350 строк документации роутер строится по принципу Progressive Disclosure:
* **Инварианты харнесса:** ссылки на `AGENTS.md` и канон 3 режимов (Mode 1: `/kb-plan`, Mode 2: `/kb-task`, Mode 3: `/kb-implement` + `/kb-complete`).
* **Таблица роутинга команд:** соответствие пользовательских интентов специализированным скиллам.
* **Структура `docs/`:** лаконичный индекс каталогов (`00_Templates` .. `05_Testing`).
* Объем файла: $\le$ 2 000 байт (сокращение на 85%).

### 3.3. Унифицированная структура специализированных скиллов (`SKILL.md`)

Каждый скилл следует жесткому трехчастному шаблону:
1. **Header & Context:** название, триггеры вызова (`/kb-<command>`).
2. **Constraints:** жесткие императивные предикаты (`CONSTRAINT: READ-ONLY`, `CONSTRAINT: Regression-First`).
3. **Procedure:** нумерованный алгоритм из 4–6 шагов без риторических повторений и эмоциональных вводных.

---

## 4. План верификации (Verification Plan)

### Автоматическая проверка:
- [x] Запуск скрипта линтинга базы знаний: `python scripts/kb_lint.py --path docs` (код завершения 0).
- [x] Проверка суммарного размера каталога `.agents/skills/`:
  ```powershell
  (Get-ChildItem -Path .agents/skills -Recurse -Filter *.md | Measure-Object -Property Length -Sum).Sum
  ```
  *Критерий:* суммарный объем $\le$ 20 000 байт (было 42 445 байт, результат: 18 728 байт).
- [x] Проверка размера `docs-as-code/SKILL.md`:
  *Критерий:* $\le$ 2 500 байт (было 13 775 байт, результат: 2 274 байта).

### Инспекция метаданных реестра:
- [x] Каждый скилл содержит валидный YAML frontmatter с `name` и лаконичным `description` ($\le$ 15 слов).

---

## 5. Критерии готовности (Definition of Done)

- [x] Все 12 скиллов переведены на микро-описания и High-SNR формат.
- [x] Скилл `docs-as-code/SKILL.md` рефакторен в легкий роутер.
- [x] Отсутствуют эмоциональные эпитеты, риторика и дублирование правил из `AGENTS.md`.
- [x] Суммарный объем скиллов сокращен более чем на 50% (-55.9%).
- [x] Проверка `python scripts/kb_lint.py --path docs` проходит без ошибок.
