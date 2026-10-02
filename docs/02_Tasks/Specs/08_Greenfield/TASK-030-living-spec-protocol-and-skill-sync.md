---
id: TASK-030
title: "Протокол Living Spec и синхронизация документации в скиллах kb-research, kb-complete, kb-release и AGENTS.md"
status: planned
type: task
phase: 8
component:
  - skills
  - agents
  - living-spec
parent_plan: "[[../../Plans/PLAN-008-greenfield-idea-first-and-living-spec|PLAN-008]]"
created: 2026-10-02
updated: 2026-10-02
tags:
  - task/spec
  - phase8
  - component/skills
  - component/agents
  - living-spec
  - documentation-drift
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-030 — Протокол Living Spec и синхронизация документации

> **ID:** TASK-030  
> **Статус:** К реализации (Режим 2)  
> **Теги:** #task/spec #phase8 #component/skills #component/agents #living-spec #documentation-drift  
> **Родительский план:** [[../../Plans/PLAN-008-greenfield-idea-first-and-living-spec|PLAN-008]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-009-greenfield-initialization-and-living-spec-drift|RESEARCH-009]], [[../../../03_Decisions_ADR/ADR-0014-greenfield-idea-first-initialization-and-living-spec-protocol|ADR-0014]], [[../../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Внедрить **Инвариант Живой Спецификации (Living Spec Invariant)** во все уровни агентного цикла разработки для предотвращения деградации и устаревания документации (Documentation Drift / Rotten Spec) согласно [[../../../03_Decisions_ADR/ADR-0014-greenfield-idea-first-initialization-and-living-spec-protocol|ADR-0014]]:
1. **Кристаллизация спецификации в `kb-research` (Режим 0):** Добавить процедуру перевода `SPEC.md` из состояния `status: discovery` в `status: active` при завершении первичного исследования выбора стека (`RESEARCH-001` + `ADR-0001`), с заполнением фактических команд сборки, тестирования и архитектурных слоев в `SPEC.md` и `README.md`.
2. **Синхронизационный шаг в `kb-complete` (Режим 3):** Добавить в завершающий чеклист задачи проверку необходимости синхронизации: если выполненная задача меняет внешние интерфейсы (CLI-флаги, API) или архитектуру системы, агент обязан актуализировать `SPEC.md` и `README.md` в той же сессии.
3. **Префлайт-чеки в `kb-release`:** Добавить в скилл выпуска релиза обязательную проверку актуальности витрины `README.md` (команды запуска, параметры CLI) и мастер-спецификации `SPEC.md` на момент среза версии.
4. **Нормативное закрепление в `AGENTS.md`:** Зафиксировать правило Living Spec Invariant в каноническом руководстве агента.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `.agents/skills/kb-research/SKILL.md` — инструкция по кристаллизации `SPEC.md` при первичном выборе стека.
* `[MODIFY]` `.agents/skills/kb-complete/SKILL.md` — чеклист актуализации `SPEC.md` / `README.md` при изменениях внешних интерфейсов.
* `[MODIFY]` `.agents/skills/kb-release/SKILL.md` — префлайт-проверка актуальности `SPEC.md` и `README.md` перед срезом версии.
* `[MODIFY]` `AGENTS.md` — добавление раздела «Living Spec Invariant & Anti-Drift Protocol».

---

## 3. Детали реализации

### 3.1. Кристаллизация в `.agents/skills/kb-research/SKILL.md`
В раздел завершения исследования Режима 0 добавляется:
```markdown
- **Primary Stack Selection (Greenfield):** If `SPEC.md` is in `status: discovery` and this research selects the foundational stack (ADR-0001):
  1. Update `SPEC.md` status to `status: active`.
  2. Populate Section 2 of `SPEC.md` with chosen tech stack, build/test commands, and architectural layers.
  3. Synchronize `README.md` with factual quickstart commands.
```

### 3.2. Чеклист актуализации в `.agents/skills/kb-complete/SKILL.md`
В процедуру финализации задачи добавляется шаг:
```markdown
3. **Living Spec Sync:** If task modified public CLI flags, APIs, or system architecture:
   - Update `SPEC.md` (contracts, modules, capabilities).
   - Update `README.md` (quick start examples, CLI flags).
```

### 3.3. Префлайт-валидация в `.agents/skills/kb-release/SKILL.md`
В шаг `1. Pre-flight Checks` добавляется:
```markdown
- [ ] Master Spec & README up to date: `README.md` contains actual CLI commands and `SPEC.md` reflects current architecture.
```

### 3.4. Норматив в `AGENTS.md`
Добавляется явный инвариант:
```markdown
### 📜 Living Spec Invariant (No Documentation Drift)
`SPEC.md` is the Master Specification and Single Source of Truth, and `README.md` is the project storefront:
1. **Never Stale:** When a task introduces new CLI arguments, exports, or architectural modules, update `SPEC.md` and `README.md` in that same task session.
2. **Release Gateway:** Releases (`/kb-release`) cannot proceed if `README.md` or `SPEC.md` omit newly introduced public interfaces.
```

---

## 4. План верификации (Verification Plan)

- [ ] Аудит синтаксиса и ссылок: `python scripts/kb_lint.py --path docs` (0 broken links, Exit code 0).
- [ ] Проверка консистентности инструкций: поиск упоминаний `Living Spec` в `.agents/skills/` и `AGENTS.md`.
- [ ] Верификация High-SNR лаконичности: размер измененных скиллов не должен вырасти более чем на 5–10 строк.

---

## 5. Критерии готовности (DoD)

- [ ] Скилл `kb-research` содержит логику кристаллизации `SPEC.md` из статуса `discovery`.
- [ ] Скилл `kb-complete` содержит пункт синхронизации документации при изменении контрактов.
- [ ] Скилл `kb-release` содержит префлайт-проверку актуальности витрины и спецификации.
- [ ] Правило Living Spec Invariant зафиксировано в `AGENTS.md`.
- [ ] Пройдена проверка целостности `kb_lint.py`.
